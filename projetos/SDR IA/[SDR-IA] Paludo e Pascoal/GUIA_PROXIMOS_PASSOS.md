# SDR IA — Paludo & Pascoal Advogados

## Guia de Implementação e Próximos Passos

---

## Sumário

1. [Arquitetura da Solução](#1-arquitetura-da-solução)
2. [Modelo de IA Recomendado](#2-modelo-de-ia-recomendado)
3. [Pré-requisitos de Infraestrutura](#3-pré-requisitos-de-infraestrutura)
4. [Passo a Passo de Configuração](#4-passo-a-passo-de-configuração)
5. [Workflows n8n](#5-workflows-n8n)
6. [Estrutura de Dados (Supabase)](#6-estrutura-de-dados-supabase)
7. [Integração Kommo CRM](#7-integração-kommo-crm)
8. [Estratégia de Follow-up](#8-estratégia-de-follow-up)
9. [Checklist de Qualidade](#9-checklist-de-qualidade)
10. [Métricas e Monitoramento](#10-métricas-e-monitoramento)
11. [Próximos Passos Cronológicos](#11-próximos-passos-cronológicos)

---

## 1. Arquitetura da Solução

```
┌─────────────────────────────────────────────────────────────────┐
│                    LEAD (Formulário + WhatsApp)                  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                     WhatsApp Cloud API                          │
│              (webhook recebe mensagens do lead)                  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    n8n — SDR IA Principal                        │
│                                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────┐   │
│  │ Normaliza │─▶│  Busca   │─▶│  Buffer  │─▶│   Agente GPT  │   │
│  │  Payload  │  │ Supabase │  │  Redis   │  │  4o Matheus   │   │
│  └──────────┘  └──────────┘  └──────────┘  └───────┬───────┘   │
│                                                     │           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │           │
│  │ Kommo    │◀─│   QA     │◀─│  Salva   │◀─────────┘           │
│  │ CRM      │  │ GPT-4o   │  │ Histórico│                      │
│  └──────────┘  └──────────┘  └──────────┘                      │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              n8n — Gerenciador Follow-up (4h)                    │
│                                                                  │
│  Schedule (5min) → Busca leads sem resposta >4h → AI gera       │
│  follow-up → Envia WhatsApp → Marca no Supabase                 │
└─────────────────────────────────────────────────────────────────┘
```

### Decisões de Arquitetura

| Decisão | Escolha | Motivo |
|---------|---------|--------|
| Modelo principal | **GPT-4o** (temp 0.2) | Conteúdo técnico-jurídico exige precisão; temperatura baixa garante consistência |
| Modelo QA | **GPT-4o** (temp 0.1) | Decisão binária (MQL ou não) precisa de determinismo |
| Modelo Follow-up | **GPT-4o-mini** (temp 0.5) | Tarefa simples de reengajamento, não justifica custo do 4o |
| Memória conversacional | **Redis** (buffer curto) + **Supabase** (histórico persistente) | Redis para debounce de mensagens; Supabase para histórico completo |
| CRM | **Kommo** | Definido no briefing do cliente |
| Canal de entrada | **WhatsApp Cloud API** + **Webhook de formulário** | Lead chega via formulário e continua no WhatsApp |
| Tratamento de áudio | **OpenAI Whisper** (transcrição) | Leads podem enviar áudio |
| Tratamento de imagem | **GPT-4o Vision** (análise) | Leads podem enviar prints de notas fiscais, documentos |

---

## 2. Modelo de IA Recomendado

### GPT-4o — SDR Principal (Matheus)

**Parâmetros:**
- Modelo: `gpt-4o`
- Temperatura: `0.2`
- Max tokens: `1024`
- System prompt: `prompt-sdr-mattheus.txt`

**Por que GPT-4o em vez de GPT-4.1 mini?**
- O conteúdo tributário (Reforma Tributária, Transfer Pricing OCDE, Lei 14.596/23) exige precisão técnica
- O tom formal e profissional para executivos C-Level requer sofisticação linguística
- A matriz de objeções (4 cenários) precisa ser aplicada com discernimento contextual
- O GPT-4o-mini tende a simplificar demais conceitos jurídico-tributários

**Por que não GPT-4.1?**
- Custo 2-3x maior que GPT-4o sem ganho perceptível para este caso de uso
- A temperatura baixa (0.2) no GPT-4o já garante a consistência necessária

### GPT-4o — QA/MQL Agent

**Parâmetros:**
- Modelo: `gpt-4o`
- Temperatura: `0.1`
- Max tokens: `512`
- System prompt: `prompt-qa-mql.txt`

**Função:** Analisar o histórico da conversa e decidir se o lead atingiu os 4 pilares BANT.

### GPT-4o-mini — Follow-up

**Parâmetros:**
- Modelo: `gpt-4o-mini`
- Temperatura: `0.5`
- Max tokens: `256`

**Função:** Gerar mensagem curta de reengajamento para leads que pararam de responder.

---

## 3. Pré-requisitos de Infraestrutura

### 3.1 Contas e Serviços

| Serviço | Finalidade | Status |
|---------|-----------|--------|
| OpenAI API | Modelo GPT-4o (SDR + QA + Follow-up) | ⬜ Pendente |
| Supabase | Banco de dados (leads, chat_history) | ⬜ Pendente |
| Redis | Buffer de mensagens (debounce) | ⬜ Pendente |
| WhatsApp Cloud API | Canal de conversa com leads | ⬜ Pendente |
| Kommo API | CRM destino dos leads | ⬜ Pendente |
| Evolution API | Bridge WhatsApp (se usar instância própria) | ⬜ Pendente |
| n8n | Orquestrador dos workflows | ⬜ Pendente |

### 3.2 Credenciais Necessárias

```
OPENAI_API_KEY=sk-...
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_KEY=eyJ...
REDIS_HOST=...
REDIS_PORT=6379
REDIS_PASSWORD=...
WHATSAPP_TOKEN=EAAT...
WHATSAPP_PHONE_NUMBER_ID=123456789
KOMMO_ACCESS_TOKEN=...
KOMMO_DOMAIN=https://xxx.kommo.com
```

---

## 4. Passo a Passo de Configuração

### 4.1 Supabase — Criar Tabelas

```sql
-- Tabela de Leads
CREATE TABLE paludo_leads (
  id BIGSERIAL PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  nomeCliente TEXT,
  telefoneCliente TEXT UNIQUE,
  sessionID TEXT,
  idMensagem TEXT,
  bitrix_id TEXT,
  lead_created_in_crm BOOLEAN DEFAULT FALSE,
  last_interaction_at TIMESTAMPTZ,
  followup_enviado BOOLEAN DEFAULT FALSE,
  followup_enviado_at TIMESTAMPTZ
);

-- Tabela de Histórico de Chat
CREATE TABLE paludo_chat_history (
  id BIGSERIAL PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  session_id TEXT,
  role TEXT,
  content TEXT
);

CREATE INDEX idx_paludo_chat_session ON paludo_chat_history(session_id);
CREATE INDEX idx_paludo_leads_telefone ON paludo_leads(telefoneCliente);
```

### 4.2 n8n — Importar Workflows

1. Abra o n8n no navegador
2. Vá em **Workflows** → **Import from File**
3. Importe `workflow-sdr-principal.n8n.json`
4. Importe `workflow-followup.n8n.json`
5. Configure as credenciais em cada nó:
   - **OpenAI**: API Key da OpenAI
   - **Supabase**: URL + Service Key
   - **Redis**: Host + Port + Password
   - **WhatsApp**: Token + Phone Number ID
   - **Kommo**: Access Token + Domain

### 4.3 WhatsApp Cloud API — Setup

1. Crie um aplicativo no [Meta for Developers](https://developers.facebook.com/)
2. Configure o webhook para apontar para o n8n
3. Adicione o número de telefone da Paludo
4. Gere o token de acesso permanente

### 4.4 Kommo CRM — Configurar Pipelines

1. Criar **Funil "Vendas"** com etapa "MQL Qualificados" (pipeline_id: 1)
2. Criar **Funil "SDR IA"** com etapa "Desqualificados" (pipeline_id: 2)
3. Criar campos customizados para:
   - `produto_interesse` (lista: Reforma Tributária / Preços de Transferência / Revisão Fiscal)
   - `regime_tributario` (texto)
   - `faturamento_estimado` (texto)

---

## 5. Workflows n8n

### 5.1 Workflow 1: SDR IA Principal

**Arquivo:** `workflow-sdr-principal.n8n.json`

| Etapa | Nó | Descrição |
|-------|-----|-----------|
| 1 | **WhatsApp Trigger** | Recebe mensagens do lead via webhook |
| 2 | **camposIniciais** | Normaliza payload (telefone, nome, tipo de mensagem) |
| 3 | **Switch Tipo Mensagem** | Roteia por tipo (texto, áudio, imagem) |
| 4 | **Buscar Lead no Supabase** | Verifica se lead já existe |
| 5 | **Lead Existe?** | Se não: cria lead + UUID. Se sim: segue |
| 6 | **Empilha Mensagem (Redis)** | Adiciona ao buffer de debounce |
| 7 | **Obtem Buffer (Redis)** | Recupera mensagens empilhadas |
| 8 | **Debounce Switch** | Verifica se passou o tempo de debounce |
| 9 | **Messages Set** | Prepara histórico para o agente |
| 10 | **Formatar Historico** | Código JS que monta o histórico legível |
| 11 | **Matheus - SDR IA** | Agente principal (GPT-4o com prompt completo) |
| 12 | **Salvar Msg IA** | Persiste resposta no Supabase |
| 13 | **Enviar WhatsApp** | Envia resposta para o lead |
| 14 | **Atualizar Lead** | Atualiza timestamp de interação |
| 15 | **QA - MQL Agent** | Avalia se lead é MQL (BANT) |
| 16 | **Parse JSON QA** | Extrai JSON estruturado da resposta da QA |
| 17 | **Eh MQL?** | Roteia MQL vs não-MQL |
| 18 | **Enviar MQL para Kommo** | Cria lead no funil Vendas com tag "SDR IA" |
| 19 | **Enviar Nao-MQL para Kommo** | Cria lead no funil SDR IA com tag de motivo |

### 5.2 Workflow 2: Gerenciador Follow-up 4h

**Arquivo:** `workflow-followup.n8n.json`

| Etapa | Nó | Descrição |
|-------|-----|-----------|
| 1 | **Schedule Trigger** | Executa a cada 5 minutos |
| 2 | **Buscar Todos Leads** | Puxa todos os leads do Supabase |
| 3 | **Filtrar com Timestamp** | Mantém só quem tem last_interaction_at |
| 4 | **Filtrar >4h sem followup** | Leads sem interação há >4h e sem followup enviado |
| 5 | **Set Followup Flag** | Marca followup = true |
| 6 | **AI Follow-up** | Gera mensagem de reengajamento (GPT-4o-mini) |
| 7 | **Enviar Follow-up WhatsApp** | Envia mensagem via Evolution API |
| 8 | **Marcar Follow-up Enviado** | Atualiza Supabase com timestamp |

---

## 6. Estrutura de Dados (Supabase)

### Schema: `paludo_leads`

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id | BIGSERIAL PK | ID interno |
| created_at | TIMESTAMPTZ | Data de criação |
| nomeCliente | TEXT | Nome do lead |
| telefoneCliente | TEXT UNIQUE | Telefone (chave de busca) |
| sessionID | TEXT | ID da sessão (UUID) |
| idMensagem | TEXT | ID da última mensagem |
| lead_created_in_crm | BOOLEAN | Se já foi enviado ao Kommo |
| kommo_lead_id | TEXT | ID do lead no Kommo |
| last_interaction_at | TIMESTAMPTZ | Última interação |
| followup_enviado | BOOLEAN | Se follow-up foi enviado |
| followup_enviado_at | TIMESTAMPTZ | Quando o follow-up foi enviado |

### Schema: `paludo_chat_history`

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id | BIGSERIAL PK | ID interno |
| created_at | TIMESTAMPTZ | Data da mensagem |
| session_id | TEXT | Sessão do lead |
| role | TEXT | "human" ou "ai" |
| content | TEXT | Conteúdo da mensagem |

---

## 7. Integração Kommo CRM

### Tags Automáticas

| Situação | Tag(s) | Funil | Etapa |
|----------|--------|-------|-------|
| Lead qualificado (MQL) | `SDR IA` | Vendas | MQL Qualificados |
| Fora do ICP | `SDR IA`, `#IA_ForaDoICP` | SDR IA | Desqualificados |
| Sem interesse | `SDR IA`, `#IA_SemInteresse` | SDR IA | Desqualificados |
| Contato inválido | `SDR IA`, `#IA_ContatoInvalido` | SDR IA | Desqualificados |

### Nota Interna no Card (MQL)

Quando o lead é qualificado, a SDR IA insere no card do Kommo uma nota estruturada:

```
[SDR IA] Lead qualificado via automação

Resumo da Qualificação:
- Nome: {nome}
- Produto de Interesse: {produto}
- Regime Tributário: {regime}
- Faturamento Estimado: {faturamento}
- Prazo: {timing}
- Objeções: {objeções}
- Observações: {observações}

Histórico completo disponível no Supabase (session_id: {sessionID})
```

---

## 8. Estratégia de Follow-up

### Configuração Atual

| Parâmetro | Valor |
|-----------|-------|
| Delay | 4 horas |
| Modelo | GPT-4o-mini (temp 0.5) |
| Tom | Formal, profissional, reengajamento sutil |

### Mensagem Base

```
Olá {nome}, tudo bem? Aqui é o Matheus da Paludo & Paschoal Advogados.
Imagino que esteja ocupado(a). Quando puder, estou à disposição para
retomarmos nossa conversa sobre as soluções fiscais para a sua empresa.
Aguardamos seu retorno!
```

### Evolução Futura (Recomendada)

Após validar o primeiro follow-up de 4h, implementar uma sequência:

| Follow-up | Delay | Estratégia |
|-----------|-------|------------|
| 1º | 4h | Reengajamento sutil |
| 2º | 24h | Novo valor (artigo, insight sobre Reforma) |
| 3º | 72h | Oferta de análise preliminar gratuita |
| Final | 7 dias | Mensagem de encerramento |

---

## 9. Checklist de Qualidade

### Antes de Publicar

- [ ] Prompt do Matheus carregado corretamente no n8n
- [ ] Anti-alucinação testada: perguntar "quanto custa?" deve bloquear
- [ ] BANT testado: lead com todos os 4 pilares vira MQL
- [ ] BANT testado: lead sem 1 pilar é desqualificado com tag correta
- [ ] Matriz de objeções testada: cada objeção tem resposta adequada
- [ ] Integração Kommo: lead MQL chega no funil correto
- [ ] Integração Kommo: lead não-MQL chega no funil SDR IA com tag
- [ ] Debounce funcionando: mensagens seguidas são agrupadas
- [ ] Histórico salvando: chat_history no Supabase
- [ ] Follow-up: após 4h sem resposta, mensagem é enviada
- [ ] Áudio: transcrição funcionando
- [ ] Imagem: análise de imagem funcionando (se aplicável)

### Testes de Conversa

```
Teste 1: Lead qualificado (MQL)
  - Empresa de grande porte, Lucro Real, CFO
  - Interesse em Reforma Tributária
  - Prazo: 60 dias
  → Deve virar MQL, ir para funil Vendas

Teste 2: Lead desqualificado (Fora do ICP)
  - Empresa pequena, Simples Nacional, auxiliar administrativo
  → Deve ir para funil SDR IA com #IA_ForaDoICP

Teste 3: Tentativa de preço
  - "Quanto custa a consultoria?"
  → Matheus deve responder "sob consulta" sem passar valor

Teste 4: Objeção BIG4
  - "Já trabalhamos com a PwC"
  → Matheus deve validar e explicar diferencial boutique
```

---

## 10. Métricas e Monitoramento

### KPIs da SDR IA

| Métrica | Fórmula | Meta |
|---------|---------|------|
| Taxa de Qualificação | MQLs / Total Leads | > 30% |
| Taxa de Conversão MQL→Reunião | Reuniões / MQLs | > 50% |
| Tempo Médio de Qualificação | Tempo até MQL | < 10 min |
| Taxa de Reengajamento (Follow-up) | Respostas / Follow-ups enviados | > 20% |
| Taxa de Acerto BANT | Precisão da QA ao classificar MQL | > 90% |

### Dashboards Sugeridos

1. **n8n**: Ativação de logs por workflow
2. **Supabase**: Queries de contagem de leads por status
3. **Kommo**: Relatório de pipeline "SDR IA" vs "Vendas"
4. **OpenAI**: Dashboard de uso de tokens (cost tracking)

---

## 11. Próximos Passos Cronológicos

### Fase 1: Setup de Infraestrutura (Dias 1-2)

| # | Tarefa | Responsável |
|---|--------|-------------|
| 1.1 | Criar projeto Supabase + tabelas SQL | Dev |
| 2.1 | Configurar Redis | Dev |
| 3.1 | Gerar API Key OpenAI | Dev |
| 4.1 | Configurar WhatsApp Cloud API + webhook | Dev |
| 5.1 | Configurar Kommo API + pipelines | Dev |
| 6.1 | Instalar n8n (se necessário) | Dev |

### Fase 2: Configurar Workflows (Dias 3-4)

| # | Tarefa | Responsável |
|---|--------|-------------|
| 2.1 | Importar `workflow-sdr-principal.n8n.json` no n8n | Dev |
| 2.2 | Configurar credenciais em cada nó | Dev |
| 2.3 | Importar `workflow-followup.n8n.json` | Dev |
| 2.4 | Configurar credenciais do follow-up | Dev |
| 2.5 | Ajustar prompts com dados finais da Paludo | Account |

### Fase 3: Testes e Validação (Dias 5-6)

| # | Tarefa | Responsável |
|---|--------|-------------|
| 3.1 | Rodar checklist de qualidade | QA |
| 3.2 | Testar fluxo completo (formulário → WhatsApp → MQL → Kommo) | Account |
| 3.3 | Testar matriz de objeções | Account |
| 3.4 | Testar follow-up automático | Account |
| 3.5 | Validar anti-alucinação | QA |

### Fase 4: Deploy (Dia 7)

| # | Tarefa | Responsável |
|---|--------|-------------|
| 4.1 | Ativar webhook de produção | Dev |
| 4.2 | Ativar schedule de follow-up | Dev |
| 4.3 | Monitorar primeiras 24h de conversas | Account |
| 4.4 | Ajustar prompt conforme interações reais | Account |

### Fase 5: Otimização Contínua (Semanas 2-4)

| # | Tarefa | Frequência |
|---|--------|------------|
| 5.1 | Revisar taxa de acerto BANT | Semanal |
| 5.2 | Ajustar temperatura do modelo | Quinzenal |
| 5.3 | Expandir matriz de objeções | Mensal |
| 5.4 | Implementar follow-up escalonado (2º e 3º) | Mensal |
| 5.5 | Criar dashboard de métricas | Quinzenal |

---

## Arquivos do Projeto

```
[SDR-IA] Paludo e Pascoal/
├── Construção do Briefing Paludo.pdf      ← Briefing original
├── prompt-sdr-mattheus.txt                ← System prompt do agente principal
├── prompt-qa-mql.txt                      ← System prompt do QA/MQL
├── workflow-sdr-principal.n8n.json        ← Workflow principal (n8n)
├── workflow-followup.n8n.json             ← Workflow de follow-up (n8n)
└── GUIA_PROXIMOS_PASSOS.md               ← Este guia
```

---

## Contatos e Suporte

**Dúvidas técnicas (n8n, Supabase, API):** Dev responsável
**Dúvidas de negócio (briefing, objeções, ICP):** Account responsável
**Dúvidas de conteúdo tributário:** Sócios da Paludo & Paschoal
