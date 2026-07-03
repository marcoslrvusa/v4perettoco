# Radar de Governança — Agents Hub

> **Data:** 2026-07-03
> **Autor:** Marcos Luciano
> **Propósito:** Mapa de fases, dependências e status para governança e escalabilidade do sistema multi-agente V4

---

## Fases do Projeto

### 🔴 Fase 1 — Fundação (Concluído)

A base já está rodando. O que existe hoje:

| Componente | Status | Localização |
|---|---|---|
| Repositório Builders Hub | ✅ Operacional | `/` com `squads/`, `projetos/`, `bases/` |
| Skills de setup | ✅ 8 skills base | `onboarding`, `sync-hub`, `contexto`, `criador-de-skills`, `compartilhar-skill`, `novo-squad`, `novo-cliente`, `novo-projeto` |
| Skills de papel | ✅ 40+ skills | `.agents/skills/` com prefixo `geral-*`, `gt-*`, `account-*`, `copy-*`, `designer-*` |
| Skill de contexto local | ✅ `/contexto` | Gera `CLAUDE.md` + `AGENTS.md` + `mission-control/` **apenas em disco** |
| Memória semântica (pgvector) | ✅ Schema + scripts | `geral-memoria-agentes` — `agent_memories` table |
| Contexto de cliente (Supabase) | ✅ Schema + scripts | `geral-contexto-cliente` — `client_context` table |
| LiteLLM config | ✅ Config YAML | `litellm-config.yaml` com DeepSeek, Gemini, GPT-OSS, MiniMax |
| OpenCode Web na VPS | ✅ Operacional | `opencode.v4.company.com` |
| n8n na VPS | ✅ Operacional | `n8n.v4.company.com` |
| Catálogo de skills | ✅ `REGISTRY.md` | Raiz do projeto |
| Site institucional | ✅ `agents-hub.html` | Raiz do projeto |
| 36 agentes OpenCode | ✅ `.opencode/agents/` | Todos configurados |

**Gap crítico identificado:** A skill `/contexto` escreve `mission-control/` apenas em arquivos locais. **Não persiste no Supabase.** Isso significa que:
- `geral-contexto-cliente` consegue puxar facts do Supabase (se foi sync feito manualmente)
- Mas `/contexto` não chama automaticamente `context.py sync --client` ao final
- Quebra o loop: agente puxa contexto → trabalha → `/contexto` atualiza → próximo agente não vê a atualização

---

### 🟡 Fase 2 — Integração Contexto ↔ Supabase (Prioridade Imediata)

Automatizar a persistência do `/contexto` no Supabase para que QUALQUER agente possa puxar os fatos do cliente sem depender de arquivos locais.

| Task | Descrição | Esforço | Depende |
|---|---|---|---|
| 2.1 | Modificar skill `/contexto` para chamar `context.py push` ao final do Passo 4 | 4h | — |
| 2.2 | Garantir que `context.py push` receba todos os campos extraídos (tom_de_voz, histórico, oferta, facts) | 2h | 2.1 |
| 2.3 | Adicionar flag `--auto-sync` ao `/contexto` para controle (on/off) | 1h | 2.1 |
| 2.4 | Testar ciclo completo: roda `/contexto` → verifica `client_context` no Supabase | 2h | 2.2 |
| 2.5 | Atualizar `geral-contexto-cliente` para puxar automático antes de qualquer trabalho (já tem o trigger, validar) | 1h | 2.4 |
| 2.6 | Documentar no SKILL.md o novo fluxo com Supabase | 1h | 2.5 |

**Total estimado:** 11h

**Métrica de sucesso:** Rodar `/contexto fips-nautica` e `context.py pull --client fips-nautica` retornar os mesmos dados.

---

### 🟡 Fase 3 — Copy: Briefing + Produção (2 Skills Separadas)

A skill `copywriting` atual faz tudo em um passo só. O método mapeado exige **briefing (reporting)** separado de **produção**. Criar duas skills especializadas.

#### 3.1 — Skill de Briefing (`copy-briefing`)

O que faz:
- Recebe demanda de conteúdo (usuário, task do Ekyte, pauta)
- Puxa contexto do cliente via `geral-contexto-cliente`
- Busca memórias similares via `geral-memoria-agentes`
- Gera brief estruturado: objetivo, tom, persona, referências, formato, prazo
- Salva brief em `docs/briefings/` + registra no Supabase

| Task | Descrição | Esforço | Depende |
|---|---|---|---|
| 3.1.1 | Criar skill `copy-briefing` com prefixo obrigatório | 2h | — |
| 3.1.2 | Implementar fluxo: puxar contexto → buscar memórias → estruturar brief | 6h | 3.1.1, Fase 2 |
| 3.1.3 | Integrar saída com Ekyte (ou salvar em `docs/briefings/`) | 3h | 3.1.2 |
| 3.1.4 | Duplo-write em `.claude/skills/` | 1h | 3.1.3 |

**Total estimado:** 12h

#### 3.2 — Skill de Produção (`copy-producao`)

O que faz:
- Recebe brief (da skill anterior ou manual)
- Puxa contexto do cliente
- Gera rascunho completo seguindo o brief
- Entrega no formato solicitado (copy para LP, email, anúncio, blog)
- Registra memória do que foi produzido

| Task | Descrição | Esforço | Depende |
|---|---|---|---|
| 3.2.1 | Criar skill `copy-producao` com prefixo obrigatório | 2h | — |
| 3.2.2 | Implementar leitura de brief estruturado (markdown frontmatter) | 3h | 3.2.1 |
| 3.2.3 | Implementar produção com contexto + memórias + brief | 8h | 3.2.2, Fase 2 |
| 3.2.4 | Registro automático de memória via `record.py` ao final | 2h | 3.2.3 |
| 3.2.5 | Duplo-write em `.claude/skills/` | 1h | 3.2.4 |

**Total estimado:** 16h

> **Nota:** O usuário mencionou "20h" para as duas skills combinadas. Ajustar os números conforme disponibilidade.

---

### 🟡 Fase 4 — LiteLLM como Gateway Único

Hoje os agentes chamam modelos diretamente de cada provider (OpenAI, OpenRouter, Google). O objetivo é que **todo agente passe pelo LiteLLM** como gateway central para:
- Roteamento de modelo por tipo de tarefa
- Fallback automático se um modelo cair
- Rate limiting centralizado
- Logs e custo centralizados

| Task | Descrição | Esforço | Depende |
|---|---|---|---|
| 4.1 | Garantir LiteLLM rodando como serviço systemd na VPS | 2h | — |
| 4.2 | Configurar `opencode.json` para usar LiteLLM como provider default | 2h | 4.1 |
| 4.3 | Criar skill `geral-gateway-modelos` para configurar roteamento por task-type | 6h | 4.2 |
| 4.4 | Mapear task-type → modelo ideal (ex: copy → Gemini, análise → DeepSeek, código → GPT-OSS) | 3h | 4.3 |
| 4.5 | Testar fallback: derrubar modelo primário e verificar se secundário assume | 2h | 4.4 |
| 4.6 | Dashboard de custo/uso dos modelos | 4h | 4.5 |

**Total estimado:** 19h

**Modelos por tipo de tarefa (proposto):**

| Tipo de Tarefa | Modelo Primário | Fallback |
|---|---|---|
| Copy / Conteúdo | `gemini/gemini-2.5-flash` | `openrouter/deepseek/deepseek-v4-flash:free` |
| Análise / Auditoria | `openrouter/deepseek/deepseek-v4-flash:free` | `gemini/gemini-2.5-flash` |
| Código / Infra | `openrouter/openai/gpt-oss-120b:free` | `openrouter/minimax/minimax-m2.5:free` |
| Estratégia / Sabatina | `openrouter/deepseek/deepseek-v4-flash:free` | `gemini/gemini-2.5-flash` |
| Design / Criação | `gemini/gemini-2.5-flash` | `openrouter/minimax/minimax-m2.5:free` |

---

### 🟢 Fase 5 — Testes Manuais e Ajustes de Qualidade

Rodar casos reais com cada agente/skill, afinar até a saída prestar.

| Task | Descrição | Esforço | Depende |
|---|---|---|---|
| 5.1 | Selecionar 3 clientes reais para teste (ex: fips-nautica, atlas-copco, conserva) | 1h | — |
| 5.2 | Rodar ciclo completo de contexto: `/contexto` + `context.py pull` | 2h | Fase 2 |
| 5.3 | Rodar copy briefing + produção com caso real | 4h | Fase 3 |
| 5.4 | Rodar search de memórias: ver se retorna resultados relevantes | 2h | — |
| 5.5 | Aferir qualidade: checklist de 10 critérios por output | 4h | 5.2, 5.3, 5.4 |
| 5.6 | Ajustar prompts/SKILL.md com base nos resultados | 6h | 5.5 |
| 5.7 | Segunda rodada de testes com os ajustes | 3h | 5.6 |
| 5.8 | Documentar critérios de qualidade no SKILL.md de cada skill | 2h | 5.7 |

**Total estimado:** 24h

**Checklist de qualidade (por output):**

```
[ ] Tom de voz do cliente foi respeitado?
[ ] Informações factuais estão corretas?
[ ] Oferta do cliente foi considerada?
[ ] Histórico foi levado em conta?
[ ] O output é acionável (dá pra usar direto)?
[ ] Tempo de geração foi aceitável?
[ ] O formato está correto (markdown, html, json)?
[ ] Precisa de ajuste manual significativo?
[ ] A memória foi registrada ao final?
[ ] O custo de inferência foi aceitável?
```

---

### 🔵 Fase 6 — Agente de Copy no OpenCode

Criar/configurar o agente `@copy-orchestrator` no OpenCode que orquestra as duas skills (briefing + produção).

| Task | Descrição | Esforço | Depende |
|---|---|---|---|
| 6.1 | Criar `.opencode/agents/copy-orchestrator.md` | 2h | Fase 3 |
| 6.2 | Configurar modelo via LiteLLM | 1h | Fase 4 |
| 6.3 | Definir sub-agentes: `@copy-briefing`, `@copy-producao` | 2h | Fase 3 |
| 6.4 | Testar fluxo completo: demanda → briefing → produção → entrega | 4h | 6.1, 6.2, 6.3 |
| 6.5 | Ajustar com feedback de copywriters reais | 4h | 6.4 |

**Total estimado:** 13h

---

### 🟣 Fase 7 — Escalabilidade e Governança

Estruturar o sistema para múltiplos squads e clientes sem degradação.

| Task | Descrição | Esforço | Depende |
|---|---|---|---|
| 7.1 | Revisar RLS do Supabase (cada squad vê só seus clientes) | 4h | Fase 2 |
| 7.2 | Pipeline de CI/CD para skills (PR → valida → deploy automático) | 8h | — |
| 7.3 | Dashboard de saúde do sistema (agentes, skills, modelos, Supabase) | 6h | Fase 4 |
| 7.4 | Playbook de onboarding para novo squad | 4h | — |
| 7.5 | Documentar arquitetura completa (este radar + whimsical) | 3h | Todas |

**Total estimado:** 25h

---

## Mapa de Dependências

```
Fase 1 (Fundação)
    │
    ▼
Fase 2 (Contexto ↔ Supabase) ◄── Crítico para tudo
    │
    ├────────────┬────────────┐
    ▼            ▼            ▼
Fase 3        Fase 4      Fase 5
(Copy 2x)   (LiteLLM)   (Testes)
    │            │            │
    └────────┬───┘            │
             ▼                │
         Fase 6               │
    (Agente Copy)              │
             │                │
             └───────┬────────┘
                     ▼
                Fase 7
          (Escalabilidade)
```

---

## Sumário de Esforço

| Fase | Horas | Prioridade | Squad |
|---|---|---|---|
| Fase 2 — Contexto ↔ Supabase | 11h | 🔴 Crítica | Tech Lead |
| Fase 3 — Copy Briefing + Produção | 28h | 🟡 Alta | Tech Lead + Copy |
| Fase 4 — LiteLLM Gateway | 19h | 🟡 Alta | Tech Lead |
| Fase 5 — Testes e Qualidade | 24h | 🟢 Média | Tech Lead + Todos |
| Fase 6 — Agente Copy | 13h | 🟢 Média | Tech Lead |
| Fase 7 — Escalabilidade | 25h | 🔵 Baixa | Tech Lead |
| **Total** | **120h** | — | — |

---

## Métricas de Governança

| Métrica | Meta | Como medir |
|---|---|---|
| Tempo entre contexto atualizado e disponível no Supabase | < 1 min | Log do `context.py push` |
| Precisão do contexto puxado vs KB local | 100% | Comparação manual trimestral |
| Taxa de uso da memória semântica | > 80% das tarefas | Log do `search.py` |
| Taxa de fallback do LiteLLM | < 5% das chamadas | Dashboard LiteLLM |
| Tempo médio de geração de copy | < 30s | Timer nas skills |
| Satisfação do usuário com output | > 8/10 | Pesquisa após cada uso |

---

## Próximos Passos Imediatos

1. ✅ **Hoje:** Documentar radar de governança (este arquivo)
2. ⬜ **Hoje:** Gerar estrutura para Whimsical (`docs/agents-hub/2026-07-03_WHIMSICAL-ESTRUTURA.txt`)
3. ⬜ **Semana 1:** Iniciar Fase 2 — modificar `/contexto` para sync automático com Supabase
4. ⬜ **Semana 1:** Criar `copy-briefing` e `copy-producao` como skills separadas
5. ⬜ **Semana 2:** Configurar LiteLLM como gateway default do OpenCode
6. ⬜ **Semana 2-3:** Rodar testes manuais com casos reais
7. ⬜ **Semana 3:** Criar agente `@copy-orchestrator`
8. ⬜ **Semana 4:** Iniciar governança e escalabilidade
