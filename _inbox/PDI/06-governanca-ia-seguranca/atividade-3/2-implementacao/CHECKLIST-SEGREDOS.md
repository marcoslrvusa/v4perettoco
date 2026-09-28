# CHECKLIST-SEGREDOS | Higiene e rotacao

Rodar mensalmente. Dono: responsavel por infraestrutura.

- [ ] Inventario de segredos atualizado (valor nunca na planilha, so referencia e dono)
- [ ] Nenhum segredo em repo: `python3 secrets_audit.py <repo>` limpo e `.gitignore` com `.env`, `*.pem`, `*.key`
- [ ] CI usa `gh secret set` por ambiente; nenhuma chave estatica de cloud no Actions (preferir OIDC)
- [ ] Rotacao em dia: criticas 30 dias, altas 90 dias, padrao 180 dias
- [ ] Dynamic secrets com TTL onde o provider suporta (alvo: banco e cloud)
- [ ] Leitura de segredo com menor privilegio e trilha de acesso ativa
- [ ] Procedimento de vazamento ensaiado (revogar, girar, auditar uso, comunicar, post-mortem)
- [ ] Ex-funcionarios e tokens pessoais antigos revogados
