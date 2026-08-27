# PDI — Apresentação: RAG Híbrido / GraphRAG com Supabase (pgvector)

> **Formato:** 5-6 slides | **Tempo:** 15-20 min
> **Audiência:** Tech Lead + Squad

---

## Slide 1: Título

```
PDI: RAG HÍBRIDO / GRAPHRAG COM SUPABASE (PGVECTOR)

Marcos Perettoco — V4 Company
25/08/2026 | Engenharia de IA
```

---

## Slide 2: O Problema

**A busca interna por dados dependia de palavra-chave, perdendo contexto semântico.**

## Diagnóstico

- Busca só lexical (semântica perdida)
- Sem rerank dos resultados
- Relações entre entidades não exploradas


---

## Slide 3: Arquitetura da Solução

## Abordagem

- RAG híbrido: vetorial (pgvector HNSW) + lexical (tsvector/BM25)
- Fusão RRF dos dois rankings
- GraphRAG: tabelas entity/relationship + traverse por CTE
- Query SQL híbrida combinando score vetorial e ts_rank


---

## Slide 4: Entregas

## Artefatos

- RAG-ARCHITECTURE.md (arquitetura + SQL)
- rag_hybrid.py (busca híbrida)
- 001_rag_schema.sql (schema pgvector)


---

## Slide 5: Métricas de Sucesso

| Métrica | Antes | Depois |
|--------|-------|--------|
| Qualidade da busca | Lexical | Híbrida + grafo |
| Cobertura semântica | Baixa | Alta |
---

## Slide 6: Próximos Passos

- Popular o índice com dados internos
- Avaliar com conjunto de perguntas (golden set)
