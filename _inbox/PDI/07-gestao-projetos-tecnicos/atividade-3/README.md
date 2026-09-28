# Atividade 3: Gestao de Incidentes e Postmortems sem Culpa

| Campo | Valor |
|---|---|
| Area | Automacao & Infraestrutura |
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

Quando uma automacao quebrava (relatorio nao chega, lead nao entra no CRM, webhook falha), a resposta era improviso no Slack: ninguem sabia quem lidera, o que ja foi tentado, nem quando avisar a operacao. Depois, nenhum registro: o mesmo incidente voltava meses depois. Esta atividade entrega resposta padronizada (papeis, severidades, comunicacao) e postmortem sem culpa com acoes rastreadas.

## Arquitetura Resumida

```
Alerta/sintoma -> Classifica severidade (S1-S4) -> Comandante assume + canal dedicado
  -> Mitiga (para o sangramento) -> Resolve (corrige a causa)
  -> Postmortem em ate 5 dias uteis (timeline, 5 porques, acoes com dono e prazo)
  -> Acoes viram cartoes no kanban ate Pronto
```

## Proximos Passos

1. Aplicar o checklist no proximo incidente real e medir tempo de deteccao e de mitigacao.
2. Escrever o primeiro postmortem real com o template e acompanhar as acoes ate Pronto.
3. Criar pagina unica com severidades e contatos colada no canal do time.

## Metricas de Sucesso

| Metrica | Atual | Meta |
|---|---|---|
| Tempo medio de mitigacao (S1/S2) | nao medido (estimado 4h+) | 1h (meta) |
| Incidentes com postmortem em 5 dias | 0% | 100% (meta) |
| Acoes de postmortem concluidas | nao medido | 80% em 30 dias (meta) |

## Decisoes e tradeoffs

1. **Mitigar antes de entender a causa raiz**: parar o impacto (rollback, desligar automacao) vem antes do diagnostico completo; tradeoff e adiar a curiosidade tecnica em troca de proteger a operacao.
2. **Postmortem sem culpa por escrito**: proibe "erro humano" como causa e foca em condicao que permitiu o erro; tradeoff e exigir mais rigor na escrita (5 porques de verdade).
3. **Prazo de 5 dias uteis para o postmortem**: memoria esfria rapido; tradeoff e escrever com acoes ainda em andamento (aceitavel, desde que rastreadas).
4. **4 severidades em vez de 3**: S4 (dor menor, sem impacto em campanha) evita inflar S3; tradeoff e 1 nivel a mais para classificar sob pressao.
5. **Acoes viram cartoes no kanban**: postmortem sem acao rastreada e terapia; tradeoff e competir com delivery no WIP (acao S1/S2 tem classe urgente).

## Impacto no negocio

Resposta padronizada reduz o tempo que campanhas ficam no escuro e postmortem sem culpa impede a repeticao do mesmo incidente, o que protege verba de midia, fluxo de leads e a confianca da operacao na automacao.

## Referencias

- Curso: SRE Fundamentals (Google Cloud Skills Boost)
- Video: Postmortem culture, SREcon (YouTube)
- Doc: Site Reliability Engineering, Google SRE Book, indice e capitulos 14 e 15: https://sre.google/sre-book/table-of-contents/
- Doc: Post-Incident Reviews, PagerDuty Docs: https://docs.pagerduty.com/docs/postmortems
