# Roteiro de Domínio | A4 Trilhas de auditoria

## P1: O que registra cada evento?
Os 6 obrigatórios: quando (UTC ISO 8601), quem, o que, onde, resultado e hash do anterior. Detalhe extra sem segredo e sem PII bruta, só referência.

## P2: Como prova que ninguém mexeu no log?
Hash SHA-256 encadeado: cada evento carrega o hash do anterior e o `verify` recalcula tudo. Edição ou remoção quebra a cadeia e o CI acusa a linha.

## P3: Quanto tempo guardar?
90 dias quente para resposta rápida e 5 anos frio imutável para auditoria. Apagar antes do prazo só com exceção formal aprovada.

## P4: Onde entra o NIST CSF 2.0?
Como linguagem comum: Govern define a política, Protect garante integridade, Detect usa os alertas, Respond reconstrui o incidente, Recover lista o que refazer. Cada workflow crítico mapeado uma vez.

## P5: Trilha substitui monitoramento?
Não: monitoramento alerta em tempo real, trilha prova depois do fato. Um detecta, a outra sustenta a resposta, a cobrança e a auditoria.
