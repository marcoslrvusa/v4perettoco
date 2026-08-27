# Fundamentos de IA Generativa (NVIDIA DLI) aplicados a RAG

Engenharia de IA

## Resumo Executivo

Conclusao do curso NVIDIA DLI 'Building RAG Agents with LLMs' com transposicao pratica. Entrego notas e um notebook funcional de RAG end-to-end.

A base sustenta as proximas atividades (RAG hibrido, multi-agente, custos).

## Contexto de Producao

- Time comenta 'RAG' mas sem padrao de chunking.

- Similaridade pura trazia contexto irrelevante.

- Sem metrica de qualidade.

## Diagnostico

- Chunk grande -> ruido; pequeno -> perde contexto.

- Embedding sem normalizacao.

- Sem rerank -> top-k ruido.

## Decisao Arquitetural (ADR)

ADR-041 — Baseline RAG

| Opcao | Pro | Contra | Decisao |

| --- | --- | --- | --- |

| Chunk 512 + overlap 64 + rerank | coeso | mais tokens | ESCOLHIDA |

> **Nota:** Normalizar embeddings; top-k=20 + rerank para top-5.

## Entregas

- DLI-NOTES.md.

- rag_baseline.py.

- CONCLUSAO.md.

## Validacao

1. Rodar rag_baseline.py.

2. Medir faithfulness em 10 perguntas.

3. Comparar com similaridade pura.

## Metricas

| SLO | Alvo |

| --- | --- |

| Faithfulness | >= 0.8 |

| Chunk | 512/64 |

## Riscos

| Risco | Mitigacao |

| --- | --- |

| Contexto irrelevante | rerank |

| Hallucination | cite trecho |

## Proximos Passos

- RAG hibrido (04-A2).

- Avaliacao RAGAS.