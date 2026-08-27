# STANDARD — Serverless Event-Driven

1. Upload nunca processa no request. Grava no store e publica `file.uploaded`.
2. Concorrencia limitada no consumer (ex.: 10).
3. Idempotencia: dedup = hash(arquivo + tenant).
4. DLQ apos N tentativas.
5. Payload carrega so metadados (URL).

## Quando NAO usar
- Carga constante alta (worker always-on sai mais barato).
