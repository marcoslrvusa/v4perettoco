# Refatoracao de Modulo Legado com SOLID e Clean Architecture

Engenharia de Software

## Resumo Executivo

Refatoracao do modulo de orquestracao de campanhas (antigo CampaignService, 600+ linhas, acoplado) para Clean Architecture com ports/adapters e os 5 principios SOLID. Entrego o antes/depois, o ADR e um teste que prova a nova testabilidade.

O ponto nao e 'estilo': e eliminar classes de risco (SQL injection, transacoes ausentes, falha silenciosa de CRM) e tornar o modulo coberto por teste sem subir infra.

## Contexto de Producao

- O modulo dispara 3-5 campanhas/dia para listas de 5k-80k leads.

- Falha silenciosa de gravacao no CRM ja causou duplo contato (reclamacao real).

- Qualquer alteracao hoje exige deploy manual e testes manuais.

## O Problema e o Blast Radius

O CampaignService original misturava regra de negocio, acesso direto a banco, envio de e-mail e chamada de CRM no mesmo metodo.

| Violacao | Manifestacao |

| --- | --- |

| SRP | 1 classe cuida de regra+DB+email+CRM |

| OCP | novo canal = editar metodo central |

| DIP | aplicacao depende de psycopg2/smtp direto |

| Sem transacao | estado parcial em falha |

## Diagnostico e Causa Raiz

- SQL concatenado (f"SELECT ... {camp.id}") — vetor de injection.

- Sem transacao: lead marcado enviado mas e-mail falha -> estado inconsistente.

- Impossivel testar: 600 linhas, 4 dependencias de I/O acopladas, 0% cobertura.

## Decisao Arquitetural (ADR)

ADR-021 — Camadas e Ports/Adapters

| Opcao | Pro | Contra | Decisao |

| --- | --- | --- | --- |

| Clean Architecture | testavel, desacoplado | mais arquivos | ESCOLHIDA |

| Hexagonal puro | simetrico | overhead | rejeitada |

| Manter acoplado + E2E | zero refactor | fragil | rejeitada |

> **Nota:** Dependencia de I/O vira interface (Protocol): LeadRepository, Notifier, Logger. O servico depende de abstracoes; implementacoes sao injetadas no bootstrap.

## Entregas desta Atividade

- SOLID-BEFORE-AFTER.md — mapeamento violacao->solucao.

- before_campaign_service.py — modulo legado.

- after_campaign_service.py — Clean Architecture + 1 teste.

## Plano de Validacao e Rollout

1. Cobrir o servico com testes de porta (mock de Notifier/Repository) — alvo 85%.

2. Feature flag: novo modulo em paralelo por 1 sprint (shadow).

3. Se divergencia < 0,1%, migrar trafego e remover legado.

4. Rollback: flag desliga o novo sem deploy.

## Metricas e SLO

| Metrica | Antes | Depois |

| --- | --- | --- |

| Acoplamento (resp/classe) | 4 | 1 |

| Cobertura | 0% | >= 85% |

| Linhas por classe | 600+ | < 45 |

| SQL injection | sim | eliminado |

## Riscos e Mitigacoes

| Risco | Mitigacao |

| --- | --- |

| Shadow com divergencia | reconciliacao diaria |

| Time nao adota | PR template + lint de arquitetura |

## Proximos Passos

- Aplicar o molde aos demais modulos legados.

- Mutation testing (mutmut) no servico.