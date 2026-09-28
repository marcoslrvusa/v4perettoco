# STANDARD-SEGREDOS-ROTACAO | Cofre, entrega e rotacao de credenciais

Versao 1.0, Setembro 2026. Escopo: API keys, tokens, senhas de servico, chaves de banco, segredos de webhook e certificados usados pela operacao.

## 1. Principios

1. Segredo mora no cofre, nunca no repo, wiki, chat ou planilha. Codigo referencia por nome de variavel de ambiente.
2. Todo segredo tem dono nomeado, criticidade (critica, alta, padrao) e prazo de rotacao.
3. Acesso pelo menor privilegio e com trilha: quem leu, quando, de onde.
4. Vazou, gira: credencial exposta e revogada e substituida em ate 4 h (critica).

## 2. Onde guardar e como entregar

| Cenario | Padrao |
|---------|--------|
| Producao e staging | Cofre central (Vault KV ou gerenciado do provider); app le por referencia |
| CI (GitHub Actions) | Secrets de repositorio/ambiente/organizacao (`gh secret set NOME`), nunca em log; preferir OIDC para cloud em vez de chave estatica |
| Desenvolvimento local | `.env` fora do git (listado no `.gitignore`), gerado a partir de `.env.example` sem valores reais |
| Segredo grande (acima de 48 KB no GitHub) | Arquivo cifrado com `gpg --symmetric --cipher-algo AES256` no repo e senha como secret (padrao documentado pelo GitHub) |

Comandos verificados (GitHub Docs): `gh secret set SECRET_NAME`, `gh secret set SECRET_NAME < secret.txt`, `gh secret set --env ENV_NAME SECRET_NAME`, `gh secret list`.

## 3. Rotacao

Critica (verba de midia, CRM, banco prod): 30 dias, automatica onde houver dynamic secret; alta: 90 dias; padrao: 180 dias com lembrete. Rotacao cobre gerar, distribuir, validar e revogar a anterior, com janela de sobreposicao curta. Dynamic secrets (credencial sob demanda com TTL) sao o alvo onde o provider suporta.

## 4. Varredura continua

`secrets_audit.py` roda no CI e falha o build ao achar padrao de segredo em codigo. Complementos: `.gitignore` com `.env`, `*.pem`, `*.key`, `secret.txt`; revisao de PR atenta a diff com valor literal; resposta padrao a deteccao: revogar, girar, auditar uso no periodo de exposicao, registrar na trilha (atividade 4).

## 5. Resposta a vazamento (ordem)

1. Revogar a credencial no provider. 2. Girar e redistribuir pelos canais oficiais. 3. Auditar uso no periodo exposto (logs, extrato de Ads). 4. Avaliar comunicacao (cliente, ANPD se houver dado pessoal, art. 48). 5. Post-mortem com causa raiz e acao preventiva.
