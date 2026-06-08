# Sessão: i18n + Imagens + Lead Magnet

## Data: 2026-06-05

## O que foi feito:
1. **i18n**: Instalado next-intl, criado routing/request/navigation/middleware, movido app/ para [locale], seletor de idiomas no header
2. **Traduções**: messages/pt.json, en.json, es.json com todos os namespaces (site, home, header, footer, newsletter, post, common, ebook)
3. **Imagens reais**: 7 covers de artigos baixados do Unsplash/Pexels, substituindo SVGs genéricos
4. **PostCard**: agora exibe cover image com hover zoom
5. **Componentes interativos**: ParticleBackground (canvas), ReadingProgress, TerminalText, BackToTop, scroll-reveal animations
6. **Lead magnet**: E-book "Guia Prático de AI Search" em PT/EN, página gated por email com print-to-PDF
7. **Google Sheets**: API newsletter já faz POST para GOOGLE_SHEETS_WEBHOOK_URL se configurado
8. **Build corrigido**: next-intl plugin path, messages movidos pra src/

## Pendente:
- Traduzir posts de PT para EN e ES
- Configurar GOOGLE_SHEETS_WEBHOOK_URL no .env.local
- Vercel precisa conectar repo marcoslrvusa/marcosv4-blog (atual: mlrv-hub/marcosv4-blog)
