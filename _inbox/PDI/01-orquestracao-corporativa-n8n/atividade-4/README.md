# Observabilidade e Logs de Sincronização n8n-CRM

Orquestração Corporativa (n8n)

## Resumo Executivo

Esta atividade institui um contrato de observabilidade para todas as integrações n8n->CRM da operação. O objetivo não é 'ter logs', e sim reduzir o MTTR de falhas de sincronização de dias para minutos e criar um sinal proativo que protege a experiência do cliente antes da reclamação.

O contrato e: todo erro de sync gera evento estruturado com trace_id, painel SQL de correlação e alerta em < 1 min.

## Contexto de Produção

- n8n orquestra 12 integrações com 4 CRMs diferentes.

- Hoje o erro de sincronização só aparece quando o cliente reclama (dias depois).

- Sem trace_id: impossível correlacionar uma falha de API ao registro afetado.

## O Problema e o Blast Radius

Uma falha de API no CRM (timeout/401/limite) faz o nó n8n falhar silenciosamente ou marcar registro como 'ok' sem confirmar. O lead some do funil sem ninguém saber.

| Falha | Hoje | Com contrato |

| --- | --- | --- |

| Detecção | reclamação (dias) | < 1 min |

| Correlação registro->causa | manual | trace_id |

| Visibilidade por CRM | 0% | 100% |

## Diagnóstico e Causa Raiz

- Ausência de padrão de log nas saídas do n8n (cada nó loga diferente).

- Sem ID de correlação entre trigger, execução e escrita no CRM.

- Sem SLO de sincronização -> nada alerta.

## Decisão Arquitetural (ADR)

ADR-011: Log estruturado + painel + alerta, não APM caro.

| Opção | Pro | Contra | Decisão |

| --- | --- | --- | --- |

| Log estruturado + painel SQL | simples, sem custo | consulta manual | ESCOLHIDA |

| APM (Datadog) | rico | custo + setup | futuro |

| Contador no n8n | zero | sem contexto | rejeitada |

> **Nota:** Não precisa de stack APM para ter observabilidade de negócio; um log JSON + view SQL já reduz MTTR drasticamente.

## Entregas desta Atividade

- STANDARD-OBSERVABILITY-LOGS.md: contrato de log (schema + níveis).

- observability_dashboard.sql: view de correlação por trace_id.

- exemplo de nó n8n com log estruturado (trecho).

## Plano de Validação e Rollout

1. Aplicar o padrão em 1 integração (piloto) por 1 semana.

2. Medir MTTR antes/depois (alvo: de dias para < 15 min).

3. Expandir para as 12 integrações via template de nó.

4. Alerta: taxa de erro por CRM > 2% em 5 min -> Slack.

## Métricas e SLO

| SLO | Alvo |

| --- | --- |

| Taxa de erro por CRM (5 min) | <= 2% |

| MTTR de falha de sync | < 15 min |

| Cobertura de trace_id | 100% |

## Riscos e Mitigações

| Risco | Mitigação |

| --- | --- |

| Log vira ruído | nível + amostragem |

| PII no log | mascarar e-mail/cnpj |

## Próximos Passos

- Tracing distribuído (OTel) quando houver orquestração multi-servico.

- SLO de negócio por cliente.

## Decisões e tradeoffs

1. Log estruturado JSON com trace_id mais painel SQL em vez de APM pago como Datadog (ADR-011): solução simples e sem custo, com consulta manual como tradeoff. Contador interno no n8n foi rejeitado por falta de contexto e o APM ficou como evolução futura.
2. trace_id com cobertura de 100% e correlação por view em vez de log solto por nó: liga trigger, execução e escrita no CRM. O tradeoff é exigir injetar trace_id e timestamp em todo evento e normalizar campos (e-mail em minúsculo, telefone em E.164), com descarte quando falta e-mail.
3. Barramento com fan-out para 3 CRMs e last-write-wins por trace_id mais timestamp em vez de cópia manual: conflito vira log auditável com rollback via trace_store. O tradeoff é que o último write vence mesmo se o dado anterior era melhor, compensado pelo rastro completo.
4. Isolamento de falha com retry de 3x e backoff por CRM em vez de travar o barramento: falha em 1 CRM não bloqueia os outros. O tradeoff é aceitar consistência eventual temporária entre os CRMs.
5. Alerta por taxa de erro por CRM acima de 2% em 5 min para o Slack, com piloto em 1 integração por 1 semana antes de expandir para 12: evita ruído com nível e amostragem e protege PII com máscara de e-mail e CNPJ. O tradeoff é que o piloto curto pode não capturar sazonalidade, mas reduz risco de rollout.

## Impacto no negócio

Hoje 12 integrações com 4 CRMs só mostram erro quando o cliente reclama, dias depois, com lead duplicado (3 e-mails e 2 telefones), disparo duplo e retrabalho de cerca de 50h por semana em conciliação manual. Com contrato de log, painel por trace_id e alerta em menos de 1 min, a meta e MTTR abaixo de 15 min, visibilidade de 0% para 100% por CRM e retrabalho de 50h para cerca de 1h por semana, mirando 99% dos leads com fonte única e zero disparo duplicado. Isso corta custo operacional direto e risco reputacional de spam.

## Referências de estudo

- Curso: Observabilidade na Prática, logs, métricas e traces, na Alura.
- Vídeo: Distributed Tracing Explained, trace_id e correlação, no YouTube, canal CNCF.
- Doc: n8n Docs, Logging and observability, na plataforma n8n Docs.
- Doc: PostgreSQL Docs, Views and JSON functions, na plataforma PostgreSQL Docs.
