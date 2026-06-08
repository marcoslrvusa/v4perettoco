import { workflow, node, links } from '@n8n-as-code/transformer';

// <workflow-map>
// Workflow : Peretto AI Ops - Google Ads Report
// Nodes   : 5  |  Connections: 4
//
// NODE INDEX
// ──────────────────────────────────────────────────────────────────
// Property name                    Node type (short)         Flags
// ScheduleTrigger                    scheduleTrigger
// FormatReport                       code
// BuildEmailHtml                     html
// SendReport                         emailSend
// GoogleAds                          googleAds
//
// ROUTING MAP
// ──────────────────────────────────────────────────────────────────
// ScheduleTrigger
//    → GoogleAds
//      → FormatReport
//        → BuildEmailHtml
//          → SendReport
// </workflow-map>

// =====================================================================
// METADATA DU WORKFLOW
// =====================================================================

@workflow({
    id: 'xgeJMXgMhZ9nTep0',
    name: 'Peretto AI Ops - Google Ads Report',
    active: false,
    isArchived: false,
    projectId: 'u3W65WbPCWTXrdjF',
    settings: { executionOrder: 'v1', binaryMode: 'separate' },
})
export class PerettoAiOpsGoogleAdsReportWorkflow {
    // =====================================================================
    // CONFIGURATION DES NOEUDS
    // =====================================================================

    @node({
        id: '0c2f49b8-9d80-4ed0-84f3-5df45f44c7fe',
        name: 'Schedule Trigger',
        type: 'n8n-nodes-base.scheduleTrigger',
        version: 1.3,
        position: [-528, -480],
    })
    ScheduleTrigger = {
        rule: {
            interval: [
                {
                    triggerAtHour: 9,
                },
            ],
        },
    };

    @node({
        id: 'a2597204-01ea-4276-86ab-c38ed2a7cf39',
        name: 'Format Report',
        type: 'n8n-nodes-base.code',
        version: 2,
        position: [16, -480],
    })
    FormatReport = {
        jsCode: `
const items = $input.all();
const now = new Date();
const dateStr = now.toLocaleDateString('pt-BR', {
  timeZone: 'America/Sao_Paulo',
  year: 'numeric',
  month: 'long',
  day: 'numeric'
});

const campaigns = items.map(item => {
  const c = item.json;
  return {
    name: c.name || 'Sem nome',
    id: c.id || '-',
    status: c.status || 'unknown',
    budget: c.campaignBudget ? c.campaignBudget.amountMicros / 1000000 : 0,
    budgetType: c.campaignBudget ? c.budgetType || '-' : '-',
    servingStatus: c.servingStatus || '-',
    startDate: c.startDate || '-',
    endDate: c.endDate || '-'
  };
});

const active = campaigns.filter(c => c.status === 'ENABLED');
const paused = campaigns.filter(c => c.status === 'PAUSED');
const removed = campaigns.filter(c => c.status === 'REMOVED');

return [{
  json: {
    generatedAt: dateStr,
    totalCampaigns: campaigns.length,
    activeCount: active.length,
    pausedCount: paused.length,
    removedCount: removed.length,
    campaigns: campaigns,
    summary: {
      hasData: campaigns.length > 0,
      mostActive: active.length > 0,
      needsBudgetCheck: campaigns.filter(c => c.budget === 0 && c.status === 'ENABLED').length
    }
  }
}];
`,
    };

    @node({
        id: '39c9a7ef-3a58-469e-8697-a412ad6a7f20',
        name: 'Build Email HTML',
        type: 'n8n-nodes-base.html',
        version: 1.2,
        position: [336, -480],
    })
    BuildEmailHtml = {
        html: `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Relatório Google Ads</title>
</head>
<body style="margin:0;padding:0;background-color:#f4f6f9;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="max-width:640px;margin:24px auto;">
    <tr>
      <td style="background:linear-gradient(135deg,#1a73e8,#0d47a1);padding:32px 24px;border-radius:12px 12px 0 0;">
        <h1 style="color:#ffffff;margin:0;font-size:24px;font-weight:700;">Relatório Google Ads</h1>
        <p style="color:rgba(255,255,255,0.85);margin:8px 0 0;font-size:14px;">
          Gerado em {{ generatedAt }}
        </p>
      </td>
    </tr>
    <tr>
      <td style="background:#ffffff;padding:24px;border-radius:0 0 12px 12px;box-shadow:0 1px 3px rgba(0,0,0,0.08);">

        <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:24px;">
          <tr>
            <td style="background:#e8f0fe;padding:12px 16px;border-radius:8px;font-size:14px;color:#1a73e8;font-weight:600;">
              Resumo: <span style="font-weight:400;color:#333;">{{ totalCampaigns }} campanhas · {{ activeCount }} ativas · {{ pausedCount }} pausadas</span>
            </td>
          </tr>
        </table>

        <h2 style="font-size:16px;color:#333;margin:0 0 12px;">Campanhas</h2>

        <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;">
          <tr>
            <td style="background:#f8f9fa;padding:10px 12px;border-bottom:2px solid #1a73e8;font-size:12px;font-weight:700;color:#555;text-transform:uppercase;">Campanha</td>
            <td style="background:#f8f9fa;padding:10px 12px;border-bottom:2px solid #1a73e8;font-size:12px;font-weight:700;color:#555;text-transform:uppercase;">Status</td>
            <td style="background:#f8f9fa;padding:10px 12px;border-bottom:2px solid #1a73e8;font-size:12px;font-weight:700;color:#555;text-transform:uppercase;">Orçamento</td>
            <td style="background:#f8f9fa;padding:10px 12px;border-bottom:2px solid #1a73e8;font-size:12px;font-weight:700;color:#555;text-transform:uppercase;">Início</td>
          </tr>
          {{#each campaigns}}
          <tr>
            <td style="padding:10px 12px;border-bottom:1px solid #eee;font-size:13px;color:#333;">{{ this.name }}</td>
            <td style="padding:10px 12px;border-bottom:1px solid #eee;">
              {{#if (eq this.status 'ENABLED')}}
                <span style="background:#e6f4ea;color:#1e7e34;padding:3px 10px;border-radius:12px;font-size:12px;font-weight:600;">Ativa</span>
              {{else if (eq this.status 'PAUSED')}}
                <span style="background:#fef7e0;color:#f9ab00;padding:3px 10px;border-radius:12px;font-size:12px;font-weight:600;">Pausada</span>
              {{else if (eq this.status 'REMOVED')}}
                <span style="background:#fce8e6;color:#d93025;padding:3px 10px;border-radius:12px;font-size:12px;font-weight:600;">Removida</span>
              {{else}}
                <span style="background:#f1f3f4;color:#5f6368;padding:3px 10px;border-radius:12px;font-size:12px;">{{ this.status }}</span>
              {{/if}}
            </td>
            <td style="padding:10px 12px;border-bottom:1px solid #eee;font-size:13px;color:#333;">
              {{#if (gt this.budget 0)}}
                R$ {{ this.budget }}
              {{else}}
                <span style="color:#999;">-</span>
              {{/if}}
            </td>
            <td style="padding:10px 12px;border-bottom:1px solid #eee;font-size:13px;color:#666;">{{ this.startDate }}</td>
          </tr>
          {{/each}}
        </table>

        <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:24px;padding-top:16px;border-top:1px solid #eee;">
          <tr>
            <td style="font-size:12px;color:#888;text-align:center;">
              Relatório automático · n8n · {{ generatedAt }}
            </td>
          </tr>
        </table>

      </td>
    </tr>
  </table>
</body>
</html>`,
    };

    @node({
        id: '7fe246ba-fb98-4f88-b375-db3495046db6',
        webhookId: 'a7e86ceb-8c88-4cae-8b3d-2561d82811c3',
        name: 'Send Report',
        type: 'n8n-nodes-base.emailSend',
        version: 2.1,
        position: [656, -480],
    })
    SendReport = {
        fromEmail: 'relatorio@seudominio.com.br',
        subject: '={{ "Relatório Google Ads - " + $json.generatedAt }}',
        options: {},
    };

    @node({
        id: '0b72ce02-db24-44bb-86aa-5f7c8c1b0ac0',
        name: 'Google Ads',
        type: 'n8n-nodes-base.googleAds',
        version: 1,
        position: [-304, -480],
    })
    GoogleAds = {
        resource: '__CUSTOM_API_CALL__',
        requestOptions: {},
    };

    // =====================================================================
    // ROUTAGE ET CONNEXIONS
    // =====================================================================

    @links()
    defineRouting() {
        this.ScheduleTrigger.out(0).to(this.GoogleAds.in(0));
        this.FormatReport.out(0).to(this.BuildEmailHtml.in(0));
        this.BuildEmailHtml.out(0).to(this.SendReport.in(0));
        this.GoogleAds.out(0).to(this.FormatReport.in(0));
    }
}
