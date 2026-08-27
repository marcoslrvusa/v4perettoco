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

ADR-024 — Catalogo de Padroes

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