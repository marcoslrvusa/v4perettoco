# Atividade 3: Documentacao como Codigo, Mermaid e Diagramas Versionados

| Campo | Valor |
|-------|-------|
| Área | Automação & Infraestrutura |
| Unidade | FV Marketing / V4 Company |
| Autor | Marcos Luciano |
| Data | Setembro 2026 |
| Status | Entregue (desenvolvido) |

## Entregas desta PDI

```
atividade-3/
├── README.md
├── 1-standards/
│   ├── 01-docs-como-codigo-fundamentos.md
│   └── 02-mermaid-guia-rapido.md
├── 2-implementacao/
│   ├── 01-exemplo-fluxo-coleta.md
│   ├── 02-exemplo-sequencia-webhook.md
│   └── 03-checklist-docs-vivos.md
└── 7-apresentacao/
    ├── DECK-PDI.md
    ├── DEMO-SCRIPT.md
    ├── ROTEIRO-DOMINIO.md
    ├── pdi-arquitetura-documentada-a3.html
    ├── pdi-arquitetura-documentada-a3.docx
    ├── pdi-arquitetura-documentada-a3.pdf
    └── gerar-docx.py
```

## Problema Resolvido

Diagramas viviam em arquivos de desenho soltos, fora do git, impossiveis de revisar em PR e sempre desatualizados. Ninguem sabia qual era a versao certa do fluxo de coleta. Esta atividade move os diagramas para dentro do repo como texto Mermaid: versionados, revisados em PR e renderizados no GitHub sem ferramenta extra, com dois exemplos reais do orquestrador.

## Arquitetura Resumida

```
[Editar .md com Mermaid] --> [PR com diff legivel] --> [CI valida sintaxe]
        |                                                    |
        +------< [Renderiza no GitHub/GitLab] <--------------+
```

## Proximos Passos

1. Converter os 3 fluxos n8n mais criticos em Mermaid no repo.
2. Ligar validacao de sintaxe Mermaid no CI.
3. Apagar arquivos de desenho soltos apos migracao (dono: Marcos Luciano).

## Metricas de Sucesso

| Metrica | Atual | Meta |
|---------|-------|------|
| Diagramas vivos no repo (Mermaid) | 4 | 10 |
| Diagramas soltos fora do git | 6 | 0 |
| PRs com diagrama revisado no trimestre | 0 | 5 |
| Diagramas quebrados (sintaxe invalida) | 0 | 0 |

## Decisoes e tradeoffs

1. **Mermaid em vez de PlantUML.** Mermaid renderiza nativo no GitHub e GitLab; PlantUML exige servidor extra. Custo: menos tipos de diagrama exoticos, suficiente para nosso uso.
2. **Diagrama mora junto do codigo que descreve.** Fluxo de coleta documentado ao lado do worker, nao em wiki separada. Custo: exige disciplina no PR, ganha frescor.
3. **CI valida sintaxe, nao semantica.** O pipeline quebra em bloco Mermaid invalido, mas nao julga se o desenho esta certo. Certo ou errado e papel do revisor com o checklist.
4. **C4 complexo fica no DSL da atividade 1.** Mermaid cobre fluxo, sequencia e contexto simples; C4 detalhado continua no Structurizr. Cada ferramenta no seu quadrado.

## Impacto no negocio

Com diagramas como codigo, a documentacao anda na mesma velocidade do sistema: cada mudanca de fluxo chega com seu desenho atualizado no mesmo PR, revisado pela mesma pessoa. Acaba a era do diagrama bonito e mentiroso em arquivo solto, e qualquer operador consulta a versao certa direto no repo, sem pedir print no chat.

## Referencias

- Curso: Version Control with Git, Atlassian (Coursera): https://www.coursera.org/learn/version-control-with-git
- Video: "Mermaid Live Editor e diagramas como codigo", canal oficial Mermaid (YouTube)
- Doc: Site oficial do Mermaid: https://mermaid.js.org/
- Doc: Sintaxe C4 no Mermaid: https://mermaid.js.org/syntax/c4.html
