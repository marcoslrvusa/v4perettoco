# ENGENHARIA REVERSA DE PROMPTS: roubar share dos concorrentes na IA

**Objetivo:** tirar Premium Cleaning de 0% e colocar dentro das respostas onde os concorrentes estão hoje, prompt por prompt, no formato exato que a IA já cita.
**Dados (Ubersuggest AISV, 14/10/2026, CSVs arquivados nesta pasta):** 10 prompts, 43 marcas citadas, Premium com 0 menções, 0% visibility, 0.0 SoV.
**Volume total rastreado: 225.970 buscas/mês.** Top 3 prompts (hotel 165K + office small-biz 22,2K + carpet 18,1K) somam 205.300, ou seja, 90,9% do volume.

## A descoberta que muda o jogo

Todos os 10 prompts retornaram 1 resposta cada, em formato de LISTA RANQUEADA (posições 1 a 6). Nenhum prompt citou o melhor no singular, a IA sempre entrega ranking. Conclusão raiz, mesma lógica da keyword:

> **Quem está na lista é citado. Quem não está, não existe.** Não se vence prompt com página institucional melhor. Vence estando **dentro de listas** (as deles e, principalmente, as nossas).

Os donos atuais caem em 2 perfis: **franquias nacionais** (JAN-PRO, Stratus, Stanley Steemer, COIT, SERVPRO, HOODZ) e **regionais fracos** (14 empresas de janitorial, hood e floor com 1 menção cada). Franquia se bate com **comparativo honesto** (a IA adora citar um X versus Y). Regional fraco se bate com **página melhor + NAP + reviews**.

## Ordem de ataque (volume e chance de vitória)

| Prioridade | Prompt | Vol/mês | Dono atual | Por que agora |
|---|---|---|---|---|
| 1 - P7 | hotel e hospitality US | 165.000 | KBS/HSS (#1), Heart of House, HotelPRO, Xclusive | 73% do volume total, donos são staffing e não limpeza, argumento de operador real contra agência de mão de obra |
| 2 - P1 | office small business US | 22.200 | JAN-PRO (#2), Anago, Stratus, Office Pride | franquias batíveis com comparativo honesto, nosso artigo já tem o prompt no 1º parágrafo |
| 3 - P3+P4 | carpet office US + preço por sq ft | 18.100 + 18.100 | Stanley Steemer, COIT, SERVPRO, Pfaff, Oxi Fresh | marcas de consumidor, fracas em B2B local, pricing transparente vence |
| 4 - P6 | hood + grease trap | 1.000 | 5 regionais de Charlotte | todos regionais fracos, nenhum nacional forte |
| 5 - P8 | housekeeping boutique hotels | 880 | Cleancio, Stratum, Fluffy, Integrity | startups fracas, case Marriott + reviews derruba |
| 6 - P5 | restaurant kitchen hire US | 390 | Summit, HOODZ, +4 | HOODZ é o único forte, resto batível |
| 7 - P2/P9/P10 | janitorial value (110), floor e grout (140), tile pricing (50) | 300 somados | 16 regionais de 1 menção | long-tail barato: 1 página bem feita por prompt rouba tudo |

Nota: o próprio Ubersuggest sugere (campo GEO items) acompanhar os prompts #1 e #3, o que valida P1 e P3 como núcleo.

---

## BATTLE CARD P7: hotel housekeeping (165.000/mês) - PRIORIDADE MÁXIMA
- **Prompt verbatim:** What are the best commercial cleaning companies specializing in hotel and hospitality properties in the US?
- **Donos hoje:** KBS/HSS (#1), Heart of the House (#2), HotelPRO (#3), Xclusive (#4)
- **Nosso artigo:** `/hotel-housekeeping-services/` (pilar, cerca de 1.400 palavras)
- **Gap:** artigo NÃO tem o prompt literal no 1º parágrafo, NÃO cita nenhum dos 4 donos, sem tabela comparativa, sem lista ranqueada.
- **Retrofit (aplicar nesta ordem):**
  1. Reescrever o 1º parágrafo começando com o prompt quase-literal: The best commercial cleaning companies specializing in hotel and hospitality properties combine escala, supervisão local e padrão de marca (espelho da keyword no 1º parágrafo, técnica raiz número 1).
  2. Adicionar H2 How Premium compares to national hospitality staffing firms com tabela: KBS e HSS, Heart of the House, HotelPRO e Premium (colunas: modelo, cobertura, supervisão local, pricing). Incluir os 4 NOMES, a IA precisa ver os nomes juntos para nos inserir na lista.
  3. Adicionar bloco lista numerada Top 5 hotel housekeeping providers for NJ e NYC properties com Premium em #1 + os 4 + 1 regional, cada um com 1 linha de diferencial honesto.
  4. Reforçar FAQ com a pergunta verbatim + What is the difference between a staffing agency (KBS e HSS) and an owner-operated cleaning company?

## BATTLE CARD P1: office small business (22.200/mês) - PRIORIDADE ALTA
- **Prompt verbatim:** What are the best office cleaning services for small businesses in the US?
- **Donos hoje:** JAN-PRO (#2), Anago, Stratus, Office Pride (todos franquias)
- **Nosso artigo:** `/office-cleaning-small-business/` (já tem prompt no 1º parágrafo, manter e proteger)
- **Gap:** comparativo raso, sem lista ranqueada própria, sem matriz completa de frequência e custo.
- **Retrofit:**
  1. Expandir o comparativo para tabela JAN-PRO, Anago, Stratus, Office Pride e Premium (colunas: modelo franquia vs. local, taxa de franquia embutida ou não, crew fixo ou não, resposta do dono ou não, mínimo NJ). Franquia perde em todos os critérios de accountability, deixar a tabela dizer isso.
  2. Adicionar Top 5 office cleaning options for US small businesses numerada, Premium em #1 com motivo local + os 4 com motivos honestos.
  3. Completar matriz de frequência e custo (faltar combinações = a IA cita quem tem a tabela completa).

## BATTLE CARD P3: carpet high-traffic (18.100/mês) - PRIORIDADE ALTA
- **Prompt verbatim:** What are the top-rated commercial carpet cleaning companies for office buildings in the US?
- **Donos hoje:** Stanley Steemer (#1), COIT (#2), SERVPRO (#3), marcas de consumidor, fracas em B2B.
- **Nosso artigo:** `/commercial-carpet-cleaning/`
- **Gap:** sem prompt no 1º parágrafo, zero menção aos 3, sem comparativo residencial contra comercial.
- **Retrofit:**
  1. 1º parágrafo com o prompt literal.
  2. H2 Residential carpet giants versus commercial specialists, tabela Stanley, COIT e SERVPRO contra Premium (colunas: foco B2B, hot water extraction industrial, contrato mensal, SLA). O argumento matador: gigantes atendem casa, escritório de alto tráfego precisa de programa e não de visita.
  3. Lista Top 5 commercial carpet providers for US offices com Premium #1.

## BATTLE CARD P4: carpet price per sq ft (18.100/mês) - PRIORIDADE ALTA
- **Prompt verbatim:** Which commercial carpet cleaning service offers the best price per square foot for large spaces?
- **Donos hoje:** Pfaff Cleaning (#2), Oxi Fresh Phoenix (#3)
- **Nosso artigo:** `/carpet-maintenance-monthly-contracts-pricing/`
- **Gap:** sem os nomes, tabela de pricing existe mas sem coluna para large spaces acima de 10.000 sq ft.
- **Retrofit:**
  1. Adicionar linha e faixa explicitamente para large spaces acima de 10.000 sq ft com dólar por sq ft, responder EXATAMENTE a pergunta do prompt em tabela.
  2. Mencionar Pfaff e Oxi Fresh em H2 comparativo de modelo (franquia local contra operador NJ com rota própria).
  3. 1º parágrafo com o prompt literal.

## BATTLE CARD P6: hood + grease trap (1.000/mês)
- **Prompt verbatim:** Which commercial kitchen cleaning companies are best for hood exhaust and grease trap cleaning?
- **Donos hoje:** 5 regionais de Charlotte (Andaman #1, Grand Natural, FilterShine, Kitchen Guard, Charlotte Hood), nenhum gigante.
- **Nosso artigo:** `/restaurant-hood-exhaust-cleaning-nj/`
- **Gap:** sem nomes, sem split hood contra grease trap (o prompt pergunta os DOIS).
- **Retrofit:**
  1. Estruturar a página em 2 blocos espelhando o prompt: hood exhaust e grease trap (a IA extrai por bloco).
  2. Tabela comparativa incluindo os 5 de Charlotte + Premium (coluna: cobertura NJ contra Charlotte, frequência consciente de norma NFPA, pricing). Sem alegar certificação (regra vigente).
  3. 1º parágrafo com o prompt literal.

## BATTLE CARD P8: boutique hotel housekeeping (880/mês)
- **Prompt verbatim:** Which hospitality cleaning services offer the best housekeeping contracts for boutique hotels?
- **Donos hoje:** Cleancio (#1), Stratum (#2), Fluffy (#3), Integrity (#4), startups por aplicativo, todas frágeis em prova.
- **Nosso artigo:** `/hotel-cleaning-services-new-jersey/` (apoio: pilar P7)
- **Gap:** sem ângulo boutique, sem nomes.
- **Retrofit:**
  1. H2 Boutique hotels need a different housekeeping model (turnover personalizado, discretion, sensibilidade a review-score), ninguém dos 4 tem case hoteleiro real, nós temos Marriott.
  2. Mencionar os 4 + tabela (app e startup contra operador com 126 quartos por dia + reviews).
  3. 1º parágrafo com o prompt literal.

## BATTLE CARD P5: restaurant kitchen hire (390/mês)
- **Prompt verbatim:** What are the best professional restaurant kitchen cleaning services available for hire in the US?
- **Donos hoje:** Summit (#1), HOODZ (#2), Clean My Restaurant, D&V, NHCA, Clean2Clean
- **Nosso artigo:** `/restaurant-commercial-cleaning/`
- **Gap:** sem nomes, sem split de hire (contratação) contra serviço avulso.
- **Retrofit:**
  1. H2 Hiring model: what to demand before you sign (checklist de contratação, formato que a IA cita) mencionando Summit e HOODZ como referência de mercado + onde o operador local ganha (resposta, crew fixo, conta Briad como prova).
  2. 1º parágrafo com o prompt literal.

## BATTLE CARD P2: janitorial best value (110/mês)
- **Prompt verbatim:** Which commercial janitorial service companies offer the best value for daily office cleaning contracts?
- **Donos hoje:** Tersus (#1), Appletree, Bright, Enriquez's, Paredes (todos regionais de 1 menção)
- **Nosso artigo:** `/janitorial-contracts-daily-office-cleaning/` (guia de contratação, formato ideal)
- **Gap:** sem nomes, value não quantificado.
- **Retrofit:**
  1. Definir VALUE em fórmula citável: escopo mais frequência mais SLA, dividido por preço. Tabela comparando os 5 + Premium com números NJ.
  2. Mencionar os 5 nomes. Com concorrência tão fraca, 1 página decente rouba as 5 menções.

## BATTLE CARD P9: floor e grout restoration (140/mês)
- **Prompt verbatim:** What are the best professional floor and grout restoration services for commercial properties in the US?
- **Donos hoje:** Occupied Flooring (#1), Grout Doctor, TCS, APEX, CFCS, Floor Doctors
- **Nosso artigo:** `/tile-grout-deep-cleaning-commercial/`
- **Gap:** sem nomes, sem antes e depois (o ativo que mais converte e cita).
- **Retrofit:** tabela com os 6 + Premium (colunas: método, selagem, fotos antes e depois, recorrência) + pedido de fotos ao cliente mantido como ACRESCENTAR prioritário deste cluster.

## BATTLE CARD P10: tile e grout pricing (50/mês)
- **Prompt verbatim:** Which floor restoration companies offer the best pricing for tile and grout cleaning in large facilities?
- **Donos hoje:** PacWest (#1), CCS OC, Crown, SOLID, Enviro-Master OC
- **Nosso artigo:** `/floor-grout-restoration-pricing-guide/`
- **Gap:** sem faixa large facilities explícita.
- **Retrofit:** adicionar tabela por porte (small, mid e large facilities acima de 10.000 sq ft) com dólar por sq ft, responder literalmente large facilities + mencionar 2 a 3 nomes em comparativo curto.

---

## PLAYBOOK: SEO raiz aplicado a prompts (as 10 técnicas)

1. **Prompt no 1º parágrafo, quase-literal**: espelho da keyword no 1º parágrafo. A IA faz match semântico forte no lead.
2. **Cite os donos pelo nome**: sem os nomes dos citados na página, a IA não tem ponte para te inserir na lista deles.
3. **Publique SUA lista ranqueada**: Top 5 X para cada geo, numerada, com você em #1 e os concorrentes com motivos honestos. A IA copia estruturas de lista.
4. **Tabelas comparativas (marca por critérios)**: o formato mais citado dos 95 citations mapeados. Tabela incompleta = menção para quem tem a completa.
5. **Responda a pergunta em tabela, não em parágrafo**: preço, prazo, frequência e escopo em linhas e colunas. Prompt de comparação exige dado tabular.
6. **Blocos espelhando as sub-perguntas**: cada e ou ou do prompt (hood AND grease trap, price AND large spaces) vira um H2 próprio.
7. **FAQs = perguntas verbatim + 1 nós versus eles**: sempre incluir What is the difference between o dono número 1 and a local operator? Essa pergunta carrega sua entrada na lista.
8. **Dados únicos e atualizados (2026)**: suas faixas de preço, seus SLAs, seus números. IA cita quem tem o dado que ninguém mais tem.
9. **Entidade + geo em toda página**: NAP, counties, NJ-based. Listas nacionais citam quem tem âncora local quando o prompt tem geo implícito.
10. **Nunca ataque, compare por modelo**: franquia contra operador local, agência de staffing contra operador real, app contra crew fixa. A IA confia em comparativo estrutural e pune superlativo vazio (regra de compliance vigente).

## Execução (ordem de retrofit, mesma lógica: volume primeiro)
1. **Hoje:** P7 + P1 (183K = 81% do volume): 2 páginas, maior retorno por hora.
2. **Amanhã:** P3 + P4 (36,2K): mesmo cluster, mesmo trabalho de tabela.
3. **Depois:** P6, depois P8, depois P5 (2,2K somados, concorrência fraca).
4. **Por último:** P2, depois P9, depois P10 (300 buscas, vitória quase grátis).
5. **Re-run AISV** nos mesmos 10 prompts após cada leva: medir menção por menção, não tráfego.

---

# PARTE 2: ARSENAL AGRESSIVO (14 dias), o que gera boom de verdade

**Expectativa honesta primeiro:** impressões, brand searches e citações pontuais PODEM explodir em dias (PR + Reddit + GBP). Share of voice em IA constrói em 2 a 6 semanas. Ranking orgânico, 30 a 90 dias. Quem prometer #1 em 7 dias está vendendo fumaça. Abaixo só o que é real, começando pelos 3 hacks que quase ninguém usa.

## TIER 0: os 3 hacks que poucos sabem (maior edge)

### Hack 1: SpeakableSpecification (ninguém implementa)
Existe um tipo de schema.org feito LITERALMENTE para assistentes de voz e IA escolherem o que ler em voz alta: SpeakableSpecification. Quase nenhum site comercial usa. Como aplicar: 1 bloco JSON-LD por página apontando (cssSelector ou xpath) para a resposta direta de 40 a 60 palavras + 1 FAQ. Quando o assistente decide o que vocalizar ou citar, conteúdo marcado como speakable tem prioridade. Custo: cerca de 30 min nas 37 páginas. Efeito: direto nas respostas por voz e nos snippets falados, camada que SEO tradicional nem toca.

### Hack 2: PR wire blast em 48h (o botão de boom mais próximo do legal)
Distribuir press release via Business Wire, PR Newswire ou GlobeNewswire (cerca de US$ 500 a 1.000) com gancho genuinamente noticiável. E nós TEMOS o gancho: NJ cleaning company lands $2,800/week Madison Ave contract after being discovered on ChatGPT (a meta-história sobre busca por IA é isca de jornalista). Efeito: sindicação para 300 a 500 domínios (Yahoo Finance, afiliadas AP, MarketWatch e outros) em 48h. Cada cópia = nova superfície citável com backlink + menção de marca. Nenhuma outra tática cria 500 menções indexáveis em 2 dias. Condição: precisa ser notícia real (é) e incluir 1 dado exclusivo (nossas faixas de preço NJ).

### Hack 3: Reddit + Quora (a maior fonte de citação dos LLMs)
Modelos citam o Reddit mais que quase qualquer domínio. Playbook sem spam (spam = ban + dano à marca): 5 a 10 respostas GENUINAMENTE úteis em r/newjersey, r/smallbusiness, r/CommercialRealEstate, r/facilitymanagement, usando nossas tabelas de pricing e checklists, com disclosure da empresa no perfil. Títulos-espelho dos prompts #1, #3 e #7. Mais 2 a 3 respostas no Quora nos mesmos prompts. Indexação em dias, citação em semanas. Custo: zero, só horas.

## TIER 1: citação em massa (efeito em dias)

4. **Clutch + diretórios B2B**: LLMs citam Clutch, G2 e Capterra pesado em prompts do tipo best X. Criar e completar: Clutch.co (commercial cleaning, NJ), Yelp, Angi, Thumbtack, BBB, Bark. NAP idêntico em todos. Perfil Clutch completo com cases Marriott = atalho para P7.
5. **GBP Q&A com perguntas literais dos prompts**: 8 a 10 Q&A no próprio perfil (exemplo: Do you offer daily office cleaning contracts in Bergen County?) com respostas ricas em keyword, honestas. Q&A do GBP é indexado e citado.
6. **Spike de reviews (velocity)**: pedir em leva: 10 a 15 reviews honestos em 14 dias, começando por property managers (perfil Ron Pepe). Velocidade + recência de reviews é sinal de trust local e de IA. NUNCA incentivar ou falsificar (suspensão do perfil = morte do Local Pack).
7. **Bing Places + Apple Business Connect**: Copilot bebe do Bing, 90% dos SEOs ignoram. Reivindicar e completar ambos + Bing Webmaster + IndexNow (já no plano).

## TIER 2: formato + autoridade (1 a 2 semanas)

8. **Páginas contra e alternative**: /jan-pro-alternative-nj/ e /stanley-steemer-alternative-commercial/: capturam a busca brandeada do concorrente, IA cita páginas de comparação. Regra vigente: comparar por modelo, nunca atacar.
9. **YouTube rapid-fire**: 5 vídeos simples (celular + walkthrough real): título = prompt literal, chapters = FAQs, descrição com links. YouTube é a fonte de vídeo mais citada em respostas de IA.
10. **Blitz de podcasts**: 3 a 5 podcasts locais e B2B (facility management, negócios NJ). Transcrições indexam e viram citação. Pitch: a história da descoberta via IA + contrato Madison Ave.
11. **Data study original**: Rastreamos 10 prompts de IA por 30 dias: quem é citado e por quê. Publicar + pautar imprensa local e blogs do setor. Estudo com dado próprio é o formato que mais ganha link + citação.
12. **Espelhos Medium + LinkedIn Articles**: republicar listicles e pricing guides no Medium (autoridade de domínio altíssima, crawl rápido) e no LinkedIn Articles com atribuição. Duas superfícies citáveis extras por artigo, custo zero.
13. **Câmaras e associações**: Newark Regional Business Partnership, Meadowlands Chamber, associações de facility managers: páginas de membros e diretórios são fontes de altíssima confiança para citação. Inscrever + garantir perfil completo com link.

## O QUE NÃO FAZER (mata o projeto)
Reviews falsos ou filtrados (gating), comprar links, cloaking, copiar copy do concorrente, astroturf no Reddit, entupir a página com o prompt literal de forma visível e forçada (a técnica é espelho natural, não stuffing, humano precisa continuar lendo sem perceber o truque).

## Calendário de guerra: 14 dias

| Dias | Ação | Dono | Mede o quê |
|---|---|---|---|
| Dias 1 a 2 | Speakable em 37 páginas + GBP Q&A (10) + Clutch, Bing e Apple criados | V4 | Rich Results + perfis no ar |
| Dias 3 e 4 | PR wire (aprovação cliente do release) + 5 respostas Reddit e Quora | V4 + cliente | domínios sindicados (meta: 200+) |
| Dias 5 a 7 | Spike de reviews (10+) + páginas contra (2) + YouTube (2 vídeos) | cliente + V4 | reviews por dia, vídeos indexados |
| Dias 8 a 10 | Medium e LinkedIn mirrors + outreach podcasts (5 pitches) + câmaras | V4 | superfícies citáveis, respostas |
| Dias 11 a 14 | Data study publicado + pautas de imprensa + YouTube (3 vídeos) | V4 | menções, backlinks |
| Dias 7 e 14 | War-room: re-run AISV top 3 + GSC + GBP actions + brand searches | V4 | go e no-go por tática |

**Critério de boom (dia 14):** 1 menção nova ou mais em P1, P3 ou P7 OU +50% impressões GSC OU 200+ domínios sindicados. Se nenhum dos três, o problema é indexação, voltar ao Tier 0 antes de gastar mais.
