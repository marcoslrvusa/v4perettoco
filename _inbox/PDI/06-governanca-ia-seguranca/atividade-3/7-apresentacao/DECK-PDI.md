# Deck PDI | A3 Gestao de segredos e rotacao de credenciais

## Slide 1: Tese
Chave de Ads e CRM em chat, planilha e commit e questao de tempo ate o vazamento. Cofre, dono, rotacao e varredura que falha o build resolvem a causa.

## Slide 2: Contexto
Tokens de Meta Ads, Google, CRM, banco e webhooks circulam entre workers, CIs e maquinas do time sem inventario nem prazo de troca.

## Slide 3: Problema
Chave vazada da acesso a verba de midia e base de leads; troca emergencial vira madrugada porque ninguem sabe onde cada segredo esta usado. Chave sem dono e chave eterna.

## Slide 4: Solucao em 5 etapas
Cofre central, entrega por referencia (env var, OIDC, secrets do Actions), rotacao 30/90/180 dias, varredura continua, resposta ensaiada a vazamento.

## Slide 5: Standard entregue
`STANDARD-SEGREDOS-ROTACAO.md`: principios, tabela onde guardar e como entregar, prazos de rotacao, varredura e resposta em 5 passos.

## Slide 6: Codigo entregue
`secrets_audit.py` em Python puro: 5 familias de padroes reais (AWS, GitHub, OpenAI, chave privada, senha em codigo), checagem de `.gitignore`, relatorio e exit code para o CI. Self-test passando.

## Slide 7: Demo
Rodar a auditoria num repo de teste com segredo plantado; mostrar deteccao por tipo e linha; mostrar `gh secret set` criando secret sem expor valor.

## Slide 8: Comandos verificados
`gh secret set NOME`, leitura de arquivo com `< secret.txt`, flag `--env`, `gh secret list`, `gpg --symmetric --cipher-algo AES256` para segredo grande. Todos tirados do GitHub Docs.

## Slide 9: Metricas
Criticas com rotacao: atual 0% para 100% em 90 dias (meta). Segredos em repos: primeira rodada mede, meta zero apos remediacao (meta). Revogar e girar vazada: sem rotina para ate 4 h (meta).

## Slide 10: Tradeoffs assumidos
Cofre central muda o bootstrap dos deploys; dynamic secrets exigem renovacao no codigo; scan que falha o build gera atrito no primeiro mes; um dono por segredo cria fila recorrente.

## Slide 11: Proximos passos
Migrar Ads e CRM para o cofre; ativar rotacao 30/90 dias com dono; bloquear push com segredo e treinar o time.

## Slide 12: Impacto
Vazamento cai de dias de retrabalho e risco de verba desviada para horas de procedimento ensaiado; auditoria encontra processo, nao improviso.
