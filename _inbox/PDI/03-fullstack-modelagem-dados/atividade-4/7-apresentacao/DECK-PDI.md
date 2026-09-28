# Deck PDI: Otimização de Core Web Vitals (LCP/INP/CLS) com Diagnóstico Real

Área: Arquitetura Full Stack

## Slide 1: Resumo Executivo
Diagnóstico e plano de Core Web Vitals (LCP, INP, CLS) para as interfaces dos agentes/portal, com evidências de campo (CrUX) e laboratório, mais correções aplicadas.
CWV e sinal de ranqueamento e de retenção.
## Slide 2: Contexto de Produção
Portais com LCP ~ 4s.
INP ruim ao clicar em ações.
CLS ao carregar cards.
## Slide 3: O Problema
| Métrica | Campo | Alvo |
| --- | --- | --- |
| LCP | 4.1 s | <= 2.5 s |
| INP | 410 ms | <= 200 ms |
| CLS | 0.22 | <= 0.1 |
## Slide 4: Diagnóstico
LCP: hero sem fetchpriority/preconnect.
INP: handler síncrono bloqueia.
CLS: cards sem aspect-ratio.
## Slide 5: Decisão Arquitetural (ADR)
ADR-034: Ordem de Otimização
| Opção | Pro | Contra | Decisão |
| --- | --- | --- | --- |
| LCP->INP->CLS | maior ROI | - | ESCOLHIDA |
> Nota: Medir no CrUX antes de cada mudança.
## Slide 6: Entregas
CWV-DIAGNOSTICO.md.
cwv_fixes.html.
field_cwv.py.
## Slide 7: Validação
Baseline de campo via field_cwv.py.
Aplicar correções; re-medir em 28 dias.
Confirmar LCP<=2.5, INP<=200, CLS<=0.1.
## Slide 8: Métricas e SLO
| SLO | Alvo |
| --- | --- |
| LCP p75 | <= 2.5 s |
| INP p75 | <= 200 ms |
| CLS p75 | <= 0.1 |
## Slide 9: Riscos
| Risco | Mitigação |
| --- | --- |
| Regressão | budgate no CI |
| CrUX baixo | RUM próprio |
## Slide 10: Próximos Passos
Lighthouse CI no pipeline.
RUM de INP por rota.