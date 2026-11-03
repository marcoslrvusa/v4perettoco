# Audit Bing Ads — 28 dias (28/09–27/10/2026) + plano de otimização 48h

Fonte: export completo de 13 relatórios (28/10/2026) em `projetos/SEO/clientes/Premium Cleaning/Bing/`.
Campanha ativa: **[V4] [BING] [AQ] B2B Commercial Cleaning NJ NY** — budget $36/dia (MaxConversions, "Limited by budget").

## 1. Performance do período

| Métrica | Overall | Search | Audience Network |
|---|---|---|---|
| Impressões | 14.721 | 2.060 | 12.661 (86%) |
| Cliques | 117 | 77 | 40 |
| CTR | 0,79% | **3,74%** | 0,32% |
| CPC | $2,01 | $2,31 | $1,44 |
| Spend | $235,32 | $177,88 | $57,44 |
| Conversões | **2** (CPA $117,66) | 1 | 1 |

Leitura: o Search é 11x mais eficiente em CTR que o Audience. 86% das impressões saem da rede de audiência a 0,32%.

## 2. Os 12 gaps (prioridade de correção)

1. **Device bids invertidos** — Desktop: 89% das impressões (13.132), CTR 0,40%, CPC $2,89, $153,04 (65% do spend) e **bid adjustment +10%**. Mobile: CTR 4,11%, CPC $1,26, $79,14 — sem ajuste. Tablet: 56 impr, $3,14. Correção: Desktop −20% a −30%, Mobile +10–15%.
2. **Quinta-feira ausente** — Schedule Mon/Tue/Wed/Fri/Sat/Sun 08:00–21:00. Ads não rodam às quintas. Correção: adicionar Thursday.
3. **Horário não cobre comprador B2B noturno** — Restaurant/hotel GMs pesquisam fora do 8–21h. Correção: estender janela (23h) nas verticals; weekend CTR já prova demanda (Sáb 2,24%, Dom 3,63% vs 0,55–0,87% dias úteis).
4. **Audience Network drenando** — 12.661 impr a 0,32% CTR. Correção: pausar/restringir rede de audiência; 1 conversão saiu dali, mas o dreno pode migrar para Search.
5. **100% do tráfego → homepage** — 14.721 impressões com destination URL única `premiumcleaningnj.com/`. Correção: rotear por ad group (office → página office; restaurant → página restaurant; hotel → página hotel; core → hub comercial).
6. **480+ keywords de alta intenção pausadas** — Hotel Staffing & Boutiques (142 kws), Restaurants|Night Cleaning (186), Post-Construction (156). Exatamente os segmentos que vencem nos prompts AISV (hotel 165k/mês; hood 1k). Correção: reativar 10–15 kws top por ad group.
7. **Genéricos phrase-match devorando verba** — "commercial cleaning services" $64,37 (CTR 1,76%), "cleaning commercial companies" $26,35 (CTR 0,58% — query embaralhada), "cleaning companies commercial" $23,33. Correção: exact-match no core + negatives (residential, list, DIY, jobs, cheap/free).
8. **Conversão #1 = residencial (ICP errado)** — negócio residencial veio por keyword genérica/mobile. Correção: negative list residencial imediata (house cleaning, home cleaning, maid, housekeeper, cleaning lady, apartment).
9. **Zero extensões** — o relatório de assets mostra apenas Headlines (32) e Descriptions (15). Sem sitelinks, callouts, phone extension. Correção: sitelinks (serviços + case Madison), callouts (Since 2012 · ★5,0 43 reviews · Bonded & Insured · 98% retention), phone (973) 204-2310.
10. **Mensagem de desconto dentro de B2B premium** — "25% Off Your First Cleaning" 8.003 impr, CTR 0,37%, $49,61; "No Strangers In Your Office" 0,18%; "Free Office Assessment" 0,40%. Os vencedores são trust/emergência: "Licensed & Insured Team" 7,32%, "Offices, retail, medical spaces" 6,75% (1 conv), "24/7 Emergency Crews" 6,06%, "Same Crew Every Visit" 2,55%, "10+ Years" 2,88%, "Trusted by luxury retailers on Madison" 1,58% ($52,26). Correção: remover desconto dos RSAs B2B, cirurgia de copy por segmento.
11. **Geo com alvos mortos** — 152 locations cadastradas com bid adjustment 0% e **0 impressões** (84 zips NJ + 50 zips Manhattan). Enquanto isso, 86% do spend vazou para New York State ($161,39) + Manhattan ($40,85). Newark $24,89 · Jersey City $8,19 · Middlesex/Monmouth/Somerset/Union ≈ $0. Correção: reconstruir geo — NJ 5 counties ativos + corredor de luxo Manhattan (zips 100xx) com bid real.
12. **MaxConversions com 2 conv/28d** — algoritmo sem volume para aprender (Bing recomenda ≥15 conv/mês). Correção: TargetCPA inicial ~$95–110 ou ManualCPC enquanto o volume sobe; budget realocar de Audience/Desktop para Search/Mobile.

Extra (baixa severidade): cross-contamination de copy (RSA Restaurant com headline "Hotel Cleaning NJ & NYC"; RSA Hotel com "Commercial Cleaning NJ & NY"); AdStrength todos "Excellent" mas CTR real 0,39–0,95% (a força não reflete intenção); sem relatório de search terms no export (pedir na próxima extração); relatório de keyword sem coluna de conversões (sem atribuição por kw); Auction Insight: You IS 6,98%, abs top 3,30% vs angi 54%, homeadvisor 73,91%, thumbtack 47,73% — somos os maiores anunciantes e a pior posição.

## 3. Reposicionamento de audiência (as 2 conversões)

- **Conv #1 — residencial** (ICP errado): veio de genérico + mobile (CTR 4,11% mobile = comportamento de consumidor doméstico). Ação: negatives residenciais + cortar genéricos scramble. O investimento B2B não deve financiar lead residencial.
- **Conv #2 — comercial, perto de Madison Avenue, Manhattan** (boa): casa com o case Madison (luxury retail, $2.800/semana, retainer $145k/ano). Ação: criar ad group dedicado **"Manhattan Luxury Corridor"** — luxury retail cleaning NYC, flagship store cleaning, boutique hotel cleaning NYC, high end retail cleaning Manhattan, commercial cleaning New York City — roteado para a página NYC + prova do case; headline âncora "Trusted by luxury retailers on Madison" (melhor CTR entre as descritivas, 1,58%).

Tese: o dinheiro real está no corredor Manhattan (luxury retail/hospitality) + NJ B2B core. A campanha atual gasta 86% em NY sem nunca ter mirado lá deliberadamente — e a única conversão boa veio de onde o acaso jogou o tráfego.

## 4. Plano de 48h (2 dias)

### Dia 1 — parar o vazamento (~2h de execução)
1. Device bids: Desktop −25%, Mobile +10%.
2. Pausar Audience Network (manter Search).
3. Adicionar Thursday ao schedule; estender até 23h nas verticals restaurant/hotel.
4. Rotear destination URLs por ad group (homepage só no core).
5. Negatives residenciais + scramble (correção da conv #1).
6. Geo: ativar NJ 5 counties + zips 100xx Manhattan com bid +20% no corredor de luxo; remover alvos mortos.

### Dia 2 — construir o que converte (~2h)
7. Copy surgery: remover "25% Off" e headlines cruzadas; cada RSA só com copy do próprio segmento; novos headlines com os ângulos vencedores (trust/emergência/Madison).
8. Extensões: 6 sitelinks (Commercial, Office, Hotel, Restaurant, Pricing, Case Madison), callouts (Since 2012 · ★5,0/43 · Bonded & Insured · 98% retention), phone extension.
9. Reativar inventário pausado: Hotel Staffing (10–15 kws), Restaurant Night (10), Post-Construction (10) — mapeados aos prompts AISV.
10. Bidding: MaxConversions → TargetCPA $95 (revisar em 14 dias) ou ManualCPC $2,50 cap.
11. Conversões segmentadas: goals separados (form vs call) + tag residencial/comercial no lead para não repetir a conv #1.

## 5. Complemento estratégico (por que Bing importa no plano AIO/GEO)

O index do Bing alimenta ChatGPT Search e Copilot — rankear bem no Bing é também fronteira de citação IA. A campanha paga deve operar com a mesma disciplina da malha orgânica: rotear para páginas por intenção, mensagem de trust (não desconto), e geo onde o cliente real compra (Manhattan luxury + NJ B2B).

---

## Evidência das 2 conversões (prints recebidos 28/10/2026)

Dados reais confirmados nos prints. PII mascarado na página pública.

### Conversão 1 — residencial, fora do ICP
- CEP 08850 (Milltown, NJ — Middlesex County)
- Negócio: "Home" · Serviço pedido: "Other"
- Keyword: `commercial cleaning services`
- Ad group: Ad Group 1 — Commercial Cleaning Services (Core)
- Referrer: `ntp.msn.com` (syndication Microsoft) · Paid Search / CPC
- Leitura: tráfego de syndication + keyword genérica atraiu consumidor doméstico. Confirma negatives residenciais + corte de genéricos embaralhados.

### Conversão 2 — comercial/retail, dentro do ICP
- CEP 10044 (Manhattan — Roosevelt Island)
- Negócio: Celso de Lemos · Serviço pedido: **Retail Cleaning**
- Keyword: `commercial cleaning janitorial services`
- Ad group: Ad Group 1 — Commercial Cleaning Services (Core)
- Referrer: `search.yahoo.com` (rede Bing) · Paid Search / CPC
- Leitura: intenção B2B/retail em Manhattan, terreno do case Madison (luxury retail, $2.800/semana, ~$145k/ano). Justifica o ad group "Manhattan Luxury Corridor" roteado à página NYC + prova do case.

### Achado que fecha a tese do audit
Nas duas conversões o ad group foi **o mesmo (Core)** — ou seja, a conta não tem roteamento por intenção: o bom lead e o lead fora do ICP caem no mesmo destino (homepage). O gargalo não é volume, é segmentação e destination URL.
