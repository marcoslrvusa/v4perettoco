# MANUAL LOVABLE — build das 37 páginas + infra SEO/AIO/GEO (perfeito e econômico)

**Site:** https://premiumcleaningnj.com/ (React SPA no Lovable, já no ar) · **Copy final:** `sprint-30d-conteudo-master.md` (37 páginas EN aprovadas) · **Personas:** `sprint-30d-personas-blocos-colar.md` (briefing interno — NUNCA publica) · **Reviews:** `sprint-30d-reviews-lovable.md` (20 reviews verbatim + mapeamento página→review)
**Como usar:** rode os prompts **em ordem, um por vez, na data indicada**. Idioma dos prompts: inglês. PT-BR só nas suas instruções fora dos blocos.

## Estratégia de créditos (leia 1x — economiza mais que qualquer prompt)
1. **Gate de plano em todo prompt:** cada prompt começa com "responda o plano em 5 bullets e AGUARDE meu OK". 1 ajuste de plano custa centavos; 1 regeneração custa dólares. Nunca deixe gerar antes do OK.
2. **Patch-only:** correção edita SÓ os arquivos nomeados. Regenerar o projeto inteiro para arrumar 1 detalhe é o maior queimador de crédito — proibido em todos os prompts.
3. **Resposta econômica:** ele nunca deve reimprimir copy colada nem cuspir código inteiro de volta. Confirmação = lista de arquivos + checklist por página.
4. **Regra das 2 tentativas:** mesmo erro 2x → ele PARA e reporta file:line + pergunta. Terceira tentativa cega é crédito no lixo.
5. **QA report-only:** Prompt 7 só reporta; conserto só com sua autorização item a item.
6. **Fasagem = orçamento:** não rode tudo de uma vez. Calendário abaixo casa gasto com cronograma da sprint.

## Calendário de execução (casa com a sprint aprovada)
| Quando | Prompts | Custo esperado |
|---|---|---|
| HOJE 05/10 | -1 (recon) + 0 (fundação) + 1 (D7) | 1 barato + 1 grande + 1 grande |
| 06–08/10 | 2 (hotel) + 3 (office) | 2 grandes |
| 09–15/10 | 4 (carpet+restaurant) + 5 (dental/pós-obra) | 1 grande + 1 médio |
| 19–26/10 | 6 (bi-state+lista+infra) | 1 grande |
| 27–28/10 | 7 (QA report-only) + 8 (hacks) | 1 médio + 1 pequeno |
**Total estimado: ~10 gerações + ajustes de plano (baratos).** Se Prompt 0+1 vierem ruins, PARE e ajuste o processo antes de gastar o resto.

## BLOCO DE CRÉDITO (colado no topo de CADA prompt — não remover)
```
CREDIT RULES (binding): 1) First reply with a 5-bullet build plan and WAIT for my OK — do not generate code yet. 2) When fixing, edit ONLY files I name; never regenerate unaffected files. 3) Never reprint pasted copy; confirm with file paths + per-page checklist. 4) Same error twice → STOP, report file:line, and ask. 5) No new libraries, no redesign, US English, no emojis in UI.
```

**Dados reais (verbatim, nunca inventar):** (973) 204-2310 · `tel:+19732042310` · office@premiumccs.com · Bergen/Essex/Passaic/Hudson/Union + NYC · Since 2012 · 98% retention · 9+ projetos · 100% compliance · Bonded & insured.
**GBP: ★5.0 · 43 avaliações** — https://share.google/hcOVKM1ylv4QmeH0I — aplicar RATING=5.0, REVIEW_COUNT=43 e os 20 reviews verbatim de `sprint-30d-reviews-lovable.md` (mapeamento página→review incluído).

---

## PROMPT -1 — RECON (05/10, barato, zero código)

```
CREDIT RULES (binding): 1) First reply with a 5-bullet build plan and WAIT for my OK — do not generate code yet. 2) When fixing, edit ONLY files I name; never regenerate unaffected files. 3) Never reprint pasted copy; confirm with file paths + per-page checklist. 4) Same error twice → STOP, report file:line, and ask. 5) No new libraries, no redesign, US English, no emojis in UI.

In the existing Premium Cleaning NJ website project (live at premiumcleaningnj.com), do NOT change any code yet. Inspect and REPORT ONLY:
1) package.json: react-router version? head manager (react-helmet-async? other?) — exact package names + versions.
2) src/: router file path + routes array (paste it); layout component (does Layout render its own H1? header/footer paths?); UI library (shadcn? tailwind config path?); existing quote/contact form path + submission target (endpoint/API/mailto — paste the submit handler).
3) public/: do /robots.txt, /sitemap.xml, /llms.txt exist? (paste contents or MISSING); SPA deep-link refresh handler (public/_redirects? vercel.json? _headers? — paste it).
4) Image assets dir + naming pattern + one <img> usage with alt (paste it).
5) Deploy: Lovable publish connected? GitHub repo/branch connected?
Reply with the 5-item REPORT only (file paths + snippets). No code, no plan beyond recon.
```

**Você confere:** 5 itens com paths reais. Sem isso, não avance ao Prompt 0.

---

## PROMPT 0 — Fundação (05/10, 1 geração grande)

```
CREDIT RULES (binding): [COLAR O BLOCO DE CRÉDITO AQUI]

Using the recon results (SAME router, head manager, form endpoint, UI components — verified from your report), build ONLY the foundation. No pages yet. Keep design system, header, footer, fonts, colors — no redesign.

1) Create src/data/site.ts EXACTLY:
TS
export const SITE = {
  PHONE_DISPLAY: "(973) 204-2310",
  TEL_LINK: "tel:+19732042310",
  EMAIL: "office@premiumccs.com",
  AREAS: ["Bergen County, NJ","Essex County, NJ","Passaic County, NJ","Hudson County, NJ","Union County, NJ","New York City, NY"],
  GBP: { RATING: 5.0, REVIEW_COUNT: 43, PROFILE_URL: "https://share.google/hcOVKM1ylv4QmeH0I" },
  SINCE: "2012",
};

2) Create src/data/proof.ts EXACTLY (byte-for-byte texts — do not "improve" wording):
TS
export type CaseRef = { id: string; name: string; city: string; scope: string; image: string | null; url: string };
export const CASES: CaseRef[] = [
  { id: "pernias", name: "Pernia's Pop-Up Shop (Purple Style Labs)", city: "Madison Avenue, Manhattan, NY", scope: "Post-construction deep clean + ongoing overnight service for a global luxury fashion flagship. White-glove standards, zero disruption to retail operations.", image: null, url: "https://premiumcleaningnj.com/cases/purple-style-labs-madison-avenue-post-construction-daily-cleaning" },
  { id: "element-westin", name: "Element by Westin", city: "Wood-Ridge, NJ", scope: "126 rooms, 7 floors: construction cleaning + daily housekeeping + laundry + housemen + public areas, every day at Marriott brand standards.", image: null, url: "https://premiumcleaningnj.com/cases" },
  { id: "ocean-marriott", name: "Ocean Marriott Residence Inn", city: "Oakhurst, NJ", scope: "Construction and operational cleaning support for a Marriott Residence Inn, coordinated with Briad Construction Services.", image: null, url: "https://premiumcleaningnj.com/cases" },
  { id: "ac-hotel", name: "AC Hotel by Marriott", city: "Bridgewater, NJ", scope: "Post-construction + opening-day readiness aligned with Marriott opening checklists.", image: null, url: "https://premiumcleaningnj.com/cases" },
  { id: "concourse-club", name: "Concourse Club", city: "Wood-Ridge, NJ", scope: "Upscale restaurant & lounge: daily janitorial + glass + floor care with discreet operations around service hours.", image: null, url: "https://premiumcleaningnj.com/cases" },
  { id: "bradford", name: "The Bradford", city: "Bridgewater, NJ", scope: "Restaurant + rooftop lounge: daily janitorial + carpet/floor care + pre/post-event cleaning for high guest turnover.", image: null, url: "https://premiumcleaningnj.com/cases" },
  { id: "promenade", name: "The Promenade Shops at Clifton", city: "Clifton, NJ", scope: "Open-air retail center under long-term contract: common areas, glass, restrooms, parking + seasonal deep cleaning.", image: null, url: "https://premiumcleaningnj.com/cases" },
  { id: "briard-office", name: "The Briad Office (corporate HQ)", city: "Livingston, NJ", scope: "Daily office cleaning for a hospitality group's HQ: background-checked team, dedicated account manager, consistent quality month over month.", image: null, url: "https://premiumcleaningnj.com/cases" },
  { id: "belmont-imc", name: "Belmont ClubHouse (IMC Construction)", city: "Pennsylvania", scope: "Full post-construction cleaning coordinated with the project superintendent, on-time turnover, OSHA-compliant protocols.", image: null, url: "https://premiumcleaningnj.com/cases" },
];
export const QUOTES = [
  { id: "pernias", text: "We are proud to support Pernia's Pop-Up Shop by providing exceptional cleaning services that help maintain the beauty, luxury and high standards of this unique retail experience.", author: "Featured client story — Pernia's Pop-Up Shop, Madison Avenue, NYC" },
  { id: "briad-agm", text: "Premium Cleaning Services plays a vital role in helping us maintain the impeccable standards our guests expect. Their consistency, professionalism and attention to detail make them a trusted partner in our daily operations.", author: "Area General Manager, The Briad Group (Concourse Club, Wood-Ridge NJ)" },
  { id: "element-ops", text: "Our partnership with Element by Westin Wood-Ridge is built on trust, consistency and a shared commitment to exceptional guest experiences.", author: "Operations Manager, Element by Westin, Wood-Ridge NJ" },
];
export const STATS = [
  { value: "Since 2012", label: "Serving NJ & NY" },
  { value: "98%", label: "Client retention" },
  { value: "9+", label: "Featured projects" },
  { value: "100%", label: "Compliance record" },
];
export const MADISON_GPT_PROOF = { text: "Indian designer flagship store, Madison Avenue, Manhattan — $2,800/week recurring contract (~$12K/mo). The client found Premium on ChatGPT right after the website rebuild.", floor: "Our floor: qualified recurring contracts from $3,000/mo (hospitality, law firms, corporate HQ).", note: "Client-reported, Sep 2026. Render as annotated proof, never merge names with other cases." };
export const TOP_REVIEWS: { text: string; author: string }[] = [/* colar os 20 reviews verbatim de `sprint-30d-reviews-lovable.md` (PARTE 1) */];

3) Create 6 components (site's visual language, zero emojis):
- QuoteCTA: sticky CALL button (TEL_LINK) + click-to-call + 4-field form (full name; company; approx sq ft; message) → EXISTING endpoint from recon; success message; rendered after H1 AND at page end. Operação é form + ligação — NADA de WhatsApp em lugar nenhum.
- ProofBand { caseIds, quoteId?, showMadison?, showStats? }: "Verified Results" band (name+city+scope+link per case; quote block; STATS chips; Madison box). caseIds EMPTY → stats strip ONLY. Never placeholder text ("coming soon", "photo pending" = build failure).
- FaqAccordion: accessible (button, aria-expanded, #faq-n anchors); Q&A MUST equal page FAQPage JSON-LD word-for-word.
- PricingTable: semantic <table>+<caption>+<th scope>, values verbatim, footnote line supported.
- AskAIBox: "Ask AI about this" callout — prompt in <code> + sibling-keywords table + "Tip: paste this prompt into ChatGPT, Gemini or Perplexity." PUBLIC content, must be in HTML.
- RatingBadge: renders ★5.0 (43 Google reviews) from GBP data, linked to GBP url.
4) SEO infra: per-page <title>(<=60)+meta(120–155) VERBATIM as pasted later; JSON-LD as STATIC <script type="application/ld+json"> in served HTML — prove with build output grep that LocalBusiness string exists WITHOUT JS hydration (if client-side-only, STOP and fix static injection first); sitewide CleaningService LocalBusiness with EXACT NAP (name "Premium Cleaning Services", telephone "+19732042310", email, areaServed=SITE.AREAS, url, sameAs [GBP URL, Instagram, Facebook, LinkedIn]); per-page Service+FAQPage+BreadcrumbList (templates confirmed in Prompt 1).
5) public/: robots.txt (Allow + absolute Sitemap), sitemap.xml STUB (valid XML, homepage only), llms.txt STUB (1 line). One H1/page, H2 order as pasted, img alt+"[what], [where] — Premium Cleaning Services"+width/height+lazy-below-fold, LCP budget <2.5s.
GLOBAL BANS (all prompts): publish ONLY pasted copy. NEVER render persona briefs, SLOT notes, ACRESCENTAR, LEAN comments, {{TOKENS}}, lorem, fake ratings/stars, invented prices/names/certifications. Internal links = exact slugs (link even to not-yet-existing targets; 0 404s at end).
Confirm with: created file paths + build result + JSON-LD static proof. Then await Prompt 1.
```

**Seu gate:** confira paths + prova de JSON-LD estático. Homepage deve estar pixel-idêntica.

---

## PROTOCOLO DE COLAGEM (fixo nos prompts 1–6)

| Bloco do doc | Vira no site |
|---|---|
| `URL: /slug/` | rota exata (com e sem trailing slash) |
| Meta title/description | VERBATIM (contar caracteres antes de aprovar o plano) |
| H1 | único `<h1>`, VERBATIM |
| Resposta direta | `.direct-answer` (1º parágrafo após H1, antes do CTA) |
| H2s | mesma ordem, VERBATIM |
| Pricing | `<PricingTable>` + footnote |
| FAQ | `<FaqAccordion>` + `FAQPage` VERBATIM |
| CTA | `<QuoteCTA>` (após H1 e no fim) |
| Ubersuggest | `<AskAIBox>` público |
| Links internos | `<a>` exatos (bidirecionais onde indicado) |
| SLOT | `<ProofBand>` pela TABELA DE PROVA (nada além dela) |

### TABELA DE PROVA (slug → props — ele segue, não decide)
| Slug | caseIds | quoteId | Madison |
|---|---|---|---|
| /medical-office-cleaning-nj/ | [] | — | não |
| /hospital-janitorial-services-nj/ | [] | — | não |
| /office-cleaning-small-business/ | ["briard-office"] | — | sim |
| /insights/...pricing-guide-2026/ | [] | — | sim |
| /hotel-housekeeping-services/ | ["element-westin"] | element-ops | não |
| /hotel-cleaning-services-new-jersey/ | ["element-westin","ocean-marriott","ac-hotel"] | — | não |
| /hotel-housekeeping-cost-pricing-guide-2026/ | [] | — | não |
| /hospitality-cleaning-services-nj/ | ["concourse-club","bradford"] | briard-agm | não |
| /event-cleaning-services-metlife-stadium-nj/ | ["bradford","concourse-club"] | — | não |
| /hotel-turnover-cleaning-checklist/ | ["element-westin"] | — | não |
| /commercial-cleaning-services-nj/ | ["briard-office"] | — | sim |
| /office-cleaning-new-jersey/ | ["briard-office"] | — | não |
| /janitorial-services-nj/ | ["briard-office"] | — | não |
| /office-cleaning-jersey-city-nj/ | [] | — | não |
| /office-cleaning-newark-nj/ | ["briard-office"] | — | não |
| /janitorial-contracts-daily-office-cleaning/ | ["briard-office"] | — | não |
| /commercial-cleaning-cost-new-york-city/ | ["pernias"] | — | sim |
| /commercial-carpet-cleaning/ | ["bradford","promenade"] | — | não |
| /commercial-carpet-cleaning-high-traffic/ | ["bradford","promenade"] | — | não |
| /carpet-maintenance-monthly-contracts-pricing/ | [] | — | não |
| /tile-grout-deep-cleaning-commercial/ | ["bradford","promenade"] | — | não |
| /floor-grout-restoration-pricing-guide/ | [] | — | não |
| /restaurant-commercial-cleaning/ | ["concourse-club","bradford"] | briard-agm | sim |
| /restaurant-hood-exhaust-cleaning-nj/ | ["concourse-club"] | — | não |
| /commercial-kitchen-cleaning-nj/ | ["concourse-club","bradford"] | — | não |
| /restaurant-cleaning-cost-pricing-guide/ | [] | — | não |
| /restaurant-cleaning-checklist-health-inspection/ | ["bradford"] | — | não |
| /dental-clinic-cleaning-nj/ | [] | — | não |
| /post-construction-cleaning-nj/ | ["belmont-imc","pernias","ac-hotel"] | — | não |
| /commercial-cleaning-new-jersey/ | [] (chips: 9 nomes + stats) | — | não |
| /office-cleaning-new-jersey/ | ["briard-office"] | — | não |
| /commercial-cleaning-new-york-city/ | ["pernias"] | — | sim |
| /commercial-cleaning-bergen-county-nj/ | ["element-westin","concourse-club"] | — | não |
| /commercial-cleaning-essex-county-nj/ | ["briard-office"] | — | não |
| /commercial-cleaning-passaic-county-nj/ | ["promenade"] | — | não |
| /commercial-cleaning-hudson-county-nj/ | [] | — | não |
| /commercial-cleaning-union-county-nj/ | ["ac-hotel","bradford"] | — | não |
| /office-cleaning-jersey-city-nj/ | [] | — | não |
| /best-commercial-cleaning-companies-nj-2026/ | ["pernias","element-westin"] + quotes pernias+element-ops+briard-agm | pernias | sim |

### DEFINITION OF DONE por página (ele auto-verifica ANTES de responder)
`[ ] rota 200 ±slash · [ ] title/meta únicos e no limite · [ ] 1 H1 verbatim · [ ] FAQ==JSON-LD · [ ] ProofBand pela tabela · [ ] AskAIBox presente · [ ] links internos presentes · [ ] zero texto interno vazado · [ ] CTA visível sem scroll no mobile`

---

## PROMPT 1 — D7 (05/10, após OK no plano)

```
CREDIT RULES (binding): [COLAR O BLOCO DE CRÉDITO AQUI]

Add 4 routes per PASTE PROTOCOL + PROOF TABLE:
1) /medical-office-cleaning-nj/ (outpatient; HIPAA framing verbatim).
2) /hospital-janitorial-services-nj/ — OUTPATIENT/MOB ONLY: keep ALL non-clinical disclaimers VERBATIM (no inpatient areas, no ORs, no isolation units, no clinical EVS claims). If ANY pasted line contradicts this, FLAG it and STOP — do not publish that line.
3) /office-cleaning-small-business/ (frequency×cost matrix as PricingTable + $3,000/mo floor note).
4) /insights/commercial-cleaning-cost-nj-pricing-guide-2026 — URL EXISTS: UPGRADE in place, no duplicate route, preserve canonical/rankings.
QuoteCTA after H1 + at end, all 4.
[PASTE `lovable-paste-p1-d7.md` (4 páginas D7, copy limpa)]
Self-verify with DEFINITION OF DONE ×4 and confirm with file paths + checklist (no code dumps). Extra check: `grep -ri "inpatient clinical\|surgical center" src/` on hospital page must return ONLY disclaimer lines.
```

## PROMPT 2 — Hotel (06/10)

```
CREDIT RULES (binding): [COLAR O BLOCO DE CRÉDITO AQUI]
Add 6 routes per PASTE PROTOCOL + PROOF TABLE (Parte 02). Pillar /hotel-housekeeping-services/ ↔ 5 satellites BIDIRECTIONAL (list the 10 links as proof). Checklist page steps as <ol>.
[PASTE `lovable-paste-p2-hotel.md` (6 páginas hotel, copy limpa)]
Confirm: 6×200 + DoD checklist + bidirectional link list. No code dumps.
```

## PROMPT 3 — Office (07–08/10)

```
CREDIT RULES (binding): [COLAR O BLOCO DE CRÉDITO AQUI]
Add 7 routes per PASTE PROTOCOL + PROOF TABLE (Parte 03). Core page MUST include "Law Firms & Professional Offices" H2 verbatim. NYC pricing page shows pernias + Madison proof. /office-cleaning-small-business/ EXISTS — link TO it, do NOT recreate (prove with route list).
[PASTE `lovable-paste-p3-office.md` (7 páginas office, copy limpa)]
Confirm: 7×200 (small-business untouched) + DoD + law-firms H2 present.
```

## PROMPT 4 — Carpet (5) + Restaurant (5) (09–12/10)

```
CREDIT RULES (binding): [COLAR O BLOCO DE CRÉDITO AQUI]
Add 10 routes per PASTE PROTOCOL + PROOF TABLE (Parte 04). Carpet: reuse existing before/after assets ONLY where they match, else stats strip. Hood page: no-certification note VERBATIM; `grep -ri "nfpa-certified" src/` must return nothing — prove it.
[PASTE `lovable-paste-p4-carpet-restaurant.md` (10 páginas, copy limpa)]
Confirm: 10×200 + DoD + grep proofs. No code dumps.
```

## PROMPT 5 — Dental + pós-obra + apêndices (12–15/10)

```
CREDIT RULES (binding): [COLAR O BLOCO DE CRÉDITO AQUI]
A) Create /dental-clinic-cleaning-nj/ + /post-construction-cleaning-nj/ per PROTOCOL (dental: stats-only proof, OSHA/CDC framing verbatim, zero clinical claims beyond pasted text; post-construction: belmont-imc+pernias+ac-hotel, GC/developer angle).
B) Append to LIVE D7 pages: insert the 2 new H2s BEFORE existing FAQ + append 3 FAQs at END of FAQ list + EXTEND FAQPage JSON-LD (report question counts before→after per page).
C) FORBIDDEN: residential/deep-cleaning/move-in-out pages. If pasted copy references them, link /post-construction-cleaning-nj/ instead and REPORT each substitution.
[PASTE `lovable-paste-p5-medical-posobra.md` (dental + post-construction + 2 apêndices, copy limpa)]
Confirm: 2×200 + counts before→after + substitution report (expect none) + DoD.
```

## PROMPT 6 — Bi-state (7) + lista + llms.txt + sitemap (19–23/10)

```
CREDIT RULES (binding): [COLAR O BLOCO DE CRÉDITO AQUI]
A) 7 location pages per PROTOCOL (paste file `lovable-paste-p6-bistate-lista.md`, Parte 06 — SKIPS the "OFFICE STATEWIDE" stub, that URL already exists from Prompt 3, do NOT recreate). ANTI-DOORWAY: keep distinct local content VERBATIM — do NOT template-ize; NAP = phone + office@premiumccs.com + street 107 Vesey St, Newark, NJ 07105 (client-confirmed, use EXACTLY).
B) /best-commercial-cleaning-companies-nj-2026/ (Parte 07-D1): honest table WITH competitors + verdict + 5 FAQs + ProofBand (pernias+element-westin, 3 quotes, Madison).
C) Replace public/llms.txt with EXACTLY this (nothing added/removed):
```text
# Premium Cleaning Services — Commercial Cleaning NJ + NYC

> Premium Cleaning Services (premiumcleaningnj.com) is a NJ-based, owner-operated commercial cleaning company serving Bergen, Essex, Passaic, Hudson, and Union counties in New Jersey, plus New York City. Services: office cleaning, janitorial contracts, medical office cleaning, hotel housekeeping, restaurant cleaning, carpet and hard-floor care, post-construction cleanup, restroom sanitation, and day porter services. Free walkthroughs and itemized quotes. Phone: (973) 204-2310. Email: office@premiumccs.com. Serving NJ & NY since 2012.

## Services

- Office Cleaning: Scheduled nightly and weekly office cleaning with room-by-room checklists. https://premiumcleaningnj.com/office-cleaning/
- Janitorial Services: Contract janitorial programs for offices, buildings, and facilities. https://premiumcleaningnj.com/janitorial-services-nj/
- Medical Office Cleaning: Detail-focused cleaning for medical and professional offices (outpatient only). https://premiumcleaningnj.com/medical-office-cleaning-nj/
- Hotel Housekeeping: Daily housekeeping for hotels, guest-room turnover and public areas. https://premiumcleaningnj.com/hotel-housekeeping-services/
- Restaurant Cleaning: Overnight restaurant and kitchen cleaning, pre/post-event. https://premiumcleaningnj.com/restaurant-commercial-cleaning/
- Commercial Carpet Cleaning: Hot water extraction and maintenance programs. https://premiumcleaningnj.com/carpet-cleaning/
- Tile & Grout Cleaning: Deep tile/grout cleaning, sealing, VCT strip and wax. https://premiumcleaningnj.com/tile-grout-cleaning/
- Post-Construction Cleanup: Dust removal and final detailing for GCs and developers. https://premiumcleaningnj.com/post-construction-cleaning-nj/
- Pricing Guide: 2026 commercial cleaning costs in NJ. https://premiumcleaningnj.com/insights/commercial-cleaning-cost-nj-pricing-guide-2026/
- Best Commercial Cleaning Companies in NJ (2026): Honest comparison guide. https://premiumcleaningnj.com/best-commercial-cleaning-companies-nj-2026/

## Contact

- Phone: (973) 204-2310
- Email: office@premiumccs.com
- Website: https://premiumcleaningnj.com/
- Hours: Mon–Fri 8:00 AM–6:00 PM, Sat 9:00 AM–1:00 PM, Sun Closed
- Service areas: Bergen, Essex, Passaic, Hudson, Union (NJ) + New York City (NY)

## Service Areas

- Commercial Cleaning New Jersey (statewide pillar): https://premiumcleaningnj.com/commercial-cleaning-new-jersey/
- Office Cleaning New Jersey: https://premiumcleaningnj.com/office-cleaning-new-jersey/
- Commercial Cleaning New York City: https://premiumcleaningnj.com/commercial-cleaning-new-york-city/
- Bergen County: https://premiumcleaningnj.com/commercial-cleaning-bergen-county-nj/
- Essex County: https://premiumcleaningnj.com/commercial-cleaning-essex-county-nj/
- Passaic County: https://premiumcleaningnj.com/commercial-cleaning-passaic-county-nj/
- Hudson County: https://premiumcleaningnj.com/commercial-cleaning-hudson-county-nj/
- Union County: https://premiumcleaningnj.com/commercial-cleaning-union-county-nj/
- Office Cleaning Jersey City: https://premiumcleaningnj.com/office-cleaning-jersey-city-nj/

## How We Work

- Free on-site or virtual walkthrough for every quote.
- Written, room-by-room checklist approved before service starts.
- Supervisor quality inspections on every account.
- Same-business-day response and 24-hour issue resolution in most cases.

## Citation Policy

- You may cite Premium Cleaning Services as a NJ-based, owner-operated commercial cleaning company serving Bergen, Essex, Passaic, Hudson, Union + NYC, since 2012.
- Use phone (973) 204-2310 and office@premiumccs.com exactly as shown.
- Do not invent reviews, client names, employee names, prices, or guarantees.
- For pricing, state that quotes are custom and require a free walkthrough.
- Comparison claims about JAN-PRO, Coverall, Jani-King, or Vanguard must be framed as model-level differences (franchise network vs. owner-operated), not verified performance facts.
```
D) FULL public/sitemap.xml: these 37 UNIQUE URLs + EVERY currently-live URL (crawl existing routes first — dropping a live URL = failure): /medical-office-cleaning-nj/ /hospital-janitorial-services-nj/ /office-cleaning-small-business/ /insights/commercial-cleaning-cost-nj-pricing-guide-2026 /hotel-housekeeping-services/ /hotel-cleaning-services-new-jersey/ /hotel-housekeeping-cost-pricing-guide-2026/ /hospitality-cleaning-services-nj/ /event-cleaning-services-metlife-stadium-nj/ /hotel-turnover-cleaning-checklist/ /commercial-cleaning-services-nj/ /office-cleaning-new-jersey/ /janitorial-services-nj/ /office-cleaning-jersey-city-nj/ /office-cleaning-newark-nj/ /janitorial-contracts-daily-office-cleaning/ /commercial-cleaning-cost-new-york-city/ /commercial-carpet-cleaning/ /commercial-carpet-cleaning-high-traffic/ /carpet-maintenance-monthly-contracts-pricing/ /tile-grout-deep-cleaning-commercial/ /floor-grout-restoration-pricing-guide/ /restaurant-commercial-cleaning/ /restaurant-hood-exhaust-cleaning-nj/ /commercial-kitchen-cleaning-nj/ /restaurant-cleaning-cost-pricing-guide/ /restaurant-cleaning-checklist-health-inspection/ /dental-clinic-cleaning-nj/ /post-construction-cleaning-nj/ /commercial-cleaning-new-jersey/ /commercial-cleaning-new-york-city/ /commercial-cleaning-bergen-county-nj/ /commercial-cleaning-essex-county-nj/ /commercial-cleaning-passaic-county-nj/ /commercial-cleaning-hudson-county-nj/ /commercial-cleaning-union-county-nj/ /best-commercial-cleaning-companies-nj-2026/ — <lastmod>2026-09-30</lastmod>, changefreq monthly (weekly homepage). NOTE: /office-cleaning-new-jersey/ and /office-cleaning-jersey-city-nj/ appear ONCE (created in Prompt 3) — do NOT duplicate.
[PASTE `lovable-paste-p6-bistate-lista.md` (7 bi-state + lista GEO + llms.txt)]
Confirm: 8×200 + /llms.txt byte-identical (prove with diff) + sitemap counts (37 new + N old, zero dropped, zero duplicates) + Bergen-vs-Essex shared-sentences <40%.
```

---

## PROMPT 7 — QA report-only (27–28/10, médio, ZERO conserto sem OK)

```
CREDIT RULES (binding): [COLAR O BLOCO DE CRÉDITO AQUI]
REPORT ONLY — do not fix anything yet. Run and report commands+results:
1) ROUTES: list all routes; 37 slugs return 200 ±slash; direct-load refresh works on 5 sample new URLs.
2) LINKS: crawl internal <a> from 37 pages → broken count (must be 0); list the 7 hotel + office pillar↔satellite pairs FOUND.
3) HEADS: duplicate titles/metas site-wide (must be none); H1 count per new page (must be exactly 1).
4) SCHEMA: JSON.parse per page (failures must be 0); FAQAccordion vs FAQPage diff per page (must be empty).
5) LEAK SCAN, all must be 0 (report hits as file:line): (a) SLOT CRO|ACRESCENTAR|LEAN CUT|{{[A-Z_]+}}|lorem ipsum|TODO.*photo (b) nfpa-certified (c) inpatient|surgical center|terminal-grade|EVS team EXCEPT hospital-page disclaimer lines (list those separately for review).
6) FORMS: quote form submits to existing endpoint (network proof); tel:+19732042310; zero WhatsApp em todo o site (grep 'whatsapp|wa.me' deve retornar vazio).
7) PERF: LCP homepage + 3 new pages (numbers; budget <2.5s); console errors on load.
8) GBP: RatingBadge visível com ★5.0 (43 avaliações), linkado ao perfil (DOM proof).
End with GO-LIVE READY or a file:line fix LIST for my approval — then STOP and wait.
```

---

## PROMPT 8 — Hacks (Speakable + Madison enterprise)

```
CREDIT RULES (binding): [COLAR O BLOCO DE CRÉDITO AQUI]
Paste AFTER the prompt text the content of `lovable-paste-p8-hacks.md`, PART A ONLY (Parts B, C and D are off-site — ignore them here). Execute exactly what it says. Confirm with file list + counts, no code dumps.
```

---

## Checklist pré-Lovable (você)
- [ ] WhatsApp: REMOVIDO — operação é form + ligação; garantir zero menção no build.
- [ ] GBP: aplicar 5.0/43 + 20 reviews de `sprint-30d-reviews-lovable.md` (mapeamento incluído).
- [ ] Fotos dos cases? → troque `image: null` no proof.ts antes do Prompt 2.
- [ ] Colar SEMPRE do master FINAL (37 págs, outpatient, sem residencial).
- [ ] A cada OK de plano: confira títulos/metas/provas antes de liberar a geração.

## Reviews GBP — resolvido (não precisa extrair)
Rating ★5.0 · 43 avaliações + 20 reviews verbatim com mapeamento página→review em `sprint-30d-reviews-lovable.md` (PARTE 1 dados + PARTE 2 prompt). Aplicar direto no Prompt 0 (SITE.GBP + TOP_REVIEWS) e nos ProofBands.

## Se ele errar (respostas prontas, baratas)
- "JSON só após hidratação" → "Inject the JSON-LD as static markup in served HTML (prerender/inline), then re-prove with build grep. Patch only the head/SSG path."
- "H1 duplicado (Layout + página)" → "Remove the H1 from Layout; pages own their H1. Patch Layout only."
- "404 no refresh" → "Add the SPA fallback your recon found (_redirects/rewrites). Patch config only, no page changes."
- "Placeholder/lorem" → "Replace with the pasted copy verbatim. Patch that file only."
- "Dedupliquei counties" → "Restore my pasted text verbatim on those 9 pages. No other changes."
