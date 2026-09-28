# A4 | Trilhas de auditoria e compliance em workflows

| Campo | Valor |
|-------|-------|
| Area | Automacao & Infraestrutura |
| Unidade | FV Marketing / V4 Company |
| Autor | Marcos Luciano |
| Data | Setembro 2026 |
| Status | Entregue (desenvolvido, homologacao pendente) |

## Entregas desta PDI

```
atividade-4/
├── README.md
├── 1-standards/
│   └── STANDARD-AUDIT-LOG.md
├── 2-implementacao/
│   ├── audit_logger.py
│   └── CHECKLIST-AUDITORIA.md
└── 7-apresentacao/
    ├── DECK-PDI.md
    ├── DEMO-SCRIPT.md
    ├── ROTEIRO-DOMINIO.md
    ├── pdi-governanca-ia-seguranca-a4.html
    ├── pdi-governanca-ia-seguranca-a4.docx
    ├── pdi-governanca-ia-seguranca-a4.pdf
    └── gerar-docx.py
```

## Problema Resolvido

Workflows de automacao (disparo de campanha, sync de leads, rotinas de midia) executam sem rastro confiavel: quando um lote sai errado, ninguem responde quem rodou, com quais parametros, quando e com que resultado. Sem trilha imutavel nao ha como reconstruir incidente, provar diligencia a auditoria (NIST CSF, LGPD art. 37) nem cobrar contrato de ferramenta.

## Arquitetura Resumida

```
[workflow executa]
  -> 1. evento de auditoria (quem, o que, quando, onde, resultado)
  -> 2. append-only com hash encadeado (audit_logger.py)
  -> 3. retencao em camadas (90 dias quente, anos frio imutavel)
  -> 4. consulta (reconstrucao de incidente, relatorio de compliance)
```

O `audit_logger.py` implementa as etapas 1 e 2 (JSON Lines, SHA-256 encadeado, verificacao de integridade) e o standard define retencao, mapeamento NIST CSF e rotina de revisao.

## Proximos Passos

1. Acoplar o logger aos 3 workflows criticos (disparo, sync CRM, rotina de verba) atras de uma funcao unica de evento.
2. Definir retencao formal (90 dias quente + 5 anos frio) e testar restauracao uma vez.
3. Revisar mensalmente os eventos de falha e alimentar o checklist de guardrails (atividade 1).

## Metricas de Sucesso

| Metrica | Atual | Meta |
|---------|-------|------|
| Workflows criticos com trilha imutavel | 0 de 3 | 3 de 3 (meta) |
| Tempo para reconstruir um incidente com a trilha | sem referencia | ate 30 min (meta) |
| Campos obrigatorios por evento (6 definidos) | 0 de 6 | 6 de 6 (meta) |

## Decisoes e tradeoffs

1. JSON Lines append-only com hash encadeado em vez de banco relacional: arquivo imutavel e verificavel sem infra nova; consulta analitica pesada exige exportar para outro motor depois.
2. Nunca logar segredo ou dado pessoal bruto: evento carrega referencia (id, hash) e nao valor; preserva LGPD e seguranca, mas reconstrucao exige cruzar com a fonte.
3. Relogio em UTC ISO 8601 em todo evento: elimina ambiguidade de fuso em incidente; exige disciplina nos produtores.
4. Retencao em camadas (90 dias quente, 5 anos frio): equilibra custo de armazenamento com exigencia de auditoria; apagar antes do prazo vira excecao formal, nao rotina.
5. Mapear eventos as funcoes do NIST CSF 2.0 (Govern, Identify, Protect, Detect, Respond, Recover): da linguagem comum com auditoria; cobra classificar cada workflow uma vez.

## Impacto no negocio

Trilha de auditoria confiavel muda a conversa quando algo da errado: em vez de versoes conflitantes, ha uma sequencia verificavel de fatos que encurta o diagnostico, sustenta resposta a cliente e auditor, e prova o dever de diligencia exigido pela LGPD e pelos frameworks que os grandes anunciantes cobram dos parceiros.

## Referencias

- Curso: Google Cybersecurity Professional Certificate, inclui frameworks, auditoria e SIEM (Google, Coursera). https://www.coursera.org/professional-certificates/google-cybersecurity
- Video: Meeting industry compliance auditing requirements on AWS (AWS Developers, YouTube). https://www.youtube.com/watch?v=_PTsygq0-NQ
- Doc oficial: NIST Cybersecurity Framework 2.0. https://www.nist.gov/cyberframework
- Doc oficial: AWS CloudTrail User Guide (event history, Lake, trails). https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html
