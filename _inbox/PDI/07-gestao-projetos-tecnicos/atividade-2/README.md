# Atividade 2: Fluxo Kanban e Metricas

| Campo | Valor |
|---|---|
| Area | Automacao & Infraestrutura |
| Unidade | FV Marketing / V4 Company |
| Autor | Marcos Luciano |
| Data | Setembro 2026 |
| Status | Entregue (desenvolvido) |

## Entregas desta PDI

```
atividade-2/
├── README.md
├── 1-standards/
│   └── STANDARD-KANBAN-METRICAS.md
├── 2-implementacao/
│   ├── politicas-kanban.md
│   └── template-metrica-semanal.md
└── 7-apresentacao/
    ├── DECK-PDI.md
    ├── DEMO-SCRIPT.md
    ├── ROTEIRO-DOMINIO.md
    ├── report.json
    ├── gerar-docx.py
    ├── pdi-gestao-projetos-tecnicos-a2.html
    ├── pdi-gestao-projetos-tecnicos-a2.docx
    └── pdi-gestao-projetos-tecnicos-a2.pdf
```

## Problema Resolvido

O trabalho da area entrava por Slack, reuniao e e-mail, sem quadro unico e sem limite de trabalho em andamento. Resultado: 9 itens "em andamento" para 2 pessoas, lead time medio de 11 dias uteis e ninguem sabia dizer o que entrega nesta semana. Esta atividade implanta um kanban com WIP limitado e 3 metricas (lead time, throughput, WIP) medidas toda semana.

## Arquitetura Resumida

```
Demanda -> Fila (A Fazer, ordenada) -> Fazendo (WIP max 2/pessoa)
  -> Revisao (WIP max 3) -> Pronto
  Medicao semanal: lead time (dias por cartao), throughput (cartoes/semana), WIP (cartoes abertos)
  Regra: estourou WIP, parar de puxar e ajudar a destravar
```

## Proximos Passos

1. Operar o quadro por 4 semanas registrando as 3 metricas toda sexta.
2. Ajustar os limites de WIP com base no lead time observado.
3. Adicionar CFD (diagrama de fluxo acumulado) quando houver 30+ cartoes concluidos.

## Metricas de Sucesso

| Metrica | Atual | Meta |
|---|---|---|
| Lead time medio | 11 dias uteis (amostra ago/2026) | 5 dias uteis (meta) |
| Throughput semanal | 1,5 entrega/semana | 3 entregas/semana (meta) |
| WIP medio | 9 itens abertos | 4 itens abertos (meta) |

## Decisoes e tradeoffs

1. **Kanban em vez de Scrum**: demanda da area e continua e interruptavel (incidentes, pedidos urgentes); sprint fixa geraria cerimonia sem valor. Tradeoff: sem cadencia fixa, a disciplina vem do WIP e da review semanal.
2. **WIP de 2 por pessoa no Fazendo**: limite baixo expoe gargalo rapido; tradeoff e a sensacao inicial de "ociosidade" quando a fila trava (que na verdade e sinal para ajudar).
3. **Coluna Revisao separada**: deploy e validacao com a operacao sao gargalo real e precisam de limite proprio; tradeoff e 1 coluna a mais para gerenciar.
4. **Medicao semanal manual antes de automatizar**: planilha simples por 4 semanas valida as metricas antes de investir em ferramenta; tradeoff e 20 min/semana de lancamento manual.
5. **Classes de servico (padrao, urgente, data fixa)**: nem tudo tem a mesma urgencia e o quadro precisa mostrar isso; tradeoff e a tentacao de marcar tudo como urgente (regra: max 1 urgente por vez).

## Impacto no negocio

Com WIP limitado e lead time medido, a area dobra a previsibilidade de entrega sem contratar ninguem: a operacao passa a saber o que chega nesta semana e o lead time menor acelera campanhas, correcoes e relatorios que geram receita.

## Referencias

- Curso: Kanban essencial para times ageis (DIO)
- Video: Cumulative Flow Diagram explained (YouTube)
- Doc: Kanban quickstart, Microsoft Learn (quadro, WIP, metricas): https://learn.microsoft.com/en-us/azure/devops/boards/boards/kanban-quickstart
- Doc: Cumulative Flow Diagram, Microsoft Learn (CFD e lead time): https://learn.microsoft.com/en-us/azure/devops/report/dashboards/cumulative-flow
