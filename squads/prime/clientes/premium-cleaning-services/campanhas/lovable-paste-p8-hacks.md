# COLAR NO LOVABLE — PROMPT 8 (Hacks: Speakable + prova Madison enterprise)

> Cole PRIMEIRO o bloco de crédito (manual, seção BLOCO DE CRÉDITO) e o plano em 5 bullets, como nos prompts 1–6. Depois cole a PARTE A abaixo. As PARTES B, C e D são OFF-SITE (não são para o Lovable) — estão aqui para não perder nada.

---

## PARTE A — para o Lovable (Speakable em 37 páginas + Madison enterprise)

```
Add SpeakableSpecification markup so voice assistants and AI answers prioritize our content, and update the Madison proof sitewide:

1) For EACH of the 37 content pages, append to the page's existing JSON-LD a SpeakableSpecification node pointing at (a) the lead/direct-answer paragraph (the 40–60 word answer right after the H1) and (b) the first TWO FAQ answers. Use this exact shape, adapting selectors to the components you built (direct-answer block + FAQ accordion). If a CSS selector is ambiguous, use xpath instead — never point at nav, header, footer, CTA or cookie text:

{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": [".direct-answer", ".faq-item:nth-child(1) .faq-answer", ".faq-item:nth-child(2) .faq-answer"]
  }
}

Rules: static markup in served HTML (same rule as all JSON-LD — prove with build grep, no client-side-only). One speakable node per page. Do NOT change any visible copy. Do NOT add speakable to homepage, /cases, /insights index or utility pages — only the 37 content pages.

2) Sitewide find-and-replace of the Madison proof box text (ProofBand Madison variant + any page repeating it). OLD: "Indian designer flagship store, Madison Avenue, Manhattan — $2,800/week recurring contract (~$12K/mo). The client found Premium on ChatGPT right after the website rebuild." NEW (verbatim): "Luxury fashion flagship store, Madison Avenue, Manhattan — $2,800/week recurring (~$145K annual contract value). Engaged after finding Premium through AI search following our 2026 website rebuild. Overnight service under owner supervision; references from Manhattan/NJ accounts available on request."

3) Acceptance: build passes; grep proves 37 speakable nodes in static HTML; Madison new text present everywhere the old text was (report file:line list of replacements); homepage pixel-identical; confirm with file list + counts, no code dumps.
```

---

## PARTE B — OFF-SITE (não é Lovable): PR wire blast 48h

- [ ] Aprovar o gancho com o cliente: "$2,800/week Madison Ave contract won after being discovered on ChatGPT" (fato reportado por ele, Sep 2026).
- [ ] Contratar distribuição (Business Wire / PR Newswire / GlobeNewswire, ~US$ 500–1.000).
- [ ] Release precisa ter: 1 dado exclusivo (faixas de preço NJ do pricing guide), 1 quote do dono, link para premiumcleaningnj.com + 1 página pilar.
- [ ] Meta D+2: 200+ domínios sindicados (monitorar via alertas + search `site:`).
- [ ] Se algum veículo grande republicar com link, pautar follow-up (data study).

## PARTE C — OFF-SITE (não é Lovable): Reddit + Quora (zero spam)

- Subreddits: r/newjersey, r/smallbusiness, r/CommercialRealEstate, r/facilitymanagement (+ r/nyc se permitir autopromoção com disclosure — ler as regras de cada um ANTES).
- Formato: 5–10 respostas genuinamente úteis usando nossas tabelas (pricing, checklists, frequency×cost). Disclosure da empresa no perfil. Nunca linkar no corpo da primeira interação; link só se a resposta exige fonte.
- Títulos-espelho (adaptar ao tom de cada comunidade): custo de office cleaning em NJ · hotel housekeeping terceirizada vs própria · quanto custa carpet comercial por sq ft.
- Quora: 2–3 respostas nos prompts #1/#3/#7 verbatim.
- Proibido: astroturf, contas falsas, upvote próprio, copiar/colar idêntico (ban = dano à marca).

## PARTE D — OFF-SITE (não é Lovable): 10 Q&As prontos para o painel do GBP

Colar 1 por vez em perguntas e respostas do perfil (pergunta como cliente, resposta como Premium, curta e com keyword):

1. **Do you offer daily office cleaning contracts in Bergen County?** — Yes. Nightly crews across Bergen, Essex, Passaic, Hudson and Union counties, plus NYC. Written checklist, supervisor inspections. Call (973) 204-2310 for a walkthrough.
2. **What is your minimum contract value?** — Our qualified recurring programs start at $3,000/mo (hospitality, law firms, corporate HQ). Request a walkthrough for an exact quote.
3. **Do you clean medical offices?** — Yes — outpatient clinics, MOBs and dental offices, with OSHA/CDC-aligned checklists. No inpatient or clinical services.
4. **Do you provide hotel housekeeping?** — Yes. Up to 126 rooms/day at Marriott brand standards, plus laundry, housemen and public areas. References available on request.
5. **Do you clean restaurants?** — Yes — overnight kitchen, hood/exhaust and dining cleaning, pre/post-event. Health-code aligned, discreet crews.
6. **How much does commercial carpet cleaning cost?** — Typical NJ ranges plus per-sq-ft pricing for large spaces on our pricing guide. Final quote after walkthrough: (973) 204-2310.
7. **Do you serve Manhattan?** — Yes. Our flagship contract is a luxury fashion store on Madison Avenue ($2,800/week). NJ-based crews serving NYC metro.
8. **Are you bonded and insured?** — Yes, fully bonded and insured. COI and references available on request for every contract.
9. **Do you do post-construction cleaning?** — Yes, for GCs and developers, with punch-list support. Most post-construction clients convert to recurring contracts.
10. **How fast can you start?** — Walkthrough within 48 hours, start in 3–5 business days across Northern NJ and NYC.
