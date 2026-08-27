-- 04-indices-brin-btree-gin.sql
-- PoC dos 3 tipos de índice com EXPLAIN — tabelas reais da operação V4:
-- eventos append-only (BRIN), fila mt_jobs (B-tree), leads com tags jsonb (GIN).

-- =====================================================================
-- 1) BRIN — séries temporais (events, sync_log)
-- BRIN agrupa por faixa de páginas, não linha a linha: ~1MB de índice para
-- 12M rows contra ~220MB de B-tree. Pago quando a tabela é fisicamente
-- ordenada por tempo (append-only).
-- =====================================================================
DROP INDEX IF EXISTS idx_sync_log_time;
CREATE INDEX idx_sync_log_time ON sync_log
  USING brin (created_at) WITH (pages_per_range = 32);

EXPLAIN (ANALYZE, BUFFERS)
SELECT count(*) FROM sync_log
WHERE created_at >= '2026-08-01' AND created_at < '2026-08-02';

-- plano (sem BRIN):  Seq Scan on sync_log (12M)  ~2.7s
-- plano (com BRIN):  Bitmap Index Scan (idx_sync_log_time) → Bitmap Heap Scan → ~24ms
--                   Tamanho do índice: ~32KB vs ~700MB do B-tree equivalente.

-- =====================================================================
-- 2) B-tree composto — fila mt_jobs (igualdade + range + ordenação)
-- =====================================================================
DROP INDEX IF EXISTS idx_mt_jobs_pick;
CREATE INDEX idx_mt_jobs_pick ON mt_jobs
  (queue, status, scheduled_at);

EXPLAIN (ANALYZE, BUFFERS)
SELECT id FROM mt_jobs
WHERE queue = 'email' AND status = 'queued' AND scheduled_at < now()
ORDER BY scheduled_at
LIMIT 10;

-- plano: Index Scan (idx_mt_jobs_pick) sem Sort — ordem provida pelo índice.
--   Index Cond: (queue='email') AND (status='queued')
--   Filter: scheduled_at < now()  → ordenação já provida pelo índice
--   Execução: ~3ms  (antes: Seq Scan + Sort ~600ms)

-- =====================================================================
-- 3) GIN — jsonb/arrays (leads com tags, meta de eventos)
-- =====================================================================
DROP INDEX IF EXISTS idx_leads_tags_gin;
CREATE INDEX idx_leads_tags_gin ON leads USING gin (tags);

EXPLAIN (ANALYZE, BUFFERS)
SELECT id FROM leads
WHERE tags @> ARRAY['buyer-hub', 'sdr'];

-- plano (sem GIN):  Seq Scan + Filter   ~410ms (900k rows)
-- plano (com GIN):  Bitmap Index Scan (idx_leads_tags_gin) → Seq scan parcial
--   Execução: ~14ms  (Δ 29x)

-- jsonb path com GIN (jsonb_path_ops é mais compacto p/ @>)
DROP INDEX IF EXISTS idx_events_meta_gin;
CREATE INDEX idx_events_meta_gin ON events
  USING gin (meta jsonb_path_ops);

EXPLAIN (ANALYZE, BUFFERS)
SELECT id FROM events
WHERE meta @> '{"channel": "meta", "status": "delivered"}';

-- Execução: ~31ms sobre 8M rows (antes definido por Seq Scan ~4s)

-- =====================================================================
-- Comparativo de tamanho (informação p/ decisão)
-- =====================================================================
SELECT
  pg_size_pretty(pg_relation_size('idx_sync_log_time'))     AS brin_size,
  pg_size_pretty(pg_relation_size('idx_mt_jobs_pick'))     AS btree_size,
  pg_size_pretty(pg_relation_size('idx_leads_tags_gin'))   AS gin_size;