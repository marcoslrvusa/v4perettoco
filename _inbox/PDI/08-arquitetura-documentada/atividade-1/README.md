# Atividade 1: Modelo C4 na Prática Aplicado ao Orquestrador de Automação V4

| Campo | Valor |
|-------|-------|
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
│   ├── 01-guia-c4-aplicado.md
│   └── 02-diagramas-sistema-automacao.md
├── 2-implementacao/
│   ├── 01-workspace-c4.dsl
│   ├── 02-exemplo-mermaid-c4.md
│   └── 03-checklist-revisao-c4.md
└── 7-apresentacao/
    ├── DECK-PDI.md
    ├── DEMO-SCRIPT.md
    ├── ROTEIRO-DOMINIO.md
    ├── pdi-arquitetura-documentada-a1.html
    ├── pdi-arquitetura-documentada-a1.docx
    ├── pdi-arquitetura-documentada-a1.pdf
    └── gerar-docx.py
```

## Problema Resolvido

Ninguém sabia desenhar o orquestrador de automação da mesma forma: cada pessoa explicava com um diagrama diferente, o onboarding de um operador novo levava 3 dias e qualquer incidente virava adivinhação sobre qual peça falhou. Esta atividade fixa os 4 níveis do C4 sobre o sistema real (n8n + workers Python + Supabase + painel Next.js) e entrega fonte versionável em Structurizr DSL mais espelho em Mermaid.

## Arquitetura Resumida

```
[Operador] [Gestor] --> [Orquestrador V4] --> [Meta Ads API] [Gmail API]
                            |
      +----------+----------+----------+----------+
      |                     |                     |
 [n8n :5678]      [Workers Python :8000]   [Painel Next.js :3000]
      |                     |
      +------> [Supabase Postgres] <------+
```

## Próximos Passos

1. Subir `workspace.dsl` no Structurizr Lite e publicar link interno.
2. Adicionar o diagrama de contexto no onboarding de operadores.
3. Revisar diagramas a cada mudança de container (dono: Marcos Luciano).

## Métricas de Sucesso

| Métrica | Atual | Meta |
|---------|-------|------|
| Sistemas com diagrama de contexto | 1 | 3 |
| Containers documentados do orquestrador | 4 de 4 | 4 de 4 |
| Diagramas desatualizados há +30 dias | 0 | 0 |
| Tempo de onboarding de operador | 3 dias | 1 dia |

## Decisões e tradeoffs

1. **Structurizr DSL como fonte, Mermaid como espelho.** DSL garante um modelo único que gera todos os níveis; Mermaid garante leitura no repo sem ferramenta extra. Custo: manter os dois sincronizados.
2. **Nível 3 só para o n8n.** Documentar componentes dos 4 containers dobraria o esforço; o n8n concentra 80 por cento das mudanças, então foi o escolhido.
3. **Nível 4 só para o retry de coleta.** Código muda rápido e apodrece no doc; fixamos só a função onde bug custa verba de tráfego.
4. **Sem deploy diagram agora.** Infra ainda e uma VPS única sem multi ambiente; o diagrama de deploy entraria genérico e falso. Fica para quando houver segundo ambiente.

## Impacto no negócio

Com o C4 aplicado ao sistema real, o time de automação passa a responder em minutos (e não em dias) as perguntas que hoje travam operação: qual peça quebrou, quem depende dela e onde mexer sem quebrar o resto. Isso reduz incidente em coleta de verba de tráfego e acelera a entrada de novos operadores, que aprendem o sistema por um mapa único em vez de perguntar no chat.

## Referências

- Curso: Software Design and Architecture Specialization, University of Alberta (Coursera): https://www.coursera.org/specializations/software-design-architecture
- Vídeo: "Visualising Software Architecture with the C4 Model", Simon Brown, Agile on the Beach 2019 (YouTube)
- Doc: Site oficial do C4 Model: https://c4model.com/
- Doc: Structurizr, ferramenta de referência do C4: https://structurizr.com/
