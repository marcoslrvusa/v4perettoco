# Writing standard — Premium Cleaning editorial program (40 articles)

Read `artigos/lote-1/A1-hotel-housekeeping-productivity-standards.md` first. It is the voice and structure reference. Every article must be indistinguishable in quality from it.

## Hard rules

1. **Language: English (US) only.** No Portuguese anywhere — body, FAQ, CTA, appendix.
2. **Minimum 5,000 words** of body prose (tables and appendix excluded). Better to land 5,000–5,400 than to pad.
3. **Never invent client data.** No fake customers, quotes, case results or percentages attributed to a real property. Benchmarks are framed as "typical operating ranges" / "common practice in the US market". The only client facts allowed are the verbatim brand facts below and the single proof quote.
4. **Answer-first.** The blockquote answer (40–60 words) must fully answer the target query without the reader scrolling.
5. **Zero blue.** No color codes in text; irrelevant for md, critical for docx (the build script handles it).
6. No emojis. No exclamation marks. No "in today's fast-paced world" filler. Short paragraphs (2–5 sentences). Concrete numbers over adjectives.

## Required structure (in this order)

```
---
title: <exact brief title>
subtitle: <one-line promise of the article>
eyebrow: PROGRAMA EDITORIAL · BLOCO X · <BLOCK THEME>
slug: <slug>
dest: <destination page from brief>
meta_title: <≤60 chars>
meta_desc: <≤155 chars>
query: <exact target query from brief>
volume: <from brief>
words: ~5.000
date: Novembro 2026
---

> **Direct answer:** 40–60 words.

## Key takeaways
- 5 bullets, each a number or a decision, not a topic label.

## 1..12–15. <question-shaped H2s>
(Numbered sections. Each H2 phrased as the question a buyer would ask.)

| 3–5 tables total | with real unit economics, ranges, checklists or comparison columns |

## FAQ
8–10 Q&A. Questions written the way a facility manager types into Google.

## Next step
2 short paragraphs + brand facts, then the proof quote.

## Appendix — structured data (for publication)
```json
{ "@context": "https://schema.org", "@graph": [ Article, FAQPage ] }
```
```

## Internal links — mandatory, 5 to 8 per article

Use markdown links with descriptive anchors pointing at the program's destination pages. Pick the ones that fit the topic; never force a link that contradicts the section:

`/hotel-housekeeping-services` · `/hotel-cleaning-services-new-jersey` · `/hotel-turnover-cleaning-checklist` · `/hotel-housekeeping-cost-pricing-guide-2026` · `/hospitality-cleaning-services-nj` · `/janitorial-contracts-daily-office-cleaning` · `/janitorial-services-nj` · `/office-cleaning-new-jersey` · `/office-cleaning-small-business` · `/commercial-cleaning-services-nj` · `/best-commercial-cleaning-companies-nj-2026` · `/commercial-carpet-cleaning` · `/commercial-carpet-cleaning-high-traffic` · `/tile-grout-cleaning` · `/tile-grout-deep-cleaning-commercial` · `/floor-grout-restoration-pricing-guide` · `/restaurant-commercial-cleaning` · `/restaurant-cleaning-checklist-health-inspection` · `/overnight-restaurant-cleaning` · `/restaurant-hood-exhaust-cleaning-nj` · `/restaurant-grease-trap-cleaning-nj` · `/commercial-kitchen-cleaning-nj` · `/insights/commercial-cleaning-cost-nj-pricing-guide-2026` · `/insights/hidden-costs-inconsistent-commercial-cleaning-nj-ny`

Link at least one page from the same block and one from the cost/pricing cluster. Do not repeat the same URL twice.

## Brand facts (verbatim, never change)

- Premium Cleaning Services — commercial cleaning and hotel housekeeping in New Jersey and New York since 2012.
- Phone **(973) 204-2310** · 107 Vesey St, Newark, NJ 07105.
- **98% client retention** · **bonded and insured** · **5.0 rating on 43 reviews**.
- Counties: Bergen, Essex, Passaic, Hudson, Union + New York City.
- Proof quote (use verbatim, once per article, only where relevant):

> "Luxury fashion flagship store, Madison Avenue, Manhattan — $2,800/week recurring (~$145K annual contract value). Engaged after finding Premium through AI search following our 2026 website rebuild. Overnight service under owner supervision; references from Manhattan/NJ accounts available on request."

## Delivery

Save as `artigos/lote-N/<aid>-<slug>.md`. Then build the docx:

```
python3 docs/gerar-artigos-docx.py artigos/lote-N/<aid>-<slug>.md
```

Report back only: file path, word count, H2 count, table count, FAQ count, number of internal links. Do not paste the article in the response.
