# Atividade 3: Gestão de Incidentes e Postmortems sem Culpa

| Campo | Valor |
|---|---|
| Área | Automação & Infraestrutura |
| Unidade | FV Marketing / V4 Company |
| Autor | Marcos Luciano |
| Data | Setembro 2026 |
| Status | Entregue (desenvolvido) |

## Entregas desta PDI

```
atividade-3/
├── README.md
├── 1-standards/
│   └── STANDARD-INCIDENTES-POSTMORTEM.md
├── 2-implementacao/
│   ├── template-postmortem.md
│   └── checklist-resposta-incidente.md
└── 7-apresentacao/
    ├── DECK-PDI.md
    ├── DEMO-SCRIPT.md
    ├── ROTEIRO-DOMINIO.md
    ├── report.json
    ├── gerar-docx.py
    ├── pdi-gestao-projetos-tecnicos-a3.html
    ├── pdi-gestao-projetos-tecnicos-a3.docx
    └── pdi-gestao-projetos-tecnicos-a3.pdf
```

## Problema Resolvido

Quando uma automação quebrava (relatório não chega, lead não entra no CRM, webhook falha), a resposta era improviso no Slack: ninguém sabia quem lidera, o que já foi tentado, nem quando avisar a operação. Depois, nenhum registro: o mesmo incidente voltava meses depois. Esta atividade entrega resposta padronizada (papéis, severidades, comunicação) e postmortem sem culpa com ações rastreadas.

## Arquitetura Resumida

```
Alerta/sintoma -> Classifica severidade (S1-S4) -> Comandante assume + canal dedicado
  -> Mitiga (para o sangramento) -> Resolve (corrige a causa)
  -> Postmortem em até 5 dias úteis (timeline, 5 porques, acoes com dono e prazo)
  -> Acoes viram cartoes no kanban até Pronto
```

## Próximos Passos

1. Aplicar o checklist no próximo incidente real e medir tempo de detecção e de mitigação.
2. Escrever o primeiro postmortem real com o template e acompanhar as ações até Pronto.
3. Criar página única com severidades e contatos colada no canal do time.

## Métricas de Sucesso

| Métrica | Atual | Meta |
|---|---|---|
| Tempo médio de mitigação (S1/S2) | não medido (estimado 4h+) | 1h (meta) |
| Incidentes com postmortem em 5 dias | 0% | 100% (meta) |
| Ações de postmortem concluídas | não medido | 80% em 30 dias (meta) |

## Decisões e tradeoffs

1. **Mitigar antes de entender a causa raiz**: parar o impacto (rollback, desligar automação) vem antes do diagnóstico completo; tradeoff é adiar a curiosidade técnica em troca de proteger a operação.
2. **Postmortem sem culpa por escrito**: proíbe "erro humano" como causa e foca em condição que permitiu o erro; tradeoff é exigir mais rigor na escrita (5 porquês de verdade).
3. **Prazo de 5 dias úteis para o postmortem**: memória esfria rápido; tradeoff é escrever com ações ainda em andamento (aceitável, desde que rastreadas).
4. **4 severidades em vez de 3**: S4 (dor menor, sem impacto em campanha) evita inflar S3; tradeoff é 1 nível a mais para classificar sob pressão.
5. **Ações viram cartões no kanban**: postmortem sem ação rastreada e terapia; tradeoff é competir com delivery no WIP (ação S1/S2 tem classe urgente).

## Impacto no negócio

Resposta padronizada reduz o tempo que campanhas ficam no escuro e postmortem sem culpa impede a repetição do mesmo incidente, o que protege verba de mídia, fluxo de leads e a confiança da operação na automação.

## Referências

- Curso: SRE Fundamentals (Google Cloud Skills Boost)
- Vídeo: Postmortem culture, SREcon (YouTube)
- Doc: Site Reliability Engineering, Google SRE Book, índice e capítulos 14 e 15: https://sre.google/sre-book/table-of-contents/
- Doc: Post-Incident Reviews, PagerDuty Docs: https://docs.pagerduty.com/docs/postmortems
