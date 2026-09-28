# A2 | LGPD em pipelines de dados: minimização, anonimização e base legal

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
│   └── STANDARD-LGPD-PIPELINE.md
├── 2-implementacao/
│   ├── anonimizacao.py
│   └── CHECKLIST-LGPD-PIPELINE.md
└── 7-apresentacao/
    ├── DECK-PDI.md
    ├── DEMO-SCRIPT.md
    ├── ROTEIRO-DOMINIO.md
    ├── pdi-governanca-ia-seguranca-a2.html
    ├── pdi-governanca-ia-seguranca-a2.docx
    ├── pdi-governanca-ia-seguranca-a2.pdf
    └── gerar-docx.py
```

## Problema Resolvido

Pipelines de marketing (captura de leads, enriquecimento, sync com CRM e relatórios) carregam CPF, e-mail, telefone e saúde de segmentação sem mapa de base legal, sem minimização e sem anonimizar nada antes de agregar. Isso viola o princípio da necessidade (art. 6, III), expõe dado sensível (art. 11) e deixa o encarregado sem resposta pronta para pedido de titular (art. 18) ou fiscalização da ANPD.

## Arquitetura Resumida

```
[fonte: form, ads, planilha]
  -> 1. catálogo de campos (pessoal, sensível, anonimizado)
  -> 2. gate de base legal por campo (art. 7: só entra com hipótese)
  -> 3. minimização (corta o que não serve a finalidade)
  -> 4. anonimizacao/pseudonimizacao antes de agregar (anonimizacao.py)
  -> 5. registro da operação + retenção com prazo e descarte
```

O `anonimizacao.py` implementa a etapa 4 (hash com salt, generalização, supressão, k-anonimato básico) e o checklist amarra as demais.

## Próximos Passos

1. Mapear base legal dos 3 pipelines ativos (leads pagos, CRM, relatórios) com os donos.
2. Publicar tabela de retenção (prazo por base + rotina de descarte) e validar com o encarregado.
3. Exigir RIPD resumido antes de qualquer pipeline novo com dado sensível ou grande volume.

## Métricas de Sucesso

| Métrica | Atual | Meta |
|---------|-------|------|
| Campos pessoais com base legal mapeada | 0% (levantamento iniciado nesta PDI) | 100% dos 3 pipelines (meta) |
| Pipelines com etapa de anonimização antes de agregar | 0 de 3 | 3 de 3 (meta) |
| Prazo de resposta a pedido de titular (DSAR) | sem rotina | até 15 dias (meta) |

## Decisões e tradeoffs

1. Anonimizar por processo baseado em risco, não por técnica única: segue o entendimento da ANPD de que nenhuma técnica sozinha garante irreversibilidade; custa mais análise, mas sustenta juridicamente o art. 12.
2. Pseudonimizar no operacional e anonimizar no analítico: o pipeline diário mantém chave separada sob controle (art. 13, parágrafo 4), relatórios agregados usam dado anonimizado sem chave; dois fluxos em vez de um, com garantias diferentes.
3. Minimizar na entrada, não na saída: campo sem finalidade declarada nem entra no pipeline; reduz retrabalho de expurgo, mas exige convencer o time a abrir mão de "coletar por precaução".
4. Hash com salt secreto em vez de hash puro: impede reidentificação por tabela arco-íris; cria um segredo novo para custodiar (ver atividade 3).
5. k-anonimato mínimo de 5 em agregados publicados: bloqueia publicação de segmento pequeno que identificaria alguém; alguns cortes de relatório deixam de existir.

## Impacto no negócio

Pipeline com base legal mapeada, dado mínimo e anonimizado antes de agregar transforma LGPD de risco de multa em rotina operacional: campanhas continuam rodando com os mesmos insumos úteis, o encarregado responde titular e ANPD com evidências, e a empresa evita o cenário mais caro, que é descobrir o excesso de dados durante um incidente.

## Referências

- Curso: Fundamentos da Lei Geral de Proteção de Dados (LGPD) (Enap, Escola Virtual Gov). https://www.escolavirtual.gov.br/curso/603
- Vídeo: Canal oficial da ANPD no YouTube, série 1 Minuto para Proteção de Dados (Autoridade Nacional de Proteção de Dados, YouTube). https://www.youtube.com/@anpdgov/streams
- Doc oficial: Lei 13.709/2018, LGPD, texto compilado (Presidência da República). https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm
- Doc oficial: Portal da Autoridade Nacional de Proteção de Dados, ANPD. https://www.gov.br/anpd/pt-br
