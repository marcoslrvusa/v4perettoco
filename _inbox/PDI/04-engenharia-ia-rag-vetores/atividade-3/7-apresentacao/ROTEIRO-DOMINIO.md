# Roteiro de dominio: Atividade 3, Orquestracao Multi-agente

## 1. Por que supervisor com handoff e nao agente unico com 8k tokens?
Resposta: prompt monolitico mistura triagem, consulta e proposta e um erro contamina tudo, com 3 workers isolados o erro fica contido e testavel.

## 2. O que vai dentro do handoff tipado?
Resposta: so o resumo minimo necessario para o proximo worker, com contexto proprio por agente para garantir vazamento 0.

## 3. O que acontece quando um worker estoura 15 s?
Resposta: dispara fallback, o supervisor faz re-rota para worker de reserva sem perder o estado geral, com cobertura em 100 por cento dos handoffs.

## 4. Como evitar loop entre agentes?
Resposta: com max hops, limite de saltos, mais supervisor em modelo leve para conter custo de reiteracao.

## 5. Como a memoria evita reexecucao do zero?
Resposta: com store de curto prazo para o turno e longo prazo para aprendizado, retomando do ultimo handoff valido e elevando o sucesso de cerca de 49 por cento para cerca de 97 por cento.
