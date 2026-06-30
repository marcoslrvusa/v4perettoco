---
name: gt-relatorios-trafego
description: Relatorio consolidado de trafego multicanal — Google Ads, Meta Ads, Bing Ads. Gera reports HTML/JSON, envia por email, salva no Drive e entrega analise com IA. Inclui deteccao de anomalias, pace de verba e comparativo entre periodos.
area: gt
author: v4team
version: 1.0.0
aliases: [gt-relatorios-trafego]
tags: [skill, area-gt]
---
# GT — Relatorios de Trafego

Skill que gera relatorios consolidados de performance de midia paga nas 3 principais plataformas: **Google Ads**, **Meta Ads** e **Bing Ads**. Integra GA4 para contexto de site e usa Claude para analise qualitativa.

## Arvore de Decisao

```
USUARIO PEDE RELATORIO DE TRAFEGO
│
├─ Qual plataforma?
│  ├─ Google Ads → GoogleAdsConnector (via google-ads SDK)
│  ├─ Meta Ads → MetaConnector (via facebook-business SDK)
│  ├─ Bing Ads → BingAdsConnector (via bingads SDK)
│  └─ Todas → relatorio consolidado
│
├─ Qual periodo?
│  ├──days 7 (default — semanal)
│  ├──days 30 (mensal)
│  └──days 90 (trimestral)
│
├─ Qual formato de saida?
│  ├─ HTML → visual + email via GmailConnector
│  ├─ JSON → estruturado + Drive via DriveConnector
│  └─ Terminal → preview rapido
│
├─ Precisa de analise?
│  ├─ Sim → Claude processa dados → relatorio CHAS
│  └─ Nao → dados brutos
│
└─ Onde salvar?
   ├─ Email → GmailConnector.send()
   ├─ Google Drive → DriveConnector.ensure_folder() + upload
   └─ Local → --out ./reports/
```

## O que produz

1. **Relatorio HTML** — visual com cards de KPI por cliente + plataforma, codigos de cor (verde/amarelo/vermelho) por ROAS
2. **Relatorio JSON** — dados estruturados para consumo por outros sistemas
3. **Analise via IA** — Claude processa os dados e entrega: resumo executivo, anomalias, recomendacoes
4. **Relatorio de Pace** — quanto gastou vs quanto deveria ter gasto no mes
5. **Upload automatico no Drive** — hierarquia `Relatorios V4/Trafego/{YYYY-MM}/`

## Pre-requisitos

- `v4-automations/config/.env` com credenciais de todas as plataformas
- `v4-automations/config/clientes.json` com os IDs das contas de cada cliente
- Dependencias Python: `pip install google-ads facebook-business bingads`

## Quando triggerar

- "Gera o relatorio de trafego da semana"
- "Quero ver performance de {cliente} nos ultimos 30 dias"
- "Comparativo entre Google e Meta do mes passado"
- "Relatorio consolidado de todos os clientes"
- "Manda o report semanal pro email do GT"

## Fluxo

### Passo 1 — Identificar escopo

Pergunte: qual cliente (ou todos), quantos dias, qual formato, quer analise IA?

Se o usuario pediu coisa vaga tipo "relatorio de trafego", assuma: todos os clientes, 7 dias, formato HTML com analise IA.

### Passo 2 — Coletar dados

Para cada cliente no escopo, coleta de cada plataforma configurada:

```python
python3 v4-automations/scripts/gt/relatorio_trafego.py \
  --cliente "Cliente A" --days 30 --format json --out ./reports
```

Ou para todos:
```python
python3 v4-automations/scripts/gt/relatorio_trafego.py \
  --all --days 7 --format html --email gt@v4company.com
```

### Passo 3 — Processar e enriquecer

- Calcula ROAS, CPA, CPC consolidados
- Detecta anomalias (desvio > 20% vs meta)
- Calcula pace de verba (gasto real vs esperado)

### Passo 4 — Analisar com IA (opcional)

Se o usuario pediu analise, Claude processa os dados e entrega:
- Resumo executivo (3 bullets)
- Analise por plataforma
- Top 3 acoes para a proxima semana

### Passo 5 — Entregar

- Se HTML: abre no browser ou envia por email
- Se JSON: salva local ou no Drive
- Se terminal: printa na tela

## Canais suportados e mapeamento

| Plataforma | Classe | Dados coletados | Config em clientes.json |
|---|---|---|---|
| Google Ads | `GoogleAdsConnector` | Investimento, conversoes, receita, ROAS, CPC, CPA, cliques | `google_ads_customer_id` |
| Meta Ads | `MetaConnector` | Investimento, conversoes, receita, ROAS, CPA, CTR, CPM, frequencia | `meta_ad_account_id` |
| Bing Ads | `BingAdsConnector` | Investimento, conversoes, receita, ROAS, CPC, CPA | `bing_ads_customer_id` + `bing_ads_account_id` |
| GA4 (ctx) | `GA4Connector` | Sessoes, conversoes, taxa de conversao | `ga4_property_id` |

## Conexao com outras skills

- **[[v4mos-dados-meta-ads]]** — alternativa quando V4mos esta disponivel para Meta Ads (mais granular)
- **[[gt-gestor-de-trafego-completo]]** — consome este relatorio para analise preditiva e planejamento
- **[[analytics-tracking]]** — valida se os eventos estao configurados corretamente
- **[[account-checkin-review]]** — alimenta check-ins com dados de trafego reais
