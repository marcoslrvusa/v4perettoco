# Relatório — Product Schema nas 78 páginas de produto

**Task:** [AIO B1] Product schema - template em 78 páginas de produto  
**ID da task:** 10049802  
**Projeto:** Lola Aviamentos - SEO / AIO (Bloco 1 - Fundação)  
**Cliente:** Lola Aviamentos (Lola Soluções em Têxteis)  
**Plataforma:** Nuvemshop · Tema Amazonas  
**Executor:** Marcos Luciano  
**Responsável:** André Bock  
**Data:** 13/08/2026

---

## 1. Objetivo

Aplicar **Product schema por template único** (e não página a página) nas 78 páginas de produto, com os campos:

- `name`
- `image`
- `description`
- `sku`
- `brand`
- `offers` → `price`, `priceCurrency`, `availability`

**Objetivo de negócio:** permitir que os LLMs (ChatGPT, Gemini, Perplexity, AI Overviews) extraiam dados estruturados de produto para responder a buscas do tipo *"onde comprar entretela de memória"*.

---

## 2. Diagnóstico

	O tema Amazonas da Nuvemshop **já injeta JSON-LD `WebPage > mainEntity Product`** em todas as páginas de produto, via template único (`data-component='structured-data.page'`). Ou seja, o esqueleto do schema não precisava ser criado do zero.
	
	O gargalo real estava **nos dados** que alimentam os campos do schema:

| Problema encontrado | Impacto no schema |
|---|---|
| 21 produtos sem `seo_title` | `name` do schema raso/genérico |
| Erro de gramatura (produto 70g dizia "50g" no título e na description) | LLM extrai spec errada |
| Títulos truncados e genéricos ("Viés de Tecido", "Tecido Suede") | Extração pobre de atributos |
| 10 produtos com brand ausente ou incorreta | Campo `brand` vazio no schema |
| 3 produtos (26 variantes) sem SKU | Campo `sku` ausente no schema |
| `seo_description` sem nome/gramatura/referência | Campo `description` do schema sem valor extraível |

---

## 3. Ações executadas

Todas as alterações foram feitas via **API Nuvemshop (PUT parcial)** — apenas os campos alterados foram enviados, sem sobrescrever o restante do cadastro.

### 3.1 Títulos (`seo_title`) — 30 produtos

- 21 títulos vazios preenchidos com o nome completo do produto (gramatura + referência)
- Correção do erro de gramatura: produto **70g Lab-407/408** estava com "50g" no título
- Títulos genéricos curtos receberam especificação completa:
  - "Viés de Tecido" → *Viés Tecido Fosco 20mm*
  - "Tecido Suede" → *Tecido Suede 160g*
  - "Aba para Boné" → *Aba Plástica para Boné Curva 19,6kg AB-60*
- Títulos truncados reconstituídos com referência preservada (ex.: *Entretela Não Tecido para Bordado Toque Macio Rasgável 60g Lef-60*)
- 4 correções manuais (informação errada no cadastro):
  - Botão de Forrar / Encapar 13mm (estava 15mm)
  - Máquina de Pregar Botão Automática BP-1000 (estava "Encapar")
  - Máquina Transfer MT-1500 (título com dois-pontos)
  - Entretela Hidrossolúvel 40g (referência Laf-40)

### 3.2 Description (`seo_description`) — 77 produtos

Padrão AEO aplicado em todas:

> `{Nome completo com gramatura e referência}: {1ª frase factual do produto}. Compre na Lola Aviamentos.`

Exemplo (produto 70g):

> *Entretela de TNT (Micro Ponto) Termocolante 70g Lab-407/408: entretelas de Alfaiataria LAB são essenciais para quem busca durabilidade. Compre na Lola Aviamentos.*

**Regra de ouro seguida:** nenhuma informação correta foi inventada, alterada ou distorcida. A especificação (gramatura/referência) vem do **nome do produto** — a fonte de verdade do cadastro. O texto factual vem da primeira frase da descrição original.

### 3.3 Brand — 10 produtos

Normalizada para **Lola Soluções Têxteis**, unificando variações:
- vazia/`None` → `Lola Soluções Têxteis`
- "Lola Aviamentos" → `Lola Soluções Têxteis`
- nomes longos de marca → `Lola Soluções Têxteis`

### 3.4 SKU de variantes — 26 variantes / 3 produtos

Preenche o campo `sku` do schema nas páginas que estavam incompletas:

| Produto | Padrão | Exemplo |
|---|---|---|
| Regulador Plástico Proflex (8 cores) | `RPP-{COR}` | `RPP-PRETO`, `RPP-AZULMARINHO` |
| Entretela ETP algodão (16 combos gramatura × dimensão) | `ETP-{G}-{LA}x{CO}` | `ETP-105-030x050`, `ETP-170-150x100` |
| Base Máquina Transfer MT-1500 (curva/reta) | `BMT-1500-{TIPO}` | `BMT-1500-CURVA`, `BMT-1500-RETA` |

---

## 4. Validação final (78 URLs de produto)

| Métrica | Antes | Depois |
|---|---|---|
| Páginas com Product schema | 77 (69 completas) | **78/78** |
| Páginas incompletas (sku/brand) | 8 | **0** |
| Divergência de gramatura (título × description) | 1 | **0** |
| Páginas sem schema | 0 | **0** |

### Estrutura do schema resultante

```json
{
  "@type": "WebPage",
  "name": "Entretela de TNT (Micro Ponto) Termocolante 70g Lab-407/408",
  "description": "Entretela de TNT (Micro Ponto) Termocolante 70g Lab-407/408: ...",
  "mainEntity": {
    "@type": "Product",
    "name": "Entretela de TNT (Micro Ponto) Termocolante 70g Lab-407/408",
    "sku": "LAB-407/408",
    "brand": { "@type": "Brand", "name": "Lola Soluções Têxteis" },
    "image": "https://...",
    "description": "<seo_description>",
    "offers": {
      "price": "...",
      "priceCurrency": "BRL",
      "availability": "https://schema.org/InStock"
    }
  }
}
```

---

## 5. Observações

- **Rascunho não publicado** (TNT 60G-UNICA) foi mantido intacto.
- O fallback GTM (`AIO-B1-AG01-product-schema-competitivo-gtm.md`) segue disponível como **evolução opcional** para enriquecimento com variantes/AggregateOffer no nível competitivo — não é necessário para o schema básico desta task.
- Nenhuma informação correta do cadastro foi alterada; apenas campos vazios, errados ou genéricos foram preenchidos/corrigidos.
- O `seo_description` é a fonte do campo `description` do schema — por isso a otimização AEO dele impacta diretamente a extração por LLMs.

---

*Relatório gerado em 13/08/2026 · Builders Hub · Peretto&Co · Fluxo OFICIAL*
