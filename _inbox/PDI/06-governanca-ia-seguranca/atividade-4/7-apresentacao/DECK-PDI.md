# Deck PDI | A4 Trilhas de auditoria e compliance em workflows

## Slide 1: Tese
Workflow sem rastro confiavel deixa incidente sem resposta. Evento padronizado, append-only com hash e retencao em camadas dao reconstrucao em minutos.

## Slide 2: Contexto
Disparo de campanha, sync de leads e rotinas de verba executam todo dia sem registrar quem rodou, com que parametros e com que resultado.

## Slide 3: Problema
Lote errado sem trilha vira versoes conflitantes: sem como reconstruir, sem como provar diligencia (NIST CSF, LGPD art. 37), sem como cobrar ferramenta.

## Slide 4: Solucao em 4 etapas
Evento com 6 campos, append-only com hash encadeado, retencao quente e fria, consulta para incidente e compliance.

## Slide 5: Standard entregue
`STANDARD-AUDIT-LOG.md`: evento minimo, propriedades da trilha, retencao 90 dias mais 5 anos, mapeamento NIST CSF 2.0 por funcao, rotina semanal, mensal e trimestral.

## Slide 6: Codigo entregue
`audit_logger.py` em Python puro: JSON Lines, SHA-256 encadeado, `verify` que detecta edicao e quebra de cadeia. Self-test com 3 eventos e adulteracao detectada.

## Slide 7: Demo
Registrar 3 eventos, verificar a cadeia integra, adulterar uma linha e mostrar a deteccao com numero da linha; aplicar o checklist a um workflow real.

## Slide 8: Espelhos de mercado
CloudTrail: event history de 90 dias, Lake com retencao de anos, trails para S3 e CloudWatch. NIST CSF 2.0: Govern, Identify, Protect, Detect, Respond, Recover. Nossa trilha espelha os dois em escala cabivel.

## Slide 9: Metricas
Criticos com trilha: atual 0 de 3 para 3 de 3 (meta). Reconstrucao de incidente: sem referencia para ate 30 min (meta). Campos obrigatorios: atual 0 de 6 para 6 de 6 (meta).

## Slide 10: Tradeoffs assumidos
Arquivo em vez de banco (sem infra, consulta pesada exporta depois); sem segredo e sem PII no evento (reconstrucao cruza com a fonte); UTC unico exige disciplina; apagar antes do prazo vira excecao formal.

## Slide 11: Proximos passos
Acoplar o logger aos 3 criticos; formalizar retencao e testar restauracao; revisar falhas mensalmente e alimentar os guardrails.

## Slide 12: Impacto
Incidente com sequencia verificavel de fatos: diagnostico curto, resposta sustentada a cliente e auditor, diligencia provada para LGPD e parceiros exigentes.
