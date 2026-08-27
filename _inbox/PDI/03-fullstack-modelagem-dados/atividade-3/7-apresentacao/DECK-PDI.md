# Deck PDI — Arquitetura Serverless para Processamento Assincrono (event-driven)

Area: Arquitetura Full Stack

## Slide 1: Resumo Executivo
Desenho serverless event-driven para processar uploads e webhooks sem servidor sempre ligado: fila + funcao + armazenamento, com backpressure e retries. Entrego o padrao e um handler real.
Valor: custo por uso + escala automatica sob rajada.
## Slide 2: Contexto de Producao
Clientes enviam planilhas de 1k-50k linhas.
Worker always-on: 90% ocioso.
Pico de 200 uploads derrubava o worker.
## Slide 3: O Problema
| Hoje | Alvo |
| --- | --- |
| worker ocioso | scale to zero |
| sem fila | queue + retry |
| sem isolamento | 1 falha nao derruba |
## Slide 4: Diagnostico
Processamento sincrono no request = timeout.
Sem idempotencia: reprocessar duplicava leads.
Sem limite de concorrencia.
## Slide 5: Decisao Arquitetural (ADR)
ADR-033 — Serverless event-driven
| Opcao | Pro | Contra | Decisao |
| --- | --- | --- | --- |
| Fila + funcao + store | scale to zero | cold start | ESCOLHIDA |
| Lambda direto no upload | simples | sem backpressure | rejeitada |
> Nota: Upload grava objeto e publica evento; consumo com concorrencia limitada e dedup.
## Slide 6: Entregas
SERVERLESS-STANDARD.md.
process_upload.py.
terraform_serverless.tf.
## Slide 7: Validacao
Enviar 200 planilhas; medir paralelismo e custo.
Forcar falha parcial; confirmar retry + sem duplicata.
1 arquivo ruim nao afeta os outros.
## Slide 8: Metricas e SLO
| SLO | Alvo |
| --- | --- |
| Custo/1k planilhas | < R$ 0,20 |
| P95 | < 60 s |
| Duplicatas | 0 |
## Slide 9: Riscos
| Risco | Mitigacao |
| --- | --- |
| Cold start | provisioned concurrency |
| Fila sem limite | DLQ |
## Slide 10: Proximos Passos
Observabilidade por trace_id.
Workers de agentes no mesmo molde.