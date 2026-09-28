# DECK PDI: Documentação como Código (Atividade 3)

## Slide 1: Capa
Documentação como código: Mermaid e diagramas versionados no repo. Marcos Luciano, FV Marketing / V4 Company, Setembro 2026.

## Slide 2: O problema
Diagramas em arquivos soltos fora do git. Ninguém sabe a versão certa, PR não revisa desenho, doc sempre desatualizado.

## Slide 3: A ideia em 1 minuto
Diagrama e texto no mesmo repo: mesmo git, mesmo PR, mesmo revisor. Mermaid renderiza no GitHub sem plugin.

## Slide 4: Regras adotadas
Texto em `.md`, diagrama perto do código, PR muda comportamento e desenho juntos, desenho solto vale só como rascunho.

## Slide 5: Mermaid que usamos
Fluxo para caminhos e retries, sequência para contratos entre n8n e worker. Sintaxe mínima no guia rápido.

## Slide 6: Exemplo real 1
Fluxo de coleta Meta Ads: trigger, webhook, backoff, Supabase, fila de erros. (Mostrar renderizado.)

## Slide 7: Exemplo real 2
Sequência do webhook: contrato de entrada `conta_id` e janela, saída sempre 200 ou 500, nunca silêncio.

## Slide 8: CI como guarda
`mermaid-cli` quebra build com sintaxe inválida. Semântica fica com o revisor e o checklist.

## Slide 9: Divisão com o C4
Mermaid no dia a dia, Structurizr DSL no C4 detalhado. Cada ferramenta no seu quadrado.

## Slide 10: Demo ao vivo
Editar um rótulo no `.md`, abrir o PR com diff legível, rodar o `mmdc`, ver o GitHub renderizar.

## Slide 11: Métricas
4 diagramas vivos rumo a 10, 6 soltos para zerar, 5 PRs com diagrama revisado no trimestre.

## Slide 12: Próximos passos
Converter os 3 fluxos críticos, ligar o CI, apagar soltos após migração.

## Slide 13: Fechamento
Doc na velocidade do código: mudou o fluxo, mudou o desenho, no mesmo PR. Perguntas.
