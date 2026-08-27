# Idempotencia — Padrao

## Premissa
Brokers sao at-least-once. Duplicata VAI acontecer. O consumidor torna o efeito unico.

## Tecnica
1. Cada evento tem event_id (UUID).
2. Tabela processed_events(event_id, ts) com PK unica.
3. INSERT event_id antes de processar; duplicata -> pula.
4. OU upsert por chave de negocio (CNPJ).

```sql
INSERT INTO processed_events(id) VALUES ($1) ON CONFLICT DO NOTHING;
```
