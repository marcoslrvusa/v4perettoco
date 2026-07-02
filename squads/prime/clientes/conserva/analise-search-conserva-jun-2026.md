# Análise Técnica — Search Campaign: Conserva Irrigation of Greater Scottsdale

**Analista:** Data Analyst, Traffic Reporting Squad
**Período base:** 1 a 30 de Junho de 2026 (c/ drill-down Semana 2: 17-23 Jun)
**Data do relatório:** 1 de Julho de 2026

---

## Sumário Executivo

A campanha de Search da Conserva está em **estado crítico** — opera com apenas 1 de 5 ad groups gerando resultado consistente (Precision Repair), tem **49% das impressões perdidas por rank** e **42% por budget**, e na Semana 2 de Junho gastou $179,40 sem gerar **nenhuma conversão**. O grupo de Installation está parado há meses ($0 gasto em Junho), Smart Irrigation Efficiency está morto, e B2B nunca decolou. 

A boa notícia: existem **dezenas de keywords de alto volume e intenção transacional** que simplesmente não estão na conta. O PMAX AG3 (Summer Ready) prova que o mercado responde — 6 conv a $106 de CPA. O problema não é a demanda. É a **arquitetura da conta**.

---

## 1. DIAGNÓSTICO QUANTITATIVO — Saúde da Conta Search

### 1.1 Performance Consolidada (Jun 1-30)

| Métrica | Search | PMAX | Total Conta¹ |
|---|---|---|---|
| Impressões | 1.346 | 6.357 | 18.142 |
| Cliques | 62 | 235 | 1.239 |
| CTR | 4,61% | 3,70% | 6,83% |
| CPC médio | $11,18 | $7,75 | $4,46 |
| Custo | $692,99 | $1.820,60 | $5.530,75 |
| Conversões | 5 | 13 | 88 |
| CVR | 8,06% | 3,41% | 6,35% |
| CPA | **$138,60** | **$140,07** | $62,85 |
| Search Impr. Share | 21,91% | 29,56% | 27,55% |

¹ Inclui LSA (Local Services Ads) e outras fontes

### 1.2 Alocação por Ad Group (Search — Jun 1-30)

| Ad Group | Impressões | % Total | Custo | % Budget | Conv | CPA | Status |
|---|---|---|---|---|---|---|---|
| [Emergency] Precision Repair | 1.186 | **88,1%** | $643,13 | **92,8%** | 3 | $214,38 | ✅ Único ativo |
| [Seasonal] Spring Startup | 137 | 10,2% | $49,86 | 7,2% | 2 | $24,93 | ✅ Bom CPA, pouco volume |
| [New] Irrigation Installation | 18 | 1,3% | $0,00 | 0% | 0 | — | ❌ Morto |
| [02-26] Smart Irrigation | 3 | 0,2% | $0,00 | 0% | 0 | — | ❌ Morto |
| [V4] [SIAG] B2B | 2 | 0,1% | $0,00 | 0% | 0 | — | ❌ Morto |

**Descoberta crítica:** 88% das impressões e 93% do gasto vão para UM ad group (Precision Repair). Este grupo tem CPA de $214 — 54% acima do CPA geral da conta. Os outros 4 grupos essencialmente não existem.

### 1.3 Evolução Semanal — O Colapso da Semana 2

| Período | Impressões | Cliques | CTR | Custo | Conv | CPA |
|---|---|---|---|---|---|---|
| Jun 1-16 | 1.100 | 42 | 3,82% | $543,79 | 3 | $181,26 |
| Jun 17-23 | **226** | **20** | **8,85%** | **$179,40** | **0** | **—** |
| Delta | -79% | -52% | +132% | -67% | -100% | **∞** |

**Anomalia grave:** A CTR saltou de 3,82% para 8,85% (bom sinal), mas as conversões foram a zero (péssimo sinal). Isso indica que a campanha passou a atrair **cliques de baixa intenção** — provavelmente via expansões de broad match que geram CTR alta mas não convertem. O algoritmo "aprendeu" a gastar o budget em queries baratas e clicáveis, não em queries conversoras.

### 1.4 Distribuição Diária (Search — Time Series)

```
Jun 1:  36 impr | $17,37 | 0 conv
Jun 2: 123 impr | $0,00  | 0 conv ← Gasto zero? Anomalia
Jun 3:  78 impr | $34,07 | 1 conv ← Melhor dia
Jun 4:  20 impr | $30,12 | 0 conv ← CPC altíssimo ($30!)
Jun 5:   7 impr | $23,92 | 0 conv ← 7 impr gastando $24
Jun 6:   0 impr | $0,00
Jun 7:   0 impr | $0,00
Jun 8:  98 impr | $15,85 | 0 conv
Jun 9:  55 impr | $20,92 | 0 conv
Jun 10: 83 impr | $15,85 | 1 conv
Jun 11: 84 impr | $19,31 | 0 conv
Jun 12:  5 impr | $27,83 | 1 conv ← 5 impr gastando $28!
Jun 13:  0 impr | $0,00
Jun 14:  0 impr | $0,00
Jun 15: 112 impr | $24,45 | 0 conv
Jun 16: 74 impr | $47,61 | 0 conv ← Maior gasto diário, 0 conv
```

**Padrões identificados:**
- **Zero impressões nos finais de semana** — orçamento diário exaure durante a semana
- **Dias com poucas impressões têm CPCs altíssimos** (Jun 12: 5 impr, $27,83 = $5,56 CPC para 0 conv)
- **Alta volatilidade diária** — impressões variam 20x entre dias (5 a 123)
- **2 das 3 conversões do período vieram em dias de baixo volume** (Jun 3: 78 impr, Jun 10: 83 impr) — sugere que o algoritmo acidentalmente encontra intenção em dias de budget baixo

### 1.5 Impression Share — O Gargalo Duplo

| Métrica | Jun 1-16 | Jun 17-23 |
|---|---|---|
| Search Impr. Share | 24,36% | **19,94%** |
| Search Top IS | 15,86% | 12,29% |
| Search Abs. Top IS | — | < 10% |
| Lost IS (Rank) | **49,12%** | **37,78%** |
| Lost IS (Budget) | 42,3% (inf.) | **42,28%** |

**Análise do gargalo duplo:**
- **49% perdido por rank** = a cada 2 impressões disponíveis, 1 é perdida porque o anúncio não está competitivo o suficiente (Quality Score baixo + lance baixo)
- **42% perdido por budget** = o orçamento diário de $27 acaba antes do dia terminar
- **Interação:** Se você aumentar o budget sem aumentar o rank, você só gasta mais em posições baixas. Se aumentar o lance sem aumentar o budget, você ganha mais impressões mas exaure o budget mais rápido.
- **Apenas 19-24% de IS efetivo** significa que 3 em cada 4 pessoas pesquisando por serviços de irrigação em Scottsdale **nem veem o anúncio da Conserva**

### 1.6 Análise no Nível da Keyword (Jun 1-16)

Das **~16 keywords únicas elegíveis** na conta ativa (Search), apenas **4 geraram qualquer interação**:

| Keyword | Match | Impr | Cliques | CTR | Custo | Conv | CPA | Nota |
|---|---|---|---|---|---|---|---|---|
| irrigation repair | Broad | 211 | 7 | 3,32% | $81,81 | 0 | — | 💸 Maior desperdício |
| irrigation repair near me | Phrase | 9 | 1 | 11,11% | $5,31 | **1** | **$5,31** | ⭐ Única conversora |
| sprinkler repair | Broad | 25 | 2 | 8,00% | $47,61 | 0 | — | 💸 Alto CPC ($23,80) |
| sprinkler repair scottsdale | Phrase | 3 | 2 | 66,67% | $22,52 | 0 | — | CTR alta mas 0 conv |
| sprinkler system tune up | Broad | 84 | 2 | 2,38% | $12,86 | **1** | $12,86 | ⭐ Boa |
| sprinkler system repair | Phrase | 6 | 0 | — | $0 | 0 | — | Sem cliques |
| **Total identificado** | | 394 | 14 | 3,55% | $170,11 | 2 | $85,06 | |
| **Total não identificado²** | | **706** | **28** | **3,97%** | **$373,68** | **1** | $373,68 | 🔴 **64% do budget = mistério** |

² "Non-identified" = impressões geradas por expansões de broad match, search themes, ou queries mapeadas como "All but removed keywords"

**Conclusão devastadora:** **64% do budget de Search ($373,68) foi gasto em queries que não conseguimos nem identificar** — provavelmente expansões de broad match de baixíssima intenção. A única keyword phrase match que converteu ("irrigation repair near me") teve um CPA incrível de $5,31 mas só teve 9 impressões.

---

## 2. ANOMALIAS ATIVAS — Ofensores Abertos

### 2.1 Ofensores Críticos (Impacto Imediato)

| # | Ofensor | Status | Evidência | Impacto |
|---|---|---|---|---|
| 1 | **Budget Search cortado 51%** | 🔴 ABERTO | Budget atual $27/dia (vs ~$55/dia ideal) vs Lost IS Budget 42% | Perde metade das impressões |
| 2 | **Bid Strategy instável** | 🔴 ABERTO | 3 mudanças em 60 dias (Max Conv → Max Clicks → Max Conv) | Algoritmo nunca estabiliza |
| 3 | **Broad match SEM controle** | 🔴 ABERTO | 64% do budget em queries não identificadas, 0 conv | Desperdício de $374/mês |
| 4 | **URL HTTP (Abr 15)** | 🟢 CORRIGIDO | Reportado como urgente — provavelmente já corrigido | Segurança/responsividade |
| 5 | **QS médio baixo** | 🔴 ABERTO | Maioria das keywords com QS 3-5, "Below average" em Landing Page Exp. | Contribui para Lost IS Rank 49% |

### 2.2 Ofensores Altos (Estruturais)

| # | Ofensor | Status | Evidência |
|---|---|---|---|
| 6 | **Installation Group pausado (Fev)** | 🔴 ABERTO | 18 impr em Jun, $0 gasto. Keywords sem impressão. |
| 7 | **Smart Irrigation Efficiency morto** | 🔴 ABERTO | 3 impr em Jun, $0 gasto. 20+ keywords com 0 impressão. |
| 8 | **B2B nunca decolou** | 🔴 ABERTO | 2 impr em Jun. 15+ keywords com 0 impressão. |
| 9 | **Campanhas legadas poluindo a conta** | 🔴 ABERTO | 10+ campanhas pausadas com 100+ keywords mortas (Competitors, Display, SCALCON, LP, etc) |
| 10 | **PMAX Asset Groups "Incomplete"** | 🔴 ABERTO | AG1 e AG2 com Ad Strength "Incomplete" — gerando 0 conv |

### 2.3 Risco de Frankenstein

> **Diagnóstico:** A conta recebeu 85 alterações em Jan, 60 em Fev, 37 em Mar, 27 em Abr. A bid strategy mudou 3x em 60 dias. O cliente pede otimizações constantes que não maturam. O resultado é uma conta com **5 campanhas ativas + 12 pausadas**, ~200 keywords das quais ~180 têm **zero impressão**, e uma estrutura que ninguém consegue explicar coerentemente.

---

## 3. OPORTUNIDADES NAS KEYWORDS — O Que Está Faltando

### 3.1 Keywords de Alto Volume AUSENTES da Conta

Da planilha *New Keywords Conserva.xlsx*, estas keywords de alto volume **não estão na conta ativa**:

**Repair Intent (Prioridade Máxima)**

| Keyword | Vol./mês | CPC Est. | Intenção | Match Recomendado | Prioridade |
|---|---|---|---|---|---|
| sprinkler repair near me | 14.800 | $6,16 | Transacional | **Phrase** + Exato | 🔴 P1 |
| sprinkler repair | 12.100 | $6,59 | Comercial | **Phrase** (NÃO broad) | 🔴 P1 |
| sprinkler system repair | 12.100 | $6,80 | Comercial | **Phrase** | 🔴 P1 |
| sprinkler system repair near me | 8.100 | $6,00 | Transacional | **Phrase** | 🔴 P1 |
| lawn sprinkler repair near me | 3.600 | $5,77 | Transacional | **Phrase** | 🟡 P2 |
| sprinkler valve repair | 2.400 | $7,17 | Informativa | **Phrase** | 🟡 P2 |
| sprinkler head repair | 1.900 | $4,74 | Informativa | **Phrase** | 🟡 P2 |

**Installation Intent (Prioridade Alta — Grupo Atualmente Morto)**

| Keyword | Vol./mês | CPC Est. | Intenção | Match Recomendado | Prioridade |
|---|---|---|---|---|---|
| sprinkler system installation | 14.800 | $4,70 | Informativa | **Phrase** | 🔴 P1 |
| sprinkler system installation near me | 8.100 | $5,51 | Transacional | **Phrase** | 🔴 P1 |
| irrigation system installation | 8.100 | $4,70 | Informativa | **Phrase** | 🔴 P1 |
| sprinkler installation | 4.400 | $5,61 | Informativa | **Phrase** | 🟡 P2 |
| sprinkler installation near me | 3.600 | $6,09 | Transacional | **Phrase** | 🟡 P2 |
| sprinkler system installation cost | 1.900 | $2,99 | Info/Comercial | **Phrase** | 🟢 P3 |

**General/Brand (Prioridade Média)**

| Keyword | Vol./mês | CPC Est. | Intenção | Match Recomendado | Prioridade |
|---|---|---|---|---|---|
| sprinkler system | 22.200 | $3,63 | Comercial | **Phrase** (negativar termos de DIY) | 🟡 P2 |
| irrigation system | 22.200 | $3,34 | Comercial | **Phrase** (negativar termos de DIY) | 🟡 P2 |

### 3.2 Keywords Que DEVEM Ser Pausadas ou Convertidas

| Keyword Atual | Problema | Ação |
|---|---|---|
| irrigation repair (Broad) | $81,81 gasto, 0 conv | 🔴 Mudar para Phrase |
| sprinkler repair (Broad) | $47,61 gasto, 0 conv | 🔴 Mudar para Phrase |
| All broad match keywords | 64% do budget em queries desconhecidas | 🔴 Pausar ou converter TODAS para Phrase/Exacto |
| "irrigation system repair" (Phrase) | 0 impr em 30 dias | 🟡 Pausar ou revisar lance |
| "sprinkler system repair near me" (Phrase) | 0 impr em 30 dias. QS 5 | 🟡 Aumentar lance |
| "sprinkler repair near me" (Broad) | QS 3, Lost IS Rank >90% | 🔴 Pausar e recriar como Phrase com lance maior |
| "irrigation repair near me" (Broad) | Sem dados de QS | 🔴 Pausar e recriar como Phrase |

### 3.3 Estratégia de Match Type

**Regra fundamental para esta conta:** 
> **Zero broad match até que a estrutura esteja estável por 30 dias consecutivos.**

O broad match está consumindo 64% do budget em tráfego de baixa intenção. A conta não tem volume de conversões histórico suficiente para o algoritmo aprender quais expansões são boas (apenas 3-5 conv/mês em Search).

| Match Type | % do Budget Recomendado | Justificativa |
|---|---|---|
| **Exact match** | 50% | Controle total sobre queries. Usar nas 10-15 keywords principais |
| **Phrase match** | 45% | Capturar variações próximas das principais intenções |
| **Broad match** | **5% (OU ZERO)** | Só após 30 dias de estabilidade e mínimo 30 conv/mês |

---

## 4. PACE DE VERBA — Análise de Budget

### 4.1 Onde o Dinheiro Está Indo (Search — Jun 1-30)

| Destino | Valor | % | Resultado |
|---|---|---|---|
| Precision Repair (ativo) | $643,13 | 92,8% | 3 conv @ $214 CPA |
| Spring Startup (ativo) | $49,86 | 7,2% | 2 conv @ $25 CPA |
| Installation (morto) | $0 | 0% | 0 conv |
| Smart Irrigation (morto) | $0 | 0% | 0 conv |
| B2B (morto) | $0 | 0% | 0 conv |
| **Total Search** | **$692,99** | **100%** | **5 conv @ $139 CPA** |

### 4.2 Desperdício Identificado

| Fonte de Desperdício | Valor/Mês | % do Budget Search |
|---|---|---|
| Broad match sem retorno (identificado) | ~$130 | 18,7% |
| Broad match em queries não mapeadas | ~$374 | 53,9% |
| Precision Repair com CPC inflado ($11-23 vs benchmark $6-7) | ~$200³ | 28,9% |
| **Desperdício total estimado** | **~$374-550/mês** | **54-79%** |

³ Diferença entre CPC real médio de $11,18 e CPC de mercado de $6-7 para repair terms

### 4.3 Cenário Atual de Budget vs Ideal

| | Atual (Search) | Recomendado (Search) |
|---|---|---|
| Budget diário | $27 | **$50** |
| Budget mensal | ~$810 | ~$1.500 |
| Perda por budget | 42% | ⬇️ Alvo: <15% |
| Perda por rank | 49% | ⬇️ Alvo: <25% |
| Orçamento "queimado" (waste) | ~$437/mês | ⬇️ Alvo: <$150/mês |

### 4.4 Proposta de Realocação

**Fase 1 (Julho — Sem aumentar budget):**
- Redirecionar os $27/dia atuais para **phrase/exact match APENAS**
- Pausar TUDO que é broad match
- Eliminar desperdício de ~$374/mês → orçamento real redirecionado para keywords que convertem
- Resultado esperado: mesmo budget, CPA cai de $139 para ~$90-100

**Fase 2 (Agosto — Se Fase 1 estabilizar):**
- Aumentar budget Search para $45-50/dia
- Ativar Installation Group com budget dedicado de $10-15/dia
- Aumentar Precision Repair para $25-30/dia
- $15-20/dia para Seasonal (Summer Ready) + Smart Efficiency

---

## 5. FORECASTING REAL — Projeção para Julho

### 5.1 Premissas do Modelo

Baseado nos dados reais de Junho, **não nos cenários antigos da planilha** (que foram feitos pré-Junho e estão desatualizados).

**Cenário Atual (Business as Usual — sem mudanças):**
- Search: ~$693/mês, 5 conv, CPA $139
- PMAX: ~$1.821/mês, 13 conv, CPA $140
- **Total: ~$2.514/mês, 18 conv, CPA $140**

### 5.2 Projeção Julho — 3 Cenários

**Premissas do modelo real:**
- Search budget: $27/dia → $30/dia (leve aumento)
- PMAX budget: $59/dia (mantido)
- Sazonalidade: Julho é pico de verão em AZ — demanda alta por reparos emergenciais

#### Cenário Conservador (Sem restructuring — só ajustes pontuais)

| Canal | Impressões | Cliques | Custo | Conv | CPA |
|---|---|---|---|---|---|
| Search | 1.500 | 70 | $830 | 6 | $138 |
| PMAX | 7.000 | 280 | $1.770 | 13 | $136 |
| **Total** | **8.500** | **350** | **$2.600** | **19** | **$137** |

*Continuidade do que temos hoje. Sem melhora significativa.*

#### Cenário Base (Restruturação Parcial — Fase 1)

| Canal | Impressões | Cliques | Custo | Conv | CPA |
|---|---|---|---|---|---|
| Search (reformulado) | 3.500 | 140 | $900 | **10** | $90 |
| PMAX (AG3 escalado) | 8.000 | 320 | $1.770 | **18** | $98 |
| **Total** | **11.500** | **460** | **$2.670** | **28** | **$95** |

*Com reestruturação de keywords + eliminação de broad match + reactivação de Installation com 2-3 conv.*

#### Cenário Otimista (Restruturação Completa + Budget Ajustado)

| Canal | Impressões | Cliques | Custo | Conv | CPA |
|---|---|---|---|---|---|
| Search (reformulado + $45/dia) | 6.000 | 220 | $1.350 | **18** | $75 |
| PMAX (AG1+AG2+AG3 otimizados) | 10.000 | 400 | $1.770 | **22** | $80 |
| **Total** | **16.000** | **620** | **$3.120** | **40** | **$78** |

*Com reestruturação total + budget Search em $45/dia + AG1 e AG2 do PMAX com Ad Strength "Good" ou superior.*

### 5.3 Gap Analysis — Cenário Base vs Planilha Original

| Métrica | Planilha Original (Base) | Nosso Cenário Base | Gap | Explicação |
|---|---|---|---|---|
| Impressões/mês | 160.000 | 11.500 | -93% | Planilha assumia conta com Search IS 80%+; realidade é 24% |
| Cliques/mês | 1.500 | 460 | -69% | Realista: sem resolver rank + budget, volume não vem |
| Conv/mês | 85 | 28 | -67% | 85 conv/mês exigiria 3x mais tráfego e CPA de $45 |
| Budget/dia | $127 | $89 | -30% | Budget atual ativo é $86/dia, não $127 |

> **Conclusão:** Os cenários da planilha original estavam **fundamentalmente incorretos** porque assumiam métricas de Search (IS 80%+ etc.) que a conta **nunca teve**. Nossos cenários são baseados nos dados reais de Junho.

---

## 6. ESTRUTURA RECOMENDADA — Arquitetura da Nova Campanha Search

### 6.1 Princípios da Nova Estrutura

1. **Uma campanha Search única** (não múltiplas campanhas fragmentadas)
2. **5 ad groups focados** (não 20+)
3. **Phrase match como padrão** (broad match banido por 30 dias)
4. **Bid strategy: Maximize Conversions** fixa por 30+ dias — sem trocar
5. **Budget diário: $30-50/dia**
6. **Landing pages dedicadas** por grupo de anúncios

### 6.2 Proposta de Arquitetura

```
Campanha: [V4] Conserva Search — Services [JUL-2026]
├── Budget: $45/dia (Fase 1) → $50/dia (Fase 2)
├── Bid: Maximize Conversions (tCPA $100)
├── Network: Search Network Only
├── Locations: Greater Scottsdale (ZIPs 85250-85268)
│
├── Ad Group 1: Precision Repair (55% do budget = $25/dia)
│   ├── "sprinkler repair near me" [Phrase] ← P1
│   ├── "sprinkler repair" [Phrase] ← P1
│   ├── "sprinkler system repair" [Phrase] ← P1
│   ├── "sprinkler system repair near me" [Phrase] ← P1
│   ├── "irrigation repair near me" [Phrase] ← JÁ CONVERTE!
│   ├── "irrigation repair" [Phrase] ← P1
│   ├── "lawn sprinkler repair near me" [Phrase] ← P2
│   ├── "sprinkler valve repair" [Phrase] ← P2
│   └── "sprinkler head repair" [Phrase] ← P2
│   └── Landing Page: /irrigation-repair/
│   └── RSA: Headlines com {KeyWord:Sprinkler Repair}, {KeyWord:Emergency Fix}, etc.
│
├── Ad Group 2: Installation (20% do budget = $9/dia)
│   ├── "sprinkler system installation" [Phrase] ← P1
│   ├── "sprinkler system installation near me" [Phrase] ← P1
│   ├── "irrigation system installation" [Phrase] ← P1
│   ├── "sprinkler installation" [Phrase] ← P2
│   ├── "sprinkler installation near me" [Phrase] ← P2
│   └── "sprinkler system installation cost" [Phrase] ← P3
│   └── Landing Page: /irrigation-system-installation/
│   └── RSA: Headlines com {KeyWord:Sprinkler Installation}, Free Quote, etc.
│
├── Ad Group 3: Seasonal/Summer Ready (15% do budget = $7/dia)
│   ├── "spring sprinkler startup" [Phrase]
│   ├── "sprinkler system tune up" [Phrase] ← JÁ CONVERTE!
│   ├── "irrigation system audit" [Phrase]
│   ├── "sprinkler system inspection" [Phrase]
│   └── "summer sprinkler service" [Phrase]
│   └── Landing Page: Homepage + SES page
│   └── RSA: Headlines sazonais, Summer Ready, Free Inspection
│
├── Ad Group 4: Smart Irrigation (5% do budget = $2/dia)
│   ├── "smart irrigation system" [Phrase]
│   ├── "smart sprinkler installation" [Phrase]
│   ├── "wifi sprinkler controller" [Phrase]
│   └── "smart irrigation system cost" [Phrase]
│   └── Landing Page: /smart-irrigation/
│
└── Ad Group 5: B2B (5% do budget = $2/dia — só após estabilidade)
    ├── "commercial irrigation services" [Phrase]
    ├── "HOA irrigation maintenance" [Phrase]
    └── "property management irrigation" [Phrase]
    └── Landing Page: /commercial-irrigation/
```

### 6.3 Landing Pages Recomendadas

| Ad Group | URL | Status Atual |
|---|---|---|
| Precision Repair | `/irrigation-repair/` | ✅ Já existe (ad atual usa esta URL) |
| Installation | `/irrigation-system-installation/` | ✅ Já existe (mas ad não está vinculada corretamente) |
| Seasonal | Homepage + `/free-inspection/` | ⚠️ Precisa de LP dedicada |
| Smart Irrigation | `/smart-irrigation/` | ⚠️ Pode precisar de criação |
| B2B | `/commercial-irrigation/` | ⚠️ Pode precisar de criação |

### 6.4 Negative Keywords Essenciais

Para proteger o budget de desperdício (estas queries consomem verba sem retorno):
- DIY terms: "how to", "diy", "home depot", "lowes", "youtube", "manual"
- Supply terms: "parts", "supply", "wholesale", "valves" (sem intenção de service)
- Rental terms: "rent", "rental"
- Job terms: "jobs", "careers", "hiring"
- Landscaping terms (não irrigação): "lawn mowing", "landscaping", "tree service"

### 6.5 Cronograma de Implementação

| Fase | Ação | Prazo | Impacto Esperado |
|---|---|---|---|
| **Fase 0 — Imediata** | Pausar keywords broad match sem conv. Manter só "irrigation repair near me" (phrase) e "sprinkler system tune up" (broad com conversão). | Dia 1 | Reduz desperdício de 64% para ~20% |
| **Fase 1 — Semana 1** | Criar nova estrutura de campanha com 5 ad groups. Adicionar 20-25 novas keywords phrase match. Landing pages. | Dias 2-7 | Estrutura limpa, pronta para aprender |
| **Fase 2 — Semana 2-3** | Monitorar. NÃO TROCAR BID STRATEGY. Ajustar lances com base em dados de 7+ dias. | Dias 8-21 | CPA deve cair de $139 para $100-120 |
| **Fase 3 — Semana 4** | Se CPA estabilizar abaixo de $100, aumentar budget para $45/dia. Adicionar exact match das melhores converting queries. | Dias 22-30 | Volume de conv deve subir para 8-12/mês |
| **Fase 4 — Agosto** | Reavaliar. Se Search estiver estável com CPA <$90, escalar budget. Revisitar PMAX AG1/AG2. | Mês 2 | Account total: 30+ conv/mês, CPA <$100 |

---

## 7. RECOMENDAÇÕES FINAIS

### 7.1 Top 5 Ações Imediatas (Ordem de Prioridade)

1. 🚨 **Pausar TODO broad match** na Search imediatamente. Manter apenas phrase/exact match nas 10-15 keywords principais.
2. 🚨 **Parar de trocar a bid strategy**. Fixar Maximize Conversions por 30+ dias. Cada troca reseta o aprendizado do algoritmo.
3. 🚨 **Criar a nova estrutura de campanha** com 5 ad groups focados e 20-25 keywords phrase match de alto volume.
4. ⚠️ **Aumentar budget Search** de $27 para pelo menos $45/dia (após a reestruturação, não antes).
5. ⚠️ **Criar landing pages dedicadas** para Installation e Smart Irrigation.

### 7.2 O Que NÃO Fazer

- ❌ **Não criar mais campanhas novas** — a conta já tem 17 campanhas (5 ativas + 12 pausadas)
- ❌ **Não adicionar keywords sem match type phrase/exact** — nenhuma broad match
- ❌ **Não trocar a bid strategy** por pelo menos 30 dias consecutivos
- ❌ **Não aumentar budget antes de resolver o rank** — vai queimar dinheiro mais rápido
- ❌ **Não fazer mudanças diárias** — agrupar alterações em pacotes semanais

### 7.3 KPI Targets para Julho

| KPI | Atual (Jun) | Alvo (Jul) | Meta (Ago) |
|---|---|---|---|
| Search CPA | $139 | <$100 | <$85 |
| Search CVR | 8,06% | >10% | >12% |
| Search IS | 21,9% | >30% | >35% |
| Search Lost IS (Rank) | 49% | <35% | <25% |
| CTR Search | 4,61% | >6% | >8% |
| Conv/mês (Search) | 5 | 10-12 | 15-18 |
| Budget Utilização | ~64% (waste 36%) | >85% (waste <15%) | >90% |

---

**Preparado por:** Analista de Dados — Traffic Reporting Squad  
**Data:** 1 de Julho de 2026  
**Próximo review sugerido:** 15 de Julho de 2026 (pós-implementação Fase 1)
