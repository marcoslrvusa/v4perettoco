# STANDARD: Serverless Event-Driven

1. Upload nunca processa no request. Grava no store e publica `file.uploaded`.
2. Concorrência limitada no consumer (ex.: 10).
3. Idempotência: dedup = hash(arquivo + tenant).
4. DLQ após N tentativas.
5. Payload carrega só metadados (URL).

## Quando NÃO usar
- Carga constante alta (worker always-on sai mais barato).
