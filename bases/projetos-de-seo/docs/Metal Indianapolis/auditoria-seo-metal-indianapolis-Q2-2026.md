# Auditoria Técnica SEO — Metal Indianápolis (preview.indianapolis.com.br)

**Data:** Junho 2026 | **Versão:** 2.0 (Revisão SEO Squad) | **Classificação:** Confidencial Cliente
**Ferramenta:** Screaming Frog SEO Spider | **Amostra:** 260 URLs rastreadas (43 HTML indexáveis)

---

## Sumário

| Métrica | Valor |
|---|---|
| **Saúde Geral SEO** | **3.5 / 10** |
| **Problemas identificados** | 25 (7 Críticos, 6 Alto, 7 Médio, 0 Baixo, 6 Info) |
| **Horas totais para correção** | 136,5 h (Fase 0 + 3 meses) |
| **Projeção de tráfego orgânico (90 dias)** | +30% a +50% |
| **Fase 0 — Pré-Lançamento** | 20 h (obrigatório antes do go-live) |

### Evolução do Projeto

| Fase | Horas | % do Total | Entregas Principais |
|---|---|---|---|
| **Fase 0** — Pré-Lançamento | 20 h | 15% | DNS typos · H1 + H2 · Schema base · GSC + Sitemap |
| **Mês 1** — Fundação Técnica | 30 h | 22% | Product/Article schema · Meta desc · Titles únicos · Performance |
| **Mês 2** — Conteúdo e Estrutura | 41,5 h | 30% | Categorias → 500+ palavras · 2 hubs (Fundição + CNC) · FAQ schema |
| **Mês 3** — Expansão e Monitoramento | 50 h | 37% | +2 hubs · +4 spokes · Core Web Vitals · Monitoramento |
| **Total** | **136,5 h** | **100%** | **+30% a +50% tráfego projetado em 90 dias** |

### Top 3 Riscos que Exigem Atenção Imediata do C-Level

1. **Zero structured data em 100% das páginas + H2 poluído.** 43/43 páginas sem JSON-LD. Telefone e email renderizados como H2 em todas as páginas — poluindo o entendimento semântico do Google. Concorrentes diretos ocupam rich snippets enquanto a Metal Indianápolis compete com "link azul simples". CTR estimado 20-30% inferior.

2. **6 páginas críticas sem H1 + 3 produtos com H1 trocado.** Home, contato, produtos, blog, empresa e soluções não têm H1. Em 3 produtos, o H1 não corresponde ao nome (ex: "Soquete do Tirante" no lugar de "Tirante para Elevador"). Quebra o message match entre SERP e página.

3. **~30 assets quebrados a revisar + 30 páginas com meta descriptions duplicadas.** Assets que não carregam (imagens, logotipos, ícones) — possível artefato de staging que precisa ser revisado durante a migração para produção. Além disso, 30 das 43 páginas HTML têm meta descriptions duplicadas de até 700 caracteres — Google gera description automática, perdendo o controle do texto exibido no SERP.

---

## Perfil do Site

| Característica | Detalhe |
|---|---|
| **Domínio** | preview.indianapolis.com.br (staging &rarr; URL de produ&ccedil;&atilde;o a definir pelo marketing) |
| **Segmento** | Metalurgia — fundição de ferro fundido nodular, cinzento e usinagem CNC |
| **CMS** | WordPress + Elementor + WooCommerce |
| **Plugins** | Royal Elementor Addons, Contact Form 7, Complianz GDPR, Header Footer Elementor |
| **Idioma** | pt-BR (sem versões multilíngue) |
| **Total URLs rastreadas** | 260 |
| **URLs HTML indexáveis** | 43 |
| **URLs não-indexáveis** | 4 (1 redirect /home/, 3 DNS lookup failed) |
| **Mobile** | Responsivo (Hello Elementor theme) |
| **Sitemap XML** | Presente (45 URLs listadas) |
| **Response time médio** | ~0,9s (6 páginas acima de 1,5s) |
| **HTTPS** | Válido. Sem mixed content. Security headers ausentes. |

---

## Diagnóstico Técnico Detalhado

### 🔴 Críticos — Impedem Indexação e Ranqueamento

#### C-01. Zero Structured Data em Todas as Páginas HTML
| Campo | Descrição |
|---|---|
| **Evidência** | 43/43 páginas HTML (100%) sem qualquer JSON-LD ou Microdata. Zero rich snippets. |
| **Impacto** | Perda total de diferenciação no SERP. Concorrentes ocupam 2× o espaço visual. CTR 20-30% inferior. |
| **Recomendação** | Organization + BreadcrumbList + Product + Article + FAQ schema |
| **Esforço** | 10 h (Dev WordPress + SEO) |

#### C-02. DNS Typos — Assets Quebrados por Erro no Domínio
| Campo | Descrição |
|---|---|
| **Evidência** | 4 URLs em `preview.indianpolis.com.br` (sem "a"): telephone.png, mail.png, 2 logotipos. Todas DNS lookup failed. |
| **Impacto** | Ícones e logotipos quebrados. Experiência comprometida. Sinal de baixa maturidade técnica. |
| **Recomendação** | Corrigir 4 URLs no tema Elementor + verificar hard-coded references |
| **Esforço** | 2 h (Dev WordPress) |

#### C-03. Homepage + 5 Páginas Críticas Sem H1
| Campo | Descrição |
|---|---|
| **Evidência** | 6 páginas com H1 vazio: Home, /contato/, /produtos/, /blog/, /empresa/, /solucoes/. |
| **Impacto** | Google perde sinal hierárquico principal. Homepage sem H1 = perda severa de ranqueamento. |
| **Recomendação** | Adicionar H1 único com keyword primária em cada página |
| **Esforço** | 4 h (SEO / Dev WordPress) |

#### C-04. H1 de Produtos Não Corresponde ao Nome do Produto
| Campo | Descrição |
|---|---|
| **Evidência** | 3 páginas: /tirante-para-elevador/ (H1="Soquete do Tirante"), /pecas-bomba-concreto/ (H1="Curva Bomba Concreto"), /rolo-de-apoio-para-betoneira/ (H1="Bucha do Rolo de Apoio"). |
| **Impacto** | Quebra de message match. Usuário chega do Google com title X e encontra H1 Y. Aumento de rejeição. |
| **Recomendação** | Alinhar H1 ao title em cada página. Revisar template do Elementor. |
| **Esforço** | 1 h (SEO / Dev WordPress) |

#### C-05. Telefone e Email Renderizados como H2 em 100% das Páginas
| Campo | Descrição |
|---|---|
| **Evidência** | (11) 4649-7722 e vendas@indianapolis.com.br como H2 em todas as 43 páginas. |
| **Impacto** | Poluição semântica severa. Google usa H2 como segundo nível hierárquico. Agrava problema de headings em páginas sem H1. |
| **Recomendação** | Remover do H2 no template global do Elementor. Renderizar como texto ou paragraph. |
| **Esforço** | 4 h (Dev WordPress) |

#### C-06. H1 Duplicado em 12 Páginas de Blog
| Campo | Descrição |
|---|---|
| **Evidência** | 12 páginas (não 8) com H1 duplicado — 2 ocorrências do mesmo H1. |
| **Impacto** | Google ignora ambos. Perda completa de sinal semântico em páginas que deveriam ranquear. |
| **Recomendação** | Remover H1 duplicado. Revisar template do Elementor. |
| **Esforço** | 3 h (Dev WordPress) |

#### C-07. Meta Descriptions Duplicadas em 30 Páginas
| Campo | Descrição |
|---|---|
| **Evidência** | 30 páginas (18 produtos + 12 blogs) com 2 meta descriptions. Segunda com 400-700 caracteres. |
| **Impacto** | Google ignora ambas. Páginas sem controle sobre texto exibido no SERP. Perda de CTR 10-20%. |
| **Recomendação** | Remover description longa. Manter 120-155 caracteres com CTA. |
| **Esforço** | 8 h (SEO / Copywriter) |

---

### 🟠 Alto — Impactam Diretamente CTR e Experiência

#### A-01. Page Titles Duplicados e Incorretos
| Campo | Descrição |
|---|---|
| **Evidência** | "Rolo de Apoio para Betoneira" em 4 URLs. Placa de Ancoragem com title errado. |
| **Impacto** | Canibalização de palavras-chave. Informação enganosa no SERP. |
| **Recomendação** | Corrigir titles. Diferenciar páginas de rolo de apoio. |
| **Esforço** | 6 h (SEO) |

#### A-02. Categoria "Sem Categoria" Indexável
| Campo | Descrição |
|---|---|
| **Evidência** | /sem-categoria/ indexável, title genérico, 277 palavras, sem meta description. |
| **Impacto** | Google indexa página sem valor editorial. |
| **Recomendação** | noindex ou criar conteúdo descritivo + mover produtos. |
| **Esforço** | 2 h (SEO / Dev WordPress) |

#### A-03. Páginas Lentas (6 acima de 1,5s)
| Campo | Descrição |
|---|---|
| **Evidência** | /solucoes/ (2,258s), /empresa/ (1,931s), +4 entre 1,5-1,7s. |
| **Impacto** | Core Web Vitals comprometidos. Taxa de rejeição maior. |
| **Recomendação** | Otimizar imagens, scripts, lazy loading, cache. |
| **Esforço** | 6 h (Dev WordPress) |

#### A-04. Category Page Titles Genéricos
| Campo | Descrição |
|---|---|
| **Evidência** | "Arquivo de Indústria Vidreira - preview.indianapolis.com.br" — padrão genérico. |
| **Impacto** | Google apresenta título sem valor no SERP. |
| **Recomendação** | Renomear titles das categorias. Remover prefixo "Arquivo de". |
| **Esforço** | 1 h (SEO) |

#### A-05. Imagens sem Atributos de Largura/Altura
| Campo | Descrição |
|---|---|
| **Evidência** | Múltiplas imagens sem dimensões definidas — risco de CLS. |
| **Impacto** | Core Web Vitals (CLS) comprometido. Layout "pula" durante carregamento. |
| **Recomendação** | Adicionar width/height em todas as imagens. |
| **Esforço** | 4 h (Dev WordPress) |

#### A-06. Meta Descriptions Vazias em Categorias
| Campo | Descrição |
|---|---|
| **Evidência** | /sem-categoria/ e /industria-vidreira/ sem meta description. |
| **Impacto** | Google gera description automática. Perda de CTR. |
| **Recomendação** | Escrever meta descriptions únicas com CTA e diferenciais. |
| **Esforço** | 1 h (Copywriter) |

---

### 🟡 Médio — Oportunidades de Melhoria

#### M-01. Missing Referrer-Policy Header
| Campo | Descrição |
|---|---|
| **Impacto** | Perda de dados de referenciamento. Risco de segurança. |
| **Recomendação** | Configurar strict-origin-when-cross-origin |
| **Esforço** | 1 h (Dev WordPress) |

#### M-02. Variação de Nome nos Titles (Indianópolis vs Indianápolis)
| Campo | Descrição |
|---|---|
| **Evidência** | 22 páginas "Indianópolis", 21 "Indianápolis" — divisão 50/50. |
| **Impacto** | Inconsistência de marca. Google pode interpretar como duas entidades. |
| **Recomendação** | Padronizar para "Metal Indianápolis". |
| **Esforço** | 2 h (SEO) |

#### M-03. Categorias sem Conteúdo Próprio
| Campo | Descrição |
|---|---|
| **Evidência** | 6 categorias com 275-375 palavras. Meta descriptions ausentes. |
| **Impacto** | Thin content. Google pode desvalorizar. |
| **Recomendação** | Adicionar 150-300 palavras + meta descriptions únicas. |
| **Esforço** | 6 h (Copywriter) |

#### M-04. /home/ Redirect com 42 Links Internos
| Campo | Descrição |
|---|---|
| **Impacto** | Pequena diluição de link equity. Baixo impacto em pré-lançamento. |
| **Recomendação** | Atualizar 42 links internos para / direto. |
| **Esforço** | 2 h (Dev WordPress) |

#### M-05. Security Headers Ausentes
| Campo | Descrição |
|---|---|
| **Evidência** | Sem HSTS, X-Content-Type-Options, X-Frame-Options. |
| **Impacto** | Risco de segurança e confiança para site B2B. |
| **Recomendação** | Implementar headers no .htaccess. |
| **Esforço** | 1 h (Dev WordPress) |

#### M-06. Placeholder.png do Elementor
| Campo | Descrição |
|---|---|
| **Evidência** | Placeholder padrão sendo servida — imagem não configurada. |
| **Impacto** | Imagem sem valor. Template incompleto. |
| **Recomendação** | Substituir. Revisar templates por imagens faltantes. |
| **Esforço** | 1 h (Dev WordPress) |

---

### ℹ️ Informativos

I-01. Paginação com rel next/prev correta
I-02. Distribuição saudável de links internos
I-03. Response time bom na maioria (~1,2s)
I-04. Sitemap XML presente
I-05. HTTPS + SSL válido
I-06. Mobile responsivo
I-07. Monolíngue pt-BR (hreflang ausente é correto)
I-08. Meta keywords ausentes (boa prática)
I-09. Links externos para redes sociais (sem spam)
I-10. Imagens em WebP (bom), Background.webp 115KB pode comprimir

---

## Fase 0 — Pré-Lançamento

Sprint de 2 semanas **obrigatório antes do go-live**. O site não deve ir ao ar sem estas correções:

| # | Ação | Horas | Resp. |
|---|---|---|---|
| 1 | Corrigir DNS typos (indianpolis → indianapolis) | 2 | Dev WP |
| 2 | Adicionar H1 único na Homepage + 5 páginas críticas | 4 | SEO |
| 3 | Remover telefone/email dos H2 em todo o template | 4 | Dev WP |
| 4 | Corrigir H1 de 3 produtos que não correspondem | 1 | SEO |
| 5 | Organization + BreadcrumbList schema global | 4 | Dev WP |
| 6 | noindex em /categoria-produto/sem-categoria/ | 0,5 | Dev WP |
| 7 | Configurar GSC + enviar sitemap | 1 | SEO |
| 8 | Corrigir title da /placa-de-ancoragem/ | 0,5 | SEO |
| 9 | Verificar robots.txt e meta robots | 1 | SEO |
| 10 | Configurar Referrer-Policy + Security Headers | 2 | Dev WP |
| **Total** | | **20 h** | |

---

## Plano de Ação Trimestral

### Mês 1 — Fundação Técnica (Dias 1-30 pós Fase 0) — 30 h

| # | Ação | Horas | Resp. | Prioridade |
|---|---|---|---|---|
| 1 | Product schema WooCommerce | 4 | Dev WP | 1 |
| 2 | Article schema blog | 2 | Dev WP | 2 |
| 3 | Remover H1 duplicado (12 páginas blog) | 3 | Dev WP | 3 |
| 4 | Corrigir meta descriptions duplicadas (30 páginas) | 8 | SEO/Copy | 4 |
| 5 | Corrigir category page titles genéricos | 1 | SEO | 5 |
| 6 | Diferenciar titles das 4 páginas de rolo de apoio | 2 | SEO | 6 |
| 7 | Padronizar brand name (Indianópolis → Indianápolis) | 2 | SEO | 7 |
| 8 | Otimizar imagens (compressão + width/height) | 4 | Dev WP | 8 |
| 9 | Otimizar 6 páginas lentas (performance) | 6 | Dev WP | 9 |
| 10 | Atualizar 42 links internos de /home/ para / | 2 | Dev WP | 10 |

### Mês 2 — Conteúdo e Estrutura (Dias 31-60) — 41,5 h

| # | Ação | Horas | Resp. |
|---|---|---|---|
| 1 | Meta descriptions para categorias + produtos restantes | 3 | Copywriter |
| 2 | Conteúdo introdutório em 6 categorias | 6 | Copywriter |
| 3 | Otimizar alt text (prioridade: produtos) | 4 | SEO |
| 4 | FAQ schema nas páginas informacionais | 4 | Dev WP |
| 5 | Mapear 2 clusters (Fundição Ferro + Usinagem CNC) | 4 | SEO |
| 6 | 2 páginas hub (2000+ palavras cada) | 16 | Copywriter |
| 7 | Malha de links internos hubs + conteúdo existente | 4 | SEO |
| 8 | Substituir placeholder.png | 0,5 | Dev WP |
| 9 | Revisar e testar correções do Mês 1 | 4 | SEO |

### Mês 3 — Expansão e Monitoramento (Dias 61-90) — 50 h

| # | Ação | Horas | Resp. |
|---|---|---|---|
| 1 | Mapear 2 clusters (Peças Industriais + Construção Civil) | 4 | SEO |
| 2 | 2 páginas hub adicionais (2000+ palavras) | 16 | Copywriter |
| 3 | 4 artigos spoke (1000+ palavras) | 12 | Copywriter |
| 4 | FAQPage schema nas páginas hub | 2 | Dev WP |
| 5 | Revisar e expandir links internos | 4 | SEO |
| 6 | Configurar monitoramento de rankings | 2 | SEO |
| 7 | Testar Core Web Vitals | 3 | SEO |
| 8 | Visuais para hubs (infográficos) | 4 | Designer |
| 9 | Relatório de fechamento do trimestre | 3 | SEO |

---

## Resumo de Esforço Consolidado

| Especialidade | Fase 0 | Mês 1 | Mês 2 | Mês 3 | Total |
|---|---|---|---|---|---|
| Desenvolvedor WordPress | 8,5 h | 15 h | 4,5 h | 2 h | **30 h** |
| SEO | 6,5 h | 13 h | 15 h | 16 h | **50,5 h** |
| Copywriter | — | 2 h | 22 h | 28 h | **52 h** |
| Designer | — | — | — | 4 h | **4 h** |
| **Total** | **15 h** | **30 h** | **41,5 h** | **50 h** | **136,5 h** |

*Fase 0 (20 h adicionais) não está incluída no escopo trimestral — é pré-requisito para o lançamento.*

---

## Projeção de Impacto

| Métrica | Conservador | Otimista |
|---|---|---|
| **Tráfego orgânico (90 dias)** | +30% | +50% |
| **Páginas indexadas** | 43 → 55+ | 43 → 65+ |
| **CTR médio no SERP** | +10% | +20% |
| **Core Web Vitals pass** | LCP < 2,5s | LCP < 2,0s |
| **Rich snippets** | 0 → 30+ | 0 → 43+ |

---

## KPIs para Acompanhamento Mensal

| KPI | Fase 0 | Mês 1 | Mês 2 | Mês 3 |
|---|---|---|---|---|
| Páginas indexadas | 43 | 43 → 48 | 48 → 55 | 55 → 65 |
| Páginas com schema | 100% | 100% | 100% | 100% |
| Páginas com H1 único | 100% | 100% | 100% | 100% |
| H2 sem telefone/email | 100% | 100% | 100% | 100% |
| DNS errors | 0 | 0 | 0 | 0 |
| Titles sem duplicação | 79% → 85% | 85% → 95% | 95% → 100% | 100% |
| Meta descriptions únicas | 58% → 70% | 70% → 85% | 85% → 100% | 100% |
| Categorias com thin content | 6 → 4 | 4 → 2 | 2 → 0 | 0 |
| Páginas lentas (> 1,5s) | 6 → 3 | 3 → 0 | 0 | 0 |

---

## Revisão do SEO Squad

Esta auditoria foi revisada pelo SEO Squad completo da V4 Company:

- **SEO Visibilidade (líder):** 7 novos problemas encontrados, severidades reclassificadas, score revisado de 4.2 → 3.5/10
- **Analista de Dados:** Performance média ~0,9s, 6 páginas lentas (não 2), blog com conteúdo de qualidade (2400-3900 palavras), imagens em WebP sem atributos de dimensão
- **Estrategista de Marketing:** 4 clusters temáticos propostos (Fundição de Ferro, Usinagem CNC, Peças Industriais, Construção Civil), gap crítico em Usinagem CNC (sem página própria)

### Erros corrigidos na auditoria original (v1.0 → v2.0)

1. **H1 duplicado**: 8 → **12** páginas
2. **Meta descriptions duplicadas**: 18 → **30** páginas
3. **Páginas lentas**: 2 → **6** páginas acima de 1,5s
4. **Categorias sem conteúdo**: 4 → **6** categorias
5. **Score de saúde**: 4.2 → **3.5/10** (após validação completa dos CSVs)
6. **Problemas totais**: 18 → **25** (7 novos)

---

*Documento gerado em Junho de 2026 pela equipe de SEO da V4 Company.*
*Revisão v2.0 — SEO Squad (seo-visibilidade, analista-dados, estrategista-marketing).*
