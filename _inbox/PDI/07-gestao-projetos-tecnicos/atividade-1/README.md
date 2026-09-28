# Atividade 1: Scoping e Estimativas Tecnicas

| Campo | Valor |
|---|---|
| Area | Automacao & Infraestrutura |
| Unidade | FV Marketing / V4 Company |
| Autor | Marcos Luciano |
| Data | Setembro 2026 |
| Status | Entregue (desenvolvido) |

## Entregas desta PDI

```
atividade-1/
├── README.md
├── 1-standards/
│   └── STANDARD-SCOPING-ESTIMATIVAS.md
├── 2-implementacao/
│   ├── planilha-estimativa.md
│   └── checklist-scoping.md
└── 7-apresentacao/
    ├── DECK-PDI.md
    ├── DEMO-SCRIPT.md
    ├── ROTEIRO-DOMINIO.md
    ├── report.json
    ├── gerar-docx.py
    ├── pdi-gestao-projetos-tecnicos-a1.html
    ├── pdi-gestao-projetos-tecnicos-a1.docx
    └── pdi-gestao-projetos-tecnicos-a1.pdf
```

## Problema Resolvido

Estimativas da area saiam como numero unico ("uns 3 dias") sem escopo escrito, sem buffer e sem revisao. Resultado: estouro recorrente de prazo em automacoes e integracoes, retrabalho e perda de credibilidade com a operacao. Esta atividade entrega um metodo repetivel: decomposicao em pacotes de ate 1 dia, estimativa de 3 pontos (PERT), buffer calculado e reestimativa por marco com o cone da incerteza.

## Arquitetura Resumida

```
Pedido (briefing) -> Checklist de scoping (DoR) -> WBS em pacotes <= 1 dia
  -> Estimativa O/M/P por pacote -> E = (O + 4M + P) / 6
  -> Buffer = 20% do total (ou raiz da soma dos quadrados)
  -> Faixa = E_total + buffer, revisada a cada marco (cone da incerteza)
  -> Compromisso = faixa + premissas registradas
```

## Proximos Passos

1. Aplicar a planilha nas proximas 4 automacoes e registrar estimado vs real.
2. Criar base historica simples (pacote, tipo, estimado, real) para calibrar buffers.
3. Apresentar o metodo em review da area e adotar como padrao de scoping.

## Metricas de Sucesso

| Metrica | Atual | Meta |
|---|---|---|
| Desvio medio estimado vs real | 60% (amostra de 6 entregas, ago/2026) | 25% (meta) |
| Entregas com escopo escrito e premissas | 30% | 100% (meta) |
| Reestimativas formais por projeto | 0 | 3 por projeto (meta) |

## Decisoes e tradeoffs

1. **Estimativa em faixa, nao numero unico**: faixa comunica incerteza e protege a credibilidade; tradeoff e exigir mais disciplina de quem consome a estimativa.
2. **Pacotes de no maximo 1 dia util**: pacotes grandes escondem risco; tradeoff e o custo de decompor (30 a 60 min por scoping).
3. **Buffer explicito de 20% em vez de gordura escondida**: buffer visivel permite negociar escopo; tradeoff e parecer "mais caro" que estimativa sem buffer.
4. **PERT simplificado (O/M/P) em vez de planning poker**: funciona para 1 pessoa estimando automacao solo; tradeoff e menor precisao em trabalho de equipe grande.
5. **Reestimativa obrigatoria em 3 marcos**: o cone da incerteza so funciona se a estimativa for refeita; tradeoff e o tempo de revisao (15 min por marco).

## Impacto no negocio

Com escopo escrito e faixa com buffer, a area passa a cumprir prazos com frequencia previsivel, o que destrava o planejamento da operacao de marketing (campanhas, relatorios e integracoes dependem dessas entregas) e reduz o custo do retrabalho de ultima hora.

## Referencias

- Curso: Agile Project Management, modulo do Google Project Management Professional Certificate (Coursera): https://www.coursera.org/learn/agile-project-management
- Video: Story points and estimation, Mountain Goat Software (YouTube)
- Doc: Manifesto Agil, valores e principios: https://agilemanifesto.org/
- Doc: The New Methodology, Martin Fowler (adaptativo vs preditivo): https://martinfowler.com/articles/newMethodology.html
