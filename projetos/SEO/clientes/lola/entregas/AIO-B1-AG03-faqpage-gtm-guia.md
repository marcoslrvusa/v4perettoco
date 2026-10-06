# AG-03 — Guia de Implementação FAQPage Schema (Template Base)

## Lola Aviamentos — https://www.lolaaviamentos.com.br/

**Task Ekyte:** 10049805 — [AIO B1] FAQPage schema - template base
**Plataforma:** Nuvemshop (Tema Amazonas)
**GTM Container:** GTM-MQW27G8G (já instalado no site)
**Status atual:** 0 páginas com FAQPage (sem conteúdo FAQ publicado ainda)
**Objetivo da task:** entregar o **template base validado** que será reaproveitado em todo o conteúdo do Bloco 2 (blog, guias, glossário, FAQs por cluster).

---

## Abordagem Recomendada: 1 Tag GTM Global + Blocos FAQ Visíveis

O FAQPage schema só gera rich results / citação por LLMs quando a página tem **conteúdo FAQ visível** (perguntas + respostas no DOM). A estratégia é:

1. O Bloco 2 publica o conteúdo FAQ como blocos visíveis usando uma **convenção de marcadores** (`data-faq`, `data-question`, `data-answer`).
2. **Uma única tag GTM** varre a página, lê os pares pergunta/resposta visíveis e injeta o JSON-LD `FAQPage` dinamicamente.
3. Zero edição por página, zero scripts por página, funciona para blog, guias, categorias e glossário automaticamente.

**Vantagens:**
- 1 tag para todo o site — todo conteúdo futuro com FAQ sai com schema automático
- O schema espelha **exatamente** o conteúdo visível (regra do Google: resposta no schema = texto na página)
- Consistente com a abordagem das tags BreadcrumbList e Product Schema já entregues

---

## Passo 1 — Convenção de marcação para o conteúdo FAQ (Bloco 2)

Ao criar conteúdo FAQ (categoria, blog, guia), estruturar assim:

```html
<div data-faq>
  <h3 data-question>O que é entretela de memória?</h3>
  <p data-answer>Entretela de memória é um tipo de entretela termocolante utilizada para forrar e estruturar peças, criando o efeito rebote (volta da forma). É muito usada na confecção de bonés, fardas e peças que precisam manter a estrutura após o uso.</p>

  <h3 data-question>Qual a diferença entre entretela de memória e entretela comum?</h3>
  <p data-answer>A entretela de memória tem a propriedade de retornar à forma original após ser amassada (efeito rebote), enquanto a entretela comum apenas reforça e estabiliza o tecido sem essa memória de forma.</p>
</div>
```

Regras:
- Cada pergunta em `<h3>` (ou `<h2>`) com `data-question`
- A resposta correspondente logo abaixo, no elemento com `data-answer`
- Perguntas e respostas precisam estar **visíveis** na página (schema reflete o que o usuário vê)

---

## Passo 2 — Criar a tag no GTM

**GTM > Tags > Nova:**

| Campo | Valor |
|---|---|
| Nome da tag | `Lola — FAQPage Schema (Global)` |
| Tipo de tag | **Custom HTML** |
| Trigger | **Todas as Páginas** (o próprio script só age onde houver blocos FAQ) |
| Advanced settings | Manter padrão — o script tem guarda anti-duplicidade |

Cole o código abaixo no campo **HTML**:

```html
<script>
(function () {
  if (window.__v4LolaFaqDone) return;
  var faqBlocks = document.querySelectorAll('[data-faq]');
  if (!faqBlocks.length) return;

  var questions = [];
  faqBlocks.forEach(function (block) {
    var items = block.querySelectorAll('[data-question], [data-answer]');
    var current = null;
    items.forEach(function (el) {
      if (el.hasAttribute('data-question')) {
        current = { name: el.textContent.trim(), answer: '' };
        questions.push(current);
      } else if (el.hasAttribute('data-answer') && current) {
        current.answer = el.textContent.trim();
      }
    });
  });

  var valid = questions.filter(function (q) {
    return q.name && q.answer && q.answer.length >= 10;
  });
  if (!valid.length) return;

  var schema = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    'mainEntity': valid.map(function (q) {
      return {
        '@type': 'Question',
        'name': q.name,
        'acceptedAnswer': { '@type': 'Answer', 'text': q.answer }
      };
    })
  };

  var s = document.createElement('script');
  s.type = 'application/ld+json';
  s.id = 'ld-json-faqpage';
  s.textContent = JSON.stringify(schema);
  document.head.appendChild(s);
  window.__v4LolaFaqDone = true;
})();
</script>
```

---

## Passo 3 — Publicar e validar

1. **Preview (GTM):** abrir uma página com bloco FAQ (ex.: categoria com o definition block + FAQ).
2. Conferir no painel do preview que há **um único** `script[type="application/ld+json"]` com `@type: FAQPage`.
3. Validar no **Rich Results Test** (https://search.google.com/test/rich-results) e no **validator** (https://validator.schema.org/) — 0 errors, 0 warnings.
4. Conferir que páginas **sem** bloco FAQ não ganham schema (a tag não dispara).
5. Publish com comentário: "FAQPage schema global a partir de blocos data-faq".

---

## Validação do Template (task)

O arquivo `AIO-B1-AG03-faqpage-template-jsonld.json` é o **template base** com 3 pares reais da auditoria §4.4 (FAQ — Entretela de Memória):

| # | Pergunta | Resposta |
|---|----------|----------|
| 1 | O que é entretela de memória? | Definição objetiva (efeito rebote, uso em bonés/fardas) |
| 2 | Qual a diferença entre entretela de memória e entretela comum? | Comparativo direto |
| 3 | Qual gramatura de entretela usar para boné? | Faixa 220g–330g com orientação |

Para adicionar pares novos no template: duplicar o objeto dentro de `mainEntity` e preencher `name` (pergunta) e `acceptedAnswer.text` (resposta).

---

## Notas e Atenção

1. **Schema deve refletir conteúdo visível** — regra do Google para FAQPage. Nunca injetar FAQ sem a pergunta/resposta estar na tela.
2. **FAQs por cluster (Bloco 2):** usar as perguntas já mapeadas na auditoria §4.4 (Entretela de Memória, Bordado, Insumos para Bonés).
3. **Precedência:** não remover o JSON-LD Product/Breadcrumb nativo da Nuvemshop — o FAQPage é complementar (`mainEntity` próprio, no `<head>`).
4. **LLMs:** o conteúdo FAQ visível em formato pergunta→resposta é citado ~3x mais pelos LLMs (estudo Authoritas 2025) — o schema reforça a extração estruturada.

---

*Gerado em 13/08/2026 · Bloco 1 (Fundação) — projeto Lola Aviamentos SEO/AIO.*
