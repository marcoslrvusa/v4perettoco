# Deck PDI — RAG Hibrido (BM25 + Vetorial) e GraphRAG para Relacoes

Area: Engenharia de IA

## Slide 1: Resumo Executivo
Upgrade do RAG baseline para hibrido (BM25 + vetorial com RRF) e GraphRAG para relacoes. Entrego o padrao e implementacao.
Similaridade falha em 'qual contrato do cliente X' — Grafos cobrem isso.
## Slide 2: Contexto de Producao
Relacionamento ('cliente->contrato->fatura') ruim.
Termos exatos (CNPJ) nao recuperados por embeddings.
BM25 sozinho perde sinonimos.
## Slide 3: Diagnostico
| Caso | Vetorial | BM25 | Hibrido |
| --- | --- | --- | --- |
| ID exato | ruim | otimo | otimo |
| sinonimo | otimo | ruim | otimo |
| relacao | ruim | ruim | grafo |
## Slide 4: Decisao Arquitetural (ADR)
ADR-042 — Recuperacao Hibrida + Grafo
| Opcao | Pro | Contra | Decisao |
| --- | --- | --- | --- |
| BM25 + vetorial + GraphRAG | cobra todos | complexo | ESCOLHIDA |
> Nota: RRF funde ranks; GraphRAG via traversal.
## Slide 5: Entregas
HYBRID-RAG.md.
hybrid_rag.py.
graph_schema.cypher.
## Slide 6: Validacao
Avaliar em 30 perguntas (10 exatas, 10 sinonimos, 10 relacao).
Comparar hit@5.
Confirmar GraphRAG resolve relacoes.
## Slide 7: Metricas e SLO
| SLO | Alvo |
| --- | --- |
| hit@5 (relacao) | >= 0.9 |
| hit@5 (exato) | >= 0.95 |
## Slide 8: Riscos
| Risco | Mitigacao |
| --- | --- |
| Grafo desatualizado | rebuild incremental |
| RRF ruim | tunar |
## Slide 9: Proximos Passos
RAGAS.
Cache de subgrafos.