# Guia de Infraestrutura dos Agentes V4

> Mapeamento completo dos 35 subagentes da Agent Orchestra V4:
> o que cada um faz, quais skills utiliza, e o que é necessário de infraestrutura/credenciais para funcionarem.

**Gerado em:** 31/05/2026
**Total de agentes:** 35
**Modelo padrão:** `opencode/deepseek-v4-flash-free` (32 agentes)
**Modelo alternativo:** `google/gemini-2.5-flash` (3 agentes: `gerar-doc`, `gerar-html`, `gerar-ppt`, `gerar-pdf`)
**Modelo alternativo 2:** `openrouter/openai/gpt-oss-120b:free` (1 agente: `csm-orquestrador`)

---

## Sumário

- [Legenda](#legenda)
- [Categoria 1: Especialistas de Domínio (12)](#categoria-1-especialistas-de-domínio)
- [Categoria 2: Orquestradores (6)](#categoria-2-orquestradores)
- [Categoria 3: Agentes de Nicho (5)](#categoria-3-agentes-de-nicho)
- [Categoria 4: Agentes de Diagnóstico / Flags (4)](#categoria-4-agentes-de-diagnóstico--flags)
- [Categoria 5: Agentes de Suporte (4)](#categoria-5-agentes-de-suporte)
- [Categoria 6: Agentes Geradores (4)](#categoria-6-agentes-geradores)
- [Tabela Consolidada de Infraestrutura](#tabela-consolidada-de-infraestrutura)
- [Checklist de Setup](#checklist-de-setup)

---

## Legenda

| Ícone | Significado |
|-------|-------------|
| 🔴 | Crítico — sem isso o agente não funciona |
| 🟡 | Importante — funcionalidade central |
| 🟢 | Opcional / nice-to-have |
| ⚪ | Nenhuma dependência externa |

### Dependências comuns entre agentes

- **🔴 OpenCode Runtime**: Todos os agentes dependem do OpenCode (ou Claude Code / Anti-Gravity) para serem executados
- **🔴 Acesso a skills locais**: Skills referenciadas precisam existir em `.agents/skills/` ou `.claude/skills/`
- **🟢 webfetch/websearch**: Navegador web funcional para o runtime (requerido por agentes que pesquisam online)
- **🟢 bash**: Permissão para executar comandos no terminal (requerido por agentes que geram HTML/PDF ou executam scripts)

---

## Categoria 1: Especialistas de Domínio

### 1. @estrategia-marketing — Estrategista de Marketing

**O que faz:** Pesquisa mercado, analisa concorrência, define posicionamento e estratégia de conteúdo.
**Output:** JSON estruturado com market_context, target_audience, positioning, strategy.

#### Skills que utiliza
| Skill | Dependência de Infra |
|-------|----------------------|
| `customer-research` | 🟢 webfetch/websearch — para minerar reviews, Reddit, fóruns |
| `competitor-profiling` | 🟢 webfetch — para acessar URLs de concorrentes |
| `competitor-alternatives` | ⚪ Nenhuma — geração de conteúdo comparativo |
| `content-strategy` | ⚪ Nenhuma — planejamento estratégico |
| `product-marketing-context` | ⚪ Nenhuma — definição de posicionamento |
| `marketing-ideas` | ⚪ Nenhuma — brainstorming |
| `marketing-psychology` | ⚪ Nenhuma — aplicação de princípios |

**Infraestrutura necessária:**
- ⚪ Nenhuma API externa obrigatória
- 🟢 webfetch/websearch para pesquisa de concorrentes (modo produção)

---

### 2. @copy-content — Copywriter e Produtor de Conteúdo

**O que faz:** Escreve landing pages, emails, anúncios, redes sociais e lead magnets.
**Output:** Headlines, corpo de copy, CTAs organizados por canal.

#### Skills que utiliza
| Skill | Dependência de Infra |
|-------|----------------------|
| `copywriting` | ⚪ Nenhuma |
| `copy-editing` | ⚪ Nenhuma |
| `ad-creative` | ⚪ Nenhuma |
| `cold-email` | ⚪ Nenhuma |
| `email-sequence` | ⚪ Nenhuma |
| `social-content` | ⚪ Nenhuma |
| `lead-magnets` | ⚪ Nenhuma |

**Infraestrutura necessária:**
- ⚪ Nenhuma API externa. Funciona 100% em modo simulado.

---

### 3. @seo-visibilidade — SEO & AI Visibility

**O que faz:** Audita tecnicamente sites, otimiza para SEO tradicional e AI Visibility (GEO/LLMO).
**Output:** Relatório JSON com auditoria técnica, AI visibility, schema markup, arquitetura.

#### Skills que utiliza
| Skill | Dependência de Infra |
|-------|----------------------|
| `seo-audit` | 🟢 webfetch — para acessar URLs auditadas |
| `ai-seo` | 🟢 webfetch/websearch — para verificar citações em IAs |
| `schema-markup` | ⚪ Nenhuma — geração de JSON-LD |
| `site-architecture` | ⚪ Nenhuma — análise de hierarquia |
| `programmatic-seo` | ⚪ Nenhuma — planejamento de páginas em escala |
| `directory-submissions` | 🟡 Requer lista de diretórios atualizada |
| `aso-audit` | 🟢 webfetch — para acessar App Store / Play Store |

**Infraestrutura necessária:**
- 🟢 webfetch para auditar URLs reais
- ⚪ Nenhuma API key obrigatória (pode operar com dados simulados)

---

### 4. @cro-otimizacao — CRO & Experimentação

**O que faz:** Otimiza conversão em páginas, signups, formulários e onboarding. Projeta experimentos A/B.

#### Skills que utiliza
| Skill | Dependência de Infra |
|-------|----------------------|
| `page-cro` | ⚪ Nenhuma |
| `signup-flow-cro` | ⚪ Nenhuma |
| `onboarding-cro` | ⚪ Nenhuma |
| `form-cro` | ⚪ Nenhuma |
| `popup-cro` | ⚪ Nenhuma |
| `paywall-upgrade-cro` | ⚪ Nenhuma |
| `ab-test-setup` | ⚪ Nenhuma |

**Infraestrutura necessária:**
- ⚪ Nenhuma API externa. Depende de dados do cliente (analytics, heatmaps) para diagnósticos reais.

---

### 5. @midia-paga — Estrategista de Mídia Paga

**O que faz:** Planeja, estrutura e otimiza campanhas em Meta, Google, LinkedIn e TikTok.

#### Skills que utiliza
| Skill | Dependência de Infra |
|-------|----------------------|
| `paid-ads` | ⚪ Nenhuma — planejamento estratégico |
| `gt-media-buyer-completo` | ⚪ Nenhuma — metodologia |
| `ad-creative` | ⚪ Nenhuma — geração de criativos |
| `v4mos-dados-meta-ads` | 🔴 **Requer V4mos API key** — para dados reais de Meta Ads |

**Infraestrutura necessária:**
- 🔴 **API V4mos** (para dados reais de Meta Ads): credencial em `clientes/<cliente>/.env`
- ⚪ Opera bem em modo simulado sem API

---

### 6. @receita-crescimento — Revenue & Growth

**O que faz:** Pricing, retenção, referrals, operações de receita.

#### Skills que utiliza
| Skill | Dependência de Infra |
|-------|----------------------|
| `pricing-strategy` | ⚪ Nenhuma |
| `churn-prevention` | ⚪ Nenhuma |
| `referral-program` | ⚪ Nenhuma |
| `revops` | ⚪ Nenhuma |
| `email-sequence` | ⚪ Nenhuma |

**Infraestrutura necessária:**
- ⚪ Nenhuma API externa. Funciona 100% em modo simulado.

---

### 7. @vendas-account — Sales & Account

**O que faz:** Cria collaterais de vendas, scripts de demo, handoff e pesquisa de cliente.

#### Skills que utiliza
| Skill | Dependência de Infra |
|-------|----------------------|
| `sales-enablement` | ⚪ Nenhuma |
| `cold-email` | ⚪ Nenhuma |
| `account-handoff` | ⚪ Nenhuma |
| `account-pesquisa-profunda-cliente` | 🔴 **Requer Gemini Deep Research** (via Google AI Studio ou API) |

**Infraestrutura necessária:**
- 🔴 **Gemini Deep Research API** (para pesquisa profunda de cliente) — opcional se usar modo simulado
- ⚪ Opera bem em modo simulado sem API

---

### 8. @criacao-design — Diretor de Criação & Design

**O que faz:** Produz interfaces HTML, imagens, vídeos e apresentações de alto nível.

#### Skills que utiliza
| Skill | Dependência de Infra |
|-------|----------------------|
| `geral-frontend-design` | ⚪ Nenhuma — geração HTML/CSS/JS |
| `image` | 🟡 **Requer API de geração de imagem** (Flux, Midjourney, DALL-E, Imagen) |
| `video` | 🟡 **Requer API de geração de vídeo** (Runway, HeyGen, Veo, Remotion) |

**Infraestrutura necessária:**
- 🟡 API de geração de imagens (para criar assets visuais)
- 🟡 API de geração de vídeo (para criar vídeos)
- ⚪ HTML/CSS/JS funciona sem dependências externas

---

### 9. @automacao-analytics — Automação & Analytics

**O que faz:** Setup de tracking, workflows n8n e pipelines de dados.

#### Skills que utiliza
| Skill | Dependência de Infra |
|-------|----------------------|
| `n8n-architect` | 🔴 **Requer n8n instance + n8n-as-code configurado** |
| `analytics-tracking` | 🟡 **Requer GA4 / GTM credentials** |
| `v4mos-dados-meta-ads` | 🟡 **Requer V4mos API key** |

**Infraestrutura necessária:**
| Recurso | Tipo | Onde configurar |
|---------|------|-----------------|
| 🔴 n8n instance (self-hosted ou n8n.cloud) | Serviço | `n8nac-config.json` |
| 🔴 n8n-as-code (`npx --yes n8nac`) | CLI | Projeto raiz |
| 🟡 Google Analytics 4 (GA4) credentials | API | `clientes/<cliente>/.env` |
| 🟡 Google Tag Manager (GTM) access | Web | Accounts GTM do cliente |
| 🟡 V4mos API key | API | `clientes/<cliente>/.env` |

---

### 10. @estrategia-lideranca — Strategy & Leadership

**O que faz:** Stress-test de planos (sabatina), brainstorm de função, parcerias, launch.

#### Skills que utiliza
| Skill | Dependência de Infra |
|-------|----------------------|
| `geral-sabatina` | ⚪ Nenhuma |
| `geral-brainstormar-sobre-minha-funcao` | ⚪ Nenhuma |
| `co-marketing` | 🟢 webfetch — para pesquisar parceiros |
| `launch-strategy` | ⚪ Nenhuma |
| `free-tool-strategy` | ⚪ Nenhuma |
| `community-marketing` | ⚪ Nenhuma |

**Infraestrutura necessária:**
- ⚪ Nenhuma API externa obrigatória

---

### 11. @relatorios-trafego — Traffic Reporting

**O que faz:** Relatórios consolidados multicanal (Google Ads, Meta Ads, Bing Ads) com detecção de anomalias.

#### Skills que utiliza
| Skill | Dependência de Infra |
|-------|----------------------|
| `gt-relatorios-trafego` | 🔴 Requer dados das plataformas de anúncio |
| `gt-media-buyer-completo` | ⚪ Nenhuma — metodologia |
| `v4mos-dados-meta-ads` | 🔴 **Requer V4mos API key** |
| `analytics-tracking` | 🟡 Requer GA4 access |
| `paid-ads` | 🟡 Requer Google Ads / Meta Ads access |

**Infraestrutura necessária:**
| Recurso | Tipo | Onde configurar |
|---------|------|-----------------|
| 🔴 V4mos API key | API | `clientes/<cliente>/.env` |
| 🟡 Google Ads API / Script | API | `clientes/<cliente>/.env` |
| 🟡 Bing Ads API | API | `clientes/<cliente>/.env` |
| 🟡 GA4 credentials | API | `clientes/<cliente>/.env` |

---

### 12. @pipeline-conteudo — Content Pipeline Producer

**O que faz:** Pipeline editorial completo: calendário → produção → aprovação → Drive.

#### Skills que utiliza
| Skill | Dependência de Infra |
|-------|----------------------|
| `copy-pipeline-conteudo` | ⚪ Nenhuma (geração via IA) |
| `copywriting` | ⚪ Nenhuma |
| `email-sequence` | ⚪ Nenhuma |
| `content-strategy` | ⚪ Nenhuma |
| `social-content` | ⚪ Nenhuma |

**Subagentes que comanda:** `@estrategia-marketing`, `@copy-content`, `@criacao-design`, `@revisor`

**Infraestrutura necessária:**
- 🟡 **Google Drive API** (para salvar/ler JSONs de conteúdo via pipeline real)
- 🟡 **Email service** (para notificações de aprovação — SendGrid, SES, etc.)
- ⚪ Opera bem em modo simulado sem APIs

---

## Categoria 2: Orquestradores

### 13. @cmoorch — CMO Orchestrator

**O que faz:** Orquestra a estratégia de marketing completa. Integra todos os times e especialistas.
**Modelo:** `opencode/deepseek-v4-flash-free`, temperature 0.2

**Subagentes que comanda:**
`@estrategia-marketing`, `@growth-team`, `@content-studio`, `@revenue-ops`, `@launch-pad`, `@analista-dados`, `@flag-*`, `@revisor`

**Infraestrutura necessária:**
- 🔴 **Permissão `task: *`** (já configurada no agente)
- 🔴 Depende de todos os subagentes que comanda — a infra deles é a infra dele
- ⚪ Nenhuma API externa direta

---

### 14. @growth-team — Growth Team Lead

**O que faz:** Orquestra crescimento integrando CRO, mídia paga, SEO, conteúdo e receita.

**Subagentes que comanda:**
`@analista-dados`, `@cro-otimizacao`, `@midia-paga`, `@seo-visibilidade`, `@copy-content`, `@receita-crescimento`

**Infraestrutura necessária:**
- 🔴 Permissão `task: *` (já configurada)
- 🔴 Depende da infra dos subagentes que comanda

---

### 15. @content-studio — Content Studio Producer

**O que faz:** Produção de conteúdo em escala integrando pesquisa, copy, design e SEO.

**Subagentes que comanda:**
`@estrategia-marketing`, `@copy-content`, `@seo-visibilidade`, `@criacao-design`, `@pesquisador`, `@revisor`

**Infraestrutura necessária:**
- 🔴 Permissão `task: *` (já configurada)
- 🔴 Depende da infra dos subagentes que comanda

---

### 16. @revenue-ops — Revenue Operations Lead

**O que faz:** Orquestra a engrenagem de receita: pricing, churn, referral, automação.

**Subagentes que comanda:**
`@receita-crescimento`, `@automacao-analytics`, `@vendas-account`, `@analista-dados`, `@flag-churn`, `@flag-roi`

**Infraestrutura necessária:**
- 🔴 Permissão `task: *` (já configurada)
- 🔴 Depende da infra dos subagentes que comanda
- 🔴 Especialmente dependente de `@automacao-analytics` (n8n + tracking)

---

### 17. @account-orchestrator — Account Orchestrator

**O que faz:** Orquestra a saúde do cliente: check-ins, mission control, flags, expansão.

**Subagentes que comanda:**
`@vendas-account`, `@flag-churn`, `@flag-okr`, `@flag-operacao`, `@csm-orquestrador`, `@pesquisador`, `@analista-dados`, `@revisor`
**Skills de account:** `account-checkin-roleplay`, `account-checkin-review`, `account-handoff`, `contexto`

**Infraestrutura necessária:**
| Recurso | Tipo | Observação |
|---------|------|------------|
| 🔴 Dados de cliente em `squads/{squad}/clientes/{cliente}/` | Filesystem | Mission Control, calls, checkins |
| 🔴 `contexto` skill | Skill | Para ler KB e gerar Mission Control |
| 🟡 NPS / CSAT data | Dado | Para flag-churn funcionar |
| 🟡 OKR data | Dado | Para flag-okr funcionar |

---

### 18. @launch-pad — Launch Pad

**O que faz:** Orquestra lançamentos de produtos: estratégia, conteúdo, mídia, SEO, diretórios.

**Subagentes que comanda:**
`@estrategia-marketing`, `@copy-content`, `@midia-paga`, `@seo-visibilidade`, `@criacao-design`, `@revisor`
**Skill:** `directory-submissions`

**Infraestrutura necessária:**
- 🔴 Permissão `task: *` (já configurada)
- 🔴 Depende da infra dos subagentes que comanda
- 🟡 Lista de diretórios atualizada (para `directory-submissions`)

---

## Categoria 3: Agentes de Nicho

### 19. @cro-lab — CRO Lab Lead

**O que faz:** Pipeline de experimentos contínuo com hipóteses, design, execução e aprendizado.

#### Skills que utiliza
| Skill | Dependência de Infra |
|-------|----------------------|
| `ab-test-setup` | 🟡 Requer dados de analytics para amostra |
| `page-cro` | ⚪ Nenhuma |
| `signup-flow-cro` | ⚪ Nenhuma |
| `onboarding-cro` | ⚪ Nenhuma |
| `form-cro` | ⚪ Nenhuma |
| `popup-cro` | ⚪ Nenhuma |
| `paywall-upgrade-cro` | ⚪ Nenhuma |
| `analytics-tracking` | 🟡 Requer GA4 / GTM |

**Infraestrutura necessária:**
- 🟡 Dados de analytics (para calcular sample size e validar experimentos)
- ⚪ Opera bem em modo simulado

---

### 20. @pesquisador — Deep Researcher

**O que faz:** Minera dados públicos, reviews, concorrentes e consumidores para insights acionáveis.

#### Skills que utiliza
| Skill | Dependência de Infra |
|-------|----------------------|
| `customer-research` | 🟢 webfetch/websearch — para G2, Reddit, fóruns |
| `competitor-profiling` | 🟢 webfetch — para acessar URLs |
| `competitor-alternatives` | ⚪ Nenhuma |
| `geral-sabatina` | ⚪ Nenhuma |
| `account-pesquisa-profunda-cliente` | 🟡 Requer Gemini Deep Research API |

**Infraestrutura necessária:**
- 🟢 webfetch/websearch (funciona sem, mas limitado)
- 🟡 Gemini Deep Research API (para pesquisa profunda de cliente)

---

### 21. @media-buyer — Senior Media Buyer

**O que faz:** Arquitetura de contas, análise preditiva, otimização ROAS/CPA com TOC.

#### Skills que utiliza
| Skill | Dependência de Infra |
|-------|----------------------|
| `gt-media-buyer-completo` | ⚪ Nenhuma — metodologia |
| `paid-ads` | ⚪ Nenhuma — planejamento |
| `v4mos-dados-meta-ads` | 🔴 **Requer V4mos API key** |
| `ad-creative` | ⚪ Nenhuma |
| `analista-dados` | 🟡 Requer dados de performance |

**Infraestrutura necessária:**
| Recurso | Tipo |
|---------|------|
| 🔴 V4mos API key (para dados reais de Meta Ads) | API |
| 🟡 Google Ads / Meta Ads data export | Dado |

---

### 22. @n8n-automator — n8n Architect

**O que faz:** Cria, edita, valida e sincroniza workflows n8n.

#### Skills que utiliza
| Skill | Dependência de Infra |
|-------|----------------------|
| `n8n-architect` | 🔴 **Requer n8n instance + n8n-as-code** |
| `analytics-tracking` | 🟡 Requer GA4 / GTM |
| `automacao-analytics` | 🔴 Requer n8n + APIs configuradas |

**Infraestrutura necessária:**
| Recurso | Tipo | Configuração |
|---------|------|-------------|
| 🔴 n8n instance (self-hosted ou cloud) | Serviço | URL + API key |
| 🔴 `npx --yes n8nac` instalado | CLI | Projeto raiz |
| 🔴 `npx --yes @n8n-as-code/n8n-manager` | CLI | Projeto raiz |
| 🔴 `n8nac-config.json` configurado | Arquivo | Raiz do projeto |
| 🟡 Google Sheets API | API | Para workflows com sheets |
| 🟡 Slack webhook | Webhook | Para notificações |
| 🟡 Email SMTP | Serviço | Para envio de relatórios |

---

### 23. @evolucao-checkins — Check-in Evolution Analyst

**O que faz:** Lê histórico do Mission Control e gera relatório de progressão: combinados, apostas, personas.

#### Skills que utiliza
| Skill | Dependência de Infra |
|-------|----------------------|
| `account-evolucao-checkins` | 🔴 Requer Mission Control do cliente |
| `account-checkin-review` | 🔴 Requer check-ins registrados |
| `account-checkin-roleplay` | 🟢 Contexto de personas |
| `contexto` | 🔴 Requer KB do cliente |

**Infraestrutura necessária:**
| Recurso | Tipo | Onde |
|---------|------|------|
| 🔴 Mission Control do cliente | Filesystem | `squads/{squad}/clientes/{cliente}/mission-control/` |
| 🔴 Histórico de check-ins | Filesystem | `squads/{squad}/clientes/{cliente}/checkins/` |
| 🔴 `contexto` skill executada | Skill | Deve ter sido rodada uma vez |

---

## Categoria 4: Agentes de Diagnóstico / Flags

### 24. @flag-churn — Churn Flag

**O que faz:** Diagnostica risco de churn quando NPS + CSAT caem juntos.

**Modelo:** `opencode/deepseek-v4-flash-free`, temperature 0.1
**Permissões restritas:** `edit: deny`, `webfetch: deny` — apenas leitura e diagnóstico.

**Infraestrutura necessária:**
| Recurso | Tipo | Observação |
|---------|------|------------|
| 🔴 NPS data (últimos 3 meses) | Dado | Lido de arquivo ou informado |
| 🔴 CSAT data (últimos 2 meses) | Dado | Lido de arquivo ou informado |
| 🟡 ROAS / CPA / OKR data | Dado | Para diagnóstico diferencial |
| ⚪ Nenhuma API externa | — | — |

---

### 25. @flag-okr — OKR Flag

**O que faz:** Diagnostica desvio de OKR quando KR < 60% do esperado.

**Permissões restritas:** `edit: deny`, `webfetch: deny`

**Infraestrutura necessária:**
- 🔴 OKR data (KRs, targets, progress %, time elapsed)
- ⚪ Nenhuma API externa

---

### 26. @flag-roi — ROI Flag

**O que faz:** Diagnostica ROAS abaixo da meta por 2+ semanas consecutivas, classifica tipo (CUSTO/CONVERSAO/VALOR).

**Permissões restritas:** `edit: deny`, `webfetch: deny`

**Infraestrutura necessária:**
| Recurso | Tipo | Observação |
|---------|------|------------|
| 🔴 ROAS trend (4+ semanas) | Dado | Por plataforma |
| 🔴 CPM, CPC, CTR, CVR, AOV | Dado | Métricas secundárias |
| ⚪ Nenhuma API externa | — | — |

---

### 27. @flag-operacao — Operations Flag

**O que faz:** Alerta de operação travada — sprint atrasada sem FCA ou timesheet zerado.

**Permissões restritas:** `edit: deny`, `webfetch: deny`

**Infraestrutura necessária:**
| Recurso | Tipo | Observação |
|---------|------|------------|
| 🔴 Sprint status | Dado | De Ekyte ou task list |
| 🔴 Timesheet data | Dado | De sistema de timesheet |
| 🔴 FCA registry | Dado | De sistema de FCA |
| ⚪ Nenhuma API externa | — | — |

---

## Categoria 5: Agentes de Suporte

### 28. @revisor — Quality Gate (Revisor)

**O que faz:** Valida outputs de outros agentes, confere números e formata saída.

**Permissões:** `edit: deny`, `bash: deny` — apenas revisão, sem alteração.

**Infraestrutura necessária:**
- ⚪ Nenhuma dependência externa
- Precisa receber o output de outro agente para revisar

---

### 29. @analista-dados — Data Analyst

**O que faz:** Analisa dados de performance, OKRs, métricas e gera insights estruturados.

**Infraestrutura necessária:**
| Recurso | Tipo | Observação |
|---------|------|------------|
| 🟡 Dados de performance (CSV, JSON, API) | Dado | Pode ser lido de arquivos |
| 🟡 Google Ads / Meta Ads / GA4 exports | Dado | Opcional |
| 🟡 `bash` para executar scripts de análise | Permissão | Já configurada |

---

### 30. @csm-orquestrador — CSM Orchestrator

**O que faz:** Setup inicial, triagem de flags, QBR, fechamento de loop.

**Modelo:** `openrouter/openai/gpt-oss-120b:free` — temperatura 0.2

**Infraestrutura necessária:**
| Recurso | Tipo | Observação |
|---------|------|------------|
| 🔴 **OpenRouter API key** | API | Para usar o modelo `openrouter/openai/gpt-oss-120b:free` |
| 🔴 Dados do cliente na KB | Filesystem | `squads/{squad}/clientes/{cliente}/` |
| 🟡 Dados de NPS, CSAT, ROAS, OKR | Dado | Para ativar flags |

---

### 31. @executor-comite — Committee Executive

**O que faz:** Gera briefing automático do Comité de P&EG com dados de OKRs, sprints e FCAs.

**Infraestrutura necessária:**
| Recurso | Tipo | Observação |
|---------|------|------------|
| 🔴 Dados de OKR de todos os clientes ativos | Dado | Lido de arquivos |
| 🔴 Sprint status por cliente | Dado | De Ekyte ou task list |
| 🔴 FCAs abertas | Dado | De sistema de FCA |
| 🟡 NPS/CSAT trends | Dado | Para briefing completo |
| 🟡 `bash` para salvar .md e .html | Permissão | Já configurada |

---

## Categoria 6: Agentes Geradores

### 32. @gerar-doc — Document Generator

**O que faz:** Gera documentos formatados (atas, relatórios, propostas) no padrão V4.

**Modelo:** `google/gemini-2.5-flash` — temperatura 0.3

**Infraestrutura necessária:**
| Recurso | Tipo | Observação |
|---------|------|------------|
| 🔴 **API key para Google Gemini** (ou OpenRouter) | API | Para usar `google/gemini-2.5-flash` |
| 🟡 `bash` para salvar arquivos | Permissão | Já configurada |

---

### 33. @gerar-html — HTML Page Generator

**O que faz:** Gera páginas HTML completas e responsivas.

**Modelo:** `google/gemini-2.5-flash` — temperatura 0.3
**Skill:** `geral-frontend-design`

**Infraestrutura necessária:**
| Recurso | Tipo | Observação |
|---------|------|------------|
| 🔴 **API key para Google Gemini** (ou OpenRouter) | API | Para usar `google/gemini-2.5-flash` |
| 🟡 Navegador para testar renderização | — | Opcional |

---

### 34. @gerar-ppt — Presentation Generator

**O que faz:** Gera apresentações em HTML/PPT no padrão visual V4.

**Modelo:** `google/gemini-2.5-flash` — temperatura 0.3
**Skill:** `geral-frontend-design`

**Infraestrutura necessária:**
| Recurso | Tipo | Observação |
|---------|------|------------|
| 🔴 **API key para Google Gemini** (ou OpenRouter) | API | Para usar `google/gemini-2.5-flash` |

---

### 35. @gerar-pdf — PDF Generator

**O que faz:** Gera PDFs estilizados no padrão V4/Peretto.

**Modelo:** `google/gemini-2.5-flash` — temperatura 0.3
**Skill:** `geral-frontend-design`

**Infraestrutura necessária:**
| Recurso | Tipo | Observação |
|---------|------|------------|
| 🔴 **API key para Google Gemini** (ou OpenRouter) | API | Para usar `google/gemini-2.5-flash` |
| 🟡 **weasyprint** ou **puppeteer** instalado | CLI | Para converter HTML → PDF |
| 🟡 `bash` para executar conversão | Permissão | Já configurada |

---

## Tabela Consolidada de Infraestrutura

### APIs Externas Necessárias

| API / Serviço | Agentes que dependem | Prioridade |
|---------------|---------------------|------------|
| **V4mos API** (Meta Ads data) | `@midia-paga`, `@automacao-analytics`, `@relatorios-trafego`, `@media-buyer` | 🔴 Alta |
| **n8n instance** (self-hosted ou cloud) | `@automacao-analytics`, `@n8n-automator` | 🔴 Alta |
| **Google Gemini API** (para modelo) | `@gerar-doc`, `@gerar-html`, `@gerar-ppt`, `@gerar-pdf` | 🔴 Alta |
| **OpenRouter API** (para modelo) | `@csm-orquestrador` | 🟡 Média |
| **Google Analytics / GTM** | `@automacao-analytics`, `@relatorios-trafego` | 🟡 Média |
| **Google Ads API** | `@relatorios-trafego` | 🟡 Média |
| **Bing Ads API** | `@relatorios-trafego` | 🟢 Baixa |
| **Google Drive API** | `@pipeline-conteudo` | 🟢 Baixa |
| **Email service** (SendGrid/SES) | `@pipeline-conteudo` | 🟢 Baixa |
| **Gemini Deep Research** | `@pesquisador`, `@vendas-account` | 🟢 Baixa |
| **Image generation API** (Flux/Midjourney) | `@criacao-design` | 🟢 Baixa |
| **Video generation API** (Runway/HeyGen) | `@criacao-design` | 🟢 Baixa |

### Dados de Cliente (File System)

| Dado | Onde deve estar | Agentes que consomem |
|------|----------------|---------------------|
| Mission Control | `squads/{squad}/clientes/{cliente}/mission-control/` | `@account-orchestrator`, `@evolucao-checkins` |
| Check-ins | `squads/{squad}/clientes/{cliente}/checkins/` | `@account-orchestrator`, `@evolucao-checkins` |
| OKRs | No Mission Control ou arquivo dedicado | `@flag-okr`, `@executor-comite` |
| NPS/CSAT | No Mission Control | `@flag-churn`, `@analista-dados` |
| ROAS/CPA | No Mission Control ou base externa | `@flag-roi`, `@analista-dados`, `@relatorios-trafego` |
| Sprint status | Ekyte ou task list | `@flag-operacao`, `@executor-comite` |
| FCAs | Sistema de FCA | `@flag-operacao`, `@executor-comite` |

### Ferramentas CLI / Runtime

| Ferramenta | Agentes que dependem |
|------------|---------------------|
| `npx --yes n8nac` | `@n8n-automator` |
| `npx --yes @n8n-as-code/n8n-manager` | `@n8n-automator` |
| `weasyprint` ou `puppeteer` | `@gerar-pdf` |

---

## Checklist de Setup

### Para funcionamento 100% (Fase 2 — Produção)

- [ ] **V4mos API key** configurada em `clientes/*/.env`
- [ ] **n8n instance** rodando e acessível via n8n-as-code
- [ ] **Google Gemini API key** configurada (para `gerar-*` e `csm-orquestrador`)
- [ ] **n8nac-config.json** com environment ativo
- [ ] **Mission Control** populado para pelo menos 1 cliente (teste)
- [ ] Dados de **NPS, CSAT, OKR, ROAS** disponíveis em arquivo
- [ ] Google Drive / Email configurados (para `pipeline-conteudo`)

### Para testes simulados (Fase 1 — Modo Dry-Run)

- [x] OpenCode rodando
- [x] Skills em `.agents/skills/` e `.opencode/skills/`
- [x] Agentes em `.opencode/agents/`
- [ ] Nenhuma API externa necessária

---

*Próximo passo: Sessão 2 - Testes dos Orquestradores*
