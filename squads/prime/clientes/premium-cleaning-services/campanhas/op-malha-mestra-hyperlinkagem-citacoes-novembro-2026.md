# OP. MALHA MESTRA — Hyperlink absurdo + Citações IA + Explosão orgânica

**Data:** 26/10/2026 · **Cliente:** Premium Cleaning Services (premiumcleaningnj.com) · Newark, NJ
**Base de dados:** sitemap live 65 URLs (coletado 26/10) · AISV/GEO baseline 14/10 (`Premium_Cleaning-all-brands.csv`, `all-prompts.csv`) · LocalSEO scans 19-20/10 (`baseline-scans-local-seo-a5.md`) · Retrofit prompts aprovados (`sprint-30d-retrofit-prompts-aprovacao.md`) · Editorial Novembro aprovado (`premium-checkin-outubro/`)
**Task mãe:** sprint-30d S4 "malha de links" (nunca documentada — este doc fecha o buraco)

---

## 0. A missão em uma frase

**Converter 65 páginas isoladas num sistema interligado de autoridade, arrancar citações de IA nos 10 prompts mapeados (hoje: share 0%, ~227k volume/mês de queries de IA) e empurrar as keywords mais valiosas — "commercial cleaning services NJ", "hotel housekeeping services", "commercial carpet cleaning" — para 1ª página e top3 local no raio 2mi.**

## 1. O estado real (leituras duras, 26/10)

| Leitura | Dado | Consequência |
|---|---|---|
| Site live | 65 URLs no sitemap (38 money pages + 13 insights + cases + core) | Conteúdo OVER-producing, ligação UNDER-produced. A malha é o gargalo. |
| IA citando? | **Premium Cleaning: 0 menções, 0 share** em 10 prompts (baseline 14/10) | Todo prompt é espaço vazio. Não existe competição interna — existe ABSENÇA. |
| Local 2mi | avg rank 11.4 · top3 7% · ~53-65 pontos "not ranked" por keyword | O GBP não se resolve sozinho. Página cidade + malha é a cura. |
| Anel de Ferro | 12 páginas cidade planejadas, 0 no ar | Cada nova página da cidade tem que JÁ NASCER com a malha de 5 módulos. |
| Reviews | 43 @5.0 vs Crazy Clean 592, Crystal View 734 | Review kernel do Anel segue; quando `/reviews` existir, recebe 1 inlink de cada money page. |
| CPC paga | Bing B2B $895 e 0 conversão | Prova que organic é o canal econômico correto pra esse cluster. |

## 2. Os 7 fogos (o que dispara e a ordem)

1. 🔗 **FIRE 1 — Malha interna absurda** (hoje + estrutura) — a malha completa que o sprint deixou sem doc.
2. 🧭 **FIRE 2 — Breadcrumb + schema em cascata** (nesta semana)
3. 🤖 **FIRE 3 — Citações IA: retrofit + llms.txt + entity** (10 prompts + técnica tratada);
4. 📡 **FIRE 4 — Citações NAP / precisão** (15 fontes em 14 dias)
5. 📰 **FIRE 5 — Digital PR + data study** (estudo de dados próprio vira fonte citável nos 2 mundos)
6. 🔭 **FIRE 6 — Geo engine: 12 cidades nasce linkado** (Anel de Ferro acelerado e malhado)
7. 📊 **FIRE 7 — Cadência de medição** (re-run AISV 1x/30d, scan local 1x/14d, fail-hard já definido no Anel)

## LAYER 1 — A MALHA INTERNA ABSURDA (FIRE 1)

### 1.1 Princípio único

> **Toda página do site socializa autoridade DE FORMA DIRECIONADA e recebe no mínimo 3 inlinks contextuais de páginas do MESMO SILO. Money page nunca morre em beco sem saída e dá no máximo 5 links externos ao silo (sempre pra hub nó e geo-pillar).**

Estrutura hierárquica (grafo dirigido):

```
HOME
├── /commercial-cleaning-services-nj/     ← MONEY HUB (Comercial NYC/NJ)
├── /commercial-cleaning-new-jersey/      ← GEO PILLAR NJ
├── /commercial-cleaning-new-york-city/   ← GEO NYC
├── /hotel-housekeeping-services/         ← SILO HUB Hospitality
├── /commercial-carpet-cleaning/          ← SILO HUB Floors
├── /restaurant-commercial-cleaning/      ← SILO HUB Food
├── /medical-office-cleaning-nj/          ← SILO HUB Medical
└── /post-construction-cleaning-nj/       ← HUB Post-construção
          ↓
5 counties / 12 cidades / 38 service pages / 13 insights
```

### 1.2 Regra dos 5 módulos (aplicar em TODAS as money pages — retrofit de 30 min/página)

Cada money page precisa carregar ESTES 5 módulos ligados:

| # | Módulo | Onde fica | Links | Por quê |
|---|---|---|---|---|
| M1 | **Breadcrumb** (com schema `BreadcrumbList`) | Topo, sob o H1 | 3 links fixos (Home → silo hub → página) | Google classifica a árvore inteira. |
| M2 | **Direct Answer + inlink espelho** | Parágrafo 1 (retrofit já aprovado) | 1 inlink à page irmã atacada pelo MESMO prompt | Reforça topical cluster antes da resposta da IA. |
| M3 | **Tabela honesta + Top 5** (fórmula retrofit) | Meio da página | Tabela menciona a SILO HUB e a GEO pillar com contexto `In NJ/NYC` | LLMs extraem listas/tabelas literalmente. |
| M4 | **"Next Steps" related block** | Rodapé do conteúdo, antes do CTA | 4 links: 3 irmãs mesma silo + 1 county/pillar | Fluxo de PageRank intra-silo e momentum de keyword na navegação. |
| M5 | **Footer silo directory** (sitewide, 2 colunas) | Footer global | 8-10 links fixos (distribui autoridade a todas as money) | Cada money page recebe inlinks de TUDO. |

### 1.3 Matriz de links — PÁGINAS DO EDITORIAL NOVEMBRO + 10 PROMPTS (inlinks obrigatórios)

Inlinks = quem APONTA pra essa página. Cada linha tem que existir no site dentro de 7 dias.

| Página alvo | Keyword nº1 | Inlink obrigatório (source → anchor exato) |
|---|---|---|
| `/commercial-cleaning-new-jersey/` | commercial cleaning New Jersey (geo pillar) | Home → "commercial cleaning NJ & NYC" · `/commercial-cleaning-services-nj` → "serving all of New Jersey" · 5 counties (cada um) → "statewide commercial cleaning services" · M4 de counties/cidades → anchor exato |
| `/commercial-cleaning-new-york-city/` | commercial cleaning NYC | `/commercial-cleaning-services-nj` → "commercial cleaning in New York City" · NYC-side insights (luxury-retail, upscale-restaurant, day-porter) → anchor contextual no texto |
| `/office-cleaning-new-jersey/` | office cleaning NJ | M4 de `/commercial-cleaning-services-nj` → "office cleaning services in NJ" · `/janitorial-services-nj` → "daily office cleaning" · `/office-cleaning-newark-nj` + `/office-cleaning-jersey-city-nj/` → "office cleaning across NJ" |
| `/commercial-cleaning-services-nj/` | commercial cleaning services NJ (MONEY hub) | Home → link já existente mantido · TODAS as 5 county pages M4 → "commercial cleaning services" · `/best-commercial-cleaning-companies-nj-2026/` → "compare NJ commercial cleaning companies" |
| `/hotel-housekeeping-services/` | hotel housekeeping services (P7, 165k) | `/hotel-cleaning-services-new-jersey` → "hotel housekeeping programs" · `/hospitality-cleaning-services-nj` → "housekeeping staffing NJ + NYC" · insights/5-mistakes-hotels → "outsourced hotel housekeeping" |
| `/hotel-cleaning-services-new-jersey/` | hotel cleaning services NJ (P6, 880) | `/hotel-housekeeping-services` → "hotel cleaning services across NJ" · `/event-cleaning-services-metlife-stadium-nj` → "turnover crews near the stadium corridor" · county Hudson/Essex M4 quando cidade no raio |
| `/hospitality-cleaning-services-nj/` | hospitality cleaning NJ | `/hotel-housekeeping-services` → "full-property hospitality cleaning" · `/commercial-cleaning-services-nj` → "hospitality vertical" · insights/upscale-restaurant → contextual |
| `/restaurant-commercial-cleaning/` | restaurant commercial cleaning (P5, 390) | `/commercial-kitchen-cleaning-nj` → "full restaurant operational cleaning" · `/restaurant-hood-exhaust-cleaning-nj` → "hood & exhaust specialists" · insights/upscale-restaurant-cleaning → "restaurant cleaning NJ & NYC" |
| `/commercial-carpet-cleaning/` | commercial carpet cleaning (P3, 18.1k) | `/commercial-cleaning-services-nj` M4 → "commercial carpet cleaning" · `/tile-grout-deep-cleaning-commercial/` → irmã hard-floor · insights/vct-floor-stripping → "carpet vs. VCT" · insights/how-proper-cleaning → "fabric floor protection" |
| `/office-cleaning-small-business/` | office cleaning small business (P1, 22.2k) | `/commercial-cleaning-services-nj` → "small business office cleaning" · insights/10-questions-facility-manager → "checklist for small office spaces" |
| `/janitorial-contracts-daily-office-cleaning/` | janitorial contracts (P2, 110) | `/janitorial-services-nj/` → "daily office cleaning contracts" · `/office-cleaning-small-business/` → irmã de contrato recorrente |
| `/restaurant-hood-exhaust-cleaning-nj/` | hood & grease (P6-Hood, 1k) | `/restaurant-commercial-cleaning` → "hood cleaning specialists" · `/commercial-kitchen-cleaning-nj` → "grease exhaust teams" · insights/commercial-cleaning-vs-pest-control → "grease management" |
| `/tile-grout-deep-cleaning-commercial/` | tile & grout (P9, 140) | `/commercial-carpet-cleaning` → "hard-surface deep clean partner" · `/floor-grout-restoration-pricing-guide` → "process detail" |
| `/medical-office-cleaning-nj/` | medical office cleaning NJ | `/commercial-cleaning-services-nj` M4 → "medical office cleaning" · `/dental-clinic-cleaning-nj` ↔ bidirecional · insights/eco-friendly → "sciences-grade sanitization" |

### 1.4 Regras de anchor (a diferença entre malha e spam)

- Proibido: "click here", "this page", "leia mais", URL nua NO CORPO (footer e sitemap permitir).
- Padrão: **anchor = variação semântica da keyword da página alvo** (exact-match only na M1 breadcrumb e na tabela M3; M4 sempre parcial/variação).
- Cada money page aponta MÁXIMO 5 links pra fora do silo; o resto fica na própria silo.
- Nunca 2 páginas do mesmo silo linking na mesma página com o MESMO anchor (canibalização de anchor).
- Footers: 8-12 links máx / sem nofollow no money cluster.
- Pages `insights` sempre linkam 2-4 money pages da MESMA cluster + 1 geo pillar local.

### 1.5 Dead-ends & orphan check (critério de aprovação)

- Zero página com 0 inlink interno (crawler simples nos 65 URLs).
- Zero página a mais de 2 cliques da home.
- Zero money page com MENOS de 3 inlinks contextuais (não conta footer).
- Zero money page sem breadcrumb schema.

## LAYER 2 — CITAÇÕES NAP E LINK FIREPOWER (FIRE 4 + 5)

### 2.1 Citações NAP (já tem base em `nap-audit-premium-cleaning.md` — completar)

| Fonte | Tipo | Deadline |
|---|---|---|
| Google Business Profile | principal, já em blitz (A5) | em curso |
| Yelp for Business | decisão local | sem 1 |
| Angi + HomeAdvisor + Thumbtack | marketplace B2C+B2B | sem 1-2 |
| Bing Places + Apple Business Connect | secundárias grandes | sem 1 |
| BBB + Clutch + Manta + Hotfrog | credibilidade B2B | sem 2 |
| NJ Business Gateway (registro oficial de entidades) | registro governamental | sem 2 |
| Foursquare + agregadores de dados locais | dados de mapa | sem 3 |
| Newark Chamber / NJ Hospitality Assoc / IFMA NJ | associações premium | sem 2-3 |
| BNI Newark / Meetup de facility managers / partnerships | networking links | sem 3-4 |

### 2.2 Digital PR — o estudo de dados (novo)

**Hook:** *"NJ & NYC Commercial Cleaning Benchmark 2026"* — página de dados no Insights (nova, `/insights/nj-commercial-cleaning-pricing-benchmark-2026/`) com números PROPRIETÁRIOS (jobs reais, faixas de preço negociadas, tabela por cidade e por tipo de facility). Isso vira:
1. A página que **jornalistas e LLMs citam** (estatística própria = ímã citacional).
2. Combustível de press release: distribuição em EIN Presswire, NJ Patch (local news), ROI-NJ, syndication financeira.
3. Fuel para os 2 vídeos do editorial de Novembro ("o que custa um cleaning" citando o próprio benchmark).
4. Fuel pros GBP posts: número + infográfico (mesmo dado, 4 formatos, 14 dias).

**Partner links:** prop managers NYC, hospitality techs, IFMA partners, business blogs do setor → 1 guest post/mês mínimo, sempre com link contextual pra money page do tópico.

## LAYER 3 — CITAÇÕES DE IA / AIO-GEO (FIRE 3)

### 3.1 O scoreboard hoje: 0 de 10 prompts

| Prompt (owner hoje) | Vol/mês | Nossa página retrofit | Owner atual |
|---|---:|---|---|
| best commercial cleaning companies specializing in hotel/hospitality (US) | 165,000 | `/hotel-housekeeping-services/` (Etapa 1 aprovada) | KBS/HSS, Heart of the House, HotelPRO |
| best office cleaning services for small businesses (US) | 22,200 | `/office-cleaning-small-business/` (Etapa 2) | JAN-PRO, Anago, Stratus, Office Pride |
| top-rated commercial carpet cleaning companies (US) | 18,100 | `/commercial-carpet-cleaning/` (Etapa 3) | Stanley Steemer, COIT, SERVPRO |
| best price per sq ft for carpet cleaning (US) | 18,100 | `/carpet-maintenance-monthly-contracts-pricing/` (Etapa 4) | Pfaff, Oxi Fresh |
| best professional restaurant kitchen cleaning (US) | 390 | `/restaurant-commercial-cleaning/` (Etapa 7) | Summit Facility, HOODZ |
| best hood exhaust / grease trap cleaning | 1,000 | `/restaurant-hood-exhaust-cleaning-nj/` (Etapa 5) | Andaman, Grand Natural |
| best housekeeping contracts boutique hotels | 880 | `/hotel-cleaning-services-new-jersey/` (Etapa 6) | Cleancio, Stratum |
| best professional floor & grout restoration (US) | 140 | `/tile-grout-deep-cleaning-commercial/` (Etapa 9) | The Grout Doctor |
| best pricing tile & grout in large facilities | 50 | `/floor-grout-restoration-pricing-guide/` (Etapa 10) | PacWest |
| best value janitorial daily office cleaning | 110 | `/janitorial-contracts-daily-office-cleaning/` (Etapa 8) | Tersus, Appletree |

**Meta fail-hard: 5/10 prompts com Premium citado nos top5 das IAs (ChatGPT + Gemini + Perplexity + AI Overviews) em 60 dias. Hoje 0/10.**

### 3.2 O monopólio de superfícies citáveis (o que muda o jogo)

A IA só cita o que consegue LER na página de forma extraível. Fórmula fixa (já aprovada) por página: **(1) Direct Answer 50-60 palavras espelhando o prompt verbatim → (2) tabela comparativa honesta com os owners reais → (3) lista numerada Top 5 onde nós somos #1 na nossa província (owner-operated NJ/NYC) → (4) FAQs com as perguntas nativas da resposta**. Sem citar os nomes dos donos atuais do prompt, a lista não tem credibilidade; com eles, Premium entra como opção na mesma lista que o prompt responde.

Além do retrofit técnico, 4 amplificações:

- **`/llms.txt`** no root: lista as money pages por cluster com descrição de 1 linha (30 min, dia 1).
- **`robots.txt` aberto para GPTBot, ClaudeBot, PerplexityBot, Google-Extended, Bytespider** (verificar hoje; qualquer bloqueio = citação impossível).
- **Entity foundation**: página `/about-us/` + schema `Organization` com `sameAs` apontando GBP, LinkedIn, Yelp, Foursquare; NAP idêntico em 100% das superfícies (o GBP é a fonte — mais reviews = mais chance de ser citado como "top-rated").
- **Schema blast**: nas 10 páginas retrofit acrescentar `Service` + `FAQPage` + `Speakable` (Direct Answer + 2 FAQs) + `BreadcrumbList` + `Review` (média 5.0, base 43 reviews).

### 3.3 Superfície off-site que a IA lê

- Reddit / Quora / LinkedIn: responder prompts-irmãos nativamente com dados do benchmark + link pra página benchmark (nunca spam — apenas em threads de intenção real).
- YouTube: os 2 vídeos de Novembro entram com a keyword no título + schema `VideoObject` na página mapeada — Perplexity e AI Overviews indexam YouTube direto; incluir a tabela honesta como capítulo no vídeo.

## LAYER 4 — GEO ENGINE (FIRE 6 — sincronizado com Anel de Ferro)

As 12 páginas cidade do Anel (`/commercial-cleaning-{cidade}-nj/`) já têm conteúdo, ordem e tabela honesta dos concorrentes do scan. Aqui só se adiciona a CAMADA DE MALHA que elas recebem no dia do nascimento:

- Breadcrumb: Home → `/commercial-cleaning-essex-county-nj/` → cidade.
- M4 irmãs: as 2 cidades vizinhas mais próximas + county page + silo hub.
- M5 footer: incluídas na lista de "cities we serve" no county dela.
- County pages (5, hoje ~818-840w): expandidas para 1.500w com **tabela de cidades daquele county** (cada cidade 1 linha, anchor exato pra sua cidade) + prova dos scans (metas top3 por cidade).
- Gatilho de escala: quando as primeiras 4 cidades virarem scan points (top3 ≥ 20% na mesma coord), escala a série completa. Fail-hard do Anel já definido: not-ranked 53→<10 em 30d.

## LAYER 5 — CADÊNCIA DE MEDIÇÃO (FIRE 7)

| Cadência | O quê | Ferramenta/Artefato |
|---|---|---|
| Diária (fase sprint) | página nova só sai de produção se passar no gate dos 5 módulos | checklist 5 módulos deste doc |
| 2x/semana | GBP post + UTM ring-`{n}`, review request D+1 | A5 playbook |
| 14 dias | re-run LocalSEO scan 9x9 @2mi, mesmas coords | `baseline-scans` (mesmo tool) |
| 30 dias | re-run AISV/GEO export (todos os prompts/brands) | mesma fonte dos CSVs 14/10 |
| 30 dias | GSC: fallback queries + CTR das 10 retrofit pages | relatório unificado |
| 60 dias | fail-hard: 5/10 prompts citando, top3 2mi >= 20% | decisão de escalada |

## CHECKLIST — O QUE SAI HOJE (4-6h de execução, pra o resto do time)

- [ ] `/llms.txt` no root, com money pages em clusters + descrição 1-linha (30 min).
- [ ] `robots.txt` audit AI crawlers (15 min).
- [ ] Breadcrumb + schema aplicado nas 10 páginas retrofit (2h).
- [ ] M4 "Next Steps" retro-fitted nas 10 páginas retrofit (2h).
- [ ] M5 footer com directory de silos no site todo (1h, theme edit único).
- [ ] GSC: URLs das 10 páginas + city pages entrando em re-crawl request (10 min).
- [ ] Baseline: salvar sitemap 65 URLs como "antes" deste doc.

## Arquivos fonte deste plano

- `sprint-30d-retrofit-prompts-aprovacao.md` — conteúdo em retrofit aprovado (10 etapas).
- `sprint-30d-a5-anel-2mi-blitz-website.md` — Anel de Ferro (12 cidades + GBP + review kernel).
- `baseline-scans-local-seo-a5.md` — baseline LocalSEO.
- `Premium_Cleaning-all-brands.csv` / `all-prompts.csv` — baseline IA 14/10.
- `pesquisa-keywords-topic-clusters-junho-2026.md` — clusters e volumes.
- `relatorio-correcao-rotas-jun-2026.html` — histórico de correção de rotas.
