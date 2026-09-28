# SOLID: Antes vs Depois

## Antes
- **SRP:** run() faz regra + SQL + SMTP + CRM.
- **OCP:** incluir canal WhatsApp exige editar o método central.
- **DIP:** importa psycopg2 e smtplib direto.

## Depois
| Princípio | Onde |
|-----------|------|
| SRP | CampaignService orquestra; Notifier/Repository/Logger fazem o resto |
| OCP | novo canal = nova impl de Notifier |
| LSP | qualquer Notifier substitui outro |
| ISP | interfaces enxutas |
| DIP | serviço recebe abstrações via construtor |

## Por que importa
SQL concatenado quebrava envio em nomes com apóstrofo. Após a refatoração, o acesso
a dados está atrás de uma porta com consulta parametrizada (injection eliminado).
