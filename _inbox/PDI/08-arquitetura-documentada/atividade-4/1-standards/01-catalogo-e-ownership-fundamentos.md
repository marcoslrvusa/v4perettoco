# Catálogo e Ownership: Fundamentos Praticados Aqui

## 1. O que o catálogo responde

Para cada sistema: o que é, onde mora o código, quem é o dono, quem é o suplente, qual o nível de criticidade e para quem escalar. Uma página por sistema, sem exceção.

## 2. Níveis de criticidade adotados

| Nível | Significado | Exemplo |
|-------|-------------|---------|
| Crítico | Quebra para a operação de tráfego | Worker de coleta Meta Ads |
| Alto | Degrada relatório ou disparo | n8n, Supabase |
| Médio | Atrapalha mas tem contorno manual | Painel Next.js |
| Baixo | Interno, sem impacto em cliente | Script de limpeza de logs |

## 3. Regras de ownership

- Dono e pessoa com nome e sobrenome, nunca "o time".
- Toda peça crítica ou alta tem suplente que já operou a peça pelo menos uma vez.
- Dono responde por: manter doc atualizado, revisar PR crítico e ser chamado primeiro em incidente.
- Dono não responde por: fazer tudo sozinho. Escala existe para isso.

## 4. Formato

`catalog-info.yaml` no padrão Backstage (exemplo real em `2-implementacao/`), uma entidade `Component` por sistema mais `API` para o webhook do worker. Sem Backstage rodando, a planilha espelho e gerada por leitura simples do YAML.
