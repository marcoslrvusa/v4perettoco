# Atividade 1: Code Review Efetivo

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
│   ├── STD-01-politica-code-review.md
│   └── STD-02-cultura-e-etiqueta-review.md
├── 2-implementacao/
│   ├── TPL-checklist-review.md
│   └── TPL-pr-descricao-e-sla.md
└── 7-apresentacao/
    ├── DECK-PDI.md
    ├── DEMO-SCRIPT.md
    ├── ROTEIRO-DOMINIO.md
    ├── pdi-lideranca-mentoria-codereview-a1.html
    ├── pdi-lideranca-mentoria-codereview-a1.docx
    ├── pdi-lideranca-mentoria-codereview-a1.pdf
    └── gerar-docx.py
```

## Problema Resolvido

Reviews na FV hoje são binários e lentos: ou o PR passa sem leitura, ou trava por dias em discussão de estilo. PRs gigantes (800+ linhas) passam com "LGTM" enquanto PRs pequenos ficam presos por preferência pessoal. O resultado é retrabalho pós merge, bugs que o review deveria ter barrado e fricção entre autor e revisor. Esta atividade cria regra escrita do que barra o merge, do que é só sugestão, checklist objetivo por categoria e SLA de primeira resposta, para review rápido, previsível e respeitoso.

## Arquitetura Resumida

```
Autor abre PR (descricao + tamanho <= 400 linhas)
  -> CI roda (lint + testes) e sinaliza no PR
  -> CODEOWNERS define revisor obrigatório
  -> Revisor aplica checklist (corretude, testes, segurança, legibilidade)
  -> Veredito em 3 vias: APPROVE, COMMENT (sugestão, merge livre) ou REQUEST CHANGES (barreira listada)
  -> Autor resolve barreiras, responde sugestões, merge com squash
  -> Métricas semanais: tempo de primeira resposta, tamanho mediano, retrabalho pós merge
```

## Próximos Passos

1. Adotar o checklist como template de PR nos 3 repositórios de maior movimento.
2. Configurar CODEOWNERS e proteção de branch exigindo 1 approval.
3. Medir 4 semanas de tempo de resposta e tamanho de PR e revisar o SLA.

## Métricas de Sucesso

| Métrica | Atual | Meta |
|---------|-------|------|
| Tempo mediano até primeira resposta no PR | 26h | 8h (meta) |
| PRs acima de 400 linhas | 38% | 10% (meta) |
| Retrabalho ou hotfix até 7 dias pós merge | 17% | 6% (meta) |
| Comentários acionáveis por PR | 1,8 | 3,0 (meta) |

## Decisões e tradeoffs

1. **Barreira curta e explícita (7 itens) vs lista exaustiva.** Lista curta é memorizável e aplicável; o risco de deixar passar algo raro é coberto pelo CI e pelo segundo revisor em áreas críticas.
2. **Sugestão não bloqueia merge.** Preferência de estilo como comentário `nit:` mantém o fluxo andando; o tradeoff é aceitar divergência cosmética em troca de velocidade.
3. **Teto de 400 linhas por PR como norma, não como trava técnica.** Trava rígida geraria fracionamento artificial; norma com justificativa obrigatória acima do teto equilibra disciplina e exceção legítima.
4. **SLA de primeira resposta (8h úteis) em vez de SLA de merge.** Merge depende do autor; resposta depende do revisor. Cobrar o que cada um controla evita meta injusta.
5. **1 approval obrigatório, 2 em áreas críticas (pagamento, dados, auth).** Dois revisores em tudo dobraria a fila; seletividade concentra rigor onde o blast radius é maior.

## Impacto no negócio

Review previsível destrava o fluxo de entrega da operação: campanhas, integrações e automações chegam a produção mais rápido e com menos hotfix, o que reduz custo de retrabalho e protege a reputação com clientes que dependem de janelas curtas de mídia e CRM. Além disso, review bem feito forma gente sênior mais rápido, porque cada PR vira mentoria prática em código real.

## Referências

- Curso: The Manager's Toolkit: A Practical Guide to Managing People at Work, University of London (Coursera): https://www.coursera.org/learn/people-management
- Vídeo: Simon Sinek, How great leaders inspire action (TEDxPuget Sound): https://www.ted.com/talks/simon_sinek_how_great_leaders_inspire_action
- Doc oficial: Google Engineering Practices, Code Review (visão geral): https://google.github.io/eng-practices/review/
- Doc oficial: GitHub Docs, About pull request reviews: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews
