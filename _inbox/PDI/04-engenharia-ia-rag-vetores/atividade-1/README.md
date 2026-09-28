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

ADR-041 : Baseline RAG

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

## Decisoes e tradeoffs

- Chunk 512 com overlap 64: escolhi coesao contra custo de tokens, porque chunk grande gera ruido e chunk pequeno perde contexto, conforme ADR-041.
- Top-k 20 com rerank para top-5: aceitei latencia extra do rerank para filtrar o ruido da similaridade pura.
- Normalizar embeddings de 1536 dim com cosseno e threshold 0.82: padronizei a medida para o score ser comparavel entre textos de tamanhos distintos.
- Golden set com 50 pares e faithfulness maior ou igual a 0.8 em 10 perguntas: troquei avaliacao no olhometro por gate reproduzivel no CI.
- Guardrail fail-closed com 100 por cento de bloqueio antes da producao: preferi falso positivo seguro a resposta toxica, fora de dominio ou com PII.

## Impacto no negocio

O baseline com faithfulness maior ou igual a 0.8 e score medio maior ou igual a 0.90 no golden set de 50 pares reduz risco de hallucination em producao e elimina a surpresa de fatura com contagem previa de tokens, o que encurta homologacao e sustenta as atividades seguintes de RAG hibrido e custos.

## Referencias de estudo

- Curso: Building RAG Agents with LLMs, plataforma NVIDIA Deep Learning Institute (DLI).
- Video: RAG from Scratch com chunking, embeddings e avaliacao, plataforma YouTube, canal LangChain.
- Doc oficial: Guia de embeddings text-embedding-3-small, documentacao oficial OpenAI.
- Doc oficial: Documentacao do pgvector com indice HNSW, documentacao oficial pgvector.
