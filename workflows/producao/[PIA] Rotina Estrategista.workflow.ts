import { workflow, node, links } from '@n8n-as-code/transformer';

// <workflow-map>
// Workflow : [PIA] Rotina Estrategista
// Nodes   : 9  |  Connections: 7
//
// NODE INDEX
// ──────────────────────────────────────────────────────────────────
// Property name                    Node type (short)         Flags
// WebhookRotina                      webhook
// ReceberAprovacao                   webhook
// ListarRotina                       supabase                   [creds]
// MontarPrompt                       code
// CriarRun                           supabase                   [creds]
// ChamarLlm                          httpRequest                [creds]
// EstruturarSaida                    code
// AtualizarRun                       supabase                   [creds]
// CriarAprovacao                     supabase                   [creds]
//
// ROUTING MAP
// ──────────────────────────────────────────────────────────────────
// WebhookRotina
//    → MontarPrompt
//      → CriarRun
//        → ChamarLlm
//          → EstruturarSaida
//            → AtualizarRun
//            → CriarAprovacao
// ReceberAprovacao
//    → AtualizarRun (↩ loop)
// </workflow-map>

// =====================================================================
// METADATA DU WORKFLOW
// =====================================================================

@workflow({
    id: 'n1JKkepCRqspJNz2',
    name: '[PIA] Rotina Estrategista',
    active: true,
    isArchived: false,
    settings: {
        saveManualExecutions: true,
        executionOrder: 'v1',
        callerPolicy: 'workflowsFromSameOwner',
        saveDataErrorExecution: 'all',
    },
})
export class PiaRotinaEstrategistaWorkflow {
    // =====================================================================
    // CONFIGURATION DES NOEUDS
    // =====================================================================

    @node({
        id: 'pia_estrategista_digital_webhook',
        webhookId: '7c820c1e-65f4-4600-85d7-f80447e60396',
        name: 'Webhook Rotina',
        type: 'n8n-nodes-base.webhook',
        version: 2,
        position: [50, 300],
    })
    WebhookRotina = {
        httpMethod: 'POST',
        path: 'pia-rotina-estrategista',
        responseMode: 'onReceived',
        responseData: 'allEntries',
        options: {},
    };

    @node({
        id: 'pia_estrategista_digital_receber_aprovacao',
        webhookId: '3b554ef3-8c48-480c-91db-b8213bbee159',
        name: 'Receber Aprovacao',
        type: 'n8n-nodes-base.webhook',
        version: 2,
        position: [50, 520],
    })
    ReceberAprovacao = {
        httpMethod: 'POST',
        path: 'pia-rotina-estrategista-aprovar',
        responseMode: 'onReceived',
        responseData: 'allEntries',
        options: {},
    };

    @node({
        id: 'pia_estrategista_digital_listar_rotina',
        name: 'Listar Rotina',
        type: 'n8n-nodes-base.supabase',
        version: 1,
        position: [250, 300],
        credentials: { supabaseApi: { id: 'NvEBLQBmAMn0Q2dD', name: 'PIA Supabase (Product)' } },
    })
    ListarRotina = {
        resource: 'row',
        operation: 'getAll',
        tableId: 'routines',
        filters: {
            conditions: [
                {
                    keyName: 'slug',
                    condition: 'eq',
                    keyValue: '={{ $json.body.routine_slug }}',
                },
            ],
        },
        returnAll: true,
    };

    @node({
        id: 'pia_estrategista_digital_montar_prompt',
        name: 'Montar Prompt',
        type: 'n8n-nodes-base.code',
        version: 2,
        position: [450, 300],
    })
    MontarPrompt = {
        mode: 'runOnceForAllItems',
        language: 'javaScript',
        jsCode: `const body = $json.body || {};
const inputData = body.input || {};
const modo = inputData.modo || 'diagnostico';
const cliente = inputData.cliente || 'Peretto & Co.';

const REQUISITOS = {diagnostico: ["cliente"],
  relatorio: ["cliente"]};
const faltantes = (REQUISITOS[modo] || []).filter((r) => !(inputData[r] || '').toString().trim());
if (faltantes.length > 0) {
  return [{
    json: {
      error: 'Campos obrigatorios faltando: ' + faltantes.join(', '),
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
      system_instruction: '',
      user_prompt: '',
    },
  }];
}

const MODOS = {diagnostico: 'Diagnostique a estrategia digital do cliente: presencia digital, funil, oferta, posicionamento. Use sabatina interna e principios V4. Entregue plano priorizado.',
  relatorio: 'Gere relatorio de evolucao da estrategia digital: o que foi implementado, o que funcionou, proximos passos com responsaveis e prazos.'};
const modoPrompt = MODOS[modo] || 'Execute a rotina conforme sua instrucao.';

const systemInstruction = body.system_instruction
  || "# SYSTEM INSTRUCTION — Rotina Kora Kotler (Estrategista)\\n\\n> Texto canônico injetado em \`routine_templates.system_instruction\` (seed: \`supabase/seed-rotinas.sql\`).\\n> Editável aqui (git) e sincronizado ao banco. Não recompila imagem.\\n\\n---\\n\\nVocê é a **Rotina Kora Kotler (Estrategista)** da Peretto & Co. — agente especialista em estratégia de marketing e posicionamento. Seu papel: enxergar a matriz do jogo antes de mover a peça. Leia o cenário do cliente (mercado, concorrência, público, oferta), defina o caminho estratégico com apostas prioritárias e entregue um documento estruturado que sustenta decisões de check-in e QBR.\\n\\n## Princípios metodológicos (filtros obrigatórios antes de QUALQUER ação)\\n\\n- **4Vs**: Vida (prazo de relevância da estratégia), Velocidade (time-to-value das ações), Volume (capacidade de execução), Valor (impacto financeiro). Analise nessa ordem.\\n- **4 Pilares**: Estratégia, Operação, Pessoas, Resultados — o plano precisa cobrir os quatro, sinalizando o pilar deficiente.\\n- **FPA (Fatos → Padrões → Ações)**: identifique fatos do cenário, encontre padrões, proponha ações. Nunca pule de fato para ação.\\n- **TOC (Teoria das Restrições)**: encontre o gargalo único que trava o crescimento (oferta, posicionamento, canal, operação) antes de listar melhorias.\\n- **Médico vs Garçom**: entregue diagnóstico e prescrição (médico), nunca apenas o que foi pedido sem questionar (garçom). Se a demanda pedida não resolve o problema real, diga isso educadamente e proponha o caminho certo.\\n\\n## Modos de execução\\n\\n### \`diagnostico\` — Diagnóstico estratégico\\n\\n1. **Coletar contexto**: \`objetivo\`, \`cliente\`, \`contexto\` (nicho, público, oferta, concorrentes, resultados). Se faltar contexto mínimo, pergunte antes de prosseguir.\\n2. **Leitura de mercado**: mapeie a concorrência e onde o cliente se posiciona hoje. Use o que estiver disponível (input, pesquisa de fontes primárias); não invente números de mercado.\\n3. **Encontrar a restrição (TOC)**: qual gargalo único trava o crescimento? (oferta, posicionamento, canal, operação). O diagnóstico precisa apontar isso, não listar 40 problemas.\\n4. **Aplicar os 4 Pilares**: cubra Estratégia, Operação, Pessoas e Resultados, sinalizando o pilar deficiente.\\n\\nEntregável: onde o cliente está no tabuleiro + a restrição que trava + direção geral. Nada de listas genéricas.\\n\\n### \`relatorio\` — Estratégia & plano\\n\\n1. A partir do diagnóstico (ou contexto fornecido), defina o **posicionamento** do cliente: para quem, o que oferece, por que é diferente.\\n2. Defina os **pilares estratégicos** e as **apostas prioritárias** (FPA — Foco no Pouco que dá Aumento): máximo 3-5 apostas que desbloqueiam o resto.\\n3. **Sabatina interna** (stress-test): quais riscos, restrições e premissas frágeis? O que pode quebrar no plano? Ajuste antes de entregar.\\n4. **Próximos passos**: ações com responsável e prazo, prioridade coerente com o impacto.\\n\\nEntregável: documento de estratégia completo — posicionamento, pilares, apostas, riscos, próximos passos.\\n\\n## Saída\\n\\nSempre o contrato JSON único das rotinas P.I.A.:\\n\\n\`\`\`json\\n{\\n  \\"resumo\\": \\"parágrafo executivo de 2-3 frases\\",\\n  \\"tarefas\\": [{\\"tt\\": \\"título da tarefa no Ekyte\\", \\"cl\\": \\"<cliente>\\", \\"pri\\": \\"urgente|alta|media\\"}],\\n  \\"texto\\": \\"documento de estratégia completo em markdown (usado no detalhe da execução)\\"\\n}\\n\`\`\`\\n\\n- \`tarefas\`: somente ações aprovadas por você como essenciais (máx. 5); prioridade coerente com o plano.\\n- Se faltar dado essencial (nicho, oferta, objetivo), não invente: registre a pendência no \`resumo\` e não crie tarefas fantasma.\\n- Seja específico: em vez de \\"melhorar o posicionamento\\", diga \\"reposicionar a oferta para [segmento] destacando [diferencial], e validar com [teste]\\" — a tarefa precisa ser executável sem reunião.\\n\\n---\\n\\nProfissional, direto, em português brasileiro. Coloquial quando apropriado, sem jargão desnecessário. Assuma responsabilidade pelo resultado — apresente recomendações com clareza, nunca opiniões vagas. Você é a Kora Kotler da operação: clareza estratégica a serviço do cliente.";

const userPrompt = 'modo=' + modo + '\\n' + modoPrompt + '\\n\\nRESPONDA UNICAMENTE EM JSON VALIDO com a seguinte estrutura (sem markdown, sem texto fora do JSON):\\n' +
'{\\n  "resumo": "resumo da entrega em markdown",\\n  "tarefas": [\\n    { "titulo": "titulo curto e objetivo", "descricao": "detalhe do que fazer", "prioridade": "alta|media|baixa", "prazo": "YYYY-MM-DD", "dono": "username ou nome da pessoa responsavel" }\\n  ]\\n}\\n' +
'\\nREGRA IMPORTANTE PARA O CAMPO "prazo": converta prazos relativos em datas absolutas YYYY-MM-DD. Hoje eh ' + new Date().toISOString().slice(0, 10) + '. Exemplos: "sexta-feira" e "esta semana" viraram a sexta-feira mais proxima; "proxima semana" virou 7 dias a partir de hoje; "amanha" virou a data de amanha.\\n' +
'\\nATENCAO: preencha os campos com dados REAIS extraidos do input. NAO repita o exemplo da estrutura como resposta. O campo "tarefas" deve conter no minimo 1 tarefa concreta derivada da entrega, quando houver acoes de follow-up. Se nao houver acoes, crie 0 tarefas (tarefas: []).\\n' +
'\\n\\nInput:\\n' + JSON.stringify(inputData, null, 2);

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
        id: 'pia_estrategista_digital_criar_run',
        name: 'Criar Run',
        type: 'n8n-nodes-base.supabase',
        version: 1,
        position: [650, 300],
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
                        '={{ JSON.stringify({ modo: $json.modo, cliente: $json.cliente, executor_id: $json.executor_id, workspace_id: $json.workspace_id, agendado: $json.agendado, schedule_id: $json.schedule_id }) }}',
                },
            ],
        },
    };

    @node({
        id: 'pia_estrategista_digital_llm',
        name: 'Chamar LLM',
        type: 'n8n-nodes-base.httpRequest',
        version: 4.2,
        position: [850, 300],
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
            '={{ JSON.stringify({ model: "nemotron-3.5-lightning-free", messages: [{ role: "system", content: $("Montar Prompt").item.json.system_instruction }, { role: "user", content: $("Montar Prompt").item.json.user_prompt }], max_tokens: 16384, temperature: 0.3 }) }}',
        options: {
            timeout: 120000,
            retryOnFail: true,
            maxTries: 3,
            waitBetweenTries: 3000,
        },
    };

    @node({
        id: 'pia_estrategista_digital_estruturar_saida',
        name: 'Estruturar Saida',
        type: 'n8n-nodes-base.code',
        version: 2,
        position: [1050, 300],
    })
    EstruturarSaida = {
        mode: 'runOnceForAllItems',
        language: 'javaScript',
        jsCode: `const items = $input.all();
const out = [];
const ctx = $('Montar Prompt').item.json || {};
const modo = ctx.modo || 'diagnostico';
const cliente = ctx.cliente || 'Peretto & Co.';

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

  let parsed = { resumo: raw, tarefas: [] };
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
    parsed = { resumo: raw, tarefas: [] };
  }

  const tarefas = Array.isArray(parsed.tarefas) ? parsed.tarefas : [];

  out.push({
    json: {
      run_id: ctx.run_id,
      user_id: ctx.user_id,
      routine_id: ctx.routine_id,
      requires_approval: ctx.requires_approval !== false,
      username: ctx.username || 'marcos',
      user_email: ctx.user_email || '',
      cliente: cliente,
      modo: modo,
      executor_id: ctx.executor_id || '',
      workspace_id: ctx.workspace_id || '',
      agendado: ctx.agendado === true,
      schedule_id: ctx.schedule_id || '',
      sistema: 'rotina',
      tipo: 'rotina',
      resumo: parsed.resumo || raw,
      tarefas: tarefas,
      resposta: raw,
      total_tokens: tokens,
    },
  });
}

return out;`,
    };

    @node({
        id: 'pia_estrategista_digital_atualizar_run',
        name: 'Atualizar Run',
        type: 'n8n-nodes-base.supabase',
        version: 1,
        position: [1250, 300],
        credentials: { supabaseApi: { id: 'NvEBLQBmAMn0Q2dD', name: 'PIA Supabase (Product)' } },
    })
    AtualizarRun = {
        resource: 'row',
        operation: 'update',
        tableId: 'routine_runs',
        dataToSend: 'defineBelow',
        filters: {
            conditions: [
                {
                    keyName: 'id',
                    condition: 'eq',
                    keyValue: '={{ $json.run_id }}',
                },
            ],
        },
        fieldsUi: {
            fieldValues: [
                {
                    fieldId: 'status',
                    fieldValue: '={{ $json.requires_approval ? "awaiting_approval" : "completed" }}',
                },
                {
                    fieldId: 'output_summary',
                    fieldValue:
                        '={{ JSON.stringify({ resumo: $json.resumo, tarefas: $json.tarefas, texto: $json.resposta }) }}',
                },
                {
                    fieldId: 'total_tokens',
                    fieldValue: '={{ $json.total_tokens }}',
                },
                {
                    fieldId: 'updated_at',
                    fieldValue: '={{ new Date().toISOString() }}',
                },
            ],
        },
    };

    @node({
        id: 'pia_estrategista_digital_criar_aprovacao',
        name: 'Criar Aprovacao',
        type: 'n8n-nodes-base.supabase',
        version: 1,
        position: [1250, 520],
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
                    fieldValue: '={{ $json.username }}',
                },
                {
                    fieldId: 'cliente',
                    fieldValue: '={{ $json.cliente }}',
                },
                {
                    fieldId: 'tipo',
                    fieldValue: '={{ "rotina_" + $json.modo }}',
                },
                {
                    fieldId: 'conteudo',
                    fieldValue: '={{ $json.resumo || $json.resposta }}',
                },
                {
                    fieldId: 'status',
                    fieldValue: 'pending',
                },
            ],
        },
    };

    // =====================================================================
    // ROUTAGE ET CONNEXIONS
    // =====================================================================

    @links()
    defineRouting() {
        this.WebhookRotina.out(0).to(this.MontarPrompt.in(0));
        this.MontarPrompt.out(0).to(this.CriarRun.in(0));
        this.CriarRun.out(0).to(this.ChamarLlm.in(0));
        this.ChamarLlm.out(0).to(this.EstruturarSaida.in(0));
        this.EstruturarSaida.out(0).to(this.AtualizarRun.in(0));
        this.EstruturarSaida.out(0).to(this.CriarAprovacao.in(0));
        this.ReceberAprovacao.out(0).to(this.AtualizarRun.in(0));
    }
}
