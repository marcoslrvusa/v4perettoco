# DECK PDI: Modelo C4 na Pratica (Atividade 1)

## Slide 1: Capa
Modelo C4 na Pratica aplicado ao Orquestrador de Automacao V4. Marcos Luciano, FV Marketing / V4 Company, Setembro 2026.

## Slide 2: O problema
Tres pessoas desenhavam o mesmo sistema de tres jeitos. Onboarding de 3 dias, incidente vira adivinhacao.

## Slide 3: O que e o C4 em 1 minuto
4 niveis de zoom: contexto, containers, componentes, codigo. Cada nivel responde uma pergunta e tem um publico.

## Slide 4: Nosso sistema real
Orquestrador V4: n8n (:5678), workers Python (:8000), Supabase Postgres, painel Next.js (:3000). Externos: Meta Ads API, Gmail API.

## Slide 5: Nivel 1, contexto
Operador opera, gestor consome, orquestrador fala com Meta e Gmail. (Mostrar diagrama Mermaid renderizado.)

## Slide 6: Nivel 2, containers
Onde cada parte executa e quem chama quem. Destaque: n8n chama workers via webhook, workers gravam no Supabase.

## Slide 7: Nivel 3, componentes do n8n
Triggers, coleta-meta-ads, disparo-gmail, cofre de credenciais, fila de erros.

## Slide 8: Nivel 4, codigo critico
`executar_com_retry` com backoff 30s/60s/120s. Porque a Meta pune rajada com 1h de bloqueio.

## Slide 9: Fonte unica versionavel
Structurizr DSL gera todos os niveis de um modelo so. Mermaid e o espelho que renderiza no repo.

## Slide 10: Regras que adotamos
Relacionamento sempre com verbo, sem misturar niveis, externo com `_Ext`, DSL e Mermaid atualizados juntos.

## Slide 11: Demo ao vivo
Abrir o Mermaid no repo, depois o Structurizr Lite com o `workspace.dsl`, navegar do contexto ao container.

## Slide 12: Metricas
1 sistema com contexto, 4 de 4 containers documentados, onboarding alvo de 3 dias para 1 dia.

## Slide 13: Proximos passos
Publicar link interno, colocar contexto no onboarding, revisar a cada mudanca de container.

## Slide 14: Fechamento
Um mapa unico: em incidente, qualquer pessoa acha a peca quebrada em minutos. Perguntas.
