# Deck PDI | A4 Trilhas de auditoria e compliance em workflows

## Slide 1: Tese
Workflow sem rastro confiável deixa incidente sem resposta. Evento padronizado, append-only com hash e retenção em camadas dão reconstrução em minutos.

## Slide 2: Contexto
Disparo de campanha, sync de leads e rotinas de verba executam todo dia sem registrar quem rodou, com que parâmetros e com que resultado.

## Slide 3: Problema
Lote errado sem trilha vira versões conflitantes: sem como reconstruir, sem como provar diligência (NIST CSF, LGPD art. 37), sem como cobrar ferramenta.

## Slide 4: Solução em 4 etapas
Evento com 6 campos, append-only com hash encadeado, retenção quente e fria, consulta para incidente e compliance.

## Slide 5: Standard entregue
`STANDARD-AUDIT-LOG.md`: evento mínimo, propriedades da trilha, retenção 90 dias mais 5 anos, mapeamento NIST CSF 2.0 por função, rotina semanal, mensal e trimestral.

## Slide 6: Código entregue
`audit_logger.py` em Python puro: JSON Lines, SHA-256 encadeado, `verify` que detecta edição e quebra de cadeia. Self-test com 3 eventos e adulteração detectada.

## Slide 7: Demo
Registrar 3 eventos, verificar a cadeia integra, adulterar uma linha e mostrar a detecção com número da linha; aplicar o checklist a um workflow real.

## Slide 8: Espelhos de mercado
CloudTrail: event history de 90 dias, Lake com retenção de anos, trails para S3 e CloudWatch. NIST CSF 2.0: Govern, Identify, Protect, Detect, Respond, Recover. Nossa trilha espelha os dois em escala cabível.

## Slide 9: Métricas
Críticos com trilha: atual 0 de 3 para 3 de 3 (meta). Reconstrução de incidente: sem referência para até 30 min (meta). Campos obrigatórios: atual 0 de 6 para 6 de 6 (meta).

## Slide 10: Tradeoffs assumidos
Arquivo em vez de banco (sem infra, consulta pesada exporta depois); sem segredo e sem PII no evento (reconstrução cruza com a fonte); UTC único exige disciplina; apagar antes do prazo vira exceção formal.

## Slide 11: Próximos passos
Acoplar o logger aos 3 críticos; formalizar retenção e testar restauração; revisar falhas mensalmente e alimentar os guardrails.

## Slide 12: Impacto
Incidente com sequência verificável de fatos: diagnóstico curto, resposta sustentada a cliente e auditor, diligência provada para LGPD e parceiros exigentes.
