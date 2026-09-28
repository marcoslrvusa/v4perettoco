# A2 | LGPD em pipelines de dados: minimizacao, anonimizacao e base legal

| Campo | Valor |
|-------|-------|
| Area | Automacao & Infraestrutura |
| Unidade | FV Marketing / V4 Company |
| Autor | Marcos Luciano |
| Data | Setembro 2026 |
| Status | Entregue (desenvolvido, homologacao pendente) |

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

Pipelines de marketing (captura de leads, enriquecimento, sync com CRM e relatorios) carregam CPF, e-mail, telefone e saude de segmentacao sem mapa de base legal, sem minimizacao e sem anonimizar nada antes de agregar. Isso viola o principio da necessidade (art. 6, III), expoe dado sensivel (art. 11) e deixa o encarregado sem resposta pronta para pedido de titular (art. 18) ou fiscalizacao da ANPD.

## Arquitetura Resumida

```
[fonte: form, ads, planilha]
  -> 1. catalogo de campos (pessoal, sensivel, anonimizado)
  -> 2. gate de base legal por campo (art. 7: so entra com hipotese)
  -> 3. minimizacao (corta o que nao serve a finalidade)
  -> 4. anonimizacao/pseudonimizacao antes de agregar (anonimizacao.py)
  -> 5. registro da operacao + retencao com prazo e descarte
```

O `anonimizacao.py` implementa a etapa 4 (hash com salt, generalizacao, supressao, k-anonimato basico) e o checklist amarra as demais.

## Proximos Passos

1. Mapear base legal dos 3 pipelines ativos (leads pagos, CRM, relatorios) com os donos.
2. Publicar tabela de retencao (prazo por base + rotina de descarte) e validar com o encarregado.
3. Exigir RIPD resumido antes de qualquer pipeline novo com dado sensivel ou grande volume.

## Metricas de Sucesso

| Metrica | Atual | Meta |
|---------|-------|------|
| Campos pessoais com base legal mapeada | 0% (levantamento iniciado nesta PDI) | 100% dos 3 pipelines (meta) |
| Pipelines com etapa de anonimizacao antes de agregar | 0 de 3 | 3 de 3 (meta) |
| Prazo de resposta a pedido de titular (DSAR) | sem rotina | ate 15 dias (meta) |

## Decisoes e tradeoffs

1. Anonimizar por processo baseado em risco, nao por tecnica unica: segue o entendimento da ANPD de que nenhuma tecnica sozinha garante irreversibilidade; custa mais analise, mas sustenta juridicamente o art. 12.
2. Pseudonimizar no operacional e anonimizar no analitico: o pipeline diario mantem chave separada sob controle (art. 13, paragrafo 4), relatorios agregados usam dado anonimizado sem chave; dois fluxos em vez de um, com garantias diferentes.
3. Minimizar na entrada, nao na saida: campo sem finalidade declarada nem entra no pipeline; reduz retrabalho de expurgo, mas exige convencer o time a abrir mao de "coletar por precaucao".
4. Hash com salt secreto em vez de hash puro: impede reidentificacao por tabela arco-iris; cria um segredo novo para custodiar (ver atividade 3).
5. k-anonimato minimo de 5 em agregados publicados: bloqueia publicacao de segmento pequeno que identificaria alguem; alguns cortes de relatorio deixam de existir.

## Impacto no negocio

Pipeline com base legal mapeada, dado minimo e anonimizado antes de agregar transforma LGPD de risco de multa em rotina operacional: campanhas continuam rodando com os mesmos insumos uteis, o encarregado responde titular e ANPD com evidencias, e a empresa evita o cenario mais caro, que e descobrir o excesso de dados durante um incidente.

## Referencias

- Curso: Fundamentos da Lei Geral de Protecao de Dados (LGPD) (Enap, Escola Virtual Gov). https://www.escolavirtual.gov.br/curso/603
- Video: Canal oficial da ANPD no YouTube, serie 1 Minuto para Protecao de Dados (Autoridade Nacional de Protecao de Dados, YouTube). https://www.youtube.com/@anpdgov/streams
- Doc oficial: Lei 13.709/2018, LGPD, texto compilado (Presidencia da Republica). https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm
- Doc oficial: Portal da Autoridade Nacional de Protecao de Dados, ANPD. https://www.gov.br/anpd/pt-br
