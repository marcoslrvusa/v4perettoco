-- SQL de verificação das tabelas no schema proanalises
-- Execute no Supabase SQL Editor para confirmar que as tabelas existem
-- ===================================================

SELECT table_name, table_type FROM information_schema.tables 
WHERE table_schema = 'proanalises' ORDER BY table_name;
