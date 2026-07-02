-- =============================================
-- Fix: expor schema proanalises à Supabase Data API
-- Rode TUDO de uma vez no SQL Editor
-- =============================================

GRANT USAGE ON SCHEMA proanalises TO anon, authenticated;
GRANT SELECT ON ALL TABLES IN SCHEMA proanalises TO anon, authenticated;
ALTER DEFAULT PRIVILEGES IN SCHEMA proanalises GRANT SELECT ON TABLES TO anon, authenticated;

CREATE POLICY "proanalises_select_anon" ON proanalises.dados_cliente
  FOR SELECT USING (true);

CREATE POLICY "proanalises_select_anon" ON proanalises.leads_mql
  FOR SELECT USING (true);

CREATE POLICY "proanalises_select_anon" ON proanalises.followup_clientes
  FOR SELECT USING (true);
