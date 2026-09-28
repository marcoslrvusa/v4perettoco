# A3 | Gestão de segredos e rotação de credenciais

| Campo | Valor |
|-------|-------|
| Área | Automação & Infraestrutura |
| Unidade | FV Marketing / V4 Company |
| Autor | Marcos Luciano |
| Data | Setembro 2026 |
| Status | Entregue (desenvolvido, homologação pendente) |

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

Tokens de API (Meta Ads, Google, CRM), chaves de banco e segredos de webhook vivem em `.env` copiado no chat, planilha compartilhada ou commitado por acidente, sem dono e sem rotação. Um vazamento desses da acesso a verba de mídia, base de leads e histórico de campanhas, e a troca emergencial vira madrugada porque ninguém sabe onde cada chave está usada.

## Arquitetura Resumida

```
[segredo nasce no provider]
  -> 1. cofre (Vault KV ou gerenciador do provider, nunca repo)
  -> 2. entrega por referência (env var, OIDC, gh secret set)
  -> 3. rotacao agenda (30 dias crítico, 90 dias padrão)
  -> 4. varredura continua (secrets_audit.py + bloqueio de push)
  -> 5. resposta a vazamento (revogar, girar, auditar uso)
```

O `secrets_audit.py` implementa a etapa 4 localmente (regex de padrões reais, checagem de `.gitignore`, relatório) e o standard amarra cofre, rotação e resposta.

## Próximos Passos

1. Migrar os segredos críticos de Ads e CRM para o cofre e referenciar por variável de ambiente.
2. Ativar rotação de 30 dias nas chaves críticas e 90 dias nas demais, com dono nomeado.
3. Bloquear push com segredo (hook ou CI com varredura) e treinar o time no fluxo novo.

## Métricas de Sucesso

| Métrica | Atual | Meta |
|---------|-------|------|
| Credenciais críticas com rotação automática ou agendada | 0% (baseline desta PDI) | 100% em 90 dias (meta) |
| Segredos detectados em repos por varredura | a medir na primeira rodada | 0 após remediação (meta) |
| Tempo médio para revogar e girar chave vazada | sem rotina | até 4 h (meta) |

## Decisões e tradeoffs

1. Cofre central em vez de `.env` por projeto: elimina a dispersão e da auditoria única; exige que todo deploy leia segredo por referência, o que muda o bootstrap dos workers.
2. Segredos dinâmicos de curta duração onde der: credencial que expira em minutos reduz a janela de abuso a quase zero; nem todo provider suporta, e o código precisa tratar renovação.
3. OIDC do CI para cloud em vez de chave estática: GitHub Actions assume papel sem guardar segredo de longa duração; configuração inicial maior, operação posterior menor.
4. Varredura que falha o build ao achar segredo: impede o vazamento na origem, mas gera atrito no primeiro mês até o time limpar histórico e ajustar padrões.
5. Um dono por segredo com prazo de rotação: acaba com "chave de ninguém"; cria fila de trabalho recorrente que precisa entrar no planejamento.

## Impacto no negócio

Segredo com dono, cofre e rotação tira a operação de mídia e CRM do modo "uma chave vazada para o desastre": o custo de um vazamento cai de dias de retrabalho e risco de verba desviada para horas de procedimento ensaiado, e auditoria ou due diligence passa a encontrar processo em vez de improviso.

## Referências

- Curso: Trilha de tutoriais oficiais do HashiCorp Vault, do básico a dynamic secrets (HashiCorp Developer). https://developer.hashicorp.com/vault/tutorials
- Vídeo: How to get dynamic with secrets management (HashiCorp, YouTube). https://www.youtube.com/watch?v=aErDyZvQjWg
- Doc oficial: Vault product documentation. https://developer.hashicorp.com/vault/docs
- Doc oficial: Using secrets in GitHub Actions (GitHub Docs). https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions
