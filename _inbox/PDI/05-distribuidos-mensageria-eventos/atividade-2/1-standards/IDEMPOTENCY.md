# STANDARD — Idempotência em Consumidores

- **Chave:** `event_id` único no cabeçalho da mensagem.
- **Store:** tabela `processed_events(event_id PK, created_at)`.
- **Fluxo:** `INSERT event_id` → se duplicado (23505), descarta silenciosamente.
- **Upsert:** `INSERT ... ON CONFLICT DO NOTHING` para o dado de negócio.
