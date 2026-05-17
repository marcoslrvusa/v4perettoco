# Estruturação de Markdowns para o Grafo do Obsidian

## Builders Hub — V4 Company

> Documento de racional e execução para replicação em outras unidades.
> Autor: gerado em sessão com IA em 12/05/2026.

---

## 1. Contexto e Objetivo

O Builders Hub é um vault do Obsidian com **230 arquivos markdown** distribuídos em skills, squads, clientes, projetos e módulos. O Obsidian já está configurado como vault (`.obsidian/` com graph, backlink e outgoing-link ativos), mas **nenhum arquivo usa wikilinks (`[[link]]`)** — o grafo está vazio, zero arestas.

**Objetivo:** Adicionar links inteligentes entre os markdowns para que o grafo do Obsidian mostre conexões reais por cluster — skills relacionadas entre si, clientes conectados a seus squads, módulos conectados a seus contextos — sem quebrar nenhum fluxo existente (skills, parsers, CI/CD).

---

## 2. Diagnóstico

| Item | Achado |
|------|--------|
| Total de arquivos .md | 230 |
| Wikilinks `[[ ]]` existentes | **Zero** |
| Links markdown comuns | **7** (apenas entre README, REGISTRY, CONTRIBUTING) |
| Nome dos arquivos de skill | `SKILL.md` — `[[skill-name]]` não resolve sem aliases |
| Skills em `.claude` vs `.agents` | 58 pares — **57 idênticos byte-a-byte**, 1 sem SKILL.md |
| Arquivos pessoais (squad/cliente) | Gitignored, sem links entre si |
| Frontmatter atual | `name`, `description`, `area`, `author`, `version` — sem `aliases` ou `tags` |

---

## 3. Design do Grafo

O grafo se organiza em **clusters** (bolhas interconectadas), não em uma estrela central.

### 3.1. Cluster Skills (por área funcional)

Cada skill linka para skills relacionadas. Exemplo real do cluster Account:

```
account-handoff ──→ contexto ──→ account-checkin-roleplay ──→ account-checkin-review
                  │                                          │
                  │                                          └──→ v4mos-dados-meta-ads
                  └──→ account-pesquisa-profunda-cliente
```

Exemplo do cluster Funil CRO:

```
seo-audit ──→ content-strategy ──→ copywriting ──→ page-cro
schema-markup ──→ ai-seo
signup-flow-cro ──→ onboarding-cro
paid-ads ──→ ad-creative ──→ copywriting
```

### 3.2. Cluster Squad → Clientes

```
squad/prime ──→ gset/README ──→ mission-control/* (5 arquivos)
                              ──→ campanhas/* (6 arquivos)
                              ──→ docs/* (2 arquivos)

squad/prime ──→ atlas-copco/README ──→ mission-control/* (5 arquivos)
                                     ──→ docs/* (2 arquivos)
                                     ──→ historico/
```

Cada cliente vira uma **constelação** com seu README no centro e sub-arquivos ao redor.

### 3.3. Cluster csm-hub

```
csm-hub/README ──→ csm-principal ──→ CONTEXT → TRIGGERS → OUTPUTS
                 ──→ flag-churn   ──→ CONTEXT → TRIGGERS → OUTPUTS
                 ──→ flag-okr     ──→ CONTEXT → TRIGGERS → OUTPUTS
                 ──→ flag-roi     ──→ CONTEXT → TRIGGERS → OUTPUTS
                 ──→ flag-operacao ──→ CONTEXT → TRIGGERS → OUTPUTS
```

### 3.4. Cluster Raiz

```
README ──→ REGISTRY ──→ CONTRIBUTING
AGENTS ──→ CONTRIBUTING
```

(Sem links diretos de README para cada skill — evita o padrão "estrela" que polui o grafo.)

---

## 4. Esquema de Links

| Tipo | Direção | Exemplo |
|------|---------|---------|
| Skill → skill relacionada | Bidirecional | `[[page-cro]]` dentro de `ab-test-setup/SKILL.md` |
| Squad → cliente | Squad → Cliente | `[[squads/prime/clientes/gset/README\|GSET]]` |
| Cliente → sub-arquivos | Cliente → mission-control, campanhas, docs | `[[gset-okr-quarter]]`, `[[gset-estrategia-2026]]` |
| Módulo csm → seus arquivos | Módulo → CONTEXT, TRIGGERS, OUTPUTS | `[[csm-principal-context]]` |
| Skill → suas referências | Skill → references/ | `[[references/test-templates]]` |
| Root → docs principais | README → REGISTRY, CONTRIBUTING | `[[REGISTRY]]`, `[[CONTRIBUTING]]` |

---

## 5. Sistema de Tags (Cores no Grafo)

Tags adicionadas ao frontmatter para colorir o grafo por categoria:

| Tag | Cor | Aplica-se a |
|-----|-----|-------------|
| `skill` | — | Todos os SKILL.md |
| `area-account` | 🔵 | Skills de account |
| `area-geral` | 🟢 | Skills gerais |
| `area-gt` | 🟠 | Gestão de tráfego |
| `area-v4mos` | 🟤 | Integrações V4mos |
| `area-cro` | 🟡 | CRO/funil |
| `area-base` | ⚪ | Skills de setup (onboarding, sync-hub, etc.) |
| `importada` | 🔘 | Skills importadas do marketplace |
| `cliente` | 🟣 | Pastas de cliente |
| `squad-prime` | 🔴 | Squad Prime |
| `csm` | 🟤 | Módulos do CSM Hub |
| `csm-flag` | 🟠 | Flags do CSM |
| `hub` | ⚫ | Arquivos raiz |

---

## 6. Análise de Risco

| Etapa | Risco | Status |
|-------|-------|--------|
| Adicionar `aliases` no frontmatter | ✅ Muito baixo — nova chave YAML ignorada por parsers existentes | Verificado no `build-registry.py` |
| Converter `.claude/skills/` em symlinks | ✅ Confirmado — 57 de 57 pares são idênticos | Diff realizado entre todos os pares |
| Adicionar `[[wikilinks]]` no corpo dos SKILL.md | ✅ Muito baixo — colchetes são inertes para Claude/Codex | Skills carregam como texto puro |
| Adicionar `[[wikilinks]]` em clientes/mission-control | ✅ Baixo — skills parseiam por padrões (tabelas, task lists), ignoram texto solto | Verificado no `account-checkin-roleplay` |
| Adicionar `tags` no frontmatter | ✅ Muito baixo — mesma lógica dos aliases | Ignorado por todos os parsers |
| REGISTRY.md (auto-gerado) | ✅ Sem alteração manual | `build-registry.py` será atualizado se desejado |

**Conclusão: nenhuma etapa quebra o funcionamento atual das skills, parsers ou CI/CD.**

---

## 7. Pré-requisitos para Replicação

1. Repositório clonado e aberto como vault no Obsidian (`.obsidian/` existente)
2. Python 3.x para o `build-registry.py` (se for modificar o script)
3. Permissão de escrita nos diretórios `.claude/skills/`, `.agents/skills/`, `squads/`, `csm-hub/`, `docs/`
4. Acesso ao shell (Linux/Mac) para criar symlinks (Etapa 2)

---

## 8. Instruções de Manutenção

**Para skills novas:** o `/criador-de-skills` já cria o SKILL.md. Após criar, adicione manualmente:
- `aliases: [nome-da-skill]` no frontmatter
- `tags: [skill, area-{area}]` no frontmatter
- `[[wikilinks]]` na seção de Related Skills

**Para clientes novos:** após `/novo-cliente`, rode `/contexto` para gerar mission-control. Depois adicione:
- `aliases` para cada arquivo com nome genérico (ex: `okr-quarter` → `cliente-okr-quarter`)
- `tags: [cliente, squad-{squad}]` no README
- `[[wikilinks]]` do README para os sub-arquivos

**Para o csm-hub:** cada novo módulo deve seguir o padrão existente (SKILL.md + CONTEXT.md + TRIGGERS.md + OUTPUTS.md) com `aliases` únicos e `tags: [csm, csm-flag]`.

---

## 9. Plano de Execução (7 Etapas)

> Instruções detalhadas para implementar em qualquer unidade.

### Etapa 1 — Aliases no frontmatter de todos os SKILL.md

Adicionar `aliases: [nome-da-skill]` em cada um dos 58 SKILL.md. Exemplo:

```yaml
---
name: account-handoff
description: Primeira skill que o account roda...
area: account
author: guilhermelippert
version: 1.0.0
aliases: [account-handoff]
---
```

**Impacto:** 58 edições, 1 linha cada. Localização: antes do `---` de fechamento.

### Etapa 2 — Symlinks no .claude/skills/

Para cada uma das 57 skills com conteúdo idêntico:

```bash
rm .claude/skills/{nome}/SKILL.md
ln -s ../../.agents/skills/{nome}/SKILL.md .claude/skills/{nome}/SKILL.md
```

**Verificação:** `ls -la .claude/skills/{nome}/SKILL.md` deve mostrar `-> ../../.agents/skills/{nome}/SKILL.md`.

**Exceção:** `gt-apresentacao-visual-modelo1` — diretório vazio, ignorar.

### Etapa 3 — Wikilinks nas seções de Related Skills

Em cada SKILL.md, converter referências textuais para wikilinks.

**Padrão marketplace skills (seção `## Related Skills`):**

```
Antes:  - **page-cro**: For generating test ideas...
Depois: - **[[page-cro]]**: For generating test ideas...
```

**Padrão V4 skills (seção `## Conexão com outras skills`):**

```
Antes:  - **`/contexto`** — cria/atualiza Mission Control
Depois: - **`[[contexto]]`** — cria/atualiza Mission Control
```

**Impacto:** ~200 edições em 58 arquivos (~3-5 links por skill). Apenas em seções específicas de "Related Skills" — não mexe no restante do conteúdo.

### Etapa 4 — Wikilinks nos arquivos raiz

**README.md:** `[[CONTRIBUTING]]` (já existe como link markdown, adicionar wikilink também)
**AGENTS.md / CLAUDE.md:** `[[REGISTRY]]`, `[[CONTRIBUTING]]`
**CONTRIBUTING.md:** `[[compartilhar-skill]]`, `[[sync-hub]]` (referências a comandos)

### Etapa 5 — Wikilinks na estrutura squad/cliente

**squads/prime/README.md:**
```markdown
- [[squads/prime/clientes/gset/README|GSET Tennis]]
- [[squads/prime/clientes/atlas-copco-usa/README|Atlas Copco USA]]
```

**cada clientes/{cliente}/README.md:**
- Links para `mission-control/`, `campanhas/`, `docs/`, `links.md`

**cada arquivo de mission-control, campanha, doc:**
- Adicionar `aliases: [cliente-nome-do-arquivo]` no frontmatter para resolução única
- Link de volta para o README do cliente

### Etapa 6 — Wikilinks no csm-hub

**csm-hub/README.md:**
```markdown
- [[csm-principal]]
- [[flag-churn]]
- [[flag-okr]]
- etc.
```

**cada módulo:**
- SKILL.md → `[[CONTEXT]]`, `[[TRIGGERS]]`, `[[OUTPUTS]]`
- CONTEXT.md, TRIGGERS.md, OUTPUTS.md → link de volta para SKILL.md + `aliases: [modulo-funcao]`

### Etapa 7 — Tags no frontmatter

**SKILL.md (skills de papel/fonte):** `tags: [skill, area-{area}]`
**SKILL.md (skills de base):** `tags: [skill, area-base]`
**SKILL.md (skills importadas):** `tags: [skill, area-{prefixo}, importada]`

**Clientes:** `tags: [cliente, squad-prime]`
**Mission-control:** `tags: [mission-control, cliente, squad-prime]`
**Campanhas:** `tags: [campanha, cliente, squad-prime]`

**csm-hub:** `tags: [csm, csm-modulo]` (SKILL.md), `tags: [csm, csm-contexto]` (CONTEXT.md), etc.

---

## 10. Referências

- [Builders Hub README](../README.md)
- [REGISTRY.md — Catálogo de Skills](../REGISTRY.md)
- [CONTRIBUTING.md — Como contribuir](../CONTRIBUTING.md)
- Documentação Obsidian: https://help.obsidian.md/Plugins/Graph+view
