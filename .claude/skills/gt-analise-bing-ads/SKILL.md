---
name: gt-analise-bing-ads
description: Skill de analise de metricas Bing Ads (Microsoft Advertising) com interpretacao contextual — sabe diferenciar metrica de operacao diaria vs diagnostico vs investigacao profunda para Search, Shopping, Audience Network. Arvores de decisao, protocolo de cenario, parametros LLM e melhores praticas.
area: gt
author: v4team
version: 1.0.0
aliases: [gt-analise-bing-ads, bing-ads-analytics, microsoft-ads-metrics]
tags: [skill, area-gt, bing-ads, microsoft-ads, analytics]
---

# GT — Analise de Bing Ads (Microsoft Advertising)

Skill de analise de metricas de **Microsoft Advertising (Bing Ads)** para gestores de trafego que precisam interpretar dados com sabedoria contextual. Diferencia metricas de operacao diaria (Camada 1), diagnostico tatico (Camada 2) e investigacao profunda (Camada 3).

Antes de usar esta skill, carregue dados de Bing Ads via `v4mos-dados-bing-ads` ou insira as metricas manualmente. Esta skill NAO puxa dados — ela INTERPRETA.

---

## Visao Geral

### O que e Bing Ads (Microsoft Advertising)

Microsoft Advertising (antigo Bing Ads) e a plataforma de midia paga da Microsoft que veicula anuncios no:

- **Bing** — aproximadamente 6-8% do mercado de busca global, mas 15-25% nos EUA em desktop
- **Yahoo** (parceria com a Verizon Media)
- **AOL**
- **Search Partners** — rede de parceiros de busca que usam o indice da Microsoft
- **Microsoft Audience Network** — rede nativa/discovery no ecossistema Microsoft (MSN, Edge, Outlook.com, Microsoft Start)
- **LinkedIn** — integrado via Audience Network com targeting por perfil profissional
- **Copilot** — respostas patrocinadas emergindo no ecossistema Microsoft AI

### Por que Bing e diferente

Bing Ads nao e "Google de segunda categoria". A audiencia tem caracteristicas UNICAS que gestores de trafego precisam entender:

| Caracteristica | Impacto |
|---|---|
| **Maior poder aquisitivo** | Usuario Bing tem renda media 30-40% maior que usuario Google medio |
| **Desktop-heavy** | ~60-70% do trafego Bing vem de desktop (vs ~40% no Google) |
| **Ecossistema Microsoft** | Windows + Edge + Office + LinkedIn + Copilot cria audiencia corporativa/profissional |
| **Menos concorrencia** | Menos anunciantes = CPCs 30-50% menores que Google em media |
| **Menos saturation** | Mesmo lance ganha posicoes melhores com menos concorrencia |
| **Age skew** | Publico mais velho (35-55+ anos), menos volateis, maior taxa de conversao em certos nichos |
| **Geolocalizacao especifica** | Alguns paises tem participacao Bing muito maior que a media global |

### Oportunidades

- **CPCs mais baixos** — tipicamente 30-50% menor que Google para as mesmas keywords
- **Menos saturacao** — leilao menos competitivo significa que campanhas bem estruturadas performam com menos investimento
- **Search Partners** — podem dobrar volume com CPA similar se bem gerenciados
- **LinkedIn targeting integrado** — Bing e a UNICA plataforma de busca que permite segmentar por cargo/empresa/setor diretamente no ambiente de search
- **Microsoft Audience Network** — discovery/native ads com CPCs muito baixos e escala via ecossistema Microsoft
- **Copilot integration** — espaco emergente para aparecer em respostas de IA no ecossistema Microsoft
- **Importacao do Google** — reduz setup, mas requer reotimizacao
- **Microsoft Clarity** — replay de sessoes e heatmaps integrados sem custo adicional

### Limitacoes

- **Volume menor** — 6-15% do volume de busca do Google dependendo do pais/industria
- **Menos funcionalidades** — menos tipos de campanha, menos opcoes de lance, menos segmentacao
- **Menos dados de atribuicao** — UET (Universal Event Tracking) e menos robusto que Google Ads + GA4
- **Menos automation** — Smart Bidding e menos maduro que Google (nao tem Portfolio Bid Strategies, por exemplo)
- **Menos integracoes de terceiros** — menos ferramentas, menos scripts, menos APIs
- **Shopping menos maduro** — Microsoft Merchant Center tem menos recursos que Google Merchant Center
- **Dados demoram mais** — Bing leva 24-48h para estabilizar metricas de conversao apos mudancas
- **Remarketing mais limitado** — menor escala de audiencia, menos opcoes de segmentacao
- **Suporte inferior** — suporte ao cliente significativamente pior que Google

---

## Premissas Fundamentais para o LLM

### Regras de Ouro do LLM ao analisar Bing Ads

1. **NUNCA trate Bing como "Google mais barato"** — a audiencia e MAIOR renda, mais velha, mais desktop. O mesmo produto pode converter muito diferente.
2. **Sempre verifique Search Partners separadamente** — eles podem inflar volume com clicks de baixa qualidade ou ser uma fonte valiosa de conversao. NUNCA analise sem o breakdown.
3. **Janela de observacao maior** — Bing precisa de 48-72h de learning apos mudancas de lance/segmentacao. Nao tome decisoes em menos de 3 dias.
4. **Destrua o mito do "Bing nao funciona"** — 80% das vezes que alguem diz isso, a conta foi importada do Google sem adaptacao. Bing requer ajustes proprios.
5. **Sempre compare Bing vs Google no mesmo periodo com mesmas keywords** — senao a analise e injusta com ambos.
6. **Nao ignore Audience Network** — muitos gestores focam so em Search e perdem a oportunidade de CPCs 60-80% menores com boa conversao em awareness/consideracao.
7. **Verifique UET tag sempre** — 90% dos problemas de atribuicao no Bing sao UET tag mal instalada, duplicada ou com delay.
8. **Bing gosta de match types diferentes do Google** — Exact Match no Bing e menos restritivo que no Google. Phrase Match se comporta diferente.
9. **Desktop e prioridade** — nao otimize para mobile da mesma forma que no Google. Bing ainda e desktop-first.
10. **LinkedIn targeting e diferencial real** — segmentar por empresa/cargo no search e exclusivo do Bing. Use com intencao de compra alta.

### Bing NAO e "Google mais barato" — evidencias

- A mesma keyword "plano de saude" tem CPC medio de R$ 8,50 no Google vs R$ 4,20 no Bing (51% menor)
- Mas a taxa de conversao do Bing para planos de saude e tipicamente 20-30% MENOR que Google porque o usuario Bing esta em estadio de pesquisa diferente (mais cedo no funil)
- O CPA final pode ser similar ou ate maior no Bing mesmo com CPC menor
- Conclusao: Bing nao e mais barato — e DIFERENTE. A estrategia de keyword, bid e landing page precisa ser adaptada.

### Search Partners — o que sao, como impactam, quando desligar

**O que sao:**
Sites parceiros que usam o indice de busca da Microsoft para mostrar resultados. Incluem Yahoo, AOL, e centenas de sites menores.

**Como impactam:**
- Podem dobrar ou triplicar o volume de clicks
- Taxa de conversao tipicamente 30-50% menor que search puro
- CPCs geralmente 40-60% menores que search puro
- CTR costuma ser maior (mais clicks acidentais em sites parceiros)
- Quality Score nao se aplica da mesma forma

**Quando desligar:**
- Se CPA em Search Partners for > 2x o CPA do search puro por mais de 7 dias
- Se taxa de conversao for < 50% da taxa de search puro consistentemente
- Se o orcamento e limitado e search puro absorve todo o investimento com ROAS positivo
- Em campanhas de branding onde qualidade do clique importa mais que volume

**Quando manter:**
- Se CPA esta dentro de 30% do search puro (vale pelo volume incremental)
- Se o negocio escala com volume bruto (exemplo: e-commerce com margem alta)
- Em campanhas de remarketing onde o clique barato ainda e valioso
- Para alimentar audiencias de remarketing com volume a baixo custo

### O impacto do ecossistema Microsoft (Windows, Edge, LinkedIn, Copilot)

O ecossistema Microsoft cria vantagens que Google nao consegue replicar:

- **Windows + Edge** — usuario que usa Edge como browser padrao tem o Bing como search padrao. Isso gera um publico "cativivo" que nao escolheu Bing ativamente — comportamento diferente do usuario Google que ativamente vai ao google.com
- **LinkedIn** — dados profissionais integrados permitem segmentar por cargo, empresa, setor, formacao academica dentro do ambiente de search. Bing e a UNICA plataforma com isso.
- **Office 365 / Microsoft 365** — usuarios corporativos expostos ao ecossistema Office tem mais tendencia a usar Bing/Edge no trabalho
- **Copilot (Bing Chat)** — as respostas de IA generativa no Bing/Edge geram oportunidades de trafego patrocinado em formato completamente novo (ainda emergente em 2025-2026)
- **Xbox** — audiencia gamer integrada via Audience Network
- **Microsoft Start / MSN** — rede de anuncios nativos com alto engajamento

### Hierarquia de confianca das metricas

| Confianca | Metrica | Por que |
|---|---|---|
| **Alta** | Cliques, Impressoes, Gasto | Dados contabilizaveis, baixo erro |
| **Alta** | CPC, CTR, Position | Calculos diretos, consistentes |
| **Media** | Conversoes (UET) | Sujeito a delay, duplicacao, tag mal instalada |
| **Media** | CPA, ROAS, Taxa de Conversao | Derivados de conversoes, herdam imprecisao |
| **Media** | Impression Share | Bing tem amostragem diferente que Google |
| **Baixa** | View-through conversions | Audience Network atribuicao questionavel |
| **Baixa** | Cross-device conversions | Bing menos robusto que Google nessa metrica |
| **Baixa** | Assisted conversions | Modelo de atribuicao do Bing e menos maturo |

### Quando Bing complementa Google vs quando substitui

**Complementa:** A maioria dos casos. Bing adiciona 10-30% de volume incremental com CPCs menores. Use Bing para capturar o que Google nao captura — audiencia corporativa, usuarios 35+, nichos de alto tiquete.

**Substitui:** Cenarios especificos onde Google e proibitivo:
- Nichos com CPC Google > R$ 20-30 (Google fica caro demais)
- Produtos/servicos B2B onde LinkedIn targeting no Bing faz diferenca
- Mercados onde Bing tem participacao alta (EUA desktop, UK, Canada, Australia)
- Contas com orcamento limitado onde Google e competitivo demais
- Produtos com margem baixa onde CPC Google inviabiliza ROAS

---

## A Piramide de Decisao Bing Ads

```
                    ┌─────────────────────────┐
                    │     CAMADA 1            │
                    │   OPERACAO DIARIA       │
                    │                         │
                    │ Cliques, Impressoes,    │
                    │ CPC, CTR, Gasto,        │
                    │ Conversoes, Tx Conv,    │
                    │ CPA, ROAS, Imp. Share   │
                    └───────────┬─────────────┘
                                │
                    ┌───────────▼─────────────┐
                    │     CAMADA 2            │
                    │   DIAGNOSTICO TATICO    │
                    │                         │
                    │ Quality Score,          │
                    │ Search Partners Perf,   │
                    │ Dispositivo Breakdown,  │
                    │ Match Type Perf,        │
                    │ Aud. Network Perf,      │
                    │ LinkedIn Targeting,     │
                    │ Tempo ate Conversao     │
                    └───────────┬─────────────┘
                                │
                    ┌───────────▼─────────────┐
                    │     CAMADA 3            │
                    │ INVESTIGACAO PROFUNDA   │
                    │                         │
                    │ Atribuicao, UET Health, │
                    │ View-through Conv,      │
                    │ Cross-device,           │
                    │ Auto-bidding Analysis,  │
                    │ Experimentos,           │
                    │ Remarketing Lists,      │
                    │ Goal Tracking Deep Dive │
                    └─────────────────────────┘
```

### Logica de navegacao entre camadas

```
PERGUNTA: "Como esta a campanha X?"
  │
  ├─【CAMADA 1】Leia metricas de operacao
  │   ├─ Tudo verde? → reportar "saudavel", recomendar otimizacao incremental
  │   ├─ Amarelo? → subir para Camada 2 no indicador especifico
  │   └─ Vermelho? → subir para Camada 2 e 3 no indicador + metricas correlatas
  │
  ├─【CAMADA 2】Diagnostico do indicador amarelo/vermelho
  │   ├─ Encontrou causa raiz? → recomendar acao, reportar
  │   └─ Nao encontrou ou sintoma persiste? → subir para Camada 3
  │
  └─【CAMADA 3】Investigacao profunda
      ├─ Causa encontrada → recomendar correcao estrutural
      └─ Causa nao encontrada → reportar como anomalia para suporte Microsoft
```

---

## Camada 1 — Metricas de Operacao Diaria

### 1. Cliques

| Aspecto | Detalhe |
|---|---|
| **Conceito** | Numero de vezes que usuarios clicaram no anuncio |
| **Normalidade por setor** | Varia totalmente por verba e industria |
| **Bing spec** | Clicks em Search Partners sao contados separadamente. Cliques em Audience Network tem comportamento diferente. |
| **Sinal verde** | Crescimento ou estabilidade dentro da media historica (desvio < 15%) |
| **Sinal amarelo** | Queda de 15-30% sem reducao de orcamento. Possiveis causas: sazonalidade, concorrencia, mudanca de Quality Score. |
| **Sinal vermelho** | Queda > 30% ou aumento > 50% sem alteracao. Possivel: campanha pausada, keyword disapproved, problema de UET (sim, UET travada afeta lances). |
| **O que NAO fazer** | Nao reagir a variacao de 1-2 dias. Bing tem maior volatilidade diaria que Google. Janela minima de analise: 7 dias. |

### 2. Impressoes

| Aspecto | Detalhe |
|---|---|
| **Conceito** | Quantas vezes o anuncio foi exibido |
| **Normalidade** | +10% de variacao diaria e normal. Bing tem maior variacao porque o leilao e menor (menos dados = mais ruido) |
| **Bing spec** | Bing pode mostrar menos impressoes em horarios comerciais (menos usuarios trabalhando no browser). Pico noturno e maior que Google. |
| **Sinal verde** | Crescimento ou estabilidade |
| **Sinal amarelo** | Queda de 20-40%. Verificar: campanha ativa? Keyword status? Orcamento? |
| **Sinal vermelho** | Queda > 40%. Verificar: conta suspensa? Mudanca de politica? Erro de importacao? |
| **O que NAO fazer** | Nao aumentar lances cegamente para recuperar impressoes sem investigar causa. |

### 3. CPC (Custo por Clique)

| Aspecto | Detalhe |
|---|---|
| **Conceito** | Valor medio pago por clique (gasto / cliques) |
| **Valor referencia (Brasil, R$)** | Search: R$ 1,50 - R$ 15,00 dependendo do setor. Audience Network: R$ 0,30 - R$ 2,00 |
| **Valor referencia (EUA, USD)** | Search: $0.50 - $8.00. Audience Network: $0.10 - $0.80 |
| **Bing spec** | CPC Bing e tipicamente 30-50% menor que Google para mesmas keywords |
| **Sinal verde** | Abaixo do benchmark do setor ou dentro da media historica |
| **Sinal amarelo** | Aumento de 15-30%. Verificar: concorrencia nova? Quality Score caiu? Keyword match type mudou? |
| **Sinal vermelho** | Aumento > 30%. Possivel: concorrente agressivo, mudanca de leilao, problema de targeting |
| **O que NAO fazer** | Nao comparar CPC Bing com CPC Google diretamente — aceite que Bing pode ter CPC mais baixo mesmo com mesma keyword, mas isso nao significa que Bing e "mais eficiente" sem considerar conversao. |

### 4. CTR (Click-Through Rate)

| Aspecto | Detalhe |
|---|---|
| **Conceito** | (Cliques / Impressoes) x 100 |
| **Normalidade** | Search: 1.5% - 5.0% (media ~2.5%). Audience Network: 0.2% - 0.8%. Search Partners: 3.0% - 8.0% (mais clicks acidentais) |
| **Bing spec** | CTR no Bing tende a ser LIGEIRAMENTE maior que Google porque audiencia e menos sofisticada (clica mais em anuncios sem filtrar) |
| **Razoes para variacao** | Posicao media, copy do anuncio, extensoes, relevancia da keyword, sazonalidade |
| **Sinal verde** | Acima de 2.5% em Search |
| **Sinal amarelo** | 1.0% - 2.5% — investigar posicao e copy |
| **Sinal vermelho** | Abaixo de 1.0% — problema grave de relevancia ou posicao |
| **O que NAO fazer** | Nao perseguir CTR alto cegamente. CTR alto com CPA alto e inutil. Contexto: CTR em topo de funil tende a ser menor que fundo de funil. |

### 5. Gasto (Spend)

| Aspecto | Detalhe |
|---|---|
| **Conceito** | Valor total gasto no periodo |
| **Normalidade** | Dentro do previsto. Variacao diaria de +20% e normal (Bing nao entrega uniformemente) |
| **Bing spec** | Bing pode ter dificuldade em gastar o orcamento diario em contas novas ou com restricao de segmentacao muita especifica |
| **Sinal verde** | Dentro do planejado |
| **Sinal amarelo** | Gastando menos de 70% do orcamento diario. Verificar: impression share, leilao, keywords |
| **Sinal vermelho** | Gastando > 20% acima do orcamento diario (Bing as vezes ultrapassa). Ou gastando < 40% — campanha pode estar travada. |
| **O que NAO fazer** | Nao aumentar lances para gastar mais orcamento — primeiro entenda por que nao esta gastando. |

### 6. Conversoes

| Aspecto | Detalhe |
|---|---|
| **Conceito** | Acoes valiosas registradas pelo UET tag |
| **Normalidade** | Depende do setor e volume. Variacao semanal (comparar mesma semana do mes passado) e mais confiavel que dia vs dia |
| **Bing spec** | Conversoes no Bing tem DELAY de 4-24h comparado com Google. Nao tome decisoes baseado em dados de hoje — use periodos completos. |
| **Sinal verde** | Crescimento ou estabilidade |
| **Sinal amarelo** | Queda de 15-30%. Verificar: UET tag funcionando? Landing page OK? Sazonalidade? |
| **Sinal vermelho** | Queda > 30% ou zero conversoes. Possivel: UET tag quebrada, pagina fora do ar, mudanca de funil, problema de tracking. |
| **O que NAO fazer** | Nao comparar conversoes do Bing com Google Ads diretamente — modelos de atribuicao sao diferentes. SEMPRE verifique UET tag primeiro. |

### 7. Taxa de Conversao (CVR)

| Aspecto | Detalhe |
|---|---|
| **Conceito** | (Conversoes / Cliques) x 100 |
| **Normalidade** | Search: 2.0% - 8.0% (media por setor). Audience Network: 0.5% - 2.0%. Search Partners: 1.0% - 3.0% |
| **Bing spec** | CVR tende a ser 10-30% MENOR que Google para as mesmas keywords porque usuario Bing esta mais cedo no funil de compra (explorando, menos intencao de compra imediata) |
| **Sinal verde** | Acima de 3.0% em Search |
| **Sinal amarelo** | 1.5% - 3.0% — aceitavel para topo de funil |
| **Sinal vermelho** | Abaixo de 1.5% — verificar landing page, keyword intent, targeting |
| **O que NAO fazer** | Nao perseguir CVR alta eliminando keywords de topo de funil — voce pode estar matando o topo do funil que alimenta remarketing. |

### 8. CPA (Custo por Aquisicao)

| Aspecto | Detalhe |
|---|---|
| **Conceito** | Gasto / Conversoes |
| **Normalidade** | Aceitavel = margem do produto/servico permitir. Benchmark setorial e referencia, nao verdade absoluta. |
| **Bing spec** | CPA Bing pode ser MENOR que Google (CPC menor) ou MAIOR (CVR menor). A media varia -30% a +20% comparado com Google. |
| **Sinal verde** | Dentro do target de CPA |
| **Sinal amarelo** | 20-40% acima do target. Investigar: keywords, match types, dispositivos, search partners |
| **Sinal vermelho** | > 40% acima do target. Investigacao profunda necessaria. |
| **O que NAO fazer** | Nao tomar decisoes de CPA baseado em menos de 30 conversoes. Amostra pequena = ruido alto. |

### 9. ROAS (Return on Ad Spend)

| Aspecto | Detalhe |
|---|---|
| **Conceito** | Receita / Gasto (ou Valor da Conversao / Gasto) |
| **Normalidade** | Minimo aceitavel: 3:1 (300%) para maioria dos e-commerces. Ideal: 5:1+ |
| **Bing spec** | ROAS Bing e geralmente 10-40% MENOR que Google (menos conversoes diretas), mas o valor medio do pedido pode ser MAIOR (publico de maior renda). |
| **Sinal verde** | ROAS > 4:1 |
| **Sinal amarelo** | ROAS 2:1 a 4:1 — viavel mas precisa otimizar |
| **Sinal vermelho** | ROAS < 2:1 — verificar urgentemente |
| **O que NAO fazer** | Nao matar campanha com ROAS 2.5:1 sem verificar margem real do produto. Se margem for 60%, ROAS 2:1 ainda e lucrativo. |

### 10. Impression Share

| Aspecto | Detalhe |
|---|---|
| **Conceito** | % de impressoes que seu anuncio recebeu do total disponivel |
| **Normalidade** | Ideal: > 80%. Aceitavel: 60-80%. Baixo: < 60% |
| **Bing spec** | Impression share no Bing e calculado de forma similar ao Google mas com menos granularidade. Bing mostra lost IS por budget vs rank separadamente. |
| **Sinal verde** | > 80% |
| **Sinal amarelo** | 50-80% — perder por budget ou rank? Cada um tem solucao diferente. |
| **Sinal vermelho** | < 50% — campanha pode estar muito restrita ou com baixo Quality Score |
| **O que NAO fazer** | Nao aumentar lances para recuperar impression share perdido por budget — isso so aumenta o custo. Se perde por budget, aumente orcamento. Se perde por rank, melhore Quality Score ou lance. |

### 11. Posicao Media (Average Position)

| Aspecto | Detalhe |
|---|---|
| **Conceito** | Posicao media do anuncio nos resultados de busca (1.0 = topo) |
| **Bing spec** | DIFERENTE DO GOOGLE: Bing ainda USA posicao media como metrica oficial (Google descontinuou em 2019). Posicao 1-4 sao normais. |
| **Sinal verde** | 1.0 - 2.0 (topo) |
| **Sinal amarelo** | 2.1 - 4.0 (meio) |
| **Sinal vermelho** | > 4.0 ou posicao 8+ (dificilmente recebe clique) |
| **O que NAO fazer** | Nao perseguir posicao 1.0 a todo custo — posicao 2-3 pode ter CTR similar com CPC muito menor. |

---

## Camada 2 — Metricas de Diagnostico Tattico

### 1. Quality Score (QS) do Bing

**Conceito:** Similar ao Google Ads, mas com diferencas importantes na composicao.

**Componentes do Quality Score no Bing vs Google:**

| Componente | Bing Ads | Google Ads |
|---|---|---|
| **Expected CTR** | Peso alto | Peso alto |
| **Ad Relevance** | Peso medio | Peso medio |
| **Landing Page Experience** | Peso medio | Peso medio |
| **Historical Performance** | Peso MAIOR que Google | Peso menor |
| **Device Performance** | Considera separadamente | Integrado no CTR |
| **Account History** | Peso SIGNIFICATIVO | Menor peso |

**Diferencas criticas:**
- Bing da muito peso ao historico da conta — contas novas comecam com QS mais baixo e sobem lentamente
- Performance por dispositivo e avaliada separadamente (um anuncio pode ter QS 8/10 em desktop e 4/10 em mobile)
- Bing e mais generoso com QS alto (7-10) que Google — e mais facil ter QS alto no Bing
- Mas QS alto no Bing NAO significa reducao de CPC tao significativa quanto no Google

**Escala Bing QS:**
- 10/10: Excelente. CPC reduzido significativamente.
- 7-9/10: Bom. Performance OK.
- 5-6/10: Medio. Precisa melhorar relevancia.
- 3-4/10: Baixo. Problemas serios.
- 1-2/10: Critico. Anuncio quase nao roda.

**Quando investigar:**
- CPC subiu sem alteracao de lances
- Impression share baixo lost to rank
- Campanha nova com baixo volume mesmo com lances agressivos

**O que fazer baseado no QS:**
- QS baixo por Expected CTR: melhore o copy do anuncio, adicione extensoes, teste headlines
- QS baixo por Ad Relevance: refine keywords, crie grupos de anuncios mais especificos
- QS baixo por Landing Page: melhore velocidade, relevancia e experiencia mobile da pagina
- QS baixo por Historical Performance: aguarde — Bing precisa de historico para subir QS

### 2. Impression Share Lost — Budget vs Rank

**Conceito:** Bing mostra explicitamente quanto do impression share foi perdido por orcamento (budget) vs por classificacao (rank).

**Cenario 1: Perde mais por budget (> 60% da perda)**
- Diagnostico: Orcamento diario insuficiente para capturar todo o trafego disponivel
- Acao: Aumentar orcamento diario se ROAS for positivo. Ou reduzir keywords/lances para focar no que converte melhor.
- Sinal: Se orcamento aumentou mas impression share nao subiu proporcionalmente, pode ser que o aumento de orcamento entrou em horarios de menor trafego.

**Cenario 2: Perde mais por rank (> 60% da perda)**
- Diagnostico: Quality Score baixo ou lances insuficientes
- Acao: Verificar QS das keywords, aumentar lances, melhorar relevancia
- Prioridade: Melhorar QS primeiro (reduz custo) antes de aumentar lances

**Cenario 3: Misto (budget + rank significativos)**
- Diagnostico: Otimizacao dupla necessaria
- Acao: Ataque rank primeiro (QS + lance), depois ajuste budget

### 3. Search Partners Performance Breakdown

**Conceito:** Separar metricas de search puro (Bing + Yahoo + AOL) vs Search Partners.

**Como interpretar:**

| Cenario | Interpretacao |
|---|---|
| Partners: CPA similar ao Search | Otimo. Mantenha — esta adicionando volume de qualidade |
| Partners: CPA 1.5x - 2.5x do Search | Aceitavel para escalar. Decida baseado na margem. |
| Partners: CPA > 3x do Search | Problema. Partners estao drenando orcamento. Considere desligar. |
| Partners: Taxa de conversao muito baixa | Clicks acidentais. Desligue. |
| Partners: CTR muito alto vs Search | Provavelmente clicks de baixa qualidade. Investigue. |

**Regra pratica:** Se Search Partners consomem > 20% do orcamento mas geram < 10% das conversoes, desligue.

**IMPORTANTE:** Search Partners NAO tem controle por site individual. Nao da para escolher quais parceiros, apenas ligar/desligar todos. Se desligar, perde TODO o volume de parceiros (incluindo os bons).

### 4. Taxa de Conversao por Dispositivo

**Conceito:** Breakdown de conversao por computador, tablet, smartphone.

**Por que importa no Bing:**
- **Desktop** = 60-70% do trafego (vs 35-45% no Google)
- **Mobile** = 30-40% do trafego (vs 55-65% no Google)
- **Tablet** = 2-5%

**Padroes tipicos:**
- Desktop no Bing costuma ter CVR 20-40% MAIOR que mobile no Bing
- Desktop Bing pode ter CVR ate 50% maior que desktop Google para certos nichos (publico profissional)
- Mobile Bing tem CVR geralmente menor que mobile Google (menos intencao de compra em mobile)

**Windows Phone:** Praticamente extinto. Nao perca tempo segmentando.

**Quando investigar:**
- Se mobile CVR caiu subitamente
- Se desktop CVR esta excepcionalmente alto (pode ser erro de tracking)
- Se um dispositivo esta com volume muito fora do padrao

### 5. Tempo ate Conversao (Time to Conversion)

**Conceito:** Quanto tempo entre o clique e a conversao, segundo o UET.

**Por que importa:**
- Bing tem janela de conversao maior que Google
- Produtos de alto tiquete (seguros, financas, automoveis) tem tempo ate conversao de 7-30 dias no Bing
- Se voce analisa apenas janela curta de conversao (ex: 1 dia), pode estar subestimando o valor do Bing

**Benchmarks (aprox.):**
- E-commerce: 1-7 dias (media 1-2 dias)
- Servicos: 3-30 dias
- Auto/Seguros: 7-60 dias
- B2B SaaS: 7-90 dias

**Acorda:**
- Sempre verifique o modelo de atribuicao e a janela de conversao configurada no Bing
- Configure janela de conversao de pelo menos 30 dias para produtos de consideracao longa

### 6. Top vs Other CPC (Bing spec)

**Conceito:** Diferenca entre o CPC quando o anuncio aparece nas primeiras posicoes (top) vs posicoes inferiores.

**Por que importa:**
- Bing cobra significativamente mais por posicoes 1-2
- A diferenca Top vs Other no Bing e MAIOR que no Google (cerca de 40-60% mais caro para topo)

**Uso pratico:**
- Se CPA esta alto, testar posicao 3-4 vs 1-2
- Para keywords de baixa intencao, posicao 3-4 pode ter CVR similar com CPC 30-40% menor
- Para keywords de alta intencao (compra), posicao 1-2 justifica o premium

### 7. Match Type Performance no Bing

**Conceito:** Como Exact Match, Phrase Match e Broad Match performam no Bing vs Google.

**Diferenca critica:**

| Match Type | Bing vs Google |
|---|---|
| **Exact Match** | MENOS restritivo que Google. Bing exact match ainda mostra variacoes proximas, plurais, erros ortograficos. |
| **Phrase Match** | Comportamento similar ao Google mas mais permissivo |
| **Broad Match** | Muito menos agressivo que Google. Bing broad match gera menos variacoes irrelevantes. |

**Padrao de performance:**
- Exact Match Bing: maior CPC, maior CVR, menor volume
- Phrase Match Bing: equilibrio
- Broad Match Bing: menor CPC, menor CVR, maior volume (mas menos lixo que Google)

**Estrategia recomendada:**
- Use Exact Match para keywords de alta conversao
- Use Phrase Match como principal (bing exact e restritivo demais para volume)
- Use Broad Match com moderacao e negativos agressivos

### 8. Bing Audience Network Performance

**Conceito:** Metricas de performance da rede nativa/discovery da Microsoft (MSN, Edge, Outlook, Microsoft Start).

**Caracteristicas da Audiencia Network:**
- Nao e Display (nao e baseado em targeting de audiencia contextual como GDN)
- Nao e Search (nao ha intencao de busca)
- E hibrido: nativo + discovery + audiences
- CPCs 60-80% menores que Search
- CVR 60-80% menor que Search
- CTR muito menor que Search (0.1% - 0.5%)

**Quando usar:**
- Para capturar audiencia fria/topo de funil
- Para remarketing (baixo custo para manter presenca)
- Para produtos/servicos de consideracao curta e baixo tiquete
- Para branding com CPA aceitavel

**Quando evitar:**
- Para produtos de alto tiquete com ciclo de venda longo (CVR muito baixa)
- Para nichos muito especificos (pouca escala)
- Quando orcamento e muito limitado (priorizar Search)

**Metricas de sucesso:**
- CTR > 0.15%
- CPC < 50% do Search CPC
- CVR > 0.5% (se < 0.3%, repense)
- ROAS > 2:1 (ou margem permitir)

### 9. LinkedIn Profile Targeting Performance

**Conceito:** Segmentacao de campanhas Search por perfil profissional do LinkedIn (cargo, empresa, setor, formacao).

**Disponibilidade no Bing:**
- Funciona apenas em campanhas de Search (nao em Audience Network)
- Requer conta de anuncios vinculada ao LinkedIn
- Custa MAIS por clique (premium de ~20-40% sobre CPC normal)
- Reduz significativamente o volume de impressoes

**Performance tipica:**
- CPC: 20-40% maior que search sem segmentacao
- CVR: 30-60% MAIOR (audiencia mais qualificada)
- Volume: 50-80% MENOR
- CPA: Pode ser menor ou maior dependendo do nicho

**Quando usar:**
- B2B com publico profissional bem definido
- Produtos/servicos que so fazem sentido para certos cargos
- Segmentacao negativa (ex: excluir estudantes) em vez de targeting positivo

**Cuidados:**
- Nao usar em campanhas com pouco volume — a segmentacao pode estrangular o trafego
- Monitore diariamente nos primeiros 7 dias
- Prepare-se para CPC maior

---

## Camada 3 — Metricas de Investigacao Profunda

### 1. Atribuicao (Modelos no Bing)

**Modelos disponiveis no Bing Ads:**

| Modelo | Descricao | Quando usar |
|---|---|---|
| **Click (ultimo clique)** | Ultimo clique ganha toda a conversao | Default. Use quando nao quer complicar. |
| **Last Click** | Ultimo clique em qualquer canal | Similar ao click |
| **Click Assisted** | Mostra quantas conversoes tiveram assistencia de outros clicks | Para entender journey multiclick |
| **View-through** | Conversao apos visualizacao (sem clique) de Audience Ad | Audience Network apenas |

**Limitacoes vs Google:**
- Bing NAO tem Data-Driven Attribution
- Bing NAO tem modelos baseados em position
- Bing e limitado a modelos baseados em regras
- Bing NAO integra com GA4 para modelos de atribuicao (precisa de UET)

**Impacto pratico:**
- Se voce usa data-driven no Google, Bing vai sempre parecer "pior" porque o modelo de atribuicao e mais simples
- As conversoes "assisted" no Bing podem ser um indicador de que o modelo de ultimo clique e injusto com seus canais de topo de funil

### 2. UET (Universal Event Tracking) Health

**O que e:** Tag de tracking universal da Microsoft para Bing Ads. Similar ao Google Tag / Google Ads Conversion Tracking.

**Como verificar saude:**
- Ping/Test: Bing tem ferramenta de diagnostico UET no painel
- Verificar tag na pagina via browser console: `window.uetq`
- Verificar se o codigo UET carrega antes dos eventos de conversao
- Verificar duplicacao de tag (ter 2 tags UET na mesma pagina pode causar dupla contagem)

**Problemas comuns:**

| Problema | Sintoma | Solucao |
|---|---|---|
| Tag nao carrega | Zero conversoes | Verificar instalacao, adblockers, conflito com CMP |
| Duplicacao de tag | Conversoes 2x maiores que o real | Remover tag duplicada |
| Evento incorreto | Conversao registra sem acao real | Revisar codigo do evento |
| Delay no UET | Conversoes aparecem 24-48h depois | Normal — aguardar. Mas se > 72h, verificar. |
| Conflito com Google Tag | Tags competindo, latencia | Usar GTAG e UET juntos com cuidado |
| CMP/Consent blocking | Conversoes caem apos implementar CMP | Verificar se UET respeita consentimento |

**Metrica de saude:**
- Se > 10% de diferenca entre Bing Ads conversoes e conversoes reais (checkout, lead), investigue
- Use Microsoft Clarity para verificar comportamento do usuario na pagina

### 3. View-Through Conversions (Audience Ads)

**Conceito:** Conversao que ocorre quando um usuario ve um anuncio de Audience Network (sem clicar) e depois converte dentro da janela de view-through (geralmente 1-7 dias).

**Por que e controverso:**
- View-through conversion e menos confiavel que click-through
- Pode inflar metricas se a janela for muito longa (> 1 dia)
- Usuarios que veriam o anuncio de qualquer forma (brand awareness) sao atribuidos a Audience Network

**Quando considerar como valida:**
- Janela de 1 dia apenas (maximo 3 dias)
- Audience com baixa frequencia (< 5 sessoes por usuario)
- Produto de consideracao curta
- Cross-check com GA4 (se GA4 mostra conversao organica, view-through e duvidoso)

**Quando desconsiderar:**
- Janela > 3 dias
- Produto de alto tiquete (o usuario provavelmente converteria de qualquer forma)
- Frequencia alta de exibicao

### 4. Cross-Device Conversions

**Conceito:** Conversoes que comecam em um dispositivo e terminam em outro (ex: clicou no celular, comprou no desktop).

**Bing vs Google:**
- Google: Cross-devise e robusto (baseado em dados de login Google)
- Bing: Cross-device e limitado. Bing usa Microsoft Account login e dados do ecossistema Microsoft.

**Impacto:**
- Bing subestima cross-device comparado com Google
- Produtos que tem jornada cross-device (celular para pesquisa, desktop para compra) vaO parecer pior no Bing do que realmente sao
- Especialmente problematico para: e-commerce, servicos financeiros, viagens

**Como mitigar:**
- Use modelos de atribuicao de ultimo clique no dispositivo onde a conversao realmente aconteceu
- Configure UET para capturar dados de login (quando possivel)
- Aceite que Bing vai reportar menos conversoes cross-device — isso nao significa que o canal e pior

### 5. Assisted Conversions

**Conceito:** Conversoes onde o Bing Ads contribuiu mas nao teve o ultimo clique.

**Por que importa:**
- Modelo de ultimo clique penaliza canais de topo de funil
- Bing geralmente atua como canal de descoberta/consideracao
- Assisted conversions podem mostrar o valor real do Bing que o ultimo clique esconde

**Interpretacao:**
- Se Bing tem alto assisted conversion rate (> 30% das conversoes totais), Bing esta sendo um canal de topo de funil importante
- Se Bing tem baixo assisted mas alto direct conversion, Bing e canal de conversao direta

### 6. Auto-Bidding Analysis

**Estrategias de lance automatico no Bing:**

| Estrategia | Disponibilidade | Comportamento | Quando usar |
|---|---|---|---|
| **Enhanced CPC (ECPC)** | Search + Shopping | Ajusta lances quando a conversao e mais provavel | Default seguro para contas sem dados |
| **Maximize Clicks** | Search | Gasta todo o orcamento para maximizar clicks | Branding, awareness, remarketing |
| **Maximize Conversions** | Search | Maximiza conversoes dentro do orcamento | Contas com historico de conversao |
| **Target CPA** | Search | Tenta atingir CPA desejado | Contas com 30+ conversoes nos ultimos 30 dias |
| **Target ROAS** | Search | Tenta atingir ROAS desejado | E-commerce com dados de receita |
| **Manual CPC** | Tudo | Controle total | Contas novas, contas pequenas, nichos |

**Diferencas vs Google:**
- Bing NAO tem Portfolio Bid Strategies
- Target CPA no Bing e MENOS preciso que Google (precisa de mais dados de conversao)
- Maximize Conversions no Bing as vezes nao gasta todo o orcamento (bug conhecido)
- ECPC no Bing aumenta menos o CPC que no Google (mais conservador)

**Quando NAO usar auto-bidding:**
- Conta com < 30 conversoes nos ultimos 30 dias
- Campanha nova (< 2 semanas)
- Alteracoes recentes de tracking/pagina
- Conta com dado de conversao inconsistente

### 7. Experimentos (Bing Experiment)

**O que e:** Recurso para testar variacoes de campanha (similar aos experiments do Google).

**Limitacoes:**
- Apenas Search campaigns
- Divisao 50/50 apenas
- Duracao minima recomendada: 2 semanas
- NAO funciona com algumas estrategias de lance automatico (Target CPA/ROAS nao sao ideais para experiments)
- Menos dados estatisticos que Google Experiments

**Quando usar:**
- Testar mudanca de copy do anuncio
- Testar alteracao de lances
- Testar mudanca de match type
- Testar landing pages diferentes

**Quando NAO usar:**
- Orcamento muito pequeno (experiment divide orcamento — campanha pode ficar inviavel)
- Periodo de learning de auto-bidding
- Alteracoes estruturais grandes (melhor fazer backup e criar nova)

### 8. Goal Tracking Deep Dive

**Conceito:** Analise detalhada dos goals configurados no UET.

**O que verificar:**
- Meta esta configurada corretamente?
- Valor da conversao esta sendo passado?
- Categoria/goal name esta correto?
- Ha goals duplicados?
- Janela de conversao adequada?

**Problemas comuns:**
- Goal de pagina de obrigado capturando tambem reloads da pagina
- Goal de lead capturando envios de formulario com erro
- Valor fixo em vez de dinamico (passar valor real do pedido)
- Count: Every (toda conversao conta) vs Unique (apenas uma por clique)

### 9. Remarketing List Performance

**Conceito:** Analise das listas de remarketing no Bing Ads.

**Limitacoes vs Google:**
- Tamanho minimo da lista: Bing exige 300 usuarios (Google: 100)
- Bing oferece menos tipos de lista (nao tem lista baseada em YouTube, Gmail, etc.)
- Duração maxima de membership: 180 dias (Google: 540 dias)
- Menos opcoes de combinacao de listas

**Metricas de performance:**
- Tamanho da lista vs impressoes possiveis
- CPC vs search normal (remarketing costuma ser 30-50% mais barato)
- CVR do remarketing vs search normal
- Frequencia ideal: 3-7 sessoes (abaixo disso: pouco impacto; acima: desperdicio)

**Estrategia de remarketing no Bing:**
- Product/service page viewers (para produtos)
- Cart abandoners (maior intencao)
- Past purchasers (para cross-sell/upsell)
- Lead form abandoners
- Blog visitors (topo de funil, alimentar com oferta)

---

## Contextos x Metricas — Cenarios Especificos

### Cenario 1: "Performance boa no Google mas ruim no Bing (mesmo targeting)"

**Por que acontece:**
- Bing tem audiencia diferente — as mesmas keywords podem ter intencao diferente
- Quality Score inicial baixo no Bing afeta lances e posicao
- Landing page pode ser otimizada para audiencia Google, nao para Bing
- UET tag pode estar mal configurada

**O que verificar (em ordem):**
1. UET tag esta funcionando? (teste no navegador)
2. Quality Score das principais keywords
3. Posicao media vs Google
4. Dispositivo breakdown (seu produto funciona em desktop?)
5. Search Partners vs Search puro — Partners estao puxando performance para baixo?
6. Copy do anuncio — Bing pode responder melhor a headlines diferentes
7. Landing page — Bing publico desktop-first, landing page e responsiva?

**Resolucao tipica:**
- Ajustar lances para Bing (nao copiar do Google)
- Criar copy especifica para Bing (testar tom mais profissional)
- Verificar se UET tag nao esta com delay
- Desligar Search Partners temporariamente
- Aumentar lances em desktop, reduzir mobile

### Cenario 2: "Search Partners drenam orcamento com conversao baixa"

**Diagnostico:**
- Search Partners consomem 25-40% do orcamento
- Search Partners geram 5-15% das conversoes
- CPA em Partners e 3-5x maior que Search puro

**O que fazer:**
1. Verifique breakdown de Search Partners vs Search puro
2. Se CPA Partners > 3x Search puro por 14 dias: desligue
3. Se CPA Partners entre 1.5x e 3x: avalie margem do produto — talvez ainda valha
4. Se Partners tem CVR decente mas CPC muito baixo: considere manter
5. Monitore por 7 dias apos mudanca

**Excecao:**
Campanhas de branding ou awareness onde baixo CPA nao e o objetivo principal. Partners geram volume a baixo custo — mesmo que nao convertam, geram exposicao.

### Cenario 3: "CPA mais baixo que Google mas volume insuficiente"

**Contexto:** Bing esta entregando CPA 20-40% menor que Google, mas com apenas 10-20% do volume.

**Analise:**
- Isso e COMUM no Bing — acontece porque a audiencia e menor mas mais qualificada
- O problema nao e Bing — e que ele e complementar, nao substituto
- Ou o orcamento esta mal distribuido entre as plataformas

**O que fazer:**
1. Verifique se ha orcamento disponivel nao gasto (impression share lost to budget?)
2. Se sim: aumente orcamento gradualmente (+30% a cada 3 dias) ate encontrar o ponto de CPA aceitavel
3. Se nao: expanda keywords (Bing responde bem a keywords long tail)
4. Teste Phrase/Broad Match para capturar mais volume
5. Considere Audience Network para awareness + remarketing
6. Aceite que Bing pode nunca ter o volume do Google — e OK se o CPA for consistentemente menor

**Regra pratica:** Se Bing tem CPA 30% menor que Google com > 10% do volume do Google, Bing esta performando BEM. Escale.

### Cenario 4: "CTR muito baixo apesar de boa posicao"

**Diagnostico:**
- Posicao media 1.5-2.5, mas CTR < 1.5%
- Geralmente significa: copy do anuncio nao e atraente para a audiencia Bing

**Por que acontece:**
- Copy foi importado do Google e nao funciona no Bing
- Headline nao chama atencao para o usuario Bing (que e diferente)
- Extensoes de anuncio ausentes ou fracas
- URL visivel nao e atraente

**O que fazer:**
1. Teste headlines diferentes (tom mais profissional, mais direto)
2. Adicione e otimize sitelinks, callouts, snippets estruturados
3. Inclua palavras-chave no headline (Bing valoriza match visual)
4. Teste ofertas e CTAs diferentes
5. Verifique concorrencia — concorrentes estao com extensoes agressivas?

**Benchmark:** CTR Bing Search medio e 2.2-3.5% (dependendo do setor). Abaixo de 1.5% merece investigacao em posicao 1-3.

### Cenario 5: "Bing Audience Network converte mas atribuicao e confusa"

**Contexto:** Audience Network mostra conversoes mas voce nao ve o valor real — parece que as conversoes aconteceriam de qualquer forma.

**Analise:**
- View-through conversions geralmente inflam metricas
- Audience Network e topo de funil — atribuir conversao direta e injusto
- Mas audience network gera awareness que alimenta search e remarketing

**O que fazer:**
1. Separe as metricas: click-through conv vs view-through conv
2. Analise apenas click-through para decisoes de otimizacao direta
3. Use view-through como "branding medido" — nao como conversao real
4. Compare com GA4 — se GA4 nao mostra essas conversoes, desconsidere para ROAS
5. Considere janela de view-through MAXIMO 1 dia

**Regra:** Bing Audience Ads = canal de awareness. Avalie por CPA de click-through e CVR, nao por ROAS total.

### Cenario 6: "LinkedIn targeting nao esta performando"

**Contexto:** Ativou segmentacao profissional no Bing e o CPA subiu, volume caiu, e conversao nao melhorou.

**Diagnosticos possiveis:**
1. Segmentacao muito restrita — poucas impressoes, lances precisam ser muito altos para ganhar
2. Publico segmentado nao e o publico que compra (cargo errado, empresa muito grande)
3. O premium de CPC (+20-40%) nao esta sendo compensado por CVR maior

**O que fazer:**
1. Amplie a segmentacao (ex: em vez de "CEO", use "Director+")
2. Teste sem segmentacao vs com segmentacao em experimento
3. Use LinkedIn targeting como NEGATIVO (excluir estudantes, estagiarios) em vez de positivo
4. Verifique se a conta esta vinculada corretamente ao LinkedIn
5. Segmentacao profissional funciona MELHOR para B2B que B2C — aceite se for B2C

### Cenario 7: "Diferenca de conversoes entre Bing e GA4"

**Contexto:** Bing reporta 50 conversoes, GA4 reporta 35. Qual esta certa?

**Analise:**
- Diferenca de 10-30% entre plataformas e NORMAL
- Bing usa UET, GA4 usa gtag — sao metodos de tracking diferentes
- Modelos de atribuicao diferentes: Bing usa ultimo clique Microsoft, GA4 usa data-driven (ou ultimo clique)

**Causas comuns:**
- UET mal configurado (duplicando eventos)
- GA4 bloqueado por adblocker (Bing UET pode ser bloqueado tambem, mas de forma diferente)
- Janela de conversao diferente (Bing 30 dias, GA4 90 dias)
- Conversao view-through contada no Bing, ignorada no GA4
- Cross-device capturado diferente

**Resolucao:**
1. Configure goals identicos em ambas as plataformas
2. Use mesma janela de atribuicao
3. Ignore view-through para comparacao
4. Aceite variacao de 15-25% como normal
5. Para fechar relatorio: use dados da plataforma onde a conversao realmente aconteceu

### Cenario 8: "Remarketing no Bing nao escala"

**Contexto:** Listas de remarketing com 300-1000 usuarios que nao geram volume significativo.

**Diagnostico:**
- Bing tem menos usuarios que Google — listas de remarketing sao naturalmente menores
- Tamanho minimo de 300 usuarios e maior que Google (100)
- Bing requer audiencias maiores para entregar volume significativo

**O que fazer:**
1. Amplie a janela de membership para 180 dias (maximo)
2. Combine listas similares para aumentar o tamanho (ex: todos que visitaram qualquer pagina de produto)
3. Use listas de "pagina inicial + blog" para topo de funil
4. Se mesmo assim nao escala: aceite que Bing tem remarketing limitado e invista em Search + Audience Network como alternativa
5. Teste RLSA (Remarketing Lists for Search Ads) — Bing permite ajustar lances para usuarios que ja visitaram o site

### Cenario 9: "Microsoft Shopping vs Google Shopping"

**Contexto:** Produtos no Microsoft Shopping com performance muito diferente do Google Shopping.

**Diferencas estruturais:**

| Aspecto | Google Shopping | Microsoft Shopping |
|---|---|---|
| **Alcance** | Maior | 10-30% do volume Google |
| **CPC** | $0.50 - $2.00 | $0.20 - $0.80 |
| **Feed** | Merchant Center | Microsoft Merchant Center |
| **Otimizacao** | Avancada | Basica |
| **Promocoes** | Sim | Limitado |
| **Atributos** | Completos | Menos atributos suportados |

**O que fazer:**
1. Feed do Microsoft Merchant Center precisa ser separado — nao use o mesmo feed do Google sem adaptar
2. Otimize titulos e descricoes para o Bing (palavras-chave diferentes)
3. Microsoft Shopping favorece produtos com boa taxa de frete e avaliacoes
4. Ajuste lances — nao copie do Google
5. Considere que o publico Bing compra mais em desktop e horario comercial

### Cenario 10: "Migracao de Search para Audience Network"

**Contexto:** Transferindo orcamento do Search para Audience Network para baratear CPA.

**Analise:**
- Audience Network tem CPC muito menor, mas CVR menor ainda
- CPA final pode ser maior ou menor — depende do produto e da audiencia
- Audience Network e canal de TOPO DE FUNIL — migrar todo o orcamento de Search (fundo de funil) para Audience e suicidio de performance

**Regra:**
- Audience Network = 10-30% do orcamento total (nao mais)
- Mantenha Search como base
- Audience e complementar para awareness e remarketing
- Produtos de baixo tiquete (< R$ 200) podem usar mais Audience
- Produtos de alto tiquete (> R$ 500) devem priorizar Search

---

## Diferencas Bing vs Google (Secao Critica)

### Tabela Comparativa Geral

| Aspecto | Bing Ads | Google Ads |
|---|---|---|
| **Share de mercado (global)** | 3-8% | 85-92% |
| **Share (EUA desktop)** | 15-25% | 60-70% |
| **CPC medio** | 40-60% do Google | Referencia |
| **Audiencia predominante** | 35+ anos, desktop, maior renda | 25-54, mobile, massa |
| **Tipos de campanha** | 8 tipos | 15+ tipos |
| **Estrategias de lance** | 6 (sem portfolio) | 10+ (com portfolio) |
| **Quality Score** | Similar, mas pesa historico | Similar, mas pesa CTR |
| **Atribuicao** | Ultimo clique + view-through | Data-driven + 6 modelos |
| **Targeting** | Demografico + LinkedIn + Audiencias | Demografico + Afinidade + No Mercado + YouTube + Gmail + App |
| **Extensoes de anuncio** | 7 tipos | 12+ tipos |
| **Remarketing** | Limitado (lista + RLSA) | Avancado (lista + similar + YouTube + Gmail) |
| **Shopping** | Basico | Avancado |
| **DSA** | Sim (limitado) | Sim (avancado) |
| **Experimentos** | Sim (limitado) | Sim (avancado) |
| **Integracao nativa** | LinkedIn, Office 365, Windows | GA4, YouTube, Gmail, Maps, Play Store |
| **API** | Completa (SOAP/REST) | Completa (gRPC/REST) |
| **Scripts** | No (apenas via API) | Sim (Google Ads Scripts) |
| **Automation rules** | Sim (basico) | Sim (avancado) |
| **Custom alerts** | Sim (basico) | Sim (avancado) |
| **Ferramentas editor** | Microsoft Advertising Editor | Google Ads Editor |

### Quality Score: Bing vs Google

**Componentes e pesos:**

| Componente | Bing | Google |
|---|---|---|
| Expected CTR | Muito alto | Muito alto |
| Ad Relevance | Alto | Alto |
| Landing Page Experience | Medio-Alto | Alto |
| Historical Account Performance | **Alto** | Baixo-Medio |
| Ad Extensions Impact | Baixo | **Alto** |
| Device Performance | **Separado** | Integrado ao CTR |

**Diferenca pratica:**
- **Bing:** Conta nova comeca com QS baixo e sobe com o tempo. O historico da conta influencia MUITO. Ter uma conta com historico positivo ajuda novas campanhas.
- **Google:** QS e mais volátil — muda rapidamente com alteracoes de copy, landing page, CTR. Extensoes tem peso significativo.

**O que isso significa para o gestor:**
- Bing: Nao desista de keywords com QS baixo na primeira semana — o QS pode subir com o tempo
- Google: Otimize copy e extensoes primeiro — o impacto no QS e rapido
- Bing: Contas com historico de boa performance tem "credito" para novas campanhas
- Google: Cada campanha e mais independente

### Estrategias de Lance: Bing vs Google

| Estrategia | Bing | Google | Diferenca |
|---|---|---|---|
| Manual CPC | Completo | Completo | Similares |
| Enhanced CPC | Sim | Sim | Bing mais conservador |
| Maximize Clicks | Sim | Sim | Bing as vezes nao gasta tudo |
| Maximize Conversions | Sim | Sim | Bing menos preciso |
| Target CPA | Sim | Sim | Bing precisa de mais dados (30+ conversoes) |
| Target ROAS | Sim | Sim | Bing menos estavel |
| Target Impression Share | **Nao** | Sim | Google exclusivo |
| Portfolio Bid Strategies | **Nao** | Sim | Google exclusivo |
| Maximize Conversion Value | Sim | Sim | Bing menos preciso |
| Seasonal Adjustments | Manual | Automatico | Bing requer ajuste manual |

**Implicacao pratica:**
- Se voce usa Smart Bidding no Google com sucesso, Bing vai parecer menos inteligente
- Bing exige mais controle manual
- Auto-bidding no Bing funciona melhor com mais dados (do que Google)

### Rede de Display: Bing Audience Ads vs Google Display Network (GDN)

| Aspecto | Bing Audience Ads | Google Display Network |
|---|---|---|
| **Alcance** | 60-90M usuarios (EUA) | 2B+ usuarios global |
| **Formatos** | Nativo, Banner, Video | Nativo, Banner, Video, Interstitial, Gmail |
| **Targeting** | Demografico, Remarketing, LinkedIn, In-market | Afinidade, No Mercado, Remarketing, Similar, Demografico, Contextual, YouTube |
| **CPC** | $0.05 - $0.30 | $0.10 - $1.00 |
| **CTR** | 0.05% - 0.30% | 0.05% - 0.50% |
| **CVR** | 0.2% - 1.0% | 0.2% - 1.5% |
| **Qualidade de audiencia** | Media (profissional, corporativa) | Varia muito |
| **Controle de posicoes** | Baixo (apenas ecossistema MS) | Alto (milhares de sites) |
| **Remarketing** | Sim (limitado) | Sim (avancado) |

**Conclusao:** Bing Audience Ads nao compete com GDN — sao complementares. Audience Ads tem menos alcance mas audiencia mais qualificada (profissional).

### Remarketing: Bing vs Google

| Aspecto | Bing | Google |
|---|---|---|
| **Tamanho minimo** | 300 usuarios | 100 usuarios |
| **Duracao maxima** | 180 dias | 540 dias |
| **Tipos de lista** | Visitantes do site, Produtos vistos | Visitantes, Produtos, YouTube, Gmail, Apps, Similares |
| **Combinacao de listas** | Sim (AND/OR) | Sim (AND/OR/NOT) |
| **RLSA (search)** | Sim (ajuste de lance) | Sim (ajuste + bid only) |
| **Audiencias similares** | **Nao** | Sim |
| **Segmentacao por pagina** | Sim | Sim |
| **Segmentacao por evento** | Sim | Sim (avancado) |
| **Frequencia cap** | Sim | Sim |

**Conclusao:** Remarketing no Bing funcional mas MUITO menos poderoso que Google. Nao espere mesma escala ou sofisticacao.

### Atribuicao: Bing UET vs Google Ads

| Aspecto | Bing UET | Google Ads |
|---|---|---|
| **Modelos** | Ultimo clique, View-through | Data-driven, Ultimo clique, Primeiro clique, Linear, Baseado em posicao, Time decay |
| **Janela de conversao** | 1-90 dias (configuravel) | 1-90 dias |
| **View-through** | Sim (1-7 dias) | Sim (1-30 dias) |
| **Cross-device** | Limitado (logado Microsoft) | Avancado (login Google) |
| **Cross-platform** | **Nao** | Sim (YouTube, Gmail, Display, Search) |
| **Integracao GA4** | Manual (importar goals) | Nativa |
| **Dados de receita** | Sim (via UET) | Sim (via Google Tag + GA4) |
| **Precisao** | Media | Alta |

**Conclusao:** Bing perde feio em atribuicao. Se atribuicao e critica para seu negocio, Google e a plataforma superior para entender jornada do cliente.

### Shopping: Microsoft Merchant Center vs Google Merchant Center

| Aspecto | Microsoft Merchant Center | Google Merchant Center |
|---|---|---|
| **Alcance** | 5-15% do volume Google | Referencia |
| **Feed** | CSV/XML/API | CSV/XML/API/Content API |
| **Atributos de produto** | 30+ atributos | 60+ atributos |
| **Promocoes** | Sim (basico) | Sim (avancado) |
| **Avaliacoes** | Sim (integracao) | Sim (nativo) |
| **Regras de feed** | Sim (basico) | Sim (avancado) |
| **Programas** | None | Shopping Ads, Shopping Actions, Buy on Google, Local Inventory |
| **Otimizacao** | Manual | Sugestoes automaticas |
| **Suporte** | Basico | Avancado |

**Conclusao:** Microsoft Shopping existe e funciona, mas esta atrasado em relacao ao Google Shopping. Feed precisa ser otimizado separadamente.

### Importacao de Campanhas do Google (como funciona, riscos)

**Funcionamento:**
Bing Ads permite importar campanhas diretamente do Google Ads — copia keywords, copy, lances, extensoes, configuracoes.

**O que e importado:**
- Keywords e match types
- Copy do anuncio (headlines, descriptions)
- Lances (CPC maximo)
- Extensoes (sitelinks, callouts, snippets)
- Segmentacao (geografica, idioma, dispositivo)
- Grupos de anuncios e estrutura de campanha
- Negativos

**O que NAO e importado:**
- Quality Score (recalculado do zero no Bing)
- Dados historicos de performance
- Smart Bidding configuracoes (converte para ECPC)
- Attribution models
- Google-specific extensions (price, promotion, app)
- Responsive Search Ads (converte para Expanded Text Ads)
- Performance Max (ignorado)
- Call-only ads
- Discovery campaigns

**Riscos da importacao:**

1. **Lances importados sao muito altos para Bing** — Google CPC medio e maior. Se importar o mesmo lance, voce vai pagar mais que o necessario no Bing.
2. **Match types se comportam diferente** — Exact match no Bing e menos restritivo. Voce pode estar competindo em variacoes que nao esperava.
3. **Copy do anuncio pode nao funcionar** — O tom que funciona no Google pode nao funcionar no Bing (audiencia diferente).
4. **Segmentacao geografica pode ser imprecisa** — Bing trata algumas localizacoes de forma diferente.
5. **Orcamento diario pode ser inadequado** — Bing entrega de forma diferente que Google.
6. **Extensoes importadas podem quebrar** — Bing nao suporta todas as extensoes do Google.

**Melhor pratica apos importar:**
1. Reduza lances em 30-50% como ponto de partida
2. Crie copy nova para Bing (nao use a importada)
3. Ajuste match types para comportamento Bing
4. Monitore diariamente por 7-14 dias
5. Reotimize baseado em performance real, nao nos dados do Google

---

## Protocolo de Leitura de Cenarios

### Fluxo Logico do LLM ao receber dados de Bing Ads

```
1. RECEBER dados de Bing Ads (metricas, periodo, contexto)
   ├─ Periodo minimo para analise: 7 dias (ideal 14-30 dias)
   └─ Contexto necessario: setor, objetivo, orcamento, benchmark se disponivel

2. VERIFICAR INTEGRIDADE dos dados
   ├─ UET tag funcionando? (se sem conversoes, suspeitar de UET)
   ├─ Search Partners vs Search puro? (sempre verificar breakdown)
   ├─ Dispositivo? (desktop vs mobile)
   └─ Conta nova ou estabelecida? (contas novas precisam de mais tempo)

3. CAMADA 1 — Ler metricas de operacao
   ├─ Se tudo OK → reportar como "saudavel", recomendar proximos passos
   ├─ Se amarelo em alguma metrica → ir para passo 4
   └─ Se vermelho → ir para passo 4 + nota de urgencia

4. IDENTIFICAR METRICA PROBLEMA
   ├─ Qual metrica esta fora do esperado?
   ├─ Ha correlacao com outra metrica? (ex: CPC subiu junto com queda de QS)
   └─ Ha variavel externa? (sazonalidade, concorrencia, feriado?)

5. CAMADA 2 — Diagnosticar a metrica problema
   ├─ Verificar breakdown relevante (dispositivo, search partners, match type, audiencia)
   ├─ Verificar Quality Score
   ├─ Verificar impression share (lost to rank vs budget)
   └─ Se causa encontrada → recomendar acao

6. CAMADA 3 — Se causa nao encontrada na Camada 2
   ├─ Verificar UET health
   ├─ Verificar modelo de atribuicao
   ├─ Verificar experimentos/alteracoes recentes
   ├─ Verificar dados de GA4 para cross-check
   └─ Se causa ainda nao encontrada → reportar como anomalia

7. RECOMENDAR ACAO
   ├─ Acao especifica (o que fazer, quando, como medir)
   ├─ Prazo para reavaliacao (quando verificar se funcionou)
   └─ Risco da acao (o que pode dar errado)
```

### Template de Resposta do LLM

```
── ANALISE BING ADS ──
Periodo: [data] a [data]
Conta: [nome]
Setor: [setor]
Objetivo: [CPA/ROAS/volume]

── CAMADA 1 — OPERACAO ──
[Click/Impressoes/Gasto] vs periodo anterior: [▲/▼ X%]
CPC: [R$ X.XX] (benchmark: R$ X.XX)
CTR: [X.X%] (benchmark: X.X%)
CVR: [X.X%] (benchmark: X.X%)
CPA: [R$ X.XX] vs target: R$ X.XX [VERDE/AMARELO/VERMELHO]
ROAS: [X.X:1] [VERDE/AMARELO/VERMELHO]
Impression Share: [X%] lost to [rank/budget/misto]

── DIAGNOSTICO ──
Sinais de alerta: [lista de metricas amarelo/vermelho]
Causa provavel (Camada 2): [diagnostico]
Investigacao adicional (Camada 3, se aplicavel): [detalhe]

── RECOMENDACOES ──
1. [Acao 1 — prioridade alta]
2. [Acao 2 — prioridade media]
3. [Acao 3 — prioridade baixa]

── PROXIMA REAVALIACAO ──
[data sugerida] — verificar se recomendacoes surtiram efeito
```

---

## Arvores de Decisao

### Arvore 1: CPA alto vs Google (comparativo)

```
BING CPA > GOOGLE CPA?
│
├─ SIM
│  ├─ Bing tem mesma janela de conversao que Google?
│  │  ├─ NAO → Ajuste janela de conversao. Reavalie em 7 dias.
│  │  └─ SIM
│  │     ├─ UET tag funcionando corretamente?
│  │     │  ├─ NAO → Corrigir UET tag. Reavalie em 3 dias.
│  │     │  └─ SIM
│  │     │     ├─ Device breakdown: Desktop ok?
│  │     │     │  ├─ NAO → Otimizar landing page para desktop ou ajustar lances mobile
│  │     │     │  └─ SIM
│  │     │     │     ├─ Search Partners estao inflando CPA?
│  │     │     │     │  ├─ SIM → Desligar Search Partners. Reavalie em 7 dias.
│  │     │     │     │  └─ NAO
│  │     │     │     │     ├─ Quality Score das keywords e baixo?
│  │     │     │     │     │  ├─ SIM → Melhorar copy, landing page, relevancia
│  │     │     │     │     │  └─ NAO
│  │     │     │     │     │     └─ Bing pode ter audiencia diferente → CPA naturalmente maior
│  │     │     │     │     │        Se CPA Bing esta dentro de 1.5x do Google com menos volume, e aceitavel
│  │     │     │     │     │        Se > 2x, investigue mais fundo (Camada 3)
│  │     │     │     │     └─ ...
│  │     │     │     └─ ...
│  │     │     └─ ...
│  │     └─ ...
│  └─ ...
│
└─ NAO (BING CPA < GOOGLE CPA)
   ├─ Volume do Bing e suficiente?
   │  ├─ SIM → Otimo. Escale orcamento gradualmente (+20% a cada 3 dias)
   │  └─ NAO → Expandir keywords, testar Phrase/Broad Match, verificar Impression Share
   └─ ...
```

### Arvore 2: Search Partners ruins vs bons

```
SEARCH PARTNER ATIVO?
│
├─ SIM
│  ├─ CPA Partners vs Search puro:
│  │  ├─ > 3x puro → DESLIGUE imediatamente. Perda de orcamento.
│  │  ├─ 2x - 3x puro → Avalie margem do produto
│  │  │  ├─ Margem alta (> 50%) → Mantenha, monitore semanal
│  │  │  └─ Margem baixa (< 30%) → Desligue ou reduza lances em 30%
│  │  └─ < 2x puro → Mantenha, Partners estao performando bem
│  │
│  ├─ Volume Partners vs conversoes:
│  │  ├─ Partners > 30% do gasto, < 10% das conversoes → Desligue
│  │  ├─ Partners 20-30% do gasto, 10-20% das conversoes → Monitore
│  │  └─ Partners < 20% do gasto → Provavelmente ok
│  │
│  └─ Decisao final:
│     ├─ Desligar → monitore search puro por 7 dias (deve melhorar CPA)
│     └─ Manter → verifique relatorio semanal de Partners
│
└─ NAO (desligado)
   └─ Considere religar em campanhas de branding ou quando precisar de volume extra
```

### Arvore 3: Impression Share baixo

```
IMPRESSION SHARE < 70%?
│
├─ SIM
│  ├─ Perde por budget?
│  │  ├─ SIM (lost to budget > 50% da perda)
│  │  │  ├─ CPA/ROAS estao positivos?
│  │  │  │  ├─ SIM → Aumente orcamento gradualmente (+20-30%)
│  │  │  │  └─ NAO → Otimize CPA/ROAS primeiro (nao adianta gastar mais em campanha negativa)
│  │  │  └─ ...
│  │  └─ NAO
│  │
│  ├─ Perde por rank?
│  │  ├─ SIM (lost to rank > 50% da perda)
│  │  │  ├─ Quality Score baixo?
│  │  │  │  ├─ SIM → Melhore QS (copy, landing page, relevancia)
│  │  │  │  └─ NAO → Aumente lances em 15-20%, reavalie
│  │  │  └─ ...
│  │  └─ NAO
│  │
│  └─ Misto? Ataque ambos: melhore QS + ajuste lances + otimize orcamento
│
└─ NAO (IS > 70%) → Nao e prioridade. Monitore.
```

### Arvore 4: CTR baixo com boa posicao

```
POSICAO 1-3 MAS CTR < 2%?
│
├─ SIM
│  ├─ Copy importado do Google?
│  │  ├─ SIM → Crie copy especifica para Bing (tom mais profissional)
│  │  └─ NAO → Teste variacoes de headline
│  │
│  ├─ Headlines e Descricoes:
│  │  ├─ Headlines tem palavras-chave estrategicas?
│  │  │  ├─ NAO → Adicione keywords principais nas headlines
│  │  │  └─ SIM
│  │  │     ├─ Ha oferta clara no anuncio?
│  │  │     │  ├─ NAO → Adicione oferta/diferencial no copy
│  │  │     │  └─ SIM
│  │  │     │     ├─ Extensoes estao configuradas?
│  │  │     │     │  ├─ NAO → Adicione sitelinks, callouts, snippets
│  │  │     │     │  └─ SIM
│  │  │     │     │     ├─ Concorrentes tem extensoes melhores?
│  │  │     │     │     │  ├─ SIM → Melhore suas extensoes
│  │  │     │     │     │  └─ NAO
│  │  │     │     │     │     └─ Possivel: audiencia Bing responde diferente ao copy
│  │  │     │     │     │        → Teste tons: profissional, direto, beneficios vs funcionalidades
│  │  │     │     │     └─ ...
│  │  │     │     └─ ...
│  │  │     └─ ...
│  │  └─ ...
│  └─ ...
│
└─ NAO → CTR aceitavel para posicao e setor
```

### Arvore 5: Bing Audience Ads vs Search

```
DEVO ALOCAR ORCAMENTO EM AUDIENCE NETWORK?
│
├─ Produto e de alto tiquete (> R$ 500)?
│  ├─ SIM → Audience so para remarketing (max 15% do orcamento)
│  └─ NAO
│     ├─ Produto e de baixo tiquete (< R$ 100)?
│     │  ├─ SIM → Audience pode ser 20-40% do orcamento
│     │  └─ NAO → Audience 10-25% do orcamento
│     └─ ...
│
├─ Voce tem audiencia de remarketing ativa?
│  ├─ NAO → Comece com Search, depois audiencia
│  └─ SIM → Audience para remarketing + prospecting basico
│
├─ Orcamento e limitado?
│  ├─ SIM → Priorize Search (Audience pode ser desperdicio com pouco orcamento)
│  └─ NAO → Teste Audience com 15% do orcamento por 30 dias
│
└─ Conclusao:
   ├─ Search primeiro, Audience como complemento
   ├─ CVR Audience e sempre menor — aceite como canal de topo de funil
   └─ Meça Audience por CPA de click-through, nao por ROAS total
```

### Arvore 6: Campanha importada do Google nao performa

```
IMPORTACAO DO GOOGLE NAO PERFORMA NO BING?
│
├─ Quanto tempo desde a importacao?
│  ├─ < 7 dias → Aguarde learning period (Bing precisa de 48-72h)
│  ├─ 7-14 dias → Continue monitorando, ajuste fino
│  └─ > 14 dias → Problema estrutural
│
├─ Lances importados vs performance:
│  ├─ CPC esta maior que no Google?
│  │  ├─ SIM → Reduza lances em 30% (lances do Google sao altos para Bing)
│  │  └─ NAO
│  │     └─ ...
│  └─ ...
│
├─ Copy importado funciona no Bing?
│  ├─ CTR < 1.5%? → Crie copy novo para Bing
│  └─ CTR OK? → Copy nao e o problema
│
├─ Match types estaveis?
│  ├─ Exact match Bing menos restritivo → adicione mais negativos
│  └─ Phrase match OK → Continue monitorando
│
├─ Segmentacao geografica correta?
│  ├─ Bing pode tratar cidades/estados diferente do Google
│  └─ Verifique configuracoes de local
│
└─ Recomendacao:
   ├─ Nao confie na importacao — use como rascunho, reotimize manualmente
   ├─ Reduza lances em 30-50%, crie copy novo, ajuste match types
   └─ Monitore por 14 dias antes de comparar com Google
```

### Arvore 7: Volume insuficiente (Bing e pequeno ou configuracao errada?)

```
VOLUME BING ABAIXO DO ESPERADO?
│
├─ Verificar 1: Campanha esta ativa e aprovada?
│  ├─ NAO → Ativar/consertar aprovacao
│  └─ SIM
│
├─ Verificar 2: Keywords tem volume no Bing?
│  ├─ Use ferramenta de planejamento de keywords do Bing
│  ├─ Algumas keywords com volume alto no Google tem volume baixo no Bing
│  └─ Se volume estimado da keyword e < 100/mes: esperado
│
├─ Verificar 3: Impression Share?
│  ├─ IS < 50% lost to budget → Aumente orcamento
│  ├─ IS < 50% lost to rank → Melhore QS ou aumente lances
│  └─ IS > 70% com volume baixo → Bing realmente tem pouco volume para suas keywords
│
├─ Verificar 4: Match types estao restritivos demais?
│  ├─ So Exact Match? → Adicione Phrase Match (2-3x mais volume)
│  ├─ So Phrase Match? → Teste Broad Match com negativos
│  └─ Mistura saudavel? → OK
│
├─ Verificar 5: Segmentacao esta restritiva demais?
│  ├─ LinkedIn targeting ativado e restringindo? → Desligue ou amplie
│  ├─ Local muito especifico? → Amplie raio
│  └─ Dispositivo segmentado? → Bing e desktop-first, nao restrinja desktop
│
├─ Verificar 6: Concorrencia no leilao?
│  ├─ Menos concorrentes no Bing que Google → esperado
│  └─ Concorrente dominando leilao? → Aumente lances para competir
│
└─ Conclusao:
   ├─ Se todas as verificacoes OK e volume continua baixo:
   │  Bing pode ser naturalmente pequeno para seu nicho → aceite como complementar
   ├─ Se alguma verificacao revelou problema:
   │  Corrija e monitore por 7 dias
   └─ Benchmark realista: Bing = 5-20% do volume do Google para mesmas keywords
```

### Arvore 8: Remarketing no Bing nao escala

```
REMARKETING BING SEM VOLUME?
│
├─ Tamanho da(s) lista(s):
│  ├─ < 300 usuarios → Lista nao ativa (minimo Bing: 300)
│  │  ├─ Solucao curto prazo: Combine listas (ex: todas paginas de produto)
│  │  └─ Solucao longo prazo: Aumente trafego no site
│  ├─ 300 - 1.000 usuarios → Lista ativa mas pequena
│  │  ├─ Aumente janela de membership para 180 dias
│  │  └─ Considere RLSA em vez de campanha separada de remarketing
│  ├─ 1.000 - 5.000 usuarios → Lista com potencial
│  │  ├─ Crie segmentacao (produto A vs B, visitantes vs compradores)
│  │  └─ Ajuste lances especificos para remarketing
│  └─ > 5.000 usuarios → Lista saudavel. Se nao esta escalando, problema e de configuração
│
├─ Tipos de lista:
│  ├─ So "visitantes do site"? → Crie listas por pagina/produto
│  ├─ Tem "abandonadores de carrinho"? → Priorize (maior intencao)
│  └─ Tem "compradores anteriores"? → Use para cross-sell/upsell
│
├─ Configuracao da campanha:
│  ├─ Remarketing com Search ou Display?
│  │  ├─ Search (RLSA): Ajuste de lance, nao campanha separada
│  │  │  ├─ "Target and bid": So mostra para lista
│  │  │  └─ "Bid only": Mostra para todos, ajusta lance para lista
│  │  └─ Audience Network: Campanha separada para remarketing
│  └─ Lances estao adequados?
│     ├─ Remarketing pode usar CPC menor (30-50% menos)
│     └─ Teste ECPC ou Manual CPC
│
└─ Conclusao:
   ├─ Se lista < 1.000: Bing tem audiencia pequena para remarketing → aceite
   ├─ Se lista > 1.000: Otimize configuracao (segmentacao, lance, membership)
   └─ Alternativa: Use Audience Network como substituto de remarketing (CPC baixo, amplo alcance)
```

---

## Parametros para o LLM

### Temperatura e Confianca

| Parametro | Valor | Quando |
|---|---|---|
| **Temperatura** | 0.1 - 0.3 | Recomendado. Baixa temperatura para analise precisa |
| **Top-p** | 0.9 | Default |
| **Max tokens** | 4096+ | Para analises completas com arvores de decisao |

### Thresholds por Setor (Bing-specific)

| Setor | CPC (R$) | CPC (USD) | CVR | CTR | CPA aceitavel |
|---|---|---|---|---|---|
| **E-commerce geral** | 0.80 - 3.50 | 0.30 - 1.50 | 1.5-4.5% | 2.0-4.0% | 10-30% do ticket medio |
| **Moda** | 0.50 - 2.00 | 0.20 - 0.80 | 1.0-3.0% | 2.5-5.0% | R$ 15-60 |
| **Saude / Clinicas** | 3.00 - 12.00 | 1.50 - 6.00 | 3.0-8.0% | 1.5-3.0% | R$ 50-200 |
| **Financas (credito)** | 5.00 - 20.00 | 2.00 - 10.00 | 2.0-6.0% | 1.0-2.5% | R$ 80-400 |
| **Seguros** | 8.00 - 25.00 | 3.00 - 15.00 | 1.5-5.0% | 1.0-2.5% | R$ 150-600 |
| **Educacao / Cursos** | 1.50 - 6.00 | 0.80 - 3.00 | 2.0-6.0% | 2.0-4.5% | R$ 30-150 |
| **Imobiliario** | 3.00 - 15.00 | 1.50 - 8.00 | 1.0-3.0% | 1.5-3.0% | R$ 100-500 |
| **SaaS** | 5.00 - 25.00 | 2.00 - 12.00 | 1.0-4.0% | 1.0-2.5% | 50-200% do MRR |
| **Automotivo** | 2.00 - 10.00 | 1.00 - 5.00 | 1.0-3.0% | 1.5-3.5% | R$ 50-300 |
| **Viagens** | 1.50 - 6.00 | 0.60 - 2.50 | 1.0-3.5% | 2.0-4.0% | R$ 30-150 |
| **B2B / Corporativo** | 5.00 - 30.00 | 2.00 - 15.00 | 1.0-4.0% | 1.0-2.5% | R$ 100-800 |
| **Servicos locais** | 2.00 - 10.00 | 1.00 - 5.00 | 3.0-8.0% | 2.0-4.0% | R$ 30-150 |
| **Audience Network** | 0.30 - 2.00 | 0.05 - 0.30 | 0.2-1.0% | 0.05-0.30% | CPA 2-5x maior que Search |
| **Search Partners** | 0.50 - 3.00 | 0.15 - 1.00 | 0.5-3.0% | 3.0-8.0% | CPA 1.5-3x Search puro |

### Pesos de Metricas por Contexto

| Contexto | Metrica #1 | Metrica #2 | Metrica #3 |
|---|---|---|---|
| Operacao diaria (health check) | CPA | Gasto | Conversoes |
| Escalabilidade | Volume de conversoes | Impression Share | CPC |
| Eficiencia | ROAS | CPA | CVR |
| Diagnostico de problema | Qual metrica esta amarela/vermelha | QS | Breakdown |
| Comparacao com Google | CPA relativo | CVR relativa | Volume relativo |
| Audience Network | CPC | CVR (click-through) | CTR |
| Remarketing | Tamanho da lista | CVR | CPA |
| Shopping | CPC | Impression Share | ROAS |
| Conta nova | Volume de dados | QS inicial | CPC |
| Migracao do Google | CPA vs Google | CTR | Search Partners |

### Regras de Precedencia

1. **Sempre verifique UET tag primeiro** se nao houver dados de conversao
2. **Nunca analise Search Partners junto com Search puro** — sempre separe
3. **Periodo minimo de analise: 7 dias** — Bing e mais volátil que Google
4. **30+ conversoes para decisao de CPA** — menos que isso e ruido
5. **Comparacao com Google: mesmo periodo, mesmas keywords** — senao a comparacao e invalida
6. **Nao tome decisoes baseado em dados de ontem** — Bing tem delay de 4-24h
7. **Verifique dispositivo separadamente** — Bing e desktop-first
8. **Contas novas requerem 2-4 semanas de maturacao** — nao otimize agressivamente no inicio
9. **Se algo parece estranho, verifique os dados brutos** — erros de tracking sao a causa #1 de anomalia
10. **Aceite que Bing e complementar** — nao force Bing a ser Google

---

## Glossario Avancado Bing Ads

### UET (Universal Event Tracking)

**O que e:**
Tag de tracking universal da Microsoft para campanhas de Bing Ads. Similar ao Google Tag / Google Ads Conversion Tracking.

**Como funciona:**
1. Instale o codigo UET (gerado no Bing Ads) no cabecalho do site
2. Crie goals de conversao no Bing Ads (URL, event, ou duration)
3. Para eventos personalizados, adicione codigo JavaScript nos botoes/formularios
4. UET envia dados para o Bing Ads via pixel

**Diferenca do Google Tag:**
- Google Tag: unico (gtag.js) para Google Ads + GA4 + Google Optimize + mais
- UET: separado (window.uetq). NAO se integra com Google Tools.
- UET pode coexistir com Google Tag, mas requer configuracao cuidadosa para nao duplicar dados

**Instalacao basica:**
```html
<script>
(function(w,d,t,r,u){var f,n,i;w[u]=w[u]||[],f=function(){
var o={ti:"SEU_ID_UET_AQUI"};o.q=w[u],w[u]=new UET(o),w[u].push("pageLoad")},
n=d.createElement(t),n.src=r,n.async=1,n.onload=n.onreadystatechange=function(){
var s=this.readyState;s&&s!=="loaded"&&s!=="complete"||(f())},
i=d.getElementsByTagName(t)[0],i.parentNode.insertBefore(n,i)})
(window,document,"script","//bat.bing.com/bat.js","uetq");
</script>
```

**Eventos comuns:**
- `pageLoad` — pagina carregada (automatico)
- `click` — clique em elemento
- `form_submit` — envio de formulario
- `purchase` — compra finalizada (passar valor e moeda)

**Verificacao de saude:**
1. Instale a extensao "Microsoft UET Tag Helper" no Chrome
2. Abra o site e veja se a tag dispara
3. Verifique no painel Bing Ads > UET > Status
4. Teste goals manualmente e veja se aparecem no relatorio em tempo real

### Bing Shopping Campaigns vs Google Shopping

**Diferencas estruturais:**
- Microsoft Merchant Center aceita feed nos mesmos formatos (XML, CSV, API)
- Menos atributos obrigatorios que Google
- Promocoes no Shopping sao mais limitadas
- Bing Shopping NAO tem "Shopping Actions" ou "Buy on Microsoft"
- Bing tem "Bing Shopping Campaigns" — similar ao Google Shopping mas com menos opcoes de segmentacao

**Otimizacao de feed para Bing:**
- Titulos: Bing prefere titulos mais descritivos (marca + modelo + tipo)
- Descricoes: inclua palavras-chave (Bing usa descricao para matching)
- Imagens: alta resolucao, fundo branco (similar ao Google)
- Preco: atualize com frequencia (Bing e sensivel a discrepancia)
- GTIN/MPN: importante para matching

**Quando usar:**
- Produtos com margem alta (CPC menor que Google compensa menor volume)
- Produtos de nicho (menos concorrencia no Shopping Bing)
- Para complementar Google Shopping (capturar o que Google perde)

### Microsoft Audience Network (Nao e Display, Nao e Search)

**O que e:**
Rede de anuncios nativos da Microsoft que aparece em:
- MSN
- Microsoft Start
- Outlook.com (webmail)
- Edge (pagina inicial e new tab)
- Microsoft 365 (aplicativos)
- Xbox
- Parceiros selecionados

**Por que e hibrido:**
- Nao e search (nao ha intencao de busca)
- Nao e display tradicional (nao ha posicoes programaticas abertas)
- E mais proximo de "discovery ads" (Google Discovery)
- Usa targeting demografico + comportamental + profissional (LinkedIn)
- Formatos: nativo (imagem + texto), banner, carrossel

**Segmentacao disponivel:**
- Demografica (idade, genero, renda)
- Geografica (pais, estado, cidade, CEP)
- Comportamental (in-market, interests)
- Profissional (LinkedIn: cargo, empresa, setor, formacao)
- Remarketing (visitantes do site)
- Custom audiences (lista de emails)

**Melhores praticas:**
- Crie copy com tom editorial (nativo = parece conteudo, nao anuncio)
- Imagens de alta qualidade (evite fotos de stock genéricas)
- Teste headlines curtas (3-5 palavras) vs longas (6-10 palavras)
- Segmentacao profissional funciona melhor para B2B
- Remarketing na Audience Network e eficiente (CPC muito baixo)

### LinkedIn Profile Targeting dentro do Bing

**O que e:**
Recurso exclusivo do Bing Ads que permite segmentar anuncios de search com base em dados do perfil LinkedIn dos usuarios.

**Disponibilidade:**
- Bing Ads + LinkedIn Account vinculadas
- Apenas em campanhas de Search (nao em Audience Network)
- Premium de 20-40% no CPC

**Opcoes de segmentacao:**
- Cargo (job title)
- Empresa (company)
- Setor (industry)
- Formacao (education)
- Habilidades (skills — quando disponivel)

**Uso pratico:**
- Positivo: "Mostrar anuncio apenas para Diretores de Marketing"
- Negativo: "NAO mostrar para estudantes ou estagiarios"
- Combinado: "Diretores de Marketing no setor de Saude"

**Performance:**
- CPC: 20-40% maior
- CVR: 30-60% maior (geralmente)
- Volume: 50-80% menor
- CPA: Varia — pode ser menor (CVR compensa CPC) ou maior (volume baixo demais)

### Search Partners: o que sao, como identificar, quando desligar

**O que sao:**
Sites que usam o indice de busca da Microsoft para exibir resultados de busca e anuncios. Incluem:
- Yahoo Search (parceria Verizon/Oath)
- AOL Search
- Centenas de sites menores que integram o search da Microsoft

**Como identificar performance:**
No painel Bing Ads, va em: Relatorios > Predefinidos > Performance por Rede e Dispositivo
Isoladamente, Bing Ads mostra "Bing, Yahoo, AOL" vs "Search Partners" vs "Audience Network"

**Quando desligar:**
- CPA em Partners > 2.5x o CPA do Search puro por 14+ dias
- CVR Partners < 50% da CVR do Search puro
- Gasto Partners > 30% do total com < 10% das conversoes

**Como desligar:**
Configuracoes da campanha > Redes > Desmarcar "Incluir parceiros de pesquisa do Bing"

### Position Value no Bing

**O que e:**
Metrica do Bing Ads que mostra o valor relativo de estar em diferentes posicoes no leilao. Bing reporta:
- "Top" — posicoes 1-4 (acima dos resultados organicos)
- "Other" — posicoes 5+ (lado direito ou abaixo dos organicos)

**Uso pratico:**
- Compare CPC Top vs Other para entender o premium de estar no topo
- Se CVR e similar entre Top e Other, vale economizar CPC ficando em Other
- Se CVR cai muito em Other, o premium do Top se justifica

### Dynamic Search Ads (DSA) no Bing

**O que e:** Anuncios de busca dinamica que usam o conteudo do site para gerar titulos e landing pages automaticamente.

**Disponibilidade:**
- Sim, Bing tem DSA
- Mas e MENOS avancado que Google DSA
- Menos controle sobre exclusoes de pagina
- Menos opcoes de targeting

**Quando usar DSA no Bing:**
- Sites grandes (+1000 paginas)
- Quando Google DSA funciona bem e Bing tem pouco trafego
- Para capturar cauda longa que voce nao mapeou manualmente

**Quando evitar:**
- Sites pequenos (< 50 paginas)
- Quando vocé tem controle total sobre keywords (prefira search manual)

### Auto-bidding Strategies no Bing

**Enhanced CPC (ECPC):**
- Ajusta lances manual +/-50% quando a conversao e mais provavel
- Funciona com qualquer campanha
- Bing e mais conservador que Google (ajusta menos)

**Maximize Clicks:**
- Tenta gastar o orcamento diario com o maximo de cliques
- Funciona melhor com Search partners ativos
- Pode gastar em clicks de baixa qualidade

**Maximize Conversions:**
- Tenta maximizar o numero de conversoes dentro do orcamento
- Requer historico de conversao (30+ nos ultimos 30 dias)
- Bing as vezes NAO gasta todo o orcamento (bug)

**Target CPA:**
- Tenta atingir um CPA desejado
- Requer 30+ conversoes nos ultimos 30 dias
- Menos preciso que Google Target CPA
- Precisa de 2-3 semanas de learning

**Target ROAS:**
- Tenta atingir um ROAS desejado
- Requer dados de receita (valor da conversao)
- Menos estavel que Google Target ROAS
- Ideal para e-commerce

### Remarketing Lists no Bing

**Como criar:**
1. UET tag instalada no site
2. Bing Ads > Audiencias > Remarketing
3. Defina regras (pagina visitada, URL contem, evento, duracao)
4. Aguardar acumular minimo de 300 usuarios

**Tipos de lista:**
- **Visitantes do site** (geral, por pagina, por secao)
- **Visitantes de produto** (pagina de produto especifica)
- **Abandonadores de carrinho** (chegou ao carrinho mas nao finalizou)
- **Compradores anteriores** (finalizou compra)
- **Visitantes de lead form** (iniciou mas nao completou)

**Tamanho minimo:** 300 usuarios (vs 100 no Google)

**Duracao maxima:** 180 dias (vs 540 dias no Google)

**RLSA (Remarketing Lists for Search Ads):**
- Ajuste de lances para usuarios que estao na lista
- "Target and bid" (so mostra para lista) ou "Bid only" (mostra para todos, ajusta lance)
- Recomendado: "Bid only" para nao perder trafego novo

**Limitacao critica:** Bing NAO tem "Similar Audiences" (audiencias similares) como o Google.

### Import from Google: o que funciona e o que quebra

**Funciona:**
- Keywords (com match types)
- Copy do anuncio (converte RSA em ETA)
- Lances (CPC maximo, porcentagens de ajuste)
- Extensoes (sitelinks, callouts, snippets — quando suportadas)
- Segmentacao geografica
- Segmentacao por dispositivo
- Negativos

**Quebra ou requer ajuste:**
- Smart Bidding (converte para ECPC)
- RSA (converte para ETA — perde variacao)
- Performance Max (ignorado — nao existe no Bing)
- Discovery campaigns (ignorado)
- Call-only ads (ignorado)
- YouTube targeting (ignorado)
- Gmail ads (ignorado)
- Extensoes de preco (nao suportado)
- Extensoes de promocao (parcial)
- Attribution models (converte para ultimo clique)

**Melhor abordagem:**
1. Importe como base
2. Crie copy novo especifico para Bing
3. Ajuste lances (reduza 30-50%)
4. Verifique match types
5. Crie extensoes manualmente
6. Monitore 14 dias antes de otimizar
7. NUNCA confie na importacao cegamente

### Microsoft Clarity integracao com Bing Ads

**O que e:** Microsoft Clarity e uma ferramenta gratuita de analytics que grava sessoes de usuario (replay), gera heatmaps e identifica rage clicks.

**Integracao com Bing Ads:**
- Instale o codigo Clarity junto com UET (ou separado)
- Clarity identifica automaticamente usuarios que vieram de Bing Ads (se UET estiver presente)
- Permite ver replays de sessoes de usuarios que clicaram em anuncios Bing
- Identifica problemas de UX que estao matando conversao

**Diferencial:** Clarity e GRATUITO (sem limite de dados) e se integra nativamente com Bing Ads — o que torna a analise de landing page para Bing muito mais barata que Google (Hotjar, etc. sao pagas).

---

## Casos Praticos

### Caso 1: E-commerce migrou campanha do Google para Bing e ROAS caiu 50%

**Contexto:**
- Loja de eletronicos (ticket medio: R$ 350)
- Google: ROAS 5:1, CPA R$ 70, 200 conversoes/mes
- Importou campanha diretamente do Google para Bing
- Resultado apos 14 dias: ROAS 2.5:1, CPA R$ 140, 15 conversoes

**Analise:**
1. UET tag: Funcionando (verificado no Tag Helper)
2. Search Partners: Consumindo 40% do gasto, gerando 10% das conversoes
3. Lances: Mantidos os mesmos do Google (CPC medio R$ 4,50 no Google virou R$ 2,80 no Bing — mas o lance maximo era R$ 8,00)
4. Copy: Importado do Google (headline generica, sem oferta especifica)
5. Match types: Exact match no Bing estava capturando variacoes irrelevantes

**Recomendacoes:**
1. Desligar Search Partners
2. Reduzir lances em 35% (de R$ 8,00 para R$ 5,00)
3. Criar copy especifico para Bing com oferta de frete gratis
4. Adicionar 200 negativos para limpar variacoes de exact match
5. Manter apenas Phrase Match como match type principal
6. Ajustar orcamento diario para gastar em horario comercial (desktop)

**Resultado apos 14 dias:**
- ROAS: 4.2:1 (recuperado)
- CPA: R$ 85
- Volume: 28 conversoes

**Licao:** NUNCA confie na importacao cega — Bing requer adaptacao.

### Caso 2: Clinica: Bing entrega CPA 40% menor que Google mas volume irrisorio

**Contexto:**
- Clinica odontologica (implantes)
- Google: CPA R$ 120, 50 leads/mes, orcamento R$ 6.000/mes
- Bing: CPA R$ 72, 8 leads/mes, orcamento R$ 600/mes
- Pergunta: Bing vale a pena? Como escalar?

**Analise:**
1. Bing esta com CPA excelente (40% mais barato que Google)
2. Mas volume e irrisorio (8 leads vs 50)
3. Impression Share: 85% (perde so 15% — nao ha muito mais trafego para capturar)
4. Keywords: "implante dentario" tem 10x mais volume no Google que no Bing
5. Bing esta capturando a audiencia de maior renda (implante dentario e caro)
6. Search Partners: Desligados (boa decisao)

**Recomendacao:**
1. ACEITE que Bing e complementar — com CPA 40% menor, cada lead do Bing vale MAIS que do Google
2. Escale: expanda keywords long tail ("implante dentario preco", "implante all-on-4", "protese sobre implante")
3. Teste Audience Network para capturar audiencia fria a baixo custo
4. Crie remarketing para nutrir leads que vieram do Bing
5. Aumente orcamento Bing para R$ 1.500-2.000 para testar se consegue mais volume
6. Nao mate o Google — Bing complementa com leads de maior qualidade

**Calculo de valor:**
- Google: 50 leads x R$ 120 = R$ 6.000
- Bing: 8 leads x R$ 72 = R$ 576
- Total: 58 leads por R$ 6.576
- Custo medio por lead: R$ 113 (melhor que so Google)
- Bing esta REDUZINDO o CPA medio da conta

**Licao:** CPA mais baixo com volume menor NAO e problema — e complementar.

### Caso 3: Seguradora: Audience Network com CTR alto mas lead nao qualifica

**Contexto:**
- Seguradora (seguro auto)
- Audience Network: CTR 0.45% (excelente), CPC R$ 0,80 (baixo), CVR 0.3% (baixa)
- Search: CTR 2.5%, CPC R$ 5,50, CVR 4.0%
- Leads da Audience: 80% nao qualificam (nunca tem carteira de motorista, interesse baixo)

**Analise:**
1. CTR alto na Audience Network pode indicar clicks acidentais ou audiencia pouco qualificada
2. Audience esta atraindo pessoas curiosas com precos baixos, nao compradores reais
3. CPC baixissimo (R$ 0,80 vs R$ 5,50 no Search) nao compensa a qualidade do lead

**Diagnostico:**
- Audience Network esta generica demais — sem segmentacao profissional
- "Seguro auto" no formato nativo atrai curiosos, nao compradores
- A oferta (preco baixo) atrai o publico errado
- Lead qualificado para seguro auto: 25-55 anos, CNH ativa, carro seminovo ou novo, busca cobertura especifica

**Recomendacoes:**
1. Segmentar Audience por LinkedIn: excluir estudantes, focar em "25-55 anos, empregado, setor especifico"
2. Mudar copy: em vez de "Seguro a partir de R$ 99/mes", focar em cobertura ("Protecao completa para seu carro")
3. Testar remarketing em vez de prospeccao fria na Audience
4. Reduzir investimento em Audience de 30% para 10% do orcamento
5. Criar lead form mais qualificador na pagina (mais campos = menos leads mas mais qualificados)

**Resultado esperado:**
- Volume de leads cai 40%
- Qualificacao sobe para 60%+
- CPA de lead qualificado MELHORA

**Licao:** CTR e CPC baixos nao significam sucesso — QUALIDADE do lead importa.

### Caso 4: Loja de nicho: Bing e 60% do ROAS total mesmo com 10% do volume

**Contexto:**
- Loja de produtos para apicultura (nicho)
- Google: ROAS 3.5:1, R$ 15.000/mes gastos, R$ 52.500 receita
- Bing: ROAS 9.0:1, R$ 1.500/mes gastos, R$ 13.500 receita
- Pergunta: Como escalar Bing para capturar mais receita?

**Analise:**
1. ROAS Bing e 2.5x melhor que Google — excepcional
2. Mas gasta apenas 10% do que gasta no Google
3. Produto de nicho + publico profissional (apicultores) + desktop-heavy = PERFEITO para Bing
4. Apicultores sao um publico mais velho (35-60 anos) que usa mais desktop
5. CPC Bing: R$ 1,20 vs Google: R$ 3,80
6. Impression Share no Bing: 92% (quase todo o trafego capturado)

**Oportunidade:**
Bing ja capturou 92% do trafego disponivel — escalar orcamento NAO vai gerar muito mais volume. Precisa de novas keywords.

**Recomendacoes:**
1. EXPANDIR keywords: "colmeia langstroth", "meliponario", "equipamento apicultura", "fumegador", "macarao apicultura"
2. Usar ferramenta de palavras-chave do Bing para encontrar termos que Google nao mostra
3. Testar Audience Network com targeting de "jardineiros", "agricultura familiar", "sitiantes"
4. Criar campanha separada para DSA (Dynamic Search Ads) capturar cauda longa
5. Implementar remarketing para quem visitou mas nao comprou
6. Se IS ja esta em 92%, o teto e baixo — considere que Bing ja esta no maximo para o nicho

**Cenario realistico:**
- Potencial de crescimento: 30-50% (de R$ 1.500 para R$ 2.000-2.250/mes)
- Nao espere Bing chegar ao volume do Google (nicho pequeno + audiencia Bing pequena)
- Mas cada R$ 1 investido no Bing retorna R$ 9,00 — e um investimento EXCELENTE

**Licao:** As vezes o melhor investimento nao e escalar, e manter o que funciona e reinvestir o lucro em outros canais.

---

## Cadencias e Rotinas

### Timeline de Operacao

| Frequencia | O que fazer |
|---|---|
| **24h** | Verificar anomalias (pico de gasto, zero conversoes, CPC disparou). Nao tome decisoes — apenas identifique. |
| **Semanal** | Review completa de Camada 1. Ajustes finos de lance, negativos, copy. Relatorio para stakeholder. |
| **Quinzenal** | Review de Camada 2. Analise de Search Partners, Quality Score, match types. Decisoes estruturais. |
| **Mensal** | Review de Camada 3. Atribuicao, UET health, experimentos. Planejamento do mes seguinte. |
| **Trimestral** | Revisao de estrutura de conta, orcamento, metas. Comparacao Bing vs Google estrategico. |

### Diferencas de Cadencia vs Google

| Aspecto | Bing | Google |
|---|---|---|
| **Learning period** | 48-72h apos mudanca | 24-48h |
| **Estabilidade de dados** | 7 dias para confiar | 3-5 dias |
| **Delay de conversao** | 4-24h | 1-6h |
| **Frequencia de otimizacao** | Semanal (nao diario) | A cada 2-3 dias |
| **Tempo para maturacao de conta nova** | 2-4 semanas | 1-2 semanas |
| **Tempo de experimento** | 2-4 semanas | 1-2 semanas |
| **Frequencia de report** | Semanal | Diario/semanal |

**Por que Bing precisa de mais tempo:**
- Menos dados = mais ruido estatistico
- Auto-bidding menos preciso = mais tempo para convergir
- UET pode ter delay maior que Google Tag
- Publico menor = levao menos frequente = mais tempo para acumular dados

### Estrutura de Report

**Template de report semanal Bing Ads:**

```
── REPORT BING ADS — SEMANA [X] ──
Periodo: [data] a [data]
Conta: [nome]
Orcamento: [R$ X.XXX] | Gasto: [R$ X.XXX] | Pace: [X%]

── RESUMO EXECUTIVO ──
[2-3 frases: como foi a semana, destaques, anomalias]

── METRICAS PRINCIPAIS ──
Cliques: [X] (▲/▼ X% vs semana anterior)
Impressoes: [X] (▲/▼ X%)
CPC: R$ [X.XX]
CTR: [X.X%]
Gasto: R$ [X.XXX]
Conversoes: [X]
CVR: [X.X%]
CPA: R$ [X.XX]
ROAS: [X.X:1]
Impression Share: [X%]

── POR REDE ──
Search (Bing + Yahoo): CPC R$ [X.XX], CPA R$ [X.XX], CVR [X.X%]
Search Partners: CPC R$ [X.XX], CPA R$ [X.XX], CVR [X.X%] (se ativo)
Audience Network: CPC R$ [X.XX], CPA R$ [X.XX], CVR [X.X%] (se ativo)

── POR DISPOSITIVO ──
Desktop: [X%] gasto, CPA R$ [X.XX], CVR [X.X%]
Mobile: [X%] gasto, CPA R$ [X.XX], CVR [X.X%]

── QUALITY SCORE ──
Media da conta: [X]/10
Keywords com QS baixo (< 5): [X] keywords

── TOP PERFORMERS (TOP 5 KEYWORDS POR CONVERSAO) ──
1. [keyword] — CPA R$ [X.XX], [X] conv
2. [keyword] — CPA R$ [X.XX], [X] conv
3. [keyword] — CPA R$ [X.XX], [X] conv
4. [keyword] — CPA R$ [X.XX], [X] conv
5. [keyword] — CPA R$ [X.XX], [X] conv

── NECESSITA ATENCAO ──
- [Item 1: keyword/campanha com CPA subindo]
- [Item 2: search partners consumindo sem conversao]
- [Item 3: etc.]

── RECOMENDACOES ──
1. [Acao prioritária]
2. [Acao secundaria]
3. [Acao de longo prazo]

── COMPARATIVO BING vs GOOGLE ──
[Se aplicavel e dados disponiveis]
Google CPA: R$ [X.XX] | Bing CPA: R$ [X.XX]
Google ROAS: [X.X:1] | Bing ROAS: [X.X:1]
Google CVR: [X.X%] | Bing CVR: [X.X%]
Volume relativo: Bing = [X%] do Google
```

---

## Regras de Ouro (Resumo Executivo)

**1. Bing NAO e Google mais barato — e DIFERENTE.** A audiencia, o comportamento de busca e a intencao sao distintos. Nao replique cegamente a estrategia do Google no Bing.

**2. Sempre verifique Search Partners separadamente.** Eles podem ser a melhor ou pior coisa da sua conta. NUNCA analise Bing sem o breakdown Search vs Partners.

**3. Periodo minimo de analise: 7 dias.** Bing e mais volátil, tem mais delay e menos dados. Decisoes prematuras custam caro.

**4. UET tag e a causa #1 de problemas de conversao.** Verifique a tag antes de qualquer diagnostico avancado. 90% das vezes que "Bing nao converte", a tag esta mal instalada.

**5. Copia do anuncio importada do Google NAO funciona.** Crie copy especifica para Bing — tom mais profissional, headlines diferentes, ofertas adaptadas.

**6. Lances importados do Google estao ERRADOS.** Reduza em 30-50% ao importar. O CPC do Bing e naturalmente menor.

**7. Desktop e prioridade no Bing.** 60-70% do trafego Bing e desktop. Nao otimize para mobile na mesma proporcao que no Google.

**8. Bing Audience Network e topo de funil.** Nao avalie Audience Ads pelo mesmo CPA do Search. Use para awareness e remarketing, nao para conversao direta.

**9. LinkedIn targeting e diferencial exclusivo.** Use para segmentar publico profissional B2B. Mas cuidado — a segmentacao reduz volume drasticamente.

**10. Bing complementa, nao substitui.** Mesmo no melhor cenario, Bing entrega 10-30% do volume do Google para as mesmas keywords. Aceite isso e use Bing como alavanca incremental de performance. Contas que tentam "substituir" Google por Bing sempre se frustram.

---

## Checklist Rapido de Diagnostico

Quando algo nao vai bem no Bing Ads, siga esta ordem:

```
[ ] 1. UET tag esta funcionando? (testar com Tag Helper)
[ ] 2. Search Partners vs Search puro? (sempre verificar)
[ ] 3. Dispositivo breakdown? (desktop vs mobile)
[ ] 4. Quality Score das principais keywords? (esta baixo?)
[ ] 5. Impression Share: perde por budget ou rank?
[ ] 6. Match types adequados para Bing? (exact e diferente)
[ ] 7. Copy e especifico para Bing? (nao copiado do Google)
[ ] 8. Lances adequados? (nao copiados do Google)
[ ] 9. Periodo de dados suficiente? (minimo 7 dias)
[ ] 10. Campanha e nova? (precisa de 2-4 semanas de maturacao)
[ ] 11. Concorrentes novos no leilao?
[ ] 12. Houve mudanca no site/landing page?
```

Se > 3 itens com problema, a causa raiz provavelmente esta nos itens 1-4.

---

## Notas Finais

Bing Ads nao e para todo mundo. Para alguns setores (B2B, alto tiquete, nichos, publico 35+), Bing pode ser o canal com melhor ROAS da conta. Para outros (B2C massivo, baixo tiquete, publico jovem), Bing pode ser irrelevante.

O gestor de trafego que SABE usar Bing Ads tem uma vantagem competitiva real — menos concorrencia, CPCs mais baixos, oportunidades que 90% dos anunciantes ignoram.

Esta skill foi construida para que um LLM possa interpretar metricas de Bing Ads com a profundidade que a plataforma merece — nao como um "Google inferior", mas como um canal unico com caracteristicas proprias.

---

## Tabela de Referencia Rapida de Metricas Bing Ads

Para consulta rapida durante analise, esta tabela resume todas as metricas por camada, o que cada uma sinaliza e a acao tipica.

| Camada | Metrica | Sinaliza | Acao tipica |
|---|---|---|---|
| 1 | Cliques | Volume de trafego | Ajustar keywords ou lances se queda > 30% |
| 1 | Impressoes | Visibilidade / alcance | Verificar status da campanha se queda > 40% |
| 1 | CPC | Custo do trafego | Verificar concorrencia e QS se subiu > 20% |
| 1 | CTR | Relevancia do anuncio | Melhorar copy e extensoes se < 1.5% |
| 1 | Gasto | Consumo de orcamento | Ajustar orcamento ou lances se fora do pace |
| 1 | Conversoes | Resultado | Verificar UET se caiu a zero |
| 1 | CVR | Qualidade do trafego | Verificar landing page e intent se < 1.5% |
| 1 | CPA | Custo do resultado | Revisar keywords e lances se > target 20% |
| 1 | ROAS | Retorno do investimento | Revisar campanha inteira se < 2:1 |
| 1 | Impression Share | Cobertura do leilao | Aumentar orcamento ou melhorar QS |
| 1 | Posicao Media | Visibilidade no leilao | Ajustar lances se < 4.0 |
| 2 | Quality Score | Saude do anuncio/keyword | Melhorar relevancia se < 5/10 |
| 2 | Search Partners Perf | Qualidade dos parceiros | Desligar se CPA > 3x search puro |
| 2 | Device CVR | Performance por dispositivo | Ajustar lances por dispositivo |
| 2 | Tempo ate Conversao | Ciclo de compra | Ajustar janela de atribuicao |
| 2 | Top vs Other CPC | Premium de posicao | Testar posicoes mais baixas |
| 2 | Match Type Perf | Performance por tipo | Ajustar mix de match types |
| 2 | Audience Network Perf | Performance da rede nativa | Ajustar targeting ou desligar |
| 2 | LinkedIn Targeting Perf | Performance B2B | Ampliar ou restringir segmentacao |
| 3 | Modelo de Atribuicao | Justica da atribuicao | Considerar modelo mais adequado |
| 3 | UET Health | Precisao do tracking | Corrigir tag ou eventos |
| 3 | View-through Conv | Impacto de visualizacao | Ignorar para decisoes de CPA |
| 3 | Cross-device Conv | Jornada multicanal | Aceitar limitacao do Bing |
| 3 | Assisted Conversions | Contribuicao indireta | Considerar em modelo de atribuicao |
| 3 | Auto-bidding Analysis | Eficacia do lance automatico | Revisar estrategia se instavel |
| 3 | Experimentos | Testes controlados | Aumentar duracao se inconclusivo |
| 3 | Goal Tracking | Configuracao de metas | Corrigir metas mal configuradas |
| 3 | Remarketing List Perf | Performance de audiencias | Aumentar tamanho das listas |

---

## Matriz de Decisao Rapida por Problema

Use esta matriz quando o usuario descrever um sintoma sem dar metricas detalhadas. Cada linha mapeia um problema comum a causa provavel e a acao recomendada.

| Sintoma do usuario | Causa #1 mais provavel | Causa #2 | Acao imediata |
|---|---|---|---|
| "Bing nao gasta o orcamento" | IS lost to rank (QS baixo) | Keywords com pouco volume | Verificar QS e lances. Ampliar match types. |
| "Bing gastou muito em um dia" | Search Partners entregaram volume | Bing ultrapassou orcamento diario | Reduzir orcamento diario ou desligar Partners |
| "Nao tem conversao no Bing" | UET tag quebrada | Janela de conversao muito curta | Testar UET Tag Helper. Aumentar janela para 30 dias. |
| "Conversao caiu do nada" | UET tag removida ou modificada | Mudanca no site/funil | Verificar UET. Verificar landing page. |
| "CPC subiu muito" | Concorrente novo no leilao | QS caiu por alteracao de landing page | Verificar QS. Verificar concorrencia. |
| "Bing esta caro" | Lances importados do Google | Search Partners ativos | Reduzir lances 30%. Desligar Partners. |
| "CTR muito baixo" | Copy generico (importado) | Extensoes faltando | Criar copy especifico Bing. Adicionar extensoes. |
| "Audience Network nao converte" | Expectativa errada (e topo de funil) | Targeting muito amplo | Reavaliar como canal de awareness. Segmentar melhor. |
| "Remarketing nao funciona" | Lista muito pequena (< 300) | Membership muito curto | Combinar listas. Estender para 180 dias. |
| "Diferenca entre Bing e GA4" | Modelos de atribuicao diferentes | UET vs gtag discrepancia | Aceitar 15-25% de variacao. Usar mesma janela. |
| "Campanha importada do Google" | Lances e copy incompativeis | Match types diferentes | Reduzir lances 40%. Criar copy novo. |
| "Bing nao entrega no mobile" | Bing e desktop-first (60-70%) | Lances mobile muito baixos | Aceitar. Aumentar lance mobile se essencial. |
| "LinkedIn targeting nao entrega" | Segmentacao muito restrita | Conta nao vinculada ao LinkedIn | Ampliar segmentacao. Verificar vinculacao. |
| "Bing Shopping nao vende" | Feed nao otimizado para Bing | CPB baixo mas volume baixo | Otimizar titulos e descricoes do feed. |

---

## Troubleshooting Avancado — Sintomas, Causas e Solucoes Detalhadas

### Problema: Zero conversoes na conta

**Passo a passo:**
1. Verificar UET Tag Helper — tag carrega na pagina?
2. Verificar goals configurados vs pagina de conversao real
3. Verificar se as paginas de conversao estao no ar
4. Verificar se nao ha CMP/consent tool bloqueando UET
5. Verificar se adblockers estao bloqueando bat.bing.com
6. Verificar delay (Bing pode levar 24h+ para mostrar conversoes)
7. Verificar janela de conversao (talvez muito curta para o ciclo de compra)
8. Verificar se a campanha tem cliques (sem cliques = sem conversao possivel)

**Ferramentas de diagnostico:**
- Microsoft UET Tag Helper (Chrome extension)
- Console do navegador: `window.uetq` deve mostrar dados
- Network tab: verificar se bat.bing.com e chamado
- Bing Ads > UET > Status da tag
- Bing Ads > Conversoes > Relatorio em tempo real

### Problema: Gasto muito acima ou abaixo do orcamento diario

**Gasto abaixo:**
1. Campanha pausada ou com status limitado? (verificar aprovacao)
2. Keywords tem volume no Bing? (usar Keyword Planner)
3. Lances estao muito baixos? (comparar com suggested bid)
4. Segmentacao muito restrita? (ampliar localizacao, idade, dispositivo)
5. Search Partners desligados? (ligar aumenta gasto 30-60%)
6. Orcamento diario muito alto para o leilao? (reduzir ou expandir keywords)

**Gasto acima:**
1. Bing ultrapassou orcamento diario (permitido ate 20% acima)
2. Search Partners entregaram mais que esperado
3. Concorrente saiu do leilao (voce capturou mais trafego)
4. Keyword com pico sazonal de busca
5. Ajuste de lances automatico (ECPC ou auto-bidding aumentou lances)

### Problema: Discrepancia entre Bing Ads e plataforma propria (CRM, checkout)

**Causas comuns e solucoes:**

| Discrepancia | Causa provavel | Solucao |
|---|---|---|
| Bing reporta +20% conversoes que o CRM | Duplicacao de UET (tag instalada 2x) | Remover tag duplicada |
| Bing reporta -30% que o checkout real | UET com delay ou perdendo eventos | Verificar UET + adicionar fallback de server-side |
| Bing mostra lead que CRM nao tem | View-through conversion contada | Ignorar view-through para comparacao |
| CRM mostra lead que Bing nao tem | Janela de conversao diferente | Alinhar janela de 30 dias em ambos |
| Discrepancia > 40% | Problema grave de tracking | Reinstalar UET do zero |
| Discrepancia varia por dispositivo | UET pode ser bloqueado em iOS/Safari | Verificar compatibilidade UET |

### Problema: Bing Ads parou de performar depois de funcionar bem

**Causas tipicas:**
1. Mudanca no site (landing page fora do ar, alteracao de layout, formulario quebrado)
2. UET tag removida ou modificada (CMS update, troca de tema, migracao de servidor)
3. Concorrente novo entrou no leilao com lances agressivos
4. Mudanca sazonal (fim de temporada, feriado)
5. Alteracao de politica Microsoft (novas restricoes de segmentacao)
6. Problema de consentimento (CMP atualizada e bloqueando UET)
7. Landing page mais lenta (Core Web Vitals pioraram)
8. Conta teve chargebacks ou violacao de politica (conta limitada)

**Diagnostico:**
1. Verificar historico de 30 dias — quando exatamente a performance caiu?
2. Verificar changelog do site na mesma data
3. Verificar UET tag ainda esta na pagina
4. Verificar status da conta (ha alertas?)
5. Verificar Microsoft Clarity replays para ver comportamento do usuario
6. Verificar concorrencia (relatorio de leilao)

---

## Metricas Avancadas e Customizadas

### Segmentacao Horaria (Hour of Day)

Bing Ads permite analisar performance por hora do dia. Isso e especialmente util porque:
- Bing tem pico em horario comercial (9h-17h) — ao contrario do Google que tem pico noturno
- Usuarios Bing sao mais ativos durante o trabalho (desktop, horario comercial)
- Audience Network tem comportamento diferente de Search

**Como analisar:**
Relatorios > Hora do dia > Performance por hora

**Padrao tipico:**
- 8h-10h: Pico de clicks (inicio do dia de trabalho)
- 11h-14h: Queda (almoco)
- 15h-17h: Segundo pico
- 18h-22h: Baixo volume (Bing e desktop, nao mobile-noturno como Google)
- 22h-6h: Volume minimo

**Acao:** Ajuste lances por horario se o padrao do seu negocio for diferente. Seu produto pode vender mais a noite — mas Bing pode nao ser o canal ideal para isso.

### Segmentacao Geografica Avancada

Bing Ads permite segmentar por pais, estado, cidade, CEP, raio, e regiao metropolitana.

**Diferenca do Google:**
- Bing tem menos granularidade em alguns paises (Brasil: estados e capitais; sem CEP)
- Bing EUA: excelente granularidade (CEP, DMA, cidade)
- Bing UK/Canada/Australia: boa granularidade
- Bing Europa: granularidade varia por pais

**Quando usar:**
- Negocio local: segmente por raio de 20-50km
- E-commerce nacional: segmente por estado/regiao se frete variar
- B2B: segmente por regioes metropolitanas (maior concentracao empresarial)

### Audience Targeting Avançado

Bing Ads oferece varias opcoes de targeting que podem ser combinadas:

**Tipos de audiencia no Bing:**
- **Remarketing:** Visitantes do site (comportamental)
- **Custom Audiences:** Lista de emails importada (hasheada)
- **In-Market Audiences:** Usuarios com intencao de compra em categorias especificas
- **Demographic:** Idade, genero, renda
- **LinkedIn Profile:** Cargo, empresa, setor, formacao
- **Similar Audiences:** **NAO DISPONIVEL** no Bing (diferenca critica)

**Combinacao de audiencias:**
- AND (usuario deve estar em todas as listas) — reduce volume
- OR (usuario deve estar em qualquer lista) — aumenta volume
- NOT (excluir usuarios de uma lista) — para segmentacao negativa

**Estrategia recomendada:**
1. Remarketing para quem visitou mas nao converteu (maior CVR)
2. Custom Audiences para lista de emails de clientes (cross-sell)
3. In-Market para prospeccao (intencao de compra)
4. Demographic para refinar (ex: 25-54 anos, renda alta)
5. LinkedIn para B2B (cargo + setor)
6. Combinacoes: Remarketing AND In-Market (volume baixo mas CVR muito alta)

### Analise de Concorrencia (Auction Insights)

**Disponivel no Bing:** Sim — relatorio de Auction Insights similar ao Google.

**Metricas do Auction Insights no Bing:**
- Impression Share (seu vs concorrente)
- Average Position (quem esta em posicao melhor)
- Overlap Rate (% de vezes que seus anuncios apareceram junto com concorrente)
- Position Above Rate (% de vezes que concorrente ficou acima)
- Outranking Share (% de vezes que voce ficou acima do concorrente)

**Interpretacao:**
- Overlap Rate alto + Position Above Rate alto = concorrente esta ganhando de voce
- Outranking Share baixo = voce precisa melhorar lances ou QS
- Concorrente com IS muito maior = esta investindo mais que voce

**Acao:**
- Se concorrente tem IS 80%+ e voce 40%: ou aumenta orcamento/lances ou aceite que ele domina o leilao
- Se concorrente tem overlap baixo: estao em keywords diferentes — voce pode expandir para as keywords dele
- Se varios concorrentes com overlap alto: leilao competitivo, foque em QS para reduzir CPC

---

## Integracoes e Ferramentas do Ecossistema Bing Ads

### Microsoft Clarity (Gratuito)

**O que faz:**
- Replay de sessoes de usuarios
- Heatmaps de clique, scroll e movimento
- Rage clicks detection
- Dead clicks detection
- Integracao nativa com Bing Ads (identifica usuarios de campanhas pagas)

**Como usar com Bing Ads:**
1. Instale o codigo Clarity no site (pode ser o mesmo que UET ou separado)
2. No Clarity, filtre por "utm_source = bing" ou "utm_medium = cpc"
3. Veja replays de usuarios que vieram do Bing
4. Identifique problemas de UX que impedem conversao

**Diferencial:**
- Gratuito e sem limites de dados
- Integracao direta com Bing Ads (mais facil que Google + Hotjar)
- Ideal para diagnosticar por que o trafego Bing nao converte

### Microsoft Advertising Editor

**O que e:** Ferramenta desktop para edicao em massa de campanhas (similar ao Google Ads Editor).

**Disponibilidade:** Windows e Mac.

**Funcionalidades:**
- Edicao offline de campanhas
- Copiar/colar entre campanhas e contas
- Importacao de CSV (bulk sheets)
- Exportacao e backup de contas
- Validacao de erros antes de publicar

**Quando usar:**
- Alteracoes em massa (+100 keywords)
- Migracao de contas
- Backup de estrutura de campanha
- Criacao de campanhas complexas com muitos grupos de anuncios

### Microsoft Shopping Campaigns Setup

**Setup basico:**
1. Criar conta no Microsoft Merchant Center (merchantcenter.microsoft.com)
2. Configurar feed de produtos (XML, CSV, ou API)
3. Submeter feed para aprovacao
4. Criar campanha Shopping no Bing Ads
5. Vincular Merchant Center a conta de anuncios

**Otimizacao de feed para Bing:**
- Titulo: [Marca] [Modelo] [Tipo] — max 150 chars
- Descricao: Incluir palavras-chave relevantes para o publico Bing (35+ anos)
- Imagens: 1200x1200px minimo, fundo branco
- Preco: Atualizado diariamente (Bing e rigido com discrepancia de preco)
- Disponibilidade: In Stock / Out of Stock
- GTIN: Altamente recomendado (melhora matching)
- MPN: Alternativa ao GTIN

**Diferencas de configuracao vs Google:**
- Microsoft Merchant Center nao tem "feed rules" avancadas como Google
- Bing requer que o feed esteja 100% correto — menos tolerancia a erros
- Promocoes no Shopping Bing precisam ser configuradas manualmente
- Bing nao tem "Shopping optional attributes" — a maioria e obrigatoria

### Power BI + Bing Ads

**Integracao:**
Bing Ads fornece conectores nativos para Power BI, permitindo criar dashboards customizados.

**Metricas disponiveis via API:**
- Todas as metricas de campanha, grupo de anuncios, keyword, search query
- Performance por dispositivo, rede, horario, geografia
- Dados de UET (conversoes, receita)
- Auction insights
- Dados de Quality Score (historico)
- Dados de Search Partners

**Quando usar:**
- Reports executivos mensais
- Dashboards comparativos Google + Bing + Meta
- Analise de tendencias de longo prazo
- Automacao de reports semanais

---

## Framework de Otimizacao Continua para Bing Ads

### Ciclo de Otimizacao de 14 Dias

```
DIA 1-3: COLETA E DIAGNOSTICO
├─ Revisar metricas de Camada 1 e 2
├─ Identificar keywords com CPA acima da media
├─ Verificar Search Partners performance
└─ Verificar UET health

DIA 4-7: EXECUCAO DE AJUSTES
├─ Ajustar lances (keywords com bom ROAS: +10-15%; ruins: -20-30%)
├─ Adicionar palavras-chave negativas (baseado em search terms)
├─ Pausar keywords sem conversao nos ultimos 30 dias (com cliques)
├─ Criar/atualizar copy de anuncios (2-3 variacoes por grupo)
└─ Ajustar Search Partners se necessario

DIA 8-10: MONITORAMENTO POS-AJUSTE
├─ Nao fazer alteracoes — deixar learning period acontecer
├─ Verificar se ajustes nao causaram efeito colateral
└─ Registrar mudancas e resultados esperados

DIA 11-14: AVALIACAO E PLANEJAMENTO
├─ Comparar performance pre vs pos ajuste
├─ Decidir se ajustes foram bem-sucedidos
├─ Planejar proximo ciclo
└─ Atualizar documentacao da conta
```

### Priorizacao de Keywords no Bing

Use a matriz abaixo para priorizar keywords no Bing Ads:

```
                    ROAS ALTO          ROAS BAIXO
                    ──────────         ──────────
VOLUME ALTO        │ PROTEGER        │ OTIMIZAR
                   │ Aumentar lance   │ Reduzir lance ou pausar
                   │ Expandir match   │ Adicionar negativos
                   │ Manter QS        │ Melhorar QS
                   └──────────────────┴──────────────────

VOLUME BAIXO       │ EXPANDIR         │ ELIMINAR
                   │ Aumentar lance   │ Pausar keyword
                   │ Buscar similares │ Destinar orcamento
                   │ Phrase/Broad     │ para keywords melhores
                   └──────────────────┴──────────────────
```

**Ordem de prioridade:**
1. **PROTEGER** — keywords com ROAL alto e volume alto. Nao mexa no que funciona.
2. **EXPANDIR** — keywords com ROAS alto mas volume baixo. Precisa de mais trafego.
3. **OTIMIZAR** — keywords com volume alto mas ROAS baixo. Precisa de correcao.
4. **ELIMINAR** — keywords com ROAS baixo e volume baixo. So consomem orcamento.

### Regras de Automacao no Bing Ads

Bing Ads permite criar automation rules para acoes recorrentes:

**Rules uteis:**

| Regra | Condicao | Acao | Frequencia |
|---|---|---|---|
| Pausar keyword com CPA alto | CPA > target, > 30 dias, > 50 cliques | Pausar keyword | Semanal |
| Aumentar lance keyword boa | ROAS > target, > 10 conversoes, > 30 dias | Aumentar lance +15% | Quinzenal |
| Reduzir lance keyword fraca | CPA > 2x target, > 20 cliques, > 14 dias | Reduzir lance -25% | Semanal |
| Alertar de gasto anormal | Gasto > orcamento diario x 1.5 | Enviar email | Diario |
| Pausar campanha a noite | Hora entre 22h e 6h | Pausar/retomar | Diario |

**Limitacao:** Bing automation rules sao menos poderosas que Google — menos condicoes, menos acoes, menos frequencia.

---

## Analise Comparativa Bing Ads vs Outras Plataformas (para contexto do LLM)

### Bing vs Google Ads (recapitulacao com metricas reais)

| Metrica | Google Ads | Bing Ads | Diferenca |
|---|---|---|---|
| CPC medio (e-commerce, USD) | $0.66 | $0.35 | Bing 47% menor |
| CPC medio (servicos, USD) | $2.69 | $1.45 | Bing 46% menor |
| CPC medio (Brasil, R$) | R$ 2.50 | R$ 1.20 | Bing 52% menor |
| CTR media (Search) | 3.17% | 2.80% | Bing 12% menor |
| CVR media (e-commerce) | 2.80% | 2.10% | Bing 25% menor |
| CVR media (lead gen) | 4.50% | 3.80% | Bing 16% menor |
| ROAS medio (e-commerce) | 4.5:1 | 3.8:1 | Bing 16% menor |
| Impression Share medio | 85% | 60-80% | Bing mais variavel |
| Mobile % | 60% | 35% | Bing muito mais desktop |
| Idade media do usuario | 34 anos | 42 anos | Bing publico mais velho |
| Renda familiar media | $75k | $100k | Bing 33% maior renda |

### Bing vs Meta Ads

| Aspecto | Bing Ads | Meta Ads |
|---|---|---|
| **Formato principal** | Search (intencional) | Feed/Stories (passivo) |
| **Intencao do usuario** | Alta (buscou ativamente) | Baixa-Media (scrollando) |
| **CPC medio** | $0.35 - $1.45 | $0.50 - $2.00 |
| **CTR media** | 2.8% | 0.9% (feed) |
| **CVR** | 2.1% | 1.5% |
| **Tempo ate conversao** | 1-7 dias | 1-3 dias (mais impulsivo) |
| **Publico principal** | 35+ anos, desktop, profissional | 18-49 anos, mobile, geral |
| **Segmentacao** | Palavra-chave (intencao) | Demografica + Comportamental |
| **Melhor para** | Fundo de funil | Topo e meio de funil |
| **Atribuicao** | Ultimo clique | View-through + ultimo clique |

### Bing vs LinkedIn Ads

| Aspecto | Bing Ads | LinkedIn Ads |
|---|---|---|
| **Formato** | Search + Audience | Feed + InMail + Text |
| **CPC medio** | $0.35 - $1.45 | $5.00 - $10.00 (feed) |
| **Segmentacao profissional** | Via LinkedIn targeting (search) | Nativa (completa) |
| **Intencao de compra** | Alta (busca ativa) | Baixa (scrolling feed) |
| **CVR** | 2-5% (dependente do setor) | 0.5-2% (feed) |
| **CPA** | Medio | Alto (3-10x mais caro) |
| **Volume** | Baixo-Médio | Medio |
| **Melhor para** | B2B com intencao de busca | B2B branding + awareness |

**Conclusao:** Bing Ads ocupa um espaco unico entre Google (intencao alta, publico geral) e Meta/LinkedIn (intencao baixa, publico segmentado). Bing tem intencao de busca MAIS Google e segmentacao profissional MAIS LinkedIn — mas com menos volume que ambos.

---

## Analise de Search Query Reports (SQR) no Bing

### Como interpretar Search Queries no Bing

O SQR (Search Query Report) do Bing mostra exatamente o que os usuarios digitaram para ver seus anuncios. E a ferramenta mais importante para otimizacao de keywords e negativos.

**Diferencas do SQR do Google:**
- Bing mostra MENOS search queries que Google (leilao menor)
- Bing demora MAIS para mostrar novas queries (pode levar 48h+)
- Bing agrupa queries similares de forma diferente do Google
- Bing pode mostrar queries com baixo volume que Google nao mostra

**Estrategia de analise SQR (a cada 7 dias):**
1. Exportar SQR dos ultimos 30 dias
2. Filtrar: gasto > R$ 0 e pelo menos 1 clique
3. Identificar queries com:
   - Conversao: manter e considerar adicionar como keyword (se fizer sentido)
   - Gasto alto sem conversao: adicionar como negativa
   - CTR baixo: verificar relevancia
   - CPC alto: verificar concorrencia na query
4. Adicionar negativos em massa (minimo 50-100 por semana em contas ativas)

**Categorizacao de Search Queries:**

| Tipo | Acao |
|---|---|
| Query converteu e e relevante | Adicionar como keyword (Exact ou Phrase) |
| Query converteu mas e coincidencia | Manter como negativa |
| Query gastou mas nao converteu (relevante) | Ajustar lance ou copy |
| Query gastou mas nao converteu (irrelevante) | Adicionar como negativa |
| Query com CTR muito baixo | Verificar copy ou adicionar negativa |
| Query com CPC muito alto | Verificar concorrencia na query |
| Query de marca do concorrente | Adicionar como negativa (geralmente) |

---

## Consideracoes Especificas por Setor no Bing Ads

### E-commerce no Bing

**Oportunidades:**
- CPCs mais baixos que Google (30-50% menor)
- Publico de maior renda (ticket medio maior)
- Menos concorrencia em nichos especificos
- Microsoft Shopping como complemento ao Google Shopping

**Desafios:**
- Volume menor (especialmente para produtos de consumo massivo)
- CVR menor que Google (usuario Bing pesquisa mais, compra menos no primeiro clique)
- Shopping Bing menos maduro que Google Shopping
- Remarketing limitado para recuperar carrinho abandonado

**Melhores praticas:**
- Priorize produtos com margem alta (CPC baixo compensa mesmo com CVR menor)
- Use Microsoft Shopping para produtos que Google Shopping tem muita concorrencia
- Otimize feed para Bing (descricoes mais ricas, titulos com mais palavras-chave)
- Capture audiencia de maior renda com produtos premium
- Configure remarketing para visitantes de produto e carrinho abandonado

### B2B no Bing

**Oportunidades:**
- Melhor plataforma de search para B2B (depois do Google)
- LinkedIn targeting integrado exclusivo em search
- Publico corporativo (Windows/Office/Edge)
- Desktop-heavy (horario comercial = horario de trabalho)
- CPCs mais baixos que Google para keywords B2B

**Desafios:**
- Volume baixo para keywords B2B muito especificas
- LinkedIn targeting reduz volume drasticamente
- Ciclo de venda B2B longo = janela de conversao precisa ser longa
- Atribuicao de ultimo clique injusta para jornadas B2B complexas

**Melhores praticas:**
- Use LinkedIn targeting como NEGATIVO (excluir estudantes, estagiarios)
- Segmente por setor (industria) + cargo (decisor)
- Configure janela de conversao de 60-90 dias
- Capture leads com formulario (nao venda direta — Bing e topo de funil B2B)
- Use Audience Network para awareness B2B (CPC baixo, branding)

### Servicos Locais no Bing

**Oportunidades:**
- Bing tem boa penetracao em cidades menores (Windows/Edge padrao)
- Menos concorrencia que Google para servicos locais
- CPCs muito mais baixos que Google
- Publico mais velho = servicos de saude, financas, assistencia

**Desafios:**
- Volume muito baixo em cidades pequenas
- Mobile e menor — servicos locais pesquisados no celular perdem
- Bing pode ter menos leads que Google para o mesmo investimento

**Melhores praticas:**
- Segmente por raio (20-50km)
- Verifique se seu publico-alvo usa Bing (teste antes de investir pesado)
- Capture leads com formulario (ligacao pode ser menos eficiente no Bing)
- Use extensoes de local e callout

---

## Scripts e Automacoes Uteis para Bing Ads

### Modelo de Planilha de Otimizacao Semanal

Embora Bing nao tenha scripts como Google Ads, voce pode usar planilhas e automacoes:

**Estrutura de planilha de otimizacao:**
```
Semana: [data]
Conta: [nome]

KEYWORDS PARA AUMENTAR LANCE (+15%):
- keyword1 (ROAS 8:1, IS 40%)
- keyword2 (CPA R$ 15, orcamento folgado)

KEYWORDS PARA REDUZIR LANCE (-25%):
- keyword3 (CPA R$ 120, target R$ 80)
- keyword4 (ROAS 1.5:1, 30 dias)

KEYWORDS PARA PAUSAR:
- keyword5 (0 conversoes, R$ 200 gastos, 30 dias)
- keyword6 (CPA R$ 200, 2 conversoes em 60 dias)

NEGATIVOS A ADICIONAR:
- "gratis", "barato" (se nao vende para esse publico)
- nomes de concorrentes

NOVAS KEYWORDS:
- baseado em search queries que converteram
- baseado em Keyword Planner do Bing
```

### Integracao com APIs Bing Ads

Para automacao avancada, Bing Ads fornece APIs REST e SOAP:

**Endpoint:** `https://ads.microsoft.com/api/v13/`

**Funcionalidades via API:**
- Gerenciamento de campanhas (CRUD)
- Relatorios customizados
- Gerenciamento de audiencias
- Gerenciamento de feeds (Microsoft Merchant Center)
- Dados de UET e conversoes

**Casos de uso de API:**
- Dashboards em tempo real
- Automacao de lances customizada
- Sincronizacao com CRM
- Relatorios multicontas consolidados
- Backup automatizado de contas

---

## Perguntas Frequentes (FAQ) para o LLM

Quando o usuario fizer perguntas comuns, use estas respostas como guia:

**P: "Bing Ads vale a pena para meu negocio?"**
R: Depende do setor, publico e orcamento. Bing tende a valer mais a pena para: B2B, alto tiquete (> R$ 300), publico 35+ anos, nichos com Google muito competitivo, produtos/servicos corporativos. Bing tende a valer menos para: B2C massivo, baixo tiquete (< R$ 100), publico jovem (< 30 anos), moda, entretenimento. Recomende testar com orcamento de 10-20% do investimento do Google por 30-60 dias antes de decidir.

**P: "Qual orcamento minimo para Bing Ads?"**
R: O minimo RECOMENDADO e R$ 500-1.000/mes ou $200-500/mes. Abaixo disso, os dados sao muito escassos para otimizacao. Bing precisa de volume minimo para aprender e estabilizar. Se o orcamento for menor que isso, concentre em 5-10 keywords de alta intencao.

**P: "Devo importar minha campanha do Google ou criar do zero?"**
R: Importe como BASE e depois reotimize manualmente. A importacao copia estrutura e keywords, mas os lances estao errados (altos demais), o copy nao funciona (feito para publico Google), e os match types se comportam diferente. NUNCA confie na importacao sem revisao. Planeje 2-4 horas de reotimizacao apos importar.

**P: "Por que Bing nao gasta meu orcamento?"**
R: Causas mais comuns: (1) Campanha nova em learning period (aguarde 48-72h), (2) Keywords com pouco volume no Bing, (3) Lances muito baixos, (4) Segmentacao muito restrita, (5) Impression Share baixo por rank. Diagnostique com as arvores de decisao desta skill.

**P: "Search Partners: devo ligar ou desligar?"**
R: Teste por 14 dias e compare. Se CPA Partners > 2.5x Search puro, desligue. Se Partners geram volume com CPA aceitavel (dentro de 1.5x), mantenha. Regra pratica: Partners tendem a ser bons para e-commerce (volume) e ruins para leads B2B (qualidade).

**P: "Como comparar Bing com Google de forma justa?"**
R: (1) Mesmo periodo, (2) Mesmas keywords, (3) Mesma janela de conversao, (4) Ignore view-through conversions no Bing para comparacao, (5) Aceite 15-25% de discrepancia entre plataformas. Bing quase sempre tera MENOS volume que Google — isso nao significa que e pior.

**P: "Bing Audience Ads e a mesma coisa que GDN?"**
R: NAO. Sao redes completamente diferentes. Audience Ads e nativa/discovery no ecossistema Microsoft (MSN, Edge, Outlook). GDN e display programatica em milhares de sites. Nao compare as duas diretamente.

**P: "Bing Shopping funciona para meu e-commerce?"**
R: Funciona melhor para: nichos, produtos com margem alta, publico 35+ anos. Funciona pior para: moda, produtos de consumo massivo, publico jovem. Teste com seus 20-50 produtos mais vendidos antes de expandir.

**P: "Qual a maior diferenca entre Bing e Google que todo gestor deveria saber?"**
R: Audiencia Bing NAO e "a mesma pessoa que usa Google". E um usuario DIFERENTE — mais velho, maior renda, mais desktop, menos sofisticado digitalmente. Ele pesquisa de forma diferente, clica de forma diferente, compra de forma diferente. Se voce tratar Bing como Google, vai perder dinheiro.

## 15 Erros Comuns em Contas Bing Ads (e Como Evitar)

1. **Importar campanha do Google sem revisar** — lances altos, copy inadequado, match types errados.
   *Solucao:* Reduza lances 30-50%, crie copy novo, monitore 14 dias.

2. **Nao verificar Search Partners separadamente** — Partners podem estar drenando 30-50% do orcamento com baixa conversao.
   *Solucao:* Sempre analise com breakdown Search vs Partners.

3. **Comparar CPA Bing com Google sem contexto** — Bing CPA pode ser diferente por causa da audiencia, nao por causa da plataforma.
   *Solucao:* Compare CVR e CPC separadamente, entenda o mix.

4. **Ignorar desktop** — Bing e 60-70% desktop. Otimizar para mobile como se fosse Google e erro grave.
   *Solucao:* Otimize landing page para desktop, ajuste lances para desktop.

5. **UET tag mal configurada** — causa #1 de "Bing nao converte".
   *Solucao:* Teste com UET Tag Helper, verifique console, faca teste de fogo.

6. **Tomar decisoes baseado em menos de 7 dias de dados** — Bing e mais volátil e tem mais delay que Google.
   *Solucao:* Periodo minimo de analise: 7 dias. Decisoes de CPA: 30+ conversoes.

7. **Nao usar negativos em quantidade suficiente** — Bing match types sao menos restritivos.
   *Solucao:* Adicione 50-100 negativos por semana nas primeiras semanas.

8. **Achar que Audience Network vai substituir Search** — Sao canais complementares, nao substitutos.
   *Solucao:* Audience = 10-30% do orcamento, nao mais.

9. **Ignorar Microsoft Clarity** — ferramenta gratuita que mostra exatamente o que o usuario faz na pagina.
   *Solucao:* Instale Clarity, filtre por trafego Bing, veja replays.

10. **Nao ajustar janela de conversao para o ciclo de compra** — default pode ser muito curto.
    *Solucao:* Configure 30-90 dias dependendo do produto.

11. **Usar Exact Match como unico match type** — Bing exact e muito restritivo, limita volume.
    *Solucao:* Use Phrase como principal, Exact para alta intencao, Broad com negativos.

12. **Copiar copy do Google sem adaptar** — o tom que funciona no Google pode nao funcionar no Bing.
    *Solucao:* Teste tom mais profissional, headlines mais descritivas, ofertas claras.

13. **Nao usar extensoes de anuncio** — Bing valoriza menos extensoes que Google, mas elas ainda importam.
    *Solucao:* Configure sitelinks, callouts, snippets — pelo menos 3 de cada.

14. **Desistir cedo demais** — Bing precisa de 2-4 semanas de maturacao antes de mostrar performance real.
    *Solucao:* Comprometa-se com 60 dias de teste antes de desligar.

15. **Tratar Bing como "segunda tela"** — Bing merece estrategia propria, nao sobra de orcamento.
    *Solucao:* Crie estrategia especifica para Bing, com metas e keywords proprias.

## 10 Metricas Pouco Conhecidas do Bing Ads Que Fazem Diferenca

1. **"Time to Conversion"** — mostra quanto tempo entre o clique e a conversao. Essencial para ajustar janela de atribuicao.

2. **"Top Impression Rate"** — % de impressoes que aparecem no topo dos resultados. Bing mostra isso separadamente.

3. **"Search Exact Match Impression Share"** — impression share apenas para exact match. Mostra quanto do trafego mais qualificado voce esta capturando.

4. **"Click Share"** — sua participacao no total de cliques do leilao. Diferente de Impression Share (mede cliques, nao impressoes).

5. **"Bing Audience Network: View-through Conversion Rate"** — mostra conversao de visualizacao. Use com cautela.

6. **"Goal Conversion Rate by Category"** — CVR por tipo de goal (se voce tem multiplos goals configurados).

7. **"Historical Quality Score"** — Bing mostra a evolucao do QS ao longo do tempo. Essencial para contas novas.

8. **"Device Overlap"** — % de usuarios que viram o anuncio em multiplos dispositivos. Para entender cross-device.

9. **"Call Duration"** — se voce usa extensao de ligacao, Bing mostra duracao media das chamadas (diferencial vs Google).

10. **"Revenue per Click (RPC)"** — receita media por clique. Mais util que ROAS para comparar campanhas com produtos de precos diferentes.

---

## Matriz de Maturidade de Conta Bing Ads

Use esta matriz para avaliar em que estagio a conta Bing Ads esta e o que priorizar.

### Nivel 1: Setup (0-30 dias)
- Conta criada e campanhas configuradas
- UET tag instalada (verificar)
- Primeiros dados chegando
- **Foco:** Estabilizar tracking, entender volume, nao otimizar agressivamente

### Nivel 2: Otimizacao Basica (30-90 dias)
- 30+ conversoes acumuladas
- Quality Score estabilizando
- Search Partners avaliados
- Keywords negativas em andamento
- **Foco:** Melhorar CPA, testar match types, ajustar lances

### Nivel 3: Otimizacao Avancada (90-180 dias)
- 100+ conversoes acumuladas
- Auto-bidding viavel (Target CPA/ROAS)
- Audience Network testada
- Experimentos rodando
- **Foco:** Escalar o que funciona, testar novas estrategias

### Nivel 4: Maturidade (180+ dias)
- Dados consistentes para tomada de decisao
- Bing como canal estabelecido
- Integracao com CRM/GA4 funcionando
- Otimizacao continua automatizada
- **Foco:** Inovacao (LinkedIn targeting, Copilot ads, novas features)

---

## Notas Finais

Bing Ads nao e para todo mundo. Para alguns setores (B2B, alto tiquete, nichos, publico 35+), Bing pode ser o canal com melhor ROAS da conta. Para outros (B2C massivo, baixo tiquete, publico jovem), Bing pode ser irrelevante.

O gestor de trafego que SABE usar Bing Ads tem uma vantagem competitiva real — menos concorrencia, CPCs mais baixos, oportunidades que 90% dos anunciantes ignoram.

Esta skill foi construida para que um LLM possa interpretar metricas de Bing Ads com a profundidade que a plataforma merece — nao como um "Google inferior", mas como um canal unico com caracteristicas proprias.

---

## Guia Rapido de Startup — Primeiros 30 Dias no Bing Ads

Para gestores que estao comecando do zero no Bing Ads, este guia fornece um roteiro dia a dia para os primeiros 30 dias.

### Semana 1: Fundacao (Dias 1-7)

**Dia 1:** Criar conta Bing Ads. Instalar UET tag no site. Verificar com UET Tag Helper.
**Dia 2:** Importar campanha do Google OU criar campanha manualmente com 10-20 keywords principais. Configurar orcamento diario.
**Dia 3:** Verificar se campanha esta rodando. Ajustar lances (reduzir 30-50% se importou do Google). Configurar Search Partners (desligar se orcamento limitado).
**Dia 4:** Configurar extensoes de anuncio (sitelinks, callouts, snippets). Adicionar 50 negativos iniciais.
**Dia 5:** Verificar primeiros dados. Nao otimizar ainda — deixar learning period.
**Dia 6:** Revisar search terms. Adicionar mais negativos.
**Dia 7:** Relatorio da primeira semana. Decidir se continua ou ajusta rota.

### Semana 2: Estabilizacao (Dias 8-14)

**Dia 8-9:** Deixar campanha rodar sem alteracoes. Apenas monitorar.
**Dia 10:** Primeira rodada de otimizacao leve: ajustar lances de keywords com performance clara.
**Dia 11:** Revisar Search Partners (se ativos). Decidir se mantem ou desliga.
**Dia 12:** Criar segunda variacao de copy para grupos com CTR baixo.
**Dia 13:** Verificar Quality Score das principais keywords.
**Dia 14:** Relatorio da segunda semana. Comparar com semana 1.

### Semana 3-4: Crescimento (Dias 15-30)

**Dia 15-17:** Expandir keywords baseado em search terms que converteram. Adicionar 20-50 novas keywords.
**Dia 18-20:** Testar Phrase/Broad Match para keywords que estao com volume baixo em Exact.
**Dia 21:** Configurar remarketing (se site tem trafego suficiente, 300+ usuarios).
**Dia 22-25:** Testar Audience Network com 10-15% do orcamento.
**Dia 26-28:** Revisar estrutura de campanha. Agrupar keywords por intencao.
**Dia 29:** Verificar se 30+ conversoes acumuladas para considerar auto-bidding.
**Dia 30:** Relatorio mensal completo. Decidir: escalar, manter ou repensar.

### Checklist de 30 Dias

```
[ ] Conta criada e campanha ativa
[ ] UET tag instalada e verificada
[ ] Primeiros dados de clique e conversao chegando
[ ] Search Partners avaliados (ligado/desligado)
[ ] 100+ negativos adicionados
[ ] Extensoes configuradas (minimo sitelinks + callouts)
[ ] Copy testado (minimo 2 variacoes por grupo)
[ ] Quality Score monitorado
[ ] Remarketing configurado (se viavel)
[ ] Audience Network testada (se viavel)
[ ] Relatorio de 30 dias gerado
[ ] Decisao tomada sobre continuidade
```

## Mapa Mental da Skill (Para Navegacao Rapida do LLM)

```
GT-ANALISE-BING-ADS
│
├── 1. VISAO GERAL
│   ├── O que e Bing Ads
│   ├── Por que e diferente
│   ├── Oportunidades vs Limitacoes
│   └── Ecossistema Microsoft
│
├── 2. PREMISSAS FUNDAMENTAIS
│   ├── Bing nao e Google mais barato
│   ├── Search Partners
│   ├── Hierarquia de confianca
│   └── Complementar vs Substituto
│
├── 3. PIRAMIDE DE DECISAO
│   ├── CAMADA 1: Operacao diaria (11 metricas)
│   ├── CAMADA 2: Diagnostico tatico (9 metricas)
│   └── CAMADA 3: Investigacao profunda (9 metricas)
│
├── 4. CAMADA 1 — METRICAS
│   └── Cada metrica: conceito, normalidade, verde/amarelo/vermelho
│
├── 5. CAMADA 2 — DIAGNOSTICO
│   └── QS, IS, Partners, Device, Match, Audience, LinkedIn
│
├── 6. CAMADA 3 — INVESTIGACAO
│   └── Atribuicao, UET, View-through, Cross-device, Auto-bidding
│
├── 7. CENARIOS ESPECIFICOS (10 cenarios)
│
├── 8. DIFERENCAS BING vs GOOGLE
│   ├── Tabela comparativa
│   ├── QS, Lances, Display, Remarketing, Atribuicao, Shopping
│   └── Importacao do Google
│
├── 9. PROTOCOLO DE LEITURA
│   └── Fluxo logico de 7 passos + template de resposta
│
├── 10. ARVORES DE DECISAO (8 arvores)
│
├── 11. PARAMETROS LLM
│   ├── Temperatura, thresholds, pesos, precedencia
│   └── Tabela de benchmarks por setor
│
├── 12. GLOSSARIO AVANCADO
│   ├── UET, Shopping, Audience, LinkedIn, Partners
│   ├── Position Value, DSA, Auto-bidding, Remarketing
│   ├── Importacao Google, Clarity
│   └── APIs e Ferramentas
│
├── 13. CASOS PRATICOS (4 casos completos)
│
├── 14. CADENCIAS E ROTINAS
│   ├── Timeline, diferencas vs Google, estrutura de report
│   └── Template de report semanal
│
├── 15. REGRAS DE OURO (10 regras)
│
├── 16. FERRAMENTAS ADICIONAIS
│   ├── Tabela de referencia rapida
│   ├── Matriz de decisao por problema
│   ├── Troubleshooting avancado
│   ├── Metricas avancadas
│   ├── Integracoes (Clarity, Editor, Shopping, Power BI)
│   ├── Framework de otimizacao continua
│   ├── Comparativo Bing vs Meta vs LinkedIn
│   ├── Search Query Reports (SQR)
│   ├── Consideracoes por setor
│   ├── Automacoes e scripts
│   ├── 10 metricas pouco conhecidas
│   ├── FAQ para o LLM
│   ├── 15 erros comuns
│   ├── Guia de startup 30 dias
│   └── Comandos rapidos
│
└── NOTAS FINAIS
```

## Comandos Rapidos para o LLM

Quando o usuario pedir acoes especificas, use estes templates de resposta:

**"Resuma a performance"**
```
Bing Ads — Resumo Rapido
Periodo: [X] dias
Gasto: R$ X.XXX
Conversoes: [X]
CPA: R$ [X.XX]
ROAS: [X.X:1]
Status: [Verde/Amarelo/Vermelho]
Destaque: [principal observacao]
```

**"O que devo otimizar primeiro?"**
```
1. [Prioridade #1] — [acao] — impacto esperado: [alto/medio/baixo]
2. [Prioridade #2] — [acao] — impacto esperado: [alto/medio/baixo]
3. [Prioridade #3] — [acao] — impacto esperado: [alto/medio/baixo]
Tempo estimado para implementacao: [X] horas
Tempo para ver resultados: [X] dias
```

**"Bing vs Google — qual canal esta melhor?"**
```
Bing: CPA R$ [X.XX], ROAS [X.X:1], CVR [X.X%], Volume [X]
Google: CPA R$ [X.XX], ROAS [X.X:1], CVR [X.X%], Volume [X]
Diferenca CPA: Bing [X% +/-] Google
Diferenca ROAS: Bing [X% +/-] Google
Melhor canal para escalar: [Bing/Google]
Melhor canal para eficiencia: [Bing/Google]
Melhor canal para volume: [Bing/Google]
```

**"Devo aumentar o orcamento do Bing?"**
```
Orcamento atual: R$ X.XXX/mes
Gasto atual: R$ X.XXX/mes (X% do orcamento)
Impression Share: X% (lost to budget: X%, lost to rank: X%)
CPA atual: R$ X.XX (target: R$ X.XX)
ROAS atual: X.X:1

Recomendacao: [Sim/Nao/Parcial]
Justificativa: [explicacao baseada nos dados]
Quanto aumentar: [X% ou R$ X.XXX] 
Risco: [descricao do que pode dar errado]
```

---

*Documento mantido pela equipe V4. Atualizacoes e contribuicoes via pull request no Builders Hub.*
