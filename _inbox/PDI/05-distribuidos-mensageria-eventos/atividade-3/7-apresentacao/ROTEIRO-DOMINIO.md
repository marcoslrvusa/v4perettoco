# Roteiro de Domínio: Atividade 3 (Circuit Breaker e Retry/Backoff)

5 perguntas que um coordenador faria, com respostas curtas para defesa no presencial.

## 1. Quando o breaker abre e o que acontece depois?
Acima de 5 falhas em 10s ele abre; em OPEN o fallback responde; após 30s uma sonda half-open testa e fecha se ok.

## 2. Por que timeout de 800ms?
Para o Pagamento não segurar thread esperando o Score; sem resposta nesse prazo conta como falha e cai no breaker.

## 3. O que o fallback devolve?
Score em cache ou default, resposta de degradação graciosa em menos de 1s, explícita em vez de 5xx.

## 4. Por que backoff com jitter e não retry imediato?
Retry imediato multiplica a carga no serviço já lento; backoff de 0.1 a 0.4s com ruído espalha as retentativas.

## 5. Como você prova a resiliência?
Simula queda, o breaker abre no limite, o fallback cobre 100% do outage e o half-open reabilita; meta de 99,9% de disponibilidade do Pagamento.
