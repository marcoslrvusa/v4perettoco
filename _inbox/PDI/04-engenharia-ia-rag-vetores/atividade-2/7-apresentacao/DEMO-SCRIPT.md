# Script de Demonstração — RAG Híbrido / GraphRAG com Supabase (pgvector)

## Setup
```bash
# Estrutura da entrega
tree 04-engenharia-ia-rag-vetores/atividade-2/
```

## Passo 1: Contexto
Explique o problema:
> A busca interna por dados dependia de palavra-chave, perdendo contexto semântico.

## Passo 2: Arquitetura
Apresente os pontos-chave:
- RAG híbrido: vetorial (pgvector HNSW) + lexical (tsvector/BM25)
- Fusão RRF dos dois rankings
- GraphRAG: tabelas entity/relationship + traverse por CTE
- Query SQL híbrida combinando score vetorial e ts_rank

## Passo 3: Entregas
Mostre os artefatos gerados:
- RAG-ARCHITECTURE.md (arquitetura + SQL)
- rag_hybrid.py (busca híbrida)
- 001_rag_schema.sql (schema pgvector)

## Passo 4: Métricas
| Métrica | Antes | Depois |
|--------|-------|--------|
| Qualidade da busca | Lexical | Híbrida + grafo |
| Cobertura semântica | Baixa | Alta |
