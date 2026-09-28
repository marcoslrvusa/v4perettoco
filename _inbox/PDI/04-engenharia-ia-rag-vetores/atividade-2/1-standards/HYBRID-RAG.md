# RAG Híbrido + GraphRAG

## Papel de cada sinal

| Sinal | Melhor para |
|-------|-------------|
| BM25 | termos exatos (IDs, CNPJ) |
| Vetorial | sinônimos, semântica |
| Grafos | relações |

Leitura prática da tabela: o sinal não é "melhor" ou "pior" no geral, ele é
melhor para um **tipo de pergunta**. Por isso a decisão de projeto não é escolher
um sinal, é decidir quem entra em quais situações e como os três são combinados
quando entram juntos.

## Fusão (RRF)

score_final = sum(1 / (k + rank_i))  # k=60

Por que só a ordem entra na conta: escore do BM25 e escore de similaridade
cosseno não vivem na mesma escala. O BM25 cresce com IDF e frequência, o cosseno
está contido em -1 a 1. Somar os dois brutos é somar metro com quilo. O RRF
resolve isso ignorando magnitude e olhando posição, o que também torna a fusão
robusta a mudança de modelo de embedding: se o modelo novo reordena a lista, a
fusão continua sensível à qualidade relativa, não ao número absoluto.

### Implementação de referência

```python
def rrf(ranks, k=60):
    """Combina várias listas ordenadas por inverso do posto."""
    s = {}
    for r in ranks:
        for i, doc in enumerate(r):
            s[doc] = s.get(doc, 0) + 1 / (k + i + 1)
    return sorted(s, key=s.get, reverse=True)
```

Três detalhes de quem já escreveu isso errado uma vez:

1. O índice começa em 0 no `enumerate`, então `k + i + 1` é obrigatório para o
   primeiro lugar valer `1 / (k + 1)` e não `1 / k`.
2. Documento ausente de uma lista não recebe zero implícito, ele simplesmente
   não soma nada. Isso é correto: ausência é ausência, não penalidade.
3. O retorno é só a ordem. Se o consumidor precisa de score, ele recebe o soma
   das frações, e esse número **não** é probabilidade.

### Curva do parâmetro k

**Exemplo numérico:** diferença entre um doc em 1º e outro em 2º em uma única
lista, para três valores de `k`. Com `k = 1`: `1/2 - 1/3 = 0,1667`. Com
`k = 60`: `1/61 - 1/62 = 0,0003`. Com `k = 1000`: `1/1001 - 1/1002 = 0,000001`.
A leitura é direta: `k` pequeno faz a primeira posição valer demais e apaga as
outras listas; `k` grande achata tudo e a fusão vira média. Faixa útil testada:
20-100, padrão 60, e qualquer mudança reavalia o conjunto-ouro por categoria.

### Listas de entrada

- Tamanho por lista: 50 candidatos.
- Corte após a fusão: 10 trechos, depois deduplicados por `doc_id`.
- A lista de grafo é construída a partir dos `doc_id` das entidades alcançadas,
  para que os três ranqueadores devolvam o mesmo tipo de objeto.

## GraphRAG

`MATCH (c:Cliente {id:$x})-[:TEM]->(ct)-[:GERA]->(f:Fatura) RETURN f`

Essa consulta responde uma pergunta que nenhum trecho de texto resolve sozinho:
ela não pergunta o que está escrito, pergunta **o que está ligado ao quê**. O
retriever textual encontra pedaços sobre cliente, pedaços sobre contrato e
pedaços sobre fatura, mas não encontra a cadeia.

### Quando o grafo entra e quando ele é desperdício

| Pergunta | Caminho | Grafo entra? |
| --- | --- | --- |
| qual o CNPJ do cliente X | lexical | não |
| como antecipar a fatura | vetorial | não |
| quais faturas o contrato K-01 gerou | grafo | sim |
| quem aprova acima de 50 mil | grafo (2 níveis) | sim |
| resuma o contrato | nenhum, é geração | não |

Regra de bolso: se a resposta é uma **lista de coisas conectadas**, o grafo
entra; se a resposta é um **trecho que explica**, o grafo é peso morto.

### Escrita incremental

```sql
INSERT INTO entity (tipo, chave_natural, nome, doc_id)
VALUES (:tipo, :chave, :nome, :doc_id)
ON CONFLICT (tipo, chave_natural)
DO UPDATE SET nome = EXCLUDED.nome, doc_id = EXCLUDED.doc_id;
```

A escrita é idempotente por chave natural. Repetir o job do dia não duplica nó
nem aresta, e isso é o que torna seguro reexecutar sem investigar antes.

### Limite de profundidade

**Exemplo numérico:** grafo com 4 entidades por nó e travessia ilimitada gera
$4^5 = 1024$ caminhos na profundidade 5, e $4^8 = 65.536$ na profundidade 8.
Limitando a 4 níveis, o teto é $4^4 = 256$ expansões por origem, que cabe em
milissegundos e cobre a cadeia cliente, contrato, fatura e centro de custo.

## Query híbrida (SQL)

```sql
SELECT id, content,
  (0.7 * (1 - (embedding <=> :q))) +
  (0.3 * ts_rank(tsv, websearch_to_tsquery(:q))) AS score
FROM docs ORDER BY score DESC LIMIT 10;
```

A versão ponderada acima serve como baseline rápida. O padrão canônico da
atividade é a fusão por rank, descrita em `RAG-ARCHITECTURE.md`, porque ela não
depende de pesos calibrados manualmente.

```sql
WITH lex AS (
  SELECT id, ROW_NUMBER() OVER (ORDER BY ts_rank(tsv, websearch_to_tsquery(:q)) DESC) AS r
  FROM docs WHERE tsv @@ websearch_to_tsquery(:q) LIMIT 50
),
vec AS (
  SELECT id, ROW_NUMBER() OVER (ORDER BY embedding <=> :qv) AS r
  FROM docs LIMIT 50
)
SELECT id, SUM(1.0 / (60 + r)) AS score FROM (
  SELECT id, r FROM lex UNION ALL SELECT id, r FROM vec
) t
GROUP BY id ORDER BY score DESC LIMIT 10;
```

## Qualidade e avaliação

| Métrica | Uso | Meta da atividade |
| --- | --- | --- |
| hit@5 exato | identificador bateu | >= 0,95 |
| hit@5 sinônimo | generalização cobriu | >= 0,9 (meta) |
| hit@5 relação | cadeia respondida | >= 0,9 |
| p95 da consulta | orçamento de latência | < 150 ms |

A avaliação roda em três configurações: só vetorial, só lexical, híbrido. Mesma
janela de tempo, mesmo top-k, mesmo prompt. Sem essa comparação, a frase "o
híbrido funciona" é opinião.

## Anti-padrões

- Somar escore bruto de fontes diferentes com pesos mágicos.
- Deixar o grafo como caminho único para toda pergunta.
- Reexecutar embedding da base inteira sem chave de hash.
- Tirar `k` do RRF de um tutorial sem medir hit@5.
- Expor o score final como "confiança de 83 por cento".
- Trocar o chunking sem reavaliar as 30 perguntas.

## Telemetria

| Métrica | Alerta |
| --- | --- |
| p95 por etapa | acima de 120 ms em duas etapas |
| hit@5 por categoria | abaixo da meta na build |
| duração do job de grafo | falha ou acima de 30 min |
| contagem de `entity` | queda de mais de 2 por cento no dia |
| taxa de hit de cache | abaixo de 20 por cento por 24 h |

## Testes

- CNPJ com pontuação deve aparecer nos 5 primeiros.
- Consulta com sinônimo deve encontrar o documento sem a forma canônica.
- Pergunta relacional deve devolver cadeia com até 4 níveis.
- Base vazia não pode lançar exceção.
- Reexecutar o lote não pode alterar a contagem de linhas.

Critério de aceite: cinco casos verdes, hit@5 por categoria na meta, p95 abaixo
de 150 ms.

## Checklist de adesão

1. Fusão por RRF, nunca por soma de escore bruto.
2. `k` justificado por curva de avaliação.
3. Tamanho de lista documentado (50) e corte final (10).
4. Embeddings normalizados na escrita.
5. `tsv` gerado e coberto por índice GIN.
6. Grafo com chave natural única.
7. Profundidade de travessia limitada a 4.
8. Grafo e índices no mesmo lote de ingestão.
9. Avaliação por categoria, não agregada.
10. Reranking desligável por feature flag.
11. Job noturno idempotente e monitorado.
12. Rollback por snapshot documentado.

## Referências

- Curso: Advanced Retrieval for AI with Chroma, plataforma DeepLearning.AI.
- Vídeo: GraphRAG com busca vetorial mais grafo de conhecimento, plataforma YouTube, canal Microsoft Developer.
- Doc oficial: Guia de BM25 e relevância textual, documentação oficial Elastic.
- Doc oficial: Documentação do pgvector com HNSW, documentação oficial pgvector.
