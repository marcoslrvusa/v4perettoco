# OUTPUTS — Account Manager V4
## Exemplos de output esperado

> Use estes exemplos para calibrar se o agente está funcionando certo. Se o output real estiver muito diferente destes modelos, revise o CONTEXT.md com mais detalhes da sua operação.

---

## Output 1: FCA de desvio de CAC

**Input:** "Abre FCA: o CAC do cliente Clínica X subiu 40% essa semana"

**Output esperado:**
```
FCA — Clínica X — [data]

FATO:
O CAC da Clínica X subiu 40% na última semana, passando de R$80 para R$112.
Volume de leads manteve-se estável (47 leads), mas o custo por lead aumentou.

CAUSA:
Identificamos duas causas combinadas:
1. Fadiga de criativo: CTR dos 3 anúncios principais caiu de 1,8% para 1,1% 
   (queda de 39%) — mesmos criativos rodando há 6 semanas sem rotação.
2. Aumento de CPM: mercado de saúde sofreu elevação de CPM de ~22% nesta semana 
   por sazonalidade (início de mês + campanha de planos de saúde de concorrente).

AÇÃO:
- GT pausa os 3 criativos com CTR < 1% até amanhã (quinta)
- Copy entrega 2 novas variações de headline até sexta
- Design prioriza 1 estático novo para teste A/B na próxima semana
- Reavaliamos CAC na análise de sexta-feira
- AM comunica desvio ao cliente com este FCA na reunião de quinta
```

---

## Output 2: OKRs quebradas para o quarter

**Input:** "Quebra em OKRs o objetivo do cliente E-commerce Moda: aumentar vendas orgânicas + pagas no Q2"

**Output esperado:**
```
OKRs — E-commerce Moda — Q2

OBJETIVO: Consolidar crescimento de receita digital combinando tráfego pago escalável 
com base orgânica crescente.

KR1 [Receita]:
  Meta: R$ 280.000 em receita atribuída ao digital no período
  Atual (baseline Q1): R$ 195.000
  Progresso: [ ] %

KR2 [Eficiência]:
  Meta: ROAS médio ≥ 3,2 nas campanhas pagas
  Atual (baseline Q1): 2,4
  Progresso: [ ] %

KR3 [Orgânico]:
  Meta: 35% das sessões vindas de tráfego orgânico (SEO + direto)
  Atual (baseline Q1): 22%
  Progresso: [ ] %

Status inicial: 🔴 (início de quarter — baseline definido, execução começa)
Próxima revisão: [data da análise semanal]
```

---

## Output 3: Pauta do Comitê P&EG

**Input:** "Prepara a pauta do comitê de segunda — temos 3 clientes ativos: Clínica X, E-commerce Moda e SaaS RH"

**Output esperado:**
```
Pauta — Comitê P&EG — [data] — Squad Mata Leão

1. STATUS QUALITY CHECK (10 min)
   Clínica X: [ ] 🟢/🟡/🔴 — observação:
   E-commerce Moda: [ ] 🟢/🟡/🔴 — observação:
   SaaS RH: [ ] 🟢/🟡/🔴 — observação:

2. STATUS OKRs (20 min)
   Clínica X — KR1: [ ]% | KR2: [ ]% | KR3: [ ]% → status geral: 🟢/🟡/🔴
   E-commerce Moda — KR1: [ ]% | KR2: [ ]% | KR3: [ ]% → status geral: 🟢/🟡/🔴
   SaaS RH — KR1: [ ]% | KR2: [ ]% | KR3: [ ]% → status geral: 🟢/🟡/🔴

3. FCAs EM ANDAMENTO (20 min)
   FCA aberta: [descrição] — avanço: [ ] — bloqueio: [ ] — dono: [ ]

4. NOVAS FCAs / SPRINTS (10 min)
   [ ] Há novos desvios que precisam de FCA?
   [ ] Alguma sprint precisa ser aberta ou revisada?

5. PRIORIZAÇÃO DA SEMANA (15 min)
   Cliente foco 1: [nome] — motivo: [ ] — ação prioritária: [ ]
   Cliente foco 2: [nome] — motivo: [ ] — ação prioritária: [ ]

---
ATA (preencher durante o ritual — não é tarefa posterior):
Decisões tomadas: [ ]
FCAs abertas/fechadas: [ ]
Priorização definida: [ ]
Ações + donos + prazos: [ ]
```

---

## Output 4: Sprint inicial — cliente novo

**Input:** "Monta a sprint inicial da Clínica X — primeiro quarter, foco em geração de leads para consultas"

**Output esperado:**
```
Sprint #1 — Clínica X — Semana 1 a 2

Objetivo da sprint: Estruturar e ativar as primeiras campanhas de geração de leads 
para consultas, validando CPL baseline antes de escalar.

Tarefas:

[ ] Pesquisa de keywords e benchmarks do setor saúde
    Dono: GT | Prazo: até quarta | Entregável: lista de keywords + CPL estimado

[ ] Briefing de campanha Meta Ads (lead gen)
    Dono: GT | Prazo: até quarta | Entregável: brief completo no padrão V4

[ ] Copy dos 3 primeiros anúncios (headline + texto + CTA)
    Dono: Copy | Prazo: até quinta | Entregável: copy aprovada pelo AM

[ ] Criação dos assets visuais (2 estáticos + 1 vídeo curto)
    Dono: Design | Prazo: até sexta | Entregável: assets prontos para subir

[ ] Ativação das campanhas no Meta e Google
    Dono: GT | Prazo: até segunda semana | Entregável: campanhas ativas e veiculando

Critério de conclusão: campanhas ativas, primeiros dados de CPL disponíveis, 
próxima sprint pode ser pautada com dados reais.
```
