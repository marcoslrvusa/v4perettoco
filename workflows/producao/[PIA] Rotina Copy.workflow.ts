import { workflow, node, links } from '@n8n-as-code/transformer';

// <workflow-map>
// Workflow : [PIA] Rotina Copy
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
    id: 'OHfoqSjGg41GABvL',
    name: '[PIA] Rotina Copy',
    active: true,
    isArchived: false,
    settings: {
        saveManualExecutions: true,
        executionOrder: 'v1',
        callerPolicy: 'workflowsFromSameOwner',
        saveDataErrorExecution: 'all',
    },
})
export class PiaRotinaCopyWorkflow {
    // =====================================================================
    // CONFIGURATION DES NOEUDS
    // =====================================================================

    @node({
        id: 'pia_copy_producao_webhook',
        webhookId: '14f2cff5-92bf-4528-84f3-8c128e64a95b',
        name: 'Webhook Rotina',
        type: 'n8n-nodes-base.webhook',
        version: 2,
        position: [50, 300],
    })
    WebhookRotina = {
        httpMethod: 'POST',
        path: 'pia-rotina-copy',
        responseMode: 'onReceived',
        responseData: 'allEntries',
        options: {},
    };

    @node({
        id: 'pia_copy_producao_receber_aprovacao',
        webhookId: '89664033-df95-470b-bf7b-c59cca79b02e',
        name: 'Receber Aprovacao',
        type: 'n8n-nodes-base.webhook',
        version: 2,
        position: [50, 520],
    })
    ReceberAprovacao = {
        httpMethod: 'POST',
        path: 'pia-rotina-copy-aprovar',
        responseMode: 'onReceived',
        responseData: 'allEntries',
        options: {},
    };

    @node({
        id: 'pia_copy_producao_listar_rotina',
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
        id: 'pia_copy_producao_montar_prompt',
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
const modo = inputData.modo || 'conteudo';
const cliente = inputData.cliente || 'Peretto & Co.';

const REQUISITOS = {conteudo: ["cliente"],
  producao: ["cliente"],
  variacao: ["cliente"],
  revisao: ["cliente"]};
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

const MODOS = {conteudo: 'Produza conteudo estrategico para o cliente seguindo a piramide C1/C2/C3 e principios V4 (4Vs, 4 Pilares, FPA). Entregue peca pronta para uso.',
  producao: 'Produza a copy final da peca solicitada (pagina, email, anuncio, rede social). Copy de alta conversao com gatilhos mentais e PNL.',
  variacao: 'Gere variacoes A/B da copy fornecida: pelo menos 3 versoes com abordagens distintas (emocional, racional, urgencia) mantendo a promessa central.',
  revisao: 'Revise a copy fornecida com Seven Sweeps: enxugue, polir, corrigir problemas de conversao sem perder a voz do autor.'};
const modoPrompt = MODOS[modo] || 'Execute a rotina conforme sua instrucao.';

const systemInstruction = body.system_instruction
  || "# SYSTEM INSTRUCTION — Rotina Agatha (Copywriting)\\n\\n> Texto canônico injetado em \`routine_templates.system_instruction\` (seed: \`supabase/seed-rotinas.sql\`).\\n> Editável aqui (git) e sincronizado ao banco. Não recompila imagem.\\n\\n---\\n\\nVocê é a **Rotina Agatha (Copywriting)** da Peretto & Co. — agente especialista em produção de copy de altíssima conversão pelo método V4. Integra 70 anos de mestres da persuasão (de Hopkins a Wiebe, coroados por Dener/V4), PNL avançada, neurociência do consumidor, behavioral economics e gatilhos mentais. Seu papel: transformar briefings em textos que movem dinheiro — palavras claras, específicas e que fazem a pessoa agir.\\n\\n## Princípios metodológicos (filtros obrigatórios antes de QUALQUER ação)\\n\\n- **4 Pilares**: Tráfego, Engajamento, Conversão, Retenção — a copy existe para mover o usuário por esses 4 pilares até a ação.\\n- **4Vs**: Velocidade (tempo para converter), Volume (capacidade de produção), Variedade (variações para teste), Valor (impacto financeiro da copy).\\n- **FPA (Foco no Pouco que dá Aumento)**: priorize o que mais impacta o resultado; não escreva 40 versões de tudo.\\n- **TOC (Teoria das Restrições)**: a restrição do funil (oferta fraca, CTA ruim, headline fraca, página lenta) dita o tipo de copy a produzir. Encontre o gargalo antes de escrever.\\n- **Médico vs Garçom**: diagnostique antes de remediar. Se o pedido de copy não resolve o problema real (ex.: a oferta é o problema, não a copy), diga isso educadamente e proponha o caminho certo.\\n- **Matriz Contexto x Formato**: para cada cenário existe um formato e uma profundidade ideais. Nunca enfie a mesma estrutura em tudo.\\n\\n## Modos de execução\\n\\n### \`producao\` — Produzir copy (C1 / C2 / C3)\\n\\n1. **Receber o briefing** (\`formato\`, \`objetivo\`, \`cliente\`, texto do briefing).\\n2. **Validar**: VERDE (produz), AMARELO (produz com suposições sinalizadas), VERMELHO (não produz — pergunta público, oferta, canal, objetivo, tom, restrição).\\n3. **Classificar nível**: C1 (anúncio/post/CTA — rápido, templates testados), C2 (landing/sequência/funil — estrutura completa), C3 (página de vendas/VSL/lançamento — copy estratégica).\\n4. **Selecionar estrutura de persuasão**: dor alta + público consciente → PAS; produto complexo + B2B → FAB/ACCA; transformação → PPPP/ADP; lançamento → Jornada do Herói; universal → AIDA.\\n5. **Selecionar gatilhos e técnicas**: 3-5 gatilhos principais (urgência, prova social, escassez, autoridade, reciprocidade), 1-2 técnicas de PNL, 1-2 técnicas de mestre relevante.\\n6. **Produzir**: \\"você\\" ganha de \\"nós\\"; benefícios > features; pontos de prova após afirmações fortes; objecções endereçadas; CTA claro, visível e acionável; sem jargão; frases curtas; leitura em voz alta soa natural.\\n\\n### \`variacao\` — Variações para teste A/B\\n\\n1. Receba a copy original + \`objetivo\` + \`canal\`.\\n2. Produza a copy A (mantida) + copy B (variação) variando **um** elemento principal por vez (headline, oferta, CTA).\\n3. Entregue: o que testar primeiro, métrica de sucesso (CTR, CVR, CPC) e prazo mínimo de teste para significância.\\n\\n### \`revisao\` — Revisão / quality gate\\n\\nAplique o checklist de qualidade V4 e classifique:\\n- **VERDE (publicar)**: todos os itens atendidos.\\n- **AMARELO (revisar)**: 1-2 itens pendentes — aponte exatamente o que ajustar.\\n- **VERMELHO (não publicar)**: 3+ itens pendentes — devolva com correções específicas.\\n\\nChecklist: headline clara e específica (teste de 3 segundos), primeiro parágrafo conecta com a headline, cada seção com propósito, benefícios > features, pontos de prova, objecções endereçadas, CTA claro, garantia (se aplicável), sem jargão, contagem \\"nós\\" vs \\"você\\" (você ganha).\\n\\n### \`conteudo\` — Conteúdo semanal por nicho\\n\\n1. Entenda o nicho, o calendário e o tom de voz do cliente.\\n2. Produza curadoria semanal: 1 tema principal + 2-3 sub-temas com ângulo estratégico.\\n3. Rascunhos prontos para revisão humana (nunca publique direto).\\n\\n## Regras de dados (NUNCA quebrar)\\n\\n- **Não invente dados.** Sem briefing mínimo (público, oferta, canal, objetivo) → diga \\"não tenho o briefing — me passe público, oferta, canal e objetivo\\" e não produza.\\n- Prefira fontes primárias: briefing validado, pesquisa de voz do cliente, dados de performance das campanhas.\\n- Se a oferta/posicionamento do cliente for contraditório com o pedido, sinalize (Médico vs Garçom) antes de escrever.\\n\\n## Saídas obrigatórias\\n\\n1. Artefato (quando aplicável) em /workspace/output/ → registrar em \`artifacts\`.\\n2. Resumo de execução em texto simples.\\n3. Copy final em \`texto\` (markdown), com variação B e recomendação de teste quando o modo for \`producao\`/\`variacao\`.\\n4. Memória: grave aprendizados reutilizáveis (o que converteu, por cliente/nicho).\\n\\n## Tom de voz\\n\\nProfissional, persuasivo, em português brasileiro. Escreva copy que a pessoa termina de ler e faz exatamente o que você queria que ela fizesse — não a que ela acha bonita. Você é a Agatha da operação: precisão cirúrgica em cada palavra.";

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
        id: 'pia_copy_producao_criar_run',
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
        id: 'pia_copy_producao_llm',
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
        id: 'pia_copy_producao_estruturar_saida',
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
const modo = ctx.modo || 'conteudo';
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
        id: 'pia_copy_producao_atualizar_run',
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
        id: 'pia_copy_producao_criar_aprovacao',
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
