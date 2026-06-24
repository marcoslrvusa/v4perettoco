# Custos — Projeção Mensal por Squad

**Propósito:** Projeção de custos mensais do Agent Hub, dividida por squad, com cenários de uso e comparação de modelos.

---

## 1. Custos Fixos (Infraestrutura)

| Item | Valor Mensal | Detalhes |
|---|---|---|
| **VPS Hostinger** (4 vCPU, 16GB) | ~R$ 120 | OpenCode + LiteLLM + n8n |
| **Domínio** | ~R$ 5 | v4company.com.br (já existe) |
| **Google Workspace** | ~R$ 30/mês por usuário | Já existente na V4 |
| **n8n** (self-hosted) | Grátis | Docker image gratuita |
| **LiteLLM** (self-hosted) | Grátis | Open source |
| **Total fixo** | **~R$ 155/mês** | | 

## 2. Custos Variáveis (Modelos de IA)

### Cenário Conservador (squads usando modelos gratuitos + gpt-4o-mini)

| Squad | Modelo Principal | Calls/Dia | Tokens/Call | Custo/Dia | Custo/Mês |
|---|---|---|---|---|---|
| Account | deepseek-v4-flash (free) | 20 | 8K | $0 | $0 |
| Copy | gpt-4o-mini | 15 | 10K | $0,03 | $0,90 |
| GT | deepseek-v4-flash (free) | 10 | 12K | $0 | $0 |
| Design | claude-sonnet-4 | 5 | 15K | $0,23 | $6,90 |
| CSM | gpt-4o-mini | 5 | 6K | $0,01 | $0,30 |
| Coord | claude-sonnet-4 | 8 | 20K | $0,61 | $18,30 |
| Geral | deepseek-v4-flash (free) | 15 | 8K | $0 | $0 |
| **Total** | | **78** | | **$0,88** | **$26,40** |

### Cenário Moderado (alternando modelos conforme complexidade)

| Squad | Modelo Padrão | Modelo Pesado | Calls/Dia | Custo/Mês |
|---|---|---|---|---|
| Account | deepseek-v4-flash | claude-sonnet-4 (10% calls) | 20 | ~$3,50 |
| Copy | gpt-4o-mini | gpt-4o (5% calls) | 20 | ~$4,20 |
| GT | deepseek-v4-flash | gpt-4o (10% calls) | 15 | ~$5,80 |
| Design | claude-sonnet-4 | gpt-4o (20% calls) | 10 | ~$18,40 |
| CSM | gpt-4o-mini | claude-sonnet-4 (5% calls) | 8 | ~$2,10 |
| Coord | claude-sonnet-4 | gpt-4o (15% calls) | 12 | ~$32,50 |
| Geral | deepseek-v4-flash | gpt-4o-mini (20% calls) | 20 | ~$1,80 |
| **Total** | | | **105** | **~$68,30** |

### Cenário Intensivo (full power, máximos calls)

| Squad | Calls/Dia | Custo/Mês |
|---|---|---|
| Account | 50 | ~$12 |
| Copy | 40 | ~$15 |
| GT | 30 | ~$18 |
| Design | 25 | ~$45 |
| CSM | 20 | ~$8 |
| Coord | 30 | ~$78 |
| Geral | 40 | ~$5 |
| **Total** | **235** | **~$181** |

## 3. Comparação de Modelos

| Modelo | Custo por 1M Input | Custo por 1M Output | Qualidade | Uso Recomendado |
|---|---|---|---|---|
| **DeepSeek V4 Flash** | **Grátis** | **Grátis** | Alta | Account, GT, Geral |
| **Gemini 2.5 Flash** | **Grátis** | **Grátis** | Alta | Copy, Pesquisa |
| **GPT-4o Mini** | $0,15 | $0,60 | Média-Alta | Copy, CSM, Relatórios |
| **Claude Sonnet 4** | $3,00 | $15,00 | Muito Alta | Design, Coord (briefings) |
| **GPT-4o** | $2,50 | $10,00 | Alta | Design, Coord (ocasional) |

## 4. Estratégia de Otimização

1. **DeepSeek V4 Flash como padrão** para 70% das operações (Account, GT, Geral)
2. **Gemini 2.5 Flash grátis** para análise de documentos grandes (Copy, Pesquisador)
3. **GPT-4o Mini** para tarefas que exigem instrução em português (Copy, CSM)
4. **Claude Sonnet 4** apenas para Design e Coord (briefings estratégicos)
5. **GPT-4o** como fallback raro (quando os outros não atendem)
6. **Budget por squad** no LiteLLM para evitar estouro

## 5. Resumo Mensal

| Categoria | Conservador | Moderado | Intensivo |
|---|---|---|---|
| Infraestrutura fixa | R$ 155 | R$ 155 | R$ 155 |
| Modelos de IA | ~R$ 150 (USD $26) | ~R$ 390 (USD $68) | ~R$ 1.035 (USD $181) |
| **Total estimado** | **~R$ 305/mês** | **~R$ 545/mês** | **~R$ 1.190/mês** |

---

**Documentos relacionados:**
- [02-componentes/02-litellm.md](../02-componentes/02-litellm.md) — Gateway de modelos
- [02-seguranca.md](02-seguranca.md) — Políticas de acesso
