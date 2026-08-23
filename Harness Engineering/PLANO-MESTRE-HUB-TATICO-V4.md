# PLANO MESTRE — HUB TÁTICO OPERACIONAL V4
**Domínio:** `ia.fvmarketing.com.br`  
**Data:** 2026-08-23  
**Rev.:** v2 — incorpora correções técnicas (slugs reais de modelos, sintaxe LiteLLM, SQL fix, cálculos determinísticos, lock anti-overlap, compose só com serviços novos)  
**Status:** Plano Master — Para revisão e execução faseada  

---

## 0. CORREÇÕES v2 (APLICADAS NESTA REVISÃO)

| # | Correção | Onde |
|---|----------|------|
| C1 | Slugs de modelos fixados com validação obrigatória antes do deploy; troca `mimo-v2.5-free`/`qwen3-coder:free` → **`ox-alpha-free`** (OpenCode Zen) | Seção 5 |
| C2 | Sintaxe LiteLLM corrigida: `fallbacks` em `router_settings` (não em `litellm_params`); cache semântico exige embedding model | Seção 5 |
| C3 | View SQL corrigida (`created_at` no lugar de `snapshot_time` inexistente) | Seção 3 |
| C4 | L1-L4 = **código determinístico** (Code node N8N / Python); LLM só interpreta o resultado — nunca calcula probabilidade/regressão | Seções 3 e 10 |
| C5 | Cron 15min com **lock anti-overlap** (`pg_try_advisory_lock`) + timeout por run + alerta GChat se travar 2x | Seção 10 |
| C6 | `docker-compose.hub.yml` só sobe **serviços NOVOS** (dashboard-api, qdrant, sync-worker). N8N/LiteLLM/OpenCode existentes no Dokploy são **referenciados por rede/URL**, não duplicados | Seção 11 |
| C7 | Escala dia-1: RLS nas tabelas novas, mapeamento token→usuário, política de retenção de snapshots, backup Qdrant, idempotência Ekyte | Seções 3 e 13 |

---

## 1. VISÃO GERAL DA ARQUITETURA (DUAS CAMADAS)

| Camada | Responsabilidade | Modelo | Onde Roda |
|--------|------------------|--------|-----------|
| **N8N (Crítico)** | Pace Calculator (cron 15min), Check-in Transcription, CSM Review Flow, Flag Diagnostics, GT/Copy/Designer Actions | **gpt-4o-mini** (credencial já no N8N) | N8N workflows |
| **Hub Inteligência** | Chat Builder, OpenCode Web, @okr-pace-analyzer, @action-planner, Memory/RAG, Agent Orchestra | **100% free tier** (`primary` = ox-alpha-free/Zen → failover Gemini free; `structured` = ox-alpha-free via LiteLLM) | OpenCode Web + LiteLLM |

**Princípio:** N8N é a **camada de execução garantida** (rotinas que não podem travar). Hub/LiteLLM é a **camada de inteligência conversacional** (chat, builder, agents, memory) — custo zero.

---

## 2. FLUXO OPERACIONAL CORE (CSM → Coordinator → Ekyte)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  CRON 15min: PACE CALCULATOR (N8N — gpt-4o-mini)                           │
│  • Query DADOS: EcommerceOKR/InsideSalesOKR + fato_ads_meta/google + CRM    │
│  • Calcula L1-L4 → Semáforo + Gap + Probabilidade                           │
│  • Salva: PRODUTO.okr_pace_snapshots + Qdrant                               │
│  • SE 🟡/🔴 → INSERE agent_queue (priority 50/85, mode semi/auto)           │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  AGENT ORCHESTRATOR (Python, cron 5min)                                    │
│  • Dequeue → search_memories (Qdrant) → classify_demand                    │
│  • Roteia: @okr-pace-analyzer (Hub/LiteLLM) + @action-planner (Hub)        │
│  • Salva output em PRODUTO.agent_outputs + agent_queue_log                 │
│  • SE type=csm_review → DISPARA N8N: csm-coordinator-sync                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
            ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
            │  CSM VIEW   │ │COORD VIEW   │ │  EKYTE SYNC │
            │ (Dashboard) │ │ (Dashboard) │ │   (N8N)     │
            └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
                   │               │               │
                   │ CSM comenta   │               │
                   │ "aprovado"    │               │
                   └───────┬───────┘               │
                           ▼                       ▼
                  ┌─────────────────┐    ┌─────────────────┐
                  │ Coordinator vê  │    │ Ekyte: Cria     │
                  │ comentário →    │    │ Project (Sprint)│
                  │ Aprova/Ajusta   │    │ Tasks por função│
                  │ Dispara N8N     │    │ • GT: otimiza   │
                  └─────────────────┘    └─────────────────┘
```

**Regra de Ouro (definida pelo usuário):**
- **CSM** = Verificador e indicador — **não cria tasks**, só **comenta** no card ("aprovado", "ajustar X", "cliente pediu Y")
- **Coordinator** = Lê comentário do CSM → **Cria tasks no Ekyte** no projeto da sprint
- **Ekyte Workspace** = Vem da `DB_Matriz_Operacional_Ago26` (sync para DADOS), fallback `16032`

---

## 3. 4 CAMADAS PREDITIVAS DE DISTÂNCIA (L1-L4)

> **⚠️ REGRA C4:** L1-L4 são **cálculos determinísticos em código** (Code node no N8N ou Python no dashboard-api). O LLM **NUNCA** calcula regressão/probabilidade — alucina números. Fluxo: código calcula → LLM (gpt-4o-mini) só interpreta o resultado e redige a ação recomendada.

| Camada | Horizonte | Fonte DADOS | Cálculo (CÓDIGO, não prompt) | Output para Ação |
|--------|-----------|-------------|---------|------------------|
| **L1 Daily Pulse** | 0-7d | `fato_ads_meta/google` (7d) + OKR meta_diaria | `pace = (realizado_7d/7) * dias_restantes` vs meta — aritmética simples em Code node | "CPA 18% acima → GT pausar HOJE" |
| **L2 Weekly Trajectory** | 7-30d | Ads (4 sem) + OKR progresso_semanal | Regressão linear por mínimos quadrados (fórmula fechada em JS/Python) | "ROAS caindo 0.15/sem → miss em 3 sem" |
| **L3 Monthly Milestone** | 30-90d | `fato_crm_leads` (MQL/SQL) + OKR meta_mensal | `gap = (meta - realizado) / sem_restantes` — aritmética | "Precisa 40 MQLs/3 sem → GT scale + Copy" |
| **L4 Quarter Outcome** | 90-120d | OKR KR_final + velocidade histórica | Monte Carlo **em código**: distribuição normal da velocidade histórica → 1000 amostras (seed fixo) → % hit | "65% hit → execução OK / 35% → replanear" |

**Papel do LLM nas camadas:** receber `{L1..L4 numéricos}` e gerar apenas: `causa_raiz`, `recommended_actions[]` (texto estruturado), `pilares_deficientes`. Números vêm sempre do código.

**Tabela PRODUTO.okr_pace_snapshots:**
```sql
CREATE TABLE okr_pace_snapshots (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  client TEXT NOT NULL,
  squad TEXT NOT NULL,
  okr_type TEXT CHECK (okr_type IN ('EcommerceOKR','InsideSalesOKR')),
  snapshot_date DATE DEFAULT CURRENT_DATE,
  -- OKR
  kr_name TEXT, kr_target NUMERIC, kr_current NUMERIC, kr_unit TEXT, quarter_week INT,
  -- L1
  l1_pace_ratio NUMERIC, l1_semaforo TEXT, l1_gap_pct NUMERIC,
  -- L2
  l2_trajectory_slope NUMERIC, l2_projected_end NUMERIC, l2_semaforo TEXT,
  -- L3
  l3_gap_monthly NUMERIC, l3_required_weekly NUMERIC, l3_semaforo TEXT,
  -- L4
  l4_probability_hit NUMERIC, l4_semaforo TEXT,
  -- Overall
  overall_semaforo TEXT CHECK (overall_semaforo IN ('verde','amarelo','vermelho')),
  recommended_actions JSONB,
  raw_data JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_pace_client_date ON okr_pace_snapshots(client, snapshot_date DESC);
CREATE INDEX idx_pace_semaforo ON okr_pace_snapshots(overall_semaforo, snapshot_date DESC);

-- FIX C3: usa created_at (snapshot_time não existe na tabela)
CREATE VIEW v_okr_pace_latest AS
SELECT DISTINCT ON (client) * FROM okr_pace_snapshots
ORDER BY client, snapshot_date DESC, created_at DESC;

-- C7 ESCALA: RLS desde o dia 1
ALTER TABLE okr_pace_snapshots ENABLE ROW LEVEL SECURITY;
CREATE POLICY pace_read_all ON okr_pace_snapshots FOR SELECT USING (true);
-- Escrita somente via service_role (N8N/dashboard-api); sem policy de INSERT/UPDATE para anon.

-- C7 ESCALA: retenção — manter 90d full; agregar além disso
-- Job diário (N8N cron): DELETE FROM okr_pace_snapshots WHERE created_at < NOW() - INTERVAL '90 days'
-- E INSERT mensal agregado em okr_pace_monthly_agg (client, mes, avg_semaforo, avg_prob)
```

---

## 4. AGENTES (Hub/LiteLLM Free + N8N gpt-4o-mini)

> **Stack de modelos = 3 apenas (minimalista, aprovado).** Nenhum modelo por agente — todos apontam para `primary` ou `structured` no LiteLLM; `fallback` cobre falhas e os fluxos críticos do N8N.
> **C1:** troca aplicada: `mimo-v2.5-free` (workflow Tráfego atual) e `qwen3-coder:free` (plano anterior) → **`ox-alpha-free`** (OpenCode Zen). Slugs validados na FASE 0 antes de qualquer deploy.

| Agente | Camada | Modelo (via LiteLLM) | Função |
|--------|--------|----------------------|--------|
| `@okr-pace-analyzer` | Hub | `primary` (ox-alpha-free → Gemini free) | Interpreta L1-L4 calculados em código; causa raiz; JSON |
| `@action-planner` | Hub | `primary` (ox-alpha-free → Gemini free) | Plano por função (GT, Copy, Designer, CSM) |
| `@media-buyer` | Hub | `primary` | Insights para GT (consulta via chat) |
| `@copy-content` | Hub | `primary` | Draft copy, variações RSA |
| `@criacao-design` | Hub | `primary` | Conceitos visuais, banners |
| `@csm-orquestrador` | Hub | `structured` (**ox-alpha-free** / Zen) | Triagem flags, comunicação cliente |
| Chat Builder (OpenCode Web) | Hub | `primary` + `structured` | Conversação e construção |
| **Pace Calculator** | N8N | **gpt-4o-mini** | Cron 15min com lock; cálculos em Code node; LLM só interpreta |
| **Check-in Transcription** | N8N | **gpt-4o-mini** | Robusto, já existe (50TranscricaoCheckin) |
| **CSM Review Flow** | N8N | **gpt-4o-mini** | Gate CSM → Coordinator → Ekyte |
| **Flag Diagnostics** | N8N | **gpt-4o-mini** | ROI/Churn/OKR/Operação |

**Workflows PIA existentes — ajuste de modelo:** `[PIA] Agente de Tráfego` usa `mimo-v2.5-free` → migrar node "Chamar LLM" para `ox-alpha-free`. Demais workflows (`nemotron-3-ultra-free`, `gemini-2.5-flash-free`) permanecem até validação FASE 0 decidir migração.

---

## 5. ROTEAMENTO LITELLM (HUB — GATEWAY MINIMALISTA)

> **C2 — sintaxe correta:** `fallbacks` fica em `router_settings.fallbacks` (mapa model→lista), nunca dentro de `litellm_params`. Cache semântico exige `embedding_model` configurado + `cache: true` em `general_settings`.
> **C1 — FASE 0 obrigatória antes de escrever o config final:**
> ```bash
> # 1. Validar slugs reais no OpenRouter
> curl -s https://openrouter.ai/api/v1/models | jq -r '.data[].id' | grep -i free
> # 2. Validar catálogo OpenCode Zen (ox-alpha-free)
> curl -s "$ZEN_API_BASE/models" -H "Authorization: Bearer $ZEN_API_KEY" | jq
> ```
> Se `gemini-2.5-flash` não estiver disponível na quota Google, substituto: slug real retornado pelo comando acima (ex.: variante `:free` do OpenRouter). **Nunca deployar com slug não confirmado.**

```yaml
# litellm-config.yaml — v2.2 (100% free tier + fallback pago; SEM billing Gemini)
model_list:
  # PRIMARY rota 1 — Ox Alpha Free via OpenCode Zen (principal)
  - model_name: primary
    litellm_params:
      model: openai/ox-alpha-free             # slug validar na FASE 0
      api_key: os.environ/ZEN_API_KEY
      api_base: os.environ/ZEN_API_BASE       # validar FASE 0
      rpm: 20                                 # janela Zen 2000req/5h é compartilhada — cache + cálculo em código protegem

  # PRIMARY rota 2 — Gemini FREE tier (failover automático se Zen saturar/instabilizar)
  - model_name: primary                       # mesmo model_name = grupo c/ failover interno
    litellm_params:
      model: gemini/gemini-2.5-flash
      api_key: os.environ/GEMINI_API_KEY      # free tier — sem billing
      rpm: 12                                 # conservador p/ free tier

  # STRUCTURED — JSON estrito / function calling (@csm-orquestrador)
  - model_name: structured
    litellm_params:
      model: openai/ox-alpha-free
      api_key: os.environ/ZEN_API_KEY
      api_base: os.environ/ZEN_API_BASE
      rpm: 20

  # FALLBACK — críticos N8N + rede final (nunca falha; credencial já existente no N8N)
  - model_name: fallback
    litellm_params:
      model: gpt-4o-mini
      api_key: os.environ/OPENAI_API_KEY
      rpm: 300

router_settings:
  routing_strategy: "latency-based-routing"
  num_retries: 2
  fallbacks:                                   # ✅ C2: fallbacks AQUI, fora de litellm_params
    primary: ["fallback"]
    structured: ["fallback"]

general_settings:
  cache: true                                  # ✅ C2: cache correto

litellm_settings:
  cache_params:
    type: semantic
    similarity_threshold: 0.85
    ttl: 3600
  embedding_model: gemini/gemini-embedding     # ✅ exigido p/ cache semântico (ou text-embedding-3-small c/ OPENAI key)
```

> **Proteção da janela Zen (sem gastar nada):**
> 1. L1-L4 são **código determinístico** — o LLM só interpreta o resultado (baixo volume: ~centenas/dia, não milhares);
> 2. Cache semântico 0.85 absorve interpretações repetidas;
> 3. Frequência adaptativa recomendada no Pace Calculator: **15min se cliente 🟡/🔴, 1h se 🟢** (maioria verde na maior parte do tempo → corta 50-70% das chamadas);
> 4. Se mesmo assim saturar: `fallback` gpt-4o-mini assume automaticamente (custo só no overflow).

**Alocação única (sem distribuição por agente):**
| Uso | Modelo |
|-----|--------|
| Chat Builder, Agents Hub, interpretação pace | `primary` = Ox Alpha Free (Zen) → failover auto → Gemini free → fallback gpt-4o-mini |
| JSON estrito / function calling / @csm-orquestrador | `structured` = Ox Alpha Free (Zen) |
| Transcription, Flags, CSM Review (N8N) + qualquer falha dos frees | `fallback` = gpt-4o-mini (só overflow) |

> **Filosofia de custo:** inicia 100% free. O único componente pago é o `fallback` (gpt-4o-mini, credencial já existente no N8N) — e ele só é acionado em overflow/falha dos frees ou nos fluxos críticos que não podem travar (Transcription, Flags). Se mais pra frente os frees se provarem instáveis em produção, aí sim avalia-se billing Gemini ou subir % de gpt-4o-mini — decisão com dado real do Langfuse/`/spend`, não especulação.

**Virtual keys (Opção A aprovada):** 6 squad keys (`squad-csm`, `squad-gt`, `squad-copy`, `squad-design`, `squad-account`, `squad-coord`) + 1 `ops-n8n`. Budgets: copy $15, coord $20, ops-n8n $25, demais $10. Rate isolation por squad preservado; observabilidade nativa por key no LiteLLM/Langfuse.

---

## 6. CUSTO gpt-4o-mini (SÓ N8N CRÍTICO)

| Rotina N8N | Runs/Mês | Tokens/Run | Custo Mês (BRL @ 5.50) |
|------------|----------|------------|------------------------|
| Pace Calculator (96/dia) | 2.880 | 10K | ~R$ 45 |
| Check-in Transcription | ~200 | 15K | ~R$ 10 |
| CSM Review + Flags | ~150 | 12K | ~R$ 6 |
| GT/Copy/Design Actions | ~500 | 12K | ~R$ 20 |
| **TOTAL** | **~3.730** | | **~R$ 81/mês** |

**Free models no Hub = R$ 0** (chat, builder, agents, memory).

> **Reduzindo a linha do Pace Calculator sem perder dinâmica:** (1) cálculos L1-L4 já são Code node — o gpt-4o-mini só interpreta o resultado (~2K output, não 10K); (2) cache semântico 0.85 absorve interpretações repetidas do dia verde; (3) frequência adaptativa — 15min se cliente 🟡/🔴, **1h se 🟢** (maioria do portfólio verde na maior parte do tempo → corta 50-70% das runs). Resultado realista: **~R$ 25-45/mês** no pior cenário de carga, com teto garantido pelo alerta em R$ 60 via `/spend`.

---

## 7. DASHBOARD V4 — 6 ABAS (Visual Idêntico `dashboard-completo.html`)

| Aba | Função | Dados |
|-----|--------|-------|
| **1. OKR PACE** | Cards por cliente com L1-L4 semáforos, ações sugeridas, botão "CSM Review" | `v_okr_pace_latest` + `agent_queue` |
| **2. CSM REVIEW** | Gate: CSM vê card → **ação única = Comentar** (textarea + "Enviar") → Badge "Aguardando CSM" some → Coordinator vê | `agent_queue` type=csm_review |
| **3. FLAGS ATIVAS** | ROI, Churn, OKR, Operação — semáforo, dias aberta, ações tomadas | `agent_queue` type=flag_* |
| **4. QUEUE AUTÔNOMA** | Fila completa com prioridade, modo, status, logs | `agent_queue` |
| **5. MEMORY/RAG** | Busca semântica: "runs similares a ROAS caindo 30%" | Qdrant collections |
| **6. AGENTS (Embed)** | Iframe `https://opencode.fvmarketing.com.br` autenticado via `X-Hub-Token` | OpenCode Web |

**Notificações:** GChat (workflow `Gchat Alert Bridge` já existe) — webhook `https://chat.googleapis.com/v1/spaces/{SPACE_ID}/messages`

---

## 8. BANCOS DE DADOS (DOIS SUPABASES — PAPÉIS DEFINIDOS)

> **v2.3 — Matriz no PRODUTO:** alinhado com a `DB_Inteligência_Dados` da própria planilha (`DBPessoas ★ / DBSquads ★ / DBClientes ★ — Atualizado no Novo DB`), a Matriz Operacional vira tabela do **PRODUTO**. Justificativa: Pace Calculator consulta cliente→squad→okr_type 96x/dia na mesma instância de `routine_runs`/`agent_queue` (uma conexão, latência mínima) + RLS multi-tenant já configurada lá.

| Banco | URL | Papel | Tabelas Chave |
|-------|-----|-------|---------------|
| **DADOS (Ops)** | `https://mhntycubvywjszweeuxs.supabase.co` | **Fonte de Verdade Operacional** | `EcommerceOKR`, `InsideSalesOKR`, `fato_ads_meta`, `fato_ads_google`, `fato_crm_leads`, `fato_carteira`, `nps_saber`, `csat_executar_ter`, `bsc_metricas`, `mission_controls` |
| **PRODUTO (Hub)** | `https://bkenzsvexfayjcrqnmpx.supabase.co` | **Orquestração, Execução & Governança** | `routine_runs`, `routine_schedules`, `routine_templates`, `agent_queue`, `agent_queue_log`, `agent_memories`, `agent_outputs`, `pending_approvals`, `approvals`, `chat_messages`, `pia_secrets`, `clientes_mrr`, `bi_acomp_mes`, `squad_insights`, `criativo_analises_ia`, `query_semantic_cache`, **`matriz_operacional` ★ (sync manual da planilha)**, `DB_Pessoas_Atualizado` (sync), `DBSquads`/`DBClientes`/`DBFuncoes`/`DBProdutos` |

### Schema `matriz_operacional` (PRODUTO)

```sql
CREATE TABLE matriz_operacional (
  cliente            TEXT PRIMARY KEY,
  squad              TEXT,
  okr_type           TEXT CHECK (okr_type IN ('EcommerceOKR','InsideSalesOKR')),
  ekyte_workspace_id TEXT,              -- fallback 16032 com warning log
  status             TEXT,              -- Ativo / Inativo
  account_email      TEXT,              -- lookup de responsáveis
  raw                JSONB,             -- linha original da planilha (auditoria/lineage)
  synced_at          TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE matriz_operacional ENABLE ROW LEVEL SECURITY;
CREATE INDEX idx_matriz_status ON matriz_operacional(status);
```

> Tabela única e desnormalizada de propósito (velocidade MVP); normalizar em `DBClientes`/`pessoa_squads` depois se necessário.
>
> **Política de repo:** o `.xlsx` real NÃO vai para o git (PII + fica obsoleto no commit seguinte — planilha é superfície viva de edição humana). O repo recebe apenas: script de sync + `matriz-column-map.json` + fixture anonimizada para testes. Caminho real via env `MATRIZ_XLSX_PATH`.

**Conexão:** Dashboard-api e N8N conectam nos **DOIS** via `SUPABASE_DADOS_URL/KEY` e `SUPABASE_URL/KEY`.

---

## 9. SINCRONIZAÇÃO INICIAL (ONE-TIME SETUP)

> **v2.3 — Sync da Matriz é MANUAL:** a planilha muda mensalmente; sem cron no MVP. Quando o ritmo fixo for definido, pluga num cron N8N sem mudar o script (é idempotente).

```bash
# Quando atualizar a planilha (mensal):
export MATRIZ_XLSX_PATH="/home/marcos/Desktop/Infraestrutura/hub-agentes-ia/projetos/pia-saas/docs/[TECH] Hub de Agentes de IA  _ Gestão e Governança (1).xlsx"
python3 scripts/sync_matriz_operacional.py
# → upsert PRODUTO.matriz_operacional
# → output: {inseridos, atualizados, sem_okr_type, workspace_fallback_warning}
```

| # | Ação | Script | Fonte → Destino |
|---|------|--------|-----------------|
| 1 | Sync Matriz Operacional (**manual**) | `sync_matriz_operacional.py` | Planilha aba `DB_Matriz_Operacional_Ago26` → `PRODUTO.matriz_operacional` (upsert idempotente) |
| 2 | Sync Pessoas | `sync_pessoas.py` | Planilha aba `DB_Pessoas_Atualizado` → `PRODUTO.DB_Pessoas_Atualizado` |
| 3 | Mapear Ekyte Workspace | `map_ekyte_workspace.py` | `matriz_operacional` → `ekyte_workspace_id` por squad/cliente → JSON config N8N (**warning log** no fallback `16032`) |
| 4 | Ingest Qdrant | `ingest_qdrant.py` | Skills (65) + Runs PIA (90d) + OKR snapshots → Qdrant |
| 5 | Virtual Keys LiteLLM | `create_litellm_keys.py` | 6 chaves por squad (csm, gt, copy, design, account, coord) + `ops-n8n` |

---

## 10. N8N WORKFLOWS NOVOS/CORRIGIDOS

| Workflow | Trigger | Modelo | Output |
|----------|---------|--------|--------|
| `pace-calculator` | Cron 15min **+ lock anti-overlap** | **gpt-4o-mini** (só interpreta; cálculos em Code node) | `okr_pace_snapshots` + `agent_queue` |
| `csm-coordinator-sync` | Webhook `csm_review` | **gpt-4o-mini** | CSM comment → Coordinator approve → Ekyte Project+Tasks (**idempotente**: `agent_queue.id` como external ref no Ekyte — duplo clique em "Aprovar" não duplica projeto) |
| `checkin-transcription` | Evento call encerrada | **gpt-4o-mini** | Transcrição bruta → `50TranscricaoCheckin` + dispara `post_checkin` |
| `flag-diagnostics` | Webhook `flag_roi/churn/okr/ops` | **gpt-4o-mini** | Diagnóstico + CHAS → `agent_queue` |
| `execute-action` | `agent_queue` type=execute | **gpt-4o-mini** | GT/Copy/Designer executam → Drive + Ekyte task update |

> **C5 — Lock anti-overlap do Pace Calculator (obrigatório no primeiro node):**
> ```sql
> -- Code node inicial: tenta lock; se falhar, encerra a run silenciosamente
> SELECT pg_try_advisory_lock(918273645) AS locked;
> ```
> - Se `locked = false` → Stop (run anterior ainda viva, evita acúmulo).
> - Se `locked = true` → prossegue; node final executa `pg_advisory_unlock(918273645)` (sempre, via nó "Always Output").
> - Timeout por run: **5 min** (configuração do workflow). Se estourar 2x seguidas → GChat alerta "Pace Calculator travado".

**Workflows PIA existentes (produção) que permanecem:**
- `[PIA] Rotina CSM` (já roda cron hourly)
- `[PIA] Rotina Estrategista`
- `[PIA] Rotina SEO`
- `[PIA] Agente de Tráfego` (**trocar modelo:** `mimo-v2.5-free` → `ox-alpha-free`)
- `[PIA] Rotina Copy`
- `CSM — Dispatcher Briefing Diário`
- `CSM — Dispatcher Resumo Semanal`
- `Gchat Alert Bridge` (já existe)

---

## 11. ENTREGÁVEIS (PARA IMPLEMENTAÇÃO)

> **C6 — Compose só com serviços NOVOS.** N8N, LiteLLM e OpenCode Web **já rodam em produção (Dokploy)** e NÃO são duplicados. O compose novo sobe apenas o que falta e conecta aos existentes pela rede Docker compartilhada / URLs.

| # | Arquivo/Componente | Notas v2 |
|---|---------------------|----------|
| 1 | `docker-compose.hub.yml` | **Somente novos:** `qdrant`, `dashboard-api`, `sync-worker`. Rede externa aponta para Dokploy (`external: true`). N8N/LiteLLM/OpenCode por URL |
| 2 | `litellm-config.yaml` | Sintaxe corrigida (Seção 5); 7 virtual keys; slugs pós-validação FASE 0 |
| 3 | `migrations/produto_okr_pace.sql` | View fixada (`created_at`) + **RLS dia 1** + tabela `okr_pace_monthly_agg` + **`matriz_operacional`** + extensões `agent_queue` (`csm_comment`, `coordinator_decision`, `ekyte_project_id`, `idempotency_key UNIQUE`) |
| 4 | `dashboard-api/main.py` | FastAPI: `/okr-pace`, `/csm-review`, `/queue`, `/flags`, `/memory`, `/analyze`, `/plan`; auth mapeia `X-Hub-Token` → usuário/função (C7) |
| 5 | `dashboard/index.html` | HTML único V4 visual, 6 abas, GChat webhook |
| 6 | `n8n-workflows/pace-calculator.json` | Com advisory lock + timeout 5min + alerta GChat 2 falhas |
| 7 | `n8n-workflows/csm-coordinator-sync.json` | Idempotência Ekyte via `agent_queue.id` |
| 8 | `n8n-workflows/checkin-transcription.json` | Referencia workflow existente |
| 9 | `n8n-workflows/flag-diagnostics.json` | — |
| 10 | `n8n-workflows/execute-action.json` | — |
| 11 | `agents/okr-pace-analyzer.md` | OpenCode, model: `primary` |
| 12 | `agents/action-planner.md` | OpenCode, model: `primary` |
| 13 | `scripts/sync_matriz_operacional.py` + `sync_pessoas.py` + `map_ekyte_workspace.py` | Sync **manual** (planilha muda mensal); lê `MATRIZ_XLSX_PATH` env; introspecção detecta coluna okr_type (heurística `okr_type/tipo_okr`) + config JSON editável — não bloqueia. Repo recebe só script + column-map + fixture anonimizada (**xlsx real fora do git**) |
| 14 | `scripts/ingest_qdrant.py` | + snapshot diário do Qdrant para volume (C7 backup) |
| 15 | `nginx/ia.fvmarketing.com.br.conf` | Proxy `/api` → dashboard-api, `/opencode` → gateway Dokploy existente |

---

## 12. CRONOGRAMA

### FASE 0 — Validações (30 min, ANTES de tudo)
```bash
# Modelos: slugs reais
curl -s https://openrouter.ai/api/v1/models | jq -r '.data[].id' | grep -i free
curl -s "$ZEN_API_BASE/models" -H "Authorization: Bearer $ZEN_API_KEY" | jq
# Teste ox-alpha-free direto:
curl "$ZEN_API_BASE/chat/completions" -H "Authorization: Bearer $ZEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"ox-alpha-free","messages":[{"role":"user","content":"ping"}],"max_tokens":5}'
```
✅ Só depois disso escrever `litellm-config.yaml` definitivo.

### Execução 6h (ORCA, 3 worktrees)
| Bloco | Horário | A1 (Infra/N8N) | A2 (Dashboard/API) | A3 (Data/Agents) |
|-------|---------|----------------|--------------------|------------------|
| Setup | 0:00-0:30 | Compose (só novos) + LiteLLM config validado | FastAPI skeleton + auth token→user | Migrations (com RLS) + sync scripts |
| B1 | 0:30-2:00 | Pace Calculator (lock + cálculos Code node) | 6 Endpoints | Qdrant ingest + backup job |
| Sync 1 | 2:00-2:15 | Teste Pace→Queue | Teste GET /okr-pace | Valida SQL+Qdrant |
| B2 | 2:15-3:45 | CSM→Coord→Ekyte (idempotente) | HTML V4 6 abas | Agents stubs (primary/structured) |
| Sync 2 | 3:45-4:00 | Teste fluxo completo | Teste CSM Review | Teste Agents via API |
| B3 | 4:00-5:15 | GChat alerts + budget `/spend` (via LiteLLM, resposta Q5) | Polish UI/mobile | Retention job + sync one-shot |
| Final | 5:15-6:00 | Smoke E2E completo | | Deploy produção |

---

## 13. RISCOS E MITIGAÇÕES

| Risco | Prob. | Impacto | Mitigação |
|-------|-------|---------|-----------|
| **Slug de modelo inexistente** (deepseek-v4-flash:free etc.) | Alta | Deploy quebra / config inválida | **FASE 0 obrigatória**: validar slugs via API antes de escrever config; nunca deployar slug não confirmado |
| Rate limit models free | Alta | Agentes Hub param | Failover interno do grupo `primary` (ox-alpha → Gemini free) + `fallback` gpt-4o-mini + cache semântico 0.85 + frequência adaptativa no pace (15min 🟡🔴 / 1h 🟢) |
| **Overlap do cron 15min** (run > 15min empilha runs) | Média | Dados duplicados, custo explode | `pg_try_advisory_lock` + timeout 5min/run + GChat se travar 2x |
| **Split-brain** (compose duplica N8N/LiteLLM/OpenCode do Dokploy) | Média | Duas filas, estado inconsistente | Compose só com serviços novos; existentes por rede/URL |
| Qdrant OOM na VPS | Média | Busca falha | `quantization: scalar`, `hnsw_ef: 64`, `m: 16`, `on_disk: true` + snapshot diário p/ volume |
| Ekyte workspace_id faltando | Média | Tasks não criam | `map_ekyte_workspace.py` valida e alerta; fallback `16032` **com warning log** toda vez que cair no fallback |
| Duplo clique "Aprovar" duplica sprint no Ekyte | Média | Projetos fantasmas | Idempotência: `agent_queue.id` como external_ref UNIQUE no Ekyte |
| OKR desatualizado no DADOS | Baixa | Pace errado | `bi_acomp_mes` cross-check; alerta se `updated_at > 7d` |
| CSM não comenta no prazo | Média | Fluxo trava | SLA 4h → escala para Coordinator + GChat reminder |
| Crescimento snapshots (96/dia × clientes × JSONB) | Baixa (média a 100 usuários) | Banco infla | Retenção 90d full + agregação mensal (`okr_pace_monthly_agg`) — job diário |

---

## 14. CRITÉRIOS "PRONTO" (DEFINITION OF DONE)

1. **FASE 0 concluída**: slugs `gemini-2.5-flash` e `ox-alpha-free` testados com request real e resposta OK
2. **Dashboard abre** em `https://ia.fvmarketing.com.br` → visual V4 idêntico, 6 abas funcionando
3. **Pace Calculator roda** com lock: duas execuções simultâneas → apenas uma processa
4. **Semáforo 🔴** → `agent_queue` inserido → interpretação LLM (números vindos do código) → output salvo
5. **CSM Review** → CSM comenta → badge some → Coordinator vê comentário + autoria (quem comentou)
6. **Coordinator Approve** → Sprint no Ekyte criada **1x mesmo com duplo clique** → Tasks por função com donos corretos
7. **RLS ativa** nas tabelas novas; anon não escreve
8. **Deploy idempotente** → compose sobe só os novos serviços sem tocar no Dokploy

---

## 15. PERGUNTAS ANTERIORES — RESOLVIDAS NA v2

| # | Decisão | Resolução v2 |
|---|---------|--------------|
| 1 | **GChat Webhook** | Placeholder + env vars no compose (`GCHAT_SPACE_ID/KEY/TOKEN`) — preenche depois sem rebuild |
| 2 | **Ekyte Workspace fallback** | Sim, `16032`, **com warning log** toda vez que cair no fallback (dado sujo silencioso é pior) |
| 3 | **OKR Type por cliente** | Script introspecta a planilha e detecta coluna por heurística (`okr_type`/`tipo_okr`) + config JSON editável — não bloqueia |
| 4 | **Check-in Transcription** | Referenciar `[PIA] Rotina CSM` modo `post_checkin`; webhook URL configurável via env |
| 5 | **Budget Alert** | Sim, R$ 60/mês — via endpoint `/spend` do próprio LiteLLM (mais simples que Langfuse) |

---

## 16. ARQUIVOS DE REFERÊNCIA EXISTENTES (PARA NÃO REINVENTAR)

### Workflows N8N Produção (já funcionando)
- `/workflows/producao/[PIA] Rotina CSM.workflow.ts` — Cron hourly, 5 modos, HITL, Ekyte
- `/workflows/producao/[PIA] Agente de Tráfego.workflow.ts` — V4mos, flags, Ekyte
- `/workflows/producao/[PIA] Rotina Estrategista.workflow.ts` — Diagnóstico/Relatório
- `/workflows/producao/[PIA] Rotina SEO.workflow.ts` — AI Visibility
- `/workflows/producao/[PIA] Rotina Copy.workflow.ts` — 4 modos
- `/workflows/producao/Gchat Alert Bridge.workflow.ts` — Já existe notificação GChat

### Rotinas PIA (Hub-Agentes-IA)
- `/projetos/pia-saas/rotinas/csm-account/ROTINA.md` + `SYSTEM_INSTRUCTION.md`
- `/projetos/pia-saas/rotinas/gt-analise-trafego/ROTINA.md` + `SYSTEM_INSTRUCTION.md`
- `/projetos/pia-saas/rotinas/copy-producao/ROTINA.md` + `SYSTEM_INSTRUCTION.md`

### Dashboard Atual (pia-saas)
- `/projetos/pia-saas/dashboard/server.js` — FastAPI-like Node, PDF/DOCX generation, Ekyte MCP, dual Supabase
- `/projetos/pia-saas/dashboard/www/index.html` — Visual V4 (Barlow Condensed, vermelho/dourado/preto)

### Configurações Deploy Atual
- `/log/2026-08-22_03-30-00_PIA-HUB-MULTIUSER-DEPLOY.json` — Containers, LiteLLM keys, Ekyte tokens, nginx
- `/litellm-config.yaml` — Já existe config base

### Planilha Governança (Fonte Verdade)
- `/Infraestrutura/hub-agentes-ia/projetos/pia-saas/docs/[TECH] Hub de Agentes de IA  _ Gestão e Governança (1).xlsx`
  - Aba `DB_Matriz_Operacional_Ago26` → Clientes, squads, OKR type, Ekyte workspace
  - Aba `DB_Pessoas_Atualizado` → Pessoas, função, senioridade, cardid
  - Aba `DB_Inteligência_Dados` → Mapeamento tabelas DADOS vs PRODUTO

---

## 17. PRÓXIMOS PASSOS IMEDIATOS (ORDEM DE EXECUÇÃO)

0. **FASE 0 (30min)** — Validar slugs: `gemini-2.5-flash` + `ox-alpha-free` com request real; definir `ZEN_API_BASE/KEY`
1. **Gerar `litellm-config.yaml` v2** — sintaxe corrigida, slugs validados, 7 virtual keys
2. **Gerar `migrations/produto_okr_pace.sql`** — view fixada, RLS, retention, idempotency_key
3. **Gerar `docker-compose.hub.yml`** — só serviços novos (qdrant, dashboard-api, sync-worker)
4. **Executar scripts de sync** — Planilha → DADOS
5. **Pace Calculator N8N** — lock anti-overlap + cálculos Code node + LLM interpreta
6. **Dashboard V4** — HTML + FastAPI (auth token→usuário)
7. **Agentes Hub** — Analyzer + Planner (model `primary`)
8. **CSM ↔ Coordinator → Ekyte** — fluxo idempotente completo
9. **Teste ponta a ponta** — Flag 🔴 → queue → Ekyte tasks (1x só)

---

> **Este documento é o plano master.** Serve como referência única para execução faseada. Cada seção pode ser validada independentemente. O usuário analisará ponto a ponto para decidir prioridades e ajustes antes da implementação.