# STANDARD: Scoping e Estimativas Tecnicas

Area: Automacao & Infraestrutura | FV Marketing / V4 Company | Setembro 2026

## 1. Regra de ouro

Nenhum compromisso de prazo sem escopo escrito. Escopo escrito = objetivo + fora de escopo + premissas + pacotes + faixa com buffer. Sem isso, a estimativa e palpite.

## 2. Decomposicao (WBS pratica)

1. Quebre a entrega em pacotes de **no maximo 1 dia util** cada.
2. Cada pacote tem: nome, criterio de pronto (1 frase) e dependencia (se houver).
3. Se um pacote nao pode ser quebrado nem estimado, marque como **spike timebox** (ex.: 4h de investigacao) e estime o spike, nao a solucao.
4. Limite pratico: 3 a 10 pacotes por entrega. Acima disso, divida a entrega em fases.

## 3. Estimativa de 3 pontos (PERT)

Para cada pacote, estime 3 numeros em horas:

- **O (otimista)**: tudo da certo, sem interrupcao.
- **M (mais provavel)**: ritmo normal, com 1 ou 2 imprevistos pequenos.
- **P (pessimista)**: dependencia atrasa, API muda, dado sujo.

Estimativa do pacote: **E = (O + 4M + P) / 6**.

Exemplo: O=2h, M=4h, P=8h. E = (2 + 16 + 8) / 6 = 4,3h.

## 4. Buffer

Opcao padrao (simples): **20% sobre a soma dos E**. Opcao avancada: raiz quadrada da soma dos quadrados das diferencas (P - E) de cada pacote, que da buffer proporcional ao risco real. Use a simples ate ter historico; migre para a avancada com 10+ entregas medidas.

Nunca esconda o buffer dentro dos pacotes. Buffer e linha propria na planilha, visivel para quem negocia.

## 5. Cone da incerteza (fatores de McConnell, adaptados)

Multiplique a estimativa pontual pela faixa conforme a fase:

| Fase | Faixa sobre a estimativa |
|---|---|
| Conceito (ideia inicial) | 0,25x a 4x |
| Requisitos aprovados | 0,5x a 2x |
| Design detalhado / prototipo | 0,8x a 1,25x |
| Pos desenvolvimento (faltam testes/deploy) | 0,9x a 1,1x |

Na pratica: na fase de conceito, comunique "entre 5 e 20 dias uteis"; apos requisitos, "entre 8 e 14 dias". A faixa estreita sozinha com o avancar do projeto, nunca por pressao.

## 6. Reestimativa por marco (obrigatoria)

Reestime em 3 marcos: (1) requisitos aprovados, (2) metade dos pacotes pronta, (3) pre deploy. Cada reestimativa leva 15 min: atualize O/M/P dos pacotes restantes e recalcule buffer. Registre as 3 faixas na planilha para mostrar o cone fechando.

## 7. Anti-padroes proibidos

1. Numero unico sem faixa ("3 dias cravados").
2. Estimativa dada por quem nao vai executar, sem consultar o executor.
3. Desconto de buffer por pressao ("tira o buffer que fecha").
4. Escopo mudando sem reestimativa (mudanca = novo pacote + nova faixa).
5. Comparar estimado vs real e nao registrar (sem historico nao ha calibragem).
