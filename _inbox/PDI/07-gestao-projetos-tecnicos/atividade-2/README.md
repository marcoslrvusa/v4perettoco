# Atividade 2: Fluxo Kanban e Métricas

| Campo | Valor |
|---|---|
| Área | Automação & Infraestrutura |
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

O trabalho da área entrava por Slack, reunião e e-mail, sem quadro único e sem limite de trabalho em andamento. Resultado: 9 itens "em andamento" para 2 pessoas, lead time médio de 11 dias úteis e ninguém sabia dizer o que entrega nesta semana. Esta atividade implanta um kanban com WIP limitado e 3 métricas (lead time, throughput, WIP) medidas toda semana.

## Arquitetura Resumida

```
Demanda -> Fila (A Fazer, ordenada) -> Fazendo (WIP max 2/pessoa)
  -> Revisao (WIP max 3) -> Pronto
  Medicao semanal: lead time (dias por cartao), throughput (cartoes/semana), WIP (cartoes abertos)
  Regra: estourou WIP, parar de puxar e ajudar a destravar
```

## Próximos Passos

1. Operar o quadro por 4 semanas registrando as 3 métricas toda sexta.
2. Ajustar os limites de WIP com base no lead time observado.
3. Adicionar CFD (diagrama de fluxo acumulado) quando houver 30+ cartões concluídos.

## Métricas de Sucesso

| Métrica | Atual | Meta |
|---|---|---|
| Lead time médio | 11 dias úteis (amostra ago/2026) | 5 dias úteis (meta) |
| Throughput semanal | 1,5 entrega/semana | 3 entregas/semana (meta) |
| WIP médio | 9 itens abertos | 4 itens abertos (meta) |

## Decisões e tradeoffs

1. **Kanban em vez de Scrum**: demanda da área e continua e interruptível (incidentes, pedidos urgentes); sprint fixa geraria cerimonia sem valor. Tradeoff: sem cadência fixa, a disciplina vem do WIP e da review semanal.
2. **WIP de 2 por pessoa no Fazendo**: limite baixo expõe gargalo rápido; tradeoff é a sensação inicial de "ociosidade" quando a fila trava (que na verdade e sinal para ajudar).
3. **Coluna Revisão separada**: deploy e validação com a operação são gargalo real e precisam de limite próprio; tradeoff é 1 coluna a mais para gerenciar.
4. **Medição semanal manual antes de automatizar**: planilha simples por 4 semanas valida as métricas antes de investir em ferramenta; tradeoff é 20 min/semana de lançamento manual.
5. **Classes de serviço (padrão, urgente, data fixa)**: nem tudo tem a mesma urgência e o quadro precisa mostrar isso; tradeoff é a tentação de marcar tudo como urgente (regra: max 1 urgente por vez).

## Impacto no negócio

Com WIP limitado e lead time medido, a área dobra a previsibilidade de entrega sem contratar ninguém: a operação passa a saber o que chega nesta semana e o lead time menor acelera campanhas, correções e relatórios que geram receita.

## Referências

- Curso: Kanban essencial para times ágeis (DIO)
- Vídeo: Cumulative Flow Diagram explained (YouTube)
- Doc: Kanban quickstart, Microsoft Learn (quadro, WIP, métricas): https://learn.microsoft.com/en-us/azure/devops/boards/boards/kanban-quickstart
- Doc: Cumulative Flow Diagram, Microsoft Learn (CFD e lead time): https://learn.microsoft.com/en-us/azure/devops/report/dashboards/cumulative-flow
