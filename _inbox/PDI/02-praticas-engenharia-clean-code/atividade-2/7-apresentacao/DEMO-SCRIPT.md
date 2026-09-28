# Roteiro de Demo: Pipeline de Testes Automatizados (Unit/Integration/E2E) com 80% de Cobertura

Abra o deck (index.html) e percorra os slides na ordem.

1. Slide de Resumo: abra com o problema de negócio e o blast radius.
2. Slide do ADR: defenda a opção escolhida vs as rejeitadas (trade-offs).
3. Slide de Validação/Rollout: mostre como provamos em produção.
4. Slide de Riscos: apresente o plano de mitigação.

Material de apoio: pdi-praticas-engenharia-clean-code-a2-report.pdf (dossiê completo).

## Pré-requisitos da demo

| Item | Estado esperado | Se estiver errado |
| --- | --- | --- |
| Python 3.12 | `python3 --version` retorna 3.12.x | Instalar a versão 3.12 antes de começar |
| Dependências | `pip install pytest pytest-cov testcontainers` sem erro | Reinstalar a partir do workflow do repositório |
| Docker ativo | `docker ps` lista sem erro | Subir o daemon, sem ele a camada de integração falha |
| Repo limpo | `git status` sem alteração pendente | Stash ou commitar, nunca demo com sujeira |
| Seed de dados | suíte roda verde do zero | Rodar `pytest` uma vez antes da apresentação |

Rollback da demo: nenhuma etapa altera arquivo de produção. Para desfazer qualquer alteração pontual feita ao vivo, `git checkout -- .` restaura o repositório ao estado inicial.

## Passos numerados

**Passo 1.** Abrir o terminal na raiz da atividade e conferir a versão.
Comando: `python3 --version`
Saída esperada: `Python 3.12.x`.
Critério de falha: versão diferente. O que fazer: abortar a demo de integração e rodar só a camada unitária, avisando a coordenação.

**Passo 2.** Mostrar a configuração do gate.
Comando: `cat 2-code/pytest.ini`
Saída esperada: linha `addopts = --cov=src --cov-report=term-missing --cov-fail-under=80`.
Critério de falha: teto ausente. O que fazer: não há demo de gate sem teto; voltar ao Passo 1.

**Passo 3.** Rodar a camada unitária isolada.
Comando: `pytest 2-code/test_agent_pipeline.py -v`
Saída esperada: testes `test_unit_parse_prompt` e `test_unit_retry_backoff` marcados como PASS.
Critério de falha: qualquer FAIL. O que fazer: imprimir o traceback, classificar como defeito de teste e corrigir antes de seguir.

**Passo 4.** Mostrar a medição de cobertura com o relatório de linhas faltantes.
Comando: `pytest 2-code/test_agent_pipeline.py --cov=src --cov-report=term-missing`
Saída esperada: bloco `Name    Stmts   Miss` e percentual impresso no fim.
Critério de falha: relatório sem porcentagem. O que fazer: verificar instalação do `pytest-cov`.

**Passo 5.** Rodar a camada de integração.
Comando: `pytest 2-code/test_integration_repo.py -v`
Saída esperada: `test_integration_happy_path` e `test_integration_marca_falha_sem_silenciar` PASS.
Critério de falha: erro de import ou de conexão. O que fazer: conferir `docker ps`; se o contêiner não subir, declarar a falha e pular para o Passo 8.

**Passo 6.** Demonstração do modo de falha do teste.
Comando: `pytest 2-code/test_agent_pipeline.py::test_unit_parse_prompt -v` após inserir temporariamente `assert False` no teste.
Saída esperada: `AssertionError` e código de saída diferente de zero.
Critério de falha: teste passar mesmo com asserção falsa. O que fazer: encerrar a demo, porque isso invalida a rede de segurança inteira.
Rollback: remover a linha inserida com `git checkout -- 2-code/test_agent_pipeline.py`.

**Passo 7.** Mostrar a leitura do código de saída.
Comando: `pytest 2-code/test_agent_pipeline.py -q; echo "exit=$?"`
Saída esperada: `exit=0` no verde e `exit=1` no vermelho.
Critério de falha: código de saída 0 com teste falhando. O que fazer: parar, porque o CI não conseguiria bloquear nada.

**Passo 8.** Executar o gate completo do repositório.
Comando: `pytest --cov=src --cov-report=term-missing --cov-fail-under=80` (o mesmo comando que o CI roda).
Saída esperada: cobertura impressa e `Required test coverage of 80% reached` quando verde.
Critério de falha: cobertura abaixo de 80%. O que fazer: mostrar a lista `Missing` como evidência de que o gate funciona, e tratar como resultado esperado da demonstração negativa.
Se o comando acusar que a origem `src` não existe na árvore da atividade, reproduzir o mesmo gate com a raiz de coleta correta: `pytest 2-code --cov=2-code --cov-report=term-missing --cov-fail-under=80`.

**Passo 9.** Demonstrar o gate negativo de propósito, provando o bloqueio.
Comando: rodar o Passo 8 após comentar um teste.
Saída esperada: mensagem de cobertura insuficiente e `exit=1`.
Critério de falha: aprovação com lacuna. O que fazer: reavaliar a configuração antes de qualquer outra etapa.
Rollback: descomentar o teste removido.

**Passo 10.** Medir a duração da suíte.
Comando: `pytest 2-code --durations=5`
Saída esperada: lista dos cinco testes mais lentos com tempo em segundos.
Critério de falha: teste unitário acima de 1 s. O que fazer: abrir item de correção de fixture e comentar o achado na demo.

**Passo 11.** Rodar duas vezes seguidas para provar determinismo.
Comando: `pytest 2-code -q && pytest 2-code -q`
Saída esperada: mesmo resultado nas duas execuções.
Critério de falha: resultado diferente. O que fazer: classificar como instabilidade e não prosseguir para o CI.

**Passo 12.** Abrir o workflow de CI.
Comando: `cat .github/workflows/ci.yml` na raiz da atividade, ou abrir o arquivo no editor.
Saída esperada: passo `pytest --cov=src --cov-report=term-missing --cov-fail-under=80` e serviço `postgres:16` declarado.
Critério de falha: passo de teste ausente. O que fazer: não há gate sem workflow; reportar como pendência de implantação.

**Passo 13.** Explicar o required check.
Clique esperado: na interface do provedor de repositório, abrir os detalhes do check do pull request e mostrar a regra de proteção da branch.
Critério de falha: regra não configurada. O que fazer: registrar o item como próximo passo de implantação e mostrar a configuração do workflow como prova de que a parte de código está pronta.

**Passo 14.** Explicar o estágio separado do E2E.
Clique esperado: alternar entre os jobs do workflow e apontar onde o E2E roda fora do caminho crítico do merge.
Critério de falha: E2E configurado como required check. O que fazer: explicar o risco e mover para estágio de alerta.

**Passo 15.** Mostrar o standard que formaliza a regra.
Comando: `cat 1-standards/TEST-STRATEGY.md`
Saída esperada: seções de escopo, tabela de decisão, anti-padrões e checklist de 15 itens.
Critério de falha: arquivo ausente. O que fazer: a demo pode continuar, mas a entrega fica incompleta.

**Passo 16.** Percorrer o checklist de adesão ao vivo.
Clique esperado: marcar item a item na tabela do standard, começando pelo teto versionado.
Critério de falha: algum item não verificável por artefato. O que fazer: não marcar e transformar em plano de ação.

**Passo 17.** Apresentar a tabela de modos de falha e recuperação do README.
Clique esperado: seção `Modos de falha`, apontando sintoma, detecção e tempo de recuperação.
Critério de falha: modo de falha sem detecção automática. O que fazer: registrar a lacuna de observabilidade.

**Passo 18.** Fechar com as métricas e o antes versus depois.
Clique esperado: seção `Métricas e SLO` e a tabela de impacto no negócio.
Critério de falha: métrica sem meta ou sem janela de medição. O que fazer: não citar a métrica no fecho.

**Passo 19.** Responder a pergunta prevista do coordenador sobre contornar o gate.
Fala esperada: o teto só muda por decisão registrada, nunca em branch de feature; o rollback do gate é uma mudança de versão comum, versionada.
Critério de falha: não ter resposta para quem tenta rebaixar o teto. O que fazer: remeter ao ADR-022.

**Passo 20.** Encerrar com os próximos passos.
Fala esperada: E2E nos fluxos críticos, mutation testing nos módulos núcleo e sustentação do teto por 12 semanas consecutivas (meta).
Critério de falha: próximo passo sem critério de pronto. O que fazer: reescrever o item em voz alta com critério verificável.
