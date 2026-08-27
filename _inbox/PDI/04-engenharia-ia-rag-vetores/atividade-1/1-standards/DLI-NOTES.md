# NVIDIA DLI — Notas

- **Embeddings**: normalizar antes de coseno.
- **Chunking**: 512 tokens + overlap 64.
- **Retrieval**: top-k=20 + rerank para top-5.
- **Evaluation**: faithfulness + answer relevance.

## Anti-padroes
- Chunk gigante sem overlap -> ruido.
- Resposta sem citar fonte -> hallucination invisible.
