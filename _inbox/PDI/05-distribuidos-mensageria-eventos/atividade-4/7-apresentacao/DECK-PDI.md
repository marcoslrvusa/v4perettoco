# Deck PDI — Conformidade LGPD em Eventos e Dados (anonimizacao, consentimento, esquecimento)

Area: Sistemas Distribuidos

## Slide 1: Resumo Executivo
Padrao LGPD para o ecossistema de dados/eventos: minimizacao, consentimento por fluxo, anonimizacao em logs/traces e direito ao esquecimento via delete em cascata. Entrego o padrao e um util de anonimizacao.
Eventos e traces carregam PII (e-mail, CNPJ); sem controle, vazamento e processo administrativo.
## Slide 2: Contexto de Producao
Logs de agente gravavam e-mail inteiro.
Sem consentimento por finalidade.
Pedido de exclusao nao propagava.
## Slide 3: Diagnostico
| Hoje | Alvo |
| --- | --- |
| PII em log/trace | anonimizado |
| sem consentimento | consent por finalidade |
| delete parcial | cascata |
## Slide 4: Decisao Arquitetural (ADR)
ADR-054 — Tratamento de PII
| Opcao | Pro | Contra | Decisao |
| --- | --- | --- | --- |
| Anon + consent + delete cascata | conforme LGPD | governanca | ESCOLHIDA |
> Nota: Minimizacao por padrao; PII so com consentimento e retencao definida.
## Slide 5: Entregas
LGPD-DATA.md.
anon.py.
retention_policy.sql.
## Slide 6: Validacao
Varrer logs: 0 e-mail/CNPJ cru.
Simular exclusao: delete em todas as tabelas.
Auditoria: consentimento por finalidade.
## Slide 7: Metricas e SLO
| SLO | Alvo |
| --- | --- |
| PII em log | 0 |
| Exclusao | <= 15 dias |
| Consentimento | 100% fluxos |
## Slide 8: Riscos
| Risco | Mitigacao |
| --- | --- |
| Delete esquece tabela | mapear subject |
| Cache PII | nao cachear |
## Slide 9: Proximos Passos
Data map de PII.
Alerta de PII em logs.