# Análise de Performance SEO — Lola Aviamentos

**Data da auditoria:** Julho 2026
**Site:** lolaaviamentos.com.br / www.lolaaviamentos.com.br
**Plataforma:** Nuvemshop (mitiendanube.com)
**Total de páginas HTML analisadas:** 153

---

## Sumário Executivo

O site Lola Aviamentos apresenta **problemas críticos de segurança e estruturais** que impactam diretamente a indexação e a confiança do Google. **100% das páginas** não possuem structured data, headers de segurança essenciais estão ausentes em praticamente todo o site, e **41 URLs não-indexáveis estão sendo incluídas no sitemap** — um erro grave que confunde os crawlers.

**Pontos críticos (ação imediata necessária):**
- ❌ 0% das páginas têm structured data (schema markup)
- ❌ 41 URLs non-indexable no sitemap (22,5% do total)
- ❌ 100% das páginas sem X-Frame-Options, sem Referrer-Policy, com unsafe cross-origin links
- ❌ 142 páginas com external outlinks sem anchor text
- ❌ 255 imagens sem atributo alt
- ❌ 2 páginas com erro 4xx (Client Error)
- ❌ 7 URLs bloqueadas por robots.txt

---

## 1. Arquitetura e Indexabilidade

### 1.1 Dupla Versão do Site

O site existe em duas versões:
- `lolaaviamentos.com.br` (non-www) — **32 URLs canonicalizadas** para www
- `www.lolaaviamentos.com.br` (www) — **112 URLs indexáveis**

| Métrica | Valor |
|---------|-------|
| Total HTML pages | 153 |
| Indexáveis (www) | 112 (73,2%) |
| Não-indexáveis | 41 (26,8%) |
| — Canonicalizadas | 32 |
| — Bloqueadas por robots.txt | 7 |
| — Client Error (4xx) | 2 |

**⚠️ Problema:** 32 URLs da versão non-www estão canonicalizadas para www, mas **continuam no sitemap** como non-indexable. Isso é um erro grave — URLs não-indexáveis não devem estar no sitemap.

### 1.2 Status Codes

| Status | Quantidade |
|--------|-----------|
| 200 OK | 407 |
| 301/302 Redirects | 35 |
| 404 | 3 |
| Blocked by robots.txt | 61 |

**⚠️ 3 URLs retornando 404** e **61 URLs bloqueadas por robots.txt** indicam problemas de rastreamento.

---

## 2. Sitemap

| Métrica | Valor |
|---------|-------|
| URLs no sitemap | 151 |
| Indexáveis no sitemap | 110 (72,8%) |
| **Não-indexáveis no sitemap** | **41 (27,2%)** |

**🚨 CRÍTICO:** 41 URLs non-indexable estão sendo incluídas no sitemap. Isso inclui:
- URLs da versão non-www canonicalizadas
- URLs bloqueadas por robots.txt
- URLs com erro 4xx

**Impacto:** O Google desperdiça orçamento de rastreio tentando indexar URLs que não podem ser indexadas.

---

## 3. Page Titles

| Métrica | Valor |
|---------|-------|
| Total de titles únicos | 142 |
| Média de caracteres | 37 chars |
| Títulos < 30 chars | **35 (24,6%)** |
| Títulos > 60 chars | **13 (9,2%)** |
| Títulos > 561 pixels | **18 (12,7%)** |
| Títulos < 200 pixels | **26 (18,3%)** |
| **Títulos duplicados** | **12 (8,5%)** |
| **Titles iguais ao H1** | **46 (32,4%)** |

**Problemas identificados:**

- **35 títulos muito curtos (< 30 chars):** Inclui páginas de produto com apenas o nome da cor ou material (ex: "Cinza", "Preta", "Tela", "Viés") — sem incluir o nome da marca ou contexto.
- **13 títulos muito longos (> 60 chars):** Podem ser truncados nos SERPs.
- **12 títulos duplicados:** Ex: "Aba Plástica", "Acessórios", "Bordado", "Branca", "Cinza" aparecem em múltiplas URLs.
- **46 títulos idênticos ao H1 (32,4%):** Perdem a oportunidade de incluir palavras-chave complementares.

**Exemplos de títulos problemáticos:**
- "Cinza" (6 chars) — sem contexto de marca ou produto
- "Tela" (6 chars) — genérico demais
- "A Lola" (8 chars) — página institucional sem descritivo

---

## 4. Meta Descriptions

| Métrica | Valor |
|---------|-------|
| Média de caracteres | 71 chars |
| Meta desc < 50 chars | várias (muito curtas) |
| Meta desc > 155 chars | **36 (25,4%)** |
| Meta desc > 985 pixels | **35 (24,6%)** |
| **Meta desc duplicadas** | **45 (31,7%)** |
| **Meta desc ausentes** | **2 (1,4%)** |

**Problemas identificados:**

- **45 meta descriptions duplicadas (31,7%):** Muitas páginas de produto compartilham a mesma descrição genérica de categoria (ex: "A entretela de memória (ou entretela cavalinho) é utilizada para estruturar bonés...").
- **36 meta descriptions muito longas (> 155 chars):** Serão truncadas nos SERPs.
- **2 páginas sem meta description:** `/contato/` em ambas as versões do site.
- Muitas meta descriptions começam com o mesmo padrão ("Compre online...", "A entretela..."), reduzindo a diversidade nos SERPs.

---

## 5. Conteúdo e Readability

| Métrica | Valor |
|---------|-------|
| Média de palavras por página | ~700 palavras |
| Média Flesch Score | ~72 (Fairly Easy) |

**Distribuição de Readability:**

| Nível | Páginas | % |
|-------|---------|---|
| Fairly Easy | 86 | 60,6% |
| Normal | 23 | 16,2% |
| Easy | 19 | 13,4% |
| Very Easy | 11 | 7,7% |
| Fairly Hard | 2 | 1,4% |
| Hard | 1 | 0,7% |

**Análise:** O conteúdo é majoritariamente "Fairly Easy" — adequado para e-commerce B2B. Apenas 3 páginas têm readability difícil, o que é aceitável para conteúdo técnico.

**⚠️ Oportunidade:** Muitas páginas de produto têm conteúdo genérico (descrições curtas e repetitivas). Isso contribui para a alta taxa de duplicação de meta descriptions e títulos.

---

## 6. Imagens

| Métrica | Valor |
|---------|-------|
| Total de imagens | 255 |
| Formatos: WebP | 231 (90,6%) |
| Formatos: JPEG | 22 (8,6%) |
| Formatos: PNG | 2 (0,8%) |
| **Imagens sem atributo alt** | **255 (100%)** |
| Imagens sem size attributes | **129 (50,6%)** |
| Imagens > 100 KB | **48 (18,8%)** |
| Alt text > 100 chars | **20 (7,8%)** |

**🚨 CRÍTICO: 100% das imagens sem atributo alt.** Isso é uma falha grave de acessibilidade e SEO. O Google não consegue entender o conteúdo das imagens.

**Pontos positivos:**
- 90,6% das imagens estão em WebP (formato moderno e eficiente)
- Imagens hospedadas em CDN (acdn-us.mitiendanube.com)

**Oportunidades:**
- 129 imagens (50,6%) sem width/height attributes — causam layout shift (CLP)
- 48 imagens (18,8%) acima de 100 KB — podem impactar tempo de carregamento

---

## 7. Structured Data (Schema Markup)

| Métrica | Valor |
|---------|-------|
| Páginas COM structured data | **0 (0%)** |
| Páginas SEM structured data | **142 (100%)** |

**🚨 CRÍTICO: Zero páginas com structured data.** Isso significa:
- Sem rich snippets nos SERPs (estrelas, preço, disponibilidade)
- Sem Product schema para as páginas de produto
- Sem Organization/LocalBusiness schema
- Sem BreadcrumbList schema
- Sem FAQ schema para páginas de conteúdo

**Impacto:** Perda massiva de oportunidades de aparecer com rich results no Google.

---

## 8. Headings (H1/H2)

| Métrica | Valor |
|---------|-------|
| H1 non-sequential | **109 (76,8%)** |
| H1 duplicado | **2 (1,4%)** |
| H1 > 70 chars | **1 (0,7%)** |
| H2 duplicado | **110 (77,5%)** |
| H2 múltiplos | **78 (54,9%)** |
| H2 non-sequential | **78 (54,9%)** |

**⚠️ Problemas estruturais graves de headings:**
- **109 páginas (76,8%)** com H1 non-sequential — a hierarquia de headings está quebrada
- **110 páginas (77,5%)** com H2 duplicado — indica conteúdo repetitivo
- **78 páginas (54,9%)** com H2 múltiplos e non-sequential

**Provável causa:** A Nuvemshop gera headings de forma automática, sem seguir uma hierarquia semântica correta.

---

## 9. Links

| Métrica | Valor |
|---------|-------|
| Total internal links | 360 |
| Total external links | 1.500 |
| Internal outlinks sem anchor text | **142 (100%)** |
| Páginas com high external outlinks | **142 (100%)** |

**⚠️ 100% das páginas** têm external outlinks sem anchor text e high external outlinks. Isso é típico de e-commerce na Nuvemshop — provavelmente links para redes sociais, CDN, e serviços terceiros.

**Top páginas com mais inlinks (produtos mais linkados internamente):**
1. Tela de Poliéster 105g
2. Entretela Não Tecido para Bordado Toque Macio Rasgável 60g
3. Aba Plástica para Boné Curva 20kg
4. Aba Plástica para Boné Curva 196kg

---

## 10. Segurança

| Header | Ausente em |
|--------|-----------|
| X-Frame-Options | **142 páginas (92,8%)** |
| Referrer-Policy | **144 páginas (94,1%)** |
| Content-Security-Policy | **2 páginas (1,3%)** |
| HSTS | **2 páginas (1,3%)** |
| Unsafe Cross-Origin Links | **142 páginas (100%)** |
| Protocol-Relative Resource Links | **142 páginas (92,8%)** |

**🚨 CRÍTICO:** A grande maioria das páginas não possui headers de segurança básicos:
- **Sem X-Frame-Options:** Vulnerável a clickjacking
- **Sem Referrer-Policy:** Vazamento de informações de referência
- **Unsafe cross-origin links em 100% das páginas:** Links para CDN e recursos externos sem `rel="noopener"`

---

## 11. Hreflang

| Métrica | Valor |
|---------|-------|
| Páginas com hreflang | **0 (0%)** |

**Análise:** O site é monolíngue (português) e mono-país (Brasil), então a ausência de hreflang é esperada e **não é um problema**.

---

## 12. Performance (PageSpeed / Core Web Vitals)

**⚠️ SEM DADOS DISPONÍVEIS.** O campo `PSI Request Status` está vazio para todas as URLs. Não foi possível coletar:
- PageSpeed Insights (mobile/desktop)
- Core Web Vitals (LCP, FID/INP, CLS)
- Mobile usability

**Recomendação:** Executar auditoria manual de PageSpeed Insights para as páginas principais (home, categoria, produto).

---

## 13. Search Console e Analytics

**⚠️ SEM DADOS DE PERFORMANCE DISPONÍVEIS.** Os CSVs de Search Console e Analytics contêm apenas listagem de URLs, sem métricas de:
- Cliques, impressões, CTR, posição média
- Sessões, bounce rate, páginas/sessão, conversões

**Recomendação:** Conectar o Search Console e Google Analytics ao sistema de auditoria para obter dados de performance reais.

---

## 14. Prioridades de Ação

### 🔴 Crítico (resolver imediatamente)

| Prioridade | Ação | Impacto |
|-----------|------|---------|
| 1 | **Implementar structured data (schema markup)** em todas as páginas | Rich snippets, melhor CTR nos SERPs |
| 2 | **Remover 41 URLs non-indexable do sitemap** | Melhorar orçamento de rastreio |
| 3 | **Adicionar atributos alt em 100% das imagens** | Acessibilidade + SEO de imagens |
| 4 | **Corrigir headers de segurança** (X-Frame-Options, Referrer-Policy, CSP, HSTS) | Segurança + confiança do Google |
| 5 | **Corrigir 2 páginas com erro 4xx** | Eliminar erros de rastreio |

### 🟡 Alta Prioridade

| Prioridade | Ação | Impacto |
|-----------|------|---------|
| 6 | **Revisar 35 títulos < 30 chars** — adicionar contexto de marca/produto | Melhor CTR nos SERPs |
| 7 | **Corrigir 12 títulos duplicados** | Evitar canibalização |
| 8 | **Corrigir 45 meta descriptions duplicadas** | Melhor diversidade nos SERPs |
| 9 | **Adicionar width/height em 129 imagens** | Reduzir CLS (Core Web Vitals) |
| 10 | **Corrigir hierarquia de headings (H1/H2)** em 109 páginas | Melhor semântica HTML |

### 🟢 Média Prioridade

| Prioridade | Ação | Impacto |
|-----------|------|---------|
| 11 | **Otimizar 48 imagens > 100 KB** | Melhor tempo de carregamento |
| 12 | **Diferenciar 46 títulos que são iguais ao H1** | Mais palavras-chave nos SERPs |
| 13 | **Revisar 36 meta descriptions > 155 chars** | Evitar truncamento nos SERPs |
| 14 | **Corrigir 7 URLs bloqueadas por robots.txt** | Melhorar rastreamento |

---

## 15. Recomendações Técnicas por Plataforma (Nuvemshop)

Por ser uma plataforma Nuvemshop, algumas limitações se aplicam:

1. **Structured data:** Verificar se o tema atual suporta Product schema nativamente. Caso contrário, considerar customização via JavaScript ou app.
2. **Sitemap:** A Nuvemshop gera o sitemap automaticamente. Pode ser necessário configurar exclusões ou usar um app para filtrar URLs non-indexable.
3. **Alt text em imagens:** A Nuvemshop permite adicionar alt text nas imagens dos produtos. É um trabalho manual de preenchimento.
4. **Page titles e meta descriptions:** Totalmente customizáveis por produto/categoria na Nuvemshop.
5. **Headings:** A hierarquia de headings depende do tema. Pode exigir customização de template.
6. **Headers de segurança:** Configuráveis via .htaccess ou painel da hospedagem/Nuvemshop.

---

## 16. Métricas-Chave (Resumo)

| KPI | Atual | Meta | Status |
|-----|-------|------|--------|
| Páginas com structured data | 0% | 100% | ❌ Crítico |
| URLs non-indexable no sitemap | 27,2% | 0% | ❌ Crítico |
| Imagens com alt text | 0% | 100% | ❌ Crítico |
| Páginas com X-Frame-Options | 7,2% | 100% | ❌ Crítico |
| Títulos < 30 chars | 24,6% | < 5% | ❌ Ruim |
| Títulos duplicados | 8,5% | 0% | ⚠️ Ruim |
| Meta desc duplicadas | 31,7% | < 5% | ❌ Ruim |
| H1 non-sequential | 76,8% | < 10% | ❌ Ruim |
| Erros 4xx | 2 URLs | 0 | ⚠️ Médio |
| Readability (Fairly Easy ou melhor) | 97,2% | > 90% | ✅ Bom |
| Imagens em WebP | 90,6% | > 90% | ✅ Bom |

---

## 17. OKRs Sugeridos (Próximos 90 Dias)

| OKR | KR | Meta Atual | Meta 90d |
|-----|----|-----------|----------|
| **Melhorar presença nos SERPs** | KR1: Implementar structured data em 100% das páginas | 0% | 100% |
| | KR2: Reduzir títulos < 30 chars para < 5% | 24,6% | < 5% |
| | KR3: Eliminar meta desc duplicadas | 31,7% | 0% |
| **Melhorar rastreamento e indexação** | KR4: Remover URLs non-indexable do sitemap | 27,2% | 0% |
| | KR5: Corrigir erros 4xx | 2 URLs | 0 |
| **Melhorar acessibilidade e segurança** | KR6: Adicionar alt text em 100% das imagens | 0% | 100% |
| | KR7: Implementar headers de segurança (X-Frame-Options, Referrer-Policy) | < 10% | 100% |
| **Melhorar semântica HTML** | KR8: Corrigir hierarquia H1/H2 | 23,2% ok | > 90% ok |

---

*Relatório gerado em Julho 2026 com base em auditoria técnica de 153 URLs do site Lola Aviamentos.*