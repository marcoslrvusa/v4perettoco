import { workflow, node, links } from '@n8n-as-code/transformer';

// <workflow-map>
// Workflow : [PIA] Agente de Tráfego
// Nodes   : 21  |  Connections: 19
//
// NODE INDEX
// ──────────────────────────────────────────────────────────────────
// Property name                    Node type (short)         Flags
// AgendaDiaria                       scheduleTrigger
// BuscarAgendamentos                 supabase                   [creds]
// CalcularDevidos                    code
// DispararRuns                       code
// ReceberDisparo                     webhook
// CriarRun                           supabase                   [creds]
// BuscarDadosAds                     code
// PreprocessDados                    code
// MontarPrompt                       code
// ChamarLlm                          httpRequest                [creds]
// EstruturarSaida                    code
// AtualizarRun                       supabase                   [creds]
// CriarAprovacao                     supabase                   [creds]
// ReceberAprovacao                   webhook
// BuscarRun                          supabase                   [creds]
// MontarEmail                        code
// MontarExecucao                     code
// CriarTarefasEkyte                  code
// AtualizarRunFinal                  supabase                   [creds]
// AtualizarAprovacao                 supabase                   [creds]
// MontarEmailFinal                   code
//
// ROUTING MAP
// ──────────────────────────────────────────────────────────────────
// AgendaDiaria
//    → BuscarAgendamentos
//      → CalcularDevidos
//        → DispararRuns
//          → ReceberDisparo
//            → CriarRun
//              → BuscarDadosAds
//                → PreprocessDados
//                  → MontarPrompt
//                    → ChamarLlm
//                      → EstruturarSaida
//                        → AtualizarRun
//                          → CriarAprovacao
// ReceberAprovacao
//    → BuscarRun
//      → MontarEmail
//      → MontarExecucao
//        → CriarTarefasEkyte
//          → AtualizarRunFinal
//            → AtualizarAprovacao
//              → MontarEmailFinal
// </workflow-map>

// =====================================================================
// METADATA DU WORKFLOW
// =====================================================================

@workflow({
    id: 'cGVicYpAJ7GMacBZ',
    name: '[PIA] Agente de Tráfego',
    active: true,
    isArchived: false,
    settings: { saveManualExecutions: true, executionOrder: 'v1', callerPolicy: 'workflowsFromSameOwner' },
})
export class PiaAgenteDeTrafegoWorkflow {
    // =====================================================================
    // CONFIGURATION DES NOEUDS
    // =====================================================================

    @node({
        id: 'pia_gt_agenda',
        name: 'Agenda Diária',
        type: 'n8n-nodes-base.scheduleTrigger',
        version: 1.3,
        position: [-650, 300],
    })
    AgendaDiaria = {
        rule: {
            interval: [
                {
                    field: 'hours',
                    hoursInterval: 1,
                    triggerAtMinute: 0,
                },
            ],
        },
    };

    @node({
        id: 'pia_gt_buscar_agendamentos',
        name: 'Buscar Agendamentos',
        type: 'n8n-nodes-base.supabase',
        version: 1,
        position: [-400, 300],
        credentials: { supabaseApi: { id: 'NvEBLQBmAMn0Q2dD', name: 'PIA Supabase (Product)' } },
    })
    BuscarAgendamentos = {
        resource: 'row',
        operation: 'getAll',
        tableId: 'routine_schedules',
        filters: {
            conditions: [
                {
                    keyName: 'is_active',
                    condition: 'eq',
                    keyValue: true,
                },
            ],
        },
        returnAll: true,
    };

    @node({
        id: 'pia_gt_calcular_devidos',
        name: 'Calcular Devidos',
        type: 'n8n-nodes-base.code',
        version: 2,
        position: [-150, 300],
    })
    CalcularDevidos = {
        jsCode: `const items = $input.all();
const agora = new Date();
const dia = agora.getDay();          // 0=domingo, 1=segunda, ..., 6=sabado
const hora = agora.getHours() * 60 + agora.getMinutes();
const diaMes = agora.getDate();

// Mapa de critérios do playbook GT (Regra 80/20): modo → quando roda
const CRITERIOS = {
  diario:     { weekday: [1, 2, 3, 4, 5],  hora: 6 * 60 },       // seg-sex 6h — análise de contas
  criativos:  { weekday: [1],              hora: 8 * 60 },       // 2ª-feira 8h — renovação de criativos
  bi_funil:   { dayOfMonth: [1, 16],       hora: 8 * 60 + 30 },  // dias 1 e 16, 8h30 — BI & funil CRM
  // diagnostico: sob demanda — não entra na agenda
};

const out = [];
for (const item of items) {
  const s = item.json || {};
  const modo = s.modo || '';
  const c = CRITERIOS[modo];
  if (!c) continue;

  const okDia = (c.dayOfMonth ? c.dayOfMonth.includes(diaMes) : false)
    || (c.weekday ? c.weekday.includes(dia) : false);
  if (!okDia) continue;

  const janela = 60; // dispara se o horário ainda não passou mais de 60 min
  const alvo = c.hora;
  const passa = (hora >= alvo && hora <= alvo + janela);
  if (!passa) continue;

  out.push({ json: {
    schedule_id: s.id,
    user_id: s.user_id,
    routine_id: s.routine_id,
    modo: modo,
    cliente: s.cliente || '',
    extra_input: s.extra_input || {},
  }});
}

return out;`,
    };

    @node({
        id: 'pia_gt_disparar_runs',
        name: 'Disparar Runs',
        type: 'n8n-nodes-base.code',
        version: 2,
        position: [100, 300],
    })
    DispararRuns = {
        jsCode: `const items = $input.all();
const out = [];

// Dispara cada agendamento devido chamando o próprio webhook da rotina —
// o fluxo principal (CriarRun → dados → LLM → aprovação) roda intacto.
for (const item of items) {
  const s = item.json || {};
  const body = {
    user_id: s.user_id,
    routine_id: s.routine_id,
    input: Object.assign({ modo: s.modo, cliente: s.cliente }, s.extra_input || {}),
    username: s.username || 'marcos',
    agendado: true,
    schedule_id: s.schedule_id,
  };

  try {
    const res = await this.helpers.httpRequest({
      url: $vars.PIA_GT_WEBHOOK_URL || 'https://n8n.fvmarketing.com.br/webhook/pia-agente-trafego',
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: body,
      json: true,
      timeout: 20000,
    });
    out.push({ json: { schedule_id: s.schedule_id, modo: s.modo, ok: true, resposta: res } });
  } catch (e) {
    out.push({ json: { schedule_id: s.schedule_id, modo: s.modo, ok: false, erro: String(e && e.message || e) } });
  }
}

return out;`,
    };

    @node({
        id: 'pia_gt_webhook',
        webhookId: '5799e7b1-4820-4125-81d4-a1bcf9002fa0',
        name: 'Receber Disparo',
        type: 'n8n-nodes-base.webhook',
        version: 2,
        position: [250, 300],
    })
    ReceberDisparo = {
        httpMethod: 'POST',
        path: 'pia-agente-trafego',
        responseMode: 'onReceived',
        responseData: 'allEntries',
        options: {},
    };

    @node({
        id: 'pia_gt_criar_run',
        name: 'Criar Run',
        type: 'n8n-nodes-base.supabase',
        version: 1,
        position: [450, 300],
        credentials: { supabaseApi: { id: 'NvEBLQBmAMn0Q2dD', name: 'PIA Supabase (Product)' } },
    })
    CriarRun = {
        resource: 'row',
        operation: 'create',
        tableId: 'routine_runs',
        dataToSend: 'defineBelow',
        fieldsUi: {
            fieldValues: [
                {
                    fieldId: 'id',
                    fieldValue: '={{ $json.run_id }}',
                },
                {
                    fieldId: 'user_id',
                    fieldValue: '={{ $json.user_id }}',
                },
                {
                    fieldId: 'routine_id',
                    fieldValue: '={{ $json.routine_id }}',
                },
                {
                    fieldId: 'status',
                    fieldValue: 'running',
                },
                {
                    fieldId: 'input',
                    fieldValue:
                        '={{ JSON.stringify({ modo: $json.input.modo, cliente: $json.input.cliente, executor_id: $json.executor_id, workspace_id: $json.workspace_id, agendado: $json.agendado, schedule_id: $json.schedule_id }) }}',
                },
            ],
        },
    };

    @node({
        id: 'pia_gt_buscar_dados',
        name: 'Buscar Dados Ads',
        type: 'n8n-nodes-base.code',
        version: 2,
        position: [650, 300],
    })
    BuscarDadosAds = {
        jsCode: `const body = $('Receber Disparo').first().json;
const input = body.input || {};
const cliente = input.cliente || '';
const modo = input.modo || 'diario';

// 1) Dados já fornecidos no input (p.ex. extra_input do agendamento) — não refetch
if (input.dados_ads) {
  return [{
    json: {
      run_id: body.run_id,
      user_id: body.user_id,
      routine_id: body.routine_id,
      modo: modo,
      cliente: cliente,
      executor_id: body.executor_id || '',
      workspace_id: body.workspace_id || '',
      agendado: body.agendado === true,
      schedule_id: body.schedule_id || '',
      dados_obtidos: true,
      fonte: 'input',
      dados: (typeof input.dados_ads === 'string' ? JSON.parse(input.dados_ads) : input.dados_ads),
      sem_dados: false,
    },
  }];
}

// 2) Fetch real via V4mos (Meta Ads) quando há credenciais configuradas
const clientId = $vars.V4MOS_CLIENT_ID || '';
const clientSecret = $vars.V4MOS_CLIENT_SECRET || '';
const workspaceId = $vars.V4MOS_WORKSPACE_ID || '';
const V4MOS_URL = $vars.V4MOS_URL || 'https://api.data.v4.marketing';

if (!clientId || !clientSecret || !workspaceId) {
  return [{
    json: {
      run_id: body.run_id,
      user_id: body.user_id,
      routine_id: body.routine_id,
      modo: modo,
      cliente: cliente,
      executor_id: body.executor_id || '',
      workspace_id: body.workspace_id || '',
      agendado: body.agendado === true,
      schedule_id: body.schedule_id || '',
      dados_obtidos: false,
      fonte: 'sem_credenciais',
      dados: [],
      sem_dados: true,
      motivo: 'Sem credenciais V4mos configuradas ($vars.V4MOS_CLIENT_ID/SECRET/WORKSPACE_ID).',
    },
  }];
}

// Modos que não dependem de dados de ads não fazem fetch
const MODOS_SEM_FETCH = ['diagnostico'];
if (MODOS_SEM_FETCH.indexOf(modo) >= 0) {
  return [{
    json: {
      run_id: body.run_id,
      user_id: body.user_id,
      routine_id: body.routine_id,
      modo: modo,
      cliente: cliente,
      executor_id: body.executor_id || '',
      workspace_id: body.workspace_id || '',
      agendado: body.agendado === true,
      schedule_id: body.schedule_id || '',
      dados_obtidos: false,
      fonte: 'modo_sem_dados',
      dados: [],
      sem_dados: false,
    },
  }];
}

const hoje = new Date();
const ate = hoje.toISOString().slice(0, 10);
const de = new Date(hoje.getTime() - 14 * 86400000).toISOString().slice(0, 10);

async function get(path, params) {
  const qs = Object.assign({ workspaceId: workspaceId, since: de, until: ate, limit: 5000 }, params);
  const url = V4MOS_URL + path + '?' + Object.keys(qs).map(function (k) {
    return encodeURIComponent(k) + '=' + encodeURIComponent(qs[k]);
  }).join('&');
  const r = await this.helpers.httpRequest({
    url: url,
    method: 'GET',
    headers: { 'x-client-id': clientId, 'x-client-secret': clientSecret, 'Accept': 'application/json' },
    json: true,
    timeout: 30000,
  });
  return r && r.data ? r.data : (Array.isArray(r) ? r : []);
}

let dados;
try {
  if (modo === 'criativos') {
    const [campanhas, anuncios] = await Promise.all([
      get('/v1/facebook/ads/campaigns', {}),
      get('/v1/facebook/ads/ad', {}),
    ]);
    dados = { campanhas: campanhas, anuncios: anuncios };
  } else {
    const campanhas = await get('/v1/facebook/ads/campaigns', {});
    const anuncios = await get('/v1/facebook/ads/ad', {});
    dados = { campanhas: campanhas, anuncios: anuncios };
  }
  return [{
    json: {
      run_id: body.run_id,
      user_id: body.user_id,
      routine_id: body.routine_id,
      modo: modo,
      cliente: cliente,
      executor_id: body.executor_id || '',
      workspace_id: body.workspace_id || '',
      agendado: body.agendado === true,
      schedule_id: body.schedule_id || '',
      dados_obtidos: true,
      fonte: 'v4mos',
      dados: dados,
      sem_dados: false,
    },
  }];
} catch (e) {
  return [{
    json: {
      run_id: body.run_id,
      user_id: body.user_id,
      routine_id: body.routine_id,
      modo: modo,
      cliente: cliente,
      executor_id: body.executor_id || '',
      workspace_id: body.workspace_id || '',
      agendado: body.agendado === true,
      schedule_id: body.schedule_id || '',
      dados_obtidos: false,
      fonte: 'erro_fetch',
      dados: [],
      sem_dados: true,
      motivo: 'Falha ao buscar dados V4mos: ' + String(e && e.message || e),
    },
  }];
}`,
    };

    @node({
        id: 'pia_gt_preprocess',
        name: 'Preprocess Dados',
        type: 'n8n-nodes-base.code',
        version: 2,
        position: [850, 300],
    })
    PreprocessDados = {
        jsCode: `const ctx = $('Buscar Dados Ads').first().json;
const dados = ctx.dados || {};
const modo = ctx.modo || 'diario';

// ── Normalização defensiva: aceita arrays de campanhas/anúncios com nomes de campos variados ──
function num(v, fallback) {
  const n = parseFloat(String(v == null ? '' : v).replace(/[R$ ]/g, '').replace(',', '.'));
  return isNaN(n) ? (fallback == null ? 0 : fallback) : n;
}
function str(v) { return String(v == null ? '' : v); }

const campanhas = Array.isArray(dados.campanhas) ? dados.campanhas : [];
const anuncios = Array.isArray(dados.anuncios) ? dados.anuncios : [];

const resumo = campanhas.slice(0, 50).map(function (c) {
  return {
    nome: str(c.name || c.nome || c.campaign_name || '—'),
    status: str(c.status || c.campaign_status || ''),
    spend: num(c.spend || c.amount_spent || c.cost, 0),
    impressions: num(c.impressions || c.impr, 0),
    clicks: num(c.clicks, 0),
    conversions: num(c.conversions || c.actions || c.results, 0),
    cpa: num(c.cpa || c.cost_per_action || c.cost_per_conversion, 0),
    roas: num(c.roas, 0),
    ctr: num(c.ctr, 0),
    cpm: num(c.cpm, 0),
    frequency: num(c.frequency, 0),
    objective: str(c.objective || c.goal || ''),
  };
});

// ── Cálculo de KPIs agregados por plataforma (Meta via V4mos) ──
const tot = {
  spend: resumo.reduce(function (a, c) { return a + c.spend; }, 0),
  impressions: resumo.reduce(function (a, c) { return a + c.impressions; }, 0),
  clicks: resumo.reduce(function (a, c) { return a + c.clicks; }, 0),
  conversions: resumo.reduce(function (a, c) { return a + c.conversions; }, 0),
};
tot.cpa = tot.conversions ? tot.spend / tot.conversions : 0;
tot.ctr = tot.impressions ? tot.clicks / tot.impressions * 100 : 0;
tot.cpm = tot.impressions ? tot.spend / tot.impressions * 1000 : 0;

// ── Protocolo de flags (quantitativo, do playbook GT) ──
const flags = [];
if (tot.cpa > 100 && tot.conversions >= 2) flags.push({ flag: 'CPA acima do teto', detalhe: 'CPA ' + tot.cpa.toFixed(2) + ' > R$ 100' });
if (tot.ctr > 0 && tot.ctr < 0.5) flags.push({ flag: 'CTR em queda', detalhe: 'CTR ' + tot.ctr.toFixed(2) + '% < 0.5%' });
resumo.forEach(function (c) {
  if (c.frequency > 8) flags.push({ flag: 'Frequência alta', detalhe: c.nome + ' freq ' + c.frequency.toFixed(1) + ' > 8' });
  if (c.ctr > 0 && c.ctr < 0.3) flags.push({ flag: 'CTR crítico', detalhe: c.nome + ' CTR ' + c.ctr.toFixed(2) + '%' });
});
// ROAS abaixo da meta exige histórico (não dá para calcular em 1 fetch) — sinaliza se disponível
resumo.forEach(function (c) {
  if (c.roas > 0 && c.roas < 2) flags.push({ flag: 'ROAS abaixo da meta', detalhe: c.nome + ' ROAS ' + c.roas.toFixed(2) + ' < 2.0' });
});

// ── Sinaleira (verde/amarelo/vermelho) ──
const vermelho = flags.filter(function (f) { return f.flag === 'CPA acima do teto' || f.flag === 'ROAS abaixo da meta'; }).length;
const amarelo = flags.filter(function (f) { return f.flag === 'CTR em queda' || f.flag === 'Frequência alta'; }).length;
let sinaleira = 'verde';
if (vermelho > 0) sinaleira = 'vermelho';
else if (amarelo > 0 || (tot.ctr > 0 && tot.ctr < 0.5)) sinaleira = 'amarelo';

return [{
  json: {
    run_id: ctx.run_id,
    user_id: ctx.user_id,
    routine_id: ctx.routine_id,
    modo: modo,
    cliente: ctx.cliente,
    executor_id: ctx.executor_id || '',
    workspace_id: ctx.workspace_id || '',
    agendado: ctx.agendado,
    schedule_id: ctx.schedule_id,
    dados_obtidos: ctx.dados_obtidos,
    fonte: ctx.fonte,
    sem_dados: ctx.sem_dados,
    motivo: ctx.motivo || '',
    kpis: tot,
    sinaleira: sinaleira,
    flags: flags,
    campanhas: resumo.slice(0, 30),
    anuncios: anuncios.slice(0, 30),
  },
}];`,
    };

    @node({
        id: 'pia_gt_montar_prompt',
        name: 'Montar Prompt',
        type: 'n8n-nodes-base.code',
        version: 2,
        position: [1050, 300],
    })
    MontarPrompt = {
        jsCode: `const body = $('Receber Disparo').first().json;
const ctx = $('Preprocess Dados').first().json;
const input = body.input || {};
const cliente = input.cliente || ctx.cliente || '';
const modo = ctx.modo || 'diario';

const systemInstruction = body.system_instruction
  || 'Você é a Rotina Gestor de Tráfego da Peretto & Co. (Regra 80/20). Execute FPA (Fatos, Padrões, Ações), TOC (gargalo único), 4Vs e Médico vs Garçom. Nunca invente dados — números sempre com fonte e período. Responda em português brasileiro.';

// ── Critérios de execução (playbook GT): dados mínimos obrigatórios por modo ──
const REQUISITOS = {
  diario:       ['cliente'],
  criativos:    ['cliente'],
  bi_funil:     ['cliente', 'leads'],   // leads/MQLs do CRM (input ou extra_input)
  diagnostico:  ['cliente', 'sintoma'], // sintoma OU flag descrita
};

const faltantes = (REQUISITOS[modo] || []).filter(function (k) {
  const v = input[k] || (k === 'leads' ? (input.mqls || input.leads_planilha) : '');
  return v === undefined || v === null || String(v).trim() === '';
});

if (faltantes.length) {
  throw new Error('[critérios de execução] modo=' + modo + ' sem dados mínimos: faltam ' + faltantes.join(', ') + '. Informe no input ou aguarde a fonte.');
}

// ── Contexto de dados pré-processados para o LLM ──
const kpis = ctx.kpis || {};
const linhasCampanhas = (ctx.campanhas || []).slice(0, 20).map(function (c) {
  return '- ' + c.nome + ' | status: ' + c.status + ' | spend: R$' + c.spend.toFixed(2) + ' | impr: ' + c.impressions + ' | cliques: ' + c.clicks + ' | conv: ' + c.conversions + ' | CPA: ' + (c.cpa ? 'R$' + c.cpa.toFixed(2) : '—') + ' | CTR: ' + (c.ctr ? c.ctr.toFixed(2) + '%' : '—') + ' | freq: ' + (c.frequency ? c.frequency.toFixed(1) : '—');
}).join('\\n');

const blocoDados = ctx.dados_obtidos
  ? 'Dados reais (fonte: ' + ctx.fonte + '):\\n' +
    'KPIs agregados: spend R$' + kpis.spend.toFixed(2) + ' | impr ' + kpis.impressions + ' | cliques ' + kpis.clicks + ' | conv ' + kpis.conversions + ' | CPA ' + (kpis.cpa ? 'R$' + kpis.cpa.toFixed(2) : '—') + ' | CTR ' + (kpis.ctr ? kpis.ctr.toFixed(2) + '%' : '—') + ' | CPM ' + (kpis.cpm ? 'R$' + kpis.cpm.toFixed(2) : '—') + '\\n' +
    'Sinaleira: ' + ctx.sinaleira + '\\n' +
    'Flags: ' + JSON.stringify(ctx.flags || []) + '\\n' +
    'Campanhas (top 20):\\n' + (linhasCampanhas || '—')
  : 'DADOS DE ADS NÃO DISPONÍVEIS (fonte: ' + ctx.fonte + '). ' + (ctx.motivo || '') + ' Siga o protocolo: não invente números, peça a fonte (API de anúncios, Torre de Comando, relatório anterior) e faça a análise qualitativa possível com o que existe no input.';

// ── Prompt do modo ──
const modoPrompt = {
  diario: 'Analise de contas (micro e macro otimizacoes): (1) Google Ads — termos de pesquisa 7/14d, CPA/impressoes/CTR/CPC, pacing vs Torre de Comando, recomendacoes do Google (aplicar so o estrategico); (2) Meta Ads — status de veiculacao, CPL/CPC, CPM/fadiga de criativo, pausa preventiva, ajustes de orcamento, estrategia por objetivo (Alcance→CPM/freq, Consideracao→engajamento GA4); (3) comparativa CAC/volume — ecommerce 7/14d (custo por compra, ticket medio, ROAS), inside sales (volume de leads, CPL, custo por MQL 14-30d). Entregue resumo executivo por plataforma com sinaleira, variacao 7 vs 14 dias, anomalias e plano de acao priorizado (urgente/3 dias/semana).',
  criativos: 'Renovacao de criativos: (1) Meta — identifique criativos com sinais de fadiga (frequencia alta, CTR caindo, CPM subindo) e proponha renovacao por conjunto de anuncios com conceito alinhado ao que performou; (2) Google — proponha atualizacao de PMax/Demand Gen por estrategia do mes, baixa performance dos ativos, sazonalidade ou A/B. Entregue lista de criativos com prioridade, o que trocar, por que (evidencia) e conceito sugerido.',
  bi_funil: 'BI & funil CRM (media 15 dias): cruze MQLs com UTM Source/Campaign para identificar canais que geram clientes qualificados; identifique UTM Term (palavras-chave) que converteram em MQL/SQL; calcule Custo por MQL e Custo por SQL (investimento / leads qualificados) e compare com periodos anteriores. Entregue tabela de canais x MQL/SQL x custo por MQL/SQL, top termos, gaps por canal (gasto sem qualificacao) e oportunidades de escala.',
  diagnostico: 'Diagnostico de gaps (framework O/H/C/P): auditoria campanha→conjunto→anuncio→tracking→CRM→comunicacao. Aplique a estrutura padrao: Objetivo → Hipoteses/Sintoma → Causa Raiz → Plano de Acao. Entregue JSON no Framework de Resolucao V4: objetivo, hipotese_sintoma, causa_raiz, plano_acao (acao/prazo/dono/evidencia), evidencias, riscos, prioridade, previsao.',
}[modo] || 'Execute a rotina conforme sua instrucao.';

const userPrompt = 'modo=' + modo + '\\n' + modoPrompt + '\\n\\n' + blocoDados + '\\n\\nRESPONDA UNICAMENTE EM JSON VALIDO com a seguinte estrutura (sem markdown, sem texto fora do JSON):\\n' +
'{\\n  "resumo": "resumo da analise em markdown (com numeros e fontes)",\\n  "sinaleira": "verde|amarelo|vermelho",\\n  "anomalias": ["lista de anomalias encontradas"],\\n  "tarefas": [\\n    { "titulo": "titulo curto e objetivo", "descricao": "detalhe do que fazer", "prioridade": "urgente|alta|media|baixa", "prazo": "YYYY-MM-DD", "dono": "username ou nome da pessoa responsavel" }\\n  ]\\n}\\n' +
'\\nREGRA IMPORTANTE PARA O CAMPO "prazo": converta prazos relativos em datas absolutas YYYY-MM-DD. Hoje é ' + new Date().toISOString().slice(0, 10) + '.\\n' +
'\\nATENCAO: preencha com dados REAIS do input. NAO repita o exemplo. "tarefas" deve conter as acoes do plano priorizado (pelo menos 1). Se nao houver acao, tarefas: [].\\n' +
'\\n\\nInput:\\n' + JSON.stringify(input, null, 2);

return [{
  json: {
    run_id: body.run_id,
    user_id: body.user_id,
    routine_id: body.routine_id,
    requires_approval: body.requires_approval !== false,
    username: body.username || 'marcos',
    user_email: body.user_email || '',
    cliente: cliente,
    modo: modo,
    executor_id: body.executor_id || '',
    workspace_id: body.workspace_id || '',
    agendado: body.agendado === true,
    schedule_id: body.schedule_id || '',
    system_instruction: systemInstruction,
    user_prompt: userPrompt,
  },
}];`,
    };

    @node({
        id: 'pia_gt_llm',
        name: 'Chamar LLM',
        type: 'n8n-nodes-base.httpRequest',
        version: 4.2,
        position: [1250, 300],
        credentials: { httpHeaderAuth: { id: 'ARFP5ADvcOh9MNoM', name: 'PIA LLM (LiteLLM) Header' } },
    })
    ChamarLlm = {
        method: 'POST',
        url: '={{ $vars?.PIA_LITELLM_URL || "https://litellm.fvmarketing.com.br" }}/v1/chat/completions',
        authentication: 'genericCredentialType',
        genericAuthType: 'httpHeaderAuth',
        sendHeaders: true,
        headerParameters: {
            parameters: [
                {
                    name: 'Content-Type',
                    value: 'application/json',
                },
            ],
        },
        sendBody: true,
        specifyBody: 'json',
        jsonBody:
            '={{ JSON.stringify({ model: "deepseek-v4-flash-free", messages: [{ role: "system", content: $("Montar Prompt").item.json.system_instruction }, { role: "user", content: $("Montar Prompt").item.json.user_prompt }], max_tokens: 16384, temperature: 0.3 }) }}',
        options: {
            timeout: 120000,
            retryOnFail: true,
            maxTries: 3,
            waitBetweenTries: 3000,
        },
    };

    @node({
        id: 'pia_gt_estruturar',
        name: 'Estruturar Saída',
        type: 'n8n-nodes-base.code',
        version: 2,
        position: [1450, 300],
    })
    EstruturarSaida = {
        jsCode: `const items = $input.all();
const out = [];
const ctx = $('Montar Prompt').item.json;

function repairJson(s) {
  let out = ''; let inStr = false; let i = 0;
  while (i < s.length) {
    const c = s[i];
    if (inStr) {
      if (c === '\\\\') { out += c; i++; if (i < s.length) { out += s[i]; i++; } continue; }
      if (c === '"') { inStr = false; out += c; i++; continue; }
      if (c === '\\n' || c === '\\r') { out += '\\\\n'; i++; continue; }
      if (c === '\\t') { out += '\\\\t'; i++; continue; }
      out += c; i++;
    } else {
      if (c === '"') inStr = true;
      out += c; i++;
    }
  }
  return out;
}

for (const item of items) {
  const raw = (item.json.choices && item.json.choices[0] && item.json.choices[0].message && item.json.choices[0].message.content)
    || JSON.stringify(item.json).slice(0, 3000);
  const tokens = (item.json.usage && item.json.usage.total_tokens) || 0;

  let parsed = { resumo: raw, sinaleira: '', anomalias: [], tarefas: [] };
  try {
    const candidatos = [];
    const global = raw.match(/{[sS]*}/g);
    if (global) candidatos.push.apply(candidatos, global);
    if (!candidatos.length) candidatos.push(raw);
    for (let i = candidatos.length - 1; i >= 0; i--) {
      const c = candidatos[i];
      try {
        const obj = JSON.parse(repairJson(c));
        if (obj && (typeof obj.resumo === 'string' || Array.isArray(obj.tarefas))) {
          parsed = obj;
          break;
        }
      } catch (e) { /* tenta proximo */ }
    }
  } catch (e) {
    parsed = { resumo: raw, sinaleira: '', anomalias: [], tarefas: [] };
  }

  const tarefas = Array.isArray(parsed.tarefas) ? parsed.tarefas : [];
  const anomalias = Array.isArray(parsed.anomalias) ? parsed.anomalias : [];

  out.push({
    json: {
      run_id: ctx.run_id,
      user_id: ctx.user_id,
      routine_id: ctx.routine_id,
      requires_approval: ctx.requires_approval !== false,
      username: ctx.username || 'marcos',
      user_email: ctx.user_email || '',
      cliente: ctx.cliente || 'Peretto & Co.',
      modo: ctx.modo,
      executor_id: ctx.executor_id || '',
      workspace_id: ctx.workspace_id || '',
      resumo: parsed.resumo || raw,
      sinaleira: parsed.sinaleira || '',
      anomalias: anomalias,
      tarefas: tarefas,
      resposta: raw,
      total_tokens: tokens,
    },
  });
}

return out;`,
    };

    @node({
        id: 'pia_gt_atualizar_run',
        name: 'Atualizar Run',
        type: 'n8n-nodes-base.supabase',
        version: 1,
        position: [1650, 300],
        credentials: { supabaseApi: { id: 'NvEBLQBmAMn0Q2dD', name: 'PIA Supabase (Product)' } },
    })
    AtualizarRun = {
        resource: 'row',
        operation: 'update',
        tableId: 'routine_runs',
        filters: {
            conditions: [
                {
                    keyName: 'id',
                    condition: 'eq',
                    keyValue: '={{ $json.run_id }}',
                },
            ],
        },
        dataToSend: 'defineBelow',
        fieldsUi: {
            fieldValues: [
                {
                    fieldId: 'status',
                    fieldValue: '={{ $json.requires_approval ? "awaiting_approval" : "completed" }}',
                },
                {
                    fieldId: 'output_summary',
                    fieldValue:
                        '={{ JSON.stringify({ resumo: $json.resumo, sinaleira: $json.sinaleira, anomalias: $json.anomalias, tarefas: $json.tarefas, texto: $json.resposta }) }}',
                },
                {
                    fieldId: 'total_tokens',
                    fieldValue: '={{ $json.total_tokens }}',
                },
                {
                    fieldId: 'finished_at',
                    fieldValue: '={{ new Date().toISOString() }}',
                },
            ],
        },
    };

    @node({
        id: 'pia_gt_criar_aprovacao',
        name: 'Criar Aprovação',
        type: 'n8n-nodes-base.supabase',
        version: 1,
        position: [1850, 300],
        credentials: { supabaseApi: { id: 'NvEBLQBmAMn0Q2dD', name: 'PIA Supabase (Product)' } },
    })
    CriarAprovacao = {
        resource: 'row',
        operation: 'create',
        tableId: 'pending_approvals',
        dataToSend: 'defineBelow',
        fieldsUi: {
            fieldValues: [
                {
                    fieldId: 'username',
                    fieldValue: '={{ $("Estruturar Saída").item.json.username }}',
                },
                {
                    fieldId: 'cliente',
                    fieldValue: '={{ $("Estruturar Saída").item.json.cliente }}',
                },
                {
                    fieldId: 'tipo',
                    fieldValue: '={{ "rotina_gt_" + $("Estruturar Saída").item.json.modo }}',
                },
                {
                    fieldId: 'conteudo',
                    fieldValue: '={{ $("Estruturar Saída").item.json.resposta }}',
                },
                {
                    fieldId: 'status',
                    fieldValue: 'pending',
                },
            ],
        },
    };

    @node({
        id: 'pia_gt_aprovacao_webhook',
        webhookId: '3948c20b-8cb2-4a53-ac04-facc646e74a3',
        name: 'Receber Aprovação',
        type: 'n8n-nodes-base.webhook',
        version: 2,
        position: [250, 700],
    })
    ReceberAprovacao = {
        httpMethod: 'POST',
        path: 'pia-agente-trafego-aprovar',
        responseMode: 'onReceived',
        responseData: 'allEntries',
        options: {},
    };

    @node({
        id: 'pia_gt_buscar_run',
        name: 'Buscar Run',
        type: 'n8n-nodes-base.supabase',
        version: 1,
        position: [450, 700],
        credentials: { supabaseApi: { id: 'NvEBLQBmAMn0Q2dD', name: 'PIA Supabase (Product)' } },
    })
    BuscarRun = {
        resource: 'row',
        operation: 'getAll',
        tableId: 'routine_runs',
        filters: {
            conditions: [
                {
                    keyName: 'id',
                    condition: 'eq',
                    keyValue: '={{ $json.body.run_id }}',
                },
            ],
        },
        returnAll: false,
        limit: 1,
    };

    @node({
        id: 'pia_gt_montar_email',
        name: 'Montar Email',
        type: 'n8n-nodes-base.code',
        version: 2,
        position: [650, 700],
    })
    MontarEmail = {
        jsCode: `const run = $('Buscar Run').first().json;
const input = run.input || {};
const output = run.output_summary || {};
const parsed = typeof output === 'string' ? JSON.parse(output) : output;
const resposta = parsed.resumo || parsed.texto || '';

const resumo = [
  '# Resumo da rotina ' + (input.modo || 'diario'),
  '',
  '## Contexto',
  '- Cliente: ' + (input.cliente || '—'),
  '- Modo: ' + (input.modo || 'diario'),
  '- Sinaleira: ' + (parsed.sinaleira || '—'),
  '- Executado em: ' + (run.finished_at || new Date().toISOString()),
  '',
  '## Análise gerada pela IA',
  '',
  (resposta || 'Sem resposta gerada.').slice(0, 6000),
  '',
  '---',
  'Gerado automaticamente pelo PIA — Hub de Agentes IA.',
].join('\\n');

return [{
  json: {
    run_id: run.id,
    user_id: run.user_id,
    cliente: input.cliente || '—',
    modo: input.modo || 'diario',
    resposta: resposta,
    tarefas: parsed.tarefas || [],
    email_body: resumo,
    to_email: $('Receber Aprovação').item.json.body.email_to || '',
  },
}];`,
    };

    @node({
        id: 'pia_gt_montar_execucao',
        name: 'Montar Execução',
        type: 'n8n-nodes-base.code',
        version: 2,
        position: [650, 900],
    })
    MontarExecucao = {
        jsCode: `const run = $('Buscar Run').first().json;
const input = (typeof run.input === 'string' ? JSON.parse(run.input) : run.input) || {};
const output = (typeof run.output_summary === 'string' ? JSON.parse(run.output_summary) : run.output_summary) || {};
const tarefas = Array.isArray(output.tarefas) ? output.tarefas : [];

const body = $('Receber Aprovação').item.json.body || {};
const executorId = body.executor_id || input.executor_id || '';
const workspaceId = body.workspace_id || input.workspace_id || 16032;
const userEmail = body.email_to || input.user_email || '';

// Modos GT geram tarefas no Ekyte (ações concretas de tráfego)
const MODOS_COM_EKYTE = ['diario', 'criativos', 'bi_funil', 'diagnostico'];
const exigeEkyte = MODOS_COM_EKYTE.indexOf(input.modo || '') >= 0;

if (exigeEkyte && !executorId) throw new Error('Sem executor_id: informe o ID do usuario Ekyte que rodou a rotina no body do webhook.');
if (exigeEkyte && !workspaceId) throw new Error('Sem workspace_id: informe o workspace do cliente no body do webhook.');

const hoje = new Date();
const iso = function (d) { return d.toISOString(); };
const somaDias = function (dias) { const d = new Date(hoje); d.setDate(d.getDate() + dias); return d; };
const p = function (pri) {
  const v = String(pri || '').toLowerCase();
  return v === 'urgente' ? 400 : v === 'alta' ? 300 : v === 'media' ? 200 : v === 'baixa' ? 100 : 200;
};

const TASK_TYPE = 55845;
const FASES = [18232, 18232];

const tasks = exigeEkyte ? tarefas.map(function (t) {
  const titulo = String(t.titulo || '').trim();
  if (!titulo) return null;
  const prazo = String(t.prazo || '').slice(0, 10);
  let fim;
  if (prazo && !isNaN(new Date(prazo).getTime())) {
    fim = new Date(prazo + 'T18:00:00');
  } else {
    fim = somaDias(7);
  }
  const inicio = new Date(hoje);
  const flow = [
    { active: 1, effort: 0, executorId: executorId, phaseId: FASES[0], sequential: 1, taskTypeId: TASK_TYPE },
    { active: 1, effort: 0, executorId: executorId, phaseId: FASES[1], sequential: 2, taskTypeId: TASK_TYPE },
  ];
  return {
    title: titulo,
    description: String(t.descricao || 'Criada pelo PIA — Hub de Agentes IA.'),
    phaseStartDate: iso(inicio),
    phaseDueDate: iso(fim),
    currentDueDate: iso(fim),
    estimatedTime: 60,
    workspaceId: parseInt(workspaceId, 10),
    executorId: executorId,
    phaseId: FASES[0],
    ctcTaskTypeId: TASK_TYPE,
    situation: 10,
    allocationType: 10,
    priority: p(t.prioridade),
    flow: flow,
  };
}).filter(Boolean) : [];

if (exigeEkyte && !tasks.length) throw new Error('Nenhuma tarefa valida extraida da resposta do LLM.');

return [{
  json: {
    run_id: run.id,
    user_id: run.user_id,
    username: input.username || 'marcos',
    user_email: userEmail,
    cliente: input.cliente || '—',
    modo: input.modo || 'diario',
    executor_id: executorId,
    workspace_id: workspaceId,
    resumo: output.resumo || '',
    tasks: tasks,
  },
}];`,
    };

    @node({
        id: 'pia_gt_criar_tarefas_ekyte',
        name: 'Criar Tarefas Ekyte',
        type: 'n8n-nodes-base.code',
        version: 2,
        position: [850, 900],
    })
    CriarTarefasEkyte = {
        jsCode: `const cfg = $('Montar Execução').first().json;
const EKYTE_TOKEN = '83dc09fffd00860c43ddf3aaa3d302ebccb42c48f79267daf0de883dc19e60f2';
const EKYTE_URL = 'https://api.ekyte.com/mcp?token=' + EKYTE_TOKEN;

if (!Array.isArray(cfg.tasks) || cfg.tasks.length === 0) {
  return [{
    json: {
      run_id: cfg.run_id,
      user_id: cfg.user_id,
      username: cfg.username,
      user_email: cfg.user_email,
      cliente: cfg.cliente,
      modo: cfg.modo,
      executor_id: cfg.executor_id || '',
      workspace_id: cfg.workspace_id || '',
      resumo: cfg.resumo || '',
      tasks: [],
      qtd_criadas: 0,
      qtd_falhas: 0,
      falhas: [],
    },
  }];
}

async function chamar(tool, args) {
  const res = await this.helpers.httpRequest({
    url: EKYTE_URL,
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream' },
    body: { jsonrpc: '2.0', id: Date.now(), method: 'tools/call', params: { name: tool, arguments: args } },
    json: true,
  });
  const parsed = res || {};
  if (parsed.error) return { erro: parsed.error.message || JSON.stringify(parsed.error) };
  const content = parsed.result && parsed.result.content;
  const txt = (content && content[0] && content[0].text) || '';
  let v;
  try { v = JSON.parse(txt); } catch (e) { v = txt; }
  if (v && typeof v === 'object' && v.text && (v.id || Object.keys(v).length <= 2)) {
    return { erro: v.text };
  }
  return { ok: true, value: v };
}

const results = [];
for (const t of cfg.tasks) {
  const r = await chamar('create_task', t);
  const id = r.ok ? (r.value || '') : '';
  results.push({ titulo: t.title, ok: r.ok, taskId: id, erro: r.erro || '' });
}

const falhas = results.filter(function (r) { return !r.ok; });
return [{
  json: {
    run_id: cfg.run_id,
    user_id: cfg.user_id,
    username: cfg.username,
    user_email: cfg.user_email,
    cliente: cfg.cliente,
    modo: cfg.modo,
    executor_id: cfg.executor_id,
    workspace_id: cfg.workspace_id,
    resumo: cfg.resumo,
    tasks: results,
    qtd_criadas: results.length - falhas.length,
    qtd_falhas: falhas.length,
    falhas: falhas,
  },
}];`,
    };

    @node({
        id: 'pia_gt_atualizar_run_final',
        name: 'Atualizar Run Final',
        type: 'n8n-nodes-base.supabase',
        version: 1,
        position: [1050, 900],
        credentials: { supabaseApi: { id: 'NvEBLQBmAMn0Q2dD', name: 'PIA Supabase (Product)' } },
    })
    AtualizarRunFinal = {
        resource: 'row',
        operation: 'update',
        tableId: 'routine_runs',
        filters: {
            conditions: [
                {
                    keyName: 'id',
                    condition: 'eq',
                    keyValue: '={{ $json.run_id }}',
                },
            ],
        },
        dataToSend: 'defineBelow',
        fieldsUi: {
            fieldValues: [
                {
                    fieldId: 'status',
                    fieldValue: 'completed',
                },
                {
                    fieldId: 'output_summary',
                    fieldValue:
                        '={{ JSON.stringify({ resumo: $json.resumo, tasks_ekyte: $json.tasks, qtd_criadas: $json.qtd_criadas }) }}',
                },
            ],
        },
    };

    @node({
        id: 'pia_gt_atualizar_aprovacao',
        name: 'Atualizar Aprovação',
        type: 'n8n-nodes-base.supabase',
        version: 1,
        position: [1250, 900],
        credentials: { supabaseApi: { id: 'NvEBLQBmAMn0Q2dD', name: 'PIA Supabase (Product)' } },
    })
    AtualizarAprovacao = {
        resource: 'row',
        operation: 'update',
        tableId: 'pending_approvals',
        filters: {
            conditions: [
                {
                    keyName: 'id',
                    condition: 'eq',
                    keyValue: '={{ $("Receber Aprovação").item.json.body.approval_id }}',
                },
            ],
        },
        dataToSend: 'defineBelow',
        fieldsUi: {
            fieldValues: [
                {
                    fieldId: 'status',
                    fieldValue: 'approved',
                },
            ],
        },
    };

    @node({
        id: 'pia_gt_email_final',
        name: 'Montar Email Final',
        type: 'n8n-nodes-base.code',
        version: 2,
        position: [1450, 900],
    })
    MontarEmailFinal = {
        jsCode: `const ex = $('Criar Tarefas Ekyte').first().json;
const resumo = ex.resumo || '';
const tasks = ex.tasks || [];
const linhas = tasks.map(function (t) {
  return '- ' + (t.ok ? '✅' : '❌') + ' **' + t.titulo + '** — ' + (t.ok ? ('task #' + t.taskId) : ('falhou: ' + t.erro));
}).join('\\n');

const secaoTarefas = tasks.length
  ? '## Tarefas criadas no Ekyte (' + ex.qtd_criadas + ' de ' + tasks.length + ')\\n\\n' + linhas
  : '## Tarefas\\n\\nNenhuma tarefa criada — modo de entrega sem ações no Ekyte.';

const corpo = [
  '# Execução da rotina ' + ex.modo,
  '',
  '**Cliente:** ' + ex.cliente,
  '**Executado por:** ' + ex.username,
  '',
  '## Análise',
  '',
  (resumo || 'Sem resumo gerado.').slice(0, 5000),
  '',
  secaoTarefas,
  '',
  '---',
  'Gerado automaticamente pelo PIA — Hub de Agentes IA.',
].join('\\n');

return [{
  json: {
    run_id: ex.run_id,
    cliente: ex.cliente,
    modo: ex.modo,
    email_body: corpo,
    to_email: ex.user_email || '',
  },
}];`,
    };

    // =====================================================================
    // ROUTAGE ET CONNEXIONS
    // =====================================================================

    @links()
    defineRouting() {
        this.AgendaDiaria.out(0).to(this.BuscarAgendamentos.in(0));
        this.BuscarAgendamentos.out(0).to(this.CalcularDevidos.in(0));
        this.CalcularDevidos.out(0).to(this.DispararRuns.in(0));
        this.DispararRuns.out(0).to(this.ReceberDisparo.in(0));
        this.ReceberDisparo.out(0).to(this.CriarRun.in(0));
        this.CriarRun.out(0).to(this.BuscarDadosAds.in(0));
        this.BuscarDadosAds.out(0).to(this.PreprocessDados.in(0));
        this.PreprocessDados.out(0).to(this.MontarPrompt.in(0));
        this.MontarPrompt.out(0).to(this.ChamarLlm.in(0));
        this.ChamarLlm.out(0).to(this.EstruturarSaida.in(0));
        this.EstruturarSaida.out(0).to(this.AtualizarRun.in(0));
        this.AtualizarRun.out(0).to(this.CriarAprovacao.in(0));
        this.ReceberAprovacao.out(0).to(this.BuscarRun.in(0));
        this.BuscarRun.out(0).to(this.MontarEmail.in(0));
        this.BuscarRun.out(0).to(this.MontarExecucao.in(0));
        this.MontarExecucao.out(0).to(this.CriarTarefasEkyte.in(0));
        this.CriarTarefasEkyte.out(0).to(this.AtualizarRunFinal.in(0));
        this.AtualizarRunFinal.out(0).to(this.AtualizarAprovacao.in(0));
        this.AtualizarAprovacao.out(0).to(this.MontarEmailFinal.in(0));
    }
}
