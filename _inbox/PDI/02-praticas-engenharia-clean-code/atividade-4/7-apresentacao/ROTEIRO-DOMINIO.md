# Roteiro de dominio: Estudo de Design Patterns aplicados ao ecossistema

Estudo para defesa presencial da atividade: 5 perguntas de coordenador com respostas curtas.

## 1. Onde cada padrao entra na operacao?

Adapter no CRM e LLM externos, Strategy no roteamento de modelo e Observer nos eventos de dominio como e-mail e estoque.

## 2. Por que Singleton para clients foi rejeitado?

Porque cria estado global oculto e dificulta teste, entao a decisao ADR-024 troca por injecao de dependencia com fakes nos testes.

## 3. Como plugar um fornecedor novo sem mexer no core?

Criando um adapter que implementa o port existente, como PayPalAdapter ou StripeAdapter, e registrando na factory sem recompilar regra de negocio.

## 4. Como a entrega e validada?

Rodando patterns_demo.py, abrindo PR com Adapter em 1 CRM piloto e aplicando o checklist de padroes no template de PR.

## 5. Como evitar over-engineering com padroes?

Aplicando padrao so onde ha variacao real e com code review que cobra valor entregue, nao quantidade de padroes.
