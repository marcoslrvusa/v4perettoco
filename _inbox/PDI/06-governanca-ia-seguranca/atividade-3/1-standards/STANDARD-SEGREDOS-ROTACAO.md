# STANDARD-SEGREDOS-ROTACAO | Cofre, entrega e rotação de credenciais

Versão 1.0, Setembro 2026. Escopo: API keys, tokens, senhas de serviço, chaves de banco, segredos de webhook e certificados usados pela operação.

## 1. Princípios

1. Segredo mora no cofre, nunca no repo, wiki, chat ou planilha. Código referencia por nome de variável de ambiente.
2. Todo segredo tem dono nomeado, criticidade (crítica, alta, padrão) e prazo de rotação.
3. Acesso pelo menor privilegio e com trilha: quem leu, quando, de onde.
4. Vazou, gira: credencial exposta e revogada e substituída em até 4 h (crítica).

## 2. Onde guardar e como entregar

| Cenário | Padrão |
|---------|--------|
| Produção e staging | Cofre central (Vault KV ou gerenciado do provider); app lê por referência |
| CI (GitHub Actions) | Secrets de repositorio/ambiente/organizacao (`gh secret set NOME`), nunca em log; preferir OIDC para cloud em vez de chave estática |
| Desenvolvimento local | `.env` fora do git (listado no `.gitignore`), gerado a partir de `.env.example` sem valores reais |
| Segredo grande (acima de 48 KB no GitHub) | Arquivo cifrado com `gpg --symmetric --cipher-algo AES256` no repo e senha como secret (padrão documentado pelo GitHub) |

Comandos verificados (GitHub Docs): `gh secret set SECRET_NAME`, `gh secret set SECRET_NAME < secret.txt`, `gh secret set --env ENV_NAME SECRET_NAME`, `gh secret list`.

## 3. Rotação

Crítica (verba de mídia, CRM, banco prod): 30 dias, automática onde houver dynamic secret; alta: 90 dias; padrão: 180 dias com lembrete. Rotação cobre gerar, distribuir, validar e revogar a anterior, com janela de sobreposição curta. Dynamic secrets (credencial sob demanda com TTL) são o alvo onde o provider suporta.

## 4. Varredura continua

`secrets_audit.py` roda no CI e falha o build ao achar padrão de segredo em código. Complementos: `.gitignore` com `.env`, `*.pem`, `*.key`, `secret.txt`; revisão de PR atenta a diff com valor literal; resposta padrão a detecção: revogar, girar, auditar uso no período de exposição, registrar na trilha (atividade 4).

## 5. Resposta a vazamento (ordem)

1. Revogar a credencial no provider. 2. Girar e redistribuir pelos canais oficiais. 3. Auditar uso no período exposto (logs, extrato de Ads). 4. Avaliar comunicação (cliente, ANPD se houver dado pessoal, art. 48). 5. Post-mortem com causa raiz e ação preventiva.
