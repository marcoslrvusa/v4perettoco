# ROTEIRO-DOMINIO: 5 Perguntas que Podem Cair

## 1. Por que Backstage se nem temos o portal rodando?
Resposta: o `catalog-info.yaml` e padrão aberto e texto simples. Usamos hoje como fonte (gera a planilha espelho) e importamos sem retrabalho quando o portal existir. Formato proprietário seria dívida futura.

## 2. Dono pessoa não cria herói e ponto único de falha?
Resposta: cria se parar ai. Por isso suplente obrigatório em peça crítica e alta, e suplente só vale após operar a peça com o dono ao lado. A matriz mostra o risco em vez de esconder: hoje há concentração declarada com plano de 60 dias.

## 3. Por que não RACI completo?
Resposta: RACI com 4 letras por peça ninguém mantém em time pequeno. Nossa matriz tem 5 colunas que respondem a pergunta real do incidente: quem chamo, quem cobre, para quem escalo. Simplicidade que sobrevive.

## 4. E se o dono sair da empresa?
Resposta: o catálogo e a matriz fazem a transferência em dias, não meses: o suplente assume, a roda continua e o próximo dono herda docs, ADRs e diagramas das atividades 1 a 3. Sem isso, a saída apaga a história.

## 5. Como isso conversa com C4, ADR e Mermaid?
Resposta: as 4 atividades formam o pacote: C4 mostra o que existe, ADR mostra por que, Mermaid mantém o desenho vivo e o catálogo diz de quem é. Uma peça nova entra pelo catálogo, ganha contexto C4, registra decisões em ADR e desenha fluxo em Mermaid.
