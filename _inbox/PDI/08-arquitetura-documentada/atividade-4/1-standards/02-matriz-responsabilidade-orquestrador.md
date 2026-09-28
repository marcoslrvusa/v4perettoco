# Matriz de Responsabilidade do Orquestrador V4

| Peca | Dono | Suplente | Responde por | Escala para |
|------|------|----------|--------------|-------------|
| n8n (fluxos, triggers) | Marcos Luciano | A definir | Fluxos, credenciais no cofre, retry de workflow | Lideranca FV |
| Workers Python (coleta) | Marcos Luciano | A definir | Coleta Meta Ads, backoff, fila de erros | Lideranca FV |
| Supabase Postgres | Marcos Luciano | A definir | Tabelas contas, coletas e erros, acessos | Lideranca FV |
| Painel Next.js | A definir | Marcos Luciano | Visao, disparo manual, login | Marcos Luciano |
| Meta Ads API (contas e tokens) | Gestor de trafego | Marcos Luciano | Tokens validos, permissoes de conta | Lideranca FV |
| Gmail API (disparo) | Marcos Luciano | A definir | Templates, limites de envio | Lideranca FV |

## Leitura honesta

Ha concentracao real em uma pessoa (efeito time pequeno) e 2 pecas sem suplente. A roda de ownership em `2-implementacao/03-roda-ownership.md` existe exatamente para distribuir: suplente so vale depois de operar a peca uma vez com o dono ao lado.

## Regra de escala

Dono nao responde em 15 minutos em incidente critico ou alto: escala automatica para o suplente, depois lideranca FV. Sem pedir permissao, sem broadcast no chat geral.
