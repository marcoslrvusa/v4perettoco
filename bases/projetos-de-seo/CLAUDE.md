# Projetos de SEO

## Resumo
Central de auditorias técnicas SEO realizadas pela equipe de SEO da V4 Company. Contém relatórios completos de diagnóstico, planos de ação trimestrais e dados de crawl (Screaming Frog) para clientes atendidos pelo SEO Squad.

## Contexto
- **Objetivo:** Armazenar e organizar entregas de auditoria SEO para clientes da V4
- **Pessoas envolvidas:** SEO Squad V4 Company (seo-visibilidade, analista-dados, estrategista-marketing)
- **Status atual:** 2 auditorias concluídas em Q2 2026 (Grupo R1 e Metal Indianápolis)

## Dados
- **Ferramenta principal:** Screaming Frog SEO Spider v20.x
- **Métricas principais:** Saúde geral SEO, problemas por severidade, horas de correção, projeção de tráfego

## Processos
- **Workflows identificados:** Auditoria técnica via crawl Screaming Frog → Análise e classificação → Plano de ação trimestral → Revisão SEO Squad
- **Ferramentas usadas:** Screaming Frog, SEO Analyzer, CSVs de dados

## Situação Atual

### Problemas
- Pasta `dados/` com CSVs brutos de crawl não existe localmente (mencionada nos relatórios mas não criada)

### Oportunidades
- 2 clientes auditados com planos de ação detalhados prontos para execução
- Base de conhecimento SEO reutilizável para novos clientes

### Decisões tomadas
- Padrão de qualidade BuiltVisible / Moz / Searchmetrics
- Auditorias classificadas por severidade (Crítico, Alto, Médio, Baixo, Info)
- Planos trimestrais com horas estimadas por especialidade

### Pendências
- Executar planos de ação: Grupo R1 (185,5h) e Metal Indianápolis (136,5h + 20h Fase 0)
- Criar pasta `dados/` com CSVs de crawl

## Clientes auditados

### GRUPO R1 (r1grupo.com.br)
- **Segmento:** Produção de eventos (audiovisual, cenografia, tecnologia)
- **Saúde SEO:** 3.8/10
- **Problemas:** 22 (3 Críticos, 7 Alto)
- **Esforço:** 185,5h em 3 meses
- **Projeção:** +35% a +55% tráfego em 90 dias
- **Principais achados:** Canonical mismatch no blog, zero structured data, 4 broken links

### Metal Indianápolis (preview.indianapolis.com.br)
- **Segmento:** Metalurgia — Fundição de Ferro Fundido
- **Saúde SEO:** 3.5/10
- **Problemas:** 25 (7 Críticos, 6 Alto)
- **Esforço:** 136,5h + 20h Fase 0
- **Projeção:** +30% a +50% tráfego em 90 dias
- **Principais achados:** Zero structured data, H2 poluído (telefone/email), Googlebot bloqueado, DNS typos

## Notas Importantes
- Entry point: não criado ainda — sugestão: `projetos-de-seo.md`
- Relatórios completos em `docs/` (formato .md e .html)
- CSVs de dados de crawl estão na subpasta `docs/Metal Indianapolis/` (31 arquivos)
- A auditoria do Grupo R1 também tem uma versão HTML interativa em `docs/auditoria-seo-r1grupo-Q2-2026.html`
