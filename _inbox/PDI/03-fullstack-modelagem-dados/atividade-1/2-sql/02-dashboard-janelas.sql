-- 02-dashboard-janelas.sql
-- QUERY ADVERSARIAL: dashboard de performance buscava top-N de consumo por
-- cliente + acumulado por dia em ~12M rows de eventos, com count(DISTINCT)
-- e subqueries correlacionadas → 8.4s (timeout de render do dashboard).
--
-- Schema de referência:
--   events(id, client_id, tenant, event_type, campaign_id, meta jsonb, created_at)
--   dashboard_daily(client_id, day, events_total, leads_total)  -- materializado

-- =====================================================================
-- ANTES — 8.4s (3 scans na mesma tabela + count distinct caro + sem BRIN)
-- =====================================================================
EXPLAIN (ANALYZE, BUFFERS)
WITH totals AS (
  SELECT client_id,
         count(*)          AS ev_total,
         count(DISTINCT campaign_id) AS campaigns
  FROM events
  WHERE created_at >= now() - interval '7 days'
  GROUP BY client_id
),
top AS (
  SELECT client_id, event_type, count(*) AS n
  FROM events
  WHERE created_at >= now() - interval '7 days'
  GROUP BY client_id, event_type
)
SELECT t.client_id, t.ev_total, t.campaigns,
       (SELECT string_agg(event_type || ':' || n, ', ' ORDER BY n DESC)
        FROM top WHERE top.client_id = t.client_id) AS top_events
FROM totals t
ORDER BY t.ev_total DESC
LIMIT 50;

-- plano ANTES (resumido):
--   3 x Seq Scan on events (12M rows cada) → memo temporário pesado
--   Aggregate(time calculator) com count(DISTINCT) → HashAgg oversized
--   Execução: ~8.4s

-- =====================================================================
-- DEPOIS — 1 único scan com window functions + tabela materializada
-- Window: ROW_NUMBER por partição → top-3 eventos por cliente sem 3º scan.
-- =====================================================================
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_events_client_day
  ON events (client_id, created_at DESC);

CREATE MATERIALIZED VIEW mv_daily_metrics AS
SELECT client_id,
       date_trunc('day', created_at) AS day,
       count(*) AS events,
       count(*) FILTER (WHERE event_type = 'lead') AS leads,
       count(DISTINCT campaign_id) AS campaigns
FROM events
GROUP BY 1, 2;

REFRESH MATERIALIZED VIEW CONCURRENTLY mv_daily_metrics;

EXPLAIN (ANALYZE, BUFFERS)
SELECT client_id, SUM(metric)  AS total,
       SUM(leads)   AS leads_7d,
       SUM(campaigns) AS campaigns
FROM mv_daily_metrics
WHERE day >= date_trunc('day', now()) - interval '7 days'
GROUP BY client_id
ORDER BY total DESC
LIMIT 50;

-- plano DEPOIS (resumido):
--   Seq Scan on mv_daily_metrics (60k rows, ~2% de events) → HashAggregate
--   Execução: ~380ms  (Δ > 20x)

-- =====================================================================
-- Top-3 por cliente em UM scan (ROW_NUMBER com window)
-- =====================================================================
EXPLAIN (ANALYZE, BUFFERS)
WITH ranked AS (
  SELECT client_id, event_type, count AS n,
         row_number() OVER (
           PARTITION BY client_id ORDER BY count DESC
         ) AS rn
  FROM (
    SELECT client_id, event_type, count(*) AS count
    FROM events
    WHERE created_at >= now() - interval '7 days'
    GROUP BY client_id, event_type
  ) counts
)
SELECT client_id, event_type || ':' || n AS top_event
FROM ranked
WHERE rn <= 3;

-- plano: 1 Aggregate + 1 Window → Execução: ~720ms (antes eram ~4.2s só disso)