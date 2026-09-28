# TPL: Checklist de Review (copiar para o PR ou usar como guia)

## Corretude
- [ ] O código faz o que a task pede (critério de aceite coberto)?
- [ ] Caminhos de erro tratados (timeout, 404, payload inválido, lista vazia)?
- [ ] Sem TODO ou flag temporária sem issue vinculada?

## Testes
- [ ] Regra nova tem teste automatizado?
- [ ] Bug corrigido tem teste de regressão que falha sem o fix?
- [ ] CI verde (lint + testes)?

## Segurança e dados
- [ ] Sem segredo hardcoded (usar env ou vault)?
- [ ] Sem SQL ou query concatenada com input?
- [ ] Sem PII em log ou resposta (e-mail, telefone, token)?
- [ ] Permissão e validação de entrada conferidas em borda pública?

## Contrato e compatibilidade
- [ ] Mudança de API, evento ou schema atualizou consumidor e doc?
- [ ] Migração de banco é reversível ou tem rollback descrito?
- [ ] Feature flag criada para comportamento novo em área crítica?

## Legibilidade e tamanho
- [ ] PR até 400 linhas ou com justificativa de fracionamento?
- [ ] Nomes explicam intenção sem precisar ler o corpo?
- [ ] Função faz uma coisa só; trecho duplicado 3x virou helper?

## Veredito (marcar um)
- [ ] APPROVE (sem barreira)
- [ ] COMMENT (só sugestões, merge liberado)
- [ ] REQUEST CHANGES (itens abaixo bloqueiam):
  - Item: ____ Arquivo/linha: ____ Motivo: ____
