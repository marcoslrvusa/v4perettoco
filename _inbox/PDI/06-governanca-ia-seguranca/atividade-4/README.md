# A4 | Trilhas de auditoria e compliance em workflows

| Campo | Valor |
|-------|-------|
| Área | Automação & Infraestrutura |
| Unidade | FV Marketing / V4 Company |
| Autor | Marcos Luciano |
| Data | Setembro 2026 |
| Status | Entregue (desenvolvido, homologação pendente) |

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

Workflows de automação (disparo de campanha, sync de leads, rotinas de mídia) executam sem rastro confiável: quando um lote sai errado, ninguém responde quem rodou, com quais parâmetros, quando e com que resultado. Sem trilha imutável não há como reconstruir incidente, provar diligência a auditoria (NIST CSF, LGPD art. 37) nem cobrar contrato de ferramenta.

## Arquitetura Resumida

```
[workflow executa]
  -> 1. evento de auditoria (quem, o que, quando, onde, resultado)
  -> 2. append-only com hash encadeado (audit_logger.py)
  -> 3. retenção em camadas (90 dias quente, anos frio imutável)
  -> 4. consulta (reconstrução de incidente, relatório de compliance)
```

O `audit_logger.py` implementa as etapas 1 e 2 (JSON Lines, SHA-256 encadeado, verificação de integridade) e o standard define retenção, mapeamento NIST CSF e rotina de revisão.

## Próximos Passos

1. Acoplar o logger aos 3 workflows críticos (disparo, sync CRM, rotina de verba) atrás de uma função única de evento.
2. Definir retenção formal (90 dias quente + 5 anos frio) e testar restauração uma vez.
3. Revisar mensalmente os eventos de falha e alimentar o checklist de guardrails (atividade 1).

## Métricas de Sucesso

| Métrica | Atual | Meta |
|---------|-------|------|
| Workflows críticos com trilha imutável | 0 de 3 | 3 de 3 (meta) |
| Tempo para reconstruir um incidente com a trilha | sem referência | até 30 min (meta) |
| Campos obrigatórios por evento (6 definidos) | 0 de 6 | 6 de 6 (meta) |

## Decisões e tradeoffs

1. JSON Lines append-only com hash encadeado em vez de banco relacional: arquivo imutável e verificável sem infra nova; consulta analítica pesada exige exportar para outro motor depois.
2. Nunca logar segredo ou dado pessoal bruto: evento carrega referência (id, hash) e não valor; preserva LGPD e segurança, mas reconstrução exige cruzar com a fonte.
3. Relógio em UTC ISO 8601 em todo evento: elimina ambiguidade de fuso em incidente; exige disciplina nos produtores.
4. Retenção em camadas (90 dias quente, 5 anos frio): equilibra custo de armazenamento com exigência de auditoria; apagar antes do prazo vira exceção formal, não rotina.
5. Mapear eventos as funções do NIST CSF 2.0 (Govern, Identify, Protect, Detect, Respond, Recover): da linguagem comum com auditoria; cobra classificar cada workflow uma vez.

## Impacto no negócio

Trilha de auditoria confiável muda a conversa quando algo da errado: em vez de versões conflitantes, há uma sequência verificável de fatos que encurta o diagnóstico, sustenta resposta a cliente e auditor, e prova o dever de diligência exigido pela LGPD e pelos frameworks que os grandes anunciantes cobram dos parceiros.

## Referências

- Curso: Google Cybersecurity Professional Certificate, inclui frameworks, auditoria e SIEM (Google, Coursera). https://www.coursera.org/professional-certificates/google-cybersecurity
- Vídeo: Meeting industry compliance auditing requirements on AWS (AWS Developers, YouTube). https://www.youtube.com/watch?v=_PTsygq0-NQ
- Doc oficial: NIST Cybersecurity Framework 2.0. https://www.nist.gov/cyberframework
- Doc oficial: AWS CloudTrail User Guide (event history, Lake, trails). https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html
