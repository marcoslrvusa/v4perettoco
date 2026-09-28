# Roteiro de Domínio: Atividade 1 (Mensageria: fila, tópico, DLQ)

5 perguntas que um coordenador faria, com respostas curtas para defesa no presencial.

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
