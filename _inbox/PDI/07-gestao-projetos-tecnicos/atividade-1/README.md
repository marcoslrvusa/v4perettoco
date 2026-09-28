# Atividade 1: Scoping e Estimativas Técnicas

| Campo | Valor |
|---|---|
| Área | Automação & Infraestrutura |
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

Estimativas da área saíam como número único ("uns 3 dias") sem escopo escrito, sem buffer e sem revisão. Resultado: estouro recorrente de prazo em automações e integrações, retrabalho e perda de credibilidade com a operação. Esta atividade entrega um método repetível: decomposição em pacotes de até 1 dia, estimativa de 3 pontos (PERT), buffer calculado e reestimativa por marco com o cone da incerteza.

## Arquitetura Resumida

```
Pedido (briefing) -> Checklist de scoping (DoR) -> WBS em pacotes <= 1 dia
  -> Estimativa O/M/P por pacote -> E = (O + 4M + P) / 6
  -> Buffer = 20% do total (ou raiz da soma dos quadrados)
  -> Faixa = E_total + buffer, revisada a cada marco (cone da incerteza)
  -> Compromisso = faixa + premissas registradas
```

## Próximos Passos

1. Aplicar a planilha nas próximas 4 automações e registrar estimado vs real.
2. Criar base histórica simples (pacote, tipo, estimado, real) para calibrar buffers.
3. Apresentar o método em review da área e adotar como padrão de scoping.

## Métricas de Sucesso

| Métrica | Atual | Meta |
|---|---|---|
| Desvio médio estimado vs real | 60% (amostra de 6 entregas, ago/2026) | 25% (meta) |
| Entregas com escopo escrito e premissas | 30% | 100% (meta) |
| Reestimativas formais por projeto | 0 | 3 por projeto (meta) |

## Decisões e tradeoffs

1. **Estimativa em faixa, não número único**: faixa comunica incerteza e protege a credibilidade; tradeoff é exigir mais disciplina de quem consome a estimativa.
2. **Pacotes de no máximo 1 dia útil**: pacotes grandes escondem risco; tradeoff é o custo de decompor (30 a 60 min por scoping).
3. **Buffer explícito de 20% em vez de gordura escondida**: buffer visível permite negociar escopo; tradeoff é parecer "mais caro" que estimativa sem buffer.
4. **PERT simplificado (O/M/P) em vez de planning poker**: funciona para 1 pessoa estimando automação solo; tradeoff é menor precisão em trabalho de equipe grande.
5. **Reestimativa obrigatória em 3 marcos**: o cone da incerteza só funciona se a estimativa for refeita; tradeoff é o tempo de revisão (15 min por marco).

## Impacto no negócio

Com escopo escrito e faixa com buffer, a área passa a cumprir prazos com frequência previsível, o que destrava o planejamento da operação de marketing (campanhas, relatórios e integrações dependem dessas entregas) e reduz o custo do retrabalho de última hora.

## Referências

- Curso: Agile Project Management, módulo do Google Project Management Professional Certificate (Coursera): https://www.coursera.org/learn/agile-project-management
- Vídeo: Story points and estimation, Mountain Goat Software (YouTube)
- Doc: Manifesto Ágil, valores e princípios: https://agilemanifesto.org/
- Doc: The New Methodology, Martin Fowler (adaptativo vs preditivo): https://martinfowler.com/articles/newMethodology.html
