# Deck PDI: Observabilidade e Logs de Sincronização n8n-CRM

Área: Orquestração Corporativa (n8n)

## Slide 1: Resumo Executivo
Esta atividade institui um contrato de observabilidade para todas as integrações n8n->CRM da operação. O objetivo não é 'ter logs', e sim reduzir o MTTR de falhas de sincronização de dias para minutos e criar um sinal proativo que protege a experiência do cliente antes da reclamação.
O contrato e: todo erro de sync gera evento estruturado com trace_id, painel SQL de correlação e alerta em < 1 min.
## Slide 2: Contexto de Produção
n8n orquestra 12 integrações com 4 CRMs diferentes.
Hoje o erro de sincronização só aparece quando o cliente reclama (dias depois).
Sem trace_id: impossível correlacionar uma falha de API ao registro afetado.
## Slide 3: O Problema e o Blast Radius
Uma falha de API no CRM (timeout/401/limite) faz o nó n8n falhar silenciosamente ou marcar registro como 'ok' sem confirmar. O lead some do funil sem ninguém saber.
| Falha | Hoje | Com contrato |
| --- | --- | --- |
| Detecção | reclamação (dias) | < 1 min |
| Correlação registro->causa | manual | trace_id |
| Visibilidade por CRM | 0% | 100% |
## Slide 4: Diagnóstico e Causa Raiz
Ausência de padrão de log nas saídas do n8n (cada nó loga diferente).
Sem ID de correlação entre trigger, execução e escrita no CRM.
Sem SLO de sincronização -> nada alerta.
## Slide 5: Decisão Arquitetural (ADR)
ADR-011: Log estruturado + painel + alerta, não APM caro.
| Opção | Pro | Contra | Decisão |
| --- | --- | --- | --- |
| Log estruturado + painel SQL | simples, sem custo | consulta manual | ESCOLHIDA |
| APM (Datadog) | rico | custo + setup | futuro |
| Contador no n8n | zero | sem contexto | rejeitada |
> Nota: Não precisa de stack APM para ter observabilidade de negócio; um log JSON + view SQL já reduz MTTR drasticamente.
## Slide 6: Entregas desta Atividade
STANDARD-OBSERVABILITY-LOGS.md: contrato de log (schema + níveis).
observability_dashboard.sql: view de correlação por trace_id.
exemplo de nó n8n com log estruturado (trecho).
## Slide 7: Plano de Validação e Rollout
Aplicar o padrão em 1 integração (piloto) por 1 semana.
Medir MTTR antes/depois (alvo: de dias para < 15 min).
Expandir para as 12 integrações via template de nó.
Alerta: taxa de erro por CRM > 2% em 5 min -> Slack.
## Slide 8: Métricas e SLO
| SLO | Alvo |
| --- | --- |
| Taxa de erro por CRM (5 min) | <= 2% |
| MTTR de falha de sync | < 15 min |
| Cobertura de trace_id | 100% |
## Slide 9: Riscos e Mitigações
| Risco | Mitigação |
| --- | --- |
| Log vira ruído | nível + amostragem |
| PII no log | mascarar e-mail/cnpj |
## Slide 10: Próximos Passos
Tracing distribuído (OTel) quando houver orquestração multi-servico.
SLO de negócio por cliente.