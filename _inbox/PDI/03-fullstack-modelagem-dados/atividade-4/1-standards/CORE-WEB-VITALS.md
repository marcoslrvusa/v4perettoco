# STANDARD — Core Web Vitals (Next.js)

## LCP (<=2.5s)
- `next/image` com `priority` no hero; `sizes` correto.
- Pré-carga de fontes; evitar layout shift.

## CLS (<=0.1)
- Sempre reservar `width/height` (ou `aspect-ratio`) em imagens.
- Evitar inserir conteúdo acima do fold via JS tardio.

## INP (<=200ms)
- `dynamic(() => import(...))` para componentes pesados (chat, mapa).
- Code splitting por rota.
