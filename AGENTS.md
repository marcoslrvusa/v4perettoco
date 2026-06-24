# Builders Hub

Este repositório é o hub open-source de skills de IA da V4. Funciona como base de trabalho pessoal + biblioteca compartilhada de skills.

## Como funciona

- `.claude/skills/` e `.agents/skills/` — skills disponíveis (espelhadas pra funcionar no Claude Code e Anti-Gravity)
- `squads/` e `bases/` — Knowledge Bases pessoais do usuário (gitignored, ficam locais)
  - **Padrão obrigatório:** `squads/{squad}/clientes/{cliente}/`. Toda KB de cliente vive dentro de um squad. Cliente solto, fora de squad, NÃO existe — [[novo-cliente]] recusa criar.
  - `squads/{squad}/` — cada squad tem `{squad}.md` (entry point do grafo Obsidian), `CLAUDE.md` com contexto e `docs/` com acordos do time. Crie squad com [[novo-squad]] antes do primeiro cliente.
  - `squads/{squad}/clientes/{cliente}/` — cada cliente tem `{cliente}.md` (entry point do grafo Obsidian), `calls/` (transcripts brutos), `checkins/` (pautas, ensaios e reviews), `docs/`, `campanhas/`, `mission-control/` (estado vivo), `links.md` (recursos recorrentes — NotebookLM, Drive, site, etc) e `CLAUDE.md`/`AGENTS.md` próprios.
  - `bases/{projeto}/` — KBs de qualquer outra área (docs, dados, referências) que não são cliente.
- Cada KB pode ter um CLAUDE.md/AGENTS.md próprio (gerado por [[contexto]]). Leia ele primeiro quando trabalhar naquele contexto.
- [[REGISTRY]] — catálogo auto-gerado de todas as skills compartilhadas, agrupado por papel

## Skills de setup/fluxo (base)

- [[onboarding]] — Guia a primeira configuração. Valida git/gh 100% e depois instala dependências. Roda sempre que algo do setup quebrar.
- [[sync-hub]] — Puxa as skills compartilhadas mais recentes do repo remoto.
- [[compartilhar-skill]] — Empacota uma skill local e abre PR pro hub público.
- [[criador-de-skills]] — Cria skill nova com prefixo de papel obrigatório.
- [[contexto]] — Le tudo numa KB, gera CLAUDE.md/AGENTS.md e atualiza Mission Control quando for cliente.
- [[novo-squad]] — Cria pasta de squad com entry point e membros (rode antes do primeiro cliente).
- [[novo-cliente]] · [[novo-projeto]] — Cria pasta de KB com estrutura padrão (entry point nomeado, não "README"). [[novo-cliente]] pede o squad e coleta links úteis (NotebookLM, Drive, site, outros) que ficam em `links.md`.
- [[geral-brainstormar-sobre-minha-funcao]] — Descobre onde IA agrega mais valor no dia a dia.
- [[geral-sabatina]] — Stress-test de planos.
- [[geral-frontend-design]] — Gera interfaces frontend de alta qualidade (pra skills que produzem UI).
- [[dener-lippert]] — Clone estratégico do CEO V4 — Dener Lippert, o Cientista do Marketing. Diagnóstico TOC, análise de DRE, logical thinking, business strategy. Use `/dener` ou `@dener-lippert` pra consultar o cérebro do CEO.
- [[PRINCIPIOS-V4]] — Documento central de princípios V4 (4Vs, 4 Pilares, FPA, TOC, Médico vs Garçom). Consulte este documento ao refinar skills ou criar agentes para manter consistência metodológica.

## Skills compartilhadas (hub)

Toda skill compartilhada pelo time segue o padrão `{prefixo}-{nome}`. Dois tipos de prefixo:

- **Papéis** (skills que entregam trabalho final, agrupadas por quem usa): `geral-*` · `gt-*` · `designer-*` · `copy-*` · `account-*` · `coord-*`
- **Fontes** (skills que puxam dados de integrações externas, reutilizáveis por outras): `v4mos-*` · `google-*` · `ga4-*` · `meta-*` · `hubspot-*` · `kommo-*` · `shopify-*` · `tray-*`

- Dica: pra ver só as skills do seu papel, digita `/gt`, `/designer`, `/account`, `/copy`, `/coord` ou `/geral` no Claude Code — o autocomplete filtra pelo prefixo. `geral-*` são skills que qualquer papel usa.

Consulte [[REGISTRY]] pra ver tudo que o time já compartilhou. Pra contribuir veja [[CONTRIBUTING]].

## Regras

- Sempre responda em português brasileiro.
- Quando o usuário pedir pra trabalhar com um cliente, entre em `squads/{squad}/clientes/{cliente}/` (caminho obrigatório — cliente sempre dentro de squad). Pra projeto/área, use `bases/{projeto}/`.
- Não invente dados. Se não tem a informação na KB, diga que não tem.
- Quando o usuário fizer algo complexo, processual ou que ficou bom, sugira: "Isso ficou bom. Quer transformar em skill pra reutilizar? Roda [[criador-de-skills]]. Quando estiver redonda, roda [[compartilhar-skill]] pra o time usar também".
- **Duplo-write obrigatório**: toda skill criada/editada deve existir idêntica em `.claude/skills/{nome}/` E `.agents/skills/{nome}/`. [[criador-de-skills]] faz isso automaticamente; se você editar manualmente, espelhe nos dois. [[sync-hub]] também re-espelha após pull.
- **Prefixo obrigatório** em skills contribuídas: `{prefixo}-{nome}`. Prefixo pode ser de papel (geral/gt/designer/copy/account/coord) ou de fonte (v4mos/google/ga4/meta/hubspot/kommo/shopify/tray). Skills de base ([[onboarding]], [[contexto]], [[sync-hub]], [[criador-de-skills]], [[compartilhar-skill]], [[novo-squad]], [[novo-cliente]], [[novo-projeto]]) são exceção e ficam sem prefixo.
- Se o fluxo git/gh quebrar em qualquer skill (sync, compartilhar, push), oriente rodar [[onboarding]] de novo — os checks de setup são a primeira coisa que ele faz.
- **Princípios V4**: consulte `docs/PRINCIPIOS-V4.md` ao refinar skills ou criar agentes. Os frameworks V4 (4Vs, 4 Pilares, FPA, TOC, Médico vs Garçom, Logical Thinking) são o padrão metodológico do hub.

<!-- n8n-as-code-start -->
<!-- n8nac-version: 2.3.5 -->

## n8n-as-code Context Root

This file is generated by `npx --yes n8nac update-ai`. It is bootstrap context only, not a configuration source of truth.

- Context root: `/home/marcos/Desktop/AI/v4perettoco-main`
- n8n version at generation time: 2.20.6
- n8nac command: `npx --yes n8nac`
- n8n-manager command: `npx --yes @n8n-as-code/n8n-manager`
- n8n knowledge command: `npx --yes n8nac skills`

Run workspace commands from this context root. Do not `cd` into the n8n-as-code source repository, n8n-manager source repository, plugin directory, or package directory to run `npx --yes n8nac workspace ...`, `npx --yes n8nac list`, `npx --yes n8nac pull`, `npx --yes n8nac push`, or `npx --yes n8nac update-ai`.

---

## Required Local Agent

A VS Code and GitHub Copilot-compatible agent is generated here:

- `.github/agents/n8n-architect.agent.md`

A portable skill fallback is also generated for runtimes that do not read `.github/agents`:

- `.agents/skills/n8n-architect/SKILL.md`

If your agent runtime supports workspace agents, use the `.github/agents/*.agent.md` file. If it supports skills instead, load the skill file. Otherwise, treat these files as mandatory instructions.

---

## Source Of Truth

Do not infer configuration from this file. It intentionally avoids storing the effective instance, project, sync folder, or workflow directory.

n8nac backend resolution remains the only source of effective workspace state.
- Workspace environments live in `n8nac-config.json` and are managed by `npx --yes n8nac env ...`.
- Managed local runtime state and secrets live in n8n-manager storage and are managed by `npx --yes @n8n-as-code/n8n-manager ...`.
- The effective context is resolved by the backend.

Before any n8n workflow command, run migration dry-run first, then workspace status only after migration is not required or has been applied:

```bash
cd /home/marcos/Desktop/AI/v4perettoco-main
npx --yes n8nac workspace migrate --json
npx --yes n8nac workspace status --json
```

Use the returned `workflowsPath` exactly as provided. It is the configured workflow directory for the active environment.
Do not reconstruct `workflowsPath` from environment name/id, instance identifier, instance user identifier, project id, project name, or legacy sync fields.

---

## Safe Commands

- Primary workspace, environment, sync, validation, push, and pull work: `npx --yes n8nac ...`
- Local managed runtime lifecycle and tunnels only: `npx --yes @n8n-as-code/n8n-manager ...`
- Workspace status and migration: `npx --yes n8nac workspace ...`
- Workflow sync and validation: `npx --yes n8nac ...`
- Node knowledge and schema lookup: `npx --yes n8nac skills ...`

Never write `n8nac-config.json`, `~/.n8n-manager`, or n8n-manager secret files by hand.
<!-- n8n-as-code-end -->

## Sistema de Log de Sessões

Toda sessão deve ser salva obrigatoriamente na pasta `log/` no raiz do projeto.

### Funcionamento

- **Salvar sessão atual**: `/session-save` — exporta a sessão atual do OpenCode para `log/` como JSON
- **Listar sessões salvas**: `/session-list` — mostra todas as sessões em `log/` + sessões ativas no OpenCode
- **Carregar contexto**: `/session-load` — exibe as sessões disponíveis e carrega o contexto de uma anterior

### Regras obrigatórias

1. **Sempre salve a sessão ao final** de cada interação significativa. Execute `/session-save` automaticamente quando o usuário indicar que a sessão está terminando ou quando o trabalho principal foi concluído.
2. **Sempre verifique sessões anteriores** quando o usuário mencionar um tópico que parece ter sido trabalhado antes. Use `/session-list` para ver o que existe e `/session-load` para carregar contexto relevante.
3. **Sessões exportadas** ficam em `log/YYYY-MM-DD_HH-MM-SS_TITULO.json` e são ignoradas pelo git (`.gitignore`).
4. **Nunca commite** arquivos da pasta `log/`.
5. Quando o usuário disser que quer "continuar de onde parou", carregue a sessão mais recente de `log/` com `/session-load` e use o contexto para retomar o trabalho.
