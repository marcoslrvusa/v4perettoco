# PROMPT 0 — BOOTSTRAP (Cole num agente ORCA aberto na raiz do repo)

Você é o agente de BOOTSTRAP do projeto HUB TÁTICO OPERACIONAL V4. Seu único trabalho é preparar o ambiente para 3 agentes paralelos trabalharem em worktrees git. NÃO desenvolva nada além do descrito aqui.

## Contexto
- Repo: /home/marcos/Desktop/v4perettoco-main (branch atual: main, tag hub-base-v1)
- Objetivo final do projeto: Hub tático em ia.fvmarketing.com.br (ver docs: Harness Engineering/PLANO-MESTRE-HUB-TATICO-V4.md e ORCA-WORKTREES-SETUP.md — LEIA OS DOIS ANTES DE COMEÇAR)

## Tarefas (nesta ordem)

### 1. Criar branches + worktrees
```bash
cd /home/marcos/Desktop/v4perettoco-main
git checkout -b ws1/infra-n8n 2>/dev/null || git checkout ws1/infra-n8n && git checkout main
git checkout -b ws2/dashboard-api 2>/dev/null || git checkout ws2/dashboard-api && git checkout main
git checkout -b ws3/data-agents 2>/dev/null || git checkout ws3/data-agents && git checkout main
git checkout -b integration/contracts 2>/dev/null || git checkout integration/contracts && git checkout main

git worktree add ../orca-infra-n8n ws1/infra-n8n
git worktree add ../orca-dashboard-api ws2/dashboard-api
git worktree add ../orca-data-agents ws3/data-agents
git worktree add ../orca-contracts integration/contracts
git worktree list   # valide: 4 worktrees + main
```

### 2. Copiar seeds (APENAS o que existe)
```bash
cp -r workflows/producao ../orca-infra-n8n/
cp -r projetos/pia-saas/dashboard ../orca-dashboard-api/
cp -r projetos/pia-saas/rotinas ../orca-data-agents/
```

### 3. FASE 0 — Validar slugs de modelos (BLOQUEANTE)
Peça ao usuário (se ainda não estiverem no ambiente) e valide com requests REAIS:
```bash
export ZEN_API_BASE="<pergunte ao usuário se faltar>"   # endpoint OpenCode Zen (openai-compatible)
export ZEN_API_KEY="<pergunte ao usuário se faltar>"
export GEMINI_API_KEY="<pergunte ao usuário se faltar>"

curl -s "$ZEN_API_BASE/chat/completions" -H "Authorization: Bearer $ZEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"ox-alpha-free","messages":[{"role":"user","content":"ping"}],"max_tokens":5}'

curl -s "https://generativelanguage.googleapis.com/v1beta/models?key=$GEMINI_API_KEY" | head -50
```
Se `ox-alpha-free` falhar, teste variações de slug no catálogo (`$ZEN_API_BASE/models`) até confirmar o slug exato.

### 4. Escrever contratos compartilhados (worktree ../orca-contracts/)
Crie estes arquivos:

**model-slugs.json** (com os slugs CONFIRMADOS no passo 3):
```json
{
  "primary_route1": "<slug zen validado>",
  "primary_route1_provider": {"api_base": "<ZEN_API_BASE>", "key_env": "ZEN_API_KEY"},
  "primary_route2": "gemini/gemini-2.5-flash",
  "primary_route2_provider": {"key_env": "GEMINI_API_KEY", "rpm": 12},
  "structured": "<slug zen validado>",
  "fallback": "gpt-4o-mini",
  "fallback_provider": {"key_env": "OPENAI_API_KEY"}
}
```

**litellm-keys.json**: `["squad-csm","squad-gt","squad-copy","squad-design","squad-account","squad-coord","ops-n8n"]`

**qdrant-collections.json**: collections `skills`, `runs`, `clients`, `okr_pace`, `transcripts` (vector_size 1536, quantization scalar, hnsw m=16 ef=64, on_disk true)

**ekyte-workspace-map.json**: `{}` vazio + `"fallback_workspace": "16032"` (usuário preencherá depois)

**pace-schema.sql** e **api-endpoints.yaml**: copie das seções 3 e do documento ORCA-WORKTREES-SETUP.md (aba AGENTE A2 lista os 8 endpoints)

Committe em integration/contracts: `git add -A && git commit -m "chore(contracts): slugs validados + contratos base"`

### 5. Relatório final
Informe ao usuário:
- [ ] 4 worktrees criados (listar caminhos)
- [ ] Seeds copiados
- [ ] Slugs validados (quais exatamente) ou FALHA (parar e reportar)
- [ ] Contratos escritos e commitados
- Próximo passo para o usuário: abrir 3 abas ORCA nas pastas ../orca-infra-n8n, ../orca-dashboard-api, ../orca-data-agents e colar os prompts A1/A2/A3

## Regras rígidas
- NÃO commite nada na main
- NÃO commite arquivos .xlsx, senhas, API keys ou tokens em qualquer arquivo versionado
- Se um comando falhar, corrija e siga; se for bloqueante, PARE e reporte
