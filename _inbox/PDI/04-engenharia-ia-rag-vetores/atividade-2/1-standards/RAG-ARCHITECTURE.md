# Arquitetura RAG Híbrido + GraphRAG (pgvector)

## Escopo e não-escopo

**Escopo deste standard:** como indexar, combinar e servir três caminhos de
recuperação no mesmo endpoint, com uma única tabela de verdade por trecho, um
único lote de ingestão e um único critério de aceite. Vale para qualquer
consulta que precise de texto relevante e de relação entre entidades.

**Não-escopo:** treino ou fine-tuning de modelo, geração de resposta (a camada
de LLM consome o contexto, ela não define o retriever), e escolha de fornecedor
de embedding. Também não entra aqui multimodal nem busca por imagem.

## Termos

| Termo | Definição operacional |
| --- | --- |
| chunk (trecho) | unidade de indexação, janela de texto com overlap |
| BM25 | ranqueador estatístico por termos, aqui via `tsvector` |
| embedding | vetor de dimensão fixa que representa o significado do trecho |
| RRF | fusão de rankings pelo inverso do posto, sem comparar escores brutos |
| traversal | caminhada de arestas entre entidades do grafo |
| conjunto-ouro | perguntas anotadas com resposta e trechos relevantes |
| hit@5 | fração de perguntas cujo primeiro relevante aparece nos 5 primeiros |
| p95 | valor no qual 95 por cento das amostras ficam abaixo dele |

## Híbrido

- Vetorial: `pgvector` HNSW, cosine.
- Lexical: `tsvector` (BM25-like) via `websearch_to_tsquery`.
- Fusão: RRF (Reciprocal Rank Fusion) dos dois rankings.

Por que os dois e não um: embedding mede proximidade de significado e não mede
igualdade de cadeia de caracteres. Um CNPJ tem significado quase nulo para o
modelo e valor absoluto para o usuário. Já o lexical não sabe que adiantamento e
antecipação são a mesma coisa na gíria da empresa. A fusão existe porque as duas
falhas são estruturais, não acidentais.

### Esquema mínimo (SQL)

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE docs (
  id bigserial PRIMARY KEY,
  content text,
  tsv tsvector GENERATED ALWAYS AS (to_tsvector('portuguese', content)) STORED,
  embedding vector(1536)
);

CREATE INDEX ON docs USING hnsw (embedding vector_cosine_ops);
CREATE INDEX ON docs USING gin (tsv);
```

Duas observações que a revisão sempre pergunta. A coluna `tsv` é gerada e
armazenada, então o custo de escrita é pagou uma vez e o de leitura é zero. O
índice GIN sobre `tsv` é o que faz a busca textual sair da varredura completa;
sem ele, o lexical é rápido só em base pequena e vira gargalo na produção.

### Consulta híbrida (SQL)

```sql
SELECT id, content,
  (0.7 * (1 - (embedding <=> :q))) +
  (0.3 * ts_rank(tsv, websearch_to_tsquery(:q))) AS score
FROM docs ORDER BY score DESC LIMIT 10;
```

Essa forma linear ponderada é o caminho simples, útil como baseline e em
homologação. Ela tem uma limitação que precisa estar explícita: ela soma duas
escalas diferentes. `1 - distância` vive em 0-1 e `ts_rank` cresce sem teto
útil, então o peso 0,7/0,3 é calibrado empiricalmente e quebra quando a
distribuição da coleção muda muito. Em produção, o padrão canônico deste
standard é fusionar por **rank**, que é insensível à escala:

```sql
WITH lex AS (
  SELECT id, ROW_NUMBER() OVER (ORDER BY ts_rank(tsv, websearch_to_tsquery(:q)) DESC) AS r
  FROM docs WHERE tsv @@ websearch_to_tsquery(:q)
  LIMIT 50
),
vec AS (
  SELECT id, ROW_NUMBER() OVER (ORDER BY embedding <=> :qv) AS r
  FROM docs
  LIMIT 50
),
fusao AS (
  SELECT id, SUM(1.0 / (60 + r)) AS score FROM lex GROUP BY id
  UNION ALL
  SELECT id, SUM(1.0 / (60 + r)) AS score FROM vec GROUP BY id
)
SELECT id, SUM(score) AS score
FROM fusao
GROUP BY id
ORDER BY score DESC
LIMIT 10;
```

**Regra canônica.** O ranking final sai de RRF com $k = 60$ sobre as duas
listas, cada lista com no máximo 50 candidatos, e o corte final em 10. Mudança
de $k$ exige reavaliação do conjunto-ouro, nunca ajuste de intuição.

## GraphRAG

- Tabelas `entity`, `relationship` extraídas por LLM.
- Consulta: semantic retrieval + traverse de grafo (CTE recursiva).

### Modelo de dados do grafo

```sql
CREATE TABLE entity (
  id bigserial PRIMARY KEY,
  tipo text NOT NULL,          -- Cliente, Contrato, Fatura
  chave_natural text NOT NULL, -- identificador estável, ex.: CNPJ ou número
  nome text,
  doc_id bigint REFERENCES docs(id),
  UNIQUE (tipo, chave_natural)
);

CREATE TABLE relationship (
  id bigserial PRIMARY KEY,
  origem_id bigint NOT NULL REFERENCES entity(id),
  destino_id bigint NOT NULL REFERENCES entity(id),
  tipo text NOT NULL,          -- TEM, GERA, POSSUI
  doc_id bigint REFERENCES docs(id),
  UNIQUE (origem_id, destino_id, tipo)
);

CREATE INDEX ON relationship (origem_id);
CREATE INDEX ON relationship (destino_id);
```

A `UNIQUE (tipo, chave_natural)` é o que impede a clássica duplicação em que a
extração por LLM devolve "Peretto Comércio" e "PERETTO COMERCIO" como duas
entidades. Deduplicar depois é possível, mas custa script de reconciliação;
evitar na escrita custa uma restrição.

### Travessia (CTE recursiva)

```sql
WITH RECURSIVE caminho AS (
  SELECT e.id, e.tipo, e.nome, 0 AS profundidade
  FROM entity e
  WHERE e.tipo = 'Cliente' AND e.chave_natural = :cnpj
  UNION ALL
  SELECT e.id, e.tipo, e.nome, c.profundidade + 1
  FROM caminho c
  JOIN relationship r ON r.origem_id = c.id
  JOIN entity e ON e.id = r.destino_id
  WHERE c.profundidade < 4
)
SELECT c.tipo, c.nome, c.profundidade
FROM caminho c
ORDER BY c.profundidade, c.tipo, c.nome;
```

O `WHERE c.profundidade < 4` não é cosmético. Sem limite, uma malha bem
conectada (centro de custo com dezenas de faturas e contratos) explode
combinatoriamente e a consulta nunca volta. Profundidade 4 cobre
cliente, contrato, fatura e centro de custo, que é a cadeia real do negócio.

Equivalente no grafo nativo, para quem opera Neo4j, é a mesma pergunta:

`MATCH (c:Cliente {id:$x})-[:TEM]->(ct)-[:GERA]->(f:Fatura) RETURN f`

A diferença prática: no Postgres a travessia vive na mesma transação dos
índices, o que simplifica backup e consistência; no Neo4j a expressão é mais
curta e o planejador de consulta costuma ser melhor em grafo denso. O standard
escolhe Postgres porque a base já vive lá e manter dois sistemas de escrita é
risco maior do que ganho sintático.

### Grafo como terceira lista no RRF

A travessia devolve entidades, não trechos. Para entrar na mesma fusão, cada
entidade resolve para os `doc_id` que a citam, e esses documentos recebem rank
na lista de grafo. Assim uma pergunta relacional alimenta os três ranqueadores
com o mesmo tipo de objeto e o RRF continua sendo a única regra de combinação.

**Exemplo numérico:** três listas, `k = 60`, documento que fica em 1º no
lexical, 3º no vetorial e 2º no grafo marca
$1/61 + 1/63 + 1/62 = 0{,}0164 + 0{,}0159 + 0{,}0161 = 0{,}0484$. Um documento
que só existe no lexical em 1º marca $1/61 = 0{,}0164$. A consulta relacional
portanto empurra o documento citado pelo grafo para o topo mesmo competindo com
um forte candidato textual isolado.

## Tabela de decisão

| Se a pergunta... | E o texto... | Então use | Corte inicial |
| --- | --- | --- | --- |
| contém CNPJ, SKU ou número de contrato | tem o identificador literal | lexical primeiro | top-20 |
| usa sinônimo ou gíria interna | não tem a forma canônica | vetorial primeiro | top-40 |
| pede relação entre entidades | exige encadear dois ou mais fatos | grafo + fusão | top-10 |
| é ambígua entre as anteriores | não dá para classificar com segurança | fusão dos três | top-40, rerank para 10 |
| é saudação ou fora de escopo | não pede informação da base | nenhuma, responda direto | 0 |

## Exemplo numérico fechado (latência)

**Exemplo numérico:** p95 medido por etapa em homologação (parâmetros: 50
candidatos por lista, 10 no corte final, embedding de 1536 dimensões).

| Etapa | p95 |
| --- | --- |
| embedding da consulta | 25 ms |
| lexical com GIN | 15 ms |
| vetorial com HNSW | 30 ms |
| travessia de grafo (2 níveis) | 18 ms |
| fusão e deduplicação | 3 ms |
| montagem do contexto | 20 ms |
| **total** | **111 ms** |

Folga contra a meta de 150 ms: 39 ms. Esgotando a folga, o primeiro item a
desligar é o reranking opcional (50 ms), porque ele é o único que pode ser
desligado sem perder cobertura de recall.

## Anti-padrões

O que a revisão reprovaria:

1. **Somar escore bruto de duas fontes sem normalizar.** Viola a regra canônica
   e faz o lexical ou o vetorial dominar por escala.
2. **Avaliar só média de hit@5.** Esconde a classe de pergunta que quebrou.
3. **Indexar sem normalizar o embedding.** Depois a comparação de escore passa a
   mentir e o cache semântico fica inconsistente.
4. **Traçar grafo sem limite de profundidade.** É consulta que não volta em base
   conectada.
5. **Atualizar só um índice.** O sistema passa a responder com duas verdades ao
   mesmo tempo, sem sinal externo.
6. **Reprocessar lote inteiro a cada alteração.** Custo desnecessário; use chave
   de hash por trecho.
7. **Expor o score do RRF como confiança.** Não é probabilidade e não tem
   interpretação percentual.
8. **Trocar `k` do RRF por feeling.** Toda constante de fusão vive presa a uma
   curva de avaliação por categoria.
9. **Confiar na extração de entidades sem chave natural.** Duplicação garantida
   em qualquer reexecução.
10. **Colocar reranking ilimitado no caminho crítico.** P95 estoura e a meta de
    150 ms some.

## Telemetria

| Métrica | Cardinalidade | Alerta |
| --- | --- | --- |
| latência p95 por etapa | etapa, ambiente | acima de 120 ms por 2 etapas |
| hit@5 por categoria | categoria (3 valores) | abaixo de meta na build |
| duração do job noturno | dia | falha ou acima de 30 min |
| contagem de `entity` e `relationship` | dia | queda de mais de 2 por cento |
| taxa de hit de cache textual e semântico | nível (2 valores) | abaixo de 20 por cento por 24 h |
| custo por consulta | dia | acima de 0,004 R$ |
| fallback de grafo acionado | motivo | acima de 5 por cento das consultas |

Cardinalidade deliberadamente baixa. Métrica por `doc_id` ou por consulta
individual explode o custo de armazenamento e não cabe em alerta: isso vai para
log estruturado, não para série temporal.

## Plano de teste

| Caso | Entrada | Esperado | Critério de falha |
| --- | --- | --- | --- |
| identificador exato | CNPJ com pontuação | lexical traz o documento exato | documento ausente dos 5 primeiros |
| sinônimo | termo interno sem a forma canônica | vetorial traz o documento | hit@5 abaixo de 0,9 |
| relação multi-hop | cliente + pedido de contrato | grafo devolve a cadeia | nenhum caminho ou caminho com mais de 4 níveis |
| consulta vazia | string vazia ou só espaço | retorno vazio, sem exceção | erro 500 |
| Unicode acentuado | "operaçãoçãoção" | normalização correta, sem erro de encoding | resposta errada ou exceção |
| base vazia | nenhuma linha em `docs` | lista vazia e métrica de latência registrada | crash por divisão por zero |
| reexecução do lote | mesmo lote duas vezes | contagem de linhas idêntica | crescimento de linhas |
| corte de contexto | resposta longa esperada | truncamento respeitando orçamento | prompt acima do limite do modelo |

Critério de aceite do standard como um todo: os oito casos acima verdes em
automação, hit@5 por categoria na meta e p95 abaixo de 150 ms em duas janelas de
24 horas consecutivas.

## Checklist de adesão

1. Escopo e não-escopo do standard entendidos antes de implementar.
2. `tsv` gerado e indexado com GIN, não calculado em consulta.
3. Índice HNSW criado com `vector_cosine_ops` e distância coerente com a
   normalização usada.
4. Embeddings normalizados na escrita e na consulta.
5. Fusão por RRF com $k = 60$ documentado, não por soma de escore bruto.
6. Candidatos por lista limitados (50) antes da fusão.
7. Grafo com chave natural única e profundidade de travessia limitada.
8. Grafo e índices atualizados no mesmo lote de ingestão.
9. Conjunto-ouro de 30 perguntas versionado e rodado em toda mudança relevante.
10. Relatório por categoria de pergunta, sem média agregada isolada.
11. p95 medido por etapa, com a etapa mais cara identificada.
12. Reranking desligável por feature flag.
13. Cache com TTL, versão de modelo e threshold documentados.
14. Rollback por snapshot de índice testado em homologação.
15. Custo por consulta calculado com parâmetros declarados.

## Versionamento e rollout

Indexação é imutável por versão. Cada lote de ingestão publica um snapshot novo,
e a aplicação aponta para um snapshot por referência, nunca por conteúdo
inline. Trocar de versão é trocar uma referência e invalidar o cache.

1. Publicar snapshot novo em paralelo ao atual.
2. Rodar o conjunto-ouro contra o snapshot novo, sem afetar a produção.
3. Se os critérios de aceite passarem, promover a referência.
4. Manter o snapshot anterior por 7 dias para rollback imediato.
5. Invalidar os três níveis de cache na troca, porque a chave de contexto
   versiona por snapshot.

Rollback consiste em apontar de volta e invalidar cache. Meta de tempo: 10
minutos (meta). Reindexar nunca é rollback, é reconstituição, e leva horas.

Mudança de modelo de embedding exige reindexação completa, não parcial: a
distância cosseno só é comparável dentro de um mesmo espaço vetorial. Por isso
a troca de modelo é a única mudança que não entra por feature flag, e sim por
janela de manutenção comunicada, com dois snapshots convivendo durante a troca.

## Referências

- Curso: Advanced Retrieval for AI with Chroma, plataforma DeepLearning.AI.
- Vídeo: GraphRAG com busca vetorial mais grafo de conhecimento, plataforma YouTube, canal Microsoft Developer.
- Doc oficial: Guia de BM25 e relevância textual, documentação oficial Elastic.
- Doc oficial: Documentação do pgvector com HNSW, documentação oficial pgvector.
