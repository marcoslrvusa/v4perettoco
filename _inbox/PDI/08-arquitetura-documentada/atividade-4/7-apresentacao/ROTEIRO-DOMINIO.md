# ROTEIRO-DOMINIO: 5 Perguntas que Podem Cair

## 1. Por que Backstage se nem temos o portal rodando?
Resposta: o `catalog-info.yaml` e padrao aberto e texto simples. Usamos hoje como fonte (gera a planilha espelho) e importamos sem retrabalho quando o portal existir. Formato proprietario seria divida futura.

## 2. Dono pessoa nao cria heroi e ponto unico de falha?
Resposta: cria se parar ai. Por isso suplente obrigatorio em peca critica e alta, e suplente so vale apos operar a peca com o dono ao lado. A matriz mostra o risco em vez de esconder: hoje ha concentracao declarada com plano de 60 dias.

## 3. Por que nao RACI completo?
Resposta: RACI com 4 letras por peca ninguem mantem em time pequeno. Nossa matriz tem 5 colunas que respondem a pergunta real do incidente: quem chamo, quem cobre, para quem escalo. Simplicidade que sobrevive.

## 4. E se o dono sair da empresa?
Resposta: o catalogo e a matriz fazem a transferencia em dias, nao meses: o suplente assume, a roda continua e o proximo dono herda docs, ADRs e diagramas das atividades 1 a 3. Sem isso, a saida apaga a historia.

## 5. Como isso conversa com C4, ADR e Mermaid?
Resposta: as 4 atividades formam o pacote: C4 mostra o que existe, ADR mostra por que, Mermaid mantem o desenho vivo e o catalogo diz de quem e. Uma peca nova entra pelo catalogo, ganha contexto C4, registra decisoes em ADR e desenha fluxo em Mermaid.
