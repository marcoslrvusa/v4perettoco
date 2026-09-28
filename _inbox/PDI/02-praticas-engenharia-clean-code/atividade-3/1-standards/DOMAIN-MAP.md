# Mapa de Domínios (DDD)

## Bounded Contexts
| Contexto | Raiz de Agregado | Filhos |
|----------|-----------------|-------|
| CRM | Lead | Activities, Scores |
| Campaign | Campaign | Segments |
| Agent | Agent | Tasks -> ToolCalls |
| Billing | Invoice | Plan, Usage |

## Linguagem ubíqua
- **Lead**: contato capturado, ainda não qualificado.
- **Deal**: oportunidade com stage e value.
- **Run**: execução de um agente com trace_id.

## Integração
Nunca via tabela compartilhada. Via evento: `LeadCreated` (CRM) -> `CampaignEligibilityCheck`.
