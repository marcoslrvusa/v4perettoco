# Matriz de Responsabilidade do Orquestrador V4

| Peça | Dono | Suplente | Responde por | Escala para |
|------|------|----------|--------------|-------------|
| n8n (fluxos, triggers) | Marcos Luciano | A definir | Fluxos, credenciais no cofre, retry de workflow | Liderança FV |
| Workers Python (coleta) | Marcos Luciano | A definir | Coleta Meta Ads, backoff, fila de erros | Liderança FV |
| Supabase Postgres | Marcos Luciano | A definir | Tabelas contas, coletas e erros, acessos | Liderança FV |
| Painel Next.js | A definir | Marcos Luciano | Visão, disparo manual, login | Marcos Luciano |
| Meta Ads API (contas e tokens) | Gestor de tráfego | Marcos Luciano | Tokens válidos, permissões de conta | Liderança FV |
| Gmail API (disparo) | Marcos Luciano | A definir | Templates, limites de envio | Liderança FV |

## Leitura honesta

Há concentração real em uma pessoa (efeito time pequeno) e 2 peças sem suplente. A roda de ownership em `2-implementacao/03-roda-ownership.md` existe exatamente para distribuir: suplente só vale depois de operar a peça uma vez com o dono ao lado.

## Regra de escala

Dono não responde em 15 minutos em incidente crítico ou alto: escala automática para o suplente, depois liderança FV. Sem pedir permissão, sem broadcast no chat geral.
