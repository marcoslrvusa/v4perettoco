# AG-01 — Tags GTM prontas: Organization (Home) + Store (/empresa/)

**Cliente:** Lola Aviamentos · **Task:** 10049800 · **Container:** GTM-MQW27G8G
**Caminho:** Opção B (fallback via GTM) — sem dependência do painel Nuvemshop

---

## Tag 1 — Organization JSON-LD (dispara apenas na home)

**Tags → Nova** → nome `AIO - Organization JSON-LD (Home)` → **HTML personalizado**:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Lola Aviamentos",
  "alternateName": "Lola Soluções em Têxteis",
  "url": "https://www.lolaaviamentos.com.br",
  "logo": "https://acdn-us.mitiendanube.com/stores/001/720/481/themes/common/logo-2381817-1754682754-c325014e3710438c242fa3453bf903381754682754-480-0.webp",
  "description": "Importação e distribuição de entretelas, insumos para bonés, aviamentos têxteis e máquinas para confecção.",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Av. Irati, 284 - Barra Funda",
    "addressLocality": "Apucarana",
    "addressRegion": "PR",
    "addressCountry": "BR",
    "postalCode": "86800-000"
  },
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+55-43-99119-6727",
    "contactType": "sales",
    "availableLanguage": ["Portuguese (Brazilian)", "Portuguese"],
    "areaServed": "BR"
  },
  "email": "vendas@lolaaviamentos.com.br",
  "sameAs": [
    "https://www.instagram.com/lolasolucoes",
    "https://www.facebook.com/lolasolucoestexteis",
    "https://www.youtube.com/@lolasolucoes"
  ]
}
</script>
```

**Disparador:** **Todas as páginas** → condição **Page URL matches RegEx**:

```
^https?://www\.lolaaviamentos\.com\.br/?$
```

---

## Tag 2 — Store JSON-LD (dispara apenas em /empresa/)

**Tags → Nova** → nome `AIO - Store JSON-LD (Empresa)` → **HTML personalizado**:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Store",
  "name": "Lola Aviamentos",
  "alternateName": "Lola Soluções em Têxteis",
  "url": "https://www.lolaaviamentos.com.br",
  "logo": "https://acdn-us.mitiendanube.com/stores/001/720/481/themes/common/logo-2381817-1754682754-c325014e3710438c242fa3453bf903381754682754-480-0.webp",
  "description": "Importação e distribuição de entretelas, insumos para bonés, aviamentos têxteis e máquinas para confecção.",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Av. Irati, 284 - Barra Funda",
    "addressLocality": "Apucarana",
    "addressRegion": "PR",
    "addressCountry": "BR",
    "postalCode": "86800-000"
  },
  "telephone": "+55-43-99119-6727",
  "email": "vendas@lolaaviamentos.com.br",
  "openingHoursSpecification": {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
    "opens": "08:00",
    "closes": "18:00"
  },
  "areaServed": {
    "@type": "Country",
    "name": "Brasil"
  },
  "sameAs": [
    "https://www.instagram.com/lolasolucoes",
    "https://www.facebook.com/lolasolucoestexteis",
    "https://www.youtube.com/@lolasolucoes"
  ]
}
</script>
```

**Disparador:** **Todas as páginas** → condição **Page URL contém**:

```
lolaaviamentos.com.br/empresa/
```

---

## Publicar e validar

1. **Preview** → home e `/empresa/` em aba anônima → conferir no `<head>` que cada JSON-LD apareceu apenas na página certa
2. **Enviar** → versão `AG-01 JSON-LD Organization + Store` → **Publicar**
3. Validar em **Rich Results Test** (search.google.com/test/rich-results) e **validator.schema.org**

## Arquivos de referência

- `AG-01-jsonld-organization.json` · `AG-01-jsonld-store.json` · `AG-01-gtm-guia-implementacao.md`