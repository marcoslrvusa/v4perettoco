# PROMPT A1 — INFRA & N8N (Cole no ORCA aberto em ../orca-infra-n8n)

Você é o agente A1 do projeto HUB TÁTICO OPERACIONAL V4. Sua branch é `ws1/infra-n8n` (você já está nela). Leia primeiro: `Harness Engineering/PLANO-MESTRE-HUB-TATICO-V4.md`, `Harness Engineering/ESTADO-ATUAL-E-OBJETIVOS-V4.md` e `../orca-contracts/model-slugs.json`.

## Regras inegociáveis
1. **NUNCA commite na main** — só na sua branch. Commit a cada bloco concluído.
2. **Compose sobe SOMENTE serviços novos** (`qdrant`, `dashboard-api`, `sync-worker`) com rede `external: true` apontando para a rede Dokploy existente. N8N, LiteLLM e OpenCode Web JÁ RODEM em produção — referencie por URL/rede, NUNCA duplique (split-brain).
3. **Modelos**: `primary` = grupo de 2 deployments (rota 1 ox-alpha-free via Zen; rota 2 gemini/gemini-2.5-flash FREE tier, rpm 12) · `structured` = ox-alpha-free · `fallback` = gpt-4o-mini. Use os slugs exatos de `../orca-contracts/model-slugs.json`.
4. **L1-L4 são cálculos DETERMINÍSTICOS em Code node** — o LLM (gpt-4o-mini) NUNCA calcula números, só interpreta o resultado.
5. Credenciais SEMPRE via env vars (`SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `SUPABASE_DADOS_URL`, `SUPABASE_DADOS_KEY`, `GEMINI_API_KEY`, `ZEN_API_KEY`, `ZEN_API_BASE`, `OPENAI_API_KEY`, `GCHAT_SPACE_ID/KEY/TOKEN` como placeholder). Se faltar alguma, pergunte ao usuário — nunca hardcode.

## ENTREGA 1 — docker-compose.hub.yml
Serviços: `qdrant` (imagem oficial, volume nomeado, healthcheck na porta 6333), `dashboard-api` (build ./dashboard-api, porta 8000), `sync-worker` (python:3.11-slim, roda scripts/, cron interno ou dorme em loop). Redes: `hub-net` (internal) + rede externa Dokploy. Volumes persistentes. `.env.example` completo ao lado.

## ENTREGA 2 — litellm-config.yaml (NO LITELLM EXISTENTE do Dokploy)
Gere o arquivo para o usuário aplicar no LiteLLM já rodando. Sintaxe OBRIGATÓRIA:
```yaml
router_settings:
  fallbacks:
    primary: ["fallback"]
    structured: ["fallback"]
general_settings:
  cache: true
litellm_settings:
  cache_params: { type: semantic, similarity_threshold: 0.85, ttl: 3600 }
  embedding_model: gemini/gemini-embedding
```
(fallbacks NUNCA dentro de litellm_params). Inclua os 7 virtual keys squad com budgets: copy $15, coord $20, ops-n8n $25, demais $10.

## ENTREGA 3 — n8n-workflows/pace-calculator.json
Workflow n8n exportável (JSON válido — valide com `n8n import:workflow --dry-run` se disponível):
1. **Schedule** 15min → **Node Lock**: Postgres/Supabase `SELECT pg_try_advisory_lock(918273645)` → false = STOP silencioso
2. **Node Clientes**: `PRODUTO.matriz_operacional WHERE status='Ativo'` → cliente, squad, okr_type, ekyte_workspace_id
3. **Nodes Fetch (DADOS)**: `EcommerceOKR`/`InsideSalesOKR` (por okr_type) + `fato_ads_meta` + `fato_ads_google` (7d/14d/30d: spend, roas, cpa, ctr) + `fato_crm_leads` (MQL/SQL)
4. **Code node "Calc L1-L4" (determinístico)**: L1 aritmética pace vs meta_diária; L2 regressão linear fórmula fechada sobre 4 semanas; L3 gap/semanas_restantes; L4 Monte Carlo 1000 sims seed fixo (velocidade_hist ± variância). Semáforos: 🟢 ±10% / 🟡 10-25% / 🔴 >25%
5. **Node gpt-4o-mini (só interpreta)**: recebe {L1..L4 numéricos} → retorna {causa_raiz, recommended_actions[funcao,acao,prazo,dono,evidencia], pilares_deficientes} — proíba no prompt qualquer cálculo
6. **Upsert** `PRODUTO.okr_pace_snapshots` + upsert Qdrant collection `okr_pace`
7. **IF 🟡/🔴** → insert `PRODUTO.agent_queue` {type:"okr_pace_alert", priority:50/85, mode:"semi"/"auto", payload}
8. **Node final Always-Output**: `SELECT pg_advisory_unlock(918273645)`
9. Timeout de execução 5min; contador de falhas consecutivas ≥2 → GChat alert

## ENTREGA 4 — n8n-workflows/csm-coordinator-sync.json
Webhook `csm_review_trigger` {queue_id} → monta card CSM (busca queue + snapshot) → status="awaiting_csm_comment" + GChat p/ CSM → webhook `csm_comment` {queue_id, comment, user} salva csm_comment → se contém "aprovad|validado" → GChat Coordinator → webhook `coordinator_approve` → **EKYTE IDEMPOTENTE**: create_project com external_ref = agent_queue.id (se já existe, reusa); loop actions[] → create_task com responsibleUserId via lookup `DB_Pessoas_Atualizado` (funcao+squad), tags ["OKR-Pace", funcao] → status="completed". Duplo clique = 1 projeto só.

## ENTREGA 5 — stubs
`flag-diagnostics.json` (webhook flag_roi/churn/okr/ops → diagnóstico gpt-4o-mini → agent_queue) e `execute-action.json` (dequeue type=execute → GT/Copy/Designer → Drive+Ekyte).

## ENTREGA 6 — Patch workflow existente
Em `[PIA] Agente de Tráfego`: trocar modelo do node "Chamar LLM" de `mimo-v2.5-free` para o slug zen validado (ox-alpha-free). Só isso — nada mais no workflow.

## ENTREGA 7 — nginx/ia.fvmarketing.com.br.conf
Server block SSL: `/api` → dashboard-api:8000 · `/opencode` → proxy ao gateway OpenCode Dokploy existente · `/` → estático dashboard.

## Critério de pronto
- [ ] JSONs dos workflows válidos
- [ ] Compose não referencia N8N/LiteLLM/OpenCode como serviços próprios
- [ ] Lock advisory presente no início E fim do pace-calculator
- [ ] Commits atômicos por entrega na ws1/infra-n8n
Ao terminar: resuma entregas + o que precisa do usuário (env vars a preencher).
