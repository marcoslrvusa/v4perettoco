# Roteiro de domínio: Mapeamento de Domínios com Domain-Driven Design (DDD)

Estudo para defesa presencial da atividade: 5 perguntas de coordenador com respostas curtas.

## 1. Por que DDD explícito em vez de schema único?

Porque schema único e simples no início mas acopla os 4 squads, enquanto DDD da consistência e linguagem comum com governança explícita.

## 2. O que muda com bounded contexts e eventos de domínio?

Cada contexto tem seu modelo e os contextos se comunicam por eventos versionados, nunca por tabela compartilhada ou SQL cruzado.

## 3. Como o agregado garante consistência?

Só a raiz e referenciada de fora e os filhos não tem identidade pública, então a regra transacional fica num ponto único em vez de espalhada.

## 4. Como o mapa e validado antes de virar código?

Em workshop de linguagem ubíqua com Product e 2 squads, validando os agregados contra 3 user stories e só depois gerando os schemas aprovados.

## 5. Quais são as metas numéricas da atividade?

4 domínios mapeados, 0 modelos duplicados e ao menos 6 eventos de domínio definidos.
