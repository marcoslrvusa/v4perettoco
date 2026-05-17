---
description: Lista todas as sessões salvas na pasta log/
---

Liste as sessões salvas anteriormente na pasta `log/`:

!`ls -lh /home/marcos/Desktop/v4perettoco-main-final/v4perettoco-main/log/*.json 2>/dev/null | awk '{print $5, $6, $7, $8, $9}'`

Liste também as sessões ativas do OpenCode:

!`opencode session list --format table 2>/dev/null`

Apresente um resumo organizado das sessões disponíveis, com data, título e tamanho. Pergunte ao usuário se ele quer carregar alguma.
