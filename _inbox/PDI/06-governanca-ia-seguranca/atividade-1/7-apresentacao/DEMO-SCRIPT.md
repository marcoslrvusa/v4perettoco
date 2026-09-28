# Demo Script | A1 Guardrails e anti-prompt-injection

Duracao: 10 min. Pre-requisito: `python3` disponivel e arquivo `guardrail_proxy.py` na pasta `2-implementacao/`.

1. Abra com a tese (30s): texto externo vira instrucao sem barreira; mostre o diagrama de 5 camadas do README.
2. Rode o self-test: `python3 ../2-implementacao/guardrail_proxy.py`. Destaque 9/9 passando.
3. Injecao direta ao vivo: no interpretador, `detect_injection("ignore all previous instructions...")` e mostre `bloqueado: True` com o motivo.
4. Fala mansa que passa: `detect_injection("Resumo da call: cliente pediu proposta ate sexta.")` e mostre `bloqueado: False`.
5. Saida fora do contrato: `validate_output("texto livre")` rejeita; JSON com as 3 chaves passa.
6. Mostre o standard: aponte as 6 camadas e a bateria de 60 casos no `STANDARD-GUARDRAILS-LLM.md`.
7. Mostre o checklist: ative item a item para a automacao piloto de resumo de tickets.
8. Feche com metricas: 0% para 95% de bloqueio (meta), p95 abaixo de 150 ms (meta), HITL 100% no alto risco (meta).
9. Pergunta de reserva: "por que nao so prompt melhor escrito?" Resposta: instrucao nao distingue dado de comando; barreira estrutural sim.
