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

ADR-023: Mapa de Dominios

| Opcao | Pro | Contra | Decisao |

| --- | --- | --- | --- |

| DDD explicito | consistencia, linguagem | governanca | ESCOLHIDA |

| Schema unico | simples | acopla squads | rejeitada |

> **Nota:** Cada bounded context tem seu modelo; integracao por eventos de dominio.

## Entregas desta Atividade

- DOMAIN-MAP.md.

- domain_models.py: agregados com invariantes.

- domain_events.py: eventos.

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
## Decisoes e tradeoffs
- DDD explicito escolhido sobre schema unico: consistencia e linguagem comum compensam o custo de governanca, enquanto tabela unica acopla os 4 squads.
- Cada bounded context tem seu modelo e a integracao ocorre por eventos de dominio: evita que a entidade Contato continue com 3 modelos diferentes e que regra de um squad vaze para outro.
- So modelar o que tem regra de consistencia, com agregado de raiz unica e filhos sem identidade publica: previne over-engineering e concentra esforco onde ha invariante real.
- Validacao em workshop de linguagem ubiqua com Product e 2 squads contra 3 user stories antes de gerar schemas: garante que o mapa reflete o negocio e nao vira teoria.
- Anti-corruption layer na fronteira entre contextos: traduz o modelo vizinho sem poluir o contexto local, em vez de SQL cruzado entre dominios.

## Impacto no negocio

Com 4 squads tocando Lead, Conta e agente sem vocabulario comum e 3 modelos diferentes de Contato, cada feature recria agregados e cada mudanca tem efeito cascata. Mapear 4 dominios com 0 modelos duplicados e ao menos 6 eventos definidos troca retrabalho e acoplamento oculto por fronteiras claras, reduz o tempo de impacto de alteracoes e evita o custo de carregar regra inconsistente para novas codificacoes.

## Referencias de estudo
- Curso: Domain-Driven Design do zero, na Alura.
- Video: Bounded contexts e linguagem ubiqua na pratica, no YouTube.
- Doc oficial: Domain-Driven Design Reference, de Eric Evans, em domainlanguage.com.
- Doc oficial: Documentacao do Python sobre dataclasses para modelar agregados e eventos, em docs.python.org.
