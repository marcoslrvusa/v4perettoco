# ROTEIRO-DOMINIO: 5 Perguntas que Podem Cair

## 1. Por que Mermaid e não PlantUML ou draw.io?
Resposta: Mermaid renderiza nativo no GitHub e GitLab sem servidor extra, e o diff em PR e legível. PlantUML exige infra e draw.io gera XML ilegível em diff. Para fluxo e sequência, Mermaid basta.

## 2. E diagramas que o Mermaid não faz bem?
Resposta: C4 detalhado continua no Structurizr DSL da atividade 1. A divisão e consciente: Mermaid no dia a dia, DSL no C4 profundo. Nenhuma ferramenta cobre tudo.

## 3. CI valida o desenho estar certo?
Resposta: não. CI valida sintaxe e quebra build em bloco inválido. Se o desenho reflete a realidade é papel do revisor com o checklist de docs vivos, mesma lógica de teste versus revisão de código.

## 4. Onde o diagrama deve morar?
Resposta: junto do código que descreve, não em wiki distante. Fluxo de coleta ao lado do worker. Wiki separada apodrece porque ninguém abre na hora do PR.

## 5. Como migrar os 6 soltos sem parar a operação?
Resposta: um por vez, começando pelos 3 fluxos críticos, cada migração em um PR que vira a fonte oficial. Só apaga o solto depois do Mermaid revisado e mergeado.
