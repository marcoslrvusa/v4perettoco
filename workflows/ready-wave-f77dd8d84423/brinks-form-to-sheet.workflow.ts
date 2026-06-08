import { workflow, node, links } from '@n8n-as-code/transformer';

// <workflow-map>
// Workflow : Brinks - Formulario para Planilha
// Nodes   : 3  |  Connections: 2
//
// NODE INDEX
// ──────────────────────────────────────────────────────────────────
// Property name                    Node type (short)         Flags
// WebhookBrinks                      webhook
// NormalizarDados                    code
// SalvarNaPlanilha                   googleSheets               [creds]
//
// ROUTING MAP
// ──────────────────────────────────────────────────────────────────
// WebhookBrinks
//    → NormalizarDados
//      → SalvarNaPlanilha
// </workflow-map>

// =====================================================================
// METADATA DU WORKFLOW
// =====================================================================

@workflow({
    id: 'DgRtCUd9crbWYpS6',
    name: 'Brinks - Formulario para Planilha',
    active: true,
    isArchived: false,
    projectId: 'u3W65WbPCWTXrdjF',
    settings: { executionOrder: 'v1' },
})
export class BrinksFormularioParaPlanilhaWorkflow {
    // =====================================================================
    // CONFIGURATION DES NOEUDS
    // =====================================================================

    @node({
        id: 'webook-brinks-1',
        webhookId: '47fabf4a-f66f-476f-9d2d-541c9aa6a48a',
        name: 'Webhook Brinks',
        type: 'n8n-nodes-base.webhook',
        version: 2.1,
        position: [250, 300],
    })
    WebhookBrinks = {
        httpMethod: 'POST',
        path: 'brinks-lead',
        responseMode: 'onReceived',
        responseData: 'firstEntryJson',
        options: {},
    };

    @node({
        id: 'normalizar-brinks-1',
        name: 'Normalizar Dados',
        type: 'n8n-nodes-base.code',
        version: 2,
        position: [500, 300],
    })
    NormalizarDados = {
        mode: 'runOnceForAllItems',
        language: 'javaScript',
        jsCode: `
const item = $input.first().json;

// GreatPages envia campos no formato { campos: { 0: { id, titulo, valor }, 1: {...} } }
const campos = item.campos || {};
const dados = { timestamp: new Date().toISOString() };

// Mapeia campos pelo titulo (mais confiavel que o id numerico)
for (const key of Object.keys(campos)) {
  const campo = campos[key];
  if (!campo || !campo.titulo) continue;
  const chave = campo.titulo.toLowerCase().replace(/[^a-z0-9]/g, '_').replace(/_+/g, '_').replace(/^_|_$/g, '');
  dados[chave] = campo.valor || '';
}

// Garantir campos principais mesmo se o titulo nao bater
const mapaPorTitulo = {};
for (const key of Object.keys(campos)) {
  const c = campos[key];
  if (c && c.titulo) mapaPorTitulo[c.titulo.toLowerCase()] = c.valor || '';
}
dados.telefone = dados.telefone || mapaPorTitulo['telefone'] || '';
dados.cnpj = dados.cnpj || mapaPorTitulo['cnpj'] || '';
dados.nome = dados.nome || mapaPorTitulo['nome'] || '';
dados.sobrenome = dados.sobrenome || mapaPorTitulo['sobrenome'] || '';
dados.email = dados.email || mapaPorTitulo['e-mail'] || mapaPorTitulo['email'] || '';
dados.empresa = dados.empresa || mapaPorTitulo['empresa'] || '';
dados.cidade = dados.cidade || mapaPorTitulo['cidade'] || '';
dados.consentimento_lgpd = dados.consentimento_lgpd || mapaPorTitulo['consentimento de privacidade'] || '';

// UTMs
dados.utm_source = dados.utm_source || mapaPorTitulo['utm_source'] || '';
dados.utm_medium = dados.utm_medium || mapaPorTitulo['utm_medium'] || '';
dados.utm_campaign = dados.utm_campaign || mapaPorTitulo['utm_campaign'] || '';
dados.utm_content = dados.utm_content || mapaPorTitulo['utm_content'] || '';
dados.utm_term = dados.utm_term || mapaPorTitulo['utm_term'] || '';

// Metadados
dados.elemento = item.elemento || '';
dados.url = item.uri || item.url || '';
dados.eid = item.eid || '';

return dados;
`,
    };

    @node({
        id: 'sheets-brinks-1',
        name: 'Salvar na Planilha',
        type: 'n8n-nodes-base.googleSheets',
        version: 4.7,
        position: [750, 300],
        credentials: { googleSheetsOAuth2Api: { id: 'COLOQUE_O_ID_DA_CREDENCIAL', name: 'Google Sheets' } },
    })
    SalvarNaPlanilha = {
        resource: 'sheet',
        operation: 'appendOrUpdate',
        documentId: {
            mode: 'list',
            value: 'COLOQUE_O_ID_DA_PLANILHA',
        },
        sheetName: {
            mode: 'list',
            value: 'Sheet1',
        },
        columns: {
            mappingMode: 'defineBelow',
            value: [
                {
                    column: 'timestamp',
                    value: '={{ $json.timestamp }}',
                },
                {
                    column: 'cnpj',
                    value: '={{ $json.cnpj }}',
                },
                {
                    column: 'nome',
                    value: '={{ $json.nome }}',
                },
                {
                    column: 'sobrenome',
                    value: '={{ $json.sobrenome }}',
                },
                {
                    column: 'email',
                    value: '={{ $json.email }}',
                },
                {
                    column: 'telefone',
                    value: '={{ $json.telefone }}',
                },
                {
                    column: 'empresa',
                    value: '={{ $json.empresa }}',
                },
                {
                    column: 'cidade',
                    value: '={{ $json.cidade }}',
                },
                {
                    column: 'consentimento_lgpd',
                    value: '={{ $json.consentimento_lgpd }}',
                },
                {
                    column: 'utm_source',
                    value: '={{ $json.utm_source }}',
                },
                {
                    column: 'utm_medium',
                    value: '={{ $json.utm_medium }}',
                },
                {
                    column: 'utm_campaign',
                    value: '={{ $json.utm_campaign }}',
                },
                {
                    column: 'utm_content',
                    value: '={{ $json.utm_content }}',
                },
                {
                    column: 'utm_term',
                    value: '={{ $json.utm_term }}',
                },
                {
                    column: 'url',
                    value: '={{ $json.url }}',
                },
                {
                    column: 'elemento',
                    value: '={{ $json.elemento }}',
                },
                {
                    column: 'eid',
                    value: '={{ $json.eid }}',
                },
            ],
        },
        options: {
            cellFormat: 'USER_ENTERED',
            handlingExtraData: 'insertInNewColumn',
        },
    };

    // =====================================================================
    // ROUTAGE ET CONNEXIONS
    // =====================================================================

    @links()
    defineRouting() {
        this.WebhookBrinks.out(0).to(this.NormalizarDados.in(0));
        this.NormalizarDados.out(0).to(this.SalvarNaPlanilha.in(0));
    }
}
