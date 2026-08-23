# PROMPT A2 — DASHBOARD & API (Cole no ORCA aberto em ../orca-dashboard-api)

Você é o agente A2 do projeto HUB TÁTICO OPERACIONAL V4. Sua branch é `ws2/dashboard-api`. Leia primeiro: `Harness Engineering/PLANO-MESTRE-HUB-TATICO-V4.md`, `Harness Engineering/ESTADO-ATUAL-E-OBJETIVOS-V4.md` e `../orca-contracts/api-endpoints.yaml` + `pace-schema.sql`.

## Regras inegociáveis
1. **NUNCA commite na main** — só na sua branch. Commit a cada bloco.
2. **Visual V4 IDÊNTICO ao existente**: `www/index.html` atual (Barlow Condensed títulos + Barlow corpo; --red #E31919, --red-dark #B80F0F, --gold #c9a96e, --black #0A0A0A, fundo #f8f7f4 ou dark conforme template). NÃO invente novo design — EVOLUA o existente.
3. **Credenciais via env apenas** (`SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `SUPABASE_DADOS_URL`, `SUPABASE_DADOS_KEY`, `QDRANT_URL`, `HUB_SHARED_TOKEN`). Pergunte se faltar.
4. Números exibidos vêm SEMPRE do banco (L1-L4 já calculados pelo pace-calculator). O dashboard nunca calcula métricas.

## ENTREGA 1 — dashboard-api/main.py (FastAPI)
Estrutura: app FastAPI + httpx + middleware auth.

**Auth (middleware global)**: header `X-Hub-Token` validado contra env `HUB_SHARED_TOKEN`; mapeie token→usuário→função via tabela `users` do PRODUTO (ou map estático em config se users ainda não tiver função). Retorne 401 inválido. A função (`csm` | `coordenador` | `gt` | `copy` | `designer`) vai no request.state e controla permissões por endpoint.

**Endpoints**:
1. `GET /api/okr-pace?client={id}` → `PRODUTO.v_okr_pace_latest` (todos os clientes se sem id) → {client, squad, okr_type, semaforo_overall, L1..L4 com números e semáforos, recommended_actions[]}
2. `GET /api/csm-review/{queue_id}` → item de `agent_queue` type csm_review + snapshot relacionado
3. `POST /api/csm-review/{queue_id}/comment` → SÓ função=csm → UPDATE agent_queue SET csm_comment, status='csm_commented', commented_by={user}, updated_at=now() → INSERT agent_queue_log(event='csm_comment') → dispara webhook n8n `csm_comment` (URL via env `N8N_WEBHOOK_BASE`)
4. `POST /api/coordinator/{queue_id}/approve` → SÓ função=coordenador → chama webhook n8n `coordinator_approve` {queue_id, approved, adjustments[]} → retorna {ekyte_project_id, tasks[]}
5. `GET /api/queue?status=&squad=&type=` → lista agent_queue com paginação
6. `GET /api/memory/search?q=&limit=` → busca Qdrant (collections skills/runs/clients/okr_pace) → [{type, content, score, source}]

Inclua: Dockerfile (python:3.11-slim, uvicorn), requirements.txt (fastapi, uvicorn, httpx, qdrant-client), healthcheck `/health`.

## ENTREGA 2 — dashboard/index.html (6 abas, vanilla JS, zero build)
Estenda o index.html existente mantendo identidade visual. Abas:

1. **OKR PACE** (padrão): grid de cards por cliente — nome, squad, badge semáforo overall, 4 mini-badges L1-L4 coloridos (verde/amarelo/vermelho), top 3 ações resumidas, botão "CSM Review" quando status awaiting_csm_comment. Filtros: squad, semáforo, busca.
2. **CSM REVIEW**: lista queue awaiting_csm_comment; card mostra ações; textarea + botão "Enviar Comentário" (só habilitado p/ função csm); após POST → toast sucesso + card sai da lista (badge some). Coordinator vê os já comentados com autoria + botão "Aprovar e Disparar Ekyte" (só função coordenador) + confirmação dupla-clique protegida (disable button após 1º clique).
3. **FLAGS ATIVAS**: queue type flag_* — tipo, cliente, semáforo, dias aberta.
4. **QUEUE AUTÔNOMA**: tabela completa com filtros status/prioridade/squad + expandir detalhe (payload JSON, logs).
5. **MEMORY/RAG**: input de busca → GET /api/memory/search → cards resultado com score e fonte.
6. **AGENTS**: iframe para o OpenCode Web existente (URL via env `OPENCODE_WEB_URL`), altura 100vh.

Comportamento: auto-refresh 30s nas abas 1-4 · loading skeletons · error toast com retry · empty states ilustrados · responsivo (1col <768px, abas viram select no mobile).

## ENTREGA 3 — nginx/ia.fvmarketing.com.br.conf
Server block: SSL (letsencrypt), `/api` → proxy_pass dashboard-api:8000, `/opencode` → proxy ao gateway OpenCode Dokploy, `/` → root do html. Gzip on, cache de assets.

## Critério de pronto
- [ ] curl nos 6 endpoints com X-Hub-Token válido → 200; sem token → 401
- [ ] CSM não consegue aprovar; coordenador não vê textarea de comentário (permissoes por função)
- [ ] Visual indistinguível do template V4 existente
- [ ] Commits atômicos na ws2/dashboard-api
Ao terminar: resuma entregas + instruções de env para o usuário.
