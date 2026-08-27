# Core Web Vitals — Diagnostico e Plano

| Metrica | Valor | Limite | Status |
|--------|-------|--------|--------|
| LCP | 4.1s | 2.5s | FAIL |
| INP | 410ms | 200ms | FAIL |
| CLS | 0.22 | 0.1 | FAIL |

## Plano
1. LCP: preconnect + fetchpriority=high + AVIF.
2. INP: chunks + debounce.
3. CLS: aspect-ratio + min-height.
