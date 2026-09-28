# Atividade 4: Aprendizado Contínuo sem Burnout

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
│   ├── 01-rotina-estudo-sustentavel.md
│   └── 02-curadoria-descanso-planejado.md
├── 2-implementacao/
│   ├── plano-estudos-trimestral.md
│   └── diario-aprendizado-energia.md
└── 7-apresentacao/
    ├── DECK-PDI.md
    ├── DEMO-SCRIPT.md
    ├── ROTEIRO-DOMINIO.md
    ├── pdi-saude-aprendizado-continuo-a4.html
    ├── pdi-saude-aprendizado-continuo-a4.docx
    ├── pdi-saude-aprendizado-continuo-a4.pdf
    └── gerar-docx.py
```

## Problema Resolvido

Estudar tudo ao mesmo tempo, de madrugada e sem pausa, gera abandono em 3 semanas e culpa em 4. Esta atividade define uma rotina de estudo de 4 horas semanais protegidas, um funil de curadoria que limita a 2 frentes de aprendizado por trimestre e trata descanso como parte do plano, com semana de recuperação a cada 6 semanas.

## Arquitetura Resumida

```
ESCOLHER 2 frentes por trimestre (1 técnica, 1 comportamental)
  -> AGENDAR 4 h semanais fixas (2 blocos de 2 h ou 4 de 1 h)
    -> ESTUDAR com técnica ativa (recordação e prática, não releitura)
      -> REGISTRAR (diário: o que aprendi, energia, próxima ação)
        -> RECUPERAR (semana leve a cada 6 semanas, zero conteúdo novo)
```

## Próximos Passos

1. Preencher o plano trimestral escolhendo as 2 frentes e as 4 horas fixas.
2. Rodar 6 semanas e revisar: conclusão de módulos, energia e abandono.
3. Executar a primeira semana de recuperação e avaliar retenção do que foi estudado.

## Métricas de Sucesso

| Métrica | Atual | Meta |
|---------|-------|------|
| Horas de estudo por semana | 0 | 4 (meta) |
| Frentes simultâneas de estudo | sem dado | 2 no máximo (meta) |
| Taxa de conclusão do plano trimestral | sem dado | 70% (meta) |

## Decisões e tradeoffs

1. 4 horas semanais em vez de 10: ritmo que sobrevive a semana de pico. O custo é progresso mais lento por mês.
2. Máximo de 2 frentes por trimestre: profundidade em vez de coleção de cursos. O custo é deixar temas interessantes na fila.
3. Recordação ativa em vez de releitura e vídeo passivo: retenção maior por hora. O custo é esforço mental maior por sessão.
4. Semana de recuperação a cada 6 semanas: consolida e evita abandono. O custo é uma semana sem conteúdo novo no cronograma.
5. Diário de 5 linhas em vez de resumo longo: registro que realmente acontece. O custo é menor detalhe por sessão.

## Impacto no negócio

Profissional de automação desatualizado vira gargalo técnico em meses. Rotina de estudo sustentável mantém o time atualizado em ferramentas e práticas sem gerar afastamento por esgotamento, o que preserva senioridade, reduz turnover e mantém a unidade competitiva em martech e infra.

## Referências

- Curso: Mindshift (Barbara Oakley, Terrence Sejnowski), Coursera: https://www.coursera.org/learn/mindshift
- Vídeo: Angela Lee Duckworth, Grit: the power of passion and perseverance, TED: https://www.youtube.com/watch?v=H14bBuluwB8
- Doc: NIMH EUA, guia de autocuidado em saúde mental: https://www.nimh.nih.gov/health/topics/caring-for-your-mental-health
- Doc: OMS, ficha sobre saúde mental no trabalho: https://www.who.int/news-room/fact-sheets/detail/mental-health-at-work
