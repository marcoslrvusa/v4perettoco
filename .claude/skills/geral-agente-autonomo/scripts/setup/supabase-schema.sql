-- Agent Queue — fila de demandas para o orquestrador autônomo
-- Executar no SQL Editor do Supabase

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS agent_queue (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  priority INTEGER DEFAULT 0,
  status TEXT DEFAULT 'pending'
    CHECK (status IN ('pending','classifying','processing','awaiting_review','completed','failed','cancelled')),
  demand_type TEXT NOT NULL
    CHECK (demand_type IN ('flag','scheduled','manual','webhook')),
  source TEXT DEFAULT '',
  function TEXT NOT NULL
    CHECK (function IN ('aquisicao','conteudo','saude_cliente','receita','lancamento','operacao','lideranca','copy')),
  urgency TEXT DEFAULT 'normal'
    CHECK (urgency IN ('baixa','normal','alta','critica')),
  scope TEXT DEFAULT 'single'
    CHECK (scope IN ('single','team','multi_team')),
  briefing JSONB DEFAULT '{}'::jsonb,
  orchestrator TEXT DEFAULT '',
  assigned_to TEXT DEFAULT '',
  classification JSONB DEFAULT '{}'::jsonb,
  execution_log JSONB DEFAULT '[]'::jsonb,
  result JSONB DEFAULT '{}'::jsonb,
  success_score INTEGER,
  error TEXT DEFAULT '',
  completed_at TIMESTAMPTZ,
  metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_agent_queue_status ON agent_queue (status);
CREATE INDEX IF NOT EXISTS idx_agent_queue_priority ON agent_queue (priority DESC, created_at ASC);
CREATE INDEX IF NOT EXISTS idx_agent_queue_function ON agent_queue (function);
CREATE INDEX IF NOT EXISTS idx_agent_queue_created ON agent_queue (created_at DESC);

ALTER TABLE agent_queue ENABLE ROW LEVEL SECURITY;
CREATE POLICY "service_role access" ON agent_queue
  USING (true) WITH CHECK (true);

CREATE OR REPLACE FUNCTION dequeue_next()
RETURNS TABLE(o_id UUID, o_demand_type TEXT, o_function TEXT, o_urgency TEXT, o_scope TEXT, o_briefing JSONB, o_source TEXT, o_priority INTEGER)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  UPDATE agent_queue
  SET
    status = 'classifying',
    updated_at = NOW()
  WHERE id = (
    SELECT id FROM agent_queue
    WHERE status = 'pending'
    ORDER BY priority DESC, created_at ASC
    LIMIT 1
    FOR UPDATE SKIP LOCKED
  )
  RETURNING
    id, demand_type, function, urgency, scope, briefing, source, priority;
END;
$$;

CREATE OR REPLACE FUNCTION enqueue_demand(
  p_demand_type TEXT,
  p_source TEXT,
  p_function TEXT,
  p_urgency TEXT DEFAULT 'normal',
  p_scope TEXT DEFAULT 'single',
  p_briefing JSONB DEFAULT '{}'::jsonb,
  p_priority INTEGER DEFAULT 0
)
RETURNS UUID
LANGUAGE plpgsql
AS $$
DECLARE
  v_id UUID;
BEGIN
  INSERT INTO agent_queue (demand_type, source, function, urgency, scope, briefing, priority)
  VALUES (p_demand_type, p_source, p_function, p_urgency, p_scope, p_briefing, p_priority)
  RETURNING id INTO v_id;
  RETURN v_id;
END;
$$;

CREATE TABLE IF NOT EXISTS agent_queue_log (
  id BIGSERIAL PRIMARY KEY,
  queue_id UUID REFERENCES agent_queue(id) ON DELETE CASCADE,
  event TEXT NOT NULL,
  detail JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_agent_queue_log_queue ON agent_queue_log (queue_id, created_at);

CREATE OR REPLACE FUNCTION log_queue_event(
  p_queue_id UUID,
  p_event TEXT,
  p_detail JSONB DEFAULT '{}'::jsonb
)
RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
  INSERT INTO agent_queue_log (queue_id, event, detail)
  VALUES (p_queue_id, p_event, p_detail);
END;
$$;

CREATE TABLE IF NOT EXISTS agent_routing_stats (
  id BIGSERIAL PRIMARY KEY,
  date DATE DEFAULT CURRENT_DATE,
  orchestrator TEXT NOT NULL,
  specialist TEXT DEFAULT '',
  function TEXT NOT NULL,
  executions INTEGER DEFAULT 0,
  success_count INTEGER DEFAULT 0,
  fail_count INTEGER DEFAULT 0,
  avg_success_score NUMERIC(3,1) DEFAULT 0,
  avg_execution_time_seconds INTEGER DEFAULT 0,
  UNIQUE(date, orchestrator, specialist, function)
);

CREATE OR REPLACE FUNCTION update_routing_stats(
  p_orchestrator TEXT,
  p_specialist TEXT,
  p_function TEXT,
  p_success_score INTEGER,
  p_execution_time_seconds INTEGER
)
RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
  INSERT INTO agent_routing_stats (date, orchestrator, specialist, function, executions, success_count, fail_count, avg_success_score, avg_execution_time_seconds)
  VALUES (CURRENT_DATE, p_orchestrator, p_specialist, p_function, 1, CASE WHEN p_success_score >= 5 THEN 1 ELSE 0 END, CASE WHEN p_success_score < 5 THEN 1 ELSE 0 END, p_success_score, p_execution_time_seconds)
  ON CONFLICT (date, orchestrator, specialist, function)
  DO UPDATE SET
    executions = agent_routing_stats.executions + 1,
    success_count = agent_routing_stats.success_count + CASE WHEN p_success_score >= 5 THEN 1 ELSE 0 END,
    fail_count = agent_routing_stats.fail_count + CASE WHEN p_success_score < 5 THEN 1 ELSE 0 END,
    avg_success_score = (agent_routing_stats.avg_success_score * agent_routing_stats.executions + p_success_score) / (agent_routing_stats.executions + 1),
    avg_execution_time_seconds = (agent_routing_stats.avg_execution_time_seconds * agent_routing_stats.executions + p_execution_time_seconds) / (agent_routing_stats.executions + 1);
END;
$$;
