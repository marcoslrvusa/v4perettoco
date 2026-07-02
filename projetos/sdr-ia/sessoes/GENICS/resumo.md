# GENICS (Vitória) — SDR IA

## Problemas encontrados

### 🔴 Credencial de mídia de outro cliente
Nodes de download de imagem e documento usavam credencial `whatsAppApi "Viajes Samser"` — resquício de cópia de template. Só áudio estava com a credencial certa da Genics.
- **Correção:** alinhado para credencial "Genics"

### 🔴 Lead não qualificado sumia (anti-limbo violado)
Caminho `nao_qualificado` só atualizava Supabase — não criava lead no Kommo. Briefing exige: funil Recepção / etapa PERDIDO + tag por motivo.
- **Correção:** cadeia completa espelhada do Handoff (Get Lead → contato → Criar Lead → tag → nota → Supabase)
- Pipeline 13236788 / status 107785912 (PERDIDO — já existia)
- Tags: `#IA_ForaDoICP` (261891), `#IA_SemInteresse` (261893), `#IA_ContatoInvalido` (261895)

### 🟡 Classificador precisa emitir motivo de desqualificação
Opção B (granular): tag por motivo. Classificador ajustado para emitir `motivo_desqualificacao` (fora_icp / sem_interesse / contato_invalido).
- **Correção:** Analisa Classificação + Parse JSON ajustados

### 🟡 Follow-up com texto errado
Estava com pergunta de turno ("Tenho horários… manhã ou tarde?"). Briefing pede reengajamento.
- **Correção:** texto alterado para "Oi 😊 Vi que nossa conversa pausou…"

### 🟡 Conexão duplicada no caminho "Outros"
Lead já existente caía no update E no caminho de criação ao mesmo tempo → lead duplicado em Procedimentos.
- **Correção:** duplicação removida (igualado aos outros 5 caminhos)

### 🔴 Redis Cloud fora
`Incluir Mensagem`: `getaddrinfo ENOTFOUND redis-11584...redislabs.com`
- 3 nós afetados: Incluir Mensagem, Buscar Mensagens, Apaga Mensagens
- Credencial compartilhada "V4 Peretto" — provavelmente outros clientes também quebrados
- **Recomendação:** migrar para Redis local (Docker) ou reativar Redis Cloud
- Erro documentado desde 18/jun — nunca resolvido na raiz

## Dashboard Lovable

### Implementação:
- Edge function `genics-data` (remix da `schwalm-data`)
- Schema `genics` (2 tabelas: `dados_cliente` + `leads_mql`)
- Necessário expor schema `genics` no Supabase API Settings
- Secret `GENICS_SERVICE_ROLE_KEY` a ser criado

### Colunas principais (leads_mql):
`session_id`, `telefone`, `nome`, `classification`, `mql`, `handoff`, `motivo_desqualificacao`, `qualification_reason`, `tratamento_interesse`, `possui_medico`, `urgencia`, `stop_reason`, `encerrado`, `last_interaction_at`, `followup_20min_*`

## Pendências
- 🔴 **Redis:** reativar Redis Cloud ou subir Redis local (Docker)
- 🟡 ALTER TABLE `genics.leads_mql ADD COLUMN motivo_desqualificacao text`
- 🟡 Criar secret `GENICS_SERVICE_ROLE_KEY` no Supabase
- 🟡 Adicionar `lookaside.fbsbx.com` nos domínios da credencial WhatsApp "Genics"
- 🟢 Decidir follow-up: 20 min (atual) vs 30 min (briefing)
- 🔒 Segurança: senha do Kommo exposta no briefing PDF (pág 4)

## Workflows para subir (2 JSONs)
1. `Genics__SDR_IA__CORRIGIDO` — fluxo principal (recepção + Vitória + RAG)
2. `Genics__Gerenciador_MQL_Handoff_Followup__FINAL` — cérebro do CRM

## Status: ⏳ Aguardando Redis + ALTER TABLE
