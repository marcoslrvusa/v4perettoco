# STANDARD — API Modular (FastAPI)

## Paginacao: SEMPRE cursor-based
`?after=<cursor>&limit=50`. Cursor = id criptografado.
Resposta: `{ items, next_cursor, limit }`. Nunca `offset` em tabelas > 10k.

## Cache
`Cache-Control: max-age=30, stale-while-revalidate=60`. Invalidar no write.

## Rate limiting (token bucket)
100 req/min por api_key -> 429 + Retry-After.

## Erros
`{ "error": { "code": "...", "message": "...", "trace_id": "..." } }`
4xx = cliente (nao retentar). 5xx = nosso (retry com backoff).
