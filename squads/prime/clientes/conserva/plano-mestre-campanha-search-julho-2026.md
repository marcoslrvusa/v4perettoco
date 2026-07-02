# PLANO MESTRE — Campanha Google Ads Search
## Conserva Irrigation of Greater Scottsdale · Julho 2026

**Produzido por:** Traffic Reporting Squad
**Líder:** Marcos Luciano (Tech Lead)
**Especialistas:** Analista de Dados · Mídia Paga · Media Buyer · Copy Team
**Data:** 1 de Julho de 2026
**Para:** Account Manager → Cliente Karina

---

## ═══════════════════════════════════════
## SUMÁRIO EXECUTIVO
## ═══════════════════════════════════════

### O Problema
A campanha Search da Conserva virou um **Frankenstein** — 7 ad groups fragmentados, 13 campanhas criadas (11 pausadas), bid strategy trocada 3x em 60 dias, e **93% do budget preso em 1 ad group** que tem CPA de $214. Installation está **morto** (18 impressões no mês). A cliente pede otimização toda semana e o time implementa sem critério.

### Dado que Muda Tudo
| Métrica | Search | PMAX |
|---|---|---|
| Budget/dia | **$27** | **$59** |
| Gasto mensal | **$693** | **$1.821** |
| CPA real | **$138,60** | **$140,07** |
| Melhor Ad Group CPA | **$24,93** (Spring Startup) | **$106** (AG3 Summer) |
| Pior Ad Group CPA | **$214** (Emergency Repair) | **$0** (AG1/AG2) |

**O Search custa o mesmo que o PMAX mas recebe 1/3 do budget.**  
**O melhor grupo (Spring Startup, CPA $25) recebe 7% do budget. O pior (Emergency, CPA $214) recebe 93%.**

### O Plano em 3 Frases
1. **Reestruturar a Search** em 1 campanha → 4 ad groups temáticos com budget dedicado de $55/dia
2. **Parar de mexer** — 30 dias de estabilidade obrigatória para o algoritmo aprender
3. **Escalar o que já funciona** — Seasonal Spring Startup (CPA $25) e PMAX AG3 Summer Ready (6 conv)

---

## ═══════════════════════════════════════
## PARTE 1: DIAGNÓSTICO CONSOLIDADO
## ═══════════════════════════════════════

### 1.1 Performance Real da Search (Junho 2026)

| Métrica | Search | PMAX | LSA* | Blended |
|---|---|---|---|---|
| Investimento | $692,99 | $1.820,60 | ~$2.500 | ~$5.000 |
| Conversões | 5 | 13 | ~55 | 73 |
| **CPA Real** | **$138,60** | **$140,07** | **~$45** | **~$68** |
| Impression Share | 21,91% | 29,56% | — | — |
| Lost IS (Rank) | 47,10% | 57,31% | — | — |
| Lost IS (Budget) | 30,98% | 13,13% | — | — |
| CTR | 4,61% | 3,70% | — | — |
| CPC | $11,18 | $7,75 | — | — |

*\*LSA estimado — precisa de confirmação*

### 1.2 Search: Breakdown por Ad Group

| Ad Group | Gasto | % Budget | Impr. | Conv. | CPA | Status |
|---|---|---|---|---|---|---|
| [Emergency] Precision Repair | $643,13 | **92,8%** | 1.186 | 3 | **$214** | 🟡 Hiper-dependente |
| [Seasonal] Spring Startup | $49,86 | 7,2% | 137 | 2 | **$25** | 🟢 Excelente, sub-financiado |
| [New] Irrigation Installation | $0 | 0% | 18 | 0 | — | 🔴 Morto |
| [02-26] Smart Irrigation | $0 | 0% | 3 | 0 | — | 🔴 Morto |
| [V4] [SIAG] B2B | $0 | 0% | 2 | 0 | — | 🔴 Morto |

### 1.3 As 5 Causas Raiz

**🔴 #1 — Budget insuficiente e mal alocado**
$27/dia para Search é metade do necessário. 49% perdido por rank, 31% por budget. Além disso, 93% do pouco que existe vai para o grupo de pior CPA ($214).

**🔴 #2 — Bid Strategy instável (learning period destruído)**
Max Conv → Max Clicks (Mar 18) → Max Conv (Abr 21). Cada troca = reset de ~14 dias de aprendizado. Em 60 dias, o algoritmo nunca aprendeu.

**🔴 #3 — Installation fragmentado e sem budget**
7 ad groups → consolidado em 1 na Semana 2, mas sem budget para testar. 18 impressões no mês = invisível.

**🟠 #4 — Keywords com falha de cobertura**
A conta tem 16 keywords ativas. Existem 10+ keywords com 2.400-14.800 de volume mensal que não estão na conta. Exemplos:
- "sprinkler repair near me" (14.800/mês) — **não está na conta**
- "sprinkler system installation near me" (8.100/mês) — grupo morto
- "irrigation company" — inexistente

**🟠 #5 — Governança zero**
Cliente pede → time executa. Sem documentação, sem hipótese, sem prazo de maturação. Resultado: mudanças semanais que nunca deixam a campanha respirar.

---

## ═══════════════════════════════════════
## PARTE 2: NOVA ARQUITETURA DA CAMPANHA
## ═══════════════════════════════════════

### Campanha: `[V4] [AQ] [SEARCH] [GOO] Conserva Services — Jul 2026`

| Parâmetro | Configuração |
|---|---|
| **Bid Strategy** | Maximize Conversions (sem tCPA) |
| **Período sem mudanças** | Mínimo 30 dias |
| **Budget total** | **$55/dia** (aumento de $27 → $55) |
| **Rede** | Search + Search Partners (Display desativado) |
| **Localização** | Scottsdale + Phoenix + Chandler + Gilbert + Paradise Valley + Fountain Hills + Tempe |
| **Idioma** | Inglês |

### Ad Group 1: Emergency Repair 🟢 (40% · ~$22/dia)

**Função:** Manter o tráfego existente mas reduzir CPA de $214 para <$130

| Keyword | Match Type | CPC Est. |
|---|---|---|
| `[irrigation repair scottsdale]` | Exact | $6.80 |
| `"sprinkler repair phoenix"` | Phrase | $6.16 |
| `"irrigation repair near me"` | Phrase | $6.71 |
| `[leak detection scottsdale]` | Exact | $7.00 |
| `"broken sprinkler repair"` | Phrase | $6.16 |
| `"sprinkler system repair"` | Phrase | $6.80 |
| `"emergency irrigation service"` | Phrase | $6.59 |
| `[fix sprinkler phoenix]` | Exact | $5.77 |
| `"sprinkler valve repair"` | Phrase | $7.17 |
| `"sprinkler head repair"` | Phrase | $4.74 |

**Negative keywords:** "installation", "install", "new system", "replace", "cost"
**Landing page:** `conservairrigation.com/irrigation-repair/`

### Ad Group 2: Irrigation Installation 🟡 (30% · ~$16,50/dia)

**Função:** Reconstruir o funil de instalação com budget dedicado

| Keyword | Match Type | CPC Est. |
|---|---|---|
| `[irrigation system installation scottsdale]` | Exact | $4.70 |
| `"irrigation installation phoenix"` | Phrase | $5.51 |
| `"sprinkler system installation"` | Phrase | $4.70 |
| `"sprinkler installation chandler"` | Phrase | $5.61 |
| `[sprinkler system installation scottsdale]` | Exact | $4.70 |
| `"irrigation install gilbert"` | Phrase | $5.51 |
| `"new sprinkler system arizona"` | Phrase | $4.70 |
| `[irrigation installer phoenix az]` | Exact | $6.09 |
| `"lawn irrigation installation"` | Phrase | $4.70 |
| `"sprinkler system installation cost"` | Phrase | $2.99 |

**Negative keywords:** "repair", "fix", "leak", "broken", "diy", "how to"
**Landing page:** `conservairrigation.com/irrigation-system-installation/`

### Ad Group 3: Smart Irrigation & Seasonal 🔵 (20% · ~$11/dia)

**Função:** Capitalizar a sazonalidade de verão + tendência smart

| Keyword | Match Type | CPC Est. |
|---|---|---|
| `"smart irrigation controller"` | Phrase | $3.34 |
| `"smart sprinkler system"` | Phrase | $3.63 |
| `"water saving irrigation"` | Phrase | $2.85 |
| `"irrigation rebate arizona"` | Phrase | $3.00 |
| `"summer sprinkler checkup"` | Phrase | $5.19 |
| `"sprinkler system upgrade"` | Phrase | $3.34 |
| `"smart irrigation scottsdale"` | Phrase | $3.34 |
| `"irrigation tune up"` | Phrase | $5.19 |
| `"free irrigation inspection"` | Phrase | $4.00 |
| `"save water sprinkler system"` | Phrase | $2.85 |

**Landing page:** `conservairrigation.com/smart-irrigation/`

### Ad Group 4: General Services ⚪ (10% · ~$5,50/dia)

**Função:** Cobertura para termos genéricos e descoberta de novas keywords

| Keyword | Match Type |
|---|---|
| `"irrigation company scottsdale"` | Phrase |
| `"sprinkler service near me"` | Phrase |
| `"irrigation services arizona"` | Phrase |
| `"lawn irrigation company"` | Phrase |
| `"best irrigation company"` | Phrase |

**Landing page:** `conservairrigation.com/`

---

## ═══════════════════════════════════════
## PARTE 3: BRIEF PARA TIME DE COPY
## ═══════════════════════════════════════

### RSA Headlines & Descriptions por Ad Group

Cada ad group precisa de RSAs com 15 headlines + 4 descrições com Ad Strength "Excellent". Abaixo, os briefs criativos por tema:

---

### AG1 — Emergency Repair (Tom: Urgência + Confiança)

**Posicionamento:** "Reparo rápido, preço justo, técnicos certificados. Quando seu sprinkler quebrar, a Conserva resolve."

**Headlines (15):**
```
1. Emergency Sprinkler Repair
2. Irrigation Repair Near You
3. Leak? Broken Head? Fix Now
4. Same-Day Service Available
5. Stop Water Waste Today
6. Licensed & Insured Techs
7. Upfront Flat Rate Pricing
8. 95% Customer Satisfaction
9. Fix It Right First Time
10. Serving Scottsdale Since 2014
11. {KeyWord:Sprinkler Fix}
12. No Hidden Fees — Ever
13. Emergency Service Call Now
14. Toro & Hunter Certified
15. Free Repair Estimate
```

**Descriptions (4):**
```
1. Leak? Broken sprinkler? We fix it fast. Upfront flat-rate pricing, no surprise fees. Same-day service in Scottsdale. Call now.
2. Tired of no-shows? Uniformed techs arrive on time & fix it right the first time. Licensed & insured. 5-star rated.
3. Stop wasting water and money. Expert diagnostics find the root cause. Any brand, any model. Schedule your repair today.
4. Emergency service available. Don't let a broken sprinkler spike your water bill. Call Conserva now for fast, reliable repair.
```

---

### AG2 — Irrigation Installation (Tom: Transformação + Investimento)

**Posicionamento:** "Sistema novo que economiza 60% de água. Projetado para o clima do Arizona. Orçamento gratuito."

**Headlines (15):**
```
1. New Irrigation System Installed
2. Save 60% on Water Bills
3. Custom Sprinkler Design
4. Free Quote — Call Today
5. Smart Sprinkler Installation
6. Scottsdale's #1 Installer
7. Upgrade Your Lawn System
8. 5-Year Warranty Included
9. Transform Your Lawn Today
10. {KeyWord:Sprinkler Install}
11. Toro & Hunter Certified
12. Arizona's Irrigation Experts
13. Control From Your Phone
14. Lush Lawn, Less Water
15. Book Your Free Estimate
```

**Descriptions (4):**
```
1. Upgrade to a smart irrigation system. Save up to 60% on water. Custom design for Arizona's climate. Free quote. Call today.
2. Expert design & installation of high-efficiency sprinkler systems. Toro & Hunter certified. 5-year warranty available.
3. Stop overwatering. Smart controllers, weather-based scheduling, and rebate-ready systems. Professional installation included.
4. New home? Renovating your yard? We design and install the perfect irrigation system for your Scottsdale property. Free estimate.
```

---

### AG3 — Smart Irrigation & Seasonal (Tom: Sazonal + Economia)

**Posicionamento:** "Verão em Arizona? Deixe seu sistema pronto para o calor. Economia + conforto."

**Headlines (15):**
```
1. Summer Ready — Free Checkup
2. Beat the Arizona Heat
3. Free System Inspection
4. Smart Irrigation Scottsdale
5. Save Water This Summer
6. Control From Your Phone
7. Is Your System Ready for 100°F+?
8. Smart Sprinkler Installation
9. Lower Your Water Bill
10. Upgrade to Smart Irrigation
11. Summerize Your System
12. Eco-Friendly Watering
13. Rebate Ready Systems
14. Stop Overwatering Today
15. Same-Day Service Available
```

**Descriptions (4):**
```
1. Is your irrigation system ready for summer? Free SES inspection. Smart systems save up to 60% on water. Book your checkup today.
2. Beat the Scottsdale heat. Free system checkup finds leaks and inefficiencies. Toro & Hunter certified. Call now.
3. Smart irrigation in Scottsdale. Control sprinklers from your phone. Save water, save money. 5-star rated. Free quote.
4. Summer is coming — don't let the heat kill your lawn. Smart irrigation + free inspection. Licensed & insured. Serving Scottsdale.
```

---

### AG4 — General Services (Tom: Confiança + Autoridade Local)

**Posicionamento:** "A empresa de irrigação mais confiável de Scottsdale. Reparo, instalação e manutenção."

**Headlines (15):**
```
1. Irrigation Company Scottsdale
2. Trusted Local Experts
3. 50+ 5-Star Reviews
4. Sprinkler Service Near Me
5. Repair · Install · Maintain
6. Serving Greater Scottsdale
7. Free Consultation
8. Licensed & Insured Pros
9. Family-Owned & Operated
10. Over 10 Years of Experience
11. {KeyWord:Irrigation Service}
12. Residential & Commercial
13. Schedule Service Online
14. We Handle It All
15. Call Conserva Today
```

**Descriptions (4):**
```
1. Scottsdale's trusted irrigation company. Repair, installation, and maintenance. Licensed, insured, 5-star rated. Call for a free quote.
2. From emergency repairs to full system installation, we handle all your irrigation needs. Serving Scottsdale and surrounding areas.
3. Family-owned and operated. Over 10 years of experience. 50+ 5-star reviews. We treat your lawn like our own.
4. Residential or commercial, we've got you covered. Free consultation. Same-day service available. Call Conserva today.
```

---

### Extensões de Anúncio (Obrigatórias)

**Sitelinks:**
- Residential Irrigation → `/residential-irrigation/`
- Commercial Services → `/commercial-services/`
- Smart Irrigation → `/smart-irrigation/`
- Free Quote → `/free-quote/`

**Callouts:**
- Licensed & Insured
- Same-Day Service
- 5-Year Warranty
- Free Estimates
- Toro & Hunter Certified

**Call Extensions:**
- Número de telefone configurado para call tracking

---

## ═══════════════════════════════════════
## PARTE 4: FRAMEWORK DE GOVERNANÇA
## ═══════════════════════════════════════

### O "Tratado de 30 Dias" — Regras para não virar Frankenstein

#### Regra #1 — Learning Period Inviolável
> Nenhuma mudança de bid strategy, budget >20%, ou pausa/ativação de campanha antes de **30 dias de dados estáveis**.
>
> **Exceção única:** Se a campanha gastar 100% do budget diário por 7+ dias sem gerar nenhuma conversão.

#### Regra #2 — Documentação Obrigatória
> Toda mudança DEVE ser registrada em `mission-control/combinados.md` com:
> - **Hipótese:** Acreditamos que [ação] vai gerar [efeito] porque [razão]
> - **KPI:** [métrica] melhorar em [X%] até [data]
> - **Prazo:** [data] — sem intervenção antes
>
> Sem documento = a mudança não acontece.

#### Regra #3 — 1 Mudança Estrutural Por Semana
> Máximo de 1 alteração estrutural por semana. Se você muda budget E keywords E ad groups na mesma semana, não sabe o que funcionou.
>
> **Não conta como estrutural:** negative keywords (pode todo dia), criativos (a cada 14 dias), pausar keyword com 0 impr em 30 dias.

#### Regra #4 — Time Decide o Timing
> A cliente pode sugerir. O time decide QUANDO implementar.
>
> **Protocolo:**
> 1. Sugestão → documentar em `combinados.md` com tag `[sugestão cliente]`
> 2. Avaliar timing (Regra #1 + Regra #3)
> 3. Se momento certo → implementar + avisar cliente
> 4. Se não → explicar racional + agendar
>
> **Frase padrão:** *"Karina, entendi. Vamos aplicar na próxima janela [data] porque [razão técnica]. Até lá, coletamos dados para validar."*

#### Regra #5 — Report Baseado em Dados
> Toda decisão justificada com número. Sem opiniões ou "a cliente acha".
>
> **Estrutura semanal:** O que aconteceu → O que testamos → O que aprendemos → O que vamos testar → O que NÃO vamos fazer (e por quê)

---

## ═══════════════════════════════════════
## PARTE 5: PLANO DE EXECUÇÃO — 30 DIAS
## ═══════════════════════════════════════

### Semana 1 (1-7 Jul) — IMPLEMENTAÇÃO 🚀

| Dia | Ação | Responsável |
|---|---|---|
| 1 Jul | Aplicar negative keywords em massa (DIY, how to, free, cost — ver lista completa) | Account |
| 1 Jul | Aumentar budget Search de $27 → $40 | Account |
| 1 Jul | Pausar PMAX AG1 e AG2 (0 conv cada) — manter só AG3 | Account |
| 1 Jul | Aplicar novas keywords (exact + phrase) na Search | Account |
| 1 Jul | Remover/consolidar ad groups mortos | Account |
| 2 Jul | Implementar RSAs novos com headlines do copy brief | Account |
| 2 Jul | Adicionar extensões de anúncio (sitelinks, callouts, call) | Account |
| 3 Jul | Verificar URL HTTPS e Quality Score | Tech Lead |
| 3 Jul | Verificar call tracking — ligações registradas como conv? | Tech Lead |
| 4-7 Jul | **NÃO MEXER EM NADA** — deixar o algoritmo aprender | Todos |

### Semana 2 (8-14 Jul) — ESTABILIZAÇÃO 📊

| Ação | Detalhe |
|---|---|
| Report parcial | Revisar dados, SEM tomar decisões |
| Monitorar IS | Search IS deve começar a subir com budget extra |
| Verificar search terms | Adicionar negativas conforme aparecerem |
| **NÃO FAZER** | Mudar bid, criar campanhas, pausar ad groups |

### Semana 3 (15-21 Jul) — AVALIAÇÃO 🔍

| Cenário | Ação |
|---|---|
| CPA Search < $130 | Manter tudo, deixar aprender mais |
| CPA Search $130-160 | Aguardar — ainda é cedo |
| CPA Search > $160 | Investigar search terms, ajustar negativas |
| Installation com 0 conv | Revisar landing page + keywords |

### Semana 4 (22-30 Jul) — DECISÃO 🎯

| KPI | Meta | Ação se atingir | Ação se não atingir |
|---|---|---|---|
| CPA Search | <$110 | Escalar budget para $55 | Revisar estrutura |
| Installation conv | >0 | Aumentar budget share | Repensar abordagem |
| Search IS | >30% | Manter budget | Investigar lost IS |
| PMAX AG3 CPA | <$100 | Escalar criativos | Revisar assets |

---

## ═══════════════════════════════════════
## PARTE 6: NEGATIVE KEYWORDS — LISTA COMPLETA
## ═══════════════════════════════════════

### Por Intenção (Aplicar em TODOS os ad groups)

| Categoria | Keywords |
|---|---|
| DIY | how to, diy, do it yourself, tutorial, install your own, build your own, homemade |
| Emprego | jobs, hiring, career, employment, work for, job opening |
| Produto/Compras | buy, price, amazon, home depot, lowes, costco, for sale, rental, lease |
| Informação | cost of, price of, what is, wiki, definition, types of, history of |
| Irrelevante | free, chicken, nasal, garden hose, rain barrel, indoor |
| Geografia (fora) | San Tan, Queen Creek, Tucson, Mesa, Flagstaff, Prescott |

### Por Ad Group (Cross-contamination)

| Ad Group | Negativar |
|---|---|
| Emergency Repair | installation, install, new system, smart controller, commercial, HOA |
| Irrigation Installation | repair, fix, leak, broken, emergency, same-day |
| Smart/Seasonal | repair, installation, emergency, broken |
| General Services | (nenhuma específica — cobertura) |

---

## ═══════════════════════════════════════
## PARTE 7: PROJEÇÃO — CENÁRIOS PARA JULHO
## ═══════════════════════════════════════

### Cenário Base (com reestruturação + $40-55/dia)

| Métrica | Projeção |
|---|---|
| Impressões (Search) | 4.500-6.000 |
| Cliques | 180-250 |
| Conversões | 10-15 |
| CPA estimado | **$95-110** |
| Search IS estimado | 30-35% |
| Budget/dia | $40-55 |

### Cenário Conservador (sem mudanças — BAU)

| Métrica | Projeção |
|---|---|
| Conversões | 5-7 |
| CPA | $138-160 |
| Search IS | 22-25% |

### Cenário Otimista (reestruturação + budget $55 + criativos novos)

| Métrica | Projeção |
|---|---|
| Conversões | 15-22 |
| CPA | $78-95 |
| Search IS | 35-40% |

---

## ═══════════════════════════════════════
## APÊNDICE: REFERÊNCIAS
## ═══════════════════════════════════════

### Documentos Gerados pelo Squad

| Documento | Autor | Arquivo |
|---|---|---|
| Análise Técnica Search | Analista de Dados | `analise-search-conserva-jun-2026.md` |
| Estratégia de Reestruturação | Mídia Paga | `estrategia-reestruturacao-search-julho-2026.md` |
| Plano Mestre (este) | Squad Consolidado | `plano-mestre-campanha-search-julho-2026.md` |

### Próximos Passos (Aguardando Account Manager)

1. [ ] Account manager apresentar plano para Karina
2. [ ] Account manager executar Semana 1 (1-7 Jul)
3. [ ] Copy team gerar RSAs com brief acima
4. [ ] Tech Lead verificar URL HTTPS e call tracking
5. [ ] Designer Lucas criar criativos exclusivos para PMAX AG1/AG2
6. [ ] Próximo report em 8 Jul (Semana 2)

---

*Documento gerado em 01/07/2026 · V4 Company · Peretto & Co. AI Ops*
*Traffic Reporting Squad: Analista de Dados · Mídia Paga · Media Buyer · Copy Team · Líder Marcos Luciano*
