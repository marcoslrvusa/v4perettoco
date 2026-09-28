# STD-02: Cultura e Etiqueta de Review

## 1. Princípio central

Critique o código, nunca a pessoa. Todo comentário deve permitir que o autor entenda o problema, a gravidade e a saída. Se o comentário não diz o que fazer, ele é desabafo, não review.

## 2. Formato de comentário que funciona

`[gravidade] O que observei + por que importa + sugestão concreta.`

Exemplos reais:

- Ruim: "isso aqui está horrível."
- Bom: "[barreira] A query concatena o id na string, o que abre SQL injection. Sugestão: usar query parametrizada como no exemplo do repo de billing."
- Ruim: "por que você fez assim?"
- Bom: "[dúvida] Não entendi por que o retry fica dentro do loop e não fora. Pode explicar? Se for para cobrir timeout parcial, sugiro um comentário no código."
- Ruim: "muda o nome disso."
- Bom: "[nit] `d` é críptico para quem vai manter. Sugestão: `diasDeAtraso`. Não bloqueia."

## 3. Deveres do autor

- PR pequeno, descrição que explica o porquê (não só o o quê) e como testar.
- Não marcar 5 revisores "para ver quem pega". Marcar 1 principal e 1 opcional.
- Responder ponto a ponto; marcar como resolvido só depois de ajustar ou alinhar.
- Nunca levar request changes para o pessoal: pedir call de 15 min quando a thread passar de 3 trocas.

## 4. Deveres do revisor

- Revisar no SLA mesmo sem tempo ideal: 20 min focados valem mais que 2h adiadas.
- Começar pelo que barra; cosmético fica para o fim e marcado como `nit:`.
- Elogiar acerto não óbvio ("bom teste de borda aqui"). Reforço específico ensina tanto quanto correção.
- Não aprovar sem ler. "LGTM" em PR de 900 linhas é atestado de ausência, não de qualidade.

## 5. Resolução de impasse

1. Thread com mais de 3 trocas vira call de 15 min.
2. Sem acordo, decide o dono da área (CODEOWNERS) em 1 dia útil.
3. Decisão registrada no PR em 3 linhas: contexto, decisão, motivo. Sem registro, o mesmo debate volta no próximo PR.

## 6. Sinais de cultura saudável (revisão mensal do líder)

- Tempo de primeira resposta caindo sem cobrança individual.
- Proporção de `nit:` estável ou caindo (time alinhando estilo via linter, não via review).
- Autores pedindo review antes de terminar (confiança) em vez de esconder PR até o fim (medo).
