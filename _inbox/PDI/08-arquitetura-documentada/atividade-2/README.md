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

Decisoes como "por que n8n e nao fila propria" ou "por que Supabase e nao planilha" viviam na cabeca de uma pessoa ou perdidas no chat. Quando alguem questionava, ninguem lembrava o motivo e a decisao era refeita do zero. Esta atividade implanta ADRs numerados e imutaveis no repo, com ciclo de vida claro, e registra as duas decisoes reais que sustentam o orquestrador.

## Arquitetura Resumida

```
[Proposta] --> [Em avaliacao] --> [Aceita] --> [Implementada]
                    |                                |
                [Rejeitada]                    [Superada por ADR novo]
                    (tudo versionado em docs/adr/NNNN-titulo.md)
```

## Proximos Passos

1. Criar `docs/adr/` no repo e mover ADR-001 e ADR-002 para la.
2. Exigir ADR para toda decisao reversivel cara (troca de banco, de fila, de provedor).
3. Revisao anual dos ADRs aceitos (dono: Marcos Luciano).

## Metricas de Sucesso

| Metrica | Atual | Meta |
|---------|-------|------|
| ADRs registrados | 2 | 6 |
| Decisoes refeitas por falta de registro (trimestre) | 3 | 0 |
| ADRs com consequencias monitoradas | 1 | 4 |
| Tempo para achar o motivo de uma decisao | dias | minutos |

## Decisoes e tradeoffs

1. **ADR imutavel, superado por ADR novo.** Editar o passado apaga o aprendizado; quando a decisao muda, um ADR novo marca o antigo como superado. Custo: mais arquivos, historico honesto.
2. **Formato curto de 5 secoes.** Contexto, decisao, alternativas, consequencias e status. Formato longo de consultoria ninguem preenche; curto de verdade entra no ritmo.
3. **So decisao arquiteturalmente relevante.** Bugfix e detalhe de codigo nao ganham ADR. Criterio: se trocar depois custa mais de 1 semana, merece ADR.
4. **Numero sequencial, nunca reutilizado.** ADR-001 e sempre ADR-001, mesmo superado. Evita referencia quebrada em conversas e docs.

## Impacto no negocio

Com ADRs, a operacao para de pagar o imposto da memoria: ninguem precisa recapitular por que o n8n foi escolhido nem por que o estado mora no Postgres toda vez que surge uma ferramenta nova. A decisao, as alternativas descartadas e o custo de troca ficam a uma busca de distancia, o que acelera avaliacao de fornecedores e protege a continuidade quando alguem sai do time.

## Referencias

- Curso: Software Architecture, University of Alberta (Coursera): https://www.coursera.org/learn/software-architecture
- Video: "Architecture Decision Records in Action", Michael Keeling e Joe Runde (YouTube)
- Doc: Organizacao ADR, praticas e templates: https://adr.github.io/
- Doc: Repositorio de exemplos e templates de ADR: https://github.com/joelparkerhenderson/architecture-decision-record
