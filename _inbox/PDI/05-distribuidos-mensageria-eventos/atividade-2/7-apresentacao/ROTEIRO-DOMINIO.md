# Roteiro de Domínio: Atividade 2 (Idempotência e exactly-once)

5 perguntas que um coordenador faria, com respostas curtas para defesa no presencial.

## 1. Por que você não garante exactly-once no broker?
Porque em sistema distribuído só existe at-least-once; o exactly-once aparece para o negócio via dedup, o effectively-once.

## 2. O que é o outbox e qual problema ele resolve?
Grava venda e evento na mesma transação; se a publicação falha, o relay republica do outbox a cada 1s em vez de perder o evento.

## 3. Onde a chave de idempotência e verificada?
No consumer, antes de cobrar, consultando a tabela de processados por `idempotency_key`.

## 4. O que acontece se dois consumers pegarem o mesmo evento?
A verificação garante 1 aplicação; o ACK só após gravar a chave sustenta isso mesmo com 2 consumers.

## 5. Como você prova que funciona?
Mesmo evento 3x gera 1 efeito, o teste injeta 5x e afirma 1 cobrança, com meta de zero duplicata e 100% dos handlers idempotentes.
