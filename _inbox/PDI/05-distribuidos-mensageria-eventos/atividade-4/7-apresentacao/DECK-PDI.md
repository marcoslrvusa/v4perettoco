# Deck PDI: Conformidade LGPD em Eventos e Dados (anonimização, consentimento, esquecimento)

Área: Sistemas Distribuídos

## Slide 1: Resumo Executivo
Padrão LGPD para o ecossistema de dados/eventos: minimização, consentimento por fluxo, anonimização em logs/traces e direito ao esquecimento via delete em cascata. Entrego o padrão e um útil de anonimização.
Eventos e traces carregam PII (e-mail, CNPJ); sem controle, vazamento e processo administrativo.
## Slide 2: Contexto de Produção
Logs de agente gravavam e-mail inteiro.
Sem consentimento por finalidade.
Pedido de exclusão não propagava.
## Slide 3: Diagnóstico
| Hoje | Alvo |
| --- | --- |
| PII em log/trace | anonimizado |
| sem consentimento | consent por finalidade |
| delete parcial | cascata |
## Slide 4: Decisão Arquitetural (ADR)
ADR-054: Tratamento de PII
| Opção | Pro | Contra | Decisão |
| --- | --- | --- | --- |
| Anon + consent + delete cascata | conforme LGPD | governança | ESCOLHIDA |
> Nota: Minimização por padrão; PII só com consentimento e retenção definida.
## Slide 5: Entregas
LGPD-DATA.md.
anon.py.
retention_policy.sql.
## Slide 6: Validação
Varrer logs: 0 e-mail/CNPJ cru.
Simular exclusão: delete em todas as tabelas.
Auditoria: consentimento por finalidade.
## Slide 7: Métricas e SLO
| SLO | Alvo |
| --- | --- |
| PII em log | 0 |
| Exclusão | <= 15 dias |
| Consentimento | 100% fluxos |
## Slide 8: Riscos
| Risco | Mitigação |
| --- | --- |
| Delete esquece tabela | mapear subject |
| Cache PII | não cachear |
## Slide 9: Próximos Passos
Data map de PII.
Alerta de PII em logs.