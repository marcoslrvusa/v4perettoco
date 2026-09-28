# Roteiro de dominio: Pipeline de Testes Automatizados (Unit/Integration/E2E) com 80% de Cobertura

Estudo para defesa presencial da atividade: 5 perguntas de coordenador com respostas curtas.

## 1. Por que 3 camadas em vez de so unitarios mockados?

Porque unitario sozinho e rapido mas cego a integracao, entao a estrategia soma unitario para logica pura, integracao com DB efemero para ports e E2E so no happy path.

## 2. Como o gate de 80 por cento bloqueia o merge na pratica?

Com pytest --cov=src --cov-fail-under=80 no CI como required check: cobertura abaixo de 80 por cento falha o pipeline e o PR nao mergeia.

## 3. Por que o E2E fica em stage separado com retry?

Porque E2E e lento e mais instavel, entao roda separado com retry para nao travar o merge enquanto unit e integracao seguram o gate em menos de 3 min.

## 4. O que significam as metas de 90 por cento, 80 por cento e menos de 1 por cento?

Unitario mira 90 por cento na logica pura, integracao mira 80 por cento nos ports com DB efemero, e flaky rate fica abaixo de 1 por cento com retry de 1 vez e isolamento.

## 5. Qual comando valida a entrega localmente?

pytest --cov=src --cov-fail-under=80, que reproduz o gate do CI em qualquer maquina antes do push.
