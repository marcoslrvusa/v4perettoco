# PDI — Apresentação: Trilha NVIDIA Deep Learning Institute + Pipelines de Dados para IA

> **Formato:** 5-6 slides | **Tempo:** 15-20 min
> **Audiência:** Tech Lead + Squad

---

## Slide 1: Título

```
PDI: TRILHA NVIDIA DEEP LEARNING INSTITUTE + PIPELINES DE DADOS PARA IA

Marcos Perettoco — V4 Company
25/08/2026 | Engenharia de IA
```

---

## Slide 2: O Problema

**Fundamentar a equipe em pipelines de dados eficientes para IA, base para os agentes e RAG.**

## Diagnóstico

- Ingestão ad-hoc sem chunking consistente
- Embeddings sem batch assíncrono (estrangulamento de API)
- Falta de versionamento de dataset de embeddings


---

## Slide 3: Arquitetura da Solução

## Abordagem

- Estágios: ingest → chunk → embed → store → serve
- Chunk semântico (512-1024 tokens, overlap 10%)
- Embed em batch assíncrono
- pgvector com índice HNSW


---

## Slide 4: Entregas

## Artefatos

- DATA-PIPELINE-AI.md (guia)
- TRILHA.md (registro de conclusão)


---

## Slide 5: Métricas de Sucesso

| Métrica | Antes | Depois |
|--------|-------|--------|
| Pipeline documentado | Não | Sim |
| Trilha NVIDIA DLI | Em andamento | Concluída |
---

## Slide 6: Próximos Passos

- Aplicar o pipeline no RAG do Módulo 04-A2
- Versionar dataset de embeddings
