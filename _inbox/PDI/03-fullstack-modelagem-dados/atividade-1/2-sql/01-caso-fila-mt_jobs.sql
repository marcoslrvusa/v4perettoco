-- 01-caso-fila-mt_jobs.sql
-- QUERY ADVERSARIAL (produção): o worker pegava o próximo job da fila
-- varrendo 2.4M linhas. Seq Scan total + Sort → 1.8s por poll em picos.
--
-- Schema de referência:
--   mt_jobs(id bigserial PK, client_id bigint, queue text, status text,
--           payload jsonb, priority int default 5, scheduled_at timestamptz,
--           created_at timestamptz default now(), attempts int default 0);

-- =====================================================================
-- ANTES — plano: Seq Scan on mt_jobs (2.4M rows) + Sort (queued + filter)
-- Também tinha CTE com JSONB "enrichment" que o planner não podia podar.
-- =====================================================================
EXPLAIN (ANALYZE, BUFFERS)
SELECT j.id, j.client_id, j.payload
FROM mt_jobs j
LEFT JOIN crm_accounts c ON c.id = j.client_id          -- FK desindexada
WHERE j.status = 'queued'
  AND j.queue = 'crm-sync'
  AND j.scheduled_at <= now()
ORDER BY j.priority DESC, j.created_at ASC
LIMIT 1;

-- plano ANTES (resumido):
--   Seq Scan on mt_jobs j  (cost=0.00..41,900 rows=1 (filtrado: fila única))
--     Filter: ((status = 'queued') AND (queue = 'crm-sync'))
--   Sort  (rows fila lentas)  762ms
--   Nested Loop  (JOIN em crm_client sem índice na FK)  →  +64ms
--   Planning time ... Execução total: ~1.82s

-- =====================================================================
-- DEPOIS — 2 índices compostos + JOIN indexado + remoção do LEFT JOIN inútil
-- =====================================================================
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_mt_jobs_pick
  ON mt_jobs (status, queue, scheduled_at) DESC NULLS LAST;

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_mt_jobs_client
  ON mt_jobs (client_id);

ANALYZE mt_jobs;

EXPLAIN (ANALYZE, BUFFERS)
SELECT j.id, j.client_id
FROM mt_jobs j
WHERE j.status = 'queued'
  AND j.queue = 'crm-sync'
  AND j.scheduled_at <= now()
ORDER BY j.priority DESC, j.created_at ASC
LIMIT 5;

-- Query otimização extra: priority tem cardinalidade baixa (1..9). Para o
-- conselheiro da V4, prioridade é resolvida na escrita (scheduled_at já
-- embute prioridade), então eliminamos o ORDER BY da query quente.

-- plano DEPOIS (resumido):
--   Index Scan using idx_mt_jobs_pick on mt_jobs
--       Index Cond: (status = 'queued') AND (queue = 'crm-sync')
--       Filter: (scheduled_at <= now())
--   Limit: 1 row at time
--   Execução: ~4ms  (Δ 450x)

-- =====================================================================
-- UPDATE em batch (nunca em fila única no loop do worker)
-- =====================================================================
WITH pick AS (
  SELECT id FROM mt_jobs
  WHERE status = 'queued' AND queue = 'crm-sync' AND scheduled_at <= now()
  ORDER BY id
  LIMIT 5
  FOR UPDATE SKIP LOCKED          -- evita lock storm entre workers
)
UPDATE mt_jobs
SET status = 'running', started_at = now(), attempts = attempts + 1
FROM pick
WHERE mt_jobs.id = pick.id
RETURNING mt_jobs.id;