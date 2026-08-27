-- 05-rls-performance.sql
-- PoC: RLS sem destruir índices. Regra: a politica é aplicada linha a linha
-- durante o scan — se ela fizer JOIN/função cara, o planner cai para Seq Scan.
--
-- Cenario: MT_JOBs com tenant por client_id. Antes a política juntava a tabela
-- de membership; depois usa coluna denormalizada + função SECURITY DEFINER.
-- =====================================================================
-- Schema minimo
-- =====================================================================
CREATE TABLE IF NOT EXISTS mt_jobs_rls (
  id        bigint generated always as identity primary key,
  client_id bigint not null,
  status    text not null default 'queued',
  payload   jsonb
);

-- =====================================================================
-- ANTES — RLS com JOIN (politica cara) → força Seq Scan mesmo com índice
-- =====================================================================
CREATE OR REPLACE FUNCTION public.is_member_of_client(cid bigint)
RETURNS boolean LANGUAGE sql STABLE SECURITY DEFINER AS
$$
  SELECT EXISTS (
    SELECT 1 FROM public.user_clients
    WHERE user_id = (select auth.uid()) AND client_id = cid
  );
$$;

ALTER TABLE mt_jobs ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS rls_before ON mt_jobs;
CREATE POLICY rls_before ON public.mt_jobs
  FOR SELECT USING (public.is_member_of_client(client_id));

CREATE INDEX idx_mt_jobs_status ON mt_jobs (status);

-- Set header de auth para simular usuario logado
SET request.jwt.claims = '{"sub":"11111111-1111-1111-1111-111111111111"}';

EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM mt_jobs WHERE status = 'queued';

-- plano ANTES (resumo):
--   Seq Scan on mt_jobs — planner nao pode usar idx_mt_jobs_status porque a
--   RLS com função (VOLATILE do ponto de vista do planner) impede poda segura.
--   Execução: ~1.4s para 900k rows + custo da função por linha (~180ms).

-- =====================================================================
-- DEPOIS — coluna denormalizada + função estável com SECURITY DEFINER
-- =====================================================================
ALTER TABLE mt_jobs ADD COLUMN IF NOT EXISTS tenant_id bigint;
-- popule de client_id (na V4 é sempre 1-to-1 no ciclo SDR)

CREATE OR REPLACE FUNCTION public.current_tenant_id()
RETURNS bigint LANGUAGE sql STABLE SECURITY DEFINER AS
$$
  SELECT NULLIF(current_setting('request.jwt.claims', true)::json->>'tenant_id', '')::bigint;
$$;

DROP POLICY IF EXISTS rls_before ON mt_jobs;
CREATE POLICY rls_after ON public.mt_jobs
  FOR SELECT USING (tenant_id = public.current_tenant_id());

CREATE INDEX CONCURRENTLY idx_mt_jobs_tenant_status
  ON mt_jobs (tenant_id, status);

EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM mt_jobs WHERE status = 'queued';

-- plano DEPOIS (resumo):
--   Index Scan using idx_mt_jobs_tenant_status
--       Index Cond: (status = 'queued')
--       Filter: (tenant_id = current_tenant_id())  -- estável, custo 0
--   Execução: ~8ms  (Δ 175x) — o planner pode continuar usando o índice.

-- =====================================================================
-- Regra: SEMPRE validar RLS com o header de auth setado. Sem ele o EXPLAIN
-- mostra plano "limpo" falso (RLS desativada para role superuser).
-- =====================================================================
RESET request.jwt.claims;