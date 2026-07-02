# Plano de Implantação — Arquitetura de Agentes Peretto & Co

> Gerado em: 2026-05-17
> Autor: OpenCode + Marcos
> Status: **Aprovado para execução**

---

## Índice

1. [Diagnóstico do Estado Atual](#1-diagnóstico-do-estado-atual)
2. [Hierarquia de Modelos Free](#2-hierarquia-de-modelos-free)
3. [Arquitetura de Agentes](#3-arquitetura-de-agentes)
4. [Pesos e Contrapesos (Governança)](#4-pesos-e-contrapesos-governança)
5. [Estrutura de Arquivos](#5-estrutura-de-arquivos)
6. [Detalhamento de Cada Agente](#6-detalhamento-de-cada-agente)
7. [Fluxo de Orquestração Async](#7-fluxo-de-orquestração-async)
8. [Blocos de Execução](#8-blocos-de-execução)
9. [Transição AM → CSM](#9-transição-am--csm)
10. [Resultado Esperado](#10-resultado-esperado)

---

## 1. Diagnóstico do Estado Atual

| Item | Status |
|---|---|
| **Providers** | Google (Gemini) ✅ + OpenRouter ✅ |
| **OpenCode Zen (gratuitos)** | `deepseek-v4-flash-free`, `minimax-m2.5-free`, `nemotron-3-super-free`, `qwen3.6-plus-free` |
| **OpenRouter free** | `deepseek-v4-flash:free`, `gpt-oss-120b:free`, `nemotron-3-super-120b:free`, `minimax-m2.5:free`, `llama-3.3-70b:free`, `hermes-3-405b:free`, `gemma-4-31b:free`, `qwen3-coder:free`, `nemotron-3-nano:free`, `trinity-large-thinking:free`, `+` dezenas mais |
| **Google (Gemini) free** | `gemini-2.5-flash`, `gemini-1.5-flash`, `gemini-2.0-flash-lite` |
| **opencode.json (projeto)** | ❌ **Não existe** — só o global com 3 commands de sessão |
| **Agentes OpenCode** | ❌ **Zero** configurados |
| **Subagents custom** | ❌ Nenhum |
| **Custom Tools** | ❌ Nenhuma |
| **Skills V4** | ✅ Existem em `.agents/skills/` e `.claude/skills/` (account, gt, copy, coord, csm, etc) |
| **MVP PDF** | Desatualizado — fala de NVIDIA NIM, não reflete OpenCode Zen + OpenRouter |
| **v4-automations/** | ✅ Existe com scripts, setup, cron |
| **csm-hub/** | ✅ Existe com módulos (csm-principal, flag-roi, flag-churn, flag-okr, flag-operacao) |
| **Squads** | 1 squad (prime) com 5+ clientes ativos |

---

## 2. Hierarquia de Modelos Free

Todos os modelos abaixo são **100% gratuitos** — seja via OpenCode Zen, Google AI ou OpenRouter.

### Tiers de Uso

| Tier | Modelo | Provider | Contexto | Força | Agentes Alvo |
|---|---|---|---|---|---|
| **S** | `opencode/deepseek-v4-flash-free` | Zen | 1M tokens | Raciocínio, código, análise complexa, matemática | `@analista-dados`, `@revisor`, `@flag-*` |
| **S** | `google/gemini-2.5-flash` | Google | 1M tokens | Criação visual, HTML, CSS, multimodal, tradução | `@gerar-pdf`, `@gerar-ppt`, `@gerar-html`, `@gerar-doc` |
| **A** | `openrouter/openai/gpt-oss-120b:free` | OpenRouter | 128k | Escrita geral, marketing, planejamento, orquestração | `@csm-orquestrador`, `@executor-comite` |
| **A** | `openrouter/nousresearch/hermes-3-llama-3.1-405b:free` | OpenRouter | 32k | 405B — raciocínio profundo, nuance, análise de contrato | Revisão crítica, segunda opinião |
| **B** | `opencode/minimax-m2.5-free` | Zen | 256k | Velocidade, tarefas rápidas, baixa latência | Quick checks, classificações, parsing |
| **B** | `opencode/nemotron-3-super-free` (ou 120B via OR) | Zen | 128k | Output estruturado, tarefas técnicas, schemas | Formatação, extração de dados |
| **C** | `opencode/qwen3.6-plus-free` | Zen | 128k | Auxiliar leve, análises simples | Backup, tarefas menores |
| **C** | `openrouter/meta-llama/llama-3.3-70b-instruct:free` | OpenRouter | 128k | Backup geral confiável | Quando os S/A rate-limitarem |
| **D** | `openrouter/google/gemma-4-31b-it:free` | OpenRouter | 8k | Tarefas triviais | Classificação simples |
| **D** | `openrouter/nvidia/nemotron-3-nano-30b-a3b:free` | OpenRouter | 128k | Tarefas mínimas | Regex, transform simples |

### Regra de Uso

```
Tarefa complexa (código, análise, decisão) → Tier S (DeepSeek)
Tarefa visual (PDF, PPT, HTML, DOC)        → Tier S (Gemini 2.5 Flash)
Tarefa de escrita/orquestração              → Tier A (GPT-OSS 120B)
Tarefa de segunda opinião                   → Tier A (Hermes 3 405B)
Tarefa rápida/estruturada                   → Tier B (MiniMax / Nemotron)
Tarefa trivial                              → Tier C/D
```

---

## 3. Arquitetura de Agentes

### Diagrama de Camadas

```
                    ┌──────────────────────────────────────┐
                    │         @csm-orquestrador             │
                    │  GPT-OSS 120B · Acima do squad       │
                    │  Planejamento · Setup · Visão         │
                    └──────────┬───────────────────────────┘
                               │ aciona (Task tool via @)
                               │
               ┌───────────────┼───────────────┐
               ▼               ▼               ▼
     ┌─────────────────┐ ┌──────────┐ ┌──────────────┐
     │  @analista-dados │ │ @revisor │ │  @flag-*     │
     │  DeepSeek V4     │ │DeepSeek  │ │ (4 agentes)  │
     │  edit:allow      │ │edit:deny │ │ DeepSeek V4  │
     │  bash:allow      │ │bash:deny │ │ bash:allow   │
     └────────┬─────────┘ └──────────┘ └──────┬───────┘
              │ feedback loop                  │ dados
              ▼                                ▼
     ┌──────────────────────────────────────────────────┐
     │              AGENTES DE ENTREGA                   │
     │                                                    │
     │  ┌──────────┐ ┌──────────┐ ┌──────────┐           │
     │  │gerar-pdf │ │gerar-ppt │ │gerar-html│           │
     │  │Gemini 2.5│ │Gemini 2.5│ │Gemini 2.5│           │
     │  └──────────┘ └──────────┘ └──────────┘           │
     │  ┌──────────┐ ┌────────────────────────┐          │
     │  │gerar-doc │ │ @executor-comite       │          │
     │  │Gemini 2.5│ │ Briefing · Ata · FCA   │          │
     │  └──────────┘ │ GPT-OSS 120B           │          │
     │               └────────────────────────┘          │
     └──────────────────────────────────────────────────┘
```

### Agentes de Flag (CSM)

```
 ┌─────────────────────────────────────────────────────┐
 │              @flag-roi                               │
 │  DeepSeek V4 · ROAS abaixo da meta 2 semanas        │
 │  Classifica: custo / conversão / valor               │
 │  Gera: CHAS para GT + comunicação ao Coordenador     │
 └─────────────────────────────────────────────────────┘

 ┌─────────────────────────────────────────────────────┐
 │              @flag-churn                             │
 │  DeepSeek V4 · NPS + CSAT caem juntos               │
 │  Distingue: churn por percepção vs churn por resultado│
 │  Gera: plano de retenção + comunicação CSM           │
 └─────────────────────────────────────────────────────┘

 ┌─────────────────────────────────────────────────────┐
 │              @flag-okr                               │
 │  DeepSeek V4 · KR abaixo de 60% do esperado         │
 │  Distingue: desvio de execução vs desvio de premissa │
 │  Gera: replanejamento ou novo plano de ação          │
 └─────────────────────────────────────────────────────┘

 ┌─────────────────────────────────────────────────────┐
 │              @flag-operacao                          │
 │  DeepSeek V4 · Sprint atrasa sem FCA / timesheet zero│
 │  Classifica: operacional / estrutural / externo      │
 │  Gera: alerta com prazo + responsável                │
 └─────────────────────────────────────────────────────┘
```

---

## 4. Pesos e Contrapesos (Governança)

### Matriz de Permissões

| Agente | read | edit | bash | webfetch | Pode sem revisão |
|---|---|---|---|---|---|
| `@analista-dados` | ✅ allow | ✅ allow | ✅ allow | ✅ allow | **Relatórios internos** |
| `@revisor` | ✅ allow | ❌ deny | ❌ deny | ❌ deny | — (só valida) |
| `@gerar-pdf/ppt/html/doc` | ✅ allow | ✅ allow | ✅ allow | ❌ deny | **Documentos** (são assets, não operação) |
| `@flag-*` | ✅ allow | ❌ deny | ✅ allow | ❌ deny | **Diagnóstico**, mas não executa ação |
| `@csm-orquestrador` | ✅ allow | ✅ allow | ✅ allow | ✅ allow | **Setup inicial** (com revisão) |
| `@executor-comite` | ✅ allow | ✅ allow | ✅ allow | ❌ deny | Briefings (com Revisor) |

### Regras de Ouro

1. **Agente que escreve em sistema real** (Ekyte, CRM, campanhas) → precisa de `@revisor` antes
2. **Agente que só cria documentos/relatórios** → roda autônomo
3. **Agente que detecta anomalia** → só diagnostica, não executa. Quem executa é o humano ou um script com crontab
4. **@revisor tem edit:deny** — ele aponta o erro, não corrige. Quem corrige é o agente executor (ou o humano)

### Fluxo de Validação Típico

```
@analista-dados                            @revisor
┌──────────────┐     output JSON     ┌──────────────┐
│ Puxa dados    │ ──────────────────► │ Valida dados  │
│ Gera análise  │                     │ Cruza histórico│
└──────────────┘                     └──────┬───────┘
                                            │
                                ┌───────────┴───────────┐
                                │ Aprovado?              │
                                │                        │
                          ┌─────┴─────┐          ┌──────┴──────┐
                          │   SIM ✅   │          │   NÃO ❌     │
                          │            │          │             │
                     ┌────▼────┐  ┌───▼───┐  ┌───▼──────────┐
                     │@gerar-ppt│  │@gerar-│  │Volta pro     │
                     │@gerar-pdf│  │html   │  │@analista     │
                     │@gerar-doc│  │       │  │com feedback  │
                     └─────────┘  └───────┘  └──────────────┘
```

---

## 5. Estrutura de Arquivos

### A criar no projeto

```
/raiz/
├── opencode.json                       ← CONFIG PRINCIPAL (NOVO)
│
├── .opencode/
│   ├── agents/
│   │   ├── gerar-pdf.md                ← Gemini 2.5 Flash
│   │   ├── gerar-ppt.md                ← Gemini 2.5 Flash
│   │   ├── gerar-html.md               ← Gemini 2.5 Flash
│   │   ├── gerar-doc.md                ← Gemini 2.5 Flash
│   │   ├── analista-dados.md           ← DeepSeek V4 Flash
│   │   ├── revisor.md                  ← DeepSeek V4 (edit:deny)
│   │   ├── csm-orquestrador.md         ← GPT-OSS 120B
│   │   ├── flag-roi.md                 ← DeepSeek V4
│   │   ├── flag-churn.md               ← DeepSeek V4
│   │   ├── flag-okr.md                 ← DeepSeek V4
│   │   ├── flag-operacao.md            ← DeepSeek V4
│   │   └── executor-comite.md          ← Gemini 2.5 Flash
│   │
│   └── commands/
│       ├── session-save.md             ← (já existe)
│       ├── session-list.md             ← (já existe)
│       ├── session-load.md             ← (já existe)
│       └── agendar-rituais.md          ← NOVO
│
├── MVP_Peretto_Co_v3.pdf              ← DOCUMENTO ATUALIZADO
└── PLANO_IMPLANTACAO_AGENTES.md        ← ESTE ARQUIVO
```

### A criar no global

```
~/.config/opencode/
├── agents/                             ← ESPELHO GLOBAL
│   ├── gerar-pdf.md
│   ├── gerar-ppt.md
│   ├── gerar-html.md
│   ├── analista-dados.md
│   ├── revisor.md
│   └── csm-orquestrador.md
│
└── opencode.jsonc                      ← (já existe, expandir)
```

---

## 6. Detalhamento de Cada Agente

### 6.1 `@gerar-pdf` — Criação de PDFs

```
Modelo:     google/gemini-2.5-flash
Skill base: geral-frontend-design
Permissão:  read:allow, edit:allow, bash:allow, webfetch:deny

Descrição: Gera PDFs estilizados no padrão visual V4/Peretto & Co.
           Usa HTML → PDF via browser/print. Layout limpo, profissional,
           com logo, cores e tipografia da marca.

Input:      "Relatório de OKRs do cliente X para o comitê"
Output:     Arquivo .pdf na pasta solicitada + preview em HTML

Quando usar: @gerar-pdf "relatório mensal de performance do cliente X"
```

### 6.2 `@gerar-ppt` — Criação de Apresentações

```
Modelo:     google/gemini-2.5-flash
Skill base: geral-frontend-design
Permissão:  read:allow, edit:allow, bash:allow, webfetch:deny

Descrição: Gera apresentações no estilo V4 (HTML-based slide deck ou
           PPTX). Cada slide segue a hierarquia: headline + data point
           + call to action. Suporte a gráficos e tabelas.

Input:      "Apresentação do comitê de P&EG da semana"
Output:     HTML interativo ou .pptx

Quando usar: @gerar-ppt "briefing do comitê de segunda com dados reais"
```

### 6.3 `@gerar-html` — Criação de Páginas Web

```
Modelo:     google/gemini-2.5-flash
Skill base: geral-frontend-design
Permissão:  read:allow, edit:allow, bash:allow, webfetch:deny

Descrição: Gera HTML/CSS/JS completos para dashboards, landing pages,
           relatórios interativos, status pages. Responsivo, acessível.

Input:      "Dashboard de performance do cliente Y com gráficos"
Output:     Arquivo .html funcional

Quando usar: @gerar-html "dashboard de OKRs do squad prime"
```

### 6.4 `@gerar-doc` — Geração de Documentos

```
Modelo:     google/gemini-2.5-flash
Permissão:  read:allow, edit:allow, bash:allow, webfetch:deny

Descrição: Gera documentos formatados (MD → DOCX/PDF). Ideal para
           atas, relatórios, propostas, manuais. Segue templates V4.

Input:      "Ata do comitê de P&EG com base no transcript da call"
Output:     .md + .docx ou .pdf

Quando usar: @gerar-doc "ata do growth de terça do cliente X"
```

### 6.5 `@analista-dados` — Análise de Dados

```
Modelo:     opencode/deepseek-v4-flash-free
Permissão:  read:allow, edit:allow, bash:allow, webfetch:allow

Descrição: Puxa dados de múltiplas fontes (Google Ads, Meta, GA4,
           Ekyte, CSV), cruza, analisa e gera JSON estruturado com
           insights. 1M de contexto permite análises profundas.

Input:      "Analisa performance do cliente X nos últimos 30 dias"
Output:     JSON estruturado com métricas, flags, hipóteses

Quando usar: @analista-dados "cruza ROAS com CPA do cliente Y este mês"
```

### 6.6 `@revisor` — Validação e Controle de Qualidade

```
Modelo:     opencode/deepseek-v4-flash-free
Permissão:  read:allow, edit:deny, bash:deny, webfetch:allow

Descrição: Valida outputs de outros agentes. Confere números, cruza
           com histórico, verifica formato, aponta inconsistências.
           NUNCA edita — só reporta. Peso e contrapeso do sistema.

Input:      Recebe output do @analista-dados ou @gerador-*
Output:     Relatório de validação: ✅ aprovado ou ❌ com lista de correções

Quando usar: Invocado automaticamente por outros agentes ou manualmente:
             "Revisor: valida este relatório antes de eu enviar"
```

### 6.7 `@csm-orquestrador` — CSM Principal

```
Modelo:     openrouter/openai/gpt-oss-120b:free
Permissão:  read:allow, edit:allow, bash:allow, webfetch:allow

Descrição: O orquestrador CSM. Setup inicial da unidade, triagem de
           flags, acionamento de áreas, QBR com cliente, fechamento
           de loop. Fica ACIMA do squad — não executa, orquestra.

Input:      "Inicie o setup da unidade Squad Prime"
Output:     Plano de ação + acionamento dos agentes de flag

Quando usar: @csm "setup inicial da carteira" / "QBR do cliente X"
```

### 6.8 `@flag-roi` — Flag de ROAS

```
Modelo:     opencode/deepseek-v4-flash-free
Permissão:  read:allow, edit:deny, bash:allow, webfetch:deny

Descrição: Ativado quando ROAS cai abaixo da meta por 2 semanas.
           Classifica o tipo (custo / conversão / valor), gera CHAS
           para o GT e estrutura a comunicação ao Coordenador.
```

### 6.9 `@flag-churn` — Flag de Risco de Churn

```
Modelo:     opencode/deepseek-v4-flash-free
Permissão:  read:allow, edit:deny, bash:allow, webfetch:deny

Descrição: Ativado quando NPS + CSAT caem juntos. Faz a distinção
           crítica entre churn por percepção e churn por resultado.
           Cada um tem plano de resposta completamente diferente.
```

### 6.10 `@flag-okr` — Flag de Desvio de OKR

```
Modelo:     opencode/deepseek-v4-flash-free
Permissão:  read:allow, edit:deny, bash:allow, webfetch:deny

Descrição: Ativado quando KR está abaixo de 60% do progresso esperado.
           Distingue desvio de execução (meta ainda atingível) de
           desvio de premissa (replanejamento necessário).
```

### 6.11 `@flag-operacao` — Flag de Operação Travada

```
Modelo:     opencode/deepseek-v4-flash-free
Permissão:  read:allow, edit:deny, bash:allow, webfetch:deny

Descrição: Ativado quando sprint atrasa sem FCA ou timesheet zera.
           Classifica em 3 níveis: operacional / estrutural / externo.
           Define quem resolve com qual prazo.
```

### 6.12 `@executor-comite` — Briefing Automático do Comitê

```
Modelo:     opencode/deepseek-v4-flash-free
Permissão:  read:allow, edit:allow, bash:allow, webfetch:allow

Descrição: Gera o briefing do Comitê de P&EG automaticamente.
           Puxa OKRs, status de sprints, FCAs abertas, flags ativas
           e monta o documento pronto pra segunda-feira 8h.

Input:      "Gera briefing do comitê para segunda-feira"
Output:     Briefing completo em markdown + HTML

Agendamento: Ideal para cron: domingo 20h (já existe no MVP)
```

---

## 7. Fluxo de Orquestração Async

### Exemplo 1: Preparação do Comitê de Segunda

```
Domingo 20h (cron ou comando manual):

1. @executor-comite
   → "Prepara o comitê de segunda"
   → Invoca @analista-dados (paralelo, um por cliente ativo)

2. @analista-dados (múltiplas sessões filhas)
   → [Cliente A] Puxa dados: OKR, ROAS, sprint, NPS
   → [Cliente B] Puxa dados: OKR, ROAS, sprint, NPS
   → [Cliente C] Puxa dados: OKR, ROAS, sprint, NPS
   → Cada um retorna JSON estruturado

3. @revisor (em paralelo)
   → Valida cada JSON vs dados históricos
   → Sinaliza discrepâncias

4. @executor-comite consolida
   → Gera briefing markdown + HTML
   → Salva em docs/ ou envia por email

5. Usuário revisa na segunda 7h
   → Aprova ou ajusta antes do comitê 8h
```

### Exemplo 2: Detecção de Flag e Resposta

```
Quinta 7h (detector_flags.py ou @csm):

1. @csm-orquestrador
   → "Roda detecção de flags para todos os clientes"

2. @flag-roi (paralelo por cliente)
   → Verifica ROAS das últimas 2 semanas
   → Se negativo: classifica tipo, gera CHAS

3. @flag-churn (paralelo)
   → Verifica NPS + CSAT
   → Se queda: diagnostica percepção vs resultado

4. @flag-okr (paralelo)
   → Verifica progresso dos KRs
   → Se < 60%: diagnostica execução vs premissa

5. @flag-operacao (paralelo)
   → Verifica sprints ativas e timesheet
   → Se atraso sem FCA: classifica nível

6. @csm-orquestrador consolida
   → Prioriza flags por urgência
   → Envia briefing consolidado ao CSM humano
   → Aciona @revisor se flag for crítica
```

### Exemplo 3: Criação de Apresentação para Cliente

```
Usuário: @csm "Prepara QBR do cliente X para próxima semana"

1. @csm-orquestrador
   → Invoca @analista-dados para puxar o quarter inteiro

2. @analista-dados
   → Puxa: ROAS q/q, OKR progress, sprints entregues, NPS trend
   → Gera JSON com estrutura do QBR

3. @revisor
   → Valida dados e sugere ajustes se necessário

4. @gerar-ppt (após aprovação)
   → Gera apresentação completa com layout V4
   → Slidedeck: headline insights + data points + recomendações

5. Usuário recebe o deck pronto
   → Revisa, ajusta tom, envia pro cliente
```

---

## 8. Blocos de Execução

### Bloco 1 — Config + Agentes (dia 1, 2-3h)

| # | Ação | Arquivo | Modelo |
|---|---|---|---|
| 1.1 | Criar `opencode.json` no raiz | `opencode.json` | — |
| 1.2 | Criar `@gerar-pdf` | `.opencode/agents/gerar-pdf.md` | Gemini 2.5 Flash |
| 1.3 | Criar `@gerar-ppt` | `.opencode/agents/gerar-ppt.md` | Gemini 2.5 Flash |
| 1.4 | Criar `@gerar-html` | `.opencode/agents/gerar-html.md` | Gemini 2.5 Flash |
| 1.5 | Criar `@gerar-doc` | `.opencode/agents/gerar-doc.md` | Gemini 2.5 Flash |
| 1.6 | Criar `@analista-dados` | `.opencode/agents/analista-dados.md` | DeepSeek V4 Flash |
| 1.7 | Criar `@revisor` | `.opencode/agents/revisor.md` | DeepSeek V4 Flash |
| 1.8 | Criar `@csm-orquestrador` | `.opencode/agents/csm-orquestrador.md` | GPT-OSS 120B |
| 1.9 | Criar `@flag-roi` | `.opencode/agents/flag-roi.md` | DeepSeek V4 Flash |
| 1.10 | Criar `@flag-churn` | `.opencode/agents/flag-churn.md` | DeepSeek V4 Flash |
| 1.11 | Criar `@flag-okr` | `.opencode/agents/flag-okr.md` | DeepSeek V4 Flash |
| 1.12 | Criar `@flag-operacao` | `.opencode/agents/flag-operacao.md` | DeepSeek V4 Flash |
| 1.13 | Criar `@executor-comite` | `.opencode/agents/executor-comite.md` | DeepSeek V4 Flash |
| 1.14 | Criar command `agendar-rituais` | `.opencode/commands/agendar-rituais.md` | — |
| 1.15 | Espelhar globais | `~/.config/opencode/agents/` | — |
| 1.16 | Atualizar `~/.config/opencode/opencode.jsonc` | Global config | — |

### Bloco 2 — PDF Atualizado (dia 1, 1h)

| # | Ação | Entrega |
|---|---|---|
| 2.1 | Gerar `MVP_Peretto_Co_v3.pdf` | Documento com hierarquia de modelos, arquitetura de agentes, CSM transition |

### Bloco 3 — Automações (dia 1-2, 2h)

| # | Ação | Comando |
|---|---|---|
| 3.1 | Revisar e instalar dependências | `pip install -r setup/requirements.txt` |
| 3.2 | Configurar `.env` (Ekyte, Google, Meta) | `cp config/.env.template config/.env` |
| 3.3 | Autenticar Google OAuth | `python setup/auth_google.py` |
| 3.4 | Instalar crons | `python setup/install_cron.py` |
| 3.5 | Testar detector_flags manualmente | `python scripts/detector_flags.py --dry-run` |

### Bloco 4 — MCPs + Integrações (dia 2, 1-2h)

| # | Ação | Ferramenta |
|---|---|---|
| 4.1 | Configurar MCPs no `opencode.json` | `opencode mcp add` |
| 4.2 | Autenticar serviços OAuth | `opencode mcp auth <server>` |
| 4.3 | Validar tools MCP funcionando | Testar no TUI |

### Bloco 5 — Validação Final (dia 2, 1h)

| # | Ação | Critério |
|---|---|---|
| 5.1 | Testar `@analista-dados` + `@revisor` | 🟢 feedback loop funcional |
| 5.2 | Testar `@gerar-ppt` com dados reais | 🟢 apresentação gerada |
| 5.3 | Testar `@csm-orquestrador` setup | 🟢 setup de unidade guiado |
| 5.4 | Testar `@flag-roi` com dados mock | 🟢 diagnóstico correto |
| 5.5 | Salvar sessão | 🟢 `/session-save` |

---

## 9. Transição AM → CSM

Baseado na **Escola de CSM - Aula 1** e no documento **Implementando o Manual de Operação**:

### O que muda

| Hoje (Account Hero) | Novo (CSM Arquiteto) |
|---|---|
| Apaga incêndio operacional | Desenha estrutura que não precisa de bombeiro |
| Atende WhatsApp 22h | Filtra comunicação: time técnico blindado |
| Sobe campanha, faz criativo | Define objetivo de negócio, não o "como" |
| Reunião de 90min | Reunião de 30min com pauta fixa |
| Descobre problema quando cliente liga | Detector de flags roda antes do cliente sentir |
| Memoriza histórico | Vault Obsidian com memória persistente |

### Nova Divisão de Responsabilidades

```
┌────────────────────────────────────────────────────────┐
│                    CSM (@csm-orquestrador)               │
│  Foco: Resultado do cliente · ROI · Retenção · QBR     │
│  Acima do squad. Não executa — orquestra.               │
│  Ponto único de responsabilidade pelo resultado.         │
├────────────────────────────────────────────────────────┤
│                    COORDENADOR                           │
│  Foco: Operação · Qualidade técnica · Time Ops          │
│  Audita checklist · Facilita rituais · Protege o tambor │
├────────────────────────────────────────────────────────┤
│         AM · GT · Copy · Design (Time Técnico)          │
│  Foco: Execução · Entrega · O "Como" técnico            │
│  Blindados pelo CSM — não falam com cliente direto      │
└────────────────────────────────────────────────────────┘
```

### Timeline

```
Q2 2026 (Agora)    → AM ainda opera como generalista
                     CSM agente em paralelo (setup + flags)
                     Documentação da transição

Q3 2026 (Início)   → CSM assume como orquestrador
                     Coordenador assume operação técnica
                     AM vira executor no squad

Q4 2026            → CSM consolidado
                     Squad roda sem supervisão do CSM
                     CSM gerencia múltiplos squads
```

---

## 10. Resultado Esperado

### Métricas

| Métrica | Hoje | Com agentes | Como medir |
|---|---|---|---|
| Tempo de preparação do Comitê | 45-60min | < 5 min | Briefing gerado domingo 20h |
| Tempo para detectar desvio de KPI | 3-5 dias | < 24h | Detector de flags quinta 7h |
| Taxa de preenchimento de ata | ~60% | > 95% | Transcrição + agente de ata |
| Tempo de abertura de FCA | 1-3 dias | Automático | FCA gerada na detecção |
| Atualização de OKRs | Manual semanal | Quinta 8h automático | Script calcula com dados reais |
| Resposta a flag de churn | Semanas | 48-72h | CSM acionado automaticamente |
| Onboarding de pessoa nova | 1-2 semanas | < 2 dias | Claude Project + agente setup |

### O que não é mensurável mas é mais importante

- **Cada agente executando em paralelo** = você faz 5 coisas ao mesmo tempo
- **@revisor como contrapeso** = autonomia sem perder controle
- **Sessões assíncronas (sessão filha)** = você navega entre tarefas sem perder contexto
- **Sistema fica mais inteligente a cada semana**: vault registra → OUTPUTS.md calibra → agente melhora
- **Vantagem composta**: quanto mais tempo opera com agentes, maior a distância de quem não tem

---

> **Próximo passo**: Executar Bloco 1 (criar opencode.json + 12 agentes) em paralelo com Bloco 2 (PDF v3)
