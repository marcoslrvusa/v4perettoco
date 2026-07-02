# SIGNOR — SDR IA (Bitrix24)

## Problemas encontrados

### 🔴 Leads pararam de chegar após ajuste de formatos
Documento (PDF) roteado para node `Obter URL da Mídia` que lia `messages[0].image.url` fixo — documento não tem `image`, execução quebrava.
- **Correção:** URL resolvida por tipo (image/audio/document/video), espelhando pipeline 2

### 🔴 Áudio não era transcrito
Cadeia de transcrição (Mensagem de Audio → Whisper) apontava para `$('Webhook4')` — node morto de versão antiga.
- **Correção:** reconectado para `$('WhatsApp Trigger').item.json.messages[0].id`

### 🟡 Fallback dos Switches (4 e 5) = none
Tipos não previstos (vídeo, figurinha, localização) sumiam em silêncio.
- **Correção:** fallback roteado para handler de texto

### 🔴 Pipeline duplicado
Dois triggers WhatsApp para o mesmo número (555499668787), mesmo webhookId — leads duplicados, IA respondia 2x.
- **Descoberta:** AI Agent do P2 referenciava `$('camposIniciais')` do P1 (bug de cópia)
- **Consolidação:** pipeline 1 removido (58 nodes), P2 mantido
- 142 → 68 nodes, 16 nodes mortos removidos

### 🔴 Authorization failed no download
`Baixar Arquivo Binário1` sem credencial. `Obter URL da Mídia` com token expirado.
- **Correção:** credencial `whatsAppApi "Signor Concretos"` adicionada ao Baixar Arquivo Binário1
- ⚠️ Token precisa ser renovado manualmente no n8n

### 🟡 Link de mídia expirado em teste
Dado pinado no trigger tinha link do `lookaside.fbsbx.com` expirado (~28 dias)
- **Instrução:** testar com mídia recém-enviada (link expira em ~5 min)
- Adicionar `lookaside.fbsbx.com` em Allowed HTTP Request Domains

## Pendências
- 🔴 **[Urgente]** Renovar token da credencial `whatsAppApi "Signor Concretos"` no n8n
- 🔴 Adicionar `lookaside.fbsbx.com` em Allowed HTTP Request Domains
- Testar com mídia recém-enviada

## Status: ⏳ Aguardando renovação de token para testar
