# Atividade 4: Catálogo de Serviços e Ownership com Matriz de Responsabilidade

| Campo | Valor |
|-------|-------|
| Área | Automação & Infraestrutura |
| Unidade | FV Marketing / V4 Company |
| Autor | Marcos Luciano |
| Data | Setembro 2026 |
| Status | Entregue (desenvolvido) |

## Entregas desta PDI

```
atividade-4/
├── README.md
├── 1-standards/
│   ├── 01-catalogo-e-ownership-fundamentos.md
│   └── 02-matriz-responsabilidade-orquestrador.md
├── 2-implementacao/
│   ├── 01-catalog-info-exemplo.yaml
│   ├── 02-template-catalog-info.yaml
│   └── 03-roda-ownership.md
└── 7-apresentacao/
    ├── DECK-PDI.md
    ├── DEMO-SCRIPT.md
    ├── ROTEIRO-DOMINIO.md
    ├── pdi-arquitetura-documentada-a4.html
    ├── pdi-arquitetura-documentada-a4.docx
    ├── pdi-arquitetura-documentada-a4.pdf
    └── gerar-docx.py
```

## Problema Resolvido

Quando o worker de coleta quebrava de madrugada, ninguém sabia quem acordar: o sistema não tinha dono declarado, cada peça tinha um "talvez o fulano saiba". Esta atividade declara dono por sistema em formato padrão (compatível com Backstage), publica a matriz de responsabilidade do orquestrador e cria a roda de ownership para não virar heroísmo individual.

## Arquitetura Resumida

```
[Catálogo: quem é o que] --> [Matriz: quem responde por qual peça]
        |                                      |
        +------> [Roda: revezamento e férias cobertos]
```

## Próximos Passos

1. Subir `catalog-info.yaml` por sistema e importar no Backstage (ou planilha espelho até la).
2. Definir dono e suplente de cada peça na próxima reunião do squad.
3. Revisão trimestral da matriz (dono: Marcos Luciano).

## Métricas de Sucesso

| Métrica | Atual | Meta |
|---------|-------|------|
| Sistemas com dono declarado | 4 de 4 | 6 de 6 |
| Peças sem suplente | 2 | 0 |
| Incidentes com dono achado em 15 min | 1 de 3 | 3 de 3 |
| Revisões trimestrais da matriz | 0 | 1 |

## Decisões e tradeoffs

1. **Formato Backstage mesmo sem Backstage rodando.** O `catalog-info.yaml` e padrão aberto e importa direto quando o portal existir; até la, uma leitura simples gera a planilha espelho. Custo: campo a mais hoje, migração zero amanhã.
2. **Dono e pessoa, suplente obrigatório.** Time não é dono, pessoa é. Sem suplente a férias vira incidente. Custo: conversa desconfortável de designar nomes, ganho de clareza total.
3. **Matriz simples, sem RACI burocrático.** Colunas: peça, dono, suplente, responde por, escala para. RACI completo ninguém mantém; simples de verdade sobrevive.
4. **Roda com revezamento semanal.** Um nome por semana responde primeiro, com regra de escala em 15 minutos. Evita herói fixo e distribui conhecimento.

## Impacto no negócio

Com dono declarado por peça, incidente deixa de ser broadcast no chat e vira chamada direta: quem responde, quem cobre férias e para quem escalar ficam visíveis em uma página. Isso encurta o tempo de resposta de madrugada, protege a operação de tráfego em período crítico e tira o conhecimento da cabeça de uma pessoa só, que é o risco mais caro de um time pequeno.

## Referências

- Curso: Agile Planning for Software Products, University of Alberta (Coursera): https://www.coursera.org/learn/agile-planning-for-software-products
- Vídeo: "Team Topologies, organização para fluxo rápido de valor", Matthew Skelton (YouTube)
- Doc: Backstage Software Catalog, entidades e ownership: https://backstage.io/docs/features/software-catalog/
- Doc: Team Topologies, padrões de times e ownership: https://teamtopologies.com/
