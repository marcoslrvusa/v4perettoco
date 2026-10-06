# AG-02 — Definition Blocks nas 4 Páginas de Categoria — Lola Aviamentos

**Task Ekyte:** 10049803 — [AIO B1] Definition blocks nas 4 páginas de categoria
**Cliente:** Lola Aviamentos
**Site:** https://www.lolaaviamentos.com.br
**Plataforma:** Nuvemshop (Tema Amazonas)
**Data de entrega:** 2026-08-10
**Status:** ✅ Textos formatados e prontos para publicação

---

## Resumo do Gargalo

| Item | Antes | Depois |
|------|-------|--------|
| Definições explícitas para LLMs | 0 | 4 definition blocks visíveis (50-80 palavras) |
| Extractability (AEO/AIO) | Praticamente zero | 4 categorias com resposta direta + termo em negrito |
| Textos aprovados na auditoria | Redigidos em §4.2 | Formatados em HTML com termo principal em negrito |

---

## Arquivos Entregues

| Arquivo                                    | Descrição                                                                 |
| ------------------------------------------ | ------------------------------------------------------------------------- |
| `AIO-B1-AG02-definition-blocks.html`       | Blocos HTML prontos (preview visual + código) para cada uma das 4 páginas |
| `AIO-B1-AG02-definition-blocks-entrega.md` | Este documento                                                            |

---

## O que foi feito

1. **Textos preservados da auditoria** (não reescritos): `docs/auditoria-seo-aio-geo-completa.md` §4.2, que já tinham sido aprovados para implantação.
2. **Formatação aplicada** conforme a task: termo principal em **negrito**, 1-2 fatos objetivos por bloco, linguagem direta.
3. **Mapeamento para as 4 páginas reais** de categoria no site:

| Bloco                   | Página                     | Níveis do Breadcrumb                 |
| ----------------------- | -------------------------- | ------------------------------------ |
| Entretela de Memória    | `/entretela-de-memoria/`   | 2                                    |
| Entretela Rasgável      | `/bordado1/rasgo-facil/`   | 3 (Início > Bordado > Rasgo Fácil)   |
| Entretela Hidrossolúvel | `/bordado1/hidrossoluvel/` | 3 (Início > Bordado > Hidrossolúvel) |
| Insumos para Bonés      | `/insumos-para-bones/`     | 2                                    |

---

## Contagem de Palavras (padrão 50-80)

| Bloco | Palavras | Status |
|-------|----------|--------|
| Entretela de Memória | 67 | ✅ Dentro do padrão |
| Entretela Rasgável | 51 | ✅ Dentro do padrão |
| Entretela Hidrossolúvel | 54 | ✅ Dentro do padrão |
| Insumos para Bonés | 45 | ⚠️ 5 palavras abaixo do mínimo — texto aprovado, mantido como está (a task manda não reescrever) |

> **Nota:** o bloco de Insumos para Bonés ficou em 45 palavras. Como a task determina "não reescrever — apenas implantar o texto aprovado", o texto foi mantido integral. Se o cliente abrir espaço para extensão, a sugestão é adicionar 1-2 fatos objetivos (ex.: aplicação em confecções e onde é usado), sempre com aprovação prévia.

---

## Como Publicar (Nuvemshop)

1. Painel Nuvemshop → **Produtos → Categorias**
2. Abrir cada categoria e localizar o campo **"Descrição"** (também chamado de "Texto de apresentação" ou "Conteúdo da categoria")
3. Colar o bloco HTML correspondente (do arquivo `AIO-B1-AG02-definition-blocks.html`) **acima da grade de produtos**
4. Salvar e publicar

> O conteúdo é renderizado como texto visível (importante para LLMs) e integra com o BreadcrumbList (AG-01).

---

## Validação

- [ ] Bloco visível na página (rolagem até a grade de produtos)
- [ ] Termo principal em negrito (`<strong>`)
- [ ] Texto idêntico ao aprovado na auditoria §4.2
- [ ] Página de categoria renderiza sem erros de HTML

---

*Entrega gerada em 10/08/2026 como parte do Bloco 1 (Fundação) do projeto AIO da Lola Aviamentos.*