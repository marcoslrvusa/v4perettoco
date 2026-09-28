# Roteiro de domínio: Atividade 3, Orquestração Multi-agente

Perguntas de coordenador, na ordem em que tendem a aparecer. Cada resposta fecha com o número, a decisão ou o
dono, para não virar conversa aberta.

## 1. Por que supervisor com handoff e não agente único com 8k tokens?
Resposta: prompt monolítico mistura triagem, consulta e proposta e um erro contamina tudo, com 3 workers isolados o erro fica contido e testável.
Aprofundamento: em tarefa de três etapas o sucesso composto é $p^3$. Com 0,79 por etapa dá 0,49, ou seja,
cerca de 49 por cento, e a conta explica por que adianta trocar de modelo sem trocar de fronteira.

## 2. O que vai dentro do handoff tipado?
Resposta: só o resumo mínimo necessário para o próximo worker, com contexto próprio por agente para garantir vazamento 0.
Aprofundamento: campos obrigatórios são `trace_id`, `seq`, `origin`, `dest`, `intent` e `payload`, com teto de
8 KB validado na origem. Payload acima do teto é rejeitado, não comprimido no destino.

## 3. O que acontece quando um worker estoura 15 s?
Resposta: dispara fallback, o supervisor faz re-rota para worker de reserva sem perder o estado geral, com cobertura em 100 por cento dos handoffs.
Aprofundamento: o estado do turno já está gravado por salto, então a re-rota continua do ponto válido e não
repete efeito externo, porque a chave de idempotência deriva de `trace_id` mais `seq`.

## 4. Como evitar loop entre agentes?
Resposta: com max hops, limite de saltos, mais supervisor em modelo leve para conter custo de reiteração.
Aprofundamento: o teto não é número escolhido a olho. Sai de
$\lfloor (L_{tarefa} - L_{roteio}) / (L_{etapa} + L_{handoff}) \rfloor$, que com 30 s, 0,8 s, 3,2 s e 0,15 s
resulta em 8 saltos e pior caso de 27,6 s.

## 5. Como a memória evita reexecução do zero?
Resposta: com store de curto prazo para o turno e longo prazo para aprendizado, retomando do último handoff válido e elevando o sucesso de cerca de 49 por cento para cerca de 97 por cento.
Aprofundamento: curto prazo guarda último salto aplicado, saltos consumidos e resultado parcial, com TTL de
30 minutos. Longo prazo guarda lição promovida pelo crítico, com TTL de 90 dias e exigência de evidência.

## 6. Qual a alternativa mais barata e por que não foi essa?
Resposta: agente único com prompt grande e um bom modelo. Não foi porque o custo unitário, que fica próximo,
esconde o retrabalho: cerca de 49 por cento de tarefa falha e é reexecutada, e reexecução não é custo de
token, é custo de hora de humano esperando.
Aprofundamento: **Exemplo numérico** (parâmetros declarados): R$ 0,14 por consulta contra cerca de R$ 0,13 do
monolítico, diferença de cerca de R$ 0,01, ou seja, R$ 10 a cada mil consultas. Uma única tarefa refeita por
dia já começa a diferença em minutos de trabalho.

## 7. E se cair no meio da noite, o que acontece com a tarefa em voo?
Resposta: a tarefa fica com estado gravado por salto. Ao voltar, o consumidor retoma do último handoff válido
com o mesmo `trace_id` e não refaz as etapas já confirmadas.
Aprofundamento: a garantia é at-least-once com deduplicação, então pode haver mensagem repetida, mas não há
efeito externo repetido. RPO do estado é zero depois da gravação; RTO depende do tempo de subida do
consumidor, medido no exercício de queda de processo.

## 8. Qual é o SLO e o que você faz quando estoura?
Resposta: sucesso de tarefa composta >= 95 por cento em 30 dias rolantes, latência ponta a ponta p95 <= 30 s,
latência por agente p95 <= 15 s, fallback acionável em 100 por cento dos handoffs e vazamento zero.
Aprofundamento: orçamento de erro de 5 por cento em 10.000 tarefas dá 500 falhas no mês, ou cerca de 167 por
etapa. Estourou, primeira ação é congelar mudança de prompt e abrir a matriz de modos de falha.

## 9. Como você prova que funciona?
Resposta: conjunto-ouro por papel com critério de aceite numérico, executado antes de publicar qualquer
prompt, mais os casos de borda do plano de teste: timeout, ciclo, base vazia, unicode, texto vazio e
reentrega.
Aprofundamento: no worker de consulta a métrica é recall@k com `ef_search` declarado; sem trecho recuperado a
resposta volta como `sem_suporte`, o que transforma a prova em verificável e não em impressão de quem leu.

## 10. Quem decide se um novo worker entra no fluxo?
Resposta: quem detém a propriedade do padrão, registrado na ADR-043. A entrada de papel novo exige contrato de
handoff, teto de timeout derivado da fórmula, conjunto-ouro e métrica de latência própria, senão não entra.
Aprofundamento: a pergunta costuma vir disfarçada de "e se a gente adicionar mais um?". A resposta é que
cada worker novo compra um salto a mais na cadeia, e o salto consome latência do mesmo orçamento de 30 s.

## 11. Qual o risco de segurança mais provável e o que você fez?
Resposta: prompt injection direta na entrada e indireta em conteúdo recuperado pelo RAG, mais vazamento entre
etapas por contexto compartilhado.
Aprofundamento: três barreiras, todas verificáveis: entrada do usuário é tratada como dado e nunca como
instrução de sistema; só o worker de consulta alcança a base vetorial, por política de rede; e toda resposta
final exige trecho recuperado correspondente. Violação de isolamento é incidente P0 com rollback imediato.

## 12. Impacto em R$ ou horas, para o negócio?
Resposta: sucesso de cerca de 49 por cento para cerca de 97 por cento em tarefas de três etapas, o que
reduz retrabalho por contaminação e dá previsibilidade de custo por papel.
Aprofundamento: **Exemplo numérico** (parâmetros declarados): em 1.000 tarefas do mês, sair de 510 falhas
para 30 falhas elimina 480 reexecuções. Com 12 minutos de retrabalho por tarefa, são 5.760 minutos de menos
por mês, ou cerca de 96 horas úteis de capacidade liberada, antes de contar o custo de oportunidade de
resposta que chega tarde. O custo de execução projetado é de cerca de R$ 140 por mil consultas, valor com
parâmetros declarados e marcado como meta.
