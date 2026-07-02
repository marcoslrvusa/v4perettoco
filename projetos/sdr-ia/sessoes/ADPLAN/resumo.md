# ADPLAN — SDR IA

## Problemas encontrados

### 🔴 Roteamento de leads não qualificados (Ajuste 2)
Create new leads1 (caminho não qualificado/contato existe) apontava para **Funil V4 / MQL** em vez de **Funil SDR IA / não qualificados**. Lead não qualificado com contato pré-existente caía como MQL.
- **Correção:** pipeline 11068075 → 13421772, status 84910015 → 106897256, tag 102360 removida
- Create new leads3: tag 102360 removida

### 🔴 SDR IA parou de responder (Ajuste 3)
Escrita de `status_resposta` no CreateUser (caminho crítico ANTES da IA responder) derrubava execução quando a coluna não existia ou dava erro transitório.
- **Correção:** Todo Ajuste 3 removido do fluxo n8n
- Campo `status_resposta` mantido por **trigger SQL no banco** — backfill + trigger automático
- SQL: `UPDATE adplan_leads SET status_resposta = 'Respondeu' WHERE EXISTS (SELECT 1 FROM adplan_chat_history h WHERE h."sessionID" = session_id AND h.role = 'human')`

### 🔴 Execução travando ~20-25 min
Code JS2/JS3: timeout de 300s no task runner × retryOnFail maxTries=5 = 25 min
- **Correção:** retryOnFail removido (corta para no máximo 300s)

### 🟡 Switch: "last can't be used on null value"
Buffer (Redis Obtem) retorna null → `.last()` e `.length` sem safe access
- **Correção:** `?.` adicionado; rightValue do debouncerTime com `?.` + fallback `|| 5`

### 🟡 Responde texto x4: Invalid expression
`$('camposIniciais').item.json...` sem `?.`
- **Correção:** safe access + `=number` → `number` no nome do parâmetro

### 🟡 HTTP Request1: 404 (PATCH Kommo)
`$json.id` vazio → `/leads/undefined`
- **Decisão:** nó deletado (update do Kommo removido)

### 🟡 Filtro Lovable "tudo Respondeu"
Dev perdeu correlação `session_id` na query derivada do chat_history
- **Correção:** `WHERE h.session_id = l."sessionID" AND h.role = 'human'`

## Pendências
- Restaurar PATCH do Kommo se necessário
- Verificar task runner do servidor (timeout residual 300s)

## Status: ✅ Versão estável publicada (22/jun) — 165 nodes
