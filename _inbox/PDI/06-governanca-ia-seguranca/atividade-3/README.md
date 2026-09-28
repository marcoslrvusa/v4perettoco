# A3 | Gestao de segredos e rotacao de credenciais

| Campo | Valor |
|-------|-------|
| Area | Automacao & Infraestrutura |
| Unidade | FV Marketing / V4 Company |
| Autor | Marcos Luciano |
| Data | Setembro 2026 |
| Status | Entregue (desenvolvido, homologacao pendente) |

## Entregas desta PDI

```
atividade-3/
├── README.md
├── 1-standards/
│   └── STANDARD-SEGREDOS-ROTACAO.md
├── 2-implementacao/
│   ├── secrets_audit.py
│   └── CHECKLIST-SEGREDOS.md
└── 7-apresentacao/
    ├── DECK-PDI.md
    ├── DEMO-SCRIPT.md
    ├── ROTEIRO-DOMINIO.md
    ├── pdi-governanca-ia-seguranca-a3.html
    ├── pdi-governanca-ia-seguranca-a3.docx
    ├── pdi-governanca-ia-seguranca-a3.pdf
    └── gerar-docx.py
```

## Problema Resolvido

Tokens de API (Meta Ads, Google, CRM), chaves de banco e segredos de webhook vivem em `.env` copiado no chat, planilha compartilhada ou commitado por acidente, sem dono e sem rotacao. Um vazamento desses da acesso a verba de midia, base de leads e historico de campanhas, e a troca emergencial vira madrugada porque ninguem sabe onde cada chave esta usada.

## Arquitetura Resumida

```
[segredo nasce no provider]
  -> 1. cofre (Vault KV ou gerenciador do provider, nunca repo)
  -> 2. entrega por referencia (env var, OIDC, gh secret set)
  -> 3. rotacao agenda (30 dias critico, 90 dias padrao)
  -> 4. varredura continua (secrets_audit.py + bloqueio de push)
  -> 5. resposta a vazamento (revogar, girar, auditar uso)
```

O `secrets_audit.py` implementa a etapa 4 localmente (regex de padroes reais, checagem de `.gitignore`, relatorio) e o standard amarra cofre, rotacao e resposta.

## Proximos Passos

1. Migrar os segredos criticos de Ads e CRM para o cofre e referenciar por variavel de ambiente.
2. Ativar rotacao de 30 dias nas chaves criticas e 90 dias nas demais, com dono nomeado.
3. Bloquear push com segredo (hook ou CI com varredura) e treinar o time no fluxo novo.

## Metricas de Sucesso

| Metrica | Atual | Meta |
|---------|-------|------|
| Credenciais criticas com rotacao automatica ou agendada | 0% (baseline desta PDI) | 100% em 90 dias (meta) |
| Segredos detectados em repos por varredura | a medir na primeira rodada | 0 apos remediacao (meta) |
| Tempo medio para revogar e girar chave vazada | sem rotina | ate 4 h (meta) |

## Decisoes e tradeoffs

1. Cofre central em vez de `.env` por projeto: elimina a dispersao e da auditoria unica; exige que todo deploy leia segredo por referencia, o que muda o bootstrap dos workers.
2. Segredos dinamicos de curta duracao onde der: credencial que expira em minutos reduz a janela de abuso a quase zero; nem todo provider suporta, e o codigo precisa tratar renovacao.
3. OIDC do CI para cloud em vez de chave estatica: GitHub Actions assume papel sem guardar segredo de longa duracao; configuracao inicial maior, operacao posterior menor.
4. Varredura que falha o build ao achar segredo: impede o vazamento na origem, mas gera atrito no primeiro mes ate o time limpar historico e ajustar padroes.
5. Um dono por segredo com prazo de rotacao: acaba com "chave de ninguem"; cria fila de trabalho recorrente que precisa entrar no planejamento.

## Impacto no negocio

Segredo com dono, cofre e rotacao tira a operacao de midia e CRM do modo "uma chave vazada para o desastre": o custo de um vazamento cai de dias de retrabalho e risco de verba desviada para horas de procedimento ensaiado, e auditoria ou due diligence passa a encontrar processo em vez de improviso.

## Referencias

- Curso: Trilha de tutoriais oficiais do HashiCorp Vault, do basico a dynamic secrets (HashiCorp Developer). https://developer.hashicorp.com/vault/tutorials
- Video: How to get dynamic with secrets management (HashiCorp, YouTube). https://www.youtube.com/watch?v=aErDyZvQjWg
- Doc oficial: Vault product documentation. https://developer.hashicorp.com/vault/docs
- Doc oficial: Using secrets in GitHub Actions (GitHub Docs). https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions
