# Atividade 1: Deep Work e Gestão de Energia

| Campo | Valor |
|-------|-------|
| Área | Automação & Infraestrutura |
| Unidade | FV Marketing / V4 Company |
| Autor | Marcos Luciano |
| Data | Setembro 2026 |
| Status | Entregue (desenvolvido, homologação pendente) |

## Entregas desta PDI

```
atividade-1/
├── README.md
├── 1-standards/
│   ├── 01-guia-deep-work-energia.md
│   └── 02-protocolo-protecao-agenda.md
├── 2-implementacao/
│   ├── modelo-agenda-semanal.md
│   └── registro-sessoes-foco.md
└── 7-apresentacao/
    ├── DECK-PDI.md
    ├── DEMO-SCRIPT.md
    ├── ROTEIRO-DOMINIO.md
    ├── pdi-saude-deep-work-energia-a1.html
    ├── pdi-saude-deep-work-energia-a1.docx
    ├── pdi-saude-deep-work-energia-a1.pdf
    └── gerar-docx.py
```

## Problema Resolvido

A jornada de quem opera automação e infraestrutura é picotada por alertas, mensagens e reuniões. O resultado é um dia cheio e nenhuma entrega cognitivamente relevante concluída. Esta atividade instala um sistema pessoal de blocos de foco de 90 minutos alinhados ao ritmo ultradiano, com proteção ativa de agenda, para que o trabalho profundo tenha horário, lugar e regra de interrupção.

## Arquitetura Resumida

```
MAPEAR pico de energia (3 dias de log)
  -> DESENHAR agenda base (2 blocos de 90 min/dia em dias úteis)
    -> PROTEGER (status, bloqueio público, lote de mensagens)
      -> EXECUTAR (ritual de entrada, 90 min, pausa real de 20 min)
        -> MEDIR (sessões concluídas, interrupções, motivo)
```

## Próximos Passos

1. Rodar 2 semanas de agenda base e registrar todas as sessões no template de registro.
2. Revisar interrupções por origem e negociar uma recorrência de reunião que invade o bloco.
3. Expandir de 2 para 3 blocos em um dia da semana se a taxa de conclusão passar de 80%.

## Métricas de Sucesso

| Métrica | Atual | Meta |
|---------|-------|------|
| Sessões de foco de 90 min por semana | 0 | 8 (meta) |
| Taxa de conclusão de blocos sem interrupção | sem dado | 80% (meta) |
| Horas em mensagens fora do lote | sem dado | queda de 50% (meta) |

## Decisões e tradeoffs

1. Blocos de 90 minutos em vez de 25 (Pomodoro): engenharia de automação exige carregar contexto grande, e 25 minutos mal cobrem o aquecimento. O custo é exigir disciplina maior de proteção.
2. Só 2 blocos por dia no início: evita plano heroico que quebra na primeira semana. O custo é parecer pouco ambicioso.
3. Pausa real longe da tela entre blocos: recuperação atencional exige desengajamento. O custo é resistir ao impulso de "aproveitar" o intervalo para mensagens.
4. Mensagens em 2 lotes diários em vez de resposta contínua: reduz resíduo de atenção. O custo é negociar expectativa de resposta com o time.
5. Medir interrupções por origem: sem dado, toda proteção é chute. O custo é o atrito de registrar cada quebra.

## Impacto no negócio

Operação de automação vive de entrega cognitiva: um fluxo bem modelado economiza horas de retrabalho em todos os clientes atendidos. Proteger foco diário aumenta a taxa de entrega de projetos de infra sem aumentar horas trabalhadas, o que reduz custo operacional e estabiliza prazos na unidade.

## Referências

- Curso: Learning How to Learn (Barbara Oakley, Terrence Sejnowski), Coursera: https://www.coursera.org/learn/learning-how-to-learn
- Vídeo: Tim Urban, Inside the Mind of a Master Procrastinator, TED: https://www.youtube.com/watch?v=arj7oStGLkU
- Doc: Todoist, guia de bloqueio de tempo (time blocking, tarefas em lote, temática diária): https://todoist.com/pt-BR/productivity-methods/time-blocking
- Doc: Asana, Deep Work: significado, benefícios e 7 táticas de foco: https://asana.com/resources/what-is-deep-work
