# Projetos de Inovação — Open-Source para Marketing

> Catálogo de projetos open-source do GitHub que podem ser usados como base para produtos/serviços a oferecer aos clientes da V4 Company.

---

## Índice

1. [Analytics, BI & Dashboards](#1-analytics-bi--dashboards)
2. [SEO & AI Search Optimization (GEO)](#2-seo--ai-search-optimization-geo)
3. [CRM & Automação de Vendas](#3-crm--automação-de-vendas)
4. [Social Media Management](#4-social-media-management)
5. [Marketing Automation & AI Agents](#5-marketing-automation--ai-agents)
6. [Email Marketing](#6-email-marketing)
7. [Landing Pages & A/B Testing](#7-landing-pages--ab-testing)
8. [Competitor Analysis & Web Scraping](#8-competitor-analysis--web-scraping)
9. [Chatbots & Automação de Atendimento](#9-chatbots--automação-de-atendimento)
10. [Infraestrutura de Dados & Pipelines](#10-infraestrutura-de-dados--pipelines)

---

## 1. Analytics, BI & Dashboards

### Apache Superset
- **GitHub:** apache/superset
- **Stars:** 72.8k | **License:** Apache 2.0
- **Stack:** Python + TypeScript + React
- **Descrição:** Plataforma de BI empresarial moderna. Visualização de dados, SQL editor, semantic layer, cache, 40+ fontes de dados.
- **Oferta V4:** Dashboard white-label para clientes — conectar Meta Ads + Google Ads + GA4 + CRM num painel unificado.

### Metabase
- **GitHub:** metabase/metabase
- **Stars:** 46.7k | **License:** AGPL v3 (open-core)
- **Stack:** Clojure + TypeScript + React
- **Descrição:** BI mais fácil de usar. Question Builder para não-técnicos. X-ray, dashboards interativos.
- **Oferta V4:** Ideal para clientes que querem self-service analytics. Menos setup que Superset.

### Grafana
- **GitHub:** grafana/grafana
- **Stars:** 72.9k | **License:** AGPL v3
- **Stack:** Go + TypeScript + React
- **Descrição:** Plataforma de observabilidade e dashboards. Suporte a métricas, logs, traces. Ideal para monitoramento de campanhas em tempo real.
- **Oferta V4:** Dashboards de performance de mídia em tempo real para clientes.

### Lightdash
- **GitHub:** lightdash/lightdash
- **Stars:** 5.8k | **License:** MIT
- **Stack:** TypeScript + dbt
- **Descrição:** Alternativa open-source ao Looker. Conecta no dbt, permite criar métricas em YAML. Self-serve analytics.
- **Oferta V4:** BI para clientes que já usam dbt ou querem camada semântica controlada.

### Redash
- **GitHub:** getredash/redash
- **Stars:** 28.3k | **License:** BSD-2
- **Stack:** Python + JavaScript
- **Descrição:** Conecte 35+ fontes de dados, faça queries SQL, visualize e crie dashboards. Manutenção congelada (Databricks).
- **Oferta V4:** Legado, mas ainda útil. Prefira Superset ou Metabase para novos deployments.

### DataEase
- **GitHub:** dataease/dataease
- **Stars:** 23.7k | **License:** GPL v3
- **Stack:** Java + Vue.js
- **Descrição:** BI drag-and-drop, conexão com várias fontes, deploy fácil via Docker. Alternativa ao Tableau.
- **Oferta V4:** Opção para clientes que preferem interface mais simples que Superset.

---

## 2. SEO & AI Search Optimization (GEO)

### GEO SEO Claude
- **GitHub:** zubair-trabzada/geo-seo-claude
- **Stars:** 6.2k | **License:** MIT
- **Stack:** Python + Shell
- **Descrição:** Skill Claude Code para GEO-first SEO. Audita citabilidade, AI crawlers, schema, brand mentions. Gera relatórios PDF.
- **Oferta V4:** Oferecer auditoria GEO como serviço premium. Clientes pagam R$X/mês para relatórios mensais de visibilidade em IA.

### AI SEO Platform (GEO Tracker)
- **GitHub:** dipakkr/ai-seo-platform
- **Stars:** 1 | **License:** MIT
- **Stack:** Python + TypeScript + shadcn/ui
- **Descrição:** Plataforma GEO open-source. Rastreia visibilidade da marca em ChatGPT, Perplexity, Gemini, Claude, Grok.
- **Oferta V4:** Produto de monitoramento de AI Visibility para clientes.

### OpenCMO
- **GitHub:** study8677/OpenCMO
- **Stars:** 26 | **License:** MIT
- **Stack:** Python + TypeScript
- **Descrição:** Multi-agent AI CMO open-source. Monitora SEO, GEO, SERP e comunidades. Dashboard com 3D Knowledge Graph. BYOK.
- **Oferta V4:** Produto completo de marketing intelligence white-label para agências.

### SEO Autopilot
- **GitHub:** tentacl-ai/seo-autopilot
- **Stars:** 2 | **License:** MIT
- **Stack:** Python + FastAPI
- **Descrição:** Plataforma multi-tenant de SEO automation. 11 analisadores, 80+ checks, Playwright JS rendering, GEO audit, llms.txt, IndexNow, GSC.
- **Oferta V4:** Oferecer como SaaS white-label para clientes. Cada cliente = um tenant.

### FreeCrawl SEO Tool
- **GitHub:** kemalai/FreeCrawl-SEO-Tool
- **Stars:** 24 | **License:** MIT
- **Stack:** TypeScript + Electron + React
- **Descrição:** SEO crawler desktop open-source. 150+ checks, 1M+ URLs, alternativa ao Screaming Frog. Desktop app cross-platform.
- **Oferta V4:** Ferramenta interna de auditoria para equipe V4 ou revenda para clientes.

### Akii SEO AI Search Optimizer
- **GitHub:** akii-technologies-ltd/akii-seo-ai-search-optimizer
- **Stars:** 1 | **License:** MIT
- **Stack:** Markdown (plugin Claude Code)
- **Descrição:** Plugin gratuito Claude Code para SEO, AEO e GEO. Audita sites, gera schema, rastreia AI Visibility em 6 engines.
- **Oferta V4:** Skill interna para equipe V4 acelerar entregas de SEO/GEO.

### SEO Agency in a Box
- **GitHub:** z1fex/SEO-AGENCY-IN-A-BOX
- **Stars:** 2 | **License:** -
- **Stack:** Python + Firecrawl + Tavily
- **Descrição:** Agência SEO completa com 12 times e 75 agentes AI auto-orquestrados. Audit, keyword research, content, AEO, link building.
- **Oferta V4:** Automação completa de SEO para clientes. Um "agência SEO" rodando 24/7.

### Open SEO Crawler
- **GitHub:** puneetindersingh/open-seo-crawler
- **Stars:** 2 | **License:** MIT
- **Stack:** JavaScript + Python
- **Descrição:** Crawler SEO auto-hospedado. Crawling concorrente, detecção de CMS (Shopify/WordPress/Wix), issues por severidade.
- **Oferta V4:** Alternativa free ao Screaming Frog para auditorias internas.

---

## 3. CRM & Automação de Vendas

### WuKong AI CRM
- **GitHub:** WuKongOpenSource/AI_CRM
- **Stars:** 620 | **License:** MIT
- **Stack:** Java + Spring Boot + Vue 3
- **Descrição:** CRM conversacional com IA. Assistente AI, RAG, gestão de clientes, geração de tarefas automática.
- **Oferta V4:** CRM white-label para clientes que precisam de gestão de leads com AI integrada.

### Signal
- **GitHub:** jay-sahnan/signal
- **Stars:** 256 | **License:** AGPL v3
- **Stack:** TypeScript + Supabase + Anthropic
- **Descrição:** Alternativa open-source ao Clay, Apollo e Outreach. Sinais de compra, enriquecimento de contatos, sequências de email.
- **Oferta V4:** Produto de sales intelligence para clientes B2B. "Clay open-source."

### Arkitekt OpenCRM
- **GitHub:** arkitekt-ai/OpenCRM
- **Stars:** 2 | **License:** MIT
- **Stack:** Python + Flask
- **Descrição:** CRM auto-hospedado. Lead automation via Meta Lead Ads, kanban, campanhas de email, AI copy generation.
- **Oferta V4:** CRM simples para pequenos clientes. Integração direta com Meta Ads.

### nowCRM
- **GitHub:** nowtec/nowCRM
- **Stars:** 23 | **License:** AGPL v3
- **Stack:** TypeScript + Next.js + Strapi
- **Descrição:** CRM com multichannel outreach (Email, SMS, WhatsApp, LinkedIn, Telegram). Journeys automatizadas, form builder, social media calendar.
- **Oferta V4:** CRM completo multicanal para clientes médios.

### ConvergioAI
- **GitHub:** InstinctBits/convergioai
- **Stars:** 1 | **License:** MIT
- **Stack:** React + Express + PostgreSQL
- **Descrição:** CRM omnichannel com AI para agências. Unified inbox, AI email agent, content generation, task management.
- **Oferta V4:** CRM feito para agências de marketing. Ideal para operação V4.

---

## 4. Social Media Management

### BrightBean Studio
- **GitHub:** brightbeanxyz/brightbean-studio
- **Stars:** 1.7k | **License:** AGPL v3
- **Stack:** Python + Django + HTMX
- **Descrição:** Alternativa open-source ao Buffer/Sendible/SocialPilot. 10+ plataformas, scheduling, unified social inbox, analytics.
- **Oferta V4:** Ferramenta white-label de gestão de redes sociais para clientes. Self-hosted, sem limites por usuário.

### SocialFlow
- **GitHub:** inbharatai/SocialFlow
- **Stars:** 0 | **License:** -
- **Stack:** Python + FastAPI + Playwright
- **Descrição:** AI CMO autônomo para redes sociais. 6 agentes (Scout, Planner, Creator, Reviewer, Publisher, Analyst). 12 plataformas.
- **Oferta V4:** Automação completa de conteúdo social para clientes. Geração + publicação 100% autônoma.

### SocialBlast (Social Auto Engine)
- **GitHub:** Freespirits/social-auto-engine
- **Stars:** 9 | **License:** -
- **Stack:** Python + FastAPI + HTMX
- **Descrição:** OS para redes sociais. Escreva uma vez, publique em Facebook, Instagram, Threads, WhatsApp, LinkedIn. MCP server incluso.
- **Oferta V4:** Ferramenta de conteúdo multiplataforma com aprovação humana no fluxo.

### Socioboard
- **GitHub:** socioboard/socioboard
- **Stars:** 1 | **License:** AGPL v3
- **Stack:** Python + FastAPI + React
- **Descrição:** Gestão de mídias sociais completa. Scheduling, analytics, asset vault, bulk CSV deployment. Suporta Facebook, Twitter, LinkedIn, Pinterest, Snapchat.
- **Oferta V4:** Alternativa madura (20k+ usuários) para gestão de social media de clientes.

### ZernFlow
- **GitHub:** zernio-dev/zernflow
- **Stars:** 0 | **License:** -
- **Stack:** TypeScript + Next.js + Supabase
- **Descrição:** Alternativa open-source ao ManyChat. Visual chatbot builder para Instagram, Facebook, Telegram, Twitter, Bluesky, Reddit.
- **Oferta V4:** Chatbot multicanal para atendimento e nutrição de leads dos clientes.

### Rebel Forge
- **GitHub:** hec-ovi/rebel-forge
- **Stars:** 1 | **License:** -
- **Stack:** Python + TypeScript + Next.js
- **Descrição:** AI agent autônomo para social media. Per-platform voice memory, 11 tools, error recovery. Publica em X, LinkedIn, Facebook, Instagram, Threads.
- **Oferta V4:** Automação de conteúdo com voz de marca consistente.

### CosyWorld
- **GitHub:** cenetex/cosyworld
- **Stars:** N/A | **License:** -
- **Stack:** Python + FastAPI
- **Descrição:** Gestão unificada de comunidades Discord, X, Telegram com AI agents autônomos.
- **Oferta V4:** Gestão de comunidades para clientes que têm presença em múltiplos canais.

---

## 5. Marketing Automation & AI Agents

### MiCA — AI Marketing Campaign Automation
- **GitHub:** RenegadeRocks/MiCA-OSS-Marketing-Automation-System
- **Stars:** 6 | **License:** MIT
- **Stack:** TypeScript + React + Supabase + HeyGen
- **Descrição:** Descreva o negócio uma vez → campanha multicanal completa em 5 min (email, WhatsApp, Instagram, vídeo avatar AI).
- **Oferta V4:** Produto de geração automática de campanhas para clientes. Ideal para pequenos negócios.

### OpenSoul
- **GitHub:** iamevandrake/opensoul
- **Stars:** 13 | **License:** MIT
- **Stack:** TypeScript + Paperclip
- **Descrição:** Stack agentic de marketing. Time de AI agents organizados como agência real: Director, Strategist, Creative, Producer, Growth, Analyst.
- **Oferta V4:** Produto "agência de marketing AI" white-label para clientes. Agência rodando 24/7.

### Marketing Engine
- **GitHub:** wesleysimplicio/marketing-engine
- **Stars:** 2 | **License:** Apache 2.0
- **Stack:** TypeScript + Node.js
- **Descrição:** Engine de marketing provider-agnostic. Pipeline: brief → script → creative → caption → compliance → publish → metrics → ads.
- **Oferta V4:** Pipeline de conteúdo escalável. Troca de provider via env, sem refatoração.

### Mureo
- **GitHub:** logly/mureo
- **Stars:** 1 | **License:** Apache 2.0
- **Stack:** Python
- **Descrição:** Framework para AI agents operarem contas de anúncio (Google Ads, Meta Ads, Search Console, GA4). Grounded em STRATEGY.md.
- **Oferta V4:** Automação de operação de mídia paga. Agente que diagnostica campanhas e sugere otimizações.

### Garnet AI
- **GitHub:** mark02252/garnet-ai
- **Stars:** 2 | **License:** MIT
- **Stack:** TypeScript + Next.js + Supabase
- **Descrição:** Marketing advisor AI autônomo. 5 especialistas (Data Analyst, Content Strategist, CRO, Psychologist, Strategy Lead). Aprende com feedback.
- **Oferta V4:** Assistente de marketing contínuo para clientes. Roda 24/7, aprende o negócio do cliente.

### Full-Funnel AI Analytics
- **GitHub:** eduardocornelsen/full-funnel-ai-analytics
- **Stars:** 2 | **License:** MIT
- **Stack:** Python + dbt + MCP + DuckDB + Streamlit
- **Descrição:** Analytics de marketing multicanal com linguagem natural. MCP servers para Meta/Google Ads, GA4, CRM. XGBoost lead scoring.
- **Oferta V4:** Produto de analytics full-funnel. Pergunte em português, receba insights.

### NexusAI
- **GitHub:** thoufiq2326/NexusAI
- **Stars:** 1 | **License:** -
- **Stack:** JavaScript + Python + Gemini
- **Descrição:** Plataforma multi-agent B2B. 4 agentes (Hunter, Guardian, Professor, Closer). Lead scoring → compliance → RAG content → CRM sync.
- **Oferta V4:** Automação completa de pipeline B2B para clientes.

### Marketing Brain (MCP Server)
- **GitHub:** timmeck/marketing-brain
- **Stars:** 0 | **License:** -
- **Stack:** TypeScript
- **Descrição:** MCP server que dá ao Claude Code memória persistente de marketing. Rastreia posts, aprende padrões, sugere conteúdo.
- **Oferta V4:** Skill interna para equipe V4. Acelera estratégia de conteúdo com memória de aprendizado.

---

## 6. Email Marketing

### Opensend
- **GitHub:** namuh-eng/opensend
- **Stars:** 28 | **License:** Elastic 2.0
- **Stack:** TypeScript + Next.js + AWS SES
- **Descrição:** Alternativa open-source ao Resend. APIs REST, templates React email, broadcasts, automations, analytics, MCP server.
- **Oferta V4:** Infraestrutura de email white-label para clientes. Self-hosted, sem custo por envio.

### Senlo
- **GitHub:** IgorFilippov3/senlo
- **Stars:** 169 | **License:** AGPL v3
- **Stack:** TypeScript + Next.js + PostgreSQL
- **Descrição:** Editor visual de email drag-and-drop. Templates com versionamento, variáveis dinâmicas, provider-agnostic (SMTP/ESP).
- **Oferta V4:** Editor de email white-label para embedded em produtos de clientes.

### SendDock
- **GitHub:** Arkhe-Systems/senddock
- **Stars:** 8 | **License:** AGPL v3
- **Stack:** Go + Vue.js
- **Descrição:** Plataforma de email marketing self-hostable. API-first, BYO-SMTP. Open/click tracking, broadcasts, webhooks.
- **Oferta V4:** Email marketing server para clientes. Zero custo por email.

### NetSendo
- **GitHub:** NetSendo/NetSendo
- **Stars:** N/A | **License:** -
- **Stack:** Laravel + Vue.js + Docker
- **Descrição:** Plataforma profissional de email marketing com webinars, funis de venda, AI suite, MCP server, SMS.
- **Oferta V4:** Plataforma all-in-one de email + automação para clientes.

### OpenMail
- **GitHub:** ShadowWalker2014/openmail
- **Stars:** 1 | **License:** Elastic 2.0
- **Stack:** TypeScript + Hono + React
- **Descrição:** Alternativa open-source ao Customer.io. API completa, SDK nativo, MCP server, campanhas event-triggered.
- **Oferta V4:** Automação de lifecycle email para clientes SaaS.

### Outlet
- **GitHub:** outlet-sh/outlet
- **Stars:** 1 | **License:** AGPL v3
- **Stack:** Go + Svelte
- **Descrição:** Plataforma de email self-hosted em binário único. Marketing + transactional + MCP. SQLite, 100k+ subscribers.
- **Oferta V4:** Solução simples de email marketing para clientes menores. Deploy em minutos.

### CadenceRelay
- **GitHub:** pulkitpareek18/CadenceRelay
- **Stars:** 2 | **License:** Custom
- **Stack:** TypeScript + React + Express
- **Descrição:** Envio de email em massa open-source. 100k+ emails personalizados via Gmail SMTP ou AWS SES. Tracking, throttling.
- **Oferta V4:** Bulk email sender white-label para clientes com grandes bases.

### Sesy
- **GitHub:** dontic/sesy
- **Stars:** 4 | **License:** MIT
- **Stack:** Python + Django + React
- **Descrição:** Gestão de campanhas de email sobre AWS SES. Configuração guiada, verificação de domínio, audience management.
- **Oferta V4:** Camada de gestão sobre SES para clientes técnicos.

---

## 7. Landing Pages & A/B Testing

### OpenPage
- **GitHub:** buildingopen/openpage
- **Stars:** 6 | **License:** MIT
- **Stack:** TypeScript + React + Tailwind + Gemini
- **Descrição:** Website builder drag-and-drop open-source. Alternativa ao Framer/Lovable/v0. JSON-first, exporta HTML standalone.
- **Oferta V4:** Building de landing pages para clientes com AI generation + editor visual.

### PageForge
- **GitHub:** G-akram/saas-landing-page-builder
- **Stars:** 1 | **License:** MIT
- **Stack:** TypeScript + Next.js + Stripe
- **Descrição:** Landing page builder com drag-and-drop, A/B testing (4 variantes), analytics, Stripe billing.
- **Oferta V4:** Produto de criação e teste de landing pages para clientes.

### Shippage
- **GitHub:** imjahanzaib/shippage
- **Stars:** 1 | **License:** MIT
- **Stack:** Python + TypeScript
- **Descrição:** Geração de landing pages com copy de conversão (1000+ fórmulas A/B testadas). Popups exit-intent, consentimento LGPD/GDPR, schemas SEO.
- **Oferta V4:** Geração de LPs otimizadas para conversão. Substitui copywriter.

### Landing Page Factory
- **GitHub:** TheMattBerman/landing-page-factory
- **Stars:** 32 | **License:** MIT
- **Stack:** Python + Shell
- **Descrição:** Pipeline completo de LP: Extract → Strategize → Profile → Write → Visual → Build → QA → Ship. Claude Cowork + OpenClaw.
- **Oferta V4:** Fábrica de landing pages baseada em dados reais do cliente. Estratégia-first.

### Mutatr
- **GitHub:** novynlabs-repo/mutatr
- **Stars:** 0 | **License:** MIT
- **Stack:** JavaScript + Electron + Claude Agent SDK
- **Descrição:** Agente autônomo de A/B testing. Sugere testes, implementa variantes, simula atenção com personas sintéticas.
- **Oferta V4:** Ferramenta de A/B testing autônoma para clientes com pouco tráfego.

### VariantLab
- **GitHub:** Minhaj-Rabby/variantlab
- **Stars:** 0 | **License:** MIT
- **Stack:** TypeScript
- **Descrição:** Toolkit universal de A/B testing e feature flags. Framework-agnostic (React, Next, Vue, Svelte, Solid). <3KB gzipped.
- **Oferta V4:** Biblioteca de experimentação para produtos digitais dos clientes.

### BuildStory Agents
- **GitHub:** zhang-liz/buildstory-agents
- **Stars:** 0 | **License:** MIT
- **Stack:** TypeScript + Next.js + Supabase
- **Descrição:** AI agents que geram, testam e otimizam landing pages em tempo real. Thompson sampling, persona-based targeting.
- **Oferta V4:** Landing pages adaptativas que mudam conforme o visitante.

### Evoloop
- **GitHub:** michellemayes/evoloop
- **Stars:** 0 | **License:** MIT
- **Stack:** TypeScript + Python + FastAPI
- **Descrição:** Engine autônoma de otimização de landing pages. Gera, testa e evolui variantes com Thompson Sampling.
- **Oferta V4:** Otimização contínua de landing pages para clientes.

---

## 8. Competitor Analysis & Web Scraping

### Rival
- **GitHub:** tessak22/rival
- **Stars:** 3 | **License:** MIT
- **Stack:** TypeScript + Next.js + Tabstack
- **Descrição:** Dashboard de inteligência competitiva. Rastreia pricing, changelogs, careers, docs, social, GitHub. MCP server incluso.
- **Oferta V4:** Produto de monitoramento de concorrentes para clientes. Briefings automáticos semanais.

### CompetitorScope
- **GitHub:** maomaozhe/CompetitorScope
- **Stars:** 7 | **License:** MIT
- **Stack:** Python + LangGraph + Next.js
- **Descrição:** Sistema multi-agent de pesquisa competitiva. Planner → Collector → Analyst → Comparator → Writer. Relatório Markdown.
- **Oferta V4:** Análise competitiva profunda para clientes. Relatórios com cadeia de evidência.

### Drift
- **GitHub:** getdrift/drift
- **Stars:** 0 | **License:** MIT
- **Stack:** TypeScript + Gemini
- **Descrição:** Intel competitiva semanal. Scrapeia pricing, changelog, hiring, blog. Snapshot + diff + relatório AI. Entrega via Slack/Discord/Email.
- **Oferta V4:** Serviço de inteligência competitiva recorrente para clientes.

### Prism
- **GitHub:** yash7agarwal/prism
- **Stars:** 0 | **License:** -
- **Stack:** TypeScript + Python + Next.js
- **Descrição:** Product OS para PMs. Agentes autônomos de inteligência competitiva, pesquisa de indústria, mapeamento de UX flows.
- **Oferta V4:** Inteligência competitiva + pesquisa de mercado para clientes de produto.

### Tech Analyst
- **GitHub:** meirk-brd/tech-analyst
- **Stars:** 0 | **License:** MIT
- **Stack:** TypeScript + Next.js + Gemini + Bright Data
- **Descrição:** Análise de mercado com visualizações Gartner Magic Quadrant, Forrester Wave, GigaOm Radar.
- **Oferta V4:** Relatórios de mercado com visuais de consultoria. Ideal para apresentações a clientes.

### AI Scraping Stack
- **GitHub:** homgorn/AI-Scraping-Stack
- **Stars:** 0 | **License:** MIT
- **Stack:** Python + FastAPI + 10+ providers
- **Descrição:** Plataforma de web intelligence com 10+ provedores de scraping, cascade fallback, análise VLM de screenshots, geração de código.
- **Oferta V4:** Infraestrutura de scraping para alimentar ferramentas de análise competitiva.

### Competitor Hunter
- **GitHub:** Duang777/competitor-hunter
- **Stars:** 3 | **License:** MIT
- **Stack:** Python + LangGraph + Playwright + MCP
- **Descrição:** AI agent para análise de concorrentes. Scraping + extração estruturada com LLM. Integração MCP com Claude Desktop.
- **Oferta V4:** Ferramenta interna rápida para análise de concorrentes.

### Competitor Monitor
- **GitHub:** Keerthivasan-Venkitajalam/competitor-monitor
- **Stars:** 3 | **License:** -
- **Stack:** Python + Playwright + sentence-transformers
- **Descrição:** Monitoramento autônomo de concorrentes. Embeddings semânticos detectam mudanças estratégicas (não só typos).
- **Oferta V4:** Monitoramento inteligente que separa ruído de sinal estratégico.

---

## 9. Chatbots & Automação de Atendimento

### ZernFlow
- (já descrito em Social Media)
- **Oferta V4:** Chatbot multicanal para atendimento e nutrição. Visual flow builder com AI Response Node.

### CosyWorld
- (já descrito em Social Media)
- **Oferta V4:** Gestão de comunidades + AI agents que interagem naturalmente.

---

## 10. Infraestrutura de Dados & Pipelines

### n8n (já usado pela V4)
- **GitHub:** n8n-io/n8n
- **Stars:** 60k+ | **License:** Sustainable Use License
- **Stack:** TypeScript + Node.js + Vue.js
- **Descrição:**Automação de workflows com 400+ integrações. Já usado na V4 para pipelines de dados.
- **Oferta V4:** Base de integração para todos os produtos acima.

### dbt Core (já usado)
- **GitHub:** dbt-labs/dbt-core
- **Stars:** 12k+ | **License:** Apache 2.0
- **Stack:** Python + SQL + Jinja
- **Descrição:** Transformação de dados analíticos. Já usado pela V4.
- **Oferta V4:** Camada de transformação para os produtos de analytics.

### DuckDB
- **GitHub:** duckdb/duckdb
- **Stars:** 28k+ | **License:** MIT
- **Stack:** C++
- **Descrição:** Database analítico embedded. Perfeito para analytics local sem infraestrutura.
- **Oferta V4:** Processamento de dados local para clientes sem data warehouse.

---

## Resumo das Ofertas por Perfil de Cliente

| Perfil do Cliente | Produtos Recomendados | Ticket Estimado |
|---|---|---|
| **Pequeno negócio local** | MiCA + ZernFlow + Sesy/Outlet + OpenPage | R$ 500-2k/mês |
| **E-commerce médio** | Metabase + BrightBean + SEO Autopilot + SendDock + CompetitorScope | R$ 2-8k/mês |
| **SaaS B2B** | Signal + Mureo + OpenCMO + VariantLab + Rival + OpenMail | R$ 5-15k/mês |
| **Empresa/grande conta** | Superset + OpenSoul + SEO Agency in a Box + Prism + NetSendo | R$ 10-30k/mês |
| **Produto white-label V4** | Combinação de 2-3 ferramentas empacotadas como plataforma única | R$ 15-50k/mês |

## Próximos Passos

1. **Priorizar 3-5 projetos** para POC baseado no perfil dos clientes atuais da V4
2. **Fazer deploy de referência** de cada projeto em Docker
3. **Testar integração** com as ferramentas que a V4 já usa (n8n, Meta Ads, Google Ads)
4. **Criar landing page** para o serviço/produto usando Landing Page Factory ou OpenPage
5. **Validar com cliente real** em 30 dias

---

> **Nota:** Para cada projeto, verificar a licença antes de usar comercialmente. Projetos AGPL requerem atenção especial se forem modificados e distribuídos como serviço.
