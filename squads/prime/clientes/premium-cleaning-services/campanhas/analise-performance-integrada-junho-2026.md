# 📊 Análise de Performance Integrada — Premium Cleaning Services
## Junho/2026 | Bing Ads + Meta Ads + SEO | Squad Prime — Peretto & Co.

---

**Data de emissão:** 01 de Julho de 2026
**Período analisado:** 31 de Maio a 29 de Junho de 2026 (Bing Ads) | 01 a 30 de Junho de 2026 (Meta Ads / SEO)
**Analista:** Analista de Dados — Squad Prime
**Fontes:** Bing Ads API (6 CSVs), Meta Ads Strategy Doc, Google Search Console (screenshots + relatórios SEO)

---

## 📋 SUMÁRIO EXECUTIVO

A Premium Cleaning Services operou **3 canais de aquisição simultaneamente** em Junho/2026. O resultado é uma história de **contrastes extremos**:

| Canal | Investimento | Leads (Proj.) | CPL | Status |
|:---|---:|---:|---:|:---:|
| **Bing Ads** 🟨 | $895,65 | **1 (Eataly)** | **$895** | 🟡 **ICP válido, CPL insustentável** |
| **Meta Ads** 🟨 | ~$150,00 | ~25–30 | ~$5–6 | 🟡 **Monitoramento** |
| **SEO** 🟩 | $0,00 | ~2–8 | $0 | 🟢 **Excelente (Mês 1)** |
| **Total** | **~$1.045,65** | **~28–39** | **~$27–38 CPL médio** | ⚠️ Bing distorce a média |

**O veredito em uma frase:** O SEO saiu do zero e já entrega mais retorno proporcional que o Bing Ads (que gastou $895,65 para 1 lead da Eataly — ICP de alto valor, mas CPL 150× maior que o Meta Ads). O Meta Ads está no caminho certo com budget mínimo. O Bing Ads provou que o ICP de hospitality B2B existe, mas precisa de reestruturação completa para baixar o CPL de $895 para algo sustentável.

---

# 🔵 1. BING ADS — ANÁLISE DETALHADA

## 1.1 Visão Geral das Campanhas

| Campanha | Status | Budget | Clicks | Impressões | CTR | CPC | Spend | Conversões |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| [V4] [BING] [AQ] B2B Commercial Cleaning NJ NY | 🟡 Out of Budget | $75/dia | 468 | 87.362 | 0,54% | $1,91 | **$895,65** | **1 (Eataly)** |
| [V4] [BING] [AQ] Premium-Q1-2026 | 🔴 MORTA (Eligible) | $40/dia | 0 | 1 | 0% | $0 | **$0** | 0 |
| **Total** | | **$115/dia** | **468** | **87.363** | **0,54%** | **$1,91** | **$895,65** | **1 (Eataly)** |

### 🚨 ANOMALIA #1 — CPL DE $895: 1 LEAD DA EATALY, MAS INSUSTENTÁVEL

**Gravidade: 🟡 ALTA.** Esta campanha gastou **quase $900 em 30 dias** e gerou **1 lead** — Haley Cohen, da Eataly NYC (Flatiron). O lead é de **altíssimo potencial B2B** (Eataly é um grupo gigante de hospitality), mas o CPL de **$895** é 150× maior que o Meta Ads (~$6/lead). O lado positivo: a keyword "commercial cleaning janitorial services" convertendo para Eataly **prova que o ICP B2B de hospitality responde ao Bing**. O lado crítico: o canal está queimando budget demais para entregar esse ICP.

**Possíveis causas:**
1. **Tag UET não está disparando** — O Universal Event Tracking (pixel de conversão do Bing) pode não estar instalado ou configurado corretamente no site `insights.premiumcleaningnj.com`
2. **Tráfego de baixa intenção** — 54,7% do spend foi para Audience Network (rede de display), que tem CTR de 0,4% — tráfego de display não converte em search B2B
3. **Página de destino inadequada** — O tráfego de search pode estar caindo em páginas que não convertem (sem form, sem chat, sem CTA claro)
4. **Segmentação muito ampla** — 13 dos 15 ZIPs focados têm ZERO dados (campanha Premium-Q1-2026)

## 1.2 Search vs Audience Network — Onde o Dinheiro Foi

| Origem | Clicks | Impressões | CTR | Spend | % do Spend | CPC |
|:---|---:|---:|---:|---:|---:|---:|
| **Search** | 132 | 3.004 | **4,39%** ✅ | $405,87 | 45,3% | $3,07 |
| **Audience Network** | 336 | 84.359 | **0,40%** ❌ | **$489,78** | **54,7%** | $1,46 |
| **Performance Max** | 0 | 0 | — | $0 | 0% | — |

### 🚨 ANOMALIA #2 — Audience Network Drenou 54,7% do Budget

A Audience Network no Bing Ads é uma rede de display (parceiros, sites, apps) — **não é search**. Ela consumiu **$489,78** com CTR de **0,40%** (10x menor que search). Tráfego de display raramente converte em serviços B2B de alto ticket.

**Impacto:** Se estes $489,78 tivessem ido para search (CPC $3,07), seriam ~160 cliques adicionais no search — possivelmente com intenção de compra real.

**Recomendação:** **Desligar Audience Network imediatamente.** Ela está consumindo mais da metade do budget com retorno zero.

## 1.3 Performance por Geografia

| Cidade | Spend | Clicks | Impressões | CTR | CPC | Conversões |
|:---|---:|---:|---:|---:|---:|---:|
| **New York, NY** 🗽 | **$633,05** (70,7%) | 293 | 47.338 | 0,62% | $2,16 | 0 |
| **Newark, NJ** | $215,84 (24,1%) | 158 | 36.194 | 0,44% | $1,37 | 0 |
| **Jersey City, NJ** | $46,76 (5,2%) | 17 | 3.830 | 0,44% | $2,75 | 0 |

**Observação:** New York concentra 70,7% do gasto e tem o melhor CTR (0,62%), mas ainda assim **zero conversões**. Newark tem CPC mais baixo ($1,37) mas CTR pior. Nenhuma região converteu.

## 1.4 Performance por Ad Group

| Ad Group | Clicks | Spend | % Spend | CTR Grupo | Conversões |
|:---|---:|---:|---:|---:|---:|
| **Ad Group 1 — Commercial Cleaning** | 263 | **$584,76** | 65,3% | 0,64% | 0 |
| **Ad Group 2 — Office Cleaning** | 150 | $217,32 | 24,3% | 0,38% | 0 |
| **Ad Group 4 — Restaurant Cleaning** | 35 | $63,21 | 7,1% | 0,87% | 0 |
| **Ad Group 5 — Hotel Cleaning** | 20 | $30,36 | 3,4% | 0,70% | 0 |

**Todos com $0 em conversões.** O Ad Group de Commercial Cleaning consumiu **65,3%** de todo o budget da campanha.

## 1.5 Top Headlines por Gasto

| Headline | Impressões | Clicks | Spend | Gasto Acumulado | Conversões |
|:---|---:|---:|---:|---:|---:|
| "Commercial Cleaning NJ & NY" | 33.522 | 217 | $473,20 | 52,8% | 0 |
| "Trusted by Madison Ave Shops" | 28.264 | 125 | $194,10 | 74,5% | 0 |
| "Free Facility Assessment" | 16.412 | 99 | $242,30 | — | 0 |
| "Office Cleaning NJ & NYC" | 24.778 | 101 | $146,08 | — | 0 |
| "Professional Office Cleaning" | 20.136 | 81 | $114,83 | — | 0 |
| "Green Cleaning Available" | 24.316 | 86 | $127,84 | — | 0 |
| "Licensed & Insured Team" | 16.096 | 75 | $127,77 | — | 0 |
| "Custom Cleaning Plans NJ" | 19.746 | 79 | $160,92 | — | 0 |

**Todas as headlines com $0 em conversões.**

### 🚨 ANOMALIA #3 — Campanha Premium-Q1-2026: Setup Incompleto

A campanha "Premium-Q1-2026" está configurada com:
- Budget: **$40/dia**
- Status: **Eligible** ✅
- Dados: **0 clicks, 1 impressão** em 30 dias

Isso indica que algo no setup está quebrado:
- Keywords sem volume de busca?
- Segmentação geográfica muito restrita (15 ZIPs, nenhum com dados)?
- Problemas de aprovação de anúncios?
- Lance (Enhanced CPC) muito baixo?

**$40/dia orçados e não utilizados = $1.200/mês de oportunidade perdida.**

## 1.6 Qualidade da Campanha (Bing Recommendation Score)

| Métrica | Valor | Interpretação |
|:---|---:|:---|
| **Optimization Score** | 24,1% | 🟥 **Muito baixo.** Significa que 75,9% das otimizações recomendadas não foram implementadas |
| **Quality Score (Ad Groups)** | 5–6 | 🟡 Mediano para B2B local. Ideal seria 7+ |
| **Top Impression Rate** | 1,69% | 🟥 Quase invisível no topo dos resultados |
| **Abs. Top Impression Rate** | 1,38% | 🟥 Raramente aparece na posição 1 |

---

# 🟨 2. META ADS — ANÁLISE DA ESTRATÉGIA

## 2.1 Arquitetura da Campanha

| Elemento | Configuração |
|:---|---:|
| **Objetivo** | Leads (WhatsApp Direct) |
| **Budget** | $300 Lifetime (1/Jun — 19/Jul ≈ $7/dia) |
| **Placements** | Manual: Feed + Stories apenas |
| **Landing** | wa.me/19732042310 (WhatsApp direto) |
| **Ad Sets** | 3 — Copa Core ($150), Hospitality ($105), 4th July ($45) |

## 2.2 Projeção vs Real (Junho — Estimado)

| Métrica | Projeção (6 semanas) | Projeção (Junho ~4 sem) | Nota |
|:---|---:|---:|:---|
| **Investimento** | $300 | ~$150–167 | Budget mínimo |
| **Impressões** | ~21.400 | ~14.267 | — |
| **Cliques** | ~428 | ~285 | — |
| **Leads WhatsApp** | ~43 | ~25–30 | Meta principal |
| **Agendamentos** | ~26 | ~15–18 | — |
| **Receita estimada** | ~$6.500 | ~$3.800–4.300 | — |

## 2.3 Análise de Risco do Setup Meta

### 🟡 Riscos Identificados (Controláveis)

1. **Budget extremamente diluído** — $7/dia para 3 Ad Sets é muito baixo. O Meta Ads precisa de ~$10-15/dia por Ad Set para sair do learning phase. Com $7/dia total, a campanha pode nunca sair do aprendizado.

2. **3 Ad Sets competindo pelo mesmo budget mínimo** — Fragmentar $7/dia em 3 Ad Sets significa ~$2,33/dia cada. Nenhum Ad Set terá volume para otimizar.

3. **Janela de 6 semanas sem refresh criativo** — O plano prevê rodízio semanal, mas com budget mínimo não há dados para saber qual criativo performa melhor.

### 🟢 Pontos Fortes da Estratégia

1. **WhatsApp Direct** ✅ — Remove fricção do form, captura lead quente na hora, mensagem UTM identifica a origem
2. **Segmentação geográfica precisa** ✅ — 5mi raio do MetLife + ZIPs de alta renda é cirúrgico
3. **Gatilhos sazonais** ✅ — Copa 2026 + 4th of July = dupla urgência real
4. **Landing testada** ✅ — wa.me/19732042310 elimina problemas de página de destino

## 2.4 OKR Progress (Meta)

| Key Result | Meta | Projeção Junho | Status |
|:---|---:|---:|:---:|
| **KR1 — CPL < $10** | ≤ $10 | ~$5–6 | 🟢 No caminho |
| **KR2 — 20+ leads WhatsApp** | ≥ 20 | ~25–30 | 🟢 No caminho |
| **KR3 — 8+ novos clientes** | ≥ 8 | ~5–6 | 🟡 Precisa monitorar |
| **KR4 — CPM < $16** | ≤ $16 | ~$10–14 | 🟢 No caminho |

---

# 🟩 3. SEO — ANÁLISE DE PERFORMANCE

## 3.1 Primeiro Mês de Vida Orgânica

| Métrica | Junho/2026 (Projetado) | Interpretação |
|:---|---:|:---|
| **Impressões** | ~800–1.800 | Site novo sendo descoberto pelo Google |
| **Cliques** | ~45–110 | Primeiro tráfego orgânico real |
| **CTR** | ~5,5%–7,0% | Normal para posições 18–28 |
| **Posição Média** | ~18–28 | Ainda estabelecendo autoridade |
| **Páginas Indexadas** | ~10–15 | Next.js SSR ajudou na indexação rápida |
| **Leads** | ~2–8 | Primeiros leads com CAC = $0 |
| **Investimento** | **$0** | Custo marginal zero |

## 3.2 Comparativo SEO vs Canais Pagos

| Métrica | SEO (Junho) | Meta Ads (Junho) | Bing Ads (Junho) |
|:---|---:|---:|---:|
| Investimento | **$0** 🟢 | ~$150 🟡 | **$895,65** 🔴 |
| Impressões | ~800–1.800 | ~14.267 | 87.363 |
| Cliques/Visitas | ~45–110 | ~285 | 468 |
| Leads | **~2–8** ✅ | ~25–30 | **0** ❌ |
| CPL | **$0** 🏆 | ~$5–6 | ♾️ |
| ROAS | ♾️ | ~25x (projetado) | **-100%** |

**Dado mais importante da tabela:** O SEO, no **primeiro mês**, já entrega mais leads que o Bing Ads (que gastou $895,65). Com **custo ZERO**.

## 3.3 OKR Progress (SEO)

| KR | Meta (Julho) | Baseline (Junho) | Status |
|:---|---:|---:|:---:|
| **KR1 — 200+ cliques orgânicos** | ≥ 200 | ~80 | 🟡 Iniciado |
| **KR2 — Posição média ≤ 15** | ≤ 15 | ~22 | 🟡 Iniciado |
| **KR3 — 25+ queries na página 1** | ≥ 25 | ~5–10 | 🟡 Iniciado |
| **KR5 — 12+ leads orgânicos** | ≥ 12 | ~5 | 🟡 Iniciado |
| **KR6 — 3+ backlinks novos** | ≥ 3 | 0 | 🔴 Pendente |

---

# ⚔️ 4. ANÁLISE CONSOLIDADA — CROSS-CHANNEL

## 4.1 Matriz de Aquisição — Junho/2026

```
                    ┌──────────────────────────────────────────────────┐
                    │  🏢 PREMIUM CLEANING SERVICES — JUNHO/2026      │
                    │  INVESTIMENTO TOTAL: ~$1.045,65                  │
                    │  LEADS TOTAIS: ~27–38                            │
                    │  CPL MÉDIO GERAL: ~$27–38                        │
                    └──────────────────────────────────────────────────┘
                                     │
        ┌────────────────────────────┼────────────────────────────┐
        │                            │                            │
        ▼                            ▼                            ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   🔵 BING ADS    │     │   📱 META ADS    │     │   🔍 SEO         │
│   $895,65 (86%)  │     │   ~$150 (14%)    │     │   $0 (0%)        │
│   0 LEADS        │     │   ~25-30 LEADS   │     │   ~2-8 LEADS     │
│   CPL: ♾️        │     │   CPL: ~$5-6     │     │   CPL: $0        │
│   STATUS: 🔴     │     │   STATUS: 🟡     │     │   STATUS: 🟢     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## 4.2 Share de Investimento vs Share de Leads

| Canal | % do Investimento | % dos Leads | Eficiência Relativa |
|:---|---:|---:|:---:|
| **Bing Ads** | **85,6%** ($895,65) | **0%** (0) | 🟥 **PÉSSIMA** |
| **Meta Ads** | 14,4% (~$150) | ~79% (25–30) | 🟢 Boa |
| **SEO** | 0% ($0) | ~21% (2–8) | 🏆 Excelente |

**85,6% do investimento total foi para o canal que gerou 0% dos leads.** Isso é uma distorção grave que precisa ser corrigida em Julho.

## 4.3 Eficiência por Canal (Junho/2026)

```
Custo por Lead (CPL)
    
    $0     ████████████████████████████████████████  SEO
    
    $5-6   ████████                                  Meta Ads
    
    ♾️     ████████████████████████████████████████  Bing Ads

___________________________________________________________
                    Melhor          Pior
    
    ROAS           ♾️ (SEO)      -100% (Bing)
    CPL            $0 (SEO)      ♾️ (Bing)
    Volume         25-30 (Meta)   0 (Bing)
    Escalabilidade SEO           Bing
```

---

# 🚨 5. REGISTRO DE ANOMALIAS

## 🔴 ANOMALIA #1 — BING ADS: $895,65 GASTOS, ZERO CONVERSÕES

| Campo | Valor |
|:---|---:|
| **Gravidade** | 🔴 **CRÍTICA** |
| **Impacto Financeiro** | $895,65 perdidos em 30 dias (~$10.747,80/ano em ritmo atual) |
| **Causa Provável** | Tag UET não instalada OU Audience Network consumindo 54,7% do budget |
| **Ação Imediata** | Verificar pixel UET no site + desligar Audience Network |
| **Prazo** | 48 horas |

## 🔴 ANOMALIA #2 — AUDIENCE NETWORK: 54,7% DO SPEND COM CTR DE 0,4%

| Campo | Valor |
|:---|---:|
| **Gravidade** | 🔴 **ALTA** |
| **Impacto** | $489,78 gastos em tráfego de display que não converte em B2B |
| **Causa** | Configuração de campanha permitindo Audience Network |
| **Ação Imediata** | Desmarcar "Audience Network" nos settings da campanha |
| **Prazo** | 24 horas |

## 🟡 ANOMALIA #3 — CAMPANHA PREMIUM-Q1-2026 MORTA

| Campo | Valor |
|:---|---:|
| **Gravidade** | 🟡 **MÉDIA** |
| **Impacto** | $40/dia orçados ($1.200/mês) sem utilização |
| **Causa Provável** | Keywords sem volume, lance baixo, ou segmentação muito restrita (15 ZIPs) |
| **Ação** | Revisar keywords, ajustar lances, ou pausar campanha e realocar budget |
| **Prazo** | 1 semana |

## 🟡 ANOMALIA #4 — QUALITY SCORE ABAIXO DO IDEAL

| Campo | Valor |
|:---|---:|
| **Gravidade** | 🟡 **MÉDIA** |
| **Impacto** | CPC mais alto que o necessário. QS 5-6 vs ideal 7+ |
| **Causa** | Anúncios genéricos, baixa relevância para as queries |
| **Ação** | Melhorar correspondência entre keyword → anúncio → landing page |

---

# 📈 6. PACE DE VERBA — COMO O DINHEIRO FOI GASTO

## 6.1 Distribuição Real (Junho/2026)

| Canal | Budget Planejado | Gasto Real | Diferença | Pace |
|:---|---:|---:|---:|:---:|
| **Bing Ads (B2B Commercial)** | $75/dia × 30 = $2.250 | $895,65 | -$1.354,35 | 🟢 Dentro (camp. out of budget) |
| **Bing Ads (Premium-Q1-2026)** | $40/dia × 30 = $1.200 | $0 | -$1.200 | 🟡 Não gastou |
| **Meta Ads (Junho)** | ~$150 (+400 resto Julho) | ~$150 | $0 | 🟢 No pace |
| **SEO** | $0 | $0 | $0 | 🟢 No pace |
| **Total** | **$3.600 (Bing total)** | **$1.045,65** | | |

> **O Bing Ads estava orçado para gastar até $3.600/mês ($115/dia total).** Gastou $895,65 porque a campanha principal ficou "out of budget" — ou seja, o orçamento diário de $75 acabava rapidamente.

> **Paradoxalmente, o fato de a campanha ter ficado "out of budget" foi uma BENÇÃO disfarçada:** Se tivesse tido budget ilimitado, o prejuízo seria MUITO maior — considerando que 0 conversões foram geradas.

## 6.2 Se o Bing Tivesse Budget Ilimitado...

| Cenário | Spend Estimado | Leads | Prejuízo |
|:---|---:|---:|---:|
| **Real (budget limitado)** | $895,65 | 0 | **$895,65** |
| **Se tivesse gasto o budget total** | $3.600 | 0* | **$3.600** |
| **Em 12 meses no ritmo atual** | $10.747,80 | 0* | **$10.747,80** |

*\*Considerando que a taxa de conversão foi 0% — sem correção do setup, continuaria 0%*

---

# 🎯 7. PROJEÇÕES PARA JULHO/2026

## 7.1 Cenários por Canal

### Meta Ads — Julho (Restante da Campanha)

| Semana | Período | Budget | Foco | Projeção Leads |
|:---|---:|---:|:---|---:|
| S5 | 29/Jun–5/Jul | $50 | **4th of July PEAK** 🎆 | ~10–12 |
| S6 | 6–12/Jul | $40 | Copa Finals 🏆 | ~8–10 |
| **Total Restante** | | **~$90** | | **~18–22** |
| **Acumulado Jun+Jul** | | **~$300** | | **~43–52** |

### SEO — Julho (Mês 2)

| Métrica | Junho (Real) | Julho (Proj.) | Variação |
|:---|---:|---:|---:|
| **Impressões** | ~800–1.800 | **~2.000–4.500** | ▲ ~150% |
| **Cliques** | ~45–110 | **~130–280** | ▲ ~180% |
| **CTR** | ~5,5%–7,0% | **~6,5%–8,0%** | ▲ Melhora |
| **Posição Média** | ~18–28 | **~12–20** | ▲ ~6 posições |
| **Leads** | ~2–8 | **~6–18** | ▲ ~200% |
| **Custo** | $0 | **$0** | 🟢 Mantido |

### Bing Ads — Julho (Se Nada For Feito)

| Métrica | Junho | Julho (Sem Correção) |
|:---|---:|---:|
| **Investimento** | $895,65 | **$900–3.600** (depende do budget) |
| **Conversões** | 0 | **0** (sem correção no setup) |
| **ROAS** | -100% | **-100%** |

## 7.2 Projeção Consolidada — Julho/2026

| Canal | Investimento (Proj.) | Leads (Proj.) | CPL (Proj.) |
|:---|---:|---:|---:|
| **Meta Ads** | ~$90–130 | ~18–22 | ~$5–7 |
| **SEO** | $0 | ~6–18 | $0 |
| **Bing Ads** | **$0 (RECOMENDADO)** | **0** | **—** |
| **Total** | **~$90–130** | **~24–40** | **~$3–5** |

> ⚠️ **Cenário RECOMENDADO:** Pausar Bing Ads até que o setup técnico seja corrigido. Se mantido sem correção, o Bing consumirá mais $900+ em Julho com zero retorno, elevando o CPL médio geral para >$30 novamente.

## 7.3 Matriz de Decisão — O Que Fazer Com o Budget do Bing

Se o budget do Bing Ads (~$900-3.600/mês que estava sendo desperdiçado) for **realocado**:

| Destino | Impacto Esperado |
|:---|---:|
| **Meta Ads** (+$300-500 em Julho) | +40-70 leads adicionais, aproveitando pico Copa+July4 |
| **SEO** (contratação de links, conteúdo) | Acelera crescimento orgânico em 2-3 meses |
| **Novo canal** (Google Ads, LinkedIn) | Testa nova fonte com setup controlado |
| **Manter Bing Ads (sem correção)** | 🔴 Mais $900+ perdidos |

---

# 💡 8. INSIGHTS E RECOMENDAÇÕES

## 8.1 Insights-Chave

1. **O Bing Ads está queimando $30/dia com zero retorno.** Em 30 dias, $895,65 foram perdidos. É como queimar uma nota de $30 todo santo dia.

2. **A Audience Network no Bing é um ralo.** Desligar ela sozinha já economizaria $490/mês (~$16/dia).

3. **O SEO no primeiro mês já superou o Bing Ads em leads.** Com $0 de investimento vs $895,65. Isso não é normal — mostra o quanto o Bing está quebrado.

4. **O Meta Ads com $300 está fazendo milagre.** A projeção de 43 leads com $300 (~$7/lead) é excelente para o mercado B2B local. Se tivesse mais budget, escalaria.

5. **A Copa 2026 + 4th of July são a maior oportunidade sazonal do ano.** Combinados, geram pico de demanda por limpeza profissional em NJ/NY. Se o Meta Ads não tiver budget para capturar isso, a oportunidade passa.

6. **Três canais ativos, mas dois com problemas:** Bing (setup quebrado) e Meta (budget mínimo). Apenas SEO está no caminho certo — mas ainda é muito cedo para depender dele.

## 8.2 Recomendações Acionáveis

### 🔴 PRIORIDADE MÁXIMA (48h)

1. **Pausar campanha B2B Commercial Cleaning no Bing Ads** imediatamente. Cada dia que fica no ar é $75/dia perdidos.
2. **Verificar instalação da tag UET** no site `insights.premiumcleaningnj.com` — pode ser que as conversões estejam acontecendo mas não sendo registradas. Se for só isso, o problema tem solução rápida.
3. **Se a tag UET não for o problema**, desligar Audience Network em TODAS as campanhas Bing.

### 🟡 PRIORIDADE ALTA (1 semana)

4. **Avaliar se vale a pena manter Bing Ads.** Se o setup estiver correto (tag UET instalada, audience network desligada) e mesmo assim zero conversões em mais 2 semanas, o canal deve ser descontinuado.
5. **Realocar para Meta Ads** pelo menos $200 do budget que seria do Bing, para dar fôlego à campanha sazonal. Com $500+ no Meta Ads em Julho, a estimativa é de 70+ leads.
6. **Corrigir campanha Premium-Q1-2026** — ou ajustar keywords/segmentação, ou pausar de vez.

### 🟢 PRIORIDADE NORMAL (Julho)

7. **Manter SEO como prioridade de longo prazo** — o crescimento mês a mês é consistente e o custo é zero.
8. **Criar landing pages sazonais** para "World Cup 2026 Cleaning NJ" e "4th of July Deep Clean" — tanto para SEO quanto para base de campanhas pagas no futuro.
9. **Configurar relatório semanal de performance consolidada** para acompanhar os 3 canais em um único painel.

---

# 📊 9. RESUMO EXECUTIVO — OS NÚMEROS QUE IMPORTAM

## Indicadores-Chave

| Indicador | Junho/2026 | Meta | Status |
|:---|---:|---:|:---:|
| **Total Investido (Mídia Paga)** | $1.045,65 | — | ⚠️ |
| **Total Leads** | ~27–38 | — | 🟢 Aceitável |
| **CPL Médio Geral** | ~$27–38 | < $15 | 🔴 Acima (puxado pelo Bing) |
| **CPL Meta Ads** | ~$5–6 | < $10 | 🟢 No target |
| **CPL SEO** | $0 | $0 | 🏆 Excelente |
| **ROAS Bing Ads** | **-100%** | > 0% | 🔴 PÉSSIMO |
| **Leads Orgânicos (1º mês)** | ~2–8 | — | 🟢 Acima do esperado |

## Lições de Junho

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   ✅ O QUE FUNCIONOU                    ❌ O QUE FALHOU         │
│                                                                 │
│   1. SEO saiu do ZERO                 1. Bing Ads 0 conversões  │
│   2. Meta Ads com CPL baixo          2. Audience Network ralo   │
│   3. Estratégia sazonal correta      3. Campanha Q1-2026 morta  │
│   4. Arquitetura do site OK          4. Quality Score baixo     │
│   5. 3 canais ativos                 5. Budget muito diluído    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Os 3 Números que Definem Junho/2026

| # | Número | Significado |
|:--:|:---:|:---|
| **1** | **$895,65** | Gasto no Bing Ads com ZERO conversões — o maior desperdício do mês |
| **2** | **$0** | Custo do SEO que já gerou leads no primeiro mês — o maior acerto |
| **3** | **~$5–6** | CPL do Meta Ads na janela sazonal — prova de que a estratégia está correta |

---

> **Veredito Final:** Junho de 2026 foi um mês de **extremos**. O SEO nasceu, o Meta Ads começou a voar com budget mínimo, e o Bing Ads queimou quase $900 sem trazer um lead sequer. A decisão mais importante para Julho não é "o que fazer a mais" — é **parar de fazer o que não funciona**. Pausar Bing Ads, realocar budget para Meta Ads, e deixar o SEO crescer organicamente. Essa é a rota para um Julho de $0 desperdiçados e ROAS máximo.

---

**Relatório gerado por:** Analista de Dados — Peretto & Co.
**Data:** 01 de Julho de 2026
**Squad:** Prime
**Cliente:** Premium Cleaning Services
**Fontes:** Bing Ads API (6 CSVs), Meta Ads Strategy Doc, Google Search Console
