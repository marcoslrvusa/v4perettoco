# Mapeamento de Dominios com Domain-Driven Design (DDD)

Engenharia de Software

## Resumo Executivo

Mapeamento dos dominios da empresa em DDD antes de novas codificacoes: bounded contexts, agregados, linguagem ubíqua e eventos de dominio. Entrego o mapa, modelos e um exemplo de invariante de agregado.

O objetivo e eliminar modelos duplicados e linguagem inconsistente entre squads.

## Contexto de Producao

- 4 squads tocam dados de Lead/Conta/agente sem vocabulario comum.

- Mesma entidade 'Contato' tem 3 modelos diferentes.

- Novas features recriam agregados ja existentes.

## Diagnostico e Causa Raiz

- Ausencia de bounded contexts -> tudo vira 'tabela unica'.

- Linguagem ubíqua ausente -> 'lead' significa 3 coisas.

- Sem agregado -> regras de consistencia espalhadas.

## Decisao Arquitetural (ADR)

ADR-023 — Mapa de Dominios

| Opcao | Pro | Contra | Decisao |

| --- | --- | --- | --- |

| DDD explicito | consistencia, linguagem | governanca | ESCOLHIDA |

| Schema unico | simples | acopla squads | rejeitada |

> **Nota:** Cada bounded context tem seu modelo; integracao por eventos de dominio.

## Entregas desta Atividade

- DOMAIN-MAP.md.

- domain_models.py — agregados com invariantes.

- domain_events.py — eventos.

## Plano de Validacao

1. Workshop de linguagem ubíqua com Product + 2 squads.

2. Validar agregados contra 3 user stories.

3. Gerar schemas dos agregados aprovados.

## Metricas e SLO

| SLO | Alvo |

| --- | --- |

| Dominios mapeados | 4 |

| Modelos duplicados | 0 |

| Eventos definidos | >= 6 |

## Riscos e Mitigacoes

| Risco | Mitigacao |

| --- | --- |

| Mapa vira teoria | code review exige mapear |

| Over-engineering | so modelar o que tem regra |

## Proximos Passos

- Adotar eventos no barramento (05-A1).

- Testes de invariante de agregado.