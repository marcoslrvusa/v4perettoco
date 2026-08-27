import { workflow, node, links } from '@n8n-as-code/transformer';

// <workflow-map>
// Workflow : [CC] MT Queue Worker
// Nodes   : 7  |  Connections: 7
//
// NODE INDEX
// ──────────────────────────────────────────────────────────────────────────
// Property name                      Node type (short)          Flags
// ScheduleTrigger                    scheduleTrigger
// QueryDueJobs                        supabase                   [creds]
// CheckSlots                          supabase                   [creds]
// CapacityAvailable                   if
// MarkRunning                          supabase                   [creds]
// ExecuteHeavyProcessor                executeWorkflow
// UpdateJobOutcome                     supabase                   [creds]
//
// ROUTING MAP
// ──────────────────────────────────────────────────────────────────────────
// ScheduleTrigger
//   → QueryDueJobs
//     → CheckSlots
//       → UseAvailable → MarkRunning → ExecuteHeavyJob
//                                 ├── true  → UpdateJobOutcome (done)
//                                 └── false → UpdateJobOutcome (queued retry)
// </workflow-map>

// =====================================================================
// [CC] MT - Queue Worker
// =====================================================================
// Le jobs due (mt_jobs status=queued e retry_at <= agora), verifica
// slot de concorrencia (mt_concurrency), marca como running e delega
// o processamento pesado ao sub-workflow [CC] MT - Heavy Payload
// Processor. Sucesso → done; falha → re-enfileira com backoff.
//
// CONFIGURE:
//  1. Setar credencial Command Center Supabase nos 4 nos supabase.
//  2. Configurar trigger ScheduleTrigger (default: a cada 15s).
//  3. Trocar o ID do workflow alvo do ExecuteWorkflow pelo ID real
//     do [CC] MT - Heavy Payload Processor apos criar.
//  4. Pipeline de producao: ativar este workflow (ou deixar manual).
// =====================================================================

@workflow({
    id: 'mt-queue-worker',
    name: '[CC] MT - Queue Worker',
    active: false,
    isArchived: false,
    settings: { timezone: 'America/Sao_Paulo', saveDataErrorExecution: 'all', executionOrder: 'v1' },
})
export class MtQueueWorkerWorkflow {
    // =====================================================================
    // TRIGGER
    // =====================================================================

    @node({
        name: 'Schedule Trigger',
        type: 'n8n-nodes-base.scheduleTrigger',
        version: 1,
        position: [250, 300],
    })
    ScheduleTrigger = {
        rule: {
            interval: [
                {
                    field: 'seconds',
                    secondsInterval: 15,
                },
            ],
        },
    };

    // =====================================================================
    // QUERY DEBTS
    // =====================================================================

    @node({
        name: 'Query Due Jobs',
        type: 'n8n-nodes-base.supabase',
        version: 1,
        position: [500, 300],
        credentials: { supabaseApi: { id: 'nRJEEi2QwVVKIAHY', name: 'Command Center Supabase' } },
    })
    QueryDueJobs = {
        resource: 'row',
        operation: 'getAll',
        tableId: 'mt_jobs',
        returnAll: true,
        filterType: 'manual',
        matchType: 'allFilters',
        filters: {
            conditions: [
                {
                    keyName: 'status',
                    condition: 'eq',
                    keyValue: 'queued',
                },
            ],
        },
        orderBy: 'priority.desc',
    };

    // =====================================================================
    // CONCURRENCY — LIMITE DE SLOTS
    // =====================================================================

    @node({
        name: 'Check Slots',
        type: 'n8n-nodes-base.supabase',
        version: 1,
        position: [750, 300],
        credentials: { supabaseApi: { id: 'nRJEEi2QwVVKIAHY', name: 'Command Center Supabase' } },
    })
    CheckSlots = {
        resource: 'row',
        operation: 'getAll',
        tableId: 'mt_concurrency',
        returnAll: true,
        filterType: 'manual',
        matchType: 'allFilters',
        filters: {
            conditions: [
                {
                    keyName: 'max_concurrency',
                    condition: 'gt',
                    keyValue: '0',
                },
            ],
        },
    };

    @node({
        name: 'Slots Available',
        type: 'n8n-nodes-base.if',
        version: 2.3,
        position: [1000, 300],
    })
    SlotsAvailable = {
        conditions: {
            conditions: [
                {
                    id: 'slot-check',
                    leftValue: '={{ $json.length }}',
                    rightValue: '0',
                    operator: {
                        type: 'number',
                        operation: 'gt',
                    },
                },
            ],
            combinator: 'and',
            options: {
                caseSensitive: true,
                typeValidation: 'strict',
            },
        },
        options: [],
    };

    // =====================================================================
    // PROCESSAMENTO
    // =====================================================================

    @node({
        name: 'Reserve Slot',
        type: 'n8n-nodes-base.supabase',
        version: 1,
        position: [1250, 120],
        credentials: { supabaseApi: { id: 'nRJEEi2QwVVKIAHY', name: 'Command Center Supabase' } },
    })
    ReserveSlot = {
        resource: 'row',
        operation: 'update',
        tableId: 'mt_concurrency',
        filterType: 'manual',
        matchType: 'allFilters',
        filters: {
            conditions: [
                {
                    keyName: 'queue',
                    condition: 'eq',
                    keyValue: '={{ $json.queue }}',
                },
            ],
        },
        dataToSend: 'defineBelow',
        fieldsUi: {
            fieldValues: [
                { fieldId: 'active_slots', fieldValue: '={{ $json.active_slots + 1 }}' },
            ],
        },
    };

    @node({
        name: 'Update Job Running',
        type: 'n8n-nodes-base.supabase',
        version: 1,
        position: [1500, 120],
        credentials: { supabaseApi: { id: 'nRJEEi2QwVVKIAHY', name: 'Command Center Supabase' } },
    })
    UpdateJobRunning = {
        resource: 'row',
        operation: 'update',
        tableId: 'mt_jobs',
        filterType: 'manual',
        matchType: 'allFilters',
        filters: {
            conditions: [
                {
                    keyName: 'id',
                    condition: 'eq',
                    keyValue: '={{ $json.id }}',
                },
            ],
        },
        dataToSend: 'defineBelow',
        fieldsUi: {
            fieldValues: [
                { fieldId: 'status', fieldValue: 'running' },
                { fieldId: 'picked_at', fieldValue: '={{ new Date().toISOString() }}' },
                { fieldId: 'heartbeat_at', fieldValue: '={{ new Date().toISOString() }}' },
            ],
        },
    };

    @node({
        name: 'Execute Heavy Payload Processor',
        type: 'n8n-nodes-base.executeWorkflow',
        version: 1.3,
        position: [1750, 120],
    })
    ExecuteHeavyPayload = {
        operation: 'call_workflow',
        source: 'database',
        workflowId: 'MT_HEAVY_PAYLOAD_PROCESSOR_ID',
        mode: 'each',
        options: {},
    };

    @node({
        name: 'Complete Job',
        type: 'n8n-nodes-base.if',
        version: 2.3,
        position: [2000, 120],
    })
    CompleteJob = {
        conditions: {
            conditions: [
                {
                    id: 'success-check',
                    leftValue: '={{ $json.success }}',
                    rightValue: 'true',
                    operator: {
                        type: 'boolean',
                        operation: 'true',
                    },
                },
            ],
            combinator: 'and',
            options: { caseSensitive: true, typeValidation: 'strict' },
        },
        options: [],
    };

    @node({
        name: 'Mark Done',
        type: 'n8n-nodes-base.supabase',
        version: 1,
        position: [2250, 0],
        credentials: { supabaseApi: { id: 'nRJEEi2QwVVKIAHY', name: 'Command Center Supabase' } },
    })
    MarkDone = {
        resource: 'row',
        operation: 'update',
        tableId: 'mt_jobs',
        filterType: 'manual',
        matchType: 'allFilters',
        filters: {
            conditions: [
                {
                    keyName: 'id',
                    condition: 'eq',
                    keyValue: '={{ $json.id }}',
                },
            ],
        },
        dataToSend: 'defineBelow',
        fieldsUi: {
            fieldValues: [
                { fieldId: 'status', fieldValue: 'done' },
                { fieldId: 'finished_at', fieldValue: '={{ new Date().toISOString() }}' },
            ],
        },
    };

    @node({
        name: 'Schedule Retry',
        type: 'n8n-nodes-base.supabase',
        version: 1,
        position: [2250, 400],
        credentials: { supabaseApi: { id: 'nRJEEi2QwVVKIAHY', name: 'Command Center Supabase' } },
    })
    ScheduleRetry = {
        resource: 'row',
        operation: 'update',
        tableId: 'mt_jobs',
        filterType: 'manual',
        matchType: 'allFilters',
        filters: {
            conditions: [
                {
                    keyName: 'id',
                    condition: 'eq',
                    keyValue: '={{ $json.id }}',
                },
            ],
        },
        dataToSend: 'defineBelow',
        fieldsUi: {
            fieldValues: [
                { fieldId: 'status', fieldValue: 'queued' },
                { fieldId: 'retry_at', fieldValue: '={{ new Date(Date.now() + 60000 * ($json.attempts + 1)).toISOString() }}' },
                { fieldId: 'attempts', fieldValue: '={{ ($json.attempts || 0) + 1 }}' },
            ],
        },
    };

    // =====================================================================
    // ROUTING
    // =====================================================================

    @links()
    defineRouting() {
        this.ScheduleTrigger.out(0).to(this.QueryDueJobs.in(0));
        this.QueryDueJobs.out(0).to(this.CheckSlots.in(0));
        this.CheckSlots.out(0).to(this.SlotsAvailable.in(0));

        this.SlotsAvailable.out(0).to(this.ReserveSlot.in(0));
        this.ReserveSlot.out(0).to(this.UpdateJobRunning.in(0));
        this.UpdateJobRunning.out(0).to(this.ExecuteHeavyPayload.in(0));

        this.ExecuteHeavyPayload.out('success').to(this.CompleteJob.in(0));
        this.CompleteJob.out(0).to(this.MarkDone.in(0));
        this.CompleteJob.out(1).to(this.ScheduleRetry.in(0));
    }
}