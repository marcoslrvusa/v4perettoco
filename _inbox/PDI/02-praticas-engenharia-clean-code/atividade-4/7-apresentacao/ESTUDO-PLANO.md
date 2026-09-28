# Plano de Estudo: Design Patterns

- [x] Head First Design Patterns
- [x] Refactoring Guru
- [x] Adapter no handler de CRM + Strategy no roteamento
- [x] Minicurso concluído

## Objetivo do plano

Transformar estudo de catálogo em prática verificável: cada padrão estudado precisa aparecer em
uma linha do standard, em um trecho executável do `patterns_demo.py` e em uma pergunta de
revisão de código. Estudo sem artefato não conta como concluído.

## Trilha percorrida

| Etapa | Material | O que ficou registrado | Status |
| --- | --- | --- | --- |
| Fundamentos | Head First Design Patterns | vocabulário de criacionais, estruturais e comportamentais | concluído |
| Catálogo com exemplos em Python | Refactoring Guru | exemplos de Adapter, Strategy e Observer adaptados ao ecossistema | concluído |
| Mínimo viável em código | `2-code/patterns_demo.py` | port com `Protocol`, adapter, factory e bus de eventos | concluído |
| Aplicação real | PR com Adapter no handler de 1 CRM | piloto em revisão, com checklist de padrões no template | concluído |
| Defesa | deck, demo e roteiro de domínio | narrativa, comandos e respostas adversariais | concluído |

## Critério de conclusão por padrão

Um padrão só é marcado como estudado quando todas as quatro condições são verdadeiras:

1. A definição está escrita com as palavras do time no `DESIGN-PATTERNS-NOTES.md`.

2. Existe um trecho de código executável que demonstra o padrão sem infraestrutura.

3. Existe ao menos um anti-padrão correspondente documentado, ou seja, o modo como o padrão
   costuma ser usado errado.

4. Existe um critério de detecção: como o revisor percebe, em um diff, que o padrão foi violado.

## Lacunas declaradas

- Padrões criacionais além da factory simples (Abstract Factory, Builder): adiados até existir
  mais de uma família de objetos trocáveis em runtime.

- Observer distribuído com broker: o piloto usa bus in-memory e síncrono de propósito; durabilidade
  e ordenação ficam para quando a ordem entre eventos virar requisito de negócio.

- Padrões de nível de sistema (event sourcing, CQRS): fora do escopo desta atividade e de outra
  trilha do PDI.

- Indicador de tempo real de leitura e de retenção: sem instrumento, o quadro acima é
  declaração de conclusão, não métrica.

## Próximo ciclo de estudo

- Estratégia aplicada ao roteamento de modelo de LLM, incluindo seleção por custo e por política
  de ferramenta.

- Command com chave de idempotência e registro de execução, para ações de agente re-jogáveis.

- Teste de arquitetura que impede import de SDK no núcleo, para transformar a regra de camadas em
  falha de build.
