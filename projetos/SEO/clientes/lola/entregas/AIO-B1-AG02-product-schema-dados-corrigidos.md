# AG-02 — Product Schema nas 78 páginas de produto (via dados)

## Resumo

O tema Amazonas da Nuvemshop já injeta JSON-LD `WebPage > mainEntity Product` em todas as páginas de produto (template único — sem GTM necessário para o schema básico). A otimização foi feita **corrigindo os dados de produto na API Nuvemshop**, que alimentam os campos do schema. Resultado: **78/78 páginas com Product schema completo** (nome, imagem, description, sku, brand, offers com price/priceCurrency/availability).

## O que foi feito (via API Nuvemshop — store 1720481)

### 1. Títulos (`seo_title`) — 30 produtos
- 21 títulos vazios preenchidos com o nome completo (gramatura + referência)
- Correção de erro de gramatura: produto 70g (Lab-407/408) dizia "50g" → corrigido
- Títulos genéricos curtos ("Viés de Tecido", "Tecido Suede", "Aba para Boné") receberam spec completa
- 4 correções manuais: Botão 13mm (era 15mm), Máquina de Pregar Botão BP-1000 (era "Encapar"), etc.

### 2. Description (`seo_description`) — 77 produtos
Padrão AEO: `{Nome completo com gramatura e referência}: {1ª frase factual}. Compre na Lola Aviamentos.`
- O `seo_description` é a fonte do campo `description` do schema Product
- Corrige divergências título × descrição (o 70g aparecia como "50g" no schema)
- Dá nome + gramatura + referência explícita para extração por LLMs

### 3. Brand — 10 produtos
Normalizados para `Lola Soluções Têxteis` (variações: vazio, "None", "Lola Aviamentos", nomes longos).

### 4. SKUs de variantes — 26 variantes / 3 produtos
Fecham o campo `sku` do schema nas páginas que estavam incompletas:
- Regulador Plástico Proflex (8 cores) → `RPP-{COR}`
- Entretela ETP algodão (16 combos gramatura × dimensão) → `ETP-{G}-{LA}x{CO}`
- Base Máquina Transfer MT-1500 (2) → `BMT-1500-CURVA/RETA`

## Validação final

| Métrica | Antes | Depois |
|---|---|---|
| Páginas com Product schema | 77 (69 completas) | **78/78** |
| Páginas incompletas (sku/brand) | 8 | **0** |
| Divergência de gramatura no description | 1 (70g→50g) | **0** |

## Estrutura do schema (gerado pelo tema, dados corrigidos)

```json
{
  "@type": "WebPage",
  "name": "...",
  "description": "...",
  "mainEntity": {
    "@type": "Product",
    "name": "...",
    "sku": "...",
    "brand": { "@type": "Brand", "name": "Lola Soluções Têxteis" },
    "image": "...",
    "description": "<seo_description>",
    "offers": { "price": "...", "priceCurrency": "...", "availability": "..." }
  }
}
```

## Nota
- Fallback GTM (`AIO-B1-AG01-product-schema-competitivo-gtm.md`) continua disponível se o cliente quiser enriquecer com variantes/AggregateOffer no nível competitivo, mas o schema básico da task já está 100% via dados.
- Rascunho não publicado (TNT 60G-UNICA) foi mantido intacto.