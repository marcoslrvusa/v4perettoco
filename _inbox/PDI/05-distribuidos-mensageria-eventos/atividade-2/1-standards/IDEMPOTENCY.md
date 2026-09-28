# Idempotência: Padrão

## Premissa
Brokers são at-least-once. Duplicata VAI acontecer. O consumidor torna o efeito único.

## Técnica
1. Cada evento tem event_id (UUID).
2. Tabela processed_events(event_id, ts) com PK única.
3. INSERT event_id antes de processar; duplicata -> pula.
4. OU upsert por chave de negócio (CNPJ).

```sql
INSERT INTO processed_events(id) VALUES ($1) ON CONFLICT DO NOTHING;
```
