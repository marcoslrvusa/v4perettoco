# Otimizacao de Core Web Vitals (LCP/INP/CLS) com Diagnostico Real

Arquitetura Full Stack

## Resumo Executivo

Diagnostico e plano de Core Web Vitals (LCP, INP, CLS) para as interfaces dos agentes/portal, com evidencias de campo (CrUX) e laboratorio, mais correcoes aplicadas.

CWV e sinal de ranqueamento e de retencao.

## Contexto de Producao

- Portais com LCP ~ 4s.

- INP ruim ao clicar em acoes.

- CLS ao carregar cards.

## O Problema

| Metrica | Campo | Alvo |

| --- | --- | --- |

| LCP | 4.1 s | <= 2.5 s |

| INP | 410 ms | <= 200 ms |

| CLS | 0.22 | <= 0.1 |

## Diagnostico

- LCP: hero sem fetchpriority/preconnect.

- INP: handler sincrono bloqueia.

- CLS: cards sem aspect-ratio.

## Decisao Arquitetural (ADR)

ADR-034 — Ordem de Otimizacao

| Opcao | Pro | Contra | Decisao |

| --- | --- | --- | --- |

| LCP->INP->CLS | maior ROI | - | ESCOLHIDA |

> **Nota:** Medir no CrUX antes de cada mudanca.

## Entregas

- CWV-DIAGNOSTICO.md.

- cwv_fixes.html.

- field_cwv.py.

## Validacao

1. Baseline de campo via field_cwv.py.

2. Aplicar correcoes; re-medir em 28 dias.

3. Confirmar LCP<=2.5, INP<=200, CLS<=0.1.

## Metricas e SLO

| SLO | Alvo |

| --- | --- |

| LCP p75 | <= 2.5 s |

| INP p75 | <= 200 ms |

| CLS p75 | <= 0.1 |

## Riscos

| Risco | Mitigacao |

| --- | --- |

| Regressao | budgate no CI |

| CrUX baixo | RUM proprio |

## Proximos Passos

- Lighthouse CI no pipeline.

- RUM de INP por rota.