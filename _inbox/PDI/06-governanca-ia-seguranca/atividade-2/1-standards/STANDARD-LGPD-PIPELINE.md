# STANDARD-LGPD-PIPELINE | Minimizacao, anonimizacao e base legal

Versao 1.0, Setembro 2026. Escopo: pipelines que coletam, enriquecem, sincronizam ou agregam dados pessoais na operacao (leads pagos, CRM, relatorios).

## 1. Catalogo de campos (obrigatorio por pipeline)

Todo pipeline declara por campo: nome, categoria (pessoal comum, sensivel art. 11, anonimizado), finalidade especifica, base legal (art. 7), prazo de retencao e destino. Campo sem esses 6 itens nao entra em producao.

## 2. Base legal: mapa pratico (art. 7)

| Situacao da operacao | Hipotese usual | Exemplo |
|----------------------|----------------|---------|
| Form com aceite claro para contato comercial | I consentimento | "Quero receber proposta" marcado pelo titular |
| Contrato ou pre-contrato a pedido do titular | V execucao de contrato | Proposta e onboarding de cliente |
| Obrigacao fiscal ou trabalhista | II obrigacao legal | Nota fiscal, folha |
| Marketing para base propria com opt-out e teste documentado | IX legitimo interesse | Oferta de servico analogo a cliente ativo |
| Estudo agregado sem identificar ninguem | IV estudos por orgao de pesquisa, com anonimizacao sempre que possivel | Relatorio estatistico interno |

Legitimo interesse exige teste de proporcionalidade escrito e canal de oposicao (art. 10). Dado sensivel so com as hipoteses estritas do art. 11; saude para vantagem economica e vedada (art. 11, paragrafos 4 e 5).

## 3. Minimizacao (art. 6, III e principio da necessidade)

Coleta o minimo necessario a finalidade declarada. Regras: sem "campo reserva"; CPF so com justificativa escrita; documento de identidade nunca em form de lead; resposta de API enriquecida e filtrada na borda (descarta o excedente antes de persistir).

## 4. Anonimizacao como processo baseado em risco (art. 12)

Anonimizacao nao e uma funcao, e um processo: (a) definir o risco aceitavel de reidentificacao para o uso; (b) aplicar o conjunto de tecnicas (supressao, generalizacao, hash com salt, agregacao com k minimo); (c) testar reidentificacao com esforco razoavel; (d) documentar e revisar a cada mudanca de fonte. Pseudonimo com chave separada sob controle continua dado pessoal (art. 13, paragrafo 4) e serve ao operacional; o analitico publicado usa anonimizado sem chave.

## 5. Direitos do titular e retencao

Pedido de confirmacao, acesso, correcao, anonimizacao, bloqueio, eliminacao ou portabilidade (art. 18) responde em ate 15 dias com rotina escrita e responsavel nomeado. Dado pessoal some apos o termino do tratamento (art. 15 e 16); cada base declara prazo e rotina de descarte. Registro das operacoes mantido para prestar contas (art. 37) e RIPD elaborado quando houver risco relevante (art. 38).
