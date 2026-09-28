# CHECKLIST-GUARDRAILS | Ativacao por automacao

Marcar por automacao antes de ir a producao. Dono: responsavel pelo fluxo.

- [ ] Entradas nao confiaveis identificadas e delimitadas (`sanitize`, teto de 4.000 caracteres)
- [ ] System prompt com precedencia escrita e proibicao de revelar instrucoes
- [ ] `detect_injection` ligado na entrada (regras + caminho para Moderation/HITL no duvidoso)
- [ ] Contrato de saida declarado e `validate_output` ligado (chaves fixas, sem HTML ativo)
- [ ] Ferramentas de escrita atras de allowlist de parametros e HITL
- [ ] `safety_identifier` com hash do usuario/sessao em toda chamada (sem PII em claro)
- [ ] Bateria de 60 casos rodada em staging com bloqueio de ao menos 95%
- [ ] Bloqueios e decisoes indo para a trilha de auditoria (atividade 4)
