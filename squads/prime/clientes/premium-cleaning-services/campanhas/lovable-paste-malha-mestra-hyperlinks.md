# COLAR NO LOVABLE — OP. MALHA MESTRA (hyperlink absoluto + citações IA)

> Plano-fonte (PT-BR, estratégico): `op-malha-mestra-hyperlinkagem-citacoes-novembro-2026.md`. Este pack traduz os 7 fogos em prompts L1–L6 executáveis, mesma disciplina dos prompts P8/P-1: **gate de plano em 5 bullets, patch-only, confirmação por file:count, zero code dump**.
> **Como usar:** rode em ordem, um por vez, AGUARDE o OK do plano de cada prompt antes de liberar a próxima fase. Prompts dentro dos blocos são EN; instruções fora dos blocos são PT-BR pra você.
> **Off-site (não é Lovable):** seção final — NAP, PR data study, Reddit/Quora, 12 cidades do Anel.

---

## BLOCO DE CRÉDITO (colado no topo de CADA prompt — não remover)

```
CREDIT RULES (binding): 1) First reply with a 5-bullet build plan and WAIT for my OK — do not generate code yet. 2) When fixing, edit ONLY files I name; never regenerate unaffected files. 3) Never reprint pasted copy; confirm with file paths + per-page checklist. 4) Same error twice → STOP, report file:line, and ask. 5) No new libraries, no redesign, US English, no emojis in UI. 6) All structured data is static in the served HTML (no client-side-only injection) — prove with build grep when asked.
```

**Dados reais (verbatim, nunca inventar):** (973) 204-2310 · `tel:+19732042310` · office@premiumccs.com · Bergen/Essex/Passaic/Hudson/Union + NYC · Since 2012 · 98% retention · Bonded & insured · `https://premiumcleaningnj.com/`
**GBP:** ★5.0 · 43 reviews · `https://share.google/hcOVKM1ylv4QmeH0I`

---

## PROMPT L1 — INFRA DA MALHA: RelatedBlock + Breadcrumbs + Footer directory (1 geração grande)

```
[BLOCO DE CRÉDITO]

In the existing Premium Cleaning NJ website project, add ONLY the three internal-linking infrastructure components. No copy changes on existing pages yet. No redesign.

1) Breadcrumbs on ALL content pages (the pages listed in src routes that are service, city, county, insight or case pages — NOT homepage, NOT utility pages). Requirements: a visible trail component under the H1: Home › [Hub name] › [Page name], where the middle crumb is the page's sidebar hub defined in step 4. Render matching static JSON-LD BreadcrumbList in each page's head (same head manager already used for page meta). Middle crumb must link to the hub URL.

2) Create src/components/RelatedBlock.tsx (or framework equivalent): a "Next steps" content module rendered ABOVE the final CTA on all money pages. Props: links = { label, href }[] (max 4). Visual: match existing design system (heading + single-column styled link list). It is server-rendered/static so links are crawlable in served HTML.

3) Footer "Cities & services we serve" directory: extend the existing site footer with ONE static block containing these hard links (2 columns OK):
   - Services: /commercial-cleaning-services-nj · /hotel-housekeeping-services · /commercial-carpet-cleaning · /restaurant-commercial-cleaning · /medical-office-cleaning-nj · /post-construction-cleaning-nj · /office-cleaning-small-business
   - Regions: /commercial-cleaning-new-jersey · /commercial-cleaning-new-york-city · /commercial-cleaning-bergen-county-nj · /commercial-cleaning-essex-county-nj · /commercial-cleaning-passaic-county-nj · /commercial-cleaning-hudson-county-nj · /commercial-cleaning-union-county-nj
   Anchor = the existing page H1/H2 naming (derive from route slug, Title Case). Do NOT add nofollow. Do NOT change footer legal links.

4) Create src/data/hubs.ts mapping every route slug → { hubName, hubHref, category } where category ∈ {hotel, office, floors, restaurant, medical, geo, insights, cases}. Use: hotel hub /hotel-housekeeping-services · office hub /commercial-cleaning-services-nj · floors hub /commercial-carpet-cleaning · restaurant hub /restaurant-commercial-cleaning · medical hub /medical-office-cleaning-nj · geo hub /commercial-cleaning-new-jersey (NJ pages) or /commercial-cleaning-new-york-city (NYC pages) · insights/cases → nearest topical hub list above. This file is the single source of truth used by breadcrumbs in step 1 and will be consumed by RelatedBlock defaults later.

Acceptance: build passes; grep proves BreadcrumbList JSON-LD present in served HTML for all content pages (report count — expect 60+ pages); RelatedBlock imported but empty-linked (no visual regression, report which pages render it); footer contains the 14 hard links above; no other files touched.
```

---

## PROMPT L2 — A MATRIZ DE INLINKS (patch-only, 1 geração grande)

> É aqui que a hyperligação entra no corpo das páginas. Antes de rodar: conferir no build atual que cada URL alvo existe (todas estão no sitemap live de 26/10).

```
[BLOCO DE CRÉDITO]

Apply the internal linking matrix below. Rules: insert each contextual link ONCE per source page, inline where semantically natural (never in nav/footer/breadcrumb), anchor EXACTLY as given, href EXACTLY as given, no redirects, do not remove existing links, do not rewrite surrounding copy beyond the minimal sentence touched.

/commercial-cleaning-new-jersey/ — RECEIVES:
  - From Home page services section: anchor "commercial cleaning NJ & NYC"
  - From /commercial-cleaning-services-nj/ body: anchor "serving all of New Jersey"
  - From EACH county page (bergen, essex, passaic, hudson, union): anchor "statewide commercial cleaning services"
/commercial-cleaning-new-york-city/ — RECEIVES:
  - From /commercial-cleaning-services-nj/ body: anchor "commercial cleaning in New York City"
  - From insights luxury-retail + upscale-restaurant + day-porter: 1 contextual anchor each mentioning "commercial cleaning NYC"
/office-cleaning-new-jersey/ — RECEIVES:
  - From /commercial-cleaning-services-nj/: anchor "office cleaning services in NJ"
  - From /janitorial-services-nj/: anchor "daily office cleaning"
  - From /office-cleaning-newark-nj/ and /office-cleaning-jersey-city-nj/: anchor "office cleaning across NJ"
/commercial-cleaning-services-nj/ — RECEIVES:
  - Each county page: anchor "commercial cleaning services"
  - /best-commercial-cleaning-companies-nj-2026/: anchor "compare NJ commercial cleaning companies"
/hotel-housekeeping-services/ — RECEIVES:
  - From /hotel-cleaning-services-new-jersey/: anchor "hotel housekeeping programs"
  - From /hospitality-cleaning-services-nj/: anchor "housekeeping staffing NJ + NYC"
  - From insights 5-mistakes-hotels: anchor "outsourced hotel housekeeping"
/hotel-cleaning-services-new-jersey/ — RECEIVES:
  - From /hotel-housekeeping-services/: anchor "hotel cleaning services across NJ"
  - From /event-cleaning-services-metlife-stadium-nj/: anchor "turnover crews near the stadium corridor"
/hospitality-cleaning-services-nj/ — RECEIVES:
  - From /hotel-housekeeping-services/: anchor "full-property hospitality cleaning"
  - From /commercial-cleaning-services-nj/: anchor "hospitality vertical"
  - From insights upscale-restaurant: 1 contextual anchor mentioning "hospitality cleaning in NJ"
/restaurant-commercial-cleaning/ — RECEIVES:
  - From /commercial-kitchen-cleaning-nj/: anchor "full restaurant operational cleaning"
  - From /restaurant-hood-exhaust-cleaning-nj/: anchor "hood & exhaust specialists"
  - From insights upscale-restaurant-cleaning: anchor "restaurant cleaning NJ & NYC"
/commercial-carpet-cleaning/ — RECEIVES:
  - From /commercial-cleaning-services-nj/: anchor "commercial carpet cleaning"
  - From /tile-grout-deep-cleaning-commercial/: contextual anchor mentioning "hard-surface deep cleaning"
  - From insights vct-floor-stripping: anchor "carpet vs. VCT"
  - From insights how-proper-cleaning-protects-luxury-flooring: anchor "fabric and floor protection"
/office-cleaning-small-business/ — RECEIVES:
  - From /commercial-cleaning-services-nj/: anchor "small business office cleaning"
  - From insights 10-questions-facility-manager: anchor "checklist for small office spaces"
/janitorial-contracts-daily-office-cleaning/ — RECEIVES:
  - From /janitorial-services-nj/: anchor "daily office cleaning contracts"
  - From /office-cleaning-small-business/: anchor "recurring janitorial service"
/restaurant-hood-exhaust-cleaning-nj/ — RECEIVES:
  - From /restaurant-commercial-cleaning/: anchor "hood cleaning specialists"
  - From /commercial-kitchen-cleaning-nj/: anchor "grease exhaust teams"
  - From insights commercial-cleaning-vs-pest-control: anchor "grease management"
/tile-grout-deep-cleaning-commercial/ — RECEIVES:
  - From /commercial-carpet-cleaning/: anchor "hard-surface deep clean partner"
  - From /floor-grout-restoration-pricing-guide/: anchor "process detail"
/medical-office-cleaning-nj/ — RECEIVES:
  - From /commercial-cleaning-services-nj/: anchor "medical office cleaning"
  - From /dental-clinic-cleaning-nj/: bidirectional (this row establishes both directions with 1 anchor each)
  - From insights eco-friendly-commercial-cleaning: anchor "clinical-grade sanitization"
ALSO: RelatedBlock defaults per silo — hotel pages get RelatedBlock links to [hotel-cleaning-services-new-jersey, hospitality-cleaning-services-nj, hotel-housekeeping-cost-pricing-guide-2026, commercial-cleaning-new-jersey]; office pages to [office-cleaning-new-jersey, office-cleaning-small-business, janitorial-services-nj, commercial-cleaning-new-jersey]; floors pages to [commercial-carpet-cleaning-high-traffic, carpet-maintenance-monthly-contracts-pricing, tile-grout-deep-cleaning-commercial, commercial-cleaning-new-jersey]; restaurant pages to [commercial-kitchen-cleaning-nj, restaurant-hood-exhaust-cleaning-nj, overnight-restaurant-cleaning, restaurant-grease-trap-cleaning-nj]; medical pages to [medical-office-cleaning-nj, hospital-janitorial-services-nj, dental-clinic-cleaning-nj, office-cleaning-new-jersey].

Acceptance: report per-target inlink count list (target URL = count) proving every line above exists in served HTML; zero duplicate anchors targeting the same URL from pages in the same silo; grep proof given as summary counts, no code dumps.
```

---

## PROMPT L3 — CITÁVEL PELA IA: llms.txt + robots.txt + sitemap refresh (1 geração média)

```
[BLOCO DE CRÉDITO]

1) Create /public/llms.txt with this exact structure (plain text, no emojis):
   # Premium Cleaning Services — Newark NJ & NYC commercial cleaning
   > Owner-operated commercial cleaning company since 2012. Bergen, Essex, Passaic, Hudson, Union counties + NYC. Star-rated GBP (5.0, 43+ reviews). Services include hotel housekeeping (126 rooms/day at Marriott standards), office & janitorial contracts, restaurant & kitchen overnight crews, carpet/tile care, medical office and post-construction cleaning. Phone (973) 204-2310. Email office@premiumccs.com.
   Then one bullet per silo, listing cluster URLs with 4-8 word descriptions: Hotel & hospitality, Offices & janitorial, Floors (carpet/tile), Restaurants & kitchens, Medical, Post-construction, Regions (county pages), Pricing guides, Insights.
   Description lines state facts verbatim from site data above — do not invent numbers.

2) Audit /public/robots.txt: ENSURE it allows GPTBot, ClaudeBot, PerplexityBot, Google-Extended, Bytespider, CCBot (if currently blocked anywhere, unblock), and keeps sitemap.xml reference. If no robots.txt exists, create with: User-agent: * Allow: / + explicit Allow blocks for the five AI crawlers above + Sitemap line.

3) Regenerate /public/sitemap.xml from current React routes (every indexable route, lastmod = today, no utility/noindex pages). Report final URL count.

Acceptance: llms.txt + robots.txt + sitemap.xml in served static files; report grep counts (AI crawler allow blocks = 5 named agents, sitemap URL total); nothing else changed.
```

---

## PROMPT L4 — ENTITY: About page + Organization schema + Review rail (1 geração média)

```
[BLOCO DE CRÉDITO]

1) Create /about-us/ page (existing design system, ~500 words US English): who we are (owner-operated, since 2012, Newark NJ HQ at 107 Vesey St area — do not print address beyond what Google GBP shows publicly in site footer if already present), what we operate (daily crews NJ + NYC, hospitality Marriott standards, office janitorial, restaurant, medical, post-construction), standards (bonded & insured, 98% retention, written checklists, supervisor inspections), proof rail (3 case cards reusing existing CaseRef data from src/data/proof.ts), CTA = existing site CTA with phone (973) 204-2310.
2) Add static Organization JSON-LD sitewide (in the root layout head): @type Organization + LocalBusiness (CommercialCleaning), name "Premium Cleaning Services", url, telephone "+19732042310", email, areaServed = the 6 areas, foundingDate "2012", aggregateRating ratingValue 5.0 reviewCount 43, sameAs: [GBP profile https://share.google/hcOVKM1ylv4QmeH0I, existing LinkedIn/Yelp/Facebook/Instagram URLs if present in footer — else omit silently and report which were found].
3) Add a one-line review rail component above the final CTA on the 10 pricing/hub pages (any 5 of the verbatim reviews from the approved review data: rating 5, service type, quote sentence only, linked text "Verified on Google" → GBP URL). Max one rail line per page.

Acceptance: about route + schema in served HTML (grep count for Nearby: "sameAs" = ≥1 sitewide node), review rail grep count = 10 pages, sitemap includes /about-us/, nothing else modified.
```

---

## PROMPT L5 — QA DA MALHA (report-only, barato)

```
[BLOCO DE CRÉDITO]

Do NOT change any code. Run link-graph QA and REPORT ONLY:
1) Orphan check: any indexed page with 0 internal inlinks → list URL.
2) Depth check: any indexed page more than 2 clicks from Home via internal links → list URL + path.
3) Duplicate anchor check: same anchor text targeting same URL from 2+ pages in the same silo → list.
4) Dead link check: any internal link returning build-404 or pointing to a route that does not exist → list.
5) Schema check: pages missing BreadcrumbList or Organization node → list.
6) Footer + llms.txt + sitemap totals vs Prompts L1-L4 acceptance numbers.
Output = 6 numbered lists only. If a list is empty, write "PASS".
```

---

## OFF-SITE (NÃO É LOVABLE) — dono: time SEO/cliente

### A) NAP / citações externas (pra quem faz)
- [ ] Yelp, Angi, HomeAdvisor, Thumbtack, Bing Places, Apple Business Connect — NAP idêntico (mesma fonte do GBP). Deadline: 14 dias.
- [ ] BBB, Clutch, Manta, Hotfrog, NJ Business Gateway, Foursquare — sem 2.
- [ ] Newark Chamber, IFMA NJ, associações hospitality — sem 2-3.

### B) Data study "NJ & NYC Commercial Cleaning Benchmark 2026"
- [ ] Coletar números REAIS com o cliente (jobs, faixas de preço negociadas, por tipo de facility) — sem dado gerado.
- [ ] Página `/insights/nj-commercial-cleaning-pricing-benchmark-2026/` (paste próprio quando dados chegarem).
- [ ] Press release (EIN Presswire / NJ Patch / ROI-NJ) citando o benchmark + link pra pilar.

### C) Reddit / Quora / LinkedIn
- Mesmas regras do P8 Parte C: resposta útil, disclosure no perfil, nunca spam nas 2 primeiras interações.

### D) Anel de Ferro — 12 páginas cidade
- Quando aprovadas, gerar paste próprio seguindo 5 módulos (breadcrumb → county, RelatedBlock com 2 cidades vizinhas + county + hub, footer "cities we serve" do condado). Base: `sprint-30d-a5-anel-2mi-blitz-website.md`.

### E) Medição
- [ ] Re-run AISV/GEO em 30d (mesma ferramenta dos CSVs de 14/10) — meta: ≥5/10 prompts citando Premium.
- [ ] Re-run LocalSEO scan 9x9 @2mi em 14d — meta: not-ranked 53→<10.
- [ ] Crawler de orfandade/depth = Prompt L5 no ar a cada deploy relevante.

---

**Fontes:** `op-malha-mestra-hyperlinkagem-citacoes-novembro-2026.md` (plano) · `sprint-30d-retrofit-prompts-aprovacao.md` (10 etapas) · `sprint-30d-reviews-lovable.md` (reviews verbatim) · sitemap live 65 URLs 26/10.
