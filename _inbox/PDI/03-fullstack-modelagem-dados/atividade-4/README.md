# Otimização de Core Web Vitals (LCP/INP/CLS) com Diagnóstico Real

Arquitetura Full Stack

## Resumo Executivo

Diagnóstico e plano de Core Web Vitals (LCP, INP, CLS) para as interfaces dos agentes/portal, com evidências de campo (CrUX) e laboratório, mais correções aplicadas.

CWV e sinal de ranqueamento e de retenção.

## Contexto de Produção

- Portais com LCP ~ 4s.

- INP ruim ao clicar em ações.

- CLS ao carregar cards.

## O Problema

| Métrica | Campo | Alvo |

| --- | --- | --- |

| LCP | 4.1 s | <= 2.5 s |

| INP | 410 ms | <= 200 ms |

| CLS | 0.22 | <= 0.1 |

## Diagnóstico

- LCP: hero sem fetchpriority/preconnect.

- INP: handler síncrono bloqueia.

- CLS: cards sem aspect-ratio.

## Decisão Arquitetural (ADR)

ADR-034: Ordem de Otimização

| Opção | Pro | Contra | Decisão |

| --- | --- | --- | --- |

| LCP->INP->CLS | maior ROI | - | ESCOLHIDA |

> **Nota:** Medir no CrUX antes de cada mudança.

## Entregas

- CWV-DIAGNOSTICO.md.

- cwv_fixes.html.

- field_cwv.py.

## Validação

1. Baseline de campo via field_cwv.py.

2. Aplicar correções; re-medir em 28 dias.

3. Confirmar LCP<=2.5, INP<=200, CLS<=0.1.

## Métricas e SLO

| SLO | Alvo |

| --- | --- |

| LCP p75 | <= 2.5 s |

| INP p75 | <= 200 ms |

| CLS p75 | <= 0.1 |

## Riscos

| Risco | Mitigação |

| --- | --- |

| Regressão | budgate no CI |

| CrUX baixo | RUM próprio |

## Decisões e tradeoffs

1. **Ordem de otimização LCP, INP e depois CLS (ADR-034, maior ROI):** ataca primeiro o que mais pesa na experiência e no ranqueamento. Tradeoff: o CLS visível continua por mais um ciclo; aceito porque o LCP de 4,1s afasta mais usuário que o deslocamento de layout.
2. **Medir no CrUX (campo, p75, janela de 28 dias) antes de cada mudança via `field_cwv.py`:** laboratório não captura gargalo real. Tradeoff: ciclo de confirmação de 28 dias; o Lighthouse guia o dia a dia e o campo da o veredito.
3. **LCP com `next/image priority` no hero + preconnect + AVIF:** entrega a maior imagem cedo. Tradeoff: priority na imagem errada atrasa o resto; só o hero recebe.
4. **INP com dynamic import e code splitting por rota + debounce:** o handler síncrono que bloqueava (410ms) sai do caminho crítico. Tradeoff: o chunk sob demanda pode dar atraso no primeiro uso do componente pesado (chat, mapa).
5. **CLS com `aspect-ratio` e width/height reservados, sem inserir conteúdo acima do fold via JS tardio:** os cards param de pular (0,22 para 0,1 ou menos). Tradeoff: a reserva fixa pode deixar espaço vazio breve em conteúdo variável; melhor que o salto.

## Impacto no negócio

Portais com LCP de 4,1s, INP de 410ms e CLS de 0,22 perdiam retenção e sinal de ranqueamento. Com o plano, a meta e 75% das sessões no "bom" (LCP até 2,5s, INP até 200ms, CLS até 0,1), o que reduz abandono no portal de agentes e protege tráfego orgânico sem reescrever o front.

## Referências de estudo

- Curso: Learn Performance (web.dev, Google)
- Vídeo: Core Web Vitals (Google Chrome Developers, YouTube)
- Doc oficial: Web Vitals, https://web.dev/vitals/ (verificada em 2026-09-28)
- Doc oficial: PageSpeed Insights, https://developers.google.com/speed/docs/insights/v5/about (verificada em 2026-09-28)

## Próximos Passos

- Lighthouse CI no pipeline.

- RUM de INP por rota.