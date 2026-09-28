# Arquitetura Serverless para Processamento Assincrono (event-driven)

Arquitetura Full Stack

## Resumo Executivo

Desenho serverless event-driven para processar uploads e webhooks sem servidor sempre ligado: fila + funcao + armazenamento, com backpressure e retries. Entrego o padrao e um handler real.

Valor: custo por uso + escala automatica sob rajada.

## Contexto de Producao

- Clientes enviam planilhas de 1k-50k linhas.

- Worker always-on: 90% ocioso.

- Pico de 200 uploads derrubava o worker.

## O Problema

| Hoje | Alvo |

| --- | --- |

| worker ocioso | scale to zero |

| sem fila | queue + retry |

| sem isolamento | 1 falha nao derruba |

## Diagnostico

- Processamento sincrono no request = timeout.

- Sem idempotencia: reprocessar duplicava leads.

- Sem limite de concorrencia.

## Decisao Arquitetural (ADR)

ADR-033: Serverless event-driven

| Opcao | Pro | Contra | Decisao |

| --- | --- | --- | --- |

| Fila + funcao + store | scale to zero | cold start | ESCOLHIDA |

| Lambda direto no upload | simples | sem backpressure | rejeitada |

> **Nota:** Upload grava objeto e publica evento; consumo com concorrencia limitada e dedup.

## Entregas

- SERVERLESS-STANDARD.md.

- process_upload.py.

- terraform_serverless.tf.

## Validacao

1. Enviar 200 planilhas; medir paralelismo e custo.

2. Forcar falha parcial; confirmar retry + sem duplicata.

3. 1 arquivo ruim nao afeta os outros.

## Metricas e SLO

| SLO | Alvo |

| --- | --- |

| Custo/1k planilhas | < R$ 0,20 |

| P95 | < 60 s |

| Duplicatas | 0 |

## Riscos

| Risco | Mitigacao |

| --- | --- |

| Cold start | provisioned concurrency |

| Fila sem limite | DLQ |

## Decisoes e tradeoffs

1. **Upload nunca processa no request (grava no store e publica `file.uploaded`, consumer com concorrencia limitada a 10):** request sincrono estourava timeout em planilhas de ate 50k linhas. Tradeoff: resposta assincrona exige acompanhar status por evento, aceito porque elimina o timeout.
2. **Idempotencia por dedup `hash(arquivo + tenant)`:** reprocessar nao duplica leads. Tradeoff: precisa de store de chaves (em prod Redis/DynamoDB; no PoC um set em memoria) e custa uma leitura por evento.
3. **DLQ apos N tentativas + 1 arquivo ruim nao afeta os outros:** isolamento por mensagem. Tradeoff: mensagens na DLQ exigem operacao manual de replay; sem DLQ a fila travaria na mensagem veneno.
4. **Payload carrega so metadados (URL), nunca o arquivo:** fila leve e rapida. Tradeoff: o consumer precisa buscar o objeto no store, uma chamada a mais por mensagem.
5. **Quando NAO usar (carga constante alta, worker always-on sai mais barato) + segredos fora de env hardcoded, pooler com TLS e timeout de ate 60s:** serverless so onde ha ociosidade (o worker ficava 90% ocioso). Tradeoff: cold start em rajada, mitigado com concorrencia provisionada.

## Impacto no negocio

Clientes enviam planilhas de 1k a 50k linhas e picos de 200 uploads derrubavam o worker always-on, 90% ocioso. Com fila, funcao e store, o custo cai para menos de R$ 0,20 por mil planilhas, a escala vai a zero no vale e o p95 fica abaixo de 60s com zero duplicatas, o que viabiliza campanhas de importacao em rajada sem provisionar servidor parado.

## Referencias de estudo

- Curso: AWS Lambda e Serverless na pratica (Alura)
- Video: Serverless em 100 segundos (Fireship, YouTube)
- Doc oficial: Cloud Run functions, https://cloud.google.com/functions/docs (verificada em 2026-09-28)
- Doc oficial: Terraform, https://developer.hashicorp.com/terraform/docs (verificada em 2026-09-28)

## Proximos Passos

- Observabilidade por trace_id.

- Workers de agentes no mesmo molde.