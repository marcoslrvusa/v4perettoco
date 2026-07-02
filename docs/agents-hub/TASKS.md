# Agents Hub — Plano de Execução

> **4 tasks · 40+ skills · 36 agentes · 1 VPS · US$ 0/mês em inferência**
>
> Documento de planejamento, instalação e registro do sistema multi-agente V4
>
> Versão: 1.0 | Junho 2026 | Autor: Marcos Luciano

---

## Índice

1. [Visão Geral do Projeto](#1-visão-geral-do-projeto)
2. [Task 1 — Sessões de Validação por Cargo](#2-task-1--sessões-de-validação-por-cargo)
3. [Task 2 — Refinamento dos SKILL.md Pós-Validação](#3-task-2--refinamento-dos-skillmd-pós-validação)
4. [Task 3 — Estrutura Base do Agente no OpenCode (Account/CSM)](#4-task-3--estrutura-base-do-agente-no-opencode-accountcsm)
5. [Task 4 — Scaffold do Serviço na VPS](#5-task-4--scaffold-do-serviço-na-vps)
6. [Catálogo de Skills por Área](#6-catálogo-de-skills-por-área)
7. [Skills de Base (Infraestrutura)](#7-skills-de-base-infraestrutura)
8. [Skills de Fonte (Integrações)](#8-skills-de-fonte-integrações)
9. [Guia de Instalação no OpenCode](#9-guia-de-instalação-no-opencode)
10. [Guia de Uso por Squad](#10-guia-de-uso-por-squad)
11. [Anexo — Caminhos das Skills no Repositório](#11-anexo--caminhos-das-skills-no-repositório)

---

## 1. Visão Geral do Projeto

### O que é o Agents Hub

O **Agents Hub** é a infraestrutura compartilhada de agentes de IA da V4 Company. Ele transforma o repositório de skills do Builders Hub em uma força de trabalho orquestrada — cada skill é um instrumento, cada agente é um músico, e o OpenCode na VPS é o palco.

### Stack Completa

```
┌──────────────────────────────────────────────────────────────┐
│                    SQUADS (usuários)                          │
│  browser → https://opencode.v4.company.com                    │
│  Account · GT · Copy · Design · CSM · Coordenação            │
└──────────────────────────┬───────────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────────┐
│                    OpenCode Web (VPS)                         │
│                                                               │
│  36 agentes · 40+ skills · sessões compartilhadas            │
│                                                               │
│  @account-orchestrator  @media-buyer  @copy-content  @design │
│  @csm-orquestrador     @analista-dados  @revisor  @flags     │
└──────┬──────────────────────┬──────────────────────┬─────────┘
       │                      │                      │
┌──────▼──────┐        ┌─────▼─────┐         ┌──────▼──────┐
│  LiteLLM    │        │  MCPs     │         │   n8n        │
│  (modelos)  │        │  Drive,   │         │  (automação) │
│  virtual    │        │  Ekyte,   │         │              │
│  keys       │        │  People   │         │  relatórios  │
│  rate limit │        │           │         │  flags       │
└──────┬──────┘        └─────┬─────┘         └──────┬──────┘
       │                      │                      │
┌──────▼──────┐        ┌─────▼─────┐         ┌──────▼──────┐
│  DeepSeek   │        │  Google   │         │  Meta Ads   │
│  Gemini     │        │  Drive    │         │  Google Ads │
│  GPT-OSS    │        │  Ekyte    │         │  APIs       │
│  MiniMax    │        │           │         │             │
└─────────────┘        └───────────┘         └─────────────┘
```

### Custo

| Item | Custo |
|------|-------|
| Modelos de IA (DeepSeek, Gemini, GPT-OSS, MiniMax) | **US$ 0/mês** |
| VPS Hostinger (4 vCPU, 16GB RAM) | ~US$ 15/mês |
| Domínio | US$ 0 (já existe) |
| **Total** | **~US$ 15/mês** |

---

## 2. Task 1 — Sessões de Validação por Cargo

### Objetivo

Validar com cada área (Account, Tráfego, Copy, Design) o que cada agente deve gerar, como deve ser o fluxo e quais dados precisa acessar.

### Duração: Semana 1-2

### Formato: 30 min por área (presencial ou call)

### Roteiro de cada sessão

#### Sessão Account (Agente: @account-orchestrator)

**Participantes:** Account(s) do squad

**Pauta:**

1. Mostrar o fluxo existente em `docs/agent-hub/03-fluxos/01-account.md`
2. Validar o ciclo: Pré-call → Call → Pós-call
3. Confirmar skills envolvidas:

| Skill | O que faz | Já existe? |
|-------|-----------|------------|
| `account-checkin-roleplay` | Prepara account pra reunião com ROPRE V4 | ✅ `.agents/skills/account-checkin-roleplay/` |
| `account-checkin-review` | Processa transcript, atualiza Mission Control | ✅ `.agents/skills/account-checkin-review/` |
| `account-evolucao-checkins` | Relatório de progressão entre check-ins | ✅ `.agents/skills/account-evolucao-checkins/` |
| `account-handoff` | Setup inicial quando cliente chega de vendas | ✅ `.agents/skills/account-handoff/` |
| `account-pesquisa-profunda-cliente` | Pesquisa profunda pra KB | ✅ `.agents/skills/account-pesquisa-profunda-cliente/` |

4. Validar output esperado:
   - Pré-call: resumo com pauta, tasks pendentes, tickets abertos
   - Pós-call: combinados viram tarefas no Ekyte, flags viram tickets
   - Periódico: relatório de evolução com score de saúde

5. Pergunta-chave: "O que mais o agente poderia gerar que hoje você perde tempo fazendo?"

**Entregável:** Ata da sessão com ajustes validados

---

#### Sessão Tráfego/GT (Agentes: @media-buyer, @midia-paga, @relatorios-trafego)

**Participantes:** GT(s) do squad

**Pauta:**

1. Mostrar o fluxo existente em `docs/agent-hub/03-fluxos/03-gt.md`
2. Validar o ciclo: Análise → Ação → Reporte
3. Confirmar skills envolvidas:

| Skill | O que faz | Já existe? |
|-------|-----------|------------|
| `gt-media-buyer-completo` | Arquitetura de contas, análise preditiva, otimização ROAS/CPA | ✅ `.agents/skills/gt-media-buyer-completo/` |
| `gt-relatorios-trafego` | Relatório consolidado multicanal com detecção de anomalias | ✅ `.agents/skills/gt-relatorios-trafego/` |
| `v4mos-dados-meta-ads` | Puxa dados de Meta Ads via API V4mos | ✅ `.agents/skills/v4mos-dados-meta-ads/` |
| `analytics-tracking` | Setup e auditoria de tracking (GA4, GTM) | ✅ `.agents/skills/analytics-tracking/` |
| `paid-ads` | Estratégia de campanhas Google/Meta/LinkedIn | ✅ `.agents/skills/paid-ads/` |

4. Validar fontes de dados:
   - Meta Ads → via API V4mos
   - Google Ads → via API Google
   - GA4 → via API Google
   - Ekyte → via MCP

5. Pergunta-chave: "Qual relatório você mais gasta tempo montando hoje?"

**Entregável:** Ata da sessão com fontes de dados confirmadas

---

#### Sessão Copy (Agentes: @content-studio, @copy-content, @pipeline-conteudo)

**Participantes:** Copywriter(s) do squad

**Pauta:**

1. Mostrar o fluxo existente em `docs/agent-hub/03-fluxos/02-copy.md`
2. Validar o ciclo: Briefing → Produção → Aprovação
3. Confirmar skills envolvidas:

| Skill | O que faz | Já existe? |
|-------|-----------|------------|
| `copywriting` | Escreve copy de páginas, emails, anúncios, LPs | ✅ `.agents/skills/copywriting/` |
| `copy-editing` | Edita e revisa copy existente | ✅ `.agents/skills/copy-editing/` |
| `copy-pipeline-conteudo` | Pipeline completo de conteúdo editorial | ✅ `.agents/skills/copy-pipeline-conteudo/` |
| `content-strategy` | Planejamento de conteúdo, tópicos, calendário | ✅ `.agents/skills/content-strategy/` |
| `email-sequence` | Sequências de email, nutrição, onboarding | ✅ `.agents/skills/email-sequence/` |
| `social-content` | Conteúdo para redes sociais, threads, scripts | ✅ `.agents/skills/social-content/` |
| `seo-audit` | Auditoria SEO técnica e on-page | ✅ `.agents/skills/seo-audit/` |
| `ai-seo` | Otimização para AI Search (AEO/GEO) | ✅ `.agents/skills/ai-seo/` |

4. Validar output:
   - Briefing chega → agente lê do Drive + Ekyte
   - Produz rascunho → salva no Drive, comenta no Ekyte
   - Revisão → ciclo de feedback até aprovação

5. Pergunta-chave: "Qual tipo de conteúdo você mais produz? Onde está o briefing hoje?"

**Entregável:** Ata da sessão com tipos de conteúdo priorizados

---

#### Sessão Design (Agentes: @criacao-design, @gerar-html, @gerar-pdf, @gerar-ppt)

**Participantes:** Designer(s) do squad

**Pauta:**

1. Mostrar que o agente de Design gera:
   - Interfaces HTML/CSS/JS completas
   - Imagens (via prompts para ferramentas de IA)
   - Apresentações em HTML interativo
   - PDFs estilizados
2. Confirmar skills envolvidas:

| Skill | O que faz | Já existe? |
|-------|-----------|------------|
| `geral-frontend-design` | Cria interfaces frontend de alta qualidade | ✅ `.agents/skills/geral-frontend-design/` |
| `image` | Cria e otimiza imagens para marketing | ✅ `.agents/skills/image/` |
| `video` | Produz vídeos com ferramentas de IA | ✅ `.agents/skills/video/` |
| `ad-creative` | Gera criativos de anúncios em escala | ✅ `.agents/skills/ad-creative/` |

3. Validar fluxo de briefing:
   - Account/copy abre task no Ekyte com briefing
   - Agente de design lê briefing, gera assets
   - Salva no Drive, comenta no Ekyte

4. Pergunta-chave: "Qual o tipo de demanda mais frequente? O briefing chega completo?"

**Entregável:** Ata da sessão com tipos de asset priorizados

---

### Checklist de Validação (para TODAS as sessões)

- [ ] Fluxo proposto faz sentido para o time?
- [ ] Skills listadas cobrem as necessidades?
- [ ] Faltou alguma skill?
- [ ] Fontes de dados estão corretas?
- [ ] Output esperado é útil?
- [ ] O que mudar no SKILL.md?

---

## 3. Task 2 — Refinamento dos SKILL.md Pós-Validação

### Objetivo

Ajustar a lógica de cada agente com base no que sair das sessões de validação.

### Duração: Semana 2-3

### O que refinar em cada SKILL.md

Cada skill em `.agents/skills/{nome}/SKILL.md` tem esta estrutura:

```yaml
---
name: {prefixo}-{nome}
description: ...
---
```

O refinamento pós-validação deve ajustar:

1. **Descrição** — está clara o suficiente para o OpenCode entender quando invocar?
2. **Trigger phrases** — adicionar termos que o time usa no dia a dia
3. **Workflow** — o passo-a-passo reflete a realidade da área?
4. **Input esperado** — o que o usuário precisa fornecer?
5. **Output gerado** — o formato está correto?
6. **Integrações** — quais MCPs/APIs precisa acessar?

### Como fazer

```bash
# Para cada skill validada:
# 1. Leia o SKILL.md atual
# 2. Aplique os ajustes da sessão
# 3. Garanta duplo-write (espelhar em .claude/skills/)

# Skills do Account
code .agents/skills/account-checkin-roleplay/SKILL.md
code .agents/skills/account-checkin-review/SKILL.md
code .agents/skills/account-evolucao-checkins/SKILL.md
code .agents/skills/account-handoff/SKILL.md
code .agents/skills/account-pesquisa-profunda-cliente/SKILL.md

# Skills do GT
code .agents/skills/gt-media-buyer-completo/SKILL.md
code .agents/skills/gt-relatorios-trafego/SKILL.md

# Skills do Copy
code .agents/skills/copywriting/SKILL.md
code .agents/skills/copy-editing/SKILL.md
code .agents/skills/copy-pipeline-conteudo/SKILL.md

# Skills do Design
code .agents/skills/geral-frontend-design/SKILL.md
```

### Entregável

- SKILL.md de cada área atualizado com feedback das sessões
- Duplo-write verificado (`.agents/` ↔ `.claude/`)

---

## 4. Task 3 — Estrutura Base do Agente no OpenCode (Account/CSM)

### Objetivo

Criar/configurar os agentes de Account e CSM no OpenCode para que estejam disponíveis para o squad.

### Duração: Semana 3-4

### O que já existe

Os arquivos de agente já foram criados em `.opencode/agents/`:

| Agente | Arquivo | Modelo |
|--------|---------|--------|
| `@account-orchestrator` | `.opencode/agents/account-orchestrator.md` | `deepseek-v4-flash-free` |
| `@csm-orquestrador` | `.opencode/agents/csm-orquestrador.md` | `gpt-oss-120b:free` |
| `@flag-roi` | `.opencode/agents/flag-roi.md` | `deepseek-v4-flash-free` |
| `@flag-churn` | `.opencode/agents/flag-churn.md` | `deepseek-v4-flash-free` |
| `@flag-okr` | `.opencode/agents/flag-okr.md` | `deepseek-v4-flash-free` |
| `@flag-operacao` | `.opencode/agents/flag-operacao.md` | `deepseek-v4-flash-free` |
| `@revisor` | `.opencode/agents/revisor.md` | `deepseek-v4-flash-free` |
| `@analista-dados` | `.opencode/agents/analista-dados.md` | `deepseek-v4-flash-free` |
| `@executor-comite` | `.opencode/agents/executor-comite.md` | `deepseek-v4-flash-free` |

### Fluxo Account/CSM (já implementado nos agentes)

```
PRÉ-CHECK-IN                          PÓS-CHECK-IN
     │                                     │
     ▼                                     ▼
@account-checkin-roleplay           @account-checkin-review
→ Carrega KB do cliente             → Lê transcript da call
→ Puxa tasks do Ekyte               → Extrai combinados
→ Puxa pauta do Drive               → Cria tarefas no Ekyte
→ Simula personas da call           → Atualiza Mission Control
→ Gera resumo + perguntas           → Se flag: aciona CSM
     │                                     │
     └──────────────┬──────────────────────┘
                    ▼
         @account-orchestrator
    (coordena o ciclo completo)
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
   @flag-roi   @flag-churn   @flag-okr
   (ROAS)      (NPS/CSAT)    (OKR)

         @csm-orquestrador
    (acima do squad, orquestra)
        │
        ▼
   @executor-comite
   (briefing semanal do comitê)
```

### Como ativar no OpenCode

```bash
# Os agentes já estão em .opencode/agents/
# O OpenCode lê automaticamente desta pasta

# Para testar o agente Account:
@account-orchestrator Vou ter check-in com o cliente X amanhã. Me prepara.

# Para testar o revisor:
@revisor Revise este relatório antes de eu enviar.

# Para testar o CSM:
@csm-orquestrador Inicie o setup da unidade Squad Prime.
```

### Entregável

- Agentes Account/CSM funcionais no OpenCode
- Teste de ciclo completo: roleplay → call → review → flag

---

## 5. Task 4 — Scaffold do Serviço na VPS

### Objetivo

Subir a infraestrutura na VPS 2 para que todos os agentes estejam disponíveis via browser.

### Duração: Semana 3-4 (pode rodar em paralelo com Task 3)

### Pré-requisitos

- [ ] VPS Hostinger acessível (SSH)
- [ ] Docker instalado
- [ ] OpenCode Web instalado
- [ ] LiteLLM configurado
- [ ] n8n instalado
- [ ] Domínio configurado (opencode.v4.company.com)
- [ ] SSL via Let's Encrypt

### Passo a passo

```bash
# 1. Conectar na VPS
ssh usuario@vps-hostinger

# 2. Clonar o repositório
git clone https://github.com/v4company/builders-hub.git /home/opencode/hub
cd /home/opencode/hub

# 3. Instalar dependências
pip install -r v4-automations/setup/requirements.txt

# 4. Configurar .env
cp config/.env.template config/.env
# Editar com as credenciais:
#   - GEMINI_API_KEY
#   - OPENROUTER_API_KEY
#   - EKYTE_MCP_TOKEN
#   - GOOGLE_OAUTH_CLIENT_ID / SECRET

# 5. Subir OpenCode Web
opencode web \
  --host 0.0.0.0 \
  --port 4096 \
  --password "${OPENCODE_SERVER_PASSWORD}"

# 6. Subir LiteLLM (gateway de modelos)
docker run -d \
  --name litellm \
  -p 4000:4000 \
  -v $(pwd)/litellm-config.yaml:/app/config.yaml \
  ghcr.io/berriai/litellm:main \
  --config /app/config.yaml

# 7. Configurar n8n
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v n8n-data:/home/node/.n8n \
  -e N8N_SECURE_COOKIE=false \
  n8nio/n8n

# 8. Configurar Nginx (reverse proxy)
# /etc/nginx/sites-available/opencode.v4.company.com
server {
    listen 443 ssl;
    server_name opencode.v4.company.com;
    
    ssl_certificate /etc/letsencrypt/live/opencode.v4.company.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/opencode.v4.company.com/privkey.pem;
    
    location / {
        proxy_pass http://localhost:4096;
        proxy_set_header Host $host;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}

# 9. Configurar crons
python v4-automations/setup/install_cron.py

# 10. Testar
openCode web health
```

### Configuração LiteLLM

```yaml
# litellm-config.yaml
model_list:
  - model_name: deepseek-v4-flash
    litellm_params:
      model: openrouter/deepseek/deepseek-v4-flash:free
      api_key: os.environ/OPENROUTER_API_KEY
      rpm: 10

  - model_name: gemini-2.5-flash
    litellm_params:
      model: gemini/gemini-2.5-flash
      api_key: os.environ/GEMINI_API_KEY
      rpm: 10

  - model_name: gpt-oss-120b
    litellm_params:
      model: openrouter/openai/gpt-oss-120b:free
      api_key: os.environ/OPENROUTER_API_KEY
      rpm: 5

  - model_name: minimax-m2.5
    litellm_params:
      model: openrouter/minimax/minimax-m2.5:free
      api_key: os.environ/OPENROUTER_API_KEY
      rpm: 15
```

### Configuração opencode.json (VPS)

```json
{
  "model": "opencode/deepseek-v4-flash-free",
  "provider": {
    "gemini": { "apiKey": "{env:GEMINI_API_KEY}" },
    "openrouter": { "apiKey": "{env:OPENROUTER_API_KEY}" }
  },
  "mcp": {
    "ekyte": {
      "type": "remote",
      "url": "https://api.ekyte.com/mcp?token={env:EKYTE_MCP_TOKEN}",
      "enabled": true
    },
    "google-drive": {
      "type": "remote",
      "url": "https://google-drive-mcp.example.com/mcp",
      "oauth-client-id": "{env:GOOGLE_OAUTH_CLIENT_ID}",
      "enabled": true
    }
  },
  "agent": {
    "build": {
      "mode": "primary",
      "permission": { "edit": "allow", "bash": "allow", "read": "allow" }
    }
  }
}
```

### Verificação de Saúde

```bash
# Testar conectividade
curl https://opencode.v4.company.com/health

# Testar modelo
opencode chat -m deepseek-v4-flash "teste"

# Testar agente
opencode run @account-orchestrator "status"

# Verificar logs
docker logs litellm --tail 50
```

### Entregável

- VPS com OpenCode Web acessível via browser
- LiteLLM configurado com modelos gratuitos
- n8n com crons instalados
- Agentes funcionando e disponíveis para o squad

---

## 6. Catálogo de Skills por Área

### Account (5 skills)

| # | Skill | Pasta | Descrição |
|---|-------|-------|-----------|
| 1 | `account-checkin-roleplay` | `.agents/skills/account-checkin-roleplay/` | Prepara account pra reunião de check-in com ROPRE V4 e roleplay realista |
| 2 | `account-checkin-review` | `.agents/skills/account-checkin-review/` | Pós-call: lê transcript, atualiza Mission Control, registra combinados |
| 3 | `account-evolucao-checkins` | `.agents/skills/account-evolucao-checkins/` | Relatório de progressão entre check-ins com score de saúde |
| 4 | `account-handoff` | `.agents/skills/account-handoff/` | Primeira skill ao receber cliente novo de vendas — gera KB inicial |
| 5 | `account-pesquisa-profunda-cliente` | `.agents/skills/account-pesquisa-profunda-cliente/` | Pesquisa profunda com Deep Research do Gemini para KB acionável |

**Como usar:**
```
@account-checkin-roleplay Vou ter check-in com o cliente X amanhã. Me prepara.

@account-checkin-review Processa o transcript da call que acabei com o cliente X.

@account-evolucao-checkins Gera relatório de evolução do cliente X entre março e junho.

@account-handoff Recebi o cliente Y de vendas. Aqui está o form + transcript.

@account-pesquisa-profunda-cliente Preciso de pesquisa profunda do cliente Z para embasar a estratégia.
```

---

### Gestão de Tráfego / GT (5 skills)

| # | Skill | Pasta | Descrição |
|---|-------|-------|-----------|
| 6 | `gt-media-buyer-completo` | `.agents/skills/gt-media-buyer-completo/` | Gestão de tráfego completa: arquitetura, análise preditiva, otimização |
| 7 | `gt-relatorios-trafego` | `.agents/skills/gt-relatorios-trafego/` | Relatório consolidado multicanal com detecção de anomalias |
| 8 | `v4mos-dados-meta-ads` | `.agents/skills/v4mos-dados-meta-ads/` | Puxa dados de Meta Ads via API V4mos |
| 9 | `analytics-tracking` | `.agents/skills/analytics-tracking/` | Setup e auditoria de tracking (GA4, GTM, eventos) |
| 10 | `paid-ads` | `.agents/skills/paid-ads/` | Estratégia de campanhas em Google, Meta, LinkedIn |

**Como usar:**
```
@media-buyer Analisa ROAS do cliente X nos últimos 30 dias.

@relatorios-trafego Gera relatório semanal consolidado do cliente X.

@v4mos-dados-meta-ads Quais campanhas mais gastaram essa semana no cliente X?

@analytics-tracking Configura conversão de lead no GA4 para o cliente X.

@midia-paga Preciso de estratégia de campanha para o lançamento do cliente X.
```

---

### Copy / Conteúdo (8 skills)

| # | Skill | Pasta | Descrição |
|---|-------|-------|-----------|
| 11 | `copywriting` | `.agents/skills/copywriting/` | Escreve copy para páginas, LPs, emails, anúncios |
| 12 | `copy-editing` | `.agents/skills/copy-editing/` | Edita e revisa copy existente |
| 13 | `copy-pipeline-conteudo` | `.agents/skills/copy-pipeline-conteudo/` | Pipeline editorial: calendário → produção → aprovação → Drive |
| 14 | `content-strategy` | `.agents/skills/content-strategy/` | Planejamento de conteúdo, tópicos, calendário editorial |
| 15 | `email-sequence` | `.agents/skills/email-sequence/` | Sequências de email: nutrição, onboarding, re-engajamento |
| 16 | `social-content` | `.agents/skills/social-content/` | Conteúdo para redes sociais, threads, scripts de vídeo |
| 17 | `seo-audit` | `.agents/skills/seo-audit/` | Auditoria SEO técnica e on-page |
| 18 | `ai-seo` | `.agents/skills/ai-seo/` | Otimização para AI Search (AEO, GEO, LLMO) |

**Como usar:**
```
@copy-content Produz LP para campanha de verão do cliente X. Briefing no Drive.

@copy-editing Revisa esta página de serviço e melhora a copy.

@pipeline-conteudo Gera calendário editorial de 4 semanas para o cliente X.

@estrategia-marketing Pesquisa o mercado do cliente X e sugere tópicos de conteúdo.

@seo-visibilidade Auditoria técnica do site do cliente X.
```

---

### Design / Criação (4 skills)

| # | Skill | Pasta | Descrição |
|---|-------|-------|-----------|
| 19 | `geral-frontend-design` | `.agents/skills/geral-frontend-design/` | Cria interfaces frontend de alto nível |
| 20 | `image` | `.agents/skills/image/` | Cria, edita e otimiza imagens para marketing |
| 21 | `video` | `.agents/skills/video/` | Produz vídeos com IA (Remotion, HeyGen, Runway) |
| 22 | `ad-creative` | `.agents/skills/ad-creative/` | Gera variações de criativos para anúncios |

**Como usar:**
```
@criacao-design Cria landing page para campanha do cliente X.

@gerar-html Dashboard de performance do cliente X com gráficos.

@gerar-pdf Relatório de OKRs do cliente X para o comitê.

@gerar-ppt Apresentação do Q3 para o cliente X.
```

---

## 7. Skills de Base (Infraestrutura)

Skills que qualquer papel usa. São o "sistema operacional" do Builders Hub.

| # | Skill | Pasta | Descrição |
|---|-------|-------|-----------|
| 23 | `onboarding` | `.agents/skills/onboarding/` | Configura ambiente, valida git/gh, instala dependências |
| 24 | `sync-hub` | `.agents/skills/sync-hub/` | Puxa skills mais recentes do repositório público |
| 25 | `contexto` | `.agents/skills/contexto/` | Lê KB do cliente, gera CLAUDE.md/AGENTS.md, atualiza Mission Control |
| 26 | `criador-de-skills` | `.agents/skills/criador-de-skills/` | Cria skills novas com prefixo obrigatório |
| 27 | `compartilhar-skill` | `.agents/skills/compartilhar-skill/` | Empacota skill e abre PR no hub público |
| 28 | `novo-squad` | `.agents/skills/novo-squad/` | Cria estrutura de squad |
| 29 | `novo-cliente` | `.agents/skills/novo-cliente/` | Cria estrutura de cliente dentro de squad |
| 30 | `novo-projeto` | `.agents/skills/novo-projeto/` | Cria estrutura de projeto em bases/ |
| 31 | `geral-brainstormar-sobre-minha-funcao` | `.agents/skills/geral-brainstormar-sobre-minha-funcao/` | Descobre onde IA agrega valor no dia a dia |
| 32 | `geral-sabatina` | `.agents/skills/geral-sabatina/` | Stress-test de planos e decisões |
| 33 | `geral-frontend-design` | `.agents/skills/geral-frontend-design/` | Cria interfaces frontend de alta qualidade |
| 34 | `geral-log-sessoes` | `.agents/skills/geral-log-sessoes/` | Sistema de log de sessões do OpenCode |
| 35 | `opensquad` | `.agents/skills/opensquad/` | Cria e orquestra squads de agentes |

---

## 8. Skills de Fonte (Integrações)

Skills que puxam dados de APIs externas. Reutilizáveis por outras skills.

| # | Skill | Pasta | Descrição |
|---|-------|-------|-----------|
| 36 | `v4mos-dados-meta-ads` | `.agents/skills/v4mos-dados-meta-ads/` | Puxa dados de Meta Ads via API V4mos |
| 37 | `n8n-architect` | `.agents/skills/n8n-architect/` | Cria, edita e sincroniza workflows n8n |
| 38 | `supabase` | `.agents/skills/supabase/` | Operações com Supabase (DB, Auth, Functions) |

---

## 9. Guia de Instalação no OpenCode

### As skills já estão no repositório

Todas as skills listadas acima já existem no repositório em duas pastas:

- `.agents/skills/{nome}/` → para OpenCode
- `.claude/skills/{nome}/` → para Claude Code

### Como o OpenCode descobre as skills

O OpenCode lê automaticamente de:
1. `.opencode/skills/` — skills locais do projeto
2. `~/.config/opencode/skills/` — skills globais

As skills em `.agents/skills/` são carregadas quando você invoca o agente correspondente ou quando o OpenCode precisa delas.

### Para instalar uma skill específica

Se precisar instalar manualmente:

```bash
# Copiar skill para a pasta de skills do OpenCode
cp -r .agents/skills/nome-da-skill ~/.config/opencode/skills/

# Verificar se foi instalada
ls ~/.config/opencode/skills/nome-da-skill/
```

### Sincronizar com o hub público

```bash
# Puxar skills mais recentes do time
/sync-hub

# Compartilhar uma skill sua
/compartilhar-skill
```

### Ativar agentes no opencode.json

Os agentes em `.opencode/agents/` são carregados automaticamente pelo OpenCode. Para garantir:

```json
{
  "agent": {
    "account-orchestrator": {
      "path": ".opencode/agents/account-orchestrator.md"
    },
    "csm-orquestrador": {
      "path": ".opencode/agents/csm-orquestrador.md"
    }
  }
}
```

---

## 10. Guia de Uso por Squad

### Squad Account

| Quando | O que fazer |
|--------|-------------|
| Cliente novo chegou | `@account-handoff` + form + transcript |
| Check-in amanhã | `@account-checkin-roleplay` + nome do cliente |
| Call acabou | `@account-checkin-review` + transcript |
| Relatório mensal | `@account-evolucao-checkins` + cliente + período |
| ROAS caiu | `@flag-roi` + cliente |
| NPS caiu | `@flag-churn` + cliente |
| OKR atrasado | `@flag-okr` + cliente |
| Sprint travou | `@flag-operacao` + cliente |

### Squad GT

| Quando | O que fazer |
|--------|-------------|
| Analisar performance | `@media-buyer` analisa ROAS do cliente X nos últimos 30 dias |
| Relatório semanal | `@relatorios-trafego` gera relatório consolidado do cliente X |
| Dados Meta Ads | `@v4mos-dados-meta-ads` campanhas que mais gastaram essa semana |
| Nova campanha | `@midia-paga` estrutura campanha de prospecção para cliente X |
| Tracking | `@analytics-tracking` configura conversão no GA4 |

### Squad Copy

| Quando | O que fazer |
|--------|-------------|
| Produzir conteúdo | `@copy-content` produz LP para campanha X. Briefing no Drive. |
| Revisar copy | `@copy-editing` revisa esta página e melhora |
| Calendário | `@pipeline-conteudo` gera calendário de 4 semanas |
| Estratégia | `@estrategia-marketing` pesquisa mercado do cliente X |
| SEO | `@seo-visibilidade` auditoria técnica do site X |

### Squad Design

| Quando | O que fazer |
|--------|-------------|
| Landing page | `@criacao-design` cria landing page para campanha X |
| Dashboard | `@gerar-html` dashboard de performance do cliente X |
| PDF relatório | `@gerar-pdf` relatório de OKRs do cliente X |
| Apresentação | `@gerar-ppt` apresentação do Q3 para cliente X |

### CSM / Coordenação

| Quando | O que fazer |
|--------|-------------|
| Setup de unidade | `@csm-orquestrador` inicia setup da unidade |
| Briefing comitê | `@executor-comite` gera briefing do comitê |
| Flags semanais | `@csm-orquestrador` roda detecção de flags |
| Relatório geral | `@analista-dados` performance consolidada do squad |

---

## 11. Anexo — Caminhos das Skills no Repositório

Todas as skills estão fisicamente no repositório em:

```
.agents/skills/
├── account-checkin-roleplay/         SKILL.md
├── account-checkin-review/           SKILL.md
├── account-evolucao-checkins/        SKILL.md
├── account-handoff/                  SKILL.md
├── account-pesquisa-profunda-cliente/SKILL.md
├── ad-creative/                      SKILL.md
├── ai-search/                        SKILL.md
├── ai-seo/                           SKILL.md
├── analytics-tracking/               SKILL.md
├── aso-audit/                        SKILL.md
├── churn-prevention/                 SKILL.md
├── co-marketing/                     SKILL.md
├── cold-email/                       SKILL.md
├── community-marketing/              SKILL.md
├── compartilhar-skill/               SKILL.md
├── competitor-alternatives/          SKILL.md
├── competitor-profiling/             SKILL.md
├── content-strategy/                 SKILL.md
├── contexto/                         SKILL.md
├── copy-editing/                     SKILL.md
├── copy-pipeline-conteudo/           SKILL.md
├── copywriting/                      SKILL.md
├── criador-de-skills/                SKILL.md
├── customer-research/                SKILL.md
├── directory-submissions/            SKILL.md
├── email-sequence/                   SKILL.md
├── form-cro/                         SKILL.md
├── free-tool-strategy/               SKILL.md
├── geral-ai-visibility/              SKILL.md
├── geral-brainstormar-sobre-minha-funcao/SKILL.md
├── geral-frontend-design/            SKILL.md
├── geral-log-sessoes/                SKILL.md
├── geral-sabatina/                   SKILL.md
├── gt-media-buyer-completo/          SKILL.md
├── gt-relatorios-trafego/            SKILL.md
├── image/                            SKILL.md
├── launch-strategy/                  SKILL.md
├── lead-magnets/                     SKILL.md
├── marketing-ideas/                  SKILL.md
├── marketing-psychology/             SKILL.md
├── n8n-architect/                    SKILL.md
├── novo-cliente/                     SKILL.md
├── novo-projeto/                     SKILL.md
├── novo-squad/                       SKILL.md
├── onboarding-cro/                   SKILL.md
├── onboarding/                       SKILL.md
├── opensquad/                        SKILL.md
├── page-cro/                         SKILL.md
├── paid-ads/                         SKILL.md
├── paywall-upgrade-cro/              SKILL.md
├── popup-cro/                        SKILL.md
├── pricing-strategy/                 SKILL.md
├── product-marketing-context/        SKILL.md
├── programmatic-seo/                 SKILL.md
├── referral-program/                 SKILL.md
├── revops/                           SKILL.md
├── sales-enablement/                 SKILL.md
├── schema-markup/                    SKILL.md
├── seo-audit/                        SKILL.md
├── signup-flow-cro/                  SKILL.md
├── site-architecture/                SKILL.md
├── social-content/                   SKILL.md
├── supabase-postgres-best-practices/ SKILL.md
├── supabase/                         SKILL.md
├── sync-hub/                         SKILL.md
├── v4mos-dados-meta-ads/             SKILL.md
└── video/                            SKILL.md
```

> **Total: 65 skills** (espelhadas em `.claude/skills/`)

---

## Apêndice — Script de Resumo para o Coordenador

Use este script na reunião com o coordenador para explicar as 4 tasks em 5 minutos:

---

**"Coordenador, aqui está o plano em 4 movimentos:**

**Task 1 — Validação (essa semana)**
30 minutos com cada área. Mostro o fluxo que o agente vai seguir, valido se está certo, pergunto o que falta. Sai de lá com o SKILL.md ajustado.

**Task 2 — Refinamento (semana que vem)**
Pego o feedback de cada sessão e ajusto os SKILL.md dos agentes. Fica a versão final validada pelo time.

**Task 3 — Agente Account/CSM (semana 3)**
Já está configurado no OpenCode. É o piloto. Account consegue testar: roleplay antes do check-in, review depois, flags automáticas.

**Task 4 — VPS (semana 3-4, paralelo)**
OpenCode Web na VPS. Todo mundo acessa pelo browser. LiteLLM, n8n, MCPs. Fica pronto para uso de todos.

**O que eu preciso de você:**
1. Aprovar as sessões de validação com as áreas
2. Liberar acesso às APIs (Google Ads, Meta, GA4, Ekyte)
3. Acesso SSH à VPS para o scaffold

**Em 2 semanas o primeiro agente está produzindo. Custo zero de IA."**

---

> **Documentos relacionados:**
> - `agents-hub.html` — Site institucional completo
> - `assets/html/apresentacao-agents-hub.html` — Slide-deck para apresentação
> - `docs/agents-hub/LOGICA-APRESENTACAO.md` — Roteiro e objeções
> - `ORCHESTRA.md` — Catálogo completo dos 36 agentes
> - `PLANO_IMPLANTACAO_AGENTES.md` — Plano original de implantação
