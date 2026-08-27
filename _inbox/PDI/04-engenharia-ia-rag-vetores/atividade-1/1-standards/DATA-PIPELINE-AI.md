# Pipelines de Dados para IA (NVIDIA DLI)

## Estágios
1. **Ingest:** conectores (Docs, CRM, SQL) → fila.
2. **Chunk:** split semântico (512-1024 tokens, overlap 10%).
3. **Embed:** batch assíncrono (evita estrangulamento de API).
4. **Store:** pgvector com índice HNSW.
5. **Serve:** retrieval + rerank.

## Boas práticas
- Desacoplar ingest de serve (fila).
- Versionar dataset de embeddings (reembed em mudança de modelo).
