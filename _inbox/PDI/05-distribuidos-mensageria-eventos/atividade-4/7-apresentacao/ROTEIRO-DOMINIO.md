# Roteiro de Domínio: Atividade 4 (LGPD em eventos e dados)

13 perguntas que um coordenador faria (12 adversariais e 1 de negócio), com respostas curtas
para defesa no presencial.

## 1. Onde o PII aparece e como você o elimina do trânsito?
O `lead.criado` carregava CPF, e-mail e telefone em texto puro; agora vai cifrado com AES e o downstream recebe `subject_id` ou hash.

**Ampliação se insistirem:** quatro destinos eram atingidos pelo dado cru: tópico, log, cache e
índice de busca. O tópico resolve com cifra e tokenização no payload; o log resolve com
`anon.py` aplicado na origem do logger; o cache resolve com proibição de chave identificadora e
TTL curto; o índice resolve com a mesma chave `subject_id` no comando de exclusão. Eliminar do
trânsito é olhar os quatro, não só o primeiro.

## 2. Como o consentimento é garantido?
Flag `consent_id` obrigatória no payload; sem base legal ativa o dado pessoal não é publicado; auditoria por finalidade.

**Ampliação se insistirem:** o `consent_id` vai no cabeçalho da mensagem, para que o middleware
de todo consumidor valide sem conhecer o schema do corpo. A checagem é feita **antes** da
publicação, e o modo é de falha fechada: com o gateway fora, o evento sai minimizado, nunca
completo. Consentimento para `campanha` não cobre `score`; a pergunta é "para quê", não "se
aceitou".

## 3. Como funciona o direito ao esquecimento?
Uma varredura apaga por `subject_id` em todas as tabelas; cai de 90 dias para menos de 1 dia, dentro do patamar de até 15 dias.

**Ampliação se insistirem:** o script grava `state = 'pending'` antes do primeiro `DELETE`
(recuperação para frente), apaga os destinos filhos e o cadastro por último, grava a linha de
auditoria na mesma transação e publica `subject.delete` pelo outbox com a mesma chave de
partição. A exclusão é idempotente, então falha no meio vira retomada, não retrabalho.

## 4. O que é minimização neste desenho?
Cada etapa recebe só o dado necessário; o Analytics recebe token sem reversão e nada de PII vai para cache.

**Ampliação se insistirem:** a minimização é a única das proteções que multiplica a exposição
por zero, porque campo que não entra não vaza. O Analytics calcula `score` cruzando
`subject_id`, não e-mail. Quando o campo nem entra no payload, dispensa cifra, cache protegido
e exclusão específica daquele campo.

## 5. Como você prova a conformidade?
Varredura de logs com 0 e-mail ou CNPJ cru, 100% dos fluxos com consentimento e TTL de 365 dias com purge automático.

**Ampliação se insistirem:** três evidências são permanentes: varredura diária automatizada
(falha o build), linha em `audit_log` por exclusão (data, hora, destinos, sem PII) e gate de
schema na esteira (campo de PII sem `pii:true` não passa). As dos testes são periódicas: T1,
T3, T6 e T9 re-executados a cada versão, com saída anexada ao ticket.

## 6. Por que não criptografar só o payload do tópico e ser mais simples?
Porque resolve 1 dos 4 destinos. As cópias em cache, índice e log continuam cruas, e a
criptografia na origem cria a sensação falsa de conformidade: o Vendas está cifrado, o Analytics
segue com o CPF em coluna simples. O custo adicional do desenho completo é governança (alguém
atualizar o `mapa-dados.md`) e um pouco de latência no gateway, e é esse o preço que a opção
barata não cobra.

## 7. Quanto custa manter isso rodando?
**(meta) 35 h** de esforço total da atividade, sendo 6 h de standards, 8 h de payload e
gateway, 6 h de cascata e auditoria, 4 h de utilitários, 7 h de testes e 4 h de material de
apresentação. Depois de entregue, o custo contínuo é de operação: revisar o `mapa-dados.md`
quando nasce tabela nova, atualizar o TTL quando muda a política, e a rotina de revisita da
DLQ de comandos. Sem número de reais nesta atividade, porque o valor por hora é definido fora
do escopo deste material.

## 8. Quem decide cada coisa?
O DPO decide a base legal e a finalidade; o dono do `mapa-dados.md` decide prazo de retenção e
destinos por tabela; a liderança técnica decide a arquitetura (ADR-054) e a chave de partição;
o time de dados é consultado quando o payload é minimizado, porque enxerga o consumo de cada
campo. O que ninguém decide sozinho: criar tabela nova sem prazo, dono e chave de exclusão.

## 9. E se cair no meio da noite?
O padrão é de falha fechada: com gateway ou cofre de chaves indisponíveis, eventos continuam
saindo minimizados e nenhum dado pessoal vaza; com o worker de exclusão caído, `deletion.pending`
acumula e o job retoma de onde parou quando volta, porque o estado é gravado antes do `DELETE`.
Runbook: checagem de `deletion.pending`, `dlq.comandos.depth` e `pii_in_log.count` (deve ser
zero); alerta em 6 h para exclusão parada, revisita de DLQ em menos de 24 h. Ninguém precisa
inventar procedimento às 3 h: o passo a passo está na seção Operação do README.

## 10. Qual é o SLO, exatamente?
PII em log: `0` (varredura diária). Consentimento: `100%` dos fluxos com dado pessoal.
Exclusão: até 15 dias de teto legal, com meta interna de menos de 1 dia. P95 do gateway de
consentimento: `<= 25 ms` (meta). Campos de PII sem marcação no schema: `0` por build. DLQ de
comandos: `0` com mais de 24 h. Quando estoura: evento sem `consent_id` é P1 e suspende a
publicação do evento; exclusão acima de 6 h escala para o dono do destino pendente.

## 11. Como você prova que funciona, na prática, hoje?
Quatro evidências com saída capturada: (a) varredura de 24 h de log com zero ocorrência de
regex de e-mail e de CNPJ; (b) exclusão do `subject_id` de teste com contagem zero nas quatro
tabelas e linha em `audit_log`; (c) `kill -9` no worker durante o lote e estado final `done`
sem intervenção; (d) `lead.criado` + `subject.delete` com rebalanceamento no meio, estado final
"apagado" em 100% das execuções. E o gate de schema, que falha o build diante de campo novo de
PII sem marcação.

## 12. O que você deixaria para trás, e qual a alternativa mais barata?
**Deixaria para trás, conscientemente:** o serviço de tokenização com revogação central (mais um
SLO, mais um plantão), a expiração automática dos backups antes da janela completa, e o TTL
diferenciado por tipo de dado dentro da mesma tabela (hoje é 365 dias por tabela, não por
campo). **Alternativa mais barata:** anonimizar só os logs e manter exclusão manual. Custa
quase nada de código e resolve o vetor mais barulhento (o log), mas deixa o dado vivo na base de
negócio e mantém o apagamento em caçada manual por serviço, que é justamente o que gera 90 dias
de resposta. A conta é simples: barato hoje, mesma dívida amanhã.

## 13. Qual o impacto no negócio, em horas e risco?
Sem o padrão, o pedido de exclusão leva 90 dias (Exemplo numérico de partida) e depende de
caçada manual; com ele, menos de 1 dia e uma varredura por `subject_id`. A resposta ao titular
passa de dias de busca por serviço para minutos com `audit_log`, que é o que separa "apagamos
quando pedem" de "apagamos com prova". O risco residual conhecido é a exclusão não alcançar
backup antes da rotacionar: está na matriz como impacto alto, mitigado por janela declarada e
mídia criptografada com chave própria.
