# Atividade 4: Rituais de Time Facilitados

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
│   ├── STD-01-facilitacao-rituais.md
│   └── STD-02-anti-patterns.md
├── 2-implementacao/
│   ├── TPL-roteiro-retro.md
│   └── TPL-ata-rituais.md
└── 7-apresentacao/
    ├── DECK-PDI.md
    ├── DEMO-SCRIPT.md
    ├── ROTEIRO-DOMINIO.md
    ├── pdi-lideranca-mentoria-codereview-a4.html
    ├── pdi-lideranca-mentoria-codereview-a4.docx
    ├── pdi-lideranca-mentoria-codereview-a4.pdf
    └── gerar-docx.py
```

## Problema Resolvido

Os rituais do time existem no calendário mas não funcionam: planning vira leitura de backlog sem meta da sprint, review vira demo para ninguém e retrospectiva vira desabafo sem dono nem prazo, com as mesmas reclamações repetidas há meses. Reunião sem facilitação consome hora cara de todo mundo e devolve zero decisão. Esta atividade entrega formato facilitado para os 3 rituais (objetivo, timebox, entradas, passo a passo, saídas obrigatórias), roteiro de retro pronto para rodar e lista de anti-patterns com correção prática.

## Arquitetura Resumida

```
Ciclo de sprint de 2 semanas:
  -> Planning (até 2h): meta da sprint + backlog fatiado + capacidade real = plano assinado
  -> Review (45 min): demo do incremento + feedback de stakeholder = backlog repriorizado
  -> Retrospectiva (60 min): fatos + votação + 1 a 3 ações com dono e prazo = melhoria rastreada
  -> Regra transversal: sem ata com dono e prazo, o ritual não aconteceu
  -> Facilitação roda entre membros; líder participa como membro, não como juiz
```

## Próximos Passos

1. Rodar os 3 rituais no formato novo já na próxima sprint, com facilitação revezada.
2. Publicar atas no canal do time em até 24h após cada ritual.
3. Cobrar as ações da retro na planning seguinte, sem exceção.

## Métricas de Sucesso

| Métrica | Atual | Meta |
|---------|-------|------|
| Rituais com ata, dono e prazo publicados | 10% | 100% (meta) |
| Ações de retro concluídas na sprint seguinte | 25% | 80% (meta) |
| Sprints que batem a meta planejada | 40% | 75% (meta) |
| Tempo total de rituais por sprint | 6h difusas | 3h45 focadas (meta) |

## Decisões e tradeoffs

1. **Timebox curto e rígido (planning 2h, review 45 min, retro 60 min).** Limite força preparo prévio; o risco de cortar discussão boa é tratado com estacionamento e continuação assíncrona.
2. **Máximo 3 ações por retro.** Poucas ações cumpridas valem mais que 10 esquecidas; o tradeoff é deixar tema relevante para a próxima retro, registrado no backlog de melhoria.
3. **Facilitação revezada, não fixa no líder.** Distribui ownership e evita viés; o custo é qualidade irregular no início, mitigada pelo roteiro passo a passo.
4. **Ata em 24h como definição de pronto do ritual.** Sem registro não há cobrança; o ônus pequeno de escrita garante rastreabilidade total.

## Impacto no negócio

Ritual que decide de verdade transforma hora de reunião em previsibilidade: a operação promete prazo com base em capacidade real, mostra progresso a stakeholder antes do problema e corrige processo a cada 2 semanas. Isso reduz atraso em entrega de cliente, corta reunião redundante e cria um time que melhora sozinho, sem depender do líder puxar tudo.

## Referências

- Curso: Leading Teams, University of Michigan (Coursera): https://www.coursera.org/learn/leading-teams
- Vídeo: Daniel Pink, The puzzle of motivation (TEDGlobal 2009): https://www.ted.com/talks/dan_pink_the_puzzle_of_motivation
- Doc oficial: Atlassian, Agile retrospectives: https://www.atlassian.com/agile/scrum/retrospectives
- Doc oficial: Atlassian, Sprint planning: https://www.atlassian.com/agile/scrum/sprint-planning
