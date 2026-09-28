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

ADR-054: Tratamento de PII

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

## Decisoes e tradeoffs

- **`consent_id` obrigatorio no payload**: so publica dado pessoal com base legal ativa; sem consentimento, o evento nao circula.
- **`subject_id` em vez de CPF bruto no downstream**: Vendas e Marketing operam com token e o Analytics recebe so hash sem reversao.
- **AES em repouso mais TLS em transito**: CPF e e-mail cifrados no broker, com campos sensiveis marcados com `pii:true` no schema `lead_event.avsc`.
- **Retencao com TTL de 365 dias e purge por `subject_id`**: o `retention_purge.py` varre e apaga, e o pedido de exclusao cai de 90 dias para menos de 1 dia, dentro do patamar de ate 15 dias.

## Impacto no negocio

Com zero PII em texto puro e 100% dos fluxos com consentimento, o risco de autuacao pela ANPD e de dano de imagem cai porque o dado passa a ter rastro no `mapa-dados.md` e prazo definido. O apagamento em menos de 1 dia transforma o direito ao esquecimento em rotina operacional de uma varredura por `subject_id`, em vez de cacada manual por servico.

## Referencias de estudo

- Curso: "LGPD na Pratica" (Udemy).
- Video: "O que e a LGPD?" (YouTube, SEBRAE).
- Documento oficial: Guia Orientativo da ANPD (gov.br/anpd).
- Documento oficial: Lei n. 13.709/2018 (planalto.gov.br).
