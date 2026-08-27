# RAG Hibrido (BM25 + Vetorial) e GraphRAG para Relacoes

Engenharia de IA

## Resumo Executivo

Upgrade do RAG baseline para hibrido (BM25 + vetorial com RRF) e GraphRAG para relacoes. Entrego o padrao e implementacao.

Similaridade falha em 'qual contrato do cliente X' — Grafos cobrem isso.

## Contexto de Producao

- Relacionamento ('cliente->contrato->fatura') ruim.

- Termos exatos (CNPJ) nao recuperados por embeddings.

- BM25 sozinho perde sinonimos.

## Diagnostico

| Caso | Vetorial | BM25 | Hibrido |

| --- | --- | --- | --- |

| ID exato | ruim | otimo | otimo |

| sinonimo | otimo | ruim | otimo |

| relacao | ruim | ruim | grafo |

## Decisao Arquitetural (ADR)

ADR-042 — Recuperacao Hibrida + Grafo

| Opcao | Pro | Contra | Decisao |

| --- | --- | --- | --- |

| BM25 + vetorial + GraphRAG | cobra todos | complexo | ESCOLHIDA |

> **Nota:** RRF funde ranks; GraphRAG via traversal.

## Entregas

- HYBRID-RAG.md.

- hybrid_rag.py.

- graph_schema.cypher.

## Validacao

1. Avaliar em 30 perguntas (10 exatas, 10 sinonimos, 10 relacao).

2. Comparar hit@5.

3. Confirmar GraphRAG resolve relacoes.

## Metricas e SLO

| SLO | Alvo |

| --- | --- |

| hit@5 (relacao) | >= 0.9 |

| hit@5 (exato) | >= 0.95 |

## Riscos

| Risco | Mitigacao |

| --- | --- |

| Grafo desatualizado | rebuild incremental |

| RRF ruim | tunar |

## Proximos Passos

- RAGAS.

- Cache de subgrafos.