# Roteiro de Domínio: Atividade 4, Observabilidade e Logs n8n-CRM

Perguntas que um coordenador faria no presencial, com respostas curtas para estudo.

## 1. Por que log estruturado com painel SQL em vez de APM pago?
Pela decisão ADR-011: log JSON com trace_id mais painel SQL e simples e sem custo, com consulta manual como tradeoff. Contador no n8n foi rejeitado por falta de contexto e Datadog ficou como evolução futura.

## 2. O que o trace_id resolve na prática?
Liga trigger, execução e escrita no CRM com cobertura de 100%. Sem ele, cada nó loga de um jeito e é impossível correlacionar timeout, 401 ou limite ao registro afetado. Com ele, o painel correlaciona por trace_id em menos de 1 min.

## 3. Como o barramento trata conflito entre 4 CRMs?
Com fan-out para 3 assinantes e last-write-wins por trace_id mais timestamp, com log auditável e rollback via trace_store. Falha em 1 CRM usa retry de 3x com backoff sem bloquear os demais, com normalização previa e descarte quando falta e-mail.

## 4. Quando o alerta dispara e como evitar ruído e PII no log?
Quando a taxa de erro por CRM passa de 2% em 5 min, com envio ao Slack. Ruído e controlado com nível e amostragem e PII e mascarada em e-mail e CNPJ.

## 5. Qual e o plano de rollout e o ganho esperado?
Piloto em 1 integração por 1 semana medindo MTTR, depois expansão para 12 integrações via template. A meta e sair de detecção em dias para menos de 15 min, de 0% para 100% de visibilidade e de 50h para cerca de 1h por semana, mirando 99% com fonte única e zero disparo duplicado.
