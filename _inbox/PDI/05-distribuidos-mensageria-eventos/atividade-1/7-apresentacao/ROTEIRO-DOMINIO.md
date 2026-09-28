# Roteiro de Domínio: Atividade 1 (Mensageria: fila, tópico, DLQ)

5 perguntas que um coordenador faria, com respostas curtas para defesa no presencial.

Ao final, 7 perguntas adversariais complementares e 1 de negócio, no total de 12 questões.

## 1. Quando você usa fila e quando usa tópico nesta atividade?
Fila na cobrança (1 mensagem para 1 worker) e tópico em pub/sub para Marketing e Operação receberem o mesmo `venda.criada`.

## 2. O que acontece se o consumer cair no meio do processamento?
Sem ACK o broker reentrega; o teste publica 1k mensagens, derruba o consumer e confirma o reprocessamento.

## 3. Para que serve a DLQ e quem cuida dela?
Recebe a mensagem inválida após N tentativas para não perder nada; o `runbook-mensageria.md` orienta o reprocessamento em menos de 24h.

## 4. O que é prefetch limitado e por que ele existe?
Limita quantas mensagens o consumer recebe por vez, então um consumer lento não estoura por falta de backpressure.

## 5. Como você prova o ganho para o negócio?
Metas de 200 msg/s, zero perda em pico e P95 abaixo de 5s de ponta a ponta, contra timeout em cascata no modelo síncrono.

## Perguntas adversariais

## 6. Por que não usar só HTTP síncrono com retry? É mais simples.
Porque o retry multiplica a carga exatamente no ponto que já falhou e mantém o acoplamento de
tempo entre times: se o Financeiro atrasa 2 s, o Vendas atrasa 2 s junto. Resposta curta: HTTP
resolve dependência de rede, não dependência de tempo; a fila transforma espera em buffer.
Complemento: o custo do broker é conhecido (operação e plantão), enquanto o custo da cascata é
descoberto em pico de campanha.

## 7. Quanto custa manter um broker em produção?
Depende de duas contas: infraestrutura (mensagens e retenção) e plantão (revisão de DLQ e
alertas). Exemplo numérico: `200 msg/s` durante 8 h diária dá `5,76 milhões` de mensagens/dia;
com 1 KB por mensagem são `172,8 GB/mês` antes de replicação, que é o número que decide
retenção de 7 dias contra 24 h. Do lado de pessoas: (meta) algumas horas por mês de revisita de
DLQ e de revisão de alerta. Essa conta compara com o custo oculto atual de perda e retrabalho.

## 8. Quem decide que uma mensagem vai para a DLQ, e quem decide que ela volta?
O código decide a ida (N tentativas esgotadas ou falha determinística de parse), com motivo
registrado. O dono da fila decide a volta, seguindo o runbook, sempre com `dry_run` antes. Ninguém
apaga mensagem de DLQ sem linha de log; exclusão não é decisão de plantão, é decisão do dono do
domínio.

## 9. E se cair no meio da noite, o que a equipe faz?
Primeiro diagnóstico em três métricas: `queue.depth` subindo (consumer caído, religar),
`consumer.unacked` no teto (consumer lento, investigar `$W$`), `dlq.depth` crescendo (dependência
externa, aumentar teto de backoff). Rollback de versão de consumer leva menos de 15 min (meta)
porque nada foi perdido, apenas represado. A perda de mensagem é a única que aciona liderança
imediatamente.

## 10. Qual é o SLO, e o que acontece quando ele estoura?
`>= 200 msg/s`, `0` mensagens perdidas, p95 `< 5 s` (meta) de ponta a ponta e DLQ revisada em
`< 24 h`. Estourou a latência: olhar `queue.depth` e dependência externa. Estourou a perda:
incidente P1, reconstruir por log e republicar. Estourou a DLQ: alerta dispara em 1 h e a revisita
ocorre antes das 24 h, com dono notificado.

## 11. Como você prova que isso funciona, além de falar?
Com testes executáveis e critérios numéricos: T1 perda (1.000 mensagens, consumer derrubado,
contagem final igual), T3 DLQ (payload inválido, `dlq.depth = 1` e fila zerada), T4 backpressure
(fila cresce, RSS varia menos de 10%) e T10 DLQ esquecida (alerta antes de 24 h). Todos estão no
plano de teste do `MESSAGING.md`, com saída esperada e critério de falha declarados.

## 12. Existe garantia de exatamente uma entrega? Por que não?
Não, de ponta a ponta. Produtor, broker e consumidor são processos separados; a janela entre
commit do efeito e envio do ACK existe sempre. O que se compra é at-least-once no transporte mais
efeito único na aplicação, com chave de idempotência registrada na mesma transação do efeito.
Dizer "exactly-once" sem essa ressalva é promessa que a produção cobra.

## 13. Qual a alternativa mais barata que você descartaria de novo?
Fila única compartilhada por todos os times. É mais barata (um canal só), mas o pico de um
domínio suga a capacidade do outro e destrói o isolamento, que é justamente o objetivo. Também
descartaria aumentar `prefetch` para "fazer a fila correr": só repassa o represamento da fila para
a memória do processo, que é um lugar pior para perder dados.

## Pergunta de negócio

## 14. Qual o impacto em R$ e em horas?
Dois lados. Lado da perda: cada lead que o Marketing não alcança por atraso é oportunidade
perdida (valor a confirmar com o time comercial) e cada cobrança duplicada gera estorno mais
atendimento, que são horas de operação. Lado do investimento: (meta) 23 horas de esforço de
implantação desta atividade mais (meta) algumas horas por mês de operação do broker e revisita de
DLQ. A troca é consciente: comprar um custo fixo e visível para eliminar um custo variável e
escondido que só aparece em pico, exatamente quando mais vale.

## O que eu deixaria para trás (resposta de fecho)

Se o tempo apertar, deixo para depois: reprodução multi-região, particionamento automático de
tópico quente e transação produtor de ponta a ponta. Não deixo nunca: ACK depois do commit,
`prefetch` derivado de `$\lambda W / workers$`, DLQ com dono e teste de perda na esteira. Esses
quatro são o que separa "temos uma fila" de "temos um sistema que não perde dinheiro".
