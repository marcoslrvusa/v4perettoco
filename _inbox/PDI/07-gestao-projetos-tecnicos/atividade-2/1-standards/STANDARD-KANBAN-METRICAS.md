# STANDARD: Fluxo Kanban e Metricas

Area: Automacao & Infraestrutura | FV Marketing / V4 Company | Setembro 2026

## 1. Colunas e limites de WIP

| Coluna | O que entra | WIP maximo | Regra de saida |
|---|---|---|---|
| A Fazer | demanda refinada (passou no checklist da A1) | sem limite, ordenada | puxar so se Fazendo tem vaga |
| Fazendo | trabalho ativo | 2 por pessoa | 1 cartao por vez por pessoa, o resto espera |
| Revisao | validacao com operacao + deploy | 3 no total | revisor responde em ate 1 dia util |
| Pronto | entregue e validado | sem limite | registra data de conclusao e lead time |

WIP estourado = parar de puxar e ajudar a destravar o gargalo. Puxar com WIP cheio e proibido, inclusive para "coisa rapida".

## 2. Classes de servico

- **Padrao**: segue a fila. 80% dos cartoes.
- **Urgente**: fura a fila, max 1 por vez no quadro. Ex.: integracao quebrada travando campanha ativa.
- **Data fixa**: tem data externa real (ex.: relatorio para reuniao de diretoria). Marca a data no cartao.

Tudo marcado como urgente = nada e urgente. Quem marca o segundo urgente decide qual dos dois volta para padrao.

## 3. As 3 metricas (definicoes oficiais da area)

- **Lead time**: dias uteis entre o cartao entrar em Fazendo e chegar em Pronto. Mede velocidade de atravessamento.
- **Throughput**: cartoes concluidos por semana. Mede capacidade real de entrega.
- **WIP**: cartoes em Fazendo + Revisao na sexta-feira. Mede carga do sistema.

Lei de Little (referencia): WIP = throughput x lead time. Se o WIP sobe sem o throughput subir, o lead time vai subir. Por isso o controle e no WIP.

## 4. Rotina semanal (sexta, 30 min)

1. Registrar as 3 metricas no `template-metrica-semanal.md`.
2. Olhar o cartao mais antigo em Fazendo: destravar ou fatiar.
3. Revisar a fila: reordenar os 5 primeiros.
4. Decidir 1 ajuste (ex.: baixar WIP de Revisao de 3 para 2).

## 5. Anti-padroes proibidos

1. Cartao sem criterio de pronto entrando em Fazendo.
2. Mais de 2 cartoes por pessoa em Fazendo.
3. Cartao parado mais de 3 dias sem acao de destrave registrada.
4. Medir produtividade individual por cartoes concluidos (metrica e do sistema, nao da pessoa).
5. Mudar limite de WIP sem registrar motivo e data.
