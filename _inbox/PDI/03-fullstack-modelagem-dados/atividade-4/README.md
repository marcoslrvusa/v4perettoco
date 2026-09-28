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

ADR-034: Ordem de Otimizacao

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

## Decisoes e tradeoffs

1. **Ordem de otimizacao LCP, INP e depois CLS (ADR-034, maior ROI):** ataca primeiro o que mais pesa na experiencia e no ranqueamento. Tradeoff: o CLS visivel continua por mais um ciclo; aceito porque o LCP de 4,1s afasta mais usuario que o deslocamento de layout.
2. **Medir no CrUX (campo, p75, janela de 28 dias) antes de cada mudanca via `field_cwv.py`:** laboratorio nao captura gargalo real. Tradeoff: ciclo de confirmacao de 28 dias; o Lighthouse guia o dia a dia e o campo da o veredito.
3. **LCP com `next/image priority` no hero + preconnect + AVIF:** entrega a maior imagem cedo. Tradeoff: priority na imagem errada atrasa o resto; so o hero recebe.
4. **INP com dynamic import e code splitting por rota + debounce:** o handler sincrono que bloqueava (410ms) sai do caminho critico. Tradeoff: o chunk sob demanda pode dar atraso no primeiro uso do componente pesado (chat, mapa).
5. **CLS com `aspect-ratio` e width/height reservados, sem inserir conteudo acima do fold via JS tardio:** os cards param de pular (0,22 para 0,1 ou menos). Tradeoff: a reserva fixa pode deixar espaco vazio breve em conteudo variavel; melhor que o salto.

## Impacto no negocio

Portais com LCP de 4,1s, INP de 410ms e CLS de 0,22 perdiam retencao e sinal de ranqueamento. Com o plano, a meta e 75% das sessoes no "bom" (LCP ate 2,5s, INP ate 200ms, CLS ate 0,1), o que reduz abandono no portal de agentes e protege trafego organico sem reescrever o front.

## Referencias de estudo

- Curso: Learn Performance (web.dev, Google)
- Video: Core Web Vitals (Google Chrome Developers, YouTube)
- Doc oficial: Web Vitals, https://web.dev/vitals/ (verificada em 2026-09-28)
- Doc oficial: PageSpeed Insights, https://developers.google.com/speed/docs/insights/v5/about (verificada em 2026-09-28)

## Proximos Passos

- Lighthouse CI no pipeline.

- RUM de INP por rota.