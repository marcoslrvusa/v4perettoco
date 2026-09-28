# CHECKLIST-AUDITORIA | Cobertura por workflow

Marcar por workflow critico. Dono: dono do workflow.

- [ ] 6 campos obrigatorios em todo evento (ts UTC, ator, acao, alvo, resultado, hash_prev)
- [ ] `detalhe` sem segredo e sem PII bruta (id ou hash como referencia)
- [ ] Log append-only com hash encadeado (`audit_logger.py`) e `verify` passando no CI
- [ ] Armazenamento separado do sistema auditado, leitura restrita
- [ ] Retencao aplicada: 90 dias quente + 5 anos frio imutavel
- [ ] Restauracao de backup testada no semestre
- [ ] Revisao semanal de `bloqueado` e `erro`; revisao mensal com o dono
- [ ] Workflow mapeado numa funcao do NIST CSF 2.0 e no relatorio trimestral
