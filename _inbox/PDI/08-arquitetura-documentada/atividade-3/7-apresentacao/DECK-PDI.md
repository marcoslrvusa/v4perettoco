# DECK PDI: Documentacao como Codigo (Atividade 3)

## Slide 1: Capa
Documentacao como codigo: Mermaid e diagramas versionados no repo. Marcos Luciano, FV Marketing / V4 Company, Setembro 2026.

## Slide 2: O problema
Diagramas em arquivos soltos fora do git. Ninguem sabe a versao certa, PR nao revisa desenho, doc sempre desatualizado.

## Slide 3: A ideia em 1 minuto
Diagrama e texto no mesmo repo: mesmo git, mesmo PR, mesmo revisor. Mermaid renderiza no GitHub sem plugin.

## Slide 4: Regras adotadas
Texto em `.md`, diagrama perto do codigo, PR muda comportamento e desenho juntos, desenho solto vale so como rascunho.

## Slide 5: Mermaid que usamos
Fluxo para caminhos e retries, sequencia para contratos entre n8n e worker. Sintaxe minima no guia rapido.

## Slide 6: Exemplo real 1
Fluxo de coleta Meta Ads: trigger, webhook, backoff, Supabase, fila de erros. (Mostrar renderizado.)

## Slide 7: Exemplo real 2
Sequencia do webhook: contrato de entrada `conta_id` e janela, saida sempre 200 ou 500, nunca silencio.

## Slide 8: CI como guarda
`mermaid-cli` quebra build com sintaxe invalida. Semantica fica com o revisor e o checklist.

## Slide 9: Divisao com o C4
Mermaid no dia a dia, Structurizr DSL no C4 detalhado. Cada ferramenta no seu quadrado.

## Slide 10: Demo ao vivo
Editar um rotulo no `.md`, abrir o PR com diff legivel, rodar o `mmdc`, ver o GitHub renderizar.

## Slide 11: Metricas
4 diagramas vivos rumo a 10, 6 soltos para zerar, 5 PRs com diagrama revisado no trimestre.

## Slide 12: Proximos passos
Converter os 3 fluxos criticos, ligar o CI, apagar soltos apos migracao.

## Slide 13: Fechamento
Doc na velocidade do codigo: mudou o fluxo, mudou o desenho, no mesmo PR. Perguntas.
