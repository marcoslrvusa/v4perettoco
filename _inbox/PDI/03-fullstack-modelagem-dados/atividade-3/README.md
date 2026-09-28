# Arquitetura Serverless para Processamento Assíncrono (event-driven)

Arquitetura Full Stack

## Resumo Executivo

Desenho serverless event-driven para processar uploads e webhooks sem servidor sempre ligado: fila + função + armazenamento, com backpressure e retries. Entrego o padrão e um handler real.

Valor: custo por uso + escala automática sob rajada.

## Contexto de Produção

- Clientes enviam planilhas de 1k-50k linhas.

- Worker always-on: 90% ocioso.

- Pico de 200 uploads derrubava o worker.

## O Problema

| Hoje | Alvo |

| --- | --- |

| worker ocioso | scale to zero |

| sem fila | queue + retry |

| sem isolamento | 1 falha não derruba |

## Diagnóstico

- Processamento síncrono no request = timeout.

- Sem idempotência: reprocessar duplicava leads.

- Sem limite de concorrência.

## Decisão Arquitetural (ADR)

ADR-033: Serverless event-driven

| Opção | Pro | Contra | Decisão |

| --- | --- | --- | --- |

| Fila + função + store | scale to zero | cold start | ESCOLHIDA |

| Lambda direto no upload | simples | sem backpressure | rejeitada |

> **Nota:** Upload grava objeto e publica evento; consumo com concorrência limitada e dedup.

## Entregas

- SERVERLESS-STANDARD.md.

- process_upload.py.

- terraform_serverless.tf.

## Validação

1. Enviar 200 planilhas; medir paralelismo e custo.

2. Forcar falha parcial; confirmar retry + sem duplicata.

3. 1 arquivo ruim não afeta os outros.

## Métricas e SLO

| SLO | Alvo |

| --- | --- |

| Custo/1k planilhas | < R$ 0,20 |

| P95 | < 60 s |

| Duplicatas | 0 |

## Riscos

| Risco | Mitigação |

| --- | --- |

| Cold start | provisioned concurrency |

| Fila sem limite | DLQ |

## Decisões e tradeoffs

1. **Upload nunca processa no request (grava no store e publica `file.uploaded`, consumer com concorrência limitada a 10):** request síncrono estourava timeout em planilhas de até 50k linhas. Tradeoff: resposta assíncrona exige acompanhar status por evento, aceito porque elimina o timeout.
2. **Idempotência por dedup `hash(arquivo + tenant)`:** reprocessar não duplica leads. Tradeoff: precisa de store de chaves (em prod Redis/DynamoDB; no PoC um set em memória) e custa uma leitura por evento.
3. **DLQ após N tentativas + 1 arquivo ruim não afeta os outros:** isolamento por mensagem. Tradeoff: mensagens na DLQ exigem operação manual de replay; sem DLQ a fila travaria na mensagem veneno.
4. **Payload carrega só metadados (URL), nunca o arquivo:** fila leve e rápida. Tradeoff: o consumer precisa buscar o objeto no store, uma chamada a mais por mensagem.
5. **Quando NÃO usar (carga constante alta, worker always-on sai mais barato) + segredos fora de env hardcoded, pooler com TLS e timeout de até 60s:** serverless só onde há ociosidade (o worker ficava 90% ocioso). Tradeoff: cold start em rajada, mitigado com concorrência provisionada.

## Impacto no negócio

Clientes enviam planilhas de 1k a 50k linhas e picos de 200 uploads derrubavam o worker always-on, 90% ocioso. Com fila, função e store, o custo cai para menos de R$ 0,20 por mil planilhas, a escala vai a zero no vale e o p95 fica abaixo de 60s com zero duplicatas, o que viabiliza campanhas de importação em rajada sem provisionar servidor parado.

## Referências de estudo

- Curso: AWS Lambda e Serverless na prática (Alura)
- Vídeo: Serverless em 100 segundos (Fireship, YouTube)
- Doc oficial: Cloud Run functions, https://cloud.google.com/functions/docs (verificada em 2026-09-28)
- Doc oficial: Terraform, https://developer.hashicorp.com/terraform/docs (verificada em 2026-09-28)

## Próximos Passos

- Observabilidade por trace_id.

- Workers de agentes no mesmo molde.