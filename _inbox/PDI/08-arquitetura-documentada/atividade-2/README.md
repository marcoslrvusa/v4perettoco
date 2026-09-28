# Atividade 2: ADRs, Architecture Decision Records com Ciclo de Vida e Exemplos Reais

| Campo | Valor |
|-------|-------|
| Área | Automação & Infraestrutura |
| Unidade | FV Marketing / V4 Company |
| Autor | Marcos Luciano |
| Data | Setembro 2026 |
| Status | Entregue (desenvolvido) |

## Entregas desta PDI

```
atividade-2/
├── README.md
├── 1-standards/
│   ├── 01-formato-e-ciclo-de-vida-adr.md
│   └── 02-exemplos-reais-adr.md
├── 2-implementacao/
│   ├── 01-template-adr.md
│   ├── 02-adr-001-n8n-orquestrador.md
│   └── 03-adr-002-supabase-postgres.md
└── 7-apresentacao/
    ├── DECK-PDI.md
    ├── DEMO-SCRIPT.md
    ├── ROTEIRO-DOMINIO.md
    ├── pdi-arquitetura-documentada-a2.html
    ├── pdi-arquitetura-documentada-a2.docx
    ├── pdi-arquitetura-documentada-a2.pdf
    └── gerar-docx.py
```

## Problema Resolvido

Decisões como "por que n8n e não fila própria" ou "por que Supabase e não planilha" viviam na cabeça de uma pessoa ou perdidas no chat. Quando alguém questionava, ninguém lembrava o motivo e a decisão era refeita do zero. Esta atividade implanta ADRs numerados e imutáveis no repo, com ciclo de vida claro, e registra as duas decisões reais que sustentam o orquestrador.

## Arquitetura Resumida

```
[Proposta] --> [Em avaliacao] --> [Aceita] --> [Implementada]
                    |                                |
                [Rejeitada]                    [Superada por ADR novo]
                    (tudo versionado em docs/adr/NNNN-titulo.md)
```

## Próximos Passos

1. Criar `docs/adr/` no repo e mover ADR-001 e ADR-002 para la.
2. Exigir ADR para toda decisão reversível cara (troca de banco, de fila, de provedor).
3. Revisão anual dos ADRs aceitos (dono: Marcos Luciano).

## Métricas de Sucesso

| Métrica | Atual | Meta |
|---------|-------|------|
| ADRs registrados | 2 | 6 |
| Decisões refeitas por falta de registro (trimestre) | 3 | 0 |
| ADRs com consequências monitoradas | 1 | 4 |
| Tempo para achar o motivo de uma decisão | dias | minutos |

## Decisões e tradeoffs

1. **ADR imutável, superado por ADR novo.** Editar o passado apaga o aprendizado; quando a decisão muda, um ADR novo marca o antigo como superado. Custo: mais arquivos, histórico honesto.
2. **Formato curto de 5 seções.** Contexto, decisão, alternativas, consequências e status. Formato longo de consultoria ninguém preenche; curto de verdade entra no ritmo.
3. **Só decisão arquiteturalmente relevante.** Bugfix e detalhe de código não ganham ADR. Critério: se trocar depois custa mais de 1 semana, merece ADR.
4. **Número sequencial, nunca reutilizado.** ADR-001 e sempre ADR-001, mesmo superado. Evita referência quebrada em conversas e docs.

## Impacto no negócio

Com ADRs, a operação para de pagar o imposto da memória: ninguém precisa recapitular por que o n8n foi escolhido nem por que o estado mora no Postgres toda vez que surge uma ferramenta nova. A decisão, as alternativas descartadas e o custo de troca ficam a uma busca de distância, o que acelera avaliação de fornecedores e protege a continuidade quando alguém sai do time.

## Referências

- Curso: Software Architecture, University of Alberta (Coursera): https://www.coursera.org/learn/software-architecture
- Vídeo: "Architecture Decision Records in Action", Michael Keeling e Joe Runde (YouTube)
- Doc: Organização ADR, práticas e templates: https://adr.github.io/
- Doc: Repositório de exemplos e templates de ADR: https://github.com/joelparkerhenderson/architecture-decision-record
