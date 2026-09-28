# Roteiro de Demo: Estudo de Design Patterns aplicados ao ecossistema

Abra o deck (index.html) e percorra os slides na ordem.

1. Slide de Resumo: abra com o problema de negócio e o blast radius.
2. Slide do ADR: defenda a opção escolhida vs as rejeitadas (trade-offs).
3. Slide de Validação/Rollout: mostre como provamos em produção.
4. Slide de Riscos: apresente o plano de mitigação.

Material de apoio: pdi-praticas-engenharia-clean-code-a4-report.pdf (dossiê completo).

## Pré-requisitos

- Python 3.10 ou superior instalado, confirmado com `python3 --version`.
- Acesso de leitura à pasta da atividade, sem credencial de serviço e sem rede.
- Terminal aberto na raiz da atividade, o que evita caminho relativo quebrado durante a
  apresentação.
- Janela do editor de código disponível para o passo de leitura de código.

## Seed e rollback

- **Seed:** não há banco nem semente de dados. O script `2-code/patterns_demo.py` usa estruturas
  em memória (`dict`, lista de assinantes) e zera tudo a cada execução.
- **Rollback:** nenhuma alteração é persistida; para reverter qualquer passo, basta fechar a
  janela do editor. Caso o `index.html` abra em cache, recarregue com `Ctrl + Shift + R`.

## Passos da demo

1. **Confirmar o ambiente.** Comando: `python3 --version`. Saída esperada: linha iniciada por
   `Python 3.10` ou superior. Critério de falha: comando não encontrado. Ação: abortar a demo e
   usar a máquina de reserva; não tentar instalar pacote durante a apresentação.

2. **Listar a estrutura da atividade.** Comando: `find . -name '*.md' | sort`. Saída esperada:
   os arquivos `.md` da atividade, incluindo `README.md`, `1-standards/DESIGN-PATTERNS-NOTES.md`
   e os da pasta `7-apresentacao`. Critério de falha: diretório errado. Ação: voltar para a raiz
   da atividade antes de continuar.

3. **Executar o script dos padrões.** Comando: `python3 2-code/patterns_demo.py`. Saída esperada:
   `ouvinte: {'id': 1}` na primeira linha (event do bus) e `smart` na segunda (estratégia
   selecionada). Critério de falha: qualquer `Traceback` ou código de saída diferente de zero.
   Ação: ler a última linha do erro, corrigir e reexecutar; se persistir, seguir para o
   diagnóstico no passo 4 e não exibir a tela quebrada.

4. **Diagnosticar falha do script.** Comando: `python3 -u 2-code/patterns_demo.py 2>&1 | tail -5`.
   Saída esperada: as últimas cinco linhas, com a classe da exceção. Critério de falha: erro de
   sintaxe. Ação: abrir o arquivo, conferir a linha indicada e reexecutar o passo 3. Rollback: o
   arquivo não é alterado pelo diagnóstico.

5. **Abrir a port e o adapter.** Clique em `2-code/patterns_demo.py` e destaque `CrmPort` e
   `HubSpotAdapter`. Fala: "A port é o contrato que o núcleo conhece; o adapter é o único lugar
   que sabe como o terceiro funciona." Critério de falha: arquivo não exibido. Ação: usar a busca
   do editor por `class CrmPort`.

6. **Mostrar o `Protocol` sem herança.** Destaque `class CrmPort(Protocol)`. Fala: "Aqui não há
   árvore de tipos: qualquer objeto com o método certo satisfaz o contrato, então o fake de teste
   é trivial." Critério de falha: não é um padrão, é observação; se alguém perguntar sobre
   `ABC`, compare rapidamente com a seção 5 do standard.

7. **Mostrar a factory de estratégias.** Destaque `model_for`. Fala: "Esse é o único ponto
   autorizado a conhecer a regra de escolha. Todas as cadeias condicionais de seleção vêm para
   cá." Critério de falha: existir outro `if` de seleção fora da factory. Ação: apontar o
   anti-padrão correspondente no standard.

8. **Executar a seleção com entrada difícil.** Comando: `python3 -c "import sys; sys.path.insert(0,'2-code'); from patterns_demo import model_for; print(model_for({'hard': True}).complete(None))"`.
   Saída esperada: `smart`. Critério de falha: `cheap`. Ação: verificar a chave `hard` no
   dicionário de entrada; a correção é no dado, não na factory.

9. **Executar a seleção com entrada simples.** Comando: a mesma linha do passo 8 com `{'hard': False}`.
   Saída esperada: `cheap`. Critério de falha: `smart`. Ação: repetir o diagnóstico do passo 8.
   Juntos, os passos 8 e 9 são o teste de mesa da tabela de decisão.

10. **Mostrar o bus de eventos.** Destaque `Bus`, `on` e `emit`. Fala: "O emissor não conhece
    quem ouve. Isso é o Observer em versão mínima." Critério de falha: pergunta sobre ordem.
    Ação: responder com a invariante: ordem não é garantida e nenhuma regra depende dela.

11. **Adicionar um observador ao vivo.** Comando: `python3 -c "import sys; sys.path.insert(0,'2-code'); from patterns_demo import Bus; b=Bus(); b.on('lead.created', lambda p: print('auditoria', p)); b.on('lead.created', lambda p: print('cache', p)); b.emit('lead.created', {'id': 7})"`.
    Saída esperada: `auditoria {'id': 7}` seguido de `cache {'id': 7}`. Critério de falha: só um
    observador executa. Ação: conferir se ambos foram registrados antes do `emit`.

12. **Sabotar um observador.** Comando: variante do passo 11 em que o primeiro observador lança
    `raise RuntimeError('falhou')`. Saída esperada: a falha aparece e o emissor não é afetado no
    desenho. Critério de falha: o desenho atual propaga a exceção. Ação: explicar que a versão de
    produção isola o erro dentro do observador, com retry e log, e que esse teste de sabotagem é
    o critério de aceite do comportamento.

13. **Abrir o standard.** Clique em `1-standards/DESIGN-PATTERNS-NOTES.md` e role até a tabela de
    decisão. Fala: "Aqui está o contrato social do time: se X e Y, então Z, com exceção
    declarada." Critério de falha: tempo acima de 30 segundos procurando. Ação: usar a busca por
    `## 4. Tabela de decisão`.

14. **Mostrar a regra de contenção.** Destaque a seção 1, não-escopo. Fala: "Padrão só entra onde
    há variação real. Isso está escrito para o revisor poder dizer não." Critério de falha:
    ninguém ligar o não-escopo ao risco de over-engineering. Ação: citar o slide de riscos.

15. **Mostrar o anti-padrão do adapter-alias.** Destaque a seção 7. Fala: "Adapter que só repassa
    a chamada não traduz erro nem idempotência, então ele mantém o vazamento de abstração."

16. **Mostrar a telemetria.** Destaque a seção 8 e a coluna de cardinalidade. Fala: "Rótulo com
    identificador de pedido destrói o painel e o orçamento de armazenamento. O conjunto de
    rótulos é fixo e revisado junto com o ADR." Critério de falha: pergunta sobre métrica que não
    existe. Ação: classificar como (meta) e registrar como pendência de instrumentação.

17. **Abrir o ADR-024 no README.** Clique em `README.md` e destaque a linha do Singleton rejeitado.
    Fala: "Registrar o que não foi escolhido evita reabrir a discussão toda revisão."

18. **Mostrar a matemática.** Destaque a seção de matemática da solução. Fala: "Com seis
    fornecedores e quatro módulos, saímos de 24 pontos de toque para 10, uma redução de 58,3 por
    cento, e a chance de erro por mudança cai de 62,3 para 15 por cento." Critério de falha:
    alguém pedir o dado real. Ação: declarar que são parâmetros de exemplo e que a medição começa
    no primeiro onboarding pós-piloto.

19. **Mostrar o checklist de domínio.** Role até a seção final do `README.md`. Fala: "Quinze
    itens que o sênior confere antes de dizer pronto. Se eu não respondo, o padrão está no papel e
    não no código."

20. **Abrir o roteiro de domínio.** Clique em `7-apresentacao/ROTEIRO-DOMINIO.md`. Fala: "As
    perguntas adversariais já estão com resposta curta, inclusive a de negócio, para a defesa não
    depender de material aberto."

21. **Fechar com métricas e próximos passos.** Volte ao deck, slide final. Fala: "O padrão só
    existe quando aparece em PR, em métrica e em onboarding medido."

22. **Encerrar e limpar.** Comando: fechar o terminal. Saída esperada: nenhuma sessão aberta.
    Critério de falha: processo pendurado. Ação: `Ctrl + C` na janela correspondente. Rollback:
    nenhum arquivo foi modificado durante a demo.
