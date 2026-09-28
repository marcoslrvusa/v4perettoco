# Refatoração de Módulo Legado com SOLID e Clean Architecture

Engenharia de Software

## Resumo Executivo

Refatoração do módulo de orquestração de campanhas (antigo CampaignService, 600+ linhas, acoplado) para Clean Architecture com ports/adapters e os 5 princípios SOLID. Entrego o antes/depois, o ADR e um teste que prova a nova testabilidade.

O ponto não é 'estilo': é eliminar classes de risco (SQL injection, transações ausentes, falha silenciosa de CRM) e tornar o módulo coberto por teste sem subir infra.

## Contexto de Produção

- O módulo dispara 3-5 campanhas/dia para listas de 5k-80k leads.

- Falha silenciosa de gravação no CRM já causou duplo contato (reclamação real).

- Qualquer alteração hoje exige deploy manual e testes manuais.

## O Problema e o Blast Radius

O CampaignService original misturava regra de negócio, acesso direto a banco, envio de e-mail e chamada de CRM no mesmo método.

| Violação | Manifestação |

| --- | --- |

| SRP | 1 classe cuida de regra+DB+email+CRM |

| OCP | novo canal = editar método central |

| DIP | aplicação depende de psycopg2/smtp direto |

| Sem transação | estado parcial em falha |

## Diagnóstico e Causa Raiz

- SQL concatenado (f"SELECT ... {camp.id}"): vetor de injection.

- Sem transação: lead marcado enviado mas e-mail falha -> estado inconsistente.

- Impossível testar: 600 linhas, 4 dependências de I/O acopladas, 0% cobertura.

## Decisão Arquitetural (ADR)

ADR-021: Camadas e Ports/Adapters

| Opção | Pro | Contra | Decisão |

| --- | --- | --- | --- |

| Clean Architecture | testável, desacoplado | mais arquivos | ESCOLHIDA |

| Hexagonal puro | simétrico | overhead | rejeitada |

| Manter acoplado + E2E | zero refactor | frágil | rejeitada |

> **Nota:** Dependência de I/O vira interface (Protocol): LeadRepository, Notifier, Logger. O serviço depende de abstrações; implementações são injetadas no bootstrap.

## Entregas desta Atividade

- SOLID-BEFORE-AFTER.md: mapeamento violacao->solução.

- before_campaign_service.py: módulo legado.

- after_campaign_service.py: Clean Architecture + 1 teste.

## Plano de Validação e Rollout

1. Cobrir o serviço com testes de porta (mock de Notifier/Repository): alvo 85%.

2. Feature flag: novo módulo em paralelo por 1 sprint (shadow).

3. Se divergência < 0,1%, migrar tráfego e remover legado.

4. Rollback: flag desliga o novo sem deploy.

## Métricas e SLO

| Métrica | Antes | Depois |

| --- | --- | --- |

| Acoplamento (resp/classe) | 4 | 1 |

| Cobertura | 0% | >= 85% |

| Linhas por classe | 600+ | < 45 |

| SQL injection | sim | eliminado |

## Riscos e Mitigações

| Risco | Mitigação |

| --- | --- |

| Shadow com divergência | reconciliação diária |

| Time não adota | PR template + lint de arquitetura |

## Próximos Passos

- Aplicar o molde aos demais módulos legados.

- Mutation testing (mutmut) no serviço.
## Decisões e tradeoffs
- Clean Architecture escolhida sobre hexagonal puro e manter acoplado com E2E: testabilidade com ports desacoplados compensa o custo de mais arquivos, como registra o ADR-021.
- Dependências de I/O como Protocol (LeadRepository, Notifier, Logger) com injeção no bootstrap: o serviço passa a depender de abstrações e o teste usa FakeRepo sem subir infra.
- Rollout em shadow por 1 sprint com reconciliação diária e corte em divergência menor que 0,1 por cento, em vez de cutover direto: compara o módulo novo com o legado de 600 linhas sem expor listas de 5k a 80k leads a estado parcial.
- Meta de cobertura de 85 por cento nos testes de porta com mocks, em vez de teste manual: o legado tinha 0 por cento de cobertura e 4 dependências de I/O acopladas, então o gate quantitativo impede regressão silenciosa.
- Classes menores que 45 linhas com 1 responsabilidade por classe, aceitando mais arquivos: elimina SQL concatenado, falta de transação e falha silenciosa de CRM que já causou duplo contato.

## Impacto no negócio

O módulo dispara 3 a 5 campanhas por dia para listas de 5k a 80k leads, então cada falha silenciosa vira duplo contato e reclamação real. Sair de 600 linhas com 0 por cento de cobertura para classes menores que 45 linhas com alvo de 85 por cento reduz o tempo de alteração de deploy manual com teste manual para validação automática, baixa o risco de SQL injection e estado parcial sem transação, e evita o custo de hotfix em base grande com rollback simples por feature flag.

## Referências de estudo
- Curso: Clean Architecture e SOLID com Python, na Alura.
- Vídeo: SOLID em código Python na prática, no YouTube.
- Doc oficial: Documentação do Python sobre Protocol e tipagem estrutural, em docs.python.org.
- Doc oficial: Documentação do pytest sobre fixtures e mocks, em docs.pytest.org.
