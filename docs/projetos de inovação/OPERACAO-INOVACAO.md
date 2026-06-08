# Incorporação de Inovação na Operação Peretto e Co

> Como os 45 projetos pesquisados viram ferramentas reais no dia a dia.
> Baseado no MANUAL_DE_USO.md — fluxos de segunda, quinta, QBR e emergência.

---

## 1. Lógica: Produto vs Ferramenta Interna

A recomendação anterior (CONCLUSAO-RECOMENDACAO.md) focou em **produtos para vender**. Aqui o foco é outro: **ferramentas para incorporar na operação** — que aumentam a capacidade de entrega, reduzem trabalho manual e melhoram a qualidade do que a Peretto já faz.

Cada projeto abaixo foi mapeado contra UM fluxo específico do manual. Se não encaixa, não está aqui.

---

## 2. Mapeamento: Fluxo do Manual vs Projetos do Catálogo

### 2.1 Segunda — Briefing do Comitê

**Hoje:** `@executor-comite` gera briefing com OKRs, sprints, FCAs, flags.

**O que incorporar:**

| Projeto | Encaixe | ROI direto |
|---------|---------|------------|
| **Drift** (intel competitiva) | Alimenta o briefing com "o que mudou nos concorrentes essa semana" — pricing, changelog, hiring, blog. Entrega via Slack/Email automático. | Briefing mais completo sem trabalho extra. Cliente percebe que a Peretto "sabe de tudo". |
| **Marketing Brain (MCP Server)** | Persistência de memória de marketing. O briefing não começa do zero toda semana — o sistema sabe o que foi discutido, decidido e entregue. | Elimina repetição. O @executor-comite passa a ter contexto contínuo. |
| **Competitor Monitor** (monitoramento semântico) | Detecta mudanças estratégicas em concorrentes (não só typos). Flags automáticas: "Concorrente X mudou posicionamento." | Alerta proativo. A Peretto avisa o cliente antes de ele descobrir sozinho. |

**Como implementar (2-3 dias):**
```
1. Deploy do Drift em Docker → aponta para 5 concorrentes dos principais clientes
2. Configurar output do Drift como feed pro @executor-comite
3. Marketing Brain → instalar como MCP server no OpenCode (já usa MCP)
4. Competitor Monitor → deploy + conectar ao n8n para disparar alerts no briefing
```

---

### 2.2 Quinta — Flags + OKRs

**Hoje:** `detector_flags.py` → `@flag-roi` / `@flag-churn` / `@flag-okr` / `@flag-operacao` → `@csm` triage.

**O que incorporar:**

| Projeto | Encaixe | ROI direto |
|---------|---------|------------|
| **Mureo** (AI agent para contas de anúncio) | Quando `@flag-roi` acusa ROAS baixo, Mureo já puxa os dados da conta (Meta Ads + Google Ads + GA4) e gera um plano de ação específico. | Fecha o loop: diagnóstico → ação. Em vez de "ROAS caiu" → "ROAS caiu porque o CPA do público X subiu 40% — sugestão: pausar público X e realocar verba para Y." |
| **Full-Funnel AI Analytics** (consulta em linguagem natural) | Substitui a leitura manual do JSON do `@analista-dados`. Em vez de "analisa esses dados", pergunta "por que meu CPA subiu?" e recebe resposta em português com dados. | Reduz tempo de análise em 70%. Qualquer membro da equipe consegue extrair insights, não só analistas. |
| **Competitor Monitor** | Adiciona "flag de concorrente" ao ecossistema de flags. Se um concorrente mudou pricing, a operação é alertada. | Nova dimensão de inteligência. Antes não existia alerta de concorrência. |

**Como implementar (1 semana):**
```
1. Mureo → setup + conectar ao output do @flag-roi via n8n
2. Full-Funnel AI Analytics → deploy Docker + conectar às fontes de dados existentes
3. Integrar output do Mureo como campo "recommended_actions" no JSON do @analista-dados
```

**Exemplo de fluxo novo (Quinta-feira com Mureo):**

```
7h → detector_flags.py identifica ROAS baixo no cliente X
7h05 → @flag-roi diagnostica: "CPA elevado, não CVR"
7h10 → Mureo puxa dados da conta Meta Ads do cliente X
7h15 → Mureo gera: "Anúncio A (público 25-35, SP) tem CPA 80% acima da média. Sugiro pausar e realocar para público 35-45, que tem CPA 30% menor."
7h20 → @csm valida e envia para o GT executar
```

**Tempo economizado por flag:** ~2h de análise manual que vira 10min de validação.

---

### 2.3 QBR (Quarterly)

**Hoje:** `@csm` → `@analista-dados` → `@revisor` → `@gerar-ppt` → `@csm` prepara roteiro.

**O que incorporar:**

| Projeto | Encaixe | ROI direto |
|---------|---------|------------|
| **Tech Analyst** (Magic Quadrant automático) | Gera visuais Gartner-style que mostram onde o cliente está vs concorrentes. Entra no deck do QBR. | QBR vira material de consultoria de alto nível. Cliente vê a Peretto como parceiro estratégico, não só executor. |
| **CompetitorScope** (análise multi-agent) | Roda pesquisa competitiva completa (Planner → Collector → Analyst → Comparator → Writer) e gera relatório Markdown. Entra como seção do QBR. | Relatório de concorrência que antes levava 1 semana para ser feito, sai em 2h. |
| **Prism** (inteligência de produto) | Adiciona análise de indústria e tendências de mercado ao QBR. | Transforma QBR de "relatório de números" em "análise estratégica do mercado". |

**Como implementar (1 semana):**
```
1. Tech Analyst → deploy + configurar para os setores dos clientes
2. CompetitorScope → deploy + alimentar com URLs dos concorrentes de cada cliente
3. Criar template de QBR que inclui seções "Mercado" e "Concorrência" alimentadas por esses projetos
```

---

### 2.4 Criação de Conteúdo Sob Demanda

**Hoje:** `@analista-dados` → `@revisor` → `@gerar-pdf` / `@gerar-ppt` / `@gerar-doc`.

**O que incorporar:**

| Projeto | Encaixe | ROI direto |
|---------|---------|------------|
| **Marketing Engine** (pipeline de conteúdo) | Pipeline provider-agnostic: brief → script → creative → caption → compliance → publish → metrics → ads. Roda como workflow no n8n. | Criação de conteúdo que antes levava 1 dia, sai em 1h com revisão. O pipeline força consistência: tudo passa por compliance antes de ir pro cliente. |
| **Landing Page Factory** (fábrica de LPs) | Extract → Strategize → Profile → Write → Visual → Build → QA → Ship. Pipeline completo que usa dados reais do cliente. | Landing page que levava 3 dias, sai em 4h. Estratégia-first: não é "fazer uma LP", é "extrair dados → definir estratégia → criar → publicar". |
| **Shippage** (copy de conversão com 1000+ fórmulas) | Geração de copy de LP com 1000+ fórmulas A/B testadas. Popups exit-intent, LGPD, schema SEO. | Copywriter não precisa começar do zero. A IA gera as variações, o humano escolhe a melhor e ajusta. |
| **MiCA** (campanha multicanal em 5min) | Descreve o negócio uma vez → campanha multicanal (email, WhatsApp, Instagram, vídeo avatar AI). | Para clientes menores ou campanhas de baixa complexidade. Substitui 4 horas de criação por 20 minutos. |

**Como implementar (2-3 semanas):**
```
1. Marketing Engine → instalar como workflow n8n + templates de prompt para cada etapa
2. Landing Page Factory → deploy + configurar pipeline para usar dados de clientes existentes
3. Shippage → usar como skill do OpenCode (integra com @gerar-html)
4. MiCA → deploy + testar com 1 cliente piloto
```

**Pipeline novo de criação de conteúdo:**

```
Brief do cliente (em linguagem natural)
  → Marketing Engine transforma em brief estruturado
  → IA gera script + criativo + legenda + compliance check
  → Humano revisa (tempo gasto: 15 min)
  → Publica automático (n8n dispatch)
  → Métricas voltam para o Superset
```

---

### 2.5 Emergência — Flag Crítica 🔴

**Hoje:** `@flag-roi` / `@flag-churn` → `@revisor` → `@csm` → `@gerar-doc` (FCA).

**O que incorporar:**

| Projeto | Encaixe | ROI direto |
|---------|---------|------------|
| **Mureo** | Quando flag 🔴 de ROAS, Mureo já entrega o plano de ação junto com o diagnóstico. A FCA já sai com ações concretas, não só com a descrição do problema. | Tempo de resposta cai de horas para minutos. O GT recebe diagnóstico + plano de ação no mesmo pacote. |
| **Garnet AI** (marketing advisor autônomo) | 5 especialistas AI analisam o problema de ângulos diferentes (dados, conteúdo, CRO, psicologia, estratégia). A FCA ganha profundidade. | Decisão mais embasada. Não é só "o que fazer", é "por que fazer e qual o impacto esperado". |
| **Competitor Hunter** | Se a flag for de churn, o Competitor Hunter verifica se o concorrente fez algo (lançou feature, mudou preço). | Impede ação errada: se o churn for por pressão competitiva, a resposta é diferente de churn por insatisfação. |

**Como implementar (3-4 dias):**
```
1. Criar workflow n8n: flag 🔴 → invoca Mureo + Garnet AI em paralelo
2. Output consolidado: diagnóstico + plano de ação + análise de concorrência
3. Template de FCA já preenchido com esses dados
```

---

## 3. Matriz: Esforço de Incorporação vs Impacto Operacional

Projeto | Esforço setup | Impacto operacional | Onde encaixa | Vai gerar receita?
--------|-------------|-------------------|-------------|-------------------
**Drift** | 2-3h | ⭐⭐⭐ Médio | Briefing segunda | ✅ Sim (inteligência como serviço)
**Marketing Brain** | 4h | ⭐⭐⭐⭐⭐ Altíssimo | Toda operação | ❌ Interno (multiplicador)
**Competitor Monitor** | 1 dia | ⭐⭐⭐ Médio | Flags + briefing | ✅ Sim (monitoria)
**Mureo** | 2-3 dias | ⭐⭐⭐⭐⭐ Altíssimo | Flags + emergência | ❌ Interno (fecha loop ação)
**Full-Funnel AI Analytics** | 2 dias | ⭐⭐⭐⭐ Alto | Análise diária | ✅ (pode virar produto)
**Marketing Engine** | 3-4 dias | ⭐⭐⭐⭐⭐ Altíssimo | Criação conteúdo | ❌ Interno (acelera entrega)
**Landing Page Factory** | 2 dias | ⭐⭐⭐⭐ Alto | Criação LP | ✅ Sim (fábrica de LPs)
**Shippage** | 1 dia | ⭐⭐⭐ Médio | Copy LP | ✅ Sim (copy IA)
**Tech Analyst** | 1 dia | ⭐⭐⭐ Médio | QBR | ❌ Interno (eleva qualidade)
**CompetitorScope** | 2 dias | ⭐⭐⭐⭐ Alto | QBR + pesquisas | ✅ (pesquisa competitiva)
**MiCA** | 2-3 dias | ⭐⭐ Baixo | Conteúdo rápido | ✅ (campanhas para clientes)
**Garnet AI** | 3-4 dias | ⭐⭐⭐⭐ Alto | Emergência + análise | ❌ Interno (advisor)
**Prism** | 2 dias | ⭐⭐⭐ Médio | QBR + pesquisa | ✅ (inteligência de mercado)

---

## 4. Plano de Incorporação (30 dias)

### Semana 1: Fundação (ROI imediato, < R$ 200)

```
Dia 1: Marketing Brain (MCP Server)
  → Instala como MCP server no OpenCode
  → Todo insight/decidido fica persistente
  → Impacto: @executor-comite passa a ter memória

Dia 2: Drift
  → Deploy Docker + configurar 5 concorrentes
  → Configurar entrega por email (já faz parte do briefing de segunda)

Dia 3: Full-Funnel AI Analytics
  → Deploy + conectar às fontes de dados já usadas
  → Testar: "por que o ROAS do cliente X caiu essa semana?"

Dia 4-5: Testar o novo fluxo de quinta
  → @flag-roi → Mureo (output: diagnóstico + ação)
  → Competitor Monitor (output: flag de concorrência)
```

### Semana 2: Criação de Conteúdo (multiplicador de entrega)

```
Dia 6-7: Marketing Engine
  → Instalar como workflow n8n
  → Criar template: brief → script → creative → caption → compliance

Dia 8-9: Shippage + Landing Page Factory
  → Deploy + testar com 1 LP real para cliente existente
  → Medir: tempo antes (3 dias) vs depois (4h)

Dia 10: Treinar a equipe
  → "Em vez de pedir 'cria uma LP', peça 'roda a Landing Page Factory para o cliente X'"
```

### Semana 3-4: Qualidade e QBR

```
Dia 11-14: CompetitorScope + Tech Analyst
  → Preparar materiais para o próximo QBR
  → Gerar Magic Quadrant + análise competitiva

Dia 15-20: Mureo + Garnet AI
  → Integrar com o sistema de flags
  → Testar em cenário real: flag 🔴 → Mureo diagnostica → Garnet valida → FCA gerada

Dia 21-30: Documentar e medir
  → Quanto tempo foi economizado?
  → Quanto conteúdo foi gerado?
  → Clientes perceberam diferença?
  → Decidir: quais viram produto vendável?
```

---

## 5. Exemplos Concretos de ROI (Baseados na Operação Real)

### Exemplo 1: Briefing de segunda com Drift

**Antes:** O briefing de segunda tem dados de OKRs e flags. Não tem inteligência de mercado.

**Depois:** O briefing inclui "O que mudou nos concorrentes essa semana" — automático, sem trabalho humano.

**ROI:** Cliente liga segunda "vi que meu concorrente lançou X" e a Peretto já sabe porque o Drift capturou. Isso é percepção de valor que justifica aumento de contrato.

### Exemplo 2: Flag de ROAS com Mureo

**Antes:** @flag-roi diagnostica → humano abre a conta → analisa → gera plano → leva 2h.

**Depois:** @flag-roi diagnostica → Mureo puxa dados → gera plano → humano valida em 10min.

**ROI:** 1h50 de analista por flag. Com 4 flags/semana = 7h20 economizadas = ~R$ 1.800/mês em horas liberadas.

### Exemplo 3: Landing Page com Landing Page Factory

**Antes:** Designer cria LP em 3 dias + copywriter faz copy em 1 dia = 4 dias.

**Depois:** Pipeline roda em 4h + humano revisa em 2h = 6h.

**ROI:** De 4 dias para 6h. Libera designer e copywriter para tarefas mais estratégicas. Cliente recebe LP em 1 dia em vez de 1 semana.

### Exemplo 4: Marketing Engine para conteúdo de redes

**Antes:** Social media produz 1 post/hora. 5 posts/dia = 5h.

**Depois:** Marketing Engine gera 5 posts em 20min. Humano revisa em 30min. Total 50min.

**ROI:** 4h10 economizadas por dia por social media = ~R$ 4.000/mês por profissional.

---

## 6. Riscos de Incorporação (Reais)

### Risco 1: "Mais uma ferramenta que ninguém usa"

Projetos open-source bonitos mas abandonados depois de 1 semana.

**Mitigação:** Só incorporar se encaixar em UM fluxo específico do manual. Se não encaixa, não instala. Drift encaixa no briefing de segunda. Mureo encaixa na flag de ROAS. Marketing Engine encaixa na criação de conteúdo.

### Risco 2: "Queueu deu erro e ninguém percebeu"

Projetos pequenos podem parar de funcionar sem aviso.

**Mitigação:** Todos os projetos rodam atrás do n8n com retry + alerta. Se o Drift não rodar, dá notificação no Slack. Se o Mureo quebrar, a flag volta ao processo manual.

### Risco 3: "A equipe não confia no output da AI"

Gente acostumada a fazer manualmente não vai delegar para uma AI de primeira.

**Mitigação:** Incorporação gradual. Semana 1: só usar como sugestão (humano decide). Semana 3: confiança aumentou, usar como recomendação com revisão. Mês 2: fluxo normal.

---

## 7. Resumo: O Que Fazer Segunda

```
□ Instalar Marketing Brain (MCP Server) → 4h, impacto imediato na memória da operação
□ Fazer deploy do Drift → 3h, briefing de segunda já na próxima semana
□ Instalar Mureo → 2 dias, quinta de flags já com plano de ação
□ Marketing Engine → 3-4 dias pipeline de conteúdo rodando em n8n
```

**Ordem:** Marketing Brain (hoje) → Drift (amanhã) → Mureo (essa semana) → Marketing Engine (semana que vem).

**Custo total para incorporar tudo:** R$ 0 de software (open-source). ~R$ 100/mês de servidor adicional. ~R$ 50/mês de APIs (Drift usa Gemini, que é grátis no tier atual).

---

> **Documento criado em:** 26/05/2026
> **Baseado em:** MANUAL_DE_USO.md (rotinas de segunda, quinta, QBR, emergência)
> **Catálogo de origem:** README.md (45 projetos)
> **Diferença da CONCLUSAO-RECOMENDACAO.md:** Lá são produtos para vender. Aqui são ferramentas para operar.
