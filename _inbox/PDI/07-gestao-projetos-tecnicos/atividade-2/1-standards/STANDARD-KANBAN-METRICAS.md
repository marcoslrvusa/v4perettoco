# STANDARD: Fluxo Kanban e Métricas

Área: Automação & Infraestrutura | FV Marketing / V4 Company | Setembro 2026

## 1. Colunas e limites de WIP

| Coluna | O que entra | WIP máximo | Regra de saída |
|---|---|---|---|
| A Fazer | demanda refinada (passou no checklist da A1) | sem limite, ordenada | puxar só se Fazendo tem vaga |
| Fazendo | trabalho ativo | 2 por pessoa | 1 cartão por vez por pessoa, o resto espera |
| Revisão | validação com operação + deploy | 3 no total | revisor responde em até 1 dia útil |
| Pronto | entregue e validado | sem limite | registra data de conclusão e lead time |

WIP estourado = parar de puxar e ajudar a destravar o gargalo. Puxar com WIP cheio é proibido, inclusive para "coisa rápida".

## 2. Classes de serviço

- **Padrão**: segue a fila. 80% dos cartões.
- **Urgente**: fura a fila, max 1 por vez no quadro. Ex.: integração quebrada travando campanha ativa.
- **Data fixa**: tem data externa real (ex.: relatório para reunião de diretoria). Marca a data no cartão.

Tudo marcado como urgente = nada e urgente. Quem marca o segundo urgente decide qual dos dois volta para padrão.

## 3. As 3 métricas (definições oficiais da área)

- **Lead time**: dias úteis entre o cartão entrar em Fazendo e chegar em Pronto. Mede velocidade de atravessamento.
- **Throughput**: cartões concluídos por semana. Mede capacidade real de entrega.
- **WIP**: cartões em Fazendo + Revisão na sexta-feira. Mede carga do sistema.

Lei de Little (referência): WIP = throughput x lead time. Se o WIP sobe sem o throughput subir, o lead time vai subir. Por isso o controle e no WIP.

## 4. Rotina semanal (sexta, 30 min)

1. Registrar as 3 métricas no `template-metrica-semanal.md`.
2. Olhar o cartão mais antigo em Fazendo: destravar ou fatiar.
3. Revisar a fila: reordenar os 5 primeiros.
4. Decidir 1 ajuste (ex.: baixar WIP de Revisão de 3 para 2).

## 5. Anti-padroes proibidos

1. Cartão sem critério de pronto entrando em Fazendo.
2. Mais de 2 cartões por pessoa em Fazendo.
3. Cartão parado mais de 3 dias sem ação de destrave registrada.
4. Medir produtividade individual por cartões concluídos (métrica e do sistema, não da pessoa).
5. Mudar limite de WIP sem registrar motivo e data.
