# Agents Hub — Lógica de Apresentação

> Documento de apoio para apresentação ao coordenador
> Autor: Marcos Luciano · V4 Company
> Data: Junho 2026

---

## 🎯 Objetivo da Apresentação

**Conseguir 3 aprovações:**
1. ✅ Validar com cada área (sessões de 30min)
2. ✅ Liberar acesso aos sistemas (Google Ads, Meta, GA4, Ekyte)
3. ✅ Go para scaffold do agente Account/CSM na VPS

**Não é objetivo:** Explicar todo o código ou detalhes de implementação

---

## 🧠 Raciocínio Lógico (80/20 + Dale Carnegie)

### Princípio 1: Comece pelo resultado (o que ganhamos)

| Métrica | Hoje | Com Agentes | Ganho |
|---------|------|-------------|-------|
| Preparação do Comitê | 45-60min | < 5 min | ~90% mais rápido |
| Detecção de desvio de KPI | 3-5 dias | < 24h | ~80% mais rápido |
| Taxa de atas preenchidas | ~60% | > 95% | ~58% melhor |
| Abertura de FCA | 1-3 dias | Automático | Imediato |
| Atualização de OKRs | Manual semanal | Quinta 8h auto | Automático |
| Resposta a flag de churn | Semanas | 48-72h | ~90% mais rápido |
| Onboarding de pessoa nova | 1-2 semanas | < 2 dias | ~80% mais rápido |

**Frase de abertura:** "Coordenador, em 2 semanas eu entrego um agente que reduz o tempo de preparação do comitê de 45 minutos para 5 minutos. E ele não custa nada de inferência — US$ 0/mês em modelo. Você aprova a gente validar com as áreas?"

### Princípio 2: Mostre o problema antes da solução

**O problema real não é falta de capacidade — é escala:**
- Um humano dá conta de 1-2 clientes com excelência
- Com agentes, um humano orquestra 5-10 clientes
- A diferença não está no esforço, está na arquitetura

**O custo da operação manual:**
- Account passa 40% do tempo em tarefas repetitivas
- GT perde 2h/dia em relatórios manuais
- Copy refaz versões porque briefing se perdeu
- Design recebe demanda sem contexto

**80/20:** 20% dos processos consomem 80% do tempo operacional. São eles que atacamos primeiro.

### Princípio 3: Peça a ação específica

**O que estou pedindo:**
1. **30 minutos com cada área** para validar o que cada agente deve gerar
   - Account → validar check-in, mission control, flags
   - GT → validar relatórios, alertas, recomendações
   - Copy → validar pipeline de conteúdo, SEO
   - Design → validar briefing de assets, padrões visuais

2. **Acesso aos sistemas** (credenciais API)
   - Google Ads · Meta Ads · GA4 · Ekyte

3. **Go para o scaffold** — subir o agente Account/CSM na VPS como piloto

**Se eu tiver esses 3 itens, em 2 semanas o primeiro agente está produzindo.**

---

## 💰 Análise de Custo

### Custo de Inferência: US$ 0,00/mês

| Modelo | Provider | Custo | Uso |
|--------|----------|-------|-----|
| DeepSeek V4 Flash | OpenCode Zen | Grátis | Agentes principais (S) |
| Gemini 2.5 Flash | Google AI | Grátis | Geração visual (S) |
| GPT-OSS 120B | OpenRouter | Grátis | Orquestração (A) |
| MiniMax M2.5 | OpenCode Zen | Grátis | Tarefas rápidas (B) |
| Hermes 3 405B | OpenRouter | Grátis | Segunda opinião (A) |
| Nemotron 3 | OpenCode Zen | Grátis | Output estruturado (B) |

**Total inferência: US$ 0,00**

### Custo de Infraestrutura

| Item | Custo |
|------|-------|
| VPS (já existe) | ~US$ 15/mês |
| Domínio (já existe) | US$ 0 |
| Modelos IA | US$ 0 |
| **Total** | **~US$ 15/mês** |

### Retorno Potencial

| Ganho | Valor estimado |
|-------|---------------|
| 3h/semana de Account recuperadas | ~R$ 1.200/mês |
| Relatórios GT automatizados | ~R$ 800/mês |
| Pipeline de conteúdo sem gargalo | ~R$ 1.500/mês |
| Detecção precoce de churn (1 cliente retido) | R$ 5.000-15.000 |

---

## 🏗️ Arquitetura Técnica (para tech lead)

### Stack
- **Orquestrador:** OpenCode (na VPS)
- **Modelos:** OpenCode Zen + Google AI + OpenRouter (tudo free)
- **Automação:** n8n (workflows como código)
- **Dados:** Supabase + APIs (Google, Meta, Ekyte)
- **Interface:** Painel Lovable (HTML/JS)
- **Memória:** Vault Obsidian + mission-control

### Fluxo de Dados
```
Fontes Externas (Google Ads, Meta, GA4, Ekyte, Drive)
       ↓
n8n Workflows (coleta agendada / webhook)
       ↓
OpenCode Agents (processamento via skills V4)
       ↓
Output Estruturado (JSON / Markdown)
       ↓
Painel Lovable (visualização) + Mission Control (estado vivo)
```

### Hierarquia de Agentes (3 camadas)
```
Swarm (cmoorch) — visão geral, ROIs
  → Orquestradores (growth-team, content-studio, account-orchestrator)
    → Especialistas (12 agentes de domínio)
      → Skills (65+ instruções especializadas)
```

### Segurança e Governança
- Pesos e contrapesos: revisor valida antes de qualquer saída crítica
- Agentes de flag só diagnosticam — não executam ações
- Tudo roda na VPS local — dados não saem do controle da V4

---

## ⏳ Cronograma

| Fase | Duração | Marcos |
|------|---------|--------|
| **Fase 1:** Validação | Semana 1-2 | Sessões com Account, GT, Copy, Design |
| **Fase 2:** Agente Account/CSM | Semana 3-4 | Piloto produzindo |
| **Fase 3:** Demais agentes | Semana 5-8 | GT, Copy, Design ativos |
| **Fase 4:** Painel integrado | Semana 9-12 | Operação autônoma |

**Risco:** Atraso na validação das áreas. Mitigação: sessões de 30min, agendadas com antecedência.

---

## 📋 Script de Abertura (Dale Carnegie)

**Cenário:** Reunião com coordenador, 20 minutos, sala de reunião ou call.

**Abertura (1min):**
"Coordenador, obrigado pelo tempo. Eu quero te mostrar um sistema que a gente já construiu — não é promessa, já está rodando aqui no meu ambiente. Ele usa IA para automatizar tarefas repetitivas dos nossos times: Account, Tráfego, Copy e Design.

O melhor: não custa nada de inferência. Os modelos são todos gratuitos. O que eu preciso de você são 3 coisas simples que vou te mostrar agora."

**Corpo (15min):**
[Passar pelos slides 2-9 do deck]

**Fechamento (4min):**
"Resumindo: em 2 semanas o agente Account está produzindo. Custo zero de IA. O que eu preciso é:

1. Validar com as áreas (30min cada)
2. Acesso às APIs
3. Go para o scaffold

Pode ser?"

---

## ❓ Objeções Previstas e Respostas

### "Isso vai substituir as pessoas?"
**Não.** Cada agente é uma ferramenta que elimina o trabalho repetitivo que ninguém gosta de fazer. O Account deixa de preparar relatório manual e passa a orquestrar mais clientes. O GT deixa de copiar/colar dados e passa a analisar estratégia.

### "Quanto tempo até funcionar?"
**2 semanas para o primeiro agente.** O sistema todo (4 agentes + painel) em 12 semanas. Mas a primeira entrega — que já gera valor real — sai em 14 dias.

### "E se o modelo ficar caro?"
**Não fica.** Todos os modelos que usamos são gratuitos. DeepSeek V4, Gemini 2.5 Flash, GPT-OSS 120B — todos free tier ou OpenRouter gratuito. Não tem surpresa na conta.

### "Precisa de infraestrutura nova?"
**Não.** Roda na VPS que já temos. O OpenCode já está instalado. É só configurar os agentes.

### "Quem vai manter?"
**Eu.** O sistema foi desenhado para ser autossustentável: os próprios agentes documentam e reportam status. Manutenção é < 2h/semana.

---

## 🏁 Checklist Pré-Apresentação

- [ ] Deck HTML aberto e testado no navegador
- [ ] Site agents-hub.html acessível para mostrar detalhes
- [ ] Documento de lógica impresso ou em segunda tela
- [ ] Cronograma definido com as 4 fases
- [ ] Respostas para objeções decoradas
- [ ] Pedido claro: 3 ações específicas
