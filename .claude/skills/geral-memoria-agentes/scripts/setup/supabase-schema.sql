-- ============================================================
-- geral-memoria-agentes — Schema pgvector para memória semântica
-- Execute no SQL Editor do Supabase (uma vez)
-- ============================================================

-- 1. Habilitar pgvector
CREATE EXTENSION IF NOT EXISTS vector WITH SCHEMA extensions;

-- 2. Tabela de memórias dos agentes
CREATE TABLE IF NOT EXISTS public.agent_memories (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  embedding   VECTOR(1536) NOT NULL,
  content     TEXT NOT NULL,
  summary     TEXT,
  client      TEXT,
  niche       TEXT,
  agent_role  TEXT,
  task_type   TEXT,
  strategy    TEXT,
  result      TEXT,
  success_score INTEGER CHECK (success_score >= 1 AND success_score <= 10),
  tags        JSONB DEFAULT '[]'::jsonb,
  metadata    JSONB DEFAULT '{}'::jsonb,
  created_at  TIMESTAMPTZ DEFAULT now(),
  updated_at  TIMESTAMPTZ DEFAULT now()
);

-- 3. Índice IVFFlat para busca por similaridade
CREATE INDEX IF NOT EXISTS idx_agent_memories_embedding
  ON public.agent_memories
  USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);

-- 4. Índices para filtros comuns
CREATE INDEX IF NOT EXISTS idx_agent_memories_client
  ON public.agent_memories (client);
CREATE INDEX IF NOT EXISTS idx_agent_memories_niche
  ON public.agent_memories (niche);
CREATE INDEX IF NOT EXISTS idx_agent_memories_task_type
  ON public.agent_memories (task_type);
CREATE INDEX IF NOT EXISTS idx_agent_memories_agent_role
  ON public.agent_memories (agent_role);
CREATE INDEX IF NOT EXISTS idx_agent_memories_created_at
  ON public.agent_memories (created_at DESC);

-- 5. Função de busca por similaridade
CREATE OR REPLACE FUNCTION public.match_agent_memories(
  query_embedding VECTOR(1536),
  match_threshold FLOAT DEFAULT 0.7,
  match_count     INT DEFAULT 5,
  filter_client   TEXT DEFAULT NULL,
  filter_niche    TEXT DEFAULT NULL,
  filter_role     TEXT DEFAULT NULL,
  filter_task     TEXT DEFAULT NULL
)
RETURNS TABLE(
  id            UUID,
  content       TEXT,
  summary       TEXT,
  client        TEXT,
  niche         TEXT,
  agent_role    TEXT,
  task_type     TEXT,
  strategy      TEXT,
  result        TEXT,
  success_score INTEGER,
  tags          JSONB,
  similarity    FLOAT,
  created_at    TIMESTAMPTZ
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    am.id,
    am.content,
    am.summary,
    am.client,
    am.niche,
    am.agent_role,
    am.task_type,
    am.strategy,
    am.result,
    am.success_score,
    am.tags,
    1 - (am.embedding <=> query_embedding) AS similarity,
    am.created_at
  FROM public.agent_memories am
  WHERE
    1 - (am.embedding <=> query_embedding) > match_threshold
    AND (filter_client IS NULL OR am.client = filter_client)
    AND (filter_niche IS NULL OR am.niche = filter_niche)
    AND (filter_role IS NULL OR am.agent_role = filter_role)
    AND (filter_task IS NULL OR am.task_type = filter_task)
  ORDER BY am.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;

-- 6. Expor à Data API (RLS obrigatório)
ALTER TABLE public.agent_memories ENABLE ROW LEVEL SECURITY;

-- Policy: leitura para anon (via RPC, precisa da permissão de SELECT)
CREATE POLICY "agent_memories_select_anon"
  ON public.agent_memories
  FOR SELECT
  TO anon
  USING (true);

-- Policy: insert para service_role via RPC
CREATE POLICY "agent_memories_insert_service"
  ON public.agent_memories
  FOR INSERT
  TO service_role
  WITH CHECK (true);

-- 7. Conceder acesso à Data API
GRANT USAGE ON SCHEMA public TO anon, authenticated, service_role;
GRANT SELECT ON TABLE public.agent_memories TO anon, authenticated, service_role;
GRANT INSERT ON TABLE public.agent_memories TO service_role;
GRANT EXECUTE ON FUNCTION public.match_agent_memories TO anon, authenticated, service_role;
