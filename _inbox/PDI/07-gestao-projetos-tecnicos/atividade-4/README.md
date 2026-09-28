# Atividade 4: Comunicacao com Stakeholders nao Tecnicos

| Campo | Valor |
|---|---|
| Area | Automacao & Infraestrutura |
| Unidade | FV Marketing / V4 Company |
| Autor | Marcos Luciano |
| Data | Setembro 2026 |
| Status | Entregue (desenvolvido) |

## Entregas desta PDI

```
atividade-4/
├── README.md
├── 1-standards/
│   └── STANDARD-COMUNICACAO-STAKEHOLDERS.md
├── 2-implementacao/
│   ├── pauta-status-semanal.md
│   └── template-status-risco.md
└── 7-apresentacao/
    ├── DECK-PDI.md
    ├── DEMO-SCRIPT.md
    ├── ROTEIRO-DOMINIO.md
    ├── report.json
    ├── gerar-docx.py
    ├── pdi-gestao-projetos-tecnicos-a4.html
    ├── pdi-gestao-projetos-tecnicos-a4.docx
    └── pdi-gestao-projetos-tecnicos-a4.pdf
```

## Problema Resolvido

Status tecnico chegava a gesto e operacao em linguagem de engenharia ("refatorei o extrator, subi o cron"), sem dizer o que muda para o negocio, sem risco explicito e sem pedido claro. Resultado: surpresa em atraso, decisao sem informacao e cobranca no Slack. Esta atividade entrega ritual semanal de status em linguagem de negocio (feito, proximo, risco com plano, pedido) e matriz de expectativa por stakeholder.

## Arquitetura Resumida

```
Segunda 9h, 30 min, pauta fixa: feito (valor entregue) -> proximo (compromisso da semana)
  -> riscos (semaforo + plano + dono) -> pedidos (decisao ou ajuda com prazo)
  Regra: sem jargao, todo risco tem plano, todo pedido tem prazo de resposta
  + matriz: quem recebe o que, em que canal e com que frequencia
```

## Proximos Passos

1. Rodar o ritual por 4 segundas com a pauta fixa e registrar presenca e decisoes.
2. Preencher a matriz de stakeholders da area (minimo 5 nomes reais).
3. Medir surpresas (atraso nao avisado com 48h) e levar a zero.

## Metricas de Sucesso

| Metrica | Atual | Meta |
|---|---|---|
| Status semanal enviado no prazo | 20% das semanas | 100% (meta) |
| Atrasos avisados com 48h de antecedencia | 0% | 100% (meta) |
| Riscos registrados com plano e dono | 0 | 100% dos riscos ativos (meta) |

## Decisoes e tradeoffs

1. **Status semanal escrito antes da reuniao**: leitura previa de 5 min elimina 20 min de exposicao; tradeoff e exigir escrita disciplinada de quem reporta.
2. **Linguagem de negocio, zero jargao**: stakeholder decide por impacto, nao por tecnica; tradeoff e traduzir cada item (custa 10 min, evita 5 perguntas).
3. **Semaforo de risco com plano obrigatorio**: risco vermelho sem plano e fofoca; tradeoff e expor problema cedo, antes de ter solucao completa.
4. **Pedido com prazo de resposta**: "preciso de decisao ate quarta" em vez de "quando puderem"; tradeoff e parecer insistente (mas e o que destrava).
5. **Matriz por stakeholder, nao mensagem unica**: diretor quer risco e prazo, operacao quer data e workaround; tradeoff e manter 2 versoes do mesmo status (curta no Slack, completa no doc).

## Impacto no negocio

Com status previsivel em linguagem de negocio, a gestao decide com antecedencia (reallocar verba, remarcar lancamento, aprovar escopo) em vez de apagar incendio, e a operacao confia nos prazos porque o atraso, quando existe, chega avisado com plano.

## Referencias

- Curso: Agile Project Management, modulo do Google Project Management Professional Certificate (Coursera): https://www.coursera.org/learn/agile-project-management
- Video: Stakeholder communication for project managers (YouTube)
- Doc: Agile project management, Atlassian (planejamento, backlog, metricas e stakeholders): https://www.atlassian.com/agile/project-management
- Doc: SRE Workbook, Google, indice (on-call, resposta e gestao organizacional): https://sre.google/workbook/table-of-contents/
