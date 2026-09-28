# DECK PDI: Modelo C4 na Prática (Atividade 1)

## Slide 1: Capa
Modelo C4 na Prática aplicado ao Orquestrador de Automação V4. Marcos Luciano, FV Marketing / V4 Company, Setembro 2026.

## Slide 2: O problema
Três pessoas desenhavam o mesmo sistema de três jeitos. Onboarding de 3 dias, incidente vira adivinhação.

## Slide 3: O que é o C4 em 1 minuto
4 níveis de zoom: contexto, containers, componentes, código. Cada nível responde uma pergunta e tem um público.

## Slide 4: Nosso sistema real
Orquestrador V4: n8n (:5678), workers Python (:8000), Supabase Postgres, painel Next.js (:3000). Externos: Meta Ads API, Gmail API.

## Slide 5: Nível 1, contexto
Operador opera, gestor consome, orquestrador fala com Meta e Gmail. (Mostrar diagrama Mermaid renderizado.)

## Slide 6: Nível 2, containers
Onde cada parte executa e quem chama quem. Destaque: n8n chama workers via webhook, workers gravam no Supabase.

## Slide 7: Nível 3, componentes do n8n
Triggers, coleta-meta-ads, disparo-gmail, cofre de credenciais, fila de erros.

## Slide 8: Nível 4, código crítico
`executar_com_retry` com backoff 30s/60s/120s. Porque a Meta pune rajada com 1h de bloqueio.

## Slide 9: Fonte única versionável
Structurizr DSL gera todos os níveis de um modelo só. Mermaid e o espelho que renderiza no repo.

## Slide 10: Regras que adotamos
Relacionamento sempre com verbo, sem misturar níveis, externo com `_Ext`, DSL e Mermaid atualizados juntos.

## Slide 11: Demo ao vivo
Abrir o Mermaid no repo, depois o Structurizr Lite com o `workspace.dsl`, navegar do contexto ao container.

## Slide 12: Métricas
1 sistema com contexto, 4 de 4 containers documentados, onboarding alvo de 3 dias para 1 dia.

## Slide 13: Próximos passos
Publicar link interno, colocar contexto no onboarding, revisar a cada mudança de container.

## Slide 14: Fechamento
Um mapa único: em incidente, qualquer pessoa acha a peça quebrada em minutos. Perguntas.
