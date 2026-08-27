# Mapa de Dominios (DDD)

## Bounded Contexts
| Contexto | Raiz de Agregado | Filhos |
|----------|-----------------|-------|
| CRM | Lead | Activities, Scores |
| Campaign | Campaign | Segments |
| Agent | Agent | Tasks -> ToolCalls |
| Billing | Invoice | Plan, Usage |

## Linguagem ubíqua
- **Lead**: contato capturado, ainda nao qualificado.
- **Deal**: oportunidade com stage e value.
- **Run**: execucao de um agente com trace_id.

## Integracao
Nunca via tabela compartilhada. Via evento: `LeadCreated` (CRM) -> `CampaignEligibilityCheck`.
