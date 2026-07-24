# Grupo R1 — Pendências da Auditoria Técnica SEO

Fonte: https://marcoslrvusa.github.io/Grupo-R1-SEO-Audit/  
Score atual: **3.8 / 10** | Esforço total: **185,5 h**

---

## Críticos (impedem indexação e ranqueamento)

- [ ] **C-01** — Canonical mismatch do blog apontando para `/?page_id=3511` + categorias com 404
- [x] **C-02** — Article schema no blog (`TAREFA-C02-article-schema-blog.md`)
- [ ] **C-03** — 4 broken internal links (blog/projetos-e-cases, blog/tendencias-de-mercado, blog/equipamentos-audiovisuais, blog/tecnologia-para-eventos)

---

## Alto (impactam CTR e experiência)

- [ ] **A-01** — 47 page titles truncados no SERP (>561px / >60 caracteres)
- [ ] **A-02** — 32 páginas sem meta description + 22 com description longa demais
- [ ] **A-03** — 22 páginas sem H1 + homepage com 5 H1s
- [ ] **A-04** — 96% das imagens >200 KB, zero WebP, 63,9 MB total
- [ ] **A-05** — 18 páginas de projeto com thin content (<200 palavras)
- [ ] **A-06** — Diretório `/devel/` exposto e indexável
- [ ] **A-07** — 28 redirect chains de `/portfolio/*` → `/projetos/*`

---

## Médio (oportunidades de melhoria)

- [ ] **M-01** — Missing Referrer-Policy header (90,15% das URLs)
- [ ] **M-02** — Páginas de categoria sem conteúdo introdutório

---

## Baixo (polimento)

- [ ] **B-01** — URLs de parâmetro no blog (`/?page_id=3511`)

---

## Por especialidade

### Dev WordPress (34 h)
- Corrigir canônico do blog e das categorias
- 301 redirects dos broken links e redirect chains
- Organization + Breadcrumb + Article + Product schema
- Bloquear `/devel/` no robots.txt
- WebP + compressão de imagens (LiteSpeed)
- Referrer-Policy header no .htaccess
- Lazy loading nativo

### SEO (43,5 h)
- H1 único em 22 páginas + reduzir homepage para 1 H1
- Reescrever 47 page titles (50-60 caracteres)
- Alt text das imagens
- Mapear 4 clusters temáticos + links hub/spokes
- Validar correções e monitorar rankings

### Copywriter (104 h)
- 32 meta descriptions + 22 descriptions longas
- 18 páginas de projeto expandidas para 500+ palavras
- Conteúdo introdutório das categorias
- 4 páginas hub (2000+ palavras) + 8 artigos spoke (1000+ palavras)

---

> Documento baseado na auditoria de Junho/2026. Prioridade máxima: C-01 (canônico do blog).
