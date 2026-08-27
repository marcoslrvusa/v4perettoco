# Monitoring — Performance de Payload e Nós Code

Queries SQL para monitorar o processamento de payloads pesados e a saúde dos
nós Code (JS/Python) após o retrofit da atividade 3.

## Premissas

- Usa as tabelas da atividade 1 (`error_*`) e da atividade 2 (`mt_*`).
- O nó `Return Metrics` dos novos workflows expõe `processedItems`, `deduped`,
  `durationMs` e `itemsPerSecond` — alimente uma tabela de métricas se quiser
  histórico (sugestão: `mt_payload_metrics`).

## 1. Pico de processamento (top runs)

```sql
SELECT
  workflow_name,
  processed_items,
  deduped,
  duration_ms,
  items_per_second,
  executed_at
FROM mt_payload_metrics
ORDER BY processed_items DESC
LIMIT 20;
```

## 2. Runs lentas (mais de 60s)

```sql
SELECT *
FROM mt_payload_metrics
WHERE duration_ms > 60000
ORDER BY duration_ms DESC;
```

## 3. Items por segundo (tendência)

```sql
SELECT
  date_trunc('hour', executed_at) AS hr,
  round(avg(items_per_second)) AS avg_ips,
  max(items_per_second) AS max_ips
FROM mt_payload_metrics
GROUP BY hr
ORDER BY hr DESC;
```

## 4. Dedupe ratio (payloads com muita duplicação)

```sql
SELECT
  workflow_name,
  round(100.0 * deduped / NULLIF(processed_items + deduped, 0), 1) AS dedupe_pct,
  count(*) AS runs
FROM mt_payload_metrics
GROUP BY workflow_name
ORDER BY dedupe_pct DESC;
```

## 5. Alertas sugeridos

| Condição | Ação |
|---|---|
| `duration_ms > 60000` | Alertar — payload ou nó regrediu |
| `items_per_second` cai > 50% vs média 24h | Investigar nó Code |
| `dedupe_pct > 50%` | Cliente envia duplicado — orientar filtro |

## 6. Schema sugerido (mt_payload_metrics)

```sql
CREATE TABLE IF NOT EXISTS mt_payload_metrics (
  id bigint generated always as identity primary key,
  workflow_name text not null,
  processed_items int,
  deduped int,
  duration_ms int,
  items_per_second numeric,
  executed_at timestamptz not null default now()
);
```

> Tabela de métricas é opcional e **aditiva** — não altera nenhuma tabela existente
> das atividades 1 e 2. Criar somente após homologação.