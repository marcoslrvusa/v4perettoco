# Deck PDI: Mapeamento de Domínios com Domain-Driven Design (DDD)

Área: Engenharia de Software

## Slide 1: Resumo Executivo
Mapeamento dos domínios da empresa em DDD antes de novas codificações: bounded contexts, agregados, linguagem ubíqua e eventos de domínio. Entrego o mapa, modelos e um exemplo de invariante de agregado.
O objetivo é eliminar modelos duplicados e linguagem inconsistente entre squads.
## Slide 2: Contexto de Produção
4 squads tocam dados de Lead/Conta/agente sem vocabulário comum.
Mesma entidade 'Contato' tem 3 modelos diferentes.
Novas features recriam agregados já existentes.
## Slide 3: Diagnóstico e Causa Raiz
Ausência de bounded contexts -> tudo vira 'tabela única'.
Linguagem ubíqua ausente -> 'lead' significa 3 coisas.
Sem agregado -> regras de consistência espalhadas.
## Slide 4: Decisão Arquitetural (ADR)
ADR-023: Mapa de Domínios
| Opção | Pro | Contra | Decisão |
| --- | --- | --- | --- |
| DDD explícito | consistência, linguagem | governança | ESCOLHIDA |
| Schema único | simples | acopla squads | rejeitada |
> Nota: Cada bounded context tem seu modelo; integração por eventos de domínio.
## Slide 5: Entregas desta Atividade
DOMAIN-MAP.md.
domain_models.py: agregados com invariantes.
domain_events.py: eventos.
## Slide 6: Plano de Validação
Workshop de linguagem ubíqua com Product + 2 squads.
Validar agregados contra 3 user stories.
Gerar schemas dos agregados aprovados.
## Slide 7: Métricas e SLO
| SLO | Alvo |
| --- | --- |
| Domínios mapeados | 4 |
| Modelos duplicados | 0 |
| Eventos definidos | >= 6 |
## Slide 8: Riscos e Mitigações
| Risco | Mitigação |
| --- | --- |
| Mapa vira teoria | code review exige mapear |
| Over-engineering | só modelar o que tem regra |
## Slide 9: Próximos Passos
Adotar eventos no barramento (05-A1).
Testes de invariante de agregado.