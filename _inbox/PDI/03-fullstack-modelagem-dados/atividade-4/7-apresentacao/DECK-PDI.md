# PDI — Apresentação: Core Web Vitals no Front-end Next.js (Lazy Loading & Code Splitting)

> **Formato:** 5-6 slides | **Tempo:** 15-20 min
> **Audiência:** Tech Lead + Squad

---

## Slide 1: Título

```
PDI: CORE WEB VITALS NO FRONT-END NEXT.JS (LAZY LOADING & CODE SPLITTING)

Marcos Perettoco — V4 Company
25/08/2026 | Arquitetura Full Stack
```

---

## Slide 2: O Problema

**Páginas de landing apresentavam LCP e CLS ruins, prejudicando SEO e conversão.**

## Diagnóstico

- Imagens sem dimensionamento (CLS)
- Componentes pesados no bundle inicial (INP)
- Sem lazy loading de widgets


---

## Slide 3: Arquitetura da Solução

## Abordagem

- next/image com priority no hero e tamanhos reservados
- dynamic() para code splitting de componentes pesados
- Reserva de aspect-ratio para evitar layout shift


---

## Slide 4: Entregas

## Artefatos

- CORE-WEB-VITALS.md (guia)
- example_next.tsx (Next.js lazy + image)


---

## Slide 5: Métricas de Sucesso

| Métrica | Antes | Depois |
|--------|-------|--------|
| LCP | > 4s | <= 2.5s |
| CLS | > 0.25 | <= 0.1 |
| INP | > 300ms | <= 200ms |
---

## Slide 6: Próximos Passos

- Medir com Lighthouse em produção
- Aplicar aos templates de landing
