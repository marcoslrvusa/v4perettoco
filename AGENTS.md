# Hub de Agentes V4

Repositório central de skills e agentes de IA da V4 Company. Usado como base de trabalho para OpenCode e Claude Code.

## Estrutura

- `.opencode/agents/` — definições dos agentes OpenCode
- `.agents/skills/` — skills para OpenCode
- `.claude/skills/` — skills para Claude Code (espelhadas)
- `docs/` — documentação fundacional (PRINCÍPIOS-V4, brand reference)

## Skills

Skills compartilhadas seguem o padrão `{prefixo}-{nome}`:

- **Papéis** (skills que entregam trabalho final): `geral-*`, `gt-*`, `designer-*`, `copy-*`, `account-*`, `coord-*`
- **Fontes** (skills que puxam dados de integrações): `v4mos-*`, `google-*`, `ga4-*`, `meta-*`, `hubspot-*`, `kommo-*`, `shopify-*`, `tray-*`

Consulte `REGISTRY.md` para o catálogo completo.

## Setup

```bash
# Instalar OpenCode
curl -fsSL https://opencode.ai/install.sh | sh

# Clonar este repositório
git clone https://github.com/PerettoCo/hub-agentes.git
cd hub-agentes

# Configurar variáveis de ambiente
cp .env.example .env
# Preencha GEMINI_API_KEY e OPENROUTER_API_KEY no .env

# Iniciar
opencode
```

## Regras

- Responda sempre em português brasileiro
- Duplo-write obrigatório: skills criadas/editadas devem existir em `.agents/skills/` E `.claude/skills/`
- Não invente dados. Se não tem a informação na KB, diga que não tem.
