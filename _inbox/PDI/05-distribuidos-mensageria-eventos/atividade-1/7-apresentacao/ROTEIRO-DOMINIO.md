# Roteiro de Dominio: Atividade 1 (Mensageria: fila, topico, DLQ)

5 perguntas que um coordenador faria, com respostas curtas para defesa no presencial.

## 1. Quando voce usa fila e quando usa topico nesta atividade?
Fila na cobranca (1 mensagem para 1 worker) e topico em pub/sub para Marketing e Operacao receberem o mesmo `venda.criada`.

## 2. O que acontece se o consumer cair no meio do processamento?
Sem ACK o broker reentrega; o teste publica 1k mensagens, derruba o consumer e confirma o reprocessamento.

## 3. Para que serve a DLQ e quem cuida dela?
Recebe a mensagem invalida apos N tentativas para nao perder nada; o `runbook-mensageria.md` orienta o reprocessamento em menos de 24h.

## 4. O que e prefetch limitado e por que ele existe?
Limita quantas mensagens o consumer recebe por vez, entao um consumer lento nao estoura por falta de backpressure.

## 5. Como voce prova o ganho para o negocio?
Metas de 200 msg/s, zero perda em pico e P95 abaixo de 5s de ponta a ponta, contra timeout em cascata no modelo sincrono.
