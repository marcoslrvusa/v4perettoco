# Pipelines de Dados para IA (NVIDIA DLI)

## Estágios
1. **Ingest:** conectores (Docs, CRM, SQL) → fila.
2. **Chunk:** split semântico (512-1024 tokens, overlap 10%).
3. **Embed:** batch assíncrono (evita estrangulamento de API).
4. **Store:** pgvector com índice HNSW.
5. **Serve:** retrieval + rerank.

## Boas práticas
- Desacoplar ingest de serve (fila).
- Versionar dataset de embeddings (reembed em mudança de modelo).

## Escopo e não-escopo

**Escopo deste standard:** o caminho de dados que vai do documento bruto até o vetor disponível para consulta, incluindo fatiamento, geração de embeddings em lote, gravação indexada, versionamento e reindexação. Inclui também o contrato de qualidade entre quem alimenta e quem consome: o consumidor só precisa saber que existe `chunk_id`, `doc_id`, modelo e hash.

**Não-escopo:** o gerador de resposta (prompt, modelo, temperatura), a interface do usuário e a política de guardrails de saída. Esses temas vivem no standard de avaliação e segurança. Aqui o objetivo é único: manter um índice vetorial íntegro, versionado e barato de reprocessar.

## Termos

| Termo | Definição operacional |
| --- | --- |
| Chunk | unidade de indexação, fatia de documento com tamanho fixo em tokens e sobreposição declarada |
| Embedding | vetor de dimensão fixa que representa a semântica de um chunk em um espaço comparável |
| Reembed | regeneração de todos os vetores por causa de troca de modelo ou de política de chunking |
| Lote (batch) | conjunto de textos enviados juntos à API de embedding em uma única chamada |
| Idempotência por chave | gravar duas vezes o mesmo `(doc_id, hash, modelo)` produz exatamente um registro |
| Recall@k | fração das evidências corretas que aparecem nas `k` primeiras posições |
| HNSW | índice de grafo de vizinhos aproximado, usado para evitar busca por força bruta |

## Regra canônica

O pipeline é correto quando toda transformação é **determinística e reversível até a fonte**:

$$\text{chunk} = f(\text{texto}, S, O) \quad \text{com} \quad f \text{ determinística}$$

$$\text{índice} = \{\, (\text{doc\_id}, \text{hash}, \text{modelo}, \text{vetor}) \,\}$$

Determinística significa: mesmo texto, mesmo `S`, mesmo `O`, mesmo modelo, gera exatamente os mesmos chunks e os mesmos vetores. É essa propriedade que permite comparar duas versões do índice, detectar divergência com hash e reprocessar só o que mudou.

Reversível até a fonte significa: a partir de um `chunk_id` é sempre possível voltar ao `doc_id`, ao hash do texto original e à versão do modelo que gerou o vetor. Sem esse caminho de volta, a citação de uma resposta é apenas um identificador decorativo.

**Fórmula de volume do índice:**

$$|\text{chunks}| = \left\lceil \frac{N}{S - O} \right\rceil$$

sendo $N$ o total de tokens do corpus, $S$ o tamanho do chunk e $O$ o overlap.

**Exemplo numérico:** corpus de 3.000.000 de tokens, $S = 512$, $O = 64$. Passo entre chunks: $512 - 64 = 448$ tokens. Total de chunks: $3.000.000 / 448 \approx 6.696$ vetores. Com $O = 0$: $3.000.000 / 512 \approx 5.859$ vetores. A diferença de 837 vetores é o preço do overlap, e ela é paga uma vez por indexação, nunca por consulta.

## Tabela de decisão

| Se X | e Y | então Z |
| --- | --- | --- |
| o corpus mudou menos de 1 por cento | o modelo de embedding é o mesmo | reindexa só os documentos com hash alterado |
| o modelo de embedding mudou | qualquer que seja o corpus | reindexa tudo e mantém a versão antiga até validar recall@5 |
| a política de chunking mudou | o modelo é o mesmo | reindexa tudo, porque `chunk_id` muda e as citações antigas quebram |
| a fila de ingestão acumula atraso maior que o SLO | o caminho de consulta está saudável | não bloqueia a consulta; drena o backlog em lote paralelo |
| o lote de embedding retorna erro parcial | alguns textos foram gravados | reenvia apenas os textos sem vetor, pela chave de idempotência |
| o índice cresce além do orçamento | a latência p95 segue dentro do SLO | não otimiza agora; registra dívida com número e data |
| o recall@5 cai após qualquer mudança | qualquer outra coisa parece normal | reverte a mudança, porque busca é a função do pipeline |

## Chunking: parâmetros e cuidados

O padrão da atividade é `S = 512` tokens e `O = 64` tokens, o que dá 12,5 por cento de cobertura dupla. O corte deve respeitar fronteira de sentido sempre que possível: cortar no meio de uma tabela separa cabeçalho de linha, e cortar no meio de uma lista separa item de critério.

```python
def fatiar(texto: str, tamanho: int = 512, overlap: int = 64) -> list[str]:
    """Fatiia por tokens com sobreposição, preservando a ordem do documento.

    Pré-condição: overlap < tamanho.
    Pós-condição: a concatenação dos chunks cobre todos os tokens do texto.
    """
    if overlap >= tamanho:
        raise ValueError("overlap deve ser menor que o tamanho do chunk")
    tokens = tokenizar(texto)          # contagem em tokens, não em caracteres
    passo = tamanho - overlap
    return [
        " ".join(tokens[i:i + tamanho])
        for i in range(0, len(tokens), passo)
        if i < len(tokens)
    ]
```

Erro clássico: fatiar por caracteres ou por `split()` de palavras quando a API cobra por tokens. O texto tem 512 palavras, mas pode ter bem mais que 512 tokens, e o orçamento estoura no faturamento, não no código.

## Embedding em lote

Enviar um texto por vez transforma a indexação em 6.696 requisições sequenciais no exemplo acima. Em lote, o mesmo trabalho cabe em muito menos chamadas, com paralelismo limitado e backoff respeitado.

```python
import asyncio

async def embedir_lotes(textos: list[str], tamanho_lote: int = 128) -> list[list[float]]:
    """Gera embeddings em lote assíncrono, com limite de concorrência e nova tentativa em erro transitório."""
    semaforo = asyncio.Semaphore(4)   # teto de chamadas simultâneas
    saida: list[list[float]] = []

    async def um_lote(lote: list[str]) -> None:
        async with semaforo:
            for tentativa in range(3):
                try:
                    vetores = await cliente.embed(lote)
                    saida.extend(vetores)
                    return
                except ErroTransitorio:
                    await asyncio.sleep(2 ** tentativa)   # backoff exponencial
            raise ErroPermanente("lote reprovado após 3 tentativas")

    await asyncio.gather(*(um_lote(textos[i:i + tamanho_lote])
                           for i in range(0, len(textos), tamanho_lote)))
    return saida
```

Dois erros que o lote introduz se ninguém tomar cuidado: ordem trocada entre o texto e o vetor, resolvida gravando junto a chave do texto; e lote parcialmente gravado, resolvida pela chave de idempotência `(doc_id, hash, modelo)`.

## Gravação e índice

```sql
CREATE TABLE IF NOT EXISTS chunks (
    chunk_id    bigserial PRIMARY KEY,
    doc_id      text        NOT NULL,
    hash_texto  text        NOT NULL,
    modelo      text        NOT NULL,
    ordem       int         NOT NULL,
    conteudo    text        NOT NULL,
    embedding   vector(1536) NOT NULL,
    UNIQUE (doc_id, hash_texto, modelo, ordem)
);

CREATE INDEX IF NOT EXISTS idx_chunks_hnsw
    ON chunks USING hnsw (embedding vector_cosine_ops);

-- Busca com normalização garantida e corte por similaridade
SELECT chunk_id, doc_id, conteudo,
       1 - (embedding <=> :consulta) AS score
FROM chunks
WHERE modelo = :modelo_atual
ORDER BY embedding <=> :consulta
LIMIT 20;
```

A expressão `embedding <=> :consulta` é a distância de cosseno do índice. Como os vetores são normalizados na escrita, a distância e a similaridade são complementares (`score = 1 - distancia`), e o threshold 0.82 passa a ser interpretável sem surpresa.

O `UNIQUE (doc_id, hash_texto, modelo, ordem)` é o que transforma a reindexação em operação segura: reexecutar o mesmo job não duplica registro, porque o banco recusa a segunda escrita da mesma chave.

## Telemetria

| Métrica | Cardinalidade | Alerta |
| --- | --- | --- |
| Idade do mensageiro mais antigo da fila | 1 por fila | acima do SLO de ingestão (meta) |
| Chunks gravados por modelo | baixa, por modelo | queda a zero por 15 min (meta) |
| Taxa de erro do lote de embedding | por faixa de tentativa | acima de 1 por cento (meta) |
| Latência p95 da busca + rerank | por etapa | acima de 800 ms (meta) |
| Recall@5 do lote de validação | por build | queda em relação ao build anterior |
| Tokens indexados por dia | 1 por dia | crescimento sem mudança de escopo declarada |

Cardinalidade alta é proibida aqui: nunca etiquetar métrica com `doc_id` ou com a consulta do usuário, porque isso transforma a base de métricas em custo e em vazamento de conteúdo.

## Plano de teste

| Caso | Entrada esperada | Critério de aceite |
| --- | --- | --- |
| Texto vazio | nenhum chunk gerado | lista vazia, sem erro, sem vetor gravado |
| Texto com 10 tokens | 1 chunk | cobre o texto inteiro |
| Texto com 512 tokens exatos | 1 chunk | nenhum chunk duplicado |
| Texto com 513 tokens | 2 chunks | segundo chunk começa em 448, com overlap real |
| Texto com acentuação e emoji | chunks preservados | nenhuma perda de caractere na round-trip |
| Reprocessar o mesmo documento | 0 escritas novas | contagem do índice inalterada |
| Trocar o modelo | índice da versão antiga permanece | busca por modelo errado devolve 0 linhas |
| Lote com erro transitório | nova tentativa automática | lote completo após backoff, sem perda |
| Corpus de 1.000 documentos | número de chunks igual à fórmula | desvio zero em relação a $ \lceil N / (S - O) \rceil $ |

## Anti-padrões

O que o sênior reprovaria em review:

- Fatiar por caracteres com limite que se chama "512 tokens": a unidade está errada e o custo real só aparece na fatura.
- Reindexar o corpus inteiro para corrigir um documento: desperdiça embedding e risco, quando a chave de idempotência já isola o que mudou.
- Gravar vetor sem a versão do modelo: torna impossível saber qual espaço está em uso em cada linha.
- Enviar um texto por chamada em produção: transforma indexação em fila infinita e latência evitável.
- Deletar o índice antigo antes de validar o novo: derruba a capacidade de rollback no momento em que ele é mais necessário.
- Medir sucesso por "job terminou sem exceção": job que terminou com 30 por cento de lote falho não é sucesso, é falha silenciosa.
- Usar a mesma tabela sem filtro de modelo depois de uma troca de modelo: busca mistura espaços e devolve coincidência.

## Critérios de aceite da entrega

1. Pipeline roda do zero em corpus de teste e reproduz o mesmo número de chunks previsto pela fórmula.
2. Reprocessamento do mesmo corpus não altera a contagem do índice.
3. Troca de modelo mantém as duas versões consultáveis por filtro explícito.
4. Recall@5 medido no lote de validação não cai em relação ao build anterior.
5. Latência p95 da etapa de busca medida separadamente do rerank.
6. Runbook com checagem de fila, mitigação de backlog e rollback documentado.

## Checklist de adesão

1. Tamanho de chunk declarado em tokens e aplicado de forma uniforme.
2. Overlap menor que o tamanho e justificado em documento.
3. Contagem de tokens feita com o mesmo tokenizador que cobra a API.
4. Normalização aplicada na escrita de todo vetor.
5. Chave de idempotência `(doc_id, hash, modelo, ordem)` existente no banco.
6. Versão do modelo gravada em cada vetor.
7. Lote assíncrono com teto de concorrência e backoff.
8. Índice HNSW criado com operador de distância coerente com a métrica usada na avaliação.
9. Rollback do índice antigo preservado até a validação do novo.
10. Métricas de fila, erro de lote, latência por etapa e recall@5 no painel.
11. Teste de borda: vazio, mínimo, limite de um token, acentuação e reexecução.
12. Versionamento do dataset de embeddings registrado em changelog.
13. Custo de reindexação estimado antes de trocar política de chunking ou modelo.
14. Nenhuma métrica com cardinalidade por documento ou por consulta.

## Referências

- Curso: Building RAG Agents with LLMs, plataforma NVIDIA Deep Learning Institute (DLI).
- Doc oficial: Documentação do pgvector com índice HNSW, documentação oficial pgvector.
- Doc oficial: Guia de embeddings text-embedding-3-small, documentação oficial OpenAI.
