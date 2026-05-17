PLANO DE AÇÃO 3 MESES (S1, S2, S3)

---

### Plano de ação 
**Objetivo:** Reativar a operação com infraestrutura de tracking funcionando e 5-6 campanhas no ar.

#### Ação 1.1 — Implementar Tracking (Dias 1-5)

**Problema crítico:** Zero tracking tags (GA4/GTM) detectadas na auditoria técnica. Sem dados de audiência, remarketing é impossível e otimização de Search é cega.

**Execução:**
1. Instalar **GA4** no domínio `atlascopco.com/en-us/`
2. Instalar **Google Tag Manager** (GTM) para gerenciar tags
3. Configurar **conversões offline** (Google Ads + CRM): leads de formulário + calls
4. Criar **audiências de remarketing** no Google Ads:
   - Visitantes do site (30 dias)
   - Visitantes de páginas de produto (30 dias)
   - Quem iniciou formulário mas não completou (7 dias)

**Dependência:** Cliente precisa dar acesso ao GTM do site. Sem isso, nenhuma campanha de remarketing funciona.

#### Ação 1.2 — Revisar e Corrigir Landing Pages (Dias 5-10)

Baseado na auditoria SEO/CRO existente:
1. **Prioridade #1:** Verificar se CTA "Contact" na homepage funciona (aponta para /products — broken)
2. **Prioridade #2:** Adicionar formulário de contato na homepage
3. **Prioridade #3:** Verificar velocidade mobile das LPs de produto (atualmente 50-65 PageSpeed)
4. **Prioridade #4:** Adicionar schema Product nas páginas de equipamento

**Critério de sucesso:** Landing pages funcionais + tracking operacional antes de qualquer campanha nova.

#### Ação 1.3 — Reestruturar Nomenclatura e Arquitetura (Dias 10-12)

**Nova nomenclatura padronizada:**

```
[V4] [SEA-S] [GOO] [BOF] [PRODUTO] — [Intenção]
```

**Estrutura de conta recomendada:**

```
Search (BOF — Alta Intenção):
├── [V4] [SEA-S] [GOO] [BOF] [COMP] — Mid-Sized Diesel     ← reativar
├── [V4] [SEA-S] [GOO] [BOF] [COMP] — Air Compressors Lg    ← reativar
├── [V4] [SEA-S] [GOO] [BOF] [PUMP] — Centrifugal Pumps     ← reativar
├── [V4] [SEA-S] [GOO] [BOF] [PUMP] — Submersible Pumps     ← reestruturar
├── [V4] [SEA-S] [GOO] [BOF] [GEN] — Specs / kW             ← reativar
├── [V4] [SEA-S] [GOO] [BOF] [GEN] — General                 ← reestruturar
├── [V4] [SEA-S] [GOO] [MOF] [SUST] — Sustainability        ← nova
└── [V4] [SEA-S] [GOO] [B2B] [DEAL] — Become A Dealer       ← reestruturar

PMax:
├── [V4] [PMAX] [GOO] [CORE] — Compressors                   ← reativar
├── [V4] [PMAX] [GOO] [CORE] — Pumps                         ← reativar
├── [V4] [PMAX] [GOO] [CORE] — Generators                    ← reativar
└── [V4] [PMAX] [GOO] [CORE] — Sustainability                ← reativar

Display / Remarketing:
├── [V4] [DSP] [GOO] [REM] — Site Visitors (30d)             ← criar
└── [V4] [DSP] [GOO] [REM] — Product Page Visitors           ← criar

Video:
└── [V4] [VID] [GOO] [TOF] — Brand Awareness (Sustainability) ← reativar com novo criativo
```

#### Ação 1.4 — Reativar Campanhas Prioritárias (Dias 12-18)

**Ordem de reativação por potencial de retorno:**

| Prioridade | Campanha | CPA Histórico | Budget Sugerido |
|---|---|---|---|
| 1 | PMax Compressors | ~$70 | $25/dia |
| 2 | PMax Pumps | ~$70 | $25/dia |
| 3 | PMax Generators | ~$70 | $25/dia |
| 4 | PMax Sustainability | ~$70 | $20/dia |
| 5 | Search: Mid-Sized Diesel Compressors | **$107** | $30/dia |
| 6 | Search: Air Compressors Large | $188 | $25/dia |
| 7 | Search: Generators Specs | $284 | $20/dia |
| 8 | Search: Centrifugal Pumps | $258 | $20/dia |

**Critérios de reativação para cada campanha:**
1. Substituir Expanded Text Ads (ETAs) obsoletos por **RSAs novos** (15 headlines + 4 descriptions)
2. Revisar keywords: pausar Broad match, manter Exact + Phrase
3. Atualizar match types (o Google mudou as regras de Broad desde 2022)
4. Verificar landing pages (subdomínios podem causar reprovação)
5. Aplicar tCPA baseado no CPA histórico de cada campanha
6. Adicionar extensões (sitelinks + callouts + call)

**Budget total sugerido:** $190/dia (~$5.700/mês) — responsivo, escalonável conforme resultado.

#### Ação 1.5 — Limpeza de Keywords e Search Terms (Dias 15-18)

**Baseado nos search terms de Q2 2022 (último período ativo):**

**Negativas a adicionar em nível de conta:**
```
- Concorrentes: sullair, ingersoll rand, doosan, generac (separar em campanha própria)
- Produto/supply: parts, repair, maintenance, manual, troubleshooting
- DIY: how to, guide, tutorial, installation guide
- Aluguel: rental, rent, lease
- Emprego: jobs, careers, hiring
- Genérico sem intenção: "air compressor", "generator", "pump" (sem qualificador)
```

**Keywords Exact + Phrase a adicionar (por produto):**

| Produto | Keywords Sugeridas | Match Type |
|---|---|---|
| Mid-Sized Diesel | "mid-sized diesel air compressor", "diesel air compressor 300 cfm" | Phrase/Exact |
| Air Compressors Large | "large air compressor industrial", "high cfm air compressor" | Phrase/Exact |
| Centrifugal Pumps | "centrifugal pump industrial", "high flow centrifugal pump" | Phrase/Exact |
| Generators | "industrial generator 500 kW", "diesel generator for industrial" | Phrase/Exact |
| Sustainability | "ESG air compressor", "energy efficient compressor industrial" | Phrase/Exact |

#### Ação 1.6 — Criar Campanha de Concorrentes (Dias 18-21)

**Baseado nos search terms históricos, concorrentes com alto volume de busca:**
- Sullair
- Ingersoll Rand
- Doosan
- Generac (geradores)
- Kaeser
- Chicago Pneumatic

**Estratégia:**
- Keywords Exact/Phrase de nome de concorrente + produto
- Criativos comparativos: "Compare [Concorrente] vs Atlas Copco"
- LP dedicada com tabela comparativa
- Budget: $10-15/dia
- CPA alvo: $100-150 (conversão mais cara mas lead quente)

#### Ação 1.7 — Campanha de Brand (Dias 18-21)

**Proteção de marca essencial — concorrentes compram "atlas copco"**

**Keywords:**
```
[atlas copco]
[atlas copco compressor]
[atlas copco pumps]
[atlas copco generator]
"atlas copco air compressor"
"atlas copco industrial"
```

**Budget:** $5-8/dia
**Bidding:** Manual CPC max $2,00

**Indicadores de sucesso S1 (Dia 21):**

| Métrica | Partida | Projetado S1 |
|---|---|---|
| Campanhas ativas | 0 | 8-10 |
| Tracking implementado | ❌ Não | ✅ GA4 + GTM + Conversões |
| LPs com CTA funcional | ❌ Broken | ✅ Funcionando |
| Search CPA (reativação) | — | $150-250 (estimado inicial) |
| PMax CPA | — | $70-100 (estimado) |
| Budget diário total | $0 | $190/dia |
| Gasto mensal estimado | $0 | $5.700 |

---

### SPRINT 2 — ACELERAÇÃO: REMARKETING + EXPANSÃO + TESTES
**Período:** Dias 22-50

**Objetivo:** Ativar funil completo, escalar o que funciona, iniciar remarketing.

#### Ação 2.1 — Ativar Remarketing (Dias 22-28)

**Dependência crítica:** GA4/GTM precisa estar instalado (Ação 1.1).

1. **Display Remarketing:**
   - Campanha: `[V4] [DSP] [GOO] [REM] — Site Visitors 30d`
   - Budget: $8-10/dia
   - Criativos: Oferta de whitepaper técnico + case studies
   - Audiência: Visitantes do site (30 dias)

2. **RLSA (Remarketing Lists for Search Ads):**
   - +25% bid adjustment para visitantes anteriores
   - Aplicar em TODAS as campanhas Search

3. **YouTube Remarketing:**
   - Audiência: Quem assistiu vídeos da Atlas Copco no YouTube
   - Anúncio: In-stream com CTA de "Request a Quote"

#### Ação 2.2 — Escalar Search com Base nos Primeiros Dados (Dias 28-35)

**Após 2 semanas de dados reais:**
1. Identificar as 3 campanhas Search com melhor CPA
2. Escalar budget em 20-30%
3. Pausar ou reduzir campanhas com CPA > $300
4. Criar novos RSAs baseados nos search terms que converteram
5. Ajustar tCPA com base nos dados reais (não nos históricos de 2022)

#### Ação 2.3 — Criar Conteúdo MOF (Nutrição) (Dias 30-40)

**Baseado na persona B2B (jornada longa), criar ofertas de nutrição:**

| Oferta | Formato | Objetivo |
|---|---|---|
| "Guia de Compra de Compressores Industriais" | PDF (LP com formulário) | Capturar lead MOF |
| "Calculadora de ROI: Diesel vs Elétrico" | Interativo | Engajar e qualificar |
| "Case Study: Economia com Oil-Free" | PDF | Prova social |
| "Webinar: Eficiência Energética em Compressores" | Inscrição | Lead qualificado |

**Campanha:** Discovery + Display para distribuir esses conteúdos.
**Budget:** $10-15/dia

#### Ação 2.4 — Reativar Campanhas com CPA Histórico Alto com Nova Estrutura (Dias 35-42)

Campanhas que tiveram CPA alto ($600-900) mas podem funcionar com nova abordagem:

| Campanha | CPA Histórico | Nova Abordagem |
|---|---|---|
| CG: Pumps - Submersible Pumps | $708 | Segmentar por aplicação (mineração, municipal, irrigação) em vez de genérico |
| CG: Compressors - General | $768 | Substituir por micro-intenções (specs, cfm, uso específico) |
| CG: Pumps - High Head | $870 | Focar em indústrias específicas (óleo e gás, química) |

#### Ação 2.5 — Iniciar Testes A/B (Dias 30-50)

| Variável | Controle (A) | Variação (B) |
|---|---|---|
| Headline | Técnica ("300 cfm compressor") | Benefício ("Reduce downtime") |
| CTA | "Request Quote" | "Talk to an Engineer" |
| Tom | Profissional | Urgência ("Stock available") |
| LP | Página de produto | LP dedicada com calculadora |

**Regra:** 2 semanas por teste. 2-3 RSAs por ad group.

#### Ação 2.6 — Criar Dashboard de Performance (Dias 45-50)

**Métricas para o dashboard mensal:**

| Métrica | Por quê |
|---|---|
| CPA por campanha | Qual produto está entregando melhor ROI |
| Search Impression Share | Estamos aparecendo nas buscas certas? |
| CTR por ad group | Os anúncios estão relevantes? |
| Taxa de conversão por LP | A página está convertendo? |
| Leads por origem (Search vs PMax vs Display) | Qual canal funciona melhor para cada produto |

**Indicadores de sucesso S2 (Dia 50):**

| Métrica | Partida | Projetado S2 |
|---|---|---|
| Campanhas ativas | 0 | 12-15 |
| Search CPA | — | $150-200 |
| PMax CPA | — | $60-80 |
| Remarketing ativo | ❌ | ✅ Display + RLSA + YouTube |
| Remarketing CPA | — | $80-120 |
| Conversões totais/semana | 0 | 15-25 |
| Budget diário | $0 | $250-300/dia |

---

### SPRINT 3 — ESCALA E REFINO
**Período:** Dias 51-90

**Objetivo:** Escalar com base preditiva, otimizar com TOC, consolidar operação.

#### Ação 3.1 — Ciclo TOC #1 (Dias 51-60)

**Com 6+ semanas de dados:**

1. **Identificar gargalo:** Qual campanha/produto está limitando o crescimento geral?
2. **Explorar:** Transferir budget das campanhas piores para a gargalo
3. **Subordinar:** Pausar ou reduzir campanhas com CPA 2x acima da média
4. **Elevar:** Criar variações do que funciona (novos RSAs, novas audiências, novas LPs)
5. **Repetir:** Reavaliar a cada 2 semanas

#### Ação 3.2 — Escalar PMax com Segmentação de Audiência (Dias 55-65)

**A PMax histórica ($70 CPA) foi o canal mais eficiente. Escalar com:**
1. Asset groups separados por produto (Compressors, Pumps, Generators)
2. Audiências: In-Market (Industrial Equipment) + Custom Intent (keywords de produto)
3. Search themes por produto + aplicação
4. Budget: $40-50/dia por campanha PMax (vs $25-30 inicial)

#### Ação 3.3 — Ativar Campanha Discovery (TOF) (Dias 60-70)

**Campanha:** `[V4] [DSC] [GOO] [TOF] — Industrial Prospecting`

- Audiências: In-Market (Industrial Equipment, Construction, Mining)
- Criativos: Whitepaper "Future of Industrial Air" + Calculadora de ROI
- Budget: $10-15/dia
- Objetivo: Capturar leads MOF para nutrir

#### Ação 3.4 — Refinar Quality Score com SEO (Dias 65-80)

**Ações coordenadas com a auditoria SEO:**
1. Resolver H1 vazio e title genérico nas LPs de produto
2. Implementar Product schema nas páginas de equipamento
3. Verificar velocidade mobile (target > 80 PageSpeed)
4. Consolidar subdomínios ou pelo menos verificar domínio principal no Google Ads

**Impacto no Ads:** Cada ponto de QS acima de 5 reduz CPC em 10-15%.

#### Ação 3.5 — Planejamento Q3-Q4 (Dias 80-90)

**Com base nos 3 meses de dados:**
1. Definir orçamento sazonal por linha de produto
2. Identificar oportunidades de expansão (novos produtos, novos mercados)
3. Preparar estratégia para feiras/eventos (Utility Expo, CONEXPO)
4. Documentar learnings e recomendações para o cliente

**Indicadores de sucesso S3 (Dia 90):**

| Métrica | Partida | Projetado S3 |
|---|---|---|
| Campanhas ativas | 0 | 15-18 |
| Search CPA | — | $120-180 |
| PMax CPA | — | $50-70 |
| Display/Remarketing CPA | — | $60-90 |
| Discovery CPA | — | $100-150 |
| Conversões totais/mês | 0 | 80-120 |
| Gasto mensal | $0 | $8.000-10.000 |
| Quality Score médio Search | — | 5-7 |

---

## FASE 4 — ORK DA OPERAÇÃO DE MÍDIA

### Objective

Reativar e escalar a operação de Google Ads da Atlas Copco USA como canal previsível de geração de leads B2B industriais, com CPA sustentável e alinhado ao ciclo de venda longo.

### Key Results

| KR | Métrica | Hoje | S1 (D21) | S2 (D50) | S3 (D90) | Meta |
|---|---|---|---|---|---|---|
| KR1 | Search CPA | — | < $250 | < $200 | < $180 | < $150 |
| KR2 | PMax CPA | — | < $100 | < $80 | < $70 | < $60 |
| KR3 | Volume conversões/mês | 0 | 20-30 | 40-60 | 80-120 | 150+ |
| KR4 | Campanhas ativas | 0 | 8-10 | 12-15 | 15-18 | 20+ |
| KR5 | Tracking funcional | ❌ | ✅ | ✅ | ✅ | ✅ |
| KR6 | QS médio Search | — | 3-4 | 4-6 | 5-7 | 7+ |

### Initiatives

| KR | Initiative | Responsável |
|---|---|---|
| KR1 | Reativação Search com tCPA + match types restritivos | Media Buyer |
| KR2 | Reativação PMax com asset groups separados + search themes | Media Buyer |
| KR3 | Remarketing + Discovery + Conteúdo MOF | Media Buyer + Copy |
| KR4 | Plano de reativação por prioridade (S1 → S2 → S3) | Media Buyer |
| KR5 | Instalação GA4 + GTM + conversões offline (ação #1) | Media Buyer + Cliente |
| KR6 | Coordenação com auditoria SEO (LPs, schema, speed) | Media Buyer + SEO |

---

## FASE 5 — FRAMEWORK DE OTIMIZAÇÃO (TOC)

### Cadência de Revisões

| Frequência | O que revisar |
|---|---|
| **A cada 3 dias** | Criativos (CTR, CPC, Ad Strength) — pausar o pior, escalar o melhor |
| **Semanal** | Search terms novos, negativas, audiências, budget allocation |
| **Quinzenal** | Funil completo (TOF → MOF → BOF taxa de passagem), LPs |
| **Mensal** | Estrutura de conta, alocação orçamentária global, ORK |

### Indicadores de Alerta

| Indicador | Threshold | Ação |
|---|---|---|
| Search IS | < 20% | Investigar QS e budget |
| CTR Search | < 2% | Revisar criativos e match type |
| CPC Search | > $8 | Pausar e revisar keyword + QS |
| PMax CPA | > $150 | Revisar asset groups + audience signals |
| Remarketing CPA | > $120 | Revisar criativos e segmentação |
| Anúncio em "Learning" | > 7 dias | Revisar segmentação |
| Custo/Conv produto específico | > $300 | Pausar ou reestruturar completamente |

---

## FASE 6 — ORÇAMENTO E PROJEÇÕES

### Alocação Orçamentária por Sprint

| Sprint | Search | PMax | Display | Discovery | Brand | Total/mês |
|---|---|---|---|---|---|---|
| **S1** (lançamento) | $2.100 | $2.400 | $0 | $0 | $210 | **~$4.710** |
| **S2** (aceleração) | $3.000 | $3.600 | $450 | $300 | $240 | **~$7.590** |
| **S3** (escala) | $4.500 | $4.500 | $600 | $450 | $300 | **~$10.350** |

### Projeção de Retorno (90 dias)

| Produto/ Canal | Investimento | Conversões Est. | CPA Est. |
|---|---|---|---|
| PMax (todos) | $10.500 | 150-175 | $60-70 |
| Search Compressors | $5.400 | 30-40 | $135-180 |
| Search Pumps | $3.600 | 12-18 | $200-300 |
| Search Generators | $2.700 | 12-15 | $180-225 |
| Search Sustainability | $1.800 | 8-12 | $150-225 |
| Remarketing | $1.650 | 18-22 | $75-92 |
| Brand | $1.050 | 15-25 | $42-70 |
| Discovery (nutrição) | $750 | 5-8 | $94-150 |
| **Total** | **$27.450** | **260-315** | **$87-105** |

---

## FASE 7 — RECOMENDAÇÕES DE RISCO

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| Cliente sem acesso GTM para tracking | Média | **CRÍTICO** — sem remarketing nem dados de conversão | Prioridade #1 das ações; escalar para cliente |
| Landing Pages com PageSpeed baixo | Alta | Alto — QS não sobe além de 5 | Coordenar com auditoria SEO já existente |
| Subdomínios causando reprovação de anúncios | Média | Alto — campanhas podem não aprovar | Verificar domínio principal no Google Ads |
| Quality Score histórico expirado (3 anos) | Certa | Médio — CPC inicial será alto nas primeiras semanas | Budget conservador nas primeiras 2 semanas |
| Ciclo de venda B2B longo sem leads visíveis | Alta | Médio — cliente pode achar que não está funcionando | Educar sobre ciclo de venda B2B; configurar leads offline |
| Equipamento de alto ticket sem formulário de captura | Alta | Alto — tráfego chega na LP e não tem onde converter | Prioridade #2 (Ação 1.2) |

---

## CHECKLIST DE EXECUÇÃO (ORDEM CRÍTICA)

### S1 — Dias 1-21

- [ ] **D1-5** Instalar GA4 + GTM + configuração de conversões
- [ ] **D5-10** Verificar e corrigir LPs (CTA, formulário, speed)
- [ ] **D10-12** Reestruturar nomenclatura e arquitetura de conta
- [ ] **D12-18** Reativar PMax (4 campanhas: Compressors, Pumps, Generators, Sustainability)
- [ ] **D12-18** Reativar Search (4 campanhas: Mid-Sized Diesel, Air Compressors Large, Generators Specs, Centrifugal Pumps)
- [ ] **D15-18** Adicionar negativas (~30 termos) + revisar search terms
- [ ] **D15-18** Substituir ETAs obsoletos por RSAs novos
- [ ] **D18-21** Criar campanha de Brand ($5-8/dia)
- [ ] **D18-21** Criar campanha de Concorrentes ($10-15/dia)
- [ ] **D21** Revisão S1: OKRs, métricas, próximos passos

### S2 — Dias 22-50

- [ ] **D22-28** Ativar remarketing Display + RLSA + YouTube
- [ ] **D28-35** Escalar Search com base nos primeiros dados reais
- [ ] **D30-40** Criar conteúdo MOF (whitepapers, calculadora, case studies)
- [ ] **D30-40** Ativar campanha Discovery para distribuição de conteúdo
- [ ] **D35-42** Reativar campanhas com CPA histórico alto com nova estrutura
- [ ] **D30-50** Iniciar testes A/B (headline, CTA, tom, LP)
- [ ] **D45-50** Criar dashboard de performance
- [ ] **D50** Revisão S2: OKRs, métricas, próximos passos

### S3 — Dias 51-90

- [ ] **D51-60** Ciclo TOC #1 — identificar gargalo e realocar budget
- [ ] **D55-65** Escalar PMax com segmentação de audiência
- [ ] **D60-70** Ativar/expandir campanha Discovery (TOF)
- [ ] **D65-80** Refinar QS com ações coordenadas de SEO (LPs, schema, speed)
- [ ] **D80-90** Planejamento Q3-Q4 + documentação de learnings
- [ ] **D90** Revisão S3: OKRs finais, recomendações Q3-Q4

---

## FLUXOGRAMA DE DECISÃO

```
Se tracking demorar > 10 dias para implementar:
  → Pausar plano até tracking funcionar
  → Sem GA4/GTM, qualquer gasto em Ads é cego
  → Usar calls como métrica de conversão alternativa

Se CPA Search > $300 nas primeiras 2 semanas:
  → Normal — QS está frio (3 anos parado)
  → Manter budget, revisar RSAs e negativas
  → Se não melhorar em 4 semanas: pausar e reestruturar

Se PMax não gastar o budget:
  → Verificar se asset groups têm "Ad Strength" boa
  → Verificar search themes e audience signals
  → Aumentar lances gradualmente (+10% a cada 3 dias)

Se anúncios forem reprovados:
  → Verificar Policy Manager
  → Causa mais provável: domínio não verificado ou LP com PageSpeed baixo
  → Verificar se subdomínios estão verificados no Google Ads

Se o cliente não aprovar aumento de budget:
  → Manter budget mínimo ($100-150/dia)
  → Focar apenas nas 3 melhores campanhas (PMax Core + Mid-Sized Diesel + Brand)
  → Resultado será mais lento, mas ainda positivo
```

---

## NOTAS IMPORTANTES

1. **Dados históricos são de 2021-2022.** O mercado de anúncios B2B mudou significativamente desde então. Use os históricos como referência, não como verdade absoluta.
2. **Quality Score precisa ser reconstruído do zero.** Espere CPC mais alto nas primeiras 2-4 semanas até o Google re-aprender a relevância dos anúncios.
3. **B2B industrial tem ciclo longo.** Não espere dezenas de conversões na primeira semana. O foco inicial é gerar dados de qualidade, não volume.
4. **Sinergia SEO/Ads é crítica.** A auditoria SEO já identificou gaps que impactam diretamente o Quality Score. Resolver esses gaps é pré-requisito para escalar com CPA baixo.
5. **Projeções são estimativas.** Resultados reais dependem de execução correta, resposta do mercado e variáveis fora do nosso controle.