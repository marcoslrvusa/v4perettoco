# ESTRATÉGIA DE REESTRUTURAÇÃO — GOOGLE ADS SEARCH
## Conserva Irrigation of Greater Scottsdale · Julho 2026

**Data:** 1 Julho 2026
**Autor:** Estrategista de Mídia Paga · Traffic Reporting Squad
**Para:** Account Manager → Karina (Conserva)
**Contexto:** Preparação para pico de verão em Arizona (100°F+) + reestruturação da campanha Search

---

## SUMÁRIO EXECUTIVO

A campanha Search da Conserva virou um "Frankenstein" — 7 campanhas pausadas, 4 estratégias de lance diferentes em 60 dias, 12 keywords sem impressão, 7 ad groups de instalação fragmentados. O resultado: Search gerou **3 conversões em 16 dias com CPA de $181** — enquanto o PMAX, com o dobro de budget, gerou 13 conversões.

**O problema não é "falta de otimização" — é excesso de otimizações sem direção.** A cada semana uma mudança nova enterra o aprendizado anterior.

**A recomendação é clara:**
1. Search precisa de **budget mínimo de $50/dia** para ter chance de competir (hoje $27/dia, perdendo 42-49% das impressões)
2. Search deve ser **reduzida a 1 campanha consolidada** com 3-4 ad groups temáticos e 15-20 keywords de alta intenção (exact + phrase com geo)
3. **Governança rígida**: nenhuma mudança de bid strategy, orçamento ou estrutura por 4 semanas após implementação
4. **Julho é a hora de escalar** o AG3 do PMAX com criativos de "Summer Ready" e Emergency Repair no Search com budget extra

---

## 1. DIAGNÓSTICO ESTRATÉGICO — Por que a Search está quebrada?

### 1.1 O Frankenstein: muitas campanhas, nenhuma aprendendo

A conta tem **13 campanhas criadas**, sendo apenas **2 ativas** (Search + PMAX). As 11 pausadas representam tentativas anteriores que foram abandonadas sem documentação do que funcionou ou não:

| Campanha | Status | Budget Original | Motivo Provável |
|---|---|---|---|
| V4 - SEARCH - SERVICES LP | Ended | $27 | Encerrada, sucedida por SERVICES |
| V4 - SEARCH - SERVICES | **Ativa** | $27 | Atual — 0 conv na Semana 2 |
| V4 | ONGOING | SEARCH | MAX CONVERSÕES | LP 2 | Paused | $45 | "most ads disapproved" |
| V4 | ONGOING | SEARCH | MAX CONVERSÕES | LP 2 SCALCON | Paused | $10 | "most ads disapproved" |
| V4 | ONGOING | SEARCH | MAX CLICKS | COMPETITORS | Paused | $18 | "most ads disapproved" |
| [V4] [AQ] CONSERVA - B2C Search - Services | Paused | $30 | Substituída |
| [V4] [AQ] B2B Services | Paused | $20 | Sem volume |
| V4 - SEARCH - SERVICES LP + Localização | Paused | $27 | Campaign ended |
| V4 - SEARCH - BRAND | Paused | $10 | Sem necessidade |
| [V4] [Ligações Diretas] | Paused | $10 | "most ads disapproved" |

**Impacto:** Cada nova campanha é um "reset" no aprendizado do Google. O algoritmo precisa de dados históricos de conversão para otimizar lances. Toda vez que uma campanha é pausada e outra criada, o aprendizado recomeça do zero.

### 1.2 Bid Strategy trocada 3x em 60 dias — learning period destruído

A estratégia de lances da Search ativa foi alterada múltiplas vezes:

```
Maximize Conversions → (troca) → Target CPA → (troca) → Maximize Conversions
```

Cada troca reinicia o **learning period** de 7-14 dias. Com apenas $27/dia, cada learning period consome ~$270-378 sem retorno — mais da metade do budget mensal da Search queimado em "aquecimento".

**Diagnóstico:** A Search nunca saiu do learning period nos últimos 60 dias. Nunca vimos o que ela realmente pode entregar.

### 1.3 Orçamento insuficiente: $27/dia vs $45-50 necessário

| Métrica | Atual (Jun 1-16) | Referencial |
|---|---|---|
| Search Impression Share | 24,36% | Mínimo aceitável: 30%+ |
| Lost IS (rank) | 49,12% | (não é budget, é rank/QS) |
| Lost IS (budget) | ~42% (Semana 2) | Deveria ser 0-15% |
| CPC médio Search | $12,95 | Benchmark irrigação local nos EUA: $6-9 |

**Análise de budget necessário:**

Com CPC médio de $12,95 e 3 conversões em 16 dias:
- $543,79 ÷ 42 cliques = $12,95/click (CPC alto, sinal de QS baixo)
- 3 conv ÷ 42 cliques = 7,14% CVR (até ok para serviço local)
- $27/dia ÷ $12,95 = ~2 cliques/dia (insuficiente para qualquer dado estatístico)

Com $50/dia e CPC estimado de $8-9 (após melhorar QS com geo keywords):
- ~5-6 cliques/dia
- Com CVR de 5-7% → 1 conv a cada 2-3 dias → ~10-15 conv/mês
- CPA projetado: $100-120 (vs $181 atual)

### 1.4 Installation fragmentado em 7 ad groups — e SEM impressões

O grupo de instalação estava espalhado em **7 ad groups diferentes**, em **3 campanhas distintas**. Resultado: 3 impressões em 90 dias na campanha ativa.

A consolidação feita em 24 Jun foi **correta** — agora há 1 grupo único `[V4] [New] Irrigation_System_Installation`. Mas sem budget, continuará sem impressões.

### 1.5 B2B: tentativa sem volume

Ad group B2B com keywords genéricas ("facility management", "property management", "HOA irrigation") e **1 impressão em 16 dias**. O problema:
- Keywords broad match sem qualificador local
- Sem landing page dedicada
- Budget diluído no mesmo pool da Search B2C

### 1.6 URL migrada para HTTP

A migração para HTTP em Abril pode ter impactado Quality Score. Se ainda não foi corrigida para HTTPS, esta é **prioridade #1 técnica** antes de qualquer outra otimização.

---

## 2. PAPEL DE CADA CANAL — Search vs PMAX vs Bing

### 2.1 A Matriz de Responsabilidades

| Canal | Papel Primário | Papel Secundário | Budget (Atual) | Budget (Recomendado) |
|---|---|---|---|---|
| **Google Search** | Capturar **intenção imediata** — reparos de emergência + instalação com alta intenção | Palavras sazonais de verão | $27/dia | **$50/dia** |
| **Google PMAX** | **Volume de leads** — cobertura full-funil via inventário combinado (Search+Shopping+Display+YouTube+Gmail) | Sazonal (AG3 Summer Ready) + Remarketing | $59/dia | **$59/dia** (manter) + $10 sazonal Julho |
| **Bing Ads** | **Extensão incremental** — baixo CPC, baixa concorrência | Cobertura de audiência 35+ anos (público Microsoft) | $0 (planejado) | **$20/dia** (após Search estabilizar) |
| **LSA (Local Services Ads)** | **Conversão de emergência** — leads por chamada de alta intenção | Já existe, não temos dados de breakdown | Não mapeado | Manter |

### 2.2 O que Search faz (e o que NÃO faz)

| Search DEVE fazer | Search NÃO deve fazer |
|---|---|
| ✅ Capturar buscas de **alta intenção** ("sprinkler repair near me", "irrigation installation scottsdale") | ❌ Competir por termos informacionais amplos ("sprinkler system", "irrigation systems") |
| ✅ Emergency/repair com **ação imediata** ("same day sprinkler repair") | ❌ Tentar capturar busca de marca (provavelmente já clicam no orgânico) |
| ✅ Installation com geo qualificada ("sprinkler installation chandler") | ❌ Disputar termos de alto volume sem geo (CPC alto, conversão baixa) |
| ✅ Sazonal de verão ("summer irrigation tune up scottsdale") | ❌ B2B genérico sem landing page dedicada |

### 2.3 O que PMAX faz (e o que NÃO faz)

| PMAX DEVE fazer | PMAX NÃO deve fazer |
|---|---|
| ✅ **Volume** — escalar com alcance em múltiplos inventários | ❌ Substituir Search para capturar intenção imediata |
| ✅ Remarketing + prospection via sinais de audiência | ❌ Ser usado com criativos genéricos (AG1 e AG2 hoje são clones) |
| ✅ Sazonal via AG3 com criativos temáticos | ❌ Receber mais budget sem diferenciação criativa entre AGs |
| ✅ Testar novas audiências que a Search não alcança | |

### 2.4 Oportunidade Bing Ads (Julho-Agosto)

Bing tem CPCs 30-50% menores que Google no mercado de serviços locais dos EUA. Com $20/dia:
- Público 35+ (proprietários de imóveis — perfil ideal para irrigação)
- Menos concorrência (concorrentes locais preocupados com Google)
- **Recomendação:** Estruturar em Julho, lançar em Agosto após Search estabilizar

---

## 3. ARQUITETURA DE CAMPANHA RECOMENDADA

### 3.1 Proposta: 1 Campanha Search, 4 Ad Groups

```
Campanha: [V4] [SEARCH] CONSERVA IRRIGATION — GREATER SCOTTSDALE
  ├── Budget: $50/dia
  ├── Bid Strategy: Maximize Conversions (sem tCPA por 4 semanas)
  ├── Local: Scottsdale + Phoenix + Chandler + Gilbert + Paradise Valley (raio 30 mi)
  ├── Language: English
  ├── Network: Google Search Network (SEM Display)
  │
  ├── Ad Group 1: [Emergency] Repair & Service
  │   ├── Keywords: Exact + Phrase com geo (alta intenção)
  │   ├── CPC médio esperado: $8-12
  │   └── Landing page: conservairrigation.com/sprinkler-repair/
  │
  ├── Ad Group 2: [New] Irrigation Installation
  │   ├── Keywords: Exact + Phrase com geo
  │   ├── CPC médio esperado: $6-9
  │   └── Landing page: conservairrigation.com/irrigation-system-installation/
  │
  ├── Ad Group 3: [Seasonal] Summer Ready (JUN-SET)
  │   ├── Keywords: Phrase + Broad (com negativas)
  │   ├── CPC médio esperado: $5-7
  │   └── Landing page: conservairrigation.com/summer-ready/
  │
  └── Ad Group 4: [Commercial] B2B (budget secundário)
      ├── Keywords: Exact + Phrase específicas B2B
      ├── Budget: $5-8/dia (do pool de $50)
      └── Landing page: conservairrigation.com/commercial-services/
```

### 3.2 Justificativa da Arquitetura

**Por que 1 campanha e não 3-4 separadas?**
- Com budget total de $50/dia, separar em múltiplas campanhas fragmenta ainda mais
- 1 campanha = 1 learning period, 1 bid strategy, 1 conjunto de dados para o algoritmo
- Ad groups bem segmentados são suficientes para dar sinais temáticos ao Google

**Por que Maximize Conversions sem tCPA?**
- A campanha nunca teve dados estáveis — qualquer tCPA seria baseado em dados não confiáveis
- Max Conv permite que o Google otimize livremente por 4 semanas
- Após 4 semanas com dados consistentes, avaliar se tCPA faz sentido

### 3.3 Estratégia de Lances

| Fase | Bid Strategy | Duração | Objetivo |
|---|---|---|---|
| **Fase 1 (Lançamento)** | Maximize Conversions | Semanas 1-4 (Julho) | Coletar dados de conversão, estabilizar learning period |
| **Fase 2 (Otimização)** | Maximize Conversions + tCPA opcional ($100-120) | Semanas 5-8 (Agosto) | Controlar custo por conversão com base nos dados da Fase 1 |
| **Fase 3 (Escala)** | Target CPA ($100-110) ou Maximize Conversions com budget maior | Setembro+ | Escalar com custo controlado |

### 3.4 Budget Allocation por Ad Group (dentro dos $50/dia)

| Ad Group | % do Budget | $/dia | Justificativa |
|---|---|---|---|
| [Emergency] Repair & Service | 40% | $20 | Maior intenção, maior volume de buscas, emergências de verão |
| [New] Irrigation Installation | 30% | $15 | Precisamos testar com budget real — 0 conv em 90 dias |
| [Seasonal] Summer Ready | 20% | $10 | Sazonal, captura pico de verão |
| [Commercial] B2B | 10% | $5 | Teste controlado, sem expectativa de conversão imediata |

---

## 4. ESTRATÉGIA DE KEYWORDS

### 4.1 Metodologia

Baseada na planilha "New Keywords Conserva.xlsx" e nos search terms report real da conta.

**Princípios:**
1. **Exact Match com geo** para alta intenção (o que converte)
2. **Phrase Match com geo** para captura de variações (o que expande)
3. **Broad Match PROIBIDO** nas primeiras 4 semanas — só com negativas robustas depois
4. **Negativas agressivas** para excluir tráfego irrelevante

### 4.2 Keywords Recomendadas por Ad Group

#### Ad Group 1: [Emergency] Repair & Service (10-12 keywords)

**Prioridade ALTA — Ativar imediatamente:**

| Keyword | Match Type | Volume Mensal | CPC Est. | Justificativa |
|---|---|---|---|---|
| `[sprinkler repair scottsdale]` | Exact | — | $6-8 | Já teve clique e conversão |
| `[sprinkler repair near me]` | Exact | 14.8k | $6.16 | Alta intenção transacional |
| `[irrigation repair scottsdale]` | Exact | — | $7-9 | Já teve impressão, alta intenção |
| `"sprinkler repair phoenix"` | Phrase | — | $6-8 | Expansão geográfica |
| `"irrigation repair phoenix az"` | Phrase | — | $6-8 | Expansão geográfica |
| `"lawn sprinkler repair"` | Phrase | 2.9k | $4.82 | Intenção comercial |
| `"sprinkler valve repair"` | Phrase | 2.4k | $7.17 | Intenção informacional mas com alta CPC (vale o teste) |
| `[same day sprinkler repair scottsdale]` | Exact | — | $8-10 | Emergência — maior intenção |
| `"emergency sprinkler repair"` | Phrase | — | $8-10 | Sazonal verão |

**Prioridade MÉDIA — Ativar após 2 semanas:**

| Keyword | Match Type | Justificativa |
|---|---|---|
| `"irrigation system repair near me"` | Phrase | Já está na conta mas sem impressão — testar com geo |
| `"sprinkler system repair"` | Phrase | 12.1k/mês — testar com CPC controlado |
| `"lawn sprinkler repair near me"` | Phrase | 3.6k/mês — transacional |

#### Ad Group 2: [New] Irrigation Installation (8-10 keywords)

**Prioridade ALTA:**

| Keyword | Match Type | Volume Mensal | CPC Est. | Justificativa |
|---|---|---|---|---|
| `[irrigation system installation scottsdale]` | Exact | — | $4-6 | Já está na conta |
| `[sprinkler system installation scottsdale]` | Exact | — | $5-6 | Já está na conta |
| `"sprinkler installation chandler"` | Phrase | — | $5-6 | Geo específica |
| `"irrigation installation phoenix"` | Phrase | — | $4-6 | Geo específica |
| `"lawn sprinkler system installation"` | Phrase | — | $4-6 | Intenção de instalação |
| `"sprinkler system installation near me"` | Phrase | 8.1k | $5.51 | Transacional |
| `"sprinkler installation near me"` | Phrase | 3.6k | $6.09 | Transacional |

**Importante:** Installation tem **mais volume** que repair (sprinkler system installation = 14.8k/mês) mas **CPC mais baixo** ($4.70 vs $6.80 de repair). Isso significa que installation PODE ser mais rentável — mas nunca foi testada com budget adequado.

#### Ad Group 3: [Seasonal] Summer Ready (5-7 keywords)

**Prioridade ALTA para Julho:**

| Keyword | Match Type | Justificativa |
|---|---|---|
| `"summer sprinkler tune up scottsdale"` | Phrase | Sazonal verão |
| `"irrigation system inspection"` | Phrase | Preventivo antes do calor |
| `"sprinkler system check"` | Phrase | Preventivo |
| `"smart irrigation installation scottsdale"` | Phrase | Intersecção sazonal + tech |
| `"save water sprinkler system"` | Phrase | Economia de água no verão |

#### Ad Group 4: [Commercial] B2B (5-7 keywords)

**Prioridade BAIXA — Teste controlado:**

| Keyword | Match Type | Justificativa |
|---|---|---|
| `"commercial irrigation services scottsdale"` | Phrase | Específica B2B |
| `"HOA irrigation maintenance"` | Phrase | Público HOA |
| `"property management irrigation"` | Phrase | Público property manager |

### 4.3 Negative Keywords Obrigatórias

**Aplicar em nível de campanha (todas as contas):**

| Grupo | Negativas | Motivo |
|---|---|---|
| DIY | `how to`, `diy`, `tutorial`, `guide`, `learn`, `manual` | Não queremos "faça você mesmo" |
| Parts/Supplies | `parts`, `supplies`, `replacement`, `head`, `valve` (se for só venda) | A Conserva é serviço, não loja |
| Free info | `free`, `cost`, `price` (atenção: pode cortar leads qualificados) | Só negativar se não venderem |
| Rental | `rental`, `rent` | Não alugam equipamento |
| Education | `classes`, `course`, `certification` | Não é escola |
| Other locations | `Tampa`, `Florida`, `Minneapolis`, `Miami` | Keywords da planilha que não servem para Scottsdale |

### 4.4 Keywords da Planilha que NÃO devem ser usadas

A planilha "New Keywords Conserva.xlsx" contém **dados do mercado nacional dos EUA**, não do Arizona especificamente. Algumas keywords são irrelevantes ou contraproducentes:

| Keyword | Motivo para Excluir |
|---|---|
| `nasal irrigation system` | Equipamento médico, NÃO irrigação de jardim |
| `drip irrigation system` (drip kit, drip line) | Volume alto ($18.1k) mas é DIY/loja — baixa intenção de serviço |
| `chicken watering system` | Criação de animais, não irrigação residencial |
| `fire sprinkler system` | Segurança contra incêndio, não irrigação |
| `rain bird sprinkler system` | Informativo/marca — baixa intenção de serviço |
| `backflow testing... tampa bay` | Tampa/FL — localização errada |
| `diy lawn sprinkler system` | DIY — não queremos |

---

## 5. GOVERNAÇA DE OTIMIZAÇÕES — Anti-Frankenstein Framework

### 5.1 O Problema Central

> "A cliente (Karina) pede otimizações constantes e o account manager implementa sem dar tempo para maturação."

Este é o comportamento que CRIOU o Frankenstein. Cada otimização individual faz sentido no momento — mas o acúmulo sem direção estratégica destrói o sistema.

### 5.2 Framework de Decisão: A Regra do "Espera 4 Semanas"

**Princípio fundamental:** Toda mudança estrutural exige **4 semanas de dados estáveis** antes da próxima mudança.

```
Mudança → 4 semanas de estabilidade → Avaliação → Próxima mudança (ou rollback)
```

Isso significa que **de 1º a 28 de Julho, NADA muda na estrutura da Search** depois da implementação inicial.

### 5.3 O Que Pode e O Que Não Pode Mudar

| Tipo de Mudança | Pode Fazer? | Frequência | Quem Decide |
|---|---|---|---|
| **Bid strategy** | ❌ NÃO | Nunca em <30 dias | Estrategista |
| **Budget da campanha** | ⚠️ Limitado | Apenas aumento (+$10-15/dia) em Julho | Account + Estrategista |
| **Pausar keywords** | ✅ SIM | A cada 7 dias, se 0 impressões ou 0 cliques em 14 dias | Account Manager |
| **Adicionar keywords** | ✅ SIM | A cada 14 dias, máx. 3 por vez | Account Manager |
| **Ajustar CPC** | ❌ NÃO (Max Conv não usa) | N/A | N/A |
| **Criativos (headlines)** | ✅ SIM | A cada 14 dias | Copy + Account |
| **Landing page** | ⚠️ Cuidado | Só se CVR < 2% por 30 dias | Estrategista + Cliente |
| **Segmentação geográfica** | ❌ NÃO | Mensal | Estrategista |
| **Negative keywords** | ✅ SIM | Semanal (baseado em search terms report) | Account Manager |

### 5.4 Calendário de Otimizações (Julho-Agosto)

| Semana | O que muda | O que NÃO muda |
|---|---|---|
| **S1 (1-7 Jul)** | ✅ IMPLEMENTAÇÃO: Nova estrutura, budget $50/dia, keywords novas | Bid strategy, criativos, landing pages |
| **S2 (8-14 Jul)** | ✅ Search terms review, adicionar negativas, pausar keywords sem cliques | Bid strategy, budget, estrutura |
| **S3 (15-21 Jul)** | ✅ Avaliar dados de 2 semanas. Se sem conversões ainda, revisar | Bid strategy, estrutura |
| **S4 (22-28 Jul)** | ✅ Avaliação de 4 semanas. Primeiro ponto de decisão real | Estrutura (aguardar avaliação) |
| **S5 (29 Jul - 4 Ago)** | ⚠️ DECISÃO: Manter, ajustar tCPA ou reestruturar | Baseado na avaliação da S4 |

### 5.5 Documentação Obrigatória

Toda mudança deve ser documentada com:

```
DATA: [dd/mm]
O QUE: [descrição clara]
POR QUE: [justificativa baseada em dado]
QUEM: [responsável]
PRAZO PRÓXIMA AVALIAÇÃO: [dd/mm]
```

Esta documentação vai para o `mission-control/combinados.md` e é revisada nos check-ins quinzenais.

### 5.6 Como Dizer "Não" para a Cliente (sem perder o relacionamento)

**Técnica V4 — Médico vs Garçom:**
- Cliente pede otimização → Garçom implementa (FRANKENSTEIN)
- Cliente pede otimização → **Médico explica por que esperar** (GOVERNAÇA)

**Scripts para Karina:**

> *"Karina, entendo que você quer ver melhoras o mais rápido possível. Mas cada mudança que a gente faz agora, mesmo que pareça pequena, reinicia o relógio de aprendizado do Google. A melhor coisa que podemos fazer é deixar a nova estrutura rodar por 4 semanas — e aí sim, com dados reais, decidir o próximo passo. Depois de 4 semanas, se não funcionar, a gente muda tudo. Mas antes disso, é chute."*

> *"Você se lembra que trocamos a estratégia de lance 3 vezes nos últimos 60 dias? Cada troca custou ~$300 de aprendizado e a gente nunca viu o resultado. Agora vamos fazer diferente: implementamos uma vez, esperamos, e avaliamos com dados. Combinado?"*

**Regra de Ouro:** Se Karina insistir em uma mudança que viola a governança, o Account Manager leva para o check-in com o Squad — **nunca implementa sozinho**.

---

## 6. SAZONALIDADE DE VERÃO — Aproveitando Julho (Pico em AZ)

### 6.1 O Contexto

Julho em Scottsdale/Arizona é **mês de pico de calor** (100°F+/38°C+). Isso significa:

| Efeito | Impacto na Demanda |
|---|---|
| ✅ Sistemas de irrigação trabalham no limite | Aumento de REPAROS DE EMERGÊNCIA |
| ✅ Contas de água disparam | Interesse em SMART IRRIGATION (economia) |
| ✅ Proprietários querem gramado verde | Instalação de sistemas novos |
| ✅ Turistas saem, moradores ficam | Demanda local estável |

### 6.2 Estratégia Search para Julho — "Beat the Heat"

**Mensagens sazonais nos RSAs (Responsive Search Ads):**

| Posição | Headline (Reparo) | Headline (Instalação) | Headline (Summer Ready) |
|---|---|---|---|
| H1 | **Same-Day Sprinkler Repair** | Beat the Heat — New System | Summer Ready — Free Checkup |
| H2 | Emergency Service Available | Smart Irrigation Scottsdale | Save 60% on Water Bills |
| H3 | 100°F+? Don't Let Your Lawn Die | Custom Installation, Free Quote | Free SES Inspection |
| H4 | 50+ 5-Star Reviews | Upgrade to Smart Control | Summerize Your System |
| H5 | Call Now — We Fix Fast | Save Water, Save Money | Don't Let June Heat Kill Your Lawn |

**Descrições sazonais:**

| Grupo | Description 1 | Description 2 |
|---|---|---|
| Repair | Is your sprinkler struggling in 100°F+ heat? Same-day repair in Scottsdale. Licensed pros. Call now. | Don't let a broken sprinkler kill your lawn in this heat. Fast repair. Free quote. Family-owned. |
| Installation | Beat the Arizona heat with smart irrigation. Save 60% on water. Free design consultation. Call today. | New system installation in Scottsdale. Toro & Hunter certified. Control from your phone. Free quote. |
| Summer Ready | Free SES inspection before summer peak. Finds leaks and inefficiencies. Save water and money. Licensed & insured. | Summer is here — is your irrigation ready? Free system checkup. Smart upgrades available. Call now. |

### 6.3 Budget Sazonal: Aumento Programado

| Período | Budget Search | Budget PMAX | Total | Motivo |
|---|---|---|---|---|
| 1-15 Jul (pico calor) | $55/dia | $65/dia | $120/dia | Máxima demanda de emergência |
| 16-31 Jul | $50/dia | $59/dia (volta normal) | $109/dia | Estabilização |
| 1-15 Ago | $45-50/dia | $59/dia | $104-109/dia | Pós-pico, manter |
| 16-31 Ago | $40-45/dia | $50-59/dia | $90-104/dia | Preparando para queda do outono |

### 6.4 Keywords Sazonais para Julho (Ad Group Summer Ready)

**Ativar APENAS em Julho:**

| Keyword | Match Type | Por que funciona em Julho |
|---|---|---|
| `"summer sprinkler tune up"` | Phrase | Proprietários preparando sistema |
| `"irrigation system inspection near me"` | Phrase | Preventivo antes do calor extremo |
| `"sprinkler system check"` | Phrase | Manutenção preventiva |
| `"smart irrigation installation scottsdale"` | Phrase | Economia de água na seca |
| `"save water sprinkler system"` | Phrase | Contas de água altas no verão |
| `"water wise irrigation"` | Phrase | Tendência de sustentabilidade |
| `"irrigation system upgrade"` | Phrase | Substituir sistemas antigos |
| `"free sprinkler inspection"` | Phrase | Lead magnet sazonal |

### 6.5 Landing Page: Página Sazonal Dedicada

Se não existir, criar uma página `conservairrigation.com/summer-ready/` com:
- "Beat the Scottsdale Heat — Free SES Inspection"
- Call to action: agendamento de inspeção gratuita
- Depoimentos de verão
- Menção à economia de água (60%)
- Selo "Licensed & Insured", Toro & Hunter Certified

### 6.6 PMAX AG3 — Escalar o que Funciona

O AG3 (Summer Ready) já é o único asset group convertendo do PMAX (6 conv, CPA $106,36 em Jun 1-16). **Para Julho:**
- Manter budget do PMAX em $59/dia (ou aumentar para $65/dia)
- AG3 com prioridade de budget (já está recebendo mais)
- **Não criar AG novo** — escalar o que funciona antes de testar
- Refresh de criativos a cada 2 semanas (novas imagens de verão)

### 6.7 Plano de Contingência: Se Search Não Converter em Julho

Se após 4 semanas (até 28 Jul) a Search ainda estiver com 0-3 conversões e CPA >$150:

| Cenário | Ação |
|---|---|
| Installation com 0 conv | Abandonar Installation no Search, migrar budget para Repair + PMAX AG2 |
| Repair com CPA >$150 | Aumentar negativas, reduzir para exact match apenas |
| Search geral falhando | Reduzir Search para $20/dia (só repair), realocar $30 para PMAX |
| PMAX AG3 mantendo CPA <$120 | Aumentar budget PMAX para $80-90/dia, Search vira complementar |

---

## ANEXOS

### A. Timeline de Implementação (Julho)

| Data | Ação | Responsável | Status |
|---|---|---|---|
| 1 Jul | Implementar nova estrutura Search (1 campanha, 4 ad groups) | Account Manager | A FAZER |
| 1 Jul | Aumentar budget Search para $50/dia | Account Manager | A FAZER |
| 1 Jul | Verificar/corrigir URL HTTPS | Account Manager | A FAZER |
| 1 Jul | Aplicar negative keywords em nível de campanha | Account Manager | A FAZER |
| 1 Jul | Ativar keywords sazonais de Julho no AG Summer Ready | Account Manager | A FAZER |
| 3 Jul | Briefing Lucas para criativos PMAX AG1/AG2 (diferenciados) | Account Manager | PENDENTE |
| 7 Jul | Search terms report review + adicionar negativas | Account Manager | RECORRENTE |
| 8-14 Jul | S2 review — avaliar primeiros dados (7 dias) | V4 + Account | AGENDADO |
| 15 Jul | S3 review — avaliar 2 semanas. Decisão: manter ou ajustar | V4 + Account | AGENDADO |
| 22-28 Jul | **S4 — AVALIAÇÃO CRÍTICA** 4 semanas. Decisão de continuidade | TODOS | AGENDADO |
| Semanal | Documentar mudanças em mission-control/combinados.md | Account Manager | RECORRENTE |

### B. KPIs para Julho

| KPI | Atual (Jun) | Meta Julho | Como Medir |
|---|---|---|---|
| Search Conv/Semana | 1-2 | **3-5** | Google Ads |
| Search CPA | $181 | **<$120** | Google Ads |
| Search Impression Share | 19-24% | **>30%** | Google Ads |
| PMAX Conv/Mês | 13 | **15-20** | Google Ads |
| PMAX CPA Geral | $140 | **<$120** | Google Ads |
| AG3 CPA | $106 | **<$100** | Google Ads |
| Installation Conv | 0 | **>1** | Google Ads (primeira conv em 90+ dias) |
| CTR Search | 3,82% | **>5%** | Google Ads |
| CPC Search | $12,95 | **<$9** | Google Ads |

### C. Alertas de Risco

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| Cliente pede mudança antes de 4 semanas | ALTA | ALTO | Framework de governança + script "Médico vs Garçom" |
| Budget $50/dia não aprovado | MÉDIA | ALTÍSSIMO | Sem budget a Search não tem chance — cenário de contingência |
| URL HTTP não corrigida | MÉDIA | ALTO | Prioridade #1 técnica |
| Rotatividade de account manager interrompe execução | BAIXA | ALTO | Documentação em mission-control + check-ins semanais |
| Pico de demanda de verão sobrecarrega capacidade da Conserva | BAIXA | MÉDIO | Alinhar com Karina capacidade de atendimento antes de escalar |

---

**Documento elaborado por:** Estrategista de Mídia Paga · Traffic Reporting Squad · V4 Company
**Para:** Account Manager → Conserva Irrigation of Greater Scottsdale
**Versão:** 1.0 · 1 Julho 2026
**Próxima revisão:** 8 Julho 2026 (pós-primeira semana de dados)
