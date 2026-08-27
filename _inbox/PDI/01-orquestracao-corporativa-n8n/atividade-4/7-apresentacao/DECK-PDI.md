# Deck PDI — Observabilidade e Logs de Sincronizacao n8n-CRM

Area: Orquestracao Corporativa (n8n)

## Slide 1: Resumo Executivo
Esta atividade institui um contrato de observabilidade para todas as integracoes n8n->CRM da operacao. O objetivo nao e 'ter logs', e sim reduzir o MTTR de falhas de sincronizacao de dias para minutos e criar um sinal proativo que protege a experiencia do cliente antes da reclamacao.
O contrato e: todo erro de sync gera evento estruturado com trace_id, painel SQL de correlacao e alerta em < 1 min.
## Slide 2: Contexto de Producao
n8n orquestra 12 integracoes com 4 CRMs diferentes.
Hoje o erro de sincronizacao so aparece quando o cliente reclama (dias depois).
Sem trace_id: impossivel correlacionar uma falha de API ao registro afetado.
## Slide 3: O Problema e o Blast Radius
Uma falha de API no CRM (timeout/401/limite) faz o no n8n falhar silenciosamente ou marcar registro como 'ok' sem confirmar. O lead some do funil sem ninguem saber.
| Falha | Hoje | Com contrato |
| --- | --- | --- |
| Deteccao | reclamacao (dias) | < 1 min |
| Correlacao registro->causa | manual | trace_id |
| Visibilidade por CRM | 0% | 100% |
## Slide 4: Diagnostico e Causa Raiz
Ausencia de padrao de log nas saidas do n8n (cada no loga diferente).
Sem ID de correlacao entre trigger, execucao e escrita no CRM.
Sem SLO de sincronizacao -> nada alerta.
## Slide 5: Decisao Arquitetural (ADR)
ADR-011 — Log estruturado + painel + alerta, nao APM caro.
| Opcao | Pro | Contra | Decisao |
| --- | --- | --- | --- |
| Log estruturado + painel SQL | simples, sem custo | consulta manual | ESCOLHIDA |
| APM (Datadog) | rico | custo + setup | futuro |
| Contador no n8n | zero | sem contexto | rejeitada |
> Nota: Nao precisa de stack APM para ter observabilidade de negocio; um log JSON + view SQL ja reduz MTTR drasticamente.
## Slide 6: Entregas desta Atividade
STANDARD-OBSERVABILITY-LOGS.md — contrato de log (schema + niveis).
observability_dashboard.sql — view de correlacao por trace_id.
exemplo de no n8n com log estruturado (trecho).
## Slide 7: Plano de Validacao e Rollout
Aplicar o padrao em 1 integracao (piloto) por 1 semana.
Medir MTTR antes/depois (alvo: de dias para < 15 min).
Expandir para as 12 integracoes via template de no.
Alerta: taxa de erro por CRM > 2% em 5 min -> Slack.
## Slide 8: Metricas e SLO
| SLO | Alvo |
| --- | --- |
| Taxa de erro por CRM (5 min) | <= 2% |
| MTTR de falha de sync | < 15 min |
| Cobertura de trace_id | 100% |
## Slide 9: Riscos e Mitigacoes
| Risco | Mitigacao |
| --- | --- |
| Log vira ruido | nivel + amostragem |
| PII no log | mascarar e-mail/cnpj |
## Slide 10: Proximos Passos
Tracing distribuido (OTel) quando houver orquestracao multi-servico.
SLO de negocio por cliente.