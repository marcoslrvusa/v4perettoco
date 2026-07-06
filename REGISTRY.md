# Builders Hub — Registry

**106 skills** · última atualização: 2026-07-06

> Catálogo auto-gerado por `scripts/build-registry.py`. Não edite à mão — rode `/sync-hub` ou envie PR pela `/compartilhar-skill`.

## Índice

- [🛠 Base (setup/fluxo)](#base) (7)
- [🌐 Geral](#geral) (88)
- [🎯 Gestao de Trafego](#gt) (3)
- [✍️ Copy](#copy) (2)
- [🤝 Account](#account) (5)
- [🔌 Integrações / Fontes](#fontes) (1)
  - [🔌 V4mos](#v4mos) (1)

## 🛠 Base (setup/fluxo)

<a id="base"></a>

| Skill | O que faz | Autor | v |
|---|---|---|---|
| `compartilhar-skill` | Empacota uma skill local e abre Pull Request no Builders Hub publico automaticamente. Use quando o usuario... | — | — |
| `contexto` | Le todos os arquivos em uma KB (cliente, squad ou projeto), gera CLAUDE.md e AGENTS.md, e quando for client... | — | — |
| `criador-de-skills` | Cria skills novas e melhora skills existentes no Builders Hub. Use quando o usuario quiser criar uma skill... | — | — |
| `novo-cliente` | Cria uma nova pasta de cliente dentro de um squad com estrutura padrao, CLAUDE.md/AGENTS.md iniciais, links... | — | — |
| `novo-projeto` | Cria uma nova pasta de projeto com estrutura padrao em bases/. Use quando o usuario rodar /novo-projeto ou... | — | — |
| `onboarding` | Configura todo o ambiente do usuario pra trabalhar com IA na V4 via o Builders Hub — valida e conserta git... | — | — |
| `sync-hub` | Atualiza o Builders Hub local puxando as skills mais recentes do repo publico, mostra diff do que mudou des... | — | — |

## 🌐 Geral

<a id="geral"></a>

| Skill | O que faz | Autor | v |
|---|---|---|---|
| `ab-test-setup` | When the user wants to plan, design, or implement an A/B test or experiment, or build a growth experimentat... | — | 1.2.0 |
| `ad-creative` | When the user wants to generate, iterate, or scale ad creative — headlines, descriptions, primary text, or... | — | 1.1.0 |
| `add-opencode-model` | Fetch OpenCode Zen model details and provide guidance for adding models to acai-ts provider configuration. | — | — |
| `agents-md-generator` | Generate hierarchical AGENTS.md structures for codebases. Use when user asks to create AGENTS.md files, ana... | — | — |
| `ai-maestro-agent-messaging` | Send and receive messages between AI agents using AI Maestro's messaging system. Use when the user asks to... | — | — |
| `ai-search` | Setor completo de AI Search (AEO + GEO + AI SEO) — diagnose, implementa e gerencia a presenca de marcas em... | — | — |
| `ai-seo` | When the user wants to optimize content for AI search engines, get cited by LLMs, or appear in AI-generated... | — | 1.2.0 |
| `all-plan` | Collaborative planning with all mounted CLIs (Claude, Codex, Gemini, OpenCode) for comprehensive solution d... | — | — |
| `analytics-tracking` | When the user wants to set up, improve, or audit analytics tracking and measurement. Also use when the user... | — | 1.1.0 |
| `aso-audit` | When the user wants to audit or optimize an App Store or Google Play listing. Also use when the user mentio... | — | 1.0.0 |
| `blip-2-vision-language` | Vision-language pre-training framework bridging frozen image encoders and LLMs. Use when needing image capt... | @davila7 | 1.0.0 |
| `churn-prevention` | When the user wants to reduce churn, build cancellation flows, set up save offers, recover failed payments,... | — | 1.1.0 |
| `claude-automation-recommender` | Analyze a codebase and recommend Claude Code automations (hooks, subagents, skills, plugins, MCP servers).... | — | — |
| `co-marketing` | When the user wants to find co-marketing partners, plan joint campaigns, or brainstorm partnership opportun... | — | 1.0.0 |
| `codeagent` | Execute codeagent-wrapper for multi-backend AI code tasks. Supports Codex, Claude, Gemini, and OpenCode bac... | — | — |
| `cold-email` | Write B2B cold emails and follow-up sequences that get replies. Use when the user wants to write cold outre... | — | 1.1.0 |
| `community-marketing` | Build and leverage online communities to drive product growth and brand loyalty. Use when the user wants to... | — | 1.0.0 |
| `competitor-alternatives` | When the user wants to create competitor comparison or alternative pages for SEO and sales enablement. Also... | — | 1.1.0 |
| `competitor-profiling` | When the user wants to research, profile, or analyze competitors from their URLs. Also use when the user me... | — | 1.0.0 |
| `computer-use-agents` | Build AI agents that interact with computers like humans do - viewing screens, moving cursors, clicking but... | — | — |
| `content-strategy` | When the user wants to plan a content strategy, decide what content to create, or figure out what topics to... | — | 1.1.0 |
| `copywriting` | When the user wants to write, rewrite, or improve marketing copy for any page — including homepage, landing... | — | 1.1.0 |
| `create-opencode-plugin` | Create OpenCode plugins using the @opencode-ai/plugin SDK. Use for building custom tools, event hooks, auth... | — | — |
| `creating-opencode-agents` | Use when creating OpenCode agents - provides markdown format with YAML frontmatter, mode/tools/permission c... | — | — |
| `customer-research` | When the user wants to conduct, analyze, or synthesize customer research. Use when the user mentions "custo... | — | 1.0.0 |
| `developer` | Portal de skills pessoais do desenvolvedor. Use /developer para acessar ferramentas técnicas (ML/LLM, OpenC... | — | — |
| `directory-submissions` | When the user wants to submit their product to startup, SaaS, AI, agent, MCP, no-code, or review directorie... | — | 1.0.0 |
| `email-sequence` | When the user wants to create or optimize an email sequence, drip campaign, automated email flow, or lifecy... | — | 1.1.0 |
| `evaluating-llms-harness` | Evaluates LLMs across 60+ academic benchmarks (MMLU, HumanEval, GSM8K, TruthfulQA, HellaSwag). Use when ben... | @davila7 | 1.0.0 |
| `fine-tuning-with-trl` | Fine-tune LLMs using reinforcement learning with TRL - SFT for instruction tuning, DPO for preference align... | @davila7 | 1.0.0 |
| `flow-next-opencode-interview` | Interview user in-depth about an epic, task, or spec file to extract complete implementation details. Use w... | — | — |
| `flow-next-opencode-plan` | Create structured build plans from feature requests or Flow IDs. Use when planning features or designing im... | — | — |
| `flow-next-opencode-work` | Execute a Flow epic or task systematically with git setup, task tracking, quality checks, and commit workfl... | — | — |
| `form-cro` | When the user wants to optimize any form that is NOT signup/registration — including lead capture forms, co... | — | 1.1.0 |
| `free-tool-strategy` | When the user wants to plan, evaluate, or build a free tool for marketing purposes — lead generation, SEO v... | — | 1.1.0 |
| `geral-agents-hub` | (sem descrição) | — | — |
| `geral-ai-visibility` | Skill migrada para ai-search. Use ai-search para acesso ao setor completo de AI Search (AEO + GEO + AI SEO). | — | — |
| `geral-brainstormar-sobre-minha-funcao` | Entrevista o usuario sobre seu trabalho para descobrir como usar IA no dia a dia dele. Configura agenda, an... | — | — |
| `geral-contexto-cliente` | Puxa, registra e sincroniza fatos exatos do cliente (tom de voz, histórico, oferta) no Supabase pra aliment... | — | 1.0.0 |
| `geral-frontend-design` | Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the... | — | — |
| `geral-log-sessoes` | >- | @Marcos Luciano Rodrigues Vieira | 1.0.0 |
| `geral-memoria-agentes` | > | @Marcos Luciano Rodrigues Vieira | 1.0.0 |
| `geral-sabatina` | Entrevista o usuario de forma implacavel sobre cada aspecto de um plano ou design ate atingir entendimento... | — | — |
| `git-advanced-workflows` | Master advanced Git workflows including rebasing, cherry-picking, bisect, worktrees, and reflog to maintain... | — | — |
| `hqq-quantization` | Half-Quadratic Quantization for LLMs without calibration data. Use when quantizing models to 4/3/2-bit prec... | @davila7 | 1.0.0 |
| `image` | When the user wants to create, generate, edit, or optimize images for marketing — blog heroes, social graph... | — | 1.0.0 |
| `implementing-agent-modes` | Guidelines to create/update a new mode for PostHog AI agent. Modes are a way to limit what tools, prompts,... | — | — |
| `implicit-decision-capture` | Automatically capture implicit technical decisions and uncertainties encountered by AI agents during coding... | — | — |
| `launch-strategy` | When the user wants to plan a product launch, feature announcement, or release strategy. Also use when the... | — | 1.1.0 |
| `lead-magnets` | When the user wants to create, plan, or optimize a lead magnet for email capture or lead generation. Also u... | — | 1.0.0 |
| `m12-lifecycle` | Use when designing resource lifecycles. Keywords: RAII, Drop, resource lifecycle, connection pool, lazy ini... | — | — |
| `marketing-ideas` | When the user needs marketing ideas, inspiration, or strategies for their SaaS or software product. Also us... | — | 1.1.0 |
| `marketing-psychology` | When the user wants to apply psychological principles, mental models, or behavioral science to marketing. A... | — | 1.1.0 |
| `n8n-architect` | Use when the user explicitly wants to create, edit, validate, sync, or troubleshoot n8n workflows, asks abo... | — | — |
| `new-agent-creation` | Provides step-by-step templates and guidance for creating new AI agents in Unite-Hub with proper registrati... | — | — |
| `novo-squad` | Cria uma nova pasta de squad em squads/ com entry point e estrutura padrao. Pergunta nome do squad e quem e... | — | — |
| `onboarding-cro` | When the user wants to optimize post-signup onboarding, user activation, first-run experience, or time-to-v... | — | 1.1.0 |
| `opend` | Fetch the latest reply from OpenCode (shorthand: oc) storage via the `opend` CLI. Use only when the user ex... | — | — |
| `openrouter-fallback-config` | Configure model fallback chains for high availability. Use when building fault-tolerant LLM systems. Trigge... | @jeremylongshore | 1.0.0 |
| `opensquad` | Opensquad — Create and run AI agent squads for your business. Acione quando o usuário rodar /opensquad. | — | — |
| `oping` | Test connectivity with OpenCode (shorthand: oc) via the `oping` CLI. Use when the user explicitly asks to c... | — | — |
| `page-cro` | When the user wants to optimize, improve, or increase conversions on any marketing page — including homepag... | — | 1.1.0 |
| `paid-ads` | When the user wants help with paid advertising campaigns on Google Ads, Meta (Facebook/Instagram), LinkedIn... | — | 1.2.0 |
| `paywall-upgrade-cro` | When the user wants to create or optimize in-app paywalls, upgrade screens, upsell modals, or feature gates... | — | 1.1.0 |
| `perry-workspaces` | Create and manage isolated Docker workspaces on your tailnet with Claude Code and OpenCode pre-installed. | — | — |
| `plugin-dev` | This skill should be used when creating extensions for Claude Code or OpenCode, including plugins, commands... | — | — |
| `popup-cro` | When the user wants to create or optimize popups, modals, overlays, slide-ins, or banners for conversion pu... | — | 1.1.0 |
| `pricing-strategy` | When the user wants help with pricing decisions, packaging, or monetization strategy. Also use when the use... | — | 1.1.0 |
| `product-marketing-context` | When the user wants to create or update their product marketing context document. Also use when the user me... | — | 1.1.0 |
| `programmatic-seo` | When the user wants to create SEO-driven pages at scale using templates and data. Also use when the user me... | — | 1.1.0 |
| `quantizing-models-bitsandbytes` | Quantizes LLMs to 8-bit or 4-bit for 50-75% memory reduction with minimal accuracy loss. Use when GPU memor... | @davila7 | 1.0.0 |
| `referral-program` | When the user wants to create, optimize, or analyze a referral program, affiliate program, or word-of-mouth... | — | 1.1.0 |
| `revops` | When the user wants help with revenue operations, lead lifecycle management, or marketing-to-sales handoff... | — | 1.1.0 |
| `sales-enablement` | When the user wants to create sales collateral, pitch decks, one-pagers, objection handling docs, or demo s... | — | 1.1.0 |
| `schema-markup` | When the user wants to add, fix, or optimize schema markup and structured data on their site. Also use when... | — | 1.1.0 |
| `seo-audit` | When the user wants to audit, review, or diagnose SEO issues on their site. Also use when the user mentions... | — | 1.2.0 |
| `signup-flow-cro` | When the user wants to optimize signup, registration, account creation, or trial activation flows. Also use... | — | 1.1.0 |
| `simpo-training` | Simple Preference Optimization for LLM alignment. Reference-free alternative to DPO with better performance... | @davila7 | 1.0.0 |
| `site-architecture` | When the user wants to plan, map, or restructure their website's page hierarchy, navigation, URL structure,... | — | 1.1.0 |
| `social-content` | When the user wants help creating, scheduling, or optimizing social media content for LinkedIn, Twitter/X,... | — | 1.3.0 |
| `station` | Use Station CLI (`stn`) for AI agent orchestration - creating agents, running tasks, managing environments,... | — | — |
| `supabase` | Use when doing ANY task involving Supabase. Triggers: Supabase products (Database, Auth, Edge Functions, Re... | @supabase | 0.1.2 |
| `supabase-postgres-best-practices` | Postgres performance optimization and best practices from Supabase. Use this skill when writing, reviewing,... | @supabase | 1.1.1 |
| `temporal-python-testing` | Test Temporal workflows with pytest, time-skipping, and mocking strategies. Covers unit testing, integratio... | — | — |
| `testing-python` | Write and evaluate effective Python tests using pytest. Use when writing tests, reviewing test code, debugg... | — | — |
| `v3-deep-integration` | Deep agentic-flow@alpha integration implementing ADR-001. Eliminates 10,000+ duplicate lines by building cl... | — | — |
| `v3-mcp-optimization` | MCP server optimization and transport layer enhancement for claude-flow v3. Implements connection pooling,... | — | — |
| `video` | When the user wants to create, generate, or produce video content using AI tools or programmatic frameworks... | — | 1.0.0 |

## 🎯 Gestao de Trafego

<a id="gt"></a>

| Skill | O que faz | Autor | v |
|---|---|---|---|
| `gt-gestor-de-trafego-completo` | >- | @marcoslrvusa | 1.0.0 |
| `gt-media-buyer-completo` | >- | @marcoslrvusa | 1.0.0 |
| `gt-relatorios-trafego` | Relatorio consolidado de trafego multicanal — Google Ads, Meta Ads, Bing Ads. Gera reports HTML/JSON, envia... | @v4team | 1.0.0 |

## ✍️ Copy

<a id="copy"></a>

| Skill | O que faz | Autor | v |
|---|---|---|---|
| `copy-editing` | When the user wants to edit, review, or improve existing marketing copy, or refresh outdated content. Also... | — | 1.3.0 |
| `copy-pipeline-conteudo` | Pipeline completo de conteudo editorial — cria calendario, produz blog posts e email marketing via IA, envi... | @v4team | 1.0.0 |

## 🤝 Account

<a id="account"></a>

| Skill | O que faz | Autor | v |
|---|---|---|---|
| `account-checkin-review` | Pos-call de check-in. Le o transcript do Gemini Notes (ou texto colado) da call que acabou e atualiza o Mis... | @guilhermelippert | 1.0.0 |
| `account-checkin-roleplay` | Prepara o account pra reunião de check-in com cliente seguindo ROPRE V4 e roda roleplay realista simulando... | @guilhermelippert | 1.0.0 |
| `account-evolucao-checkins` | Relatorio de evolucao entre check-ins. Le o historico de check-ins, combinados e apostas do Mission Control... | @guilhermelippert | 1.0.0 |
| `account-handoff` | Primeira skill que o account roda quando recebe um cliente novo de vendas. Le form de kickoff + transcript... | @guilhermelippert | 1.0.0 |
| `account-pesquisa-profunda-cliente` | Pesquisa profunda de cliente para KB acionavel. PREMISSA OBRIGATORIA - dados do cliente ja na pasta (no min... | @guilhermelippert | 1.5.0 |

## 🔌 Integrações / Fontes

<a id="fontes"></a>

_Skills que puxam dados de integrações externas. Reutilizáveis por outras skills._

## 🔌 V4mos

<a id="v4mos"></a>

| Skill | O que faz | Autor | v |
|---|---|---|---|
| `v4mos-dados-meta-ads` | Puxa qualquer dado de Meta Ads (Facebook + Instagram) via API V4mos pra um cliente especifico. Use sempre q... | @guilhermelippert | 2.0.0 |

---

_Quer contribuir? Roda `/compartilhar-skill`. Mais detalhes em [CONTRIBUTING.md](./CONTRIBUTING.md)._
