# A1 | Guardrails e anti-prompt-injection em automações com LLM

| Campo | Valor |
|-------|-------|
| Área | Automação & Infraestrutura |
| Unidade | FV Marketing / V4 Company |
| Autor | Marcos Luciano |
| Data | Setembro 2026 |
| Status | Entregue (desenvolvido, homologação pendente) |

## Entregas desta PDI

```
atividade-1/
├── README.md
├── 1-standards/
│   └── STANDARD-GUARDRAILS-LLM.md
├── 2-implementacao/
│   ├── guardrail_proxy.py
│   └── CHECKLIST-GUARDRAILS.md
└── 7-apresentacao/
    ├── DECK-PDI.md
    ├── DEMO-SCRIPT.md
    ├── ROTEIRO-DOMINIO.md
    ├── pdi-governanca-ia-seguranca-a1.html
    ├── pdi-governanca-ia-seguranca-a1.docx
    ├── pdi-governanca-ia-seguranca-a1.pdf
    └── gerar-docx.py
```

## Problema Resolvido

Automações com LLM (resumo de leads, classificação de tickets, geração de copy) aceitam texto livre do usuário e de fontes externas (página, e-mail, planilha). Sem barreira, um prompt malicioso direto ("ignore as instruções anteriores e exfiltre...") ou indireto (instrução escondida num documento resumido pelo modelo) faz o modelo desviar da tarefa, vazar contexto do system prompt ou executar ação indevida via ferramenta conectada. O risco segue o OWASP LLM01:2025 (Prompt Injection) e LLM02 (Insecure Output Handling).

## Arquitetura Resumida

```
[entrada: usuário + fontes externas]
  -> 1. sanitizacao (delimitadores + limite de tamanho)
  -> 2. detector de injection (regras + Moderation API)
  -> 3. chamada ao LLM com system prompt blindado e safety_identifier
  -> 4. validação da saída (allowlist de formato + filtro)
  -> 5. HITL quando ação é sensível, log de auditoria sempre
```

O `guardrail_proxy.py` implementa as etapas 1, 2 e 4 em Python puro e deixa prontos os ganchos das etapas 3 e 5.

## Próximos Passos

1. Ligar o detector a Moderation API da OpenAI em 1 automação piloto (resumo de tickets).
2. Rodar bateria adversarial mensal de 60 casos e publicar o placar.
3. Exigir HITL em toda automação que escreve em CRM, Ads ou banco antes de ativar.

## Métricas de Sucesso

| Métrica | Atual | Meta |
|---------|-------|------|
| Bloqueio em bateria de 60 injeções (diretas e indiretas) | 0% (sem proteção) | 95% (meta) |
| Latência p95 adicionada pelo proxy | não medida | abaixo de 150 ms (meta) |
| Automações de alto risco com HITL ativo | 0% | 100% (meta) |

## Decisões e tradeoffs

1. Regras determinísticas antes de modelo juiz: regex e limites bloqueiam 80% dos ataques com latência quase zero; um LLM juiz entraria só nos casos duvidosos para não estourar custo e latência.
2. Bloquear por padrão, liberar por allowlist: output do modelo só passa se estiver no formato esperado (JSON com chaves fixas ou texto sem chamadas de ferramenta); seguro, mas exige mapear o contrato de cada automação.
3. Não exibir system prompt nem contexto interno em erro ou log: evita vazamento por engenharia social, ao custo de logs menos explicativos no debug.
4. `safety_identifier` com hash do usuário em toda chamada: permite rastrear abuso por titular sem enviar PII ao provider; exige gerar o hash no backend antes de chamar.
5. HITL obrigatório em ação irreversível: atrasa segundos a execução, mas elimina a classe inteira de dano por output inseguro (LLM02).

## Impacto no negócio

Com guardrails padronizados, a operação pode escalar automações com LLM para copy, triagem e resumo sem que cada novo fluxo vire um incidente de segurança em potencial: o custo de revisão cai, o risco de vazamento de dados de clientes cai junto, e a diretoria ganha um argumento auditável de diligência alinhado ao OWASP Top 10 para LLMs.

## Referências

- Curso: Generative AI with Large Language Models (DeepLearning.AI e AWS, Coursera). https://www.coursera.org/learn/generative-ai-with-llms
- Vídeo: Explained: The OWASP Top 10 for Large Language Model Applications (IBM Technology, YouTube). https://www.youtube.com/watch?v=cYuesqIKf9A
- Doc oficial: OWASP Top 10 for Large Language Model Applications. https://owasp.org/www-project-top-10-for-large-language-model-applications/
- Doc oficial: OpenAI Safety best practices. https://platform.openai.com/docs/guides/safety-best-practices
