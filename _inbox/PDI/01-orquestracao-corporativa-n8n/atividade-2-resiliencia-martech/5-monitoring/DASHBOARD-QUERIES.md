# Dashboard de Monitoramento MarTech: Queries Supabase

> Banco: Supabase `gswzuzetverulcgzhynb` · Schema v3.0 (mt_*)

## 1. Backlog por Fila (agora)

```sql
SELECT * FROM vw_mt_queue_backlog;
```

Retorna: `queue | queued | running | failed | oldest_queued_at | stale_queued`

- `stale_queued > 0` = job parado na fila há mais de 10 min (worker pode estar off).

## 2. Uso de Concorrência (semáforo)

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

## 9. Throughput da Fila (por hora, 24h)

```sql
SELECT
  date_trunc('hour', finished_at) AS hora,
  queue,
  COUNT(*) AS concluidos,
  COUNT(*) FILTER (WHERE status = 'failed') AS falhos,
  ROUND(100.0 * COUNT(*) FILTER (WHERE status = 'failed') / GREATEST(COUNT(*), 1), 2)
    AS falha_pct
FROM mt_jobs
WHERE finished_at > now() - INTERVAL '24 hours'
GROUP BY 1, 2
ORDER BY 1 DESC;
```

Serve para responder a pergunta que o backlog não responde: "o problema é que
chegou muito trabalho ou que paramos de concluir?". Se `concluidos` cai com
`queued` estável, o gargalo está na entrada; se `concluidos` cai com `queued`
subindo, o gargalo está na execução.

## 10. Latência de ACK do Gateway

```sql
SELECT
  ROUND(AVG(EXTRACT(EPOCH FROM (picked_at - created_at)))::numeric, 2) AS espera_s,
  ROUND(MAX(EXTRACT(EPOCH FROM (picked_at - created_at)))::numeric, 2) AS espera_max_s,
  COUNT(*) AS jobs
FROM mt_jobs
WHERE created_at > now() - INTERVAL '1 hour'
  AND picked_at IS NOT NULL;
```

`espera_s` mede o tempo entre o ACK e o início da execução, que é o custo real
de ter escolhido a fila assíncrona. É o número que se compara ao SLO de 2 s do
ACK mais o tempo de ciclo do poller (15 s), ou seja, espera mediana esperada na
faixa de 0 a 15 s e nunca acima do timeout configurado de 10 min.

## 11. Retomadas e Retentativas (indicador de saúde do padrão)

```sql
SELECT
  queue,
  COUNT(*) AS jobs,
  ROUND(AVG(attempts), 2) AS tentativas_media,
  COUNT(*) FILTER (WHERE attempts > 1) AS com_retry,
  COUNT(*) FILTER (WHERE status = 'failed') AS dlq
FROM mt_jobs
WHERE created_at > now() - INTERVAL '7 days'
GROUP BY queue
ORDER BY com_retry DESC;
```

- `tentativas_media` perto de 1,00 = fluxo limpo.
- Acima de 1,50 = investigar causa raiz antes de mexer em `max_attempts`.
- `dlq > 0` = existe trabalho parado esperando decisão humana.

## Painel sugerido (ordem das cartões)

| Posição | Cartão | Fonte |
|---------|--------|-------|
| 1 | Fila agora (por fila) | Query #1 |
| 2 | Slots em uso | Query #2 |
| 3 | Taxa de sucesso 24h | Query #3 |
| 4 | Drifts abertos | Query #4 |
| 5 | Health abaixo do mínimo | Query #5 |
| 6 | Jobs lentos | Query #6 |
| 7 | Top erros (7 dias) | Query #7 |
| 8 | Checkpoints em execução | Query #8 |
| 9 | Throughput por hora | Query #9 |
| 10 | Espera média do ACK | Query #10 |
| 11 | Tentativas médias | Query #11 |

Os cartões 1 a 6 são de sala de operação (sempre visíveis); os de 7 a 11 são de
análise semanal, revisados no mesmo horário toda segunda-feira.