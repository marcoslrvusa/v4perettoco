# Roteiro de domínio: Pipeline de Testes Automatizados (Unit/Integration/E2E) com 80% de Cobertura

Estudo para defesa presencial da atividade: 5 perguntas de coordenador com respostas curtas.

## 1. Por que 3 camadas em vez de só unitários mockados?

Porque unitário sozinho é rápido mas cego a integração, então a estratégia soma unitário para lógica pura, integração com DB efêmero para ports e E2E só no happy path.

## 2. Como o gate de 80 por cento bloqueia o merge na prática?

Com pytest --cov=src --cov-fail-under=80 no CI como required check: cobertura abaixo de 80 por cento falha o pipeline e o PR não mergeia.

## 3. Por que o E2E fica em stage separado com retry?

Porque E2E é lento e mais instável, então roda separado com retry para não travar o merge enquanto unit e integração seguram o gate em menos de 3 min.

## 4. O que significam as metas de 90 por cento, 80 por cento e menos de 1 por cento?

Unitário mira 90 por cento na lógica pura, integração mira 80 por cento nos ports com DB efêmero, e flaky rate fica abaixo de 1 por cento com retry de 1 vez e isolamento.

## 5. Qual comando valida a entrega localmente?

pytest --cov=src --cov-fail-under=80, que reproduz o gate do CI em qualquer máquina antes do push.
