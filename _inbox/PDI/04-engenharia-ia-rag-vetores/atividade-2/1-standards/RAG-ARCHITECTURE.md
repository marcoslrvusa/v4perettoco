# Arquitetura RAG Híbrido + GraphRAG (pgvector)

## Híbrido
- Vetorial: `pgvector` HNSW, cosine.
- Lexical: `tsvector` (BM25-like) via `websearch_to_tsquery`.
- Fusão: RRF (Reciprocal Rank Fusion) dos dois rankings.

## GraphRAG
- Tabelas `entity`, `relationship` extraídas por LLM.
- Consulta: semantic retrieval + traverse de grafo (CTE recursiva).

## Query híbrida (SQL)
```sql
SELECT id, content,
  (0.7 * (1 - (embedding <=> :q))) +
  (0.3 * ts_rank(tsv, websearch_to_tsquery(:q))) AS score
FROM docs ORDER BY score DESC LIMIT 10;
```
