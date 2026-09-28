# Estudo de Design Patterns aplicados ao ecossistema

Engenharia de Software

## Resumo Executivo

Conclusão do minicurso de Design Patterns com aplicação prática aos problemas reais da operação. Entrego notas com exemplos funcionais de Adapter, Strategy, Observer e Command.

Entrega de evidência técnica: código que já roda no ecossistema.

## Contexto de Produção

- Código repetitivo em handlers de webhook e workers.

- Sem vocabulário comum: PRs discutem 'àquela classe'.

- Oportunidade de aplicar padrões em agentes.

## Diagnóstico

- Acoplamento a APIs de terceiro espalhado (sem Adapter).

- Seleção de modelo de LLM por if/else (sem Strategy).

- Logs de domínio sem padrão (sem Observer).

## Decisão Arquitetural (ADR)

ADR-024: Catálogo de Padrões

| Padrão | Onde | Decisão |

| --- | --- | --- |

| Adapter | CRM/LLM externos | ESCOLHIDO |

| Strategy | roteamento de modelo | ESCOLHIDO |

| Observer | eventos de domínio | ESCOLHIDO |

| Singleton p/ clients | rejeitado (DI) | NÃO |

## Entregas desta Atividade

- DESIGN-PATTERNS-NOTES.md.

- patterns_demo.py.

- ESTUDO-PLANO.md.

## Validação

1. Rodar patterns_demo.py.

2. PR aplicando Adapter no handler de 1 CRM.

3. Checklist de padrões no template de PR.

## Métricas

| SLO | Alvo |

| --- | --- |

| Handlers com Adapter | >= 1 piloto |

| Padrões documentados | criacionais/estruturais/comportamentais |

## Riscos

| Risco | Mitigação |

| --- | --- |

| Over-engineering | só onde há variação |

| Padrão como fim | code review foca em valor |

## Próximos Passos

- Refatorar handlers de CRM para Adapter.

- Roteamento de modelo via Strategy.
## Decisões e tradeoffs
- Adapter para CRM e LLM externos: isola o acoplamento a APIs de terceiro em tradutores atrás de ports, então novo fornecedor vira um adapter novo sem tocar o core.
- Strategy para roteamento de modelo de LLM e cálculo variável: troca if e else espalhados por estratégias selecionadas em runtime via factory selecionar.
- Observer para eventos de domínio com bus.assinar: reações como e-mail e estoque assinam eventos sem acoplar ao core, aceitando ordem não garantida entre observadores.
- Singleton para clients rejeitado em favor de DI: evita estado global oculto e mantém o core testável com fakes dos ports.
- Padrão aplicado só onde há variação real, com code review focado em valor: evita over-engineering e impede que padrão vire fim em si mesmo.

## Impacto no negócio

Handlers de webhook e workers repetitivos com seleção de modelo por if e else fazem cada onboarding de fornecedor duplicar pontos de falha e travar o time. Com Adapter, Strategy e Observer mais piloto em ao menos 1 CRM, o onboarding cai para até 2 dias atrás de adapter testado, o teste do core usa fake sem chamar terceiro, e o custo de plugar parceiro novo deixa de ser reescrita do fluxo.

## Referências de estudo
- Curso: Design Patterns com Python, na Alura.
- Vídeo: Strategy na prática para trocar if else, no YouTube.
- Doc oficial: Catálogo de padrões com exemplos em Python, em refactoring.guru.
- Doc oficial: Documentação do Python sobre abc e protocolos para ports e adapters, em docs.python.org.
