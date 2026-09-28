# Deck PDI: RAG Híbrido (BM25 + Vetorial) e GraphRAG para Relações

Área: Engenharia de IA

## Slide 1: Resumo Executivo
Upgrade do RAG baseline para híbrido (BM25 + vetorial com RRF) e GraphRAG para relações. Entrego o padrão e implementação.
Similaridade falha em 'qual contrato do cliente X': Grafos cobrem isso.
## Slide 2: Contexto de Produção
Relacionamento ('cliente->contrato->fatura') ruim.
Termos exatos (CNPJ) não recuperados por embeddings.
BM25 sozinho perde sinônimos.
## Slide 3: Diagnóstico
| Caso | Vetorial | BM25 | Híbrido |
| --- | --- | --- | --- |
| ID exato | ruim | ótimo | ótimo |
| sinônimo | ótimo | ruim | ótimo |
| relação | ruim | ruim | grafo |
## Slide 4: Decisão Arquitetural (ADR)
ADR-042: Recuperação Hibrida + Grafo
| Opção | Pro | Contra | Decisão |
| --- | --- | --- | --- |
| BM25 + vetorial + GraphRAG | cobra todos | complexo | ESCOLHIDA |
> Nota: RRF funde ranks; GraphRAG via traversal.
## Slide 5: Entregas
HYBRID-RAG.md.
hybrid_rag.py.
graph_schema.cypher.
## Slide 6: Validação
Avaliar em 30 perguntas (10 exatas, 10 sinônimos, 10 relação).
Comparar hit@5.
Confirmar GraphRAG resolve relações.
## Slide 7: Métricas e SLO
| SLO | Alvo |
| --- | --- |
| hit@5 (relação) | >= 0.9 |
| hit@5 (exato) | >= 0.95 |
## Slide 8: Riscos
| Risco | Mitigação |
| --- | --- |
| Grafo desatualizado | rebuild incremental |
| RRF ruim | tunar |
## Slide 9: Próximos Passos
RAGAS.
Cache de subgrafos.