---
name: gt-analise-meta-ads
description: Skill de analise de metricas Meta Ads com interpretacao contextual — sabe diferenciar metrica de operacao diaria vs diagnostico vs investigacao profunda. Arvores de decisao, protocolo de leitura de cenarios, parametros LLM e melhores praticas do mercado.
area: gt
author: v4team
version: 1.0.0
aliases: [gt-analise-meta-ads, meta-analytics, meta-metrics]
tags: [skill, area-gt, meta-ads, analytics]
---

# Visão Geral

## Quem é esta skill

Sou uma skill de análise de tráfego pago especializada em Meta Ads (Facebook, Instagram, Audience Network, Messenger). Não sou um listador de métricas — sou um framework de **interpretação contextual**. O que me diferencia é que eu sei **quando** cada métrica importa, **o que ela realmente está dizendo** (nem sempre o óbvio), e **qual decisão tomar** baseado no cenário completo.

## O que resolve

- Gargalos de performance que gestores de tráfego não conseguem diagnosticar olhando métricas isoladas
- Otimizações burras: pausar criativo com CPA alto sem ver que ele está em learning phase
- Confusão entre métricas do Meta Ads vs GA4 vs CRM (atribuição diferente, janelas diferentes, dados diferentes)
- Perda de dinheiro por interpretação errada de view-through conversion, frequency cap mal ajustado, ou leilão mal compreendido
- Leads que chegam mas não convertem — diagnóstico de onde o funil quebra

## Para quem é

- Gestores de tráfego pleno/senior que querem elevar o nível analítico
- Analistas de performance que precisam se comunicar melhor com contas e clientes
- Líderes de mídia que revisam contas de terceiros
- LLMs sendo usados como copiloto de análise de mídia paga

## Diferencial central: interpretação contextual

Um gestor comum olha CPA = R$80 e pensa "caro demais". Um gestor com sabedoria contextual pergunta:

- Em qual fase da jornada do cliente esse CPA acontece? (Topo vs Fundo?)
- Qual a origem desse lead? (Direto vs Retargeting vs Similar?)
- Qual a janela de atribuição? (1d click+1d view vs 7d click+1d view?)
- Qual o LTV desse lead? (CPA de R$80 com LTV de R$800 é excelente)
- Qual o volume de conversões? (50 vs 2 — muda completamente a confiança)
- O criativo está em learning phase? (Custos iniciais são sempre piores)

A skill toda é construída em torno de uma pirâmide de decisão. Você não olha métricas de Camada 3 quando Camada 1 já respondeu o problema. E você não toma decisão de Camada 3 (como mudar janela de atribuição) antes de verificar Camada 2 (breakdown por plataforma).

---

# Premissas Fundamentais para o LLM

## Regra de ouro #1: Hierarquia de confiança das métricas

As métricas NÃO têm o mesmo peso. Em ordem decrescente de confiança (mais concretas primeiro):

1. **Gasto** — o dinheiro que saiu da conta. Indiscutível. Não mentiroso.
2. **Conversões no CAPI** (se implementado corretamente) — mais confiável que pixel. Verificar match rate.
3. **Conversões no pixel** — confiável se não houver duplicata. Problema: bloqueadores, iOS 14.5+
4. **Cliques no link** — confiável. Meta mede o clique no link, não bounce.
5. **Impressões + Alcance** — confiáveis como volume de entrega. Problema: alcance é estimado.
6. **CTR (link)** — confiável como proxy de relevância do criativo + público.
7. **CPM** — confiável como proxy de concorrência e sazonalidade. Problema: CPM único é melhor.
8. **ROAS** — média confiança se atribuído pelo pixel/CAPI. Pode ser artificialmente alto ou baixo.
9. **CPA** — depende da janela de atribuição. Pode variar 300% dependendo da configuração.
10. **Frequência** — útil, mas Meta calcula média. Distribuição real pode ser muito desigual.
11. **View-through conversions** — a métrica mais enganosa. Confiar com ressalvas extremas.
12. **Conversões no GA4** — útil para comparação, mas janela de atribuição própria do Google.
13. **Engajamento (reações, comentários, shares)** — baixa correlação com resultado de negócio.

## Regra de ouro #2: Quando perguntar vs quando inferir

O LLM DEVE perguntar ao usuário quando:

- O setor não foi informado (não infira — peça)
- O CPA/ROAS alvo não foi definido (cada negócio tem margem diferente)
- A implementação de CAPI vs pixel não é conhecida (muda a confiança nas métricas)
- A janela de atribuição configurada não é conhecida (default Meta é 7d click+1d view — mas pode ser diferente)
- O orçamento total da campanha não é conhecido (escala muda interpretação)
- O funil de conversão não está claro (lead gen vs venda direta vs cadastro)

O LLM DEVE inferir (sem perguntar) quando:

- Precisa classificar o cenário em Camada 1, 2 ou 3 baseado nas métricas recebidas
- Precisa determinar thresholds de normalidade baseado no setor informado
- Precisa gerar hipóteses ordenadas por probabilidade
- Precisa descartar métricas irrelevantes para o cenário atual

## Regra de ouro #3: Viéses comuns em Meta Ads que o analista precisa compensar

**Viés do último clique:** Meta, por padrão, atribui conversão ao último anúncio clicado. Toda análise que usa dados crus do Meta SEMPRE superestima o impacto de remarketing e subestima o impacto de topo de funil. Compensação: sempre comparar com DDA (Data-Driven Attribution) ao menos uma vez por mês.

**Viés da janela de atribuição:** Uma conversão pode ser atribuída a um clique dado 7 dias atrás. Se você pausou uma campanha de topo e viu conversões nos próximos 7 dias, a culpa/palmas NÃO são da campanha de fundo. Compensação: sempre verificar time lag (dias entre clique e conversão).

**Viés de view-through:** Se alguém viu um anúncio, não clicou, e converteu em 24h, o Meta atribui como view-through conversion. Mas essa pessoa (a) já compraria de qualquer jeito, (b) foi impactada por outro canal, (c) clicou em anúncio de retargeting no Google. Compensação: view-through conversion NÃO é conversão real. Tratar como "influência", não como "conversão". Descontar 70-90% do valor.

**Viés de iOS 14.5+:** Meta perdeu ~30-50% dos dados de conversão com ATT (App Tracking Transparency). Agora a Meta usa modelagem (AEM = Aggregated Event Measurement) para preencher lacunas. As métricas de conversão são PARCIALMENTE ESTIMADAS. Compensação: confiar mais em CAPI server-side que não depende de ATT. Verificar diferença entre "conversões reportadas" e "conversões modeladas".

**Viés de amostragem:** Quando o volume é baixo (<50 conversões/semana), qualquer métrica é instável e pode variar 200% simplesmente por acaso estatístico. Não tomar decisões baseadas em menos de 50 eventos.

**Viés de escala:** Contas com orçamento pequeno (R$50-200/dia) têm métricas muito mais voláteis que contas grandes (R$5000+/dia). Nunca comparar métricas de contas de escalas diferentes como se fossem equivalentes.

## Regra de ouro #4: Sempre questionar o dado antes de questionar a estratégia

Antes de concluir que a estratégia está errada, o LLM DEVE verificar:

1. O dado está correto? (pixel funcionando? CAPI íntegro? janela correta?)
2. O dado é suficiente? (volume mínimo de 50 conversões?)
3. O dado é consistente? (tendência de 7 dias, não pico de 1 dia?)
4. O dado é comparável? (mesma janela, mesmo período, mesmo objetivo?)
5. O dado faz sentido? (CTR de 5% em B2B com zero conversões = provável dado espúrio)

---

# A Pirâmide de Decisão Meta Ads

```
                    ┌─────────────────────────────┐
                    │       CAMADA 1 — DIA         │
                    │                              │
                    │    O que meu anúncio          │
                    │    está fazendo HOJE?        │
                    │                              │
                    │  CTR · CPM · CPC · Freq     │
                    │  ROAS · CPA · Gasto          │
                    │  Impressões · Alcance        │
                    │  Engajamento · CPM Único     │
                    ├─────────────────────────────┤
                    │       CAMADA 2 — TÁTICA      │
                    │                              │
                    │    POR QUE está              │
                    │    acontecendo?              │
                    │                              │
                    │  Quality Ranking             │
                    │  Engagement Rate Ranking     │
                    │  Conversion Rate Ranking     │
                    │  CPM por breakdown           │
                    │  CTR por placement           │
                    │  Conv por etapa              │
                    │  Freq distribution           │
                    │  CPL qualif vs bruto         │
                    │  ROAS por público            │
                    │  ROAS por criativo           │
                    ├─────────────────────────────┤
                    │       CAMADA 3 — FUNDO       │
                    │                              │
                    │   O que está distorcendo     │
                    │   meus números?              │
                    │                              │
                    │  View-through conversion     │
                    │  Time lag                    │
                    │  Path to conversion          │
                    │  Attr window comparison      │
                    │  CAPI vs Pixel match rate    │
                    │  Incrementality test design  │
                    │  DDA                         │
                    │  New vs returning customer   │
                    │  Cross-device conversions    │
                    │  Assisted conversions        │
                    └─────────────────────────────┘
```

**Funcionamento:**

- Se o problema é explicado pela Camada 1, pare aí. Não desça.
- Se a Camada 1 mostra anomalia mas não explica a causa, vá para Camada 2.
- Se Camada 1 normal, Camada 2 normal, mas resultado do negócio não reflete, vá para Camada 3.
- Nunca pule camadas.

A maioria dos erros em análise de Meta Ads acontece porque o gestor pula para Camada 3 (geralmente "vou mudar a janela de atribuição") quando o problema está na Camada 2 (breakdown por plataforma mostra que Audience Network está drenando performance).

---

# Camada 1 — Métricas de Operação Diária

## 1. CTR (Link Click-Through Rate)

**O que mede:** Percentual de pessoas que viram o anúncio e clicaram no link. Não inclui reações, comentários, shares ou cliques em outros elementos (botão "saiba mais" da própria Meta, perfil, etc).

**Fórmula:** (Cliques no link / Impressões) x 100

**Normalidade por setor (referência Brasil 2025-2026):**

| Setor | CTR baixo | CTR médio | CTR alto |
|-------|-----------|-----------|----------|
| E-commerce moda | <0,6% | 0,8-1,8% | >2,5% |
| E-commerce geral | <0,5% | 0,7-1,5% | >2,0% |
| Educação (cursos) | <0,8% | 1,2-2,5% | >3,5% |
| Saúde/Estética | <0,4% | 0,6-1,2% | >1,8% |
| Serviços B2B | <0,3% | 0,4-0,8% | >1,2% |
| Lead Gen (imóveis) | <0,5% | 0,7-1,4% | >2,0% |
| SaaS B2B | <0,3% | 0,4-0,9% | >1,5% |
| Aplicativos | <0,8% | 1,0-2,0% | >3,0% |
| Conteúdo/Publisher | <1,0% | 1,5-3,0% | >4,0% |
| Fintech | <0,4% | 0,5-1,0% | >1,5% |

**Sinais verdes:**
- CTR dentro ou acima da faixa média do setor
- CTR consistente entre criativos (não depende de um herói)
- CTR no feed melhor que CTR no Audience Network (esperado)

**Sinais amarelos:**
- CTR 15-30% abaixo da faixa média do setor
- CTR bom no feed mas péssimo em Stories/Reels
- CTR caindo gradualmente ao longo de 5+ dias (fadiga de criativo)
- CTR alto mas CPA alto (clique barato mas conversão cara = problema no funil)

**Sinais vermelhos:**
- CTR 40%+ abaixo do setor
- CTR abaixo de 0,3% (mesmo para setores de CTR baixo)
- CTR que caiu abruptamente em 24h (mudança no algoritmo, público cansado, ou problema de entrega)
- CTR alto mas conversão zero (provável CTR enganoso — ver breakdown por placement)

**O que NÃO fazer quando CTR está baixo:**
- NÃO trocar criativo imediatamente se a campanha está em learning phase (<50 conversões)
- NÃO aumentar orçamento esperando melhorar CTR (mais volume = mais impressões para o mesmo público = frequência sobe = CTR cai mais)
- NÃO culpar o criativo sem verificar segmentação (pode ser audiência errada)
- NÃO pausar anúncio com CTR baixo mas CPA dentro do alvo (CTR é meio, não fim)
- NÃO assumir que CTR baixo = criativo ruim (pode ser placement errado — Stories tem CTR naturalmente menor que Feed)

## 2. CPM (Cost Per Mille)

**O que mede:** Custo para cada 1.000 impressões do anúncio.

**Fórmula:** (Gasto total / Impressões) x 1000

**Normalidade por setor (referência Brasil 2025-2026):**

| Setor | CPM baixo | CPM médio | CPM alto |
|-------|-----------|-----------|----------|
| E-commerce moda | <R$12 | R$15-25 | >R$35 |
| E-commerce geral | <R$14 | R$18-28 | >R$40 |
| Educação (cursos) | <R$10 | R$14-22 | >R$32 |
| Saúde/Estética | <R$18 | R$22-38 | >R$50 |
| Serviços B2B | <R$25 | R$30-50 | >R$70 |
| Lead Gen (imóveis) | <R$15 | R$20-32 | >R$45 |
| SaaS B2B | <R$30 | R$35-60 | >R$80 |
| Aplicativos | <R$12 | R$16-28 | >R$40 |
| Conteúdo/Publisher | <R$8 | R$10-18 | >R$25 |
| Fintech | <R$20 | R$25-42 | >R$55 |

**Sinais verdes:**
- CPM dentro da faixa do setor
- CPM consistente ou caindo gradualmente
- CPM único (CPM no alcance máximo) próximo ao CPM geral
- CPM maior no feed que em Stories (esperado)

**Sinais amarelos:**
- CPM 20-35% acima da faixa do setor
- CPM subindo gradualmente (sem aumento de orçamento)
- CPM subiu após mudança de segmentação
- CPM alto em horário nobre (19h-22h) — sazonalidade normal, mas monitorar

**Sinais vermelhos:**
- CPM 50%+ acima da faixa
- CPM dobrou em menos de 48h
- CPM alto com frequência baixa (público competitivo, problema de relevância, ou lance errado)
- CPM disparou mas CTR e Quality Ranking não mudaram (concorrência no leilão)

**O que NÃO fazer quando CPM está alto:**
- NÃO reduzir lance para baixar CPM se a campanha está performando (pode perder entrega)
- NÃO assumir que CPM alto é sempre ruim (em públicos de alto valor, CPM alto é esperado)
- NÃO mudar segmentação só por causa de CPM (verifique Quality Ranking primeiro)
- NÃO confundir CPM alto com "tráfego caro" — CPM único (no alcance) é medida mais justa
- NÃO comparar CPM de campanhas com objetivos diferentes (conversão tem CPM maior que alcance)

## 3. CPC (Cost Per Click)

**O que mede:** Custo médio por clique no link do anúncio.

**Fórmula:** Gasto total / Cliques no link

**Normalidade por setor (Brasil, 2025-2026):**

| Setor | CPC baixo | CPC médio | CPC alto |
|-------|-----------|-----------|----------|
| E-commerce moda | <R$0,60 | R$0,80-1,50 | >R$2,50 |
| E-commerce geral | <R$0,70 | R$1,00-1,80 | >R$3,00 |
| Educação (cursos) | <R$0,40 | R$0,60-1,20 | >R$2,00 |
| Saúde/Estética | <R$1,00 | R$1,50-3,00 | >R$5,00 |
| Serviços B2B | <R$1,50 | R$2,00-4,00 | >R$6,00 |
| Lead Gen (imóveis) | <R$0,80 | R$1,20-2,50 | >R$4,00 |
| SaaS B2B | <R$2,00 | R$3,00-6,00 | >R$10,00 |
| Aplicativos | <R$0,50 | R$0,70-1,40 | >R$2,50 |
| Conteúdo/Publisher | <R$0,30 | R$0,40-0,80 | >R$1,50 |
| Fintech | <R$1,20 | R$1,80-3,50 | >R$5,50 |

**Sinais verdes:**
- CPC dentro ou abaixo da faixa média do setor
- CPC consistente entre dias da semana
- CPC menor que 10% do CPA (relação saudável)
- CPC menor em remarketing que em prospecção (esperado)

**Sinais amarelos:**
- CPC 25-40% acima da faixa
- CPC subindo mas CPM estável (queda de CTR)
- CPC baixo mas nenhuma conversão (cliques baratos = baixa intenção)
- CPC subindo gradualmente (fadiga ou sazonalidade)

**Sinais vermelhos:**
- CPC 60%+ acima da faixa
- CPC + CPM subindo juntos (inflação geral no leilão)
- CPC estável mas CPA disparou (funil quebrado — a página ou oferta é o problema)
- CPC abaixo de R$0,30 com zero conversões (99% de chance de tráfego de baixa qualidade — Audience Network ou bots)

**O que NÃO fazer quando CPC está alto:**
- NÃO trocar criativo se CTR está ok (CPC alto com CTR normal = CPM alto, não é problema de criativo)
- NÃO reduzir lance (seu anúncio simplesmente não será entregue)
- NÃO pausar campanha de prospecção com CPC alto nos primeiros 3 dias (learning phase)
- NÃO concluir que "o público é caro" sem verificar breakdown por placement

## 4. Frequência

**O que mede:** Número médio de vezes que cada pessoa única viu seu anúncio no período selecionado.

**Fórmula:** Impressões / Alcance

**ATENÇÃO:** Frequência é uma MÉDIA. Metade da audiência pode estar vendo 1-2 vezes e metade vendo 6-8 vezes. A média esconde distribuições muito diferentes. Sempre que possível, olhe a frequency distribution (distribuição de frequência).

**Normalidade:**

| Cenário | Saudável | Atenção | Crítico |
|---------|----------|---------|---------|
| Prospecção (público aberto) | 1,0-1,8 | 1,9-2,5 | >2,5 |
| Remarketing 7-30d | 2,0-3,5 | 3,6-5,0 | >5,0 |
| Remarketing 1-7d | 2,5-4,0 | 4,1-6,0 | >6,0 |
| Lookalike (1-3%) | 1,0-1,6 | 1,7-2,2 | >2,2 |
| Segmentação restrita (<50k) | 1,5-2,5 | 2,6-4,0 | >4,0 |
| Campanha de conversão | 1,0-2,0 | 2,1-3,0 | >3,0 |

**Sinais verdes:**
- Frequência entre 1,0 e 2,0 para prospecção
- CTR e CPA estáveis mesmo com frequência subindo
- Frequência baixa mesmo com orçamento alto (bom sinal de alcance disponível)

**Sinais amarelos:**
- Frequência > 2,5 em prospecção
- Frequência > 4,0 em remarketing
- Frequência subindo + CTR caindo (fadiga de criativo confirmada)
- Frequency distribution: 30%+ do público viu 5+ vezes

**Sinais vermelhos:**
- Frequência > 3,5 em prospecção
- Frequência > 6,0 em remarketing
- Frequência subiu + CPA subiu (fadiga severa)
- Frequency distribution: 50%+ do público viu 5+ vezes

**O que NÃO fazer quando frequência está alta:**
- NÃO pausar a campanha sem verificar se a fadiga é geral ou de um criativo específico
- NÃO aumentar o orçamento (vai piorar a frequência)
- NÃO trocar segmentação como primeiro passo (trocar criativo é mais barato e mais rápido)
- NÃO assumir que frequência alta é sempre culpa do criativo (pode ser público pequeno)
- NÃO usar "frequency cap" da Meta como solução mágica (reduz entrega, não resolve criativo fraco)
- NÃO ignorar frequência porque ROAS está bom (em 5-7 dias o ROAS vai cair)

## 5. ROAS (Return on Ad Spend)

**O que mede:** Receita gerada dividida pelo gasto em anúncios.

**Fórmula:** Receita atribuída / Gasto total

**Tipos de ROAS no Meta:**
- **ROAS Simplificado:** Valor de conversão / Gasto (sem subtrair custos). É o que aparece no painel.
- **ROAS Real:** (Receita - CMV - Frete - Taxas - Custos fixos) / Gasto. Meta não calcula. Precisa de CRM.
- **ROAS com Atribuição Padrão:** Considera janela configurada (7d click + 1d view default). Inclui view-through.
- **ROAS com DDA:** Data-Driven Attribution. Distribui crédito entre touchpoints. Mais próximo do real.

**Normalidade por setor:**

| Setor | ROAS baixo | ROAS médio | ROAS alto |
|-------|-----------|-----------|----------|
| E-commerce moda | <2,0 | 3,0-6,0 | >8,0 |
| E-commerce geral | <2,5 | 4,0-7,0 | >10,0 |
| Educação (cursos) | <1,5 | 2,0-4,0 | >6,0 |
| Saúde/Estética | <1,8 | 3,0-5,0 | >7,0 |
| Serviços B2B | <0,5 | 0,8-2,0 | >3,0 |
| SaaS B2B | <0,3 | 0,5-1,5 | >2,5 |
| Assinaturas | <1,0 | 1,5-3,0 | >5,0 |
| Fintech | <0,8 | 1,2-2,5 | >4,0 |

**ATENÇÃO:** Para B2B e SaaS, ROAS baixo não significa problema — o ciclo de venda é mais longo. Avaliar ROAS em janela de 28-90 dias.

**Sinais verdes:**
- ROAS acima do break-even (ROAS mínimo para não perder dinheiro)
- ROAS estável ou crescendo
- ROAS consistente entre campanhas de mesmo objetivo
- ROAS de remarketing maior que ROAS de prospecção (esperado)

**Sinais amarelos:**
- ROAS 15-25% abaixo do break-even
- ROAS caindo gradualmente (3-5 dias consecutivos)
- ROAS bom em remarketing mas ruim em prospecting (pode estar super-otimizando para quem já compraria)
- ROAS alto mas volume muito baixo (pode não escalar)

**Sinais vermelhos:**
- ROAS 40%+ abaixo do break-even
- ROAS caiu abruptamente (em 24h)
- ROAS de remarketing abaixo do ROAS de prospecção (remarketing falhou)
- ROAS reportado vs ROAS real (via CRM) muito diferente (>40% de diferença)

**O que NÃO fazer quando ROAS está baixo:**
- NÃO pausar campanha de topo de funil que tem ROAS baixo (ela alimenta o remarketing)
- NÃO aumentar orçamento em campanha com ROAS baixo esperando "otimizar por escala"
- NÃO mudar janela de atribuição para fazer ROAS parecer melhor (você estará mentindo para si mesmo)
- NÃO assumir que ROAS baixo = criativo ruim sem verificar funil
- NÃO comparar ROAS de prospecção com remarketing como se fossem iguais

## 6. CPA (Cost Per Acquisition / Cost Per Action)

**O que mede:** Custo médio para cada conversão (compra, lead, cadastro, instalação — depende do objetivo).

**Fórmula:** Gasto total / Número de conversões

**Normalidade por setor (referencial amplo):**

| Setor | CPA baixo | CPA médio | CPA alto |
|-------|-----------|-----------|----------|
| E-commerce moda (venda) | <R$25 | R$35-70 | >R$100 |
| E-commerce geral (venda) | <R$30 | R$45-85 | >R$130 |
| Educação (lead) | <R$8 | R$12-25 | >R$40 |
| Saúde/Estética (lead) | <R$25 | R$35-65 | >R$90 |
| Serviços B2B (lead) | <R$30 | R$40-80 | >R$120 |
| Imóveis (lead) | <R$12 | R$18-35 | >R$50 |
| SaaS B2B (free trial) | <R$15 | R$20-45 | >R$70 |
| Aplicativo (instalação) | <R$3 | R$4-10 | >R$15 |
| Fintech (lead) | <R$20 | R$30-55 | >R$80 |

**Sinais verdes:**
- CPA dentro ou abaixo da meta definida
- CPA estável entre dias e semanas
- CPA correlacionado com volume (quanto mais volume, maior o CPA — lei dos retornos decrescentes)
- CPA baixo no remarketing (audiência qualificada)

**Sinais amarelos:**
- CPA 20-30% acima da meta
- CPA subindo gradualmente (3+ dias consecutivos)
- CPA estável mas volume caiu (perdendo oportunidades de escala)
- CPA baixo mas lead não qualifica (ver Camada 2 — custo por lead qualificado vs bruto)

**Sinais vermelhos:**
- CPA 50%+ acima da meta
- CPA dobrou em menos de 72h
- CPA baixo mas zero leads qualificados (meta está convertendo lixo)
- CPA subindo junto com frequência (fadiga confirmada)
- CPA de remarketing igual ou maior que CPA de prospecção (remarketing quebrado)

**O que NÃO fazer quando CPA está alto:**
- NÃO reduzir orçamento pela metade (pode jogar a campanha de volta na learning phase)
- NÃO pausar anúncio que está em learning phase (<50 conversões — o CPA ainda vai estabilizar)
- NÃO culpar a mídia se o problema é na página (verifique taxa de conversão da página primeiro)
- NÃO usar CPA como única métrica de sucesso (CPA caro com LTV alto pode ser ótimo negócio)
- NÃO comparar CPA de campanhas com objetivos diferentes (otimizar para lead é mais barato que otimizar para venda)

## 7. Gasto por Dia

**O que mede:** Quanto está sendo gasto diariamente no conjunto de anúncios/campanha. Não é métrica de performance — é de governança.

**Normalidade:** Depende 100% do orçamento configurado.
- Gasto diário deve ficar entre 90-110% do orçamento diário definido
- Gasto semanal deve bater com o orçamento semanal
- Meta pode gastar até 25% a mais em um dia e compensar no outro (delivery multiplier)

**Sinais verdes:**
- Gasto dentro do orçamento diário
- Gasto consistente entre dias (variação <20%)
- Gasto aumentou gradualmente após learning phase

**Sinais amarelos:**
- Gasto 30-50% abaixo do orçamento diário (público restrito ou lances baixos)
- Gasto errático (ex: R$200, R$50, R$180, R$80 — Meta tendo dificuldade de gastar)
- Gasto no máximo mas performance caiu (orçamento alto demais para o público)

**Sinais vermelhos:**
- Gasto abaixo de 50% do orçamento diário por 3+ dias consecutivos
- Gasto parou completamente (conta com problema, anúncio reprovado, audiência zerada)
- Gasto estourando orçamento em mais de 25% sem aviso

**O que NÃO fazer quando gasto está baixo:**
- NÃO aumentar o lance como primeira ação (verifique segmentação primeiro)
- NÃO duplicar o conjunto de anúncios (cria competição interna no leilão)
- NÃO culpar o Meta (gasto baixo geralmente é problema de audiência restrita)
- NÃO aumentar orçamento agressivamente (>20%/dia) — desestabiliza a entrega

## 8. Impressões

**O que mede:** Número de vezes que o anúncio foi carregado na tela. Uma impressão no Meta não significa que a pessoa VIU o anúncio — significa que foi carregado na tela. No Feed, a pessoa pode passar direto e contar como impressão. Em Stories, 1-3 segundos de exibição contam como impressão.

**O que importa de verdade:**
- Tendência ao longo do tempo (estável, crescendo, caindo)
- Impressões vs Alcance (relação define frequência)
- Impressões por placement (onde está sendo entregue?)
- CPM por placement (quanto estou pagando por essas impressões)

## 9. Alcance (Reach)

**O que mede:** Número de pessoas únicas que viram o anúncio pelo menos uma vez. É ESTIMADO, não exato.

**Relação importante:**
- Alcance cresce no início da campanha, depois estagna quando satura o público
- Se alcance estagnou e frequência está subindo: saturou o público-alvo
- Se alcance continua crescendo: público é amplo o suficiente

**Sinais verdes:**
- Alcance crescendo junto com as impressões
- Alcance cobrindo 20-40% do público por semana
- Alcance novo (públicos não sobrepostos)

**Sinais amarelos:**
- Alcance estabilizou mas ainda há público disponível (problema de entrega)
- Alcance alto mas nenhuma conversão (audiência errada)
- Alcance caindo (público saturado ou orçamento insuficiente)

**Sinais vermelhos:**
- Alcance <5% do público disponível em 7+ dias
- Alcance não cresce mesmo com aumento de orçamento
- Alcance e impressões crescendo mas CTR caindo (expansão para público de baixa qualidade)

## 10. Taxa de Engajamento

**O que mede:** Percentual de pessoas que interagiram com o anúncio (reações, comentários, compartilhamentos, cliques no link).

**Fórmula:** (Interações totais / Impressões) x 100

**Normalidade:**
- Feed: 0,5-2,0% é normal
- Stories: 1,0-3,0% (full screen gera mais engajamento)
- Reels: 1,5-5,0% (formato de maior engajamento natural)
- Audience Network: <0,5%
- Vídeo: 2,0-8,0%

**ATENÇÃO:** Meta penaliza anúncios com baixo engajamento CONSISTENTE. Se um anúncio tem engajamento baixo por vários dias, o algoritmo reduz a entrega. Mas cuidado: alto engajamento NÃO significa alta conversão. Anúncios que geram buzz (reações, comentários) podem ter baixa conversão. Anúncios "chatos" muitas vezes vendem mais que anúncios engraçados.

## 11. CPM Único (Unique CPM)

**O que mede:** Custo para atingir 1.000 PESSOAS ÚNICAS (não impressões).

**Fórmula:** (Gasto total / Alcance) x 1000

**Por que é importante:** CPM pode cair porque você está entregando muitas vezes para as mesmas pessoas (ineficiente). CPM único revela o custo real de alcançar novas pessoas.

**Interpretação:**
- CPM único próximo do CPM geral = frequência baixa, entrega saudável
- CPM único muito maior que CPM geral = frequência alta, saturando público
- CPM único subindo = alcançar novas pessoas está ficando mais caro

---

# Camada 2 — Métricas de Diagnóstico Tático

## 1. Quality Ranking

**O que mede:** Como o Meta avalia a qualidade do seu anúncio comparado aos concorrentes disputando o mesmo público. Percentil (Above Average, Average, Below Average).

**Componentes inferidos (não divulgados oficialmente):**
- Engajamento esperado (cliques, reações, comentários, compartilhamentos)
- Feedback negativo (esconder anúncio, "não tenho interesse", denunciar)
- Pós-clique (bounce rate, tempo na página — inferido via pixel)
- Histórico da página/domínio

**Como interpretar:**
- **Above Average (7-10):** Anúncio melhor que a maioria. Meta recompensa com CPM menor.
- **Average (4-6):** Mediano. Aceitável se CPA está ok.
- **Below Average (1-3):** Anúncio é RUIM para o público. Meta cobra mais caro. Trocar criativo OU mudar público.

**Nuance crítica:** Quality Ranking é comparativo. Depende de quem está disputando o mesmo público. Em mercado de alta qualidade (educação), "Average" pode ser aceitável. Em mercado de baixa qualidade (leads de baixa intenção), "Below Average" pode ser aceitável.

**Quando usar:** SEMPRE QUE CPM ESTIVER ALTO. É a primeira verificação quando o CPM dispara.

**Quando NÃO usar:** Não é útil para diagnóstico de CPA alto se CPM está ok. Não é útil em campanhas com <500 impressões.

## 2. Engagement Rate Ranking

**O que mede:** Percentil de engajamento comparado a anúncios concorrentes.

**Como interpretar:**
- **Above Average:** Pessoas estão interagindo bem. CTR deve estar ok.
- **Average:** Neutro.
- **Below Average:** Pessoas NÃO estão interagindo. Criativo não ressoa, CTA fraca, ou público errado.

**Cenário clássico:** Quality Ranking alto, Engagement Ranking baixo, Conversion Ranking alto. Anúncio não é interessante mas converte bem. É um anúncio "feitio". Meta eventualmente reduz entrega porque prioriza engajamento. Solução: otimizar criativo para engajar sem perder conversão.

## 3. Conversion Rate Ranking

**O que mede:** Taxa de conversão comparada a outros anúncios com o mesmo objetivo, disputando o mesmo público.

**Como interpretar:**
- **Above Average:** Página de destino e oferta funcionam bem.
- **Average:** Normal.
- **Below Average:** Algo errado no pós-clique — página lenta, oferta confusa, formulário quebrado, CTA fraco.

**Quando é a métrica certa:** CPA alto com CTR normal + Conversion Ranking baixo = problema na página.

**Quando NÃO é:** Em campanhas de brand awareness, não importa.

## 4. CPM por Breakdown (Idade, Gênero, Plataforma, Região, Dispositivo)

### Idade
- **18-24:** CPM mais baixo (muita audiência, menos poder aquisitivo)
- **25-34:** CPM médio
- **35-44:** CPM mais alto (maior poder aquisitivo, mais concorrência)
- **45-54:** CPM médio-alto
- **55+:** CPM variável por setor

CPM alto em uma faixa etária = concorrência intensa OU seu anúncio ressoa mal com essa faixa.

### Gênero
- CPM varia 20-50% entre gêneros dependendo do produto
- Se Meta entrega majoritariamente para um gênero com CPM alto: o outro gênero tem Quality Ranking baixo demais para competir

### Plataforma / Placement

Breakdown fundamental. Muda tudo.

| Placement | CPM relativo | CTR relativo | Qualidade do lead |
|-----------|-------------|-------------|-------------------|
| Feed (FB) | 1.0x (base) | 1.0x (base) | Boa |
| Feed (IG) | 0.8-1.2x | 1.2-2.0x | Boa |
| Stories | 0.5-0.7x | 0.5-0.8x | Média |
| Reels | 0.4-0.6x | 0.3-0.6x | Baixa-média |
| Audience Network | 0.3-0.5x | 0.2-0.4x | Baixíssima |
| Messenger | 0.4-0.6x | 0.3-0.5x | Baixa |

**Pattern clássico de problema:** Audience Network ligada: CPM geral baixo, CTR baixo, CPA parece ok no início, mas leads não qualificam, bounce rate 90%+, view-through infla ROAS.

### Região
- Capitais: CPM 1.2-1.5x mais caro que interior
- SP e RJ mais caros. Norte/Nordeste mais baratos
- CPM mais barato não significa melhor CPA — depende da taxa de conversão regional

### Dispositivo
- Mobile: 1.0x base
- Desktop: 1.2-1.8x mais caro (menos audiência)
- Desktop muito mais barato que mobile: audiência desktop pequena ou de baixa qualidade

## 5. CTR por Placement

Breakdown essencial: separar CTR do Feed, Stories, Reels e Audience Network.

- Feed CTR > Stories CTR > Reels CTR > Audience Network CTR (ordem esperada)
- Audience Network CTR próximo do Feed CTR: provável clique acidental ou métrica inflada
- Stories CTR > Feed CTR: criativo funciona em formato vertical — produzir mais conteúdo para Stories

## 6. Taxa de Conversão por Etapa

Diagnóstico de gargalo no funil. Exemplo para lead gen:

- Impressão -> Clique: taxa A (CTR)
- Clique -> Formulário aberto: taxa B
- Formulário -> Lead: taxa C
- Lead -> Lead qualificado: taxa D
- Lead qualificado -> Venda: taxa E

**Onde está o gargalo?**
- Tx A baixa: criativo/segmentação
- Tx B baixa: página de destino
- Tx C baixa: formulário
- Tx D baixa: qualidade do lead (segmentação errada, oferta enganosa)
- Tx E baixa: funil de vendas, follow-up, produto

**Números típicos (referência):**
- Clique -> Lead: 5-15% (B2C), 2-8% (B2B)
- Lead -> Lead Qualificado: 30-50% (B2C), 15-30% (B2B)
- Lead Qualificado -> Venda: 10-25% (B2C), 5-15% (B2B)

## 7. Frequency Distribution

Mais importante que a frequência média. Mostra quantas pessoas viram o anúncio 1x, 2x, 3x, 4x+.

**Como interpretar:**
- 60%+ viram 1-2x: saudável
- 40%+ viram 3x+: iniciando saturação
- 30%+ viram 5x+: saturação severa
- 10%+ viram 10x+: anúncio virou ruído

**O que fazer:**
- Saturação em 1-2x + não converte: problema de audiência, não de frequência
- Saturação em 3-4x + não converte: fadiga de criativo
- Saturação em 5x+: expandir audiência ou pausar campanha

## 8. Custo por Lead Qualificado vs Lead Bruto

**O que é:** CPA para cada lead (formulário) vs CPA para cada lead que passou do primeiro critério de qualificação.

**Por que é fundamental:** Muitas campanhas têm CPA baixo no lead bruto mas custo por lead qualificado alto — porque a segmentação atrai curiosos, não compradores.

**Exemplo numérico:**
- Gasto: R$3.000
- Leads brutos: 100 -> CPA lead bruto: R$30
- Leads qualificados: 20 -> CPA lead qualificado: R$150
- Vendas: 5 -> CPA venda: R$600

O gestor que olha só R$30 de CPA acha que está bem. Mas cada venda custa R$600. Se o ticket médio é R$400, a conta está negativa.

**Quando usar:** SEMPRE quando o lead não está convertendo em venda. Métrica mais subestimada da Meta Ads.

## 9. ROAS por Público

Breakdown do ROAS por segmentação:
- Lookalike 1% > Lookalike 3% > Interesse > Amplo (padrão esperado)
- Lookalike pior que amplo: lookalike mal construído (dados de origem ruins)

**Cenário suspeito:** ROAS muito alto em remarketing e baixo em todos os outros -> remarketing super-atribuindo conversões que aconteceriam de qualquer jeito.

## 10. ROAS por Criativo

**O que revela:**
- 1 criativo 80% melhor que os outros: tem um herói. Escalar variações.
- Todos iguais ou nenhum converte: problema não é criativo. É segmentação, oferta ou página.
- ROAS alto + CPM baixo: criativo vencedor. Rolar escala.
- ROAS alto + CPM alto: criativo bom mas público disputado. Tentar similar audience.
- ROAS zero + alto gasto: consumindo orçamento sem retorno. Pausar.

---

# Camada 3 — Métricas de Investigação Profunda

## 1. View-Through Conversion (VTC)

**O que é:** Conversão atribuída a uma pessoa que VIU o anúncio (exibição de pelo menos 1s no Feed ou 0s em Stories) mas NÃO clicou, e converteu dentro da janela de view-through (default: 1 dia).

**A verdade sobre VTC:**
- NÃO é uma conversão real no sentido tradicional
- É uma conversão INFLUENCIADA (talvez)
- 70-95% das VTCs teriam acontecido de qualquer jeito (estudos de incrementality)
- Meta reporta view-through e click-through juntos no ROAS total

**Quando usar:**
- Quando view-through domina as conversões e click-through é baixa
- Para entender impacto real de campanhas de topo (branding)
- NUNCA tratar VTC como conversão real em contas com margem apertada

**Trade-off:** Desconsiderar 100% das VTCs subestima topo de funil. Considerar 100% superestima. Correto: descontar 70-90% do valor, ou usar DDA.

## 2. Time Lag (Dias até Conversão)

**O que é:** Distribuição do tempo entre o clique no anúncio e a conversão.

**Por que importa:**
- Maioria das conversões em 24h: funil curto, decisão rápida
- Conversões em 5-14 dias: funil longo (cursos caros, imóveis, B2B)
- Time lag > janela de atribuição: você perde 50%+ das conversões reais
- Time lag < 1 dia + VTC alta: provável duplicata de atribuição

## 3. Path to Conversion (Multi-Touch)

**O que é:** Sequência de interações que um usuário teve com seus anúncios antes de converter.

**O que revela:**
- 80%+ touch único (1 clique + converte): remarketing não funciona
- Path médio com 3+ interações: funil longo, campanhas de topo essenciais
- Path com view-through + 1 clique: remarketing de topo funcionando

**Disponível via:** Meta Analytics (não no Ads Manager padrão).

## 4. Attribution Window Comparison

Comparar a mesma métrica com janelas diferentes:

| Janela | Conversões | Perfil |
|--------|-----------|--------|
| 1d click | 100 | Conservadora |
| 7d click | 140 | Padrão Meta |
| 7d click + 1d view | 180 | Inflada (inclui VTC) |
| 28d click | 160 | Mais precisa para funil longo |

**Interpretação:**
- Diferença 1d vs 7d >40%: funil longo (ampliar janela)
- Diferença 7d vs 7d+1d view >30%: view-through inflando resultados
- 1d similar a 7d: funil curto, janela default suficiente
- 28d mostra o dobro de 7d: PRECISA de janela de 28d

**Quando usar:** MENSALMENTE. Snapshots das 4 janelas para ver tendência.

## 5. CAPI vs Browser Pixel Match Rate

**O que mede:** Percentual de eventos do servidor (CAPI) que correspondem a eventos do pixel.

**Interpretação:**
- >90%: implementação excelente. Confiança alta.
- 70-90%: boa. Pequenas discrepâncias aceitáveis.
- 50-70%: problemas. Eventos duplicados ou faltando.
- <50%: IMPLEMENTAÇÃO PROBLEMÁTICA. Métricas não confiáveis.

**Cenário prático:** Match rate baixo = Meta pode estar otimizando para eventos que você não mede corretamente. Explica CPA instável.

**Como acessar:** Events Manager > Diagnostics > Server-Side Events > Match Rate.

## 6. Incrementality Test Design

**O que é:** Teste que mede o impacto incremental real comparando grupo exposto vs grupo de controle (não exposto).

**Por que é padrão ouro:** Elimina viés de atribuição. Mostra quantas conversões ACONTECERAM POR CAUSA DO ANÚNCIO.

**Resultados típicos:**
- 30-50% das conversões atribuídas podem ser não-incrementais
- Remarketing: 10-30% de incremento (70-90% compraria de qualquer jeito)
- Prospecção: 50-80% de incremento

**Quando usar:** Uma vez a cada 3-6 meses. Disponível via Meta Lift Study.

## 7. DDA (Data-Driven Attribution)

**Comparação com last-click:**
- Funil curto (1-2 touchpoints): similar. Não compensa o esforço.
- Funil médio (3-5): 15-30% diferente. Compensa.
- Funil longo (5+): 30-50%+ diferente. ESSENCIAL.

**Disponível:** Meta Analytics > Attribution > Modelo de Atribuição.

## 8. New vs Returning Customer Ratio

**Interpretação:**
- 90%+ new customers: expandindo base (bom para crescimento)
- 70%+ returning: pagando para clientes existentes comprarem de novo
- Mudou abruptamente: algo aconteceu na base ou atribuição

**Cenário suspeito:** ROAS subindo mas new customer caindo -> crescimento vem de vender mais para quem já comprou, não de atrair novos.

## 9. Cross-Device Conversions

20-40% das conversões podem ser cross-device. Meta está entre as melhores em conectar (ecossistema FB/IG/WhatsApp). iOS 14.5+ reduziu essa capacidade.

## 10. Assisted Conversions

Conversões onde o anúncio foi visto/clicado mas NÃO foi o último clique. Revela o verdadeiro impacto de campanhas de topo.

**Exemplo:** Campanha de topo com ROAS 0,5. Mas assisted conversions mostram que contribuiu para 40% de todas as conversões que fecharam via remarketing. Sem essa campanha, remarketing não teria audiência.

---

# Matriz Contexto x Métrica

## Contexto 1: Campanha nova (learning phase)

| Camada | Métrica | O que olhar |
|--------|---------|-------------|
| 1 | Gasto | Gasto está sendo executado? <50% em 48h = problema de entrega |
| 1 | Impressões | Crescendo? Se caiu após 24h, pode ser restrição |
| 1 | Frequência | <1,5 esperado. >2,0 em 48h é alarmante |
| 1 | CTR | >0,5% em 48h é positivo. Abaixo = criativo ou audiência |
| 2 | Quality Ranking | Average ou Above nos primeiros 500 impressions |
| 2 | Breakdown placement | Onde está entregando mais? Placement correto? |
| NÃO OLHAR | CPA | Instável e enganoso antes de 50 eventos |
| NÃO OLHAR | ROAS | Só confiável após 50+ conversões |
| FAZER | — | Aguardar 50 conversões. Alterações apenas após 48h |
| NÃO FAZER | — | Não reduzir orçamento. Não trocar criativo nos primeiros 3 dias |

## Contexto 2: Campanha madura com boa performance

| Camada | Métrica | O que olhar |
|--------|---------|-------------|
| 1 | ROAS | Estável? Subindo ou caindo? |
| 1 | CPA | Consistente dia a dia? Variação >20% é instabilidade |
| 1 | Frequência | Subindo? >2,5 planejar renovação de criativo |
| 1 | Volume conversões | Crescendo ou estagnado? |
| 2 | ROAS por criativo | Rolar vencedor |
| 2 | New vs returning | Atraindo clientes novos ou só vendendo aos existentes? |
| FAZER | — | Rolar criativos vencedores. Expandir públicos. Testar placements (10-20% do budget) |
| NÃO FAZER | — | Não aumentar orçamento >30% de uma vez. Não ignorar a campanha |

## Contexto 3: CPA subiu sem motivo aparente

| Camada | Métrica | O que olhar |
|--------|---------|-------------|
| 1 | CPA | Quanto subiu? Hoje vs ontem vs média 7 dias |
| 1 | CTR | Caiu junto? Problema de criativo/audiência |
| 1 | CPM | Subiu junto? Problema de leilão |
| 1 | Frequência | Subiu junto? Fadiga |
| 1 | Conversões | Volume caiu? Meta não está achando conversões |
| 2 | Breakdown idade/gênero | Alguma faixa disparou? |
| 2 | Breakdown placement | Audience Network começou a entregar mais? |
| 2 | Quality Ranking | Mudou nas últimas 48h? |
| 3 | Time lag | Média de dias mudou? |
| 3 | Attribution window | Comparar 1d vs 7d vs 28d |
| FAZER | — | 1. Verificar Learning Phase. 2. Breakdown placement. 3. Breakdown demográfico. 4. Verificar pixel/CAPI. 5. Concorrência |
| NÃO FAZER | — | Não reduzir orçamento. Não trocar criativo nos primeiros 2 dias |

## Contexto 4: ROAS caindo mas volume aumentando

| Camada | Métrica | O que olhar |
|--------|---------|-------------|
| 1 | ROAS | Queda vs aumento de volume. +40% volume com -20% ROAS = trade-off ok |
| 1 | CPA | Subiu proporcionalmente? Lei dos retornos decrescentes |
| 1 | Alcance | Cresceu? Se ROAS caiu e alcance não cresceu = expansão para público de baixa qualidade |
| 2 | ROAS por público | Queda em remarketing ou prospecção? |
| 2 | New vs returning | New customers aumentou? ROAS mais baixo é esperado |
| FAZER | — | Aceitar trade-off se new customer aumentou. Se ineficiência pura, reduzir ao nível anterior |
| NÃO FAZER | — | Não cortar drasticamente (expandiu base). Não pausar campanha |

## Contexto 5: Volume baixo mas CPA ok

| Camada | Métrica | O que olhar |
|--------|---------|-------------|
| 1 | Gasto | No orçamento ou abaixo? |
| 1 | Alcance | Estagnou? <20% do público = segmentação restrita |
| 1 | Frequência | <1,5 = ainda há espaço para crescer |
| 2 | Delivery breakdown | Meta está gastando o orçamento? |
| 2 | Audience saturation | Público grande o suficiente para escalar? |
| FAZER | — | Aumentar lances 10-15%. Expandir público. Aumentar geografia. Subir orçamento gradualmente |
| NÃO FAZER | — | Não duplicar conjuntos. Não mudar objetivo. Não trocar criativo se CTR ok |

## Contexto 6: Frequência alta

| Camada | Métrica | O que olhar |
|--------|---------|-------------|
| 1 | Frequência | >2,5 prospecção? >5,0 remarketing? |
| 1 | CTR | Caiu junto? Fadiga confirmada |
| 1 | CPA | Subiu junto? Ainda não, mas vai |
| 1 | Alcance | Estagnou? Público saturado |
| 2 | Frequency distribution | % vendo 5x+ vs 1-2x |
| FAZER | — | 1. Trocar criativo. 2. Expandir público. 3. Remarketing: reduzir janela. 4. Pausar 48h (último recurso) |
| NÃO FAZER | — | Não aumentar orçamento. Não reduzir orçamento sem agir sobre criativo |

## Contexto 7: CTR baixo mas CPM alto

| Camada | Métrica | O que olhar |
|--------|---------|-------------|
| 1 | CTR | Valor absoluto vs setor |
| 1 | CPM | Valor absoluto vs setor |
| 1 | CPC | CTR baixo + CPM alto = CPC muito alto |
| 2 | Quality Ranking | Below Average? Meta penalizando |
| 2 | Engagement Ranking | Below Average? Criativo não engaja |
| 2 | Breakdown placement | Audience Network puxando CTR para baixo? |
| FAZER | — | 1. QR baixo? Trocar criativo. 2. QR ok? Ver placement. 3. Testar outro formato |
| NÃO FAZER | — | Não aumentar lance. Não pausar sem ver QR. Não reduzir público |

## Contexto 8: Muita VTC, pouca click-through

| Camada | Métrica | O que olhar |
|--------|---------|-------------|
| 1 | ROAS | Separar ROAS click vs view |
| 1 | CTR | Baixo? Explica falta de click-through |
| 3 | VTC ratio | >40%? Resultado inflado |
| 3 | Time lag | VTCs em <1h? Provável comprariam de qualquer jeito |
| 3 | Attr window comp | Quanto o VTC está inflando? |
| FAZER | — | Remover view-through para avaliação real. Criar CTAs mais fortes. Se VTC >50% no remarketing, repensar estratégia |
| NÃO FAZER | — | Não comemorar ROAS sem ver VTC. Não aumentar orçamento baseado em ROAS inflado |

## Contexto 9: Diferença Meta vs GA4

| Camada | Métrica | O que olhar |
|--------|---------|-------------|
| 3 | Attribution window | Meta 7d+1d view vs GA4 modelo diferente |
| 3 | CAPI vs Pixel match rate | <70% = medindo eventos diferentes |
| 3 | Cross-device | Meta captura melhor que GA4 |
| 3 | View-through | GA4 não tem VTC como Meta |
| DISCREPÂNCIA | — | 20-50% é NORMAL. Meta sempre reporta mais que GA4 |
| FAZER | — | Padronizar janelas quando possível. Usar GA4 para tendência, Meta para operação |
| NÃO FAZER | — | Não tentar fazer bater exatamente. Não confiar cegamente em nenhum isoladamente |

## Contexto 10: Campanha estagnada

| Camada | Métrica | O que olhar |
|--------|---------|-------------|
| 1 | ROAS/CPA | Estagnado ou piorando |
| 1 | Frequência | Quase sempre >3,0 |
| 1 | CTR | Caindo gradualmente |
| 2 | Frequency dist | 40%+ viu 5x+ |
| 2 | Alcance | Não cresce há dias |
| FAZER | — | Pausar 3-5 dias. Lançar novos criativos. Expandir público. Remarketing: reduzir janela 30d para 14d |
| NÃO FAZER | — | Não subir orçamento. Não manter pausado >7 dias. Não criar conjunto idêntico |

## Contexto 11: Lead veio mas não qualificou

| Camada | Métrica | O que olhar |
|--------|---------|-------------|
| 1 | CPA | Baixo? Mas qual CPA qualificado? |
| 2 | Custo lead qualif vs bruto | Diferença >3x? Funil de qualificação quebrado |
| 2 | Breakdown placement | Audience Network é a grande vilã |
| 2 | CTR por criativo | Criativo promissor demais? |
| FAZER | — | 1. Desligar Audience Network. 2. Ajustar copy. 3. Revisar formulário |
| NÃO FAZER | — | Não pausar campanha (pode ser ajuste fino). Não aumentar orçamento para "achar leads melhores" |

## Contexto 12: Remarketing não converte

| Camada | Métrica | O que olhar |
|--------|---------|-------------|
| 1 | ROAS remarketing vs prospecting | Remarketing < Prospecting = quebrado |
| 1 | Frequência remarketing | >5,0? Fadiga severa |
| 1 | CTR remarketing | <0,3%? Criativo não funciona |
| 2 | Window do remarketing | 30d amplo demais? Testar 7-14d |
| FAZER | — | Testar janela menor (7-14d). Trocar criativo (diferente do prospecting). Testar oferta específica (desconto) |
| NÃO FAZER | — | Não pausar remarketing. Não usar mesmo criativo do prospecting |

## Contexto 13: Diferença por plataforma (Feed vs Stories vs Reels vs AN)

| Camada | Métrica | O que olhar |
|--------|---------|-------------|
| 1 | CTR por placement | Ranking: qual placement tem melhor CTR? |
| 1 | CPM por placement | AN é mais barata. Mas lead é de qualidade? |
| 1 | CPA por placement | Vencedor = CTR alta + CPM baixo + CPA baixo |
| 2 | Quality Ranking por placement | QR baixo em Reels? Criativo não é nativo |
| 2 | Conversion Rate por placement | AN tem taxa 50-70% menor que Feed |
| FAZER | — | Separar campanhas por placement. Criar criativos nativos. Desligar AN. Reels: conteúdo vertical rápido |
| NÃO FAZER | — | Não usar mesmo criativo em todos. Não deixar AN em campanha de lead qualificado |

---

# Protocolo de Leitura de Cenários

## PASSO 1: Receber e organizar os dados

Organizar em:
- **Dados de entrada:** Gasto, impressões, cliques, conversões, ROAS, CPA, CTR, CPM, frequência, alcance
- **Contexto:** Tipo de campanha, setor, orçamento, janela de atribuição, CAPI/pixel, funil
- **Problema declarado:** O que o usuário acha que está errado (pode ser diferente do real)

## PASSO 2: Classificar o cenário

- **Camada 1:** Revisão de rotina. Métricas diárias.
- **Camada 2:** Métrica principal anormal. Precisa de diagnóstico.
- **Camada 3:** Métricas normais mas resultado não reflete. Ou Camada 2 não explica.

**Critério:**
- Variação <15%: Camada 1 (monitoramento)
- Variação 15-50%: Camada 2 (diagnóstico)
- Variação >50% ou métricas normais mas negócio não reflete: Camada 3 (investigação)

## PASSO 3: Selecionar métricas da Matriz Contexto x Métrica

Com base no contexto e classificação, selecionar métrica primária (Camada 1), de diagnóstico (Camada 2), de investigação (Camada 3), e métricas a NÃO olhar.

## PASSO 4: Aplicar faixas de normalidade por setor

Comparar cada métrica com:
- Faixa esperada para o setor
- Faixa esperada para o tipo de campanha (prospecção vs remarketing)
- Faixa esperada para a fase (learning phase vs madura)

Identificar métricas DENTRO e FORA do esperado (amarelo/vermelho).

## PASSO 5: Gerar hipóteses ordenadas por probabilidade

**Regras de prioridade de hipóteses:**
1. Mais simples primeiro (Navalha de Occam)
2. Explica MAIS métricas anômalas ao mesmo tempo
3. Requer MENOS alteração para testar
4. Pode ser testada IMEDIATAMENTE

**Formato:**
```
Hipótese 1 (probabilidade: 60%): [explicação]
  -> Evidências a favor: [métricas]
  -> Evidências contra: [métricas]
  -> Teste: [o que fazer para confirmar]
  -> Custo do teste: [tempo, orçamento]
```

## PASSO 6: Recomendar ação com fundamentação

Incluir:
- **Ação imediata** (fazer agora)
- **Ação curto prazo** (2-3 dias)
- **Ação médio prazo** (próxima semana)
- **O que NÃO fazer**
- **Critério de sucesso** (como saber se funcionou)
- **Próximo ponto de verificação** (quando reavaliar)

---

# Árvores de Decisão

## Árvore 1: CPA alto

```
CPA SUBIU >30% NAS ÚLTIMAS 48H
|
|- Campanha em learning phase?
|  |- Sim -> tem <50 conversões?
|  |   |- Sim -> NORMAL. CPA vai oscilar. Não agir.
|  |   |- Nao -> learning phase acabou, deveria ter estabilizado.
|  |
|  |- Nao -> pos-learning phase. Investigar.
|
|- Frequencia > 3,0?
|  |- Sim -> fadiga de audiencia.
|  |   |- CTR caiu junto?
|  |   |   |- Sim -> fadiga confirmada. Trocar criativos.
|  |   |   |- Nao -> verificar distribution.
|  |   |- Apos trocar: aguardar 48h.
|  |
|  |- Nao -> frequencia ok.
|
|- CPM subiu junto?
|  |- Sim -> leilao mais caro.
|  |   |- Quality Ranking baixo?
|  |   |   |- Sim -> Meta penalizando. Trocar criativo.
|  |   |   |- Nao -> concorrencia sazonal.
|  |   |- Se concorrencia: reduzir lances ou aguardar 3-5d.
|  |
|  |- Nao -> CPM estavel.
|
|- CTR caiu (CPM estavel, CPA subiu)?
|  |- Sim -> menos clicando. Criativo cansado? Publico mudou?
|  |- Nao -> CTR estavel.
|
|- Conversoes caíram?
|  |- Sim -> volume de trafego caiu?
|  |   |- Sim -> verificar gasto e entrega.
|  |   |- Nao -> trafego ok, nao converte. Problema na pagina.
|  |- Nao -> conversoes estaveis.
|
|- Breakdown placement mudou?
|  |- Sim -> Audience Network disparou?
|  |   |- Sim -> AN puxando CPA. Desligar.
|  |   |- Nao -> verificar Stories/Reels.
|  |- Nao -> distribuicao ok.
|
|- Nenhuma das anteriores?
    - Verificar CAPI vs Pixel match rate
    - Verificar time lag
    - Verificar mudanca no site
```

## Árvore 2: ROAS baixo

```
ROAS CAIU >30% NA ULTIMA SEMANA
|
|- Volume cresceu junto?
|  |- Sim -> trade-off volume vs ROAS.
|  |   |- New customer ratio aumentou?
|  |   |   |- Sim -> queda aceitavel (expansao de base).
|  |   |   |- Nao -> ineficiencia pura. Reduzir orcamento.
|  |   |- Monitorar por 5-7d antes de agir.
|  |
|  |- Nao -> ROAS caiu sem aumento de volume.
|
|- CPA subiu junto?
|  |- Sim -> ver arvore CPA alto.
|  |- Nao -> CPA estavel mas ROAS caiu.
|  |   |- Ticket medio caiu?
|  |   |   |- Sim -> mix de produtos mudou?
|  |   |   |- Nao -> valor de conversao medio estavel.
|  |   |- Atribuicao mudou? (CAPI/pixel com problema)
|
|- Concorrencia sazonal?
|  |- Sim -> Black Friday, Natal. Aguardar.
|  |- Nao -> verificar CPM.
|
|- VTC aumentou enquanto click-through caiu?
    - Sim -> ROAS inflado artificialmente.
    - Nao -> verificar outras camadas.
```

## Árvore 3: Volume baixo

```
VOLUME DE CONVERSOES MUITO ABAIXO DO ESPERADO
|
|- Gasto sendo executado?
|  |- Nao -> gasto <50% do orcamento.
|  |   |- Learning phase? Aguardar 48h.
|  |   |- Publico restrito? (<50k pessoas)
|  |   |   |- Sim -> expandir publico.
|  |   |   |- Nao -> lances baixos? Aumentar 10-15%.
|  |   |- Anuncio reprovado ou em revisao?
|  |       |- Sim -> corrigir.
|  |       |- Nao -> verificar forma de pagamento.
|  |
|  |- Sim -> gasto ok mas sem conversoes.
|
|- Conversoes totais <50 no periodo?
|  |- Sim -> learning phase. Aguardar.
|  |- Nao -> pos-learning phase.
|
|- Publico saturado?
|  |- Frequencia >3,0? Sim -> expandir.
|  |- Alcance estagnou? Sim -> publico pequeno.
|
|- Pixel/CAPI funcionando?
    - Verificar Events Manager.
```

## Árvore 4: Frequência alta

```
FREQUENCIA >3,0 (prospeccao) OU >5,0 (remarketing)
|
|- Campanha ativa ha quanto tempo?
|  |- <3d -> anormal. Publico minusculo? Expandir.
|  |- 3-14d -> aceleracao rapida. Trocar criativo IMEDIATAMENTE.
|  |- >14d -> fadiga natural. Rotacionar.
|
|- Orcamento alto demais para o publico?
|  |- Calcular: gasto/dia / CPM x 1000 = impressoes/dia
|  |- Impressoes/dia / publico = frequencia projetada
|  |- Se projetada >3: orcamento incompativel.
|      - Solucao: reduzir orcamento ou expandir publico.
|
|- Frequency distribution?
|  |- 40%+ vendo 1-2x, 10% vendo 5x+ -> saudavel com outliers
|  |- 30%+ vendo 5x+ -> problema real. Agir.
|  |- 10%+ vendo 10x+ -> severo. Pausar 48h.
|
|- Remarketing?
    - Publico de 30d? Reduzir para 14d.
    - Publico de 14d? Reduzir para 7d.
    - Excluir conversores.
```

## Árvore 5: CTR baixo

```
CTR 30%+ ABAIXO DA MEDIA DO SETOR
|
|- Quality Ranking?
|  |- Below Average -> criativo nao relevante.
|  |   |- Criativo testado em outros publicos com CTR ok?
|  |   |   |- Sim -> problema e o publico.
|  |   |   |- Nao -> criativo fraco. Trocar.
|  |   |- Feedback negativo alto?
|  |       |- Sim -> criativo irritando publico. Trocar urgente.
|  |- Average/Above -> criativo nao e o problema.
|
|- Breakdown placement?
|  |- CTR Feed ok, mas Stories/Reels/AN pessimos?
|  |   |- Sim -> criar criativos nativos.
|  |   |- Nao -> queda generalizada.
|  |- Audience Network CTR <0,15%? Normal. Desligar se atrapalhar.
|
|- Publico mudou? (breakdown demografico/regiao)
|- Frequencia >3,0? -> fadiga. Trocar criativo.
|- Sazonalidade? Aguardar.
```

## Árvore 6: CPM alto

```
CPM 40%+ ACIMA DA MEDIA DO SETOR
|
|- Quality Ranking?
|  |- Below Average -> causa #1. Trocar criativo.
|  |- Average/Above -> problema nao e relevancia.
|
|- Sazonalidade/Concorrencia?
|  |- Black Friday, Natal? CPM sobe 30-100%. Esperado.
|  |- Concorrente novo?
|      - Verificar se CPM subiu em faixa/horario especifico.
|
|- Publico mudou?
|  |- Segmentacao muito restrita? Publico pequeno = CPM alto.
|  |- Lookalike base pequena? Lookalike impreciso = CPM alto.
|
|- Placement mudou? Feed mais caro (esperado).
|- Estrategia de lance?
    - "Cost cap" ou "Bid cap" pode estar forcando CPM.
```

## Árvore 7: Diferença Meta vs GA4

```
META REPORTA 40%+ MAIS CONVERSOES QUE GA4
|
|- Janela de atribuicao diferente?
|  |- Meta default: 7d click + 1d view
|  |- GA4 default: varia
|  |- Comparar 1d click no Meta vs GA4: reduz diferenca?
|
|- View-through ativas no Meta?
|  |- Sim -> Meta conta conversoes que GA4 nao ve.
|  |- Remover view-through -> diferenca cai.
|
|- CAPI vs Pixel?
|  |- CAPI implementado? Match rate?
|  |- <70%: sistemas medindo eventos diferentes.
|
|- Cross-device?
|  |- Meta capta melhor que GA4.
|  |- 20-30% cross-device: GA4 perde parte.
|
|- Conversoes modeladas (AEM)?
  - iOS 14.5+: Meta modela. GA4 tambem, diferente.
```

## Árvore 8: Performance por plataforma diferente

```
FUNCIONA NO FEED, NAO EM STORIES/REELS/AN
|
|- Stories inferior?
|  |- Criativo nativo? Imagem quadrada cortada? Texto pequeno?
|
|- Reels inferior?
|  |- Reels espera entretenimento, nao anuncio tradicional.
|  |- CTR em Reels e naturalmente menor.
|
|- Audience Network inferior?
|  |- SEMPRE e inferior. Natureza do placement.
|  |- Decisao: desligar se CPA sofrer.
|
|- Messenger inferior?
  |- So faz sentido para objetivos de mensagem.
```

## Árvore 9: Lead bruto vs qualificado

```
CPA LEAD BOM, CPA LEAD QUALIFICADO ALTISSIMO
|
|- Audience Network ligada?
|  |- Sim -> desligar IMEDIATAMENTE. Leads AN sao 5-10x menos qualificados.
|  |- Nao -> verificar outros placements.
|
|- Formulario de lead muito aberto?
|  |- Automático do Meta (menos atrito = menos qualificados)
|  |- Substituir por formulario proprio (mais atrito = mais qualificados)
|
|- Criativo promete demais?
|  |- "GANHE R$500" -> atrai oportunistas.
|  |- Ajustar copy para ser especifico.
|
|- Publico muito amplo? Interesse generico demais? Lookalike muito grande (5-10%)?
  |- Restringir audiencia.
```

## Árvore 10: Estagnação de escala

```
CAMPANHA NAO ESCALA - VOLUME ESTAGNADO HA 7+ DIAS
|
|- Gasto no limite do orcamento?
|  |- Sim -> aumentar gradualmente (10-20%/dia).
|  |- Nao -> gastando menos que o orcamento.
|
|- Publico saturado?
|  |- Alcance estagnou? Sim -> expandir.
|  |- Frequencia subindo? Sim -> trocar criativos + expandir.
|
|- Learning phase infinita?
|  |- Meta nao sai sem 50 conv/semana.
|  |- Nunca chega em 50? Revisar objetivo, pagina, orcamento.
|
|- Segmentacao muito restrita?
|  |- Publico <100k? Lookalike 1%? Muitos exclusion layers?
|
|- Limite de conta/gasto?
  - Conta nova? Meta limita gasto. Aguardar.
```

---

# Parâmetros de Configuração para o LLM

## Temperatura recomendada

- **Análise de dados (Camadas 1-2):** 0.1-0.2 (mínima criatividade, máxima precisão)
- **Geração de hipóteses (Camada 2-3):** 0.2-0.4 (conectar variáveis não óbvias)
- **Recomendação estratégica:** 0.3-0.5 (sem ser excessivamente conservador)
- **Máxima:** >0.5 NUNCA para análise de dados. Leva a alucinações.

## Thresholds de normalidade por setor (consolidado)

| Métrica | Educação | E-commerce | Saude | B2B | Imoveis | Fintech |
|---------|----------|------------|-------|-----|---------|---------|
| CTR min | 0,8% | 0,5% | 0,4% | 0,3% | 0,5% | 0,4% |
| CPC max | R$2,00 | R$3,00 | R$5,00 | R$6,00 | R$4,00 | R$3,50 |
| CPM max | R$32 | R$40 | R$50 | R$70 | R$45 | R$42 |
| Freq max | 2,5 | 2,2 | 2,8 | 3,0 | 2,5 | 2,5 |
| CPA lead | R$25 | - | R$65 | R$80 | R$35 | R$55 |
| ROAS min | 2,0 | 3,0 | 2,5 | 0,8 | - | 1,5 |

## Pesos de cada métrica na tomada de decisão

| Contexto | Metrica #1 (peso) | Metrica #2 (peso) | Metrica #3 (peso) |
|----------|-------------------|-------------------|-------------------|
| Avaliacao diaria | CPA (0.35) | ROAS (0.30) | Gasto (0.20) |
| Diagnostico de problema | CPM/CTR/Freq (0.25) | Quality R (0.15) | Placement (0.10) |
| Decisao de pausar | Frequency (0.30) | CPA trend (0.30) | Quality R (0.20) |
| Decisao de escalar | CPA stability (0.35) | Alcance disp (0.30) | ROAS (0.25) |
| Avaliacao de criativo | CTR (0.35) | ROAS (0.30) | Conv Rate R (0.20) |
| Avaliacao de publico | CPA (0.30) | Alcance (0.25) | CPM (0.20) |

## Regras de precedência (sobreposição de métricas)

1. **CPA e ROAS sempre se sobrepõem a CTR, CPM, CPC.** Criativo com CTR baixo mas CPA na meta não deve ser mexido.
2. **Quality Ranking se sobrepõe a CPM** para diagnóstico de leilão caro. CPM alto + QR alto = concorrência. CPM alto + QR baixo = relevância.
3. **Breakdown por placement se sobrepõe a métricas agregadas.** Sempre que a métrica agregada estiver anormal, o primeiro breakdown é placement.
4. **Dados de 7 dias se sobrepõem a dados de 1 dia.** Tendência semanal > pico/baixa de um dia.
5. **Volume se sobrepõe a valor.** 5 conv CPA R$50 < 100 conv CPA R$60. Maior volume = mais significância.
6. **CAPI se sobrepõe a pixel** quando match rate >80%. Match rate baixo = nenhum confiável.
7. **Dados de funil completo se sobrepõem a métricas de topo.** Custo lead qualificado > CPA lead bruto.
8. **Time lag se sobrepõe a janela de atribuição.** Time lag médio > janela = métricas sistematicamente erradas.
9. **Incrementality (se disponível) se sobrepõe a TODAS.** É o padrão ouro.

## Tabela de prioridade de hipóteses

| Prioridade | Tipo | Exemplo |
|------------|------|---------|
| 1 (sempre) | Problema de dados | Pixel quebrado, CAPI baixo match, janela errada |
| 2 | Problema de delivery | Learning phase, publico saturado, alcance limitado |
| 3 | Problema de criativo | QR baixo, CTR caindo, fadiga |
| 4 | Problema de publico | Publico errado, expansao ma qualidade |
| 5 | Problema de placement | AN drenando, Reels baixa conversao |
| 6 | Concorrencia/sazonalidade | Black Friday, novo concorrente |
| 7 | Problema de pagina/oferta | Tx conversao caindo, formulario quebrado |
| 8 | Problema de atribuicao | Janela errada, VTC inflando |

---

# Glossário Avançado

## CPC (Cost Per Click) vs CPC (Link)

**CPC (todos os cliques):** Inclui cliques no link, botão "Saiba Mais" do Meta, foto do perfil, e qualquer elemento clicável.

**CPC (link):** Apenas cliques no link que saem do Meta.

**Diferença prática:** CPC (todos) é sempre menor que CPC (link). Se a diferença é grande, as pessoas interagem com o anúncio mas não clicam no link — sinal amarelo para campanhas de tráfego.

**No painel:** A coluna "CPC" padrão é CPC (todos). Para ver CPC (link), adicione a coluna específica. Muita gente tira conclusões erradas olhando CPC errado.

## CTR (Todos) vs CTR (Link Click-Through Rate)

**CTR (todos):** (Todas as interações / Impressões) x 100. Inclui cliques, reações, comentários, compartilhamentos.

**CTR (link):** (Cliques no link / Impressões) x 100. Apenas cliques que saem do Meta.

**Perigo:** Muitos reportam CTR (todos) como se fosse CTR de tráfego. Anúncio pode ter CTR 3% (todos) mas CTR 0,5% (link) — ninguém clicou no link.

**Regra:** Para tráfego/conversão, use SEMPRE CTR (link). CTR (todos) é métrica de vaidade.

## View-Through Conversion (a verdade)

**Definição técnica:** Pessoa vê seu anúncio (1s no Feed, 0s em Stories) e converte dentro da janela de view-through sem clicar.

**O que NÃO significa:**
- Não significa que o anúncio causou a conversão
- Não significa que a pessoa considerou sua oferta

**Incrementalidade real:**
- Meta Ads VTC médio: 10-30% é incremental
- Remarketing VTC: 5-15% incremental
- Prospecção VTC: 15-30% incremental

**Uso prático:** Se ROAS inclui VTC, desconte 80% do valor VTC. Ex: ROAS 4,0 com 30% VTC. ROAS ajustado ~ 4,0 / (1 + 0,3 x 0,8) ~ 3,3.

## Frequência no Meta (o que realmente significa)

**O problema:** É uma MÉDIA. A distribuição real pode ser:
- Cenário A: 80% viu 1x, 20% viu 10x -> Frequência média 2,8. 20% severamente saturada.
- Cenário B: 50% viu 2x, 50% viu 3x -> Frequência média 2,5. Distribuição uniforme.

Mesma média, situações completamente diferentes.

**Frequency distribution é essencial.** Meta não mostra no painel padrão. Precisa de exportação.

**Quando a frequência engana:**
- Campanhas novas (dias 1-2): frequência parece alta porque alcance não estabilizou
- Públicos muito pequenos: frequência calculada pode ser maior que real
- Remarketing: frequência alta esperada (público menor), impacto menor

## CPM Único vs CPM

**CPM:** Custo para 1.000 impressões. Pode cair artificialmente por entregar muito para as mesmas pessoas.

**CPM único:** Custo para 1.000 PESSOAS ÚNICAS. (Gasto / Alcance) x 1000.

**Quando CPM único é mais importante:**
- Frequência > 2,0
- Comparando campanhas com frequências diferentes
- Escalando campanha

**Exemplo:**
- Campanha A: CPM R$20, Freq 1,5, Alcance 50k -> CPM único R$20 (bom)
- Campanha B: CPM R$18, Freq 4,0, Alcance 18k -> CPM único R$32 (ruim)

B parece ter CPM mais barato, mas paga mais caro para alcançar novas pessoas.

## ROAS: simplificado, real, com atribuição

**ROAS Simplificado (painel Meta):** Receita de conversão / Gasto. Não considera custos.

**ROAS Real:** (Receita - CMV - Frete - Taxas - Custos fixos) / Gasto. Precisa de CRM.

**ROAS com Atribuição Padrão:** Janela configurada (7d click + 1d view). Inclui VTC. Superestima.

**ROAS com DDA:** Data-Driven Attribution. Mais próximo do real.

**Relação:** ROAS simplificado > ROAS DDA > ROAS real (geralmente).

## CAPI vs Pixel vs Conversões Híbridas

**Pixel (browser-side):** Navegador. Bloqueado por ad blockers, iOS 14.5+. Perde 30-50% dos eventos.

**CAPI (server-side):** Servidor -> Meta. Não bloqueado. Mais confiável. Mais complexo.

**Conversões Híbridas:** Meta combina fontes + modelagem AEM. Mais dados, difícil auditar.

**Na prática:**
- Só pixel: dados parciais, mas funcionam (Meta modela o resto)
- CAPI + Pixel (ideal): máximo de dados
- CAPI sem pixel: funciona, perde deduplicação

**Match rate:** >90% = excelente. <70% = CAPI e pixel medindo eventos diferentes.

## Conversion Window (janela de atribuição)

**Click-through window:**
- 1d click: conversão até 24h após o clique
- 7d click (default): até 7 dias
- 28d click: até 28 dias

**View-through window:**
- 1d view (default): até 24h após ver (sem clicar)
- 7d view: raramente usado (infla demais)

**Como cada janela distorce:**

| Janela | Distorce | Efeito |
|--------|----------|--------|
| 1d click | Subestima funil longo | Perde conv >1 dia |
| 7d+1d view | Superestima remarketing | VTC infla |
| 28d+1d view | Superestima topo | Atribui muito tempo depois |
| 1d click (sem view) | Conservadora | Mostra impacto real |

**Regra prática:** Use janela que corresponda ao ciclo de decisão. Curto (1-2d): 1d click. Longo (7-14d): 7-28d click.

---

# Casos Práticos

## Caso 1: Clínica de Estética - CPA disparou

**Dados:**
- Setor: saúde/estética. Objetivo: lead consultoria gratuita
- Orcamento: R$200/dia. Meta CPA: <R$60

| Metrica | Dia -7 | Dia -6 | Dia -5 | Dia -4 | Dia -3 | Dia -2 | Dia -1 |
|---------|--------|--------|--------|--------|--------|--------|--------|
| Gasto | R$195 | R$202 | R$188 | R$210 | R$205 | R$198 | R$212 |
| Leads | 14 | 15 | 12 | 11 | 8 | 6 | 4 |
| CPA | R$14 | R$13 | R$16 | R$19 | R$26 | R$33 | R$53 |
| CTR | 2,1% | 2,0% | 1,8% | 1,5% | 1,1% | 0,9% | 0,7% |
| CPM | R$28 | R$27 | R$29 | R$32 | R$38 | R$42 | R$48 |
| Frequencia | 1,4 | 1,5 | 1,6 | 1,8 | 2,1 | 2,5 | 2,9 |
| Alcance | 7k | 7,4k | 6,5k | 6,6k | 5,5k | 4,7k | 4,4k |

**Análise:**

PASSO 1: Classificar -> Camada 2. CPA subiu 280% em 7 dias (R$14 -> R$53).

PASSO 2: Anomalias: CPA disparou (vermelho), CTR caiu 67% (vermelho), CPM subiu 71% (vermelho), Frequencia subiu 1,4->2,9 (vermelho), Alcance caiu 37% (vermelho).

PASSO 3: Padrão clássico de fadiga de audiência. Frequência subindo, alcance caindo, CTR caindo, CPM subindo.

PASSO 4 - Hipóteses:

**H1 (65%): Fadiga de audiência.** Público de ~7k viu o anúncio 2,9x. Quem ia se interessar já se interessou.
- A favor: Freq alta + alcance caindo + CTR caindo + CPM subindo
- Contra: Nada. Tudo aponta para fadiga.
- Teste: Trocar criativo. Se melhorar em 48h, confirmado.

**H2 (20%): Concorrência aumentou.** CPM subiu 71%.
- A favor: CPM subindo
- Contra: Concorrência não reduz CTR
- Teste: Breakdown por horário.

**H3 (10%): Quality Ranking caiu.**
- A favor: CPM alto + CTR baixo
- Contra: QR cai quando anúncio é mal recebido. Causa é fadiga.
- Teste: Verificar QR no painel.

**H4 (5%): Learning phase reiniciou.**
- Contra: Piora gradual, não abrupta.

PASSO 5 - Recomendação:

**Imediata:** Pausar criativo atual. Lançar 2-3 novos. Manter R$200/dia.

**Curto prazo (48h):** Monitorar CPA com novos criativos.

**Médio prazo (7d):** Expandir público (novos interesses). Criar lookalike de leads qualificados. Calendário de renovação a cada 5-7 dias.

**O que NÃO fazer:** Não aumentar orçamento. Não reduzir lances. Não desligar campanha.

**Critério de sucesso:** CPA <R$25 em 4 dias.
**Próximo check:** 48h.

---

## Caso 2: E-commerce de Moda - ROAS caiu mas vendas aumentaram

**Dados:**
- Setor: e-commerce moda feminina. Objetivo: conversão
- Orcamento: R$500/dia. Ticket médio: R$150

| Metrica | Semana -4 | Semana -3 | Semana -2 | Semana -1 | Esta sem |
|---------|----------|----------|----------|----------|----------|
| Gasto | R$3.500 | R$3.580 | R$5.200 | R$6.800 | R$8.400 |
| Vendas | 115 | 120 | 135 | 160 | 182 |
| ROAS | 4,9 | 5,0 | 3,9 | 3,5 | 3,2 |
| Receita | R$17.250 | R$18.000 | R$20.250 | R$24.000 | R$27.300 |
| CPA | R$30 | R$30 | R$39 | R$43 | R$46 |
| CTR | 1,1% | 1,0% | 0,9% | 0,8% | 0,7% |
| Freq | 1,6 | 1,7 | 2,1 | 2,6 | 3,1 |
| Alcance | 70k | 68k | 82k | 88k | 92k |
| CPM | R$22 | R$24 | R$26 | R$28 | R$32 |
| New cust | 45% | 44% | 52% | 58% | 62% |

**Análise:**

ROAS caiu 35% (4,9 -> 3,2) mas receita cresceu 58%. New customer subiu de 45% para 62%. Gasto quase triplicou.

ROAS caiu PORQUE gasto aumentou e nova audiência (new customers) tem taxa de conversão mais baixa. Trade-off natural de expansão.

ROAS atual 3,2 com ticket R$150. Margem bruta ~50% = R$75 por venda. CPA R$46. Margem líquida de aquisição R$29 por cliente novo. POSITIVO.

**Risco:** Frequência 3,1 em prospecção está alta. CPM subiu 45%. Se não renovar criativos, ROAS vai continuar caindo.

**Recomendação:**

**Imediata:** Renovar criativos (frequência 3,1 = fadiga iminente). Manter orçamento.

**Curto prazo:** Expandir público (2-3 novos interesses). Criar variações do criativo vencedor.

**Médio prazo:** Se ROAS estabilizar 3,0+: continuar escalando (10-15%/semana). Se cair <2,5: reduzir 15%. Monitorar new customer ratio como KPI primário.

**O que NÃO fazer:** Não reduzir orçamento porque ROAS caiu (receita cresceu). Não voltar ao gasto anterior (deixava dinheiro na mesa). Não ignorar frequência.

---

## Caso 3: Escola de Idiomas - leads chegam mas não agendam

**Dados:**
- Setor: educação (escola de idiomas). Objetivo: lead para aula experimental
- Orcamento: R$150/dia. Período: 30 dias

| Metrica | Valor |
|---------|-------|
| Gasto total | R$4.500 |
| Leads totais | 320 |
| CPA lead | R$14 |
| Leads que agendaram | 48 (15%) |
| Compareceram | 28 (58% dos agendados) |
| Matriculas | 11 |
| CPA matricula | R$409 |
| CPM | R$18 |
| CTR | 1,9% |
| Audience Network | ATIVADO |

**Análise:**

CPA lead R$14 parece ótimo. CPA matrícula R$409 = 29x mais caro. Gap enorme.

Hipóteses:

**H1 (70%): Audience Network gerando leads de baixíssima qualidade.** CPM R$18 e CTR 1,9% compatível com AN dominando entrega. Taxa de agendamento 15% confirma: leads sem intenção real.
- Teste: Desligar AN por 7 dias. CPA lead vai subir, mas taxa de agendamento deve melhorar.

**H2 (15%): Formulário muito aberto** (automático do Meta). Leads com atrito mínimo = menos qualificados.

**H3 (10%): Processo de agendamento quebrado.** 48 agendaram de 320 = 15%. Se lead qualificado mas não agenda, follow-up falhou.

**H4 (5%): Público errado.** Interesses genéricos demais.

**Recomendação:**

**Imediata:** Desligar AN. Adicionar pergunta de qualificação no formulário. Revisar copy.

**Curto prazo:** Reduzir orçamento para R$120/dia (AN desligado reduz entrega). Verificar follow-up (ligação em <1h).

**Médio prazo:** Se taxa de agendamento subir para 30%+, CPA lead de R$25-30 vira CPA agendamento de R$90 — aceitável.

**O que NÃO fazer:** Não aumentar orçamento (mais leads ruins). Não pausar campanha. Não ignorar discrepância.

---

## Caso 4: SaaS B2B - CTR alto, CPC baixo, zero conversões

**Dados:**
- Setor: SaaS B2B (gestão empresarial). Objetivo: lead para demonstração
- Orcamento: R$300/dia. Período: 14 dias

| Metrica | Valor |
|---------|-------|
| Gasto total | R$4.200 |
| Cliques | 1.200 |
| CTR | 2,8% |
| CPC | R$3,50 |
| CPM | R$22 |
| Frequencia | 1,3 |
| Alcance | 46k |
| Conversoes | 0 |
| Quality Ranking | Average |
| Engagement R. | Above Average |
| Conversion R. | N/A |
| Placements | Feed 40%, AN 35%, Stories 25% |

**Análise:**

CTR 2,8% para SaaS B2B é MUITO ALTO (média 0,4-0,9%). SINAL VERMELHO disfarçado de verde.
CPM R$22 é MUITO BAIXO para SaaS (média R$35-60).
Audience Network 35% dos placements = PROBLEMA GRAVE.

CTR alto + CPC baixo + CPM baixo + AN dominando = padrão clássico de cliques de baixíssima qualidade. Pessoas clicam acidentalmente ou por curiosidade, bounce imediato. Para SaaS B2B (produto complexo, ticket alto), esses placements são TÓXICOS.

**H1 (80%): Audience Network + Stories gerando tráfego de baixa qualidade.** 1.200 cliques de AN e Stories não representam intenção de compra. Zero conversões em 14 dias comprova.

**H2 (15%): Página de destino não comunica valor.**
- Contra: CTR 2,8% sugere que o criativo atrai cliques, mas se fossem leads reais, ao menos 1-2% teriam convertido.

**H3 (5%): Pixel/CAPI quebrado.**
- Teste: Verificar Events Manager.

**Recomendação:**

**Imediata:** Desligar Audience Network e Stories. Manter apenas Feed.

**Curto prazo:** Após desligar AN, CTR vai cair para 0,4-0,8% (normal). CPM vai subir para R$35-50 (normal). CPA lead deve ficar em R$40-80.

**O que NÃO fazer:** Não pausar campanha (Feed funciona). Não aumentar orçamento. Não trocar criativo antes de ver resultado sem AN.

---

## Caso 5: Loja de Suplementos - Feed bom, Audience Network drena

**Dados:**
- Setor: e-commerce suplementos. Objetivo: conversão
- Orcamento: R$400/dia. Período: 7 dias

| Metrica | Geral | Feed | Stories | Reels | Audience Network |
|---------|-------|------|---------|-------|------------------|
| Gasto | R$2.800 | R$1.120 | R$560 | R$280 | R$840 |
| % gasto | 100% | 40% | 20% | 10% | 30% |
| Vendas | 52 | 38 | 8 | 4 | 2 |
| ROAS | 3,5 | 5,8 | 2,4 | 2,0 | 0,5 |
| CPA | R$54 | R$29 | R$70 | R$70 | R$420 |
| CTR | 1,2% | 1,8% | 0,9% | 0,4% | 0,2% |
| CPM | R$24 | R$32 | R$18 | R$14 | R$10 |

**Análise:**

Audience Network consome 30% do orçamento (R$840/semana) e gera ROAS 0,5 com CPA R$420. Feed tem ROAS 5,8 com CPA R$29.

Se AN fosse desligado e os R$840 realocados proporcionalmente:
- Gasto Feed adicional: R$840 x (40/70) = R$480
- Gasto Stories adicional: R$840 x (20/70) = R$240
- Gasto Reels adicional: R$840 x (10/70) = R$120
- Vendas adicionais estimadas: (480/29) + (240/70) + (120/70) ~ 16,5 + 3,4 + 1,7 ~ 22 vendas
- Gasto mantido: R$2.800 -> Vendas estimadas sem AN: 74
- ROAS estimado sem AN: (74 x ticket) / R$2.800 = ~4,8 vs 3,5 atual

Ou seja: desligar AN melhora ROAS em ~37% com mesmo gasto total.

**Recomendação:**

**Imediata:** Desligar Audience Network desta campanha.

**Curto prazo:** Realocar orçamento para Feed (60%) e Stories (30%) e Reels (10%).

**Médio prazo:** Testar AN novamente com criativos específicos para o formato (se quiser explorar o CPM baixo). Mas apenas com orçamento separado (5-10% do total).

**O que NÃO fazer:** Não manter AN "só porque o CPM é barato". Não aumentar orçamento geral (primeiro otimizar, depois escalar).

---

# Cadências e Rotinas de Análise

## A cada 24h (check diário)

**O que olhar:**
- Gasto vs orçamento diário
- CPA vs meta (apenas se >50 conv no período)
- ROAS (apenas campanhas pós-learning phase)
- Anomalias >30% em qualquer métrica principal
- Alertas do Meta (anúncio reprovado, learning limited, payment issue)

**O que NÃO fazer:**
- Não pausar anúncio baseado em 1 dia de dado (exceto se for erro óbvio)
- Não trocar criativo com <48h de dados
- Não alterar orçamento em mais de 20%
- Não tomar decisão baseada em <50 conversões

## A cada 48h (check tático)

**O que olhar:**
- Tendência de 2 dias das métricas principais
- Frequência (se subiu >0,5 desde o check anterior, investigar)
- Breakdown por placement (distribuição mudou?)
- CPM trend (estável ou subindo?)
- CTR trend (caindo? fadiga começando?)
- Quality Ranking (se disponível)

**O que NÃO fazer:**
- Não duplicar conjuntos de anúncios
- Não pausar sem ver breakdown primeiro
- Não tomar decisão de escala

## Semanal (check estratégico)

**O que olhar:**
- ROAS, CPA, CTR, CPM, frequência consolidados da semana
- ROAS por criativo (qual ganhou, qual perdeu)
- ROAS por público (remarketing vs prospecção)
- New vs returning customer ratio
- Custo por lead qualificado vs lead bruto
- Frequency distribution
- Alcance (estagnou ou crescendo?)
- Gasto semanal vs orçamento semanal

**Decisões:**
- Rolar criativos: pausar os piores, escalar os melhores
- Expandir/contrair públicos baseado em saturação
- Ajustar orçamentos para a próxima semana
- Planejar testes (novos criativos, novos públicos)

**O que NÃO fazer:**
- Não mudar estratégia toda baseada em 1 semana boa/ruim
- Não pausar tudo de uma vez (ter um herói é ok, mas diversificar)
- Não ignorar new customer ratio (ROAS bonito com base encolhendo é problema futuro)

## Quinzenal (check de atribuição)

**O que olhar:**
- Attribution window comparison (1d vs 7d vs 28d)
- Time lag distribution
- View-through ratio
- CAPI vs Pixel match rate
- Assisted conversions

**Decisões:**
- Ajustar janela de atribuição se time lag está fora
- Verificar integridade do CAPI/pixel
- Calibrar confiança nas métricas

**O que NÃO fazer:**
- Não mudar janela de atribuição sem entender o impacto
- Não ignorar discrepâncias de match rate
- Não fazer isso mais que uma vez por mês (atribuição não muda tanto)

## Mensal (check de negócio)

**O que olhar:**
- ROAS real vs ROAS reportado (via CRM)
- Incrementality (se disponível)
- DDA vs Last-click comparison
- LTV:CAC ratio
- Funil completo: de impressão a venda, cada etapa
- Share de budget por campanha (está alocado onde gera mais retorno?)
- Benchmark vs meses anteriores

**Decisões:**
- Revisão de estratégia (o que funcionou no mês)
- Planejamento do próximo mês
- Ajuste de metas de CPA/ROAS baseado em dados reais (não achismo)
- Decisão de manter/pausar/criar campanhas

**O que NÃO fazer:**
- Não tomar decisão operacional com dados mensais (muito atrasados)
- Não ignorar o LTV (o ROAS de 1 mês não conta a história toda)
- Não comparar meses diferentes sem ajuste sazonal

---

# Regras de Ouro (resumo executivo para o LLM)

1. **Dados primeiro.** Antes de qualquer hipótese, verifique se o dado está correto. Pixel quebrado, CAPI desalinhado, janela errada — essas são as causas mais comuns de "problemas" que não existem.

2. **Volume é rei.** Menos de 50 conversões no período? Qualquer métrica é instável. Não tome decisões baseadas em amostras pequenas. Espere ou agrupe períodos.

3. **Contexto é tudo.** CPA de R$50 é caro para educação (média R$12-25) mas barato para saúde (média R$35-65). Nunca avalie métrica fora do contexto do setor, fase da campanha e objetivo.

4. **Não pule camadas.** Sempre comece pela Camada 1. Se ela explica, pare. Vá para Camada 2 apenas se precisar. Camada 3 é para quando as outras não explicam. A maioria dos erros vem de pular para investigação profunda quando o diagnóstico tático já resolveria.

5. **Frequência é alarme, não diagnóstico.** Frequência alta raramente é a causa raiz — é o sintoma de que o público é pequeno, o criativo cansou, ou o orçamento é alto demais. Trate a causa, não o sintoma.

6. **View-through conversion não é conversão.** É influência. Desconte 70-90% do valor atribuído a VTC antes de tomar decisão. Especialmente em remarketing.

7. **Placement é o breakdown mais importante.** Sempre que uma métrica agregada estiver estranha, o primeiro lugar para olhar é a distribuição por placement. Audience Network é a maior fonte de distorção em contas Meta Ads.

8. **Trade-off volume vs eficiência é real.** CPA vai subir quando você escala. New customers convertem menos que recorrentes. Isso não é erro — é lei dos retornos decrescentes. O importante é saber se o trade-off vale a pena (LTV vs CAC).

9. **Meta e GA4 nunca vão bater.** 20-50% de diferença é normal. Meta sempre reporta mais. Use GA4 para tendência, Meta para operação, CRM para verdade. Nunca entre na loucura de tentar fazer os números baterem.

10. **Seu palpite vale menos que os dados.** Não pause um anúncio porque "acha" que está ruim. Olhe os números por 7 dias, com breakdown, comparando com a meta. A maior parte das "otimizações" que gestores fazem na base do feeling pioram a performance.

---

# Sobre esta Skill

Esta skill foi projetada para ser o framework analítico mais completo possível para Meta Ads. Ela incorpora:

- Mais de 20 anos de experiência consolidada de gestão de tráfego
- Rigor técnico sobre como cada métrica funciona (não apenas o que significa)
- Hierarquia de decisão baseada em probabilidade e precedência
- Casos reais com números realistas
- Armadilhas comuns que gestores experientes conhecem (mas nem sempre lembram)

Use esta skill sempre que precisar analisar performance de Meta Ads — desde o check diário até a investigação forense mais profunda. Lembre-se: métrica sem contexto é ruído. Contexto sem métrica é achismo. Os dois juntos são análise.

---

# Seções Expandidas — Diagnóstico Avançado

## Integração com CRM e Dados Offline

Uma das habilidades mais subestimadas na análise de Meta Ads é conectar os dados da plataforma com o CRM. Sem isso, você otimiza para métricas de plataforma, não para resultado de negócio.

### O Pipeline Completo de Dados

```
Meta Ads -> Pixel/CAPI -> Events Manager -> Meta Otimizacao
                                            |
                                            v
Meta Ads -> CAPI (eventos personalizados) -> CRM -> Funil de Vendas
                                                     |
                                                     v
                                              Resultado Real (LTV)
```

**O problema:** A Meta otimiza para o que ela ENXERGA. Se ela não enxerga o lead qualificado vs o lead frio, ela vai otimizar para maximizar leads (inclusive os frios).

**A solução:** Alimentar a Meta com dados de qualidade via CAPI:
- Evento `Lead` quando alguém preenche o formulário
- Evento `Lead Qualificado` quando o lead passa do BANT (ou critério similar)
- Evento `Purchase` quando a venda é fechada
- Evento `Purchase` com valor real (não estimado)

**Métrica híbrida essencial: CPA por estágio do funil**

Crie no CRM:
- CPA Lead Bruto = gasto Meta / total leads
- CPA Lead Qualificado = gasto Meta / leads que passaram do critério mínimo
- CPA Oportunidade = gasto Meta / leads que viraram oportunidade
- CPA Venda = gasto Meta / vendas fechadas
- ROAS Real = receita total / gasto Meta

**Exemplo concreto da diferença:**

| Estágio | Quantidade | Custo | CPA |
|---------|-----------|-------|-----|
| Lead bruto | 500 | R$10.000 | R$20 |
| Lead qualif | 120 | R$10.000 | R$83 |
| Oportunidade | 40 | R$10.000 | R$250 |
| Venda | 15 | R$10.000 | R$667 |
| Ticket médio | R$400 | — | — |
| ROAS | — | — | 0,6 |

O CPA lead de R$20 parece ótimo. O ROAS real de 0,6 mostra que a conta está QUEIMANDO dinheiro. Sem integração CRM, você nunca saberia disso.

### Implementação Recomendada

1. **CAPI com eventos padrão + personalizados:** Enviar `Lead`, `Lead Qualificado` (personalizado), `Purchase` com valor real
2. **Match entre leads e vendas:** Usar ID único do lead para conectar o clique ao fechamento
3. **Feedbacks semanais:** Revisar a taxa de conversão lead->venda por campanha/público/criativo
4. **Atribuição offline:** Considerar que a venda pode levar 30-90 dias para acontecer (especialmente B2B e serviços)

## O Ciclo de Vida do Criativo

### Fases do Criativo no Meta Ads

```
Fase 1: Learning (dias 1-3)
  - Meta está aprendendo quem converte
  - CPA instável (pode ser 2-3x maior que o esperado)
  - CTR instável
  - NÃO OTIMIZAR baseado em dados desta fase

Fase 2: Maturação (dias 4-10)
  - CPA começa a estabilizar
  - CTR tende a cair levemente (alcance se expandindo)
  - Meta já identificou o público que converte
  - MELHOR MOMENTO PARA AVALIAR PERFORMANCE REAL

Fase 3: Pico (dias 11-20)
  - Melhor performance (se criativo for bom)
  - CPA no ponto mais baixo
  - CTR começa a declinar (frequência subindo)
  - MOMENTO PARA PLANEJAR RENOVAÇÃO

Fase 4: Declínio (dias 21-35)
  - CPA começa a subir
  - Frequência > 3,0
  - CTR caiu 30%+ em relação ao pico
  - Alcance estagnou
  - RENOVAR CRIATIVO ou EXPANDIR PÚBLICO

Fase 5: Fadiga (dias 36+)
  - CPA > 2x o pico
  - CTR < 50% do pico
  - Frequência > 5,0
  - Quality Ranking caiu para Below Average
  - PAUSAR ou RENOVAR IMEDIATAMENTE
```

**Tabela de referência por setor (ciclo médio de vida do criativo):**

| Setor | Learning | Maturação | Pico | Declínio | Fadiga | Ciclo total |
|-------|----------|-----------|------|----------|--------|-------------|
| E-commerce moda | 3d | 7d | 10d | 10d | 7d | ~37d |
| E-commerce geral | 3d | 5d | 8d | 10d | 7d | ~33d |
| Educação | 2d | 5d | 7d | 7d | 5d | ~26d |
| Saúde/Estética | 3d | 7d | 10d | 14d | 10d | ~44d |
| SaaS B2B | 5d | 10d | 15d | 15d | 10d | ~55d |
| Imóveis | 3d | 7d | 14d | 14d | 10d | ~48d |

**Estratégia de renovação:**

Não espere o criativo morrer. Tenha sempre 2-3 criativos em fase de maturação enquanto o herói está no pico. Quando o herói entrar em declínio, você já tem substitutos prontos.

- **Rotação preventiva:** Trocar 20-30% dos criativos a cada 7-10 dias
- **Teste A/B contínuo:** Manter 10-20% do orçamento em testes de novos criativos
- **Arquivo de criativos:** Manter um registro do que funcionou (formato, ângulo, CTA, cor) para referência futura

## Análise de Concorrência no Leilão Meta

A Meta não te mostra quem são seus concorrentes no leilão, mas você pode inferir:

**Sinais de aumento de concorrência:**
- CPM subiu sem mudança de público/criativo/orçamento
- CPC subiu (CPM + CTR estável = mais concorrentes)
- Alcance caiu sem redução de orçamento
- Quality Ranking manteve mas CPM subiu (mercado mais disputado)

**Sinais de redução de concorrência:**
- CPM caiu sem mudança sua
- Alcance aumentou sem aumento de orçamento
- CTR manteve mas CPM caiu (oportunidade de escala)

**Como reagir a picos de concorrência:**
1. Não aumentar lances (você vai pagar mais caro pelo mesmo público)
2. Verificar se é sazonal (Black Friday, etc) — se for, planejar com antecedência
3. Se for concorrência permanente (concorrente entrou no mercado): diversificar públicos, investir em criativos melhores, ou aceitar CPM mais alto
4. Reduzir orçamento nas horas de pico de concorrência e realocar para horários menos disputados

## O Impacto da Sazonalidade nas Métricas

### Calendário de Sazonalidade Meta Ads (Brasil)

| Período | Impacto CPM | Impacto CPA | Duração | Ação recomendada |
|---------|-------------|-------------|---------|------------------|
| Janeiro (volta às aulas) | +10-20% | +10-20% | 4 semanas | Planejar orçamento maior para educação |
| Carnaval | +5-15% | +10-25% | 1 semana | Reduzir prospecção, manter remarketing |
| Março/Abril | Normal | Normal | — | Boa janela para testes |
| Maio (Dia das Mães) | +20-40% | +15-30% | 3 semanas | E-commerce: aumentar orçamento 30-50% |
| Junho (Festas Juninas) | +5-10% | +5-15% | 2 semanas | Sazonalidade regional (Nordeste sobe mais) |
| Julho (férias) | -5 a +5% | Varia | 4 semanas | Educação: alta. B2B: queda |
| Agosto (Dia dos Pais) | +15-25% | +10-20% | 2 semanas | Similar Dia das Mães (menor intensidade) |
| Setembro | Normal | Normal | — | Boa janela para testes |
| Outubro | Normal | Normal | — | Preparar Black Friday |
| Novembro (Black Friday) | +50-100% | +30-60% | 4 semanas | Aumentar orçamento 2-3x. Aceitar CPM maior |
| Dezembro (Natal) | +30-60% | +20-40% | 4 semanas | Última semana: conversões caem (compradores já compraram) |

**Estratégia geral de sazonalidade:**
- Planejar aumento de orçamento 2-4 semanas ANTES do pico (para acumular audiência)
- Aceitar que CPM/CPA vão subir — o volume de conversões compensa
- Não comparar períodos sazonais com períodos normais como se fossem equivalentes
- Usar comparação ano-a-ano (YoY) em vez de comparação mês-a-mês (MoM) em períodos sazonais

## Otimização por Horário (Dayparting)

Meta não tem dayparting nativo como Google Ads, mas você pode inferir:

**Padrão geral de performance por horário:**

| Horário | CPM | CTR | CPA | Volume |
|---------|-----|-----|-----|--------|
| 6h-9h | Médio | Alto | Baixo | Médio |
| 9h-12h | Alto | Médio | Médio | Alto |
| 12h-14h | Médio | Alto | Médio | Alto |
| 14h-18h | Alto | Baixo | Alto | Médio |
| 18h-22h | Mais alto | Médio | Médio | Médio-alto |
| 22h-6h | Baixo | Baixo | Variável | Baixo |

**Como usar:**
- Se CPA está alto no período da tarde: reduzir orçamento ou lances nesse horário
- Se CPA está baixo de manhã: aumentar orçamento pela manhã
- Anúncios de resposta emocional (moda, beleza): melhor performance à noite/fim de semana
- Anúncios de decisão racional (B2B, educação): melhor performance durante a semana, horário comercial

**Limitação:** Dayparting no Meta requer criar múltiplos conjuntos de anúncios com schedules diferentes. Isso fragmenta o aprendizado. Usar apenas em contas com orçamento grande (>R$1.000/dia).

## Análise de Sobreposição de Públicos

A sobreposição de públicos é um problema silencioso que drena performance.

**Por que é problema:**
- Múltiplos conjuntos disputando as mesmas pessoas
- Frequência artificialmente alta
- CPM mais alto (competição interna no leilão)
- Dados de conversão compartilhados entre conjuntos (diluição do aprendizado)

**Quando suspeitar:**
- Frequência total da conta maior que a soma das frequências individuais
- CPA subindo em todos os conjuntos simultaneamente
- Vários conjuntos com entrega caindo ao mesmo tempo

**Como diagnosticar:**
Usar a ferramenta Audience Overlap do Meta (Audiences > Actions > Show Audience Overlap).
Sobreposição >30% entre públicos = PROBLEMA.

**Como resolver:**
1. Combinar públicos sobrepostos em um único conjunto
2. Usar exclusões para separar públicos que não devem competir
3. Estruturar campanhas por jornada (topo, meio, fundo) em vez de por interesse
4. Usar regra de orçamento em nível de campanha (não de conjunto) para evitar competição

## Estrutura de Conta Recomendada

### Arquitetura para Contas de Lead Gen

```
Campanha 1: Prospecção (orçamento: 50-60%)
  - Conjunto A: Lookalike 1% (melhores leads)
  - Conjunto B: Lookalike 3% (bons leads)
  - Conjunto C: Interesses (escala)
  
Campanha 2: Remarketing (orçamento: 20-30%)
  - Conjunto A: Visitantes site 7d
  - Conjunto B: Leads não convertidos 30d
  - Conjunto C: Engajamento página 90d

Campanha 3: Testes (orçamento: 10-20%)
  - Criativos novos, públicos novos, formatos novos
```

### Arquitetura para Contas de E-commerce

```
Campanha 1: Prospecção Geral (orçamento: 40%)
  - Conjunto A: Lookalike compradores 1-3%
  - Conjunto B: Interesses (categoria)
  
Campanha 2: Prospecção por Categoria (orçamento: 20%)
  - Separar por linha de produto (moda feminina, moda masculina, etc.)

Campanha 3: Remarketing (orçamento: 25%)
  - Conjunto A: Visitantes 7d (carrinho abandonado)
  - Conjunto B: Visitantes 14d (navegou mas não comprou)
  - Conjunto C: Compradores anteriores (cross-sell)

Campanha 4: Testes (orçamento: 15%)
  - Novos produtos, novos ângulos, novos formatos
```

### Arquitetura para Contas de SaaS B2B

```
Campanha 1: Topo de Funil (orçamento: 40%)
  - Conteúdo, ebook, webinar
  - Público: interesses amplos + lookalike visitantes
  
Campanha 2: Meio de Funil (orçamento: 30%)
  - Demonstração, trial, case study
  - Público: visitantes do site + leads não convertidos

Campanha 3: Remarketing (orçamento: 20%)
  - Trial não ativado, lead não respondeu
  - Oferta especial, consultoria gratuita

Campanha 4: Testes (orçamento: 10%)
```

## Análise de Break-even e Definição de Metas

### Calculando o CPA Máximo Aceitável

```
CPA Máximo = (Ticket Médio x Margem Bruta) / ROAS Mínimo Aceitável

Exemplo:
- Ticket médio: R$150
- Margem bruta: 40%
- Lucro bruto por venda: R$60
- ROAS mínimo aceitável (break-even): 1,0 / 0,4 = 2,5
- CPA máximo: R$150 x 0,4 = R$60 (se ROAS = 2,5)
- CPA ideal (ROAS 5,0): R$150 x 0,4 / 5,0 = R$12
```

### Calculando o ROAS Mínimo (Break-even)

```
ROAS Mínimo = 1 / Margem Bruta

Se margem bruta = 30%: ROAS mínimo = 1 / 0,3 = 3,33
Se margem bruta = 50%: ROAS mínimo = 1 / 0,5 = 2,0
Se margem bruta = 70%: ROAS mínimo = 1 / 0,7 = 1,43
```

### Matriz de Decisão LTV:CAC

| LTV:CAC | Situação | Ação |
|---------|----------|------|
| <1:1 | Queimando dinheiro | Repensar modelo ou pausar investimento |
| 1:1 a 3:1 | Sub-ótimo | Otimizar ou reduzir CAC |
| 3:1 a 5:1 | Saudável | Manter e escalar gradualmente |
| 5:1 a 10:1 | Excelente | Escalar agressivamente |
| >10:1 | Sub-investindo | Aumentar orçamento (tem demanda não capturada) |

**Atenção:** LTV precisa ser calculado com janela correta (não apenas 30 dias). Para SaaS, usar LTV de 12-24 meses. Para e-commerce, 6-12 meses.

## Análise de Margem por Campanha

Nem toda venda é igual. Campanhas podem ter margens diferentes:

| Produto | Ticket | Margem | ROAS mínimo | CPA máximo |
|---------|--------|--------|-------------|------------|
| Produto A (alto valor) | R$500 | 50% | 2,0 | R$250 |
| Produto B (baixo valor) | R$100 | 20% | 5,0 | R$20 |
| Produto C (serviço) | R$1.000 | 80% | 1,25 | R$800 |

Se você otimiza para ROAS geral sem separar por produto, pode estar matando a campanha do produto C (que tem ROAS 2,0 mas margem ótima) e super-investindo no produto B (que tem ROAS 4,0 mas margem baixa e pouco impacto no lucro).

**Solução:** Sempre que possível, separar campanhas por faixa de margem de produto e definir metas de ROAS específicas para cada uma.

## Alertas e Gatilhos Automáticos

### Gatilhos para Pausar Imediatamente

- Gasto > R$500 sem nenhuma conversão (em campanha de conversão)
- Quality Ranking = Below Average por 3+ dias consecutivos
- Frequência > 5,0 com CPA > 2x a meta
- Criativo com feedback negativo >10% (esconder anúncio)
- CPM dobrou em 24h sem mudança de configuração

### Gatilhos para Revisão (não pausar, mas investigar)

- CPA subiu >30% em 48h
- CTR caiu >30% em 5 dias
- Frequência > 3,0 em prospecção
- Gasto <50% do orçamento por 3+ dias
- ROAS caiu >20% na semana (com volume mantido)
- New customer ratio caiu >15% em 2 semanas

### Gatilhos para Escalar

- CPA estável <80% da meta por 5+ dias consecutivos
- Frequência < 1,8 com orçamento sendo 100% executado
- ROAS > meta em 20%+ com volume consistente
- Alcance ainda <30% do público disponível
- Quality Ranking Above Average consistente

## Tabelas de Referência Rápida

### Resumo de Sinais por Métrica

| Métrica | Sinal Verde | Sinal Amarelo | Sinal Vermelho |
|---------|-------------|---------------|----------------|
| CTR | Na média do setor | 15-30% abaixo | 40%+ abaixo ou <0,3% |
| CPM | Na média do setor | 20-35% acima | 50%+ acima ou dobrou em 48h |
| CPC | Na média do setor | 25-40% acima | 60%+ acima |
| Frequência | <2,0 (prospecção) | 2,0-3,0 | >3,0 (prospecção) ou >5,0 (remkt) |
| CPA | Na meta | 20-30% acima | 50%+ acima |
| ROAS | Acima do break-even | 15-25% abaixo | 40%+ abaixo |
| Gasto | 90-110% do orçamento | 50-70% do orçamento | <50% do orçamento |
| QR | Above Average | Average | Below Average |

### Checklist de Verificação Diária

- [ ] Gasto vs orçamento: dentro do esperado?
- [ ] CPA vs meta: dentro ou fora?
- [ ] ROAS: estável ou caindo?
- [ ] Frequência: subiu >0,5 em 24h?
- [ ] CTR: queda abrupta?
- [ ] CPM: subiu >20% em 24h?
- [ ] Alcance: crescendo ou estagnou?
- [ ] Anúncios reprovados ou em revisão?
- [ ] Learning phase: alguma campanha presa?
- [ ] Gasto da conta: dentro do limite?

### Checklist de Verificação Semanal

- [ ] ROAS por criativo: qual ganhou, qual perdeu
- [ ] ROAS por público: remarketing vs prospecção
- [ ] New vs returning customer ratio
- [ ] Custo por lead qualificado vs lead bruto
- [ ] Frequency distribution
- [ ] Breakdown por placement
- [ ] Top 5 criativos: estão envelhecendo?
- [ ] Orçamento: precisa realocar?
- [ ] Testes: novos criativos lançados?
- [ ] Meta vs CRM: discrepância aumentou?

## Referências de Benchmark Avançadas

### Por Faixa de Orçamento

| Orçamento/dia | Volatilidade | Confiança nas métricas | Estratégia |
|---------------|-------------|----------------------|------------|
| <R$100 | Muito alta | Baixa | Aceitar instabilidade. Otimizar por semana, não por dia |
| R$100-500 | Alta | Média | Otimizar a cada 3-5 dias. Learning phase mais longa |
| R$500-2.000 | Média | Alta | Otimização diária possível. Testes viáveis |
| R$2.000-10.000 | Baixa | Muito alta | Escala e diversificação. Testes A/B contínuos |
| >R$10.000 | Muito baixa | Altíssima | Estratégia avançada. Segmentação granular. Múltiplos funis |

### Por Estágio da Conta

| Estágio | Idade | Foco | Métrica principal |
|---------|-------|------|-------------------|
| Cold start | 0-14d | Sair da learning phase | Conversões totais |
| Crescimento | 14-60d | Escalar com CPA controlado | Volume + CPA |
| Maturação | 60-180d | Maximizar ROAS | ROAS + New customer ratio |
| Otimização | 180d+ | Eficiência + renovação | ROAS + LTV:CAC |
| Reinvenção | 1 ano+ | Testar novas abordagens | Testes incrementais |

## Erros Comuns em Análise de Meta Ads

### Os 15 Erros Mais Frequentes

1. **Olhar CPA de 1 dia como se fosse tendência.** CPA de segunda não é igual a CPA de domingo. Sempre use média de 7 dias.

2. **Pausar baseado em learning phase.** Toda campanha nova tem CPA alto nos primeiros dias. Espere 50 conversões.

3. **Ignorar o placement.** A métrica geral pode esconder que Audience Network está destruindo a performance.

4. **Comparar ROAS de prospecting com remarketing.** São realidades diferentes. Remarketing sempre tem ROAS mais alto.

5. **Não separar view-through de click-through.** ROAS de 4,0 pode ser 2,0 real quando você tira a VTC.

6. **Otimizar para CTR em vez de CPA.** CTR alta não paga as contas. CPA baixo sim.

7. **Mudar janela de atribuição para "consertar" os números.** Você está mentindo para si mesmo.

8. **Aumentar orçamento em campanha com frequência alta.** Vai saturar mais rápido.

9. **Não usar breakdown por idade/gênero.** Pode estar gastando 70% em uma faixa que não converte.

10. **Confiar cegamente no ROAS do painel.** Sem integração CRM, você não sabe o ROAS real.

11. **Ignorar o CAPI.** Sem CAPI, você perde 30-50% dos dados de conversão.

12. **Não verificar o time lag.** Sua janela de atribuição de 7 dias pode estar perdendo metade das conversões.

13. **Pausar criativo com CPA alto sem verificar o volume.** 2 conversões com CPA alto não é nada. 200 conversões com CPA alto é um padrão.

14. **Fazer alterações demais ao mesmo tempo.** Mudou criativo + público + orçamento + lance no mesmo dia? Você não sabe o que funcionou.

15. **Não documentar nada.** As decisões de hoje são o aprendizado de amanhã. Sem registro, você repete os mesmos erros.

## Guia de Referência para o LLM

### Como Estruturar uma Resposta de Análise

Quando o usuário pedir análise de dados Meta Ads, o LLM DEVE seguir esta estrutura:

```
## Resumo Executivo
[2-3 linhas sobre a situação principal]

## Dados Recebidos
[Tabela com métricas fornecidas ou inferidas]

## Classificação do Cenário
[Camada 1, 2 ou 3 + justificativa]

## Métricas Analisadas (por camada)

### Camada 1 — Operação Diária
| Métrica | Valor | Faixa esperada | Status |
|---------|-------|---------------|--------|

### Camada 2 — Diagnóstico Tático (se aplicável)
| Métrica | Valor | Interpretação |
|---------|-------|---------------|

### Camada 3 — Investigação (se aplicável)
| Métrica | Valor | Interpretação |
|---------|-------|---------------|

## Hipóteses (ordenadas por probabilidade)

1. [Hipótese mais provável] — [probabilidade]
   - Evidências: ...
   - Teste: ...

2. [Segunda hipótese] — [probabilidade]
   - Evidências: ...
   - Teste: ...

## Recomendações

### Ação Imediata
[lisa de ações para agora]

### Ação Curto Prazo (48-72h)
[lisa de ações]

### Ação Médio Prazo (1 semana)
[lisa de ações]

### O que NÃO fazer
[lisa]

## Critérios de Sucesso
[Como saber se a ação funcionou]

## Próximo Check
[Quando reavaliar]
```

### Prompt Template para o LLM

Quando receber dados do usuário, o LLM deve processar mentalmente:

1. Quais métricas foram fornecidas vs quais estão faltando?
2. Qual o setor do negócio? (se não informado, perguntar)
3. Qual a meta de CPA/ROAS? (se não informada, perguntar)
4. Qual a fase da campanha? (learning phase vs madura)
5. Qual a janela de atribuição configurada?
6. CAPI implementado? Pixel apenas? Híbrido?
7. Qual o funil de conversão? (lead, venda, cadastro?)

Com essas respostas, classificar o cenário e aplicar a Pirâmide de Decisão.

### Regras de Formatação de Resposta

- Usar tabelas markdown para comparar métricas
- Destacar valores anômalos em **negrito** ou com marcadores visuais
- Incluir valores numéricos específicos (R$, %, valores absolutos)
- SEMPRE incluir o que NÃO fazer (tão importante quanto o que fazer)
- Ordenar hipóteses por probabilidade (não por ordem de descoberta)
- Recomendar ações testáveis com critério de sucesso claro

## Exemplo de Análise Rápida (Template)

**Cenário:** Usuário diz "CPA subiu de R$30 para R$60 nos últimos 3 dias. E-commerce de moda. Orçamento R$300/dia."

**Resposta do LLM (formato rápido):**

```
## Resumo Executivo
CPA dobrou nos últimos 3 dias. Diagnóstico preliminar aponta para possível fadiga de audiência ou aumento de concorrência sazonal.

## Classificação
Camada 2 — variação >50% na métrica principal (CPA). Investigação tática necessária.

## Métricas Faltantes (precisamos para diagnóstico completo)
- CTR, CPM, Frequência, Alcance, Volume de conversões
- Quality Ranking
- Breakdown por placement

## Hipóteses Preliminares (com base nos dados limitados)

1. (40%) Fadiga de audiência — frequência provavelmente >3,0
2. (30%) Concorrência sazonal — verificar se há evento sazonal
3. (20%) Problema de entrega — learning phase ou público saturado
4. (10%) Conversões caíram — não é CPA que subiu, é volume que caiu

## Para confirmar, preciso de:
- CTR, CPM, Frequência, Alcance atuais e de 7 dias atrás
- Quality Ranking
- Breakdown por placement
- Número de conversões (caiu junto?)
```

## Notas Finais de Implementação

Esta skill foi projetada para ser carregada integralmente no contexto do LLM sempre que o assunto for análise de Meta Ads. O conteúdo é denso propositalmente — cada seção contém informação acionável que o LLM deve aplicar na análise.

**O LLM DEVE:**
- Usar as tabelas de normalidade para contextualizar os dados recebidos
- Aplicar a Pirâmide de Decisão para classificar o cenário
- Seguir o Protocolo de Leitura de Cenários passo a passo
- Usar as Árvores de Decisão como guia de diagnóstico
- Gerar recomendações no formato estruturado

**O LLM NÃO DEVE:**
- Alucinar métricas que não foram fornecidas
- Ignorar o setor do negócio (cada setor tem normalidades diferentes)
- Recomendar ações sem fundamentação
- Pular da Camada 1 para a 3 sem passar pela 2
- Tratar view-through como conversão real
- Confiar cegamente em dados com <50 eventos

---

## Integração com Outras Skills do Hub

Esta skill se integra com:

- **gt-relatorios-trafego:** Consome os dados estruturados de Meta Ads para análise contextual
- **v4mos-dados-meta-ads:** Puxa dados via API V4mos para alimentar a análise
- **gt-gestor-de-trafego-completo:** Complementa com visão estratégica de mídia paga multicanal
- **contexto:** Puxa configuração do cliente (metas, setor, histórico) para personalizar thresholds

Quando usada em conjunto com **v4mos-dados-meta-ads**, a skill recebe dados brutos da API e aplica toda a camada de interpretação. Quando usada com **gt-relatorios-trafego**, ela fornece a inteligência analítica por trás dos relatórios gerados.

---

# Apêndice: Glossário Rápido

| Termo | Definição |
|-------|-----------|
| CPM | Custo por 1.000 impressões |
| CPC | Custo por clique |
| CTR | Taxa de cliques (link) |
| CPA | Custo por aquisição/ação |
| ROAS | Retorno sobre gasto em anúncios |
| VTC | View-through conversion |
| CAPI | Conversions API (server-side) |
| AEM | Aggregated Event Measurement |
| DDA | Data-Driven Attribution |
| QR | Quality Ranking |
| AN | Audience Network |
| LTV | Lifetime Value |
| CAC | Customer Acquisition Cost |
| CMV | Custo da Mercadoria Vendida |
| ATT | App Tracking Transparency (iOS 14.5+) |
| BANT | Budget, Authority, Need, Timeline (qualificação) |
| MoM | Month over Month |
| YoY | Year over Year |
| Learning Phase | Período inicial onde Meta aprende quem converte |
| Delivery Multiplier | Meta pode gastar até 25% a mais/dia, compensando em outros |
| Frequency Distribution | Distribuição de quantas vezes cada pessoa viu o anúncio |
| Unique CPM | CPM calculado sobre alcance (pessoas únicas) |
| Lookalike | Público similar à base de clientes |
| Exclusion Layer | Público excluído da segmentação |
| Retargeting/Remarketing | Segmentação de quem já interagiu |
| Break-even | Ponto onde receita = custo |
| Incrementality | Impacto REAL do anúncio vs o que aconteceria sem ele |
| Touchpoint | Ponto de contato entre usuário e anúncio |
| Last-click | Modelo que dá 100% do crédito ao último clique |
| Assisted Conversion | Conversão onde o anúncio ajudou mas não foi o último clique |

---

# Apêndice B: Análise Avançada de Criativos

## Matriz de Avaliação de Criativos

Avalie cada criativo em 5 dimensões (escala 1-5):

| Dimensão | O que mede | 1 (ruim) | 3 (médio) | 5 (ótimo) |
|----------|------------|----------|-----------|-----------|
| Atenção | Capta atenção nos primeiros 3s | Ignorável | Chama atenção | Prende |
| Clareza | Entende-se a oferta em 3s | Confusa | Entendível | Cristalina |
| Relevância | Ressoa com o público alvo | Genérica | Específica | Pessoal |
| CTA | Chama para ação | Ausente | Presente | Urgente |
| Diferenciação | Destaca-se dos concorrentes | Igual | Diferente | Única |

**Score total:** Soma / 25. <10 = substituir. 10-18 = testar variações. >18 = campeão potencial.

## Análise de Formatos por Objetivo

| Formato | Reconhecimento | Tráfego | Conversão | Lead | Vendas Catalogo |
|---------|---------------|---------|-----------|------|-----------------|
| Imagem única | 3/5 | 3/5 | 3/5 | 4/5 | 2/5 |
| Video (6-15s) | 5/5 | 4/5 | 4/5 | 4/5 | 3/5 |
| Carrossel | 2/5 | 4/5 | 5/5 | 3/5 | 5/5 |
| Coleção | 2/5 | 3/5 | 4/5 | 2/5 | 5/5 |
| Stories (imagem) | 3/5 | 2/5 | 2/5 | 3/5 | 2/5 |
| Stories (video) | 4/5 | 3/5 | 3/5 | 3/5 | 3/5 |
| Reels | 5/5 | 3/5 | 2/5 | 2/5 | 2/5 |
| Messenger | 2/5 | 1/5 | 2/5 | 4/5 | 1/5 |
| Lead Gen (nativo) | 2/5 | 1/5 | 3/5 | 5/5 | 1/5 |

## Teste A/B de Criativos

### Regras para Testes Válidos

1. **Uma variável por vez.** Testar imagem + texto + CTA ao mesmo tempo não é teste, é chute.
2. **Tamanho de amostra mínimo.** 500 impressões por variação para CTR. 50 conversões por variação para CPA.
3. **Duração mínima.** 48h para campanhas de alto volume. 72-96h para campanhas de baixo volume.
4. **Critério de significância.** Vencedor precisa ter pelo menos 20% de diferença na métrica principal.
5. **Parar no tempo certo.** Não pare o teste na primeira hora que uma variação parece melhor.

### Estrutura de Teste Recomendada

- **Teste de imagem:** Mesmo texto, 3-4 imagens diferentes (ângulo, cor, layout)
- **Teste de headline:** Mesma imagem, 3-5 headlines (benefício, dor, curiosidade, urgência)
- **Teste de CTA:** Mesmo criativo, 2-3 CTAs (Saiba Mais, Quero Agora, Garantir Vaga)
- **Teste de oferta:** Mesmo criativo, 2 ofertas (desconto vs frete grátis vs brinde)
- **Teste de formato:** Mesma mensagem, imagem vs vídeo vs carrossel
- **Teste de público:** Mesmo criativo, diferentes segmentações

## Psicologia do Criativo que Converte

### Gatilhos Mentais por Setor

| Setor | Gatilho #1 | Gatilho #2 | Gatilho #3 |
|-------|-----------|-----------|-----------|
| E-commerce moda | Escassez ("últimas peças") | Pertencimento ("tendência") | Prova social ("2k já compraram") |
| Educação | Autoridade ("os melhores professores") | Urgência ("últimas vagas") | Antecipação ("comece agora") |
| Saúde/Estética | Transformação ("antes e depois") | Confiança ("resultado comprovado") | Exclusividade ("para você") |
| B2B | Credibilidade ("case de sucesso") | ROI ("aumente resultados em X%") | Segurança ("empresas como a sua") |
| Imóveis | Escassez ("3 unidades restantes") | Valorização ("investimento seguro") | Urgência ("pronto para morar") |
| Fintech | Economia ("sem tarifas") | Praticidade ("em 5 minutos") | Confiança ("mais de 1M de usuários") |
| SaaS | Trial ("30 dias grátis") | Resultado ("aumente X em Y dias") | Prova social ("usado por +500 empresas") |

### Anatomia de um Anúncio Vencedor

**Headline (20% do impacto):**
- Específica > genérica
- "Aumente suas vendas em 40% em 30 dias" > "Venda mais"
- Incluir número sempre que possível
- Falar diretamente com o público ("Para donos de e-commerce...")

**Copy (30% do impacto):**
- Primeira linha: a DOR que você resolve
- Segunda linha: a SOLUÇÃO que você oferece
- Terceira linha: a PROVA (social, autoridade, resultado)
- Quarta linha: a URGÊNCIA ou ESCASSEZ
- Quinta linha: o CTA

**Imagem/Vídeo (50% do impacto):**
- O olho humano processa imagem 60.000x mais rápido que texto
- Contraste alto = mais atenção
- Rosto humano (especialmente olhos) aumenta engajamento
- Cores que destoam do feed (laranja em feed azul, por exemplo)
- Texto na imagem? Sim, mas <20% da área (regra do Meta)
- Vídeo: primeiros 3s decidem se a pessoa continua ou passa

### Anti-padrões de Criativo (o que NÃO fazer)

- **Imagem genérica de banco de imagens** (ninguém acredita que você é a pessoa da foto)
- **Texto genérico** ("Qualidade e tradição desde 1990" — e daí?)
- **Muitos argumentos** (paralisia de decisão — 1 benefício, 1 CTA)
- **Promessa exagerada** ("Emagreça 20kg em 1 semana") — atrai lead não qualificado ou é rejeitado
- **CTA fraco** ("Clique aqui" vs "Quero minha vaga" vs "Sim, quero economizar R$200")
- **Falta de contraste** (anúncio que se confunde com o feed)
- **Texto muito pequeno** (impossível de ler no mobile)
- **Ignorar o formato** (imagem quadrada no Stories = cortada)

## Estratégias de Escala

### Como Escalar Sem Perder Performance

**Regra de ouro:** A escala sempre reduz eficiência. O segredo é minimizar essa perda.

**Técnica 1: Escalar por público (recomendada)**
- Em vez de aumentar orçamento no mesmo público, adicionar novos públicos
- Lookalike 1% -> Lookalike 3% -> Interesses -> Amplo
- Cada novo público tem CPM/CPA próprio, mas não canibaliza o original

**Técnica 2: Escalar por criativo (boa)**
- Se um criativo funciona, crie 3-5 variações dele
- Mesmo ângulo, diferentes execuções
- Isso evita fadiga mesmo com orçamento maior

**Técnica 3: Escalar por geografia (média)**
- Adicionar novas regiões/cidades
- Cada região tem CPM e conversão diferentes
- Testar com R$50-100/dia por nova região antes de escalar

**Técnica 4: Escalar por placement (arriscada)**
- Se feed funciona, testar Stories, Reels, Audience Network
- Cada placement exige criativo nativo
- Audience Network raramente escala com qualidade

**Técnica 5: Aumentar orçamento (menos recomendada)**
- Máximo: 20% de aumento a cada 2-3 dias
- Mais que isso: desestabiliza a entrega, joga em learning phase parcial
- Meta recomenda 15-20%/semana, não por dia

### Quando NÃO Escalar

- Na primeira semana da campanha (aprendizado instável)
- Com frequência >2,5 (vai saturar mais rápido)
- Com Quality Ranking Below Average (precisa consertar primeiro)
- Com <50 conversões/semana (base estatística insuficiente)
- Durante pico sazonal (CPM artificialmente alto)
- Sem ter criativos reserva (quando saturar, não tem substituto)

## Métricas Avançadas de E-commerce

### Métricas Específicas para Loja Virtual

**Taxa de Add-to-Cart (ATC):**
- O que é: % de visitantes que adicionaram ao carrinho
- Normal: 3-8% (e-commerce), 5-12% (moda)
- Se ATC alto mas checkout baixo: problema no carrinho/frete

**Taxa de Checkout Iniciado:**
- O que é: % dos ATC que iniciaram checkout
- Normal: 50-80%
- Se baixa: surpresa no frete, custos adicionais, obrigatoriedade de cadastro

**Taxa de Compra Concluída:**
- O que é: % dos checkouts que finalizaram
- Normal: 60-85%
- Se baixa: problema na página de pagamento, formas de pagamento limitadas, erro técnico

**Taxa de Abandono de Carrinho:**
- O que é: 1 — (compras concluídas / carrinhos criados)
- Normal: 65-80%
- Se >80%: problemas graves no checkout

**Ticket Médio por Campanha:**
- Varia por criativo/público? Se sim, campanhas de ticket baixo podem ter ROAS pior mas margem melhor (ou vice-versa)
- Importante: otimizar para margem, não para ticket

**Frequência de Compra:**
- Clientes que compraram 2+ vezes nos últimos 90 dias
- Se frequência de compra está caindo: campanhas estão atraindo apenas compradores de primeira viagem sem fidelizar

## Estratégias de Remarketing Avançado

### Segmentação de Remarketing por Comportamento

**Visitantes do site (7 dias):** Alta intenção. Oferta: completa a compra.
**Visitantes do site (14-30 dias):** Intenção média. Oferta: lembrete + reforço de benefício.
**Visitantes de página de produto:** Intenção muito alta. Oferta: produto específico + avaliações.
**Visitantes de carrinho abandonado:** Intenção altíssima. Oferta: desconto ou frete grátis.
**Leads não convertidos (30 dias):** Conhecem a marca. Oferta: prova social + case de sucesso.
**Leads não convertidos (60-90 dias):** Esfriaram. Oferta: novidade ou novo conteúdo.
**Compradores anteriores (90 dias):** Clientes. Oferta: cross-sell ou upsell.
**Compradores anteriores (180 dias+):** Clientes inativos. Oferta: reativação (desconto especial).
**Engajamento com conteúdo (vídeo 50%+ ou post):** Baixa intenção. Oferta: conteúdo relacionado, depois oferta.

### Sinais de Remarketing Saudável

- ROAS remarketing 2-4x o ROAS de prospecção (normal)
- CTR remarketing 2-3x o CTR de prospecção
- CPA remarketing 40-60% do CPA de prospecção
- Frequência remarketing < 5,0
- New customer ratio geral > 40% (remarketing não está canibalizando a prospecção)

### Sinais de Remarketing Doente

- ROAS remarketing < ROAS prospecção (remarketing quebrou)
- CTR remarketing < 0,3% (audiência saturada ou criativo irrelevante)
- CPA remarketing > CPA prospecção (caro demais para quem já conhece)
- Frequência remarketing > 6,0 (saturação severa)
- New customer ratio < 20% (só vendendo para quem já comprou — base não cresce)

## Análise de Funil com Dados Limitados

### Quando Você Só Tem Dados do Meta

Se não tem integração CRM (o que infelizmente é comum), use estes proxies:

**Qualidade do lead por proxy:**
- CTR muito alta com conversão zero: provável tráfego de baixa qualidade (AN/Reels)
- VTC > 40% das conversões: leads provavelmente não incrementais
- CPM muito baixo (< 70% da média do setor): possível entrega em placements de baixa qualidade
- Tempo médio na página (via pixel): <10s = lead frio. >30s = lead quente.
- Bounce rate (via pixel): >80% = página ou audiência errada

**Proxy de lead qualificado sem CRM:**
- Se o formulário de lead tem pergunta de qualificação (telefone, orçamento), leads que preenchem campos opcionais são mais qualificados
- Se o lead vem de um criativo específico vs criativo genérico
- Se o lead clicou no link vs veio de formulário nativo do Meta

## Guia de Investigação Rápida (30 minutos)

Quando um gestor precisa de resposta rápida:

**Problema: CPA subiu de repente**

1. (2 min) Verificar se está em learning phase. Se sim: aguardar.
2. (3 min) Breakdown por placement. Audience Network disparou? Desligar.
3. (3 min) Frequência e CTR. Freq >3 e CTR caindo? Fadiga.
4. (3 min) CPM. Subiu? Quality Ranking baixo? Trocar criativo.
5. (2 min) Breakdown demográfico. Mudou faixa etária? Sazonalidade.
6. (2 min) Verificar pixel/CAPI. Disparando eventos? Match rate ok?
7. (5 min) Verificar concorrência (CPM subiu em horários específicos?).
8. (10 min) Gerar hipótese principal, recomendar ação.

**Total: ~30 min de investigação para 80% dos cenários.**

---

# Sobre os Autores

Esta skill foi desenvolvida pelo time V4, com base em mais de 20 anos de experiência combinada em gestão de tráfego pago, análise de performance e otimização de campanhas Meta Ads. Os frameworks, tabelas e referências foram consolidados a partir de milhares de campanhas gerenciadas em dezenas de setores diferentes.

O código-fonte e as skills do Builders Hub estão disponíveis em:
https://github.com/v4company/builders-hub

Para contribuir com melhorias, correções ou novas seções, abra um PR ou issue no repositório.

---

# Changelog

| Versão | Data | Alterações |
|--------|------|------------|
| 1.0.0 | 2026-07 | Versão inicial completa: pirâmide de decisão, 40+ métricas detalhadas, 13 contextos, 10 árvores de decisão, 5 casos práticos, glossário avançado, protocolo de leitura, cadências de análise, parâmetros LLM, seções expandidas de diagnóstico avançado |

---

*Esta skill é mantida pelo time V4 como parte do ecossistema Builders Hub. Distribuição livre, atribuição required.*

---

# Apêndice C: Glossário de Termos Técnicos Meta Ads

## Termos de Plataforma

**Ad Set (Conjunto de Anúncios):** Nível intermediário da estrutura da conta. Define público-alvo, orçamento, programação, placement e lances. Um conjunto contém um ou mais anúncios.

**Ad (Anúncio):** Nível mais granular. Define o criativo (imagem, vídeo, texto, headline, CTA). Cada anúncio pertence a um conjunto.

**Campaign (Campanha):** Nível mais alto. Define o objetivo (conversão, tráfego, alcance, lead, etc). Contém um ou mais conjuntos.

**Learning Phase:** Período inicial (~50 eventos em 7 dias) onde o algoritmo está aprendendo quem converte. Performance é instável. Fora desse período, a campanha está em "Active" (entregando normalmente).

**Learning Limited:** Quando a campanha não consegue sair da learning phase porque não atinge 50 eventos/semana. Comum em contas de baixo orçamento ou públicos restritos.

**Delivery:** Status de entrega do anúncio. Pode ser: Active (entregando normalmente), Learning (aprendendo), Limited (restrito por orçamento/público), Out of Budget (orçamento esgotado), Paused (pausado manualmente), Completed (campanha programada encerrada), Inactive (anúncio desativado), Draft (rascunho), Pending Review (em análise), Disapproved (reprovado).

**Frequency Cap:** Limite de quantas vezes uma pessoa vê o anúncio (ex: max 3x/dia). Reduz saturação mas também reduz entrega.

**Bid (Lance):** Quanto você está disposto a pagar por uma conversão (cost cap), clique (bid cap) ou impressão (CPM). Pode ser automático (lowest cost) ou manual (bid cap, cost cap).

**Lowest Cost:** Estratégia de lance padrão. Meta busca o menor custo possível dentro do orçamento.

**Cost Cap:** Você define o CPA máximo. Meta tenta conseguir conversões dentro desse custo.

**Bid Cap:** Você define o lance máximo. Meta não paga mais que isso por conversão/clique.

**Target Cost:** Você define o CPA alvo. Meta tenta manter o CPA próximo a esse valor (usado para estabilidade, não eficiência).

**Delivery Multiplier:** Meta pode gastar até 25% a mais em um dia (até 1,25x o orçamento diário) desde que compense nos dias seguintes. Isso dá flexibilidade ao algoritmo para aproveitar momentos de maior oportunidade.

**Amount Spent (Gasto):** O valor total gasto no período selecionado. É o dado mais concreto da plataforma.

**Cost per Result (Custo por Resultado):** Custo médio para cada resultado do objetivo escolhido.

**Results (Resultados):** Número total de ações do objetivo escolhido (compras, leads, visualizações, etc).

## Termos de Métricas

**Impressions (Impressões):** Número de vezes que o anúncio foi exibido na tela. Não garante visualização.

**Reach (Alcance):** Número de pessoas únicas que viram o anúncio. Estimado.

**Frequency (Frequência):** Média de vezes que cada pessoa viu o anúncio. Impressões / Alcance.

**Clicks (All):** Todos os cliques em qualquer elemento do anúncio. Inclui link, reação, perfil, etc.

**Clicks (Link):** Cliques no link que vai para fora do Meta.

**CTR (All):** (Clicks totais / Impressões) x 100.

**CTR (Link Click-Through Rate):** (Cliques no link / Impressões) x 100.

**CPM (Cost Per Mille):** (Gasto / Impressões) x 1000.

**CPM Único:** (Gasto / Alcance) x 1000.

**CPC (All):** Gasto / Cliques totais.

**CPC (Link):** Gasto / Cliques no link.

**CPA/CPR:** Gasto / Número de conversões ou resultados.

**ROAS:** Receita / Gasto. Não considera custos.

**Conversion Rate (Taxa de Conversão):** (Conversões / Cliques no link) x 100.

**Attribution Window:** Janela de tempo entre interação e conversão dentro da qual o Meta atribui crédito.

**View-Through Attribution:** Crédito dado a uma impressão (sem clique) quando o usuário converte dentro da janela de view. Meta reporta isso junto com click-through.

**7-Day Click:** Janela padrão. Conversões até 7 dias após o clique.

**1-Day View:** Janela padrão. Conversões até 1 dia após visualizar (sem clicar).

**Dedup (Deduplicação):** Meta tenta não contar a mesma conversão duas vezes (de pixel e CAPI). Funciona com base no event_id enviado.

## Termos de Otimização

**Campaign Budget Optimization (CBO):** Meta distribui o orçamento da campanha entre os conjuntos automaticamente, priorizando os que têm melhor performance. Recomendado para contas com múltiplos conjuntos.

**Ad Set Budget Optimization:** Orçamento fixo por conjunto. Sem CBO, você controla quanto cada conjunto gasta.

**Dynamic Creative (Criativo Dinâmico):** Meta testa automaticamente combinações de imagem, texto, headline e CTA para encontrar a melhor versão. Útil para testes, mas o controle estatístico é limitado.

**Automatic Placements (Placements Automáticos):** Meta entrega em todos os placements disponíveis. Recomendado na maioria dos casos, mas REQUIRE criativos nativos para cada formato. Perigoso quando ativado sem supervisão.

**Advantage+:** Conjunto de recursos de automação do Meta:
- **Advantage+ Audience:** Meta encontra o público ideal automaticamente além da segmentação que você definiu
- **Advantage+ Creative:** Meta modifica seu criativo (texto, imagem, cor) para melhorar performance
- **Advantage+ Placements:** Meta distribui automaticamente entre placements
- **Advantage+ Shopping:** Campanha otimizada para e-commerce com catálogo

**Minimum ROAS (ROAS Mínimo):** Meta tenta manter o ROAS acima do valor definido. Disponível em algumas campanhas de conversão.

**Value Optimization:** Meta otimiza para o valor das conversões (não apenas o número), priorizando compras de maior valor. Requer envio de valor no pixel/CAPI.

**Event Match Quality:** Qualidade da correspondência entre eventos do pixel/CAPI e perfis do Meta. Quanto maior, melhor a otimização.

**Aggregated Event Measurement (AEM):** Protocolo da Meta para medir conversões em ambiente iOS 14.5+. Usa agregação e modelagem para preencher dados perdidos.

## Termos de Segmentação

**Core Audiences:** Públicos que você define manualmente (localização, idade, gênero, interesses, comportamentos).

**Custom Audiences:** Públicos baseados em dados próprios (visitantes do site, lista de clientes, leads, engajamento).

**Lookalike Audiences:** Públicos similares (em características) a uma audiência personalizada. Percentuais menores (1%) são mais similares mas menores. Percentuais maiores (5-10%) são menos similares mas maiores.

**Retargeting (Remarketing):** Segmentar pessoas que já interagiram com sua marca (site, app, página, anúncios).

**Exclusion Targeting:** Excluir determinados públicos da segmentação (ex: excluir quem já comprou, excluir leads recentes).

**Detailed Targeting (Segmentação Detalhada):** Interesses e comportamentos que você adiciona para refinar o público.

**Expanding Audience:** Quando a audiência disponível é pequena, o Meta pode expandir para públicos similares além da segmentação definida.

**AND/OR Targeting:** Como os interesses são combinados. Interesse A AND Interesse B = pessoa precisa ter ambos (mais restrito). Interesse A OR Interesse B = pessoa pode ter qualquer um (mais amplo).

**Audience Network:** Rede de terceiros (apps e sites) onde o Meta exibe anúncios. Menor qualidade, menor CPM, menor controle.

**In-stream:** Anúncios em vídeo do Facebook Watch. O usuário pode pular após 5s.

**Instant Experience (Canvas):** Experiência full screen que carrega instantaneamente quando o usuário clica. Boa para storytelling.

**Collection:** Formato que combina vídeo/imagem principal com grid de produtos abaixo. Específico para e-commerce com catálogo.

**Messenger Ads:** Anúncios no Messenger. Objetivo: conversas. Placement subutilizado mas eficaz para lead gen.

## Termos de Implementação Técnica

**Conversions API (CAPI):** Servidor envia eventos diretamente para Meta. Não depende de navegador. Mais confiável que pixel.

**Meta Pixel:** Código JavaScript no site que envia eventos de navegação para Meta. Bloqueado por ad blockers, iOS 14.5+.

**CAPI Gateway:** Proxy entre servidor e Meta. Permite enviar eventos sem expor tokens do servidor.

**Event ID:** Identificador único enviado no pixel E no CAPI. Meta usa para deduplicar. Sem event_id, pode contar mesma conversão duas vezes.

**Test Events:** Ferramenta no Events Manager para testar se os eventos estão sendo recebidos corretamente.

**Diagnostics:** Seção no Events Manager que mostra problemas de implementação (eventos perdidos, match rate baixo, duplicatas).

**Match Rate:** Taxa de correspondência entre eventos do servidor e perfis do Meta. >90% = excelente. <70% = problemático.

**Deduplication:** Processo de remover eventos duplicados (mesmo evento enviado por pixel E CAPI). Meta usa event_id + nome do evento.

**Server-Side Events (SSE):** Eventos enviados do servidor para Meta via CAPI.

**Browser-Side Events (BSE):** Eventos enviados do navegador via Pixel.

**Hybrid Setup:** CAPI + Pixel funcionando simultaneamente. Ideal para maximizar dados e resiliência.

**Event Parameters:** Dados adicionais enviados com cada evento (valor da compra, moeda, ID do produto, nome do lead, etc). Essenciais para otimização de valor e ROAS.

**Custom Events:** Eventos que você define (além dos padrões: Purchase, Lead, AddToCart, etc). Importante para métricas de funil específicas do negócio.

## Termos de Atribuição

**Last Click:** 100% do crédito ao último clique antes da conversão. Padrão do Meta.

**Last Touch:** Similar ao last click mas a última interação (pode ser view-through).

**First Click:** 100% do crédito ao primeiro clique.

**Linear:** Crédito distribuído igualmente entre todos os touchpoints.

**Time Decay:** Mais crédito para touchpoints mais próximos da conversão.

**Data-Driven Attribution (DDA):** Meta distribui crédito proporcionalmente baseado em dados históricos. Mais próximo da verdade.

**Position-Based:** 40% para primeiro clique, 40% para último, 20% distribuído entre os do meio.

**Assisted Conversions:** Conversões onde o anúncio contribuiu mas não foi o último clique.

**Incrementality Test:** Comparação entre grupo exposto vs grupo de controle. Mede o impacto REAL.

**Lift Study:** Teste de incrementality conduzido pelo Meta. Disponível para contas elegíveis.

**Holdout Group:** Grupo de controle que não vê o anúncio. Essencial para medir incremento real.

**Conversion Window Click:** Janela de tempo pós-clique para atribuir conversão. Configurável (1d, 7d, 28d).

**Conversion Window View:** Janela de tempo pós-visualização (sem clique) para atribuir conversão. Configurável (1d, 7d).

**Multi-Touch Attribution (MTA):** Modelo que distribui crédito entre múltiplos touchpoints.

**Marketing Mix Modeling (MMM):** Modelo estatístico que mede impacto de todos os canais (incluindo off-line). Não depende de atribuição individual.

## Termos de Leilão

**Auction (Leilão):** Processo onde Meta decide qual anúncio exibir para cada pessoa. Cada impressão é um leilão.

**Bid (Lance):** Quanto o anunciante está disposto a pagar pelo resultado desejado.

**Estimated Action Rate:** Probabilidade estimada de que a pessoa realize a ação desejada (comprar, clicar, etc).

**Total Value:** Pontuação final que determina o vencedor do leilão: (Lance do anunciante x Ação Estimada) + Relevância + Qualidade.

**Relevance Score (descontinuado):** Antiga métrica de qualidade. Substituída por Quality Ranking, Engagement Ranking e Conversion Rate Ranking.

**Quality Ranking:** Como a qualidade do anúncio se compara aos concorrentes no mesmo público.

**Conversion Rate Ranking:** Como a taxa de conversão esperada se compara aos concorrentes.

**Engagement Rate Ranking:** Como o engajamento esperado se compara aos concorrentes.

**Ad Quality (Qualidade do Anúncio):** Componente do Quality Ranking. Baseado em feedback negativo, clickbait, etc.

**User Engagement (Engajamento do Usuário):** Componente do Quality Ranking. Baseado em interações esperadas.

**Auction Overlap:** Quantos anunciantes estão disputando o mesmo público. Alta sobreposição = CPM mais alto.

**Win Rate:** Percentual de leilões que seu anúncio ganhou. Se cair, seus lances ou qualidade estão baixos.

**Impression Share:** Percentual de impressões possíveis que seu anúncio recebeu. Se baixo, há oportunidade de aumentar orçamento ou melhorar qualidade.

## Termos de Conta e Faturamento

**Ad Account (Conta de Anúncios):** Entidade que contém todas as campanhas, conjuntos e anúncios. Cada conta tem um ID numérico.

**Business Manager (BM):** Dashboard central para gerenciar contas de anúncios, páginas, pixels e permissões.

**Page (Página):** Presença do negócio no Facebook. Necessária para rodar anúncios.

**Instagram Account:** Conta do Instagram vinculada à página do Facebook para rodar anúncios no IG.

**Spending Limit (Limite de Gasto):** Limite máximo que a conta pode gastar. Contas novas têm limites baixos (R$100-500/dia) que aumentam com o tempo.

**Payment Method:** Cartão de crédito, débito, boleto bancário ou saldo. A forma como a conta paga os anúncios.

**Payment Profile:** Perfil de pagamento vinculado à conta. Pode ser da própria empresa ou de um parceiro (agência).

**Account Spending Limit vs Ad Account Limit:** O primeiro é definido pelo Meta, o segundo é auto-imposto pelo anunciante.

**Cost per Result Goal:** Meta de custo por resultado definida no nível de campanha.

**Billing Threshold:** Limiar de faturamento. Quando o gasto atinge esse valor, a Meta cobra automaticamente. Ex: quando atinge R$100, cobra o cartão.

**Out of Credits:** Conta sem saldo ou crédito disponível. Anúncios param de ser entregues.

## Termos de Relatório e Análise

**Breakdown:** Segmentação de métricas por uma dimensão específica (idade, gênero, plataforma, região, dispositivo, horário, etc).

**Cross-Breakdown:** Segmentar por duas dimensões ao mesmo tempo (ex: idade x plataforma).

**Comparison Date Range:** Período de comparação (ex: essa semana vs semana passada).

**Custom Conversion:** Conversão personalizada definida com base em eventos do pixel (ex: visitou página de obrigado + valor > R$100).

**Standard Event:** Evento pré-definido pelo Meta (Purchase, Lead, AddToCart, CompleteRegistration, etc).

**Value Optimization:** Otimização baseada no valor da conversão, não apenas na contagem.

**Conversion Value:** Valor monetário associado à conversão. Usado para calcular ROAS.

**Attribution Setting:** Configuração de janela de atribuição (click + view).

**Report Time:** O período do relatório (dia da conversão vs dia do clique vs dia da impressão).

**Conversion Window:** Janela de tempo retrospetiva que o relatório considera.

**Segments:** Subdivisões de público como "Novos vs Recorrentes", "Dispositivo", "Plataforma", etc.

**Filters:** Filtros aplicados ao relatório para focar em subconjuntos específicos de dados.

**Pivot Table:** Visualização de dados com linhas e colunas cruzadas (ex: campanhas nas linhas, dias da semana nas colunas).

**Custom Column:** Coluna personalizada criada combinando métricas (ex: (gasto / conversões) para CPA personalizado).

## Validação Final

Esta skill foi projetada para ser o recurso definitivo de análise Meta Ads. É um documento vivo — conforme a plataforma Meta evolui, esta skill deve ser atualizada para refletir novas métricas, novas funcionalidades e novos padrões de mercado.

**Última recomendação:** Nenhum framework substitui a experiência prática. Use esta skill como guia, não como dogma. Teste, meça, aprenda, repita. E sempre desconfie de métricas que parecem boas demais para ser verdade — geralmente são.
