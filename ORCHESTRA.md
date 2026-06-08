# Agent Orchestra V4

> **23 subagentes · 65 skills · 7 formacões de time · combinações infinitas**
>
> Um humano + um enxame de IA = o output de uma agência completa.

```
                    ┌─────────────────────────────────────┐
                    │         CMO ORCHESTRATOR            │
                    │         (cmoorch)                   │
                    │    Visão · Direção · ROIs           │
                    └──────────┬──────────────────────────┘
          ┌────────────────────┼────────────────────┐
          ▼                    ▼                    ▼
   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
   │ GROWTH TEAM  │   │ CONTENT      │   │ ACCOUNT      │
   │ (growth-team)│   │ STUDIO       │   │ ORCHESTRATOR │
   │              │   │ (content-    │   │ (account-    │
   │              │   │  studio)     │   │  orchestrator)│
   └──────┬───────┘   └──────┬───────┘   └──────┬───────┘
          │                  │                  │
   ┌──────┴──────┐    ┌─────┴──────┐    ┌──────┴──────┐
   │ Especialistas│    │ Especialis-│    │ Especialis- │
   │ CRO · Mídia │    │ tas Copy   │    │ tas Vendas  │
   │ SEO · Email │    │ · Design   │    │ · CS · Rev  │
   └─────────────┘    └────────────┘    └─────────────┘
```

---

## Índice

1. [A Visão](#1-a-visão)
2. [Arquitetura do Sistema](#2-arquitetura-do-sistema)
3. [Catálogo dos Agentes](#3-catálogo-dos-agentes)
4. [Formações de Times (Party Compositions)](#4-formações-de-times)
5. [Padrões de Orquestração](#5-padrões-de-orquestração)
6. [Cenários Reais](#6-cenários-reais)
7. [Guia Rápido de Uso](#7-guia-rápido-de-uso)

---

## 1. A Visão

Cada skill no Builders Hub é um instrumento. Sozinho, ele faz bonito. Mas quando você junta **20 agentes especializados** numa orquestração consciente, o que emerge é uma capacidade multiplicativa — não aditiva.

**O princípio:** um agente sozinho executa. Dois agentes juntos criam. Três ou mais **orquestram**.

A Agent Orchestra V4 transforma o repositório de skills numa força de trabalho de IA:

| Camada | Função | Exemplos |
|--------|--------|----------|
| **Especialistas** | Execução profunda em 1 domínio | copy-content, midia-paga, seo-visibilidade |
| **Orquestradores** | Coordenação de times multidisciplinares | growth-team, content-studio, account-orchestrator |
| **Comando** | Visão estratégica, direção, ROI | cmoorch, revenue-ops |

---

## 2. Arquitetura do Sistema

### Mapa de Composição

Cada agente é alimentado por skills do hub. A hierarquia é:

```
SKILL (instrumento individual)
  → AGENTE ESPECIALISTA (músico que domina 4-8 instrumentos)
    → AGENTE ORQUESTRADOR (maestro de uma seção)
      → CMO ORCHESTRATOR (regente geral)
```

### Como os agentes se comunicam

- **Output estruturado**: agentes produzem JSON/Markdown padronizado que outros consomem
- **Cadeia de valor**: `pesquisador → copy-content → criacao-design → revisor`
- **Flag system**: agentes de diagnóstico (`flag-*`) alimentam orquestradores
- **Revisor**: gate de qualidade que valida output antes de entrega

---

## 3. Catálogo dos Agentes

### 3.1 Especialistas por Domínio

| # | Agente | Archetype | Skills Fonte | O Que Cria |
|---|--------|-----------|-------------|------------|
| 1 | **estrategia-marketing** | 🧠 Estrategista | `marketing-ideas`, `customer-research`, `content-strategy`, `product-marketing-context`, `competitor-profiling`, `marketing-psychology` | Plano de marketing, pesquisa de mercado, posicionamento, ICP, análise competitiva |
| 2 | **copy-content** | ✍️ Conteúdo | `copywriting`, `copy-editing`, `ad-creative`, `cold-email`, `email-sequence`, `social-content`, `lead-magnets` | Copy de páginas, emails, anúncios, redes sociais, lead magnets |
| 3 | **seo-visibilidade** | 🔍 SEO | `seo-audit`, `ai-seo`, `schema-markup`, `site-architecture`, `programmatic-seo`, `directory-submissions`, `aso-audit` | Auditoria SEO, estratégia de AI Visibility, schema, arquitetura de site |
| 4 | **cro-otimizacao** | 🧪 Experimentação | `page-cro`, `signup-flow-cro`, `onboarding-cro`, `form-cro`, `popup-cro`, `paywall-upgrade-cro`, `ab-test-setup` | Testes A/B, hipóteses CRO, otimização de funis, experimentos |
| 5 | **midia-paga** | 📊 Mídia | `paid-ads`, `gt-media-buyer-completo`, `ad-creative`, `v4mos-dados-meta-ads` | Planos de mídia, alocação de budget, análise de campanhas, relatórios Meta |
| 6 | **receita-crescimento** | 📈 Crescimento | `pricing-strategy`, `churn-prevention`, `referral-program`, `revops`, `email-sequence` | Estratégia de preços, plano de retenção, programa de referrals, funil de receita |
| 7 | **vendas-account** | 🤝 Vendas | `sales-enablement`, `cold-email`, `account-handoff`, `account-pesquisa-profunda-cliente` | Deck de vendas, scripts de demo, material de handoff, pesquisa de cliente |
| 8 | **criacao-design** | 🎨 Design | `geral-frontend-design`, `image`, `video`, `gt-apresentacao-visual-modelo1` | Interfaces HTML, imagens, vídeos, apresentações, assets visuais |
| 9 | **automacao-analytics** | ⚙️ Automação | `n8n-architect`, `analytics-tracking`, `v4mos-dados-meta-ads` | Workflows n8n, tracking plan, dashboards, automações |
| 10 | **estrategia-lideranca** | 🏛️ Liderança | `geral-sabatina`, `geral-brainstormar-sobre-minha-funcao`, `co-marketing`, `launch-strategy`, `free-tool-strategy`, `community-marketing` | Plano estratégico, parcerias, launch plan, free tool strategy |
| 11 | **relatorios-trafego** | 📊 Reports | `gt-relatorios-trafego`, `gt-media-buyer-completo`, `v4mos-dados-meta-ads`, `analytics-tracking`, `paid-ads` | Relatório consolidado multicanal, detecção de anomalias, pace de verba, análise IA |
| 12 | **pipeline-conteudo** | 🏭 Conteúdo | `copy-pipeline-conteudo`, `copywriting`, `email-sequence`, `content-strategy`, `social-content` | Calendário editorial, blog posts, email marketing, fluxo de aprovação, JSONs no Drive |

### 3.2 Orquestradores (Times)

| # | Agente | Archetype | Skills Fonte | O Que Cria |
|---|--------|-----------|-------------|------------|
| 13 | **cmoorch** | 👑 CMO | *Todas as skills de marketing* | Estratégia integrada de marketing, alocação de recursos, OKRs de marketing |
| 14 | **growth-team** | 🚀 Growth | `analista-dados`, `cro-otimizacao`, `midia-paga`, `seo-visibilidade`, `copy-content`, `receita-crescimento` | Plano de growth integrado, experimentos cross-canal, relatório de tração |
| 15 | **content-studio** | 🏭 Conteúdo | `estrategia-marketing`, `copy-content`, `seo-visibilidade`, `criacao-design`, `pesquisador`, `pipeline-conteudo` | Calendário editorial, pacote de conteúdo, SEO content, assets multimídia |
| 16 | **revenue-ops** | 💰 Revenue | `receita-crescimento`, `automacao-analytics`, `vendas-account`, `analista-dados` | Funil de receita, automação RevOps, forecasting, plano de expansão |
| 17 | **account-orchestrator** | 🤗 CS | `account-checkin-roleplay`, `account-checkin-review`, `account-handoff`, `vendas-account`, `flag-*`, `csm-orquestrador`, `evolucao-checkins` | Mission Control, plano de conta, QBR, diagnóstico de saúde |
| 18 | **launch-pad** | 🚀 Launch | `launch-strategy`, `copy-content`, `midia-paga`, `seo-visibilidade`, `directory-submissions`, `criacao-design` | Plano de lançamento, landing page, campanha, PR, diretórios |

### 3.3 Agentes de Nicho

| # | Agente | Archetype | Skills Fonte | O Que Cria |
|---|--------|-----------|-------------|------------|
| 19 | **cro-lab** | 🔬 CRO | `ab-test-setup`, `page-cro`, `signup-flow-cro`, `onboarding-cro`, `form-cro`, `popup-cro`, `paywall-upgrade-cro`, `analytics-tracking` | Pipeline de experimentos, roadmap CRO, relatório de significância |
| 20 | **pesquisador** | 🔎 Pesquisador | `customer-research`, `competitor-profiling`, `geral-sabatina`, `account-pesquisa-profunda-cliente`, `competitor-alternatives` | Dossiê de concorrente, pesquisa de consumidor, personas, análise de mercado |
| 21 | **media-buyer** | 🎯 Media Buyer | `gt-media-buyer-completo`, `paid-ads`, `v4mos-dados-meta-ads`, `ad-creative`, `analista-dados` | Arquitetura de contas, plano de mídia, análise preditiva, otimização ROAS |
| 22 | **n8n-automator** | 🤖 Automator | `n8n-architect`, `analytics-tracking`, `automacao-analytics` | Workflows n8n, integrações, automações de dados, ETL |
| 23 | **evolucao-checkins** | 📈 CS Analytics | `account-evolucao-checkins`, `account-checkin-review`, `account-checkin-roleplay`, `contexto` | Relatório de progressão, score de saúde, taxa de cumprimento, ciclo das apostas |

---

## 4. Formações de Times

Combine agentes como party compositions num RPG. Cada formação tem um propósito específico.

### ⚡ Growth Strike Team
**Missão:** Acelerar aquisição e conversão em 30-60 dias

```
growth-team (líder)
  ├── cro-lab        → pipeline de experimentos
  ├── midia-paga     → campanhas pagas
  ├── seo-visibilidade → SEO + AI Visibility
  └── copy-content   → criativos e landing pages
```

**Output:** Plano de growth integrado, experimentos rodando, relatório semanal de tração

### 🏭 Content Factory
**Missão:** Produzir conteúdo em escala com qualidade consistente

```
content-studio (líder)
  ├── estrategia-marketing → pesquisa e briefing
  ├── copy-content         → produção de texto
  ├── criacao-design       → assets visuais
  ├── seo-visibilidade     → otimização SEO
  └── revisor              → quality gate
```

**Output:** Calendário editorial mensal, pacote completo de conteúdo, relatório de performance

### 🤗 Client Success Pod
**Missão:** Saúde do cliente, expansão e retenção

```
account-orchestrator (líder)
  ├── revenue-ops          → pricing e expansão
  ├── pesquisador          → pesquisa de mercado do cliente
  ├── vendas-account       → material de vendas
  ├── flag-churn           → diagnóstico de churn
  └── flag-okr             → diagnóstico de OKR
```

**Output:** QBR completo, plano de expansão, diagnóstico de saúde, action plan

### 🚀 Product Launch Squad
**Missão:** Lançar produto com impacto máximo

```
launch-pad (líder)
  ├── estrategia-marketing → positioning e messaging
  ├── copy-content         → copy do launch
  ├── midia-paga           → campanha de aquisição
  ├── criacao-design       → landing page e assets
  ├── seo-visibilidade     → SEO pré-launch
  └── directory-submissions → diretórios
```

**Output:** Launch plan completo, landing page, campanha multicanal, PR kit

### 🏢 Full Agency
**Missão:** Operar como agência completa para um cliente

```
cmoorch (regente)
  ├── growth-team
  ├── content-studio
  ├── account-orchestrator
  └── revenue-ops
```

**Output:** Estratégia integrada, execução cross-funil, reporting executivo

### 🧪 CRO Lab
**Missão:** Máquina de experimentos contínua

```
cro-lab (líder)
  ├── estrategia-marketing → hipóteses baseadas em pesquisa
  ├── copy-content         → variações de copy
  ├── criacao-design       → variações de UI
  └── automacao-analytics  → tracking e dados
```

**Output:** Pipeline de experimentos, resultados com significância estatística, learning log

### 📊 Traffic Reporting Squad
**Missão:** Relatórios consolidados de tráfego multicanal com análise e recomendações

```
relatorios-trafego (líder)
  ├── analista-dados       → análise de performance e anomalias
  ├── midia-paga           → contexto estratégico das campanhas
  └── media-buyer          → recomendações de otimização
```

**Output:** Relatório consolidado HTML/JSON, detecção de anomalias, pace de verba, análise IA

### 🏭 Content Pipeline Full
**Missão:** Pipeline completo de conteúdo editorial: calendário → produção → aprovação → Drive

```
pipeline-conteudo (líder)
  ├── estrategia-marketing → pesquisa e tópicos
  ├── copy-content         → produção de texto
  ├── criacao-design       → assets visuais
  ├── seo-visibilidade     → otimização SEO
  └── revisor              → quality gate
```

**Output:** Calendário editorial, blog posts, email marketing, JSONs no Google Drive

### 🎯 Media Buying Command
**Missão:** Máquina de mídia paga data-driven

```
media-buyer (comandante)
  ├── analista-dados       → análise de performance
  ├── copy-content         → ad creatives
  ├── criacao-design       → banners e vídeos
  └── automacao-analytics  → tracking e automação
```

**Output:** Arquitetura de contas, análise preditiva, plano de otimização, report

### 📊 Executive Board
**Missão:** Decisões estratégicas de alto nível

```
cmoorch (CEO)
  ├── estrategia-lideranca → sabatina de planos
  ├── revenue-ops          → números e forecasting
  ├── account-orchestrator → saúde dos clientes
  └── analista-dados       → dados consolidados
```

**Output:** Board deck, OKRs revisados, alocação de recursos, decisões

---

## 5. Padrões de Orquestração

### Cadeia Linear (Pipeline)
```
pesquisador → copy-content → criacao-design → revisor → entrega
```
Quando a saída de um alimenta o próximo.

### Estrela (Hub & Spoke)
```
        ┌── cro-lab
        ├── midia-paga
cmoorch ── seo-visibilidade
        ├── copy-content
        └── content-studio
```
Um orquestrador coordena múltiplos especialistas em paralelo.

### Malha (Mesh)
```
content-studio ←→ copy-content ←→ criacao-design
      ↕              ↕                ↕
seo-visibilidade ←→ pesquisador ←→ estrategia-marketing
```
Múltiplos agentes colaboram e iteram — ideal para projetos complexos.

### Flag-Triggered
```
flag-churn → account-orchestrator → revenue-ops → copy-content
```
Um gatilho (flag) inicia uma cascata de agentes.

### Ciclo PDCA
```
analista-dados (check)
      ↑
      │    ┌─ estrategia-marketing (plan)
      │    ↓
cro-lab (act) ← copy-content + criacao-design (do)
```
Loop contínuo de melhoria.

---

## 6. Cenários Reais

### Cenário 1: "Cliente com churn iminente"

**Gatilho:** NPS caiu de 75 para 40, CSAT caiu de 4.5 para 3.0.

**Sequência automática:**
1. `flag-churn` → diagnóstico: 🔴 Churn por Percepção
2. `account-orchestrator` → consolida dados e aciona time
3. `pesquisador` → pesquisa o setor do cliente, encontra 3 tendências que justificam reposicionamento
4. `estrategia-marketing` → elabora novo posicionamento e plano de valor
5. `content-studio` → produz apresentação de QBR emergencial com estudos de caso
6. `vendas-account` → prepara script de renovação com upsell
7. `revisor` → valida o pacote
8. **Humano entrega** → renovação fechada com +30% de escopo

### Cenário 2: "Lançar novo produto em 2 semanas"

**Gatilho:** Briefing do produto recebido.

**Sequência:**
1. `estrategia-marketing` → pesquisa concorrência, define positioning
2. `launch-pad` → estrutura plano de lançamento multicanal
3. `copy-content` → escreve landing page, emails de launch, social posts
4. `criacao-design` → produz landing page HTML, banners, OG images
5. `midia-paga` → estrutura campanhas de aquisição
6. `seo-visibilidade` → prepara SEO pré-launch e AI Visibility
7. `directory-submissions` → submete em 50+ diretórios
8. `revisor` → quality gate final
9. **Humanos aprovam e publicam** → 200+ leads no dia 1

### Cenário 3: "Otimizar funil completo de crescimento"

**Gatilho:** "Quero crescer 40% nos próximos 3 meses."

**Sequência:**
1. `analista-dados` → diagnostica estado atual do funil
2. `growth-team` → define hipóteses e priorização (ICE score)
3. Em paralelo:
   - `cro-lab` → 5 experimentos no funil de conversão
   - `midia-paga` → reestrutura campanhas com base em dados históricos
   - `seo-visibilidade` → auditoria técnica + plano de conteúdo SEO
   - `copy-content` → novas variações de copy para páginas-chave
   - `receita-crescimento` → revisa pricing, cria programa de referral
4. `content-studio` → produz conteúdo para atrair topo de funil
5. `automacao-analytics` → configura tracking para medir tudo
6. `analista-dados` → relatório semanal de tração vs meta
7. **Humanos revisam e ajustam** → 40% de crescimento em 90 dias

---

## 7. Guia Rápido de Uso

### Invocando Agentes

Use `@nome-do-agente` seguido da missão:

```
@estrategia-marketing Quero posicionar um SaaS de IA para PMEs. Pesquise o mercado, analise 3 concorrentes e sugira posicionamento.
```

```
@growth-team Quero crescer 30% em 60 dias. Diagnostique o funil e monte um plano integrado.
```

```
@pesquisador Analise o perfil de consumidor de [cliente] e gere personas detalhadas.
```

### Formando Times

```
@cmoorch Monte um plano integrado para o cliente X. Use @growth-team para aquisição, @content-studio para conteúdo e @account-orchestrator para retenção.
```

### Algule um Especialista num Orquestrador

```
@growth-team Preciso de 5 experimentos CRO. Chame o @cro-lab para desenhar e priorizar.
```

### Peça Revisão

```
@revisor Revise o plano que o @growth-team acabou de gerar.
```

---

## Mapa Visual Rápido

```
                     👑 cmoorch
                   /     |      \
                  /      |       \
          🚀 growth    🏭 content  🤗 account
          -team        -studio     -orchestrator
         /  |  \      / | \        /  |  \
        🧠  🧪 📊  ✍️ 🎨 🔍   🤝 💰 🔎
        |   |   |   |   |   |    |   |   |
       10 especialistas + 4 nicho + revisor + analista
```

**Total: 23 subagentes × 65 skills = capacidade de agência completa em texto.**

---

*"Sozinho você é uma skill. Em orquestra, você é uma agência."*
