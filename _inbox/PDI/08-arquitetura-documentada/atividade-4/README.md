# Atividade 4: Catalogo de Servicos e Ownership com Matriz de Responsabilidade

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

Quando o worker de coleta quebrava de madrugada, ninguem sabia quem acordar: o sistema nao tinha dono declarado, cada peca tinha um "talvez o fulano saiba". Esta atividade declara dono por sistema em formato padrao (compativel com Backstage), publica a matriz de responsabilidade do orquestrador e cria a roda de ownership para nao virar heroismo individual.

## Arquitetura Resumida

```
[Catalogo: quem e o que] --> [Matriz: quem responde por qual peca]
        |                                      |
        +------> [Roda: revezamento e ferias cobertos]
```

## Proximos Passos

1. Subir `catalog-info.yaml` por sistema e importar no Backstage (ou planilha espelho ate la).
2. Definir dono e suplente de cada peca na proxima reuniao do squad.
3. Revisao trimestral da matriz (dono: Marcos Luciano).

## Metricas de Sucesso

| Metrica | Atual | Meta |
|---------|-------|------|
| Sistemas com dono declarado | 4 de 4 | 6 de 6 |
| Pecas sem suplente | 2 | 0 |
| Incidentes com dono achado em 15 min | 1 de 3 | 3 de 3 |
| Revisoes trimestrais da matriz | 0 | 1 |

## Decisoes e tradeoffs

1. **Formato Backstage mesmo sem Backstage rodando.** O `catalog-info.yaml` e padrao aberto e importa direto quando o portal existir; ate la, uma leitura simples gera a planilha espelho. Custo: campo a mais hoje, migracao zero amanha.
2. **Dono e pessoa, suplente obrigatorio.** Time nao e dono, pessoa e. Sem suplente a ferias vira incidente. Custo: conversa desconfortavel de designar nomes, ganho de clareza total.
3. **Matriz simples, sem RACI burocratico.** Colunas: peca, dono, suplente, responde por, escala para. RACI completo ninguem mantem; simples de verdade sobrevive.
4. **Roda com revezamento semanal.** Um nome por semana responde primeiro, com regra de escala em 15 minutos. Evita heroi fixo e distribui conhecimento.

## Impacto no negocio

Com dono declarado por peca, incidente deixa de ser broadcast no chat e vira chamada direta: quem responde, quem cobre ferias e para quem escalar ficam visiveis em uma pagina. Isso encurta o tempo de resposta de madrugada, protege a operacao de trafego em periodo critico e tira o conhecimento da cabeca de uma pessoa so, que e o risco mais caro de um time pequeno.

## Referencias

- Curso: Agile Planning for Software Products, University of Alberta (Coursera): https://www.coursera.org/learn/agile-planning-for-software-products
- Video: "Team Topologies, organizacao para fluxo rapido de valor", Matthew Skelton (YouTube)
- Doc: Backstage Software Catalog, entidades e ownership: https://backstage.io/docs/features/software-catalog/
- Doc: Team Topologies, padroes de times e ownership: https://teamtopologies.com/
