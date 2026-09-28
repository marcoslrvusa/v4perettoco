# Mapeamento de Domínios com Domain-Driven Design (DDD)

Engenharia de Software

## Resumo Executivo

Mapeamento dos domínios da empresa em DDD antes de novas codificações: bounded contexts, agregados, linguagem ubíqua e eventos de domínio. Entrego o mapa, modelos e um exemplo de invariante de agregado.

O objetivo é eliminar modelos duplicados e linguagem inconsistente entre squads.

## Contexto de Produção

- 4 squads tocam dados de Lead/Conta/agente sem vocabulário comum.

- Mesma entidade 'Contato' tem 3 modelos diferentes.

- Novas features recriam agregados já existentes.

## Diagnóstico e Causa Raiz

- Ausência de bounded contexts -> tudo vira 'tabela única'.

- Linguagem ubíqua ausente -> 'lead' significa 3 coisas.

- Sem agregado -> regras de consistência espalhadas.

## Decisão Arquitetural (ADR)

ADR-023: Mapa de Domínios

| Opção | Pro | Contra | Decisão |

| --- | --- | --- | --- |

| DDD explícito | consistência, linguagem | governança | ESCOLHIDA |

| Schema único | simples | acopla squads | rejeitada |

> **Nota:** Cada bounded context tem seu modelo; integração por eventos de domínio.

## Entregas desta Atividade

- DOMAIN-MAP.md.

- domain_models.py: agregados com invariantes.

- domain_events.py: eventos.

## Plano de Validação

1. Workshop de linguagem ubíqua com Product + 2 squads.

2. Validar agregados contra 3 user stories.

3. Gerar schemas dos agregados aprovados.

## Métricas e SLO

| SLO | Alvo |

| --- | --- |

| Domínios mapeados | 4 |

| Modelos duplicados | 0 |

| Eventos definidos | >= 6 |

## Riscos e Mitigações

| Risco | Mitigação |

| --- | --- |

| Mapa vira teoria | code review exige mapear |

| Over-engineering | só modelar o que tem regra |

## Próximos Passos

- Adotar eventos no barramento (05-A1).

- Testes de invariante de agregado.
## Decisões e tradeoffs
- DDD explícito escolhido sobre schema único: consistência e linguagem comum compensam o custo de governança, enquanto tabela única acopla os 4 squads.
- Cada bounded context tem seu modelo e a integração ocorre por eventos de domínio: evita que a entidade Contato continue com 3 modelos diferentes e que regra de um squad vaze para outro.
- Só modelar o que tem regra de consistência, com agregado de raiz única e filhos sem identidade pública: previne over-engineering e concentra esforço onde há invariante real.
- Validação em workshop de linguagem ubíqua com Product e 2 squads contra 3 user stories antes de gerar schemas: garante que o mapa reflete o negócio e não vira teoria.
- Anti-corruption layer na fronteira entre contextos: traduz o modelo vizinho sem poluir o contexto local, em vez de SQL cruzado entre domínios.

## Impacto no negócio

Com 4 squads tocando Lead, Conta e agente sem vocabulário comum e 3 modelos diferentes de Contato, cada feature recria agregados e cada mudança tem efeito cascata. Mapear 4 domínios com 0 modelos duplicados e ao menos 6 eventos definidos troca retrabalho e acoplamento oculto por fronteiras claras, reduz o tempo de impacto de alterações e evita o custo de carregar regra inconsistente para novas codificações.

## Referências de estudo
- Curso: Domain-Driven Design do zero, na Alura.
- Vídeo: Bounded contexts e linguagem ubíqua na prática, no YouTube.
- Doc oficial: Domain-Driven Design Reference, de Eric Evans, em domainlanguage.com.
- Doc oficial: Documentação do Python sobre dataclasses para modelar agregados e eventos, em docs.python.org.
