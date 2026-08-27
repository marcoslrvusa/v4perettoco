# Queries de monitoramento — Observabilidade CRM

## Taxa de erro por CRM (janela 5 min)
```sql
SELECT crm, COUNT(*) FILTER (WHERE level='ERROR') * 1.0 / COUNT(*) AS error_rate
FROM crm_sync_logs
WHERE ts > now() - interval '5 minutes'
GROUP BY crm HAVING error_rate > 0.02;
```

## Record com 3 falhas consecutivas (sistêmico)
```sql
SELECT record_id, crm, count(*) AS fails
FROM crm_sync_logs
WHERE level='ERROR' AND ts > now() - interval '1 hour'
GROUP BY record_id, crm HAVING count(*) >= 3;
```

## p95 de latência por entidade (SLO)
```sql
SELECT entity, percentile_cont(0.95) WITHIN GROUP (ORDER BY duration_ms) AS p95_ms
FROM crm_sync_logs WHERE ts > now() - interval '24 hours' GROUP BY entity;
```
