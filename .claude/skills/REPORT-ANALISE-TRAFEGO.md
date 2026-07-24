# Report: Skills de Análise de Tráfego — v1.0.0

**Data:** 21/07/2026
**Autor:** v4team
**Total de linhas:** 9.088 (3 skills combinadas)

---

## Sumário

| Skill | Arquivo | Linhas | Tamanho |
|-------|---------|--------|---------|
| `gt-analise-meta-ads` | `.agents/skills/gt-analise-meta-ads/SKILL.md` | 3.047 | 133 KB |
| `gt-analise-google-ads` | `.agents/skills/gt-analise-google-ads/SKILL.md` | 3.039 | 137 KB |
| `gt-analise-bing-ads` | `.agents/skills/gt-analise-bing-ads/SKILL.md` | 3.002 | 135 KB |
| **Espelhadas** | `.claude/skills/gt-analise-*/` | ✔ | idêntico |

---

## 1. `gt-analise-meta-ads` (3.047 linhas)

### Estrutura

| Seção | Subseções | O que contém |
|-------|-----------|-------------|
| **Visão Geral** | 4 | Propósito, o que resolve (5), para quem (4 perfis), diferencial |
| **Premissas Fundamentais p/ LLM** | 4 regras | Hierarquia de confiança (13 métricas ranqueadas), quando perguntar vs inferir (6+4), 6 viéses comuns, 5 verificações de dado |
| **Pirâmide de Decisão** | 3 camadas | Arquitetura conceitual da skill |
| **Camada 1 — Operação Diária** | 11 métricas | CTR, CPM, CPC, Frequência, ROAS, CPA, Gasto/dia, Impressões, Alcance, Taxa de Engajamento, CPM Único. Cada uma com: fórmula, tabela de normalidade (10 setores), sinais V/A/V, "O que NÃO fazer" (~56 itens no total) |
| **Camada 2 — Diagnóstico Tático** | 10 métricas | Quality Ranking, Engagement Rate Ranking, Conversion Rate Ranking, CPM por breakdown (idade/gênero/plataforma/região/dispositivo), CTR por placement, Taxa de Conv por etapa, Frequency Distribution, Custo Lead Qualificado vs Bruto, ROAS por público, ROAS por criativo |
| **Camada 3 — Investigação Profunda** | 10 métricas | VTC, Time Lag, Path to Conversion, Attribution Window Comparison, CAPI vs Pixel Match Rate, Incrementality Test, DDA, New vs Returning Customer, Cross-Device, Assisted Conversions |
| **Matriz Contexto × Métrica** | 13 cenários | Campanha nova, madura, CPA subiu, ROAS caindo, volume baixo, frequência alta, CTR baixo+CPM alto, VTC vs click, Meta vs GA4, estagnação, lead não qualifica, remarketing não converte, diferença por plataforma |
| **Protocolo de Leitura** | 6 passos | Classificação de cenário (variação <15% / 15-50% / >50%), seleção de métricas, aplicação de normalidade, geração de hipóteses (com template), recomendação de ação |
| **Árvores de Decisão** | 10 | CPA alto, ROAS baixo, volume baixo, frequência alta, CTR baixo, CPM alto, Meta vs GA4, performance por plataforma, lead bruto vs qualificado, estagnação |
| **Parâmetros LLM** | 5 seções | Temperatura (0.1-0.5), thresholds consolidados (6 setores × 7 métricas), pesos por contexto (6 × 3), 9 regras de precedência, tabela de prioridade de hipóteses (8) |
| **Glossário Avançado** | 8 | CPC vs CPC link, CTR vs CTR link, VTC, Frequência, CPM Único, ROAS tipos, CAPI vs Pixel, Conversion Window |
| **Casos Práticos** | 5 | Clínica estética (CPA R$45→R$120), E-commerce moda (ROAS 5→2.5, vendas +40%), Escola idiomas (lead não agenda), SaaS B2B (CTR alto, 0 conv), Suplementos (feed bom, Audience Network drena) |
| **Cadências** | 5 | 24h, 48h, semanal, quinzenal, mensal — cada com "o que olhar" + "o que NÃO fazer" |
| **Seções Expandidas** | 10 | CRM offline, ciclo de vida do criativo (5 fases + tabela por setor), concorrência no leilão, sazonalidade (calendário Brasil 12 períodos), dayparting (6 horários), sobreposição de públicos, 3 arquiteturas de conta (Lead Gen/E-commerce/SaaS), break-even LTV:CAC, margem por campanha, alertas automáticos (17 gatilhos) |
| **Referências Rápidas** | 3 | Resumo sinais (8 métricas × 3), checklist diário (10 itens), checklist semanal (10 itens) |
| **Benchmarks Avançados** | 2 | Por faixa de orçamento (5 faixas), por estágio da conta (5 estágios) |
| **15 Erros Comuns** | 1 lista | Os erros mais frequentes em análise de Meta Ads |
| **Guia de Referência LLM** | 4 | Template de resposta (10 seções), prompt template (7 perguntas), regras de formatação (6), exemplo de análise |
| **Integrações** | 4 skills | v4mos-dados-meta-ads, gt-gestor-de-trafego, gt-relatorios-trafego, account-checkin-review |
| **Apêndice C — Glossário Técnico** | 10 categorias | ~150 termos (Plataforma, Métricas, Otimização, Segmentação, Implementação, Atribuição, Leilão, Conta, Relatório) |
| **Regras de Ouro** | 10 | Resumo executivo para o LLM |

**Tabelas:** ~35

**Diferenciais:** Pirâmide de 3 camadas com lógica de navegação entre verde→amarelo→vermelho, foco em fadiga criativa e frequência, breakdowns por plataforma/placement, CAPI vs Pixel, VTC vs click-through

---

## 2. `gt-analise-google-ads` (3.039 linhas)

### Estrutura

| Seção | Subseções | O que contém |
|-------|-----------|-------------|
| **Visão Geral** | — | Multi-rede: Search, Shopping, Display, YouTube, PMax, Demand Gen |
| **Premissas Fundamentais p/ LLM** | 10 regras | Intenção de busca vs descoberta, hierarquia de confiança (15+ métricas), Quality Score (componentes com pesos), atribuição (5 modelos), armadilha do IS, posição média, conversões vs GA4 (divergência 10-40%), brand vs non-brand (tabela), estratégias de lance (7), search terms |
| **Pirâmide de Decisão** | 3 camadas | Arquitetura específica Google |
| **Camada 1 — Operação Diária** | 11 métricas | Cliques, Impressões, CPC Médio (22 setores), CTR (6 redes), Gasto, Conversões, CVR (12 setores), CPA (15 setores), ROAS (6 setores + margem), Impression Share (4 redes), Budget. Cada uma com sinais V/A/V e "O que NÃO fazer" (~60 itens) |
| **Camada 2 — Diagnóstico Tático** | 12 métricas | QS (3 componentes detalhados), IS Lost Rank vs Budget (tabela), Search Impression Share, Lost Top/Absolute Top, CVR por dispositivo, Time Lag (8 setores), Top vs Other CPC, Brand vs Non-brand CPA, Match Type (5×4), Search Terms sem conversão, ROAS por produto Shopping, Abandono de carrinho |
| **Camada 3 — Investigação Profunda** | 12 métricas | DDA vs Last-click gap, Search Term Overlap, Incrementality (geo lift/holdout), Brand Lift, New vs Returning Customer, Cross-device, Assisted Conversions, VTC vs CTC, Campaign Experiments, PMax Asset Group, Audience Insights, Customer Match |
| **Contextos × Métricas por Rede** | 15 cenários | **Search** (7): CPA subiu, IS caindo, QS baixo, search term irrelevante, brand vs non-brand, mobile/desktop, exata vs ampla. **Shopping** (4): ROAS variado, produto sem impressão, CTR baixo, preço vs concorrência. **Display/YouTube** (3): VTC vs CTC, CPM alto+CTR baixo, Brand Lift. **PMax** (3): caixa preta, asset group, canibalização |
| **Protocolo de Leitura** | 6 fases | Contexto mínimo (9 perguntas), Camada 1 → V/A/V, coerência entre métricas (4 incoerências), Camada 2 (8 causas), Camada 3 (5 investigações), priorização (gravidade×facilidade×impacto) |
| **Árvores de Decisão** | 12 | CPA subiu, ROAS caindo, IS baixo, CTR baixo Search, QS baixo, muitos cliques poucas conv, Display VTC>60%, PMax sem transparência, Shopping produto drena, YouTube sem engajamento, Google vs GA4 divergentes, Marca vs concorrência |
| **Parâmetros LLM** | 5 seções | Temperatura, thresholds (15 setores × 5 métricas), pesos (8 cenários), precedência (7 regras), prioridade de hipóteses (10) |
| **Glossário Avançado** | 14 seções | QS 3 componentes, IS (5 tipos), Top vs Other CPC, Estratégias de Lance (7), Brand vs Non-brand (4 passos), Conversões (o que conta/não conta), Enhanced Conversions, DDA vs Last Click (tabela 9×2), GCLID (6 causas de quebra), VTC, PMax (6 redes), Experimentos |
| **Casos Práticos** | 6 | E-commerce moda (CPC baixo, CTR ok, ROAS 0), Clínica odonto (IS 30%, budget subutilizado), SaaS B2B (QS 10, 0 conv), Material construção (ROAS 8 geral, 0.5 categoria), Universidade (CPC +60% concorrência), Seguros auto (PMax ROAS 12, Search despenca) |
| **Cadências** | 4 timelines + 3 reports | 24h (5 min), semanal (30-60 min), quinzenal (1-2h), mensal (3-4h). Reports: Daily Check, Weekly Review (7 campos), Monthly Deep Dive (11 campos) |
| **Seções Avançadas** | ~15 | Demand Gen, Auction Insights (5 métricas), Tipos de Correspondência, Extensões (tabela 7 × CTR), Análise por tipo de campanha (6), Troubleshooting Rápido (5 problemas), Configuração de Conversão (checklist 15 itens), Ferramentas (10), Automação/Scripts (2), Sazonalidade (índice 12 meses + 3 fases), Otimização por objetivo (vendas/lead/reconhecimento), Break-Even (4 exemplos + LTV), Planejamento Orçamento (2 métodos), Documentação de Mudanças, Remarketing Avançado (6 tipos + tabela 8×4), Smart Bidding (tabela 4×3 + 5 cenários de falha), Custo de Má Otimização (7 custos + checklist anti-desperdício 12 itens) |
| **Regras de Ouro** | 12 | Resumo executivo para o LLM |

**Tabelas:** ~18

**Diferenciais:** Abordagem multi-rede (não trata Google como "um canal só"), Quality Score com pesos reais (40/30/30), Auction Insights, Smart Bidding com cenários de falha, extensões com impacto real no CTR

---

## 3. `gt-analise-bing-ads` (3.002 linhas)

### Estrutura

| Seção | Subseções | O que contém |
|-------|-----------|-------------|
| **Visão Geral** | 4 | O que é, por que é diferente (audiência maior poder aquisitivo), oportunidades, limitações |
| **Premissas Fundamentais p/ LLM** | 6 regras | 10 regras de ouro, "Bing não é Google mais barato" (CPC R$8,50 Google vs R$4,20 Bing), Search Partners, ecossistema Microsoft, hierarquia de confiança (8 métricas classificadas), complementa vs substitui |
| **Pirâmide de Decisão** | 3 camadas | Lógica de navegação entre camadas |
| **Camada 1 — Operação Diária** | 11 métricas | Cliques, Impressões, CPC (Search R$1,50-R$15, 30-50% < Google), CTR (Search 1.5-5%, Aud.Network 0.2-0.8%), Gasto, Conversões (delay 4-24h), CVR (Search 2-8%, 10-30% < Google), CPA (mín 30 conv), ROAS (mín 3:1), Impression Share (ideal >80%), Posição Média (Bing ainda usa) |
| **Camada 2 — Diagnóstico Tático** | 9 métricas | QS (tabela vs Google), IS Lost (3 cenários), Search Partners (tabela 5 cenários), CVR por dispositivo (Desktop 60-70%, Mobile 30-40%), Time Lag (4 setores), Top vs Other CPC (40-60% mais caro), Match Type, Bing Audience Network (metas: CTR>0.15%, CPC<50% Search, CVR>0.5%, ROAS>2:1), LinkedIn Profile Targeting (CPC +20-40%, CVR +30-60%, volume -50-80%) |
| **Camada 3 — Investigação Profunda** | 9 métricas | Atribuição (4 modelos + limitações), UET Health (6 problemas comuns), VTC (janela 1 dia máx 3), Cross-Device, Assisted Conversions (>30% = TOF), Auto-Bidding (tabela 6 estratégias), Experimentos (apenas Search, 50/50, mín 2 sem), Goal Tracking (5 verificações, 4 problemas), Remarketing Lists (min 300, máx 180d, sem Similar) |
| **Contextos × Métricas** | 10 cenários | Google bom/Bing ruim (7 verificações), Search Partners drenam (5 passos), CPA menor que Google/volume insuficiente (6 ações), CTR baixo/boa posição (5 ações), Audience Network atribuição confusa (5 ações), LinkedIn não performa (5 ações), Bing vs GA4 (5 causas + 5 resoluções), Remarketing não escala (5 ações), Shopping vs Google (tabela + 5 ações), Migração Search→Audience Network (regra 10-30%) |
| **Diferenças Bing vs Google** | 8 subseções | Tabela geral (18 aspectos), QS (componentes + pesos), Estratégias de Lance (10, 2 exclusivas Google), Audience Ads vs GDN (8 aspectos), Remarketing (9 aspectos), Atribuição (8 aspectos), Shopping (9 aspectos), Importação do Google (funciona 7 / quebra 10) |
| **Protocolo de Leitura** | 7 passos | Fluxo completo + template de resposta LLM (8 seções) |
| **Árvores de Decisão** | 8 | CPA alto vs Google, Search Partners, IS baixo, CTR baixo/boa posição, Audience Ads vs Search, Importada não performa, Volume insuficiente, Remarketing não escala |
| **Parâmetros LLM** | 5 seções | Temperatura (0.1-0.3), thresholds (14 setores × 5 métricas + Aud.Network + Search Partners), pesos (10 contextos × 3 métricas), precedência (10 regras) |
| **Glossário Avançado** | 11 verbetes | UET, Shopping vs Google, Audience Network (8 canais, 5 formatos, 6 targeting), LinkedIn (5 opções), Search Partners, Position Value, DSA, Auto-bidding (5), Remarketing Lists (5 tipos), Import from Google, Microsoft Clarity |
| **Casos Práticos** | 4 | E-commerce migrado (ROAS 5→2.5), Clínica (CPA R$72 vs R$120, 8 vs 50 leads), Seguros (Audience Network lead não qualifica), Nicho apicultura (60% ROAS total com 10% volume) |
| **Cadências e Rotinas** | 3 seções | Timeline (5 frequências), Diferenças vs Google (7 aspectos), Template report (12 seções) |
| **Seções Avançadas** | ~15 | Checklist diagnóstico (12 itens), Tabela referência (29 métricas), Matriz decisão (14 sintomas), Troubleshooting (4 problemas detalhados), Segmentação horária/geográfica, Auction Insights, Framework otimização (ciclo 14 dias + matriz 2×2), Regras automação (5), Análise comparativa (Bing vs Meta vs LinkedIn, 3 tabelas), SQR (7 tipos de query), Considerações por setor (3), Scripts/API, FAQ (10), Erros comuns (15), 10 métricas pouco conhecidas, Matriz maturidade (4 níveis), Guia startup 30 dias, Mapa mental (17 ramos), Comandos rápidos (4 templates) |
| **Regras de Ouro** | 10 | Resumo executivo para o LLM |

**Tabelas:** 37

**Diferenciais:** Tratamento de Bing como canal distinto (não "Google mais barato"), Search Partners com métricas de decisão, LinkedIn targeting integrado, UET Health troubleshooting, importação do Google com riscos, 14 setores de benchmarks em dólar e real, matriz de maturidade

---

## Comparativo entre as 3 Skills

| Característica | Meta Ads | Google Ads | Bing Ads |
|---|---|---|---|
| **Linhas** | 3.047 | 3.039 | 3.002 |
| **Seções ##** | 32 | 33 | 36 |
| **Métricas Camada 1** | 11 | 11 | 11 |
| **Métricas Camada 2** | 10 | 12 | 9 |
| **Métricas Camada 3** | 10 | 12 | 9 |
| **Árvores de Decisão** | 10 | 12 | 8 |
| **Casos Práticos** | 5 | 6 | 4 |
| **Contextos/Cenários** | 13 | 15 | 10 |
| **Tabelas** | ~35 | ~18 | 37 |
| **Regras de Ouro** | 10 | 12 | 10 |
| **Erros Comuns** | 15 | — | 15 |
| **Glossário Técnico** | ~150 termos | 14 seções | 11 verbetes |

### Estrutura Compartilhada (as 3 skills seguem)

```
Pirâmide de Decisão
├── Camada 1 — Operação Diária (métricas de todo dia)
├── Camada 2 — Diagnóstico Tático (quando algo está errado)
└── Camada 3 — Investigação Profunda (quando nada explica)
        │
Matriz Contexto × Métrica → Protocolo de Leitura → Árvores de Decisão
        │
Parâmetros LLM (temperatura, thresholds, pesos, precedência)
        │
Glossário Avançado + Casos Práticos + Cadências + Regras de Ouro
```

### Como usar

| Comando | Skill |
|---------|-------|
| `/gt-analise-meta-ads` | Análise de métricas Meta Ads (Facebook/Instagram) |
| `/gt-analise-google-ads` | Análise de métricas Google Ads (Search/Shopping/Display/YouTube/PMax) |
| `/gt-analise-bing-ads` | Análise de métricas Bing Ads (Microsoft Advertising) |

---

## Localização dos Arquivos

### Skills (duplo-write obrigatório — ambas as pastas)

```
.agents/skills/
├── gt-analise-meta-ads/SKILL.md       (3.047 linhas)
├── gt-analise-google-ads/SKILL.md     (3.039 linhas)
├── gt-analise-bing-ads/SKILL.md       (3.002 linhas)
└── REPORT-ANALISE-TRAFEGO.md          (este arquivo)

.claude/skills/
├── gt-analise-meta-ads/SKILL.md       (espelho)
├── gt-analise-google-ads/SKILL.md     (espelho)
└── gt-analise-bing-ads/SKILL.md       (espelho)
```
