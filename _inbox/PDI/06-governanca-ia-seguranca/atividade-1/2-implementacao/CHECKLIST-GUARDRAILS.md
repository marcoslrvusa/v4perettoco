# CHECKLIST-GUARDRAILS | Ativação por automação

Marcar por automação antes de ir a produção. Dono: responsável pelo fluxo.

- [ ] Entradas não confiáveis identificadas e delimitadas (`sanitize`, teto de 4.000 caracteres)
- [ ] System prompt com precedência escrita e proibição de revelar instruções
- [ ] `detect_injection` ligado na entrada (regras + caminho para Moderation/HITL no duvidoso)
- [ ] Contrato de saída declarado e `validate_output` ligado (chaves fixas, sem HTML ativo)
- [ ] Ferramentas de escrita atrás de allowlist de parâmetros e HITL
- [ ] `safety_identifier` com hash do usuário/sessão em toda chamada (sem PII em claro)
- [ ] Bateria de 60 casos rodada em staging com bloqueio de ao menos 95%
- [ ] Bloqueios e decisões indo para a trilha de auditoria (atividade 4)
