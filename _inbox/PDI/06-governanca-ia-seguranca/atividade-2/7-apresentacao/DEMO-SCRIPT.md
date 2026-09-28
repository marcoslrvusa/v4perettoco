# Demo Script | A2 LGPD em pipelines

Duracao: 10 min. Pre-requisito: `python3` disponivel e `anonimizacao.py` na pasta `2-implementacao/`.

1. Abra com a tese (30s): pipeline carrega pessoal sem base legal nem minimizacao; mostre as 5 etapas do README.
2. Rode o self-test: `python3 ../2-implementacao/anonimizacao.py`. Destaque e-mail virando pseudonimo e k calculado.
3. Mostre a linha do exemplo anonimizado: sem `@`, idade em faixa, CEP por prefixo.
4. Force a discussao de risco: pergunte o que acontece se k viesse abaixo de 5; resposta: suprimir ou generalizar mais, o script falha de proposito.
5. Mostre o mapa de base legal do standard aplicado a captura de leads real da operacao.
6. Mostre o checklist: marque catalogo, minimizacao e DSAR para o pipeline de leads pagos.
7. Aponte art. 12 e o processo baseado em risco: tecnica sozinha nao basta, documentacao sim.
8. Feche com metricas: 0% para 100% de campos mapeados (meta), 0 de 3 para 3 de 3 pipelines anonimizados (meta), DSAR em ate 15 dias (meta).
9. Pergunta de reserva: "hash nao e anonimizar?" Resposta: hash sem salt e reversivel por tabela; com salt sob controle e pseudonimo, ainda dado pessoal, por isso o analitico usa agregado com k minimo.
