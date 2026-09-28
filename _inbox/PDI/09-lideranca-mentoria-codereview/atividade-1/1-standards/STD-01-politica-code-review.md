# STD-01: Política de Code Review

## 1. Objetivo

Definir o que o review garante (corretude, testes, segurança básica, legibilidade mínima) e o que ele não faz (redesenhar arquitetura, discutir gosto, substituir pair programming). Review bom barra pouco e ensina muito.

## 2. O que BARRA o merge (request changes)

1. Lógica errada ou requisito não atendido conforme a task.
2. Ausência de teste para regra nova ou correção de bug sem teste de regressão.
3. Falha de segurança básica: SQL concatenado, segredo hardcoded, input sem validação em borda pública, permissão faltando.
4. Quebra de contrato: endpoint, evento ou schema alterado sem atualizar consumidor e doc.
5. Código que não roda: CI vermelho, migração que quebra, dependência não declarada.
6. Vazamento de dados: log com PII, e-mail ou token exposto em resposta.
7. PR acima de 400 linhas sem justificativa de fracionamento no corpo do PR.

## 3. O que é SUGESTÃO (comment ou nit, nunca bloqueia)

- Estilo, nome "melhor", formatação e ordem de métodos.
- Refatoração maior ("extrai isso para um service") quando o código atual está correto.
- Performance micro sem evidência de gargalo.
- Ideia de arquitetura alternativa sem defeito concreto na atual.

Prefixo obrigatório: `nit:` para cosmético, `sugestão:` para opcional com motivo. Sugestão sem motivo deve ser ignorada sem culpa.

## 4. SLA

- Primeira resposta em até 8h úteis.
- PR urgente (hotfix, cliente parado): 2h úteis, marcado com label `urgente`.
- Revisor que não consegue atender no SLA reatribui no mesmo dia, sem precisar pedir permissão.
- Autor responde todo comentário em até 1 dia útil, mesmo que seja "feito" ou "discordo porque...".

## 5. Tamanho e fatiamento

- Teto padrão: 400 linhas alteradas por PR.
- Acima do teto, o corpo do PR explica por que não deu para fatiar (migração, rename, gerado).
- Fatiar por: primeiro refatoração pura, depois comportamento; primeiro backend, depois consumo.

## 6. Papéis

- Autor: descreve contexto, testa local, marca reviewers, responde tudo.
- Revisor: lê tudo, roda mentalmente os caminhos, verifica testes, dá veredito claro.
- CODEOWNERS: pagamento, dados pessoais, auth e infra exigem dono da área. Demais áreas, 1 approval qualquer basta.

## 7. Vereditos

| Veredito | Quando usar | Efeito |
|----------|-------------|--------|
| Approve | Sem barreira, no máximo sugestões | Autor pode dar merge |
| Comment | Dúvida ou sugestão, sem barreira | Autor pode dar merge |
| Request changes | Ao menos 1 item da seção 2 | Merge bloqueado até resolver |
