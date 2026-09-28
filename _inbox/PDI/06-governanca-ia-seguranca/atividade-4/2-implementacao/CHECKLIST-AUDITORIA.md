# CHECKLIST-AUDITORIA | Cobertura por workflow

Marcar por workflow crítico. Dono: dono do workflow.

- [ ] 6 campos obrigatórios em todo evento (ts UTC, ator, ação, alvo, resultado, hash_prev)
- [ ] `detalhe` sem segredo e sem PII bruta (id ou hash como referência)
- [ ] Log append-only com hash encadeado (`audit_logger.py`) e `verify` passando no CI
- [ ] Armazenamento separado do sistema auditado, leitura restrita
- [ ] Retenção aplicada: 90 dias quente + 5 anos frio imutável
- [ ] Restauração de backup testada no semestre
- [ ] Revisão semanal de `bloqueado` e `erro`; revisão mensal com o dono
- [ ] Workflow mapeado numa função do NIST CSF 2.0 e no relatório trimestral
