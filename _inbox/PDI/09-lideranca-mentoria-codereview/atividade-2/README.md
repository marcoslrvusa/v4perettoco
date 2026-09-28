# Atividade 2: Mentoria e 1:1

| Campo | Valor |
|-------|-------|
| Área | Automação & Infraestrutura |
| Unidade | FV Marketing / V4 Company |
| Autor | Marcos Luciano |
| Data | Setembro 2026 |
| Status | Entregue (desenvolvido, homologação pendente) |

## Entregas desta PDI

```
atividade-2/
├── README.md
├── 1-standards/
│   ├── STD-01-estrutura-1-1.md
│   └── STD-02-plano-de-evolucao.md
├── 2-implementacao/
│   ├── TPL-pauta-1-1.md
│   └── TPL-plano-evolucao-liderado.md
└── 7-apresentacao/
    ├── DECK-PDI.md
    ├── DEMO-SCRIPT.md
    ├── ROTEIRO-DOMINIO.md
    ├── pdi-lideranca-mentoria-codereview-a2.html
    ├── pdi-lideranca-mentoria-codereview-a2.docx
    ├── pdi-lideranca-mentoria-codereview-a2.pdf
    └── gerar-docx.py
```

## Problema Resolvido

1:1 na operação hoje é status report disfarçado: o líder pergunta "como estão as tarefas", o liderado lista tickets e ambos saem sem tratar carreira, carga ou bloqueios reais. Sem pauta fixa, sem registro e sem plano de evolução, o crescimento do liderado depende de sorte e o líder só descobre o burnout na saída. Esta atividade entrega estrutura de conversa em 4 blocos, banco de perguntas por tema e modelo de plano de evolução trimestral com metas verificáveis.

## Arquitetura Resumida

```
Ciclo quinzenal de 30 min por liderado
  -> Bloco 1 check-in humano (5 min): energia, carga, contexto pessoal
  -> Bloco 2 progresso do plano (10 min): metas do trimestre, evidências
  -> Bloco 3 bloqueios e feedback bidirecional (10 min): SBI nos dois sentidos
  -> Bloco 4 combinados (5 min): até 3 ações com dono e prazo, registradas
  -> Plano trimestral revisado a cada 6 ciclos, com nota de evolução por competência
```

## Próximos Passos

1. Agendar 1:1 quinzenal fixo com cada liderado direto usando a pauta padrão.
2. Abrir um plano de evolução por liderado com 2 a 3 metas para o trimestre.
3. Revisar após 6 semanas: taxa de combinados cumpridos e qualidade das metas.

## Métricas de Sucesso

| Métrica | Atual | Meta |
|---------|-------|------|
| Liderados com 1:1 quinzenal recorrente | 20% | 100% (meta) |
| Planos de evolução ativos por liderado | 0 | 1 (meta) |
| Combinados de 1:1 cumpridos no prazo | sem medição | 75% (meta) |
| Cancelamentos de 1:1 por mês | 3 por liderado | 0 (meta) |

## Decisões e tradeoffs

1. **30 min quinzenal como padrão, não 60 min mensal.** Frequência alta detecta problema cedo; o custo é mais slots na agenda, compensado por pauta rígida que impede estouro.
2. **Pauta do liderado, não do líder.** Quem traz os temas é o liderado, o que exige preparo dele; o tradeoff é 1:1 vazio nas primeiras semanas até o hábito formar.
3. **Registro escrito mínimo (combinados + decisões).** Sem ata completa para não burocratizar; o risco de perder contexto é mitigado pelo histórico de combinados.
4. **Plano trimestral com no máximo 3 metas.** Foco supera cobertura; metas extras viram backlog explícito em vez de promessa difusa.

## Impacto no negócio

Liderado com conversa regular e plano claro produz mais e pede demissão menos: a FV reduz turnover de quem já conhece os clientes e acelera a formação de gente plena, o que baixa custo de reposição e mantém continuidade nas contas. 1:1 bem feito também antecipa risco de entrega, porque bloqueio aparece na conversa antes de virar atraso no cliente.

## Referências

- Curso: Leading Teams, University of Michigan (Coursera): https://www.coursera.org/learn/leading-teams
- Vídeo: Brené Brown, The power of vulnerability (TEDxHouston): https://www.ted.com/talks/brene_brown_the_power_of_vulnerability
- Doc oficial: Google Engineering Practices, How to do a code review (mentoria via comentários): https://google.github.io/eng-practices/review/reviewer/
- Doc oficial: Atlassian, Agile retrospectives (ritual de evolução contínua): https://www.atlassian.com/agile/scrum/retrospectives
