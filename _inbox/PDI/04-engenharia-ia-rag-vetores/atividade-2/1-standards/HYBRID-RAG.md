# RAG Híbrido + GraphRAG

| Sinal | Melhor para |
|-------|-------------|
| BM25 | termos exatos (IDs, CNPJ) |
| Vetorial | sinônimos, semântica |
| Grafos | relações |

## Fusão (RRF)
score_final = sum(1 / (k + rank_i))  # k=60

## GraphRAG
`MATCH (c:Cliente {id:$x})-[:TEM]->(ct)-[:GERA]->(f:Fatura)`
