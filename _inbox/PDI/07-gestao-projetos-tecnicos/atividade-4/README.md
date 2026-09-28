# Atividade 4: Comunicação com Stakeholders não Técnicos

| Campo | Valor |
|---|---|
| Área | Automação & Infraestrutura |
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

Status técnico chegava a gesto e operação em linguagem de engenharia ("refatorei o extrator, subi o cron"), sem dizer o que muda para o negócio, sem risco explícito e sem pedido claro. Resultado: surpresa em atraso, decisão sem informação e cobrança no Slack. Esta atividade entrega ritual semanal de status em linguagem de negócio (feito, próximo, risco com plano, pedido) e matriz de expectativa por stakeholder.

## Arquitetura Resumida

```
Segunda 9h, 30 min, pauta fixa: feito (valor entregue) -> próximo (compromisso da semana)
  -> riscos (semaforo + plano + dono) -> pedidos (decisao ou ajuda com prazo)
  Regra: sem jargao, todo risco tem plano, todo pedido tem prazo de resposta
  + matriz: quem recebe o que, em que canal e com que frequencia
```

## Próximos Passos

1. Rodar o ritual por 4 segundas com a pauta fixa e registrar presença e decisões.
2. Preencher a matriz de stakeholders da área (mínimo 5 nomes reais).
3. Medir surpresas (atraso não avisado com 48h) e levar a zero.

## Métricas de Sucesso

| Métrica | Atual | Meta |
|---|---|---|
| Status semanal enviado no prazo | 20% das semanas | 100% (meta) |
| Atrasos avisados com 48h de antecedência | 0% | 100% (meta) |
| Riscos registrados com plano e dono | 0 | 100% dos riscos ativos (meta) |

## Decisões e tradeoffs

1. **Status semanal escrito antes da reunião**: leitura previa de 5 min elimina 20 min de exposição; tradeoff é exigir escrita disciplinada de quem reporta.
2. **Linguagem de negócio, zero jargão**: stakeholder decide por impacto, não por técnica; tradeoff é traduzir cada item (custa 10 min, evita 5 perguntas).
3. **Semáforo de risco com plano obrigatório**: risco vermelho sem plano é fofoca; tradeoff é expor problema cedo, antes de ter solução completa.
4. **Pedido com prazo de resposta**: "preciso de decisão até quarta" em vez de "quando puderem"; tradeoff é parecer insistente (mas é o que destrava).
5. **Matriz por stakeholder, não mensagem única**: diretor quer risco e prazo, operação quer data e workaround; tradeoff é manter 2 versões do mesmo status (curta no Slack, completa no doc).

## Impacto no negócio

Com status previsível em linguagem de negócio, a gestão decide com antecedência (reallocar verba, remarcar lançamento, aprovar escopo) em vez de apagar incêndio, e a operação confia nos prazos porque o atraso, quando existe, chega avisado com plano.

## Referências

- Curso: Agile Project Management, módulo do Google Project Management Professional Certificate (Coursera): https://www.coursera.org/learn/agile-project-management
- Vídeo: Stakeholder communication for project managers (YouTube)
- Doc: Agile project management, Atlassian (planejamento, backlog, métricas e stakeholders): https://www.atlassian.com/agile/project-management
- Doc: SRE Workbook, Google, índice (on-call, resposta e gestão organizacional): https://sre.google/workbook/table-of-contents/
