# STANDARD-LGPD-PIPELINE | Minimização, anonimização e base legal

Versão 1.0, Setembro 2026. Escopo: pipelines que coletam, enriquecem, sincronizam ou agregam dados pessoais na operação (leads pagos, CRM, relatórios).

## 1. Catálogo de campos (obrigatório por pipeline)

Todo pipeline declara por campo: nome, categoria (pessoal comum, sensível art. 11, anonimizado), finalidade específica, base legal (art. 7), prazo de retenção e destino. Campo sem esses 6 itens não entra em produção.

## 2. Base legal: mapa prático (art. 7)

| Situação da operação | Hipótese usual | Exemplo |
|----------------------|----------------|---------|
| Form com aceite claro para contato comercial | I consentimento | "Quero receber proposta" marcado pelo titular |
| Contrato ou pre-contrato a pedido do titular | V execução de contrato | Proposta e onboarding de cliente |
| Obrigação fiscal ou trabalhista | II obrigação legal | Nota fiscal, folha |
| Marketing para base própria com opt-out e teste documentado | IX legítimo interesse | Oferta de serviço análogo a cliente ativo |
| Estudo agregado sem identificar ninguém | IV estudos por órgão de pesquisa, com anonimização sempre que possível | Relatório estatístico interno |

Legítimo interesse exige teste de proporcionalidade escrito e canal de oposição (art. 10). Dado sensível só com as hipóteses estritas do art. 11; saúde para vantagem econômica e vedada (art. 11, parágrafos 4 e 5).

## 3. Minimização (art. 6, III e princípio da necessidade)

Coleta o mínimo necessário a finalidade declarada. Regras: sem "campo reserva"; CPF só com justificativa escrita; documento de identidade nunca em form de lead; resposta de API enriquecida e filtrada na borda (descarta o excedente antes de persistir).

## 4. Anonimização como processo baseado em risco (art. 12)

Anonimização não é uma função, é um processo: (a) definir o risco aceitável de reidentificação para o uso; (b) aplicar o conjunto de técnicas (supressão, generalização, hash com salt, agregação com k mínimo); (c) testar reidentificação com esforço razoável; (d) documentar e revisar a cada mudança de fonte. Pseudônimo com chave separada sob controle continua dado pessoal (art. 13, parágrafo 4) e serve ao operacional; o analítico publicado usa anonimizado sem chave.

## 5. Direitos do titular e retenção

Pedido de confirmação, acesso, correção, anonimização, bloqueio, eliminação ou portabilidade (art. 18) responde em até 15 dias com rotina escrita e responsável nomeado. Dado pessoal some após o término do tratamento (art. 15 e 16); cada base declara prazo e rotina de descarte. Registro das operações mantido para prestar contas (art. 37) e RIPD elaborado quando houver risco relevante (art. 38).
