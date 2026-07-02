# Grupo R1 — Páginas sem H1 (Crawl Real)

Fonte: Crawl via script (2026-06-29) — confirmação de páginas sem `<h1>` no HTML renderizado.  
Complementa o item **A-03** da auditoria Screaming Frog: 22 páginas sem H1 de 83 indexáveis.

---

## Páginas confirmadas SEM H1 (21 encontradas via crawl)

| #   | URL                                                                                           | Título (Title Tag)                                                          |
| --- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| 1   | `/projetos/`                                                                                  | Portfólio de Eventos Realizados com Excelência \| R1 Grupo                  |
| 2   | `/projetos/audiovisual-e-cenografia/`                                                         | Audiovisual e Cenografia \| R1 Grupo                                        |
| 3   | `/projetos/cenografia/`                                                                       | Cenografia \| R1 Grupo                                                      |
| 4   | `/projetos/audiovisual-e-cenografia/apix-2025/`                                               | APIX - 2025 \| R1 Grupo                                                     |
| 5   | `/projetos/audiovisual-e-cenografia/7th-ai-experience/`                                       | 7Th AI Experience \| R1 Grupo                                               |
| 6   | `/projetos/audiovisual-e-cenografia/ilos-wtc/`                                                | Ilos - WTC \| R1 Grupo                                                      |
| 7   | `/projetos/audiovisual-cenografia-e-tecnologia-interativa/panrotas/`                          | Panrotas \| R1 Grupo                                                        |
| 8   | `/projetos/audiovisual-cenografia-e-tecnologia-interativa/mulheres-de-eventos/`               | Mulheres de Eventos \| R1 Grupo                                             |
| 9   | `/projetos/audiovisual-cenografia-e-tecnologia-interativa/lacte/`                             | Lacte \| R1 Grupo                                                           |
| 10  | `/projetos/audiovisual-cenografia-e-tecnologia-interativa/safe-experience/`                   | Safe Experience \| R1 Grupo                                                 |
| 11  | `/projetos/audiovisual-cenografia-e-tecnologia-interativa/r1-talks-bem-estar/`                | R1 Talks Bem Estar \| R1 Grupo                                              |
| 12  | `/projetos/audiovisual-cenografia-e-tecnologia-interativa/lamec-the-westin/`                  | LAMEC - The Westin \| R1 Grupo                                              |
| 13  | `/projetos/audiovisual-cenografia-e-tecnologia-interativa/r1-talks-esg-2025/`                 | R1 Talks ESG - 2025 \| R1 Grupo                                             |
| 14  | `/projetos/audiovisual-cenografia-e-tecnologia-interativa/innovation-talks/`                  | Innovation Talks \| R1 Grupo                                                |
| 15  | `/projetos/audiovisual-cenografia-e-tecnologia-interativa/safe/`                              | Safe Experience Campinas \| R1 Grupo                                        |
| 16  | `/projetos/audiovisual-cenografia-e-tecnologia-interativa/mice-meeting/`                      | Mice Meeting \| R1 Grupo                                                    |
| 17  | `/projetos/cenografia/conlicitantes/`                                                         | Conlicitantes \| R1 Grupo                                                   |
| 18  | `/portfolio/`                                                                                 | Portfolio e Cases de Eventos Corporativos realizados \| R1 Grupo            |
| 19  | `/portfolio-items-old/convencao-nestle-2022/`                                                 | *(sem title tag)*                                                           |
| 20  | `/tecnologia-para-eventos/por-que-usar-gamification-em-eventos/`                              | Por que usar gamification em eventos? \| R1 Grupo                           |
| 21  | `/equipamentos-audiovisuais/6-dicas-para-escolher-o-fornecedor-de-equipamentos-para-eventos/` | 6 dicas para escolher o fornecedor de equipamentos para eventos \| R1 Grupo |

> **Nota:** O Screaming Frog apontou 22 páginas. Este crawl encontrou 21 — a diferença de 1 pode ser uma página não-listada no sitemap ou removida desde a auditoria.

---

## Páginas com MÚLTIPLOS H1s (precisam reduzir para 1)

| # | URL | Qtd H1s | H1s Atuais |
|---|-----|---------|------------|
| 1 | `/` (homepage) | 5 | Combinamos audiovisual...; Do conceito à execução...; O maior grupo de audiovisual...; Histórias de quem produziu...; Seu evento merece o melhor... |
| 2 | `/quem-somos/` (antiga) | 3 | Quem Somos - Velha; O Grupo R1 não é apenas...; Nossa missão é clara. |
| 3 | `/quem-somos-3/` | 2 | O maior grupo de audiovisual...; Seu evento merece o melhor... |
| 4 | `/r1-talks/` | 2 | Quatro capítulos para transformação...; R1 Talks: Eventos e Palestras... |
| 5 | `/dicas/festa-junina-corporativa-como-criar-uma-experiencia-de-marca/` | 2 | *(H1 duplicado)* |
| 6 | `/esg/cop30-os-principais-destaques/` | 2 | COP30: os principais destaques...; Conclusão: a COP30 acelera... |
| 7 | `/tendencias-de-mercado/dia-do-cliente/` | 2 | *(H1 duplicado)* |

---

## O que mudou em relação à versão anterior

O arquivo antigo continha **páginas "prováveis" sem verificação real** e misturava **H1s genéricos** com ausência total de H1. Esta versão é baseada em **crawl real** (requisição HTTP + parsing de HTML) de todas as URLs do sitemap.

- `/trabalhe-conosco/` → **tem H1** ("Trabalhe conosco eventos") — não está mais na lista
- `/projetos/audiovisual-cenografia-e-tecnologia-interativa/` → **tem H1** — não está mais na lista
- `/projetos/tecnologia-interativa-e-cenografia/` → **tem H1** ("Tecnologia Interativa e Cenografia") — não está mais na lista
- `/contato/` → **tem H1** ("Fale com o Grupo R1...") — não está mais na lista

---

## Como implementar

Cada página precisa de **1 H1 único**. No Elementor:

1. **Páginas sem H1** → adicionar widget Heading com tag `<h1>`
2. **Páginas com H1 genérico** → editar o heading existente para a versão recomendada
3. **Homepage** → reduzir de 5 H1s para 1 (vide `h2-para-arrumar-homepage.md`)

Prioridade: páginas com maior volume potencial (`/projetos/`, páginas de categoria de projeto) primeiro.
