'# AI Visibility — Manual de Operações

> Produto: Otimização para Inteligências Artificiais (AI SEO / GEO)
> Versão: 1.0 | Maio 2026
> Unidade: Peretto & Co. / V4 Company

---

## Índice

1. [Visão Geral do Produto](#1-visão-geral-do-produto)
2. [Estrutura Comercial e Precificação](#2-estrutura-comercial-e-precificação)
3. [Framework de Métricas](#3-framework-de-métricas)
4. [Jornada do Cliente: End-to-End](#4-jornada-do-cliente-end-to-end)
5. [Playbook Operacional](#5-playbook-operacional)
6. [NRR — Net Revenue Retention](#6-nrr--net-revenue-retention)
7. [Tecnologia e Infraestrutura](#7-tecnologia-e-infraestrutura)
8. [Estrutura de Time](#8-estrutura-de-time)
9. [Anexos](#9-anexos)

---

## 1. Visão Geral do Produto

### 1.1 O que é

**AI Visibility** é um serviço de **Otimização para Motores de Inteligência Artificial** (AI SEO / GEO — Generative Engine Optimization). O objetivo é fazer com que a marca e o conteúdo do cliente sejam **descobertos, extraídos e citados como fonte** por sistemas de IA como ChatGPT, Perplexity, Google AI Overviews, Gemini, Claude e Copilot.

Diferente do SEO tradicional (que busca ranquear na página 1 do Google), o AI SEO busca ser **citado como referência** dentro das respostas geradas por IA — um posicionamento que gera autoridade, tráfego e conversão sem depender de clicks tradicionais.

### 1.2 Proposta de Valor

```
Para CMOs e VPs de Marketing que estão vendo o tráfego orgânico tradicional cair
e percebem que sua marca está invisível nas novas interfaces de busca por IA,
o AI Visibility é um serviço de otimização contínua que
faz sua marca ser citada como fonte confiável por ChatGPT, Perplexity e Google AI Overviews.
Diferente de agências de SEO tradicionais que ainda ignoram este canal,
nós combinamos tecnologia proprietária (agentes de IA + SEMRush) com
um framework baseado em pesquisa acadêmica (Princeton KDD 2024)
para entregar resultados mensuráveis em 30-60 dias.
```

### 1.3 Mercado-Alvo

| Segmento | Fit | Ticket | Ciclo de Venda |
|---|---|---|---|
| SaaS B2B (US$ 5-50M ARR) | ⭐⭐⭐⭐⭐ | R$ 8-15k/mês | 2-4 semanas |
| E-commerce médio/grande | ⭐⭐⭐⭐ | R$ 6-12k/mês | 3-6 semanas |
| Empresas de serviços digitais | ⭐⭐⭐⭐ | R$ 5-10k/mês | 2-4 semanas |
| Franquias/multi-localidade | ⭐⭐⭐ | R$ 10-20k/mês | 4-8 semanas |
| Institucional (indústria/financeiro) | ⭐⭐⭐ | R$ 8-15k/mês | 6-12 semanas |

**Critérios de qualificação (BANT adaptado):**
- **B**udget: Dispõe de R$ 5k+/mês para presença digital além de SEO tradicional
- **A**uthority: Domínio com DR 30+ ou conteúdo estabelecido
- **N**eed: Já percebeu queda em tráfego orgânico ou quer estar à frente
- **T**imeline: Quer resultados em 30-60 dias

### 1.4 Diferenciais V4

| Diferencial | O que significa |
|---|---|
| **Agentes de IA na entrega** | 12 agentes especializados (analista, revisor, geradores, flags) que aceleram cada etapa |
| **SEMRush Enterprise** | Dados reais de AI Overview tracking, keyword research, content gap analysis |
| **Framework acadêmico** | Metodologia baseada no Princeton GEO Study (KDD 2024) — não é chute |
| **Monitoramento contínuo** | Relatórios mensais com métricas de citação em IA, share of voice e tendências |
| **Infraestrutura própria** | n8n workflows + Python scripts para automação do monitoring |
| **Cobertura multi-plataforma** | ChatGPT, Perplexity, Google AI Overviews, Gemini, Claude, Copilot |

---

## 2. Estrutura Comercial e Precificação

### 2.1 Tiers de Serviço

```
                    ┌─────────────────────────────────────────────────┐
                    │           DIAGNÓSTICO (One-time)                │
                    │  Diagnóstico de visibilidade em IA              │
                    │  Preço: R$ 4.900                               │
                    │  Prazo: 5-7 dias                               │
                    └──────────────────────┬──────────────────────────┘
                                           │ upgrade
                                           ▼
                    ┌─────────────────────────────────────────────────┐
                    │        IMPLANTAÇÃO (Projeto 45-60d)             │
                    │  Diagnóstico + otimização completa              │
                    │  Preço: R$ 14.900                               │
                    │  Prazo: 45-60 dias (split em 3 sprints)         │
                    └──────────────────────┬──────────────────────────┘
                                           │ upgrade
                                           ▼
                    ┌─────────────────────────────────────────────────┐
                    │      GESTÃO CONTÍNUA (Mensal recorrente)        │
                    │  Monitoramento + otimização + reporting         │
                    │  Preço: R$ 7.900/mês                            │
                    │  Contrato: 12 meses (mínimo 6)                  │
                    └─────────────────────────────────────────────────┘
```

### 2.2 Detalhamento por Tier

#### Tier 1: Diagnóstico de Visibilidade em IA — R$ 4.900

| O que entrega | Descrição |
|---|---|
| **Auditoria de 20 queries** | Testa as 20 queries mais importantes do cliente em ChatGPT, Perplexity e Google AI Overviews |
| **Mapeamento de concorrentes** | Quem está sendo citado no lugar do cliente? Qual o share of voice atual? |
| **Auditoria técnica AI SEO** | robots.txt (bloqueia bots?), schema markup, extractability score, freshness signals |
| **Análise de conteúdo** | As páginas atuais são extraíveis por IA? (definition blocks, FAQ, tables, statistics) |
| **Relatório executivo** | PDF com priorização: "aqui está onde você está, aqui está onde precisa estar" |
| **Apresentação de resultados** | Deck para apresentação ao C-level (15min de duração) |

**Objetivo do diagnóstico:** Ser uma amostra de valor tão forte que o cliente queira automaticamente a implantação.

#### Tier 2: Implantação AI SEO — R$ 14.900

| Sprint | Duração | O que entrega |
|---|---|---|
| **Sprint 1: Foundation** | Dias 1-15 | robots.txt liberação, schema markup, llms.txt, pricing.md, correções técnicas |
| **Sprint 2: Content** | Dias 16-35 | Otimização de 10 páginas críticas (definition blocks, FAQ sections, comparison tables, statistic blocks) |
| **Sprint 3: Presence** | Dias 36-50 | Estratégia de terceiros (Wikipedia, Reddit, G2, YouTube, Quora), validação + relatório final |
| **Handoff** | Dias 51-60 | Treinamento do time do cliente, entrega de documentação, transição para gestão contínua |

#### Tier 3: Gestão Contínua de Presença em IA — R$ 7.900/mês

| Entregável | Frequência |
|---|---|
| Monitoramento de citações em IA (ChatGPT + Perplexity + AI Overviews) | Mensal |
| Relatório de métricas (citation count, share of voice, sentiment, traffic) | Mensal |
| Otimização de conteúdo (5 páginas/mês) | Mensal |
| Atualização de schema markup (se necessário) | Mensal |
| Benchmark competitivo trimestral | Trimestral |
| QBR (Quarterly Business Review) com recomendações estratégicas | Trimestral |
| Disponibilidade para emergências (ex: Google atualizou critérios de AI Overview) | Contínua |

### 2.3 Add-ons e Upsells

| Add-on | Preço | Descrição |
|---|---|---|
| **Domínio adicional** | +R$ 2.900/mês | Monitoramento e otimização de um domínio extra do mesmo cliente |
| **Pacote de conteúdo** | +R$ 3.900/mês | +10 páginas/mês de otimização |
| **Competitor Intelligence** | +R$ 1.900/mês | Monitoramento aprofundado de 5 concorrentes específicos |
| **Content Production** | +R$ 2.900/mês | Criação de conteúdo novo otimizado para IA (4 posts/mês) |
| **Technical Deep Dive** | +R$ 4.900 (one-time) | Auditoria técnica completa + implementação de schema avançado |
| **Agente de IA personalizado** | Sob consulta | Treinar um agente customizado no conteúdo do cliente |

### 2.4 Modelo de Contrato

**Gestão Contínua:**
- Mínimo: 6 meses
- Ideal: 12 meses
- Faturamento: Mensal, com reajuste anual pelo IPCA + 5%
- Garantia: Se após 3 meses não houver nenhuma citação em IA, o cliente pode cancelar sem multa

**Cláusulas-chave:**
- Escopo mensal definido em SOW (Statement of Work) anexo
- Revisão trimestral de escopo e pricing
- Confidencialidade dos relatórios e dados
- Propriedade intelectual do conteúdo otimizado pertence ao cliente
- Metodologia e templates V4 são proprietários

---

## 3. Framework de Métricas

### 3.1 Hierarquia de Métricas

```
                    ┌──────────────────────────────────────┐
                    │       BUSINESS IMPACT (LAGGING)       │
                    │  ↑ Tráfego via IA ↑ Leads via IA      │
                    │  ↑ Receita atribuída a citações       │
                    └──────────────────┬───────────────────┘
                                       │
                    ┌──────────────────▼───────────────────┐
                    │     AI VISIBILITY (OUTCOME METRICS)   │
                    │  Citation Count · Share of AI Voice   │
                    │  Query Coverage · Citation Sentiment  │
                    └──────────────────┬───────────────────┘
                                       │
                    ┌──────────────────▼───────────────────┐
                    │     IMPLEMENTAÇÃO (LEADING METRICS)   │
                    │  Extractability Score · Schema Score  │
                    │  Bot Accessibility · Freshness Index  │
                    │  Content Optimization %               │
                    └──────────────────────────────────────┘
```

### 3.2 Métricas Emergentes (AI-Specific)

Estas métricas são novas no mercado. Nós as definimos e padronizamos para garantir clareza para o cliente.

#### Métricas de Outcome (Resultado)

| Métrica | Definição | Como Medir | Benchmark Inicial | Meta |
|---|---|---|---|---|
| **AI Citation Count** | Número de vezes que a marca/domínio é citado como fonte em respostas de IA | Checagem manual das 20 queries + SEMRush AI Overview (quando disponível) | 0 → alvo: 5+ citações no mês 3 | 15+ citações no mês 6 |
| **Share of AI Voice (SAIV)** | % de citações do cliente ÷ total de citações (cliente + top 5 concorrentes) nas queries-alvo | Planilha padronizada (anexo 9.5) | 0% → alvo: 15% no mês 3 | 30%+ no mês 6 |
| **Query Coverage Rate** | % das queries-alvo onde o cliente aparece em pelo menos uma resposta de IA | Checagem cruzada das 20 queries | 0% → alvo: 40% no mês 3 | 70%+ no mês 6 |
| **Citation Sentiment Score** | Tom da citação: +1 positiva (recomendação), 0 neutra (menção), -1 negativa (crítica) | Revisão humana de cada citação | N/A → alvo: 80%+ positivas | 90%+ positivas |
| **AI Referral Traffic** | Visitas ao site vindas de chat.openai.com, perplexity.ai, copilot.microsoft.com | GA4 (source/medium report) | 0 → alvo: 5% do tráfego orgânico | 10%+ do tráfego orgânico |

#### Métricas de Implementação (Leading Indicators)

| Métrica | Definição | Medição | Frequência |
|---|---|---|---|
| **Extractability Score** | % das páginas críticas com structure blocks adequados (definition, FAQ, comparison, statistic) | Checklist interno por página | Mensal (Sprint) |
| **Schema Coverage** | % das páginas críticas com schema markup correto (FAQPage, HowTo, Article, Product) | SEMRush Site Audit + manual | Mensal |
| **Bot Accessibility** | AI crawlers (GPTBot, PerplexityBot, ClaudeBot, Google-Extended) liberados no robots.txt | Checagem manual | Semanal (mês 1), depois mensal |
| **Freshness Index** | % de páginas atualizadas nos últimos 6 meses (com "last updated" visível) | SEMRush + varredura manual | Mensal |
| **Citable Content Rate** | % do conteúdo existente que contém dados originais, estatísticas ou citações externas | Auditoria de conteúdo | Mensal (proporcional) |

### 3.3 Dashboard de Resultados (para o cliente)

Relatório mensal em 1 página:

```
─────────────────────────────────────────────────────────────
AI VISIBILITY REPORT — [CLIENTE] — [MÊS/ANO]
─────────────────────────────────────────────────────────────

CITAÇÕES EM IA
  ┌────────────────────────────────────┬────────┬──────────┐
  │ Plataforma                         │ Mês    │ vs Mês   │
  │                                    │ atual  │ anterior │
  ├────────────────────────────────────┼────────┼──────────┤
  │ Google AI Overviews                │  8     │  +3 ▲    │
  │ ChatGPT                            │  5     │  +2 ▲    │
  │ Perplexity                         │  3     │  +1 ▲    │
  │ Gemini                             │  2     │   0      │
  │ Claude/Copilot                     │  1     │  +1 ▲    │
  ├────────────────────────────────────┼────────┼──────────┤
  │ TOTAL                              │ 19     │  +7 ▲    │
  └────────────────────────────────────┴────────┴──────────┘

SHARE OF AI VOICE (vs top 5 concorrentes)
  ┌───────────────────────────────────────────────────┐
  │ Cliente:       ████████████████░░ 32% (+8% vs mês)│
  │ Concorrente A: ██████████████░░░░ 28%              │
  │ Concorrente B: ██████████░░░░░░░░ 18%              │
  │ Concorrente C: ███████░░░░░░░░░░░ 14%              │
  │ Concorrente D: ████░░░░░░░░░░░░░░  8%              │
  └───────────────────────────────────────────────────┘

QUERY COVERAGE: 55% (+12% vs mês anterior)
  ├─ Cobertas: 11 das 20 queries-alvo
  ├─ Novas no mês: "best [category] software", "how to [problem]"
  └─ Em desenvolvimento: 4 queries com progresso parcial

AI REFERRAL TRAFFIC: 1.247 visitas (+34% vs mês anterior)
  ├─ ChatGPT: 612 (49%)
  ├─ Perplexity: 348 (28%)
  ├─ Google AI Overviews: 204 (16%)
  └─ Outros: 83 (7%)

PRÓXIMAS AÇÕES (próximos 30 dias)
  1. Otimizar 5 páginas com baixo extractability score
  2. Criar comparison table para query "[cliente] vs [concorrente]"
  3. Atualizar 3 páginas com dados de 2026
  4. Adicionar FAQ schema na página de pricing
```

### 3.4 SEMRush na Operação

| Funcionalidade SEMRush               | Como usamos no AI Visibility                                                    | Frequência           |
| ------------------------------------ | ------------------------------------------------------------------------------- | -------------------- |
| **AI Overviews (Position Tracking)** | Monitoramento de quais queries têm AI Overviews e quem é citado                 | Diário (automático)  |
| **Domain Analytics**                 | Comparação share of voice entre cliente e concorrentes                          | Semanal              |
| **Content Analyzer**                 | Gap analysis: o que o concorrente tem que o cliente não tem                     | Mensal               |
| **Keyword Magic Tool**               | Expansão do universo de queries-alvo (incluindo variações de linguagem natural) | Mensal               |
| **Site Audit**                       | Schema markup check, page structure analysis, technical issues                  | Semanal (automático) |
| **Topic Research**                   | Identificação de tópicos emergentes no setor do cliente                         | Mensal               |
| **Brand Monitoring**                 | Menções à marca em fontes externas                                              | Contínuo             |
| **Backlink Analytics**               | Correlação entre backlinks de qualidade e citações em IA                        | Mensal               |

**Nota operacional:** O SEMRush Position Tracking já inclui dados de AI Overviews. Usamos o conector de API do SEMRush (disponível nas automações V4) para puxar esses dados automaticamente para o dashboard.

---

## 4. Jornada do Cliente: End-to-End

### 4.1 Mapa da Jornada

```
PRÉ-VENDA ────────────────────────────────────────────────────
  Lead qualificado → Proposta → Fechamento
  (dias 1-14)

ONBOARDING ───────────────────────────────────────────────────
  Kickoff → Auditoria → Diagnóstico → Apresentação
  (dias 1-7)

FASE 1: FOUNDATION ──────────────────────────────────────────
  Técnico (robots.txt, schema, llms.txt, pricing.md)
  (dias 8-22)

FASE 2: CONTENT ─────────────────────────────────────────────
  Otimização de 10 páginas → Validação
  (dias 23-42)

FASE 3: PRESENCE ────────────────────────────────────────────
  Terceiros (Wikipedia, Reddit, G2, etc) → Validação final
  (dias 43-55)

HANDOFF ─────────────────────────────────────────────────────
  Treinamento → Documentação → Transição para gestão contínua
  (dias 56-60)

GESTÃO CONTÍNUA ─────────────────────────────────────────────
  Mês a mês: monitorar → relatar → otimizar → expandir
  (mês 3+)

QBR (trimestral) ────────────────────────────────────────────
  Revisão de resultados → Ajuste de estratégia → Upsell

RENOVAÇÃO ───────────────────────────────────────────────────
  Análise NRR → Expansão → Renovação anual
```

### 4.2 Fase 0: Pré-Venda

#### Lead Scoring para AI Visibility

| Sinal | Pontos | Como detectar |
|---|---|---|
| Cliente menciona "tráfego orgânico caindo" | +30 | Call de discovery |
| Cliente pergunta "como aparecer no ChatGPT" | +40 | Call ou e-mail |
| Cliente tem domínio com DR 30+ | +20 | SEMRush |
| Cliente tem concorrentes sendo citados em IA | +25 | Pesquisa rápida |
| Cliente já investe em SEO tradicional | +15 | Discovery |
| Cliente é SaaS ou e-commerce | +20 | Obviamente |
| Cliente tem conteúdo (blog, docs, comparisons) | +15 | Site check |
| Cliente tem orçamento para inovação digital | +10 | Discovery call |

**Score mínimo para proposta: 50 pontos.**

#### Proposta Comercial

A proposta deve conter:

1. **Diagnóstico gratuito de 3 queries** (amostra do que o serviço faz)
   - "Pesquisei sua marca em ChatGPT/Perplexity para 3 queries do seu negócio. Aqui está o que vi..."
   - Mostra o gap: onde o cliente está vs onde deveria estar

2. **Estrutura do serviço** (tiers, prazos, entregáveis)

3. **Caso de uso real** (se possível, um case anônimo de outro cliente)

4. **ROI estimado:**
   - "Se 47% das buscas no Google têm AI Overviews e você não aparece em nenhuma..."
   - "Seu concorrente X está sendo citado em 12 respostas de IA por mês — cada citação é um contato com um comprador no topo do funil"

5. **Preço** com 3 opções:
   - Recomendado: Diagnóstico + Implantação + Gestão (R$ 4.900 + R$ 14.900 + R$ 7.900/mês)
   - Alternativo A: Só Gestão (já entra com implantação inclusa no primeiro mês)
   - Alternativo B: Só Diagnóstico (para quem quer testar)

### 4.3 Fase 1: Onboarding (Dias 1-7)

#### Kickoff

| Atividade | Quem | Duração | Entregável |
|---|---|---|---|
| Kickoff meeting | Account + Cliente | 60min | Ata de kickoff alinhada |
| Coleta de queries-alvo | Cliente (formulário) | Na call | Top 20 queries |
| Acesso ao SEMRush | Cliente (ou via V4) | 1 dia | Conta conectada |
| Acesso ao GA4 | Cliente | 1 dia | View configurada |
| Acesso ao robots.txt / site | Cliente | Imediato | Credenciais |

#### Formulário de Queries-Alvo

Coletar do cliente no kickoff:

```
Query Type                          Exemplos (preencher 5 cada)
────────────────────────────────────────────────────────────────────
"What is [category]?"               1.
                                    2.

"Best [category] for [use case]"    1.
                                    2.

"[Brand] vs [competitor]"           1.
                                    2.

"How to [problem they solve]"       1.
                                    2.

"[Category] pricing"                1.
                                    2.

[Dúvidas comuns do cliente]         1.
                                    2.
```

#### Auditoria Técnica Completa

Realizada pelo @analista-dados + SEMRush:

```json
{
  "robots_txt": {
    "gptbot_allowed": true/false,
    "perplexitybot_allowed": true/false,
    "claudebot_allowed": true/false,
    "google_extended_allowed": true/false
  },
  "schema_markup": {
    "organization": true/false,
    "article": true/false,
    "faq": true/false,
    "howto": true/false,
    "product": true/false,
    "review": true/false
  },
  "content_audit": {
    "total_pages": 0,
    "pages_with_definitions": 0,
    "pages_with_faq": 0,
    "pages_with_comparison_tables": 0,
    "pages_with_statistics": 0,
    "pages_with_last_updated": 0,
    "pages_with_author_attribution": 0
  },
  "freshness": {
    "pages_updated_6_months": 0,
    "pages_updated_12_months": 0,
    "pages_never_updated": 0
  },
  "third_party": {
    "wikipedia": "exists/not_exists",
    "reddit_mentions": 0,
    "g2_capterra": "exists/not_exists",
    "youtube_channel": "exists/not_exists"
  }
}
```

#### Entrega do Diagnóstico (Dia 7)

Relatório PDF gerado pelo @gerar-pdf com:

- Status atual: onde o cliente está hoje (provavelmente zero citações)
- Benchmark: onde os concorrentes estão
- Gap analysis: o que precisa mudar
- Roadmap: sprints 1-3 com prazos
- Recomendação: "comece pela implantação"

### 4.4 Fase 2: Implantação — Sprint 1: Foundation (Dias 8-22)

**Objetivo:** Remover todas as barreiras técnicas para que os AI crawlers possam ler, entender e citar o conteúdo.

#### Checklist Foundation

| # | Tarefa | Responsável | Prazo | Status |
|---|---|---|---|---|
| 1 | Auditar robots.txt e liberar AI crawlers | GT/Técnico | Dia 8 | ☐ |
| 2 | Implementar Organization schema | GT/Técnico | Dia 10 | ☐ |
| 3 | Implementar Article/BlogPosting schema | GT/Técnico | Dia 12 | ☐ |
| 4 | Implementar FAQPage schema (páginas FAQ) | GT/Técnico | Dia 14 | ☐ |
| 5 | Implementar HowTo schema (se aplicável) | GT/Técnico | Dia 14 | ☐ |
| 6 | Implementar Product schema (se aplicável) | GT/Técnico | Dia 14 | ☐ |
| 7 | Criar /pricing.md (pricing legível por agentes de IA) | Copy + GT | Dia 16 | ☐ |
| 8 | Criar /llms.txt (contexto para IAs) | Copy | Dia 16 | ☐ |
| 9 | Adicionar "last updated" visível em todas as páginas | GT/Técnico | Dia 18 | ☐ |
| 10 | Adicionar author attribution com credentials | Copy + GT | Dia 20 | ☐ |
| 11 | Validar tudo com SEMRush Site Audit | Revisor (@revisor) | Dia 22 | ☐ |

#### Entregáveis da Sprint 1

- `robots.txt` otimizado
- Schema markup implementado nas páginas identificadas
- `pricing.md` no root do domínio
- `llms.txt` no root do domínio
- Relatório de validação técnica

### 4.5 Fase 2: Implantação — Sprint 2: Content (Dias 23-42)

**Objetivo:** Tornar o conteúdo extraível e citável por IA.

#### Priorização de Páginas

Selecionar 10 páginas com base em:
1. Relevância para as queries-alvo
2. Potencial de citação (conteúdo que pode ser "definition block", "comparison", etc)
3. Tráfego orgânico atual (dados SEMRush)
4. Gap competitivo (concorrente tem, cliente não tem)

#### Content Blocks por Tipo de Query

Para cada página, aplicar o bloco correto:

| Query Pattern | Bloco | Exemplo de Implementação |
|---|---|---|
| "What is X?" | **Definition Block** | Primeiro parágrafo: definição clara de 40-60 palavras. "X é um [categoria] que [funcionalidade principal], diferente de [alternativa] porque [diferencial]." |
| "How to X?" | **Step-by-Step Block** | Lista numerada com 4-7 passos. Cada passo: verbo + resultado esperado. + HowTo schema. |
| "X vs Y" | **Comparison Table** | Tabela com 5-8 critérios lado a lado. Linhas: preço, features, suporte, integrações, etc. |
| "Best X for Y" | **Pros/Cons + Use Case** | Para cada opção: 3 pros + 3 cons + "best for [specific use case]". |
| "X pricing" | **Pricing Block** | Tabela de tiers com: preço, limites, features. + Product schema. |
| "X review" | **Review Block** | Nota geral + breakdown por critério + AggregateRating schema. |
| Questions comuns | **FAQ Block** | 5-8 perguntas reais (do suporte, vendas, reviews) + FAQPage schema. |

#### Regras de Ouro para Content Optimization

1. **Lead com a resposta** — primeira frase de cada seção já responde a pergunta
2. **Blocos autossuficientes** — cada section funciona standalone (IA pode extrair só aquele trecho)
3. **40-60 palavras** para trechos-chave (tamanho ideal de snippet extraction)
4. **Dados originais com fonte** — toda estatística tem link para a fonte original
5. **Datas em tudo** — "Last updated: [data]" em toda página otimizada
6. **Autor com credencial** — nome, cargo, link para LinkedIn/bio
7. **Tom autoritativo** — "De acordo com [fonte]" em vez de afirmações sem apoio
8. **Sem keyword stuffing** — a skill do Princeton GEO mostra que keyword stuffing reduz visibilidade em IA em -10%

#### Entregáveis da Sprint 2

- 10 páginas otimizadas com blocks adequados
- Relatório de validação com extractability score (target: 80%+)

### 4.6 Fase 2: Implantação — Sprint 3: Presence (Dias 43-55)

**Objetivo:** Estabelecer presença do cliente nos locais onde as IAs buscam fontes.

#### Third-Party Presence Strategy

| Canal | Ação | Prioridade |
|---|---|---|
| **Wikipedia** | Verificar se página existe. Se existir: atualizar com dados precisos. Se não: avaliar viabilidade (notoriedade exigida). | Alta |
| **Reddit** | Participação autêntica em subreddits do setor (sem spam). Respostas com profundidade técnica. | Alta |
| **G2 / Capterra / TrustRadius** | Perfil atualizado com reviews reais. Responder reviews negativos. | Alta |
| **YouTube** | Criar/vincular conteúdo para "how to" queries (Google AI Overviews cita YouTube frequentemente). | Média |
| **Quora** | Responder perguntas do nicho com profundidade. | Média |
| **Industry publications** | Guest posts em veículos relevantes do setor. | Média |
| **LinkedIn Articles** | Publicação de thought leadership do time do cliente. | Baixa |

#### Princípios de Third-Pressure Presence

1. **Autenticidade > Quantidade** — Uma resposta de qualidade no Reddit vale mais que 10 posts genéricos
2. **Links de volta** — Sempre que possível, referenciar o conteúdo do cliente como fonte
3. **Consistência** — Presença contínua, não campanha única
4. **Monitoramento** — Rastrear menções e citações resultantes (SEMRush Brand Monitoring)

#### Entregáveis da Sprint 3

- Perfis verificados e atualizados nas plataformas-alvo
- Calendário de presença em terceiros (próximos 3 meses)
- Relatório de citações capturadas pós-implementação

### 4.7 Handoff para Gestão Contínua (Dias 56-60)

| Atividade | Duração | Entregável |
|---|---|---|
| Treinamento do time do cliente | 60min | Time capacitado a manter conteúdo otimizado |
| Entrega de documentação | — | Manual de boas práticas AI SEO (customizado) |
| Transição de métricas | — | Dashboard configurado + baseline estabelecido |
| Alinhamento de expectativas | 30min | O que muda: de projeto para gestão contínua |
| Definição de comunicação | — | Canais: e-mail mensal, call trimestral, emergência WhatsApp |

### 4.8 Fase 3: Gestão Contínua (Mês 3+)

#### Ciclo Mensal

```
Semana 1: MONITORAR
  → Puxar dados de citações (manual + SEMRush)
  → Verificar novas queries com AI Overviews
  → Rodar SEMRush Site Audit
  → Alimentar dashboard

Semana 2: RELATAR
  → @analista-dados gera análise do mês
  → @revisor valida
  → @gerar-html gera dashboard interativo
  → Enviar relatório ao cliente (+ call de 15min se necessário)

Semana 3: OTIMIZAR
  → 5 páginas do mês (selecionadas por prioridade)
  → Aplicar content blocks onde faltam
  → Atualizar dados e freshness

Semana 4: EXPANDIR
  → Nova query discovery (SEMRush)
  → Ajustes em third-party presence
  → Preparar recomendações para o próximo mês
```

#### Ciclo Trimestral (QBR)

```
Pré-QBR (1 semana antes):
  → @analista-dados puxa dados do trimestre completo
  → Comparativo mês a mês + vs trimestre anterior
  → Atualização do benchmark competitivo
  → Draft do deck de QBR

QBR Call (60min):
  → Resultados do trimestre (métricas vs baseline)
  → Novas queries descobertas + cobertura
  → Novos concorrentes entrando no radar
  → Recomendações estratégicas
  → Oportunidades de expansão (add-ons, upsells)

Pós-QBR:
  → @gerar-ppt gera deck final
  → SOW atualizado (se houver mudança de escopo)
  → Próximos passos registrados
```

### 4.9 Fase 4: Renovação e Expansão

#### Gatilhos de Expansão (Upsell)

| Sinal | Ação | Add-on Sugerido |
|---|---|---|
| Cliente atingiu 70%+ de query coverage | Expandir para mais 20 queries | Pacote de conteúdo + |
| Marca do cliente foi citada 15+ vezes/mês por 3 meses consecutivos | Introduzir competitive intelligence | Competitor Intelligence |
| Cliente tem 2+ marcas/domínios | Expandir para o segundo domínio | Domínio adicional |
| NRR estável há 6+ meses | Propor programa de conteúdo novo | Content Production |
| QBR mostra gap técnico identificado | Oferecer Technical Deep Dive | Technical Deep Dive |

#### Gatilhos de Risco (Retenção)

| Sinal | Risco | Ação Imediata |
|---|---|---|
| Citation count cai 2 meses consecutivos | 🟡 Médio | Auditoria de mudanças (Google update? Concorrente novo?) + Plano de recuperação |
| Share of AI Voice cai abaixo do baseline | 🟡 Médio | Revisão de concorrentes + conteúdo urgente |
| Query coverage estagna por 3 meses | 🔴 Alto | Reunião de alinhamento + replanejamento de estratégia |
| Cliente não responde relatórios por 2 meses | 🔴 Alto | Escalar para CSM + call de alinhamento |
| Google anuncia mudança em AI Overviews | 🟢 Oportunidade | Análise de impacto + comunicação proativa ao cliente |

---

## 5. Playbook Operacional

### 5.1 Primeiros 30 Dias (Novo Cliente)

| Dia | Atividade | Ferramenta | Responsável |
|---|---|---|---|
| **Dia 0** | Kickoff + formulário de queries | Call + Google Forms | Account |
| **Dia 1** | Setup SEMRush + GA4 + robots.txt check | SEMRush | GT |
| **Dia 2** | Auditoria técnica completa | @analista-dados + SEMRush | GT + Revisor |
| **Dia 3** | Teste de 20 queries em 3 plataformas | ChatGPT + Perplexity + Google | Account |
| **Dia 4** | Mapeamento de concorrentes + benchmark | SEMRush | Analista |
| **Dia 5** | Montagem do relatório de diagnóstico | @gerar-pdf | Analista |
| **Dia 6** | Revisão do relatório | @revisor | Revisor |
| **Dia 7** | Apresentação do diagnóstico + proposta de implantação | Call + Deck | Account |
| **Dia 8-10** | robots.txt + schema markup inicial | GT | GT |
| **Dia 11-16** | /pricing.md + /llms.txt + "last updated" | Copy + GT | Copy |
| **Dia 17-22** | Validação técnica final | @revisor + SEMRush | Revisor |
| **Dia 23-35** | Content optimization (10 páginas) | Copy | Copy |
| **Dia 36-42** | Validação de conteúdo + ajustes | @revisor | Revisor |
| **Dia 43-50** | Third-party presence strategy | Account | Account |
| **Dia 51-55** | Validação final + relatório de conclusão | @gerar-pdf | Analista |
| **Dia 56-60** | Handoff + treinamento + transição | Account | Account |

### 5.2 Runbook de Operação Mensal (Gestão Contínua)

Usar este checkrun toda semana:

```bash
# Semana 1: Monitoramento
1. Abrir SEMRush Position Tracking → verificar AI Overviews novas
2. @analista-dados "puxa citações em IA do cliente X este mês" → salva resultado
3. Verificar GA4 → tráfego de referência AI sources
4. Registrar manualmente citações em ChatGPT + Perplexity (20 queries)
5. Alimentar planilha de métricas do cliente

# Semana 2: Relatório
6. @analista-dados "gera análise mensal de AI Visibility do cliente X"
7. @revisor "valida análise mensal do cliente X"
8. @gerar-html "dashboard de AI Visibility do cliente X — mês [mês]"
9. Enviar para o cliente + agendar call de 15min

# Semana 3: Otimização
10. Selecionar 5 páginas para otimizar (prioridade: baixo extractability + alta relevância)
11. Aplicar content blocks (definition, FAQ, comparison, stats)
12. Atualizar datas e freshness
13. @revisor "valida otimização das 5 páginas do cliente X"

# Semana 4: Expansão
14. SEMRush Topic Research → novas queries do setor
15. SEMRush Content Gap → o que concorrentes publicaram
16. Atualizar third-party presence (Reddit, Quora, etc)
17. Preparar recomendações do próximo mês
```

### 5.3 Runbook de Emergência

| Gatilho | Ação | Prazo |
|---|---|---|
| Google anuncia mudança em AI Overviews | 1. Pesquisar impacto nas 20 queries | 24h |
| | 2. Ajustar estratégia | 72h |
| | 3. Comunicar cliente proativamente | 48h |
| Citation count cai 50%+ em 1 mês | 1. Auditoria de causas (Google update? Concorrente?) | 48h |
| | 2. Plano de recuperação | 72h |
| | 3. Call com cliente | 72h |
| Concorrente novo dominando AI answers | 1. Análise do conteúdo do concorrente | 48h |
| | 2. Definição de contra-estratégia | 72h |
| | 3. Execução de conteúdo | 1 semana |
| Cliente pede resultado imediato (urgência) | 1. Verificar métricas mais recentes | 24h |
| | 2. Se estável: tranquilizar com dados | 24h |
| | 3. Se caindo: ativar plano de recuperação | 48h |

---

## 6. NRR — Net Revenue Retention

### 6.1 Modelo de NRR para AI Visibility

Diferente de SaaS, serviços têm NRR mais desafiador. Construímos o produto para que NRR > 100% seja atingível pela expansão orgânica dos clientes.

```
NRR = (MRR_fim_do_período - MRR_de_churn) / MRR_início_do_período

Onde:
- MRR considera ticket médio mensal de cada cliente
- Churn = cliente que cancelou completamente
- Expansão = upgrades de tier + add-ons + reajustes
```

### 6.2 Curva de Expansão por Cliente

```
Mês 0:  Diagnóstico (one-time)            → R$ 4.900 (não recorrente)
Mês 1:  Implantação (parcela 1/2)         → R$ 7.450
Mês 2:  Implantação (parcela 2/2)         → R$ 7.450
Mês 3+: Gestão Contínua                    → R$ 7.900/mês
Mês 6+: Gestão + Add-on (ex: domínio extra) → R$ 10.800/mês
Mês 12: Reajuste anual                     → R$ 11.340/mês (+5%)
```

**Expansão total: do diagnóstico (R$ 4.900 one-time) para gestão + add-on (R$ 10.800/mês) = cliente que começa pagando R$ 4.900 vira R$ 129.600/ano.**

### 6.3 Metas de NRR

| Indicador | Ano 1 | Ano 2 |
|---|---|---|
| **NRR alvo** | 85% (ano de construção) | 120%+ (operação madura) |
| **Churn rate mensal** | < 5% (target: 3%) | < 3% (target: 2%) |
| **Expansion rate** | 15% dos clientes com add-on no mês 6 | 40% dos clientes com add-on |
| **Taxa de conversão Diagnóstico → Implantação** | 50% | 60% |
| **Taxa de conversão Implantação → Gestão** | 70% | 80% |
| **Vida média do cliente (LTV)** | 14 meses | 24 meses |

### 6.4 Estratégias de Expansão

**Expansão Natural (produto puxa):**
- Diagnóstico (R$ 4.900) → cliente vê o gap → quer implantação (R$ 14.900)
- Implantação termina → cliente já acostumado com relatórios mensais → quer gestão (R$ 7.900/mês)
- Gestão por 6 meses → métricas subindo → cliente quer mais → add-ons

**Expansão Ativa (time empurra):**
- Call de QBR = oportunidade natural de upsell
- Relatórios mensais incluem "próximos passos" que geram necessidade
- Marcos de sucesso (ex: 70% query coverage) disparam conversa de expansão

**Expansão Técnica (sistema empurra):**
- @analista-dados detecta gap → sugere add-on automaticamente
- Dashboard mostra "você cresceu X, que tal adicionar Y?"

### 6.5 Renovação Antecipada

Oferecer desconto para renovação anual antecipada:

| Prazo de Contrato | Preço Mensal | Economia |
|---|---|---|
| Mensal (sem fidelidade) | R$ 9.900 (preço cheio) | — |
| 6 meses | R$ 7.900/mês | 20% |
| 12 meses | R$ 6.900/mês | 30% |

---

## 7. Tecnologia e Infraestrutura

### 7.1 Stack Tecnológica

| Camada | Ferramenta | Uso |
|---|---|---|
| **Monitoring** | SEMRush (Position Tracking + AI Overviews) | Dados de AI Overviews, rankings, concorrentes |
| **Monitoring** | Checagem manual (ChatGPT + Perplexity) | Validação qualitativa + citações não capturadas pelo SEMRush |
| **Analytics** | Google Analytics 4 | AI referral traffic |
| **Auditoria** | SEMRush Site Audit | Schema, technical issues, extractability |
| **Content** | SEMRush Content Analyzer + Topic Research | Gap analysis, topic discovery |
| **Relatórios** | @analista-dados + @gerar-html | Dashboard interativo |
| **Apresentações** | @gerar-ppt | Relatórios executivos, QBR |
| **Workflows** | n8n + v4-automations | Automação de monitoramento |
| **Memória** | Obsidian Vault | Histórico de cada cliente |
| **Documentação** | @gerar-doc | SOWs, atas, FCAs |

### 7.2 Agentes V4 na Entrega

| Agente | Papel no AI Visibility | Quando |
|---|---|---|
| **@analista-dados** | Auditoria inicial, análise mensal, gap analysis, competitive benchmark | Diagnóstico + mensal |
| **@revisor** | Validação de todo output antes de ir para o cliente | Contínuo |
| **@gerar-pdf** | Relatório de diagnóstico, relatórios mensais, relatório de conclusão | Diagnóstico + mensal |
| **@gerar-html** | Dashboard interativo de métricas | Mensal |
| **@gerar-ppt** | Deck de kickoff, deck de diagnóstico, deck de QBR | Diagnóstico + trimestral |
| **@gerar-doc** | SOW, atas de reunião, FCAs, documentação de handoff | Conforme necessário |
| **@csm-orquestrador** | Gestão do cliente, QBR, plano de expansão, retenção | Gestão contínua |

### 7.3 Automações (n8n + Python)

| Automação | Função | Frequência | Trigger |
|---|---|---|---|
| **ai_visibility_monitor** | Puxa AI Overviews do SEMRush API para cada cliente | Semanal | Cron (segunda 8h) |
| **citation_checker** | Roda as 20 queries em ChatGPT + Perplexity via browser automation | Mensal | Cron (dia 1 8h) |
| **content_gap_analyzer** | Compara conteúdo do cliente vs concorrentes via SEMRush | Mensal | Cron (dia 15) |
| **dashboard_generator** | Gera dashboard HTML com dados do mês | Mensal | Cron (dia 20) |
| **report_delivery** | Envia relatório por e-mail + notifica time | Mensal | Após dashboard gerado |
| **qbr_preparer** | Prepara dados para QBR trimestral | Trimestral | 7 dias antes do QBR |

### 7.4 Workflow de Monitoramento (Diagrama)

```
SEMRush API
    │
    ▼
n8n workflow (ai_visibility_monitor)
    │
    ├── Puxa AI Overviews por query
    ├── Puxa rankings dos concorrentes
    ├── Puxa Site Audit (schema, tech issues)
    │
    ▼
v4-automations/scripts/ai_seo/
    │
    ├── parse_semrush_data.py → JSON estruturado
    ├── check_ai_citations.py → busca manual assistida
    ├── generate_dashboard.py → HTML com gráficos
    │
    ▼
Obsidian Vault → /clientes/[cliente]/campanhas/ai-visibility/
    │
    ├── metricas/[mes]-[ano].json
    ├── relatorios/[mes]-[ano].md
    ├── dashboard/[mes]-[ano].html
    │
    ▼
@gerar-pdf → relatório final → cliente
```

---

## 8. Estrutura de Time

### 8.1 Papéis e Responsabilidades

| Papel | Responsabilidades | Carga por Cliente (mês) | Skills Necessárias |
|---|---|---|---|
| **Account (AI Visibility)** | Venda, kickoff, relacionamento, QBR, upsell | 8h/mês | AI SEO knowledge, consultoria, apresentação |
| **GT/Técnico** | robots.txt, schema, llms.txt, technical audit | 4h/mês (mês 1: 20h) | Schema markup, HTML, SEMRush |
| **Copy/Content** | Content optimization, content blocks, third-party content | 12h/mês (mês 2: 40h) | Copywriting, AI SEO content patterns |
| **Analista de Dados** | SEMRush analytics, métricas, dashboard, monitoring | 8h/mês | SEMRush, GA4, Excel/Google Sheets |
| **Revisor (@revisor)** | Validação de todos os outputs | 2h/mês | Atenção a detalhes, conhecimento AI SEO |
| **Coordenador** | Supervisão, qualidade, gestão de time | 2h/mês | Liderança, operação |

**Total de horas por cliente/mês (steady state): ~34h/mês**

**Distribuição por fase:**

| Fase | Account | GT | Copy | Analista | Total |
|---|---|---|---|---|---|
| Diagnóstico (one-time) | 12h | 8h | 0h | 16h | 36h |
| Implantação (total) | 20h | 40h | 60h | 20h | 140h |
| Gestão (por mês) | 8h | 4h | 12h | 8h | 32h |

### 8.2 Capacidade e Escalabilidade

**Cenário atual (time existente da Peretto & Co.):**

| Recurso | Capacidade | Clientes Suportados |
|---|---|---|
| Account (1 pessoa) | 24h disponíveis/mês para AI SEO (além dos clientes atuais) | 3 clientes em gestão |
| GT (1 pessoa) | 16h/mês | 4 clientes |
| Copy (1 pessoa) | 24h/mês (dedicada) | 2 clientes (ou 1 em implantação + 1 em gestão) |
| Analista (1 pessoa, compartilhada) | 16h/mês | 2 clientes |
| **Total** | **80h/mês disponíveis** | **3-4 clientes em gestão contínua** |

**Para escalar para 10+ clientes:**
- Copy dedicada em tempo integral (1 pessoa = 8 clientes em gestão)
- Analista de dados
- Automações cobrindo 70% do monitoramento (n8n + scripts)
- @analista-dados + @revisor absorvendo parte da carga

### 8.3 RACI Matrix

| Atividade | Account | GT | Copy | Analista | Revisor | Coord |
|---|---|---|---|---|---|---|
| Venda e proposta | R | I | I | C | — | A |
| Kickoff | R | C | C | C | — | A |
| Auditoria técnica | C | R | C | C | — | I |
| Content optimization | C | — | R | C | I | A |
| Schema markup | — | R | — | C | I | I |
| Third-party presence | R | — | C | — | — | A |
| Relatório mensal | C | C | I | R | I | I |
| QBR | R | C | I | C | — | A |
| Upsell/Expansão | R | — | — | C | — | A |
| Retenção | R | — | — | — | — | C |

**Legenda:** R = Responsible, A = Accountable, C = Consulted, I = Informed

---

## 9. Anexos

### Anexo 1: Template de Diagnóstico Inicial

> Ver `docs/templates/ai-seo-diagnostico-template.md` para o template completo.

Estrutura do diagnóstico:
```
1. Resumo Executivo (1 página)
2. Metodologia
3. Resultados por Plataforma
4. Benchmark Competitivo
5. Auditoria Técnica
6. Análise de Conteúdo
7. Gap Analysis
8. Roadmap Recomendado
9. ROI Projetado
10. Próximos Passos
```

### Anexo 2: Template de Relatório Mensal

> Ver `docs/templates/ai-seo-relatorio-mensal-template.md` para o template completo.

Estrutura:
```
1. Dashboard de Métricas (1 página)
2. Detalhamento por Plataforma
3. Share of AI Voice vs Concorrentes
4. Query Coverage Progress
5. AI Referral Traffic
6. Otimizações Realizadas no Mês
7. Próximas Ações (30 dias)
```

### Anexo 3: Template de QBR

> Ver `docs/templates/ai-seo-qbr-template.md` para o template completo.

Estrutura:
```
1. Resultados do Trimestre (vs baseline, vs trimestre anterior)
2. Métricas Principais (citation count, SAIV, query coverage, traffic)
3. Benchmarks
4. Concorrentes: Novos Entrantes e Movimentações
5. Google/Mercado: Mudanças em AI Overviews/plataformas
6. Recomendações Estratégicas
7. Oportunidades de Expansão
8. SOW Atualizado (se aplicável)
```

### Anexo 4: Checklist de Implementação

```markdown
## Sprint 1 — Foundation
- [ ] robots.txt libera GPTBot
- [ ] robots.txt libera PerplexityBot
- [ ] robots.txt libera ClaudeBot
- [ ] robots.txt libera Google-Extended
- [ ] Organization schema implementado
- [ ] Article/BlogPosting schema implementado
- [ ] FAQPage schema implementado
- [ ] HowTo schema implementado (se aplicável)
- [ ] Product schema implementado (se aplicável)
- [ ] /pricing.md criado
- [ ] /llms.txt criado
- [ ] "Last updated" visível em todas as páginas
- [ ] Author attribution com credentials
- [ ] Validação SEMRush Site Audit: sem erros críticos

## Sprint 2 — Content
- [ ] Página 1: definition block + bloco correto
- [ ] Página 2: definition block + bloco correto
- [ ] Página 3: definition block + bloco correto
- [ ] Página 4: definition block + bloco correto
- [ ] Página 5: definition block + bloco correto
- [ ] Página 6: definition block + bloco correto
- [ ] Página 7: definition block + bloco correto
- [ ] Página 8: definition block + bloco correto
- [ ] Página 9: definition block + bloco correto
- [ ] Página 10: definition block + bloco correto
- [ ] Extractability score: 80%+ em todas as páginas otimizadas
- [ ] Estatísticas com fontes citadas em todas as páginas
- [ ] Datas atualizadas em todo o conteúdo otimizado

## Sprint 3 — Presence
- [ ] Wikipedia: página verificada/atualizada
- [ ] Reddit: respostas iniciadas em 3 subreddits relevantes
- [ ] G2/Capterra: perfil atualizado
- [ ] YouTube: conteúdo otimizado vinculado (se aplicável)
- [ ] Quora: respostas para 5 perguntas do nicho
- [ ] Validação final: 20 queries testadas em ChatGPT + Perplexity
- [ ] Validação final: relatório de citações capturadas
```

### Anexo 5: Planilha de Métricas (Estrutura)

```csv
mes,cliente,query,plataforma,resultado,citou_cliente,concorrente_citado,sentimento,notas
2026-06,Cliente X,what is category X,ChatGPT,Resposta completa,TRUE,Concorrente A,positivo,"Citou como melhor opção"
2026-06,Cliente X,best category X for Y,Perplexity,Lista com 5 opções,TRUE,Concorrente B,neutro,"Citou mas não destacou"
...
```

### Anexo 6: Estrutura da Pasta do Cliente em AI Visibility

```
squads/{squad}/clientes/{cliente}/campanhas/ai-visibility/
├── diagnostico/
│   ├── diagnostico-YYYY-MM-DD.pdf
│   └── queries-alvo.md
├── implementacao/
│   ├── sprint-1-foundation/
│   ├── sprint-2-content/
│   ├── sprint-3-presence/
│   └── checklist-completo.md
├── gestao/
│   ├── metricas/
│   │   ├── 2026-06.csv
│   │   ├── 2026-07.csv
│   │   └── ...
│   ├── relatorios/
│   │   ├── 2026-06.md
│   │   ├── 2026-07.md
│   │   └── ...
│   ├── dashboards/
│   │   ├── 2026-06.html
│   │   ├── 2026-07.html
│   │   └── ...
│   └── qbr/
│       ├── Q3-2026.md
│       ├── Q3-2026.html
│       └── ...
├── links.md
└── README.md
```

---

## Apêndice: FAQs Internas

### Para o time de vendas

**P: "O que eu falo quando o cliente pergunta: 'Isso não é a mesma coisa que SEO?'"**

R: Não é. SEO tradicional otimiza para ranquear na página de resultados do Google. AI SEO otimiza para ser citado como fonte dentro das respostas geradas por IA. A diferença prática: uma página no topo do Google pode ser ignorada pela IA se não tiver a estrutura certa. E uma página na página 3 pode ser citada se tiver conteúdo extraível. São canais complementares.

**P: "Qual o argumento mais forte pra fechar?"**

R: "47% das buscas no Google já mostram AI Overviews. Seu concorrente X está sendo citado em 12 respostas de IA diferentes este mês. Cada citação é um contato com um comprador sem você pagar por clique. Enquanto você não estiver otimizado, seu concorrente ocupa esse espaço de graça."

**P: "Quanto tempo até ver resultado?"**

R: "Resultados técnicos (robots.txt, schema) em 2 semanas. Primeiras citações em 30-60 dias. Curva completa de maturação em 3-4 meses."

### Para o time de entrega

**P: "Como priorizar quais páginas otimizar primeiro?"**

R: (1) Páginas mais relevantes para as queries-alvo do cliente → (2) Páginas com maior tráfego orgânico → (3) Páginas com maior gap competitivo → (4) Páginas que já têm algum conteúdo aproveitável.

**P: "E se o cliente não tem blog/conteúdo?"**

R: O serviço se adapta. Foco maior em product pages, pricing, comparisons, e third-party presence. Também sugerimos Content Production como add-on.

**P: "Como medimos se está funcionando antes de 3 meses?"**

R: Métricas leading: extractability score, schema coverage, bot accessibility. Todas melhoram nas primeiras semanas. Citation count começa a aparecer entre dias 30-60.

### Para o coordenador

**P: "Qual a margem desse serviço?"**

R: Considerando time existente (já pago pelos clientes atuais) + ferramentas já contratadas (SEMRush), o custo incremental de entregar AI Visibility é aproximadamente 30-40% do ticket. Margem bruta: 60-70%.

**P: "Quantos clientes precisamos pra valer a pena?"**

R: 3 clientes em gestão contínua (R$ 23.700/mês) pagam o custo de uma pessoa dedicada. 5 clientes (R$ 39.500/mês) tornam a operação lucrativa com sobra para investimento.

> **Documento gerado em:** 21/05/2026
> **Próxima revisão:** 21/08/2026
> **Responsável:** [Nome do Coordenador]
