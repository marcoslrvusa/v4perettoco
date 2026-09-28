# Roteiro de Dominio: Atividade 3 (Circuit Breaker e Retry/Backoff)

5 perguntas que um coordenador faria, com respostas curtas para defesa no presencial.

## 1. Quando o breaker abre e o que acontece depois?
Acima de 5 falhas em 10s ele abre; em OPEN o fallback responde; apos 30s uma sonda half-open testa e fecha se ok.

## 2. Por que timeout de 800ms?
Para o Pagamento nao segurar thread esperando o Score; sem resposta nesse prazo conta como falha e cai no breaker.

## 3. O que o fallback devolve?
Score em cache ou default, resposta de degradacao graciosa em menos de 1s, explicita em vez de 5xx.

## 4. Por que backoff com jitter e nao retry imediato?
Retry imediato multiplica a carga no servico ja lento; backoff de 0.1 a 0.4s com ruido espalha as retentativas.

## 5. Como voce prova a resiliencia?
Simula queda, o breaker abre no limite, o fallback cobre 100% do outage e o half-open reabilita; meta de 99,9% de disponibilidade do Pagamento.
