# Script de Demonstração — APIs Modulares de Missão Crítica (FastAPI) com Paginação, Cache e Rate Limiting

## Setup
```bash
# Estrutura da entrega
tree 03-fullstack-modelagem-dados/atividade-2/
```

## Passo 1: Contexto
Explique o problema:
> Os endpoints internos eram monolíticos e sem proteção, sofrendo sobrecarga em picos e sem paginação.

## Passo 2: Arquitetura
Apresente os pontos-chave:
- API modular FastAPI versionada (/v1)
- Paginação com envelope {items,page,size,total}
- Rate limiting por api_key (slowapi, 100/min)
- Cache via Redis para listas quentes

## Passo 3: Entregas
Mostre os artefatos gerados:
- API-STANDARD.md (padrão)
- main_api.py (FastAPI paginação + rate limit)
- requirements.txt

## Passo 4: Métricas
| Métrica | Antes | Depois |
|--------|-------|--------|
| Proteção de sobrecarga | Não | Sim (rate limit) |
| Paginação | Não | Sim |
