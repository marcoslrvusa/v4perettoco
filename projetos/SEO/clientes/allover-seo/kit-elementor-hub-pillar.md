# KIT PAINEL ELEMENTOR — Blocos hub pillar → cluster (fase DOWN da malha)

> Resposta direta: **SIM, dá para fazer CSS + HTML direto no painel sem quebrar nada.**
> O método seguro é **aditivo**: um widget "HTML" do Elementor no fim do conteúdo de cada pillar,
> com o bloco abaixo (CSS escopado `.ao-hub`, sem tocar no tema). Nada via API, nada no `_elementor_data`.
> Tempo estimado: ~10 min por pillar (6 pillars). Backup: duplicar a página antes (Elementor > Ferramentas > Duplicar).

## Passo a passo no painel (repetir por pillar)
1. Páginas > abrir a pillar > **Editar com Elementor**.
2. No fim do conteúdo, arrastar um widget **HTML** (não "Texto").
3. Colar o **CSS (uma vez por página)** + o **bloco da pillar**.
4. Atualizar > conferir no front (links abrem os artigos, estilo navy/vermelho).
5. Repetir nas 6 pillars. Siding/Windows entram quando as pillars existirem.

## CSS (colar uma vez por página, junto do bloco)
<!-- COLE no widget HTML do Elementor (ou em Aparência > Personalizar > CSS adicional) -->
<style>
.ao-hub{background:#fff;border:1px solid #dbe2ef;border-radius:12px;padding:20px 24px;margin:22px 0;border-top:4px solid #CA0302}
.ao-hub p.ao-hub-title{margin:0 0 10px;font-weight:800;color:#0A1C38;font-size:1.05rem}
.ao-hub ul{margin:0 0 0 20px;padding:0}
.ao-hub li{margin:6px 0;font-size:.95rem}
.ao-hub li a{color:#0A1C38;text-decoration:underline}
.ao-hub li a:hover{color:#CA0302}
.ao-hub .ao-hub-cta{margin:12px 0 0;font-weight:700}
</style>


## Bloco — Storm Damage & Reparos de Emergência (11 links) — colar na pillar https://allovertxroofing.com/storm-damage-repair-houston/

```html
<div class="ao-hub">
  <p class="ao-hub-title">Guias e recursos sobre Storm Damage &amp; Reparos de Emergência</p>
  <ul>
  <li><a href="https://allovertxroofing.com/roof-leak-repair-houston-tx/">Roof Leak Repair in Houston, TX: Fast Help When It Matters</a></li>
  <li><a href="https://allovertxroofing.com/storm-damage-roof-repair-houston-guide/">Storm Damage Roof Repair in Houston: Hail, Wind, Insurance</a></li>
  <li><a href="https://allovertxroofing.com/emergency-roof-repair-houston/">Emergency Roof Repair in Houston: What to Do First</a></li>
  <li><a href="https://allovertxroofing.com/hurricane-preparedness-roof-houston/">Hurricane Preparedness for Your Roof in Houston</a></li>
  <li><a href="https://allovertxroofing.com/hail-damage-roof-checklist-houston/">Hail Damage Roof Checklist for Houston Homeowners</a></li>
  <li><a href="https://allovertxroofing.com/roof-insurance-claims-texas-guide/">How Insurance Claims Work for Roof Damage in Texas</a></li>
  <li><a href="https://allovertxroofing.com/how-to-tell-roof-leaking/">How to Tell If Your Roof Is Leaking</a></li>
  <li><a href="https://allovertxroofing.com/what-to-do-after-roof-leak/">What to Do After a Roof Leak: Emergency Steps</a></li>
  <li><a href="https://allovertxroofing.com/spot-storm-damage-houston-hailstorm/">How to Spot Storm Damage After a Houston Hailstorm</a></li>
  <li><a href="https://allovertxroofing.com/roof-leak-repair-in-houston/">Roof Leak Repair in Houston: What You Need to Know</a></li>
  <li><a href="https://allovertxroofing.com/steps-take-after-storm-damages-roof-houston/">3 Steps to Take after a Storm Damages Your Roof in Houston</a></li>
  </ul>
  <p class="ao-hub-cta">Prefere falar com um especialista? <a href="tel:+12818466665">(281) 846-6665</a> — inspeção gratuita.</p>
</div>
```


## Bloco — Residential Roofing & Replacement (23 links) — colar na pillar https://allovertxroofing.com/residential-roofing/

```html
<div class="ao-hub">
  <p class="ao-hub-title">Guias e recursos sobre Residential Roofing &amp; Replacement</p>
  <ul>
  <li><a href="https://allovertxroofing.com/asphalt-shingle-roofing-houston-guide/">Asphalt Shingle Roofing in Houston: Replacement Guide</a></li>
  <li><a href="https://allovertxroofing.com/roof-replacement-houston-tx-cost/">Roof Replacement in Houston, TX: Cost and Financing</a></li>
  <li><a href="https://allovertxroofing.com/roof-repair-houston-tx-service/">Roof Repair in Houston, TX: Same-Day Service</a></li>
  <li><a href="https://allovertxroofing.com/new-roof-cost-houston/">How Much Does a New Roof Cost in Houston?</a></li>
  <li><a href="https://allovertxroofing.com/signs-you-need-roof-repair-houston/">7 Signs You Need Roof Repair in Houston</a></li>
  <li><a href="https://allovertxroofing.com/roof-maintenance-checklist-houston/">Roof Maintenance Checklist for Houston Homeowners</a></li>
  <li><a href="https://allovertxroofing.com/how-long-roof-lasts-houston/">How Long Does a Roof Last in Houston?</a></li>
  <li><a href="https://allovertxroofing.com/best-roof-type-houston-homes/">Best Roof Type for Houston Homes: Asphalt vs Metal vs Tile</a></li>
  <li><a href="https://allovertxroofing.com/pros-cons-asphalt-shingles-houston/">Pros and Cons of Asphalt Shingles in Houston</a></li>
  <li><a href="https://allovertxroofing.com/roof-ventilation-houston-heat/">Roof Ventilation: Why It Matters in Houston Heat</a></li>
  <li><a href="https://allovertxroofing.com/roof-flashing-problems-repairs/">Roof Flashing Problems and Repairs in Houston</a></li>
  <li><a href="https://allovertxroofing.com/best-time-replace-roof-houston/">Best Time of Year to Replace a Roof in Houston</a></li>
  <li><a href="https://allovertxroofing.com/roof-repair-cost-houston/">How Much Does Roof Repair Cost in Houston?</a></li>
  <li><a href="https://allovertxroofing.com/repair-or-replace-roof-guide/">Should You Repair or Replace Your Roof?</a></li>
  <li><a href="https://allovertxroofing.com/prevent-roof-leaks-houston/">How to Prevent Roof Leaks in Houston Homes</a></li>
  <li><a href="https://allovertxroofing.com/roof-repair-rainy-season-houston/">Can a Roof Be Repaired During Rainy Season?</a></li>
  <li><a href="https://allovertxroofing.com/repair-vs-replacement-houston-guide/">Repair vs Replacement: Choosing Wisely in Houston</a></li>
  <li><a href="https://allovertxroofing.com/most-popular-asphalt-shingle-styles-houston/">Most Popular Asphalt Shingle Styles in Houston</a></li>
  <li><a href="https://allovertxroofing.com/will-asphalt-shingles-add-home-value-houston/">Will Asphalt Shingles Add Home Value to Your Home in Houston</a></li>
  <li><a href="https://allovertxroofing.com/most-popular-roof-type-houston/">Most Popular Roof Type in Houston</a></li>
  <li><a href="https://allovertxroofing.com/faqs-about-new-roofs-what-to-ask-about-a-new-roofing-project-in-houston/">FAQs About New Roofs: What to Ask About a New Roofing Projec</a></li>
  <li><a href="https://allovertxroofing.com/tips-choose-right-home-hunters-creek-village/">5 Tips to Help You Choose the Right Roof for Your Home in Hu</a></li>
  <li><a href="https://allovertxroofing.com/reasons-roof-replacement-houston/">The Top 6 Reasons Houston Residents Replace Their Roofs</a></li>
  </ul>
  <p class="ao-hub-cta">Prefere falar com um especialista? <a href="tel:+12818466665">(281) 846-6665</a> — inspeção gratuita.</p>
</div>
```


## Bloco — Metal Roofing (12 links) — colar na pillar https://allovertxroofing.com/metal-roofing-houston/

```html
<div class="ao-hub">
  <p class="ao-hub-title">Guias e recursos sobre Metal Roofing</p>
  <ul>
  <li><a href="https://allovertxroofing.com/metal-roofing-houston-tx-guide/">Metal Roofing in Houston, TX: Costs, Benefits, Installation</a></li>
  <li><a href="https://allovertxroofing.com/best-roofing-material-houston-heat/">Best Roofing Material for Houston Heat</a></li>
  <li><a href="https://allovertxroofing.com/metal-roof-cost-houston-2/">Metal Roof Cost in Houston: Price per Square Foot</a></li>
  <li><a href="https://allovertxroofing.com/pros-cons-metal-roofing-texas/">Pros and Cons of Metal Roofing in Texas</a></li>
  <li><a href="https://allovertxroofing.com/best-roof-colors-heat-reduction/">Best Roof Colors for Heat Reduction in Texas</a></li>
  <li><a href="https://allovertxroofing.com/metal-roofs-worth-investment-houston/">Are Metal Roofs Worth the Investment in Houston?</a></li>
  <li><a href="https://allovertxroofing.com/how-long-metal-roofs-last-the-woodlands/">How Long Do Metal Roofs Last in The Woodlands?</a></li>
  <li><a href="https://allovertxroofing.com/why-metal-roofs-are-green-choice/">Why Metal Roofs are a Green Choice</a></li>
  <li><a href="https://allovertxroofing.com/guide-standing-seam-metal-roofs/">Guide to Standing Seam Metal Roofs</a></li>
  <li><a href="https://allovertxroofing.com/matching-metal-roof-home-exterior-houston/">Matching Metal Roof to Home Exterior: How to Match Home Aest</a></li>
  <li><a href="https://allovertxroofing.com/pros-and-cons-of-metal-roofing/">Exploring the Pros and Cons of Metal Roofing: What Houston H</a></li>
  <li><a href="https://allovertxroofing.com/metal-roof-cost-houston/">What Can I Expect to Pay for a Metal Roof In Houston?</a></li>
  </ul>
  <p class="ao-hub-cta">Prefere falar com um especialista? <a href="tel:+12818466665">(281) 846-6665</a> — inspeção gratuita.</p>
</div>
```


## Bloco — Commercial Roofing (12 links) — colar na pillar https://allovertxroofing.com/commercial-roofing-houston/

```html
<div class="ao-hub">
  <p class="ao-hub-title">Guias e recursos sobre Commercial Roofing</p>
  <ul>
  <li><a href="https://allovertxroofing.com/commercial-roofing-houston-tx-guide/">Commercial Roofing in Houston, TX: Repairs and Maintenance</a></li>
  <li><a href="https://allovertxroofing.com/tpo-roofing-houston-tx-guide/">TPO Roofing in Houston, TX: Flat and Membrane Systems</a></li>
  <li><a href="https://allovertxroofing.com/flat-roofing-houston-tx-guide/">Flat Roofing in Houston, TX: Repair and Drainage</a></li>
  <li><a href="https://allovertxroofing.com/commercial-roof-repair-signs/">Top Signs Your Commercial Roof Needs Repair</a></li>
  <li><a href="https://allovertxroofing.com/flat-roof-maintenance-businesses/">Flat Roof Maintenance Tips for Houston Businesses</a></li>
  <li><a href="https://allovertxroofing.com/tpo-vs-epdm-roofing/">TPO vs EPDM Roofing: Which Membrane Wins?</a></li>
  <li><a href="https://allovertxroofing.com/roofing-small-businesses-houston/">Roofing for Small Businesses in Houston</a></li>
  <li><a href="https://allovertxroofing.com/how-choose-best-commercial-roofing-option-houston/">Covering Your Assets: How to Choose the Best Commercial Roof</a></li>
  <li><a href="https://allovertxroofing.com/top-tips-finding-perfect-houston-commercial-roof-contractor/">Top Tips for Finding the Perfect Houston Commercial Roof Con</a></li>
  <li><a href="https://allovertxroofing.com/commercial-roofing-faqs-answers-top-questions/">Commercial Roofing FAQs: Answers to Your Top Questions</a></li>
  <li><a href="https://allovertxroofing.com/importance-regular-commercial-roof-maintenance/">The Importance of Regular Commercial Roof Maintenance</a></li>
  <li><a href="https://allovertxroofing.com/dont-sign-a-contract-until-you-ask-these-6-commercial-roofing-questions/">Don’t Sign a Contract Until You Ask These 6 Commercial Roofi</a></li>
  </ul>
  <p class="ao-hub-cta">Prefere falar com um especialista? <a href="tel:+12818466665">(281) 846-6665</a> — inspeção gratuita.</p>
</div>
```


## Bloco — Siding (5 links) — colar na pillar https://allovertxroofing.com/siding-houston/

```html
<div class="ao-hub">
  <p class="ao-hub-title">Guias e recursos sobre Siding</p>
  <ul>
  <li><a href="https://allovertxroofing.com/top-questions-ask-siding-contractor-before-hiring/">Top Questions to Ask Your Siding Contractor Before Hiring</a></li>
  <li><a href="https://allovertxroofing.com/comparing-siding-types-home-exterior/">Comparing Siding Types for Your Home Exterior</a></li>
  <li><a href="https://allovertxroofing.com/popular-siding-types-discovering-top-choices-houston/">Popular Siding Types: Discovering the Top Choices in Houston</a></li>
  <li><a href="https://allovertxroofing.com/new-siding-cost-houston/">How Much Does New Siding Cost in Houston?</a></li>
  <li><a href="https://allovertxroofing.com/ways-new-siding-make-home-more-valuable/">Increasing Home Value: 7 Ways New Siding Can Make Your Home </a></li>
  </ul>
  <p class="ao-hub-cta">Prefere falar com um especialista? <a href="tel:+12818466665">(281) 846-6665</a> — inspeção gratuita.</p>
</div>
```


## Bloco — Gutters (3 links) — colar na pillar https://allovertxroofing.com/gutters-houston/

```html
<div class="ao-hub">
  <p class="ao-hub-title">Guias e recursos sobre Gutters</p>
  <ul>
  <li><a href="https://allovertxroofing.com/most-popular-gutter-style-houston/">Most Popular Gutter Style in Houston</a></li>
  <li><a href="https://allovertxroofing.com/why-seamless-gutters-superior-choice/">Sectional or Seamless: Why Seamless Gutters are the Superior</a></li>
  <li><a href="https://allovertxroofing.com/cost-install-new-gutters-houston/">What is the Cost to Install New Gutters in Houston?</a></li>
  </ul>
  <p class="ao-hub-cta">Prefere falar com um especialista? <a href="tel:+12818466665">(281) 846-6665</a> — inspeção gratuita.</p>
</div>
```


## Bloco — Windows (1 links) — colar na pillar https://allovertxroofing.com/window-replacement-houston/

```html
<div class="ao-hub">
  <p class="ao-hub-title">Guias e recursos sobre Windows</p>
  <ul>
  <li><a href="https://allovertxroofing.com/new-window-cost-in-houston/">New Window Cost in Houston</a></li>
  </ul>
  <p class="ao-hub-cta">Prefere falar com um especialista? <a href="tel:+12818466665">(281) 846-6665</a> — inspeção gratuita.</p>
</div>
```


## Bloco — Confiança & Contratação (13 links) — colar na pillar https://allovertxroofing.com/

```html
<div class="ao-hub">
  <p class="ao-hub-title">Guias e recursos sobre Confiança &amp; Contratação</p>
  <ul>
  <li><a href="https://allovertxroofing.com/choosing-roofing-companies-houston/">How to Choose Among Roofing Companies in Houston</a></li>
  <li><a href="https://allovertxroofing.com/roofing-contractor-houston-tx-guide/">Roofing Contractor in Houston, TX: What a Good One Does</a></li>
  <li><a href="https://allovertxroofing.com/roofers-in-houston-local/">Roofers in Houston: Local Help Near You</a></li>
  <li><a href="https://allovertxroofing.com/how-to-choose-roofing-contractor-houston/">How to Choose a Roofing Contractor in Houston</a></li>
  <li><a href="https://allovertxroofing.com/common-roofing-problems-texas/">Common Roofing Problems in Texas Homes</a></li>
  <li><a href="https://allovertxroofing.com/roof-inspection-before-buying-house/">Roof Inspection Checklist Before Buying a Houston House</a></li>
  <li><a href="https://allovertxroofing.com/gutter-installation-cost-houston/">Gutter Installation Cost in Houston</a></li>
  <li><a href="https://allovertxroofing.com/why-gutters-matter-roof-health/">Why Gutters Matter for Roof Health</a></li>
  <li><a href="https://allovertxroofing.com/roof-warranties-explained/">Roof Warranties Explained: Workmanship vs Manufacturer</a></li>
  <li><a href="https://allovertxroofing.com/professional-roof-inspection-includes/">What a Professional Roof Inspection Includes</a></li>
  <li><a href="https://allovertxroofing.com/how-often-roof-inspection-houston/">How Often Should Houston Homes Get a Roof Inspection?</a></li>
  <li><a href="https://allovertxroofing.com/roofer-near-me-houston-guide/">Roofer Near Me in Houston: What to Look For</a></li>
  <li><a href="https://allovertxroofing.com/benefits-hiring-local-roofing-company-houston/">7 Benefits of Hiring a Local Roofing Company in Houston</a></li>
  </ul>
  <p class="ao-hub-cta">Prefere falar com um especialista? <a href="tel:+12818466665">(281) 846-6665</a> — inspeção gratuita.</p>
</div>
```


## GUTTER (2 guias sem pillar)
Os 2 guias de gutter já linkam entre si e para o free-inspection. Quando a pillar
`/gutters-houston/` for criada, colar nela o bloco com estes 2 links + as 3 expansões
(most-popular-gutter-style-houston, why-seamless-gutters-superior-choice, cost-install-new-gutters-houston).
