# Script de Demonstração — Core Web Vitals no Front-end Next.js (Lazy Loading & Code Splitting)

## Setup
```bash
# Estrutura da entrega
tree 03-fullstack-modelagem-dados/atividade-4/
```

## Passo 1: Contexto
Explique o problema:
> Páginas de landing apresentavam LCP e CLS ruins, prejudicando SEO e conversão.

## Passo 2: Arquitetura
Apresente os pontos-chave:
- next/image com priority no hero e tamanhos reservados
- dynamic() para code splitting de componentes pesados
- Reserva de aspect-ratio para evitar layout shift

## Passo 3: Entregas
Mostre os artefatos gerados:
- CORE-WEB-VITALS.md (guia)
- example_next.tsx (Next.js lazy + image)

## Passo 4: Métricas
| Métrica | Antes | Depois |
|--------|-------|--------|
| LCP | > 4s | <= 2.5s |
| CLS | > 0.25 | <= 0.1 |
| INP | > 300ms | <= 200ms |
