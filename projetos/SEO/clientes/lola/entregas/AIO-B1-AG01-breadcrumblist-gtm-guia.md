# AG-01 — Guia de Implementação JSON-LD BreadcrumbList (todas as páginas)

## Lola Aviamentos — https://www.lolaaviamentos.com.br/

**Task Ekyte:** 10049804 — [AIO B1] BreadcrumbList schema global
**Plataforma:** Nuvemshop (Tema Amazonas)
**GTM Container:** GTM-MQW27G8G (já instalado no site)
**Status atual:** 0 páginas com BreadcrumbList. O tema já renderiza breadcrumbs VISUAIS (`.breadcrumbs .crumb`), mas não gera JSON-LD.

---

## Abordagem Recomendada: GTM + Script que Reutiliza o Breadcrumb do Tema

Como a Nuvemshop renda a trilha visual em todas as páginas (`Início > Categoria > Subcategoria > Produto`), a solução mais escalável é **um único script via GTM** que lê os links `.crumb` já renderizados e gera o JSON-LD `BreadcrumbList` dinamicamente.

**Vantagens:**
- 1 tag para todo o site (142+ páginas) — zero trabalho por página
- Consistência garantida com a árvore real (o schema espelha o menu que o usuário vê)
- Fluxo automático ao adicionar categorias/subcategorias/produtos futuros

---

## Passo 1 — Acessar o Google Tag Manager

1. Login em https://tagmanager.google.com/
2. Selecionar o container **GTM-MQW27G8G**
3. Ir em **Tags → Novo**

## Passo 2 — Criar a Tag de BreadcrumbList

1. **Nome da tag:** `Schema BreadcrumbList — Global`
2. **Tipo de tag:** Custom HTML
3. **HTML** (colar exatamente):

```html
<script>
(function() {
  if (document.getElementById('ld-json-breadcrumb')) { return; }

  var crumbList = document.querySelectorAll('.breadcrumbs .crumb');
  if (!crumbList.length) { return; }

  var items = [];
  var pos = 1;
  var pageUrl = window.location.href.split('#')[0].split('?')[0];

  crumbList.forEach(function(crumb) {
    var name = crumb.textContent.trim();
    if (!name) { return; }

    var isActive = crumb.getAttribute('class') && crumb.getAttribute('class').indexOf('active') !== -1;
    var href = crumb.getAttribute('href');
    var url;

    if (isActive) {
      url = pageUrl;   // último item = a própria página
    } else if (href) {
      url = new URL(href, window.location.origin).href;
    } else {
      url = pageUrl;
    }

    // Normaliza para https://www.lolaaviamentos.com.br
    url = url.replace(/^https?:\/\/lolaaviamentos\.com\.br/, 'https://www.lolaaviamentos.com.br');
    url = url.replace(/\/+$/, '') || 'https://www.lolaaviamentos.com.br/';

    items.push({
      '@type': 'ListItem',
      'position': pos++,
      'name': name,
      'item': url
    });
  });

  if (!items.length) { return; }

  var ld = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    'itemListElement': items
  };

  var script = document.createElement('script');
  script.type = 'application/ld+json';
  script.id = 'ld-json-breadcrumb';
  script.textContent = JSON.stringify(ld);

  var head = document.head || document.getElementsByTagName('head')[0];
  head.appendChild(script);
})();
</script>
```

4. **Acionamento:** **All Pages** → `Page View` (todas as páginas)
5. **Opção extra (recomendada):** Adicionar condição de página para **não** disparar na home:
   - Trigger: `Page View` com `{{Page Hostname}}` igual a `www.lolaaviamentos.com.br` E `{{Page Path}}` diferente de `/`
   - Na home o Breadcrumb visual do tema é só "Início", o que torna o schema redundante.

## Passo 3 — Publicar o container

1. Clicar em **Enviar (Submit)**
2. Nome da versão: `AG-01 BreadcrumbList Schema Global`
3. Descrição: `JSON-LD BreadcrumbList gerado dinamicamente a partir do menu visível em todas as páginas`

---

## Validação

| Verificação | Ferramenta | Critério |
|-------------|-----------|----------|
| JSON-LD presente | View Source | `<script type="application/ld+json" id="ld-json-breadcrumb">` |
| Sem erros de schema | https://validator.schema.org/ | 0 errors, 0 warnings |
| Rich Results | https://search.google.com/test/rich-results | Breadcrumb reconhecido |
| Profundidade correta | Testar URL produto e subcategoria | `Início > Categoria > Subcat > Produto` |
| URL canônica no último item | Testar URL com e sem www | Item final = URL www da página |
| Não duplica | View Source | Apenas 1 bloco `ld-json-breadcrumb` por página |

**Testar depois de publicar:**
1. Home — schema ausente ou só Início (aceitável)
2. `/entretela-de-memoria/cinza/` — `Início > Entretela de Memória > Cinza`
3. `/bordado1/rasgo-facil/` — `Início > Bordado > Rasgo Fácil`
4. `/produtos/entretela-para-bordado-rasgavel-40g-90cm-200m/` — `Início > Bordado > Rasgo Fácil > [Produto]`
5. `/empresa/` — `Início > Empresa`

---

## Fallback — JSON-LD Estático (se GTM inviável)

Se a equipe preferir injeção direta, usar os templates do arquivo `AIO-B1-AG01-breadcrumblist-jsonld.json`:

- **Produtos:** o tema Nuvemshop permite custom HTML por produto → colar no campo de código customizado de cada produto, ajustando a trilha conforme a categoria real do produto.
- **Categorias:** painel Nuvemshop → categoria → **Descrição** (permite HTML) antes da grade de produtos.

> ⚠️ O fallback exige edição por página e desatualiza quando o menu mudar. Prefira a tag GTM.

---

## Dados de Referência

| Campo | Valor |
|-------|-------|
| Base URL | https://www.lolaaviamentos.com.br |
| Menor trilha | `Início > Categoria` (2 níveis) |
| Maior trilha | `Início > Categoria > Subcategoria > Produto` (4 níveis) |
| Precedência | Não remover JSON-LD Product da Nuvemshop |

---

## ⚠️ Pontos de Atenção

1. **Slug vs nome exibido:** no JSON-LD o `name` usa o texto do menu (`Rasgo Fácil`, `Hidrossolúvel`), **não** a slug (`rasgo-facil`, `hidrossoluvel`). O script acima já usa `textContent` do crumb.
2. **www vs non-www:** o site canonicaliza non-www → www. O script normaliza URLs para `www.lolaaviamentos.com.br`.
3. **Home:** não é obrigatório ter Breadcrumb na home — pode deixar sem disparar a tag lá.
4. **Latência GTM:** via GTM o JSON-LD pode levar até 24h para o Google recriar o cache da página.