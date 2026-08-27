# PDI — Apresentação: APIs Modulares de Missão Crítica (FastAPI) com Paginação, Cache e Rate Limiting

> **Formato:** 5-6 slides | **Tempo:** 15-20 min
> **Audiência:** Tech Lead + Squad

---

## Slide 1: Título

```
PDI: APIS MODULARES DE MISSÃO CRÍTICA (FASTAPI) COM PAGINAÇÃO, CACHE E RATE LIMITING

Marcos Perettoco — V4 Company
25/08/2026 | Arquitetura Full Stack
```

---

## Slide 2: O Problema

**Os endpoints internos eram monolíticos e sem proteção, sofrendo sobrecarga em picos e sem paginação.**

## Diagnóstico

- Sem paginação (vazamento de memória em listas grandes)
- Sem rate limiting (abuso de quota)
- Sem cache (pressão desnecessária no banco)


---

## Slide 3: Arquitetura da Solução

## Abordagem

- API modular FastAPI versionada (/v1)
- Paginação com envelope {items,page,size,total}
- Rate limiting por api_key (slowapi, 100/min)
- Cache via Redis para listas quentes


---

## Slide 4: Entregas

## Artefatos

- API-STANDARD.md (padrão)
- main_api.py (FastAPI paginação + rate limit)
- requirements.txt


---

## Slide 5: Métricas de Sucesso

| Métrica | Antes | Depois |
|--------|-------|--------|
| Proteção de sobrecarga | Não | Sim (rate limit) |
| Paginação | Não | Sim |
---

## Slide 6: Próximos Passos

- Expor os endpoints críticos por trás do gateway
- Adicionar autenticação OAuth2
