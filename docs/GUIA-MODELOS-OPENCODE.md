# Guia de Modelos para OpenCode

## OpenCode Zen + OpenRouter — Como escolher o motor certo para seu agente

---

## 1. Entendendo a Arquitetura

Antes de falar de modelos, uma verdade fundamental:

**O modelo é o motor, não o carro.**

No OpenCode, você tem:

- **Agentes**: a inteligência arquitetural — skills, ferramentas, cadeia de raciocínio, plano de execução. Eles definem **como** o trabalho é feito.
- **Skills**: bibliotecas de know-how reutilizável — ROPRE de check-in, pipeline de SEO, roteiro de copy. Elas definem **o que** fazer.
- **Modelos (LLMs)**: o motor que processa as instruções dos agentes. Eles definem **a potência, velocidade e custo** da execução.

> Trocar o modelo não muda o agente. Trocar o modelo muda como rápido, quão fundo, e quanto custa cada operação.

Você pode usar o mesmo agente de check-in com um DeepSeek V4 Flash (rápido e barato) ou com um Claude Opus 4.7 (profundo e caro) — o roteiro, as perguntas, a estrutura de saída são idênticos. Só muda a qualidade do raciocínio e o tempo de resposta.

---

## 2. Os Dois Grandes Fornecedores

### OpenCode Zen

**O que é:** Curadoria oficial do time do OpenCode. Modelos testados e validados para funcionar com agentes de código. Eles mesmos benchmarkam cada combinação modelo + provedor.

**Vantagens:**
- Qualidade garantida — você sabe que o modelo foi testado
- Um API key só, um billing só
- Modelos hospedados nos EUA com política zero-retention
- Suporte a reasoning, tool calling, visão

**Desvantagens:**
- Catálogo menor que OpenRouter
- Planos pagos (exceto os free temporários)

**Modelos disponíveis por família:**

| Família | Modelos | API |
|---------|---------|-----|
| **OpenAI** | GPT 5.5, 5.4, 5.3 Codex, 5.2, 5.1, 5 | `responses` (SDK OpenAI) |
| **Anthropic** | Claude Opus 4.8/4.7/4.6/4.5/4.1, Sonnet 4.6/4.5/4, Haiku 4.5/3.5 | `messages` (SDK Anthropic) |
| **Google** | Gemini 3.1 Pro, Gemini 3 Flash | `models/gemini-*` (SDK Google) |
| **DeepSeek** | DeepSeek V4 Flash | `chat/completions` (OpenAI-compatível) |
| **Alibaba** | Qwen3.7 Max/Plus, Qwen3.6 Plus, Qwen3.5 Plus | `chat/completions` |
| **MiniMax** | MiniMax M2.7, M2.5 | `chat/completions` |
| **Z.AI (Zhipu)** | GLM 5.1, GLM 5 | `chat/completions` |
| **Moonshot** | Kimi K2.6, K2.5 | `chat/completions` |
| **xAI** | Grok Build 0.1 | `chat/completions` |
| **NVIDIA** | Nemotron 3 Ultra/Super (grátis) | `chat/completions` |
| **Xiaomi** | MiMo-V2 Pro/Omni (grátis) | `chat/completions` |
| **Tencent** | Hy3 Preview (grátis) | `chat/completions` |
| **StepFun** | Ling 2.6 Flash (grátis) | `chat/completions` |
| **OpenCode** | Big Pickle (modelo secreto, grátis) | `chat/completions` |

---

### OpenRouter

**O que é:** Um mercado de modelos. Roteia sua requisição para o provedor que está servindo aquele modelo naquele momento. Centenas de modelos de dezenas de provedores.

**Vantagens:**
- Catálogo gigantesco — centenas de modelos
- Free models reais sem cartão de crédito (rate limit: ~20 req/min, ~200/dia)
- Roteadores inteligentes (Pareto Router, Free Router)
- Pay-as-you-go para modelos pagos
- Suporte a reasoning, tool calling, multimodal

**Desvantagens:**
- Qualidade inconsistente — o mesmo modelo pode vir de provedores diferentes com performance diferente
- Modelos free podem aparecer e desaparecer
- Rate limits nos gratuitos

**Modelos notáveis no OpenRouter (junho/2026):**

**Grátis (sufixo `:free`):**
- `qwen/qwen3-coder:free` — melhor free para código (262K contexto)
- `deepseek/deepseek-v4-flash:free` — soberba geral (1M contexto)
- `deepseek/deepseek-r1:free` — raciocínio profundo
- `moonshotai/kimi-k2.6:free` — agente longa duração
- `meta-llama/llama-4-maverick:free` — 1M contexto, multimodal
- `nvidia/nemotron-3-ultra:free` — orquestração NVIDIA (1M)
- `google/gemini-2.0-flash:free` — multimodal (1M)
- `openai/gpt-oss-120b:free` — modelo aberto da OpenAI (131K)
- `poolside/laguna-xs.2:free` — dev-focused (128K)
- `mistralai/mistral-small-3.1-24b-instruct:free` — rápido equilibrado

**Pagos (melhores do mercado):**
- `anthropic/claude-opus-4.7` — 87.6% SWE-bench ($5/$25)
- `openai/gpt-5.5` — 88.7% SWE-bench ($5/$30)
- `google/gemini-3.1-pro-preview` — 80.6% SWE-bench ($2/$12)
- `deepseek/deepseek-v4-pro` — 80.6% SWE-bench ($0.44/$0.87)

---

## 3. Catálogo por Finalidade

### 3.1 Coding pesado — Agente multi-arquivo, refatoração

| Modelo | Onde | Custo | Contexto | SWE-bench |
|--------|------|:-----:|:--------:|:---------:|
| Claude Opus 4.7 | Zen / OR | $5/$25 | 1M | 87.6% |
| Claude Opus 4.8 | OR | $5/$25 | 1M | frontier |
| GPT 5.5 | Zen / OR | $5/$30 | 400K | 88.7% |
| GPT 5.4 Pro | Zen | $2.50/$15 | 200K | 78.2% |
| GPT 5.3 Codex | Zen | $2/$10 | 200K | — |
| Claude Sonnet 4.6 | Zen / OR | $3/$15 | 200K | ~79.6% |

**Free:** `qwen/qwen3-coder:free` (OR), `deepseek/deepseek-v4-flash:free` (OR/Zen)

### 3.2 Custo-benefício — 80% da qualidade por 10% do preço

| Modelo | Onde | Custo | Contexto | SWE-bench |
|--------|------|:-----:|:--------:|:---------:|
| DeepSeek V4 Pro | OR | $0.44/$0.87 | 1M | 80.6% |
| Gemini 3.1 Pro | Zen / OR | $2/$12 | 1M | 80.6% |
| Kimi K2.6 | Zen / OR | $0.75/$3.50 | 128K | 80.2% |
| MiniMax M2.5 | Zen | $0.30/$1.20 | 1M | 80.2% |
| MiMo-V2.5 Pro | OR | $1/$3 | 1M | ~78% |

### 3.3 Dia a dia — Rápido, barato, 90% das tarefas

| Modelo | Onde | Custo | Contexto | Ideal para |
|--------|------|:-----:|:--------:|------------|
| DeepSeek V4 Flash | Zen / OR | $0.14/$0.28 | 1M | Busca, comandos, templates, análises |
| Claude Haiku 4.5 | Zen / OR | $1/$5 | 200K | Subagente rápido, 73%+ SWE-bench |
| Gemini 3 Flash | Zen | ~$0.10/$0.40 | 200K | Chat, busca, estruturado |
| GLM 5.1 | Zen | $1/$3.20 | 205K | 8h+ autônomo contínuo |

### 3.4 Subagentes e paralelismo

| Modelo | Onde | Custo | Contexto | Ideal para |
|--------|------|:-----:|:--------:|------------|
| MiniMax M2.5 | Zen | $0.30/$1.20 | 1M | Subagente principal |
| Qwen3.5 Plus | Zen | $0.20/$1 | 262K | Draft e tarefas leves |
| Nemotron 3 Super | Zen/OR free | $0 | 1M | Orquestração |
| MiMo-V2 Omni | Zen free | $0 | 1M | Multimodal leve |

### 3.5 Raciocínio profundo

| Modelo | Onde | Custo | Ideal para |
|--------|------|:-----:|------------|
| DeepSeek R1 | OR free | $0 | Matemática, lógica, problemas complexos |
| Nemotron 3 Ultra | OR free | $0 | Multi-step reasoning, planejamento |
| Arcee Trinity Large Thinking | OR free | $0 | Reasoning puro |

### 3.6 Contexto gigante (1M+)

| Modelo | Onde | Custo | Contexto |
|--------|------|:-----:|:--------:|
| Claude Opus 4.7 | Zen / OR | $5/$25 | 1M |
| Gemini 3.1 Pro | Zen / OR | $2/$12 | 1M |
| DeepSeek V4 Flash/Pro | Zen / OR | $0.14/$0.28 | 1M |
| MiniMax M2.7 | Zen | $0.50/$3 | 1M |
| MiMo-V2.5 Pro | OR | $1/$3 | 1M |
| Nemotron 3 Ultra | OR free | $0 | 1M |
| Llama 4 Maverick | OR free | $0 | 1M |
| Gemini 2.0 Flash | OR free | $0 | 1M |

---

## 4. Guia Prático de Escolha

### 4.1 Como pensar

```
Tarefa simples (< 5 tools) → modelo rápido e barato
Tarefa complexa (multi-arquivo) → modelo frontier
Contexto enorme (> 200K) → modelo 1M
Pipeline de alto volume → custo por token domina
Orçamento zero → free models do OpenRouter + Zen free
```

### 4.2 Árvore de decisão

```
Precisa de código?
├── Tarefa rápida (1 arquivo) → DeepSeek V4 Flash
├── Refatoração multi-arquivo → Claude Sonnet 4.6 ou GPT-5.3 Codex
├── Projeto inteiro, agente autônomo → Claude Opus 4.7 ou GPT 5.5
└── Orçamento apertado → DeepSeek V4 Pro ou Gemini 3.1 Pro

Precisa de pesquisa/análise?
├── Documentos enormes → Gemini 3.1 Pro (1M) ou Llama 4 Maverick (free 1M)
├── Raciocínio matemático → DeepSeek R1 (free)
├── Dados estruturados → MiniMax M2.5 ou Qwen3.5 Plus
└── Web scraping + análise → Claude Haiku 4.5

Precisa de conteúdo criativo?
├── Copy/Landing → Claude Sonnet 4.6 ou GPT 5.4
├── Draft rápido → DeepSeek V4 Flash
└── Refino/edição → Claude Haiku 4.5

É subagente?
├── Leve, alta frequência → MiniMax M2.5 ou DeepSeek V4 Flash
├── Orquestração → Nemotron 3 Ultra (free)
└── Tarefa isolada simples → Qwen3.5 Plus
```

### 4.3 Estratégia de camadas (recomendada)

```
FREE TIER (custo zero)
├── opencode/deepseek-v4-flash-free — principal dia a dia (Zen)
├── opencode/minimax-m2.5-free — subagente (Zen)
├── openrouter/deepseek/deepseek-v4-flash:free — fallback (OR)
├── openrouter/deepseek/deepseek-r1:free — reasoning pesado (OR)
└── openrouter/nvidia/nemotron-3-ultra:free — orquestração (OR)

PAY-AS-YOU-GO (quando precisar de potência)
├── Claude Sonnet 4.6 (Zen: $3/$15) — coding médio-pesado
├── Gemini 3.1 Pro (Zen: $2/$12) — contexto 1M, custo-benefício
├── Claude Opus 4.7 (Zen: $5/$25) — o ápice para agente
└── GPT-5.3 Codex (Zen: $2/$10) — coding especializado OpenAI

REGRA: comece sempre pelo mais barato que resolve. Só suba de camada
quando o modelo atual bater no teto de qualidade.
```

---

## 5. Configuração Prática no OpenCode

### 5.1 Usando apenas Zen (recomendado para começar)

```jsonc
// opencode.json
{
  "model": "opencode/deepseek-v4-flash-free",
  "small_model": "opencode/minimax-m2.5-free"
}
```

### 5.2 Adicionando OpenRouter como segundo provider

```jsonc
// opencode.json
{
  "model": "opencode/deepseek-v4-flash-free",
  "small_model": "opencode/minimax-m2.5-free",
  "provider": {
    "openrouter": {
      "apiKey": "sk-or-v1-xxxxxxxxxxxxxxxx"
    }
  }
}
```

Depois no TUI: `/model openrouter/deepseek/deepseek-r1:free` para trocar na hora.

### 5.3 Hierarquia de agentes com modelos diferentes

```jsonc
{
  "agent": {
    "build": {
      "model": "opencode/claude-sonnet-4-6",     // código pesado
      "mode": "primary"
    },
    "plan": {
      "model": "opencode/deepseek-v4-flash-free", // planejamento leve
      "mode": "primary"
    }
  }
}
```

### 5.4 Conectando OpenRouter

1. Crie conta em openrouter.ai (sem cartão de crédito)
2. Vá em Settings → Keys → Create Key
3. Copie a chave (começa com `sk-or-`)
4. No OpenCode TUI: `/connect` → selecione OpenRouter → cole a chave
5. `/models` para ver a lista completa

---

## 6. Tabela Rápida de Modelos Free

### OpenCode Zen (grátis por período limitado)

| ID | Contexto | Especialidade |
|----|:--------:|---------------|
| `opencode/deepseek-v4-flash-free` | 1M | Melhor geral: rápido, forte, barato |
| `opencode/minimax-m2.5-free` | 1M | Subagente, 80% SWE-bench |
| `opencode/nemotron-3-super-free` | 1M | Orquestração NVIDIA |
| `opencode/nemotron-3-ultra-free` | 1M | Mesma familia, mais capacidade |
| `opencode/hy3-preview-free` | 200K | Tencent, agentic workflows |
| `opencode/mimo-v2-pro-free` | 1M | Xiaomi, agente multimodal |
| `opencode/mimo-v2-omni-free` | 1M | Xiaomi, versão omnimodal |
| `opencode/qwen3.6-plus-free` | 262K | Alibaba, draft/análise |
| `opencode/ling-2.6-flash-free` | 128K | StepFun, rápido |
| `opencode/big-pickle` | 200K | Modelo secreto OpenCode |

### OpenRouter (grátis, sufixo `:free`)

| ID | Contexto | Especialidade |
|----|:--------:|---------------|
| `qwen/qwen3-coder:free` | 262K | **Melhor free para código** |
| `moonshotai/kimi-k2.6:free` | 128K | Agente longa duração |
| `deepseek/deepseek-v4-flash:free` | 1M | Soberba geral |
| `deepseek/deepseek-r1:free` | 128K | Raciocínio profundo |
| `nvidia/nemotron-3-ultra:free` | 1M | Orquestração multi-step |
| `meta-llama/llama-4-maverick:free` | 1M | Documentos enormes, multimodal |
| `google/gemini-2.0-flash:free` | 1M | Multimodal rápido |
| `openai/gpt-oss-120b:free` | 131K | Modelo aberto OpenAI (Apache 2.0) |
| `poolside/laguna-xs.2:free` | 128K | Dev-focused |
| `mistralai/mistral-small-3.1-24b-instruct:free` | 128K | Equilibrado rápido |
| `google/gemma-4-31b-it:free` | 128K | Google open |
| `arcee-ai/trinity-large-thinking:free` | 128K | Reasoning puro |
| `meta-llama/llama-3.3-70b-instruct:free` | 128K | All-purpose sólido |

### Roteador free do OpenRouter

Use `openrouter/free` como model ID — ele escolhe automaticamente o melhor modelo free disponível que suporta as features que sua requisição precisa (tool calling, imagem, etc).

---

## 7. Glossário

| Termo | Significado |
|-------|-------------|
| **Zen** | OpenCode Zen — curadoria oficial de modelos testados |
| **OR** | OpenRouter — mercado de modelos |
| **SWE-bench** | Benchmark de coding realista (GitHub issues reais) |
| **MoE** | Mixture of Experts — arquitetura que ativa só parte dos parâmetros |
| **Contexto** | Quantos tokens o modelo consegue "lembrar" de uma vez |
| **Tool calling** | Capacidade do modelo de chamar ferramentas (bash, editar arquivos, etc) |
| **Reasoning** | Raciocínio encadeado (chain-of-thought) |
| **`:free`** | Sufixo do OpenRouter para versão gratuita |
| **Rate limit** | Limite de requisições por minuto/dia |

---

## 8. Resumo Final

```
Arquitetura (sempre igual) → Agentes + Skills
Motor (você escolhe)     → Modelo LLM via Zen ou OpenRouter

Zen  = segurança, qualidade testada, curadoria
OR   = variedade, free models, mercado aberto

Regra de ouro:
  Use o modelo mais barato que entrega o resultado esperado.
  Só suba para modelos mais caros quando o atual não der conta.
```

---

*Documento gerado em junho/2026. Modelos e preços mudam com frequência. Para lista ao vivo: `https://opencode.ai/zen/v1/models` (Zen) e `https://openrouter.ai/models` (OR).*
