# STANDARD — Serverless Seguro

- **Secrets:** nunca em env var hardcoded → usar Secret Manager / AWS Secrets Manager.
- **Conexão DB:** via connection pooler (PgBouncer) com TLS; não abrir por IP público.
- **IAM:** função com política mínima (only `cloudfunctions.invoker` + secret accessor).
- **Timeout:** <= 60s; jobs longos → Cloud Tasks / fila.
- **Idempotência:** chave de evento para não reprocessar duplicado.
