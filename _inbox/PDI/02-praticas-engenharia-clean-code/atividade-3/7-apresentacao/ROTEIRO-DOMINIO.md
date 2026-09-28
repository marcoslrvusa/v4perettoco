# Roteiro de dominio: Mapeamento de Dominios com Domain-Driven Design (DDD)

Estudo para defesa presencial da atividade: 5 perguntas de coordenador com respostas curtas.

## 1. Por que DDD explicito em vez de schema unico?

Porque schema unico e simples no inicio mas acopla os 4 squads, enquanto DDD da consistencia e linguagem comum com governanca explicita.

## 2. O que muda com bounded contexts e eventos de dominio?

Cada contexto tem seu modelo e os contextos se comunicam por eventos versionados, nunca por tabela compartilhada ou SQL cruzado.

## 3. Como o agregado garante consistencia?

So a raiz e referenciada de fora e os filhos nao tem identidade publica, entao a regra transacional fica num ponto unico em vez de espalhada.

## 4. Como o mapa e validado antes de virar codigo?

Em workshop de linguagem ubiqua com Product e 2 squads, validando os agregados contra 3 user stories e so depois gerando os schemas aprovados.

## 5. Quais sao as metas numericas da atividade?

4 dominios mapeados, 0 modelos duplicados e ao menos 6 eventos de dominio definidos.
