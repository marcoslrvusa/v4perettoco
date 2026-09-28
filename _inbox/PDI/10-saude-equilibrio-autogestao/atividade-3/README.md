# Atividade 3: Carga Sustentável e Limites

| Campo | Valor |
|-------|-------|
| Área | Automação & Infraestrutura |
| Unidade | FV Marketing / V4 Company |
| Autor | Marcos Luciano |
| Data | Setembro 2026 |
| Status | Entregue (desenvolvido, homologação pendente) |

## Entregas desta PDI

```
atividade-3/
├── README.md
├── 1-standards/
│   ├── 01-guia-dizer-nao.md
│   └── 02-wip-pessoal-sinais-sobrecarga.md
├── 2-implementacao/
│   ├── contrato-limites-wip.md
│   └── inventario-carga-semanal.md
└── 7-apresentacao/
    ├── DECK-PDI.md
    ├── DEMO-SCRIPT.md
    ├── ROTEIRO-DOMINIO.md
    ├── pdi-saude-carga-sustentavel-limites-a3.html
    ├── pdi-saude-carga-sustentavel-limites-a3.docx
    ├── pdi-saude-carga-sustentavel-limites-a3.pdf
    └── gerar-docx.py
```

## Problema Resolvido

Aceitar tudo gera fila paralela infinita: 6 frentes abertas, nenhuma fechada, qualidade caindo e cansaço subindo. Esta atividade instala um limite explícito de trabalho em progresso (WIP pessoal de 3 itens), um roteiro para dizer não sem romper relação e um painel de sinais de sobrecarga com ação definida para cada nível.

## Arquitetura Resumida

```
INVENTARIAR frentes abertas (tudo, inclusive favores)
  -> LIMITAR WIP em 3 (1 entrega principal, 1 secundária, 1 operacional)
    -> NEGAR com roteiro (não + motivo + alternativa + prazo)
      -> MONITORAR sinais (verde, amarelo, vermelho)
        -> AGIR (vermelho fecha entrada e renegocia prazo em 48 h)
```

## Próximos Passos

1. Preencher o inventário de carga e cortar ou delegar até caber no WIP de 3.
2. Usar o roteiro de negativa nas próximas 3 solicitações fora do WIP.
3. Revisar o painel de sinais toda sexta e registrar o nível da semana.

## Métricas de Sucesso

| Métrica | Atual | Meta |
|---------|-------|------|
| Frentes simultâneas abertas | sem dado | 3 no máximo (meta) |
| Solicitações recusadas ou renegociadas por mês | 0 | 4 (meta) |
| Semanas em nível vermelho por trimestre | sem dado | 0 (meta) |

## Decisões e tradeoffs

1. WIP de 3 em vez de 5: força conclusão e expõe gargalo. O custo é dizer não com mais frequência.
2. Roteiro de negativa com alternativa: preserva relação em vez de confronto. O custo é gastar 10 minutos para formular cada resposta.
3. Semáforo de sinais em vez de questionário longo: checagem de 2 minutos toda sexta. O custo é menor precisão clínica, é triagem, não diagnóstico.
4. Trava de entrada no nível vermelho: impede nova demanda até renegociar. O custo é atrito pontual com solicitantes.
5. Inventário inclui favores e tarefas invisíveis: carga real aparece. O custo é o desconforto de ver o tamanho da fila.

## Impacto no negócio

WIP estourado atrasa todas as frentes ao mesmo tempo e queima o profissional que sustenta a operação. Limite explícito aumenta previsibilidade de prazo, reduz retrabalho por pressa e preserva a capacidade do time, o que se traduz em SLA mais estável para os clientes da unidade.

## Referências

- Curso: Work Smarter, Not Harder (Margaret Meloni, UC Irvine), Coursera: https://www.coursera.org/learn/work-smarter-not-harder
- Vídeo: Brené Brown, The Power of Vulnerability, TED: https://www.youtube.com/watch?v=iCvmsMzlF7o
- Doc: Atlassian, guia de limites de WIP no Kanban: https://www.atlassian.com/agile/kanban/wip-limits
- Doc: OMS, perguntas e respostas sobre estresse (sinais e manejo): https://www.who.int/news-room/questions-and-answers/item/stress
