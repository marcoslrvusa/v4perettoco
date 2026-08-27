# Deck PDI — Mapeamento de Dominios com Domain-Driven Design (DDD)

Area: Engenharia de Software

## Slide 1: Resumo Executivo
Mapeamento dos dominios da empresa em DDD antes de novas codificacoes: bounded contexts, agregados, linguagem ubíqua e eventos de dominio. Entrego o mapa, modelos e um exemplo de invariante de agregado.
O objetivo e eliminar modelos duplicados e linguagem inconsistente entre squads.
## Slide 2: Contexto de Producao
4 squads tocam dados de Lead/Conta/agente sem vocabulario comum.
Mesma entidade 'Contato' tem 3 modelos diferentes.
Novas features recriam agregados ja existentes.
## Slide 3: Diagnostico e Causa Raiz
Ausencia de bounded contexts -> tudo vira 'tabela unica'.
Linguagem ubíqua ausente -> 'lead' significa 3 coisas.
Sem agregado -> regras de consistencia espalhadas.
## Slide 4: Decisao Arquitetural (ADR)
ADR-023 — Mapa de Dominios
| Opcao | Pro | Contra | Decisao |
| --- | --- | --- | --- |
| DDD explicito | consistencia, linguagem | governanca | ESCOLHIDA |
| Schema unico | simples | acopla squads | rejeitada |
> Nota: Cada bounded context tem seu modelo; integracao por eventos de dominio.
## Slide 5: Entregas desta Atividade
DOMAIN-MAP.md.
domain_models.py — agregados com invariantes.
domain_events.py — eventos.
## Slide 6: Plano de Validacao
Workshop de linguagem ubíqua com Product + 2 squads.
Validar agregados contra 3 user stories.
Gerar schemas dos agregados aprovados.
## Slide 7: Metricas e SLO
| SLO | Alvo |
| --- | --- |
| Dominios mapeados | 4 |
| Modelos duplicados | 0 |
| Eventos definidos | >= 6 |
## Slide 8: Riscos e Mitigacoes
| Risco | Mitigacao |
| --- | --- |
| Mapa vira teoria | code review exige mapear |
| Over-engineering | so modelar o que tem regra |
## Slide 9: Proximos Passos
Adotar eventos no barramento (05-A1).
Testes de invariante de agregado.