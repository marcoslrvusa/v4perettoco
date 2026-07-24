# Auditoria SEO + AIO + GEO — Lola Aviamentos

**Site:** lolaaviamentos.com.br / www.lolaaviamentos.com.br
**Data:** 23 de julho de 2026
**Plataforma:** Nuvemshop (Loja Integrada)
**Empresa:** Lola Aviamentos — Importação e Distribuição de Insumos para Confecção (Entretelas, Aviamentos, Insumos para Bonés, Acessórios)
**Escopo:** Site completo (153 páginas HTML — 112 indexáveis, 41 não-indexáveis)
**Volume médio de palavras:** ~700/página | **Readability média:** Fairly Easy

---

## Sumário Executivo

| Pilar | Score | Status |
|-------|-------|--------|
| SEO Técnico | **1.5/10** | ❌ Crítico |
| SEO On-Page (Texto) | **2/10** | ❌ Crítico |
| Structured Data | **0/10** | 🚨 Zero schema |
| AIO / Extractability | **1/10** | ❌ Crítico |
| GEO / AI Search | **0/10** | 🚨 Zero presença |
| Segurança | **1/10** | ❌ Crítico |

**Score geral:** 0.9/10 — Severamente abaixo do mínimo para competir digitalmente.

### Problemas Críticos (ação imediata)

- 🚨 **0% das páginas com structured data** — sem Product, Organization, BreadcrumbList, FAQPage ou HowTo schema
- 🚨 **41 URLs non-indexable no sitemap (27,2%)** — desperdício de orçamento de rastreio
- 🚨 **255 imagens sem atributo alt (100%)** — falha grave de acessibilidade e SEO
- 🚨 **100% das páginas com headers de segurança ausentes** — X-Frame-Options, Referrer-Policy, CSP
- 🚨 **Títulos genéricos** — "Cinza", "Preta", "Branca", "Tela", "Tecidos", "A Lola", "Acessórios"
- 🚨 **Zero conteúdo informacional** — sem blog, sem FAQ, sem guias, sem glossário
- 🚨 **Zero presença em AI Search** — nenhuma citação em ChatGPT, Perplexity, Gemini ou AI Overviews
- 🚨 **Dupla versão do site** — non-www canonicalizando para www, mas ambas no sitemap

---

## PARTE 1 — SEO TÉCNICO

### 1.1 Arquitetura e Indexabilidade

#### Dupla Versão do Site

O site existe em duas versões concorrentes:

| Versão | URLs | Status |
|--------|------|--------|
| `lolaaviamentos.com.br` (non-www) | 41 URLs | Canonicalizadas para www |
| `www.lolaaviamentos.com.br` (www) | 112 URLs | Indexáveis |

| Métrica | Valor |
|---------|-------|
| Total HTML pages | 153 |
| Indexáveis (www) | 112 (73,2%) |
| Não-indexáveis | 41 (26,8%) |
| — Canonicalizadas | 32 |
| — Bloqueadas por robots.txt | 7 |
| — Client Error (4xx) | 2 |

**🚨 CRÍTICO:** 32 URLs non-www canonicalizadas para www mas **continuam no sitemap**. Isso confunde o Googlebot e desperdiça orçamento de rastreio.

#### Status Codes

| Status | Quantidade |
|--------|-----------|
| 200 OK | 407 |
| 301/302 Redirects | 35 |
| 404 | 3 |
| Blocked by robots.txt | 61 |

**⚠️ 3 URLs retornando 404** e **61 URLs bloqueadas por robots.txt** — problemas de rastreamento.

### 1.2 Sitemap

| Métrica | Valor |
|---------|-------|
| URLs no sitemap | 151 |
| Indexáveis no sitemap | 110 (72,8%) |
| **Não-indexáveis no sitemap** | **41 (27,2%)** |

**🚨 CRÍTICO:** URLs non-indexable no sitemap incluem:
- Versão non-www canonicalizada (32 URLs)
- URLs bloqueadas por robots.txt (7 URLs)
- URLs com erro 4xx (2 URLs)

### 1.3 Robots.txt

**7 URLs bloqueadas**, incluindo:
- `/account/register`
- `/search/?q=...` (páginas de busca interna)

### 1.4 Canonical Tags

A canonicalização está configurada corretamente (non-www → www) para 32 URLs, mas o problema é que ambas as versões estão no sitemap.

**Recomendação:** Escolher www como versão canônica definitiva e:
1. Remover todas as URLs non-www do sitemap
2. Implementar redirect 301 de non-www para www no .htaccess
3. Configurar o Search Console com a versão www como propriedade principal

### 1.5 Performance (PageSpeed / Core Web Vitals)

**⚠️ SEM DADOS DISPONÍVEIS.** O PageSpeed Insights não retornou dados para nenhuma URL. Necessário auditoria manual.

### 1.6 Segurança

| Header | Ausente em |
|--------|-----------|
| X-Frame-Options | 142 páginas (92,8%) |
| Referrer-Policy | 144 páginas (94,1%) |
| Content-Security-Policy | 2 páginas (1,3%) |
| HSTS | 2 páginas (1,3%) |
| Unsafe Cross-Origin Links | 142 páginas (100%) |
| Protocol-Relative Resource Links | 142 páginas (92,8%) |

**🚨 CRÍTICO:** 100% das páginas com unsafe cross-origin links (`target="_blank"` sem `rel="noopener"`). Vulnerabilidade a clickjacking (sem X-Frame-Options).

---

## PARTE 2 — SEO ON-PAGE (TEXTOS)

### 2.1 Page Titles

| Métrica | Valor |
|---------|-------|
| Total de titles únicos | 142 |
| Média de caracteres | 37 chars |
| Títulos < 30 chars | **35 (24,6%)** |
| Títulos > 60 chars | **13 (9,2%)** |
| Títulos > 561 pixels | **18 (12,7%)** |
| Títulos < 200 pixels | **26 (18,3%)** |
| **Títulos duplicados** | **12 (8,5%)** |
| Titles iguais ao H1 | **46 (32,4%)** |

#### Exemplos de Títulos Problemáticos

| URL | Title Atual | Problema |
|-----|------------|----------|
| `/entretela-de-memoria/cinza/` | **"Cinza"** (5 chars) | Só a cor — sem contexto de produto/marca |
| `/entretela-de-memoria/branca/` | **"Branca"** (6 chars) | Idem |
| `/entretela-de-memoria/preta/` | **"Preta"** (6 chars) | Idem |
| `/insumos-para-bones/tela/` | **"Tela"** (6 chars) | Genérico — não especifica para boné |
| `/insumos-para-bones/suede1/` | **"Tecidos"** (7 chars) | Não fala de Suede |
| `/insumos-para-bones/vies1/` | **"Viés"** (6 chars) | Sem contexto de boné |
| `/acessorios/` | **"Acessórios"** (10 chars) | Genérico |
| `/bordado1/` | **"Bordado"** (7 chars) | Sem qualificação |
| `/empresa/` | **"A Lola"** (6 chars) | Sem descritivo |

#### Titles Recomendados (10 prioridades)

| URL Atual | Atual | Recomendado |
|-----------|-------|-------------|
| `/entretela-de-memoria/cinza/` | "Cinza" | "Entretela de Memória Cinza Termocolante | Lola Aviamentos" |
| `/entretela-de-memoria/branca/` | "Branca" | "Entretela de Memória Branca Termocolante | Lola Aviamentos" |
| `/entretela-de-memoria/preta/` | "Preta" | "Entretela de Memória Preta Termocolante | Lola Aviamentos" |
| `/bordado1/` | "Bordado" | "Entretelas para Bordado Profissional | Lola Aviamentos" |
| `/insumos-para-bones/tela/` | "Tela" | "Tela de Poliéster Mesh para Boné | Lola Aviamentos" |
| `/insumos-para-bones/suede1/` | "Tecidos" | "Tecido Suede para Boné e Estofados | Lola Aviamentos" |
| `/insumos-para-bones/vies1/` | "Viés" | "Viés para Boné (Carneira) | Lola Aviamentos" |
| `/acessorios/` | "Acessórios" | "Acessórios para Confecção Profissional | Lola Aviamentos" |
| `/empresa/` | "A Lola" | "Lola Aviamentos: Entretelas, Insumos e Aviamentos para Confecção" |
| `/entretela-alfaiataria/termocolante1/` | "Entretela de tecido" | "Entretela Termocolante para Alfaiataria e Camisaria | Lola" |

### 2.2 Meta Descriptions

| Métrica | Valor |
|---------|-------|
| Média de caracteres | 71 chars |
| Meta desc < 50 chars | Várias (muito curtas) |
| Meta desc > 155 chars | **36 (25,4%)** |
| Meta desc duplicadas | **45 (31,7%)** |
| Meta desc ausentes | **2 (1,4%)** |

**🚨 45 meta descriptions duplicadas (31,7%):** Muitas páginas de produto compartilham a mesma descrição genérica de categoria. Ex: "A entretela de memória..." aparece em 5+ páginas diferentes.

### 2.3 Headings (H1/H2)

| Métrica | Valor |
|---------|-------|
| H1 non-sequential | **109 (76,8%)** |
| H1 duplicado | **2 (1,4%)** |
| H1 > 70 chars | **1 (0,7%)** |
| H2 duplicado | **110 (77,5%)** |
| H2 múltiplos | **78 (54,9%)** |
| H2 non-sequential | **78 (54,9%)** |

**⚠️ Problemas estruturais graves:**
- **109 páginas (76,8%)** com H1 non-sequential — hierarquia quebrada
- **110 páginas (77,5%)** com H2 duplicado — conteúdo repetitivo
- **78 páginas (54,9%)** com H2 múltiplos e non-sequential
- Provável causa: Nuvemshop gera headings automaticamente sem hierarquia correta

#### Análise Detalhada de Headings da Homepage (www)

| Heading | Texto | Observação |
|---------|-------|------------|
| H1 | Lola Aviamentos - Entretelas para confecções e insumos para Bonés | OK como H1, mas poderia incluir "aviamentos" e "acessórios" |
| H2 | Total: R$0,00 | **ERRO** — valor de carrinho como heading |
| H2 | Mais vendidos | Seção de produtos — OK, sem keyword relevante |
| H2 | (produtos individuais como H2) | Produtos como H2 sem contexto descritivo |

**Problema:** A homepage tem apenas 1 H1 e 2 H2s reais. A estrutura semântica é extremamente pobre para uma página que deveria comunicar o portfólio completo.

### 2.4 Conteúdo e Readability

| Métrica | Valor |
|---------|-------|
| Média de palavras por página | ~700 palavras |
| Média Flesch Score | ~72 (Fairly Easy) |

| Nível | Páginas | % |
|-------|---------|---|
| Fairly Easy | 86 | 60,6% |
| Normal | 23 | 16,2% |
| Easy | 19 | 13,4% |
| Very Easy | 11 | 7,7% |
| Fairly Hard | 2 | 1,4% |
| Hard | 1 | 0,7% |

**Análise:** Conteúdo majoritariamente "Fairly Easy" — adequado para e-commerce B2B. Mas as descrições de produto são curtas e genéricas, contribuindo para a alta taxa de duplicação.

### 2.5 Imagens

| Métrica | Valor |
|---------|-------|
| Total de imagens | 255 |
| Formatos: WebP | 231 (90,6%) |
| **Imagens sem atributo alt** | **255 (100%)** |
| Imagens sem size attributes | **129 (50,6%)** |
| Imagens > 100 KB | **48 (18,8%)** |

**🚨 CRÍTICO: 100% das imagens sem alt text.** Falha grave de acessibilidade (WCAG) e SEO.

### 2.6 Links Internos

| Métrica | Valor |
|---------|-------|
| Total internal links | 360 |
| Internal outlinks sem anchor text | 142 (100%) |
| Anchor texts principais | "Mais Vendidos" (62,75%), "Comprar" (11,76%) |

**⚠️ Links internos pobres:** 100% dos internal outlinks sem anchor text descritivo. Os únicos anchor texts são "Mais Vendidos" e "Comprar" — sem contexto semântico.

---

## PARTE 3 — STRUCTURED DATA (SCHEMA MARKUP)

### 3.1 Situação Atual

| Métrica | Valor |
|---------|-------|
| Páginas COM structured data | **0 (0%)** |
| Páginas SEM structured data | **142 (100%)** |

**🚨 CRÍTICO: Zero schema markup em todo o site.** Nenhum tipo de schema:
- ❌ Sem Organization
- ❌ Sem LocalBusiness / Store
- ❌ Sem Product (imperdoável para e-commerce com 78 páginas de produto)
- ❌ Sem BreadcrumbList
- ❌ Sem FAQPage
- ❌ Sem HowTo
- ❌ Sem ItemList
- ❌ Sem Review / AggregateRating

### 3.2 Schema Obrigatório (P0 — Implementação Imediata)

#### Organization + Store

```json
{
  "@context": "https://schema.org",
  "@type": "Store",
  "name": "Lola Aviamentos",
  "url": "https://www.lolaaviamentos.com.br",
  "logo": "https://acdn-us.mitiendanube.com/stores/001/720/481/themes/common/logo-2381817-1754682754-c325014e3710438c242fa3453bf903381754682754-480-0.webp",
  "description": "Importação e distribuição de entretelas, aviamentos, insumos para bonés e acessórios para confecção profissional.",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Apucarana",
    "addressRegion": "PR",
    "addressCountry": "BR"
  },
  "email": "contato@lolaaviamentos.com.br",
  "priceRange": "$$",
  "sameAs": [
    "https://www.instagram.com/lolaaviamentos/",
    "https://www.facebook.com/lolaaviamentos"
  ]
}
```

#### Product (para cada página de produto — template)

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Entretela Não Tecido para Bordado Rasgável 40g",
  "description": "Entretela rasgável para bordado, 40g, 90cm x 200m. Remoção fácil puxando a peça.",
  "sku": "LEC-40",
  "category": "Entretelas para Bordado",
  "material": "Poliéster",
  "offers": {
    "@type": "Offer",
    "price": "175.00",
    "priceCurrency": "BRL",
    "availability": "https://schema.org/InStock",
    "url": "https://www.lolaaviamentos.com.br/produtos/entretela-para-bordado-rasgavel-40g-90cm-200m/"
  }
}
```

### 3.3 Schema Avançado (P1 — 30 dias)

#### BreadcrumbList (em todas as páginas)

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [{
    "@type": "ListItem",
    "position": 1,
    "name": "Home",
    "item": "https://www.lolaaviamentos.com.br/"
  }, {
    "@type": "ListItem",
    "position": 2,
    "name": "Entretela de Memória",
    "item": "https://www.lolaaviamentos.com.br/entretela-de-memoria/"
  }, {
    "@type": "ListItem",
    "position": 3,
    "name": "Entretela de Memória Cinza",
    "item": "https://www.lolaaviamentos.com.br/entretela-de-memoria/cinza/"
  }]
}
```

#### ItemList (para categorias e página inicial)

```json
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Entretelas para Bordado" },
    { "@type": "ListItem", "position": 2, "name": "Entretela de Memória" },
    { "@type": "ListItem", "position": 3, "name": "Entretelas para Alfaiataria" },
    { "@type": "ListItem", "position": 4, "name": "Insumos para Bonés" },
    { "@type": "ListItem", "position": 5, "name": "Acessórios" }
  ]
}
```

### Matriz Schema por Tipo de Página

| Tipo de Página | Schema | Prioridade | Impacto |
|----------------|--------|------------|---------|
| Homepage | Organization + Store + ItemList + BreadcrumbList | P0 | Alto |
| Categoria | BreadcrumbList + ItemList | P0 | Alto |
| Produto | Product + BreadcrumbList | P0 | Crítico |
| Empresa/Sobre | Organization + Store | P0 | Alto |
| Blog/Conteúdo (futuro) | Article + FAQPage + HowTo | P1 | Alto |
| Contato | LocalBusiness + ContactPoint | P1 | Médio |

---

## PARTE 4 — AIO (EXTRACTABILITY PARA AI SEARCH)

### 4.1 O Conteúdo Atual é Amigável para LLMs?

**Avaliação geral: 1/10** — Extractability praticamente zero.

#### Problemas Identificados

1. **Zero definições explícitas:** LLMs (ChatGPT, Perplexity, Gemini, Claude) precisam de conteúdo que responda perguntas de forma direta. O site não tem frases como "Entretela de memória é um tipo de entretela termocolante utilizada para..." ou "Entretela rasgável é um material não tecido que..."

2. **Zero estrutura de perguntas e respostas:** Não há FAQ, Q&A, ou qualquer formato de pergunta explícita seguida de resposta. LLMs citam conteúdo em formato FAQ com 3x mais frequência (estudo Authoritas, 2025).

3. **Parágrafos muito curtos para citação:** Média de 2-4 palavras por sentença. LLMs precisam de 50-120 palavras por parágrafo para considerar uma fonte citável.

4. **Descrições de produto genéricas e duplicadas:** 45 meta descriptions duplicadas significam que o Google provavelmente ignora todas. LLMs também percebem conteúdo duplicado como de baixa autoridade.

5. **Sem dados técnicos numéricos:** Gramaturas (30g, 40g, 50g, 105g, 160g, 220g, 285g, 330g) existem nos produtos mas não em formato de conteúdo informacional que LLMs possam citar.

6. **Zero autoridade temática:** Sem blog, sem guias, sem artigos, sem glossário — o site não estabelece knowledge graph algum.

7. **Zero schema de conteúdo:** FAQPage, HowTo, QAPage, Article — nenhum presente.

### 4.2 Estratégia "Extractability First" para Lola

#### Definition Blocks (adicionar em cada categoria)

**Entretela de Memória:**
> Entretela de memória é um tipo de entretela termocolante fabricada em não tecido (TNT) com resina termofusível em um dos lados. Também conhecida como entretela cavalinho, é amplamente utilizada na fabricação de bonés, viseiras e acessórios estruturados. Disponível em gramaturas que variam de 220g a 330g, nas cores branca, cinza e preta. A ativação térmica ocorre entre 130°C e 160°C com prensa térmica ou ferro de passar.

**Entretela Rasgável:**
> Entretela rasgável (ou de rasgo fácil) é um tipo de entretela não tecido descartável utilizada como base para bordado computadorizado. Após o bordado, é removida manualmente puxando-a da peça, sem necessidade de água ou produtos químicos. Ideal para bordados em camisetas, uniformes e tecidos delicados. Gramaturas comuns: 30g, 40g e 50g.

**Entretela Hidrossolúvel:**
> Entretela hidrossolúvel é um filme plástico à base de PVA (álcool polivinílico) que se dissolve em água. Utilizada como base para bordados onde o tecido não pode ser danificado por remoção mecânica — ideal para bordados em toalhas, tecidos felpudos e peças com aviamentos delicados. A dissolução ocorre em água a partir de 40°C.

**Insumos para Bonés:**
> Insumos para bonés são todos os componentes necessários para a fabricação de bonés personalizados ou prontos. Incluem aba plástica (curva ou reta), regulador plástico (snapback ou proflex), tela de poliéster (mesh ou fechada), viés de carneira, tecido suede, botão de forrar e case para bonés.

#### FAQs por Cluster (adicionar como conteúdo visível + FAQPage schema)

**FAQ — Entretela de Memória:**
- O que é entretela de memória?
- Qual a diferença entre entretela de memória e entretela comum?
- Qual gramatura de entretela usar para boné?
- Como aplicar entretela termocolante de memória?
- Onde comprar entretela de memória por atacado?

**FAQ — Entretela para Bordado:**
- Qual a diferença entre entretela rasgável e hidrossolúvel?
- Como usar entretela hidrossolúvel no bordado?
- Qual entretela usar para bordado em camiseta?
- O que significa a gramatura da entretela (30g, 40g, 50g)?
- Onde comprar entretela para bordado profissional?

**FAQ — Insumos para Bonés:**
- Quais insumos preciso para fabricar bonés?
- Qual a diferença entre aba plástica curva e reta?
- Como colocar regulador plástico em boné?
- Qual tela usar para boné (mesh vs poliéster)?
- Como escolher fornecedor de insumos para bonés?

#### How-To Steps (formato preferido de LLMs)

**How-To 1: Como aplicar entretela termocolante em bonés**
1. Corte a entretela no formato da frente do boné
2. Posicione a entretela com o lado termocolante (áspero) virado para o tecido
3. Aplique pressão com prensa térmica a 150°C por 10-15 segundos
4. Deixe esfriar por 30 segundos antes de manusear
5. Verifique a aderência puxando suavemente uma ponta

**How-To 2: Como usar filme hidrossolúvel no bordado**
1. Posicione o filme hidrossolúvel sobre o tecido a ser bordado
2. Fixe com bastidor garantindo que o filme fique esticado
3. Borde normalmente sobre o filme
4. Após o bordado, mergulhe a peça em água morna (40°C)
5. Aguarde 30-60 segundos até o filme se dissolver completamente
6. Seque a peça e finalize o acabamento

**How-To 3: Como escolher a gramatura ideal de entretela**
1. Identifique o tipo de peça: bonés (220g-330g), camisetas (30g-40g), alfaiataria (60g-70g)
2. Considere o tecido base: tecidos leves exigem entretela leve
3. Verifique a estrutura desejada: mais estruturado = maior gramatura
4. Teste em um pedaço do tecido antes da produção em lote
5. Consulte a tabela de compatibilidade do fornecedor

### 4.3 Guias Pilares para LLM Authority

| # | Guia Pilar | Palavras | Cluster | Schema |
|---|-----------|----------|---------|--------|
| 1 | Tipos de Entretela para Bordado: Guia Completo | 2.500+ | Bordado | Article + FAQPage |
| 2 | Entretela de Memória: O que é, Como Usar e Qual Escolher | 2.000+ | Entretela Memória | Article + FAQPage + HowTo |
| 3 | Insumos para Bonés: Guia Completo para Fabricantes | 3.000+ | Insumos Bonés | Article + FAQPage + HowTo |
| 4 | Entretela Rasgável vs Hidrossolúvel: Diferenças | 1.500+ | Bordado | Article + FAQPage |
| 5 | Entretela para Alfaiataria: Tipos e Aplicações | 2.000+ | Alfaiataria | Article + FAQPage |
| 6 | Como Montar uma Fábrica de Bonés: Lista de Insumos | 2.500+ | Insumos Bonés | Article + HowTo |

### 4.4 Glossário Técnico (Autoridade Temática + LLM Citation)

**Glossário de Entretelas** (20+ termos técnicos):
- Entretela, entretela termocolante, entretela costurável, entretela de memória, entretela cavalinho, entretela rasgável, entretela de toque macio, entretela hidrossolúvel, entretela não tecido, TNT termocolante, gramatura (g/m²), ponto de fusão, resina termofusível, filme hidrossolúvel (PVA), filme plástico para bordado, entretela dupla face, entretela de malha, entretela de tecido plano, entretela de algodão, entretela de poliéster

**Glossário de Insumos para Bonés** (15+ termos):
- Aba plástica, aba curva, aba reta, regulador plástico, snapback, proflex, tela mesh, tela de poliéster, viés de carneira, viés para boné, tecido suede, botão de forrar, case para bonés, medidor de circunferência, fita de regulagem

---

## PARTE 5 — GEO / AI SEARCH (OTIMIZAÇÃO PARA MECANISMOS DE RESPOSTA)

### 5.1 Presença Atual em AI Search

**Avaliação: 0/10** — Nenhuma presença.

- ❌ Zero citações em ChatGPT
- ❌ Zero citações em Perplexity
- ❌ Zero citações em Google AI Overviews
- ❌ Zero citações em Gemini / Claude / Copilot
- ❌ Sem Google Business Profile otimizado
- ❌ Sem domínio de referência (backlinks)
- ❌ Sem conteúdo em formato de resposta direta

### 5.2 Oportunidades de AI Search por Cluster

#### Cluster Entretela de Memória

| Pergunta | Volume Est. | Oportunidade | Tipo de Conteúdo |
|----------|-------------|--------------|------------------|
| O que é entretela de memória? | 320/mês | ★★★★★ | Definition block + FAQ |
| Qual a diferença entre entretela de memória e entretela comum? | 90/mês | ★★★★ | FAQ comparativo |
| Qual gramatura de entretela usar para boné? | 130/mês | ★★★★★ | How-To + tabela |
| Como aplicar entretela termocolante em bonés? | 200/mês | ★★★★★ | How-To schema |
| Onde comprar entretela de memória por atacado? | 100/mês | ★★★★ | Local + página de categoria |

#### Cluster Bordado

| Pergunta | Volume Est. | Oportunidade | Tipo de Conteúdo |
|----------|-------------|--------------|------------------|
| Qual a melhor entretela para bordado? | 240/mês | ★★★★★ | Guia comparativo |
| Diferença entre entretela rasgável e hidrossolúvel? | 110/mês | ★★★★★ | Tabela comparativa |
| Como usar filme hidrossolúvel no bordado? | 140/mês | ★★★★★ | How-To schema |
| O que é entretela termocolante? | 280/mês | ★★★★★ | Definition block |
| Como fazer bainha sem costura? | 400/mês | ★★★★★ | How-To + FAQ |

#### Cluster Insumos para Bonés

| Pergunta | Volume Est. | Oportunidade | Tipo de Conteúdo |
|----------|-------------|--------------|------------------|
| Quais insumos para fabricar bonés? | 150/mês | ★★★★★ | Lista + guia |
| Como montar uma fábrica de bonés? | 210/mês | ★★★★ | Guia completo |
| Qual a diferença entre aba curva e reta? | 80/mês | ★★★★ | FAQ + tabela |
| Onde comprar insumos para bonés? | 130/mês | ★★★★ | Local + página de categoria |

### 5.3 Estratégia de Citação em LLMs

Para aparecer nas respostas de IA, a Lola precisa:

1. **Criar conteúdo definitivo** — o guia mais completo em português sobre entretelas e insumos para bonés
2. **Estruturar em FAQ com FAQPage schema** — LLMs priorizam FAQPage estruturado
3. **Incluir How-To steps** — ChatGPT e Perplexity citam passos práticos com frequência
4. **Usar definition blocks** — parágrafos de 50-80 palavras que começam respondendo diretamente à pergunta
5. **Incluir dados técnicos** — gramaturas, temperaturas, medidas, composições
6. **Criar página "Sobre" com autoridade** — quem é a Lola, há quanto tempo atua, portfólio, diferenciais

### 5.6 Métricas de AI Search (Baseline vs Meta 90d)

| Métrica | Atual | Meta 90d |
|---------|-------|----------|
| AI Citation Count (total) | 0 | 10+ |
| Perguntas com resposta própria | 0 | 15+ |
| Páginas com FAQPage schema | 0 | 5 |
| Páginas com HowTo schema | 0 | 6 |
| Extractability Score | 10% | 70%+ |
| Conteúdo em formato de resposta direta | 0 | 10+ peças |

---

## PARTE 6 — MAPA DE KEYWORDS

### 6.1 Keywords Head (Alta Busca)

| Keyword | Volume Est. | Intenção | Cluster | Prioridade |
|---------|-------------|----------|---------|------------|
| entretela para bordado | 2.400/mês | Transacional | Bordado | P0 |
| aviamentos | 3.600/mês | Navegacional | Geral | P0 |
| patchwork | 2.600/mês | Informacional | Bordado | P1 |
| tecido para boné | 2.200/mês | Transacional | Insumos Bonés | P0 |
| entretela termocolante | 1.900/mês | Comercial | Bordado/Alfaiataria | P0 |
| fita mágica | 1.800/mês | Transacional | Acessórios | P1 |
| insumos para bonés | 1.600/mês | Transacional | Insumos Bonés | P0 |
| entretela de memória | 1.300/mês | Comercial | Entretela Memória | P0 |

### 6.2 Keywords Middle (Oportunidade Imediata)

| Keyword | Volume Est. | Intenção | Cluster | Gap Atual |
|---------|-------------|----------|---------|-----------|
| entretela rasgável | 720/mês | Comercial | Bordado | ❌ Só em titles de produto duplicados |
| entretela hidrossolúvel | 590/mês | Comercial | Bordado | ❌ Subcategoria sem qualificação |
| aba plástica para boné | 480/mês | Transacional | Insumos Bonés | ❌ Subcategoria sem contexto |
| entretela não tecido | 440/mês | Comercial | Bordado | ❌ 15+ repetições no mesmo title |
| tecido suede | 410/mês | Transacional | Insumos Bonés | ❌ Subcategoria chamada "Tecidos" |
| regulador plástico para boné | 390/mês | Transacional | Insumos Bonés | ✅ Única subcategoria bem nomeada |
| tela de poliéster para boné | 350/mês | Transacional | Insumos Bonés | ❌ Subcategoria chamada "Tela" |
| entretela de memória colorida | 320/mês | Comercial | Entretela Memória | ❌ Titles "Cinza", "Branca", "Preta" |
| viés para boné | 280/mês | Transacional | Insumos Bonés | ❌ Subcategoria chamada "Viés" |

### 6.3 Gaps Críticos de Keyword

| Keyword | Volume | Por que deveria rankear | Status |
|---------|--------|------------------------|--------|
| entretela para bordado | 2.400/mês | Core business | Não aparece em title/H1 de categoria |
| aviamentos para confecção | 1.100/mês | Termo do segmento | Zero menção |
| bordado computadorizado | 990/mês | Público-alvo | Zero menção |
| entretela para alfaiataria | 880/mês | Core business | Pilar existe mas H1 genérico |
| entretela cavalinho | 400/mês | Nome popular do produto | Zero menção |
| como fazer bainha sem costura | 400/mês | Informacional | Zero conteúdo |
| como fazer patchwork | 600/mês | Informacional | Zero conteúdo |
| o que é entretela de memória | 320/mês | Informacional | Zero conteúdo |
| o que é entretela termocolante | 280/mês | Informacional | Zero conteúdo |
| como montar uma fábrica de bonés | 210/mês | Informacional | Zero conteúdo |

### 6.4 Cluster de Entidades (para AI Search)

Para aparecer em respostas de IA, o site precisa estabelecer estas entidades e relacionamentos:

```
[Lola Aviamentos] — tipo: [Store] — localização: [Apucarana, PR]
  → importa e distribui → [Insumos para Confecção]
    → categoria: [Entretelas]
      → tipos: [Memória] [Rasgável] [Toque Macio] [Hidrossolúvel] [Termocolante] [Dupla Face]
      → gramaturas: [30g] [40g] [50g] [60g] [70g] [105g] [160g] [220g] [285g] [330g]
    → categoria: [Insumos para Bonés]
      → tipos: [Aba Plástica] [Regulador] [Tela Mesh] [Viés] [Suede] [Botão] [Case]
    → categoria: [Acessórios]
      → tipos: [Fita Mágica] [Cortador] [Medidor] [Aparelho de Bronze]
    → categoria: [Alfaiataria]
      → tipos: [Tecido Plano] [Algodão] [TNT] [Malha]
  → atende → [Confecções] [Bonés Personalizados] [Ateliês] [Indústria Têxtil]
  → público → [Fabricantes] [Profissionais de Costura] [Bordadeiras] [Personalizadores]
```

Cada entidade deve ser mencionada pelo menos 2-3 vezes no texto visível do site.

---

## PARTE 7 — RECOMENDAÇÃO DETALHADA: TEXTO PURO vs SCHEMA ESTRUTURADO

### 7.1 Estratégia Híbrida

A abordagem correta é **texto + schema**, onde o schema é subordinado ao texto e ambos falam a mesma língua semântica.

| Elemento | Texto Visível | Schema | Prioridade |
|----------|--------------|--------|------------|
| Homepage | H1 + parágrafo de introdução (100 palavras) + lista de categorias | Store + ItemList | P0 |
| Categoria | Descrição editorial de 100-150 palavras + lista de produtos | BreadcrumbList + ItemList | P0 |
| Produto | Descrição técnica de 80-120 palavras + especificações | Product | P0 |
| Página "Empresa" | Quem somos (200-300 palavras) com história e diferenciais | Store + LocalBusiness | P0 |
| Guia Pilar (blog) | Artigo de 2.000+ palavras com FAQ embutido | Article + FAQPage | P1 |
| Tutorial (blog) | Passo a passo com imagens | Article + HowTo | P1 |
| Glossário | Definições de 20+ termos técnicos | Article + FAQPage (se Q&A) | P1 |
| FAQ page | 10 perguntas com respostas visíveis | FAQPage | P1 |
| Contato | Endereço, telefone, email, formulário | Store + ContactPoint | P1 |

### 7.2 Exemplos Práticos para Lola

**Exemplo — Página de Categoria "Entretela de Memória Cinza"**

> **Texto Visível (H1 + P):**
> ### Entretela de Memória Cinza Termocolante
> A entretela de memória cinza é um material não tecido (TNT) com resina termofusível, amplamente utilizado como estruturação para bonés, viseiras e acessórios. Também chamada de entretela cavalinho, está disponível em três gramaturas: 220g (ideal para bonés leves), 285g (uso padrão em bonés estruturados) e 330g (para bonés de alta estruturação). A ativação térmica ocorre entre 130°C e 160°C, com prensa térmica ou ferro a seco. Venda por metro ou por rolo, com largura de 90cm.
>
> **Schema Correspondente:**
> ```json
> {
>   "@context": "https://schema.org",
>   "@type": "Product",
>   "name": "Entretela de Memória Cinza Termocolante",
>   "description": "Entretela não tecido termocolante para estruturação de bonés, viseiras e acessórios. Disponível em 220g, 285g e 330g.",
>   "category": "Entretela de Memória",
>   "color": "Cinza",
>   "material": "TNT com resina termofusível"
> }
> ```

**Exemplo — Bloco FAQ na Homepage**

> **Texto Visível:**
> ### Perguntas Frequentes sobre Entretelas
> **O que é entretela de memória?**
> Entretela de memória é um TNT termocolante usado para estruturar bonés, viseiras e acessórios. Disponível em 220g, 285g e 330g.
>
> **Qual a diferença entre entretela rasgável e hidrossolúvel?**
> A entretela rasgável é removida manualmente após o bordado, enquanto a hidrossolúvel se dissolve em água morna. A rasgável é ideal para tecidos resistentes, a hidrossolúvel para tecidos delicados e felpudos.
>
> **Como escolher a gramatura ideal de entretela?**
> Para bonés: 220g-330g. Para bordado em camisetas: 30g-40g. Para alfaiataria: 60g-70g.

> **FAQPage Schema** (mesmo conteúdo em JSON-LD no `<head>`)

---

## PARTE 8 — PLANO DE AÇÃO PRIORIZADO

### P0 — Hoje (Implementação Imediata)

| # | Tarefa | Esforço | Impacto | Detalhamento |
|---|--------|---------|---------|--------------|
| 1 | Remover 41 URLs non-indexable do sitemap | 1h | 🚨 Crítico | Parar de incluir URLs non-www + blocked + 4xx |
| 2 | Implementar Product schema nas 78 páginas de produto | 4h | 🚨 Crítico | Template JSON-LD por página de produto |
| 3 | Adicionar Organization + Store schema na homepage + empresa | 1h | 🚨 Crítico | JSON-LD com dados da Lola |
| 4 | Renomear 10 títulos críticos (< 30 chars) | 2h | 🔴 Alto | "Cinza" → "Entretela de Memória Cinza Termocolante | Lola" |
| 5 | Adicionar alt text em 255 imagens | 8h | 🔴 Alto | Alt text descritivo para cada imagem de produto |
| 6 | Corrigir 2 páginas com erro 4xx | 1h | 🔴 Alto | Identificar e redirecionar ou remover |

### P1 — 1 a 2 Semanas (Textos + Schema + Conteúdo)

| # | Tarefa | Esforço | Impacto | Detalhamento |
|---|--------|---------|---------|--------------|
| 7 | Escrever descrições editoriais para 5 categorias-pilar | 4h | 🔴 Alto | Entretela Memória, Bordado, Bonés, Alfaiataria, Acessórios |
| 8 | Corrigir 12 títulos duplicados | 2h | 🔴 Alto | Diferenciar páginas com mesmo title |
| 9 | Corrigir 45 meta descriptions duplicadas | 4h | 🔴 Alto | Descrições únicas por página |
| 10 | Adicionar BreadcrumbList schema em todas as páginas | 2h | 🟡 Médio | Navegação estruturada |
| 11 | Corrigir headings H1/H2 (109 páginas non-sequential) | 6h | 🟡 Médio | Ajustar hierarquia semântica |
| 12 | Implementar redirect 301 de non-www para www | 1h | 🟡 Médio | .htaccess + canonical definitivo |
| 13 | Criar page "Empresa" com conteúdo completo | 3h | 🟡 Médio | História, diferenciais, valores, equipe |

### P2 — 30 a 60 Dias (Conteúdo AEO/GEO)

| # | Tarefa | Esforço | Impacto | Detalhamento |
|---|--------|---------|---------|--------------|
| 14 | Guia Pilar: "Tipos de Entretela para Bordado" | 12h | 🔴 Alto | 2.500+ palavras, FAQ embutido, FAQPage schema |
| 15 | Guia Pilar: "Entretela de Memória: Guia Completo" | 10h | 🔴 Alto | 2.000+ palavras, HowTo schema |
| 16 | Guia Pilar: "Insumos para Bonés: Guia Completo" | 14h | 🔴 Alto | 3.000+ palavras, FAQ + HowTo schema |
| 17 | FAQ Page: 10 perguntas sobre entretelas (FAQPage schema) | 4h | 🟡 Médio | Conteúdo visível + schema |
| 18 | How-To: "Como aplicar entretela termocolante" | 3h | 🟡 Médio | HowTo schema |
| 19 | How-To: "Como usar filme hidrossolúvel" | 3h | 🟡 Médio | HowTo schema |
| 20 | Glossário de Entretelas (20+ termos) | 6h | 🟡 Médio | Autoridade temática |
| 21 | Glossário de Insumos para Bonés (15+ termos) | 4h | 🟡 Médio | Autoridade temática |
| 22 | Adicionar width/height em 129 imagens sem size attributes | 4h | 🟡 Médio | Reduzir CLS |
| 23 | Otimizar 48 imagens > 100 KB | 3h | 🟡 Médio | Comprimir sem perder qualidade |

### P3 — 60 a 90 Dias (Expansão e Autoridade)

| # | Tarefa | Esforço | Impacto | Detalhamento |
|---|--------|---------|---------|--------------|
| 24 | Headless blog com 12+ artigos (um por semana) | 60h | 🔴 Alto | Blog técnico com categoria por cluster |
| 25 | Estratégia de backlinks (diretórios, guest posts, parcerias) | 20h | 🔴 Alto | Sites de costura, moda, artesanato |
| 26 | Google Business Profile otimizado | 2h | 🟡 Médio | Fotos, posts, reviews, perguntas |
| 27 | LinkedIn da Lola ativo | 4h/mês | 🟡 Médio | Conteúdo técnico para o setor |
| 28 | Instagram com conteúdo educativo | 4h/mês | 🟡 Médio | Vídeos de aplicação, dicas técnicas |
| 29 | Ferramenta: Calculadora de Gramatura de Entretela | 8h | 🟢 Baixo | Lead magnet interativo |
| 30 | Avaliação de performance (90 dias) | 2h | — | Medir posições, tráfego, citações LLM |

### Matriz de Impacto vs Esforço

```
🚨 CRÍTICO
  │
P0-1 (Sitemap) 🟥       P2-14 (Guia Bordado) 🟥
P0-2 (Product) 🟥        P2-15 (Guia Memória) 🟥
P0-3 (Schema) 🟥         P2-16 (Guia Bonés) 🟥
P0-4 (Titles) 🟥         P1-7 (Descrições) 🟥
P0-5 (Alt text) 🟥       P1-8 (Titles dup) 🟥
P0-6 (4xx) 🟥            P1-9 (Meta desc) 🟥
                         P2-24 (Blog 12 artigos) 🟥
  │
P1-10 (Breadcrumb) 🟨    P2-17 (FAQ page) 🟨
P1-11 (Headings) 🟨      P2-18/19 (How-To) 🟨
P1-12 (Redirect) 🟨      P2-20/21 (Glossários) 🟨
P1-13 (Empresa) 🟨       P2-22/23 (Imagens) 🟨
  │
  ────────────────────────────────────────
  BAIXO ESFORÇO          ALTO ESFORÇO

  🟥 = Fazer agora   🟨 = Fazer depois
```

---

## PARTE 9 — RESUMO DOS PROBLEMAS POR GRAVIDADE

| ID | Problema | Gravidade | SEO | Acessibilidade | AI SEO | UX |
|----|----------|-----------|-----|---------------|--------|-----|
| 1 | Zero structured data em 100% das páginas | 🚨 **CRÍTICO** | ● | — | ● | ● |
| 2 | 41 URLs non-indexable no sitemap | 🚨 **CRÍTICO** | ● | — | — | — |
| 3 | 255 imagens sem alt text (100%) | 🚨 **CRÍTICO** | ● | ● | — | ● |
| 4 | 35 títulos com < 30 chars (genéricos) | 🚨 **CRÍTICO** | ● | — | ● | ● |
| 5 | Segurança: headers ausentes (X-Frame-Options, etc.) | 🚨 **CRÍTICO** | — | — | — | ● |
| 6 | Zero conteúdo informacional (blog, FAQ, guias) | 🚨 **CRÍTICO** | ● | — | ● | ● |
| 7 | 45 meta descriptions duplicadas (31,7%) | 🔴 **ALTO** | ● | — | ● | — |
| 8 | 109 páginas com H1 non-sequential (76,8%) | 🔴 **ALTO** | ● | ● | — | ● |
| 9 | 12 títulos duplicados | 🔴 **ALTO** | ● | — | — | — |
| 10 | Dupla versão do site sem redirect 301 | 🔴 **ALTO** | ● | — | — | — |
| 11 | 46 títulos idênticos ao H1 (32,4%) | 🟡 **MÉDIO** | ● | — | — | — |
| 12 | 48 imagens > 100 KB sem otimização | 🟡 **MÉDIO** | ● | — | — | ● |
| 13 | 129 imagens sem size attributes (CLS) | 🟡 **MÉDIO** | ● | — | — | ● |
| 14 | Unsafe cross-origin links em 100% das páginas | 🟡 **MÉDIO** | — | — | — | ● |
| 15 | 7 URLs bloqueadas por robots.txt | 🟡 **MÉDIO** | ● | — | — | — |

---

## PARTE 10 — OKRs (PRÓXIMOS 90 DIAS)

| OKR | KR | Meta Atual | Meta 90d |
|-----|----|-----------|----------|
| **Melhorar presença nos SERPs** | KR1: Implementar structured data em 100% das páginas | 0% | 100% |
| | KR2: Reduzir títulos < 30 chars para < 5% | 24,6% | < 5% |
| | KR3: Eliminar meta descriptions duplicadas | 31,7% | 0% |
| **Melhorar rastreamento e indexação** | KR4: Remover URLs non-indexable do sitemap | 27,2% | 0% |
| | KR5: Corrigir erros 4xx | 2 URLs | 0 |
| | KR6: Implementar redirect 301 non-www → www | Não feito | Feito |
| **Criar presença em AI Search** | KR7: Guias pilares publicados (AEO) | 0 | 3 |
| | KR8: Páginas com FAQPage + HowTo schema | 0 | 10+ |
| | KR9: Glossários técnicos publicados | 0 | 2 |
| | KR10: AI Citation Count | 0 | 10+ |
| **Melhorar acessibilidade e UX** | KR11: Adicionar alt text em 100% das imagens | 0% | 100% |
| | KR12: Corrigir hierarquia H1/H2 | 23,2% ok | > 90% ok |
| | KR13: Adicionar width/height em imagens | 49,4% ok | 100% |

---

## PARTE 11 — MÉTRICAS-CHAVE (RESUMO)

| KPI | Atual | Meta 90d | Status |
|-----|-------|----------|--------|
| Páginas com structured data | 0% | 100% | 🚨 Crítico |
| URLs non-indexable no sitemap | 27,2% | 0% | 🚨 Crítico |
| Imagens com alt text | 0% | 100% | 🚨 Crítico |
| Páginas com headers de segurança | < 10% | 100% | 🚨 Crítico |
| Títulos < 30 chars | 24,6% | < 5% | 🚨 Crítico |
| Títulos duplicados | 8,5% | 0% | 🔴 Ruim |
| Meta desc duplicadas | 31,7% | 0% | 🔴 Ruim |
| H1 non-sequential | 76,8% | < 10% | 🔴 Ruim |
| Guias pilares AEO publicados | 0 | 3 | 🚨 Crítico |
| Páginas com FAQPage schema | 0 | 5 | 🚨 Crítico |
| AI Citation Count | 0 | 10+ | 🚨 Crítico |
| Erros 4xx | 2 URLs | 0 | 🟡 Médio |
| Readability (Fairly Easy+) | 97,2% | > 90% | ✅ Bom |
| Imagens em WebP | 90,6% | > 90% | ✅ Bom |

---

*Relatório gerado em 23/07/2026 com base em auditoria técnica de 153 URLs + análise de conteúdo + pesquisa de keywords + avaliação de AI Search. Recomenda-se reavaliação em 90 dias após implementação das ações P0 e P1.*

*Template: Auditoria Completa SEO + AIO + GEO — Padrão V4 Peretto Consultoria*
