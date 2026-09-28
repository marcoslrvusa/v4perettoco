# Atividade 2: Ergonomia e Pausas no Trabalho Remoto

| Campo | Valor |
|-------|-------|
| Área | Automação & Infraestrutura |
| Unidade | FV Marketing / V4 Company |
| Autor | Marcos Luciano |
| Data | Setembro 2026 |
| Status | Entregue (desenvolvido, homologação pendente) |

## Entregas desta PDI

```
atividade-2/
├── README.md
├── 1-standards/
│   ├── 01-padrao-estacao-trabalho.md
│   └── 02-protocolo-pausas-movimento.md
├── 2-implementacao/
│   ├── checklist-ergonomico.md
│   └── plano-pausas-diario.md
└── 7-apresentacao/
    ├── DECK-PDI.md
    ├── DEMO-SCRIPT.md
    ├── ROTEIRO-DOMINIO.md
    ├── pdi-saude-ergonomia-pausas-a2.html
    ├── pdi-saude-ergonomia-pausas-a2.docx
    ├── pdi-saude-ergonomia-pausas-a2.pdf
    └── gerar-docx.py
```

## Problema Resolvido

Trabalho remoto prolongado em setup improvisado gera dor cervical, lombar e fadiga visual, além de jornadas sem pausa que derrubam a atenção à tarde. Esta atividade define um padrão mínimo de estação de trabalho de baixo custo e um protocolo de micro-pausas e movimento que cabe dentro da jornada real, sem depender de acadêmia ou equipamento caro.

## Arquitetura Resumida

```
AUDITAR setup atual (checklist de 20 itens)
  -> CORRIGIR o essencial (altura de tela, apoio lombar, luz)
    -> AGENDAR pausas (micro 2 min/hora, movimento 10 min/turno)
      -> SINALIZAR (timer visível, regra 20-20-20 para os olhos)
        -> REAVALIAR dor e energia a cada 2 semanas
```

## Próximos Passos

1. Aplicar o checklist na estação atual e corrigir os 3 itens de maior impacto na primeira semana.
2. Rodar o plano de pausas por 10 dias úteis e anotar dor (escala 0 a 10) e energia à tarde.
3. Fotografar antes e depois do setup e anexar ao registro para comparação.

## Métricas de Sucesso

| Métrica | Atual | Meta |
|---------|-------|------|
| Itens conformes no checklist (20 itens) | sem dado | 17 de 20 (meta) |
| Nível de dor cervical/lombar ao fim do dia (0 a 10) | sem dado | 3 ou menos (meta) |
| Pausas de movimento cumpridas por dia | 0 | 4 (meta) |

## Decisões e tradeoffs

1. Padrão mínimo de baixo custo em vez de setup ideal: eleva a adesão imediata. O custo é não atingir ergonomia perfeita de imediato.
2. Micro-pausas de 2 minutos por hora em vez de uma pausa longa: mantém fluxo de trabalho e reduz rigidez. O custo é precisar de timer e disciplina.
3. Regra 20-20-20 para os olhos (a cada 20 min, olhar 20 segundos a 6 metros): simples e memorizável. O custo é parecer simplória perto de soluções de software.
4. Caminhada curta em vez de treino estruturado no expediente: cabe em qualquer agenda. O custo é não substituir exercício real, só complementar.
5. Autoavaliação de dor quinzenal em vez de avaliação profissional: dá autonomia e custo zero. O custo é não diagnosticar nada, só sinalizar piora para buscar ajuda.

## Impacto no negócio

Dor crônica e fadiga derrubam velocidade de entrega e aumentam afastamentos. Um setup minimamente correto e pausas reais preservam horas produtivas por semana por pessoa, com investimento próximo de zero, o que protege capacidade da equipe e reduz risco de passivo de saúde ocupacional.

## Referências

- Curso: Catálogo de cursos de ergonomia, Udemy (busca verificada): https://www.udemy.com/courses/search/?q=ergonomia
- Vídeo: Daniel Levitin, How to stay calm when you know you'll be stressed, TED: https://www.youtube.com/watch?v=8jPQjjsBbIc
- Doc: OMS, ficha sobre condições musculoesqueléticas (1,71 bilhão de pessoas afetadas): https://www.who.int/news-room/fact-sheets/detail/musculoskeletal-conditions
- Doc: HSE Reino Unido, central de distúrbios musculoesqueléticos no trabalho: https://www.hse.gov.uk/msd/
