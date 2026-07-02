-- =============================================
-- Fix: expor schema genics à Supabase Data API
-- Rode TUDO de uma vez no SQL Editor
-- =============================================

-- 1. Permissão de schema pras roles da API
GRANT USAGE ON SCHEMA genics TO anon, authenticated;

-- 2. SELECT em todas as tabelas existentes
GRANT SELECT ON ALL TABLES IN SCHEMA genics TO anon, authenticated;

-- 3. Default pra tabelas futuras
ALTER DEFAULT PRIVILEGES IN SCHEMA genics GRANT SELECT ON TABLES TO anon, authenticated;

-- 4. Policies de SELECT (obrigatório porque RLS está habilitado)
CREATE POLICY "genics_select_anon" ON genics.dados_cliente
  FOR SELECT USING (true);

CREATE POLICY "genics_select_anon" ON genics.leads_mql
  FOR SELECT USING (true);
