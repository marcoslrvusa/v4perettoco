# Infraestrutura de IA — Peretto & Co

## Arquitetura para adoção em escala com eficiência, segurança e governança

> Documento corrigido: substitui Open WebUI por OpenCode Web como interface de execução,
> integra os 35 agentes da Agent Orchestra V4 e alinha com a stack real da operação.

---

## Índice

1. [Fundamentos Estratégicos](#1-fundamentos-estratégicos)
2. [Arquitetura Atual vs Proposta](#2-arquitetura-atual-vs-proposta)
3. [Componentes da Infraestrutura](#3-componentes-da-infraestrutura)
4. [Fluxo de Execução](#4-fluxo-de-execução)
5. [Docker Compose da Stack](#5-docker-compose-da-stack)
6. [Integração com OpenCode Web](#6-integração-com-opencode-web)
7. [Modelos e Alocação por Agente](#7-modelos-e-alocação-por-agente)
8. [Fases de Implementação](#8-fases-de-implementação)
9. [Custos e Viabilidade](#9-custos-e-viabilidade)

---

## 1. Fundamentos Estratégicos

No cenário tecnológico contemporâneo, a velocidade de lançamento de modelos e a queda
acentuada nos custos por milhão de tokens criam uma ilusão de facilidade de implementação.

Conforme destacado por Ben Haklai (CTO da Microsoft Israel), a transição real da IA das fases de
laboratório para o mercado corporativo envolve preparação estrutural. As barreiras reais não são
técnicas — são de **governança e segurança**.

### Quatro Pilares Críticos

| Pilar | Descrição |
|-------|-----------|
| **Segurança de Dados** | Informações corporativas e dados de clientes sob controle estrito da empresa |
| **Responsabilidade Jurídica** | Salvaguardas contra litígios por geração de conteúdo e violação de direitos |
| **Conformidade Organizacional** | Padrões regulatórios internacionais + políticas internas de auditoria |
| **Propriedade Intelectual** | Filtros preventivos sobre entradas e saídas do sistema |

### Princípios de Operação

- Equidade, confiabilidade, segurança e privacidade
- Transparência de fontes (rastreabilidade)
- Fator humano no loop (human-in-the-loop)
- Para uma unidade de 80-100 colaboradores

---

## 2. Arquitetura Atual vs Proposta

### Fluxo Local (atual)

```
NotebookLM → OpenCode CLI → Obsidian Vault
      ↓                       ↓
  Pesquisa               Conhecimento
  documental             estruturado
```

**Limitações identificadas:**
- Silos de conhecimento (vaults locais, sem colaboração)
- Complexidade de setup (Node.js, git, links simbólicos)
- CLI não amigável para profissionais de negócios
- Cada colaborador precisa configurar o próprio ambiente
- Sem governança centralizada de API keys

### Arquitetura Proposta

```
                    ┌──────────────────────────────────────────┐
                    │            Usuários / Squads              │
                    │   (browser: opencode.fvmarketing.com.br)  │
                    └────────────────┬─────────────────────────┘
                                     │ HTTPS + Basic Auth
                                     ▼
               ┌─────────────────────────────────────────────┐
               │              OpenCode Web                    │
               │      Interface de agente no browser          │
               │                                              │
               │  @analista-dados  @flag-roi  @copy-content  │
               │  @gerar-ppt       @csm        @revisor       │
               │  ... +35 subagentes da Agent Orchestra V4    │
               └────────────────────┬────────────────────────┘
                                    │
                                    ▼
               ┌─────────────────────────────────────────────┐
               │           LiteLLM Proxy (Gateway)            │
               │                                              │
               │  ● Rate limit por agente/squad               │
               │  ● Chaves virtuais (sem expor API keys)      │
               │  ● Teto de gastos por usuário                │
               │  ● Fallback automático entre provedores      │
               │  ● Cache semântico                           │
               │  ● Logs de auditoria                         │
               └──────┬──────────────────┬───────────────────┘
                      │                  │
              ┌───────┴───────┐  ┌──────┴────────┐
              ▼               ▼  ▼               ▼
      ┌────────────┐  ┌──────────┐  ┌──────────────┐
      │  OpenCode  │  │  Google  │  │  OpenRouter  │
      │  Zen Free  │  │  Gemini  │  │  Free/Paid   │
      │  (DeepSeek │  │  2.5     │  │  (Fallback)  │
      │   Flash)   │  │  Flash   │  │              │
      └────────────┘  └──────────┘  └──────────────┘
                      │
                      ▼
      ┌──────────────────────────────────────────────┐
      │           Qdrant (Banco Vetorial)             │
      │  ● Playbooks SKILL.md                         │
      │  ● Conhecimento de clientes                   │
      │  ● Transcrições de reuniões                   │
      │  ● Documentos técnicos                        │
      └──────────────────────────────────────────────┘
                      │
                      ▼
      ┌──────────────────────────────────────────────┐
      │           n8n (Automação)                      │
      │  ● APIs de tráfego (Meta Ads, Google Ads)     │
      │  ● Workflows de automação                     │
      │  ● Disparo de flags CSM                       │
      │  ● Relatórios consolidados                    │
      └──────────────────────────────────────────────┘
```

### Por que OpenCode Web no lugar de Open WebUI

| Aspecto | Open WebUI | OpenCode Web |
|---------|-----------|--------------|
| **Interface** | Chat estilo ChatGPT | Terminal gráfico + chat + agente |
| **Agentes** | Workflows do n8n registrados como "modelos" | **35 subagentes nativos** com skills, ferramentas e memória |
| **Skills** | Não tem | 66 skills compartilhadas em `.agents/skills/` |
| **Ferramentas** | Só chat + MCP | Bash, edição de arquivos, web search, web fetch, task agent |
| **Orquestração** | Manual (trocar de modelo) | Times multi-agente: `/team-growth`, `/team-content` |
| **Sessões** | Conversas lineares | Sessões com contexto persistente, exportáveis |
| **Autonomia** | Responde perguntas | **Executa**: edita arquivos, roda comandos, puxa APIs |
| **Governança** | RBAC por usuário | Permissões por agente (`edit:deny`, `bash:deny`) |
| **Código aberto** | Sim | Sim (MIT) |

**Conclusão:** Open WebUI é um chat com modelos. OpenCode Web é um **ambiente de execução de agentes**. Para uma operação que já tem 35 agentes e 66 skills, OpenCode Web é a escolha certa.

---

## 3. Componentes da Infraestrutura

### Componente A: OpenCode Web (Interface de Agentes)

**O que é:** A interface web do OpenCode, rodando via `opencode web`. Substitui o Open WebUI.

**Funções:**
- Interface para os 35 subagentes da Agent Orchestra V4
- Execução de comandos custom (`/team-growth`, `/team-content`, etc.)
- Sessões paralelas com contexto persistente
- Upload/download de arquivos
- Autenticação via HTTP Basic Auth (senha mestra)
- Acessível de qualquer lugar via browser

**Como os agentes funcionam no OpenCode Web:**

```
                  ┌─────────────────────────────┐
                  │  browser: opencode.fv...    │
                  │  "@analista-dados           │
                  │   'análise ROAS cliente X'" │
                  └─────────────┬───────────────┘
                                ▼
                  ┌─────────────────────────────┐
                  │  OpenCode Web Server         │
                  │  Lê .opencode/agents/        │
                  │  Encontra analista-dados.md  │
                  │  Aplica frontmatter:         │
                  │    model: deepseek-v4-flash  │
                  │    permission: edit:allow    │
                  │    temperature: 0.1          │
                  └─────────────┬───────────────┘
                                ▼
                  ┌─────────────────────────────┐
                  │  LiteLLM (se configurado)    │
                  │  OU diretamente no provider  │
                  └─────────────┬───────────────┘
                                ▼
                  ┌─────────────────────────────┐
                  │  DeepSeek V4 Flash Free     │
                  │  (opencode/deepseek-v4-     │
                  │   flash-free)               │
                  └─────────────────────────────┘
```

### Componente B: LiteLLM Proxy (Gateway de IA)

**O que é:** Proxy open-source (MIT) que centraliza o roteamento para 100+ provedores de LLM.

**Já temos:** OpenRouter integrado direto no OpenCode. O LiteLLM adiciona a camada de governança.

**Funções:**
- **Centralização de chaves:** em vez de dar a chave do OpenRouter/Zen para cada agente, as chaves ficam no LiteLLM
- **Chaves virtuais:** cada squad recebe uma chave virtual com permissões específicas
- **Controle de gastos:** teto diário por squad (ex: $2/dia), evitando loops infinitos
- **Rate limit por agente:** impede que um agente consuma o limite dos outros
- **Fallback automático:** se DeepSeek cair, redireciona para OpenRouter
- **Cache semântico:** requisições similares são servidas do cache Redis
- **Auditoria:** logs de todas as chamadas para compliance

### Componente C: n8n (Automação)

**Já temos:** n8n rodando em produção na VPS.

**Funções:**
- Conectar APIs de tráfego pago (Meta Ads, Google Ads)
- Processar leads em volume
- Orquestrar workflows de automação (relatórios, flags CSM, briefing comitê)
- Servir como backend de dados para os agentes do OpenCode

### Componente D: Qdrant (Banco Vetorial)

**O que é:** Banco de dados vetorial open-source, alta performance.

**Funções:**
- Armazenar embeddings dos playbooks, skills, transcrições
- Busca semântica (RAG) para os agentes
- Conhecimento corporativo centralizado (substitui vaults locais do Obsidian)
- Conecta nativamente ao n8n

### Componente E: Langfuse (Observabilidade)

**O que é:** Plataforma open-source de observabilidade para LLMs.

**Funções:**
- Tracing de cada chamada de agente
- Custo por squad/mês
- Detecção de anomalias (latência, erros)
- Alerta de rate limit

---

## 4. Fluxo de Execução

### Cenário 1: Analista usando agente no browser

```
1. Usuário abre https://opencode.fvmarketing.com.br
2. Digita: @analista-dados "ROAS do cliente X nos últimos 30 dias"
3. OpenCode Web:
   a. Carrega o agente de .opencode/agents/analista-dados.md
   b. Aplica modelo: deepseek-v4-flash-free
   c. Aplica permissões: edit:allow, bash:allow
4. Opção A — Direto: OpenCode → OpenCode Zen → DeepSeek V4 Flash Free
   Opção B — Com LiteLLM: OpenCode → LiteLLM → OpenRouter/Zen
5. Agente executa:
   a. Puxa dados via scripts Python (v4-automations/)
   b. Analisa no contexto de 1M tokens
   c. Gera JSON estruturado
6. Usuário recebe resposta no browser
```

### Cenário 2: Time multi-agente no browser

```
1. Usuário digita: /team-growth "quero aumentar ROAS do cliente X"
2. OpenCode executa o comando custom:
   a. Ativa @growth-team como líder
   b. Convoca @cro-otimizacao, @midia-paga, @seo-visibilidade, @copy-content
   c. Cada subagente roda em seu modelo designado
3. Resposta consolidada: plano integrado com ações de CRO + mídia + SEO + copy
```

### Cenário 3: Automação noturna (sem humano)

```
Domingo 20h (cron):
1. Script no VPS invoca: opencode --headless @executor-comite "prepara comitê"
2. @executor-comite invoca @analista-dados para cada cliente ativo
3. @revisor valida cada saída
4. @executor-comite consolida briefing em markdown + HTML
5. Briefing salvo em /docs e enviado por email
```

---

## 5. Docker Compose da Stack

```yaml
# docker-compose.yml
# Infraestrutura completa: OpenCode Web + n8n + LiteLLM + Qdrant + Langfuse

version: '3.8'

networks:
  v4-network:
    name: v4-ai-network
    driver: bridge

volumes:
  pgdata:
  qdrant_data:
  langfuse_data:
  opencode_agents:
  opencode_logs:
  n8n_data:

services:
  # ─── PostgreSQL (compartilhado: LiteLLM + Langfuse) ───
  postgres:
    image: postgres:16-alpine
    container_name: v4-postgres
    networks:
      - v4-network
    environment:
      POSTGRES_USER: v4_admin
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: v4_ai
    volumes:
      - pgdata:/var/lib/postgresql/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U v4_admin -d v4_ai"]
      interval: 5s
      timeout: 5s
      retries: 5

  # ─── OpenCode Web (Interface de Agentes) ───
  opencode:
    image: smanx/opencode:latest
    container_name: v4-opencode
    networks:
      - v4-network
    ports:
      - "4096:4096"
    volumes:
      # Monta o repositório com agentes, skills e config
      - /data/v4-repo/opencode.json:/workspace/opencode.json:ro
      - /data/v4-repo/.opencode/agents:/workspace/.opencode/agents:ro
      - /data/v4-repo/.opencode/skills:/workspace/.opencode/skills:ro
      - /data/v4-repo/.agents/skills:/workspace/.agents/skills:ro
      - /data/v4-repo/.env:/workspace/.env:ro
      # Volumes persistentes
      - opencode_logs:/workspace/log
    environment:
      - OPENCODE_SERVER_PASSWORD=${OPENCODE_SERVER_PASSWORD}
      - OPENCODE_HOSTNAME=0.0.0.0
      - OPENCODE_PORT=4096
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:4096/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G

  # ─── LiteLLM Proxy (Gateway de IA) ───
  litellm:
    image: ghcr.io/berriai/litellm:main-latest
    container_name: v4-litellm
    networks:
      - v4-network
    ports:
      - "4000:4000"
    volumes:
      - ./litellm-config.yaml:/app/config.yaml:ro
    environment:
      - LITELLM_MASTER_KEY=${LITELLM_MASTER_KEY}
      - LITELLM_SALT_KEY=${LITELLM_SALT_KEY}
      - DATABASE_URL=postgresql://v4_admin:${POSTGRES_PASSWORD}@postgres:5432/v4_ai
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    command: ["--config=/app/config.yaml", "--port=4000"]
    restart: unless-stopped
    depends_on:
      postgres:
        condition: service_healthy
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G

  # ─── n8n (Automação) ───
  n8n:
    image: n8nio/n8n:latest
    container_name: v4-n8n
    networks:
      - v4-network
    ports:
      - "5678:5678"
    volumes:
      - n8n_data:/home/node/.n8n
      - /data/v4-repo/workflows:/workflows
      - /data/v4-repo/v4-automations:/v4-automations
    environment:
      - N8N_SECURE_COOKIE=false
      - N8N_METRICS=true
    restart: unless-stopped

  # ─── Qdrant (Banco Vetorial) ───
  qdrant:
    image: qdrant/qdrant:latest
    container_name: v4-qdrant
    networks:
      - v4-network
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_data:/qdrant/storage
    restart: unless-stopped

  # ─── Langfuse (Observabilidade) ───
  langfuse:
    image: ghcr.io/langfuse/langfuse:latest
    container_name: v4-langfuse
    networks:
      - v4-network
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://v4_admin:${POSTGRES_PASSWORD}@postgres:5432/v4_ai
      - NEXTAUTH_SECRET=${LANGFUSE_SECRET}
      - NEXTAUTH_URL=http://localhost:3000
    restart: unless-stopped
    depends_on:
      postgres:
        condition: service_healthy
```

### Configuração do LiteLLM

```yaml
# litellm-config.yaml
model_list:
  # Modelos gratuitos do OpenCode Zen
  - model_name: deepseek-v4-flash-free
    litellm_params:
      model: openrouter/deepseek/deepseek-v4-flash:free
      api_key: os.environ/OPENROUTER_API_KEY
      rpm: 5
      fallbacks:
        - qwen3-coder-free

  - model_name: google-gemini-flash
    litellm_params:
      model: gemini/gemini-2.5-flash
      api_key: os.environ/GEMINI_API_KEY
      rpm: 10

  - model_name: qwen3-coder-free
    litellm_params:
      model: openrouter/qwen/qwen3-coder:free
      api_key: os.environ/OPENROUTER_API_KEY
      rpm: 5

router_settings:
  routing_strategy: "latency-based-routing"
  num_retries: 3
  fallback_strategy: "strict"
  cache:
    type: semantic
    similarity_threshold: 0.85
```

---

## 6. Integração com OpenCode Web

### 6.1 Estrutura de Arquivos no VPS

```
/data/v4-repo/                          ← Montado no container OpenCode
├── opencode.json                       ← Config principal
├── .env                                ← API keys
│
├── .opencode/
│   ├── agents/                         ← 35 subagentes
│   │   ├── analista-dados.md
│   │   ├── flag-roi.md
│   │   ├── copy-content.md
│   │   ├── gerar-ppt.md
│   │   └── ... (35 agentes)
│   │
│   ├── skills/                         ← 21 skills OpenCode
│   │   ├── obsidian-markdown/
│   │   ├── json-canvas/
│   │   └── ...
│   │
│   └── commands/                       ← Comandos custom
│       ├── team-growth.md
│       ├── team-content.md
│       └── ...
│
├── .agents/skills/                     ← 66 skills V4
│   ├── account-checkin-review/
│   ├── copywriting/
│   └── ...
│
├── docs/                               ← Documentação
│
└── scripts/                            ← Automações Python
    ├── session-save.sh
    └── build-registry.py
```

### 6.2 Configuração do opencode.json

```json
{
  "model": "opencode/deepseek-v4-flash-free",
  "small_model": "opencode/minimax-m2.5-free",
  "provider": {
    "gemini": {
      "apiKey": "{env:GEMINI_API_KEY}"
    },
    "openrouter": {
      "apiKey": "{env:OPENROUTER_API_KEY}"
    }
  },
  "server": {
    "port": 4096,
    "hostname": "0.0.0.0",
    "enabled": true
  },
  "agent": {
    "plan": {
      "mode": "primary",
      "model": "opencode/deepseek-v4-flash-free",
      "permission": {
        "edit": "deny",
        "bash": "deny",
        "read": "allow",
        "glob": "allow",
        "grep": "allow",
        "webfetch": "allow",
        "websearch": "allow",
        "skill": "allow"
      }
    },
    "build": {
      "mode": "primary",
      "permission": {
        "edit": "allow",
        "bash": "allow",
        "read": "allow",
        "glob": "allow",
        "grep": "allow",
        "webfetch": "allow",
        "websearch": "allow",
        "skill": "allow",
        "task": { "*": "allow" }
      }
    }
  },
  "command": {
    "team-growth": {
      "description": "Monta Growth Strike Team",
      "template": "Ative o @growth-team e convoque @cro-lab + @midia-paga + @seo-visibilidade + @copy-content"
    },
    "team-content": {
      "description": "Monta Content Factory",
      "template": "Ative o @content-studio e convoque @estrategia-marketing + @copy-content + @criacao-design + @seo-visibilidade"
    },
    "team-account": {
      "description": "Monta Client Success Pod",
      "template": "Ative o @account-orchestrator e convoque @receita-crescimento + @pesquisador + @vendas-account + @flag-churn"
    },
    "team-launch": {
      "description": "Monta Launch Squad",
      "template": "Ative o @launch-pad e convoque @estrategia-marketing + @copy-content + @midia-paga + @criacao-design + @seo-visibilidade"
    },
    "orquestra": {
      "description": "Mapa completo da Agent Orchestra V4",
      "template": "Leia ORCHESTRA.md e apresente o mapa dos 35 subagentes"
    },
    "session-save": {
      "description": "Exporta sessão para log/",
      "template": "Exporte a sessão atual para log/ usando scripts/session-save.sh"
    },
    "session-list": {
      "description": "Lista sessões salvas",
      "template": "Liste as sessões em log/ e as ativas no OpenCode"
    },
    "session-load": {
      "description": "Carrega sessão anterior",
      "template": "Liste as sessões em log/, usuário escolhe, carrega contexto"
    }
  }
}
```

### 6.3 Como os agentes são carregados no OpenCode Web

```
1. Container OpenCode inicia com opencode web
2. OpenCode lê opencode.json do /workspace
3. Varre .opencode/agents/ e registra cada .md como subagente
4. Varre .opencode/skills/ e carrega as skills
5. Fim: ambiente pronto no browser

Browser abre → https://opencode.fvmarketing.com.br
Autentica → prompt aparece
Digita → @analista-dados "..." → agente responde
```

---

## 7. Modelos e Alocação por Agente

### Estratégia de 3 Tiers + 3 Providers

Para evitar rate limits, cada agente usa um modelo diferente de acordo com sua função,
distribuídos entre os 3 provedores gratuitos:

### Tier A — DeepSeek V4 Flash Free (Zen) — Análise e Raciocínio

| Agente | Contexto | Ideal para |
|--------|:--------:|------------|
| `@analista-dados` | 1M | Análise de performance, OKRs, métricas |
| `@revisor` | 1M | Validação cruzada de dados |
| `@flag-roi` | 1M | Diagnóstico ROAS |
| `@flag-churn` | 1M | Risco de churn |
| `@flag-okr` | 1M | Desvio de OKR |
| `@flag-operacao` | 1M | Sprint travada |
| `@executor-comite` | 1M | Briefing do comitê |
| `@estrategia-marketing` | 1M | Pesquisa e posicionamento |
| `@growth-team` | 1M | Orquestração growth |
| `@content-studio` | 1M | Planejamento conteúdo |
| `@account-orchestrator` | 1M | Orquestração CSM |
| `@launch-pad` | 1M | Lançamento |
| `@revenue-ops` | 1M | Funil de receita |
| `@cmoorch` | 1M | Estratégia marketing |

### Tier B — MiniMax M2.5 Free (Zen) — Subagentes Leves

| Agente | Contexto | Ideal para |
|--------|:--------:|------------|
| `@cro-otimizacao` | 1M | CRO de páginas |
| `@cro-lab` | 1M | Pipeline de experimentos |
| `@midia-paga` | 1M | Planejamento campanha |
| `@copy-content` | 1M | Draft de copy |
| `@vendas-account` | 1M | Sales collateral |
| `@media-buyer` | 1M | Media buying |
| `@automacao-analytics` | 1M | Setup tracking |
| `@n8n-automator` | 1M | Workflows n8n |
| `@pipeline-conteudo` | 1M | Pipeline editorial |
| `@relatorios-trafego` | 1M | Reports tráfego |
| `@receita-crescimento` | 1M | Pricing e churn |

### Tier C — Gemini 2.5 Flash (Google) — Geração Visual

| Agente | Contexto | Ideal para |
|--------|:--------:|------------|
| `@gerar-pdf` | 1M | PDFs estilizados |
| `@gerar-ppt` | 1M | Apresentações |
| `@gerar-html` | 1M | Páginas web |
| `@gerar-doc` | 1M | Documentos |
| `@criacao-design` | 1M | Design e interfaces |

### Tier D — GPT-OSS-120B Free (OpenRouter) — Orquestração

| Agente | Contexto | Ideal para |
|--------|:--------:|------------|
| `@csm-orquestrador` | 131K | Setup CSM, triagem flags |
| `@estrategia-lideranca` | 131K | Sabatina, brainstorm |

### Fallbacks (quando rate limit bater)

| Agente principal | Fallback |
|-----------------|----------|
| DeepSeek V4 Flash | `qwen/qwen3-coder:free` (OR) |
| MiniMax M2.5 | `mistralai/mistral-small-3.1-24b-instruct:free` (OR) |
| Gemini 2.5 Flash | `google/gemini-2.0-flash:free` (OR) |

### Rate Limit Awareness

```
Máximo por modelo free:
  Zen:    ~20 req/min (não documentado, estimado)
  Google: ~60 req/min (não documentado, estimado)
  OR:     ~20 req/min, ~200 req/dia

Estratégia:
  1. Distribuir entre 3 providers (não concentrar)
  2. Sequenciar em vez de paralelizar
  3. Fallback automático via LiteLLM
  4. Orçamento de contingência: ~$20-55/mês se free sumirem
```

---

## 8. Fases de Implementação

### Fase 1 — Diagnóstico e Correção (1-2 dias)

| # | Ação | Responsável | Entrega |
|---|------|-------------|---------|
| 1.1 | Acessar VPS, ver Dokploy, entender setup atual | Dev | Diagnóstico |
| 1.2 | Verificar se agentes e skills estão no container | Dev | Relatório |
| 1.3 | Corrigir modelos dos geradores (gpt-oss-120 pago → Gemini gratis) | Dev | 4 agentes corrigidos |
| 1.4 | Criar volume persistente no Dokploy pro repositório | Dev | Volume configurado |
| 1.5 | Sincronizar repo local → VPS (git pull no volume) | Dev | Código no ar |

### Fase 2 — Infraestrutura Base (3-5 dias)

| # | Ação | Responsável | Entrega |
|---|------|-------------|---------|
| 2.1 | Subir docker-compose com LiteLLM + Qdrant + Langfuse | Dev | Stack rodando |
| 2.2 | Configurar LiteLLM com modelos free + rate limits | Dev | Gateway funcionando |
| 2.3 | Conectar OpenCode → LiteLLM (opcional: via proxy) | Dev | Rota alternativa |
| 2.4 | Subir Langfuse com tracing das chamadas | Dev | Observabilidade |
| 2.5 | Configurar healthcheck + auto-restart dos containers | Dev | Resiliência |

### Fase 3 — Automações e Agentes (3-5 dias)

| # | Ação | Responsável | Entrega |
|---|------|-------------|---------|
| 3.1 | Testar todos os 35 agentes no web | Squad | Validação |
| 3.2 | Testar comandos de time (/team-growth, /team-content, etc) | Squad | Orquestração |
| 3.3 | Configurar cron do comitê de segunda (domingo 20h) | Dev | Automação |
| 3.4 | Configurar detector de flags (quinta 7h) | Dev | Automação |
| 3.5 | Testar rate limits com carga real | Dev | Limites conhecidos |

### Fase 4 — Governança e Segurança (3-5 dias)

| # | Ação | Responsável | Entrega |
|---|------|-------------|---------|
| 4.1 | Configurar chaves virtuais no LiteLLM por squad | Dev | Isolamento |
| 4.2 | Definir tetos de gastos por squad | Coord. | Budget |
| 4.3 | Configurar Langfuse alertas de anomalia | Dev | Monitoramento |
| 4.4 | Documentar procedimentos de segurança | Coord. | Manual |
| 4.5 | Testar fallback: derrubar Zen, ver se vai pro OR | Dev | Resiliência |

### Fase 5 — Escala e Otimização (contínuo)

| # | Ação | Responsável | Entrega |
|---|------|-------------|---------|
| 5.1 | Avaliar migração para modelos pagos (~$20-55/mês) | Coord. | Budget |
| 5.2 | Configurar cache semântico no LiteLLM | Dev | Economia |
| 5.3 | Onboarding de novos squads no Dokploy | Dev | Expansão |
| 5.4 | Revisar alocação de modelos por agente | Squad | Ajuste fino |

---

## 9. Custos e Viabilidade

### Custos Fixos (Infraestrutura)

| Item | Custo | Nota |
|------|:----:|------|
| VPS (Hetzner CX42: 4 vCPU, 16GB RAM) | ~$15/mês | Comporta stack inteira |
| Docker Compose (OpenCode + LiteLLM + n8n + Qdrant + Langfuse) | $0 | Todos open-source |
| Domínio + SSL (fvmarketing.com.br) | ~$10/mês | Já existe |
| **Total fixo** | **~$25/mês** | |

### Custos Variáveis (APIs)

| Cenário | Custo | Situação |
|---------|:----:|----------|
| 100% free (Zen + Google + OR free) | **$0** | Hoje |
| Free + contingência LiteLLM | **~$5/mês** | Se algum free cair |
| Todos os free sumirem (modelos pagos mínimos) | **~$20-55/mês** | Cenário pessimista |

### Projeção de Crescimento

```
Mês 1-2:            $0/mês   (free models, testando)
Mês 3-4:            $5-15/mês (primeiros pagos por confiabilidade)
Mês 5-6:           $20-40/mês (escala com 3 squads)
Mês 7-12:          $50-100/mês (produção consolidada)
```

### O que $20-55/mês compra (se os free sumirem)

| Modelo Pago | Custo | Substitui |
|-------------|:----:|-----------|
| DeepSeek V4 Flash ($0.14/$0.28) | ~$10/mês | DeepSeek V4 Flash Free |
| MiniMax M2.5 ($0.30/$1.20) | ~$5/mês | MiniMax M2.5 Free |
| Gemini Flash API (Google, quase gratis) | ~$2/mês | Gemini Free |
| OpenRouter free (ainda existe) | $0 | Fallback |

---

## Apêndice A — Comandos Úteis para VPS

```bash
# Ver containers rodando
docker ps

# Ver logs do OpenCode Web
docker logs v4-opencode --tail 50 -f

# Entrar no container
docker exec -it v4-opencode bash

# Testar se agente existe
docker exec v4-opencode ls .opencode/agents/ | wc -l

# Sincronizar repo manualmente
cd /data/v4-repo && git pull origin main

# Reiniciar OpenCode após sincronia
docker restart v4-opencode

# Ver healthcheck
curl -I https://opencode.fvmarketing.com.br

# Ver consumo de recursos
docker stats v4-opencode v4-litellm v4-n8n
```

## Apêndice B — Arquitetura de Permissões dos Agentes

```
Agente               | read | edit | bash | webfetch | Pode sem revisão
─────────────────────|──────|──────|──────|──────────|──────────────────
analista-dados       | ✅  | ✅  | ✅  | ✅      | Relatórios internos
revisor              | ✅  | ❌  | ❌  | ✅      | — (só valida)
gerar-pdf/ppt/html   | ✅  | ✅  | ✅  | ❌      | Documentos (assets)
flag-*               | ✅  | ❌  | ✅  | ❌      | Diagnóstico (não executa)
csm-orquestrador     | ✅  | ✅  | ✅  | ✅      | Setup inicial (com revisão)
executor-comite      | ✅  | ✅  | ✅  | ✅      | Briefings (com revisor)
```

---

*Documento gerado em junho/2026. Baseado no original "Infraestrutura de AI (Em construção).pdf",
corrigido para refletir o uso de OpenCode Web no lugar de Open WebUI, e estendido com a
Agent Orchestra V4 (35 agentes, 66 skills, 3 providers).*
