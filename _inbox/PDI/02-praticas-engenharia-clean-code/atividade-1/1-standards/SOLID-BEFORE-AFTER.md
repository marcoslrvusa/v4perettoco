# SOLID — Antes vs Depois

## Antes
- **SRP:** run() faz regra + SQL + SMTP + CRM.
- **OCP:** incluir canal WhatsApp exige editar o metodo central.
- **DIP:** importa psycopg2 e smtplib direto.

## Depois
| Principio | Onde |
|-----------|------|
| SRP | CampaignService orquestra; Notifier/Repository/Logger fazem o resto |
| OCP | novo canal = nova impl de Notifier |
| LSP | qualquer Notifier substitui outro |
| ISP | interfaces enxutas |
| DIP | servico recebe abstracoes via construtor |

## Por que importa
SQL concatenado quebrava envio em nomes com apostrofo. Apos a refatoracao, o acesso
a dados esta atras de uma porta com consulta parametrizada (injection eliminado).
