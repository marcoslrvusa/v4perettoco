# AG-03 — FAQPage Schema — Template Base — Lola Aviamentos

**Task Ekyte:** 10049805 — [AIO B1] FAQPage schema - template base
**Cliente:** Lola Aviamentos
**Site:** https://www.lolaaviamentos.com.br
**Plataforma:** Nuvemshop (Tema Amazonas)
**GTM Container:** GTM-MQW27G8G
**Data de entrega:** 2026-08-13
**Status:** ✅ Template validado e pronto para receber pares de pergunta e resposta

---

## Resumo do Gargalo

| Item | Antes | Depois |
|------|-------|--------|
| FAQPage schema | 0 em 142 páginas | Template base + tag GTM global pronta |
| Conteúdo FAQ visível | 0 (sem blog/FAQ publicado) | Convenção `data-faq` definida para o Bloco 2 |
| Extração por LLMs | FAQ citado ~3x mais (Authoritas 2025) — hoje zero | FAQPage estruturado quando o Bloco 2 publicar |

---

## Arquivos Entregues

| Arquivo | Descrição |
|---------|-----------|
| `AIO-B1-AG03-faqpage-template-jsonld.json` | **Template base validado** — FAQPage com 3 pares reais (auditoria §4.4, Entretela de Memória) |
| `AIO-B1-AG03-faqpage-gtm-guia.md` | Guia de implantação: 1 tag GTM global + convenção `data-faq` para o Bloco 2 |
| `AIO-B1-AG03-faqpage-entrega.md` | Este documento |

---

## O que foi feito

### 1. Template base validado (entregável principal da task)
- JSON-LD `FAQPage` com estrutura schema.org correta (`mainEntity > Question > acceptedAnswer.Answer`).
- 3 pares pergunta/resposta reais extraídos das **FAQs por cluster** já mapeadas na auditoria (§4.4 — Entretela de Memória), sem inventar dados.
- Validado: JSON parseável + estrutura schema.org confirmada.

### 2. Mecanismo reutilizável para todo o Bloco 2
- **Convenção de marcação** `data-faq` / `data-question` / `data-answer` para o conteúdo FAQ (categorias, blog, guias, glossário).
- **1 tag GTM global** que lê os blocos visíveis e injeta o JSON-LD dinamicamente — o conteúdo novo do Bloco 2 sai com FAQPage automaticamente, sem edição por página.
- Padrão consistente com as tags já entregues (BreadcrumbList global + Product Schema enriquecido).

### 3. Alinhamento com o Bloco 2
- As perguntas por cluster da auditoria (Entretela de Memória, Bordado, Insumos para Bonés) são o ponto de partida para os pares que o Bloco 2 vai preencher.
- O template aceita novos pares apenas duplicando objetos em `mainEntity`.

---

## Validação

| Verificação | Ferramenta | Status |
|-------------|-----------|--------|
| JSON válido | Parser local | ✅ |
| Estrutura schema.org (`Question`/`Answer`) | Validação local + spec | ✅ |
| Rich Results / validator | https://validator.schema.org/ · https://search.google.com/test/rich-results | ⏳ Validar com conteúdo visível no Bloco 2 |

---

## Próximos Passos

1. **Bloco 2:** criar os blocos FAQ visíveis (categorias/blog/guia) usando a convenção `data-faq`.
2. Publicar a tag GTM (após o cliente liberar acesso ao container).
3. Validar rich results em uma página com FAQ real.

---

*Entrega gerada em 13/08/2026 como parte do Bloco 1 (Fundação) do projeto AIO da Lola Aviamentos.*