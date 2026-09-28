# Demo Script | A1 Guardrails e anti-prompt-injection

Duração: 10 min. Pre-requisito: `python3` disponível e arquivo `guardrail_proxy.py` na pasta `2-implementacao/`.

1. Abra com a tese (30s): texto externo vira instrução sem barreira; mostre o diagrama de 5 camadas do README.
2. Rode o self-test: `python3 ../2-implementacao/guardrail_proxy.py`. Destaque 9/9 passando.
3. Injeção direta ao vivo: no interpretador, `detect_injection("ignore all previous instructions...")` e mostre `bloqueado: True` com o motivo.
4. Fala mansa que passa: `detect_injection("Resumo da call: cliente pediu proposta até sexta.")` e mostre `bloqueado: False`.
5. Saída fora do contrato: `validate_output("texto livre")` rejeita; JSON com as 3 chaves passa.
6. Mostre o standard: aponte as 6 camadas e a bateria de 60 casos no `STANDARD-GUARDRAILS-LLM.md`.
7. Mostre o checklist: ative item a item para a automação piloto de resumo de tickets.
8. Feche com métricas: 0% para 95% de bloqueio (meta), p95 abaixo de 150 ms (meta), HITL 100% no alto risco (meta).
9. Pergunta de reserva: "por que não só prompt melhor escrito?" Resposta: instrução não distingue dado de comando; barreira estrutural sim.
