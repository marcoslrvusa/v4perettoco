---
description: Carrega contexto de uma sessão anterior salva em log/
---

Primeiro, liste as sessões disponíveis em `log/`:

!`ls -1t /home/marcos/Desktop/v4perettoco-main-final/v4perettoco-main/log/*.json 2>/dev/null | head -20`

O usuário vai escolher uma sessão pelo nome do arquivo (ou número). Carregue o arquivo escolhido, extraia o resumo das mensagens e apresente o contexto relevante para a sessão atual.

Se o usuário pedir para carregar uma sessão específica que não está em `log/`, tente exportá-la primeiro com `/session-save` e depois carregue.
