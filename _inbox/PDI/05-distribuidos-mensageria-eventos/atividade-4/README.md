# Conformidade LGPD em Eventos e Dados (anonimização, consentimento, esquecimento)

Sistemas Distribuídos

## Resumo Executivo

Padrão LGPD para o ecossistema de dados/eventos: minimização, consentimento por fluxo, anonimização em logs/traces e direito ao esquecimento via delete em cascata. Entrego o padrão e um útil de anonimização.

Eventos e traces carregam PII (e-mail, CNPJ); sem controle, vazamento e processo administrativo.

## Contexto de Produção

- Logs de agente gravavam e-mail inteiro.

- Sem consentimento por finalidade.

- Pedido de exclusão não propagava.

## Diagnóstico

| Hoje | Alvo |

| --- | --- |

| PII em log/trace | anonimizado |

| sem consentimento | consent por finalidade |

| delete parcial | cascata |

## Decisão Arquitetural (ADR)

ADR-054: Tratamento de PII

| Opção | Pro | Contra | Decisão |

| --- | --- | --- | --- |

| Anon + consent + delete cascata | conforme LGPD | governança | ESCOLHIDA |

> **Nota:** Minimização por padrão; PII só com consentimento e retenção definida.

## Entregas

- LGPD-DATA.md.

- anon.py.

- retention_policy.sql.

## Validação

1. Varrer logs: 0 e-mail/CNPJ cru.

2. Simular exclusão: delete em todas as tabelas.

3. Auditoria: consentimento por finalidade.

## Métricas e SLO

| SLO | Alvo |

| --- | --- |

| PII em log | 0 |

| Exclusão | <= 15 dias |

| Consentimento | 100% fluxos |

## Riscos

| Risco | Mitigação |

| --- | --- |

| Delete esquece tabela | mapear subject |

| Cache PII | não cachear |

## Próximos Passos

- Data map de PII.

- Alerta de PII em logs.

## Decisões e tradeoffs

- **`consent_id` obrigatório no payload**: só publica dado pessoal com base legal ativa; sem consentimento, o evento não circula.
- **`subject_id` em vez de CPF bruto no downstream**: Vendas e Marketing operam com token e o Analytics recebe só hash sem reversão.
- **AES em repouso mais TLS em trânsito**: CPF e e-mail cifrados no broker, com campos sensíveis marcados com `pii:true` no schema `lead_event.avsc`.
- **Retenção com TTL de 365 dias e purge por `subject_id`**: o `retention_purge.py` varre e apaga, e o pedido de exclusão cai de 90 dias para menos de 1 dia, dentro do patamar de até 15 dias.

## Impacto no negócio

Com zero PII em texto puro e 100% dos fluxos com consentimento, o risco de autuação pela ANPD e de dano de imagem cai porque o dado passa a ter rastro no `mapa-dados.md` e prazo definido. O apagamento em menos de 1 dia transforma o direito ao esquecimento em rotina operacional de uma varredura por `subject_id`, em vez de caçada manual por serviço.

## Referências de estudo

- Curso: "LGPD na Prática" (Udemy).
- Vídeo: "O que é a LGPD?" (YouTube, SEBRAE).
- Documento oficial: Guia Orientativo da ANPD (gov.br/anpd).
- Documento oficial: Lei n. 13.709/2018 (planalto.gov.br).
