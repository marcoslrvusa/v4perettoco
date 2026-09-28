# Roteiro de Demo: Mapeamento de Domínios com Domain-Driven Design (DDD)

Abra o deck (index.html) e percorra os slides na ordem.

Pré-requisito: Python 3.10+ no PATH, terminal na pasta da atividade e o arquivo `2-code/domain_models.py` presente. Nenhum serviço externo é necessário: a demo é local e determinística.

Rollback: nenhum arquivo é alterado durante a demo. Se algo sair do padrão, basta fechar o terminal e reabrir a pasta; nada de estado fica gravado.

1. Slide de Resumo: abra com o problema de negócio e o blast radius.
   - Saída esperada: o público entende que são 4 squads, 3 modelos de Contato e 5 toques por mudança de regra.
   - Critério de falha: ninguém consegue repetir o problema em uma frase.
   - Se falhar: volte ao slide 1 e leia a tabela de partida em voz alta.

2. Slide do ADR: defenda a opção escolhida vs as rejeitadas (trade-offs).
   - Saída esperada: a matriz de tradeoffs é lida por completo, com ganho e custo de cada alternativa.
   - Critério de falha: a discussão vira "DDD é bom" sem citar o custo de governança.
   - Se falhar: cite o ADR-023 e diga que governança é o preço aceito, enquanto acoplamento não era.

3. Slide de Validação/Rollout: mostre como provamos em produção.
   - Saída esperada: as 4 etapas com critério de aceite e gate de CI.
   - Critério de falha: alguém pergunta "e se o glossário divergir do código?".
   - Se falhar: aponte o gate de dependência entre contextos que bloqueia o merge.

4. Slide de Riscos: apresente o plano de mitigação.
   - Saída esperada: cada risco com mitigação correspondente.
   - Critério de falha: o risco "mapa vira teoria" fica sem resposta.
   - Se falhar: mostre o item da revisão de código que exige mapear antes de aprovar.

5. Abra o terminal na pasta da atividade e confirme a estrutura:
   - Comando: `find . -name '*.md' -type f | sort`
   - Saída esperada: `README.md`, `1-standards/DOMAIN-MAP.md` e os `.md` de `7-apresentacao/`.
   - Critério de falha: algum arquivo faltando.
   - Se falhar: verifique se você está na raiz da atividade e não em outra trilha.

6. Conte a volumetria da atividade para provar que o material existe:
   - Comando: `find . -name '*.md' -exec wc -w {} + | tail -1`
   - Saída esperada: um total de palavras maior que zero e a linha `total`.
   - Critério de falha: total menor que a meta combinada.
   - Se falhar: rode de novo na pasta correta antes de continuar.

7. Abra `1-standards/DOMAIN-MAP.md` e mostre a tabela de Bounded Contexts:
   - Comando: `sed -n '1,40p' 1-standards/DOMAIN-MAP.md`
   - Saída esperada: as quatro linhas CRM, Campaign, Agent e Billing com raiz e filhos.
   - Critério de falha: algum contexto sem raiz de agregado declarada.
   - Se falhar: isso é um bug do material; anote e sinalize à coordenação ao final.

8. Mostre a regra canônica com a fórmula de ampliação de mudança:
   - Comando: `grep -n 'A =' 1-standards/DOMAIN-MAP.md`
   - Saída esperada: a fórmula $A = C_{tocados} / C_{dono}$ com meta $A = 1$.
   - Critério de falha: a fórmula aparece sem exemplo numérico junto.
   - Se falhar: abra o bloco "Exemplo numérico" logo abaixo da fórmula.

9. Explique o caso do lead não qualificado:
   - Comando: `grep -n 'DomainError' 2-code/domain_models.py`
   - Saída esperada: `raise DomainError("lead nao qualificado nao pode ser contatado")`.
   - Critério de falha: a exceção não aparece no arquivo.
   - Se falhar: o código não reflete a invariante; interrompa a demo e registre.

10. Execute a invariante de agregado ao vivo:
    - Comando:
      ```bash
      python3 - <<'PY'
      import sys
      sys.path.insert(0, "2-code")
      from domain_models import Lead, DomainError
      lead = Lead(id="1", email="a@b.c")
      print(lead.qualified)
      try:
          lead.contact("email")
      except DomainError as exc:
          print("OK:", exc)
      lead.qualified = True
      print(type(lead.contact("email")).__name__)
      PY
      ```
    - Saída esperada: `False`, depois `OK: lead nao qualificado nao pode ser contatado`, depois `Contact`.
    - Critério de falha: qualquer linha diferente, inclusive sem a exceção.
    - Se falhar: verifique a versão do Python e se o caminho `2-code` está correto; não siga sem a exceção aparecer.

11. Mostre o evento de domínio e o seu tipo:
    - Comando: `cat 2-code/domain_events.py`
    - Saída esperada: a dataclass `DomainEvent` e `LeadCreated` com tipo `crm.lead.created`.
    - Critério de falha: o evento não tem identificador nem carimbo de tempo.
    - Se falhar: explique que sem `event_id` não existe deduplicação no consumidor.

12. Aponte a forma do contrato (raiz + valor primitivo):
    - Comando: `grep -A3 'class LeadCreated' 2-code/domain_events.py`
    - Saída esperada: apenas `email` como dado do payload.
    - Critério de falha: o payload carrega objeto interno do agregado.
    - Se falhar: isso é acoplamento disfarçado; use como exemplo do que reprovar em revisão.

13. Leia a tabela de decisão do standard:
    - Comando: `grep -n 'Se | E | Então' -A6 1-standards/DOMAIN-MAP.md || sed -n '/## Tabela de decisão/,/^## /p' 1-standards/DOMAIN-MAP.md`
    - Saída esperada: linhas do tipo "se precisa de transação conjunta, então mesmo agregado".
    - Critério de falha: alguma linha vaga, sem condição e ação.
    - Se falhar: troque por uma pergunta ao público e resolva na lâmina.

14. Percorra os anti-padrões como lista de reprovação de revisão:
    - Comando: `sed -n '/## Anti-padrões/,/## Telemetria/p' 1-standards/DOMAIN-MAP.md | head -30`
    - Saída esperada: ao menos 10 itens, começando por foreign key cruzando fronteira.
    - Critério de falha: menos de 10 itens listados.
    - Se falhar: cite de memória os três primeiros: FK cruzada, coluna só para o vizinho e entidade filha exposta.

15. Mostre o checklist de adesão usado na revisão de código:
    - Comando: `sed -n '/## Checklist de adesão/,$p' 1-standards/DOMAIN-MAP.md`
    - Saída esperada: 14 itens numerados.
    - Critério de falha: checklist sem gate de CI.
    - Se falhar: reforce o item "gate de dependência entre contextos está em verde".

16. Volte ao deck e abra o slide de matemática:
    - Clique: slide "Matemática da solução".
    - Saída esperada: quatro contas fechadas, com 96 h/trimestre como resultado do ganho.
    - Critério de falha: o público não sabe de onde vem o 96.
    - Se falhar: refaça a conta na lousa: 12 x 4 x 2 h = 96 h.

17. Abra o slide de falha e recuperação:
    - Clique: slide "Falha e recuperação".
    - Saída esperada: a tabela com sintoma, detecção, mitigação e recuperação.
    - Critério de falha: falta a coluna de detecção.
    - Se falhar: cite o exemplo do ETL que falha após migração sem dono de schema.

18. Abra a matriz de tradeoffs e leia a coluna de decisão:
    - Clique: slide "Tradeoffs (matriz)".
    - Saída esperada: 6 linhas com ganho, custo e decisão.
    - Critério de falha: alguma linha sem custo declarado.
    - Se falhar: lembre que toda opção escolhida tem preço e o preço do DDD é governança.

19. Feche com as métricas antes e depois:
    - Clique: slide "Fecho com métricas".
    - Saída esperada: 0 para 4 contextos, 3 para 1 modelo, 5 para 1 em $A$.
    - Critério de falha: alguma linha sem valor de antes ou de depois.
    - Se falhar: retome o slide 2 e refaça a contagem do problema.

20. Encerre com os próximos passos e donos:
    - Clique: slide "Próximos passos e donos".
    - Saída esperada: 5 itens numerados com responsável e prazo.
    - Critério de falha: algum item sem dono.
    - Se falhar: não encerre; distribua os itens na hora e anote no quadro da equipe.

21. Verificação final de integridade do material:
    - Comando: `grep -rn $'\u2014' . --include='*.md' ; grep -rnE ' \u2013 ' . --include='*.md'`
    - Saída esperada: nenhuma saída (vazia).
    - Critério de falha: qualquer arquivo listado.
    - Se falhar: trate como pendência de revisão e sinalize antes de apresentar.

Material de apoio: pdi-praticas-engenharia-clean-code-a3-report.pdf (dossiê completo).
