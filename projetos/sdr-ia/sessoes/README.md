# Sessões SDR IA — Builders Hub V4

> Conversa original: Claude Compartilhar — Histórico completo de 16/jun a 24/jun/2026
> Clientes cobertos: **ADPLAN**, **SIGNOR**, **SCHWALM (Maia)**, **GENICS (Vitória)**
> Foco: Diagnóstico e correção de workflows n8n de SDR IA (WhatsApp → IA → CRM)

---

## Estrutura

```
Sessões SDR IA/
├── README.md                   ← Este arquivo (visão geral, resoluções, pendências)
├── TRANSCRICAO_COMPLETA.md     ← Histórico integral da conversa
├── ADPLAN/
│   └── resumo.md               ← Problemas, correções, status da ADPLAN
├── SIGNOR/
│   └── resumo.md               ← Problemas, correções, status da SIGNOR
├── SCHWALM/
│   └── resumo.md               ← Problemas, correções, status da SCHWALM (Maia)
└── GENICS/
    └── resumo.md               ← Problemas, correções, status da GENICS (Vitória)
```

---

## Resumo Geral — O Que Fizemos

### 1. ADPLAN — SDR IA (Fortics/Kommo)

**Problemas abordados:**
1. **Roteamento de leads não qualificados** — leads sem qualificação iam pro Funil V4 (como MQL) em vez do Funil SDR IA / não qualificados.
2. **Tags Respondeu/Sem resposta** — briefing pedia categorização no dashboard Lovable para filtrar leads que retornaram.
3. **Execução travando ~20 min** — Code JS com timeout 300s + retryOnFail de 5 tentativas.
4. **Erros diversos pós-correção** — HTTP Request1 (404), Switch (last on null), Responde texto (Invalid expression).
5. **SDR IA parou de responder** — escrita de `status_resposta` no caminho crítico derrubava execução.

**Correções aplicadas:**
- Ajuste 2: Create new leads1 redirecionado para Funil SDR IA; tag de qualificado removida dos leads não qualificados.
- Ajuste 3 removido do fluxo principal: `status_resposta` passou a ser mantido por trigger SQL no banco (backfill + trigger), não mais pelo n8n.
- Switch: safe access (`?.`) adicionado em `.last()` e `.length`; rightValue do debouncerTime protegido.
- Code JS2/JS3: retryOnFail removido (cortou de 25 min para no máximo 300s).
- HTTP Request1 (PATCH Kommo): deletado (causava 404).
- `=number` → `number` nos 4 nós Responde texto.
- Credenciais verificadas: 12 nós Kommo ("ADPLAN"), OpenAI, Supabase, Redis, WhatsApp.

**Pendências:**
- [ ] Restaurar PATCH do Kommo se necessário (Vendedor Remo1 → atualização de lead).
- [ ] Verificar task runner do servidor (timeout residual de 300s nos Code JS).

---

### 2. SIGNOR — SDR IA (Bitrix24)

**Problemas abordados:**
1. **Leads pararam de chegar** após ajuste de formatos de arquivo — documento (PDF) travava execução.
2. **Assimetria entre pipelines duplicados** — pipeline 1 quebrado, pipeline 2 já corrigido.
3. **Credencial de download expirada** — `Authorization failed` no Baixar Arquivo Binário.
4. **Pipeline duplicado** — dois triggers WhatsApp idênticos para o mesmo número.

**Correções aplicadas:**
- Obter URL da Mídia (pipeline 1): URL fixa `.image.url` substituída por resolução por tipo (image/audio/document/video).
- Áudio reconectado: cadeia de transcrição (Whisper) apontava para Webhook4 (morto) → corrigido para `messages[0].id`.
- Fallback dos Switches 4 e 5: saída none → roteamento para handler de texto.
- Pipeline duplicado consolidado: pipeline 1 removido (58 nodes), pipeline 2 mantido.
- Bug de cópia corrigido: AI Agent do P2 referenciando `$('camposIniciais')` do P1 → corrigido para `camposIniciais1`.
- 16 nodes mortos removidos.
- Credencial `whatsAppApi "Signor Concretos"` adicionada ao Baixar Arquivo Binário1.
- Token WhatsApp: explicado que precisa renovar + adicionar `lookaside.fbsbx.com` em Allowed HTTP Request Domains.

**Pendências:**
- [ ] **Renovar token** da credencial `whatsAppApi "Signor Concretos"` no n8n.
- [ ] Adicionar `lookaside.fbsbx.com` em Allowed HTTP Request Domains.
- [ ] Testar com mídia recém-enviada (link da Meta expira em ~5 min).

---

### 3. SCHWALM (Maia) — SDR IA

**Problemas abordados:**
1. **Qualificando leads sem qualificação** — frase de cortesia "Anotei tudo e vou repassar" disparava qualificação.
2. **CreateUser1: `telefoneCliente` viola not-null** — eventos de status (sem `messages[]`) passavam pelo filtro e tentavam criar usuário com telefone nulo.

**Correções aplicadas:**
- If de qualificação: condição OR removida — agora só `[LEAD_QUALIFICADO]]` qualifica.
- If3: adicionado filtro `messages[0].from` não-vazio para barrar eventos de status.
- Segurança: Bearer token do Kommo exposto no node `normatização-dados` — recomendado migrar para credencial n8n.

**Pendências:**
- [ ] Migrar token do Kommo de texto puro para credencial n8n.
- [ ] Rotacionar token exposto.

---

### 4. GENICS (Vitória) — SDR IA

**Problemas abordados:**
1. **Implementação do zero** — briefing → prompt → fluxo n8n + gerenciador MQL/handoff/follow-up.
2. **Credencial de mídia errada** — nodes de imagem/documento usavam credencial de "Viajes Samser".
3. **Follow-up com texto errado** — pergunta de turno em vez de reengajamento.
4. **Conexão duplicada no caminho "Outros"** — criava lead duplicado.
5. **Lead não qualificado sumia** — não ia para o Kommo (violava "anti-limbo" do briefing).
6. **Redis Cloud fora** — `getaddrinfo ENOTFOUND` no nó Incluir Mensagem.

**Correções aplicadas:**
- Fluxo principal: credencial de mídia corrigida; fallback do Switch de mídia.
- Gerenciador: caminho do não qualificado completo (Recepção/PERDIDO + tag por motivo); texto do follow-up corrigido; duplicação do "Outros" removida.
- Classificador ajustado para emitir `motivo_desqualificacao` (fora_icp / sem_interesse / contato_invalido).
- Dashboard Lovable: prompt para remix com edge function e schema `genics`.
- Necessário expor schema `genics` no Supabase API Settings.

**Pendências:**
- [ ] **Redis Cloud** — host `redis-11584.crce196.sa-east-1-2.ec2.cloud.redislabs.com` não resolve. Migrar para Redis local (Docker) ou reativar instância.
- [ ] ALTER TABLE `genics.leads_mql ADD COLUMN motivo_desqualificacao text`.
- [ ] Criar secret `GENICS_SERVICE_ROLE_KEY` no Supabase.
- [ ] Incluir `lookaside.fbsbx.com` nos domínios permitidos da credencial WhatsApp "Genics".
- [ ] Follow-up: está 20 min, briefing pede 30 — decidir.
- [ ] Segurança: senha do Kommo exposta no briefing PDF.

---

## Pendências Globais

| # | Item | Cliente | Tipo | Urgência |
|---|------|---------|------|----------|
| 1 | Renovar token WhatsApp + domínios | SIGNOR | Infra | 🔴 Alta |
| 2 | Redis Cloud fora (local ou reativar) | GENICS | Infra | 🔴 Alta |
| 3 | Migrar token Kommo para credencial | SCHWALM | Segurança | 🟡 Média |
| 4 | Rodar ALTER TABLE `motivo_desqualificacao` | GENICS | Banco | 🟡 Média |
| 5 | Criar secret GENICS_SERVICE_ROLE_KEY | GENICS | Config | 🟡 Média |
| 6 | Decidir follow-up 20 vs 30 min | GENICS | Decisão | 🟢 Baixa |
| 7 | Restaurar PATCH Kommo? | ADPLAN | Decisão | 🟢 Baixa |

---

## Arquivos Gerados (JSONs n8n)

Cada cliente teve seu(s) workflow(s) corrigido(s) em JSON para importar no n8n. Os arquivos originais estavam na conversa do Claude como anexos. Para recuperá-los, é necessário acessar o histórico da conversa no Claude ou pedir regeneração.
