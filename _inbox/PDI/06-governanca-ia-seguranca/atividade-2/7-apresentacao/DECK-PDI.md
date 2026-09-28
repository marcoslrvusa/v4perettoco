# Deck PDI | A2 LGPD em pipelines de dados

## Slide 1: Tese
Pipeline de marketing carrega dado pessoal sem base legal, sem minimizacao e sem anonimizar. LGPD vira rotina com catalogo, gate de base legal e anonimizacao antes de agregar.

## Slide 2: Contexto
Captura de leads, enriquecimento, sync com CRM e relatorios movem CPF, e-mail, telefone e sinais de segmentacao todos os dias.

## Slide 3: Problema
Campo sem base legal viola necessidade (art. 6, III); sensivel sem hipotese estrita viola art. 11; sem rotina de titular (art. 18) nem registro (art. 37), fiscalizacao e incidente pegam a empresa sem resposta.

## Slide 4: Mapa da lei aplicado
Art. 7 em tabela pratica (consentimento, contrato, obrigacao legal, legitimo interesse, estudos); art. 11 para sensivel; art. 12 para anonimizado; art. 13 para pseudonimo; art. 15 a 18 para retencao e direitos.

## Slide 5: Solucao em 5 etapas
Catalogo de campos, gate de base legal, minimizacao na entrada, anonimizacao antes de agregar, registro com prazo e descarte.

## Slide 6: Standard entregue
`STANDARD-LGPD-PIPELINE.md`: catalogo obrigatorio de 6 itens, mapa de base legal, minimizacao, anonimizacao como processo baseado em risco, DSAR em ate 15 dias.

## Slide 7: Codigo entregue
`anonimizacao.py` em Python puro: pseudonimo com salt, faixa etaria, prefixo de CEP, supressao e checagem de k-anonimato minimo 5. Self-test passando.

## Slide 8: Demo
Rodar o script na base de teste: e-mail vira pseudonimo, idade vira faixa, k calculado ao vivo; mostrar o checklist aplicado a um pipeline real.

## Slide 9: Metricas
Campos com base legal: atual 0% para 100% dos 3 pipelines (meta). Pipelines com anonimizacao: atual 0 de 3 para 3 de 3 (meta). DSAR: sem rotina para ate 15 dias (meta).

## Slide 10: Tradeoffs assumidos
Risco calculado em vez de tecnica unica (mais analise, amparo juridico); dois fluxos (pseudonimo no operacional, anonimizado no analitico); minimizar na entrada cobra dizer nao a coleta por precaucao.

## Slide 11: Proximos passos
Mapear os 3 pipelines com os donos; publicar tabela de retencao com o encarregado; RIPD resumido antes de pipeline novo com sensivel ou volume alto.

## Slide 12: Impacto
Campanhas com os mesmos insumos uteis, encarregado com evidencias para titular e ANPD, e fim do cenario mais caro: descobrir excesso de dados durante um incidente.
