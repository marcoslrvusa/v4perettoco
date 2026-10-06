# AG-01 — Product Schema Competitivo (GEO/AIO) via GTM — Lola Aviamentos

**Task Ekyte:** 10049802 — [AIO B1] Product schema — template nas 78 páginas de produto
**Cliente:** Lola Aviamentos · **Site:** https://www.lolaaviamentos.com.br
**Plataforma:** Nuvemshop (Tema Amazonas) · **Container GTM:** GTM-MQW27G8G

---

## Contexto

O tema Amazonas já emite um Product schema válido e completo com os campos mínimos
(`name`, `image`, `description`, `sku`, `brand`, `offers`), mas **sem as variações por opção**
(entre 0,30m×100m e 1,50m×100m, cores, estoque por variante), sem `priceValidUntil`, sem
`additionalImage` e sem dados de oferta agregada.

A página expõe um atributo rico no DOM — `data-variants` — com JSON completo de **cada variante**:
`sku`, `price_number`, `stock`, `available`, `image_url` e a opção (ex.: "Preta 0,30m x 100m").

**Estratégia:** uma tag GTM única que, em páginas de produto:
1. Remove o Product schema nativo (evita 2 schemas de produto na mesma página → conflito de rich results).
2. Injeta um schema enriquecido a partir do `data-variants` + schema nativo:
   - **1 Offer por variante** (preço, `availability`, `sku`, imagem, `priceValidUntil`)
   - **AggregateOffer** quando há múltiplas variantes (low/high price)
   - `additionalImage` com todas as imagens das variantes
   - `itemCondition`, `seller`, `brand`, `description` (o description vem do produto — melhora junto da passada de dados via API)

Nenhuma edição de tema, nenhuma permissão nova no token.

---

## Passo 1 — Criar a tag no GTM

**GTM > Criar Nova Tag:**

| Campo | Valor |
|---|---|
| Nome da tag | `Lola — Product Schema Enriquecido (GEO/AIO)` |
| Tipo de tag | **Custom HTML** |
| Trigger | **Todas as Páginas** (o próprio script filtra `/produtos/`) |
| Advanced settings | Desmarcar "Once per page" não é necessário — o script tem guarda anti-duplicidade |

Cole o código abaixo no campo **HTML**:

```html
<script>
(function () {
  if (window.__v4LolaProductDone) return;
  var p = window.location.pathname;
  if (!/^\/produtos\//.test(p)) return;

  try {
    var variantsEl = document.querySelector('[data-variants]');
    if (!variantsEl) return;
    var variants = JSON.parse(variantsEl.getAttribute('data-variants') || '[]');
    if (!Array.isArray(variants) || !variants.length) return;

    var all = document.querySelectorAll('script[type="application/ld+json"]');
    var native = null;
    for (var i = 0; i < all.length; i++) {
      var t;
      try { t = JSON.parse(all[i].textContent); } catch (e) { continue; }
      if (t && t.mainEntity && t.mainEntity['@type'] === 'Product') { native = t; all[i].parentNode.removeChild(all[i]); break; }
    }
    if (native) {
      var url = location.origin + location.pathname;
      var brandName = 'Lola Soluções Têxteis';
      if (native.mainEntity.brand && native.mainEntity.brand.name) brandName = native.mainEntity.brand.name;
      var desc = native.mainEntity.description || '';
      var name = native.mainEntity.name || document.title;

      var imgs = [];
      variants.forEach(function (v) {
        if (v.image_url) imgs.push(v.image_url.indexOf('//') === 0 ? 'https:' + v.image_url : v.image_url);
      });
      if (native.mainEntity.image) imgs.push(native.mainEntity.image);
      imgs = imgs.filter(function (u, k) { return imgs.indexOf(u) === k; });

      var validUntil = new Date(Date.now() + 60 * 24 * 3600 * 1000).toISOString();
      var offers = variants.map(function (v) {
        var o = {
          '@type': 'Offer',
          'price': v.price_number,
          'priceCurrency': 'BRL',
          'availability': v.available ? 'https://schema.org/InStock' : 'https://schema.org/OutOfStock',
          'itemCondition': 'https://schema.org/NewCondition',
          'url': url,
          'priceValidUntil': validUntil,
          'sku': v.sku
        };
        if (v.image_url) o.image = v.image_url.indexOf('//') === 0 ? 'https:' + v.image_url : v.image_url;
        if (v.option0) o['additionalProperty'] = [{ '@type': 'PropertyValue', 'name': 'Opção', 'value': v.option0 }];
        o['seller'] = { '@type': 'Organization', 'name': 'Lola Aviamentos - Entretelas para confecções e insumos para Bonés' };
        return o;
      });

      var offerBlock;
      if (offers.length > 1) {
        var prices = offers.map(function (o) { return o.price; });
        offerBlock = {
          '@type': 'AggregateOffer',
          'lowPrice': Math.min.apply(null, prices),
          'highPrice': Math.max.apply(null, prices),
          'priceCurrency': 'BRL',
          'offerCount': offers.length,
          'offers': offers
        };
      } else {
        offerBlock = offers[0];
      }

      var schema = {
        '@context': 'https://schema.org/',
        '@type': 'Product',
        '@id': url,
        'name': name,
        'image': imgs[0] || undefined,
        'additionalImage': imgs.length > 1 ? imgs : undefined,
        'description': desc,
        'sku': offers[0].sku,
        'brand': { '@type': 'Brand', 'name': brandName },
        'offers': offerBlock
      };

      var s = document.createElement('script');
      s.type = 'application/ld+json';
      s.textContent = JSON.stringify(schema);
      document.head.appendChild(s);
      window.__v4LolaProductDone = true;
    }
  } catch (e) {
    /* deixa o schema nativo intacto em caso de erro */
  }
})();
</script>
```

---

## Passo 2 — Testar antes de publicar

1. **Preview:** GTM > Preview → abrir uma URL de produto (ex.: `/produtos/entretela-de-tnt-micro-ponto-termocolante-70g-lab-407-408/`).
2. No preview, conferir no console que não houve exceção.
3. No painel: **Elemento > script com `@type: Product`** → deve existir **um único** Product schema, agora com `AggregateOffer` e `offers` por variante.
4. Validar no **Rich Results Test** (https://search.google.com/test/rich-results) — 0 errors. E no validator (https://validator.schema.org/) colar o JSON gerado.
5. Confirmar que **home/categoria não mudaram** (o script não roda fora de `/produtos/`).

---

## Passo 3 — Publicar

Publish da versão do container com comentário tipo: "Product schema enriquecido GEO/AIO (variantes, AggregateOffer, additionalImage)".

---

## Rodapé de dados (opcional, sem código)

- **`description` do schema = description do produto.** A passada de qualidade de dados (via API do token) que corrige textos incongruentes (ex.: produto 70g descrito como "50g") reflete **automaticamente** no schema injetado.
- **`aggregateRating`/`review`:** preparado para ativar quando a loja tiver um widget de avaliações com dados no DOM — até lá, não é incluído (não inventamos dado).
- **`gtin`:** quando o cliente tiver os EANs, dá para subir via API (campo `gtin` do produto) e o script passará a emitir no Offer.

---

*Gerado em 12/08/2026 · Bloco 1 (Fundação) — projeto Lola Aviamentos SEO/AIO.*