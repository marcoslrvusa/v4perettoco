# ESTADO ATUAL E OBJETIVOS TRAÇADOS — V4 COMPANY
**Para análise paralela pela DeepSeek (agente codificador)**  
**Data:** 2026-08-23  
**Companion do:** `PLANO-MESTRE-HUB-TATICO-V4.md`

---

## 1. INFRAESTRUTURA ATUAL (PRODUÇÃO)

### 1.1 Stack Deployada (VPS Hostinger/Hetzner via Dokploy + Compose Local)

| Componente | Onde Roda | Status | Detalhes |
|------------|-----------|--------|----------|
| **N8N** | Dokploy (produção) | ✅ Healthy | Workflows PIA + SDR IA + alertas |
| **OpenCode Web** | Dokploy (multi-user) | ✅ Healthy | 12 containers usuários + gateway auth |
| **LiteLLM** | Dokploy | ✅ Healthy | 10 virtual keys (por pessoa) |
| **Supabase PRODUTO** | Cloud (`bkenzsvexfayjcrqnmpx`) | ✅ | Orquestração, runs, queue, chat, secrets |
| **Supabase DADOS** | Cloud (`mhntycubvywjszweeuxs`) | ✅ | Fonte verdade operacional (OKRs, Ads, CRM, NPS) |
| **Ekyte** | SaaS externo | ✅ | MCP tokens por usuário (10 configurados) |
| **GChat** | Workspace Google | ✅ | Webhook `Gchat Alert Bridge` no N8N |
| **Dashboard PIA** | Node.js (`server.js`) | ✅ | Porta 8080, PDF/DOCX, dual Supabase, Ekyte MCP |

### 1.2 Containers OpenCode Ativos (Multi-user)
```
opencode-marcos      → hub-agentes (compose local)
opencode-bruno       → opencodemultiusers (Dokploy)
opencode-stefanny    → opencodemultiusers (Dokploy)
opencode-paolo       → opencodemultiusers (Dokploy)
opencode-samuel      → opencodemultiusers (Dokploy)
opencode-italo       → opencodemultiusers (Dokploy)
opencode-lucasnunes  → opencodemultiusers (Dokploy)
opencode-rafaela     → opencodemultiusers (Dokploy)
opencode-lucasbarros → hub-agentes (compose local) — NOVO
opencode-alexandercortes → hub-agentes (compose local) — NOVO
opencode-gateway     → opencodemultiusers (Dokploy) — nginx auth routing
opencode-auth        → ambos — healthy
```

### 1.3 Credenciais Configuradas

**LiteLLM Virtual Keys (10):**
- `LITELLM_KEY_MARCOS`, `LITELLM_KEY_BRUNO`, `LITELLM_KEY_STEFANNY`, `LITELLM_KEY_PAOLO`, `LITELLM_KEY_SAMUEL`, `LITELLM_KEY_ITALO`, `LITELLM_KEY_LUCASNUNES`, `LITELLM_KEY_LUCASBARROS`, `LITELLM_KEY_ALEXANDERCORTES`, `LITELLM_KEY_FHELIPE` (removido)

**Ekyte MCP Tokens (9):**
- `marcos.luciano`, `paolo.carmine`, `bruno.lindenmeyer`, `stefanny.santos`, `samuel.costa`, `lucas.barros` + 3 compartilhados

**Supabase Service Keys:**
- PRODUTO: `SUPABASE_SERVICE_KEY` (bkenzsvexfayjcrqnmpx)
- DADOS: `SUPABASE_DADOS_KEY` (mhntycubvywjszweeuxs) — **NOVA**

**N8N API Key:** `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (já no N8N)

**OpenCode Server Password:** `***REDACTED — rotacionada, ver vault***`

---

## 2. WORKFLOWS N8N EXISTENTES (PRODUÇÃO)

### 2.1 Workflows PIA (5 Rotinas Core) — `/workflows/producao/`

| Workflow | Trigger | Modos | Output |
|----------|---------|-------|--------|
| `[PIA] Rotina CSM` | Cron hourly + webhook | `post_checkin`, `diagnostico`, `sprint`, `relatorio`, `conteudo` | `routine_runs`, `pending_approvals`, Ekyte tasks |
| `[PIA] Agente de Tráfego` | Cron hourly + webhook | `diario`, `criativos`, `bi_funil`, `diagnostico` | Pace, flags, Ekyte tasks |
| `[PIA] Rotina Estrategista` | Webhook | `diagnostico`, `relatorio` | Análise estratégica, relatórios |
| `[PIA] Rotina SEO` | Webhook | `diagnostico`, `relatorio` | AI Visibility + SEO |
| `[PIA] Rotina Copy` | Webhook | `conteudo`, `producao`, `variacao`, `revisao` | Copy assets |

### 2.2 Workflows Auxiliares
- `CSM — Dispatcher Briefing Diário` — Cron diário
- `CSM — Dispatcher Resumo Semanal` — Cron semanal
- `Gchat Alert Bridge` — Webhook → GChat (já funcional)
- `[Dashboard] Collector` — Sync workflows → Supabase
- `[Dashboard] Heartbeat` — Healthcheck N8N
- `Error Handler Central` + `Circuit Breaker Monitor` — Resiliência

### 2.3 Workflows SDR IA (Separados)
- `[SIGNOR] SDR IA`, `[SIGNOR] SDR IA BLINDADA`, `[PRO ANALISES] SDR IA`, `[PALUDO] SDR IA`, `[CESLA] SDR IA - Íris`, `[Genics] SDR IA`

---

## 3. ESTRUTURA DE DADOS ATUAL (DOIS SUPABASES)

### 3.1 Banco PRODUTO (`bkenzsvexfayjcrqnmpx`) — Orquestração & Governança
```sql
-- Core PIA
routine_runs, routine_schedules, routine_templates
agent_queue, agent_queue_log, agent_memories, agent_outputs
pending_approvals, approvals, chat_messages, pia_secrets

-- BI Produto
clientes_mrr, bi_acomp_mes, bi_ticket_medio, mission_controls
squad_insights, criativo_analises_ia, criativo_aprendizados
query_semantic_cache, schema_metadata

-- Governança ★ (alinhado com DB_Inteligência_Dados: "Atualizado no Novo DB")
matriz_operacional          -- NOVA: sync manual da planilha Matriz (cliente, squad,
                            -- okr_type, ekyte_workspace_id, status, raw JSONB, RLS)
DBPessoas ★, DBSquads ★, DBClientes ★, DBFuncoes, DBProdutos

-- RPCs Agent Orchestra
enqueue_demand, dequeue_next, log_queue_event, match_agent_memories
search_memories_fts, consolidate_similar_memories, cleanup_expired_memories
update_routing_stats, update_access_count, store_secret, get_ekyte_token
is_tech_user, rls_auto_enable, show_limit, show_trgm
```

### 3.2 Banco DADOS (`mhntycubvywjszweeuxs`) — Fonte Verdade Operacional
```sql
-- OKRs (JÁ POPULADOS E ATUAIS)
EcommerceOKR ★, InsideSalesOKR ★

-- Ads & CRM
fato_ads_meta, fato_ads_google, fato_crm_leads, fato_carteira
fato_roi_lancamento_mensal

-- NPS/CSAT
nps_saber ★, nps_executar_ter, csat_saber ★, csat_executar_ter ★

-- BSC & Operação
bsc_metricas, bsc_apuracoes_manuais

-- Check-ins / Comunicação
50TranscricaoCheckin ★, chat_conversations, chat_messages
pia_conversations, pia_messages
whatsapp_* (combinados, grupo_cliente_mapa, mensagens, metricas, reclamacoes, relatorio_semanal, sinaleira)

-- Qualidade
QualityCheck, avaliacoes_spiced
```

> **v2.3:** a Matriz Operacional NÃO é mais sincronizada para o DADOS — vai direto ao **PRODUTO.matriz_operacional** (mesma instância de runs/queue = 1 conexão para o Pace Calculator 96x/dia + RLS multi-tenant). Planilha continua sendo a superfície de edição humana; sync **manual** via `MATRIZ_XLSX_PATH`.

### 3.3 Planilha Governança (Fonte Primária)
`/Infraestrutura/hub-agentes-ia/projetos/pia-saas/docs/[TECH] Hub de Agentes de IA  _ Gestão e Governança (1).xlsx`

| Aba | Conteúdo | Uso |
|-----|----------|-----|
| `DB_Matriz_Operacional_Ago26` | Clientes, squads, OKR type, Ekyte workspace, status | Fonte verdade clientes × squads |
| `DB_Pessoas_Atualizado` | Pessoas, emailv4company, equipe, funcao, senioridade, cardid | Lookup responsáveis Ekyte |
| `DB_Inteligência_Dados` | Mapeamento tabelas DADOS vs PRODUTO + categorias | Dicionário de dados |
| `Envs` | Credenciais, URLs, keys | Referência deploy |

---

## 4. ROTINAS PIA DEFINIDAS (HUB-AGENTES-IA)

### 4.1 CSM & Accounts (`/projetos/pia-saas/rotinas/csm-account/`)
- **5 Modos:** `post_checkin`, `diagnostico`, `sprint`, `relatorio`, `conteudo`
- **4 Flags Quantitativas:** ROAS baixo, Churn (NPS+CSAT), Desvio OKR (<60%), Operação travada
- **Agendamento:** Sprint (2ª 9h), Relatório (2ª 9h30 + 1º dia), Conteúdo (4ª 10h), Diagnóstico (1º dia 8h)
- **HITL:** `ui_card` antes de criar tasks Ekyte
- **Ekyte Actions:** `ekyte-actions.md` checklist operacional

### 4.2 GT Análise Tráfego (`/projetos/pia-saas/rotinas/gt-analise-trafego/`)
- **4 Modos:** `diario`, `criativos`, `bi_funil`, `diagnostico`
- **Dados:** V4mos (Meta Ads) + Google Ads (via N8N direto)
- **Flags:** CPA > 100, CTR < 0.5%, Frequência > 8, ROAS < 2.0
- **Sinaleira:** Verde/Amarelo/Vermelho

### 4.3 Copy Produção (`/projetos/pia-saas/rotinas/copy-producao/`)
- **4 Modos:** `conteudo`, `producao`, `variacao`, `revisao`
- **Pirâmide C1/C2/C3 + Princípios V4**
- **Seven Sweeps** para revisão

### 4.4 Estrategista Digital + SEO AI Visibility
- Diagnóstico estratégico + relatório evolução
- AI Visibility (AEO/GEO) + SEO técnico

---

## 5. DASHBOARD ATUAL (PIA-SAAS)

### 5.1 Server.js (`/projetos/pia-saas/dashboard/server.js`)
- **Node.js HTTP server** porta 8080
- **Dual Supabase:** PRODUTO (escrita) + DADOS (leitura)
- **Ekyte MCP** integrado
- **Geração PDF/DOCX** nativa (sem dependências externas)
- **Entregas** em `/entregas` (volume montado)
- **Matriz clientes** em `matriz_clientes.json` (sync da planilha)

### 5.2 Frontend (`/projetos/pia-saas/dashboard/www/index.html`)
- **Visual V4:** Barlow Condensed + Barlow, preto/vermelho/dourado
- **Single page** com chat incorporado + HITL
- **OpenCode Web embed** via iframe autenticado
- **Geração relatórios** PDF com logo Peretto

### 5.3 Protótipos Anteriores
- `prototipo-v1.html` (35KB) — painel rotinas + chat + HITL
- `prototipo-v2.html` (93KB) — refinamentos visuais

---

## 6. OBJETIVOS TRAÇADOS (CONSOLIDADOS)

### 6.1 Objetivo Principal
> **Criar Hub Tático Operacional em `ia.fvmarketing.com.br` que cruze pace de campanhas (DADOS) com OKRs → 4 camadas preditivas L1-L4 → sugira ações por função (GT, Copy, Designer, CSM, Coordinator) → fluxo CSM→Coordinator→Ekyte cadenciado e fluido.**

### 6.2 Objetivos Específicos

| # | Objetivo | Status | Prioridade |
|---|----------|--------|------------|
| 1 | **Pace Calculator automático** (cron 15min) cruzando OKRs + Ads + CRM | 🔴 Não iniciado | Crítica |
| 2 | **4 Camadas L1-L4** com semáforos e probabilidade Monte Carlo | 🔴 Não iniciado | Crítica |
| 3 | **Dashboard V4 unificado** (6 abas: OKR Pace, CSM Review, Flags, Queue, Memory, Agents) | 🟡 Parcial (protótipos) | Crítica |
| 4 | **Fluxo CSM → Coordinator → Ekyte** (CSM comenta, Coordinator cria tasks) | 🔴 Não iniciado | Crítica |
| 5 | **Agent Queue autônoma** com learning loop (Qdrant + Supabase) | 🟡 Parcial (schema existe) | Alta |
| 6 | **Agentes Hub especializados** (`@okr-pace-analyzer`, `@action-planner`) | 🔴 Não iniciado | Alta |
| 7 | **Integração N8N ↔ Hub** (N8N chama Hub para análise/plano via API) | 🔴 Não iniciado | Alta |
| 8 | **Memory/RAG unificado** (Skills + Runs + OKR snapshots no Qdrant) | 🔴 Não iniciado | Média |
| 9 | **GChat notifications** integradas em todos os fluxos | 🟡 Parcial (bridge existe) | Média |
| 10 | **Deploy idempotente** via Docker Compose versionado | 🔴 Não iniciado | Média |

### 6.3 Decisões Técnicas Já Tomadas

| Decisão | Definição |
|---------|-----------|
| **Duas camadas** | N8N (gpt-4o-mini) = execução crítica | Hub/LiteLLM (free) = chat/builder/agents |
| **Modelos N8N** | gpt-4o-mini (credencial já no N8N) — ~R$ 25-81/mês (teto com alerta R$ 60 via `/spend`) |
| **Modelos Hub (free-first, v2.2)** | `primary` = ox-alpha-free (Zen) → failover Gemini FREE tier · `structured` = ox-alpha-free · custo R$ 0 |
| **LiteLLM Routing** | Grupo primary c/ failover interno + fallback gpt-4o-mini + cache semântico 0.85 |
| **Matriz Operacional (v2.3)** | Planilha → sync **MANUAL** → `PRODUTO.matriz_operacional` (muda mensal; cron só quando ritmo definido); xlsx fora do git |
| **Qdrant Config** | `quantization: scalar`, `hnsw_ef: 64`, `m: 16`, `on_disk: true` + snapshot diário p/ volume |
| **Ekyte Workspace** | Da `PRODUTO.matriz_operacional` → fallback `16032` com warning log |
| **Auth Dashboard** | Header `X-Hub-Token` mapeado para usuário→função (CSM comenta / Coordinator aprova) |
| **Notificações** | GChat (workflow `Gchat Alert Bridge` existente) |
| **Visual** | Mantido idêntico ao `dashboard-completo.html` / `pia-analise-completa.html` |

---

## 7. INTEGRAÇÕES NECESSÁRIAS (MAPEAMENTO)

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   N8N           │     │   HUB/LiteLLM   │     │   DASHBOARD     │
│   (gpt-4o-mini) │     │   (Free Models) │     │   (FastAPI)     │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                       │
         │  POST /api/analyze    │                       │
         ├──────────────────────►│                       │
         │  {client, context}    │  @okr-pace-analyzer   │
         │                       │  (DeepSeek)           │
         │◄──────── JSON ────────┤                       │
         │                       │                       │
         │  POST /api/plan       │                       │
         ├──────────────────────►│                       │
         │  {semaforo, gaps}     │  @action-planner      │
         │                       │  (DeepSeek)           │
         │◄──────── JSON ────────┤                       │
         │                       │                       │
         │                       │                       │  GET /api/okr-pace
         │                       │                       ◄──────────────┤
         │                       │                       │  Cards L1-L4  │
         │                       │                       │               │
         │  Webhook csm_review   │                       │  POST /csm-comment
         ├──────────────────────►│                       ◄──────────────┤
         │                       │                       │               │
         │  Ekyte Create Project │                       │  GET /queue   │
         │  + Tasks por função   │                       ◄──────────────┤
         └───────────────────────┴───────────────────────┴───────────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │   SUPABASE      │
                     │   PRODUTO +     │
                     │   DADOS         │
                     └─────────────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │    QDRANT       │
                     │  (Vectors:      │
                     │   skills, runs, │
                     │   clients, OKR) │
                     └─────────────────┘
```

---

## 8. SCRIPTS DE SYNC NECESSÁRIOS

> **v2.3:** sync da Matriz/Pessoas é **MANUAL** (planilha muda mensal; cron só quando ritmo definido). Idempotente — roda quantas vezes precisar.

| Script | Função | Fonte → Destino |
|--------|--------|-----------------|
| `sync_matriz_operacional.py` | Lê `MATRIZ_XLSX_PATH` (env), introspeciona colunas (heurística `okr_type/tipo_okr`) → upsert `PRODUTO.matriz_operacional` |
| `sync_pessoas.py` | Planilha aba `DB_Pessoas_Atualizado` → `PRODUTO.DB_Pessoas_Atualizado` (upsert) |
| `map_ekyte_workspace.py` | Extrai `ekyte_workspace_id` de `matriz_operacional` → JSON config N8N (**warning** no fallback `16032`) |
| `ingest_qdrant.py` | Skills (65 SKILL.md) + Runs PIA (90d) + OKR snapshots → Qdrant collections |
| `create_litellm_keys.py` | Cria 7 virtual keys por squad (`squad-csm`...`squad-coord`, `ops-n8n`) |

```bash
# Uso manual (quando atualizar a planilha):
export MATRIZ_XLSX_PATH="/home/marcos/Desktop/Infraestrutura/hub-agentes-ia/projetos/pia-saas/docs/[TECH] Hub de Agentes de IA  _ Gestão e Governança (1).xlsx"
python3 scripts/sync_matriz_operacional.py && python3 scripts/sync_pessoas.py && python3 scripts/map_ekyte_workspace.py
```

> **Política repo:** o `.xlsx` real NÃO vai para o git. Repo recebe: script + `matriz-column-map.json` + fixture anonimizada para testes.

---

## 9. MIGRATIONS SQL NECESSÁRIAS (PRODUTO)

```sql
-- migrations/produto_okr_pace.sql
CREATE TABLE okr_pace_snapshots (...);   -- Ver Plano Mestre Seção 3 (view usa created_at)
CREATE TABLE matriz_operacional (...);   -- Ver Plano Mestre Seção 8 (RLS + índice status)
CREATE TABLE agent_queue (...);          -- Já existe, verificar/adicionar colunas v2
CREATE VIEW v_okr_pace_latest AS ...;    -- Latest por cliente
-- Índices para performance dashboard + RLS em todas as tabelas novas
```

---

## 10. ARQUIVOS DE REFERÊNCIA PARA DEEPSEEK (CODING AGENT)

### 10.1 Workflows N8N Tipo (para replicar padrões)
- `/workflows/producao/[PIA] Rotina CSM.workflow.ts` — Padrão cron + webhook + Supabase + HITL + Ekyte
- `/workflows/producao/[PIA] Agente de Tráfego.workflow.ts` — Padrão V4mos + flags + sinaleira

### 10.2 Rotinas PIA (System Instructions + Regras)
- `/projetos/pia-saas/rotinas/csm-account/SYSTEM_INSTRUCTION.md`
- `/projetos/pia-saas/rotinas/gt-analise-trafego/SYSTEM_INSTRUCTION.md`
- `/projetos/pia-saas/rotinas/copy-producao/SYSTEM_INSTRUCTION.md`

### 10.3 Dashboard Atual (para manter visual)
- `/projetos/pia-saas/dashboard/server.js` — Backend Node.js com PDF/DOCX, dual Supabase
- `/projetos/pia-saas/dashboard/www/index.html` — Visual V4 (Barlow Condensed, vermelho/dourado/preto)

### 10.4 Configurações Deploy
- `/litellm-config.yaml` — Config base existente
- `/log/2026-08-22_03-30-00_PIA-HUB-MULTIUSER-DEPLOY.json` — Estado containers, keys, tokens
- `/projetos/pia-saas/dashboard/nginx/ia.fvmarketing.com.br.conf` — Reverse proxy (se existir)

### 10.5 Planilha Governança (Estrutura)
- `/Infraestrutura/hub-agentes-ia/projetos/pia-saas/docs/[TECH] Hub de Agentes de IA  _ Gestão e Governança (1).xlsx`

---

## 11. PERGUNTAS BLOQUEANTES PARA DEEPSEEK RESOLVER

| # | Pergunta | Contexto |
|---|----------|----------|
| 1 | **Qual o nome exato da coluna na `DB_Matriz_Operacional_Ago26` que define `EcommerceOKR` vs `InsideSalesOKR` por cliente?** | Pace Calculator precisa saber qual tabela OKR consultar |
| 2 | **Qual o nome exato do workflow N8N que faz transcrição bruta de check-in e salva em `50TranscricaoCheckin`?** | Referenciar no fluxo `post_checkin` |
| 3 | **Quais são os `SPACE_ID`, `KEY`, `TOKEN` do GChat para webhook de notificações?** | Placeholder no código, documentar config |
| 4 | **A tabela `agent_queue` no PRODUTO já tem os campos `priority`, `mode`, `demand_type`, `csm_comment`, `coordinator_decision`?** | Se não, migration necessária |
| 5 | **O `server.js` atual do dashboard roda em container separado ou no mesmo compose do N8N?** | Definir no `docker-compose.hub.yml` |

---

## 12. CRITÉRIOS DE SUCESSO PARA DEEPSEEK VALIDAR

### 12.1 Pace Calculator (N8N)
- [ ] Roda cron 15min sem falha
- [ ] Query DADOS: `EcommerceOKR`/`InsideSalesOKR` + `fato_ads_meta/google` + `fato_crm_leads`
- [ ] Calcula L1-L4 corretamente (fórmulas validadas)
- [ ] Salva em `PRODUTO.okr_pace_snapshots` + Qdrant `okr_pace_vectors`
- [ ] Insere `agent_queue` se 🟡/🔴 (priority 50/85, mode semi/auto)

### 12.2 Dashboard V4
- [ ] Abre em `https://ia.fvmarketing.com.br` com visual V4 idêntico
- [ ] 6 abas funcionando: OKR Pace, CSM Review, Flags, Queue, Memory, Agents
- [ ] Aba OKR Pace: cards por cliente com L1-L4 semáforos + botão "CSM Review"
- [ ] Aba CSM Review: CSM comenta → badge "Aguardando CSM" some → Coordinator vê
- [ ] Aba Agents: iframe OpenCode Web autenticado via `X-Hub-Token`

### 12.3 Fluxo CSM → Coordinator → Ekyte
- [ ] CSM comenta no Dashboard → salva `agent_queue.csm_comment` + `agent_queue_log`
- [ ] Coordinator vê comentário → clica "Aprovar e Disparar Ekyte"
- [ ] N8N `csm-coordinator-sync` cria Project (Sprint) no Ekyte
- [ ] Cria Tasks por função (GT, Copy, Designer, CSM) com `responsibleUserId` via lookup `DB_Pessoas_Atualizado`
- [ ] Tasks aparecem no Ekyte com tags `["OKR-Pace", funcao]`

### 12.4 Agentes Hub (OpenCode/LiteLLM)
- [ ] `@okr-pace-analyzer` recebe `client_id` + L1-L4 **já calculados em código** → retorna `{causa_raiz, pilares_deficientes, recommended_actions[]}` (nunca calcula números)
- [ ] `@action-planner` recebe semáforo + gaps → retorna `actions[funcao, acao, prazo, dono, evidencia]`
- [ ] Ambos usam `primary` via LiteLLM (ox-alpha-free → Gemini free — 100% free tier)
- [ ] Fallback gpt-4o-mini funciona se os frees falharem

### 12.5 Integração N8N ↔ Hub
- [ ] N8N `pace-calculator` → POST `/api/analyze` → Hub → JSON response
- [ ] N8N `csm-coordinator-sync` → POST `/api/plan` → Hub → JSON response
- [ ] N8N `execute-action` → dispara agentes Hub via queue → resultados no Drive/Ekyte

---

## 13. COMANDOS ÚTEIS PARA DEEPSEEK (VPS)

```bash
# Status stack
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Logs
docker logs v4-opencode --tail 50 -f
docker logs v4-litellm --tail 50 -f
docker logs v4-n8n --tail 50 -f

# Testar LiteLLM
curl http://localhost:4000/v1/models -H "Authorization: Bearer $LITELLM_MASTER_KEY" | jq .

# Testar Qdrant
curl http://localhost:6333/collections

# Sync planilha → PRODUTO (manual, quando a planilha mudar)
export MATRIZ_XLSX_PATH="/home/marcos/Desktop/Infraestrutura/hub-agentes-ia/projetos/pia-saas/docs/[TECH] Hub de Agentes de IA  _ Gestão e Governança (1).xlsx"
python3 scripts/sync_matriz_operacional.py
python3 scripts/sync_pessoas.py
python3 scripts/map_ekyte_workspace.py

# Ingest Qdrant
python3 scripts/ingest_qdrant.py

# Deploy
git pull && docker compose -f docker-compose.hub.yml up -d --build

# Healthcheck dashboard
curl -I https://ia.fvmarketing.com.br
```

---

## 14. ARQUIVOS PARA CRIAR (LISTA DE TAREFAS DEEPSEEK)

| Ordem | Arquivo | Descrição |
|-------|---------|-----------|
| 1 | `docker-compose.hub.yml` | Stack completa (7 serviços) |
| 2 | `litellm-config.yaml` | Gateway models free + virtual keys + fallbacks |
| 3 | `migrations/produto_okr_pace.sql` | Schema `okr_pace_snapshots` + views |
| 4 | `dashboard-api/main.py` | FastAPI endpoints (/okr-pace, /csm-review, /queue, /flags, /memory, /ekyte-sync) |
| 5 | `dashboard/index.html` | HTML único V4 visual (6 abas) |
| 6 | `n8n-workflows/pace-calculator.json` | Motor preditivo cron 15min |
| 7 | `n8n-workflows/csm-coordinator-sync.json` | Fluxo CSM→Coord→Ekyte |
| 8 | `n8n-workflows/checkin-transcription.json` | Ref. workflow existente |
| 9 | `n8n-workflows/flag-diagnostics.json` | ROI/Churn/OKR/Ops |
| 10 | `n8n-workflows/execute-action.json` | GT/Copy/Designer actions |
| 11 | `agents/okr-pace-analyzer.md` | Agente OpenCode Tier A |
| 12 | `agents/action-planner.md` | Agente OpenCode Tier A |
| 13 | `scripts/sync_matriz_operacional.py` | Planilha (via `MATRIZ_XLSX_PATH`) → `PRODUTO.matriz_operacional` — manual |
| 14 | `scripts/sync_pessoas.py` | Planilha → `PRODUTO.DB_Pessoas_Atualizado` |
| 15 | `scripts/map_ekyte_workspace.py` | Ekyte workspace mapping |
| 16 | `scripts/ingest_qdrant.py` | Skills + Runs + OKR → Qdrant |
| 17 | `nginx/ia.fvmarketing.com.br.conf` | Reverse proxy |

---

## 15. COMANDO PARA DEEPSEEK INICIAR

```bash
# 1. Clonar/atualizar repo na VPS
cd /opt/hub-agentes && git pull

# 2. Criar estrutura de pastas
mkdir -p dashboard-api dashboard n8n-workflows agents scripts migrations nginx

# 3. Começar pelo docker-compose.hub.yml (fundação)
# 4. Seguir ordem da tabela na Seção 14
```

---

> **Este documento + `PLANO-MESTRE-HUB-TATICO-V4.md` = Contexto completo para DeepSeek codificar em paralelo.**  
> O DeepSeek deve tratar cada arquivo da Seção 14 como task independente, validando contra os Critérios de Sucesso (Seção 12) e referenciando os Arquivos de Referência (Seção 10).