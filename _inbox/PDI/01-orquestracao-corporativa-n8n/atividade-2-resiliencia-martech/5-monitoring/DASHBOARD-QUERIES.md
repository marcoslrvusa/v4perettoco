# Dashboard de Monitoramento MarTech — Queries Supabase

> Banco: Supabase `gswzuzetverulcgzhynb` · Schema v3.0 (mt_*)

## 1. Backlog por Fila (agora)

```sql
SELECT * FROM vw_mt_queue_backlog;
```

Retorna: `queue | queued | running | failed | oldest_queued_at | stale_queued`

- `stale_queued > 0` = job parado na fila há mais de 10 min (worker pode estar off).

## 2. Uso de Concorrencia (semáforo)

```sql
SELECT * FROM vw_mt_slots;
```

Retorna: `queue | max_concurrency | in_use | usage_pct`

- `usage_pct` perto de 100% = fila saturada; aumentar `max_concurrency` ou revisar tempo de processamento.

## 3. Health por Objeto (24h)

```sql
SELECT * FROM vw_mt_sync_summary_24h;
```

Retorna: `object | direction | total | success | failed | success_rate_pct | drifted | last_sync_at`

- `success_rate_pct < 95` = atenção; `< 90` = crítico.

## 4. Deltas Abertos (divergências não resolvidas)

```sql
SELECT * FROM vw_mt_drift_abertos;
```

- Qualquer linha = divergência que pode impactar cliente. Resolver antes do fim do dia.

## 5. Health Consolidado por Empresa

```sql
SELECT * FROM vw_mt_crm_health;
```

- `below_min = true` = health abaixo do mínimo configurado (`min_health`, default 0.90).

## 6. Job Lento (heartbeat antigo)

```sql
SELECT id, job_key, queue, status, picked_at, heartbeat_at,
       EXTRACT(EPOCH FROM (now() - heartbeat_at))::INTEGER / 60 AS minutes_since_heartbeat
FROM mt_jobs
WHERE status = 'running'
  AND heartbeat_at < now() - INTERVAL '10 minutes';
```

- Indica worker travado ou payload pesado demais. Se aparecer, verificar o worker.

## 7. Top Erros de Sync por Classe (7 dias)

```sql
SELECT
  object,
  error_class,
  COUNT(*) AS total,
  COUNT(*) FILTER (WHERE status = 'error') AS failed,
  MAX(created_at) AS ultimo_erro
FROM mt_sync_log
WHERE created_at > now() - INTERVAL '7 days'
GROUP BY object, error_class
ORDER BY total DESC
LIMIT 20;
```

## 8. Progresso de Jobs Pesados (checkpoint)

```sql
SELECT j.job_key, j.queue, p.chunk_index, p.total_chunks, p.status, p.updated_at
FROM mt_job_progress p
JOIN mt_jobs j ON j.id = p.job_id
WHERE p.status = 'running'
ORDER BY p.updated_at DESC;
```

## Alertas Sugeridos (Cron + n8n)

| Condição | Query | Ação |
|----------|-------|------|
| Fila parada (stale > 0) | View #1 | Alertar equipe (worker off) |
| Uso de concorrência > 90% | View #2 | Escalar worker / revisar chunks |
| Success rate < 90% | View #3 | Investigar integração CRM |
| Drift aberto > 4h | View #4 | Priorizar resolução (cliente impactado) |
| Health below_min | View #5 | Alertar + revisar `min_health` |
| Heartbeat antigo > 10 min | Query #6 | Reiniciar worker |