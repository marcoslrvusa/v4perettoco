import { workflow, node, links } from '@n8n-as-code/transformer';

// <workflow-map>
// Workflow : Peretto AI Ops - Briefing Comite
// Nodes   : 6  |  Connections: 5
//
// NODE INDEX
// ──────────────────────────────────────────────────────────────────
// Property name                    Node type (short)         Flags
// ScheduleTrigger                    scheduleTrigger
// LoadClientData                     code
// AnalyzeWithOpenrouter              httpRequest                [creds]
// CompileBriefing                    code
// BuildEmailHtml                     html
// SendEmail                          emailSend
//
// ROUTING MAP
// ──────────────────────────────────────────────────────────────────
// ScheduleTrigger
//    → LoadClientData
//      → AnalyzeWithOpenrouter
//        → CompileBriefing
//          → BuildEmailHtml
//            → SendEmail
// </workflow-map>

// =====================================================================
// METADATA DU WORKFLOW
// =====================================================================

@workflow({
    id: 'McbdlfvByxxkzr7u',
    name: 'Peretto AI Ops - Briefing Comite',
    active: false,
    isArchived: false,
    settings: { executionOrder: 'v1' },
})
export class PerettoAiOpsBriefingComiteWorkflow {
    // =====================================================================
    // CONFIGURATION DES NOEUDS
    // =====================================================================

    @node({
        id: 'e97a96c0-754d-4dfc-93f3-4350c295f607',
        name: 'Schedule Trigger',
        type: 'n8n-nodes-base.scheduleTrigger',
        version: 1.3,
        position: [250, 300],
    })
    ScheduleTrigger = {
        rule: {
            interval: [
                {
                    field: 'days',
                    daysInterval: 1,
                    triggerAtHour: 20,
                    triggerAtMinute: 0,
                },
            ],
        },
    };

    @node({
        id: 'ec3c7d76-ce0c-471a-b7d8-44462112b9dc',
        name: 'Load Client Data',
        type: 'n8n-nodes-base.code',
        version: 2,
        position: [520, 300],
    })
    LoadClientData = {
        mode: 'runOnceForAllItems',
        language: 'javaScript',
        jsCode: `// Carrega dados dos clientes + performance das APIs
// Substitua pelos dados reais dos seus clientes
const clientes = [
  {
    nome: "Cliente A",
    vertical: "ecommerce",
    verba_mensal: 5000,
    okrs: {
      objetivo: "Consolidar crescimento de receita digital no Q2",
      krs: [
        { descricao: "ROAS médio", meta: 3.2, unidade: "x", atual: 2.8 },
        { descricao: "Leads mensais", meta: 150, unidade: "leads", atual: 112 },
        { descricao: "CAC máximo", meta: 80, unidade: "R$", atual: 95, inverso: true },
      ]
    },
    google_ads: { investimento: 2850, roas: 2.8, cliques: 1420, conversoes: 38 },
    meta_ads: { investimento: 1980, roas: 3.1, cliques: 890, conversoes: 22 },
    ga4: { sessoes: 3420, taxa_conversao: 2.1 },
  },
  {
    nome: "Cliente B",
    vertical: "b2b_saas",
    verba_mensal: 8000,
    okrs: {
      objetivo: "Gerar leads qualificados para vendas B2B no Q2",
      krs: [
        { descricao: "CPL máximo", meta: 120, unidade: "R$", atual: 145, inverso: true },
        { descricao: "MQLs mensais", meta: 40, unidade: "MQLs", atual: 28 },
      ]
    },
    google_ads: { investimento: 4200, cpl: 145, cliques: 2100, conversoes: 29 },
    meta_ads: { investimento: 3500, cpl: 138, cliques: 1670, conversoes: 25 },
    ga4: { sessoes: 5100, taxa_conversao: 3.4 },
  },
];

// Calcula pace de verba
const hoje = new Date();
const diasNoMes = 30;
const diasPassados = hoje.getDate();
const dataStr = hoje.toLocaleDateString('pt-BR', { timeZone: 'America/Sao_Paulo', year: 'numeric', month: 'long', day: 'numeric' });

clientes.forEach(c => {
  const paceEsperado = c.verba_mensal * (diasPassados / diasNoMes);
  const gastoTotal = (c.google_ads?.investimento || 0) + (c.meta_ads?.investimento || 0);
  c.pace = {
    esperado: Math.round(paceEsperado),
    gasto: gastoTotal,
    diferenca: Math.round(gastoTotal - paceEsperado),
    percentual: Math.round(((gastoTotal - paceEsperado) / paceEsperado) * 100),
  };
  c.pace.status = Math.abs(c.pace.diferenca / paceEsperado) < 0.1 ? 'ok' : c.pace.diferenca > 0 ? 'acima' : 'abaixo';
});

const dataSemana = {
  geradoEm: dataStr,
  semana: diasPassados,
  clientes: clientes,
};

return [{ json: dataSemana }];`,
    };

    @node({
        id: '71a2cb3a-a3bb-4f5e-8daa-1032d0446f59',
        name: 'Analyze with OpenRouter',
        type: 'n8n-nodes-base.httpRequest',
        version: 4.2,
        position: [790, 300],
        credentials: { openAiApi: { id: 'SN4AwfKsQ1EMDELQ', name: 'OpenRouter' } },
    })
    AnalyzeWithOpenrouter = {
        method: 'POST',
        url: 'https://openrouter.ai/api/v1/chat/completions',
        authentication: 'genericCredentialType',
        genericAuthType: 'openAiApi',
        sendBody: true,
        specifyBody: 'json',
        jsonBody: `={
  "model": "deepseek/deepseek-v4-flash:free",
  "messages": [
    {"role": "system", "content": "Você é o Agente Coordenador da V4 Company. Analise dados de performance de clientes, cruze com OKRs, identifique desvios e gere hipóteses acionáveis para o Comitê de P&EG. Seja direto. Para cada cliente: status (verde/amarelo/vermelho), desvio principal, hipótese, ação sugerida. Formato estruturado, escaneável, máximo 3 ações por cliente. Use FCA: Fato → Causa → Ação."},
    {"role": "user", "content": "{{ $json.clientes | toJson }}"}
  ],
  "max_tokens": 2000
}`,
        options: {},
    };

    @node({
        id: '55880513-ef7e-409b-ba9d-3e393dce48e8',
        name: 'Compile Briefing',
        type: 'n8n-nodes-base.code',
        version: 2,
        position: [1060, 300],
    })
    CompileBriefing = {
        mode: 'runOnceForAllItems',
        language: 'javaScript',
        jsCode: `const input = $input.first().json;
const analise = input.choices?.[0]?.message?.content || '(falha na análise)';

const data = new Date();
const dataStr = data.toLocaleDateString('pt-BR', { timeZone: 'America/Sao_Paulo', day: 'numeric', month: 'long' });

return [{
  json: {
    analise: analise,
    data: dataStr,
    geradoEm: data.toISOString(),
  }
}];`,
    };

    @node({
        id: '58c39db8-6ebe-4a75-bcd4-b6c0235b6d63',
        name: 'Build Email HTML',
        type: 'n8n-nodes-base.html',
        version: 1.2,
        position: [1330, 300],
    })
    BuildEmailHtml = {
        operation: 'generateHtmlTemplate',
        sourceData: 'json',
        dataPropertyName: 'data',
        html: `<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;max-width:700px;margin:0 auto;color:#333;">

  <table width="100%" cellpadding="0" cellspacing="0">
    <tr>
      <td style="background:linear-gradient(135deg,#1a1a2e,#16213e);padding:32px 24px;border-radius:12px 12px 0 0;">
        <h1 style="color:#ffffff;margin:0;font-size:24px;">Briefing Comitê P&amp;EG</h1>
        <p style="color:rgba(255,255,255,0.7);margin:8px 0 0;font-size:14px;">{{ geradoEm }}</p>
      </td>
    </tr>
    <tr>
      <td style="background:#ffffff;padding:24px;border-radius:0 0 12px 12px;box-shadow:0 1px 3px rgba(0,0,0,0.08);">

        <div style="background:#f0f4ff;padding:12px 16px;border-radius:8px;font-size:12px;color:#444;margin-bottom:20px;">
          <strong>Legenda:</strong> 🟢 On track &nbsp;|&nbsp; 🟡 Atenção &nbsp;|&nbsp; 🔴 Crítico
        </div>

        <div style="white-space:pre-wrap;line-height:1.6;font-size:14px;">
{{ analise }}
        </div>

      </td>
    </tr>
    <tr>
      <td style="padding:16px 24px;text-align:center;font-size:11px;color:#999;">
        Peretto AI Ops — V4 Company<br>
        Gerado automaticamente domingo às 20h
      </td>
    </tr>
  </table>

</body>
</html>`,
    };

    @node({
        id: '28fc184a-8d47-4d3c-8387-6b98369ac5c1',
        webhookId: '6423c350-3df8-4f9d-a677-76171f86d7c6',
        name: 'Send Email',
        type: 'n8n-nodes-base.emailSend',
        version: 2.1,
        position: [1600, 300],
    })
    SendEmail = {
        resource: 'email',
        operation: 'send',
        fromEmail: 'ops@v4company.com.br',
        toEmail: '',
        subject: '={{ "Briefing Comitê P&EG — " + $json.geradoEm }}',
        message: '',
        emailFormat: 'html',
    };

    // =====================================================================
    // ROUTAGE ET CONNEXIONS
    // =====================================================================

    @links()
    defineRouting() {
        this.ScheduleTrigger.out(0).to(this.LoadClientData.in(0));
        this.LoadClientData.out(0).to(this.AnalyzeWithOpenrouter.in(0));
        this.AnalyzeWithOpenrouter.out(0).to(this.CompileBriefing.in(0));
        this.CompileBriefing.out(0).to(this.BuildEmailHtml.in(0));
        this.BuildEmailHtml.out(0).to(this.SendEmail.in(0));
    }
}
