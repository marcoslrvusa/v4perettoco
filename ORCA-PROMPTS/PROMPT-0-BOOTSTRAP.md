# PROMPT 0 — FASE 0 + CONTRATOS (Cole no ORCA aberto no worktree `contracts`)

> Os 4 worktrees já foram criados pela UI do ORCA (opção "Name"). Seu trabalho NÃO é criar worktrees nem copiar seeds — é só validar os modelos e escrever os contratos compartilhados.

Você é o agente de BOOTSTRAP do projeto HUB TÁTICO OPERACIONAL V4, na branch `integration/contracts`. Leia primeiro: `Harness Engineering/PLANO-MESTRE-HUB-TATICO-V4.md` (seções 5 e 12) e `Harness Engineering/ORCA-WORKTREES-SETUP.md`.

## TAREFA ÚNICA: FASE 0 + Contratos

### 1. Validar slugs de modelos (BLOQUEANTE — requests reais)

Peça ao usuário (interativamente) as env vars que faltarem: `ZEN_API_BASE`, `ZEN_API_KEY`, `GEMINI_API_KEY`.

```bash
# 1a. Testar ox-alpha-free no OpenCode Zen
curl -s "$ZEN_API_BASE/chat/completions" -H "Authorization: Bearer $ZEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"ox-alpha-free","messages":[{"role":"user","content":"ping"}],"max_tokens":5}'

# 1b. Se falhar, listar catálogo Zen e testar variações até achar o slug exato
curl -s "$ZEN_API_BASE/models" -H "Authorization: Bearer $ZEN_API_KEY"

# 1c. Validar gemini-2.5-flash free tier
curl -s "https://generativelanguage.googleapis.com/v1beta/models?key=$GEMINI_API_KEY"
```

Se algum slug não responder OK, PARE e reporte ao usuário antes de seguir.

### 2. Escrever os contratos (nesta pasta, raiz do worktree)

**model-slugs.json** (com slugs CONFIRMADOS no passo 1):
```json
{
  "primary_route1": "<slug zen validado>",
  "primary_route1_provider": {"api_base": "<ZEN_API_BASE>", "key_env": "ZEN_API_KEY", "rpm": 20},
  "primary_route2": "gemini/gemini-2.5-flash",
  "primary_route2_provider": {"key_env": "GEMINI_API_KEY", "rpm": 12},
  "structured": "<slug zen validado>",
  "fallback": "gpt-4o-mini",
  "fallback_provider": {"key_env": "OPENAI_API_KEY", "rpm": 300}
}
```

**litellm-keys.json**: `["squad-csm","squad-gt","squad-copy","squad-design","squad-account","squad-coord","ops-n8n"]`

**qdrant-collections.json**: collections `skills`, `runs`, `clients`, `okr_pace`, `transcripts` — vector_size conforme embedding escolhido (1536 OpenAI / 384 MiniLM — documente qual), quantization scalar, hnsw m=16 ef=64, on_disk true

**ekyte-workspace-map.json**: `{"fallback_workspace": "16032"}` (usuário preencherá os IDs depois)

**pace-schema.sql**: copie fielmente o schema SQL das seções 3 e 8 do PLANO-MESTRE-HUB-TATICO-V4.md (okr_pace_snapshots com view em created_at, matriz_operacional com RLS, okr_pace_monthly_agg, extensões agent_queue com idempotency_key UNIQUE)

**api-endpoints.yaml**: os 6 endpoints listados em ORCA-WORKTREES-SETUP.md → AGENTE A2 (okr-pace, csm-review GET/POST comment, coordinator approve, queue, memory search), com request/response schemas

### 3. Commitar
```bash
git add -A && git commit -m "chore(contracts): fase 0 ok — slugs validados + contratos base"
```

### 4. Relatório final ao usuário
- [ ] Slugs validados (listar exatamente quais) OU falha (parar e reportar)
- [ ] 6 arquivos de contrato criados e commitados
- Próximo passo: abrir as abas ORCA nos worktrees infra-n8n / dashboard-api / data-agents e colar PROMPT-A1/A2/A3

## Regras rígidas
- NÃO commite nada fora desta branch
- NUNCA escreva API keys/tokens em arquivos versionados — só nomes de env vars
