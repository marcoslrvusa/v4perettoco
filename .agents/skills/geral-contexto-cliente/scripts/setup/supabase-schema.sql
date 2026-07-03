-- ============================================================
-- geral-contexto-cliente — Schema pgvector para contexto de cliente
-- Execute no SQL Editor do Supabase (uma vez)
-- ============================================================

-- 1. Habilitar pgvector (se já não estiver)
CREATE EXTENSION IF NOT EXISTS vector WITH SCHEMA extensions;

-- 2. Tabela de contexto dos clientes
CREATE TABLE IF NOT EXISTS public.client_context (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  client      TEXT NOT NULL,
  squad       TEXT,

  -- Campos estruturados principais
  tom_de_voz  TEXT,
  historico   TEXT,
  oferta      TEXT,

  -- Fatos extras chave-valor (segmento, público, diferenciais, canais, etc.)
  facts       JSONB DEFAULT '{}'::jsonb,

  -- Embedding para busca semântica (concatenado de todos os campos textuais)
  embedding   VECTOR(1536),

  -- Metadados
  source      TEXT DEFAULT 'manual',
  updated_at  TIMESTAMPTZ DEFAULT now(),
  created_at  TIMESTAMPTZ DEFAULT now(),

  UNIQUE(client)
);

-- 3. Índice IVFFlat para busca por similaridade
CREATE INDEX IF NOT EXISTS idx_client_context_embedding
  ON public.client_context
  USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);

-- 4. Índices para filtros comuns
CREATE INDEX IF NOT EXISTS idx_client_context_client
  ON public.client_context (client);
CREATE INDEX IF NOT EXISTS idx_client_context_squad
  ON public.client_context (squad);

-- 5. Função de busca por similaridade
CREATE OR REPLACE FUNCTION public.match_client_context(
  query_embedding VECTOR(1536),
  match_threshold FLOAT DEFAULT 0.7,
  match_count     INT DEFAULT 5,
  filter_client   TEXT DEFAULT NULL,
  filter_squad    TEXT DEFAULT NULL
)
RETURNS TABLE(
  id            UUID,
  client        TEXT,
  squad         TEXT,
  tom_de_voz    TEXT,
  historico     TEXT,
  oferta        TEXT,
  facts         JSONB,
  source        TEXT,
  similarity    FLOAT,
  updated_at    TIMESTAMPTZ,
  created_at    TIMESTAMPTZ
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    cc.id,
    cc.client,
    cc.squad,
    cc.tom_de_voz,
    cc.historico,
    cc.oferta,
    cc.facts,
    cc.source,
    1 - (cc.embedding <=> query_embedding) AS similarity,
    cc.updated_at,
    cc.created_at
  FROM public.client_context cc
  WHERE
    1 - (cc.embedding <=> query_embedding) > match_threshold
    AND (filter_client IS NULL OR cc.client = filter_client)
    AND (filter_squad IS NULL OR cc.squad = filter_squad)
  ORDER BY cc.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;

-- 6. Função para fazer upsert (insert or update on conflict client)
CREATE OR REPLACE FUNCTION public.upsert_client_context(
  p_client      TEXT,
  p_squad       TEXT DEFAULT NULL,
  p_tom_de_voz  TEXT DEFAULT NULL,
  p_historico   TEXT DEFAULT NULL,
  p_oferta      TEXT DEFAULT NULL,
  p_facts       JSONB DEFAULT '{}'::jsonb,
  p_embedding   VECTOR(1536) DEFAULT NULL,
  p_source      TEXT DEFAULT 'manual'
)
RETURNS UUID
LANGUAGE plpgsql
AS $$
DECLARE
  v_id UUID;
BEGIN
  INSERT INTO public.client_context (client, squad, tom_de_voz, historico, oferta, facts, embedding, source)
  VALUES (p_client, p_squad, p_tom_de_voz, p_historico, p_oferta, p_facts, p_embedding, p_source)
  ON CONFLICT (client)
  DO UPDATE SET
    squad       = COALESCE(p_squad, client_context.squad),
    tom_de_voz  = COALESCE(p_tom_de_voz, client_context.tom_de_voz),
    historico   = COALESCE(p_historico, client_context.historico),
    oferta      = COALESCE(p_oferta, client_context.oferta),
    facts       = client_context.facts || p_facts,
    embedding   = COALESCE(p_embedding, client_context.embedding),
    source      = p_source,
    updated_at  = now()
  RETURNING id INTO v_id;

  RETURN v_id;
END;
$$;

-- 7. RLS
ALTER TABLE public.client_context ENABLE ROW LEVEL SECURITY;

CREATE POLICY "client_context_select_anon"
  ON public.client_context
  FOR SELECT
  TO anon
  USING (true);

CREATE POLICY "client_context_insert_service"
  ON public.client_context
  FOR INSERT
  TO service_role
  WITH CHECK (true);

CREATE POLICY "client_context_update_service"
  ON public.client_context
  FOR UPDATE
  TO service_role
  USING (true)
  WITH CHECK (true);

-- 8. Conceder acesso à Data API
GRANT USAGE ON SCHEMA public TO anon, authenticated, service_role;
GRANT SELECT ON TABLE public.client_context TO anon, authenticated, service_role;
GRANT INSERT, UPDATE ON TABLE public.client_context TO service_role;
GRANT EXECUTE ON FUNCTION public.match_client_context TO anon, authenticated, service_role;
GRANT EXECUTE ON FUNCTION public.upsert_client_context TO service_role;
