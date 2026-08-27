# SOLID — Antes vs Depois

## ANTES (violações)
- **SRP:** `CampaignService` cuidava de regra, DB, e-mail e CRM.
- **OCP:** mudar canal de envio exigia editar o método central.
- **DIP:** camada de aplicação dependia diretamente de `psycopg2`.

## DEPOIS (aplicado)
- **SRP:** `CampaignService` (app) orquestra; `SendCampaign` port; `EmailSender`, `CrmSync` adapters.
- **OCP:** novo canal = nova implementação de `NotificationPort`, sem tocar no service.
- **LSP:** qualquer `NotificationPort` substituto funciona.
- **ISP:** interfaces enxutas (`Repository`, `Notifier`, `Logger`).
- **DIP:** serviço depende de abstrações, não de infraestrutura concreta.
