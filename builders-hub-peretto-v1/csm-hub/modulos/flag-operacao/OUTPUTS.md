# OUTPUTS — Flag Operação V1

## Output: Diagnóstico de operação travada

**Input:** "Sprint do cliente B2B SaaS atrasada 5 dias. Sem FCA aberta. GT não atualizou timesheet."

```
DIAGNÓSTICO — B2B SaaS — Operação Travada

SINTOMAS:
Sprint atrasada: 5 dias (threshold: 3) ❌
FCA aberta: não ❌
Timesheet GT: zerado essa semana ❌

NÍVEL: 2 — Estrutural
Múltiplos sintomas simultâneos sem registro = falha de processo,
não de pessoa.

CAUSA PROVÁVEL:
Sprint foi montada sem handoff claro do AM para o GT.
GT não sabia exatamente o que era prioridade.
Resultado: tudo parado, nada registrado.

PLANO DE DESBLOQUEIO:

AÇÃO IMEDIATA (CSM → Coordenador agora):
"[Coordenador], operação travada no B2B SaaS — Nível 2.

Sprint 5 dias atrasada, sem FCA, timesheet zerado.
Causa provável: handoff AM→GT sem clareza de prioridade.

Preciso que você: conduza alinhamento de sprint com GT e AM hoje.
Impacto: entrega da semana não acontece se não resolver até amanhã."

APÓS RESOLUÇÃO:
FCA a ser aberta pelo AM documentando o que travou e como foi resolvido.
Ajuste no processo de handoff para próxima sprint.

SLA: 48h para desbloqueio. Se não resolver → escala para gerência.
```
