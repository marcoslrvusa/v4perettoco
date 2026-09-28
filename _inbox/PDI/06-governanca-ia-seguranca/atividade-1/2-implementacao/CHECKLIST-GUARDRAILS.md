# CHECKLIST-GUARDRAILS | Ativação por automação

Marcar por automação antes de ir a produção. Dono: responsável pelo fluxo.

Leitura de uso: cada item tem evidência aceitável. Item marcado sem evidência não conta como pronto, e a coordenação da trilha só libera a automação com os oito itens marcados e a evidência anexada ao ticket de ativação.

- [ ] Entradas não confiáveis identificadas e delimitadas (`sanitize`, teto de 4.000 caracteres)
  - Evidência: lista das fontes (formulário, e-mail, página, planilha) e teste automatizado que falha se a chamada a `sanitize` for removida.
  - Critério de falha: qualquer fonte externa chegando ao worker sem delimitador.

- [ ] System prompt com precedência escrita e proibição de revelar instruções
  - Evidência: texto do prompt versionado no repositório com hash registrado.
  - Critério de falha: prompt editado direto em ferramenta de configuração, sem versão.

- [ ] `detect_injection` ligado na entrada (regras + caminho para Moderation/HITL no duvidoso)
  - Evidência: `feature-flag` ligada em produção e motivo de bloqueio visível na trilha.
  - Critério de falha: exceção engolida no caminho de chamada, que faz o fluxo seguir sem detecção.

- [ ] Contrato de saída declarado e `validate_output` ligado (chaves fixas, sem HTML ativo)
  - Evidência: contrato escrito por automação e teste TC-05, TC-06 e TC-07 verdes.
  - Critério de falha: chave extra aceita "para flexibilidade" ou validação só de `json.loads`.

- [ ] Ferramentas de escrita atrás de allowlist de parâmetros e HITL
  - Evidência: nomes e tipos permitidos documentados e reprovação registrada na trilha.
  - Critério de falha: ferramenta chamada com parâmetro livre ou aprovação automática.

- [ ] `safety_identifier` com hash do usuário/sessão em toda chamada (sem PII em claro)
  - Evidência: captura de payload sem e-mail, telefone ou CPF, apenas hash.
  - Critério de falha: identificador enviado em claro ou ausente na chamada.

- [ ] Bateria de 60 casos rodada em staging com bloqueio de ao menos 95%
  - Evidência: placar datado, com versão da bateria e versão do modelo, e caso a caso arquivado.
  - Critério de falha: placar sem data ou reexecução apenas dos casos reprovados.

- [ ] Bloqueios e decisões indo para a trilha de auditoria (atividade 4)
  - Evidência: reconciliação diária casando decisões tomadas com linhas gravadas.
  - Critério de falha: decisão tomada sem registro, inclusive reprovação de HITL.

## Complementos de ativação (mesma revisão)

- [ ] PII mascarada antes do envio ao provedor, com marcador estável para agrupamento.
- [ ] Log sem prompt completo e sem dado pessoal; trecho truncado e mascarado quando existir.
- [ ] Rollback testado por `feature-flag`, sem dependência de deploy para desligar uma regra.
- [ ] Métricas ligadas: p95 do proxy, taxa de bloqueio por motivo, falso positivo e idade da fila de HITL.
- [ ] Alerta configurado para queda de bloqueio a zero (detector desligado) em 15 minutos.
- [ ] Dono nomeado para o fluxo e para a revisão mensal do placar.
- [ ] SLA de aprovação de HITL acordado com quem vai revisar, em minutos ou horas.
- [ ] Retenção da trilha definida e partição antiga marcada para descarte no fim do prazo.
- [ ] Postmortem e ação corretiva rastreáveis definidos caso haja escape confirmado.
- [ ] Plano de reexecução da bateria a cada troca de versão de modelo ou de política.

## O que reprova a ativação

Qualquer um destes casos derruba o pedido, mesmo com os oito itens principais marcados: contrato de saída ausente; ferramenta de escrita sem allowlist; bateria com placar abaixo de 57 de 60; log com dado pessoal; `safety_identifier` em claro; ou `feature-flag` do detector desligada em produção.
