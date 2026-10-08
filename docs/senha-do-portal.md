# Senha do portal: o que a barreira segura e o que não segura

Data: outubro de 2026. Escopo: home (`index.html`), apresentação didática,
proposta, escopo do report, referência do produto e relatório de produtização.

## O que foi feito

Barreira por senha única em `gate.js`, incluído no `<head>` dessas páginas,
com regra `html.gated body{visibility:hidden}` e meta `noindex, nofollow`.
Conteúdo só aparece após a senha. Sessão válida por aba (sessionStorage).

## O que a barreira segura

Visitante casual ou curioso sem a senha: vê só a tela de acesso, não lê o
conteúdo e o Google não indexa as páginas.

## O que a barreira NÃO segura (limites honestos)

1. Os arquivos continuam públicos no GitHub Pages. Quem inspeciona o
   tráfego, desliga o JS ou baixa a URL direta passa pela barreira.
2. A senha é validada no navegador por hash SHA-256 sem sal. Ofusca, não
   blinda: ataque offline de força bruta é possível, por isso a senha precisa
   ser forte e rotacionada.
3. O histórico do git guarda versões antigas sem senha. Reescrever histórico
   publicado não apaga cópias já feitas.
4. Só as páginas listadas acima têm a barreira. Qualquer página nova precisa
   incluir `gate.js`, a regra de ocultação e o `noindex`.

## Operação

Troca de senha: gerar senha forte, calcular o SHA-256 e substituir
`PORTAL_HASH` em `gate.js`. Entregar a nova senha pelo canal já combinado
com o comercial. Nunca commitar a senha em texto claro.

Se o requisito virar sigilo de verdade (preços, dados de cliente), o caminho
é tirar os arquivos da URL pública e servir pela infra autenticada existente.
