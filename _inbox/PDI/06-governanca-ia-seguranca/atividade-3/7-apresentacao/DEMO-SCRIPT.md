# Demo Script | A3 Segredos e rotacao

Duracao: 10 min. Pre-requisito: `python3` e `gh` (GitHub CLI) instalados; `secrets_audit.py` na pasta `2-implementacao/`.

1. Abra com a tese (30s): chave em chat e commit e incidente futuro; mostre as 5 etapas do README.
2. Rode o self-test: `python3 ../2-implementacao/secrets_audit.py`. Destaque deteccao de AKIA e ghp e `.gitignore` validado.
3. Rode contra um repo real: `python3 ../2-implementacao/secrets_audit.py <repo>` e leia o relatorio (tipo, arquivo, linha).
4. Mostre o exit code: limpo retorna 0 (CI passa), com achado retorna 1 (CI falha). Fale de ligar no pipeline.
5. Crie um secret sem expor valor: `gh secret set NOME_DO_SECRET` e digite quando pedir; liste com `gh secret list`.
6. Mostre o padrao de segredo grande: `gpg --symmetric --cipher-algo AES256 arquivo.json` e senha como secret.
7. Mostre o standard: prazos 30/90/180 dias e resposta a vazamento em 5 passos.
8. Feche com metricas: 0% para 100% das criticas com rotacao em 90 dias (meta), zero segredos em repos apos remediacao (meta), giro de vazada em ate 4 h (meta).
9. Pergunta de reserva: "e o historico do git com segredo antigo?" Resposta: revogar e girar primeiro, depois expurgar com `git filter-repo` ou BFG e avisar o time, pois hash antigo circula em clone.
