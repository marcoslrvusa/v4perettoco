# SCHWALM (Maia) — SDR IA

## Problemas encontrados

### 🔴 Qualificando leads sem qualificação
If de qualificação com duas condições em **OR**:
1. `output contains "[LEAD_QUALIFICADO]"` ✅ (correto)
2. `output contains "Anotei tudo e vou repassar"` ❌ (problema)

A frase "Anotei tudo e vou repassar" é o **encerramento padrão** da Maia em qualquer conversa. Como a condição é OR, toda despedida educada qualificava o lead.
- **Correção:** condição 2 removida. Qualificação depende exclusivamente do marcador `[LEAD_QUALIFICADO]`

### 🟡 CreateUser1: `telefoneCliente` null viola not-null
Eventos de status do WhatsApp (enviado/entregue/lido) chegam com `statuses[]` em vez de `messages[]`. If3 só filtrava pelo número da clínica — eventos sem `messages[0].from` passavam e tentavam criar lead com telefone nulo.
- **Correção:** no If3, adicionado `messages[0].from` não-vazio (com optional chaining)

### 🟡 Segurança: Bearer token exposto
Node `normatização-dados` tem token JWT do Kommo em texto puro no JSON.

## Pendências
- 🟡 Migrar token do Kommo para credencial n8n e rotacionar

## Status: ✅ Corrigido — pode subir
