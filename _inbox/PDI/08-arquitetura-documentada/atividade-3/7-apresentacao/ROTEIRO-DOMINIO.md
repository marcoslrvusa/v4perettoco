# ROTEIRO-DOMINIO: 5 Perguntas que Podem Cair

## 1. Por que Mermaid e nao PlantUML ou draw.io?
Resposta: Mermaid renderiza nativo no GitHub e GitLab sem servidor extra, e o diff em PR e legivel. PlantUML exige infra e draw.io gera XML ilegivel em diff. Para fluxo e sequencia, Mermaid basta.

## 2. E diagramas que o Mermaid nao faz bem?
Resposta: C4 detalhado continua no Structurizr DSL da atividade 1. A divisao e consciente: Mermaid no dia a dia, DSL no C4 profundo. Nenhuma ferramenta cobre tudo.

## 3. CI valida o desenho estar certo?
Resposta: nao. CI valida sintaxe e quebra build em bloco invalido. Se o desenho reflete a realidade e papel do revisor com o checklist de docs vivos, mesma logica de teste versus revisao de codigo.

## 4. Onde o diagrama deve morar?
Resposta: junto do codigo que descreve, nao em wiki distante. Fluxo de coleta ao lado do worker. Wiki separada apodrece porque ninguem abre na hora do PR.

## 5. Como migrar os 6 soltos sem parar a operacao?
Resposta: um por vez, comecando pelos 3 fluxos criticos, cada migracao em um PR que vira a fonte oficial. So apaga o solto depois do Mermaid revisado e mergeado.
