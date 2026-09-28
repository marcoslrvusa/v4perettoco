# STANDARD: Scoping e Estimativas Técnicas

Área: Automação & Infraestrutura | FV Marketing / V4 Company | Setembro 2026

## 1. Regra de ouro

Nenhum compromisso de prazo sem escopo escrito. Escopo escrito = objetivo + fora de escopo + premissas + pacotes + faixa com buffer. Sem isso, a estimativa e palpite.

## 2. Decomposição (WBS prática)

1. Quebre a entrega em pacotes de **no máximo 1 dia útil** cada.
2. Cada pacote tem: nome, critério de pronto (1 frase) e dependência (se houver).
3. Se um pacote não pode ser quebrado nem estimado, marque como **spike timebox** (ex.: 4h de investigação) e estime o spike, não a solução.
4. Limite prático: 3 a 10 pacotes por entrega. Acima disso, divida a entrega em fases.

## 3. Estimativa de 3 pontos (PERT)

Para cada pacote, estime 3 números em horas:

- **O (otimista)**: tudo da certo, sem interrupção.
- **M (mais provável)**: ritmo normal, com 1 ou 2 imprevistos pequenos.
- **P (pessimista)**: dependência atrasa, API muda, dado sujo.

Estimativa do pacote: **E = (O + 4M + P) / 6**.

Exemplo: O=2h, M=4h, P=8h. E = (2 + 16 + 8) / 6 = 4,3h.

## 4. Buffer

Opção padrão (simples): **20% sobre a soma dos E**. Opção avançada: raiz quadrada da soma dos quadrados das diferenças (P - E) de cada pacote, que da buffer proporcional ao risco real. Use a simples até ter histórico; migre para a avançada com 10+ entregas medidas.

Nunca esconda o buffer dentro dos pacotes. Buffer e linha própria na planilha, visível para quem negocia.

## 5. Cone da incerteza (fatores de McConnell, adaptados)

Multiplique a estimativa pontual pela faixa conforme a fase:

| Fase | Faixa sobre a estimativa |
|---|---|
| Conceito (ideia inicial) | 0,25x a 4x |
| Requisitos aprovados | 0,5x a 2x |
| Design detalhado / protótipo | 0,8x a 1,25x |
| Pós desenvolvimento (faltam testes/deploy) | 0,9x a 1,1x |

Na prática: na fase de conceito, comunique "entre 5 e 20 dias úteis"; após requisitos, "entre 8 e 14 dias". A faixa estreita sozinha com o avançar do projeto, nunca por pressão.

## 6. Reestimativa por marco (obrigatória)

Reestime em 3 marcos: (1) requisitos aprovados, (2) metade dos pacotes pronta, (3) pré-deploy. Cada reestimativa leva 15 min: atualize O/M/P dos pacotes restantes e recalcule buffer. Registre as 3 faixas na planilha para mostrar o cone fechando.

## 7. Anti-padroes proibidos

1. Número único sem faixa ("3 dias cravados").
2. Estimativa dada por quem não vai executar, sem consultar o executor.
3. Desconto de buffer por pressão ("tira o buffer que fecha").
4. Escopo mudando sem reestimativa (mudança = novo pacote + nova faixa).
5. Comparar estimado vs real e não registrar (sem histórico não há calibragem).
