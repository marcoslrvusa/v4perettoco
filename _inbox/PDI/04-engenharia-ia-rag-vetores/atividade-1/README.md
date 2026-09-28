# Fundamentos de IA Generativa (NVIDIA DLI) aplicados a RAG

Engenharia de IA

## Resumo Executivo

Conclusão do curso NVIDIA DLI 'Building RAG Agents with LLMs' com transposição prática. Entrego notas e um notebook funcional de RAG end-to-end.

A base sustenta as próximas atividades (RAG híbrido, multi-agente, custos).

## Contexto de Produção

- Time comenta 'RAG' mas sem padrão de chunking.

- Similaridade pura trazia contexto irrelevante.

- Sem métrica de qualidade.

## Diagnóstico

- Chunk grande -> ruído; pequeno -> perde contexto.

- Embedding sem normalização.

- Sem rerank -> top-k ruído.

## Decisão Arquitetural (ADR)

ADR-041 : Baseline RAG

| Opção | Pro | Contra | Decisão |

| --- | --- | --- | --- |

| Chunk 512 + overlap 64 + rerank | coeso | mais tokens | ESCOLHIDA |

> **Nota:** Normalizar embeddings; top-k=20 + rerank para top-5.

## Entregas

- DLI-NOTES.md.

- rag_baseline.py.

- CONCLUSAO.md.

## Validação

1. Rodar rag_baseline.py.

2. Medir faithfulness em 10 perguntas.

3. Comparar com similaridade pura.

## Métricas

| SLO | Alvo |

| --- | --- |

| Faithfulness | >= 0.8 |

| Chunk | 512/64 |

## Riscos

| Risco | Mitigação |

| --- | --- |

| Contexto irrelevante | rerank |

| Hallucination | cite trecho |

## Próximos Passos

- RAG híbrido (04-A2).

- Avaliação RAGAS.

## Decisões e tradeoffs

- Chunk 512 com overlap 64: escolhi coesão contra custo de tokens, porque chunk grande gera ruído e chunk pequeno perde contexto, conforme ADR-041.
- Top-k 20 com rerank para top-5: aceitei latência extra do rerank para filtrar o ruído da similaridade pura.
- Normalizar embeddings de 1536 dim com cosseno e threshold 0.82: padronizei a medida para o score ser comparável entre textos de tamanhos distintos.
- Golden set com 50 pares e faithfulness maior ou igual a 0.8 em 10 perguntas: troquei avaliação no olhômetro por gate reproduzível no CI.
- Guardrail fail-closed com 100 por cento de bloqueio antes da produção: preferi falso positivo seguro a resposta tóxica, fora de domínio ou com PII.

## Impacto no negócio

O baseline com faithfulness maior ou igual a 0.8 e score médio maior ou igual a 0.90 no golden set de 50 pares reduz risco de hallucination em produção e elimina a surpresa de fatura com contagem previa de tokens, o que encurta homologação e sustenta as atividades seguintes de RAG híbrido e custos.

## Referências de estudo

- Curso: Building RAG Agents with LLMs, plataforma NVIDIA Deep Learning Institute (DLI).
- Vídeo: RAG from Scratch com chunking, embeddings e avaliação, plataforma YouTube, canal LangChain.
- Doc oficial: Guia de embeddings text-embedding-3-small, documentação oficial OpenAI.
- Doc oficial: Documentação do pgvector com índice HNSW, documentação oficial pgvector.
