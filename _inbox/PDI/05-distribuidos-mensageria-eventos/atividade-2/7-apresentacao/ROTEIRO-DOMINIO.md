# Roteiro de Dominio: Atividade 2 (Idempotencia e exactly-once)

5 perguntas que um coordenador faria, com respostas curtas para defesa no presencial.

## 1. Por que voce nao garante exactly-once no broker?
Porque em sistema distribuido so existe at-least-once; o exactly-once aparece para o negocio via dedup, o effectively-once.

## 2. O que e o outbox e qual problema ele resolve?
Grava venda e evento na mesma transacao; se a publicacao falha, o relay republica do outbox a cada 1s em vez de perder o evento.

## 3. Onde a chave de idempotencia e verificada?
No consumer, antes de cobrar, consultando a tabela de processados por `idempotency_key`.

## 4. O que acontece se dois consumers pegarem o mesmo evento?
A verificacao garante 1 aplicacao; o ACK so apos gravar a chave sustenta isso mesmo com 2 consumers.

## 5. Como voce prova que funciona?
Mesmo evento 3x gera 1 efeito, o teste injeta 5x e afirma 1 cobranca, com meta de zero duplicata e 100% dos handlers idempotentes.
