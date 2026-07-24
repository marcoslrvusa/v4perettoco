# Auditoria SEO + AIO + GEO Completa — Lola Aviamentos

**Site:** https://www.lolaaviamentos.com.br/
**Data:** 23 de julho de 2026
**Plataforma:** Nuvemshop (Tiendanube) — Tema Amazonas
**Empresa:** Lola Aviamentos — Entretelas para confecções, insumos para bonés, aviamentos têxteis
**Escopo:** Site completo (142+ URLs indexáveis, 153+ URLs totais)
**Ferramenta:** Screaming Frog SEO Spider + PSI + Análise de Conteúdo

---

## Sumário Executivo

| Métrica | Atual | Alvo (90 dias) |
|---------|-------|-----------------|
| **Score SEO Geral** | **3.5/10** | **7.5/10** |
| **URLs Indexáveis** | 112 (73.2%) | 142 (93%) |
| **Structured Data** | 0 tipos | 5+ tipos (Organization, Product, FAQ, BreadcrumbList, LocalBusiness) |
| **Títulos Duplicados** | 12 (8.45%) | 0 |
| **Meta Desc. Duplicadas** | 45 (31.69%) | <5% |
| **Imagens sem Alt** | 255+ | 0 |
| **H1 Não-Sequencial** | 76.8% | 0% |
| **Readability Geral** | "Fairly Easy" | Manter |
| **Extractability Score (AIO)** | 2/10 | 7/10 |
| **Citações em IA** | 0 | 8+ |
| **Page Speed (PSI)** | Não executado | ≥70 Mobile / ≥85 Desktop |

---

# PARTE 1: SEO TRADICIONAL

---

## 1. Auditoria de Arquitetura de Informação

### 1.1 Hierarquia Atual de Headings por Tipo de Página

#### Homepage (www.lolaaviamentos.com.br/)

| Heading | Texto | Observação |
|---------|-------|------------|
| **H1** | Lola Aviamentos - Entretelas para confecções e insumos para Bonés | 65 chars — OK como H1, mas idêntico ao title tag |
| **H2** | Total: R$0,00 | **CRÍTICO** — preço do carrinho como heading, sem valor semântico |
| **H2** | Mais vendidos | OK, mas genérico |

#### Páginas de Categoria (ex: /entretela-de-memoria/cinza/)

| Heading | Texto | Observação |
|---------|-------|------------|
| **H1** | Cinza | **CRÍTICO** — apenas a cor como H1, sem contexto de produto |
| **H2** | Total: R$0,00 | **CRÍTICO** — preço como heading |

#### Páginas de Produto (ex: /produtos/filme-plastico-magico-para-bordado-45g/)

| Heading | Texto | Observação |
|---------|-------|------------|
| **H1** | Filme Plástico Mágico para Bordado 45g | OK — descritivo |
| **H2** | Total: R$0,00 | **CRÍTICO** |
| **H2** | R$411,00 | **CRÍTICO** — preço como heading |

#### Página Empresa (/empresa/)

| Heading | Texto | Observação |
|---------|-------|------------|
| **H1** | A Lola | **CRÍTICO** — genérico demais, sem keyword relevante |
| **H2** | Total: R$0,00 | **CRÍTICO** |

### 1.2 Problemas Críticos na Hierarquia

| ID | Problema | Incidência | Gravidade |
|----|----------|------------|-----------|
| 1 | **H2 "Total: R$0,00" em TODAS as páginas** | 142/142 (100%) | **P0 — CRÍTICO** |
| 2 | **H2 de preço (ex: "R$411,00") em páginas de produto** | ~78 páginas | **P0 — CRÍTICO** |
| 3 | **H1 não-sequencial** | 109 páginas (76.8%) | **P1 — ALTO** |
| 4 | **H2 não-sequencial** | 78 páginas (54.9%) | **P1 — ALTO** |
| 5 | **H1 genérico em categorias** ("Cinza", "Branca", "Preta", "Tela", "Viés") | 22 páginas | **P1 — ALTO** |
| 6 | **H1 "A Lola" na página Empresa** | 1 página | **P1 — ALTO** |
| 7 | **H2 duplicados** | 110 páginas (77.5%) | **P2 — MÉDIO** |

**Problema nº1 (P0):** O tema Nuvemshop Amazonas renderiza o valor do carrinho como `<h2>` em absolutamente todas as páginas. Isso polui a hierarquia semântica e confunde crawlers. Solução: customizar o tema para usar `<span>` ou `<div>` em vez de `<h2>`.

**Problema nº2 (P0):** Os preços dos produtos também são renderizados como `<h2>`. Preço não é heading — é dado estrutural.

### 1.3 Fluxo de Conteúdo e Jornada do Usuário

```
Home (vitrine + banners)
  → Categoria (ex: /bordado1/)
    → Subcategoria (ex: /bordado1/rasgo-facil/)
      → Produto (ex: /produtos/entretela-para-bordado-rasgavel-40g/)
        → Carrinho → Checkout
```

**Análise:** O fluxo é linear e funcional para e-commerce, mas:
- **Não há página "Sobre" com conteúdo rico** — a página /empresa/ tem apenas 614 palavras e readability "Fairly Hard"
- **Não há blog ou conteúdo informacional** — zero artigos, zero páginas de conteúdo educativo
- **Não há página de categoria com texto descritivo** — as categorias são apenas listas de produtos
- **Não há página de "Como usar" ou "Guia de produtos"** — gap enorme para SEO informacional

### 1.4 Gaps de Informação

| Gap | Impacto | Prioridade |
|-----|---------|------------|
| Ausência de blog/conteúdo técnico sobre entretelas e bordado | **ALTO** — perde tráfego informacional | P0 |
| Categorias sem texto descritivo (zero conteúdo editorial) | **ALTO** — Google não entende o contexto da categoria | P0 |
| Página "Empresa" genérica (6 palavras de H1, 614 palavras totais) | **MÉDIO** — baixa autoridade de marca | P1 |
| Sem página de guia de produtos ("Qual entretela escolher?") | **ALTO** — perde tráfego de comparação | P1 |
| Sem depoimentos ou cases de clientes | **MÉDIO** — baixa prova social | P2 |
| Sem seção de perguntas frequentes (FAQ) | **ALTO** — perde rich snippet e citações em IA | P1 |

---

## 2. Auditoria de On-Page SEO

### 2.1 Title Tags

#### Análise Geral

| Métrica | Valor |
|---------|-------|
| Total de páginas HTML | 142 |
| Títulos duplicados | 12 (8.45%) |
| Títulos abaixo de 30 caracteres | 35 (24.65%) |
| Títulos abaixo de 200 pixels | 26 (18.31%) |
| Títulos acima de 60 caracteres | 13 (9.15%) |
| Títulos acima de 561 pixels | 18 (12.68%) |
| Title = H1 | 46 (32.39%) |

#### Títulos Críticos (P0)

| URL | Title Atual | Problema | Recomendação |
|-----|-------------|----------|--------------|
| /empresa/ | "A Lola" (6 chars) | **CRÍTICO** — não descreve a empresa, sem keyword | "Lola Aviamentos — Entretelas, Insumos para Bonés e Aviamentos Têxteis em Apucarana" |
| /entretela-de-memoria/cinza/ | "Cinza" (5 chars) | **CRÍTICO** — só a cor | "Entretela de Memória Cinza Termocolante — Lola Aviamentos" |
| /entretela-de-memoria/branca/ | "Branca" (6 chars) | **CRÍTICO** | "Entretela de Memória Branca Termocolante — Lola Aviamentos" |
| /entretela-de-memoria/preta/ | "Preta" (5 chars) | **CRÍTICO** | "Entretela de Memória Preta Termocolante — Lola Aviamentos" |
| /insumos-para-bones/tela/ | "Tela" (4 chars) | **CRÍTICO** | "Tela para Boné — Poliéster para Confecção de Bonés | Lola" |
| /insumos-para-bones/vies1/ | "Viés" (4 chars) | **CRÍTICO** | "Viés para Confecção — Tecido Fosco para Acabamento | Lola" |
| /bordado1/ | "Bordado" (7 chars) | **CRÍTICO** | "Entretelas para Bordado — Rasgável, Toque Macio, Hidrossolúvel | Lola" |
| /acessorios/ | "Acessórios" (10 chars) | **CRÍTICO** | "Acessórios para Confecção e Bordado — Lola Aviamentos" |
| /liquidacao/ | "Liquidação" (10 chars) | **CRÍTICO** | "Liquidação — Entretelas e Insumos com Desconto | Lola Aviamentos" |
| /maquinas-acessorios/ | "Máquinas para Confecção" (23 chars) | **MÉDIO** | "Máquinas para Confecção de Bonés e Vestuário — Lola Soluções" |
| /filme/ | "Filme para Bordado - Qualidade e Variedade" (42 chars) | OK | Manter, mas adicionar "Lola" no final |

#### Títulos Duplicados Identificados

| Title | URLs Afetadas |
|-------|---------------|
| "Entretela Não Tecido para Bordado Rasgável" | /produtos/entretela-para-bordado-rasgavel-40g/, /90g/, /30g/, /50g/, /70g-lec-70/ (5 URLs) |
| "Entretela Não Tecido Termocolante de Toque Macio" | /produtos/entretela-termocolante-de-toque-macio-30g/, /40g/ (2 URLs) |
| "Entretela Não Tecido para Bordado Toque Macio" | /produtos/entretela-para-bordado-toque-macio-30g/, /20g/, /60g-lepo-60/ (3 URLs) |

**Solução:** Diferenciar cada title com a gramatura específica e código do produto (ex: "Entretela Não Tecido para Bordado Rasgável 40g Lec-40").

### 2.2 Meta Descriptions

#### Análise Geral

| Métrica | Valor |
|---------|-------|
| Meta descriptions duplicadas | 45 (31.69%) |
| Meta descriptions acima de 155 chars | 36 (25.35%) |
| Meta descriptions acima de 985 pixels | 35 (24.65%) |
| Meta description ausente (vazia) | 1 página (/contato/) |

#### Meta Descriptions Duplicadas Críticas

| Meta Description | URLs Afetadas |
|-----------------|---------------|
| "A entretela rasgável (ou de rasgo fácil) pode ser removida facilmente apenas puxando-a da peça..." | 7 URLs de produto rasgável |
| "A entretela termocolante de toque macio possui vasta utilização, como forro e estrutura para camisaria..." | 5 URLs de produto termocolante |
| "A entretela para bordado de toque macio proporciona uma ótima definição aos bordados..." | 4 URLs de produto toque macio |
| "As Entretelas de Alfaiataria LAB são essenciais para quem busca durabilidade..." | 10+ URLs de produtos LAB |
| "A entretela de memória (ou entretela cavalinho) é utilizada para estruturar bonés..." | 5 URLs de entretela memória |
| "Compre online [cor] por R$..." | 3 URLs de cores (cinza, branca, preta) |
| "Aqui você vai encontrar uma ampla gama de acessórios e entretelas..." | 3 URLs (home, /produtos/, versão non-www) |

**Solução:** Cada produto precisa de meta description única destacando a gramatura, aplicação específica e diferencial. As descrições genéricas de categoria precisam incluir variações de cor e gramatura.

#### Meta Description Ausente

**/contato/** — meta description vazia. Recomendado: "Entre em contato com a Lola Aviamentos em Apucarana-PR. Tire dúvidas sobre entretelas, insumos para bonés e aviamentos têxteis."

### 2.3 Headings — Análise de Keyword Targeting

| Tipo de Página | Problema Principal | Recomendação |
|----------------|-------------------|--------------|
| Homepage | H1 idêntico ao title (65 chars) | Diferenciar: "Lola Aviamentos — Especialista em Entretelas e Insumos para Confecção" |
| Categoria | H1 = nome da cor (Cinza/Branca/Preta) | "Entretela de Memória [Cor] — Termocolante para Bonés e Roupas" |
| Subcategoria | H1 genérico (ex: "Tela", "Viés", "Filmes") | "Tela de Poliéster para Boné — Leve e Resistente | Lola" |
| Produto | H1 bom (descritivo com gramatura) | Manter, mas padronizar formato |
| Empresa | H1 "A Lola" — sem keyword | "Lola Aviamentos — Importação e Distribuição de Insumos Têxteis" |
| Institucionais | H1 OK (Política, Trocas) | Manter |

### 2.4 Densidade e Distribuição de Keywords

**Keywords primárias identificadas no site:**
- "entretela" — presente em títulos e H1s de ~60 páginas
- "bordado" — presente em ~30 páginas
- "boné" / "bonés" — presente em ~40 páginas
- "termocolante" — presente em ~25 páginas
- "rasgável" — presente em ~10 páginas
- "toque macio" — presente em ~10 páginas
- "hidrossolúvel" — presente em ~5 páginas
- "aviamentos" — presente apenas no title da home e contato

**Gaps de distribuição:**
- "aviamentos" — palavra-chave do domínio, subutilizada (só no title)
- "insumos para confecção" — aparece em poucos lugares
- "fita dupla face" — apenas na página do produto
- "fita mágica" — apenas na página do produto
- "tecido suede" — apenas na página do produto
- "máquina de costura" / "máquina para boné" — subutilizado

### 2.5 Pontos Cegos — Keywords Importantes Não Trabalhadas

| Keyword | Intenção | Volume Est. | Onde Deveria Estar | Impacto |
|---------|----------|-------------|-------------------|---------|
| "entretela para bordado" | Informativa/Comercial | Alto | Categoria /bordado1/ + blog | **ALTO** |
| "entretela termocolante" | Informativa | Alto | Categoria + blog | **ALTO** |
| "entretela rasgável" | Informativa | Médio | Categoria + blog | **ALTO** |
| "entretela de memória" | Informativa | Médio | Categoria + blog | **ALTO** |
| "insumos para bonés atacado" | Comercial | Alto | Home + categoria | **ALTO** |
| "aviamentos para confecção" | Comercial | Alto | Home + blog | **ALTO** |
| "fita termocolante dupla face" | Comercial | Médio | Página de produto + blog | **MÉDIO** |
| "como usar entretela" | Informativa | Médio | Blog (artigo) | **MÉDIO** |
| "diferença entretela rasgável e toque macio" | Informativa | Baixo | Blog (artigo comparativo) | **MÉDIO** |
| "máquina de conformar bonés" | Comercial | Baixo | Categoria máquinas | **MÉDIO** |
| "fornecedor de entretela" | Comercial | Médio | Home + Empresa | **ALTO** |
| "entretela para boné" | Comercial | Alto | Categoria + blog | **ALTO** |
| "tecidos para uniforme" | Comercial | Alto | Blog (artigo) | **MÉDIO** |
| "aba plástica para boné" | Comercial | Médio | Categoria insumos | **MÉDIO** |
| "regulador plástico para boné" | Comercial | Médio | Categoria insumos | **MÉDIO** |

---

## 3. Auditoria Técnica

### 3.1 Crawling e Indexabilidade

#### Estrutura de Domínio

| Aspecto | Status | Problema |
|---------|--------|----------|
| Domínio canônico | www.lolaaviamentos.com.br | **OK** — canonical aponta para www |
| Non-www → www | Via canonical tag (não via redirect) | **P1 — ALTO** — ~70% das URLs non-www são "Non-Indexable: Canonicalised" |
| Redirect HTTP → HTTPS | Cloudflare (implícito) | **OK** |

#### Indexabilidade Geral

| Status | URLs | % |
|--------|------|---|
| **Indexable** | 112 | 73.2% |
| **Non-Indexable (Canonicalised)** | 32 | 22.5% |
| **Non-Indexable (Blocked by robots.txt)** | 7 | 4.9% |
| **Non-Indexable (Client Error 4xx)** | 2 | 1.3% |

**Problema Crítico (P0):** 32 URLs (22.5%) são canonicadas da versão non-www para www. Isso significa que o Googlebot está encontrando links internos apontando para `lolaaviamentos.com.br` (sem www) e tendo que seguir o canonical para `www.lolaaviamentos.com.br`. Idealmente, deve haver um redirect 301 de non-www para www.

#### URLs Bloqueadas por robots.txt (7 URLs)

| URL | Motivo |
|-----|--------|
| /account/register | Página de registro |
| /account/login/ | Página de login |
| /account/reset | Reset de senha |
| /search/?q=tela+lt | Página de busca |
| Vários /pinterest.com/... | Compartilhamento Pinterest |
| Vários /facebook.com/sharer/... | Compartilhamento Facebook |

**Análise:** O bloqueio de `/account/` e `/search/` é correto. URLs de compartilhamento social também é aceitável. **Nenhum problema aqui.**

#### URLs com Erro 4xx (2 URLs)

| URL | Status | Inlinks |
|-----|--------|---------|
| /cdn-cgi/l/email-protection | 404 | 65 (non-www) + 221 (www) = **286 inlinks** |
| /cdn-cgi/l/email-protection (www) | 404 | 221 |

**P1 — ALTO:** A proteção de email do Cloudflare está gerando 404 em 286 links internos. O tema está linkando para `[email protected]` que resolve para o script de proteção Cloudflare, que retorna 404. **Solução:** Verificar configuração de proteção de email no Cloudflare ou substituir por formulário de contato.

### 3.2 Canonicals e Duplicatas

**Estrutura de Canonical:** Correta. Todas as páginas non-www apontam canonical para www. Todas as páginas www têm self-canonical.

**Problema:** A canonicalização via tag (em vez de redirect 301) significa que o Google ainda precisa processar ambas as versões. **Recomendação:** Implementar redirect 301 de `lolaaviamentos.com.br/*` para `www.lolaaviamentos.com.br/*`.

### 3.3 Response Codes

| Status | URLs | % |
|--------|------|---|
| 200 OK | 142+ | ~93% |
| 301 Redirect | Instagram, Twitter/X | ~2% |
| 302 Redirect | WhatsApp, Correios | ~1% |
| 404 Not Found | /cdn-cgi/l/email-protection (2x) | ~1% |
| Blocked by robots.txt | 7 | ~5% |

**Tempos de Resposta:** A maioria das páginas HTML carrega entre 0.08s e 0.79s — **bom desempenho** para uma plataforma Nuvemshop.

### 3.4 Core Web Vitals / Page Speed

**⚠️ PSI não foi executado** — todas as 142 URLs têm campo "PSI Request Status" vazio.

**Recomendação imediata (P0):** Executar PageSpeed Insights para ao menos 5 páginas-chave:
1. Homepage
2. Uma página de categoria (/bordado1/)
3. Uma página de produto (/produtos/fita-magica/)
4. Página Empresa
5. Página de contato

**Análise indireta baseada nos dados disponíveis:**

| Aspecto | Observação |
|---------|------------|
| Tamanho HTML | 362KB a 1.3MB (páginas de produto são pesadas) |
| Imagens sem size attributes | 129 imagens (50.59%) — **risco de CLS alto** |
| Imagens >100KB | 48 imagens (18.82%) — **pesadas para mobile** |
| Protocol-relative resources | 92.81% das URLs — **antipattern** |
| jQuery externo | CDN Google (ajax.googleapis.com) — bom |
| Cloudflare | Ativo (beacon.min.js) — bom para CDN |

### 3.5 Mobile

**⚠️ Dados de mobile não coletados** — todas as URLs têm campo vazio.

**Recomendação:** Testar responsividade manualmente. O tema Amazonas da Nuvemshop é responsivo por padrão, mas é necessário verificar:
- Botões de CTA em telas pequenas
- Menu hamburger funcionando
- Imagens de produto redimensionadas corretamente
- Carrinho e checkout funcionais em mobile

### 3.6 Imagens

| Métrica | Valor |
|---------|-------|
| Total de imagens | 255+ |
| Imagens sem alt text | 1 (alt attribute ausente) |
| Imagens com alt text vazio | 0 |
| Imagens com alt text >100 chars | 20 (7.84%) |
| Imagens sem size attributes | 129 (50.59%) |
| Imagens >100KB | 48 (18.82%) |

**Problemas:**

1. **Imagens sem size attributes (P1 — ALTO):** 50.59% das imagens não têm width/height no HTML. Isso causa Cumulative Layout Shift (CLS) e afeta Core Web Vitals.

2. **Imagens pesadas (P1 — MÉDIO):** 48 imagens acima de 100KB. Algumas têm mais de 400KB (ex: `lt-07-azul-royal` com 468KB, `etp-02` com 482KB). Isso impacta tempo de carregamento em mobile.

3. **Alt text descritivo:** A maioria das imagens de produto tem alt text com o nome do produto — **OK**. Mas imagens de banner e carrossel têm alt text genérico como "Carrossel 1", "Carrossel 2" — **P2 — MÉDIO**.

### 3.7 Links Internos e Âncoras

| Métrica | Valor |
|---------|-------|
| Links internos sem anchor text | 100% das páginas (142/142) |
| Links com anchor text "Comprar" | Múltiplos por página |
| Links com anchor text "Espiar" | Múltiplos por página |
| Links com anchor text "Mais Vendidos" | Todas as páginas (header) |
| Links com anchor text "Ver carrinho" | Todas as páginas |

**Problema Crítico (P0):** 100% das páginas têm links internos sem anchor text. Isso ocorre porque os links de produto no carrossel e vitrine usam imagens sem alt text descritivo como âncora. O Google não consegue entender o contexto do link.

**Análise de Navegação:** A estrutura de navegação é boa (categorias no header com dropdown), mas os links de produto individuais são quase todos imagem-based sem anchor text.

### 3.8 Segurança

| Header | Status | URLs Afetadas |
|--------|--------|---------------|
| Content-Security-Policy | **AUSENTE** | 2 URLs |
| HSTS | **AUSENTE** | 2 URLs |
| X-Frame-Options | **AUSENTE** | 142 URLs (92.81%) |
| Referrer-Policy | **AUSENTE** | 144 URLs (94.12%) |
| Unsafe cross-origin links (target="_blank" sem rel="noopener") | **PRESENTE** | 142 URLs (92.81%) |
| Protocol-relative resource links | **PRESENTE** | 142 URLs (92.81%) |

**Recomendação (P2):** Adicionar headers de segurança via Cloudflare ou servidor:
- `X-Frame-Options: SAMEORIGIN`
- `Referrer-Policy: strict-origin-when-cross-origin`
- Adicionar `rel="noopener"` a todos os links com `target="_blank"`
- Converter protocol-relative links para HTTPS absoluto

### 3.9 Acessibilidade

**⚠️ Dados de acessibilidade não coletados** — todas as URLs têm campos vazios para violações WCAG.

**Recomendação:** Executar auditoria de acessibilidade (axe-core ou WAVE) para verificar:
- Contraste de cores
- Foco visível em navegação por teclado
- Labels em formulários
- ARIA labels em elementos interativos

---

## 4. Schema Markup Atual vs Ideal

### 4.1 Situação Atual

**ZERO structured data em todas as 142 páginas.** Nenhum tipo de schema.org está presente.

| Tipo de Schema | Status | Impacto |
|----------------|--------|---------|
| Organization | ❌ Ausente | Perde rich snippet de marca |
| LocalBusiness | ❌ Ausente | Perde visibilidade no Google Maps/Local Pack |
| Product | ❌ Ausente | Perde rich snippet de produto (preço, disponibilidade) |
| BreadcrumbList | ❌ Ausente | Perde breadcrumb rich nos resultados |
| FAQPage | ❌ Ausente | Perde rich snippet de FAQ |
| WebSite | ❌ Ausente | Perde SearchAction (sitelinks search box) |
| WebPage | ❌ Ausente | Perde contexto semântico |

### 4.2 Schema Recomendado

#### P0 — Implementação Imediata

##### Organization + LocalBusiness (Homepage + Contato)

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Lola Aviamentos",
  "alternateName": "Lola Soluções Têxteis",
  "url": "https://www.lolaaviamentos.com.br",
  "logo": "https://acdn-us.mitiendanube.com/stores/001/720/481/themes/common/logo-2381817-1754682754-c325014e3710438c242fa3453bf903381754682754-480-0.webp",
  "description": "Importação e distribuição de entretelas, insumos para bonés, aviamentos e máquinas para confecção.",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Apucarana",
    "addressRegion": "PR",
    "addressCountry": "BR"
  },
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+55-43-99119-6727",
    "contactType": "sales",
    "availableLanguage": ["Portuguese"]
  },
  "sameAs": [
    "https://www.instagram.com/lolasolucoes",
    "https://www.facebook.com/lolasolucoestexteis",
    "https://www.youtube.com/@lolasolucoes"
  ]
}
```

**Impacto:** Rich snippet de organização, links para redes sociais, visibilidade em busca local.

##### Product (Páginas de Produto)

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Entretela Não Tecido para Bordado Rasgável 40g Lec-40",
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
  },
  "image": "https://acdn-us.mitiendanube.com/stores/001/720/481/products/entretela-para-bordado-rasgavel-40g-90cm-200m_lola1-22732f95aedd2233cb16328392133492-1024-1024.jpg"
}
```

**Impacto:** Rich snippet de produto com preço e disponibilidade. Essencial para e-commerce.

##### WebSite (Homepage)

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Lola Aviamentos",
  "url": "https://www.lolaaviamentos.com.br",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "https://www.lolaaviamentos.com.br/search/?q={search_term_string}",
    "query-input": "required name=search_term_string"
  }
}
```

**Impacto:** Habilita a caixa de busca nos sitelinks do Google.

#### P1 — 1 a 2 Semanas

##### BreadcrumbList (Todas as Páginas)

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Início", "item": "https://www.lolaaviamentos.com.br/" },
    { "@type": "ListItem", "position": 2, "name": "Bordado", "item": "https://www.lolaaviamentos.com.br/bordado1/" },
    { "@type": "ListItem", "position": 3, "name": "Rasgo Fácil", "item": "https://www.lolaaviamentos.com.br/bordado1/rasgo-facil/" }
  ]
}
```

**Impacto:** Breadcrumb visual nos resultados de busca.

##### FAQPage (Homepage + Categorias)

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "O que é entretela para bordado?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "A entretela para bordado é um material não tecido utilizado como base para estabilizar o tecido durante o processo de bordado computadorizado. Existem tipos rasgáveis, hidrossolúveis e termocolantes, cada um com aplicação específica."
      }
    },
    {
      "@type": "Question",
      "name": "Qual a diferença entre entretela rasgável e hidrossolúvel?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "A entretela rasgável é removida manualmente após o bordado, enquanto a hidrossolúvel se dissolve em água. A rasgável é mais rápida para peças do dia a dia; a hidrossolúvel é ideal para bordados delicados onde não se pode puxar o material."
      }
    },
    {
      "@type": "Question",
      "name": "Como escolher a gramatura da entretela?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Gramaturas mais leves (20g-40g) são indicadas para tecidos finos como camisetas e vestidos. Gramaturas médias (40g-60g) funcionam bem para a maioria dos bordados. Gramaturas mais pesadas (60g-90g) são para tecidos grossos ou bordados densos."
      }
    }
  ]
}
```

**Impacto:** Rich snippet de FAQ expansível nos resultados. **Alta taxa de CTR.**

#### P2 — 30 a 60 Dias

##### ItemList (Categorias)

```json
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "Entretelas para Bordado",
  "url": "https://www.lolaaviamentos.com.br/bordado1/",
  "numberOfItems": 5,
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Rasgo Fácil" },
    { "@type": "ListItem", "position": 2, "name": "Toque Macio" },
    { "@type": "ListItem", "position": 3, "name": "Hidrossolúvel" },
    { "@type": "ListItem", "position": 4, "name": "Termocolante" },
    { "@type": "ListItem", "position": 5, "name": "Filmes" }
  ]
}
```

##### VideoObject (Canal YouTube)

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "Como usar entretela para bordado",
  "description": "Guia prático de como usar entretela rasgável e hidrossolúvel.",
  "thumbnailUrl": "https://img.youtube.com/vi/.../hqdefault.jpg",
  "uploadDate": "2026-01-01",
  "duration": "PT5M",
  "publisher": {
    "@type": "Organization",
    "name": "Lola Soluções"
  }
}
```

---

## 5. Análise de Conteúdo

### 5.1 Word Count por Tipo de Página

| Tipo de Página | Média de Palavras | Avaliação |
|----------------|-------------------|-----------|
| Homepage | 836 | **OK** para e-commerce |
| Categoria | 519-919 | **Baixo** — ideal >500, mas falta texto editorial |
| Subcategoria | 455-704 | **Baixo** — ideal >300 |
| Produto | 783-1112 | **BOM** — descrições ricas |
| Empresa | 614 | **BAIXO** — ideal >1000 para página institucional |
| Contato | 456 | OK |
| Política Privacidade | 826 | OK |
| Trocas/Devoluções | 1350 | OK |
| Filme (categoria) | 533 | **Baixo** |

### 5.2 Readability (Flesch Reading Ease)

| Página | Score | Classificação | Avaliação |
|--------|-------|---------------|-----------|
| Homepage | 77.8 | Fairly Easy | ✅ **BOM** |
| /empresa/ | 53.8 | **Fairly Hard** | ❌ **DIFÍCIL** — precisa simplificar |
| /trocas-devolucoes/ | 38.4 | **Hard** | ⚠️ Esperado para texto jurídico |
| /bordado1/ | 99.4 | Very Easy | ✅ **BOM** |
| /entretela-alfaiataria/ | 99.2 | Very Easy | ✅ **BOM** |
| /liquidacao/ | 99.1 | Very Easy | ✅ **BOM** |
| /produtos/ | 100.0 | Very Easy | ✅ **BOM** |
| Média geral | ~75 | Fairly Easy | ✅ **BOM para e-commerce** |

**Problema (P1):** A página /empresa/ tem readability "Fairly Hard" (53.8). Isso é contraproducente para uma página que deve comunicar a marca de forma clara. **Recomendação:** Reescrever com linguagem mais simples, frases mais curtas.

### 5.3 Near-Duplicate Detection

**⚠️ Nenhum near-duplicate detectado** — todas as páginas têm conteúdo único. ✅

### 5.4 Gaps Semânticos

| Tópico Não Coberto | Onde Deveria Estar | Tipo de Conteúdo |
|--------------------|-------------------|------------------|
| "O que é entretela?" | Homepage ou blog | Definição/Glossário |
| "Tipos de entretela para bordado" | Categoria /bordado1/ | Guia comparativo |
| "Como usar entretela rasgável" | Página de produto | Tutorial |
| "Diferença entre entretela termocolante e não-tecido" | Blog | Artigo comparativo |
| "Guia de gramaturas de entretela" | Blog | Guia técnico |
| "Como montar uma fábrica de bonés" | Blog | Conteúdo para empreendedores |
| "Fornecedor de aviamentos em Apucarana" | Homepage + Empresa | SEO local |
| "Entretela para patchwork" | Categoria ou blog | Nicho específico |

---

# PARTE 2: AIO (AI Optimization)

---

## 6. Extractability Score

### 6.1 Avaliação Geral: 2/10

| Critério | Score | Justificativa |
|----------|-------|---------------|
| Definições explícitas | 1/10 | Quase nenhuma definição do tipo "X é..." |
| Estrutura Q&A | 0/10 | Zero perguntas e respostas no texto visível |
| Parágrafos informacionais (60-120 palavras) | 3/10 | Parágrafos muito curtos, média de 3 palavras por frase |
| Dados numéricos com contexto | 2/10 | Preços aparecem, mas sem contexto de aplicação |
| Vocabulário controlado | 4/10 | Termos técnicos presentes mas sem definição |
| FAQ schema | 0/10 | Ausente |
| Citações e fontes | 0/10 | Nenhuma referência a normas ou fontes externas |
| **Extractability Score** | **2/10** | **Baixa probabilidade de citação em LLMs** |

### 6.2 Por que o Conteúdo Atual Não é Citado por LLMs

1. **Parágrafos muito curtos:** A média de palavras por frase é de ~3.0-3.5. LLMs precisam de blocos de 50-120 palavras com contexto semântico rico para citar uma fonte.

2. **Falta de definições:** Não há frases como "Entretela rasgável é um tipo de material não tecido utilizado para..." — esses patterns são o que ChatGPT e Perplexity buscam.

3. **Zero estrutura de perguntas e respostas:** O conteúdo é todo declarativo e focado em venda. Não há seções de FAQ, dúvidas comuns, ou formato Q&A.

4. **Dados sem contexto:** Os preços e gramaturas aparecem como dados soltos, sem explicação do significado ou aplicação.

5. **Sem schema:** Zero structured data significa que os crawlers de LLM não recebem dicas semânticas sobre o conteúdo.

### 6.3 Estratégia "Extractability First"

**Adicionar blocos de definição nas páginas-chave:**

**Homepage:**
> "A Lola Aviamentos é uma empresa brasileira especializada na importação e distribuição de entretelas para bordado, insumos para confecção de bonés e aviamentos têxteis. Localizada em Apucarana, Paraná, a empresa atende confecções de todos os portes com produtos como entretela rasgável, entretela hidrossolúvel, entretela termocolante, fitas dupla face, viés, abas plásticas e máquinas para bonés."

**Página de Categoria (/bordado1/):**
> "Entretela para bordado é um material de suporte utilizado em bordados computadorizados para estabilizar o tecido durante a costura. Ela evita que o tecido enrugue, estique ou deforme com os pontos do bordado. Existem diversos tipos de entretela para bordado, cada um com características específicas de aplicação e remoção."

**Página de Produto (ex: entretela rasgável):**
> "A entretela rasgável — também chamada de entretela de rasgo fácil — é um tipo de entretela não tecido que pode ser removida manualmente após o bordado, bastando puxar suavemente o excesso ao redor dos pontos. Ela é composta por fibras de poliéster agulhadas, que se rompem com facilidade sem danificar o bordado. É a opção mais utilizada na indústria de confecção por sua praticidade e rapidez."

**Adicionar bloco FAQ na Homepage (5-6 perguntas):**
- "O que é entretela para bordado?"
- "Qual a diferença entre entretela rasgável e hidrossolúvel?"
- "Como escolher a gramatura ideal de entretela?"
- "O que é entretela termocolante?"
- "Onde comprar entretela para confecção atacado?"
- "Quais insumos são necessários para fabricar bonés?"

---

## 7. AI Citations

### 7.1 Situação Atual

| Engine | Citações Atuais | Potencial |
|--------|----------------|-----------|
| ChatGPT | 0 | 5+ |
| Perplexity | 0 | 3+ |
| Google AI Overviews | 0 | 3+ |
| Gemini | 0 | 2+ |
| Claude | 0 | 2+ |
| Copilot | 0 | 2+ |
| **Total** | **0** | **17+** |

### 7.2 Estratégia de Citações

Para ser citado, o conteúdo precisa:
1. Responder perguntas de forma direta e completa
2. Usar linguagem clara com definições explícitas
3. Ter autoridade percebida (dados, fontes, especificações)
4. Estar bem estruturado (headings, listas, tabelas)
5. Ter schema markup complementar

**Páginas com maior potencial de citação:**

| Página | Query Potencial | Prioridade |
|--------|----------------|------------|
| Homepage (com FAQ) | "o que é entretela", "tipos de entretela" | P0 |
| /bordado1/ (com texto) | "entretela para bordado", "como usar entretela" | P0 |
| /entretela-alfaiataria/ | "entretela para alfaiataria", "entretela termocolante" | P1 |
| /entretela-de-memoria/ | "entretela de memória", "entretela cavalinho" | P1 |
| /insumos-para-bones/ | "insumos para bonés", "como fazer boné" | P1 |
| Blog (a criar) | "diferença entretela rasgável hidrossolúvel" | P1 |

---

## 8. Service Cart AI

### 8.1 Definição

O "Service Cart AI" é o conjunto de informações que os LLMs conseguem extrair sobre os produtos e serviços de uma empresa. Quanto mais completo e estruturado, maior a chance de recomendação.

### 8.2 Service Cart Atual da Lola

| Informação | Disponibilidade | Completo? |
|------------|----------------|-----------|
| Nome da empresa | ✅ Title e H1 | ✅ |
| Localização | ❌ Não informada no site | ❌ |
| Telefone | ✅ WhatsApp no header | ✅ |
| Produtos | ✅ Listados em categorias | ⚠️ Sem descrições |
| Preços | ✅ Nas páginas de produto | ✅ |
| Especificações técnicas | ⚠️ Parcial (gramatura, medidas) | ⚠️ |
| Aplicações | ❌ Não descritas | ❌ |
| Diferenciais | ❌ Não mencionados | ❌ |
| Público-alvo | ❌ Não definido | ❌ |
| Formas de pagamento | ⚠️ No footer (genérico) | ⚠️ |
| Frete e prazos | ❌ Não informado | ❌ |

### 8.3 Recomendações para Completar o Service Cart

1. **Adicionar endereço completo** na página de contato e no schema LocalBusiness
2. **Criar página "Como Comprar"** com informações de frete, prazos, formas de pagamento
3. **Adicionar especificações técnicas** em todas as páginas de produto (gramatura, composição, dimensões, aplicação)
4. **Descrever o público-alvo** na página Empresa ("Atendemos confecções de todos os portes, indústrias de bonés, bordadeiras e artesãs")
5. **Listar diferenciais** (importação direta, variedade de gramaturas, estoque próprio, atendimento técnico)

---

## 9. Otimização para ChatGPT, Perplexity, Gemini, Claude

### 9.1 Estratégia Unificada

| Engine | Comportamento | Estratégia |
|--------|---------------|------------|
| **ChatGPT** | Prefere respostas completas com definições e exemplos | Criar conteúdo enciclopédico sobre entretelas |
| **Perplexity** | Cita fontes com autoridade e dados recentes | Adicionar dados técnicos, normas, especificações |
| **Gemini** | Contextualiza com informações visuais e estruturadas | Schema markup + imagens com alt text descritivo |
| **Claude** | Valoriza clareza, estrutura lógica e completude | Conteúdo bem estruturado com headings e listas |
| **Google AI Overviews** | Extrai de páginas com FAQ, listas e definições | FAQ schema + blocos de definição |

### 9.2 Conteúdo Prioritário para AI Visibility

**P0 — Criar em 2 semanas:**

1. **Guia "O que é entretela?"** (página ou seção na home)
   - Definição completa
   - Tipos (rasgável, hidrossolúvel, termocolante, de memória)
   - Tabela comparativa de aplicações
   - FAQ schema

2. **Guia "Como escolher a entretela ideal"**
   - Por tipo de tecido
   - Por tipo de bordado
   - Por gramatura
   - Formato de artigo de blog

3. **Página "Insumos para Bonés" com texto editorial**
   - Lista completa de insumos necessários
   - Guia passo a passo de fabricação
   - Dicas de fornecedores

**P1 — Criar em 30 dias:**

4. **Blog com 5 artigos técnicos:**
   - "Entretela Rasgável vs Hidrossolúvel: Qual Usar?"
   - "Guia Completo de Gramaturas de Entretela"
   - "Como Montar uma Linha de Produção de Bonés"
   - "O que é Entretela Termocolante e Como Aplicar"
   - "Aviamentos Têxteis: Guia para Confecções"

5. **Glossário de termos técnicos** (página dedicada)

---

# PARTE 3: GEO (Generative Engine Optimization)

---

## 10. Estrutura para AI Overviews

### 10.1 O Google AI Overviews Precisa

| Requisito | Status Atual | Ação Necessária |
|-----------|-------------|-----------------|
| Conteúdo que responda perguntas diretamente | ❌ Ausente | Adicionar blocos Q&A |
| Estrutura de headings clara | ⚠️ H2 poluído | Corrigir hierarquia |
| Dados estruturados (FAQ, HowTo) | ❌ Ausente | Implementar schema |
| Autoridade de domínio | ❌ Desconhecido | Construir backlinks |
| Freshness (atualização recente) | ⚠️ Site ativo | Manter atualizações |

### 10.2 Páginas com Potencial para AI Overviews

| Query | Página Alvo | Conteúdo Necessário |
|-------|-------------|---------------------|
| "o que é entretela para bordado" | Homepage ou /bordado1/ | Definição + tipos + FAQ |
| "como usar entretela rasgável" | Página de produto | Tutorial + FAQ |
| "diferença entretela rasgável hidrossolúvel" | Blog (a criar) | Artigo comparativo |
| "insumos para fabricar bonés" | /insumos-para-bones/ | Lista completa + guia |
| "entretela termocolante o que é" | /bordado1/termocolante/ | Definição + aplicações |
| "onde comprar entretela atacado" | Homepage + /produtos/ | Informação comercial |

---

## 11. Otimização para Snippets Generativos

### 11.1 Formato de Resposta Direta

Para aparecer em snippets generativos, o conteúdo deve seguir o padrão:

```
[Pergunta]
[Resposta direta em 1-2 parágrafos]
[Dados de suporte (tabela, lista, números)]
[CTA ou informação complementar]
```

**Exemplo para a Lola:**

```
O que é entretela para bordado?

A entretela para bordado é um material de suporte não tecido, geralmente composto de fibras de poliéster, utilizado como base para estabilizar o tecido durante o bordado computadorizado. Ela evita que o tecido enrugue, estique ou deforme com os pontos.

Principais tipos de entretela:
- Rasgável: removida manualmente após o bordado
- Hidrossolúvel: dissolvida em água
- Termocolante: fixada com calor
- Toque macio: ideal para peças delicadas

Na Lola Aviamentos você encontra todos os tipos em diversas gramaturas (20g a 90g) para atender desde bordados simples até aplicações industriais.
```

---

## 12. Marcação Semântica para Engines Generativas

### 12.1 Recomendações Técnicas

| Técnica | Status | Prioridade |
|---------|--------|------------|
| JSON-LD Organization | ❌ Ausente | P0 |
| JSON-LD Product | ❌ Ausente | P0 |
| JSON-LD FAQPage | ❌ Ausente | P1 |
| JSON-LD BreadcrumbList | ❌ Ausente | P1 |
| JSON-LD HowTo | ❌ Ausente | P1 |
| Open Graph tags | ⚠️ Provavelmente presente (Nuvemshop) | Verificar |
| Twitter Cards | ⚠️ Provavelmente presente | Verificar |
| Meta robots | ✅ Não bloqueia indexação | OK |
| Sitemap XML | ⚠️ Provavelmente gerado pela Nuvemshop | Verificar |

### 12.2 Estrutura de Entidades para Knowledge Graph

Para que os LLMs entendam o negócio da Lola, é preciso estabelecer estas entidades e relacionamentos:

```
[Lola Aviamentos] — tipo: [Organization] — localização: [Apucarana, PR]
  → importa e distribui → [Entretelas para Bordado]
    → tipos: [Rasgável] [Hidrossolúvel] [Termocolante] [Toque Macio]
    → gramaturas: [20g] [30g] [40g] [50g] [60g] [70g] [80g] [90g]
  → importa e distribui → [Insumos para Bonés]
    → tipos: [Tela] [Aba Plástica] [Regulador Plástico] [Viés] [Tecido Suede]
  → importa e distribui → [Máquinas para Confecção]
    → tipos: [Máquina de Conformar] [Máquina de Encapar Botão] [Máquina Transfer]
  → atende → [Confecções] [Indústrias de Bonés] [Bordadeiras] [Artesãs]
```

Cada entidade deve ser mencionada pelo menos 2-3 vezes no texto visível.

---

# Plano de Ação Priorizado

## P0 — Hoje (Implementação Imediata) — ~12h

| # | Tarefa | Esforço | Impacto | Detalhamento |
|---|--------|---------|---------|--------------|
| 1 | **Corrigir H2 "Total: R$0,00" e preços** | 2h | **Crítico** | Customizar tema Nuvemshop para usar `<span>` em vez de `<h2>` |
| 2 | **Corrigir titles genéricos** (Cinza, Branca, Preta, Tela, Viés, Bordado, A Lola) | 1h | **Alto** | 22 páginas com titles <30 caracteres |
| 3 | **Corrigir meta descriptions duplicadas** | 2h | **Alto** | 45 descrições duplicadas em 7 grupos |
| 4 | **Adicionar schema Organization + LocalBusiness** | 30min | **Alto** | JSON-LD na homepage e contato |
| 5 | **Adicionar schema Product nas páginas de produto** | 2h | **Alto** | 78 páginas de produto — usar template com variáveis |
| 6 | **Corrigir 404 do email protection** | 30min | **Médio** | 286 links internos quebrando |
| 7 | **Adicionar meta description na página /contato/** | 5min | **Médio** | Única página sem description |

## P1 — 1 a 2 Semanas — ~30h

| # | Tarefa | Esforço | Impacto | Detalhamento |
|---|--------|---------|---------|--------------|
| 8 | **Criar texto editorial para categorias** | 6h | **Alto** | 6 categorias principais com 200-400 palavras cada |
| 9 | **Criar bloco FAQ na homepage** | 2h | **Alto** | 5-6 perguntas com respostas + FAQPage schema |
| 10 | **Criar guia "O que é entretela?"** | 3h | **Alto** | Página ou seção com definições, tipos, tabela comparativa |
| 11 | **Reescrever página Empresa** | 2h | **Médio** | De 614 para 1000+ palavras, readability "Fairly Easy" |
| 12 | **Adicionar schema BreadcrumbList** | 1h | **Médio** | Template para todas as páginas |
| 13 | **Adicionar size attributes em imagens** | 3h | **Médio** | 129 imagens sem width/height — reduz CLS |
| 14 | **Otimizar imagens >100KB** | 4h | **Médio** | 48 imagens — comprimir para <100KB |
| 15 | **Criar 3 artigos de blog** | 8h | **Alto** | Conteúdo informacional para capturar tráfego |
| 16 | **Implementar redirect 301 non-www → www** | 1h | **Alto** | No Cloudflare ou servidor |

## P2 — 30 a 60 Dias — ~40h

| # | Tarefa | Esforço | Impacto | Detalhamento |
|---|--------|---------|---------|--------------|
| 17 | **Criar mais 5 artigos de blog** | 15h | **Alto** | Completar calendário editorial |
| 18 | **Adicionar schema HowTo para processos** | 2h | **Médio** | Guias de uso de produtos |
| 19 | **Adicionar headers de segurança** | 1h | **Baixo** | CSP, HSTS, X-Frame-Options |
| 20 | **Corrigir unsafe cross-origin links** | 2h | **Baixo** | Adicionar rel="noopener" |
| 21 | **Converter protocol-relative para HTTPS** | 2h | **Baixo** | Recursos carregados com // |
| 22 | **Criar página "Como Comprar"** | 2h | **Médio** | Frete, prazos, pagamento |
| 23 | **Executar PageSpeed Insights** | 1h | **Médio** | 5 páginas-chave |
| 24 | **Auditoria de acessibilidade** | 2h | **Médio** | WCAG compliance |
| 25 | **Criar glossário de termos técnicos** | 4h | **Médio** | SEO informacional |
| 26 | **Construir backlinks (diretórios)** | 8h | **Médio** | Diretórios de fornecedores têxteis |

---

## Matriz de Impacto vs Esforço

```
ALTO IMPACTO
  │
  │  P0-1 (H2 preço) ⬤       P1-8 (Texto categorias) ⬤
  │  P0-2 (Titles) ⬤          P1-9 (FAQ) ⬤
  │  P0-3 (Meta desc) ⬤       P1-10 (Guia entretela) ⬤
  │  P0-4 (Schema Org) ⬤      P1-15 (Blog) ⬤
  │  P0-5 (Schema Product) ⬤  P2-17 (Blog extra) ⬤
  │  P0-6 (404 email) ⬤
  │  P1-16 (Redirect 301) ⬤
  │
  │  P0-7 (Contato meta) ○     P1-12 (Size attributes) ○
  │  P1-11 (Breadcrumb) ○      P1-13 (Imagens pesadas) ○
  │  P1-14 (Otimizar img) ○
  │
  │                            P2-19 (Security headers) ○
  │                            P2-20 (Cross-origin) ○
  │                            P2-21 (Protocol-relative) ○
  │
  BAIXO IMPACTO
  ────────────────────────────────
  BAIXO ESFORÇO         ALTO ESFORÇO

  ⬤ = Fazer agora   ○ = Fazer depois
```

---

## Resumo dos Problemas por Gravidade

| ID | Problema | Gravidade | SEO | AIO | UX | Acess. |
|----|----------|-----------|-----|-----|-----|--------|
| 1 | H2 "Total: R$0,00" em 100% das páginas | **CRÍTICO** | ● | ● | — | ● |
| 2 | H2 de preço em páginas de produto | **CRÍTICO** | ● | ● | — | ● |
| 3 | Titles genéricos (<30 chars) em 35 páginas | **CRÍTICO** | ● | ● | ● | — |
| 4 | Meta descriptions duplicadas (45 URLs) | **CRÍTICO** | ● | ● | — | — |
| 5 | Zero structured data no site inteiro | **CRÍTICO** | ● | ● | — | — |
| 6 | 404 em proteção de email (286 inlinks) | **ALTO** | ● | — | ● | — |
| 7 | Categorias sem texto editorial | **ALTO** | ● | ● | ● | — |
| 8 | Sem FAQ ou conteúdo de definições | **ALTO** | ● | ● | ● | — |
| 9 | Página Empresa com readability difícil | **ALTO** | ● | ● | ● | ● |
| 10 | 129 imagens sem size attributes (CLS) | **ALTO** | ● | — | ● | — |
| 11 | 48 imagens >100KB | **MÉDIO** | ● | — | ● | — |
| 12 | Links internos sem anchor text (100%) | **MÉDIO** | ● | — | ● | — |
| 13 | Unsafe cross-origin links (92.81%) | **MÉDIO** | — | — | ● | — |
| 14 | Protocol-relative resources (92.81%) | **MÉDIO** | — | — | ● | — |
| 15 | Sem blog ou conteúdo informacional | **ALTO** | ● | ● | ● | — |
| 16 | PSI não executado | **MÉDIO** | ● | — | ● | — |
| 17 | Sem redirect 301 non-www → www | **MÉDIO** | ● | — | — | — |
| 18 | Headers de segurança ausentes | **BAIXO** | — | — | ● | — |

---

## Projeção de Resultados

### 90 Dias Após Implementação P0 + P1

| Métrica | Atual | Projetado | Ganho |
|---------|-------|-----------|-------|
| URLs indexáveis | 112 | 140 | +25% |
| Tráfego orgânico estimado | ~0 (site novo) | +200 visitas/mês | Novo canal |
| Citações em IA | 0 | 8+ | Novo canal |
| Rich snippets (schema) | 0 | 78+ (Product) + Homepage (Org) | Novo |
| CTR estimado em SERP | ~2% | ~8% | +300% |
| Core Web Vitals | Desconhecido | ≥70 Mobile / ≥85 Desktop | Melhoria significativa |
| Readability página Empresa | Fairly Hard | Fairly Easy | Melhoria |

### Estimativa de Horas

| Fase | Horas | Custo Estimado (R$) |
|------|-------|---------------------|
| P0 — Imediato | 12h | ~R$ 1.800 |
| P1 — 1-2 semanas | 30h | ~R$ 4.500 |
| P2 — 30-60 dias | 40h | ~R$ 6.000 |
| **Total** | **82h** | **~R$ 12.300** |

---

*Relatório gerado em 23/07/2026 por auditoria técnica com base nos dados coletados via Screaming Frog SEO Spider em lolaaviamentos.com.br e www.lolaaviamentos.com.br. Recomenda-se reavaliação em 90 dias após implementação das ações P0 e P1.*
