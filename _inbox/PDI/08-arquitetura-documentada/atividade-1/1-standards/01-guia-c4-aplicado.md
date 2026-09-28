# Guia C4 Aplicado: os 4 Niveis sem Enrolacao

Sistema de referencia: **Orquestrador de Automacao V4** (n8n + workers Python + Supabase + painel Next.js).

## 1. Os 4 niveis

| Nivel | Pergunta que responde | Publico | Exemplo nesta PDI |
|-------|----------------------|---------|-------------------|
| 1. Contexto | O que o sistema faz e com quem fala | Qualquer pessoa | Operador, Meta Ads API, Gmail, Supabase(Auth) em volta do Orquestrador |
| 2. Containers | Onde cada parte executa | Tech lead, dev | n8n, workers Python, Supabase Postgres, painel Next.js |
| 3. Componentes | Como um container se divide por dentro | Dev do container | Dentro do n8n: triggers, credenciais, subworkflows, fila de erros |
| 4. Codigo | Como a peca critica funciona | Dev que vai mexer | Funcao `executar_com_retry` do worker de coleta Meta Ads |

Regra de ouro: cada nivel faz zoom em **um unico elemento** do nivel anterior. Nunca misture container e componente no mesmo diagrama.

## 2. Notacao minima obrigatoria

Todo elemento precisa de: nome, tipo (pessoa, sistema, container, componente) e descricao de uma linha com verbo. Todo relacionamento precisa de: origem, destino e rotulo com verbo ("consulta", "grava", "dispara"). Relacionamento sem rotulo e erro de revisao.

## 3. Quando usar cada nivel

- Contexto: sempre. E o cartao de visita, cabe em 1 slide.
- Containers: sempre que houver mais de um runtime (aqui ha 4, entao e obrigatorio).
- Componentes: so para o container que o time mais mexe (aqui: n8n).
- Codigo: so para a peca onde um bug custa dinheiro (aqui: worker de coleta, que decide verba de trafego).

## 4. Convenções de nomes adotadas

- Sistemas externos ganham sufixo `_Ext` (ex.: `Meta Ads API_Ext`).
- Banco segue o padrao `ContainerDb` no Mermaid e `database` no DSL.
- Arquivos: `workspace.dsl` (fonte), `02-exemplo-mermaid-c4.md` (espelho), ambos nesta atividade.
- Diagramas desatualizados ha mais de 30 dias entram na tabela de metricas como divida.
