---
name: google-ads-dados
description: Consulta qualquer dado do Google Ads (campanhas, keywords, search terms, conversoes, account) via API oficial. Use quando o usuario pedir metricas de Google Ads — spend, impressoes, clicks, CTR, CAC, conversoes, quality score, search impression share. Aceita linguagem natural e traduz em query GAQL. Credenciais em clientes/<cliente>/.env.
area: google
author: marcoslrvusa
version: 1.0.0
---

# /google-ads-dados

Integração direta com Google Ads API v19 via biblioteca oficial `google-ads`. Sem N8N, sem intermediário.

## Setup inicial (uma vez por conta Google)

### 1 — Credenciais OAuth2

```bash
python3 .claude/skills/google-ads-dados/scripts/gerar_oauth_token.py
```

Você vai precisar de:
- **Developer Token**: [ads.google.com](https://ads.google.com) → Ferramentas → Centro de API
- **Client ID + Secret**: [console.cloud.google.com](https://console.cloud.google.com) → APIs & Services → Credentials → Create OAuth 2.0 Client (Desktop App)
  - Habilitar antes: Google Ads API em "Enable APIs"

O script abre o navegador, você autoriza, e imprime o `REFRESH_TOKEN` na tela.

### 2 — Customer ID

É o ID de 10 dígitos da conta Google Ads do cliente (sem hifens). Aparece no canto superior direito do Google Ads.

Se usar conta gerenciadora (MCC), preencha também `GOOGLE_ADS_LOGIN_CUSTOMER_ID`.

### 3 — Salvar em .env do cliente

```
# clientes/<cliente>/.env
GOOGLE_ADS_DEVELOPER_TOKEN=xxxx
GOOGLE_ADS_CLIENT_ID=xxxx.apps.googleusercontent.com
GOOGLE_ADS_CLIENT_SECRET=xxxx
GOOGLE_ADS_REFRESH_TOKEN=1//xxxx
GOOGLE_ADS_CUSTOMER_ID=1234567890
# GOOGLE_ADS_LOGIN_CUSTOMER_ID=9876543210  (só se usar MCC)
```

`DEVELOPER_TOKEN`, `CLIENT_ID`, `CLIENT_SECRET` e `REFRESH_TOKEN` são seus (V4er) — valem para todos os clientes. Só `CUSTOMER_ID` muda por cliente.

---

## Como usar

### Passo 1 — Identificar cliente
Mesmo padrão da v4mos: detecta pela pasta atual ou pergunta.

### Passo 2 — Verificar credenciais
```bash
grep "^GOOGLE_ADS" clientes/<cliente>/.env | sed 's/=.*$/=<set>/'
```
Se faltar algo, pede e salva interativamente.

### Passo 3 — Executar query

```bash
python3 .claude/skills/google-ads-dados/scripts/google_ads_query.py <preset> --cliente <nome> [flags]
```

**Presets disponíveis:**

| Preset | O que retorna |
|---|---|
| `account` | Métricas totais da conta (spend, clicks, conversões, CTR) |
| `campaigns` | Performance por campanha + budget + search impression share |
| `adgroups` | Performance por grupo de anúncios |
| `keywords` | Keywords + quality score + métricas |
| `search_terms` | Termos de busca reais (o que as pessoas digitaram) |
| `conversions` | Ações de conversão configuradas |

**Flags:**

| Flag | Exemplo | Descrição |
|---|---|---|
| `--days N` | `--days 7` | Janela em dias (terminando ontem) |
| `--since/--until` | `--since 2026-04-01 --until 2026-04-22` | Período explícito |
| `--fields` | `--fields campaign.name,metrics.cost,metrics.conversions` | Subset de colunas |
| `--format` | `--format json` | `table` (default), `json`, `csv` |
| `--out` | `--out relatorios/semana.csv` | Salvar em arquivo |
| `--max N` | `--max 20` | Limitar linhas |
| `--customer-id` | `--customer-id 1234567890` | Override do ID |

### Exemplos de tradução linguagem natural → comando

| Pergunta | Comando |
|---|---|
| "top campanhas da semana" | `campaigns --days 7 --max 10` |
| "quanto gastei esse mês" | `account --days 30 --fields customer.descriptive_name,metrics.cost` |
| "keywords com quality score baixo" | `keywords --days 30 --fields ad_group_criterion.keyword.text,metrics.quality_score,metrics.cost` |
| "o que as pessoas estão buscando" | `search_terms --days 7 --max 50` |
| "CAC de cada campanha" | `campaigns --days 30 --fields campaign.name,metrics.cost,metrics.conversions,metrics.cost_per_conversion` |
| "exporta tudo pra CSV" | `campaigns --days 30 --format csv --out relatorios/google-ads-mes.csv` |

### Passo 4 — Entregar resultado

Se não ficou claro no pedido, pergunte como quer consumir:
1. **Conversar** — analiso os dados, aponto anomalias, sugiro ações
2. **HTML** — dashboard ou relatório via `/frontend-design`
3. **CSV** — para Excel ou análise offline
4. **PDF** — via Chrome headless a partir do HTML

---

## Gotchas

- `metrics.cost_micros` é convertido automaticamente para dólares como `metrics.cost`
- `metrics.ctr` vem como proporção (0.05 = 5%) — o script não normaliza, cheque no output
- `search_impression_share` pode vir como string `"< 10%"` para valores baixos
- Dados do Google Ads têm latência de 1-3 dias para conversões com janela de atribuição
- Se a conta usar conversões importadas do CRM, elas aparecem em `conversions` com delay maior

## Debug

```bash
# Testar autenticação sem puxar dados
python3 .claude/skills/google-ads-dados/scripts/google_ads_query.py account --cliente <nome> --max 1

# Ver estrutura JSON bruta
python3 ... --format json --max 1
```

Exit 2 = credencial faltando. Exit 1 = erro na API (mensagem impressa).
