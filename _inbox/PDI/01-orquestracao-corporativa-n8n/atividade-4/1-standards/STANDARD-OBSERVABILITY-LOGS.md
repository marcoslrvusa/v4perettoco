# STANDARD — Observabilidade de Sincronização CRM

## 1. Log estruturado (JSON)
Cada node de saída para CRM emite log com:
- `trace_id` (correlaciona a execução inteira do workflow)
- `entity` (Lead/Contact/Deal), `crm` (salesforce|hubspot|rdstation)
- `action` (upsert|create|update), `record_id`, `http_status`, `duration_ms`
- `error_class` (quando falha) e `retry_count`

## 2. Níveis
- INFO: início/fim de sync, contagem de registros
- WARN: retorno parcial, rate-limit próximo do limite
- ERROR: falha de gravação no CRM (gatilho de alerta)

## 3. Trace de ponta a ponta
`trace_id` único por webhook/trigger, propagado em todos os nodes via `$vars.traceId`.

## 4. Alerta proativo (SLO)
Subir alerta em #ops-crm quando: taxa de erro > 2% em 5 min, OU mesma `record_id` com 3 falhas consecutivas.
