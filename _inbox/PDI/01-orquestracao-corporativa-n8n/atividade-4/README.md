# Observabilidade e Logs de Sincronizacao n8n-CRM

Orquestracao Corporativa (n8n)

## Resumo Executivo

Esta atividade institui um contrato de observabilidade para todas as integracoes n8n->CRM da operacao. O objetivo nao e 'ter logs', e sim reduzir o MTTR de falhas de sincronizacao de dias para minutos e criar um sinal proativo que protege a experiencia do cliente antes da reclamacao.

O contrato e: todo erro de sync gera evento estruturado com trace_id, painel SQL de correlacao e alerta em < 1 min.

## Contexto de Producao

- n8n orquestra 12 integracoes com 4 CRMs diferentes.

- Hoje o erro de sincronizacao so aparece quando o cliente reclama (dias depois).

- Sem trace_id: impossivel correlacionar uma falha de API ao registro afetado.

## O Problema e o Blast Radius

Uma falha de API no CRM (timeout/401/limite) faz o no n8n falhar silenciosamente ou marcar registro como 'ok' sem confirmar. O lead some do funil sem ninguem saber.

| Falha | Hoje | Com contrato |

| --- | --- | --- |

| Deteccao | reclamacao (dias) | < 1 min |

| Correlacao registro->causa | manual | trace_id |

| Visibilidade por CRM | 0% | 100% |

## Diagnostico e Causa Raiz

- Ausencia de padrao de log nas saidas do n8n (cada no loga diferente).

- Sem ID de correlacao entre trigger, execucao e escrita no CRM.

- Sem SLO de sincronizacao -> nada alerta.

## Decisao Arquitetural (ADR)

ADR-011: Log estruturado + painel + alerta, nao APM caro.

| Opcao | Pro | Contra | Decisao |

| --- | --- | --- | --- |

| Log estruturado + painel SQL | simples, sem custo | consulta manual | ESCOLHIDA |

| APM (Datadog) | rico | custo + setup | futuro |

| Contador no n8n | zero | sem contexto | rejeitada |

> **Nota:** Nao precisa de stack APM para ter observabilidade de negocio; um log JSON + view SQL ja reduz MTTR drasticamente.

## Entregas desta Atividade

- STANDARD-OBSERVABILITY-LOGS.md: contrato de log (schema + niveis).

- observability_dashboard.sql: view de correlacao por trace_id.

- exemplo de no n8n com log estruturado (trecho).

## Plano de Validacao e Rollout

1. Aplicar o padrao em 1 integracao (piloto) por 1 semana.

2. Medir MTTR antes/depois (alvo: de dias para < 15 min).

3. Expandir para as 12 integracoes via template de no.

4. Alerta: taxa de erro por CRM > 2% em 5 min -> Slack.

## Metricas e SLO

| SLO | Alvo |

| --- | --- |

| Taxa de erro por CRM (5 min) | <= 2% |

| MTTR de falha de sync | < 15 min |

| Cobertura de trace_id | 100% |

## Riscos e Mitigacoes

| Risco | Mitigacao |

| --- | --- |

| Log vira ruido | nivel + amostragem |

| PII no log | mascarar e-mail/cnpj |

## Proximos Passos

- Tracing distribuido (OTel) quando houver orquestracao multi-servico.

- SLO de negocio por cliente.

## Decisoes e tradeoffs

1. Log estruturado JSON com trace_id mais painel SQL em vez de APM pago como Datadog (ADR-011): solucao simples e sem custo, com consulta manual como tradeoff. Contador interno no n8n foi rejeitado por falta de contexto e o APM ficou como evolucao futura.
2. trace_id com cobertura de 100% e correlacao por view em vez de log solto por no: liga trigger, execucao e escrita no CRM. O tradeoff e exigir injetar trace_id e timestamp em todo evento e normalizar campos (e-mail em minusculo, telefone em E.164), com descarte quando falta e-mail.
3. Barramento com fan-out para 3 CRMs e last-write-wins por trace_id mais timestamp em vez de copia manual: conflito vira log auditavel com rollback via trace_store. O tradeoff e que o ultimo write vence mesmo se o dado anterior era melhor, compensado pelo rastro completo.
4. Isolamento de falha com retry de 3x e backoff por CRM em vez de travar o barramento: falha em 1 CRM nao bloqueia os outros. O tradeoff e aceitar consistencia eventual temporaria entre os CRMs.
5. Alerta por taxa de erro por CRM acima de 2% em 5 min para o Slack, com piloto em 1 integracao por 1 semana antes de expandir para 12: evita ruido com nivel e amostragem e protege PII com mascara de e-mail e CNPJ. O tradeoff e que o piloto curto pode nao capturar sazonalidade, mas reduz risco de rollout.

## Impacto no negocio

Hoje 12 integracoes com 4 CRMs so mostram erro quando o cliente reclama, dias depois, com lead duplicado (3 e-mails e 2 telefones), disparo duplo e retrabalho de cerca de 50h por semana em conciliacao manual. Com contrato de log, painel por trace_id e alerta em menos de 1 min, a meta e MTTR abaixo de 15 min, visibilidade de 0% para 100% por CRM e retrabalho de 50h para cerca de 1h por semana, mirando 99% dos leads com fonte unica e zero disparo duplicado. Isso corta custo operacional direto e risco reputacional de spam.

## Referencias de estudo

- Curso: Observabilidade na Pratica, logs, metricas e traces, na Alura.
- Video: Distributed Tracing Explained, trace_id e correlacao, no YouTube, canal CNCF.
- Doc: n8n Docs, Logging and observability, na plataforma n8n Docs.
- Doc: PostgreSQL Docs, Views and JSON functions, na plataforma PostgreSQL Docs.
