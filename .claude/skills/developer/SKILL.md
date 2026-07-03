---
name: developer
description: Portal de skills pessoais do desenvolvedor. Use /developer para acessar ferramentas técnicas (ML/LLM, OpenCode tooling, Supabase, testes, automação pessoal). Esse comando carrega skills de .claude/skills/privado/ que não ficam visíveis no dia a dia.
---

# developer — Portal de Skills Pessoais

Este portal ativa as skills técnicas e pessoais que ficam em `privado/` — fora da lista padrão para não poluir o dia a dia dos usuários comuns.

## Skills disponíveis

### ML/LLM
- `blip-2-vision-language` — Visão e linguagem multimodal
- `evaluating-llms-harness` — Benchmarks acadêmicos (MMLU, HumanEval, GSM8K)
- `fine-tuning-with-trl` — RLHF com SFT, DPO, PPO, GRPO
- `hqq-quantization` — Quantização 4/3/2-bit sem dados de calibração
- `quantizing-models-bitsandbytes` — Quantização 8/4-bit com bitsandbytes
- `simpo-training` — Preference optimization sem modelo de referência

### OpenCode Tooling
- `add-opencode-model` — Adicionar modelos no OpenCode
- `codeagent` — Multi-backend code tasks (Codex, Claude, Gemini, OpenCode)
- `create-opencode-plugin` — Criar plugins com SDK @opencode-ai/plugin
- `creating-opencode-agents` — Criar agentes OpenCode
- `flow-next-opencode-interview` — Entrevistar requisitos de epic/task
- `flow-next-opencode-plan` — Criar build plans estruturados
- `flow-next-opencode-work` — Executar épicos com git workflow
- `opend` — Fetch reply do OpenCode storage
- `oping` — Testar conectividade OpenCode
- `plugin-dev` — Extensões Claude Code + OpenCode

### Infraestrutura pessoal
- `agents-md-generator` — Gerar AGENTS.md hierárquicos
- `all-plan` — Planejamento colaborativo multi-CLI
- `claude-automation-recommender` — Recomendar automações Claude
- `computer-use-agents` — Agentes que interagem com tela
- `git-advanced-workflows` — Git avançado (rebase, bisect, worktrees)
- `implementing-agent-modes` — Modos de agente PostHog
- `implicit-decision-capture` — Captura de decisões implícitas
- `m12-lifecycle` — Resource lifecycles (Rust)
- `new-agent-creation` — Templates de agentes Unite-Hub
- `openrouter-fallback-config` — Fallback chains para LLM
- `perry-workspaces` — Docker workspaces isolados
- `station` — CLI Station para orquestração
- `v3-deep-integration` — Deep agentic-flow integration
- `v3-mcp-optimization` — MCP server optimization

### Supabase
- `supabase` — Tarefas com Supabase (DB, Auth, Edge Functions, etc.)
- `supabase-postgres-best-practices` — Boas práticas Postgres

### Testes
- `temporal-python-testing` — Testes de Temporal workflows com pytest
- `testing-python` — Testes Python com pytest

### OpenCode skills pessoais (`.opencode/skills/privado/`)
- `ah`, `ah-*` — Sistema de conhecimento pessoal Ah
- `defuddle` — Extrair markdown limpo de páginas web
- `json-canvas` — Criar/editar JSON Canvas (.canvas)
- `obsidian-bases`, `obsidian-cli`, `obsidian-markdown` — Integração Obsidian

## Como usar

```bash
# Carregar este portal
/developer

# Ou carregar uma skill específica diretamente
skill("supabase")
skill("fine-tuning-with-trl")
```

As skills em `privado/` não aparecem na lista padrão de skills disponíveis. Use este portal como index.
