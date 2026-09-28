# Deck PDI: Estudo de Design Patterns aplicados ao ecossistema

Área: Engenharia de Software

## Slide 1: Resumo Executivo
Conclusão do minicurso de Design Patterns com aplicação prática aos problemas reais da operação. Entrego notas com exemplos funcionais de Adapter, Strategy, Observer e Command.
Entrega de evidência técnica: código que já roda no ecossistema.
## Slide 2: Contexto de Produção
Código repetitivo em handlers de webhook e workers.
Sem vocabulário comum: PRs discutem 'àquela classe'.
Oportunidade de aplicar padrões em agentes.
## Slide 3: Diagnóstico
Acoplamento a APIs de terceiro espalhado (sem Adapter).
Seleção de modelo de LLM por if/else (sem Strategy).
Logs de domínio sem padrão (sem Observer).
## Slide 4: Decisão Arquitetural (ADR)
ADR-024: Catálogo de Padrões
| Padrão | Onde | Decisão |
| --- | --- | --- |
| Adapter | CRM/LLM externos | ESCOLHIDO |
| Strategy | roteamento de modelo | ESCOLHIDO |
| Observer | eventos de domínio | ESCOLHIDO |
| Singleton p/ clients | rejeitado (DI) | NÃO |
## Slide 5: Entregas desta Atividade
DESIGN-PATTERNS-NOTES.md.
patterns_demo.py.
ESTUDO-PLANO.md.
## Slide 6: Validação
Rodar patterns_demo.py.
PR aplicando Adapter no handler de 1 CRM.
Checklist de padrões no template de PR.
## Slide 7: Métricas
| SLO | Alvo |
| --- | --- |
| Handlers com Adapter | >= 1 piloto |
| Padrões documentados | criacionais/estruturais/comportamentais |
## Slide 8: Riscos
| Risco | Mitigação |
| --- | --- |
| Over-engineering | só onde há variação |
| Padrão como fim | code review foca em valor |
## Slide 9: Próximos Passos
Refatorar handlers de CRM para Adapter.
Roteamento de modelo via Strategy.