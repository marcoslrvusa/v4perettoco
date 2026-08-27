# Deck PDI — Estudo de Design Patterns aplicados ao ecossistema

Area: Engenharia de Software

## Slide 1: Resumo Executivo
Conclusao do minicurso de Design Patterns com aplicacao pratica aos problemas reais da operacao. Entrego notas com exemplos funcionais de Adapter, Strategy, Observer e Command.
Entrega de evidencia tecnica: codigo que ja roda no ecossistema.
## Slide 2: Contexto de Producao
Codigo repetitivo em handlers de webhook e workers.
Sem vocabulario comum: PRs discutem 'aquela classe'.
Oportunidade de aplicar padroes em agentes.
## Slide 3: Diagnostico
Acoplamento a APIs de terceiro espalhado (sem Adapter).
Selecao de modelo de LLM por if/else (sem Strategy).
Logs de dominio sem padrao (sem Observer).
## Slide 4: Decisao Arquitetural (ADR)
ADR-024 — Catalogo de Padroes
| Padrao | Onde | Decisao |
| --- | --- | --- |
| Adapter | CRM/LLM externos | ESCOLHIDO |
| Strategy | roteamento de modelo | ESCOLHIDO |
| Observer | eventos de dominio | ESCOLHIDO |
| Singleton p/ clients | rejeitado (DI) | NAO |
## Slide 5: Entregas desta Atividade
DESIGN-PATTERNS-NOTES.md.
patterns_demo.py.
ESTUDO-PLANO.md.
## Slide 6: Validacao
Rodar patterns_demo.py.
PR aplicando Adapter no handler de 1 CRM.
Checklist de padroes no template de PR.
## Slide 7: Metricas
| SLO | Alvo |
| --- | --- |
| Handlers com Adapter | >= 1 piloto |
| Padroes documentados | criacionais/estruturais/comportamentais |
## Slide 8: Riscos
| Risco | Mitigacao |
| --- | --- |
| Over-engineering | so onde ha variacao |
| Padrao como fim | code review foca em valor |
## Slide 9: Proximos Passos
Refatorar handlers de CRM para Adapter.
Roteamento de modelo via Strategy.