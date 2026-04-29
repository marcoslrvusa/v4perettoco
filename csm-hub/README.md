# CSM Hub — V4 Company

> Sistema agêntico de Customer Success Management para squads de marketing.
> Repositório especializado — depende do builders-hub operacional, mas tem vida própria.

---

## O que é o CSM na V4

O CSM (Customer Success Manager) é a figura que fica **acima do squad operacional**.
Não executa — orquestra. Conecta o squad com outras áreas da empresa para garantir
que o objetivo do cliente seja cumprido independentemente de quais fronteiras precisem ser cruzadas.

É o defensor do cliente dentro da empresa.

---

## Como este repositório se relaciona com o builders-hub

```
builders-hub/          ← operação do squad (GT, Copy, AM, Coordenador)
    └── skills V4 por função

csm-hub/               ← este repositório
    └── CSM acima do squad
    └── depende dos dados gerados pelo builders-hub
    └── não substitui — reposiciona
```

O Agente AM continua existindo dentro do squad como executor.
O CSM sobe um nível — AM vira executor, CSM vira orquestrador.

---

## Estrutura de módulos

```
csm-hub/
├── README.md
├── central/
│   └── README.md              ← este arquivo
├── modulos/
│   ├── csm-principal/         ← o agente CSM em si (setup + orquestração)
│   │   ├── SKILL.md
│   │   ├── CONTEXT.md
│   │   ├── TRIGGERS.md
│   │   └── OUTPUTS.md
│   ├── flag-roi/              ← agente específico para ROI negativo
│   ├── flag-churn/            ← agente específico para risco de churn
│   ├── flag-okr/              ← agente específico para desvio de OKR
│   └── flag-operacao/         ← agente específico para operação travada
├── setup/
│   ├── ONBOARDING.md          ← passo a passo de setup inicial por unidade
│   └── setup_inicial.py       ← script de configuração automatizada
└── automacoes/
    ├── detector_flags.py      ← roda quinta 7h e domingo 20h
    ├── flag_roi.py            ← script da flag de ROI
    ├── flag_churn.py          ← script da flag de churn
    ├── flag_okr.py            ← script da flag de OKR
    └── flag_operacao.py       ← script da flag de operação travada
```

---

## Como implementar em uma unidade nova

**Etapa 1 — Setup inicial (feito uma vez)**
```bash
python setup/setup_inicial.py
```

**Etapa 2 — Configurar Claude Projects**
Crie 5 Projects no claude.ai, um por módulo.
Cada Project recebe o `SKILL.md` + `CONTEXT.md` do módulo no system prompt.

**Etapa 3 — Ativar automações**
```bash
python setup/setup_inicial.py --instalar-crons
```

**Etapa 4 — Setup inicial do CSM**
Abra o Project do CSM Principal e rode:
> "Inicie o setup da unidade [nome da unidade]"

O agente guia o processo completo.

---

## Agenda de automações

| Script | Quando | O que faz |
|---|---|---|
| `detector_flags.py` | Quinta 7h + Domingo 20h | Coleta dados, detecta flags, aciona agentes |
| `flag_roi.py` | Quando ROI < meta por 2 semanas | Diagnóstico + escalada automática |
| `flag_churn.py` | Quando NPS < 50 + CSAT < 3.5 | Plano de retenção + comunicação CSM |
| `flag_okr.py` | Quando KR < 60% do esperado | Análise de desvio + replanejamento |
| `flag_operacao.py` | Sprint atrasada sem FCA | Alerta operacional + cobrança automática |

---

## Dependências

- `builders-hub` — para contexto operacional dos clientes
- `v4-automations` — para conectores Google Ads, Meta, GA4, Ekyte, Gmail
- `obsidian-vault` — para memória histórica dos clientes
- Python 3.9+ com dependências do v4-automations instaladas
