# Relatório — Hub de Agentes OpenCode

**Data:** 2026-07-17 10:03 BRT  
**Servidor:** root@2.25.148.214 (Dokploy + Traefik)  
**URL principal:** https://ia.fvmarketing.com.br (login) → redireciona para subdomínios por usuário

---

## 1. Estado Atual da Infraestrutura

### ✅ O que ESTÁ funcionando

| Componente | Status |
|---|---|
| **6 containers OpenCode** (marcos, fhelipe, paolo, lucasnunes, bruno, italo) | `Up 10h (healthy)` |
| **Gateway Nginx** | `Up 11h (healthy)` |
| **Auth server** (Express + Supabase sync) | `Up 11h (healthy)`, 6 users sincronizados |
| **LiteLLM** | `Up 4 days`, com chaves virtuais por usuário |
| **Traefik** | `Up 35h` |
| **Git clone do workspace** | ✅ Todos os 6 containers têm `/workspace` clonado (`infra-v2-clean`, commit `03efc90`) |
| **35 agentes custom** no `opencode.json` | ✅ Registrados e servidos via proxy |
| **97 skills** em `.agents/skills/` | ✅ Presentes no workspace, descrições em PT |
| **Proxy `/api/agent`** | ✅ Retorna 200, ~132KB JSON com agentes nativos + custom |
| **GITHUB_TOKEN** | ✅ Configurado (`ghp_Bzyo0zq...`) — entrypoint clona com sucesso |

### ❌ Problema 1: Versão OpenCode atualiza para 1.18.3 (v2 UI)

O `entrypoint.sh` tem esta linha:

```bash
npm install -g opencode-ai@latest 2>&1 | tail -1
```

Isso **sempre instala a versão mais recente** (hoje `1.18.3`). Na sessão anterior (16/07), vocês tinham fixado em `1.17.20` — mas o entrypoint atual **NÃO fixa a versão**. O `npm install -g opencode-ai@latest` está instalando a v2.

**Consequência na v2 (1.18.3):**
- `build` e `plan` viram **abas de MODO** na UI, e **não aparecem mais no seletor/@**
- Os subagentes custom (35 agentes do `opencode.json`) **não aparecem via `@`** na v2 — a v2 espera agentes definidos em arquivos `.md` no diretório `.agents/` (que estão lá como untracked files, mas a v2 carrega de forma diferente)

### ❌ Problema 2: Agentes não invocáveis via `@` na v2

Na v2 (1.18.3), o formato mudou:
- Agentes definidos no `opencode.json` com `"mode": "subagent"` **não são listados como invocáveis via `@`** na UI v2
- A v2 carrega agentes de `.agents/*.md` como agent definitions, mas os trata diferentemente
- O proxy injeta os agentes custom no response de `/api/agent`, mas a UI v2 não os exibe no autocomplete de `@`

### ⚠️ Problema 3: Workspace clona mas sessão não inicia

O workspace está clonado corretamente (commit `03efc90`, branch `infra-v2-clean`). Os logs mostram `[entrypoint] Workspace ready`. **Mas** o que você reporta como "não clona a pasta workspace" pode ser um problema de UI — na v2, ao abrir a interface, ela pode não estar mostrando o workspace como "ativo" para iniciar uma sessão, possivelmente porque:

1. O `opencode.json` **não tem a chave `"workspace"`** (foi removida no commit anterior por invalidar o schema da 1.17.20)
2. Na v2, sem `"workspace"` explícito, o OpenCode pode mostrar opções conflitantes (como `/` vs `/workspace`)

---

## 2. Configurações Atuais

### Entrypoint (mesmo no host e no container)

```
infra/entrypoint.sh → monta em /entrypoint.sh:ro
```

- Clona `PerettoCo/hub-agentes` branch `infra-v2-clean` usando `GITHUB_TOKEN`
- Copia `opencode.json` da config para `~/.config/opencode/`  
- Copia agents `.md` de `infra/agents/` para `~/.config/opencode/agents/`
- Symlink skills de `.agents/skills/` para `~/.config/opencode/skills`
- **`npm install -g opencode-ai@latest`** ← PROBLEMA: não fixa versão
- Inicia opencode em `:4097`, proxy em `:4096`

### `opencode.json` (config montado como read-only)

```json
{
  "model": "opencode/deepseek-v4-flash-free",
  "small_model": "opencode/deepseek-v4-flash-free",
  "provider": {
    "opencode": {
      "options": {
        "apiKey": "{env:OPENAI_API_KEY}",
        "baseURL": "{env:OPENAI_BASE_URL}"
      }
    }
  },
  "agent": { /* 35 agentes com mode: subagent */ },
  "permission": { "edit": "allow", "bash": "allow", ... }
}
```

> [!WARNING]
> O `provider` no JSON está como `"opencode"` e os models como `opencode/deepseek-v4-flash-free`. Porém a `OPENAI_BASE_URL` aponta para `http://litellm:4000/v1`. Confirme que o LiteLLM tem esses modelos registrados com o prefixo correto.

### Docker Compose

- 6 containers OpenCode (build do `infra/Dockerfile.opencode`)
- 1 gateway (Nginx com auth_request para cookie de sessão)
- 1 auth (Express + Supabase sync)
- Rede: `dokploy-network` (compartilhada com LiteLLM)

---

## 3. Diagnóstico dos 2 Problemas Reportados

### Problema A: "Não clona a pasta workspace"

**Na verdade, o workspace está clonado.** Todos os 6 containers mostram `/workspace` com o repo completo (`AGENTS.md`, `infra/`, `.agents/skills/`, etc). Os logs confirmam `[entrypoint] Workspace ready (commit: 03efc90)`.

O que pode estar acontecendo é que **a UI v2 não mostra o workspace como sessão ativa** — você abre o browser e não vê como iniciar uma conversa. Isso pode ser causado pela ausência da chave `"workspace"` no `opencode.json` ou por um bug da v2 ao inicializar com `HOME=/workspace`.

### Problema B: "Não consigo invocar agentes/subagentes via @"

**Confirmado como consequência da v2 (1.18.3).** Na v1 (1.17.20):
- `build` e `plan` apareciam no **seletor** de agente e via `@`
- Os 35 custom agents apareciam via `@`

Na v2 (1.18.3):
- `build` e `plan` viraram **modos** (abas), não invocáveis por `@`
- Custom agents definidos no JSON **não são expostos via `@`** na UI v2
- Skills com `/` continuam funcionando porque usam um endpoint diferente (`/api/skill`)

---

## 4. Soluções Propostas

### Opção A: Fixar versão em 1.17.20 (restaurar o que funcionava)

Alterar **uma linha** no `entrypoint.sh`:

```diff
-npm install -g opencode-ai@latest 2>&1 | tail -1
+npm install -g opencode-ai@1.17.20 2>&1 | tail -1
```

**Prós:** Tudo volta a funcionar como na sessão de 16/07 (agentes via `@`, build/plan no seletor)  
**Contras:** Fica preso numa versão antiga

### Opção B: Adaptar para v2 (1.18.3)

1. Manter `opencode-ai@latest`
2. Converter os 35 agentes de JSON para `.md` files no formato que a v2 espera (os `.md` já existem em `.agents/` e `infra/agents/`)
3. Aceitar que `build` e `plan` são modos, não invocáveis por `@`
4. Testar se a v2 reconhece os `.md` agents como invocáveis por `@`

**Prós:** Fica atualizado  
**Contras:** Mais trabalho, e o comportamento do `@` na v2 pode continuar diferente

### Opção C: Fixar em uma versão intermediária testada

Testar se existe uma versão entre 1.17.20 e 1.18.3 que mantém o comportamento do `@` enquanto recebe bugfixes.

---

## 5. Ação Mínima Recomendada

> [!IMPORTANT]
> **A correção mais rápida é a Opção A:** editar o `entrypoint.sh` no host do servidor para fixar `opencode-ai@1.17.20` e reiniciar os containers. São 2 comandos SSH.

Precisa da sua decisão antes de eu tocar no servidor.
