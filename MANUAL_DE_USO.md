# Manual de Uso — Arquitetura de Agentes Peretto & Co

> Versão: 1.0 | Data: 17/05/2026
> Como usar os 12 agentes, commands e automações no dia a dia

---

## Índice Rápido

| Seção | Descrição |
|---|---|
| [1. Comece por Aqui](#1-comece-por-aqui) | Como abrir o OpenCode e testar se está tudo funcionando |
| [2. Lista Completa de Agentes](#2-lista-completa-de-agentes) | Todos os 12 agentes, o que cada um faz e exemplo de uso |
| [3. Commands Disponíveis](#3-commands-disponíveis) | Comandos `/` que você pode usar no TUI |
| [4. Hierarquia de Uso dos Agentes](#4-hierarquia-de-uso-dos-agentes) | Qual modelo usar pra cada tipo de tarefa |
| [5. Fluxos do Dia a Dia](#5-fluxos-do-dia-a-dia) | Rotinas prontas: comitê, flags, QBR, criação de conteúdo |
| [6. Pesos e Contrapesos](#6-pesos-e-contrapesos) | Como o @revisor protege você de erros |
| [7. Sessões Assíncronas](#7-sessões-assíncronas) | Como navegar entre tarefas paralelas |
| [8. Automações e Crons](#8-automações-e-crons) | O que roda automático e quando |
| [9. Troubleshooting](#9-troubleshooting) | Problemas comuns e soluções |
| [10. Glossário](#10-glossário) | Termos técnicos explicados |

---

## 1. Comece por Aqui

### 1.1 Abrir o OpenCode no projeto

```bash
cd /home/marcos/Desktop/v4perettoco-main-final/v4perettoco-main
opencode
```

### 1.2 Verificar se os agentes estão disponíveis

Dentro do TUI, digite `@` e veja se aparecem no autocomplete:
- `@analista-dados`
- `@gerar-pdf`
- `@gerar-ppt`
- `@gerar-html`
- `@gerar-doc`
- `@revisor`
- `@csm-orquestrador`
- `@flag-roi`
- `@flag-churn`
- `@flag-okr`
- `@flag-operacao`
- `@executor-comite`

### 1.3 Teste rápido

No TUI, digite:

```
@analista-dados "teste de conexão — analisa estes dados mock: ROAS 3.2, CPA R$45, CVR 3.5%"
```

Se funcionar, está tudo pronto.

### 1.4 Alternar entre modos (Tab)

- **Tab** alterna entre **Build** (pode editar arquivos) e **Plan** (só analisa, não altera nada)
- Use **Plan** quando quiser revisar algo sem risco de alteração
- Use **Build** para executar tarefas

---

## 2. Lista Completa de Agentes

### 2.1 Agentes de Entrega (criação de artefatos)

#### `@gerar-pdf` — Cria PDFs estilizados

| Campo | Valor |
|---|---|
| **Modelo** | Gemini 2.5 Flash |
| **Skill base** | geral-frontend-design |
| **Permissões** | read:✅ edit:✅ bash:✅ webfetch:❌ |
| **Autonomia** | Completa (sem revisão obrigatória) |

**O que faz:** Gera PDFs profissionais com layout V4 (logo, cores, tipografia). Usa HTML → PDF.

**Exemplos de uso:**
```
@gerar-pdf "relatório mensal de performance do cliente Atlas Copco — inclui ROAS, CPA, CVR e OKR progress dos últimos 30 dias"
@gerar-pdf "proposta comercial para o lead Premium Contractors com 3 tiers de serviço"
@gerar-pdf "checklist semanal de conformidade da squad — formato S/N"
```

---

#### `@gerar-ppt` — Cria apresentações

| Campo | Valor |
|---|---|
| **Modelo** | Gemini 2.5 Flash |
| **Skill base** | geral-frontend-design |
| **Permissões** | read:✅ edit:✅ bash:✅ webfetch:❌ |
| **Autonomia** | Completa |

**O que faz:** Gera slide decks HTML interativos (Reveal.js ou HTML puro) com a estrutura V4: headline + dado + visual + ação.

**Exemplos de uso:**
```
@gerar-ppt "apresentação do comitê de P&EG desta semana — briefing com dados reais"
@gerar-ppt "QBR do cliente X — resultados do quarter vs metas, insights e plano para o próximo"
@gerar-ppt "deck de check-in para reunião com o cliente Y — métricas, flags e recomendações"
```

---

#### `@gerar-html` — Cria páginas web

| Campo | Valor |
|---|---|
| **Modelo** | Gemini 2.5 Flash |
| **Skill base** | geral-frontend-design |
| **Permissões** | read:✅ edit:✅ bash:✅ webfetch:❌ |
| **Autonomia** | Completa |

**O que faz:** Gera HTML/CSS/JS completos e responsivos em arquivo único.

**Exemplos de uso:**
```
@gerar-html "dashboard de OKRs do squad Prime com gráficos de progresso por KR"
@gerar-html "landing page de apresentação do serviço de CSM da Peretto & Co"
@gerar-html "status page com indicadores de saúde de todos os clientes ativos"
@gerar-html "relatório interativo de ROAS por cliente com filtro por período"
```

---

#### `@gerar-doc` — Cria documentos formatados

| Campo | Valor |
|---|---|
| **Modelo** | Gemini 2.5 Flash |
| **Permissões** | read:✅ edit:✅ bash:✅ webfetch:❌ |
| **Autonomia** | Completa |

**O que faz:** Gera documentos em markdown (padrão Obsidian) com estrutura V4. Pode converter para DOCX/PDF.

**Exemplos de uso:**
```
@gerar-doc "ata da reunião de Growth de terça — cliente Atlas Copco — baseada no transcript que vou colar abaixo"
@gerar-doc "FCA — desvio de ROAS do cliente GSET Tennis identificado na análise de quinta"
@gerar-doc "briefing criativo para campanha do Dia dos Pais do cliente Premium Contractors"
@gerar-doc "relatório semanal de operações — formato padrão com status de sprints e blockers"
```

---

### 2.2 Agentes de Análise

#### `@analista-dados` — Análise multi-fonte

| Campo | Valor |
|---|---|
| **Modelo** | DeepSeek V4 Flash Free |
| **Permissões** | read:✅ edit:✅ bash:✅ webfetch:✅ |
| **Autonomia** | Relatórios internos (revisão opcional) |

**O que faz:** Puxa dados de múltiplas fontes (Google Ads, Meta, GA4, CSVs, Ekyte), cruza métricas e gera JSON estruturado com insights e recomendações.

**Exemplos de uso:**
```
@analista-dados "analisa performance do cliente Atlas Copco nos últimos 30 dias — ROAS, CPA, CVR por canal"
@analista-dados "cruza ROAS com CPA do cliente GSET Tennis este mês vs mês passado — identifica tendências"
@analista-dados "puxa OKRs de todos os clientes do squad Prime e calcula progresso vs esperado"
@analista-dados "compara eficiência de campanhas Meta vs Google Ads do cliente X — últimas 4 semanas"
```

**O output do @analista-dados é JSON estruturado que outros agentes consomem:**

```json
{
  "client": "Atlas Copco",
  "period": "2026-04-17 to 2026-05-17",
  "metrics": {
    "roas": {"value": 3.2, "target": 4.0, "status": "below_target"},
    "cpa": {"value": 45.00, "target": 35.00, "status": "above_target"}
  },
  "flags": ["roi"],
  "insights": ["CPA subiu 28% vs mês passado devido a aumento de concorrência"],
  "recommendations": ["Revisar segmentação de audiência no Meta Ads"]
}
```

---

#### `@revisor` — Validação e controle de qualidade

| Campo | Valor |
|---|---|
| **Modelo** | DeepSeek V4 Flash Free |
| **Permissões** | read:✅ edit:❌ **DENY** bash:❌ **DENY** webfetch:✅ |
| **Autonomia** | Nenhuma — só valida, nunca executa |

**O que faz:** Valida outputs de outros agentes. Confere números, cruza com dados históricos, verifica formato, aponta inconsistências. É o **peso e contrapeso** do sistema.

**IMPORTANTE:** Este agente NÃO PODE EDITAR ARQUIVOS. Ele só identifica problemas e reporta.

**Exemplos de uso:**
```
@revisor "valida este JSON de análise de performance antes de eu gerar o relatório" [cola o JSON]
@revisor "revisa a ata que o @gerar-doc acabou de gerar — confere se tem todos os campos obrigatórios"
@revisor "confere os números deste briefing de comitê — cruza ROAS, CPA e OKR progress"
```

**Output típico:**
```
## Revisão: ANÁLISE - Atlas Copco

### Status: ❌ REQUER CORREÇÕES

### Pontos verificados
- ✅ ROAS 3.2 confere com dados históricos
- ✅ Período correto (30 dias)
- ❌ CPA calculado com custo total em vez de custo de mídia (incluiu taxa de agência)
- ❌ Seção "recomendações" sem prazos definidos

### Correções necessárias
1. Recalcular CPA: usar apenas custo de mídia (R$ 38,50, não R$ 45,00)
2. Adicionar prazos nas recomendações
```

---

#### `@executor-comite` — Briefing automático do comitê

| Campo | Valor |
|---|---|
| **Modelo** | DeepSeek V4 Flash Free |
| **Permissões** | read:✅ edit:✅ bash:✅ webfetch:✅ |
| **Autonomia** | Briefings (ideal com @revisor depois) |

**O que faz:** Prepara o briefing semanal do Comitê de P&EG automaticamente. Puxa OKRs, sprints, FCAs e flags de todos os clientes e monta o documento.

**Exemplos de uso:**
```
@executor-comite "prepara o briefing do comitê de segunda para o squad Prime"
@executor-comite "gera relatório de status semanal de todos os clientes"
```

**Output:** Briefing completo em .md e .html na pasta `docs/` ou `rituais/comites/`.

---

### 2.3 Agentes CSM

#### `@csm-orquestrador` — Orquestrador CSM

| Campo | Valor |
|---|---|
| **Modelo** | GPT-OSS 120B Free (OpenRouter) |
| **Permissões** | read:✅ edit:✅ bash:✅ webfetch:✅ |
| **Autonomia** | Setup inicial (com @revisor) |

**O que faz:** O cérebro da operação CSM. Fica acima do squad. Não executa — orquestra. Baseado na Escola de CSM - Aula 1.

**Exemplos de uso:**
```
@csm "inicia o setup da unidade Squad Prime — configura carteira de clientes no framework CSM"
@csm "faz triagem de flags de todos os clientes — consolida e prioriza"
@csm "prepara QBR do cliente Atlas Copco — quarter review com dados reais"
@csm "diagnóstico de saúde da carteira — quais clientes estão em risco e por quê"
```

---

#### `@flag-roi` — Diagnóstico de ROAS

| Campo | Valor |
|---|---|
| **Modelo** | DeepSeek V4 Flash Free |
| **Permissões** | read:✅ edit:❌ **DENY** bash:✅ webfetch:❌ |
| **Autonomia** | Diagnóstico — não executa |

**O que faz:** Ativado quando ROAS cai abaixo da meta por 2 semanas. Classifica o tipo (custo / conversão / valor) e gera CHAS para o GT.

**Exemplo:**
```
@flag-roi "analisa ROAS do cliente GSET Tennis — últimas 4 semanas: semana1=3.8, semana2=3.2, semana3=2.9, semana4=2.7 — meta é 4.0"
```

---

#### `@flag-churn` — Diagnóstico de churn

| Campo | Valor |
|---|---|
| **Modelo** | DeepSeek V4 Flash Free |
| **Permissões** | read:✅ edit:❌ **DENY** bash:✅ webfetch:❌ |
| **Autonomia** | Diagnóstico — não executa |

**O que faz:** Ativado quando NPS e CSAT caem juntos. Faz a distinção crítica entre churn por **percepção** (comunicação falhou) e churn por **resultado** (entrega falhou).

**Exemplo:**
```
@flag-churn "cliente Premium Contractors — NPS caiu de 75 para 45, CSAT de 4.5 para 3.2 nos últimos 2 meses. ROAS está em 3.8 (meta 4.0) — diagnostique"
```

---

#### `@flag-okr` — Diagnóstico de OKR

| Campo | Valor |
|---|---|
| **Modelo** | DeepSeek V4 Flash Free |
| **Permissões** | read:✅ edit:❌ **DENY** bash:✅ webfetch:❌ |
| **Autonomia** | Diagnóstico — não executa |

**O que faz:** Ativado quando KR está abaixo de 60% do progresso esperado. Distingue desvio de execução (ainda dá tempo) de desvio de premissa (precisa replanejar).

**Exemplo:**
```
@flag-okr "KR: Reduzir CPA em 15% — progresso atual: 5% (estamos no mês 3 de 6). Meta: de R$40 para R$34. CPA atual: R$38. Diagnostique"
```

---

#### `@flag-operacao` — Diagnóstico de operação travada

| Campo | Valor |
|---|---|
| **Modelo** | DeepSeek V4 Flash Free |
| **Permissões** | read:✅ edit:❌ **DENY** bash:✅ webfetch:❌ |
| **Autonomia** | Diagnóstico — não executa |

**O que faz:** Ativado quando sprint atrasa sem FCA ou timesheet zera. Classifica em 3 níveis: operacional / estrutural / externo.

**Exemplo:**
```
@flag-operacao "sprint 'Otimização de Landing Page' do cliente Atlas Copco está sem atualização há 5 dias. Não tem FCA aberta. Timesheet do designer zerado há 3 dias. Classifique"
```

---

## 3. Commands Disponíveis

### `/session-save`
Exporta a sessão atual para a pasta `log/` como JSON. Faça isso ao final de cada interação significativa.

### `/session-list`
Lista todas as sessões salvas em `log/` + sessões ativas no OpenCode.

### `/session-load`
Carrega o contexto de uma sessão anterior. Escolha pelo nome do arquivo.

### `/agendar-rituais`
Configura os crons de automação (detector_flags, briefing de comitê, OKRs). Roda uma vez só.

### `/csm-diagnostico`
Roda diagnóstico CSM completo de um cliente (flags + OKRs + saúde). Invoca múltiplos agentes em paralelo.

---

## 4. Hierarquia de Uso dos Agentes

Use esta tabela para decidir qual agente/modelo usar em cada situação:

| Tarefa | Agente | Modelo | Por quê |
|---|---|---|---|
| Análise complexa de dados | @analista-dados | DeepSeek V4 | 1M de contexto, melhor em raciocínio |
| Criar PDF/PPT/HTML/DOC | @gerar-* | Gemini 2.5 Flash | Excelente em criação visual |
| Validar output antes de enviar | @revisor | DeepSeek V4 | Precisão, edit:deny (seguro) |
| Orquestração CSM / QBR | @csm-orquestrador | GPT-OSS 120B | Escrita estratégica, tom consultivo |
| Flag de ROAS | @flag-roi | DeepSeek V4 | Análise, classificação |
| Flag de churn | @flag-churn | DeepSeek V4 | Diagnóstico crítico |
| Flag de OKR | @flag-okr | DeepSeek V4 | Raciocínio sobre metas |
| Flag de operação | @flag-operacao | DeepSeek V4 | Classificação |
| Briefing de comitê | @executor-comite | DeepSeek V4 | Síntese multi-cliente |
| Tarefa rápida (classificar) | (nenhum agente específico) | MiniMax M2.5 | Velocidade |
| Fallback (rate limit) | (nenhum) | Llama 3.3 70B / Qwen 3.6 | Backup |

### 4.1 Tabela de Fallback

Se um modelo rate-limit (ficar indisponível por excesso de uso), use esta ordem:

| Se falhar | Tente |
|---|---|
| DeepSeek V4 (Zen) | `openrouter/deepseek/deepseek-v4-flash:free` |
| Gemini 2.5 Flash | `google/gemini-2.0-flash` |
| GPT-OSS 120B | `openrouter/meta-llama/llama-3.3-70b-instruct:free` |
| MiniMax M2.5 | `opencode/qwen3.6-plus-free` |
| Nemotron 3 Super | `openrouter/nvidia/nemotron-3-nano-30b-a3b:free` |

---

## 5. Fluxos do Dia a Dia

### 5.1 Rotina de Segunda-feira (Comitê)

```
Setup automático (domingo 20h):
  → @executor-comite gera o briefing
  → Salva em docs/ e no vault

Na segunda 7h:
  → Revisa o briefing
  → Se quiser validar: @revisor "confere o briefing do comitê"
  → Se quiser apresentação: @gerar-ppt "deck do comitê baseado no briefing"
```

### 5.2 Rotina de Quinta-feira (Flags + OKRs)

```
Setup automático (quinta 7h):
  → detector_flags.py coleta dados de todos os clientes
  → Scripts de flag analisam ROAS, OKRs, sprints

Na quinta 8h:
  → @csm "faz triagem de flags da semana"
  → @revisor "valida diagnóstico do CSM antes de agir"
  → ⚠️ Se flag crítica: agir imediatamente (ver seção 5.4)
```

### 5.3 Rotina de QBR (Quarterly)

```
1. @csm-orquestrador "inicia QBR do cliente X"
2. @analista-dados "puxa dados do quarter completo do cliente X"
3. @revisor "valida análise do QBR"
4. @gerar-ppt "cria apresentação de QBR do cliente X"
5. @csm-orquestrador "prepara roteiro da reunião de QBR com talking points"
```

### 5.4 Kit de Emergência — Flag Crítica

Quando uma flag 🔴 aparece, siga este protocolo:

```
1. @flag-roi / @flag-churn / @flag-okr / @flag-operacao
   → "diagnostica [cliente] com dados: [cole os dados]"

2. @revisor → "confirma este diagnóstico"

3. Se @revisor aprovar:
   → @csm → "plano de ação para flag [tipo] do cliente [nome]"

4. Se @revisor reprovar:
   → Volte ao passo 1 com os apontamentos do revisor

5. Documente tudo:
   → @gerar-doc "FCA para [cliente] com base no diagnóstico de flag"
```

### 5.5 Criação de Conteúdo Sob Demanda

```
Exemplo: criar relatório + apresentação + ata em sequência

@analista-dados "puxa dados do cliente X última semana"
  → output: JSON

@revisor "valida este JSON" [cola o JSON]
  → output: ✅ ou ❌ com correções

@gerar-pdf "relatório semanal do cliente X com estes dados" [cola JSON validado]
  → output: .pdf

@gerar-ppt "deck semanal do cliente X com estes dados" [cola JSON validado]  
  → output: .html (apresentação)
```

---

## 6. Pesos e Contrapesos

### 6.1 Matriz de Risco

| Ação do Agente | Risco | Precisa de @revisor? |
|---|---|---|
| Criar PDF/PPT/HTML/DOC | Baixo (é asset, não operação) | Não |
| Analisar dados internamente | Baixo | Opcional |
| **Diagnosticar flag** | **Médio** (pode classificar errado) | **Sim, se for 🔴** |
| **Escrever em Ekyte/CRM** | **Alto** (altera produção) | **Sim, obrigatório** |
| **Recomendar replanejamento de OKR** | **Alto** (muda meta do cliente) | **Sim, obrigatório** |
| Responder cliente diretamente | Alto | Sim |

### 6.2 O Papel do @revisor

O @revisor é seu **guardião de qualidade**. Ele:

- ✅ Confere se números estão corretos
- ✅ Verifica se o formato segue o padrão V4
- ✅ Aponta inconsistências antes do cliente ver
- ❌ **NUNCA edita arquivos** (edit:deny)
- ❌ **NUNCA executa comandos** (bash:deny)

Regra: **se pode causar dano ao cliente, passe pelo @revisor primeiro.**

---

## 7. Sessões Assíncronas

O OpenCode permite que agentes rodem **em paralelo** em sessões filhas. Você navega entre elas.

### 7.1 Navegação entre sessões

| Tecla | Ação |
|---|---|
| **Down** (↓) | Entrar na sessão filha |
| **Right** (→) | Próxima sessão filha |
| **Left** (←) | Sessão filha anterior |
| **Up** (↑) | Voltar para a sessão pai |

### 7.2 Quando usar

- **Múltiplos clientes**: `@analista-dados` para cada cliente → cada um roda em paralelo na sua sessão
- **Análise + criação**: `@analista-dados` numa sessão, `@gerar-ppt` noutra
- **Flags em paralelo**: @flag-roi, @flag-churn, @flag-okr e @flag-operacao rodando juntos

### 7.3 Exemplo prático

```
1. Peça ao @csm: "diagnóstico completo de todos os clientes"
2. O @csm invoca 4 @flag-* em paralelo (4 sessões filhas)
3. Use → para ver cada diagnóstico
4. Cada filho volta resultado independente
5. Use ↑ para voltar ao @csm e consolidar
```

---

## 8. Automações e Crons

### 8.1 O que roda automático

| Horário | Script | O que faz |
|---|---|---|
| **Domingo 20h** | `briefing_comite.py` | Gera briefing do Comitê de segunda com pace vs OKR |
| **Quinta 7h** | `analise_performance.py` | Análise de performance semanal do GT |
| **Quinta 8h** | `atualizar_okrs.py` | Atualiza OKRs com dados reais de API |
| **Sexta 16h** | `checklist.py` | Gera checklist S/N de conformidade |
| **Dia 1 do mês 8h** | `enviar_nps.py` | Dispara pesquisa NPS/CSAT para clientes |
| **Quinta 7h + Dom 20h** | `detector_flags.py` | (do csm-hub) Coleta dados, detecta flags |

### 8.2 Como gerenciar

```bash
# Ver crons ativos
crontab -l

# Instalar crons (já feito na instalação)
python /home/marcos/Desktop/v4perettoco-main-final/v4perettoco-main/v4-automations/setup/install_cron.py

# Ver logs dos scripts
ls -la /home/marcos/Desktop/v4perettoco-main-final/v4perettoco-main/v4-automations/logs/
cat /home/marcos/Desktop/v4perettoco-main-final/v4perettoco-main/v4-automations/logs/coordenador.log
```

---

## 9. Troubleshooting

### 9.1 "Agente X não aparece no @ autocomplete"

**Causa:** Arquivo .md mal formatado ou fora do lugar.
**Solução:**
```bash
ls .opencode/agents/*.md  # Verificar se os arquivos existem
ls ~/.config/opencode/agents/*.md  # Verificar globais
```
Cada arquivo precisa ter frontmatter válido (---description: / mode: subagent)

### 9.2 "Modelo Y está rate-limited"

**Causa:** Uso excessivo do modelo gratuito.
**Solução:** Use o fallback manualmente:
```
@analista-dados (use openrouter/deepseek/deepseek-v4-flash:free) "analisa..."
```

### 9.3 "Agent says it can't edit files"

**Causa esperada se for o @revisor** — ele tem edit:deny propositalmente.
**Causa inesperada:** Verifique se o agente correto foi invocado.

### 9.4 "Comando / não funciona"

**Verifique:**
```bash
cat opencode.json | grep -A5 '"command"'  # Comandos no projeto
cat ~/.config/opencode/opencode.jsonc | grep -A5 '"command"'  # Comandos globais
```

### 9.5 "Sessão filha não aparece"

Use **Down (↓)** para entrar na sessão filha.
Use **Tab** para ver os agentes primários.
Use `session list` no TUI para ver todas as sessões ativas.

---

## 10. Glossário

| Termo | Significado |
|---|---|
| **Subagent** | Agente secundário invocado com `@`. Roda em sessão própria. |
| **Primary Agent** | Agente principal (Build/Plan). Alterna com Tab. |
| **Sessão filha** | Sessão paralela criada quando um subagent é invocado. |
| **Peso e Contrapeso** | Sistema de governança: @revisor valida antes de ações críticas. |
| **Flag** | Sinal de alerta automático (ROI, Churn, OKR, Operação). |
| **FCA** | Ferramenta de Correção e Ação — documento de desvio e plano. |
| **CHAS** | Chain of Action Steps — sequência de ações para corrigir um problema. |
| **QBR** | Quarterly Business Review — reunião trimestral de resultados. |
| **CSM** | Customer Success Manager — orquestrador de resultado do cliente. |
| **ROAS** | Return on Ad Spend — retorno sobre investimento em anúncios. |
| **CPA** | Cost per Acquisition — custo por aquisição. |
| **CVR** | Conversion Rate — taxa de conversão. |
| **NPS** | Net Promoter Score — lealdade do cliente (0-100). |
| **CSAT** | Customer Satisfaction — satisfação do cliente (1-5). |
| **KR** | Key Result — resultado-chave de uma OKR. |
| **OKR** | Objectives and Key Results — metodologia de metas. |
| **OpenCode Zen** | Modelos gratuitos gerenciados pelo OpenCode (DeepSeek, MiniMax, Nemotron, Qwen). |
| **OpenRouter** | Agregador de modelos de AI com opções gratuitas. |
| **Rate Limit** | Limite de requisições por minuto/dia do modelo gratuito. |
| **TUI** | Terminal User Interface — interface de texto do OpenCode. |

---

> **Dica final:** Comece simples. Use `@analista-dados` e `@gerar-doc` no primeiro dia. Depois adicione `@revisor`. Depois os flags. Depois o CSM. Cada camada aumenta seu poder sem aumentar seu risco.

> **Salve a sessão:** No final de cada dia, rode `/session-save` para não perder o histórico.
