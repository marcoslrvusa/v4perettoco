# STANDARD — API Modular (FastAPI)

- **Paginação:** `?page=1&size=50` → envelope `{items, page, size, total}`.
- **Cache:** `Cache-Control: max-age=30` + `Redis` para listas quentes.
- **Rate limiting:** token bucket por `api_key` (100 req/min).
- **Erros:** envelope `{error:{code,message}}`, HTTP 429 em limite.
- **Versionamento:** prefixo `/v1`.
