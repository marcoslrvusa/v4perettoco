# Template Padrão — Relatórios SEO / AIO / GEO

Este é o template visual padrão para todos os relatórios de SEO, AIO e GEO da V4 Company.

## Localização

- Relatórios ficam em `projetos/seo/clientes/{cliente}/{cliente}-seo-audit.html`
- Assets (logos) ficam em `projetos/seo/clientes/{cliente}/assets/`
- Assets obrigatórios: `logo-v4-white.png` (V4 Company) + `logo-{cliente}.{ext}`

## Estrutura visual

### Cabeçalho (Cover)
- Fundo escuro gradient (`#0d0d0d` → `#1a1a1a` → `#2a2a2a`)
- Logos lado a lado no topo: V4 Company (esquerda) + Cliente (direita)
- Badge de confidencialidade com mês/ano
- Título: "Auditoria SEO + AIO + GEO" (ou o escopo específico)
- Subtítulo: nome do cliente
- Metadados: ferramenta, URLs rastreadas, CSVs analisados

### Paleta de cores
- `--red: rgb(229, 9, 20)` — cor primária V4, usada em títulos, valores KPI, badges críticos
- `--gold: #c9a96e` — cor de destaque, bordas, linhas decorativas
- `--gold-light: #f5f0e6` — fundo de badges baixo
- Cinzas escala — `--gray-50` a `--gray-900`

### Cards
- `.card` — container branco com borda arredondada (16px), sombra suave, borda gold no topo
- `.card-body` — padding interno de 44px 52px (24px 20px em mobile)
- `.finding` — bloco de achado com hover, borda lateral, grid 2 colunas
- `.kpi-grid` — grid de 5 colunas com cards de KPI (2 em mobile)
- `.timeline` — linha do tempo horizontal com fases coloridas
- `.risk-box` — box vermelho com borda esquerda para riscos críticos

### Severidade
- `.badge-critico` / `.sev-critico` — vermelho (#fef2f2 fundo)
- `.badge-alto` / `.sev-alto` — laranja (#fff7ed fundo)
- `.badge-medio` / `.sev-medio` — amarelo (#fefce8 fundo)
- `.badge-baixo` / `.sev-baixo` — gold claro (#f5f0e6 fundo)
- `.badge-info` / `.sev-info` — cinza (#f5f5f5 fundo)

### Status indicators
- `.status.ok` — verde (#16a34a)
- `.status.warn` — laranja (#c2410c)
- `.status.fail` — vermelho (#e50914)

### Bar charts
- `.bar-container` / `.bar-row` / `.bar-track` / `.bar-fill` — barras horizontais
- Cores: `.red`, `.orange`, `.gold`, `.gray`

### Footer
- Logos lado a lado (V4 + Cliente)
- Texto: "V4 Company & peretto.co"
- Confidencial + data + slug + versão

### Responsivo
- Breakpoint 640px: cover reduzido, card-body compacto, grid 2 colunas, timeline wrap

## Como usar

1. Copiar `lola/lola-seo-audit.html` como base
2. Substituir dados, findings, tabelas e KPIs
3. Trocar `logo-lola.webp` pelo logo do cliente em `assets/`
4. Ajustar título, subtítulo, badges e severidades
5. Publicar via gh-pages em `{cliente}-seo-audit/`

## Exemplos publicados

- `lola-seo-audit/` — lolaaviamentos.com.br
- `indianapolis-seo-audit/` — metalindianapolis.com.br
