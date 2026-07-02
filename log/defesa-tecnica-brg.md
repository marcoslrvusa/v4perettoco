# Defesa Técnica — Visão Estratégica BID BRG

## A Tese Central (o que você precisa defender)

> A maior alavanca de GMV e margem nos 12 canais não está dentro dos marketplaces — está na integração entre o ecossistema D2C e a operação 3P.

O D2C da Integralmedica está podre por baixo. Structured data ZERO. 12s de carregamento. 302 em produto. 83% não indexado. Consertar isso **triplica a visibilidade orgânica em 6 meses** — e essa visibilidade se reflete em busca no marketplace.

---

## A Auditoria (sua prova concreta — ninguém mais tem isso)

| Métrica | Status | Impacto em Marketplace |
|---------|--------|----------------------|
| Structured data | ZERO em 100% das páginas | Sem rich snippets, sem compatibilidade com feeds de marketplace |
| Homepage | 1,17 MB HTML, 12s resposta | Mobile inviável, CWV penalizado |
| Meta descriptions duplicadas | 16 páginas com o mesmo texto genérico | Perde CTR orgânico |
| Páginas indexáveis | Apenas 40 de 237 (16,9%) | 83% do site invisível para busca |
| 302 redirects em produtos | 100% redirecionam com 302 | Não passa link equity |
| Imagens >100KB | 89 imagens (45,88%) | Lentidão em páginas de produto e feeds |
| H1 ausente | 10 páginas sem H1 | Heading principal ausente |
| X-Frame-Options | 78,9% sem | Risco de segurança para integrações |

**Por que isso é sua blindagem**: Ninguém pode contestar dados. Você não está opinando — está mostrando o crawl. Se questionarem "por que começar por aí?", você aponta os números.

---

## Os 3 Movimentos (90 dias)

### 1º — Governança e Baseline (Dias 1-30)

**O que é**: Mapear 10 contas × 5 marcas + documento de fronteiras + dashboard consolidado + setup ANYMARKET.

**Por que primeiro**: Sem governança, a operação inteira trava. Na Webcontinental, aprendi que múltiplos sellers e times sem documento de fronteiras geram retrabalho infinito. Depois do After Click, o risco dobra — quem cadastra? quem precifica? quem responde avaliação? Isso tem que estar preto no branco antes de qualquer campanha.

**Se questionarem "por que gastar 30 dias só em governança?"**:
> "Porque governança mal feita é o que mais mata operação de marketplace. Na Webcontinental, os primeiros 30 dias sem fronteiras claras geraram conflito entre sellers 1P e 3P que levamos 2 meses para desfazer. Para a BRG, com After Click entrando como operador logístico, o risco é ainda maior. Documento de fronteiras na primeira semana não é burocracia — é seguro de operação."

### 2º — Catálogo e Reputação (Dias 30-60)

**O que é**: 302 → 301, structured data em 100%, meta descriptions únicas, monitoramento de reputação SLA 24h, compressão de imagens.

**Por que nessa ordem**: Structured data e redirects são a fundação. Sem schema, o produto não aparece com rich snippets nem no Google Shopping. Com 302, qualquer link building ou mídia apontando pra produto perde autoridade. Reputação é KPI de sobrevivência em marketplace — não se recupera, se previne.

**Se questionarem "reputação é com o SAC, não com tecnologia"**:
> "Reputação em marketplace é responsabilidade de quem opera o canal. O cliente não reclama no SAC — ele dá nota baixa no MELI. E uma estrela a menos derruba conversão em 20% no mesmo dia. Monitoramento não é opcional, é operação. Na Webcontinental, eu atuava na rotina do call center e sei como SLA de resposta impacta review score."

### 3º — MELI FULL + Brandstores + Mídia (Dias 60-90)

**O que é**: Go-live FULL MELI, brandstores em 3 canais, primeira rodada de mídia, JBP preliminar.

**Por que depois dos outros dois**: Mídia em cima de catálogo quebrado é dinheiro queimado. FULL com estoque desalinhado gera cancelamento e reputação negativa. A ordem importa.

**Se questionarem sobre seu nível Intermediário em FULL**:
> "Declarei Intermediário por honestidade intelectual, não por incapacidade. Nunca liderei um go-live FULL do zero, mas coordenei migração VTEC com SPA em React — complexidade técnica muito maior — sem perder uma linha de tráfego orgânico. Para o FULL, vou buscar apoio técnico dedicado no go-live. O resto — catalogação, precificação, mídia, reputação, JBP — é Especialista."

---

## Arquitetura de Mídia — Racional Técnico

### Defesa 60% vs Conquista 40%

Por que ESSA divisão e não outra:

- Consumidor de suplemento **pesquisa a marca** antes de comprar (dado comportamental do setor)
- Se a Growth aparecer na busca por "Integralmedica" antes da Integralmedica, o cliente **não volta** — ele compra da Growth
- 60% defesa garante ocupação total do topo da SERP de marca
- 40% conquista ataca concorrentes com product targeting onde eles são fracos

**Se pressionarem**: "Posso mostrar dados de search volume e competividade por keyword que validam esse split. A elasticidade de marca vs. genérica em suplementos justifica 60/40. Se os dados mostrarem outra coisa no planejamento, ajustamos."

### Dayparting

- **MELI + Amazon**: Fim de semana (consumidor fitness pesquisa mais)
- **Shopee**: Seg/ter (dias de oferta relâmpago)
- **Magalu**: Qua/qui (clube de assinatura)

**Racional**: Baseado em padrão de compra do setor de suplementos — o consumidor pesquisa durante a semana e compra no fim de semana, exceto em canais de impulso (Shopee).

### ANYMARKET como hub de inteligência

Quatro usos e por que cada um importa:

1. **Precificação dinâmica**: Cada marca tem margem diferente (Integralmedica margem maior que Optimum Nutrition de distribuição). Regra por marca, não por canal.
2. **Repricing no MELI**: Manter Buy Box sem queimar margem. Automático, não manual.
3. **Alerta de ruptura**: Estoque baixo → pausa mídia → ajusta preço → notifica After Click. Sem isso, FULL vende o que não tem e gera cancelamento.
4. **Cross-selling inteligente**: Kits de alta margem + frete barato (creatina + coqueteleira). Alavanca ticket médio sem aumentar custo de aquisição.

---

## Interface com After Click — Racional

A pergunta que vão fazer: **"Como garante que a After Click não vira um gargalo?"**

Cinco pontos da sua estratégia (todos baseados em experiência real na Webcontinental com múltiplos sistemas coexistindo):

1. **Documento de fronteiras na Semana 1** — responsabilidades claras com SLA e escalonamento. Sem isso, cada problema vira reunião.
2. **Reunião semanal de operação** — alinhar pedidos, ocorrências, SLA de entrega. Rotina, não exceção.
3. **Dashboard compartilhado** — pedidos pendentes, taxa de avaria, SLA de faturamento. Todo mundo vendo o mesmo número.
4. **Canal direto com KA da After Click** — issues que impactam reputação resolvidas em horas, não dias.
5. **Reconciliação de estoque ANYMARKET/VTEX ↔ After Click** — aprendi na Webcontinental que sistema desalinhado gera estoque fantasma. FULL com estoque errado = cancelamento = reputação negativa.

---

## Resumo de 30 Segundos (seu elevator pitch técnico)

> "Eu crawlee 237 URLs da Integralmedica. Structured data ZERO. 12s de carregamento. 83% do site não indexado. 302 em produto. Isso não é opinião — é dado.
>
> A tese é: consertar o D2C triplica a visibilidade orgânica em 6 meses, e essa visibilidade se reflete em marketplace. Porque o consumidor de suplemento pesquisa a marca no Google antes de comprar no MELI.
>
> Três movimentos em 90 dias: governança, catálogo/reputação, e aí mídia + brandstores. Nessa ordem. Qualquer outra ordem queima dinheiro.
>
> A After Click entra como operador logístico. A V4 entra como quem integra o ecossistema. A BRG entra com a estratégia comercial. Cada um no seu papel, com fronteiras claras desde a primeira semana."

---

## Checklist de Defesa

| Se perguntarem... | Sua âncora |
|-------------------|-----------|
| "Por que começar pelo D2C?" | 83% não indexado + structured data zero = 12 canais competindo com marca invisível |
| "Prova que isso gera resultado?" | Case Webcontinental: migração VTEC sem perda de tráfego, SEO 3P com 80% de coverage |
| "Seu nível em FULL é Intermediário" | Honestidade intelectual. O resto da operação é Especialista. FULL se resolve com apoio técnico. |
| "Quanto tempo pra resultado?" | 30 dias governança, 60 dias catálogo, 90 dias primeiras campanhas |
| "E a After Click?" | Documento de fronteiras + reunião semanal + dashboard compartilhado + canal direto KA |
| "Por que 60/40 defesa/conquista?" | Consumidor fitness pesquisa marca antes de comprar. Perder busca de marca é perder o cliente. |
| "Isso já foi feito antes?" | Webcontinental: mesma complexidade (VTEX + ANYMARKET + múltiplos sellers), entregue com zero perda. |
| "Qual o risco maior?" | Não fazer structured data e 302 → 301. O resto é otimização; isso é fundação quebrada. |

Documento salvo em `log/defesa-tecnica-brg.md`
