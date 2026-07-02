# Transcrição Completa — Sessão SDR IA

> **Período:** 16/jun/2026 a 24/jun/2026
> **Fonte:** Claude Share + arquivo local `Histórico Claude SDR IA 1.md`
> **Total de interações:** ~70 turnos
> **Clientes:** ADPLAN, SIGNOR, SCHWALM, GENICS

---

## 16/jun — Abertura: Diagnóstico de 3 workflows

### Contexto inicial
Usuário submete 3 JSONs de workflows n8n (ADPLAN, SIGNOR, SCHWALM) para análise de bugs:

### ADPLAN — 3 ajustes solicitados pelo comercial:
1. Leads qualificados não migrando para Kommo no Funil V4 etapa MQL
2. Leads não qualificados não aparecendo no Funil SDR IA
3. Tags "Respondeu"/"Sem resposta" para filtrar no dashboard

### SIGNOR — Leads pararam de chegar após ajuste de formatos de arquivo

### SCHWALM (Maia) — Qualificando leads sem qualificação

### Diagnósticos do Claude:
- **ADPLAN:** Create new leads1 (não qualificado/contato existe) apontava para Funil V4 em vez de Funil SDR IA. Get a row1 filtra por `followup_enabled = true`.
- **SIGNOR:** Obter URL da Mídia com URL fixa em `.image.url` — documento quebra. Pipeline 2 já corrigido, pipeline 1 não.
- **SCHWALM:** If de qualificação com OR — "[LEAD_QUALIFICADO]" OU "Anotei tudo e vou repassar". Frase de cortesia dispara falso positivo.

---

## 16/jun — Correções iniciais

### ADPLAN — Ajuste 2 aplicado:
- Create new leads1: pipeline 11068075 → 13421772, status 84910015 → 106897256, tag 102360 removida
- Create new leads3: tag 102360 removida
- `followup_enabled = true` confirmado como intencional

### ADPLAN — Ajuste 3 proposto:
- Coluna `status_resposta` no Supabase (default 'Sem resposta')
- CreateUser: nasce como Sem resposta
- AtualizaUsuario: vira Respondeu
- Node A1: volta Sem resposta quando follow-up esgota

### SIGNOR — Correção parcial:
- Obter URL da Mídia: espelhado lógica do pipeline 2

### SCHWALM — Correção:
- Condição "Anotei tudo" removida do If

### Changelogs gerados (dev e operação)

---

## 17/jun — SIGNOR completo + GENICS entra

### SIGNOR — Correção completa (de uma vez):
- Documento resolvido
- Áudio reconectado (Webhook4 → WhatsApp Trigger)
- Fallback dos Switches 4 e 5
- **Problema no teste:** "Authorization failed" — na verdade link de mídia expirado (dado pinado) + credencial sem `lookaside.fbsbx.com` em Allowed HTTP Request Domains

### SIGNOR — Pipeline duplicado:
- Descoberto: dois triggers WhatsApp para o mesmo número (555499668787)
- Consolidado: pipeline 1 removido, pipeline 2 mantido
- Bug: AI Agent do P2 referenciando `$('camposIniciais')` do P1 → corrigido
- 142 → 68 nodes

### GENICS (Vitória) — Novo cliente:
- Briefing PDF + prompt SDR IA + JSON do workflow analisados
- Prompt bate com JSON (19.407 caracteres)
- **Bug crítico:** credencial de mídia apontando para "Viajes Samser"
- **Faltando:** sub-workflow "Gerenciador MQL/Handoff + Follow-up 20min"

---

## 17/jun — GENICS: Gerenciador + Cruzamento briefing

### Gerenciador analisado:
- Classificador IA → Switch 6 caminhos (mql, handoff, doadora, receptora, outros_procedimentos, nao_qualificado)
- Funis OK: Vendas, Recepção, Procedimentos, Ovodoação
- Follow-up com texto errado (pergunta de turno em vez de reengajamento)
- Conexão duplicada no caminho "Outros"

### Discrepâncias briefing × implementação:
- ❌ Lead não qualificado não vai pro Kommo ("anti-limbo" violado)
- ❌ Follow-up: 20 min (briefing pede 30)
- ⚠️ Tom: briefing diz "Casual", prompt é acolhedor/empático (melhor)

---

## 17/jun — GENICS: Tags e etapa PERDIDO

### Tags mapeadas (Kommo):
- `#IA_ForaDoICP` = 261891
- `#IA_SemInteresse` = 261893
- `#IA_ContatoInvalido` = 261895
- `SDR IA` = 248407
- `Handoff SDR IA` = 248409

### Etapa PERDIDO:
- Já existe no Funil Recepção: status_id **107785912** (pipeline 13236788)

### Opção B escolhida: tag por motivo (granular)

---

## 18/jun — GENICS finalizada + SCHWALM erro telefone

### GENICS — Finalizada:
- Caminho do não qualificado completo: Recepção/PERDIDO + tag por motivo + nota interna + Supabase
- Classificador ajustado para emitir `motivo_desqualificacao`
- Node antigo `Update Parcial (NaoQualificado)` desconectado

### SCHWALM — Erro `telefoneCliente` null:
- Causa: eventos de status (entrega/leitura) sem `messages[]` passavam pelo If3
- Correção: adicionado `messages[0].from` não-vazio no If3

### Dashboard Lovable GENICS:
- Prompt para remix do dashboard SCHWALM → GENICS
- Edge function lendo schema `genics` (2 tabelas: `dados_cliente` + `leads_mql`)
- Necessário criar `GENICS_SERVICE_ROLE_KEY`

---

## 18/jun — ADPLAN: Filtro Lovable + SDR para de responder

### Filtro ADPLAN no Lovable:
- Campo `status_resposta` (Respondeu/Sem resposta)
- Backfill + trigger no Supabase
- Etiqueta colorida no card + filtro ao lado do filtro de data

### 🔴 Problema crítico: SDR IA ADPLAN parou de responder
- **Causa:** escrita de `status_resposta` no CreateUser (caminho crítico antes da IA responder)
- Quando coluna não existia ou dava erro, execução morria → lead novo sem resposta
- **Solução:** remover todo Ajuste 3 do fluxo n8n
- Campo `status_resposta` passou a ser mantido por **trigger SQL no banco** (backfill + trigger)

### SQL definitivo gerado:
```sql
UPDATE adplan_leads SET status_resposta = 'Respondeu'
WHERE EXISTS (SELECT 1 FROM adplan_chat_history h WHERE h."sessionID" = session_id AND h.role = 'human');
-- + trigger para manter automaticamente
```

---

## 18/jun — Bug do filtro (tudo "Respondeu")

### Diagnóstico:
- Dev do Lovable derivou status do `chat_history` mas perdeu a correlação por `session_id`
- Query sem `WHERE h.session_id = l."sessionID"` casava com todos (891 leads)
- Solução: view `adplan_leads_status` com EXISTS correlacionado + `role = 'human'`

---

## 19/jun — Crise: ADPLAN fora do ar

### Relato:
- SDR IA não respondendo
- Execução de teste durando ~20 min
- Usuário pede arquivo original (16/jun) para recovery

### Arquivo original recuperado:
- `SDR IA - ADPLAN.json` (166 nodes, baseline limpo)

---

## 22/jun — ADPLAN: Múltiplas falhas pós-correção

### Erros reportados:
1. `HTTP Request1` — The resource you are requesting could not be found
2. `Switch` — last can't be used on null value
3. `Responde texto` (x4) — Invalid expression
4. `Code in JavaScript3` — Task execution timed out after 300 seconds

### Diagnóstico:
- Ao conectar LLM no AiAgent5 (19/06), fluxo voltou a executar até o fim → nós downstream começaram a rodar e quebrar
- Code JS não é "dataset grande/loop" — é trivial (formata um telefone). Timeout é do **task runner** do servidor
- `retryOnFail` com maxTries=5 ⇒ 5 × 300s = 25 min
- **HTTP Request1 ≠ HTTP Request:** report confundiu os nós. HTTP Request1 (PATCH Kommo) dava 404 por `$json.id` vazio
- Switch: `message.last()` e `message.length` sem safe access
- Responde texto: `=number` em vez de `number` no nome do parâmetro

### Correções aplicadas na versão revisada (22/jun):
- Switch regra 1: rightValue com safe access (`?.` + fallback `|| 5`)
- `=number` → `number` nos 4 Responde texto
- HTTP Request1 deletado (PATCH Kommo removido)
- retryOnFail removido dos Code JS
- Safe access nos Responde texto
- **165 nodes, 0 conexões quebradas**

### Pós-importação:
- Verificar credenciais: Kommo (12 nós, "ADPLAN"), OpenAI ("OpenAi Peretto"), Supabase ("Peretto"), Redis ("Adplan-bot-memory"), WhatsApp
- Responde texto/Mídia usam Evolution API (apikey inline de `camposIniciais`)

---

## 24/jun — GENICS: Redis fora

### Erro:
```
Problem in node 'Incluir Mensagem'
getaddrinfo ENOTFOUND redis-11584.crce196.sa-east-1-2.ec2.cloud.redislabs.com
```

### Diagnóstico:
- Redis Cloud (Redis Labs) — host não resolve de lugar nenhum
- Instância foi deletada, expirou ou foi suspensa
- 3 nós afetados na GENICS: Incluir Mensagem, Buscar Mensagens, Apaga Mensagens
- Credencial compartilhada "V4 Peretto" — provavelmente afeta outros clientes

### Recorrência:
- Mesmo erro documentado desde diagnóstico de 18/jun
- Nunca foi resolvido na raiz

### Recomendação:
- Opção A: Reativar/recriar endpoint no Redis Cloud
- Opção B (definitiva): Subir Redis local (Docker) — `docker run -d --name redis-local -p 6379:6379 redis:7-alpine`

---

## Linha do Tempo

| Data | Cliente | Evento |
|------|---------|--------|
| 16/jun | Todos | Abertura, diagnóstico dos 3 workflows |
| 16/jun | ADPLAN | Ajuste 2 aplicado (roteamento) |
| 16/jun | SCHWALM | Correção qualificação |
| 16/jun | SIGNOR | Correção parcial |
| 17/jun | SIGNOR | Correção completa + consolidação pipelines |
| 17/jun | GENICS | Início análise + credencial errada descoberta |
| 17/jun | GENICS | Gerenciador analisado + discrepâncias |
| 17/jun | GENICS | Tags mapeadas + etapa PERDIDO confirmada |
| 18/jun | GENICS | Finalizada (caminho não qualificado + tags) |
| 18/jun | SCHWALM | Correção erro telefone null |
| 18/jun | ADPLAN | Filtro Lovable + SDR PARA DE RESPONDER |
| 18/jun | ADPLAN | Ajuste 3 removido, trigger SQL implementado |
| 18/jun | ADPLAN | Bug do filtro (tudo "Respondeu") diagnosticado |
| 19/jun | ADPLAN | Crise: recovery do arquivo original |
| 22/jun | ADPLAN | Revisão completa: 4 erros corrigidos |
| 24/jun | GENICS | Redis Cloud fora |
