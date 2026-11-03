# Bing Ads — Plano de correção

**Cliente:** Premium Cleaning Services
**Conta:** `[V4] [BING] [AQ] B2B Commercial Cleaning NJ NY`
**Período analisado:** 04/10/2026 a 02/11/2026 (30 dias)
**Fontes:** export de 13 relatórios em `campanhas/Bing/` (campaign, adgroup, ad, keyword, search term, negativas, auction insight, geo, age, device, schedule, audience, assets)

---

## 0. Diagnóstico em uma frase

A campanha não tem problema de verba — tem problema de **para quem entrega**. Gastou 17% do orçamento disponível e comprou 76% de tráfego fora do alvo a um CPC 64% mais caro que o tráfego bom.

| Métrica | Total | Search | Audience |
|---|---|---|---|
| Impressões | 9.026 | 1.768 | **7.258 (80%)** |
| Cliques | 95 | 68 | 27 |
| CTR | 1,05% | **3,85%** | **0,37%** |
| CPC | $1,96 | $2,11 | $1,60 |
| Gasto | $186,59 | $143,37 | **$43,22** |
| Conversões | 2 | 1 | 1 (residencial) |
| CPA | $93,30 | — | — |

- Orçamento: **$36/dia** (~$1.080/mês) · gasto real **$6,22/dia = 17%**
- Impression share: **8,54%** · Abs. top: **5,30%**
- Optimization Score: **30,2%**
- Conversão válida: **1** (a outra veio de CEP 08850, residencial, via `ntp.msn.com`)

---

## 1. Negativas — P0 (o maior vazamento)

### 1.1 Evidência: o que o search terms mostrou

161 termos no período, 55 com gasto:

| Bucket | Termos | Cliques | Gasto | % do gasto | CPC |
|---|---|---|---|---|---|
| Marca / concorrente | 33 | 16 | **$59,06** | **43%** | $3,69 |
| Serviço fora do escopo (hazmat, mold, HVAC) | 21 | 29 | **$25,59** | **18%** | $0,88 |
| Geo / idioma fora do ICP | 10 | 4 | $11,46 | 8% | $2,87 |
| Supply-side (quem procura contrato) | 2 | 2 | $5,49 | 4% | $2,75 |
| Pesquisa / lista | 4 | 1 | $3,32 | 2% | $3,32 |
| **Dentro do alvo** | **91** | **15** | **$33,78** | **24%** | **$2,25** |

**76% do gasto de search ($104,92 de $138,70) foi para fora do alvo.**

Os 10 cliques mais caros do mês:

| Termo | Custo | Motivo |
|---|---|---|
| commercial cleaning services near 9410 s. lacienga blvd | $4,99 | endereço colado |
| mongoose cleaning warthogs | $4,90 | marca |
| commercial cleaning | $4,89 | genérico (aceitável) |
| janico inc official website | $4,86 | marca |
| afl-cio affiliate carpet cleaning companies nyc corp | $4,76 | marca/junk |
| cleaining businesses white plains ny | $4,66 | fora da área |
| skyler cleaning serviced | $4,64 | marca |
| elite compania de limpieza new york | $4,51 | espanhol, LP em inglês |
| stanley steemer cleaning cost estimate calculator | $4,35 | marca + pesquisa |
| cintas ptac cleaning | $4,22 | marca + HVAC |

### 1.2 A lista atual está quebrada

`NegativeKeywords.csv` tem 82 linhas, mas **9 estão coladas** e não bloqueiam nada:

| Está hoje | Deveria ser |
|---|---|
| `rentalrent` | rental · rent |
| `toolswindow cleaning` | tools · window cleaning |
| `duct cleaningair duct` | duct cleaning · **air duct** |
| `deep cleaning housemiami` | deep cleaning house · **miami** |
| `austinlos angeles` | austin · **los angeles** |
| `phoenixdenver` | phoenix · **denver** |
| `texaswhat is` | **texas** · what is |
| `priceschecklist` | **prices** · checklist |
| `how to starttraining` | how to start · **training** |

São **18 termos perdidos**. Prova: `commercial cleaning services prices` custou $4,45 e `air duct cleaning commercial` $0,51 — nenhum dos dois está barrado.

Além disso a lista protege contra o problema errado: bloqueia DIY, produto e equipamento (`amazon`, `walmart`, `bissell`, `hoover`, `shark`, `supplies`, `kit`), mas **não bloqueia nenhuma marca de concorrente nem nenhum serviço adjacente**.

E a coluna `Added / Excluded` está vazia nos 161 termos — nenhuma negativa veio do relatório.

### 1.3 Blocos para adicionar

**A. Marcas e concorrentes**
```
janico
cbre
osborne
rampart
cleanoutlook
skyler
lisbon cleaning
wyette
service pro
servpro
cintas
b line
stanley steemer
jan pro
amda
floorfool
allied cleaning
trillium
rinse
thumbtack
angi
homeadvisor
bark
yelp
care.com
mold inspection
air quality
```

**B. Serviço adjacente / fora do escopo**
```
hazardous
hazmat
decontamination
decontaminate
biohazard
crime scene
mold remediation
mold testing
mildew
water damage restoration
fire damage restoration
hvac
air conditioner
air conditioning
ac cleaning
ptac
duct cleaning
air duct
dryer vent
gutter
septic
pest
```

**C. Supply-side**
```
cleaning contracts
contracts to clean
find cleaning contracts
bid on cleaning
building to clean
janitorial bid
```

**D. Geo e idioma**
```
white plains
red bank
miami
chicago
houston
atlanta
austin
los angeles
san francisco
seattle
dallas
phoenix
denver
boston
california
florida
texas
nevada
ohio
zurich
zürich
limpieza
servicios de limpieza
aire acondicionado
```

**E. Pesquisa, emprego e DIY**
```
list of
prices
price list
how much
calculator
cost estimate
checklist
what is
how does
definition
template
training
course
cleaning jobs
janitorial jobs
cleaning salary
hiring
vacancy
```

### 1.4 Decisão pendente — hood cleaning

A lista atual bloqueia `hood cleaning`, `exhaust cleaning` e `NFPA 96`, mas o site tem `/restaurant-hood-exhaust-cleaning-nj` e o programa editorial tem o artigo D1 sobre NFPA 96.

**Escolher:**
- **(a)** É serviço ativo → **remover essas 3 negativas** e criar ad group próprio + keywords
- **(b)** Não é serviço → manter e não investir em conteúdo de hood

### 1.5 Como aplicar

1. Bing Ads → campanha B2B → **Configurações da campanha → Palavras-chave negativas**
2. Colar os blocos A–E (uma por linha). O Bing aceita várias de uma vez.
3. Corrigir as 9 linhas coladas (item 1.2).
4. Definir match type: **Phrase** para marcas compostas (`jan pro`, `stanley steemer`) e **Broad** para termos únicos (`hazmat`, `limpieza`).
5. Aplicar também como **lista de negativas compartilhada** para cobrir futuras campanhas.
6. Revisar search terms **toda semana** por 4 semanas e alimentar a lista.

> Arquivo pronto para importar: `negativas-import-bing.csv` nesta mesma pasta.

---

## 2. Keywords — P0

### 2.1 Pausar (trazem marca e consulta embaralhada)

| Keyword | Gasto | O que trouxe |
|---|---|---|
| cleaning companies commercial | $13,00 | "janico inc official website", "cbre/cleaners" |
| cleaning commercial companies | $9,73 | "osborne janitorial services" |
| commercial cleaning services list | $11,80 | "afl-cio affiliate carpet…", "hazardous material" |
| commercial cleaning local | $4,51 | "elite compania de limpieza new york" |
| services restaurant cleaning | $2,90 | "restaurant cleaning company in nyc" (ok) |
| services cleaning restaurant | $1,64 | variação embaralhada |
| cleaning in restaurant | $1,15 | variação embaralhada |
| commercial window washing | $0,00 | fora de escopo |
| professional resturant cleaning new york | $0,75 | **typo duplicado** — corrigir ou remover |

### 2.2 Manter só como Exact

`commercial cleaning services` ($48,80 em phrase, 29 cliques) e `commercial cleaning company` ($19,25) → criar versão **Exact** e deixar a phrase com lance menor, ou pausar a phrase.

### 2.3 Criar como Exact (vieram do search terms e estão no alvo)

```
nyc retail cleaning services
retail cleaning nyc
store cleaners nyc
restaurant cleaning company nyc
restaurant cleaners new york
restaurant cleaners nyc
professional cleaning services office
office cleaning services new york
janitorial services for offices new york city
commercial building maintenance companies new york
commercial cleaning provider quote
hotel cleaning services nyc
grease removal service
```

### 2.4 Reativar das campanhas pausadas (10–15 por vertical)

480+ keywords estão paradas em três campanhas: `Premium-Q1-2026` (Hotel Staffing 142 kw), `Restaurants | Night Cleaning` (186), `Post-Construction` (156). São exatamente os segmentos que o conteúdo orgânico já cobre.

Prioridade:
1. **Hotel** — `hotel cleaning services`, `hotel housekeeping services`, `hotel deep cleaning NJ`, `boutique hotel cleaning nyc`
2. **Restaurant** — `restaurant deep cleaning`, `commercial kitchen deep cleaning`, `restaurant cleaning services near me`
3. **Post-construction** — `post construction cleaning nj`, `construction final cleaning services`

---

## 3. Geo — P0

| Local | Cliques | Impressões | Gasto |
|---|---|---|---|
| New York, NY (city) | 71 | 5.316 | **$139,91** |
| Manhattan, NY (city) | 12 | 2.596 | $26,14 |
| Newark, NJ (city) | 10 | 580 | $15,34 |
| Jersey City, NJ (city) | 2 | 346 | $5,20 |
| Middlesex, NJ | 0 | 17 | $0 |
| Monmouth Junction, NJ | 0 | 16 | $0 |
| Somerset, NJ | 0 | 53 | $0 |
| Union, NJ | 0 | 95 | $0 |
| Morris Plains, NJ | 0 | 7 | $0 |

**89% do gasto em NY ($166,05) · 11% em NJ ($20,54).**

### 3.1 Ações

1. **Remover** (fora do ICP, 0 clique): Middlesex, Monmouth Junction, Morris Plains, Somerset.
2. **Manter** NYC + Manhattan, mas **sem duplicar** — hoje as duas estão listadas e podem sobrepor.
3. **Adicionar** as cidades do ICP que não existem na conta:
   - **Bergen:** Hackensack, Paramus, Fort Lee, Teaneck, Englewood, Ridgewood
   - **Essex:** Newark (já existe), Montclair, Livingston, Irvington, Bloomfield
   - **Hudson:** Jersey City (já existe), Hoboken, Secaucus, Bayonne, Weehawken
   - **Passaic:** Paterson, Clifton, Wayne
   - **Union:** Elizabeth, Linden, Plainfield
4. **Conferir a opção de local:** está em *"People in"* ou *"People in or interested in"*? Consultas de **Nevada** e **Ohio** geraram impressão, e uma da **Suíça** ("anbieter zürich novadura baureinigung büro") gerou **clique pago de $0,57**. Isso só acontece com segmentação aberta. → marcar **"People in"**.
5. **Lances por local:** +20% no corredor de luxo Manhattan (zips 100xx) · +10% Newark/Jersey City · 0% nas demais NJ.

---

## 4. Dispositivo e horário — P0

### 4.1 Dispositivo (está invertido)

| Dispositivo | Ajuste | Cliques | Impressões | CTR | CPC | Gasto |
|---|---|---|---|---|---|---|
| Desktop | **+10%** | 37 | 7.024 | 0,53% | **$3,16** | **$116,97** |
| Smartphone | 0% | 58 | 1.965 | **2,95%** | **$1,20** | $69,62 |
| Tablet | 0% | 0 | 37 | 0% | — | $0 |

**Correção:** Desktop **−30%** · Smartphone **+15%** · Tablet **−100%**

### 4.2 Horário (quinta não roda)

| Dia | Cliques | Impressões | CTR | Gasto |
|---|---|---|---|---|
| Segunda | 12 | 1.282 | 0,94% | $25,58 |
| Terça | 10 | 1.521 | 0,66% | $20,57 |
| Quarta | 20 | 2.313 | 0,86% | $58,65 |
| Quinta | — | — | — | **ausente** |
| Sexta | 15 | 1.678 | 0,89% | $26,32 |
| Sábado | 13 | 750 | **1,73%** | $13,67 |
| Domingo | 25 | 1.482 | **1,69%** | $41,80 |

**Correção:**
1. **Adicionar quinta** 08:00–21:00.
2. **+15%** sábado e domingo (CTR 1,7% vs 0,66–0,94% nos dias úteis).
3. **Estender até 23:00** nos ad groups Hotel e Restaurant (GMs pesquisam fora do horário comercial).
4. `AdScheduleUseSearcherTimeZone = False` — confirmar que a conta está em **Eastern Time**, senão a janela está deslocada.

---

## 5. Lances e conversões — P0

### 5.1 O algoritmo está aprendendo com o lead errado

- Estratégia: **MaxConversions com tCPA $95**
- Volume: **2 conversões/mês** (Bing pede ~15 para aprender)
- Uma das duas é **residencial** (CEP 08850, `ntp.msn.com`, "Home / Other")

**Correção:**
1. Criar **goals separados** no UET `97249867`: formulário comercial · formulário residencial · ligação · WhatsApp
2. **Excluir o residencial** da otimização
3. Trocar para **ECPC com cap $2,50–3,00** (ou Manual CPC) até atingir 15 conv/mês
4. Validar se o formulário (iframe LeadConnector) está disparando o evento — sem isso nenhum lance automático funciona
5. Adicionar **valor de conversão** (ticket médio do caso Madison: $2.800/semana) para o algoritmo priorizar lead grande

---

## 6. Landing pages — P1 (causa do QS baixo)

**100% dos anúncios apontam para `https://premiumcleaningnj.com/`.** O Quality Score é 4 no Core e 4 nas Offices.

As páginas corretas existem e respondem 200 (verificado):

| Ad group | Landing page |
|---|---|
| Ad Group 1 — Core | `/commercial-cleaning-services-nj` |
| Ad Group 2 — Office | `/office-cleaning` |
| Ad Group 4 — Restaurant | `/restaurant-cleaning` |
| Ad Group 5 — Hotel | `/hotel-cleaning` |
| NYC / luxury (novo) | `/commercial-cleaning-new-york-city` |
| Case Madison (sitelink) | `/cases/purple-style-labs-madison-avenue-post-construction-daily-cleaning` |

Páginas extras disponíveis: `/commercial-carpet-cleaning` · `/commercial-kitchen-cleaning-nj` · `/hotel-housekeeping-services` · `/restaurant-hood-exhaust-cleaning-nj` · `/janitorial-services-nj` · `/post-construction-cleaning-nj`

> Atenção: `/commercial-cleaning-services` e `/hotel-cleaning-services` **dão 404**. Não usar.

**Manter o tracking:** `utm_source=bing&utm_medium=cpc&utm_campaign=b2b_commercial_cleaning&utm_content={adgroup}` — só ajustar o `utm_content` por grupo.

---

## 7. Anúncios — P1

### 7.1 Três headlines com contagem de caracteres vazando

| Está no ar | Deveria ser |
|---|---|
| `Health Code Ready Always (25)` | Health Code Ready Always |
| `10+ Years of Excellence (24)` | 10+ Years of Excellence |
| `Night Shift Kitchen Crews (26)` | Night Shift Kitchen Crews |

O número entre parênteses é a contagem de caracteres da planilha que entrou no texto.

### 7.2 Copy cruzada entre segmentos

- **RSA Restaurant** tem 3 headlines de hotel: `Hotel Cleaning NJ & NYC`, `Guest Room Deep Clean Pros`, `Free Hotel Assessment`
- **RSA Hotel** tem 3 de restaurante/cozinha: `Restaurant Cleaning NJ & NY`, `Commercial Kitchen Experts`, `Free Kitchen Assessment`
- **RSA Core** tem hotel + cozinha: `Trusted by NJ Hotels`, `Guest Room Deep Clean Pros`, `Commercial Kitchen Experts`

O ad group Hotel recebeu **114 impressões e 0 cliques**.

### 7.3 RSA Hotel (hoje 15 headlines, 3 vazando)

| # | Headline | Descrição |
|---|---|---|
| 1 | Hotel Cleaning NJ & NYC | |
| 2 | Guest Room Deep Clean Pros | |
| 3 | Free Hotel Assessment | |
| 4 | Housekeeping That Shows Up | |
| 5 | 5-Star Guest Experiences | |
| 6 | Same Crew Every Visit | |
| 7 | Bonded & Insured Crews | |
| 8 | Lobby, Rooms & Back of House | |
| 9 | Trusted by NJ Hotels | |
| 10 | 98% Client Retention | |
| 11 | Since 2012 | |
| 12 | Night & Weekend Crews | |
| 13 | Walkthrough Quote in 48h | |
| 14 | Serving Bergen to Manhattan | |
| 15 | Call (973) 204-2310 | |

| # | Description |
|---|---|
| 1 | Guest rooms, public areas and back of house. One crew, one supervisor, one standard. |
| 2 | No rotating crews, no missed shifts. Dedicated teams that learn your property. |
| 3 | Bonded, insured, background-checked. 98% retention since 2012 across NJ and NYC. |
| 4 | Request a walkthrough and get a written scope with room-credit pricing. |

### 7.4 RSA Restaurant (hoje 15 headlines, 3 vazando)

| # | Headline |
|---|---|
| 1 | Restaurant Cleaning NJ & NY |
| 2 | Commercial Kitchen Experts |
| 3 | Night Shift Kitchen Crews |
| 4 | Health Code Ready Always |
| 5 | Grease, Floors, Hoods, Restrooms |
| 6 | Spotless Before Service |
| 7 | Same Crew Every Visit |
| 8 | Free Kitchen Assessment |
| 9 | 10+ Years Restaurant Care |
| 10 | Bonded & Insured |
| 11 | Pass Inspection With Records |
| 12 | Overnight, Zero Downtime |
| 13 | Since 2012 · NJ & NYC |
| 14 | Serving Newark to Manhattan |
| 15 | Call (973) 204-2310 |

| # | Description |
|---|---|
| 1 | Kitchen, dining room, bar and restrooms cleaned overnight. Ready before first service. |
| 2 | Trained crews for NJ and NY food establishments. Inspection-ready documentation. |
| 3 | No rotating crews, no missed shifts. Dedicated night teams that know your line. |
| 4 | Free kitchen assessment with a written scope and per-visit pricing. |

### 7.5 RSA Office (hoje 10 headlines)

| # | Headline |
|---|---|
| 1 | Office Cleaning NJ & NYC |
| 2 | Professional Office Cleaning |
| 3 | Same Crew Every Visit |
| 4 | Background-Checked Crews |
| 5 | No Strangers In Your Office |
| 6 | Daily & Nightly Service |
| 7 | Free Office Assessment |
| 8 | Dedicated Account Manager |
| 9 | Green Cleaning Available |
| 10 | Call (973) 204-2310 |

| # | Description |
|---|---|
| 1 | Offices, retail and medical spaces — one accountable partner. Licensed and insured. |
| 2 | No rotating crews, no missed shifts. Dedicated teams that know your building. |
| 3 | QA checklists every visit, green products on request, backup staff on call. |
| 4 | Trusted by NJ and NY businesses since 2012. Free assessment this week. |

### 7.6 RSA Core

| # | Headline |
|---|---|
| 1 | Commercial Cleaning NJ & NY |
| 2 | Licensed & Insured Team |
| 3 | Same Crew Every Visit |
| 4 | Premium Janitorial Services |
| 5 | 10+ Years of Excellence |
| 6 | Free Facility Assessment |
| 7 | Night & Weekend Crews |
| 8 | Bonded & Insured Crews |
| 9 | Trusted by Madison Ave Shops |
| 10 | 98% Client Retention |
| 11 | Since 2012 |
| 12 | Serving NJ & NYC |
| 13 | Offices, Retail & Medical |
| 14 | Written Scope in 48h |
| 15 | Call (973) 204-2310 |

| # | Description |
|---|---|
| 1 | NJ and NY commercial cleaning. Background-checked crews. Free facility audit. |
| 2 | No rotating crews, no missed shifts. Dedicated teams that know your building. |
| 3 | Trusted by luxury retailers on Madison Ave. Request a custom quote today. |
| 4 | Offices, retail, medical spaces — one trusted partner. Licensed, insured, 24/7. |

### 7.7 A oferta de 25%

`25% Off Your First Cleaning` é o headline **mais servido** (3.414 impressões) com o **pior CTR** (0,47%). A campanha `[PROMO] August 25% Off Deep Cleaning` está pausada, mas a oferta segue no ar em 3 RSAs.

**Decisão:** se a oferta expirou, remover dos 4 RSAs. Se vale, fixar prazo e colocar em campanha própria.

### 7.8 O que manter (CTR comprovado)

| Headline | CTR |
|---|---|
| Licensed & Insured Team | **4,85%** |
| Same Crew Every Visit | 2,17% |
| Premium Janitorial Services | 1,78% |
| 24/7 Emergency Crews | 1,47% |
| 10+ Years of Excellence (24) | 1,46% |
| Trusted by Madison Ave Shops | 0,78% |

| Description | CTR |
|---|---|
| No rotating crews, no missed shifts… | **3,05%** |
| Offices, retail, medical spaces — one trusted partner… | 2,53% |
| Your office cleaned by trained, uniformed teams. QA checklists… | 2,51% |

### 7.9 O que matar

| Headline | CTR |
|---|---|
| No Strangers In Your Office | 0,23% |
| Green Cleaning Available | 0,42% |
| 25% Off Your First Cleaning | 0,47% |
| Free Office Assessment | 0,51% |

### 7.10 Preencher Path 1 e Path 2

Estão vazios nos 13 anúncios. Espaço grátis no display URL:

| Ad group | Path 1 | Path 2 |
|---|---|---|
| Core | Commercial-Cleaning | NJ-NY |
| Office | Office-Cleaning | NJ-NYC |
| Restaurant | Restaurant | Night-Cleaning |
| Hotel | Hotel-Cleaning | NJ-NYC |
| NYC | Manhattan | Luxury-Retail |

---

## 8. Extensões — P1 (hoje: zero)

Só existem 32 headlines e 15 descriptions. Sem sitelink, callout, telefone, local, imagem ou structured snippet. Impacto direto em CTR e em área ocupada.

**Sitelinks (6)**

| Texto | Descrição | URL |
|---|---|---|
| Commercial Cleaning | Offices, retail and medical spaces | `/commercial-cleaning-services-nj` |
| Office Cleaning | Daily and nightly janitorial contracts | `/office-cleaning` |
| Hotel Cleaning | Guest rooms, public areas, back of house | `/hotel-cleaning` |
| Restaurant Cleaning | Kitchens, dining rooms, bars | `/restaurant-cleaning` |
| Carpet & Floor Care | Extraction, encapsulation, tile and grout | `/commercial-carpet-cleaning` |
| Madison Avenue Case | Flagship retail, post-construction + daily | `/cases/purple-style-labs-madison-avenue-post-construction-daily-cleaning` |

**Callouts (6):** `Since 2012` · `Bonded & Insured` · `98% Client Retention` · `★ 5,0 · 43 reviews` · `Same Crew Every Visit` · `Background-Checked`

**Structured snippet (Services):** Commercial Cleaning · Office Cleaning · Hotel Cleaning · Restaurant Cleaning · Carpet Care · Post-Construction

**Extensão de telefone:** (973) 204-2310
**Extensão de local:** 107 Vesey St, Newark, NJ 07105 (+ área: Bergen, Essex, Passaic, Hudson, Union + NYC)
**Extensão de imagem:** 4 imagens (equipe, lobby de hotel, cozinha, carpet)

---

## 9. Auction Insights — leitura

| Domínio | IS | Sobreposição | Topo pág. | Abs. topo |
|---|---|---|---|---|
| **You** | **21,52%** | 100% | 46,09% | **30,86%** |
| thumbtack.com | 12,16% | 16,85% | 45,16% | 3,23% |
| abm.com | 9,59% | 19,02% | 42,86% | 20,00% |
| angi.com | 7,95% | 16,85% | 67,74% | 16,13% |
| homeadvisor.com | 6,08% | 9,78% | 61,11% | 16,67% |
| moldinspectioninstitute.com | 4,91% | 14,67% | **100%** | 3,70% |
| care.com | 4,56% | 10,33% | 31,58% | 10,53% |
| airqualitytesters.com | 4,44% | 13,04% | **100%** | 8,33% |
| uline.com | 2,92% | 1,09% | 50,00% | 0,00% |
| trilliumfacility.com | 2,69% | 4,89% | 11,11% | 11,11% |
| walmart.com | 2,69% | 8,70% | 50,00% | 50,00% |
| bark.com | 2,57% | 7,07% | 30,77% | 0,00% |
| amazon.com | 2,57% | 2,17% | 50,00% | 25,00% |
| yelp.com | 1,64% | 3,80% | 42,86% | 28,57% |
| alliedcleaningservices.com | 1,64% | 3,80% | 28,57% | 14,29% |
| rinse.com | 1,52% | 2,17% | 25,00% | 25,00% |
| servpro.com | 1,40% | 1,63% | 100,00% | 100,00% |

**Três conclusões:**

1. **Você é o maior anunciante do leque** — 21,52% de IS, quase o dobro do Thumbtack — e mesmo assim aparece em 46% no topo e 31% no absoluto. Está pagando para ser o mais presente e não o mais visível.
2. **Prova independente do vazamento:** está leiloando contra `moldinspectioninstitute.com`, `airqualitytesters.com`, `care.com` (cuidado domiciliar), `rinse.com` (lavanderia) e `uline/walmart/amazon` (fornecedores). Nenhum é seu concorrente. É a mesma assinatura de query errada do search terms.
3. **Concorrente real que importa:** `trilliumfacility.com` e `alliedcleaningservices.com` — IS baixo mas sobreposição em 100% do topo de página. Vale monitorar preço e copy.

**Ação:** confirmar em `Campanha → Configurações → Distribuição de anúncios` que **Audience Network está desmarcada** e que a syndication do MSN também. A conversão residencial veio de `ntp.msn.com`.

---

## 10. Higiene — P2

1. Três campanhas pausadas (`Premium-Q1-2026`, `Search-Campaign_070826_152517`, `[PROMO] August 25% Off`) têm **9 anúncios com status Enabled**. Se alguém reativar, sobe oferta de agosto.
2. Ad group `Draft` e keyword `teste` na `Search-Campaign_070826` — remover.
3. **Não existe Ad Group 3** (vai de 2 para 4) — renumerar.
4. Nomenclatura `Premium-Q1-2026` em novembro — padronizar para `[V4] [BING] [AQ]` + vertical + data.
5. Listas de audience (+15%) com **12 impressões** no mês — inertes. Criar **remarketing de visitantes** (30/90 dias) e excluir quem já converteu.
6. Idade: +10% em 35–49 e 50–64 **sem nenhuma base de conversão**. Deixar 0% até ter 15 conv.
7. Sem valor de conversão e sem importação de conversões offline.

---

## 11. Ordem de execução

### Bloco 1 — estancar (30 min)
- [ ] Desligar Audience Network / syndication
- [ ] Aplicar as negativas A–E + corrigir as 9 linhas coladas
- [ ] Pausar as 7 keywords embaralhadas
- [ ] Desktop −30% · Mobile +15% · Tablet −100%
- [ ] Adicionar quinta ao schedule

### Bloco 2 — converter (1h)
- [ ] Trocar as 5 landing pages por ad group
- [ ] Substituir os 4 RSAs (sem copy cruzada, sem "(25)")
- [ ] Resolver a oferta de 25%
- [ ] Subir 6 sitelinks + callouts + telefone + local
- [ ] Corrigir geo (remover 4, adicionar 20, "People in", +20% Manhattan)
- [ ] MaxConversions → ECPC cap $2,50–3,00

### Bloco 3 — semana seguinte
- [ ] Separar goals no UET e excluir residencial
- [ ] Revisar search terms → alimentar negativas
- [ ] Reativar 10–15 keywords de Hotel / Restaurant / Post-Construction
- [ ] Criar ad group **Manhattan Luxury Corridor**
- [ ] Preencher Path 1 / Path 2 nos 13 anúncios

---

## 12. Como medir se funcionou

| Métrica | Hoje | Meta 30 dias |
|---|---|---|
| % do gasto fora do alvo | 76% | **< 20%** |
| CPC médio | $1,96 | **< $1,60** |
| CTR | 1,05% | **> 2,0%** |
| Conversões válidas | 1 | **4–6** |
| CPA | $93,30 | **< $60** |
| Impression share | 8,54% | **> 15%** |
| % do gasto em Search | 77% | **> 95%** |

Com o mesmo orçamento e CPC de $2,25 do tráfego bom, os **$105 hoje desperdiçados** compram **~47 cliques no alvo** — hoje você tem 15.

---

## 13. Três respostas que faltam

1. **Hood cleaning é serviço ativo?** (está negativado mas tem página e artigo)
2. **A conta está em Eastern Time?**
3. **A oferta de 25% ainda vale?**

---

*Documento gerado a partir dos 13 relatórios de 04/10 a 02/11/2026. Dados de Bing Ads, nenhum valor estimado.*
