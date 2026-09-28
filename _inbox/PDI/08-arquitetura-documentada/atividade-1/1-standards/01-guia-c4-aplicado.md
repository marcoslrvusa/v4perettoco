# Guia C4 Aplicado: os 4 Níveis sem Enrolação

Sistema de referência: **Orquestrador de Automação V4** (n8n + workers Python + Supabase + painel Next.js).

## 1. Os 4 níveis

| Nível | Pergunta que responde | Público | Exemplo nesta PDI |
|-------|----------------------|---------|-------------------|
| 1. Contexto | O que o sistema faz e com quem fala | Qualquer pessoa | Operador, Meta Ads API, Gmail, Supabase(Auth) em volta do Orquestrador |
| 2. Containers | Onde cada parte executa | Tech lead, dev | n8n, workers Python, Supabase Postgres, painel Next.js |
| 3. Componentes | Como um container se divide por dentro | Dev do container | Dentro do n8n: triggers, credenciais, subworkflows, fila de erros |
| 4. Código | Como a peça crítica funciona | Dev que vai mexer | Função `executar_com_retry` do worker de coleta Meta Ads |

Regra de ouro: cada nível faz zoom em **um único elemento** do nível anterior. Nunca misture container e componente no mesmo diagrama.

## 2. Notação mínima obrigatória

Todo elemento precisa de: nome, tipo (pessoa, sistema, container, componente) e descrição de uma linha com verbo. Todo relacionamento precisa de: origem, destino e rótulo com verbo ("consulta", "grava", "dispara"). Relacionamento sem rótulo é erro de revisão.

## 3. Quando usar cada nível

- Contexto: sempre. E o cartão de visita, cabe em 1 slide.
- Containers: sempre que houver mais de um runtime (aqui há 4, então é obrigatório).
- Componentes: só para o container que o time mais mexe (aqui: n8n).
- Código: só para a peça onde um bug custa dinheiro (aqui: worker de coleta, que decide verba de tráfego).

## 4. Convenções de nomes adotadas

- Sistemas externos ganham sufixo `_Ext` (ex.: `Meta Ads API_Ext`).
- Banco segue o padrão `ContainerDb` no Mermaid e `database` no DSL.
- Arquivos: `workspace.dsl` (fonte), `02-exemplo-mermaid-c4.md` (espelho), ambos nesta atividade.
- Diagramas desatualizados há mais de 30 dias entram na tabela de métricas como dívida.
