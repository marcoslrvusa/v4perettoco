# Deck PDI — Otimizacao de Core Web Vitals (LCP/INP/CLS) com Diagnostico Real

Area: Arquitetura Full Stack

## Slide 1: Resumo Executivo
Diagnostico e plano de Core Web Vitals (LCP, INP, CLS) para as interfaces dos agentes/portal, com evidencias de campo (CrUX) e laboratorio, mais correcoes aplicadas.
CWV e sinal de ranqueamento e de retencao.
## Slide 2: Contexto de Producao
Portais com LCP ~ 4s.
INP ruim ao clicar em acoes.
CLS ao carregar cards.
## Slide 3: O Problema
| Metrica | Campo | Alvo |
| --- | --- | --- |
| LCP | 4.1 s | <= 2.5 s |
| INP | 410 ms | <= 200 ms |
| CLS | 0.22 | <= 0.1 |
## Slide 4: Diagnostico
LCP: hero sem fetchpriority/preconnect.
INP: handler sincrono bloqueia.
CLS: cards sem aspect-ratio.
## Slide 5: Decisao Arquitetural (ADR)
ADR-034 — Ordem de Otimizacao
| Opcao | Pro | Contra | Decisao |
| --- | --- | --- | --- |
| LCP->INP->CLS | maior ROI | - | ESCOLHIDA |
> Nota: Medir no CrUX antes de cada mudanca.
## Slide 6: Entregas
CWV-DIAGNOSTICO.md.
cwv_fixes.html.
field_cwv.py.
## Slide 7: Validacao
Baseline de campo via field_cwv.py.
Aplicar correcoes; re-medir em 28 dias.
Confirmar LCP<=2.5, INP<=200, CLS<=0.1.
## Slide 8: Metricas e SLO
| SLO | Alvo |
| --- | --- |
| LCP p75 | <= 2.5 s |
| INP p75 | <= 200 ms |
| CLS p75 | <= 0.1 |
## Slide 9: Riscos
| Risco | Mitigacao |
| --- | --- |
| Regressao | budgate no CI |
| CrUX baixo | RUM proprio |
## Slide 10: Proximos Passos
Lighthouse CI no pipeline.
RUM de INP por rota.