# MD — Reviews reais no site (carrossel + badge)

**Origem:** Google Business Profile — Premium Cleaning Services · **★5.0 · 43 avaliações** · https://share.google/hcOVKM1ylv4QmeH0I
**Regra:** textos verbatim do Google, sem edição. Respostas do owner NÃO publicam. 6 reviews descartados permanentemente (3 citam outras marcas — Bright/Sparkle/Excellent; 1 de funcionária; 1 sobre franquia; 1 cita "Premium Contractors"). Reviews truncados com "… More" usam só o trecho visível.

## PARTE 1 — Dados oficiais (colar primeiro no Lovable)

**Badge (valores únicos — nunca digitados à mão):** `RATING = 5.0` · `REVIEW_COUNT = 43`

**TOP_REVIEWS:**
1. **Gessyara Ferreira** (hotel) — *"Premium Cleaning Services has a strong housekeeping, houseman, and laundry team. Everyone works hard and stays committed to doing a good job. Their effort really shows in the daily routine of the hotel."*
2. **Isabela Pinheiro** (hotel) — *"Amazing team of housekeepers! Totally recommend!"*
3. **Samuel Escobar** (hotel) — *"Great environment and hotel cleaning crew amazing."*
4. **Amandha Rodrigues** (Local Guide · 9 reviews | office) — *"We are a flooring company and requested a cleaning quote for our office from Premium Cleaning Services. They were very attentive, offered an extremely competitive price, and delivered an impeccable service. Great team and very professional when it comes to office cleaning. Highly recommended!"*
5. **Monalisa Melo** (corporate/contratos) — *"I know the corporate team from Premium Cleaning and I gotta say, the way they handle contracts is next level. Super organized and always on top of things. It's way more than just cleaning… they keep constant communication with the client, and that makes all the difference. 100% recommend!"*
6. **golden apple** (Local Guide · 13 reviews | office) — *"I recently worked with Premium Cleaning on a project and requested a full quotation for office cleaning. The team was quick to respond, very professional, and transparent with their pricing. The estimate was detailed and fair…"*
7. **Rafael Kumagai** (corporate) — *"Fantastic corporate team, fast communication and very flexible with negotiations."*
8. **Ana Cynthia** (Local Guide · 14 reviews | restaurant) — *"I requested a quote from Premium Cleaning Services for the restaurant/bar, and they responded very quickly. The company is well-organized, communication was fast and clear, and the proposal was very competitive."*
9. **Vanessa De Matos** (restaurant) — *"I've negotiated with their team before — super easy to work with. They offer competitive pricing, are flexible, transparent, and always deliver top-notch quality."*
10. **Ron Pepe** (varejo/property) — *"Premium Cleaning Services have been servicing our Promenade Shops at Clifton Mall for quite some time. Their attention to detail is second to none…"*
11. **Devin Olguin** (varejo) — *"they manage the cleaning operations at the store where I work and they go above and beyond!"*
12. **Isha Katwala** (varejo) — *"We are super happy using their services. The team they've provided for our store is excellent & super helpful… Italo has been great to work with."*
13. **Bruno Parreira** (Local Guide · 23 reviews | commercial) — *"We had a great experience with Premium Cleaning for our commercial cleaning needs. Their team is always on time, and the supervisor regularly checks the work with the employees to make sure everything is done properly."*
14. **Valber Araujo Sousa** (Local Guide · **55 reviews** | valor) — *"Working with Premium Cleaning Services has been a great experience. They're easy to work with, very reasonable on pricing, and always willing to find the best solution without compromising quality."*
15. **Silvia Perpétua Domingos** (valor) — *"Easy to negotiate with, fairly priced, and the quality is unmatched."* (marcada como $500+ no perfil)
16. **Giovanni Evangelista** (valor) — *"Excellent service, great pricing, and outstanding quality. It's hard to find a team this reliable."*
17. **Roberto Santos** (gestão) — *"They understand the importance of maintaining the standards of your business and are always willing to address any issues that come up. Highly recommended!"*
18. **Rafael Silva Cardoso** (gestão) — *"The management team at Premium Cleaning Services is fantastic to partner with… prioritize delivering real value…"*
19. **SIMONE SOUZA LUZ** (9 reviews | gestão) — *"always very quick, professional, and attentive to every detail… take pride in their work. Highly recommend!"*
20. **Gabriela Almeida** (NYC/diferencial) — *"What I liked the most is they speak English, Spanish, and Portuguese – makes everything way easier to talk and deal with. Super helpful!"*

**Mapeamento review → páginas (usar exatamente):**
- Hotel (housekeeping, hotel-nj, turnover, cost-guide, hospitality, event) → 1, 2, 3 (+ cases/quotes existentes)
- Office core, office-nj, janitorial, Newark, Essex, Jersey City → 4, 6, 7, 17, 19
- janitorial-contracts → 5 (Monalisa = prova de contrato)
- NYC + Hudson + listicle verdict → 20, 14 (+ prova GPT Madison)
- Restaurant (5 págs) → 8, 9
- Carpet/floor (5 págs) → 13, 14
- Pricing guides + NJ pillar + Passaic/Bergen/Union → 14, 15, 16 (+ 10 no Passaic e na lista)
- Homepage (novo): carrossel rotativo 10, 14, 19, 8, 1
- Medical/hospital/dental/pós-obra: SEM review (sem case setorial publicado — manter stats + flag honesto)

## PARTE 2 — Prompt para o Lovable (colar depois dos dados)

```
Using the TOP_REVIEWS data and RATING=5.0 / REVIEW_COUNT=43 pasted above:
1) Create src/data/reviews.ts exporting TOP_REVIEWS (id, segment, text verbatim, author, authorMeta, stars: 5) and GBP { rating: 5.0, count: 43, url: "https://share.google/hcOVKM1ylv4QmeH0I" }. Texts are final client-approved Google reviews — reproduce byte-for-byte, never edit, never invent.
2) Build ReviewCarousel (auto-slide + manual arrows/dots, pause on hover, accessible, mobile swipe): review text in quotes, author + authorMeta, 5 stars, link "See on Google" to GBP url. No fake reviews anywhere — render ONLY array items.
3) Embed ONE carousel inside ProofBand (after the case/static proof, before the CTA): show only the reviewIds mapped per page (table below). Pages not listed keep stats-only ProofBand (medical, hospital, dental, post-construction — do NOT force mismatched reviews).
4) RatingBadge: render ★5.0 (43 Google reviews) from GBP data, linked to GBP url. Replace any stats-only fallback where carousel now exists.
5) Homepage: add rotating carousel (reviews 10, 14, 19, 8, 1) in the social-proof section.
6) Mapping (page slug → reviewIds): hotel-housekeeping-services [1,2] · hotel-cleaning-services-new-jersey [1,3] · hotel-turnover-checklist [2] · hotel-housekeeping-cost-guide [1] · hospitality-cleaning-services-nj [1] + existing cases · event-metlife [2] · commercial-cleaning-services-nj [4,17] · office-cleaning-new-jersey [4,19] · janitorial-services-nj [6,7] · janitorial-contracts [5] · office-newark [4] · office-jersey-city [6] · essex-county [4] · bergen-county [19] · passaic-county [10] · hudson-county [20] · union-county [16] · NYC pages [20,14] · restaurant-commercial [8,9] · hood/kitchen/checklist [8 or 9] · carpet pages + floor [13,14] · carpet/restaurant pricing guides [14,15,16] · NJ pillar [10,14] · listicle [10,14,16] + verdict.
7) Acceptance: build passes; every mapped page shows its carousel with correct texts; untouched pages unchanged; grep for invented stars/text returns zero. Confirm with page→reviews list, no code dumps.
```
