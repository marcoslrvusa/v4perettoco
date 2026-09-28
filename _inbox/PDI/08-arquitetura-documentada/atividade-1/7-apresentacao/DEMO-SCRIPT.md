# DEMO-SCRIPT: C4 na Pratica (10 minutos)

## 0:00 : 1:30 | Abertura e problema
Mostre dois desenhos antigos diferentes do mesmo sistema. Fale: "o mesmo orquestrador explicado de dois jeitos, nenhum com portas nem donos".

## 1:30 : 4:00 | Contexto no repo
Abra `1-standards/02-diagramas-sistema-automacao.md` renderizado. Aponte pessoas, sistema e os dois externos (Meta, Gmail). Pergunte a plateia: "falta algum ator?".

## 4:00 : 6:30 | Containers e portas
Abra o bloco C4Container. Destaque portas 5678, 8000, 3000 e o cofre de credenciais. Explique o caminho feliz: trigger, webhook, worker, Supabase.

## 6:30 : 8:30 | Structurizr DSL
Abra `2-implementacao/01-workspace-c4.dsl` no Structurizr Lite. Navegue de Contexto para Containers sem redesenhar nada. Frase chave: "um modelo, varios diagramas".

## 8:30 : 10:00 | Codigo critico e checklist
Mostre `executar_com_retry` e o backoff. Feche com o checklist de revisao e o convite para perguntas.

Plano B sem internet: use os prints em `pdi-arquitetura-documentada-a1.pdf`, ja gerado nesta pasta.
