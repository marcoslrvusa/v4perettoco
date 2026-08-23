# ORCA Worktrees Setup — Plano 6h (v2)

## ⚡ FLUXO SEM TERMINAL (recomendado)

### Passo A — Criar os 4 worktrees na UI do ORCA
No diálogo **Create Worktree**: Project = `v4perettoco-main` · Run on = local linux · Create from = **Name** · Start-from = `main`.
No drawer **Advanced**, preencha o Branch name exato:

| # | Name | Branch name (Advanced) | Prompt depois |
|---|------|------------------------|---------------|
| 1 | `infra-n8n` | `ws1/infra-n8n` | PROMPT-A1 |
| 2 | `dashboard-api` | `ws2/dashboard-api` | PROMPT-A2 |
| 3 | `data-agents` | `ws3/data-agents` | PROMPT-A3 |
| 4 | `contracts` | `integration/contracts` | PROMPT-0 |

> Não use "Branch"/"GitHub"/"Smart" — as branches ainda não existem e nada há no remoto. Docs/seeds já estão commitados na main: os worktrees nascem completos, **sem copiar nada**.

### Passo B — Rodar os prompts nas abas ORCA

| Ordem | Arquivo de prompt | Aba ORCA onde colar | O que o agente faz |
|-------|-------------------|---------------------|--------------------|
| 1º | `ORCA-PROMPTS/PROMPT-0-BOOTSTRAP.md` | Aba do worktree `contracts` | FASE 0 (valida slugs com request real) + escreve os 6 contratos |
| 2º | `ORCA-PROMPTS/PROMPT-A1-INFRA-N8N.md` | Aba do worktree `infra-n8n` | Compose, LiteLLM config, Pace Calculator, CSM→Coord→Ekyte |
| 3º | `ORCA-PROMPTS/PROMPT-A2-DASHBOARD-API.md` | Aba do worktree `dashboard-api` | FastAPI 6 endpoints + HTML V4 6 abas + nginx |
| 4º | `ORCA-PROMPTS/PROMPT-A3-DATA-AGENTS.md` | Aba do worktree `data-agents` | Migrations (matriz+pace, RLS), syncs manuais, Qdrant, 2 agentes |

**Sequência:** PROMPT-0 primeiro (gera `model-slugs.json` que A1/A3 consomem) → depois A1/A2/A3 em paralelo. Prompts autocontidos: cada agente lê os docs da própria pasta e pergunta a você apenas env vars faltantes.

---

> **Rev. v2** — incorpora correções da análise técnica: slugs de modelo validados na FASE 0 (`ox-alpha-free` do OpenCode Zen substitui `mimo-v2.5-free`/`qwen3-coder`), sintaxe LiteLLM correta, cálculos L1-L4 determinísticos em código, lock anti-overlap no cron, idempotência Ekyte, compose só com serviços novos.
>
> **Stack de modelos (100% free tier primeiro):** `primary` = **ox-alpha-free** (Zen) → failover Gemini free · `structured` = **ox-alpha-free** (Zen) · `fallback`/críticos N8N = gpt-4o-mini (credencial já existente, só overflow)

## FASE 0 — Validar Modelos (VOCÊ roda antes de abrir o ORCA — 15min)

```bash
# 1. Slugs reais disponíveis
curl -s https://openrouter.ai/api/v1/models | jq -r '.data[].id' | grep -i free

# 2. Catálogo OpenCode Zen + teste ox-alpha-free (ajuste ZEN_API_BASE)
export ZEN_API_BASE="https://zen.opencode.ai/v1"   # confirmar URL real
export ZEN_API_KEY="<sua-key-zen>"
curl -s "$ZEN_API_BASE/models" -H "Authorization: Bearer $ZEN_API_KEY" | jq
curl -s "$ZEN_API_BASE/chat/completions" -H "Authorization: Bearer $ZEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"ox-alpha-free","messages":[{"role":"user","content":"ping"}],"max_tokens":5}'
```

✅ Só siga se ambos responderem OK. Anote os slugs exatos e cole nas instruções dos agentes.

---

## Estrutura de Worktrees

| Worktree           | Branch                  | Pasta Local             | Agente     | Foco                                                  |
| ------------------ | ----------------------- | ----------------------- | ---------- | ----------------------------------------------------- |
| `orca-infra-n8n`   | `ws1/infra-n8n`         | `../orca-infra-n8n`     | **A1**     | Docker Compose, LiteLLM 7 keys, Qdrant, N8N workflows |
|                    | `ws2/dashboard-api`     | `../orca-dashboard-api` | **A2**     | FastAPI (6 endpoints), HTML V4 (6 abas), Auth         |
| `orca-data-agents` | `ws3/data-agents`       | `../orca-data-agents`   | **A3**     | Migrations SQL, Sync scripts, Qdrant ingest, 2 Agents |
| `orca-contracts`   | `integration/contracts` | `../orca-contracts`     | **Shared** | API spec, LiteLLM keys, Qdrant collections, Ekyte map |

---

## Comandos de Criação (Execute na raiz do repo)

### Passo 0 — Base identificada na `main` (worktrees só herdam commitado)

```bash
cd /home/marcos/Desktop/v4perettoco-main

git add "Harness Engineering/" ORCA-WORKTREES-SETUP.md
git commit -m "docs(hub): plano v2.3 — matriz no PRODUTO, sync manual, modelos free-first"
git tag -a hub-base-v1 -m "Base para worktrees ORCA — HUB Tático 6h"
```

A tag `hub-base-v1` é a âncora: todos os worktrees nascem deste estado identificado.

### Passo 1 — Branches + Worktrees

```bash
# 1. Branches
git checkout -b ws1/infra-n8n 2>/dev/null || git checkout ws1/infra-n8n
git checkout main
git checkout -b ws2/dashboard-api 2>/dev/null || git checkout ws2/dashboard-api
git checkout main
git checkout -b ws3/data-agents 2>/dev/null || git checkout ws3/data-agents
git checkout main
git checkout -b integration/contracts 2>/dev/null || git checkout integration/contracts
git checkout main

# 2. Worktrees (já nascem com os docs da hub-base-v1 dentro)
git worktree add ../orca-infra-n8n ws1/infra-n8n
git worktree add ../orca-dashboard-api ws2/dashboard-api
git worktree add ../orca-data-agents ws3/data-agents
git worktree add ../orca-contracts integration/contracts

# Confirmação
git worktree list

# 3. Seeds — APENAS o que já existe no repo
cp -r workflows/producao ../orca-infra-n8n/
cp -r projetos/pia-saas/dashboard ../orca-dashboard-api/
cp -r projetos/pia-saas/rotinas ../orca-data-agents/

# NOTA: docker-compose.hub.yml, migrations/, agents/*.md, dashboard-api/main.py são
# ENTREGÁVEIS criados pelos agentes (Seção 14 do Plano Mestre) — não existem como seed.
# A planilha governança NÃO vai pro repo: o agente A3 recebe o caminho via env
# MATRIZ_XLSX_PATH (instrução no prompt dele).

# 4. Contratos (crie os arquivos em orca-contracts/)
# api-endpoints.yaml, litellm-keys.json, model-slugs.json (saída da FASE 0),
# qdrant-collections.json, ekyte-workspace-map.json, pace-schema.sql
```

---

## Instruções por Agente (Cole no ORCA)

### AGENTE A1 — Infra & N8N (`../orca-infra-n8n`)

**Arquivos alvo:**
- `docker-compose.hub.yml` — **SOMENTE serviços novos**: `qdrant`, `dashboard-api`, `sync-worker`. Rede `external: true` apontando para a rede Dokploy existente. **NÃO duplicar** N8N/LiteLLM/OpenCode (já rodam no Dokploy — referenciar por URL)
- `litellm-config.yaml` — **primary = grupo de 2 deployments free** (ox-alpha-free/Zen rota 1 → Gemini free tier rota 2, failover automático) + `structured`=ox-alpha-free + `fallback`=gpt-4o-mini (só overflow) + 7 virtual keys squad + **sintaxe correta**:
  ```yaml
  model_list:
    - model_name: primary                    # rota 1: Ox Alpha Free via Zen (principal)
      litellm_params: { model: openai/ox-alpha-free, api_key: os.environ/ZEN_API_KEY, api_base: os.environ/ZEN_API_BASE, rpm: 20 }
    - model_name: primary                    # rota 2: MESMO nome = grupo c/ failover interno
      litellm_params: { model: gemini/gemini-2.5-flash, api_key: os.environ/GEMINI_API_KEY, rpm: 12 }
    - model_name: structured                 # JSON estrito (volume baixo, ok na janela Zen)
      litellm_params: { model: openai/ox-alpha-free, api_key: os.environ/ZEN_API_KEY, api_base: os.environ/ZEN_API_BASE, rpm: 20 }
    - model_name: fallback                   # críticos N8N + rede final (só overflow)
      litellm_params: { model: gpt-4o-mini, api_key: os.environ/OPENAI_API_KEY, rpm: 300 }

  router_settings:
    routing_strategy: "latency-based-routing"
    num_retries: 2
    fallbacks:
      primary: ["fallback"]
      structured: ["fallback"]

  general_settings: { cache: true }
  litellm_settings:
    cache_params: { type: semantic, similarity_threshold: 0.85, ttl: 3600 }
    embedding_model: gemini/gemini-embedding
  ```
  > 🛡️ **Proteção da janela Zen (2000 req/5h compartilhada) sem gastar nada:** cálculos L1-L4 são Code node (LLM só interpreta), cache semântico absorve repetidos, e frequência adaptativa no pace — **15min se cliente 🟡/🔴, 1h se 🟢**. Overflow cai no gpt-4o-mini automaticamente.
- `n8n-workflows/pace-calculator.json` — Cron 15min com:
  - **Node 1 = lock anti-overlap:** `SELECT pg_try_advisory_lock(918273645)` → se false, STOP
  - **Node 2 = lista de clientes** de `PRODUTO.matriz_operacional WHERE status='Ativo'` (squad + okr_type + ekyte_workspace_id)
  - **L1-L4 em Code node (determinístico):** L1 aritmética; L2 regressão linear fórmula fechada; L4 Monte Carlo em JS/Python com seed fixo. **LLM NUNCA calcula números** — gpt-4o-mini só interpreta `{L1..L4}` e redige `causa_raiz` + `recommended_actions[]`. Dados de OKR/Ads/CRM vêm do DADOS
  - Frequência adaptativa (opcional B3): 15min se 🟡/🔴, 1h se 🟢
  - Timeout run 5min; se falhar 2x seguidas → GChat alerta
- `n8n-workflows/csm-coordinator-sync.json` — Webhook → CSM comment → Coordinator approve → Ekyte project+tasks **idempotente** (`agent_queue.id` como external_ref UNIQUE — duplo clique não duplica)
- `n8n-workflows/flag-diagnostics.json` (stub) · `execute-action.json` (stub)
- **Patch workflow existente:** `[PIA] Agente de Tráfego` — trocar modelo do node "Chamar LLM": `mimo-v2.5-free` → `ox-alpha-free`
- `nginx/ia.fvmarketing.com.br.conf` — Proxy `/api` → dashboard-api:8000 · `/opencode` → gateway Dokploy existente

**Credenciais necessárias (env):**
- `SUPABASE_DADOS_URL`, `SUPABASE_DADOS_KEY` (mhntycubvywjszweeuxs)
- `SUPABASE_URL`, `SUPABASE_SERVICE_KEY` (bkenzsvexfayjcrqnmpx)
- `GEMINI_API_KEY`, `OPENAI_API_KEY`, `ZEN_API_BASE`, `ZEN_API_KEY`
- `HUB_SHARED_TOKEN` · `GCHAT_SPACE_ID/KEY/TOKEN` (placeholder ok) · `EKYTE_MCP_TOKEN` por squad

---

### AGENTE A2 — Dashboard & API (`../orca-dashboard-api`)

**Arquivos alvo:**
- `dashboard-api/main.py` — FastAPI com 6 endpoints + middleware `X-Hub-Token` que **mapeia token → usuário → função** (CSM vê só comentar; Coordinator aprova — a UI esconde/mostra ações conforme função)
- `dashboard/index.html` — HTML único V4 visual (6 abas), vanilla JS, CSS Barlow Condensed
- `nginx/ia.fvmarketing.com.br.conf` — Proxy `/api` → dashboard-api:8000, `/` → index.html, `/opencode` → gateway Dokploy existente

**6 Endpoints (conforme `api-endpoints.yaml`):**
1. `GET /api/okr-pace?client={id}` → `v_okr_pace_latest`
2. `GET /api/csm-review/{queue_id}` → `agent_queue`
3. `POST /api/csm-review/{queue_id}/comment` → atualiza `csm_comment`
4. `POST /api/coordinator/{queue_id}/approve` → chama N8N webhook
5. `GET /api/queue?status=pending` → lista queue
6. `GET /api/memory/search?q={query}` → Qdrant search

**6 Abas Dashboard:**
1. **OKR PACE** — Grid cards (cliente, semáforo overall, 4 badges L1-L4, botão "CSM Review")
2. **CSM REVIEW** — Lista `awaiting_csm_comment`, textarea + botão "Enviar"
3. **FLAGS ATIVAS** — Queue type `flag_%`
4. **QUEUE AUTÔNOMA** — Filtros status/prioridade/squad
5. **MEMORY/RAG** — Busca semântica Qdrant
6. **AGENTS** — Iframe `https://opencode.fvmarketing.com.br?token={HUB_SHARED_TOKEN}`

---

### AGENTE A3 — Data & Agents (`../orca-data-agents`)

**Arquivos alvo:**
- `migrations/produto_okr_pace.sql` — `okr_pace_snapshots` (view usa `created_at`, NÃO `snapshot_time`) + **`matriz_operacional`** (cliente PK, squad, okr_type, ekyte_workspace_id, status, account_email, raw JSONB, RLS) + **RLS dia 1** em todas as tabelas novas + `okr_pace_monthly_agg` + extensões `agent_queue` (`csm_comment TEXT`, `coordinator_decision JSONB`, `ekyte_project_id UUID`, `idempotency_key UNIQUE`)
- `scripts/sync_matriz_operacional.py` — **MANUAL** (planilha muda mensal; sem cron no MVP). Lê caminho via env `MATRIZ_XLSX_PATH`; introspeciona colunas (heurística `okr_type`/`tipo_okr`) + config JSON editável; upsert idempotente em **`PRODUTO.matriz_operacional`**; output `{inseridos, atualizados, sem_okr_type, workspace_fallback_warning}`. Repo recebe só script + `matriz-column-map.json` + fixture anonimizada (**xlsx real fora do git**)
- `scripts/sync_pessoas.py` — Planilha aba `DB_Pessoas_Atualizado` → `PRODUTO.DB_Pessoas_Atualizado`
- `scripts/map_ekyte_workspace.py` → lê `matriz_operacional` → gera `ekyte-workspace-map.json` (**warning log** quando cair no fallback `16032`)
- `scripts/ingest_qdrant.py` — Skills (65) + Runs (90d) + OKR snapshots → Qdrant + job de snapshot diário do Qdrant para volume
- `agents/okr-pace-analyzer.md` — OpenCode agent, model: **`primary`** (ox-alpha-free → Gemini free). Recebe L1-L4 JÁ CALCULADOS em código; nunca calcula números
- `agents/action-planner.md` — OpenCode agent, model: **`primary`**

**Agentes OpenCode (registrar em `.opencode/agents/`):**
- `@okr-pace-analyzer` → Input: `{client_id, pace_snapshot: {L1..L4 numéricos}, client_kb}` → Output: `{causa_raiz, pilares_deficientes, recommended_actions[]}` (só interpretação)
- `@action-planner` → Input: `{semaforo, gaps, client_context}` → Output: `actions[funcao, acao, prazo, dono, evidencia]`

**Credenciais/env adicionais (A3):**
```bash
export MATRIZ_XLSX_PATH="/home/marcos/Desktop/Infraestrutura/hub-agentes-ia/projetos/pia-saas/docs/[TECH] Hub de Agentes de IA  _ Gestão e Governança (1).xlsx"
export SUPABASE_URL="https://bkenzsvexfayjcrqnmpx.supabase.co"   # sync escreve AQUI (PRODUTO)
export SUPABASE_SERVICE_KEY="<service-role>"
```

---

### CONTRATOS (Shared — `../orca-contracts`)

Crie estes arquivos **antes** dos agentes começarem:

| Arquivo | Conteúdo |
|---------|----------|
| `api-endpoints.yaml` | 8 endpoints com request/response schemas (inclui campo `user_funcao` no auth p/ CSM vs Coordinator) |
| `litellm-keys.json` | 7 keys: `squad-csm`, `squad-gt`, `squad-copy`, `squad-design`, `squad-account`, `squad-coord`, `ops-n8n` |
| `model-slugs.json` | **Saída da FASE 0**: slugs exatos validados (`gemini-2.5-flash`, `ox-alpha-free`, `gpt-4o-mini`) + `ZEN_API_BASE` confirmado |
| `qdrant-collections.json` | Collections: `skills`, `runs`, `clients`, `okr_pace`, `transcripts` (vector_size: 1536, quantization scalar) |
| `ekyte-workspace-map.json` | `{ "squad-gt": "workspace_id", "cliente-x": "workspace_id" }` + fallback `16032` |
| `pace-schema.sql` | `okr_pace_snapshots` (view com `created_at`), RLS, `okr_pace_monthly_agg`, extensões `agent_queue` com `idempotency_key UNIQUE` |

---

## Cronograma 6h (Blocos 90min)

| Bloco | Horário | A1 (Infra/N8N) | A2 (Dashboard/API) | A3 (Data/Agents) | Você |
|-------|---------|----------------|--------------------|------------------|------|
| **FASE 0** | -15min a 0:00 | — | — | — | Valida slugs (`gemini-2.5-flash`, `ox-alpha-free`) e cola em `model-slugs.json` |
| **Setup** | 0:00-0:30 | Compose (só novos) + LiteLLM config v2 | FastAPI skeleton + auth token→função | Migrations (RLS+retention) + sync scripts | Cria worktrees + contratos |
| **B1** | 0:30-2:00 | Pace Calculator (lock + Code node determinístico) | 6 Endpoints | Qdrant ingest + backup job | Monitora |
| **Sync 1** | 2:00-2:15 | Teste Pace→Queue (+ teste lock: 2 runs simultâneas = 1 processa) | Teste GET /okr-pace | Verifica Qdrant + SQL | Valida integração |
| **B2** | 2:15-3:45 | CSM→Coord→Ekyte (idempotente) + patch mimo→ox-alpha-free no Tráfego | HTML V4 6 abas | Agents stubs (`primary`/`structured`) | |
| **Sync 2** | 3:45-4:00 | Teste duplo-clique Aprovar = 1 sprint só | Teste CSM Review aba | Teste Agents via API | Valida fluxo completo |
| **B3** | 4:00-5:15 | GChat Alerts + Budget via `/spend` LiteLLM | Polish UI + Mobile + função visível | Retention job + sync one-shot | |
| **Final** | 5:15-6:00 | **Smoke test E2E completo** | | | Deploy produção |

---

## Checklist Final (6h)

- [ ] **FASE 0 ok:** `ox-alpha-free` respondeu request real via Zen
- [ ] `https://ia.fvmarketing.com.br` abre → Dashboard 6 abas
- [ ] `matriz_operacional` populada no PRODUTO (sync manual rodou 1x)
- [ ] Pace Calculator rodou com lock → 2 execuções simultâneas = 1 processa
- [ ] L1-L4 numéricos batem com cálculo manual (LLM não inventa números)
- [ ] CSM comenta (com autoria) → badge some → Coordinator aprova → Ekyte project+tasks criados **1x mesmo com duplo clique**
- [ ] `[PIA] Agente de Tráfego` rodando com `ox-alpha-free`
- [ ] RLS ativa nas tabelas novas (`okr_pace_snapshots`, `matriz_operacional`)
- [ ] Compose subiu só serviços novos — Dokploy intacto

---

## Abrir no ORCA

```bash
# Terminal 1
cd ../orca-infra-n8n && orca .

# Terminal 2
cd ../orca-dashboard-api && orca .

# Terminal 3
cd ../orca-data-agents && orca .
```

Cole o prompt correspondente em cada aba e diga "começa".