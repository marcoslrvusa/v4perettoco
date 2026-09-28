# Roteiro de dominio: Atividade 4, Engenharia de Custos de LLM

## 1. Por que nao usar modelo maxi para tudo?
Resposta: porque custa 10x, a regra manda trivial para modelo leve, complexo para forte e repetido para cache.

## 2. Como o cache atinge hit maior ou igual a 30 por cento sem vazar PII?
Resposta: cache semantico para perguntas repetidas com regra dura de nunca cachear PII, medindo hit rate a cada lote.

## 3. O que significa custo por tarefa menor ou igual a baseline vezes 0.4?
Resposta: e a meta de pagar no maximo 40 por cento do custo original por tarefa, com ledger de tokens e reais por fluxo para auditar.

## 4. Como o budget por cliente funciona na pratica?
Resposta: cada cliente tem teto com alerta em 80 por cento, cache miss mais modelo caro dispara aviso antes do estouro.

## 5. Como manter reducao maior ou igual a 85 por cento com score maior ou igual a 0.90?
Resposta: combinando roteamento mais cache mais batch assincrono dentro do SLA, com eval que barra troca que derrube qualidade.
