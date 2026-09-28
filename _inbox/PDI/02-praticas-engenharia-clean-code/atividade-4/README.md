# Estudo de Design Patterns aplicados ao ecossistema

Engenharia de Software

## Resumo Executivo

Conclusao do minicurso de Design Patterns com aplicacao pratica aos problemas reais da operacao. Entrego notas com exemplos funcionais de Adapter, Strategy, Observer e Command.

Entrega de evidencia tecnica: codigo que ja roda no ecossistema.

## Contexto de Producao

- Codigo repetitivo em handlers de webhook e workers.

- Sem vocabulario comum: PRs discutem 'aquela classe'.

- Oportunidade de aplicar padroes em agentes.

## Diagnostico

- Acoplamento a APIs de terceiro espalhado (sem Adapter).

- Selecao de modelo de LLM por if/else (sem Strategy).

- Logs de dominio sem padrao (sem Observer).

## Decisao Arquitetural (ADR)

ADR-024: Catalogo de Padroes

| Padrao | Onde | Decisao |

| --- | --- | --- |

| Adapter | CRM/LLM externos | ESCOLHIDO |

| Strategy | roteamento de modelo | ESCOLHIDO |

| Observer | eventos de dominio | ESCOLHIDO |

| Singleton p/ clients | rejeitado (DI) | NAO |

## Entregas desta Atividade

- DESIGN-PATTERNS-NOTES.md.

- patterns_demo.py.

- ESTUDO-PLANO.md.

## Validacao

1. Rodar patterns_demo.py.

2. PR aplicando Adapter no handler de 1 CRM.

3. Checklist de padroes no template de PR.

## Metricas

| SLO | Alvo |

| --- | --- |

| Handlers com Adapter | >= 1 piloto |

| Padroes documentados | criacionais/estruturais/comportamentais |

## Riscos

| Risco | Mitigacao |

| --- | --- |

| Over-engineering | so onde ha variacao |

| Padrao como fim | code review foca em valor |

## Proximos Passos

- Refatorar handlers de CRM para Adapter.

- Roteamento de modelo via Strategy.
## Decisoes e tradeoffs
- Adapter para CRM e LLM externos: isola o acoplamento a APIs de terceiro em tradutores atras de ports, entao novo fornecedor vira um adapter novo sem tocar o core.
- Strategy para roteamento de modelo de LLM e calculo variavel: troca if e else espalhados por estrategias selecionadas em runtime via factory selecionar.
- Observer para eventos de dominio com bus.assinar: reacoes como e-mail e estoque assinam eventos sem acoplar ao core, aceitando ordem nao garantida entre observadores.
- Singleton para clients rejeitado em favor de DI: evita estado global oculto e mantem o core testavel com fakes dos ports.
- Padrao aplicado so onde ha variacao real, com code review focado em valor: evita over-engineering e impede que padrao vire fim em si mesmo.

## Impacto no negocio

Handlers de webhook e workers repetitivos com selecao de modelo por if e else fazem cada onboarding de fornecedor duplicar pontos de falha e travar o time. Com Adapter, Strategy e Observer mais piloto em ao menos 1 CRM, o onboarding cai para ate 2 dias atras de adapter testado, o teste do core usa fake sem chamar terceiro, e o custo de plugar parceiro novo deixa de ser reescrita do fluxo.

## Referencias de estudo
- Curso: Design Patterns com Python, na Alura.
- Video: Strategy na pratica para trocar if else, no YouTube.
- Doc oficial: Catalogo de padroes com exemplos em Python, em refactoring.guru.
- Doc oficial: Documentacao do Python sobre abc e protocolos para ports e adapters, em docs.python.org.
