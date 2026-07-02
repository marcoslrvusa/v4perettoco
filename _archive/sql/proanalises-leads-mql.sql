-- DDL da tabela leads_mql para o schema proanalises
-- Execute UMA VEZ no Supabase SQL Editor antes de ativar o workflow
-- ===================================================

CREATE TABLE IF NOT EXISTS proanalises.leads_mql (
  id BIGSERIAL PRIMARY KEY,
  session_id TEXT UNIQUE NOT NULL,
  telefone TEXT,
  nome TEXT,
  classification TEXT,
  exames_interesse TEXT,
  convenio TEXT,
  urgencia TEXT,
  motivo_handoff TEXT,
  qualification_reason TEXT,
  last_context TEXT DEFAULT '',
  mql BOOLEAN DEFAULT false,
  handoff BOOLEAN DEFAULT false,
  encerrado BOOLEAN DEFAULT false,
  lead_created_in_kommo BOOLEAN DEFAULT false,
  kommo_lead_id TEXT,
  followup_24h_enabled BOOLEAN DEFAULT true,
  followup_24h_sent BOOLEAN DEFAULT false,
  followup_24h_sent_at TIMESTAMPTZ,
  last_interaction_at TIMESTAMPTZ,
  stop_reason TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
