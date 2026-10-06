# AG-01 — JSON-LD BreadcrumbList Global — Lola Aviamentos

**Task Ekyte:** 10049804 — [AIO B1] BreadcrumbList schema global
**Cliente:** Lola Aviamentos
**Site:** https://www.lolaaviamentos.com.br
**Plataforma:** Nuvemshop (Tema Amazonas)
**GTM Container:** GTM-MQW27G8G
**Data de entrega:** 2026-08-10
**Status:** ✅ Pronto para implantação

---

## Resumo do Gargalo

| Item | Antes | Depois |
|------|-------|--------|
| BreadcrumbList schema | 0 em 142 páginas | 1 tag GTM → todas as páginas |
| Contexto hierárquico para LLMs | Nenhum | Trilha completa `Início > Categoria > Subcat > Produto` |
| Consistência com árvore real | — | Schema espelha o breadcrumb visível do tema Amazonas |

---

## Arquivos Entregues

| Arquivo | Descrição |
|---------|-----------|
| `AIO-B1-AG01-breadcrumblist-jsonld.json` | Árvore real de categorias + templates JSON-LD por tipo de página |
| `AIO-B1-AG01-breadcrumblist-gtm-guia.md` | Guia de implantação: script GTM global (recomendado) + fallback estático |
| `AIO-B1-AG01-breadcrumblist-entrega.md` | Este documento |

---

## O que foi feito

### 1. Validação da árvore real de categorias
Mapeei a estrutura viva do site (menu + breadcrumbs renderizados):

```
Início
├── Entretela de Memória            /entretela-de-memoria/
│   └── Cinza | Branca | Preta
├── Bordado                         /bordado1/
│   └── Filmes | Hidrossolúvel | Toque Macio | Termocolante | Rasgo Fácil
├── Entretelas para Alfaiataria     /entretela-alfaiataria/
│   └── Tecido Plano | Malha | TNT | Termocolante | Algodão
├── Insumos para Bonés              /insumos-para-bones/
│   └── Regulador | Tela | Suede | Aba Plástica | Viés
├── Acessórios                      /acessorios/
├── Máquinas para Confecção         /maquinas-acessorios/
└── Institucional                   /empresa/, /contato/, ...
```

### 2. Solução global via GTM
Uma única tag `Custom HTML` que lê os elementos `.breadcrumbs .crumb` já renderizados pelo tema e gera o JSON-LD `BreadcrumbList` dinâmico. Zero edição por página.

### 3. Templates estáticos de fallback
JSON-LD prontos para cada tipo de página (categoria nível 1, subcategoria por cluster, produto, institucional), com a profundidade real do site (2 a 4 níveis).

---

## Profundidade Validada

| Tipo de página | Trilha | Níveis |
|----------------|--------|--------|
| Categoria nível 1 | `Início > Entretela de Memória` | 2 |
| Subcategoria Bordado | `Início > Bordado > Rasgo Fácil` | 3 |
| Subcategoria Memória | `Início > Entretela de Memória > Cinza` | 3 |
| Subcategoria Bonés | `Início > Insumos para Bonés > Aba Plástica` | 3 |
| Produto | `Início > Bordado > Rasgo Fácil > [Produto]` | 4 |
| Institucional | `Início > Empresa` | 2 |

Máxima profundidade encontrada: **4 níveis** (produto). O script gera a trilha inteira automaticamente.

---

## Validação

| Ferramenta | URL | Status |
|------------|-----|--------|
| Schema Markup Validator | https://validator.schema.org/ | ✅ Templates sintaticamente válidos |
| Google Rich Results Test | https://search.google.com/test/rich-results | ⏳ Validar pós-implantação |

**Validação manual obrigatória após publicar:**
1. Testar `/bordado1/rasgo-facil/` no Rich Results Test → 3 níveis
2. Testar um produto → 4 níveis (breadcrumb + item final = URL do produto)
3. Testar `/entretela-de-memoria/cinza/` → 3 níveis
4. Confirmar 0 errors e 0 warnings

---

## Próximos Passos Relacionados

1. **AG-02 (task 10049803):** implanta os 4 definition blocks nas categorias — texto + BreadcrumbList juntos dão contexto hierárquico aos LLMs.
2. **AG-04 (futuro):** breadcrumbs + ItemList nas categorias (já especificado na auditoria §3.3).
3. Confirmar com o cliente que a tag GTM pode ser publicada no container do cliente.

---

---

## Reavaliação em 12/08/2026 — Schema já no ar, sem necessidade de acesso ao cliente

Revalidei o site ao vivo após o mapeamento das categorias. **O tema Amazonas já emite o JSON-LD `BreadcrumbList` nativamente em todas as páginas**, aninhado no schema `WebPage`/`Product` (válido no schema.org). Testei 19+ URLs: home, institucionais, todas as categorias nível 1, subcategorias e produtos.

| Página | Trilha nativa |
|--------|---------------|
| Home | `Início` |
| `/empresa/` | `Início > A Lola` |
| `/entretela-de-memoria/branca/` | `Início > Entretela de Memória > Branca` |
| `/bordado1/filmes/` | `Início > Bordado > Filmes` |
| `/rasgo-facil/` | `Início > Rasgo Fácil` |
| `/hidrossoluvel/` | `Início > Hidrossolúvel` |
| `/produtos/...` | `Início > Alfaiataria > TNT Termocolante > [Produto]` |

Observações:
- O registro de "0 páginas com BreadcrumbList" no delivery original foi um **falso negativo de método**: a checagem procurava um script `BreadcrumbList` de nível raiz, mas o tema emite o breadcrumb como propriedade do schema `WebPage`/`Product`, que é tecnicamente correto.
- As trilhas nativas já espelham a árvore real e **refletem a correção da 10049803**: `rasgo-facil` e `hidrossoluvel` aparecem na raiz (`Início > Rasgo Fácil`), não mais sob Bordado.
- Profundidade validada: 2 a 4 níveis, consistente com o mapeamento original.

**Conclusão:** o objectivo da task (schema presente em todas as páginas + contexto hierárquico para LLMs) **já está implementado no site hoje**. A tag GTM proposta em 10/08 não precisa ser publicada. **Não é necessário pedir acesso ao cliente** — a validação acima serve de evidência para fechamento da task.

*Entrega gerada em 10/08/2026 como parte do Bloco 1 (Fundação) do projeto AIO da Lola Aviamentos. Reavaliada em 12/08/2026.*