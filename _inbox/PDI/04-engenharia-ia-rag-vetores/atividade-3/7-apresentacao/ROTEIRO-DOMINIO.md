# Roteiro de domínio: Atividade 3, Orquestração Multi-agente

## 1. Por que supervisor com handoff e não agente único com 8k tokens?
Resposta: prompt monolítico mistura triagem, consulta e proposta e um erro contamina tudo, com 3 workers isolados o erro fica contido e testável.

## 2. O que vai dentro do handoff tipado?
Resposta: só o resumo mínimo necessário para o próximo worker, com contexto próprio por agente para garantir vazamento 0.

## 3. O que acontece quando um worker estoura 15 s?
Resposta: dispara fallback, o supervisor faz re-rota para worker de reserva sem perder o estado geral, com cobertura em 100 por cento dos handoffs.

## 4. Como evitar loop entre agentes?
Resposta: com max hops, limite de saltos, mais supervisor em modelo leve para conter custo de reiteração.

## 5. Como a memória evita reexecução do zero?
Resposta: com store de curto prazo para o turno e longo prazo para aprendizado, retomando do último handoff valido e elevando o sucesso de cerca de 49 por cento para cerca de 97 por cento.
