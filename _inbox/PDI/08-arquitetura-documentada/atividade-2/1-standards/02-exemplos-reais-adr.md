# Exemplos Reais Comentados (resumos, textos integrais em 2-implementacao)

## ADR-001: n8n como orquestrador (Aceita, Implementada)

Contexto real: em marco de 2026 a operacao rodava automacoes em scripts soltos e planilhas, sem retry nem visibilidade. Alternativas: fila propria em Python (potente, mas 3 semanas de obra sem UI) e planilha com Apps Script (gratis, mas sem log nem retry). Decisao: n8n self-hosted na VPS, workers Python para o pesado. Consequencia monitorada: taxa de falha de coleta por conta, alerta se passar de 5 por cento na janela de 24h.

## ADR-002: Supabase Postgres como estado (Aceita, Implementada)

Contexto real: estado de coleta morava em abas de planilha editadas a mao, com sobrescrita e sem historico. Alternativas: SQLite local (simples, mas sem acesso concorrente do painel) e planilha (zero obra, mas sem integridade). Decisao: Supabase Postgres com tabelas `coletas`, `erros` e `contas`. Consequencia monitorada: linhas na fila de erros por dia e tempo de resolucao.

## O que esses exemplos ensinam

- Bom contexto traz numero (3 semanas de obra, 5 por cento de falha), nao adjetivo.
- Alternativa descartada sempre com motivo de uma linha, sem julgamento moral.
- Consequencia sempre com metrica observavel, senao o ADR vira declaracao de intencao.
