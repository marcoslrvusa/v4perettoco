# Atividade 3: Delegação e Feedback

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
│   ├── STD-01-matriz-delegacao.md
│   └── STD-02-feedback-sbi.md
├── 2-implementacao/
│   ├── TPL-matriz-delegacao.md
│   └── TPL-roteiro-feedback-sbi.md
└── 7-apresentacao/
    ├── DECK-PDI.md
    ├── DEMO-SCRIPT.md
    ├── ROTEIRO-DOMINIO.md
    ├── pdi-lideranca-mentoria-codereview-a3.html
    ├── pdi-lideranca-mentoria-codereview-a3.docx
    ├── pdi-lideranca-mentoria-codereview-a3.pdf
    └── gerar-docx.py
```

## Problema Resolvido

O líder da operação centraliza por medo de erro: delega a tarefa mas não a autoridade, cobra no meio do caminho e refaz o trabalho no final. O liderado, sem critério claro, ou espera ordem para tudo ou decide além da conta e erra. Feedback só aparece quando explode, genérico ("precisa melhorar a qualidade") e sem exemplo, o que gera defesa em vez de mudança. Esta atividade entrega matriz de delegação em 5 níveis, regra do que nunca se delega e roteiro de feedback SBI (Situação, Comportamento, Impacto) com exemplos prontos de TI e marketing.

## Arquitetura Resumida

```
Para cada pacote de trabalho:
  -> Classificar na matriz (nível 1 executar sob instrução até nível 5 decidir e informar)
  -> Registrar por escrito: resultado esperado, restrições, prazo, ponto de checagem
  -> Executar sem interferência até o checkpoint combinado
  -> Feedback SBI em até 48h do fato, 1 reforço para cada 1 correção
  -> Revisar nível de delegação a cada ciclo: acertou, sobe um nível
```

## Próximos Passos

1. Mapear as 10 tarefas mais centralizadas do líder na matriz e delegar 4 no próximo ciclo.
2. Registrar 1 feedback SBI por liderado por semana durante 1 mês.
3. Revisar níveis de delegação por pessoa ao fim do mês.

## Métricas de Sucesso

| Métrica | Atual | Meta |
|---------|-------|------|
| Tarefas delegadas com critério escrito | 15% | 80% (meta) |
| Feedbacks SBI registrados por mês | 2 | 12 (meta) |
| Retrabalho do líder em tarefa delegada | 40% | 10% (meta) |
| Horas do líder em execução operacional/semana | 25h | 10h (meta) |

## Decisões e tradeoffs

1. **5 níveis de delegação em vez de binário delega/não delega.** Graduação permite soltar aos poucos; o custo é classificar cada tarefa no início, que some após 1 mês de prática.
2. **Checkpoint combinado substitui acompanhamento contínuo.** Confiança com verificação pontual; o risco de desvio entre checkpoints é limitado pelo tamanho do pacote (máximo 1 semana).
3. **SBI escrito antes de falar.** Escrever Situação, Comportamento e Impacto evita feedback vago; o tradeoff é 5 min de preparo que salvam 50 min de conversa defensiva.
4. **Proporção mínima 1:1 entre reforço e correção.** Feedback só corretivo destrói moral; registrar reforço exige atenção ativa do líder, que é o próprio exercício de liderança.

## Impacto no negócio

Líder que delega com critério libera agenda para vender, planejar e resolver exceção, em vez de revisar vírgula. Liderado com autonomia graduada erra mais barato e aprende mais rápido, o que aumenta a capacidade real do time sem contratar. Feedback específico e frequente corrige rota em dias, não em trimestres, e isso aparece direto na qualidade entregue ao cliente.

## Referências

- Curso: Successful Negotiation, University of Michigan (Coursera): https://www.coursera.org/learn/negotiation-skills
- Vídeo: Simon Sinek, Why good leaders make you feel safe (TED2014): https://www.ted.com/talks/simon_sinek_why_good_leaders_make_you_feel_safe
- Doc oficial: Google Engineering Practices, How to do a code review (feedback escrito): https://google.github.io/eng-practices/review/reviewer/
- Doc oficial: GitHub Docs, About pull request reviews: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews
