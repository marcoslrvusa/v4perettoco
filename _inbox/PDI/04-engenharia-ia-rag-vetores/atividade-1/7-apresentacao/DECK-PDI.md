# Deck PDI: Fundamentos de IA Generativa (NVIDIA DLI) aplicados a RAG

Área: Engenharia de IA

## Slide 1: Resumo Executivo
Conclusão do curso NVIDIA DLI 'Building RAG Agents with LLMs' com transposição prática. Entrego notas e um notebook funcional de RAG end-to-end.
A base sustenta as próximas atividades (RAG híbrido, multi-agente, custos).
## Slide 2: Contexto de Produção
Time comenta 'RAG' mas sem padrão de chunking.
Similaridade pura trazia contexto irrelevante.
Sem métrica de qualidade.
## Slide 3: Diagnóstico
Chunk grande -> ruído; pequeno -> perde contexto.
Embedding sem normalização.
Sem rerank -> top-k ruído.
## Slide 4: Decisão Arquitetural (ADR)
ADR-041: Baseline RAG
| Opção | Pro | Contra | Decisão |
| --- | --- | --- | --- |
| Chunk 512 + overlap 64 + rerank | coeso | mais tokens | ESCOLHIDA |
> Nota: Normalizar embeddings; top-k=20 + rerank para top-5.
## Slide 5: Entregas
DLI-NOTES.md.
rag_baseline.py.
CONCLUSAO.md.
## Slide 6: Validação
Rodar rag_baseline.py.
Medir faithfulness em 10 perguntas.
Comparar com similaridade pura.
## Slide 7: Métricas
| SLO | Alvo |
| --- | --- |
| Faithfulness | >= 0.8 |
| Chunk | 512/64 |
## Slide 8: Riscos
| Risco | Mitigação |
| --- | --- |
| Contexto irrelevante | rerank |
| Hallucination | cite trecho |
## Slide 9: Próximos Passos
RAG híbrido (04-A2).
Avaliação RAGAS.