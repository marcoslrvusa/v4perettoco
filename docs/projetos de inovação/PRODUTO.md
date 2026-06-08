# Atlas — Plataforma de Inteligência de Marketing

> Produto único da V4 Company construído sobre open-source.
> De 45 projetos a um ecossistema coeso.

---

## 1. Visão do Produto

**Atlas** é uma plataforma white-label de inteligência de marketing que unifica analytics, SEO/GEO, CRM, social media, email marketing, landing pages e inteligência competitiva em um único ecossistema — tudo auto-hospedado, com dados do cliente, sem custos por usuário ou vendor lock-in.

### Problema que resolve

Clientes de assessoria de marketing usam 8-15 ferramentas diferentes (RD Station, SEMRush, Mailchimp, Buffer, Hotjar, etc.) pagando R$ 3-15k/mês em assinaturas separadas, sem integração entre elas. Atlas substitui tudo por uma plataforma única, integrada e com custo previsível.

### Público-alvo

- Agências de marketing que querem oferecer dados aos clientes sem repassar custo de ferramentas
- Médias empresas que querem centralizar marketing sem departamento de martech dedicado
- E-commerces que precisam de visão unificada de performance

---

## 2. Arquitetura do Produto

```
┌─────────────────────────────────────────────────────────────┐
│                     ATLAS PLATFORM                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   ORQUESTRA  │  │   NÚCLEO    │  │  INTELIGÊNCIA│        │
│  │  (n8n + dbt) │  │  (Superset) │  │  (OpenCMO)   │        │
│  └──────┬───────┘  └──────┬──────┘  └──────┬──────┘        │
│         │                 │                 │               │
│  ┌──────┴─────────────────┴─────────────────┴──────┐       │
│  │               PAINEL UNIFICADO                   │       │
│  │  (Grafana + Metabase embutido)                   │       │
│  └──────────────────────┬──────────────────────────┘       │
│                         │                                   │
│  ┌──────────────────────┴──────────────────────────┐       │
│  │              MÓDULOS DO PRODUTO                  │       │
│  │                                                  │       │
│  │  ┌──────────┐ ┌────────┐ ┌────────┐ ┌────────┐ │       │
│  │  │ ANÁLISE  │ │  SEO   │ │  CRM   │ │ SOCIAL │ │       │
│  │  │e BI      │ │ GEO    │ │e VENDAS│ │ MEDIA  │ │       │
│  │  └──────────┘ └────────┘ └────────┘ └────────┘ │       │
│  │                                                  │       │
│  │  ┌──────────┐ ┌────────┐ ┌────────┐ ┌────────┐ │       │
│  │  │  EMAIL   │ │ LANDING│ │COMPETI-│ │CHATBOT │ │       │
│  │  │MARKETING │ │ PAGES  │ │DORES   │ │e AI    │ │       │
│  │  └──────────┘ └────────┘ └────────┘ └────────┘ │       │
│  └──────────────────────────────────────────────────┘       │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           CAMADA DE INTEGRAÇÃO                        │   │
│  │  Meta Ads | Google Ads | GA4 | Shopify | HubSpot      │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Módulos do Produto

### Módulo 1: Análise e BI (Core)
**Projetos-base:** Superset + Metabase + Lightdash + DuckDB

| Funcionalidade | O que entrega | Projeto Origem |
|---|---|---|
| Dashboard unificado de marketing | Métricas de todas as plataformas em um lugar | Superset + Metabase |
| SQL Lab para análises avançadas | Analistas fazem queries sob demanda | Superset |
| Alertas inteligentes | "Gasto do Meta Ads subiu 30% sem aumento de ROAS" | Grafana |
| Semantic layer para métricas | KPIs consistentes entre times (receita, CAC, ROAS) | Lightdash + dbt |
| Data warehouse leve | Processamento local sem infraestrutura cara | DuckDB |

### Módulo 2: SEO e AI Visibility
**Projetos-base:** GEO SEO Claude + OpenCMO + SEO Autopilot + FreeCrawl

| Funcionalidade | O que entrega | Projeto Origem |
|---|---|---|
| AI Visibility Score | Nota 0-100 de visibilidade em IAs | GEO SEO Claude |
| Monitoria semanal de GEO | Relatório de presença em ChatGPT, Gemini, Perplexity | OpenCMO |
| Auditoria técnica SEO | Crawl completo com 80+ checks | SEO Autopilot + FreeCrawl |
| Geração de schema markup | JSON-LD automático para rich snippets | Akii Plugin |
| llms.txt automático | Otimização para AI crawlers | SEO Autopilot |
| Cluster de palavras-chave | Agrupamento por intenção de busca | SEO Agency in a Box |

### Módulo 3: CRM e Automação de Vendas
**Projetos-base:** Signal + WuKong AI CRM + OpenCRM

| Funcionalidade | O que entrega | Projeto Origem |
|---|---|---|
| Captura de leads multicanal | Meta Lead Ads + Site + CRM unificado | OpenCRM + Signal |
| Enriquecimento automático | Dados de LinkedIn, GitHub e empresa | Signal |
| Scoring de leads com IA | Priorização por ICP | Signal + NexusAI |
| Sequências de email automáticas | Drip campaigns segmentadas | Signal |
| Kanban de pipeline | Visual do funil de vendas | OpenCRM |
| Assistente CRM com RAG | "Qual a previsão de receita esse mês?" | WuKong AI CRM |

### Módulo 4: Social Media
**Projetos-base:** BrightBean Studio + SocialFlow + ZernFlow

| Funcionalidade | O que entrega | Projeto Origem |
|---|---|---|
| Agendamento multiplataforma | Publique em 10+ redes de uma vez | BrightBean Studio |
| AI content pipeline | Scout → Planner → Creator → Publisher | SocialFlow |
| Chatbot multicanal | Atendimento automático em Instagram, WhatsApp, Telegram | ZernFlow |
| Unified inbox | Todas as mensagens num lugar só | BrightBean Studio |
| Analytics de engajamento | Métricas por post, por rede, por período | BrightBean Studio |

### Módulo 5: Email Marketing
**Projetos-base:** Opensend + OpenMail + Senlo + CadenceRelay

| Funcionalidade | O que entrega | Projeto Origem |
|---|---|---|
| Campanhas broadcast | Newsletter, promoções, comunicados | Opensend |
| Email transactional | Recibo, confirmação, recovery | Opensend |
| Automação de lifecycle | Boas-vindas, nutrição, reativação | OpenMail (alternativa Customer.io) |
| Editor drag-and-drop | Templates visuais sem código | Senlo |
| Envio em massa com throttling | 100k+ emails sem cair em spam | CadenceRelay |
| Tracking de abertura/clique | Métricas por campanha | Opensend + CadenceRelay |

### Módulo 6: Landing Pages e Testes
**Projetos-base:** OpenPage + Landing Page Factory + VariantLab + Shippage

| Funcionalidade | O que entrega | Projeto Origem |
|---|---|---|
| Criador de LP visual | Drag-and-drop, 19 blocos, 42 variantes | OpenPage |
| Geração por AI | "Crie uma LP para curso de marketing digital" | OpenPage + Shippage |
| A/B testing nativo | Até 4 variantes por página | PageForge + VariantLab |
| Copy de conversão automática | Headlines, CTAs baseados em dados | Shippage + Landing Page Factory |
| Exit-intent popups | Recuperação de visitantes | Shippage |
| Consentimento LGPD/GDPR | Banner de cookies + preferências | Shippage |

### Módulo 7: Inteligência Competitiva
**Projetos-base:** Rival + CompetitorScope + Drift + Tech Analyst

| Funcionalidade | O que entrega | Projeto Origem |
|---|---|---|
| Monitoria semanal de concorrentes | Pricing, changelog, hiring, blog | Drift |
| Perfil detalhado de concorrentes | Features, pricing, posicionamento | CompetitorScope |
| Magic Quadrant automático | Visual Gartner-style do mercado | Tech Analyst |
| Alertas de mudança | "Concorrente X mudou precificação" | Rival |
| Deep research com citações | Pesquisa profunda com fontes | Rival |

### Módulo 8: Agente de Marketing Autônomo (Premium)
**Projetos-base:** OpenSoul + Garnet AI + MiCA + Mureo

| Funcionalidade | O que entrega | Projeto Origem |
|---|---|---|
| Time de 6 especialistas AI | Director, Strategist, Creative, Producer, Growth, Analyst | OpenSoul |
| Diagnóstico automático de mídia | "Campanha X está com CPA alto por quê?" | Mureo |
| Geração de campanha completa | Brief → roteiro → criativo → legenda → compliance → publish | MiCA + Marketing Engine |
| Aprendizado contínuo | Fica mais inteligente com feedback do cliente | Garnet AI |
| Operação autônoma de ads | Pausa campanha com baixo ROAS, sugere realocação | Mureo |

---

## 4. Planos e Precificação

### Atlas Core — R$ 2.500/mês
- Módulos 1-3 (BI + SEO + CRM básico)
- Até 3 usuários
- 1 domínio/empresa
- Dashboard unificado
- Suporte por email

### Atlas Pro — R$ 5.900/mês
- Módulos 1-6 (todos exceto Agente Autônomo)
- Até 10 usuários
- Até 3 domínios/marcas
- A/B testing
- Email marketing com 50k envios/mês
- Suporte prioritário

### Atlas Enterprise — R$ 12.900/mês
- Todos os 8 módulos
- Usuários ilimitados
- Domínios ilimitados
- Agente de Marketing Autônomo 24/7
- Email marketing ilimitado
- Ambiente dedicado (cluster próprio)
- Suporte 24h + Customer Success dedicado
- SLA 99.5%

### Atlas White-Label (para agências) — R$ 19.900/mês
- Plataforma completa com marca da agência
- Multi-tenant (gerencie todos os clientes num painel)
- Até 50 clientes
- Customizações de branding
- API completa para integrações
- Treinamento da equipe

> **Margem estimada:** Custo de infraestrutura (VPS + APIs) ~R$ 300-800/mês para Core/Pro. Hospedagem white-label ~R$ 2-5k/mês.

---

## 5. Stack Técnica Unificada

```
Camada                    Tecnologia              Projeto Origem
────────────────────────────────────────────────────────────────
Orquestrador              Docker Compose + K8s    —
Gateway API               KrakenD / Nginx         nowCRM
Auth unificado            Better Auth / Keycloak  —
Frontend                 Grafana + React + Vue    Superset/Metabase/Grafana
BI Engine                Apache Superset 6.x      Superset
Dashboards em tempo real Grafana + Prometheus     Grafana
Database principal       PostgreSQL 16            —
Cache + filas            Redis + BullMQ           Opensend/OpenMail
Data warehouse           DuckDB / ClickHouse      DuckDB
ETL/Orquestração         n8n + dbt Core           n8n
AI/LLM provider          BYOK (Claude, Gemini)    —
SEO crawler              FreeCrawl / SEO Autopilot FreeCrawl
Email engine             Opensend + AWS SES       Opensend
Social publishing        BrightBean API           BrightBean Studio
Chatbot engine           ZernFlow flow builder    ZernFlow
Landing pages            OpenPage JSON engine     OpenPage
A/B testing              VariantLab core          VariantLab
MCP servers              n8n + custom MCP         —
```

---

## 6. Roadmap de Desenvolvimento

### Fase 1 — Fundação (Semanas 1-4) — R$ 15k investimento
- [ ] Deploy do Superset + Metabase + Grafana em Docker Compose
- [ ] Integração Meta Ads + Google Ads + GA4 via n8n
- [ ] Dashboard unificado "Visão 360 do Marketing"
- [ ] Autenticação multi-tenant
- [ ] Tests com 1 cliente real (gratuito)

### Fase 2 — Módulos Core (Semanas 5-8) — R$ 25k investimento
- [ ] Módulo SEO/GEO (OpenCMO + GEO Claude + SEO Autopilot)
- [ ] Módulo CRM (Signal + OpenCRM + Meta Lead Ads)
- [ ] Módulo Email (Opensend + OpenMail)
- [ ] Painel de controle do cliente (self-service)
- [ ] 2 clientes pagantes (Core)

### Fase 3 — Expansão (Semanas 9-16) — R$ 35k investimento
- [ ] Módulo Social Media (BrightBean + SocialFlow)
- [ ] Módulo Landing Pages (OpenPage + VariantLab)
- [ ] Módulo Competitivo (Rival + Drift)
- [ ] Chatbot multicanal (ZernFlow)
- [ ] 5 clientes pagantes
- [ ] Precificação validada

### Fase 4 — AI Autônomo (Semanas 17-24) — R$ 40k investimento
- [ ] Agente de Marketing (OpenSoul + Garnet AI)
- [ ] Automação de campanhas (MiCA + Mureo)
- [ ] Diagnóstico automático de mídia paga
- [ ] Relatórios executivos semanais com AI
- [ ] 10+ clientes pagantes
- [ ] Produto white-label para agências

### Fase 5 — Escala (Meses 6-12)
- [ ] Marketplace de integrações
- [ ] API pública
- [ ] Programa de parcerias
- [ ] 50+ clientes
- [ ] ARR > R$ 1M

---

## 7. Diferenciais Competitivos

| Critério | RD Station | SEMRush | Atlas (V4) |
|---|---|---|---|
| BI/Analytics | ❌ Não tem | ❌ Não tem | ✅ Superset nativo |
| AI Visibility/GEO | ❌ | Parcial | ✅ Completo (5 engines) |
| CRM integrado | Parcial | ❌ | ✅ Signal + OpenCRM |
| Social Media | ❌ | ❌ | ✅ BrightBean Studio |
| Email Marketing | ✅ (limitado) | ❌ | ✅ Opensend + OpenMail |
| Landing Pages | ✅ (limitado) | ❌ | ✅ OpenPage + VariantLab |
| Inteligência Competitiva | ❌ | ✅ (caro) | ✅ Rival + Drift |
| Agente AI Autônomo | ❌ | ❌ | ✅ OpenSoul + Garnet |
| Preço | R$ 3-15k/mês | $200-800/mês | R$ 2.5-13k/mês |
| Dados do cliente | Servidor deles | Servidor deles | 100% self-hosted |
| White-label | ❌ | ❌ | ✅ Incluso no plano Enterprise |

---

## 8. Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| Projeto open-source abandonar | Média | Alto | Escolher projetos com comunidade ativa (Superset, n8n). Ter fallback planejado. |
| Licença AGPL restringir uso comercial | Média | Alto | Usar AGPL como serviço interno (não distribuir). Ou escolher alternativas MIT/Apache. |
| Complexidade de integração | Alta | Médio | Investir em Fase 1 robusta. Documentar tudo. n8n como cola entre módulos. |
| Cliente não adotar | Média | Alto | Validar com cliente real na Fase 1. Iterar rápido. |
| Custo de infraestrutura escalar | Média | Médio | Cada cliente no próprio VPS (isolamento). Custo linear. |

---

## 9. Estratégia de Vendas

### Quem vende
- Account V4 (já tem relação com cliente)
- Apresentação: "Vamos substituir 5 ferramentas por uma plataforma única, com dados melhores e custo menor."

### Argumento principal
> "Hoje você paga R$ 8.500/mês em RD Station + SEMRush + Mailchimp + Buffer + Hotjar. Com Atlas, você tem tudo isso por R$ 5.900/mês, integrado, com seus dados na sua nuvem, e com um agente de IA trabalhando 24/7 para você."

### Prova de conceito
- 30 dias grátis com onboarding completo
- Relatório "antes vs depois" no final do período
- Se não gostar, fica com o dashboard de BI de presente (Superset roda mesmo sem plano)

---

## 10. Próximas Ações Imediatas

1. **Escolher 3 projetos** para começar a POC (recomendação: Superset + Opensend + BrightBean Studio)
2. **Fazer deploy de referência** com Docker Compose unificado
3. **Conectar dados reais** de 1 cliente (Meta Ads + Google Ads)
4. **Apresentar preview** ao cliente como "novo painel V4"
5. **Coletar feedback** e iterar
6. **Formalizar produto** com naming, precificação e contrato

---

> **Documento criado em:** 26/05/2026
> **Autor:** OpenCode + V4 Company
> **Status:** Rascunho estratégico — validar com cliente antes de desenvolver
