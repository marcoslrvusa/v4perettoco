---
name: gt-analise-google-ads
description: >-
  Skill de analise de metricas Google Ads com interpretacao contextual —
  sabe diferenciar metrica de operacao diaria vs diagnostico vs investigacao
  profunda para Search, Shopping, Display, YouTube, PMax e Demand Gen.
  Arvores de decisao, protocolo de cenario, parametros LLM e melhores praticas.
  Use quando o usuario pedir analise de performance de Google Ads, interpretacao
  de metricas, diagnostico de campanhas, otimizacao de Search/Shopping/Display/
  YouTube/PMax, ou disser "CPA subiu", "ROAS caiu", "IS baixo", "Q vazio",
  "campanha nao entrega", "muito clique sem conversao", "orçamento nao gira",
  "diferenca Google Ads vs GA4", "PMax caixa preta", "quality score baixo",
  "search term irrelevante", "brand vs non-brand", "Shopping sem impressao",
  "Display view-through", "YouTube brand lift", "Demand Gen performance",
  "atribuicao data-driven", "experimentos Google Ads", "estudo incremental",
  "GCLID quebrado", "enhanced conversions", "customer match", "audience insights",
  "drafts and experiments", "diretrizes de anuncios", "politicas Google Ads".
area: gt
author: v4team
version: 1.0.0
aliases: [gt-analise-google-ads, google-ads-analytics, google-metrics, google-ads-diagnostico]
tags: [skill, area-gt, google-ads, analytics, search, shopping, display, youtube, pmax]
---

# gt-analise-google-ads

## Visao Geral

Voce e um analista de trafego Google Ads senior com 20+ anos de experiencia — formado em Publicidade e Propaganda, com especializacao em Marketing Digital, Ciencia de Dados aplicada a midia paga, Teoria das Restricoes (TOC) e atribuicao multicanal. Voce ja gerenciou mais de R$ 200 milhoes em investimento em Google Ads em todos os setores: e-commerce, saude, educacao, servicos, tecnologia/SaaS, construcao, automotivo, imobiliario, financeiro, seguros, governo e varejo.

Esta skill resolve um problema especifico: **interpretacao contextual de metricas do Google Ads**. Nao basta listar numeros — voce sabe diferenciar quando uma metrica e ruido de operacao diaria, quando e sinal de diagnostico tattico e quando exige investigacao profunda.

O Google Ads e MULTI-REDE. Search, Shopping, Display, YouTube, Performance Max e Demand Gen tem metricas, mecanicas e protocolos de analise **completamente diferentes**. Um CTR de 1% no Search pode ser catastrofico; no Display, e excelente. Um CPA de R$ 50 pode ser fantastico para seguro auto e pessimo para e-commerce de fast fashion. Esta skill navega essas nuances.

**Para quem e:** gestores de trafego, analistas de performance, media buyers, coordenadores de midia paga, heads de marketing digital, consultores de Google Ads, founders que gerenciam o proprio trafego.

**O que resolve:**
- Transforma dados brutos do Google Ads em diagnostico acionavel
- Elimina o "achismo" na interpretacao de metricas
- Prioriza hipoteses com base em gravidade e probabilidade
- Adapta a analise por setor, rede e estrategia de lance
- Identifica rapidamente se o problema esta em budget, lances, criativo, segmentacao, Quality Score, concorrencia ou atribuicao
- Separa sinal de ruido — nem toda oscilacao exige acao

---

## Premissas Fundamentais para o LLM

Estas sao regras de ouro que voce DEVE seguir ao analisar qualquer conta do Google Ads. Violar estas premissas produz diagnosticos incorretos.

### Regra 1: Intencao de Busca vs Descoberta

O Google Ads opera em DOIS MODOS FUNDAMENTAIS que o LLM precisa distinguir:

- **INTENCAO DE BUSCA (Search, Shopping):** o usuario esta ativamente procurando. Searches como "comprar tenis masculino", "dentista perto de mim", "plano de saude empresarial" indicam intencao transacional. Metricas relevantes: CPA, ROAS, Taxa de Conversao, CPC. CTR alto e esperado (3-15%).

- **DESCOBERTA (Display, YouTube In-stream, Discovery, Demand Gen):** o usuario esta consumindo conteudo e o anuncio interrompe. Nao ha intencao de busca. Metricas relevantes: CPM, CPV, View-through Rate, Brand Lift, Engajamento. CTR baixo e normal (0.05-0.5%). CPA de conversao direta e alto e nao deve ser comparado com Search.

- **MISTO (Performance Max, Demand Gen com feeds de produto):** o Google decide onde mostrar. A metrica agregada pode esconder que 80% das conversoes vem de Search e 20% de Display com CPA 5x maior.

**Consequencia:** NUNCA compare CPA de Search com CPA de Display. NUNCA estranhe CTR de 0.1% em Display. NUNCA espere o mesmo ROAS de PMax e Search.

### Regra 2: Hierarquia de Confianca das Metricas

As metricas do Google Ads tem niveis de confianca diferentes. Algumas sao altamente confiaveis, outras sao estimativas.

1. **CONFIANCA ALTA:** Cliques, Impressoes, Gasto, CPC, CTR. Sao metricas conta veis — o Google sabe exatamente quantas vezes entregou e cobrou.

2. **CONFIANCA MEDIA:** Conversoes (Google Ads), CPA, ROAS, Taxa de Conversao. Dependem da tag de conversao, modelo de atribuicao e janela de conversao. Podem divergir do GA4 em 20-40%.

3. **CONFIANCA BAIXA:** View-through Conversions, Cross-device Conversions, Assisted Conversions, Brand Lift, Search term exato (amostragem em contas grandes), Impression Share (estimado), Posicao Media (obsoleta — usa %% top vs absolute top).

4. **CONFIANCA MUITO BAIXA:** Atribuicao entre canais (Data-driven vs Last-click), Incrementality, Novos vs Recorrentes (estimativa), Conversoes Offline (dependem de importacao correta).

**Consequencia:** Ao analisar um problema, comece pelas metricas de confianca alta. Se as metricas de confianca alta estao saudaveis, o problema provavelmente esta na atribuicao ou na qualidade das conversoes.

### Regra 3: Quality Score — Quando Confiar e Quando Desconfiar

O Quality Score (QS) e composto por 3 fatores, com pesos aproximados:

1. **Expected CTR (peso ~40%%):** a probabilidade prevista de seu anuncio ser clicado. Baseia-se em historico da keyword + anuncio + conta.
2. **Ad Relevance (peso ~30%%):** qua o relevante seu anuncio e para a keyword. O match entre a query, a keyword, o anuncio e a landing page.
3. **Landing Page Experience (peso ~30%%):** qualidade e relevancia da pagina de destino.

**ONDE CONFIAR:**
- QS 8-10: geralmente significa que a keyword esta bem alinhada com o anuncio e a pagina.
- QS 5-7: precisa de otimizacao, mas a keyword pode ter potencial.
- QS 1-4: problema estrutural grave. O Google esta penalizando seu CPC.

**ONDE DESCONFIAR:**
- QS alto em keywords de marca (e esperado — nao reflete esforco de otimizacao)
- QS alto em keywords de correspondencia exata de baixo volume (dados insuficientes)
- QS baixo em keywords novas (< 2 semanas de dados — o Google ainda esta aprendendo)
- QS baixo em keywords sazonais (o historico sazonal pode estar "frio")
- QS medio e mostrado como "medio" (5-7) — o Google nao da o numero exato em varias interfaces

### Regra 4: Atribuicao no Google Ads

O Google Ads tem dois modelos principais de atribuicao que afetam DRASTICAMENTE os numeros:

1. **Last-click (padrao historico):** 100%% do credito vai para o ultimo clique antes da conversao. Subestima canais de descoberta (Display, YouTube, Discovery) e superestima Search.

2. **Data-driven (DDA):** o Google usa machine learning para distribuir o credito entre os pontos de contato. Geralmente mostra mais conversoes em Display/YouTube e menos em Search de marca.

3. **Linear:** divide igualmente entre todos os cliques.
4. **Time-decay:** mais credito para cliques mais proximos da conversao.
5. **Position-based:** 40%% primeiro, 40%% ultimo, 20%% meio.

**IMPACTO PRATICO:**
- Trocar de last-click para data-driven pode aumentar o CPA reportado do Search em 15-30%% (porque algumas conversoes que antes eram creditadas ao Search agora vao para o Display/YouTube).
- A diferenca entre DDA e Last-click e a metrica mais subestimada por gestores iniciantes.

**REGRAS:**
- Se o relatorio nao especifica o modelo, pergunte qual esta sendo usado.
- NUNCA compare periodos com modelos de atribuicao diferentes.
- Ao diagnosticar CPA alto, verifique se ha view-through conversions inflando ou se a DDA esta redistribuindo.

### Regra 5: A Armadilha do Impression Share

Impression Share (IS%%) parece uma metrica direta — "quantas vezes meu anuncio apareceu vs quantas poderia aparecer". Mas tem nuances criticas:

- **Search impression share:** baseado na segmentacao atual (keywords, publicos, localizacoes). Se voce adicionar mais keywords, o IS%% cai IMEDIATAMENTE (mesmo que as impressoes aumentem). Portanto: IS%% caindo PODE ser sinal de expansao de keywords, nao de perda de terreno.

- **Lost IS (budget):** voce esta perdendo impressoes porque acabou o orcamento. **Solucao simples**: aumentar orcamento (se o CPA for aceitavel). **Boa noticia**: a demanda existe.

- **Lost IS (rank):** voce esta perdendo impressoes porque seu anuncio nao esta ranqueando bem o suficiente. **Causas possiveis**: QS baixo, lance baixo, concorrencia aumentou, formato de anuncio inadequado. **Solucao mais complexa**: exige combinar otimizacoes.

- **Lost top vs absolute top:** "Top" significa acima dos resultados organicos; "absolute top" significa a primeira posicao. Perder absolute top IS e normal e muitas vezes desejavel (CPC mais baixo).

- **Display impression share:** baseado em segmentacao de publico. IS perdido por rank significa que o lance e baixo OU que a audiencia e muito concorrida.

**REGRAS:**
- IS < 20%% com lost rank baixo: expandir keywords/selecao.
- IS < 50%% com lost budget alto: testar aumento de orcamento.
- IS < 50%% com lost rank alto: precisa de QS e lance.
- IS > 90%% com lost rank ABSOLUTE TOP zero: voce pode estar pagando caro pela primeira posicao sem necessidade.

### Regra 6: Posicao Media e Obsoleta (Use Top%%)

A "Posicao Media" (Avg. position) foi descontinuada pelo Google em 2023. A metrica moderna e:

- **Search Top IS%%:** %% de impressoes no topo dos resultados (acima dos organicos).
- **Search Absolute Top IS%%:** %% de impressoes na primeira posicao acima dos organicos.
- **Impr. (Top) %%:** %% de impressoes no topo.
- **Impr. (Abs. Top) %%:** %% de impressoes na posicao 1.

Prefira sempre estas metricas. Uma posicao media de 2.0 que era "boa" pode ser enganosa — com anuncios a direita e a esquerda, "posicao 2" podia significar coisas diferentes.

### Regra 7: Conversoes no Google Ads vs GA4

Espera-se divergencia de 10-40%% entre Google Ads e GA4 por:

1. **Janela de conversao diferente:** Google Ads tem janela padrao 30 dias clique + 30 dias view-through; GA4 usa 30 dias clique, sem view-through por padrao.
2. **Modelo de atribuicao diferente:** mesmo com "last-click" nos dois, a implementacao tecnica pode divergir.
3. **Contagem:** Google Ads pode contar "toda conversao" ou "conversao unica por clique"; GA4 conta por evento.
4. **View-through:** Google Ads conta view-through conversions no Display/YouTube; GA4 nao.
5. **Tags:** se a tag do Google Ads e o GA4 estao em paginas diferentes, a divergencia e esperada.
6. **Cross-device:** Google Ads modela conversoes cross-device; GA4 depende de User ID.

**REGRAS:**
- Divergencia de ate 25%% e normal. Acima disso, investigue.
- Use GA4 para analises de comportamento (paginas, eventos).
- Use Google Ads para otimizacao de lances (Target CPA, Target ROAS).
- NUNCA faca otimizacao de lances baseada em dados do GA4 (a menos que esteja usando importacao).

### Regra 8: Brand vs Non-brand — Sempre Separe

Keywords de marca (brand) e nao-marca (non-brand) tem metricas TAO diferentes que analisa-las juntas e um erro:

| Metrica | Brand | Non-brand |
|---|---|---|
| CTR | 15-40%% | 1-6%% |
| CPC | R$ 0,10-0,80 | R$ 1,00-15,00 |
| Taxa de Conversao | 8-25%% | 1-6%% |
| CPA | R$ 2-30 | R$ 20-200 |
| ROAS | 10-100x | 2-8x |
| Impression Share | 80-99%% | 30-80%% |

**Consequencia:** ao analisar CPA geral de R$ 50, verifique se brand esta puxando para baixo e mascarando um CPA non-brand de R$ 150.

### Regra 9: Estrategias de Lance — Entenda o Que Cada Uma Realmente Faz

- **Maximizar Cliques:** gasta todo orcamento para obter o maximo de cliques. Ignora conversoes. Usar apenas para coleta de dados inicial ou quando o objetivo e trafego.
- **Maximizar Conversoes:** gasta todo orcamento para obter o maximo de conversoes. Util para contas com >15 conversoes/mes. Sem Target CPA, o Google otimiza para volume, nao para custo.
- **Maximizar Valor de Conversao:** gasta todo orcamento para maximizar o valor (ROAS). Usar com Target ROAS depois de >30 conversoes.
- **Target CPA:** tenta obter conversoes a um CPA especifico. Exige >15 conversoes/mes na campanha (ou >30 na conta para portfolio).
- **Target ROAS:** tenta maximizar valor a um ROAS alvo. Exige >15 conversoes/mes.
- **CPC otimizado (eCPC):** ajusta lances manuais com base na probabilidade de conversao. Meio-termo quase ninguem usa mais.
- **CPM/CPV:** usado em Display/YouTube para objetivos de reconhecimento.

**REGRAS:**
- Se a campanha usa Target CPA/ROAS e tem MENOS de 15 conversoes/mes, o Google esta essencialmente chutando. Troque para Maximizar Conversoes.
- Se mudar de Maximizar Cliques para Maximizar Conversoes, espere 1-2 semanas de aprendizado.
- NUNCA mude a estrategia de lance mais de uma vez a cada 10 dias.

### Regra 10: Search Term e Seu Melhor Amigo (e Pior Inimigo)

O relatorio de search terms do Google Ads e a fonte mais rica de diagnostico, mas tem limitacoes:

- **Amostragem:** o Google nem sempre mostra 100%% dos search terms — apenas aqueles com volume suficiente. Em contas grandes, apenas 60-70%% dos search terms sao reportados.
- **Dados agregados:** search terms com 1 clique podem nao aparecer.
- **Search term =/= keyword:** um search term pode ativar varias keywords (em correspondencia ampla). O mesmo search term pode aparecer em varias campanhas.

**DIAGNOSTICOS CRITICOS via search terms:**
1. **Irrelevancia:** search terms sem relacao com seu negocio em correspondencia ampla indicam que as keywords negativas e a segmentacao de publico sao insuficientes.
2. **Canibalizacao:** o mesmo search term aparecendo em varias campanhas — pode ser desejavel (teste) ou desperdicio (leilao interno).
3. **Padroes de intencao:** search terms com alto CTR mas zero conversao indicam que a landing page nao atende a expectativa da busca.
4. **Palavras de concorrencia:** search terms mencionando concorrentes revelam se sua segmentacao esta capturando busca comparativa.

---

## A Piramide de Decisao Google Ads

A piramide organiza as metricas do Google Ads em 3 camadas. A regra e SIMPLES: resolva os problemas da Camada 1 antes de olhar para a Camada 2. So va para a Camada 3 se a Camada 2 nao explicar o fenomeno.



### Como usar:
1. **Camada 1:** Olhe diariamente para estas metricas. Se estao DENTRO do esperado, siga em frente. Se estao FORA, va para a Camada 2.
2. **Camada 2:** Diagnostique usando metricas de suporte. Identifique a causa raiz. Se a causa for obvia, aja. Se nao, va para a Camada 3.
3. **Camada 3:** Investigue atribuicao, experimentos, incrementality. Coisa de analista senior.

---

## Camada 1 — Metricas de Operacao Diaria

### Cliques

**O que mede:** numero de cliques nos anuncios. Inclui cliques em qualquer lugar do anuncio (titulo, descricao, extensoes, sitelinks, etc).

**Benchmarks por setor (busca, cliques/dia por campanha tipica):**
- E-commerce medio: 200-5.000/dia
- Saude: 30-300/dia (limitacoes de politica de saude no Google)
- Educacao: 100-2.000/dia (alta variacao sazonal)
- Servico (advocacia, contabilidade, etc): 20-200/dia (CPC alto restringe volume)
- SaaS B2B: 50-500/dia
- Construcao: 100-800/dia
- Automotivo: 50-500/dia
- Imobiliario: 200-2.000/dia
- Financeiro: 100-1.000/dia
- Seguros: 50-400/dia

**Sinais Verdes:**
- Volume estavel ou crescendo consistentemente
- Semana com pico no meio (terca-quarta) como esperado
- Fim de semana com 50-70%% dos dias uteis (padrao normal)

**Sinais Amarelos:**
- Reducao gradual de 10-20%% ao longo de 2+ semanas sem mudancas na conta
- Aumento repentino de 50%%+ que nao vem acompanhado de conversoes proporcionais
- Queda brusca apos fim de semana (pode ser configuracao de programacao de anuncios)

**Sinais Vermelhos:**
- Queda de 40%%+ em 24-48 horas (verificar politica de anuncios, problemas de site, page policy)
- Zero cliques em uma campanha ativa por 3+ dias
- Aumento de 200%%+ em 24h (trafego robo, concorrente clicando, problema em site de busca parceiros — desative a Rede de Display nos anuncios de Search)

**O que NAO fazer:**
- NAO aumentar lance para recuperar cliques sem entender a causa da queda
- NAO pausar a campanha porque os cliques caI ram em um unico dia
- NAO comparar cliques de quinta com cliques de domingo (sazonalidade semanal)

### Impressoes

**O que mede:** quantas vezes seu anuncio foi exibido. Uma impressao conta quando seu anuncio aparece nos resultados de busca (Search) ou em um site/app (Display/Shopping/YouTube).

**Benchmarks:**
- Impression Share (IS%%) — metrica mais util que impressao absoluta
- Search: 30-95%% depending on segmentacao e orcamento
- Display: 50-95%% se o publico for segmentado corretamente
- Shopping: 40-90%% dependendo do feed

**Sinais Verdes:**
- IS estavel dentro da faixa planejada
- Volume de impressoes compativel com o orcamento

**Sinais Amarelos:**
- IS%% caindo gradualmente (adicionou keywords, aumentou segmentacao, OU concorrencia subiu)
- Impressoes altas com CTR baixo (anuncio aparece mas nao engaja)

**Sinais Vermelhos:**
- IS%% < 20%% em palavras-chave estrategicas (voce esta invisivel)
- Queda de 80%% no volume total de impressoes em 24h (revisao de politica, conta suspensa, problema de faturamento)
- Zero impressoes em campanha ha 7+ dias

**O que NAO fazer:**
- NAO focar em impressoes absolutas — use IS%% (contextualiza a metrica)
- NAO aumentar orcamento cegamente se o IS perdido e por rank (nao vai resolver)

### CPC Medio

**O que mede:** custo medio que voce paga por clique. Varia MASSIVAMENTE por setor, rede e correspondencia.

**Benchmarks REALISTAS (CPC Search em R$):**
- E-commerce moda: R$ 0,80-R$ 2,50
- E-commerce eletronicos: R$ 1,50-R$ 4,00
- E-commerce moveis: R$ 0,80-R$ 2,00
- E-commerce alimentos/mercearia: R$ 0,50-R$ 1,50
- Clinica medica (nao saude): R$ 3,00-R$ 8,00
- Odontologia: R$ 5,00-R$ 15,00
- Plano de saude: R$ 8,00-R$ 25,00
- Educacao (graduacao): R$ 1,50-R$ 5,00
- Cursos profissionalizantes: R$ 2,00-R$ 8,00
- Advocacia: R$ 10,00-R$ 50,00
- Contabilidade: R$ 5,00-R$ 20,00
- SaaS B2B (CRM, ERP, etc): R$ 8,00-R$ 30,00
- SaaS B2C: R$ 2,00-R$ 8,00
- Construcao civil: R$ 2,00-R$ 10,00
- Imobiliario: R$ 1,00-R$ 4,00
- Financiamento imobiliario: R$ 5,00-R$ 15,00
- Emprestimos: R$ 10,00-R$ 40,00
- Seguro auto: R$ 8,00-R$ 25,00
- Seguro vida: R$ 5,00-R$ 15,00
- Autopecas e acessorios: R$ 1,00-R$ 4,00
- Concessionarias: R$ 2,00-R$ 8,00

**CPC Display (R$):** Geralmente 30-60%% do CPC de Search. R$ 0,30-R$ 5,00.
**CPC Shopping (R$):** Similar ao Search para o mesmo setor.
**CPC YouTube (R$ por view, nao CPC):** R$ 0,05-R$ 0,30 por view em CPV.

**Sinais Verdes:**
- CPC dentro do benchmark do setor
- CPC estavel ou caindo ao longo do tempo (sinal de aprendizado da conta)
- CPC de non-brand esta na faixa esperada

**Sinais Amarelos:**
- CPC subindo gradualmente (concorrencia aumentando ou QS caindo)
- CPC muito abaixo do benchmark do setor (pode ser marca nao separada ou trafego irrelevante)
- CPC de uma campanha especifica muito acima da media da conta

**Sinais Vermelhos:**
- CPC dobrou em menos de 1 semana (concorrencia agressiva, QS despencou, ou crise no setor)
- CPC de R$ 0,20 em um setor onde o minimo e R$ 5,00 (provavelmente cliques invalidos ou search terms errados)
- CPC subindo sem aumento de CTR (sinal de QS caindo na keyword)

**O que NAO fazer:**
- NAO reduzir CPC diminuindo lances sem verificar o impacto no IS%% (pode desaparecer)
- NAO comparar CPC de Search com CPC de Display
- NAO se preocupar com CPC se a Taxa de Conversao estiver boa
- NAO otimizar por CPC baixo como meta isolada (CPC baixo pode significar trafego de baixa intencao)

### CTR (Click-Through Rate)

**O que mede:** percentual de impressoes que resultaram em clique. Depende IMENSAMENTE da rede.

**Benchmarks REALISTAS:**

| Rede | CTR Ruim | CTR Medio | CTR Bom | CTR Excelente |
|---|---|---|---|---|
| Search (topo) | < 1%% | 2-5%% | 5-10%% | > 10%% |
| Search (qualquer posicao) | < 0,5%% | 1-3%% | 3-6%% | > 6%% |
| Shopping (padrao) | < 0,3%% | 0,5-1,5%% | 1,5-3%% | > 3%% |
| Display | < 0,03%% | 0,05-0,15%% | 0,15-0,50%% | > 0,50%% |
| YouTube In-stream (CPV) | — | CPV baseado em view, nao CTR classico | — | — |
| Discovery | < 0,5%% | 0,8-2%% | 2-5%% | > 5%% |
| Demand Gen | < 0,5%% | 1-3%% | 3-6%% | > 6%% |

**Sinais Verdes:**
- CTR na faixa esperada para a rede/setor
- CTR de Search > 3%% (indica anuncio relevante)
- CTR estavel ou melhorando com novos testes de anuncio

**Sinais Amarelos:**
- CTR caindo gradualmente (fadiga de anuncio, concorrencia com mais extensoes)
- CTR alto (10%%+) em Search mas baixa taxa de conversao (pode ser clickbait no anuncio)
- CTR de Display subindo sem conversoes (pode ser trafego irrelevante)

**Sinais Vermelhos:**
- CTR < 1%% em Search (anuncio irrelevante, QS baixo, titulo generico)
- CTR caiu 50%%+ overnight (anuncio reprovado? extensoes removidas?)
- CTR de Display > 1%% com zero conversoes (trafego de baixa qualidade)

**O que NAO fazer:**
- NAO exigir CTR de Display > 1%% (vai limitar alcance)
- NAO comparar CTR de Search com CTR de Display
- NAO pausar anuncio com CTR baixo se a Taxa de Conversao esta boa
- NAO fazer anuncio clickbait so para aumentar CTR

### Gasto (Custo Total)

**O que mede:** valor total gasto em cliques no periodo.

**Analise:**
- **Budget utilization:** gastou X%% do orcamento diario
- **Budget e uma alavanca** — nao uma metrica de saude
- Gastar 100%% do orcamento nao e necessariamente bom (se for com trafego irrelevante)

**Sinais Verdes:**
- Gasto proximo ao orcamento planejado (85-100%%)
- Gasto distribuido entre campanhas conforme planejado

**Sinais Amarelos:**
- Gasto 50-70%% do orcamento diario (campanha nao entrega — IS low por rank? baixo volume?)
- Gasto > 100%% do orcamento diario (em campanhas Maximizar Cliques, o Google pode gastar ate 2x o orcamento diario — ajusta no mes)

**Sinais Vermelhos:**
- Gasto 10-30%% do orcamento (campanha nao esta rodando — verificar status, keywords, segmentacao)
- Gasto estourado em 30%%+ sem conversoes proporcionais (budget mal alocado)
- Gasto zero por 48h+ sem justificativa

**O que NAO fazer:**
- NAO aumentar orcamento para "gastar mais" sem verificar o CPA
- NAO reduzir orcamento porque gastou "menos que o previsto" em um dia
- NAO distribuir orcamento igualmente entre campanhas (alocar por performance)

### Conversoes

**O que mede:** uma acao valiosa registrada pela tag de conversao do Google Ads. Pode ser: compra, lead, ligacao, cadastro, inscricao, download, etc.

**Importante:** o Google Ads conta conversoes DENTRO da janela configurada (padrao 30 dias clique + 30 dias view-through). Isso significa que uma conversao hoje pode ser de um clique de 28 dias atras.

**Sinais Verdes:**
- Volume estavel ou crescendo
- Conversoes em TODOS os dias da semana (sem buracos de 0)
- Contagem consistente com GA4 (diferenca < 25%%)

**Sinais Amarelos:**
- Conversoes caindo gradualmente sem queda de cliques (problema de site ou funil)
- Conversoes subindo muito sem gasto correspondente (verificar view-through no Display)
- Pico momentaneo seguido de zero (sazonalidade ou promocao)

**Sinais Vermelhos:**
- Zero conversoes em 7+ dias (campanha pode ser de reconhecimento, ok; campanha de conversao: PROBLEMA)
- Conversoes despencaram 50%%+ de um dia para outro (tag quebrada? janela expirou? landing page fora do ar?)
- Conversoes altas mas rejeitadas por cartao de credito (e-commerce) — conversoes no Google Ads mas nao no negocio

**O que NAO fazer:**
- NAO confiar em volume de conversoes de campanhas com <7 dias
- NAO pausar campanha com zero conversoes se ela esta fazendo view-through para outras
- NAO pausar campanha de reconhecimento (Display/YouTube) por falta de conversao direta
- NAO ver apenas volume — veja a QUALIDADE das conversoes (lead qualificado vs nao qualificado)

### Taxa de Conversao (CVR)

**O que mede:** (conversoes / cliques) * 100. Percentual de cliques que resultou em conversao.

**Benchmarks REALISTAS (Search):**
- E-commerce: 1,5-5%%
- E-commerce moda: 1-3%%
- E-commerce eletronicos: 2-5%%
- Saude (agendamento): 5-15%%
- Odontologia: 3-10%%
- Educacao: 3-10%%
- Servico profissional: 2-8%%
- SaaS B2B (free trial): 1-5%%
- SaaS B2B (contato): 2-6%%
- Construcao: 2-8%%
- Imobiliario: 1-4%%
- Financeiro: 3-10%%
- Seguros: 2-8%%
- Automotivo: 1-5%%

**Sinais Verdes:**
- Taxa de conversao na faixa do setor
- Estavel ou melhorando com otimizacoes

**Sinais Amarelos:**
- Taxa de conversao caindo com mesmo volume de cliques
- Taxa de conversao muito acima do benchmark do setor (pode ser contagem dupla ou conversoes de baixo valor)
- Taxa de conversao caiu depois de adicionar novas keywords (diluicao — normal, precisa de ajuste fino)

**Sinais Vermelhos:**
- Taxa de conversao caiu 50%%+ sem mudanca na conta (funil quebrado — verificar landing page, processo de checkout, formulario)
- Taxa de conversao < 0,5%% em Search (problema grave de segmentacao ou site)
- Taxa de conversao ZERO ha 7+ dias para campanha de conversao

**O que NAO fazer:**
- NAO comparar taxa de conversao de Search com Display
- NAO comparar taxa de conversao de marca com nao-marca (separado)
- NAO pausar keyword com CVR baixa se ela esta gerando conversoes assistidas
- NAO tentar "consertar CVR" mudando lances (mudar a landing page ou a oferta)

### CPA (Custo por Aquisicao)

**O que mede:** gasto / conversoes. Quanto custou cada conversao.

**Benchmarks REALISTAS (R$, Search, non-brand, setor tipico):**
- E-commerce (moda): R$ 15-R$ 40
- E-commerce (eletronicos): R$ 30-R$ 80
- E-commerce (moveis): R$ 20-R$ 60
- E-commerce (alimentos): R$ 10-R$ 25
- Salao de beleza: R$ 15-R$ 30
- Clinica: R$ 40-R$ 120
- Dentista: R$ 80-R$ 250
- Plano de saude: R$ 150-R$ 400
- Curso online: R$ 30-R$ 100
- Faculdade (captacao): R$ 80-R$ 200
- Advogado: R$ 100-R$ 400
- SaaS B2B (contato): R$ 80-R$ 250
- Emprestimo: R$ 50-R$ 150
- Seguro auto: R$ 60-R$ 180
- Construtora (lead): R$ 60-R$ 200
- Imobiliaria (visita): R$ 40-R$ 150

**Sinais Verdes:**
- CPA dentro do benchmark ou abaixo da meta
- CPA estavel ou caindo com aprendizado da conta

**Sinais Amarelos:**
- CPA subiu 20-50%% sem perda de volume (concorrencia, sazonalidade)
- CPA baixo demais (pode ser brand nao separada)
- CPA subindo e volume caindo (estrategia de lance pode estar restringindo demais)

**Sinais Vermelhos:**
- CPA dobrou em 1 semana
- CPA > margem do produto (ROAS < 1)
- CPA subiu 50%%+ com volume caindo 50%%+ (tempestade perfeita — mercado e estrategia)

**O que NAO fazer:**
- NAO aumentar Target CPA de repente (2-3 dias de dados nao sao suficientes)
- NAO olhar apenas CPA sem ver o valor do ticket medio (CPA de R$ 200 e caro para produto de R$ 50; e barato para produto de R$ 5.000)
- NAO reduzir Target CPA drasticamente (vai matar o volume)
- NAO basear decisao de Target CPA em menos de 15 conversoes

### ROAS (Return on Ad Spend)

**O que mede:** receita / gasto. Retorno sobre o investimento em anuncios.

**Benchmarks REALISTAS:** depende da margem do produto, nao apenas do setor.

- **Margem baixa (5-20%%):** ROAS minimo vavel 5.0-20.0
- **Margem media (20-50%%):** ROAS minimo vavel 2.0-5.0
- **Margem alta (50-80%%):** ROAS minimo vavel 1.25-2.0

**Benchmarks por setor (Search):**
- E-commerce moda: 4-12x (margem 30-60%%)
- E-commerce eletronicos: 3-8x (margem 15-30%%)
- E-commerce moveis: 5-15x (margem 40-60%%)
- SaaS: depende do LTV, mas ROAS direto costuma ser 1-3x
- Seguros: 3-8x no primeiro clique (LTV e mais importante)
- Financeiro: 5-15x

**Sinais Verdes:**
- ROAS acima do ponto de equilibrio (break-even) considerando margem
- ROAS estavel ou melhorando
- ROAS aguenta Testes de novos publicos/segmentos

**Sinais Amarelos:**
- ROAS caindo gradualmente (concorrencia, sazonalidade)
- ROAS alto em brand (10-50x) esconde ROAS non-brand baixo (2-3x)
- ROAS caindo depois de expansao de keywords (normal — precisa de maturacao)

**Sinais Vermelhos:**
- ROAS < 1 com margem positiva = cada R$ 1 gasto gera R$ 0,90 de receita
- ROAS caindo 50%%+ em 2 semanas
- ROAS semanal positivo mas diario variando 300%% (instabilidade)

**O que NAO fazer:**
- NAO exigir ROAS 10x em todos os produtos
- NAO pausar campanha inteira com ROAS baixo — verifique por produto/keyword
- NAO esquecer que LTV pode justificar ROAS baixo no primeiro clique
- NAO comparar ROAS de campanha de marca com campanha de prospeccao

### Impression Share (IS%%)

**O que mede:** %% de impressoes que seu anuncio recebeu vs o total de impressoes que ele poderia receber.

**Benchmarks:**
- Search (marca): 90-99%%
- Search (non-brand): 30-80%%
- Display: 50-90%%
- Shopping: 40-80%%
- PMax: diffcil de medir (visao agregada)

**Sinais Verdes:**
- IS > 80%% para campanhas importantes
- IS estavel ou crescendo
- IS perdido por budget > rank (sinal de que o mercado quer seu anuncio)

**Sinais Amarelos:**
- IS 30-60%% em campanha principal (precisa avaliar se expandir ou nao)
- IS perdido igual por budget e rank (duplo problema)
- IS caindo sem mudanca na conta

**Sinais Vermelhos:**
- IS < 20%% com lost rank alto (nao consegue competir)
- IS de marca < 60%% (concorrencia esta tomando suas palavras de marca)
- IS caiu 40pp+ em 1 semana

**O que NAO fazer:**
- NAO buscar 100%% de IS em todas as campanhas (custa caro e pode ser desnecessario)
- NAO se preocupar com IS baixo se CPA e ROAS estao dentro da meta
- NAO usar IS como KPI principal de performance (e metrica de diagnostico, nao de resultado)

### Budget

**O que mede:** orcamento diario ou mensal da campanha.

**Analise:**

- **Budget diario medio:** e o que voce configura. O Google pode gastar ate 2x em um unico dia e compensar nos outros.
- **Budget share:** %% do orcamento total alocado para cada campanha.
- **Budget pacing:** quanto do orcamento ja foi gasto no mes vs quantos dias faltam.

**Sinais Verdes:**
- Gasto real = 85-100%% do orcamento
- Distribuicao entre campanhas compativel com prioridade
- Budget pacing no ritmo esperado

**Sinais Amarelos:**
- Gasto < 70%% em campanhas de alta performance (esta perdendo oportunidade)
- Gasto > 100%% todos os dias (orcamento muito baixo para a demanda)
- Budget mal distribuido (campanha C gasta 60%% mas entrega 10%% das conversoes)

**Sinais Vermelhos:**
- Gasto zero ha 3+ dias (campanha parou — verificar faturamento)
- Budget concentrado em campanha de baixa performance pressionando outras
- Budget diario previsto no inicio do mes no dia 15 ja gastou 80%%+ (vai faltar budget no fim do mes)

**O que NAO fazer:**
- NAO reduzir budget de campanha de baixo ROAS sem verificar se ela alimenta conversoes assistidas
- NAO distribuir budget igualmente sem pesar por performance
- NAO manter budget congelado por meses — reavalie periodicamente


---

## Camada 2 — Metricas de Diagnostico Tattico

### Quality Score (QS)

**O que mede:** O Google avalia a qualidade dos seus keywords/anuncios/paginas de destino em uma escala de 1 a 10 (10 = melhor). O QS afeta diretamente o CPC e o ranking.

**Os 3 componentes (com pesos reais aproximados):**

1. **Expected CTR (40%):** historico de CTR da keyword e do anuncio. Keywords novas podem ter expected CTR baixo por falta de dados.
2. **Ad Relevance (30%):** o anuncio corresponde a intencao da busca? O Google compara a query, a keyword, o anuncio e a landing page.
3. **Landing Page Experience (30%):** qualidade da pagina de destino: relevancia, velocidade, experiencia mobile, navegacao.

**Cenarios de uso:**

- **QS 8-10:** Competitivo. CPA tende a ser mais baixo, CPC mais baixo. Nao mexa se estiver convertendo.
- **QS 5-7:** Medio. Precisa de otimizacao. Verifique qual componente esta baixo.
- **QS 1-4:** Critico. Google esta basicamente te penalizando. O CPC e artificialmente alto.

**Interpretacao profunda:**

- Um QS 10 com 100 impressoes/semana significa que o Google tem dados insuficientes? Sim, pode ser "sorte" — confie em QS com >1.000 impressoes.
- Um QS 5 em palavra de alto volume (10.000+ impressoes) e o retrato real. Aja.
- QS nao e global — cada keyword tem seu QS. Mas o historico da conta afeta todas as keywords.

**Quando engana:**

- QS de keywords de marca e sempre 8-10 (ma informacao — e natural, nao indica esforco)
- QS de keywords novas (< 2 semanas) e instavel
- QS sazonal (ex: "presente de Natal" em julho) pode estar baixo porque o Google nao tem dados recentes
- O QS mostrado no Google Ads e uma "foto" — atualiza periodicamente

### Impression Share Lost (Rank vs Budget)

**O que mede:** separa a causa de perda de impressoes entre orcamento insuficiente (lost IS budget) e posicionamento inadequado (lost IS rank).

**Interpretacao:**

| Lost Budget | Lost Rank | Diagnostico |
|---|---|---|
| Alto | Baixo | ORCAMENTO — aumento de budget deve gerar mais impressoes. Bom sinal: a demanda existe. |
| Baixo | Alto | RANK — QS ou lance estao baixos. Precisa melhorar relevancia ou aumentar lances. |
| Alto | Alto | PROBLEMA DUPLO — precisa de mais budget E melhor QS/lance. O mais comum. |
| Baixo | Baixo | IS alto — campanha saudavel. |

**Quando e a metrica certa:** ao decidir se deve aumentar orcamento ou melhorar anuncios.
**Quando engana:** se a segmentacao for muito restrita, o "lost budget" pode ser baixo simplesmente porque o Google nao tem para quem mostrar.

### Search Impression Share

**O que mede:** IS especifico da Rede de Pesquisa (exclui Display/YouTube).

**Analise:**
- Search IS global: pode ser baixo se voce tem muitas keywords irrelevantes que competem entre si.
- Search lost top IS: perdeu de ficar no topo.
- Search lost absolute top IS: perdeu de ficar na posicao 1.

**Cenarios de uso:**
- Se lost top > lost absolute top: seu anuncio aparece abaixo dos concorrentes, mas nao no final da pagina.
- Se lost absolute top > lost top: concorrencia feroz pela primeira posicao. Considere se vale a pena.

### Search Lost Top IS / Search Lost Absolute Top IS

**O que mede:** % de impressoes perdidas no topo (acima dos resultados organicos) e na primeira posicao absoluta.

**Interpretacao:**

| Lost Top | Lost Abs. Top | Diagnostico |
|---|---|---|
| <20% | <30% | Boa visibilidade |
| 20-40% | 30-60% | Visibilidade mediana — pode otimizar |
| >40% | >60% | Baixa visibilidade — QS, lance ou concorrencia |

**Quando usar:** quando a campanha esta com IS baixo e voce quer entender se o problema e aparecer ou aparecer bem.

### Taxa de Conversao por Dispositivo

**O que mede:** divisao da taxa de conversao entre mobile, desktop e tablet.

**Benchmarks (Search):**
- Mobile: 1.5-4x desktop em e-commerce (mais trafego, CVR menor)
- Desktop: CVR 1.5-2x mobile
- Tablet: volume baixo, tende a seguir desktop

**Interpretacao:**

- **Mobile com CVR baixa e muito clique:** problema de responsividade ou experiencia mobile
- **Desktop com CVR muito superior ao mobile:** site nao otimizado para mobile
- **Mobile CVR igual ou maior que desktop:** site bem feito ou publico mobile qualificado

**Cenarios de uso:**
- Se mobile = 70% dos cliques e 30% das conversoes, priorize otimizacao mobile
- Se desktop = 30% dos cliques e 60% das conversoes, lance por dispositivo pode ser ajustado

**Quando engana:**
- Se a tag de conversao nao funciona bem em mobile
- Se o formulario mobile e mais longo que o desktop

### Tempo ate Conversao (Time Lag)

**O que mede:** quantos dias entre o primeiro clique e a conversao.

**Benchmarks:**
- E-commerce (impulso): 0-3 dias
- E-commerce (alto ticket): 3-14 dias
- Saude (agendamento): 1-7 dias
- Educacao: 7-30 dias
- SaaS B2B: 7-90 dias
- Seguros: 7-30 dias
- Imobiliario: 7-60 dias
- Financeiro (credito): 1-14 dias

**Interpretacao:**
- Se o time lag e maior que sua janela de conversao, voce esta perdendo conversoes
- Time lag aumenta em periodos de consideracao (seguro, educacao, imovel)
- Time lag curto indica intencao de compra imediata

**Cenario de uso:** util para janela de conversao, modelo de atribuicao e para entender qual campanha merece credito.

**Quando engana:** em ciclos sazonais (ex: presente de Natal em outubro tem lag longo porque a compra e em dezembro).

### Top vs Other CPC

**O que mede:** diferenca de CPC entre anuncios no topo da pagina vs em outras posicoes.

**Analise:**
- **Top CPC:** o custo para aparecer acima dos resultados organicos.
- **Other CPC:** o custo para aparecer em qualquer outra posicao.

**Padrao:** Top CPC geralmente e 20-60% mais caro que Other CPC.

**Cenarios de uso:**
- Se Top CPC for 80%+ mais caro que Other CPC: a primeira posicao e muito cara — talvez nao valha a pena insistir no topo
- Se a diferenca Top vs Other for < 10%: o ranking nao esta impactando o CPC — lance pode estar muito baixo ou muito alto

**Quando engana:** em palavras com pouco volume, a amostra pode ser insuficiente.

### Brand vs Non-brand CPA

**O que mede:** a diferenca de CPA entre palavras de marca e nao-marca.

**Interpretacao:**
- **CPA brand:** idealmente < 30% do CPA non-brand
- **CPA brand alto (proximo do non-brand):** concorrencia pesada em marca, problemas no site ou palavras de marca amplas demais
- **CPA non-brand subindo sem brand subir:** concorrencia aumentou no setor

**Cenarios de uso:**
- Essencial para entender a verdadeira eficiencia da campanha de prospeccao
- CPA geral "R$ 30" pode ser R$ 5 de brand e R$ 80 de non-brand — decisoes diferentes para cada

**Quando engana:**
- Se a separacao brand/non-brand nao esta correta (keywords amplas podem capturar trafego de marca)

### Match Type Performance

**O que mede:** desempenho por tipo de correspondencia (exata, frase, ampla).

**Benchmarks:**
| Tipo | CTR | CPC | Conversoes | CVR | CPA |
|---|---|---|---|---|---|
| Exata | 4-10% | 100% (base) | Alta | 3-8% | 100% (base) |
| Frase | 2-5% | 80-100% do exato | Media-Alta | 2-5% | 110-150% do exato |
| Ampla | 1-3% | 60-90% do exato | Baixa-Media | 1-3% | 150-300% do exata |

**Interpretacao:**
- **Se exata converte melhor:** padrao esperado. Use ampla para descoberta e exata para controle.
- **Se ampla converte igual ou melhor que exata:** segmentacao de publico ou landing page muito boa — ou as exatas sao ruins.
- **Se frase converte mal:** provavelmente o search term nao e tao relevante.

**Cenarios de uso:**
- Quando CPA esta subindo, verifique se a correspondencia ampla esta gastando mais que o esperado
- Ao planejar expansao, use ampla para descoberta com negativas frequentes

**Quando engana:** correspondencia ampla com redes de pesquisa parceiras pode gerar muito trafego irrelevante — desative.

### Palavras de Search Term Sem Conversao

**O que mede:** search terms que geraram cliques mas nunca converteram.

**Interpretacao:**
- **Search terms com >20 cliques e zero conversao:** precisa de analise. Pode ser search term irrelevante, landing page ruim para aquela intencao, ou baixo volume
- **Search terms com >50 cliques e zero conversao:** acao necessaria — adicione como negativa ou ajuste a landing page
- **Search terms de marca com zero conversao:** problema grave (algo quebrado no funil)

**Cenarios de uso:**
- Revise semanalmente search terms com >10 cliques
- Adicione negativas para termos irrelevantes
- Analise landing page para termos relevantes que nao convertem

**Quando engana:** se a janela de conversao e maior que o periodo analisado (ex: lead educacional pode converter em 30 dias).

### ROAS por Produto (Shopping)

**O que mede:** ROAS individual de cada produto no feed do Shopping.

**Interpretacao:**
- **ROAS alto (>10x):** produto popular. Considere aumentar investimento.
- **ROAS medio (3-10x):** saudavel. Monitore concorrencia de preco.
- **ROAS baixo (0-3x):** produto pode estar com preco descompetitivo, imagem fraca, titulo ruim ou baixa intencao.
- **ROAS negativo (custa + que vende):** pause ou ajuste o produto.

**Cenarios de uso:**
- Descobrir "produtos dreno" que consomem budget sem retorno
- Identificar produtos-heroi para aumentar lances

**Quando engana:** produtos sazonais, produtos com estoque limitado (podem ter ROAS baixo porque estao em falta).

### Taxa de Abandono de Carrinho

**O que mede:** % de usuarios que adicionaram ao carrinho mas nao concluiram a compra.

**Benchmark:** 60-80% e a taxa de abandono tipica no Brasil.

**Interpretacao no Google Ads:**
- Google Ads nao mede abandono de carrinho diretamente — precisa de integracao com a tag de e-commerce
- Quando disponivel: alto abandono indica problemas no checkout (frete caro, formas de pagamento, burocracia)

**Cenarios de uso:**
- Combinar com dados de ROAS por produto: um produto com ROAS 2x mas 80% de abandono pode ter problema de preco no checkout
- Usar para campanhas de remarketing dinamico de carrinho abandonado

---

## Camada 3 — Metricas de Investigacao Profunda

### Atribuicao Data-driven vs Last-click Gap

**O que mede:** a diferenca percentual entre o modelo de atribuicao data-driven e last-click.

**Complexidade:** media-alta. Exige que a conta tenha conversoes suficientes para DDA funcionar (>15 nos 30 dias anteriores).

**Interpretacao:**
- **Gap < 10%:** a atribuicao nao esta fazendo diferenca significativa. O modelo de conversao e simples (ciclo curto, 1 clique).
- **Gap 10-30%:** normal. Display/YouTube/Discovery estao recebendo mais credito do que em last-click. Search (especialmente brand) perde credito.
- **Gap > 30%:** sua jornada do cliente e complexa. Confiar cegamente em last-click pode levar a cortar canais de descoberta que geram conversao indireta.

**Trade-offs:**
- DDA e mais preciso para jornadas multicanal, mas exige dados suficientes
- Last-click e mais simples, mas subestima canais de topo de funil

**Quando usar:** antes de qualquer decisao de corte de orcamento em Display/YouTube/Discovery.

### Search Term Overlap Analysis

**O que mede:** quando o mesmo search term ativa keywords em campanhas diferentes.

**Interpretacao:**

- **Canibalizacao intencional:** ter o mesmo search term em campanhas separadas (ex: marca em campanha de marca e em campanha de non-brand) e desejavel — o Google prioriza a com maior QS/lance.
- **Canibalizacao desperdicio:** search term "plano odontologico" em 5 campanhas diferentes, cada uma com granularidade diferente. Voce esta competindo consigo mesmo.
- **Overlap alto com IS baixo:** voce esta fragmentando seu proprio IS.

**Complexidade:** alta. Exige extracao de search terms em multiplas campanhas e comparacao.

**Quando usar:** quando o IS geral esta baixo mas cada campanha individualmente parece ok.

### Incrementality Measurement (Geo Lift, Holdout)

**O que mede:** se suas campanhas estao gerando conversoes incrementais ou canibalizando conversoes que aconteceriam organicamente.

**Metodo:**
- **Geo lift:** divide o mercado em grupos regionais. Um grupo recebe anuncios, outro nao. Compara a diferenca de conversoes.
- **Holdout:** uma % do publico nao ve anuncios. Compara incrementalidade.
- **Google's Brand Lift:** especifico para YouTube/Display.

**Complexidade:** muito alta. Exige configuracao de experimentos e pode levar 4-8 semanas.

**Trade-offs:**
- Extremamente caro em termos de orcamento perdido (holdout significa deixar de anunciar para um grupo)
- O resultado e o mais confiavel de todos
- So faz sentido quando o orcamento e grande (> R$ 50k/mes)

**Quando engana:** sazonalidade pode distorcer resultados se o experimento cruzar fronteiras sazonais.

### Brand Lift Studies (YouTube/Display)

**O que mede:** impacto das campanhas de video/display em metricas de marca como reconhecimento, consideracao e preferencia.

**Interpretacao:**
- **Awareness lift:** % adicional de pessoas que lembram da sua marca vs grupo de controle
- **Consideration lift:** % adicional que consideraria comprar
- **Preference lift:** % adicional que prefere sua marca
- **Search uplift:** aumento nas buscas pela sua marca durante/periodo da campanha

**Complexidade:** alta. Exige campanha com volume minimo de impressoes (geralmente > 1-2 milhoes) e questionario do Google.

**Quando usar:** campanhas de branding/reconhecimento onde CPA direto nao faz sentido.

**Quando engana:** amostra pequena, publico muito nichado, vies de resposta.

### New vs Returning Customer (Customer Lifecycle)

**O que mede:** divisao entre novos clientes e clientes recorrentes gerados pelo Google Ads.

**Configuracao:** exige tag de conversao com parametros de new/returning (disponivel em Enhanced Conversions ou via feed offline).

**Interpretacao:**
- **% de novos clientes baixa (< 20%):** campanha esta capturando apenas clientes existentes
- **% de novos clientes alta (> 50%):** saudavel para aquisicao, mas pode indicar que clientes recorrentes estao usando Google Ads como atalho

**Trade-offs:**
- Dados precisos exigem implementacao correta da tag
- Clientes recorrentes via Google Ads podem ser "vazamento" — voce esta pagando para clientes fieis que iriam ao site de qualquer forma

**Quando usar:** para decidir entre campanhas de aquisicao vs retencao.

### Cross-device Conversions

**O que mede:** conversoes que ocorreram em um dispositivo diferente daquele em que o clique aconteceu.

**Interpretacao:**
- Alta (15-30%+): seu publico pesquisa em mobile e compra em desktop (ou vice-versa)
- Baixa (< 5%): conversoes no mesmo dispositivo

**Complexidade:** media.

**Quando usar:** quando voce suspeita que o Google Ads esta perdendo credito por conversoes cross-device.

**Quando engana:** se o usuario nao esta logado na conta Google, o Google nao consegue rastrear.

### Assisted Conversions

**O que mede:** conversoes onde o Google Ads esteve presente como ponto de contato de assistencia (nao o ultimo clique).

**Interpretacao:**
- **Assisted / Last-click ratio:** se > 1, o canal e mais assistente do que finalizador (Display, YouTube)
- Se < 1, canal e mais finalizador (Search, Shopping de marca)
- Display/YouTube costumam ter assisted/last-click ratio 2-5x

**Quando usar:** para entender o verdadeiro valor de canais de topo de funil.

**Quando engana:** se a janela de conversao e curta e nao captura assistencias anteriores.

### Clicks vs View-through Conversions (Display/YouTube)

**O que mede:** conversoes que vieram de um clique no anuncio vs conversoes que vieram de uma impressao sem clique.

**Interpretacao:**
- **View-through rate alto (>50% do total de conversoes do Display):** suspeito. View-through e uma metrica fraca — o usuario viu o anuncio mas nao clicou. Pode ter convertido organicamente depois.
- **View-through rate baixo (< 20%):** o Display esta gerando principalmente cliques.
- **View-through e INFLADA:** qualquer conversao dentro da janela de view-through (30 dias) conta. Infla o valor do Display artificialmente.

**Complexidade:** baixa (o dado esta la), mas a interpretacao e complexa.

**Quando usar:** ao justificar investimento em Display (ou questiona-lo).

**Quando engana:** SEMPRE. View-through e a metrica mais enganosa do Google Ads. Use com cautela.

### Campaign Experiments (Drafts & Experiments)

**O que mede:** mudanca de performance em um experimento controlado (A/B test) dentro do Google Ads.

**Tipos:**
- **Campanha vs campanha:** compare uma campanha experimental com a original
- **Custom experiment:** grupos aleatorios dentro da mesma campanha
- **Video experiments:** A/B de criativos de video

**Interpretacao:**
- **Resultado com significancia estatistica:** siga o vencedor
- **Sem significancia:** continue coletando dados ou aceite que a mudanca nao e detectavel nesse volume

**Complexidade:** alta. Exige:

- Configuracao correta do experimento (split 50/50)
- Duracao minima de 2-3 semanas (dependendo do volume)
- Sem mudancas externas durante o experimento

**Trade-offs:**
- Exige trafego suficiente para resultados significativos
- Exige disciplina para nao encerrar cedo

**Quando engana:** encerrar experimento ao ver resultado "positivo" cedo demais (vies de confirmacao).

### Performance Max Asset Group Analysis

**O que mede:** performance de cada asset group (grupo de ativos) dentro de uma campanha PMax.

**Interpretacao:**
- **Asset group com ROAS 2x abaixo da media:** problema de ativos, segmentacao ou oferta
- **Asset group com CTR baixo:** imagens/headlines fracas, ou segmentacao errada
- **Asset group sem dados de rede:** o PMax nao revela onde esta gastando

**Complexidade:** alta. PMax e uma caixa-preta limitada.

**Quando engana:** o PMax esconde muito. Voce ve o agregado, mas nao consegue atribuir performance a Search vs Shopping vs Display vs YouTube dentro da mesma campanha.

### Audience Insights (Demographics, Affinity, In-market)

**O que mede:** perfil demografico e de interesses dos usuarios que interagiram com seus anuncios.

**Interpretacao:**
- **Alta concentracao (> 60%) em uma faixa etaria:** natural se o produto e especifico
- **Diferenca entre audiencia que clicou vs converteu:** esta atraindo o publico errado?
- **In-market segments:** quais intencoes de compra seus anuncios estao capturando

**Complexidade:** baixa-media.

**Quando engana:** dados demograficos para publicos pequenos sao modelados (nao reais). Confie apenas em publicos com > 5.000 impressoes.

### Customer Match Performance

**O que mede:** performance de campanhas segmentadas por listas de Customer Match (e-mails/telefones da sua base).

**Interpretacao:**
- **Match rate:** % de registros da sua lista que o Google conseguiu encontrar. Ideal: > 60%.
- **CPA em Customer Match:** deve ser MAIOR que o CPA de prospeccao (e trafego mais quente)
- **ROAS em Customer Match:** idealmente 2-5x maior que non-brand

**Complexidade:** media. Exige upload da lista com e-mails/telefones (hash por SHA-256).

**Trade-offs:**
- Customer Match e limitado pelo match rate
- Politicas de privacidade (LGPD) afetam a disponibilidade
- Pode nao escalar se sua base e pequena

**Quando engana:** match rate baixo pode DISTORCER os resultados (apenas os usuarios "matchados" entram).

---

## Contextos x Metricas por Rede

### SEARCH — Search Contexts especificos

#### Contexto: "CPA subiu mas CTR estavel"

**Interpretacao:**
- Se CTR esta estavel, o problema NAO e o anuncio (as pessoas continuam clicando na mesma proporcao)
- Causas possiveis:
  1. Concorrencia elevou o CPC (verifique CPC e leilao)
  2. A Taxa de Conversao caiu (verifique CVR e Landing Page)
  3. Adicionou keywords menos relevantes que diluiram a conversao
  4. Sazonalidade — usuarios pesquisando mas sem intencao de compra imediata
- Acao: va para o diagnostico entre CPC vs CVR. Qual dos dois mudou?

#### Contexto: "Impressions share caindo"

**Interpretacao:**
- IS caindo SEMPRE tem uma causa. Verifique:
  1. Adicionou novas keywords ou expandiu segmentacao? (IS cai MECANICAMENTE)
  2. Concorrencia aumentou lances? (use o relatorio de leilao — Auction Insights)
  3. QS caiu em keywords importantes?
  4. Orcamento acabando mais cedo? (perde IS por budget)
  5. Politica de anuncios afetou alguma keyword?
- Acao: abra o relatorio de IS perdido por rank vs budget. Qual e a dominante?

#### Contexto: "Quality Score baixo em palavras-chave importantes"

**Interpretacao:**
- Identifique QUAL componente esta baixo (expected CTR, ad relevance, landing page)
- Se expected CTR baixo: reescreva o anuncio, teste novas headlines/calls-to-action
- Se ad relevance baixo: o anuncio nao corresponde a intencao da keyword — crie anuncios especificos
- Se landing page baixa: pagina de destino nao atende a promessa do anuncio — revise UX, velocidade, conteudo
- Acao: nao mude sem entender qual componente

#### Contexto: "Muita impressao em search term irrelevante"

**Interpretacao:**
- Correspondencia ampla esta capturando termos nao relacionados
- Acao IMEDIATA: adicione search terms irrelevantes como negativas
- Acao ESTRATEGICA: reavalie se a correspondencia ampla e adequada para essa campanha
- Se for correspondencia exata: a keyword em si e muito ampla

#### Contexto: "Campanha de marca vs nao-marca"

**Interpretacao:**
- A separacao de marca vs nao-marca e OBRIGATORIA em contas que trabalham prospeccao
- Marca: baixo CPC, alta CVR, alto ROAS — protecao de marca
- Nao-marca: alto CPC, baixa CVR, baixo ROAS — prospeccao
- ROAS geral pode ser 8x com brand 50x e non-brand 3x — nao se engane
- Acao: crie campanhas separadas, com budget separado, e ANALISE SEPARADAMENTE

#### Contexto: "Diferenca entre dispositivo mobile e desktop"

**Interpretacao:**
- Mobile tende a ter mais volume mas menor CVR
- Desktop tende a ter menor volume mas maior CVR
- Se mobile CVR >= desktop CVR: sua landing page mobile e boa (ou seu desktop e muito ruim)
- Acao: verifique o site — se mobile CVR for < 50% da desktop, priorize otimizacao mobile
- Considere diferentes ajustes de lance por dispositivo

#### Contexto: "Palavras de correspondencia exata vs ampla"

**Interpretacao:**
- Exata: controle, previsibilidade, CPC mais alto, CVR mais alta
- Ampla: descoberta, volume, CPC mais baixo, CVR mais baixa, search terms imprevisiveis
- A estrategia moderna do Google favorece ampla + smart bidding
- Acao: use ampla para descoberta em campanhas separadas. Use exata para controle de ROAS com dados historicos

### SHOPPING — Contextos especificos de e-commerce

#### Contexto: "ROAS por produto muito variado"

**Interpretacao:**
- E NORMAL (e desejavel) que produtos tenham ROAS diferente
- Produtos de alto ticket tendem a ter ROAS mais baixo (mas valor absoluto maior)
- Produtos de baixo ticket podem ter ROAS alto mas margem baixa
- Acao: priorize produtos com (ROAS x margem) maior — o verdadeiro retorno
- Filtrar por "produtos dreno" (gasto sem retorno) e "produtos heroi" (high ROAS)

#### Contexto: "Produtos sem impressao"

**Interpretacao:**
- Causas: feed desatualizado, preco nao competitivo, produto sem estoque, violacao de politica, categoria excluida
- Check: Google Merchant Center — verifique status dos produtos e violacoes
- Produtos novos podem levar 3-7 dias para comecar a ter impressoes
- Acao: abra o Merchant Center e resolva os erros do feed

#### Contexto: "Taxa de clique baixa no Shopping"

**Interpretacao:**
- CTR baixo = anuncio de produto nao esta atraente
- Causas comuns: imagem fraca, preco nao competitivo, titulo generico, avaliacoes baixas
- Acao: melhore imagens do produto, otimize titulos com palavras-chave, avalie competitividade de preco
- Considere que CTR de Shopping e naturalmente menor que Search

#### Contexto: "Preco vs concorrentes no leilao"

**Interpretacao:**
- O Google Shopping mostra o preco. Se seu preco e maior que a media, o CTR cai
- Se seu preco e o mais baixo, pode ter CTR alto mas margem baixa
- O leilao do Shopping considera: lance, qualidade do feed, relevancia do produto, avaliacao do vendedor
- Acao: para competir com preco alto, tenha imagem + titulo + avaliacao superiores

### DISPLAY / YOUTUBE — Contextos especificos

#### Contexto: "View-through conversion vs click-through"

**Interpretacao:**
- View-through conversion (VTC): usuario viu o anuncio (sem clique) e converteu depois
- Click-through conversion (CTC): usuario clicou no anuncio e converteu
- VTC e controversa — o Google conta qualquer conversao dentro da janela de 30 dias apos a impressao
- Pode inflar artificialmente o valor do Display
- Acao: ao reportar Display, mostre VTC e CTC separadamente. NAO some sem contexto

#### Contexto: "CPM alto com CTR baixo"

**Interpretacao:**
- CPM alto: seu anuncio esta caro para aparecer
- CTR baixo: as pessoas nao estao clicando
- Pode ser:
  1. Segmentacao muito especifica (CPM alto pela concorrencia, CTR baixo pelo publico pequeno)
  2. Criativo fraco ou formatos inadequados
  3. Posicionamento em sites caros e pouco relevantes
- Acao: revise posicionamentos e criativos. Considere mudar de CPM para CPV (YouTube)

#### Contexto: "Brand lift nao mensuravel"

**Interpretacao:**
- Brand lift exige um volume MINIMO de impressoes (geralmente > 1-2 milhoes)
- Se voce nao tem volume suficiente, o Brand Lift nao atinge significancia
- Alternativas: pesquisa de marca propria antes/depois, Google Trends, Search volume da marca
- Acao: aceite que brand lift nao e para todos os orcamentos. Use metricas substitutas (search uplift, site traffic direct)

### PERFORMANCE MAX — Contextos especificos

#### Contexto: "Caixa preta — nao vejo onde gasta"

**Interpretacao:**
- PMax e intencionalmente opaco — o Google nao detalha onde o orcamento foi gasto (Search vs Shopping vs Display vs YouTube vs Gmail vs Discover)
- Voce ve apenas a performance agregada
- Mitigacao: crie asset groups separados por produto/categoria para ter granularidade
- Mitigacao 2: use relatorios de topicos ou campanhas separadas para comparar
- Acao: aceite a falta de transparencia, mas monitore asset groups

#### Contexto: "Asset group com performance muito abaixo"

**Interpretacao:**
- Dentro de uma campanha PMax, um asset group especifico esta com ROAS 50% abaixo da media
- Pode ser: ativos ruins (imagens/headlines), segmentacao errada, produto sazonal fora de epoca
- Acao: revise os ativos do asset group. Adicione novas imagens, headlines e videos. Ajuste a segmentacao

#### Contexto: "PMax canibalizando Search"

**Interpretacao:**
- PMax pode incluir Search. Se voce tem campanhas Search separadas + PMax, elas podem competir no mesmo search term
- O Google diz que nao canibaliza, mas na pratica ha sobreposicao
- Sinal de canibalizacao: campanhas Search standard perderam volume depois de ativar PMax
- Acao: monitore de perto. Se a canibalizacao for alta, considere:
  1. Excluir campanhas de marca do PMax (via brand exclusions)
  2. Reduzir orcamento do PMax e realocar para Search
  3. Aceitar a canibalizacao se PMax entrega melhor ROI geral


---

## Protocolo de Leitura de Cenarios

Siga este fluxo logico quando o usuario fornecer dados de Google Ads. Nao pule etapas.

### Fase 0: Obter o Contexto Minimo

Antes de analisar qualquer metrica, voce PRECISA saber:
1. Qual o SETOR/CATEGORIA do anunciante?
2. Qual o OBJETIVO da campanha? (Conversao, Reconhecimento, Trafego, Lead, Vendas)
3. Qual a REDE? (Search, Shopping, Display, YouTube, PMax, Demand Gen)
4. Qual o ORCAMENTO mensal?
5. Qual o TICKET MEDIO e a MARGEM do produto/servico?
6. Qual o MODELO DE ATRIBUICAO configurado?
7. Qual a JANELA DE CONVERSAO?
8. A campanha existe ha quanto tempo? (>15 conversoes nos ultimos 30 dias?)
9. Separa brand vs non-brand?

Se o usuario nao forneceu estes dados automaticamente, FACA AS PERGUNTAS.

### Fase 1: Verificar Metricas de Camada 1

Pegue os dados fornecidos e classifique cada metrica da Camada 1:

- Cliques: volume e tendencia
- Impressoes: volume e IS%
- CPC: dentro do benchmark do setor?
- CTR: adequado para a rede?
- Gasto: % do orcamento utilizado
- Conversoes: volume, consistencia, qualidade
- CVR: dentro do benchmark do setor?
- CPA: dentro da meta e do benchmark?
- ROAS: acima do break-even considerando margem?
- IS%: aceitavel?
- Budget: pacing, alocacao

Para cada metrica, atribua: VERDE, AMARELO ou VERMELHO.

### Fase 2: Verificar Coerencia entre Metricas

Alguns sinais de incoerencia:

- CTR alta + CVR baixa = anuncio clickbait ou landing page desconectada
- CPA baixo + IS% baixo = esta tudo bem com quem converte, mas o alcance e limitado
- CPC baixo + ROAS baixo = trafego barato mas de baixa intencao
- Impression share alto + CPA alto = visibilidade demais, pagando caro por posicoes que nao convertem

Identifique INCOERENCIAS antes de sugerir acoes.

### Fase 3: Camada 2 se Camada 1 Apontar Problema

Se a Camada 1 mostrou sinais amarelos ou vermelhos, mergulhe na Camada 2:

1. Quality Score: esta baixo em keywords importantes? Qual componente?
2. IS Lost rank vs budget: qual esta dominando?
3. Taxa de conversao por dispositivo: mobile esta convertendo?
4. Tempo ate conversao: compativel com o ciclo do produto?
5. Brand vs non-brand CPA: qual esta impulsionando o CPA?
6. Match type performance: ampla esta gastando demais?
7. Search terms: ha termos irrelevantes gastando budget?
8. ROAS por produto (Shopping): tem produto dreno?

Para cada possivel causa, priorize por IMPACTO POTENCIAL x FACILIDADE DE IMPLEMENTACAO.

### Fase 4: Camada 3 se Camada 2 Nao Explicar

Se mesmo com a Camada 2 voce nao encontra a causa, e hora de investigacao profunda:

1. Modelo de atribuicao: DDA vs last-click gap?
2. Search term overlap: canibalizacao?
3. Assisted conversions / view-through: canais de topo estao subvalorizados?
4. Incrementality: as conversoes sao incrementais?
5. Experimentos: ja testou mudancas?

### Fase 5: Priorizar Acoes

Priorize acoes por:

1. **Gravidade:** risco de parar a campanha? perda financeira?
2. **Facilidade:** ajuste de lance, adicionar negativa, mudar anuncio — acoes rapidas primeiro
3. **Impacto:** o que vai gerar mais resultado com menos esforco

Apresente ao usuario:
- Diagnostico resumido (1-2 frases)
- Prioridade de acoes (ordenada)
- Metricas que voce usou para chegar la
- O que monitorar depois da acao

---

## Arvores de Decisao

### Arvore 1: CPA Subiu de Repente

```
CPA subiu >20% em 1-3 dias?
|
+-- Sim -> Verificar CPC e CVR
|        |
|        +-- CPC subiu proporcionalmente?
|        |   +-- Sim -> Verificar QS e concorrencia
|        |   |        |
|        |   |        +-- QS caiu? -> Otimizar componente do QS (expected CTR, ad relevance, LP)
|        |   |        +-- QS estavel? -> Concorrencia aumentou (Auction Insights)
|        |   |        |              |
|        |   |        |              +-- Concorrencia nova? -> Decidir: competir ou nicho diferente
|        |   |        |              +-- Concorrencia sazonal? -> Aguardar ou ajustar lance
|        |   |        +-- CPC estavel? -> Ir para "CVR caiu"
|        |   |
|        |   +-- CPC estavel? -> CVR caiu
|        |        |
|        |        +-- Search terms mudaram? (nova correspondencia ampla trouxe trafego ruim)
|        |        +-- Landing page mudou? (teste A/B, reformulacao)
|        |        +-- Dispositivo: mobile CVR despencou? (site responsivo quebrou)
|        |        +-- Sazonalidade? (periodo de baixa intencao)
|        |
|        +-- CPC caiu? (raro, mas verificar)
|            +-- Trafego de baixa qualidade? -> ver search terms
|
+-- Nao -> Oscilacao normal. Monitorar.
|   +-- CPA variou <20% -> Nenhuma acao. Aguardar 3-5 dias.
|
+-- CPA subiu gradualmente (2+ semanas)?
    +-- Perda gradual de eficiencia (concorrencia entrando, QS degradando, fadiga)
```

### Arvore 2: ROAS Caindo

```
ROAS caiu >30% em relacao ao periodo anterior?
|
+-- Sim -> Separar brand vs non-brand
|        |
|        +-- Brand ROAS estavel? -> Problema e NON-BRAND
|        |   +-- Verificar: CPC subiu? CVR caiu? Search terms mudaram?
|        |
|        +-- Non-brand ROAS estavel? -> Problema e BRAND
|        |   +-- Concorrencia em marca? Google esta exibindo anuncios de concorrentes?
|        |       +-- Aumentar lance de marca ou adicionar concorrentes como negativas
|        |
|        +-- Ambos cairam? -> Problema SISTEMICO
|            +-- Mercado: crise/queda de demanda?
|            +-- Site: taxa de conversao geral caiu?
|            +-- Tag de conversao: esta funcionando?
|
+-- Nao -> Verificar se ROAS esta acima do break-even
|   +-- Sim -> Monitorar.
|   +-- Nao -> Mesmo que a queda nao seja "repentina", o ROAS esta baixo demais.
|
+-- ROAS caiu sazonalmente? (comparar com mesmo periodo do ano anterior)
    +-- Se sim: comportamento esperado. Comparar YoY e mais confiavel que WoW.
```

### Arvore 3: Impression Share Baixo

```
IS% < 50% na campanha principal?
|
+-- Sim -> Verificar IS Lost por Rank vs Budget
|        |
|        +-- Lost IS (Budget) > Lost IS (Rank)?
|        |   +-- Sim -> ORCAMENTO: aumentar budget (se CPA aceitavel)
|        |   |   +-- CPA ja esta alto? -> Verificar se aumentar budget vai diluir performance
|        |   +-- Nao -> Verificar Lost IS (Rank)
|        |
|        +-- Lost IS (Rank) > Lost IS (Budget)?
|        |   +-- Sim -> Verificar QS, Lance, Concorrencia
|        |   |   +-- QS < 7? -> Otimizar QS (anuncio, landing page)
|        |   |   +-- Lance vs concorrencia? -> Aumentar lance ou aceitar posicao mais baixa
|        |   |   +-- Concorrencia subiu? -> Auction Insights
|        |   +-- Nao -> Ambos baixos? IS bom. Verifique segmentacao
|        |
|        +-- Lost IS (Rank) ~= Lost IS (Budget)?
|            +-- Duplo problema: precisa de budget + otimizacao
|
+-- Nao -> IS > 50%: aceitavel.
|   +-- IS > 80%: excelente (a menos que budget esteja sobrando)
|
+-- IS% caindo progressivamente?
    +-- Expandiu keywords/segmentacao?
    |   +-- Sim -> IS cai MECANICAMENTE. Acompanhe CPA, nao IS.
    |   +-- Nao -> Concorrencia aumentou. Verifique Auction Insights.
    +-- Nao -> Tendencia normal
```

### Arvore 4: CTR Baixo nos Anuncios de Search

```
CTR < 2% em campanha de Search?
|
+-- Sim -> Verificar posicao do anuncio (Top vs Other)
|        |
|        +-- Top % < 50%? -> Anuncio aparece abaixo da dobra
|        |   +-- QS baixo? -> Otimizar QS
|        |   +-- Lance baixo? -> Aumentar lance
|        |   +-- Concorrencia alta? -> Nicho especifico ou aceitar posicao
|        |
|        +-- Top % > 50% com CTR baixo? -> Anuncio aparece no topo mas nao engaja
|        |   +-- Headline fraca? -> Testar novas headlines com beneficios claros
|        |   +-- Extensoes insuficientes? -> Adicionar sitelinks, callouts, snippets
|        |   +-- Anuncio muito generico? -> Criar anuncios especificos por keyword group
|        |   +-- Concorrencia com mais extensoes/formatos? -> Melhorar ativos
|        |
|        +-- Search terms relevantes?
|            +-- Nao -> Search terms errados estao ativando seu anuncio. Adicionar negativas.
|
+-- Nao -> CTR > 2% em Search: aceitavel.
|
+-- CTR estava bom e caiu?
    +-- Novo anuncio perdeu o teste? -> Reativar anuncio vencedor
    +-- Extensoes removidas? -> Verificar aprovacao das extensoes
    +-- Concorrencia lancou anuncio similar? -> Diferenciar proposta de valor
```

### Arvore 5: Quality Score Baixo em Palavras Estrategicas

```
QS < 5 em keyword com >500 impressoes/mes?
|
+-- Sim -> Verificar componente do QS
|        |
|        +-- Expected CTR baixo? -> Reescrever anuncio
|        |   +-- Headline nao atrai atencao? -> Testar CTAs
|        |   +-- Descricao fraca? -> Incluir beneficios
|        |   +-- Extensoes faltando? -> Adicionar extensoes (aumentam CTR esperado)
|        |
|        +-- Ad Relevance baixo? -> Criar anuncio especifico para essa keyword
|        |   +-- Anuncio generico serve para 50 keywords? -> Criar grupos de anuncios menores
|        |   +-- Keyword nao esta no anuncio? -> Incluir keyword no headline ou descricao
|        |
|        +-- Landing Page Experience baixo? -> Melhorar pagina de destino
|            +-- Pagina lenta? -> Otimizar velocidade (Core Web Vitals)
|            +-- Pagina irrelevante? -> Criar landing page com conteudo especifico
|            +-- Mobile e ruim? -> Otimizar responsividade
|
+-- Nao -> QS > 5: aceitavel. Se QS > 8: excelente.
|
+-- QS baixo mas < 500 impressoes? -> Pode ser falta de dados.
    +-- Aguardar mais volume antes de otimizar.
```

### Arvore 6: Muitos Cliques mas Poucas Conversoes

```
Cliques subiram 30%+ mas conversoes estaveis ou caindo?
|
+-- Sim -> Verificar de ONDE vieram os novos cliques
|        |
|        +-- Search terms novos? -> Listar search terms com >10 cliques e zero conversao
|        |   +-- Termos irrelevantes? -> Adicionar como negativas
|        |   +-- Termos relevantes? -> Landing page nao atende expectativa. Otimizar LP.
|        |
|        +-- Dispositivo especifico? -> Mobile com baixa CVR? Otimizar mobile.
|        |
|        +-- Rede de Display (Search Partners)? -> Desativar Search Partners
|        |
|        +-- Nova keyword em correspondencia ampla? -> Monitorar de perto.
|        |
|        +-- Sazonalidade? -> Mesmo periodo do ano anterior teve comportamento similar?
|
+-- Nao -> Verificar Taxa de Conversao Geral
|   +-- CVR abaixo do benchmark do setor? -> Revisar funil completo (site, oferta, formulario)
|
+-- Tendencia gradual ao longo de semanas?
    +-- Fadiga de anuncio ou concorrencia com ofertas melhores?
```

### Arvore 7: Display com Muita View-through mas Pouca Conversao Direta

```
Display: VTC (view-through) = 60%+ do total de conversoes declaradas?
|
+-- Sim -> View-through esta INFLANDO o resultado
|   +-- VTC e controversa: Google conta qualquer conversao em 30 dias apos impressao
|   +-- O usuario provavelmente converteria de qualquer forma (organicamente)
|   +-- Acao: reporte VTC e CTC SEPARADAMENTE
|   +-- Acao 2: reduza janela de view-through para 1-7 dias
|   +-- Acao 3: se ROAS geral so e bom com VTC, o Display REAL nao esta performando
|
+-- Nao -> VTC < 30%: mais saudavel. Display esta gerando cliques diretos.
|
+-- Display com CPM alto e CTR baixo?
    +-- CPM > R$ 15 com CTR < 0,05%? -> Revisar posicionamentos e criativos
    +-- Segmentacao muito nichada -> Expandir audiencia
    +-- Criativo nao comunica valor -> Testar formatos e mensagens
```

### Arvore 8: PMax sem Transparencia

```
PMax nao mostra onde gasta?
|
+-- Sim (quase sempre) -> PMax e caixa-preta por design
|   +-- O que voce PODE ver:
|   |   +-- Asset group performance (agregado)
|   |   +-- Topicos / canais (relatorio limitado)
|   |   +-- Produtos (Shopping dentro de PMax)
|   +-- O que NAO ve:
|   |   +-- Search vs Shopping vs Display vs YouTube vs Gmail vs Discover
|   |   +-- Keywords individuais
|   |   +-- Search terms
|   +-- Acoes possiveis:
|   |   +-- Crie asset groups separados por produto/categoria
|   |   +-- Use brand exclusions para separar marca vs nao-marca
|   |   +-- Monitore canibalizacao com Search standard
|   |   +-- Configure experimentos para comparar PMax vs Search+Standard
|   |
|   +-- Decisao: continuar com PMax ou migrar para campanhas standard?
|       +-- PMax funciona bem se: feed de produto bom, conversoes suficientes, orcamento > R$ 5k/mes
|       +-- PMax nao funciona se: perdeu transparencia e ROAS nao justifica
|
+-- Nao -> Se voce TEM visibilidade (ex: relatorios de topicos), use dados de canal
|
+-- PMax esta performando bem mas Search standard caiu?
    +-- PROVAVEL canibalizacao. Considere reduzir PMax ou excluir brand.
```

### Arvore 9: Shopping — ROAS Bom no Geral, mas Produto X Drena Orcamento

```
Produto X tem ROAS 50% menor que a media da campanha de Shopping?
|
+-- Sim -> Produto Dreno detectado
|   +-- Verificar:
|   |   +-- Preco competitivo? (produto mais caro que concorrentes -> CTR baixo)
|   |   +-- Imagem do produto? (imagem fraca -> CTR baixo -> CVR baixa)
|   |   +-- Titulo e descricao? (SEO do feed fraco -> nao aparece para termos certos)
|   |   +-- Avaliacoes? (produtos com 0 ou poucas avaliacoes -> baixa confianca)
|   |   +-- Estoque? (produto sem estoque -> sem impressao)
|   |   +-- Concorrencia? (muita concorrencia nesse produto -> CPC alto)
|   +-- Acoes:
|   |   +-- Melhorar titulo, imagem, preco
|   |   +-- Reduzir lance desse produto especifico
|   |   +-- Se ROAS < 0,5 e nao ha perspectiva de melhora -> pausar
|   |   +-- Se produto e estrategico (vitrine, sazonal, alto ticket) -> aceitar ROAS baixo
|   |
|   +-- Se produto nao e essencial -> Pausar ou reduzir ao minimo
|
+-- Nao -> Produto dreno? Produtos com ROAS baixo existem. Avalie se estao dentro da margem de tolerancia.
|
+-- Varios produtos com ROAS baixo? -> Problema de feed, landing page de produto, checkout ou pricing geral
```

### Arvore 10: YouTube — Campanha de Reconhecimento Sem Engajamento

```
YouTube (In-stream): VTR < 15% ou CTR < 0,5%?
|
+-- Sim -> Problemas de engajamento
|   +-- VTR baixa (< 15%)? -> Video nao prende atencao nos primeiros 5s
|   |   +-- Hook fraco? -> Refinar primeiros segundos (problema, curiosidade, beneficio)
|   |   +-- Publico errado? -> Audiencia nao se interessa pelo tema
|   +-- CTR baixa (< 0,5%)? -> CTA ou oferta nao atraente
|   |   +-- CTA claro? -> "Saiba mais", "Inscreva-se"?
|   |   +-- Target correto? -> Segmentacao pode estar generica demais
|   +-- CPM muito alto? -> Publico muito concorrido ou nichado
|   |   +-- Se CPM > R$ 30 em campanha de awareness -> reconsiderar segmentacao
|   |
|   +-- Acoes:
|       +-- Testar multiplos hooks (5-10s) em diferentes versoes
|       +-- Usar experimento de video (Teste A/B de criativo)
|       +-- Revisar segmentacao: afinidade, eventos de vida, keywords de video
|
+-- Nao -> VTR > 30%, CTR > 1%: campanha de YouTube saudavel
|   +-- Verificar Brand Lift se orcamento justificar
|
+-- YouTube gerando view-through conversions mas nao diretas?
    +-- Normal. YouTube e canal de topo de funil. A conversao direta e bonus.
```

### Arvore 11: Conversoes no Google Ads vs GA4 Diferentes

```
Diferenca Google Ads vs GA4 > 30%?
|
+-- Sim -> Investigar causas
|   +-- Janela de conversao diferente?
|   |   +-- Google Ads: 30 dias clique + 30 dias view-through (padrao)
|   |   +-- GA4: 30 dias clique (sem view-through por padrao)
|   |   +-- Alinhar janelas para comparar
|   |
|   +-- Modelo de atribuicao diferente?
|   |   +-- Google Ads: last-click ou data-driven
|   |   +-- GA4: last-click Google Ads (padrao) ou data-driven
|   |   +-- Alinhar modelo para comparar
|   |
|   +-- View-through conversions?
|   |   +-- Google Ads conta VTC em Display/YouTube (se configurado)
|   |   +-- GA4 nao conta VTC por padrao
|   |   +-- Subtrair VTC do Google Ads para comparar
|   |
|   +-- Tag de conversao implementada corretamente?
|   |   +-- Google Ads: tag gtag.js ou Google Tag Manager
|   |   +-- GA4: tag de evento separada ou via GTM
|   |   +-- Ambas no mesmo lugar? Uma pode estar em paginas diferentes
|   |
|   +-- Cross-device?
|   |   +-- Google Ads modela conversoes cross-device
|   |   +-- GA4 precisa de User ID para cross-device
|   |   +-- Diferenca pode vir dai
|   |
|   +-- Acoes:
|       +-- Alinhar janela e modelo de atribuicao
|       +-- Fazer teste de tag (Google Tag Assistant, GA4 DebugView)
|       +-- Se tudo alinhado e diferenca > 30%, use GA4 como referencia de verdade
|
+-- Nao -> Diferenca 10-30%: normal. Monitorar.
|
+-- Diferenca 0-10%: surpreendentemente alinhado. Parabens pela implementacao.
```

### Arvore 12: Marca vs Concorrencia no Mesmo Search Term

```
Search term que menciona concorrente esta convertendo?
|
+-- Sim -> Concorrente perdeu cliente — vantagem sua
|   +-- Esta competindo em preco, recurso ou avaliacao?
|   +-- Se custo for aceitavel (CPA similar ao non-brand), mantenha
|   +-- Crie anuncio especifico comparativo (dentro das regras do Google)
|
+-- Nao -> Search term de concorrente gastando sem retorno
|   +-- Google Ads permite licitar em termos de concorrente? SIM (exceto marca registrada)
|   +-- Mas: se a intencao do usuario e especificamente o concorrente, dificilmente voce converte
|   +-- Acoes:
|       +-- Se nao converte -> adicione a marca do concorrente como negativa
|       +-- Se converte ocasionalmente -> lance baixo, monitore
|
+-- Concorrente esta aparecendo em SEU search term de marca?
    +-- Isso e LEGAL (exceto se marca registrada restrita)
    +-- Acoes:
        +-- Aumentar lance na sua marca para recuperar IS
        +-- Criar anuncios especificos de "Protecao de Marca"
        +-- Se concorrente e agressivo, aceite que IS de marca sera 85-90% em vez de 95-99%
```

---

## Parametros de Configuracao para o LLM

### Temperatura e Configuracao

| Parametro | Valor | Motivo |
|---|---|---|
| Temperatura | 0.1-0.3 | Analise de metricas exige precisao, nao criatividade. Use 0.1 para diagnosticos, 0.3 para recomendacoes. |
| Top P | 0.9 | Mantem alguma variedade na redacao sem perder precisao. |
| Presence Penalty | 0 | Nao precisa evitar repeticao em recomendacoes tecnicas. |
| Frequency Penalty | 0 | Idem. |
| Max Output Tokens | 8000-16000 | Diagnosticos completos podem ser longos. |

### Thresholds de Normalidade por Setor (Tabela Completa)

| Setor | CTR Search | CPC Search (R$) | CVR | CPA (R$) | ROAS |
|---|---|---|---|---|---|
| E-commerce Moda | 3-8% | 0,80-2,50 | 1,5-3% | 15-40 | 4-12x |
| E-commerce Eletronicos | 2-5% | 1,50-4,00 | 2-5% | 30-80 | 3-8x |
| E-commerce Moveis | 2-6% | 0,80-2,00 | 2-4% | 20-60 | 5-15x |
| E-commerce Alimentos | 4-10% | 0,50-1,50 | 2-6% | 10-25 | 8-20x |
| Clinica/Saude | 3-8% | 3,00-8,00 | 5-15% | 40-120 | 3-6x |
| Odontologia | 2-6% | 5,00-15,00 | 3-10% | 80-250 | 2-5x |
| Plano de Saude | 2-5% | 8,00-25,00 | 3-8% | 150-400 | 3-8x |
| Educacao | 3-7% | 1,50-5,00 | 3-10% | 30-100 | 5-15x |
| Advocacia | 3-8% | 10,00-50,00 | 2-5% | 100-400 | 3-8x |
| SaaS B2B | 2-5% | 8,00-30,00 | 1-5% | 80-250 | 1-3x |
| Construcao | 3-7% | 2,00-10,00 | 2-8% | 60-200 | 5-15x |
| Imobiliario | 2-5% | 1,00-4,00 | 1-4% | 40-150 | 5-20x |
| Financeiro | 2-6% | 5,00-15,00 | 3-10% | 50-150 | 5-15x |
| Seguros | 2-5% | 8,00-25,00 | 2-8% | 60-180 | 3-8x |
| Automotivo | 2-6% | 2,00-8,00 | 1-5% | 50-150 | 4-10x |

### Pesos de Metricas na Tomada de Decisao

| Cenario | Metrica Primaria | Peso | Metrica Secundaria | Peso |
|---|---|---|---|---|
| Otimizacao de Search | CPA / ROAS | 50% | Taxa de Conversao | 25% |
| Expansao de volume | IS% | 40% | CPA Incremental | 30% |
| Diagnostico de queda | CPC | 30% | CVR | 30% |
| Avaliacao de criativo | CTR | 50% | CVR | 30% |
| Alocacao de budget | ROAS | 40% | Volume de Conversoes | 30% |
| Analise de PMax | ROAS Geral | 60% | Asset Group ROAS | 20% |
| Analise de Display | VTC Ratio | 40% | CPM | 30% |
| Analise de Shopping | ROAS por Produto | 50% | CTR Produto | 25% |

### Regras de Precedencia

1. **Dados de conversao (com tag valida)** tem precedencia sobre metricas de engajamento.
2. **Tendencia de 7+ dias** tem precedencia sobre oscilacao de 1-2 dias.
3. **Segmentacao brand vs non-brand** tem precedencia sobre metrica geral.
4. **Comparacao YoY** tem precedencia sobre WoW (elimina sazonalidade).
5. **Metrica de confianca alta** tem precedencia sobre confianca baixa (ver hierarquia na Regra 2).
6. **Lucro real (ROAS x margem)** tem precedencia sobre ROAS nominal.
7. **Dados de experimento** tem precedencia sobre dados observacionais.

### Tabela de Prioridade de Hipotese

| Prioridade | Hipoteses | Evidencia Minima | Acao Recomendada |
|---|---|---|---|
| 1 | Search term irrelevante | >5 search terms com >10 cliques e 0 conv | Adicionar negativas |
| 2 | Quality Score baixo | QS < 6 em keyword >500 impressoes | Otimizar componente especifico |
| 3 | Concorrencia aumentou | Auction Insights: concorrente novo ou subiu | Reavaliar lances |
| 4 | Site/Landing Page quebrou | CVR caiu 30%+ em 24h | Testar site, tag, formulario |
| 5 | Budget mal alocado | Campanha com ROAS alto sem budget | Realocar orcamento |
| 6 | Atribuicao distorcida | DDA vs Last-click gap >30% | Revisar modelo |
| 7 | Estrategia de lance errada | <15 conv/mes com Target CPA/ROAS | Trocar para Maximizar |
| 8 | PMax canibalizando Search | Search standard perdeu volume com PMax | Ajustar exclusoes |
| 9 | Brand vs non-brand nao separado | CPA geral e baixo mas non-brand e caro | Criar campanha separada |
| 10 | Sazonalidade nao considerada | Comparacao WoW ruim mas YoY ok | Aceitar e planejar |

---

## Glossario Avancado

### Quality Score — Os 3 Componentes

1. **Expected CTR (peso ~40%)**
   - O Google preve a probabilidade de seu anuncio ser clicado
   - Baseado no historico da keyword + anuncio + conta
   - Keywords novas: expected CTR pode ser "baixo" por falta de dados
   - Como melhorar: use extensoes de anuncio, teste CTAs fortes, inclua keyword no titulo

2. **Ad Relevance (peso ~30%)**
   - O Google avalia a correspondencia entre: search term -> keyword -> anuncio -> landing page
   - Baixa relevancia = Google nao entende por que seu anuncio esta sendo exibido para aquela busca
   - Como melhorar: grupos de anuncios pequenos (<15 keywords), anuncios especificos, landing page dedicada

3. **Landing Page Experience (peso ~30%)**
   - Qualidade da pagina de destino (nao necessariamente a homepage)
   - Fatores: relevancia do conteudo, velocidade de carregamento, experiencia mobile, navegacao clara, transparencia
   - Como melhorar: especifica para cada grupo de anuncios, rapida (<3s), mobile-friendly, com CTA claro

### Impression Share — As Diferencas

- **Search Impression Share:** % de impressoes que seu anuncio de pesquisa recebeu do total possivel.
- **Display Impression Share:** % de impressoes de display recebidas do total possivel na segmentacao atual.
- **Search Lost Top IS:** % de impressoes perdidas no topo dos resultados.
- **Search Lost Absolute Top IS:** % de impressoes perdidas na primeira posicao.
- **Search Exact Match Impression Share:** IS para correspondencia exata (util para avaliar cobertura de marca).

### "Top" vs "Other" no CPC

O Google divide o CPC em duas categorias:

- **Top CPC:** custo medio por clique quando o anuncio aparece no topo da pagina (acima dos resultados organicos). Geralmente 20-60% mais caro que Other.
- **Other CPC:** custo medio por clique quando o anuncio aparece em outras posicoes (abaixo dos organicos, sidebar, final da pagina).
- **Implicacao:** se voce otimiza para "Other" (posicoes mais baixas), paga menos mas tambem tem menos cliques.
- **Estrategia:** para campanhas de conversao, prefira Top (mais cliques, mesmo que mais caros). Para campanhas de awareness em orcamento limitado, Other pode ser aceitavel.

### Estrategias de Lance — O Que Cada Uma Realmente Faz

**1. Maximizar Cliques (Maximize Clicks)**
- O Google gasta TODO o orcamento para obter o MAXIMO de cliques possivel
- Ignora QUALIDADE do clique (nao considera conversao)
- Util para: coleta de dados inicial, campanhas de trafego puro (ex: blog)
- Nao usar: quando o objetivo e conversao e voce tem dados >15 conv/mes

**2. Maximizar Conversoes (Maximize Conversions)**
- O Google gasta TODO o orcamento para obter o MAXIMO de conversoes
- Sem Target CPA: otimiza para VOLUME, sem limite de custo
- Com Target CPA: respeita o CPA alvo, mas pode gastar menos orcamento
- Util para: contas com >15 conversoes/mes que querem escalar

**3. Maximizar Valor de Conversao (Maximize Conversion Value)**
- Idem Maximizar Conversoes, mas otimiza para VALOR (receita)
- Com Target ROAS: busca o ROAS alvo
- Sem Target ROAS: maximiza valor sem restricao de ROAS
- Util para: e-commerce com valores de conversao variados

**4. Target CPA (Target Cost Per Action)**
- Tenta manter o CPA proximo do alvo definido
- Pode gastar acima do alvo se acredita que a conversao e provavel
- Exige >15 conversoes/mes na campanha (ou >30 na conta com portfolio)
- Se o CPA alvo e muito baixo (ex: R$ 20 quando o historico e R$ 50), o Google simplesmente NAO GASTA

**5. Target ROAS (Target Return on Ad Spend)**
- Tenta manter o ROAS proximo do alvo definido
- Exige >15 conversoes/mes
- Se o ROAS alvo e muito alto (ex: 800% quando o historico e 400%), o Google para de gastar
- Ideal para e-commerce com margens conhecidas

**6. CPC Otimizado (Enhanced CPC)**
- Ajusta lances manuais automaticamente com base na probabilidade de conversao
- Meio-termo: voce controla o lance base, Google ajusta +/-30%
- Quase ninguem usa mais — as estrategias automatizadas superam

**7. CPM / CPV (Cost Per Mille / Cost Per View)**
- CPM: usado em Display para otimizar impressoes
- CPV: usado em YouTube para otimizar views
- Objetivos de reconhecimento, nao conversao direta

### Brand vs Non-brand — Como Separar e Por Que Importa

- **Brand:** keywords que contem o nome da marca (ex: "Nike", "Nike Air Max", "loja Nike")
- **Non-brand:** keywords sem mencao a marca (ex: "tenis de corrida", "produto para dor nas costas")
- **Separacao na pratica:**
  1. Crie uma campanha separada para brand com orcamento especifico (geralmente 5-15% do total)
  2. Coloque todas as variacoes de marca em um grupo de anuncios
  3. Adicione a marca como negativa nas campanhas non-brand (para evitar sobreposicao)
  4. Analise SEMPRE separado

**Por que importa:**
- A performance de brand distorce a analise geral
- Decisoes de corte de orcamento em brand afetam protecao de marca
- Decisoes de orcamento em non-brand afetam aquisicao real
- O ROAS geral "bonito" pode estar escondendo um ROAS non-brand baixo

### "Conversoes" no Google Ads — O Que Conta (e O Que NAO)

**Conta como conversao:**
- Acoes medidas pela tag de conversao do Google Ads (compra, lead, ligacao, cadastro, etc.)
- Importacoes de dados offline (ligacoes, visitas, assinaturas)
- Conversoes cross-device (modeladas, se houver dados)
- View-through conversions (se a janela estiver ativa)
- Conversoes de cliques de produtos no Shopping

**NAO conta como conversao (a menos que configurado):**
- Visualizacoes de pagina
- Scrolls
- Cliques em botoes sem acao de conversao real
- Acoes em site sem tag de conversao

### Enhanced Conversions for Web

- Recurso que usa dados first-party (e-mail, telefone, nome) para melhorar a medicao de conversoes
- Os dados sao hashados (SHA-256) e enviados ao Google em paralelo a tag de conversao
- Melhora a precisao em cenarios de:
  - Cookie blocking (ITP, ETP)
  - Cross-device tracking
  - Conversoes offline
- Exige implementacao tecnica (codigo no site ou via GTM)

### DDA vs Last Click — Diferenca Pratica

| Aspecto | Last-click | Data-driven (DDA) |
|---|---|---|
| Credito | 100% para ultimo clique | Distribuido entre pontos de contato |
| Search Brand | Superestimado | Menos credito |
| Display | Subestimado | Mais credito |
| YouTube | Subestimado | Mais credito |
| Discovery | Subestimado | Mais credito |
| Dados necessarios | Nenhum | >15 conv nos ultimos 30 dias |
| Confiabilidade | Baixa para jornadas complexas | Alta para jornadas complexas |
| Impacto no CPA reportado | Base | 15-30% de diferenca |

### Click ID (GCLID) — Como Funciona e Quando Quebra

- GCLID: Google Click ID — um parametro unico adicionado ao final da URL de destino
- Como funciona:
  1. Usuario clica no anuncio
  2. Google adiciona ?gclid=xxxxx a URL
  3. O sistema do anunciante (CRM, site) registra o GCLID
  4. Google Ads conecta o clique a conversao

- Quando quebra:
  - Redirecionamentos que removem o GCLID (redirect limpa query params)
  - Landing pages que fazem redirect HTTP -> HTTPS mal configurado
  - Scripts no site que limpam a URL
  - Usuarios que limpam cookies
  - Bloqueadores de anuncio que removem parametros
  - Ambientes iOS com ITP (Intelligent Tracking Prevention)

### View-through Conversion no Display e YouTube

- **View-through Conversion (VTC):** usuario viu um anuncio de Display/YouTube (nao clicou) e depois converteu dentro da janela de view-through (padrao 30 dias)
- **Problema:** o Google atribui a conversao ao anuncio mesmo que o usuario fosse converter de qualquer forma
- **Polemica:** VTC e a metrica MAIS questionada do Google Ads. Criticos dizem que infla o valor do Display.
- **Defesa do Google:** estudos mostram que VTC tem correlacao com conversao real, especialmente em campanhas de consideracao.
- **Na pratica:**
  - Reporte VTC e CTC separadamente
  - Use janela de view-through de 1-3 dias (mais conservadora)
  - Se o ROAS do Display so fecha com VTC, questione o valor real do Display

### Performance Max — Como a IA Distribui Entre Redes

- PMax decide AUTOMATICAMENTE onde mostrar cada anuncio:
  - Search (incluindo Shopping e Local Inventory Ads)
  - Display
  - YouTube
  - Gmail
  - Discover (Google Feed)
  - Maps
- O Google otimiza para o objetivo de conversao escolhido
- A distribuicao muda constantemente com base no aprendizado
- **Voce NAO controla:**
  - Percentual de budget por rede
  - Keywords individuais
  - Search terms
  - Posicionamentos de Display

**Estrategias para lidar com a falta de transparencia:**
1. Crie asset groups separados por produto ou categoria
2. Use brand exclusions para proteger trafego de marca
3. Configure experimentos (PMax vs campanhas standard)
4. Monitore relatorios de topicos e canais (quando disponiveis)

### Experimentos: Drafts & Experiments

- **Draft:** uma copia da campanha onde voce faz alteracoes (sem publicar)
- **Experiment:** publica as alteracoes para uma fracao do trafego e compara com a original
- **Como configurar:**
  1. Crie um draft da campanha
  2. Faca as alteracoes desejadas
  3. Inicie o experimento com split 50/50
  4. Monitore por 2-3 semanas (minimo)
  5. Encerre e aplique o vencedor

**Regras:**
- Nao mude a campanha original durante o experimento
- Nao encerre o experimento cedo (mesmo que pareca claro)
- Verifique significancia estatistica antes de decidir
- Experimente UMA variavel por vez

---

## Casos Praticos

### Caso 1: E-commerce de Moda — CPC Baixo, CTR Ok, mas Zero ROAS

**Dados:**
- Setor: E-commerce de moda feminina (ticket medio R$ 120, margem 50%)
- Campanha: Search — "vestido festa", "vestido longo", "vestido midi"
- Periodo: 30 dias
- Gasto: R$ 3.450
- Cliques: 4.312
- Impressoes: 61.600
- CPC: R$ 0,80 (ok para moda)
- CTR: 7% (bom para Search)
- Conversoes: 12
- Taxa de Conversao: 0,28%
- CPA: R$ 287 (preocupante)
- ROAS: 0,42x (cada R$ 1 gerou R$ 0,42 de receita)

**Analise passo a passo:**

1. **Camada 1:** CPA de R$ 287 e 7-15x acima do benchmark. ROAS 0,42x e terrivel. VERMELHO.
2. **Camada 2 — Hipotese:**

   a. **Search terms:** os search terms sao realmente "vestido festa" de alta intencao ou trafego generico?
   - Abre search terms e descobre: 60% dos cliques vem de termos como "vestido" (sem qualificador) e "look festa" (mais generico)
   - Trafego de baixa intencao esta consumindo 60% do orcamento

   b. **Landing Page:** a page para "vestido festa" e uma pagina de categoria com 200 produtos. O usuario chega e tem 200 opcoes — paralisia de decisao.
   - Landing page e muito generica para search terms especificos

   c. **Dispositivo:** 75% dos cliques sao mobile. A taxa de conversao mobile e 0,15% (vs desktop 0,7%) — site mobile e lento e checkout dificil

   d. **Match type:** as keywords principais sao correspondencia ampla. "Vestido" esta ativando search terms como "vestido de noiva" (intencao completamente diferente)

3. **Diagnostico:**
   - Causa #1: correspondencia ampla esta gerando trafego irrelevante (60% do gasto em search terms de baixa intencao)
   - Causa #2: landing page generica nao atende a expectativa da busca (paralisia de decisao)
   - Causa #3: site mobile tem CVR 5x menor que desktop

4. **Plano de acao:**
   1. IMEDIATO: revisar search terms e adicionar negativas para termos irrelevantes (10 min)
   2. CURTO PRAZO: mudar correspondencia ampla para frase/exata nas palavras principais
   3. MEDIO PRAZO: criar landing pages especificas por colecao/subcategoria
   4. MEDIO PRAZO: otimizar site mobile (velocidade, checkout, UX)

### Caso 2: Clinica Odontologica — Impression Share 30% mas Budget Subutilizado

**Dados:**
- Setor: Odontologia (implantes e lentes de contato dental)
- Campanha: Search — "implante dentario", "lente de contato dental", etc
- Orcamento diario: R$ 200
- Gasto diario medio: R$ 80 (40% do orcamento)
- IS: 32%
- Lost IS (rank): 55%
- Lost IS (budget): 5%
- CPC medio: R$ 12
- CPA: R$ 180
- Conversoes/mes: 13

**Analise passo a passo:**

1. **Camada 1:** IS 32% e baixo. Gastando apenas 40% do orcamento. Isso e INCOMUM — normalmente IS baixo vem de BUDGET baixo, nao de RANK baixo.
2. **Camada 2:** Lost IS (rank) = 55%, Lost IS (budget) = 5%. O problema NAO e orcamento — e RANK. O Google nao mostra o anuncio porque ele nao e competitivo o suficiente.

3. **Hipotese:**
   a. QS baixo: QS medio 5/10 para as principais keywords. Componente mais baixo: landing page experience (a pagina de implante e generica, sem fotos, mobile lento).
   b. Lance baixo: lance maximo de R$ 15 para keywords que custam R$ 12 — margem de apenas R$ 3. Concorrencia pode estar dando lance de R$ 20+.
   c. Concorrencia: Auction Insights mostra 2 concorrentes novos nos ultimos 60 dias com maior dominancia.

4. **Diagnostico:**
   - O orcamento sobra porque o anuncio nao consegue competir por rank
   - Aumentar orcamento NAO resolve — precisa melhorar QS ou aumentar lance
   - Melhor caminho: melhorar landing page (mais relevante, mais rapida, mobile otimizada)

5. **Plano de acao:**
   1. CURTO PRAZO: criar landing page dedicada para implante dentario (com fotos, depoimentos, videos, CTA de agendamento)
   2. CURTO PRAZO: otimizar landing page existente para mobile e velocidade
   3. MEDIO PRAZO: testar lance de R$ 18 para ver se IS sobe
   4. Se depois de melhorar QS o IS continuar baixo: considerar que o mercado esta mais competitivo que antes

### Caso 3: SaaS B2B — Quality Score 10 em Todas as KWs mas Ninguem Converte

**Dados:**
- Setor: SaaS B2B — CRM para pequenas empresas
- Campanha: Search — "CRM para pequenas empresas", "CRM barato", "sistema de vendas"
- QS: 10 em todas as 30 keywords
- CTR: 8% (excelente)
- CPC: R$ 5 (abaixo da media para SaaS B2B)
- Gasto mensal: R$ 12.000
- Cliques: 2.400
- Conversoes (cadastro free trial): 3
- Taxa de Conversao: 0,125%
- CPA: R$ 4.000 (altissimo)
- IS: 85%

**Analise passo a passo:**

1. **Camada 1:** QS 10, CTR 8%, CPC baixo, IS 85% — tudo verde no topo da piramide. Mas CVR de 0,125% e CPA de R$ 4.000 — VERMELHO.
2. **Camada 2 — contradicao aparente:** tudo ok na Camada 1, mas Camada 2 revela problema grave no funil pos-clique.

3. **Hipotese:**
   a. Landing page: a pagina de destino e a homepage generica. O usuario chega procurando "CRM barato" e ve uma homepage com 5 planos diferentes. Falta direcionamento.
   b. Formulario de cadastro: pede nome, e-mail, telefone, empresa, cargo, numero de funcionarios. MUITOS campos para uma conversao de trial. A taxa de abandono e alta.
   c. Proposta de valor: o anuncio promete "CRM mais barato do mercado" mas a pagina destaca "solucao completa para empresas em crescimento" — disconnect.
   d. Tempo ate conversao: ciclo de vendas B2B e 7-90 dias. 30 dias de dados podem nao capturar todas as conversoes. Verificar janela.

4. **Investigacao profunda (Camada 3):**
   - Tempo ate conversao: dados do GA4 mostram que o tempo medio entre primeiro clique e cadastro e de 14 dias. 30 dias de dados podem estar subestimando.
   - Assisted conversions: as campanhas de Search podem estar assistindo conversoes em outros canais (Display, remarketing).

5. **Diagnostico:**
   - Causa #1: landing page generica nao corresponde a promessa do anuncio
   - Causa #2: formulario muito longo para uma oferta de trial (paradoxo: pede dados demais para "gratis")
   - Causa #3: janela de conversao pode estar subestimando (ciclo B2B)

6. **Plano de acao:**
   1. IMEDIATO: criar landing page especifica para cada keyword com oferta clara e formulario minimo (apenas e-mail)
   2. CURTO PRAZO: implementar fluxo de onboarding no trial para converter cadastro em uso ativo
   3. MEDIO PRAZO: estender janela de conversao para 60-90 dias
   4. MEDIO PRAZO: configurar acompanhamento de leads offline (demonstracoes agendadas via telefone)

### Caso 4: Loja de Material de Construcao — ROAS 8.0 no Geral, mas Uma Categoria com ROAS 0.5

**Dados:**
- Setor: E-commerce de material de construcao
- Campanha: Shopping (todos os produtos no mesmo feed)
- ROAS geral: 8,0x (parece otimo)
- ROAS por categoria:
  - Ferramentas eletricas: ROAS 12x (gasto R$ 15k/mes)
  - Hidraulica: ROAS 9x (gasto R$ 8k/mes)
  - Tintas: ROAS 6x (gasto R$ 5k/mes)
  - Pisos e revestimentos: ROAS 0,5x (gasto R$ 10k/mes)
- Categoria problema (Pisos): 35% do orcamento, 2% das conversoes

**Analise passo a passo:**

1. **Camada 1:** ROAS geral 8,0x parece EXCELENTE. Mas 35% do orcamento em uma categoria com ROAS 0,5 significa que as outras categorias precisam ter ROAS MUITO alto para compensar.
2. **Camada 2:** Por que Pisos tem ROAS 0,5?

   a. **Preco:** os pisos da loja sao 15-20% mais caros que a concorrencia. No Shopping, o preco e exibido. Usuario clica, ve o preco, nao compra.
   b. **Frete:** pisos sao pesados — o frete e caro (R$ 80-200). Muitos abandonos no checkout pela surpresa do frete.
   c. **Imagem:** as fotos de piso sao genericas (amostra de piso no chao). Concorrentes usam fotos de ambientes decorados.
   d. **Avaliacoes:** categoria com menos avaliacoes (media 3,2 estrelas vs loja 4,5).

3. **Diagnostico:**
   - A categoria Pisos nao e competitiva em preco no Shopping
   - O frete alto esta matando a conversao pos-clique
   - As imagens e avaliacoes nao geram confianca

4. **Plano de acao:**
   1. CURTO PRAZO: reduzir lance de pisos em 50% para limitar o dreno de orcamento
   2. CURTO PRAZO: melhorar imagens dos produtos (contratar fotos de ambiente)
   3. MEDIO PRAZO: negociar frete gratis ou subsidiado para pisos (ou criar regra de frete gratis acima de R$ 500)
   4. MEDIO PRAZO: campanha de coleta de avaliacoes para pisos
   5. Se apos 60 dias o ROAS de pisos continuar < 1,5: considerar pausar a categoria no Shopping e focar em Search (onde preco nao e exibido)

### Caso 5: Universidade — Concorrencia Elevou CPC em 60% no Periodo de Matriculas

**Dados:**
- Setor: Educacao (universidade privada, cursos de graduacao)
- Campanha: Search — "faculdade de administracao", "curso de direito", "vestibular"
- Orcamento mensal: R$ 60.000 (orcamento de matriculas, outubro-dezembro)
- CPC medio antes (setembro): R$ 3,50
- CPC medio atual (novembro): R$ 5,60 (+60%)
- IS antes: 75%
- IS atual: 42%
- Gasto diario antes: R$ 2.000/dia (100% do orcamento)
- Gasto diario atual: R$ 1.600/dia (80% do orcamento)
- CPA antes: R$ 80
- CPA atual: R$ 140 (+75%)

**Analise passo a passo:**

1. **Camada 1:** CPC subiu 60%, IS caiu de 75% para 42%, gasto caiu para 80% do orcamento, CPA quase dobrou. Multiplos VERMELHOS.
2. **Camada 2:**

   a. **Auction Insights:** 3 novas universidades entraram com campanhas agressivas em novembro + as existentes aumentaram lances. A concorrencia no leilao aumentou 80%.
   b. **QS:** estavel (media 7/10). Nao e o problema.
   c. **Lost IS (rank):** 52%. Perdendo claramente por rank — concorrencia esta dando lances mais altos.
   d. **Search terms:** ainda relevantes. A intencao do usuario nao mudou.
   e. **Brand vs non-brand:** brand CPC subiu menos (+20%), non-brand subiu muito (+70%).

3. **Camada 3:**
   - Sazonalidade: novembro-dezembro e pico de matriculas. O aumento de CPC e ESPERADO — mas 60% e agressivo.
   - Comparacao YoY: no ano passado, CPC subiu 30% no mesmo periodo. Este ano subiu o dobro.

4. **Diagnostico:**
   - A concorrencia aumentou significativamente (mais players + lances mais altos)
   - O mercado esta mais caro — a universidade precisa decidir se compete ou nao
   - A margem do ticket da universidade (R$ 500-1.000/mes) permite CPA mais alto

5. **Plano de acao:**
   1. IMEDIATO: aumentar orcamento diario para R$ 2.500
   2. CURTO PRAZO: testar lance 20% maior nas keywords principais para recuperar IS perdido
   3. CURTO PRAZO: revisar anuncios — garantir que extensoes de anuncio (sitelinks de cursos, callouts de bolsas) estejam ativas
   4. MEDIO PRAZO: campanhas de remarketing para capturar quem pesquisou mas nao se inscreveu
   5. ESTRATEGICO: planejar orcamento para 2025 ja considerando aumento de 40-50% no CPC de periodo de matriculas

### Caso 6: Seguros Auto — PMax Entrega ROAS 12.0, mas ao Desligar Search, Trafego de Marca Despenca

**Dados:**
- Setor: Seguros auto
- Campanha 1: PMax (ROAS 12,0x, gasto R$ 50k/mes, conv 200/mes)
- Campanha 2: Search Standard (ROAS 8,0x, gasto R$ 30k/mes, conv 120/mes)
- Campanha 3: Search Brand (ROAS 40x, gasto R$ 3k/mes, conv 50/mes)
- Total: ROAS ponderado ~10,5x

- Teste: pararam a campanha Search Standard por 2 semanas. Resultado:
  - PMax continuou ROAS 12x (R$ 50k/mes, conv 200)
  - Search Brand: IS caiu para 40% (era 95%) — Google comecou a mostrar concorrentes
  - Total da conta: ROAS caiu para 8x (porque brand perdeu visibilidade e muitas conversoes de marca sumiram)

**Analise passo a passo:**

1. **Camada 1:** PMax com ROAS 12x parece o heroi da conta. Mas quando Search e desligado:
   - PMax NAO absorveu o trafego de Search standard
   - Brand perdeu IS (concorrente tomou espaco)
   - Total da conta piorou

2. **Camada 2 — Investigacao:**
   - PMax pode estar atuando em redes DIFERENTES do Search (Shopping, Display, YouTube)
   - Search standard estava protegendo a marca indiretamente (mais presenca -> mais recall -> mais busca por marca)
   - Brand campanha isolada nao foi suficiente para proteger contra concorrentes no leilao de marca

3. **Camada 3:**
   - **Search term overlap:** PMax e Search estavam atuando em canais complementares, nao concorrentes
   - **Assisted conversions:** Search standard estava assistindo conversoes de marca (usuario via anuncio non-brand, depois buscava pela marca)
   - **PMax nao cobre Search de marca de forma confiavel** — sem a campanha de marca dedicada, o Google nao prioriza seu anuncio de marca

4. **Diagnostico:**
   - PMax nao substitui Search standard — atuam em redes diferentes
   - Search standard tem papel indireto de protecao de marca (presenca -> recall)
   - Desligar Search standard sem proteger marca foi um erro

5. **Plano de acao:**
   1. IMEDIATO: reativar Search standard (perda de 2 semanas de dados)
   2. CURTO PRAZO: redistribuir budget — reduzir PMax em R$ 10k e realocar para Search standard R$ 5k + Brand R$ 5k
   3. MEDIO PRAZO: testar experimento PMax vs Search (split de 50% do orcamento) para 30 dias
   4. MEDIO PRAZO: fortalecer campanha de marca com IS target 95%+
   5. LICAO APRENDIDA: PMax nao canibaliza Search o suficiente para substitui-lo completamente

---

## Cadencias e Rotinas de Analise

### Timeline de Revisao

#### 24h (Daily Check — 5 minutos)

O que fazer:
- Verificar se campanhas estao rodando (gasto > R$ 0)
- Verificar se NENHUMA metrica esta VERMELHA
- Verificar aprovacoes de anuncios/extensoes pendentes
- Verificar orcamento restante (pacing)
- Escalar: apenas se metrica VERMELHA ou anuncio reprovado

O que NAO fazer:
- NAO tomar decisoes de otimizacao baseadas em 1 dia de dados
- NAO pausar keywords por baixo desempenho em 24h
- NAO mudar estrategia de lance por 1 dia ruim
- NAO mexer em campanha que esta performando bem so "para testar"

#### Semanal (Weekly Review — 30-60 minutos)

O que fazer:
- Revisar metricas de Camada 1 da semana vs semana anterior
- Verificar search terms com >10 cliques e zero conversao (adicionar negativas)
- Verificar aprovacoes de anuncios/extensoes pendentes
- Verificar pacing de orcamento (gastou X% do mes em Y% do tempo)
- Verificar mudancas no Auction Insights (concorrentes novos ou removidos)
- Atualizar extensoes de anuncio com promocoes/sazonalidades
- Verificar Quality Score de keywords top 10 por gasto

O que NAO fazer:
- NAO pausar campanha baseado em 1 semana de dados (excecao: metrica VERMELHA com perda financeira comprovada)
- NAO fazer mudancas radicais em todas as campanhas ao mesmo tempo
- NAO ignorar search terms — e o diagnostico mais barato que existe

#### Quinzenal (Biweekly Deep Dive — 1-2 horas)

O que fazer:
- Mesmo que a Semanal, mais:
- Analisar brand vs non-brand separadamente
- Verificar desempenho por dispositivo
- Verificar match type performance (exata vs frase vs ampla)
- Revisar ROAS por produto/grupo de produto (Shopping)
- Verificar experimentos ativos (nao encerrar prematuramente)
- Analise de assisted conversions (canais de topo de funil)
- Comparacao com periodo anterior (YoY se possivel)

O que NAO fazer:
- NAO ignorar sazonalidade — sempre compare com periodo anterior
- NAO fazer mudancas em TODAS as campanhas — priorize top 3 problemas
- NAO esquecer de documentar o que foi mudado e por que

#### Mensal (Monthly Deep Dive — 3-4 horas)

O que fazer:
- Mesmo que a Quinzenal, mais:
- Analise completa de atribuicao (DDA vs last-click gap)
- Revisao de budget e alocacao entre campanhas
- Revisao de CPA/ROAS targets (estao realistas?)
- Analise de incrementality (geo lift, holdout, se aplicavel)
- Revisao de Customer Match lists e match rate
- Planejamento do mes seguinte (budget, keywords, campanhas)
- Relatorio consolidado para o cliente/gestor

O que NAO fazer:
- NAO fazer relatorio enorme que ninguem le — va direto ao ponto
- NAO tomar decisoes de orcamento sem dados consistentes de 30+ dias
- NAO ignorar tendencias de longo prazo em favor de picos curtos

### Estrutura de Report

#### Daily Check (para si mesmo)
```
1. Campanhas rodando? [SIM/NAO]
2. Gasto: R$ X / R$ Y (X% do budget)
3. Metricas VERMELHAS: [nenhuma / listar]
4. Aprovacoes pendentes: [0 / N]
5. Acao necessaria: [sim / nao]
```

#### Weekly Review (para o time/cliente)
```
1. Resumo executivo: 2-3 frases
2. Tabela de metricas (Camada 1) com comparacao semana anterior + sinalizacao verde/amarelo/vermelho
3. Top 3 problemas identificados (se houver)
4. Acoes tomadas na semana
5. Acoes planejadas para a proxima semana
6. Search terms: N negativas adicionadas
7. Testes/experimentos: status
```

#### Monthly Deep Dive (relatorio completo)
```
1. Resumo executivo com highlights e lowlights
2. Visao geral da conta: gasto, conversoes, CPA, ROAS, comparacao mes anterior e YoY
3. Analise por campanha/rede
4. Brand vs non-brand
5. Dispositivo
6. Shopping (se aplicavel): top 5 produtos por gasto e ROAS
7. PMax (se aplicavel): asset groups, canibalizacao
8. Atribuicao: DDA vs last-click
9. Search terms: principais adicoes/negativas
10. Plano para o proximo mes
11. Anexos: dados brutos em CSV/Google Sheets
```

---

## Regras de Ouro (Resumo Executivo para o LLM)

1. **Contexto primeiro, metrica depois.** Nunca analise uma metrica sem saber o setor, objetivo, rede e modelo de atribuicao do anunciante. O mesmo numero pode ser verde em um cenario e vermelho em outro.

2. **Confie em metricas de volume, desconfie de metricas modeladas.** Cliques, gasto e impressoes sao fatos. CPA, ROAS e conversoes sao interpretacoes (dependentes de tag, janela, modelo).

3. **Separe brand de non-brand SEMPRE.** Analisar junto e o erro mais comum. ROAS de 10x pode ser 50x brand + 2x non-brand.

4. **Nao trate Search e Display como a mesma midia.** Metricas, benchmarks e estrategias sao completamente diferentes. CTR de 0,1% no Display e normal; no Search e catastrofe.

5. **Camada 1 antes da Camada 2, Camada 2 antes da Camada 3.** Resolva problemas obvios primeiro. 80% dos problemas se resolvem com search terms, QS e budget.

6. **Nao reaja a 1-2 dias de dados.** Oscilacao diaria e normal. So aja se a tendencia for consistente por 5-7 dias.

7. **Quality Score e sintoma, nao causa.** QS baixo e resultado de anuncio irrelevante, CTR baixo ou LP ruim. Nao tente "melhorar QS" — melhore os componentes.

8. **View-through conversion e a metrica mais enganosa.** Use com cautela. Reporte VTC e CTC separadamente. Nao tome decisoes baseado em VTC.

9. **PMax e caixa-preta por design.** Nao tente extrair transparencia que o Google nao da. Aceite, monitore asset groups e proteja a marca com exclusoes.

10. **Search terms sao o diagnostico mais barato e eficaz.** Revise semanalmente. Adicione negativas. E a acao de maior impacto com menor esforco.

11. **Comparacao YoY > WoW.** Sazonalidade e real. Comparar esta semana com a anterior pode enganar; comparar com o mesmo periodo do ano passado e mais confiavel.

12. **Otimize para lucro, nao para ROAS.** ROAS de 5x com margem de 10% e pior que ROAS de 2x com margem de 60%. Sempre considere a margem.


---

## Demand Gen — Contextos Especificos

Demand Gen e a evolucao do Discovery Ads, focada em gerar demanda nas superficies mais visuais do Google (YouTube Shorts, In-stream, Gmail, Discover). Opera com criativos visuais (video + imagem + texto) e e projetada para despertar intencao onde ela nao existe ativamente.

### Contexto: "Demand Gen com CPA alto vs Search"

**Interpretacao:**
- Demand Gen e topo/meio de funil. CPA 2-5x maior que Search e NORMAL.
- O valor do Demand Gen esta em gerar consideracao, nao conversao direta.
- Acoes: nao compare CPA do Demand Gen com Search. Compare custo por engajamento (CPE) e taxa de clique.

### Contexto: "Criativos de video vs imagem no Demand Gen"

**Interpretacao:**
- Video tende a ter maior engajamento e melhor CVR que imagem estatica.
- Imagem estatica tende a ter CTR mais baixo mas pode funcionar para publicos frios.
- Acao: teste ambos os formatos em asset groups separados.

### Contexto: "Segmentacao por afinidade vs in-market no Demand Gen"

**Interpretacao:**
- Afinidade: publico com interesse geral no tema (topo de funil). CPM mais baixo, CTR mais baixo.
- In-market: publico pesquisando ativamente para comprar (fundo de funil). CPM mais alto, CTR mais alto.
- Acao: use in-market para campanhas com objetivo de conversao; afinidade para reconhecimento.

---

## Analise Avancada de Leilao (Auction Insights)

O relatorio de Auction Insights mostra como seus anuncios se comparam aos concorrentes no mesmo leilao.

### Metricas do Auction Insights

1. **Impression Share:** sua % de participacao de impressoes no leilao.
2. **Overlap Rate:** % de vezes que voce e um concorrente especifico apareceram no mesmo leilao.
3. **Position Above Rate:** % de vezes que um concorrente especifico apareceu acima de voce.
4. **Top of Page Rate:** % de vezes que voce apareceu no topo da pagina vs concorrentes.
5. **Outranking Share:** % de vezes que voce superou um concorrente especifico (apareceu acima ou ele nao apareceu).

### Interpretacao Avancada

- **Overlap alto + Position Above alto:** concorrente direto que esta te superando consistentemente. Precisa de acao.
- **Overlap baixo + Outranking alto:** voce domina um nicho onde o concorrente mal aparece. Mantenha.
- **Novo concorrente com overlap crescendo:** alguem esta aumentando investimento. Monitore.
- **Overlap alto + Outranking 50%:** empate. Quem melhorar QS/lance primeiro ganha.

### Quando usar Auction Insights

- CPA subiu sem explicacao -> verificar se concorrente novo entrou
- IS caiu sem mudanca na conta -> verificar se concorrente aumentou lances
- Planejamento de expansao -> verificar quais concorrentes dominam keywords que voce nao esta
- Relatorio mensal para cliente -> mostrar posicionamento competitivo

---

## Tipos de Correspondencia Avancados

O Google Ads tem 4 tipos de correspondencia (apos a simplificacao de 2021):

1. **Exata:** o search term deve corresponder EXATAMENTE a keyword (com pequenas variacoes como plural, erro ortografico, preposicao). Simbolo: [palavra chave].
   - Exemplo: keyword [tenis de corrida] ativa search terms: "tenis de corrida", "tenis para corrida", "tenis de corridas".
   - Nao ativa: "tenis", "corrida", "tenis de corrida masculino".

2. **Frase:** o search term deve conter a frase na ordem correta, mas pode ter palavras antes ou depois. Simbolo: "palavra chave".
   - Exemplo: keyword "tenis de corrida" ativa: "comprar tenis de corrida", "tenis de corrida masculino", "melhores tenis de corrida".
   - Nao ativa: "corrida de tenis" (ordem errada), "tenis" (faltam palavras).

3. **Ampla:** o Google usa machine learning para encontrar variacoes relacionadas. Nao ha simbolo. Pode ativar search terms que nao contem nenhuma palavra da keyword.
   - Exemplo: keyword tenis de corrida pode ativar: "tenis para academia", "melhores marcas de running", "calcados esportivos confortaveis".
   - O comportamento exato depende do historico da conta e da segmentacao.

4. **Ampla modificada (removida em 2021):** nao existe mais. Keywords com +palavra agora funcionam como ampla normal.

### Estrategia de Correspondencia Moderna

O Google recomenda usar predominantemente correspondencia ampla + smart bidding para maximizar resultados. Na pratica:

- **Contas novas (< 30 dias):** use exata e frase para controle. Ampla pode gerar muito trafego irrelevante.
- **Contas maduras (> 30 conversoes/mes, > 3 meses):** ampla + target CPA tende a funcionar bem. O Google tem dados suficientes para aprender.
- **E-commerce:** exata para produtos principais, ampla para descoberta em campanha separada.
- **Saude/Financeiro:** exata e frase. Ampla pode trazer trafego de baixa qualidade e desperdicio.

---

## Extensoes de Anuncio (Ad Extensions) — Guia Avancado

Extensoes sao informacoes adicionais que aumentam o tamanho e a relevancia do anuncio. Impactam DIRETAMENTE o expected CTR (componente do QS).

### Tipos de Extensao

1. **Sitelinks:** links para paginas especificas do site. O mais impactante. Use pelo menos 4.
2. **Callouts:** frases curtas de beneficios. Ex: "Frete Gratis", "Suporte 24h", "30 Dias de Garantia".
3. **Structured Snippets:** lista de produtos/servicos. Ex: "Tipos de Plano: Basico, Premium, VIP".
4. **Call:** botao de ligacao. Essencial para saude, servicos, emergencia.
5. **Message:** botao de SMS/WhatsApp.
6. **Location:** endereco e mapa. Essencial para negocios fisicos.
7. **Price:** tabela de precos. Impactante para e-commerce e servicos.
8. **App:** link para app store.
9. **Promotion:** promocao/desconto. Ex: "20% OFF ate 30/06".
10. **Image:** imagem no anuncio de Search. Relativamente nova, testar.

### Impacto no CTR

| Extensao | Aumento Medio de CTR |
|---|---|
| Sitelinks | +10-30% |
| Callouts | +5-15% |
| Structured Snippets | +5-10% |
| Call | +5-10% |
| Price | +10-20% |
| Promotion | +10-50% (sazonal) |
| Image | +5-15% (testando) |

### Regras para Extensoes

- Use NO MINIMO sitelinks + callouts em TODAS as campanhas de Search.
- Mantenha as extensoes ATUALIZADAS (nada de promocao que venceu ha 3 meses).
- Sitelinks com texto relevante a keyword aumentam o QS.
- Nao use extensao de promocao o ano todo — ela perde o efeito.

---

## Analise por Tipo de Campanha Google Ads

### Search Standard

**Caracteristicas:** total controle. Keywords, grupos de anuncios, lances manuais/automaticos.
**Melhor para:** contas que precisam de granularidade, setores com regulamentacao (saude, financeiro), marcas estabelecidas.
**Metricas chave:** QS, IS, CTR, CVR, CPA, ROAS, search terms.

### Shopping Standard

**Caracteristicas:** feed de produtos, lances por produto/produto.
**Melhor para:** e-commerce com catalogo organizado.
**Metricas chave:** ROAS por produto, CTR do produto, impressoes por SKU, benchmark de preco.
**Cuidados:** feed precisa ser excelente (titulo, imagem, preco, disponibilidade).

### Display Standard

**Caracteristicas:** segmentacao por publico (afinidade, in-market, remarketing, similar), posicionamento, topicos.
**Melhor para:** reconhecimento, consideracao, remarketing.
**Metricas chave:** CPM, CTR, View-through, CVR, assisted conversions.
**Cuidados:** view-through e inflado. Reporte separadamente.

### YouTube

**Caracteristicas:** In-stream, In-feed, Shorts, Bumper, Masthead.
**Melhor para:** reconhecimento, brand lift, consideracao.
**Metricas chave:** VTR (View-through Rate), CPV, CPM, Brand Lift.
**Cuidados:** otimizar hook nos primeiros 5 segundos.

### Performance Max

**Caracteristicas:** automatizado, omnichannel (Search + Shopping + Display + YouTube + Gmail + Discover + Maps), asset groups.
**Melhor para:** contas com >30 conversoes/mes, feed de produto bom, objetivo de conversao.
**Metricas chave:** ROAS geral, CPA geral, asset group ROAS.
**Cuidados:** falta de transparencia, canibalizacao com campanhas standard.

### Demand Gen

**Caracteristicas:** visual (video + imagem), YouTube + Gmail + Discover, foco em gerar demanda.
**Melhor para:** despertar interesse, consideracao, publicos qualificados.
**Metricas chave:** CPE (custo por engajamento), CTR, CPV, CPA.
**Cuidados:** CPA alto comparado a Search. Nao comparar diretamente.

---

## Troubleshooting Rapido — Problemas Comuns e Solucoes em 5 Minutos

### Problema: Campanha parou de gastar

1. Verificar status da campanha (ativada?)
2. Verificar status das keywords (aprovadas?)
3. Verificar status dos anuncios (aprovados?)
4. Verificar orcamento (nao acabou?)
5. Verificar programacao de anuncios (esta rodando no dia/hora certos?)
6. Verificar segmentacao geografica (mudou?)
7. Verificar faturamento (conta ativa?)

### Problema: Muitas impressoes, poucos cliques (CTR baixo)

1. Anuncio aparece no topo? (Top IS%% < 50%? Se sim, ajustar lance)
2. Qualidade do anuncio? (Headline fraca? Extensoes faltando?)
3. Search terms relevantes? (Se nao, adicionar negativas)
4. Concorrencia com mais extensoes? (Usar Auction Insights)

### Problema: Muitos cliques, poucas conversoes (CVR baixa)

1. Search terms: trafego e relevante? (Se nao, negativas + ajuste de keyword)
2. Landing page: corresponde a promessa do anuncio? (Se nao, criar LP especifica)
3. Site: mobile ok? (Se nao, priorizar otimizacao mobile)
4. Formulario: muito longo? (Se sim, simplificar)
5. Checkout (e-commerce): surpresas no frete/pagamento?

### Problema: CPA subiu mas CPC estavel

1. CVR que caiu? (Verificar LP, search terms, dispositivo)
2. Concorrencia entrou no leilao? (Auction Insights)
3. Sazonalidade diminuindo intencao? (Comparar YoY)
4. Tag de conversao quebrada? (Verificar com Tag Assistant)

### Problema: ROAS geral excelente, mas cliente reclama

1. Separa brand vs non-brand? (Provavelmente brand mascarando non-brand)
2. Produtos dreno no Shopping? (Verificar ROAS por produto)
3. VTC inflando Display? (Subtrair VTC)
4. Atribuicao DDA inflando canais de topo? (Comparar com last-click)

---

## Configuracao de Conversao — Checklist de Qualidade

Uma tag de conversao mal configurada e a causa #1 de diagnosticos errados.

### Checklist

- [ ] Tag de conversao instalada em TODAS as paginas relevantes
- [ ] Tag NÃO instalada em paginas que nao sao de conversao (blog, FAQ, etc.)
- [ ] Janela de conversao configurada adequadamente (padrao 30 dias, ajustar por setor)
- [ ] Modelo de atribuicao definido (last-click ou data-driven)
- [ ] Contagem: "toda conversao" ou "unica" depende do objetivo
- [ ] Valor da conversao configurado (para e-commerce, o valor da transacao)
- [ ] View-through conversions: desligado ou janela reduzida (1-7 dias)
- [ ] Cross-device conversions: habilitado
- [ ] Enhanced Conversions: configurado (se aplicavel)
- [ ] Conversoes offline: configuradas (se aplicavel)
- [ ] Tag Google Ads e GA4 em paginas SEPARADAS ou juntas (consistente)
- [ ] Testar a tag com Google Tag Assistant ou GTM Preview
- [ ] Verificar se a tag dispara em mobile e desktop
- [ ] Verificar se a tag NAO dispara em cliques de outros anuncios (ex: affiliate)

### Sinais de Tag Quebrada

- Zero conversoes por 48h+ em campanha que antes convertia
- Conversoes despencaram 80%+ de um dia para outro
- Diferenca Google Ads vs GA4 > 40% sem explicação
- Tag disparando multiplas vezes por sessao
- Tag disparando em paginas de administracao/preview

---

## Referencias e Boas Praticas

### Fontes Confiaveis de Benchmark

- Google Ads Benchmarks (WordStream): atualizado anualmente por setor
- Google Ads Grader (WordStream): ferramenta gratuita de auditoria
- Google Benchmarking Report (no Google Ads): mostra como sua conta se compara a concorrentes do mesmo setor
- Relatorios setoriais: IAB Brasil, Statista, eMarketer

### Livros e Recursos Recomendados

- "Advanced Google Ads" — Brad Geddes (referencia definitiva)
- "Google Ads (AdWords) Workbook" — Jason McDonald
- Blog oficial do Google Ads: blog.google/products/ads-commerce
- Google Ads Help Center: support.google.com/google-ads
- Google Skillshop: skillshop.withgoogle.com (certificacao gratuita)
- Search Engine Land: searchengineland.com (noticias e analises)
- PPC Hero: ppchero.com (casos e tutoriais)

### Ferramentas Recomendadas

| Ferramenta | Uso | Preco |
|---|---|---|
| Google Ads Editor | Gerenciamento em massa offline | Gratuito |
| Google Tag Assistant | Debug de tags | Gratuito |
| Google Optimize | Testes A/B de landing page | Gratuito |
| Google Data Studio | Dashboards e relatorios | Gratuito |
| Optmyzr | Automacao e alertas | Pago |
| AdEspresso | Testes A/B de anuncios | Pago |
| SEMrush | Pesquisa de concorrencia e keywords | Pago |
| Ahrefs | Backlinks e pesquisa organica | Pago |
| SpyFu | Historico de keywords dos concorrentes | Pago |
| Supermetrics | Automacao de dados para Sheets/Data Studio | Pago |

### Metricas de Vaidade (Evite)

- **Impressoes:** sozinhas nao significam nada. Sempre contextualize com IS%.
- **Cliques:** podem ser inflados por Search Partners e trafego irrelevante.
- **Posicao Media:** obsoleta. Use Top%% e Absolute Top%%.
- **CTR de Display:** comparar com Search e erro. Contexto e tudo.
- **CPC baixo:** pode indicar trafego de baixa qualidade, nao eficiencia.
- **View-through conversions:** a mais polemica. Use com cautela extrema.
- **Quality Score medio:** entre 5-7, o Google nao mostra o numero exato — "medio" pode ser 5 ou 7.
- **Budget utilizado 100%:** pode ser desperdicio se o CPA esta alto.

---

## Consideracoes Finais

### O Ciclo do Gestor de Trafego Google Ads

1. **Planejar:** definir objetivos, orcamento, estrategia, segmentacao.
2. **Executar:** configurar campanhas, criar anuncios, subir feed, implementar tags.
3. **Monitorar:** daily check, semanal, quinzenal, mensal.
4. **Analisar:** Camadas 1, 2, 3. Identificar problemas e oportunidades.
5. **Otimizar:** executar mudancas baseadas em dados.
6. **Reportar:** comunicar resultados de forma clara e acionavel.
7. **Repetir:** o ciclo nunca termina — Google Ads e um organismo vivo.

### O Legado de 20 Anos

Esta skill carrega a experiencia de duas decadas gerenciando centenas de contas, dezenas de milhoes em investimento e incontaveis licoes aprendidas. Algumas verdades atemporais:

- Os fundamentos do Google Ads mudam MENOS do que parece. Intencao de busca, relevancia do anuncio e qualidade da landing page sao os pilares desde 2003.
- As ferramentas mudam (Drafts & Experiments, PMax, Demand Gen), mas os principios de analise permanecem: entenda o negocio, separe os sinais do ruido, siga os dados.
- O Google sempre favorece contas bem estruturadas. Keywords em grupos de anuncios pequenos. Anuncios relevantes. Landing pages rapidas e uteis. Nada substitui o basico bem feito.
- O melhor gestor de trafego nao e quem faz o ROAS mais alto em um mes — e quem constroi performance SUSTENTAVEL por meses e anos.


---

## Automacao e Scripts no Google Ads

### Google Ads Scripts — Automacao Avancada

Scripts sao trechos de JavaScript que rodam no Google Ads para automatizar tarefas repetitivas.

### Scripts Essenciais para Gestao

1. **Pausar keywords com alto gasto e zero conversao**
```
function main() {
  var campaignIterator = AdsApp.campaigns().get();
  while (campaignIterator.hasNext()) {
    var campaign = campaignIterator.next();
    var keywordIterator = campaign.keywords()
      .withCondition("Cost > 100")
      .withCondition("Conversions < 1")
      .forDateRange("LAST_30_DAYS").get();
    while (keywordIterator.hasNext()) {
      var keyword = keywordIterator.next();
      keyword.pause();
    }
  }
}
```

2. **Alertar quando CPA excede limite**
```
function main() {
  var dateRange = "LAST_7_DAYS";
  var campaigns = AdsApp.campaigns()
    .withCondition("Cost > 1000")
    .forDateRange(dateRange).get();
  while (campaigns.hasNext()) {
    var campaign = campaigns.next();
    var stats = campaign.getStats();
    var cpa = stats.getCost() / (stats.getConversions() || 1);
    if (cpa > 100) {
      Logger.log("ALERTA: CPA de R$ " + cpa.toFixed(2) + " na campanha " + campaign.getName());
    }
  }
}
```

### Automacao Responsavel vs Irresponsavel

**Responsavel:**
- Scripts de alerta (email/Slack quando metrica sai do normal)
- Automacao de pausa de keywords com alto gasto e zero conv
- Relatorios automaticos para Data Studio/Sheets
- Ajuste de lances baseado em ROAS minimo

**Irresponsavel:**
- Script que aumenta lances automaticamente sem limite
- Script que pausa campanhas baseado em 1 dia de dados
- Automacao que muda estrategia de lance sem revisao humana
- Script que adiciona keywords sem controle de qualidade

---

## Analise de Sazonalidade Avancada

### Como Identificar Sazonalidade

1. **Comparacao YoY:** o metodo mais confiavel. Compare mes com mesmo mes do ano anterior.
2. **Indice Sazonal:** calcule a media de cada mes dividido pela media anual. Meses com indice > 1.2 sao acima da media; < 0.8 sao abaixo.
3. **Eventos fixos:** Natal, Black Friday, Dia das Maes, Dia dos Pais, Volta as Aulas, Carnaval.
4. **Eventos moveis:** Pascoa (marco/abril), Carnaval (fevereiro/marco).

### Exemplo de Indice Sazonal (E-commerce)

| Mes | Indice | Interpretacao |
|---|---|---|
| Janeiro | 0.70 | Queda pos-Natal/13o |
| Fevereiro | 0.65 | Carnaval — baixa |
| Marco | 0.85 | Recuperacao |
| Abril | 0.90 | Normal |
| Maio | 1.00 | Normal (Dia das Maes) |
| Junho | 0.80 | Normal baixo |
| Julho | 0.85 | Ferias escolares |
| Agosto | 0.90 | Normal |
| Setembro | 0.95 | Pre-Black Friday |
| Outubro | 1.10 | Alta pre-BF |
| Novembro | 2.50 | Black Friday |
| Dezembro | 1.80 | Natal |

### Como Otimizar para Sazonalidade

- **Antes do pico (T-30 dias):** aumentar budget em 30-50%, testar criativos sazonais, ampliar keywords
- **Durante o pico:** monitorar de hora em hora, ter budget extra reservado, nao fazer mudancas estruturais
- **Depois do pico (T+7 dias):** reduzir budget, analisar dados, documentar licoes

---

## Otimizacao Avancada por Tipo de Objetivo

### Objetivo: VENDAS (E-commerce)

**Foco:** ROAS, Receita, Ticket Medio.

**Otimizacoes especificas:**
- Target ROAS: comecar com ROAS historico -20%, ir ajustando
- Feed de produtos: titulos com palavras-chave, imagens de alta qualidade, precos competitivos
- Remarketing: carrinho abandonado, visualizacao de produto, compradores anteriores
- Shopping: segmentar por margem, nao apenas por ROAS
- PMax: asset groups por categoria de produto

**Metricas que importam:**
- ROAS (por produto, categoria, campanha)
- Ticket Medio (esta crescendo?)
- Taxa de Abandono de Carrinho
- Novos vs Recorrentes
- Receita total

**Armadilhas:**
- Otimizar para ROAS ignorando margem
- Ignorar LTV em favor de ROAS de curto prazo
- Pausar produtos de baixo ROAS que sao importantes para o mix

### Objetivo: LEAD (Geracao de Leads)

**Foco:** CPA, Qualidade do Lead, Taxa de Aprovacao.

**Otimizacoes especificas:**
- Landing page: formulario minimo, CTA claro, prova social
- Extensoes: Call (essencial), Sitelinks de servicos
- Segmentacao: in-market para alta intencao
- Remarketing: para leads que nao converteram na primeira visita
- Offline conversion tracking: importar leads qualificados para otimizar lances

**Metricas que importam:**
- CPA (por campanha, keyword, dispositivo)
- Taxa de Aprovacao de Lead (% que se qualifica)
- Custo por Lead Qualificado (CPQL)
- Tempo ate contato da equipe comercial

**Armadilhas:**
- Otimizar para volume de leads ignorando qualidade
- Formulario muito curto (leads de baixa qualidade)
- Formulario muito longo (poucos leads, mas muito caros)
- Nao integrar Google Ads com CRM para otimizar por lead qualificado

### Objetivo: RECONHECIMENTO (Branding)

**Foco:** Alcance, CPM, Brand Lift.

**Otimizacoes especificas:**
- YouTube In-stream + Discovery
- Segmentacao por afinidade e dados demograficos
- Frequencia: limitar a 3-5 impactos/semana/usuario
- Criativos que comunicam valor de marca, nao oferta
- Medir com Brand Lift ou pesquisa de marca

**Metricas que importam:**
- CPM (custo por mil impressoes)
- Alcance Unico (reach)
- Frequencia Media
- VTR (View-through Rate no YouTube)
- Brand Lift (awareness, consideration, preference)
- Search Uplift (aumento nas buscas pela marca)

**Armadilhas:**
- Esperar CPA baixo de campanha de reconhecimento
- Segmentacao muito ampla (desperdicio)
- Segmentacao muito restrita (pouco alcance)
- Nao medir brand lift (nao sabe se funcionou)

---

## Interpretacao de Metricas no Relatorio de Leilao (Auction Insights)

O relatorio de leilao mostra como voce se compara a concorrentes que participam dos mesmos leiloes que voce.

**Dominancia:** Impression Share > 60% + Outranking Share > 70%. Voce domina este concorrente.
**Equilibrio:** Impression Share 30-60% + Outranking Share 40-60%. Disputa acirrada. Qualquer melhoria de QS/lance pode virar o jogo.
**Ameaca:** Impression Share baixo (< 30%) + Position Above alto (> 60%). Concorrente esta te superando. Precisa de acao.
**Novo entrante:** Concorrente que nao aparecia ha 30 dias e subiu para top 5 de repente. Alguem aumentou investimento.

### Metricas Avancadas do Auction Insights

- **Overlap Rate:** % de leiloes em que ambos participaram. Quanto maior, mais direta a competicao.
- **Position Above Rate:** % de leiloes em que o concorrente ficou acima de voce. Ideal: < 30%.
- **Top of Page Rate:** % de vezes que voce (ou o concorrente) ficou no topo. Diferenca grande indica vantagem competitiva.
- **Outranking Share:** % de leiloes em que voce superou o concorrente. Ideal: > 50%.

---

## Como Calcular o Ponto de Equilibrio (Break-Even) no Google Ads

O ponto de equilibrio e o CPA ou ROAS minimo para nao perder dinheiro.

### Formula Basica

```
Break-Even CPA = Margem x Ticket Medio
Break-Even ROAS = 1 / Margem
```

### Exemplos Praticos

**Produto: Tenis (R$ 200, margem 40%)**
- Break-Even CPA = 0,40 x 200 = R$ 80
- Acima de R$ 80 de CPA, voce PERDE dinheiro
- Break-Even ROAS = 1 / 0,40 = 2,5x

**Servico: Plano Odontologico (R$ 150/mes, margem 60%, permanencia 24 meses)**
- LTV total: R$ 150 x 24 = R$ 3.600
- LTV com margem: R$ 3.600 x 0,60 = R$ 2.160
- Break-Even CPA (considerando LTV): R$ 2.160
- Break-Even ROAS: 1 / 0,60 = 1,67x (por mes)
- Mas: se considerar LTV total, CPA de R$ 500 e aceitavel

**E-commerce: Eletronico (R$ 1.000, margem 15%)**
- Break-Even CPA = 0,15 x 1000 = R$ 150
- Break-Even ROAS = 1 / 0,15 = 6,67x
- Este produto precisa de ROAS muito alto — qualquer ineficiencia vira prejuizo

### Calculo com LTV (Life Time Value)

Para negocios com recorrencia (assinatura, seguros, SaaS):

```
Break-Even CPA (com LTV) = Margem x Receita Mensal x Meses de Permanencia
```

**Exemplo: SaaS (R$ 100/mes, margem 80%, permanencia 12 meses)**
- LTV: R$ 100 x 12 = R$ 1.200
- LTV com margem: R$ 1.200 x 0,80 = R$ 960
- Break-Even CPA: R$ 960 (CPA de R$ 200 e lucrativo)

### Calculo Inverso: Qual ROAS Preciso?

```
ROAS necessario = Custo do Produto / (Preco - Custo)
```

**Exemplo: Custa R$ 70, vende por R$ 100**
- ROAS necessario = 70 / (100 - 70) = 70 / 30 = 2,33x
- Qualquer ROAS acima de 2,33x e lucro

---

## Planejamento de Orcamento (Budget Planning)

### Metodo Top-Down (do orcamento para as campanhas)

1. Orcamento total definido (ex: R$ 100k/mes)
2. Alocar % por rede:
   - Search: 40% = R$ 40k
   - Shopping: 30% = R$ 30k
   - PMax: 20% = R$ 20k
   - Display/YouTube: 10% = R$ 10k
3. Alocar % por objetivo:
   - Vendas/Aquisicao: 70%
   - Reconhecimento: 20%
   - Remarketing: 10%
4. Distribuir por campanha com base em performance historica

### Metodo Bottom-Up (das campanhas para o orcamento)

1. Calcular CPA medio por campanha (ultimos 30-90 dias)
2. Definir numero de conversoes desejado
3. Multiplicar: CPA x Conversoes = Orcamento necessario
4. Somar todas as campanhas = Orcamento total

### Regras de Alocacao

- Campanhas com ROAS > 2x o break-even: prioridade maxima para aumentar budget
- Campanhas com ROAS entre 1x e 2x: manter, otimizar antes de escalar
- Campanhas com ROAS < 1x: reduzir ou pausar (exceto se forem de reconhecimento)
- Sempre reservar 10-20% do orcamento para TESTES (novas keywords, novos anuncios, novos publicos)

---

## Documentacao de Mudancas — Um Habito Essencial

Toda mudanca em uma conta do Google Ads deve ser documentada. Sem documentacao, voce nao sabe o que funcionou.

### O que Documentar Obrigatoriamente

1. **Data da mudanca**
2. **O que foi mudado** (campanha, keyword, anuncio, lance, budget)
3. **Valor anterior e valor novo**
4. **Motivo da mudanca** (qual dado ou hipotese motivou?)
5. **Resultado esperado** (o que voce acha que vai acontecer?)
6. **Resultado observado** (depois de 7-14 dias, o que realmente aconteceu?)
7. **Licao aprendida** (o que levar para o futuro?)

### Modelo de Documentacao

```
Data: 15/01/2026
Campanha: CRM_Search_NonBrand_Brasil
Mudanca: Adicionadas 50 keywords de correspondencia ampla
Motivo: Expandir alcance apos QS 8+ em keywords exatas
Resultado esperado: Aumento de 20% no volume com CPA +10%
Resultado observado (28/01): Volume +35%, CPA +8% (melhor que esperado)
Licao: Keywords amplas funcionam para esta conta com smart bidding ativo
```


---

## Remarketing Avancado (Listas de Remarketing)

### Tipos de Lista de Remarketing no Google Ads

1. **Visitantes do site:** usuarios que visitaram paginas especificas. A mais comum.
2. **Visitantes do app:** usuarios que usaram seu app.
3. **Lista de clientes (Customer Match):** upload de e-mails/telefones de clientes.
4. **Listas similares (Similar Audiences):** Google encontra usuarios similares aos seus visitantes. Descontinuado em 2023, substituido por otimizacao automatizada.
5. **Segmentos de dados demograficos:** idade, genero, renda familiar.
6. **Segmentos de afinidade e in-market:** interesses e intencoes de compra.

### Configuracao Avancada de Listas

| Tipo de Lista | Membro por | Duracao Padrao | Ideal para |
|---|---|---|---|
| Todos Visitantes | 1 visita | 30 dias | Reconhecimento geral |
| Visitantes de Pagina Especifica | 1 visita a URL X | 30-180 dias | Remarketing segmentado |
| Carrinho Abandonado | Adicionou ao carrinho | 7-30 dias | Recuperacao de vendas |
| Convertidos | Comprou/Lead | 30-180 dias | Upsell, cross-sell |
| Nao Convertidos | Visitou sem converter | 30-90 dias | Prospeccao |
| Lista de Clientes | Upload | Ilimitado | Customer Match |
| Listas Combinadas | AND/OR entre listas | Varia | Segmentacao avancada |

### Estrategias de Remarketing por Ciclo de Decisao

**Ciclo Curto (1-7 dias): e-commerce, saude, servicos locais**
- Remarketing em 1-3 dias: oferta de desconto, frete gratis
- Remarketing em 4-7 dias: prova social, urgencia (estoque limitado)
- Frequencia: 3-5 impactos/dia

**Ciclo Medio (7-30 dias): educacao, seguros, imoveis**
- Remarketing em 1-7 dias: conteudo educativo, comparacao de opcoes
- Remarketing em 8-14 dias: depoimentos, casos de sucesso
- Remarketing em 15-30 dias: oferta final, contato direto
- Frequencia: 2-3 impactos/dia

**Ciclo Longo (30-90 dias): SaaS B2B, alto ticket, financeiro**
- Remarketing em 1-14 dias: whitepapers, webinars
- Remarketing em 15-30 dias: comparacao de planos
- Remarketing em 31-60 dias: case studies, calculadora ROI
- Remarketing em 61-90 dias: oferta de demonstracao
- Frequencia: 1-2 impactos/dia

### Regras de Ouro do Remarketing

- **Separe convertidos de nao convertidos.** Nao mostrar o mesmo anuncio para quem ja comprou.
- **Duração da lista:** nao manter listas ativas por mais de 180 dias (dados ficam velhos).
- **Frequencia:** limitar a 5 impactos/dia/usuario para evitar saturacao.
- **Criativo especifico:** anuncio de remarketing deve ser DIFERENTE do anuncio de prospeccao.
- **Nao canibalize:** se remarketing tem ROAS 20x e prospeccao tem ROAS 3x, nao aloque 80% do budget para remarketing — voce precisa de novos clientes.
- **Segmentacao negativa:** exclua convertidos das listas de prospeccao.

---

## Smart Bidding — Guia de Sobrevivencia

### O Que e Smart Bidding

Smart Bidding sao estrategias de lance automatizadas que usam machine learning do Google para otimizar conversoes ou valor de conversao. Incluem: Target CPA, Target ROAS, Maximizar Conversoes, Maximizar Valor de Conversao.

### Como o Smart Bidding Realmente Funciona

O Google usa sinais contextuais (dispositivo, localizacao, horario, navegador, idioma, sistema operacional, comportamento anterior) para ajustar lances em tempo real no nivel do leilao.

**Mito:** Smart Bidding "aprende" automaticamente e funciona sozinho.
**Realidade:** Smart Bidding precisa de:
- Dados historicos suficientes (>15 conv/30 dias)
- Tag de conversao funcionando corretamente
- Dados de conversao consistentes (mesmo evento, mesmo valor)
- Tempo de aprendizado (1-2 semanas para estabilizar)

### Quando o Smart Bidding Falha

1. **Poucos dados:** <15 conversoes/mes. O Google nao tem o que aprender.
2. **Dados inconsistentes:** tag de conversao quebrada, mudanca frequente de evento de conversao, valores flutuantes.
3. **Mudancas estruturais:** mudar campanha, adicionar/remover muitas keywords, mudar segmentacao durante o aprendizado.
4. **Janela de conversao longa:** se a conversao leva 30 dias e voce tem 30 dias de dados, metade das conversoes ainda nao aconteceu.
5. **Orcamento muito restrito:** Smart Bidding precisa de espaco para ajustar lances. Orcamento muito baixo limita a capacidade de otimizacao.

### Smart Bidding na Pratica

| Estrategia | Quando Usar | Cuidados |
|---|---|---|
| Maximizar Conversoes | Contas com <15 conv/mes, ou querendo escalar volume | Pode gastar muito sem controle de CPA |
| Target CPA | Contas com >15 conv/mes, CPA conhecido | Nao defina CPA muito baixo (vai limitar volume) |
| Maximizar Valor | E-commerce com >30 conv/mes | Otimiza valor, nao volume |
| Target ROAS | E-commerce com >30 conv/mes, ROAS conhecido | Nao defina ROAS muito alto (vai limitar volume) |

### Dicas Praticas de Smart Bidding

- Comece com Maximizar Conversoes (sem target) por 2 semanas para coletar dados
- Depois mude para Target CPA com CPA 20% acima do historico
- Ajuste gradualmente ate encontrar o equilibrio entre volume e custo
- NUNCA mude a estrategia de lance mais de uma vez a cada 10-14 dias
- Monitore o "conversion delay" (tempo ate conversao) — se for longo, estenda a janela

---

## O Verdadeiro Custo de um Google Ads Mal Otimizado

### Custos Ocultos

1. **CPC inflado por QS baixo:** cada ponto de QS perdido pode aumentar o CPC em 10-20%.
2. **Search terms irrelevantes:** R$ 1.000/mes gasto em cliques que nunca convertem e comum em contas sem revisao de search terms.
3. **Display sem controle:** search partners e display network podem gastar 30-50% do orcamento sem retorno.
4. **PMax sem exclusao de marca:** voce pagando para aparecer para quem ja te conhece.
5. **Atribuicao errada:** decidir cortar canais de topo de funil baseado em last-click, perdendo conversao futura.
6. **Budget mal alocado:** R$ 10k em campanha de ROAS 2x e R$ 5k em campanha de ROAS 8x.
7. **Falta de negativas:** cada clique irrelevante e R$ 1-50 jogados fora.

### O Calculo do Desperdicio

Se uma conta gasta R$ 100k/mes e voce identifica que 20% do gasto e em search terms irrelevantes com zero conversao:
- Desperdicio: R$ 20k/mes = R$ 240k/ano
- Acao: adicionar negativas (30 minutos de trabalho)
- ROI da acao: R$ 240k/ano por 30 min de trabalho

### Checklist Anti-Desperdicio (Faca uma vez por mes)

- [ ] Search terms com >10 cliques e zero conversao revisados
- [ ] Search partners ativos ou desativados intencionalmente?
- [ ] Display network ativa em campanhas de Search?
- [ ] Brand vs non-brand separado?
- [ ] Negativas de marca nas campanhas non-brand?
- [ ] Concorrentes como negativas onde necessario?
- [ ] Palavras de baixo ROAS com lance reduzido ou pausadas?
- [ ] Produtos dreno no Shopping identificados?
- [ ] View-through conversion janela reduzida para 1-3 dias?
- [ ] Orcamento alinhado com performance (nao com historico)?
- [ ] Experimentos ativos com resultados?
- [ ] Smart Bidding configurado com dados suficientes?
