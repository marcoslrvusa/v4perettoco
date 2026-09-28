# Catalogo e Ownership: Fundamentos Praticados Aqui

## 1. O que o catalogo responde

Para cada sistema: o que e, onde mora o codigo, quem e o dono, quem e o suplente, qual o nivel de criticidade e para quem escalar. Uma pagina por sistema, sem excecao.

## 2. Niveis de criticidade adotados

| Nivel | Significado | Exemplo |
|-------|-------------|---------|
| Critico | Quebra para a operacao de trafego | Worker de coleta Meta Ads |
| Alto | Degrada relatorio ou disparo | n8n, Supabase |
| Medio | Atrapalha mas tem contorno manual | Painel Next.js |
| Baixo | Interno, sem impacto em cliente | Script de limpeza de logs |

## 3. Regras de ownership

- Dono e pessoa com nome e sobrenome, nunca "o time".
- Toda peca critica ou alta tem suplente que ja operou a peca pelo menos uma vez.
- Dono responde por: manter doc atualizado, revisar PR critico e ser chamado primeiro em incidente.
- Dono nao responde por: fazer tudo sozinho. Escala existe para isso.

## 4. Formato

`catalog-info.yaml` no padrao Backstage (exemplo real em `2-implementacao/`), uma entidade `Component` por sistema mais `API` para o webhook do worker. Sem Backstage rodando, a planilha espelho e gerada por leitura simples do YAML.
