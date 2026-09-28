# Demo Script | A4 Trilhas de auditoria

Duração: 10 min. Pre-requisito: `python3` disponível e `audit_logger.py` na pasta `2-implementacao/`.

1. Abra com a tese (30s): incidente sem trilha vira versões conflitantes; mostre as 4 etapas do README.
2. Rode o self-test: `python3 ../2-implementacao/audit_logger.py`. Destaque cadeia integra e adulteração detectada na linha 4.
3. Mostre um evento real no JSONL: ts UTC, ator, ação, alvo, resultado, hash_prev.
4. Simule a pergunta de incidente: "quem pausou a campanha 77 e quando?" Responda filtrando o log.
5. Mostre o `verify` no CI: qualquer edição quebra o encadeamento e o build acusa.
6. Mostre o standard: 6 campos, retenção 90 dias mais 5 anos, mapeamento NIST CSF por função.
7. Mostre o checklist aplicado ao workflow de disparo de campanha.
8. Feche com métricas: 0 de 3 para 3 de 3 críticos com trilha (meta), reconstrução em até 30 min (meta), 6 de 6 campos (meta).
9. Pergunta de reserva: "por que não logar tudo, incluindo payload?" Resposta: payload tem segredo e PII; evento leva referência e a fonte completa e cruzada sob controle, senão o log vira o vazamento.
