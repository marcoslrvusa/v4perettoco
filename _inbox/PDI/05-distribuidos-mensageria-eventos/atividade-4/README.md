# Conformidade LGPD em Eventos e Dados (anonimizacao, consentimento, esquecimento)

Sistemas Distribuidos

## Resumo Executivo

Padrao LGPD para o ecossistema de dados/eventos: minimizacao, consentimento por fluxo, anonimizacao em logs/traces e direito ao esquecimento via delete em cascata. Entrego o padrao e um util de anonimizacao.

Eventos e traces carregam PII (e-mail, CNPJ); sem controle, vazamento e processo administrativo.

## Contexto de Producao

- Logs de agente gravavam e-mail inteiro.

- Sem consentimento por finalidade.

- Pedido de exclusao nao propagava.

## Diagnostico

| Hoje | Alvo |

| --- | --- |

| PII em log/trace | anonimizado |

| sem consentimento | consent por finalidade |

| delete parcial | cascata |

## Decisao Arquitetural (ADR)

ADR-054 — Tratamento de PII

| Opcao | Pro | Contra | Decisao |

| --- | --- | --- | --- |

| Anon + consent + delete cascata | conforme LGPD | governanca | ESCOLHIDA |

> **Nota:** Minimizacao por padrao; PII so com consentimento e retencao definida.

## Entregas

- LGPD-DATA.md.

- anon.py.

- retention_policy.sql.

## Validacao

1. Varrer logs: 0 e-mail/CNPJ cru.

2. Simular exclusao: delete em todas as tabelas.

3. Auditoria: consentimento por finalidade.

## Metricas e SLO

| SLO | Alvo |

| --- | --- |

| PII em log | 0 |

| Exclusao | <= 15 dias |

| Consentimento | 100% fluxos |

## Riscos

| Risco | Mitigacao |

| --- | --- |

| Delete esquece tabela | mapear subject |

| Cache PII | nao cachear |

## Proximos Passos

- Data map de PII.

- Alerta de PII em logs.