# Builders Hub — Estrutura do Projeto

```
v4perettoco-main/
│
├── README.md                         # Documentação principal
├── AGENTS.md                         # Instruções para agentes de IA
├── CLAUDE.md                         # Instruções para Claude Code
├── CONTRIBUTING.md                   # Guia de contribuição de skills
├── REGISTRY.md                       # Catálogo auto-gerado de skills
├── opencode.json                     # Configuração do OpenCode
├── n8nac-config.json                 # Configuração n8n-as-code
├── skills-lock.json                  # Lock de hashes de skills importadas
├── ESTRUTURA.md                      # ← Este arquivo
│
├── .agents/skills/                   # Skills (espelho para Anti-Gravity/OpenCode) — 61 skills
├── .claude/skills/                   # Skills (espelho para Claude Code) — 60 skills
├── .opencode/                        # Configurações do OpenCode
│   ├── agents/                       #   12 agentes especializados
│   ├── commands/                     #   3 comandos custom (/session-*)
│   └── skills/                       #   21 skills (ah-*, obsidian-*, defuddle)
│
├── squads/                           # Squads e clientes (gitignored)
│   └── prime/                        #   Squad com 6 clientes
│       ├── README.md                 #   Membros: Marcos, Alexander, Fhelipe, Lucas, Bruno
│       ├── AGENTS.md / CLAUDE.md
│       ├── docs/
│       └── clientes/
│           ├── all-over-exterior-roofing/
│           ├── atlas-copco-usa/
│           ├── cliente-teste/
│           ├── conserva-irrigation/
│           ├── gset/
│           └── premium-cleaning-services/
│
├── bases/                            # Knowledge Bases não-cliente (gitignored)
│   ├── _template/                    #   Templates de estrutura
│   └── peretto-co/                   #   KB pessoal Peretto Co
│
├── csm-hub/                          # Customer Success Manager Hub
│   ├── modulos/                      #   csm-principal, flag-churn, flag-okr, flag-operacao, flag-roi
│   ├── automacoes/
│   └── setup/
│
├── v4-automations/                   # Automações em Python
│   ├── scripts/                      #   Scripts por área (gt, am, copy, coordenador, ekyte)
│   ├── config/                       #   Credenciais e configs
│   ├── cron/                         #   Agendamentos
│   └── setup/
│
├── workflows/                        # n8n workflows as code (TypeScript)
│   └── ready-wave/                   #   8 workflows (jarvis-*, google-ads-report)
│
├── premium-contractors-website/      # Projeto Next.js completo (shadcn/ui)
├── onepage-site/                     # Site one-page estático
├── peretto-co/                       # Pasta pessoal Peretto Co
│
├── docs/                             # Documentação geral + CSVs de auditoria
├── log/                              # Sessões exportadas (JSON, gitignored)
├── scripts/                          # Scripts utilitários
│
├── .github/                          # GitHub Actions, PR template, agentes
├── .obsidian/                        # Config do vault Obsidian
├── .n8nac/                           # n8n-as-code runtime
└── .opencode-runtime/                # OpenCode runtime
```

## Estrutura padrão de um cliente

```
squads/{squad}/clientes/{cliente}/
├── .env / .env.example
├── AGENTS.md / CLAUDE.md / README.md / links.md
├── calls/               # Transcripts brutos de reuniões
├── checkins/            # Pautas, ensaios e reviews de check-in
├── campanhas/           # Dados de campanhas (CSVs, estratégias)
├── docs/                # Documentos do cliente
├── criativos/           # Assets criativos
└── mission-control/     # Estado vivo do cliente
    ├── okr-quarter.md
    ├── apostas-vivas.md
    ├── combinados.md
    ├── historico-checkins.md
    └── personas-call.md
```

## Skills por categoria

| Prefixo | Categoria | Quantidade |
|---------|-----------|-----------|
| `geral-*` | Qualquer papel | 5 |
| `gt-*` | Gestão de Tráfego | 2 |
| `account-*` | Account | 4 |
| `copy-*` | Copy | 2 |
| (sem prefixo) | Skills de base | 13 |
| Demais | Marketing/Growth (EN) | ~34 |
| `ah-*` | Pessoais (OpenCode) | 16 |
| `obsidian-*` | Obsidian (OpenCode) | 3 |

## Papeis dos agentes OpenCode

- `analista-dados` — Análise de performance e OKRs
- `csm-orquestrador` — Setup, triagem, QBR, fechamento
- `executor-comite` — Briefing do Comitê de P&EG
- `flag-churn` — Diagnóstico de risco de churn
- `flag-okr` — Diagnóstico de desvio de OKR
- `flag-operacao` — Alerta de operação travada
- `flag-roi` — Diagnóstico de ROAS abaixo da meta
- `gerar-doc` / `gerar-html` / `gerar-pdf` / `gerar-ppt` — Geração de documentos
- `revisor` — Validação e revisão de outputs

## Estatísticas

| Item | Total |
|------|-------|
| Skills (.claude) | 60 |
| Skills (.agents) | 61 |
| Skills (.opencode) | 21 |
| Agentes OpenCode | 12 |
| Comandos custom | 3 |
| Squads | 1 (prime) |
| Clientes | 6 |
| Módulos CSM | 5 |
| Workflows n8n | 8 |
| Scripts Python | ~12 |
| Sessões em log/ | 4 |
