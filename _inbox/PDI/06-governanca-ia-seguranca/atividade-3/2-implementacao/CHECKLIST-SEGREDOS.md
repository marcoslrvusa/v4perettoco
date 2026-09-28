# CHECKLIST-SEGREDOS | Higiene e rotação

Rodar mensalmente. Dono: responsável por infraestrutura.

- [ ] Inventário de segredos atualizado (valor nunca na planilha, só referência e dono)
- [ ] Nenhum segredo em repo: `python3 secrets_audit.py <repo>` limpo e `.gitignore` com `.env`, `*.pem`, `*.key`
- [ ] CI usa `gh secret set` por ambiente; nenhuma chave estática de cloud no Actions (preferir OIDC)
- [ ] Rotação em dia: críticas 30 dias, altas 90 dias, padrão 180 dias
- [ ] Dynamic secrets com TTL onde o provider suporta (alvo: banco e cloud)
- [ ] Leitura de segredo com menor privilegio e trilha de acesso ativa
- [ ] Procedimento de vazamento ensaiado (revogar, girar, auditar uso, comunicar, post-mortem)
- [ ] Ex-funcionarios e tokens pessoais antigos revogados
