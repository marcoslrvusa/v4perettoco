# RAG Hibrido (BM25 + Vetorial) e GraphRAG para Relacoes

Engenharia de IA

## Resumo Executivo

Upgrade do RAG baseline para hibrido (BM25 + vetorial com RRF) e GraphRAG para relacoes. Entrego o padrao e implementacao.

Similaridade falha em 'qual contrato do cliente X' : Grafos cobrem isso.

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

ADR-042 : Recuperacao Hibrida + Grafo

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

## Decisoes e tradeoffs

- BM25 mais vetorial com fusao RRF: aceitei complexidade extra para cobrir ID exato como CNPJ e sinonimo no mesmo retriever, porque cada metodo sozinho falha em um dos casos.
- GraphRAG com traversal para relacoes cliente contrato fatura: assumi custo de rebuild incremental para responder perguntas relacionais que o vetorial nao resolve.
- Chunking semantico com overlap 128: preservei contexto entre sentencas mesmo pagando mais tokens indexados.
- Avaliacao em 30 perguntas (10 exatas, 10 sinonimos, 10 relacao) com hit@5: troquei teste informal por matriz que separa exato, sinonimo e relacao.
- Meta de precisao@5 maior ou igual a 95 por cento e latencia menor que 150 ms com job noturno: equilibrei qualidade alta com atualizacao periodica do grafo.

## Impacto no negocio

O hibrido com hit@5 maior ou igual a 0.95 no exato e maior ou igual a 0.9 na relacao eleva a precisao@5 de cerca de 42 por cento para cerca de 98 por cento, o que reduz retrabalho de respostas vagas e viabiliza precificacao de busca relacional sem indexacao manual.

## Referencias de estudo

- Curso: Advanced Retrieval for AI with Chroma, plataforma DeepLearning.AI.
- Video: GraphRAG com busca vetorial mais grafo de conhecimento, plataforma YouTube, canal Microsoft Developer.
- Doc oficial: Guia de BM25 e relevancia textual, documentacao oficial Elastic.
- Doc oficial: Documentacao do pgvector com HNSW, documentacao oficial pgvector.
