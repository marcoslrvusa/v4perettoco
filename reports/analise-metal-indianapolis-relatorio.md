# Relatório de Auditoria SEO — Metal Indianápolis

**Data:** 19/06/2026  
**Site:** https://lightblue-loris-222364.hostingersite.com/  
**Analista:** SEO Squad — Data Analyst  

---

## 1. Diagnóstico de Indexação: 🔴 CRÍTICO

### Páginas indexadas no Google: **ZERO**

### Causa Raiz — robots.txt incorreto

```
User-agent: Googlebot
Disallow: /
```

O Googlebot está **completamente bloqueado** de rastrear qualquer página do site. Curiosamente, outros bots (`*`) estão liberados (`Allow: /`). Isso parece um erro de configuração — provavelmente o `Disallow: /` foi adicionado durante o desenvolvimento e nunca foi removido.

---

## 2. Inventário Completo do Site (via Sitemaps)

Apesar de não estar indexado, o site tem **84 URLs** prontas e bem estruturadas no sitemap (Yoast SEO):

| Tipo | Quantidade | Exemplos |
|------|-----------|----------|
| **Páginas institucionais** | 5 | Home, Empresa, Soluções, Produtos, Contato |
| **Blog posts** | 49 | artigos técnicos sobre fundição, anéis de segmento, peças |
| **Produtos (WooCommerce)** | 17 | Abraçadeira fixa, Anéis de Segmento, Polia de elevador... |
| **Categorias de blog** | 4 | Componentes Mecânicos, Fundição, Materiais, Processos Industriais |
| **Categorias de produto** | 6 | Automotivo, Construção Civil, Máquinas e Equipamentos... |
| **Autores** | 1 | perettov4company-com |
| **Total** | **84** | |

**Ou seja:** 84 páginas com conteúdo relevante estão invisíveis para o Google.

---

## 3. Análise de Conteúdo do Blog

O blog tem **49 posts** com palavras-chave de alto valor para o setor industrial:

- `ferro fundido cinzento`
- `fundição em São Paulo`
- `anel de segmento para compressor`
- `peças para bombeamento de concreto`
- `fabricante de peças automotivas`
- `preço do ferro fundido kg`
- E dezenas de outras variações de cauda longa

📌 **Potencial desperdiçado:** Esses termos têm intenção de compra B2B forte (engenheiros, compradores industriais buscando fornecedores).

---

## 4. Stack Tecnológica

| Componente | Identificado |
|-----------|-------------|
| **CMS** | WordPress |
| **Page Builder** | Elementor |
| **E-commerce** | WooCommerce |
| **SEO Plugin** | Yoast SEO (sitemaps ativos) |
| **Caching** | WP Rocket |
| **Imagens** | WebP (otimizadas) |
| **Hospedagem** | Hostinger (subdomínio temporário) |

✅ **Positivo:** Sitemaps bem configurados, WebP, cache ativo.  
⚠️ **Negativo:** Elementor pode adicionar CSS/JS pesados, e o subdomínio Hostinger impede construção de autoridade.

---

## 5. Backlinks e Autoridade

- **Zero backlinks** — o site está em um subdomínio temporário `hostingersite.com`, que não tem autoridade e provavelmente nunca terá.
- A empresa **tem presença em redes sociais**: Instagram e LinkedIn (links no site).
- O contato e endereço físico são reais (Rua do Zinco, 205/225 — Itaquaquecetuba, SP), o que é um bom sinal de E-A-T.

---

## 6. Sobre a Empresa (Contexto para SEO)

| Dado | Valor |
|------|-------|
| Fundação | 1966 (60+ anos) |
| Certificação | ISO 9001 |
| Localização | Itaquaquecetuba, SP |
| Segmentos | Automotivo, Construção Civil, Máquinas, Agrícola, Ferroviário, Vidreiro |
| Produtos | Anéis de segmento, peças fundidas, usinagem CNC, componentes industriais |

💡 **Forte E-A-T:** Empresa com 60 anos de história + ISO 9001 = excelente base para SEO B2B.

---

## 7. Recomendações (Priorizadas)

### 🔴 Imediatas (esta semana)

| # | Ação | Impacto |
|---|------|---------|
| 1 | **Corrigir robots.txt** → alterar `Disallow: /` para `Allow: /` no Googlebot | Desbloqueia todo o site |
| 2 | **Solicitar reindexação** no Google Search Console | Inicia o processo de indexação |
| 3 | **Submeter sitemaps** manualmente no GSC | Acelera a descoberta das 84 URLs |

### 🟡 Curto Prazo (1 mês)

| # | Ação |
|---|------|
| 4 | Definir domínio definitivo (ex: indianapolis.com.br) e planejar migração |
| 5 | Configurar Google Search Console + Google Analytics 4 |
| 6 | Avaliar PageSpeed Insights e otimizar performance |

### 🟢 Médio Prazo (2-3 meses)

| # | Ação |
|---|------|
| 7 | Criar páginas dedicadas para cada segmento industrial (7 oportunidades) |
| 8 | Manter produção de conteúdo técnico no blog |
| 9 | Implementar schema markup (Organization, LocalBusiness, Product, Article) |

---

## 8. KPIs Sugeridos para Acompanhamento Pós-Correção

### Semana 1-4: Descoberta
- ✅ Páginas indexadas — meta: 84/84 em 30 dias
- ✅ Erros de crawling no GSC — meta: zero
- ✅ Impressões e cliques orgânicos (baseline)

### Mês 2-3: Estabilização
- 📈 Crescimento de impressões semana a semana
- 📈 CTR médio orgânico
- 📈 Posição média para palavras-chave principais

### Mês 4-6: Otimização
- 💰 Conversões orgânicas (formulários de cotação)
- 💰 Leads gerados via tráfego orgânico
- 🔗 Backlinks (após domínio definitivo)

---

## 9. Resumo em Uma Linha

> Site com 84 páginas de conteúdo B2B industrial de qualidade está **100% invisível** para o Google por causa de uma linha errada no robots.txt. Corrigir isso é a ação mais barata e de maior impacto que pode ser feita agora.

---

*Relatório gerado pelo SEO Squad — Data Analyst em 19/06/2026*
