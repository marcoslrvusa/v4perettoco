# A1 | Guardrails e anti-prompt-injection em automacoes com LLM

| Campo | Valor |
|-------|-------|
| Area | Automacao & Infraestrutura |
| Unidade | FV Marketing / V4 Company |
| Autor | Marcos Luciano |
| Data | Setembro 2026 |
| Status | Entregue (desenvolvido, homologacao pendente) |

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

Automacoes com LLM (resumo de leads, classificacao de tickets, geracao de copy) aceitam texto livre do usuario e de fontes externas (pagina, e-mail, planilha). Sem barreira, um prompt malicioso direto ("ignore as instrucoes anteriores e exfiltre...") ou indireto (instrucao escondida num documento resumido pelo modelo) faz o modelo desviar da tarefa, vazar contexto do system prompt ou executar acao indevida via ferramenta conectada. O risco segue o OWASP LLM01:2025 (Prompt Injection) e LLM02 (Insecure Output Handling).

## Arquitetura Resumida

```
[entrada: usuario + fontes externas]
  -> 1. sanitizacao (delimitadores + limite de tamanho)
  -> 2. detector de injection (regras + Moderation API)
  -> 3. chamada ao LLM com system prompt blindado e safety_identifier
  -> 4. validacao da saida (allowlist de formato + filtro)
  -> 5. HITL quando acao e sensivel, log de auditoria sempre
```

O `guardrail_proxy.py` implementa as etapas 1, 2 e 4 em Python puro e deixa prontos os ganchos das etapas 3 e 5.

## Proximos Passos

1. Ligar o detector a Moderation API da OpenAI em 1 automacao piloto (resumo de tickets).
2. Rodar bateria adversarial mensal de 60 casos e publicar o placar.
3. Exigir HITL em toda automacao que escreve em CRM, Ads ou banco antes de ativar.

## Metricas de Sucesso

| Metrica | Atual | Meta |
|---------|-------|------|
| Bloqueio em bateria de 60 injecoes (diretas e indiretas) | 0% (sem protecao) | 95% (meta) |
| Latencia p95 adicionada pelo proxy | nao medida | abaixo de 150 ms (meta) |
| Automacoes de alto risco com HITL ativo | 0% | 100% (meta) |

## Decisoes e tradeoffs

1. Regras deterministicas antes de modelo juiz: regex e limites bloqueiam 80% dos ataques com latencia quase zero; um LLM juiz entraria so nos casos duvidosos para nao estourar custo e latencia.
2. Bloquear por padrao, liberar por allowlist: output do modelo so passa se estiver no formato esperado (JSON com chaves fixas ou texto sem chamadas de ferramenta); seguro, mas exige mapear o contrato de cada automacao.
3. Nao exibir system prompt nem contexto interno em erro ou log: evita vazamento por engenharia social, ao custo de logs menos explicativos no debug.
4. `safety_identifier` com hash do usuario em toda chamada: permite rastrear abuso por titular sem enviar PII ao provider; exige gerar o hash no backend antes de chamar.
5. HITL obrigatorio em acao irreversivel: atrasa segundos a execucao, mas elimina a classe inteira de dano por output inseguro (LLM02).

## Impacto no negocio

Com guardrails padronizados, a operacao pode escalar automacoes com LLM para copy, triagem e resumo sem que cada novo fluxo vire um incidente de seguranca em potencial: o custo de revisao cai, o risco de vazamento de dados de clientes cai junto, e a diretoria ganha um argumento auditavel de diligencia alinhado ao OWASP Top 10 para LLMs.

## Referencias

- Curso: Generative AI with Large Language Models (DeepLearning.AI e AWS, Coursera). https://www.coursera.org/learn/generative-ai-with-llms
- Video: Explained: The OWASP Top 10 for Large Language Model Applications (IBM Technology, YouTube). https://www.youtube.com/watch?v=cYuesqIKf9A
- Doc oficial: OWASP Top 10 for Large Language Model Applications. https://owasp.org/www-project-top-10-for-large-language-model-applications/
- Doc oficial: OpenAI Safety best practices. https://platform.openai.com/docs/guides/safety-best-practices
