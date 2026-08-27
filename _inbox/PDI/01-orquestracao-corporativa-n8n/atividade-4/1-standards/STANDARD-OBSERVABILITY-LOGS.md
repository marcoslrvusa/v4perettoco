# STANDARD — Observabilidade de Sync n8n -> CRM

## Contrato (obrigatorio em toda saida)
Todo no que escreve em CRM deve emitir log estruturado:
```json
{"ts":"2026-08-27T10:00:00Z","level":"warn","trace_id":"abc123",
 "integration":"hubspot","op":"upsert_lead","status":"error",
 "code":"401","lead_id":"L-9","msg":"token expirado"}
```
## Niveis
- `info`: sucesso de sincronizacao (1 por lote).
- `warn`: falha recuperavel (retry depois).
- `error`: falha persistente -> alerta.

## Proibido
- Logar PII cru (e-mail/CNPJ) sem mascarar.
- Swallow de erro sem registro (falha silenciosa).
