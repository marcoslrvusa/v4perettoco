# Deck PDI | A2 LGPD em pipelines de dados

## Slide 1: Tese
Pipeline de marketing carrega dado pessoal sem base legal, sem minimização e sem anonimizar. LGPD vira rotina com catálogo, gate de base legal e anonimização antes de agregar.

## Slide 2: Contexto
Captura de leads, enriquecimento, sync com CRM e relatórios movem CPF, e-mail, telefone e sinais de segmentação todos os dias.

## Slide 3: Problema
Campo sem base legal viola necessidade (art. 6, III); sensível sem hipótese estrita viola art. 11; sem rotina de titular (art. 18) nem registro (art. 37), fiscalização e incidente pegam a empresa sem resposta.

## Slide 4: Mapa da lei aplicado
Art. 7 em tabela prática (consentimento, contrato, obrigação legal, legítimo interesse, estudos); art. 11 para sensível; art. 12 para anonimizado; art. 13 para pseudônimo; art. 15 a 18 para retenção e direitos.

## Slide 5: Solução em 5 etapas
Catálogo de campos, gate de base legal, minimização na entrada, anonimização antes de agregar, registro com prazo e descarte.

## Slide 6: Standard entregue
`STANDARD-LGPD-PIPELINE.md`: catálogo obrigatório de 6 itens, mapa de base legal, minimização, anonimização como processo baseado em risco, DSAR em até 15 dias.

## Slide 7: Código entregue
`anonimizacao.py` em Python puro: pseudônimo com salt, faixa etária, prefixo de CEP, supressão e checagem de k-anonimato mínimo 5. Self-test passando.

## Slide 8: Demo
Rodar o script na base de teste: e-mail vira pseudônimo, idade vira faixa, k calculado ao vivo; mostrar o checklist aplicado a um pipeline real.

## Slide 9: Métricas
Campos com base legal: atual 0% para 100% dos 3 pipelines (meta). Pipelines com anonimização: atual 0 de 3 para 3 de 3 (meta). DSAR: sem rotina para até 15 dias (meta).

## Slide 10: Tradeoffs assumidos
Risco calculado em vez de técnica única (mais análise, amparo jurídico); dois fluxos (pseudônimo no operacional, anonimizado no analítico); minimizar na entrada cobra dizer não a coleta por precaução.

## Slide 11: Próximos passos
Mapear os 3 pipelines com os donos; publicar tabela de retenção com o encarregado; RIPD resumido antes de pipeline novo com sensível ou volume alto.

## Slide 12: Impacto
Campanhas com os mesmos insumos úteis, encarregado com evidências para titular e ANPD, e fim do cenário mais caro: descobrir excesso de dados durante um incidente.
