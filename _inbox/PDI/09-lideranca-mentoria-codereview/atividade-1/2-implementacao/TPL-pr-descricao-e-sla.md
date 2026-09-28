# TPL: Descrição de PR + SLA (template de corpo do PR)

```markdown
## Contexto
(máx 5 linhas: qual problema, para quem, link da task)

## O que muda
- item 1
- item 2

## Como testar
1. passo 1
2. resultado esperado

## Riscos e rollback
- Risco: ____ Mitigação: ____
- Rollback: ____ (flag, revert, migração reversa)

## Tamanho
- Linhas alteradas: ____ (se > 400, justificativa: ____)

## Checklist do autor
- [ ] Rodei lint e testes local
- [ ] Marquei revisor principal: @____
- [ ] Labels: ____ (`urgente` só se cliente parado ou hotfix)
```

## SLA aplicado a este PR

| Tipo | Primeira resposta |
|------|-------------------|
| Padrão | 8h úteis |
| Urgente (`urgente`) | 2h úteis |

## CODEOWNERS sugerido

```
# áreas críticas exigem dono da área
/pagamento/      @time-pagamentos
/dados-pessoais/ @time-dados
/auth/           @time-plataforma
/infra/          @time-plataforma
```

Regra: proteção de branch exige CI verde + 1 approval (2 approvals nas pastas acima).
