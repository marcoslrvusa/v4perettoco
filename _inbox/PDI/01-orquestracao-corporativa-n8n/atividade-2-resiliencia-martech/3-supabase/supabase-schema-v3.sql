-- ============================================================
-- N8N ENTERPRISE — Supabase Schema Extension v3.0
-- MarTech Resilience: Queues + Concurrency + Heavy Payload + CRM Observability
-- ============================================================
-- Uso: Rodar no SQL Editor do Supabase (projeto: gswzuzetverulcgzhynb)
-- Compatível com schema v2.x existente (adiciona tabelas, nao altera)
-- Prefixo: mt_ (MarTech) + vw_mt_ (views)
-- ============================================================

-- ============================================================
-- 1. JOB QUEUE (fila assíncrona)
-- ============================================================
CREATE TABLE IF NOT EXISTS mt_jobs (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  job_key         TEXT NOT NULL,
  queue           TEXT NOT NULL,
  status          TEXT NOT NULL DEFAULT 'queued'
    CHECK (status IN ('queued', 'running', 'done', 'failed')),
  priority        INTEGER DEFAULT 0,
  payload         JSONB DEFAULT '{}',
  attempts        INTEGER DEFAULT 0,
  max_attempts    INTEGER DEFAULT 3,
  created_at      TIMESTAMPTZ DEFAULT now(),
  picked_at       TIMESTAMPTZ,
  finished_at     TIMESTAMPTZ,
  heartbeat_at    TIMESTAMPTZ,
  retry_at        TIMESTAMPTZ DEFAULT now(),
  error_message   TEXT,
  UNIQUE (job_key, queue)
);

CREATE INDEX IF NOT EXISTS idx_mt_jobs_pick
  ON mt_jobs (queue, status, priority DESC, created_at ASC)
  WHERE status = 'queued' AND retry_at <= now();
CREATE INDEX IF NOT EXISTS idx_mt_jobs_running ON mt_jobs (status) WHERE status = 'running';
CREATE INDEX IF NOT EXISTS idx_mt_jobs_heartbeat ON mt_jobs (heartbeat_at) WHERE status = 'running';

-- ============================================================
-- 2. CONCURRENCY SLOTS (semáforo distribuído)
-- ============================================================
CREATE TABLE IF NOT EXISTS mt_concurrency (
  queue            TEXT PRIMARY KEY,
  max_concurrency  INTEGER NOT NULL DEFAULT 5,
  active_slots     INTEGER NOT NULL DEFAULT 0,
  updated_at       TIMESTAMPTZ DEFAULT now()
);

-- Slots são contados de mt_jobs running, mas guardamos o limite por fila aqui.

-- ============================================================
-- 3. JOB PROGRESS (checkpoint de payloads pesados)
-- ============================================================
CREATE TABLE IF NOT EXISTS mt_job_progress (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  job_id        UUID NOT NULL REFERENCES mt_jobs(id) ON DELETE CASCADE,
  chunk_index   INTEGER NOT NULL DEFAULT 0,
  total_chunks  INTEGER NOT NULL DEFAULT 0,
  status        TEXT NOT NULL DEFAULT 'running'
    CHECK (status IN ('running', 'paused', 'done')),
  error_message TEXT,
  updated_at    TIMESTAMPTZ DEFAULT now(),
  UNIQUE (job_id)
);

-- ============================================================
-- 4. CRM SYNC LOG (auditoria de sincronização)
-- ============================================================
CREATE TABLE IF NOT EXISTS mt_sync_log (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  sync_id       TEXT NOT NULL,
  object        TEXT NOT NULL,
  direction     TEXT NOT NULL DEFAULT 'push'
    CHECK (direction IN ('push', 'pull')),
  source        TEXT,
  client        TEXT,
  payload_hash  TEXT,
  response_hash TEXT,
  status        TEXT NOT NULL DEFAULT 'in_progress'
    CHECK (status IN ('in_progress', 'done', 'error')),
  http_status   INTEGER,
  error_class   TEXT,
  error_message TEXT,
  attempts      INTEGER DEFAULT 0,
  execution_url TEXT,
  drift         INTEGER DEFAULT 0,
  expected      INTEGER,
  synced        INTEGER,
  created_at    TIMESTAMPTZ DEFAULT now(),
  finished_at   TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_mt_sync_log_lookup
  ON mt_sync_log (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_mt_sync_log_object
  ON mt_sync_log (object, status, created_at DESC);

-- ============================================================
-- 5. CRM HEALTH (agregado por entidade)
-- ============================================================
CREATE TABLE IF NOT EXISTS mt_crm_health (
  id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  company          TEXT NOT NULL,
  object           TEXT NOT NULL,
  direction        TEXT NOT NULL DEFAULT 'push',
  total            INTEGER DEFAULT 0,
  success          INTEGER DEFAULT 0,
  failed           INTEGER DEFAULT 0,
  error_class_count JSONB DEFAULT '{}',
  last_sync_at     TIMESTAMPTZ,
  drift_count      INTEGER DEFAULT 0,
  min_health       NUMERIC(4,3) DEFAULT 0.90,
  updated_at       TIMESTAMPTZ DEFAULT now(),
  UNIQUE (company, object, direction)
);

-- ============================================================
-- 6. CRM SYNC DELTA (divergências detectadas)
-- ============================================================
CREATE TABLE IF NOT EXISTS mt_sync_delta (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  sync_id         TEXT NOT NULL,
  object          TEXT NOT NULL,
  client          TEXT,
  expected        INTEGER NOT NULL,
  confirmed       INTEGER NOT NULL,
  drift_pct       NUMERIC(6,3) NOT NULL,
  status          TEXT NOT NULL DEFAULT 'open'
    CHECK (status IN ('open', 'investigating', 'resolved', 'wont_fix')),
  execution_url   TEXT,
  notes           TEXT,
  created_at      TIMESTAMPTZ DEFAULT now(),
  resolved_at     TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_mt_delta_open
  ON mt_sync_delta (status, created_at DESC)
  WHERE status = 'open';

-- ============================================================
-- VIEWS DE MONITORAMENTO
-- ============================================================

-- 1. Filas com backlog (jobs aguardando processamento)
CREATE OR REPLACE VIEW vw_mt_queue_backlog AS
SELECT
  queue,
  COUNT(*) FILTER (WHERE status = 'queued')   AS queued,
  COUNT(*) FILTER (WHERE status = 'running')  AS running,
  COUNT(*) FILTER (WHERE status = 'failed')   AS failed,
  MAX(created_at) AS oldest_queued_at,
  COUNT(*) FILTER (WHERE status = 'queued' AND created_at < now() - INTERVAL '10 minutes') AS stale_queued
FROM mt_jobs
WHERE created_at > now() - INTERVAL '24 hours'
GROUP BY queue
ORDER BY queued DESC;

-- 2. Slots em uso vs limite por fila
CREATE OR REPLACE VIEW vw_mt_slots AS
SELECT
  c.queue,
  c.max_concurrency,
  COALESCE(r.running, 0) AS in_use,
  CASE WHEN c.max_concurrency > 0
       THEN ROUND((COALESCE(r.running, 0)::DECIMAL / c.max_concurrency) * 100, 1)
       ELSE 0 END AS usage_pct
FROM mt_concurrency c
LEFT JOIN (
  SELECT queue, COUNT(*) AS running
  FROM mt_jobs
  WHERE status = 'running'
  GROUP BY queue
) r ON r.queue = c.queue;

-- 3. Resumo de sync por objeto (24h)
CREATE OR REPLACE VIEW vw_mt_sync_summary_24h AS
SELECT
  object,
  direction,
  COUNT(*) AS total,
  COUNT(*) FILTER (WHERE status = 'done')   AS success,
  COUNT(*) FILTER (WHERE status = 'error')  AS failed,
  ROUND(COUNT(*) FILTER (WHERE status = 'done')::DECIMAL / NULLIF(COUNT(*), 0) * 100, 1) AS success_rate_pct,
  COUNT(*) FILTER (WHERE drift > 0) AS drifted,
  MAX(created_at) AS last_sync_at
FROM mt_sync_log
WHERE created_at > now() - INTERVAL '24 hours'
GROUP BY object, direction
ORDER BY total DESC;

-- 4. Deltas abertos (divergências não resolvidas)
CREATE OR REPLACE VIEW vw_mt_drift_abertos AS
SELECT
  object,
  client,
  sync_id,
  expected,
  confirmed,
  drift_pct,
  execution_url,
  created_at,
  EXTRACT(EPOCH FROM (now() - created_at))::INTEGER / 60 AS minutes_open
FROM mt_sync_delta
WHERE status = 'open'
ORDER BY drift_pct DESC;

-- 5. Health consolidado por empresa (abaixo do mínimo alerta)
CREATE OR REPLACE VIEW vw_mt_crm_health AS
SELECT
  company,
  object,
  direction,
  total,
  success,
  failed,
  CASE WHEN total > 0
       THEN ROUND(success::DECIMAL / NULLIF(total, 0) * 100, 1)
       ELSE 100 END AS health_score_pct,
  min_health,
  CASE WHEN total > 0 AND (success::DECIMAL / NULLIF(total, 0)) < min_health
       THEN true ELSE false END AS below_min,
  last_sync_at,
  updated_at
FROM mt_crm_health
ORDER BY below_min DESC, health_score_pct ASC;

-- ============================================================
-- REALTIME (novas tabelas)
-- ============================================================
DO $$ BEGIN ALTER PUBLICATION supabase_realtime ADD TABLE mt_jobs; EXCEPTION WHEN SQLSTATE '42710' THEN NULL; END $$;
DO $$ BEGIN ALTER PUBLICATION supabase_realtime ADD TABLE mt_sync_log; EXCEPTION WHEN SQLSTATE '42710' THEN NULL; END $$;
DO $$ BEGIN ALTER PUBLICATION supabase_realtime ADD TABLE mt_sync_delta; EXCEPTION WHEN SQLSTATE '42710' THEN NULL; END $$;
DO $$ BEGIN ALTER PUBLICATION supabase_realtime ADD TABLE mt_crm_health; EXCEPTION WHEN SQLSTATE '42710' THEN NULL; END $$;
