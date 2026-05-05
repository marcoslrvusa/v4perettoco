---
name: trafego-relatorio-semanal-okr
description: Gera relatório HTML semanal com performance Google Ads vs OKR de todos os clientes configurados. Ideal para rodar toda segunda-feira e ter visão consolidada de investimento, conversões, CAC e progresso de metas. Pode ser agendado via /schedule. Depende da skill google-ads-dados para autenticação.
area: trafego
author: marcoslrvusa
version: 1.0.0
---

# /trafego-relatorio-semanal-okr

Gera relatório semanal consolidado de Google Ads + OKR para todos os clientes com credenciais configuradas. Substitui o processo manual de segunda-feira.

## Pré-requisitos

1. Skill `google-ads-dados` configurada (credenciais em `clientes/<cliente>/.env`)
2. Arquivo `clientes/<cliente>/okrs.json` com metas do quarter (opcional, mas necessário para comparar vs OKR)

## Configurar OKRs do cliente

Crie `clientes/<cliente>/okrs.json`:

```json
{
  "quarter": "Q2 2026",
  "meta_anual": "$10MM/ano",
  "targets": {
    "investimento_semana": 3000,
    "leads_semana": 15,
    "cac_max": 300
  }
}
```

| Campo | Descrição |
|---|---|
| `investimento_semana` | Budget semanal esperado em USD |
| `leads_semana` | Conversões esperadas por semana |
| `cac_max` | CAC máximo aceitável em USD |

## Rodar manualmente

```bash
# De dentro do builders-hub:
python3 .claude/skills/trafego-relatorio-semanal-okr/scripts/gerar_relatorio_semanal.py

# Só alguns clientes:
python3 ... --clientes all-over-exterior-roofing,conserva-irrigation

# Janela de 30 dias:
python3 ... --days 30

# Salvar em local específico:
python3 ... --out relatorios/semana-personalizada.html
```

O relatório é salvo em `relatorios/okr-semanal-YYYY-WNN.html`.

## Agendar para toda segunda-feira

Rode `/schedule` e use:
- **Schedule**: `0 8 * * 1` (toda segunda às 8h)
- **Prompt**: `Rode o relatório semanal de Google Ads: python3 .claude/skills/trafego-relatorio-semanal-okr/scripts/gerar_relatorio_semanal.py e me dê um resumo dos alertas (clientes com CAC acima do teto, conversões abaixo de 50% da meta, campanhas com gasto zerado).`

## O que o relatório mostra

Para cada cliente com `GOOGLE_ADS_CUSTOMER_ID` no `.env`:

- **Investimento** — spend da semana vs meta (verde/amarelo/vermelho)
- **Conversões** — leads/conversões vs meta
- **CAC** — custo por conversão vs teto definido
- **CTR** — taxa de clique geral da conta
- **Top 5 campanhas** — por spend, com CAC individual

## Interpretar as cores dos KPIs

| Cor | Significado |
|---|---|
| Verde | Dentro do esperado (±20%) |
| Amarelo | Atenção — desvio entre 20-40% |
| Vermelho | Crítico — desvio >40% ou acima do teto |
| Cinza | Sem meta configurada |

## Depois do relatório

O Claude analisa o HTML e pode:
- Apontar alertas prioritários
- Sugerir FCAs para clientes fora do OKR
- Exportar CSV por cliente via `/google-ads-dados`
- Gerar versão apresentável via `/frontend-design`
