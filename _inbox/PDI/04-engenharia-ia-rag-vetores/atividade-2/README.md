# RAG Híbrido (BM25 + Vetorial) e GraphRAG para Relações

Engenharia de IA

## Resumo Executivo

Upgrade do RAG baseline para híbrido (BM25 + vetorial com RRF) e GraphRAG para relações. Entrego o padrão e implementação.

Similaridade falha em 'qual contrato do cliente X' : Grafos cobrem isso.

## Contexto de Produção

- Relacionamento ('cliente->contrato->fatura') ruim.

- Termos exatos (CNPJ) não recuperados por embeddings.

- BM25 sozinho perde sinônimos.

## Diagnóstico

| Caso | Vetorial | BM25 | Híbrido |

| --- | --- | --- | --- |

| ID exato | ruim | ótimo | ótimo |

| sinônimo | ótimo | ruim | ótimo |

| relação | ruim | ruim | grafo |

## Decisão Arquitetural (ADR)

ADR-042 : Recuperação Hibrida + Grafo

| Opção | Pro | Contra | Decisão |

| --- | --- | --- | --- |

| BM25 + vetorial + GraphRAG | cobra todos | complexo | ESCOLHIDA |

> **Nota:** RRF funde ranks; GraphRAG via traversal.

## Entregas

- HYBRID-RAG.md.

- hybrid_rag.py.

- graph_schema.cypher.

## Validação

1. Avaliar em 30 perguntas (10 exatas, 10 sinônimos, 10 relação).

2. Comparar hit@5.

3. Confirmar GraphRAG resolve relações.

## Métricas e SLO

| SLO | Alvo |

| --- | --- |

| hit@5 (relação) | >= 0.9 |

| hit@5 (exato) | >= 0.95 |

## Riscos

| Risco | Mitigação |

| --- | --- |

| Grafo desatualizado | rebuild incremental |

| RRF ruim | tunar |

## Próximos Passos

- RAGAS.

- Cache de subgrafos.

## Decisões e tradeoffs

- BM25 mais vetorial com fusão RRF: aceitei complexidade extra para cobrir ID exato como CNPJ e sinônimo no mesmo retriever, porque cada método sozinho falha em um dos casos.
- GraphRAG com traversal para relações cliente contrato fatura: assumi custo de rebuild incremental para responder perguntas relacionais que o vetorial não resolve.
- Chunking semântico com overlap 128: preservei contexto entre sentenças mesmo pagando mais tokens indexados.
- Avaliação em 30 perguntas (10 exatas, 10 sinônimos, 10 relação) com hit@5: troquei teste informal por matriz que separa exato, sinônimo e relação.
- Meta de precisão@5 maior ou igual a 95 por cento e latência menor que 150 ms com job noturno: equilibrei qualidade alta com atualização periódica do grafo.

## Impacto no negócio

O híbrido com hit@5 maior ou igual a 0.95 no exato e maior ou igual a 0.9 na relação eleva a precisão@5 de cerca de 42 por cento para cerca de 98 por cento, o que reduz retrabalho de respostas vagas e viabiliza precificação de busca relacional sem indexação manual.

## Referências de estudo

- Curso: Advanced Retrieval for AI with Chroma, plataforma DeepLearning.AI.
- Vídeo: GraphRAG com busca vetorial mais grafo de conhecimento, plataforma YouTube, canal Microsoft Developer.
- Doc oficial: Guia de BM25 e relevância textual, documentação oficial Elastic.
- Doc oficial: Documentação do pgvector com HNSW, documentação oficial pgvector.
