// n8n — [CC] CRM Observability Logger
export const workflow = {
  name: '[CC] CRM Observability Logger',
  nodes: [
    { id:'trigger', type:'n8n-nodes-base.webhook', params:{ path:'crm-sync-obs' } },
    { id:'enrich', type:'n8n-nodes-base.code', code:`
      const trace = $vars.traceId || crypto.randomUUID();
      const r = $json;
      return { trace_id: trace, entity: r.entity, crm: r.crm, action: r.action,
               record_id: r.id, ts: new Date().toISOString() };` },
    { id:'sendLog', type:'n8n-nodes-base.httpRequest', params:{ url:'https://logs.internal/ingest', method:'POST' } },
    { id:'alert', type:'n8n-nodes-base.if', conditions:[{ left:'={{ $json.error_rate }}', operator:'gt', right:0.02 }] },
    { id:'notify', type:'n8n-nodes-base.slack', params:{ channel:'#ops-crm' } },
  ],
};
