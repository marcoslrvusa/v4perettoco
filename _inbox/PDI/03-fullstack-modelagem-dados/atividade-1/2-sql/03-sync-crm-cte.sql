-- 03-sync-crm-cte.sql
-- QUERY ADVERSARIAL: auditoria de sync de CRM por cliente, com JOINs em
-- FKs sem índice e filtro em coluna sem índice → 4.2s, estourava o timeout
-- do job que calcula drift (divergência esperado × confirmado).
--
-- Schema de referência:
--   sync_log(id, client_id, object, direction, expected, synced,
--            http_status, error text, created_at)
--   clients(id, name, tier)

-- =====================================================================
-- ANTES — 4.2s: Seq Scan sync_log (12M) + Hash Join sem índice na FK + Sort
-- =====================================================================
EXPLAIN (ANALYZE, BUFFERS)
SELECT c.id,
       s.object,
       s.direction,
       sum(s.expected) AS expected,
       sum(s.synced)   AS synced,
       count(*) FILTER (WHERE s.http_status <> 200) AS failures
FROM sync_log s
JOIN clients c ON c.id = s.client_id          -- FK s.client_id SEM índice
WHERE s.created_at >= now() - interval '30 days'
GROUP BY c.id, s.object, s.direction
ORDER BY (sum(s.expected) - sum(s.synced)) DESC;

-- plano ANTES (resumo):
--   Seq Scan on sync_log s (12M rows) — filtro created_at não podável
--   Hash Join on clients.id         — sem índice na FK → re-scan + spill
--   HashAggregate oversized          — work_mem estourado (temp files)
--   Execução: ~4.2s

-- =====================================================================
-- DEPOIS — 2 índices (FK composta + BRIN na série de tempo) + CTE de drift
-- =====================================================================
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_sync_log_client_created
  ON sync_log (client_id, created_at DESC);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_sync_log_created_brin
  ON sync_log (created_at) WITH (pages_per_range = 32);

ANALYZE sync_log;

EXPLAIN (ANALYZE, BUFFERS)
WITH drift AS (
  SELECT c.id,
         s.object,
         s.direction,
         sum(s.expected) AS expected,
         sum(s.synced)   AS synced,
         count(*) FILTER (WHERE s.http_status <> 200) AS failures
  FROM sync_log s
  JOIN clients c ON c.id = s.client_id
  WHERE s.created_at >= now() - interval '30 days'
  GROUP BY 1, 2, 3
)
SELECT d.id, d.object, d.direction,
       d.expected, d.synced, d.failures,
       round(100.0 * (1 - (d.synced::numeric / NULLIF(d.expected, 0))), 2) AS drift_pct
FROM drift d
WHERE d.expected > 0
  AND 100.0 * (1 - (d.synced::numeric / d.expected)) > 5
ORDER BY drift_pct DESC;

-- plano DEPOIS (resumo):
--   Bitmap Index Scan (idx_sync_log_client_created) poda 12M → ~180k rows
--   Bitmap Heap Scan + HashAggregate em 180k rows (30 dias)
--   Nested Loop indexado em clients (PK) — sem re-scan
--   Execução: ~180ms  (Δ 23x)

-- =====================================================================
-- Drift aggregation por object/direction (para o dashboard de sync)
-- =====================================================================
EXPLAIN (ANALYZE, BUFFERS)
WITH daily AS (
  SELECT direction,
         date_trunc('day', created_at) AS day,
         sum(expected) AS expected,
         sum(synced)   AS synced
  FROM sync_log
  WHERE created_at >= now() - interval '7 days'
  GROUP BY 1, 2
)
SELECT direction, day, expected, synced,
       round(100.0 * (1 - (synced::numeric / NULLIF(expected, 0))), 2) AS drift_pct
FROM daily
ORDER BY day, direction;

-- plano: BRIN + janela diária → Execução: ~96ms (antes ~1.9s com Seq Scan)