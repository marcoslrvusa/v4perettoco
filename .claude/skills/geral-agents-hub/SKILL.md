# Skill: geral-agents-hub

Cria e gerencia o ecossistema de apresentação do Agents Hub — sistema multi-agente de IA da V4 Company.

## O que esta skill entrega

| Artefato | Localização | Descrição |
|----------|------------|-----------|
| Site institucional | `agents-hub.html` (raiz) | Site completo com arquitetura, catálogo, 80/20, roadmap |
| Slide-deck apresentação | `assets/html/apresentacao-agents-hub.html` | 11 slides interativos para coordenador |
| Lógica de apresentação | `docs/agents-hub/LOGICA-APRESENTACAO.md` | Script, objeções, métricas, cronograma |
| Agentes OpenCode | `.opencode/agents/account-orchestrator.md` e `csm-orquestrador.md` | Agentes Account/CSM configurados |

## Quando usar

- O usuário disser que precisa apresentar o Agents Hub para coordenador, diretoria ou unidade
- O usuário mencionar "apresentar agentes", "site institucional agentes", "slide deck agents hub"
- O usuário precisar de materiais de apresentação de alto impacto (Dale Carnegie)
- O usuário quiser mostrar a arquitetura multi-agente para stakeholders técnicos

## Estrutura de apresentação (Dale Carnegie)

1. **Comece pelo resultado** — métricas de ganho (comitê 45min → 5min)
2. **Mostre o problema** — o custo oculto da operação manual
3. **Peça a ação** — 3 pedidos claros (validar, acessar, scaffold)

## Conteúdo do site

O site `agents-hub.html` contém:
- Hero com citações do Dener Lippert + Dr. Tom Chung + stats animados
- Arquitetura em 5 camadas (CEO Dener → Swarm → Orquestradores → Especialistas → Skills)
- CEO Dener Lippert com TOC, 4Vs, FPA, Logical Thinking
- Catálogo dos 5 pilares (CEO + Account, Tráfego, Copy, Design)
- OpenSquad + VPS com diagrama de fluxo
- Regra 80/20 com gráfico de barras antes/depois
- Princípios V4 (4Vs, 4 Pilares, FPA, TOC, Médico vs Garçom)
- Filosofia do Cientista do Marketing
- Princípios Dale Carnegie + Gantt do projeto
- Roadmap 2026 em 4 fases
- FAQ e CTA final

## Templates de comando

```
@criacao-design Cria site institucional do Agents Hub seguindo o padrão geral-agents-hub
```

```
Abra assets/html/apresentacao-agents-hub.html no navegador e use setas ← → para navegar
```

```
Leia docs/agents-hub/LOGICA-APRESENTACAO.md para entender o roteiro da apresentação
```

## Duplo-write

Esta skill existe em:
- `.agents/skills/geral-agents-hub/` (OpenCode)
- `.claude/skills/geral-agents-hub/` (Claude Code)
