# Roteiro de Demo: Refatoração de Módulo Legado com SOLID e Clean Architecture

Abra o deck (index.html) e percorra os slides na ordem.

## Pré-requisitos

- Python 3.10 ou superior no `PATH`.
- Diretório de trabalho: `atividade-1/2-code/`.
- Sem variável `DB` definida, porque é exatamente isso que prova a independência de infraestrutura.
- Nenhum serviço de banco, SMTP ou CRM precisando estar no ar.

## Seed

```bash
python3 -c "print('seed ok: 0 dependencia de rede')"
```

Saída esperada: `seed ok: 0 dependencia de rede`.

Critério de falha: qualquer mensagem de módulo não encontrado. Se o Python não for 3.10+, os `Protocol` do exemplo não se comportam como esperado; corrija o interpretador antes de continuar.

## Passos

1. Abra o arquivo do legado e mostre o método `run()`.
   Comando: `cat before_campaign_service.py`
   Saída esperada: 10 linhas com `psycopg2`, `f"SELECT ... {camp.id}"`, `requests.post` e `smtplib.sendmail` no mesmo método.
   Critério de falha: arquivo vazio ou inexistente.
   Se der errado: confirme que você está em `atividade-1/2-code/`.

2. Aponte o vetor de injection com a linha exata.
   Comando: `grep -n "f\"SELECT" before_campaign_service.py`
   Saída esperada: linha 6 com a interpolação de `{camp.id}`.
   Critério de falha: nenhum resultado.
   Se der errado: não continue a demo; sem essa linha o diagnóstico não tem peça de acusação.

3. Mostre que o legado não tem teste.
   Comando: `ls test_* 2>/dev/null || echo "nenhum teste"`
   Saída esperada: `nenhum teste`.
   Critério de falha: aparecer teste do legado, o que invalidaria a afirmação de 0 por cento de cobertura.

4. Abra o módulo refatorado e mostre as portas.
   Comando: `grep -n "Protocol" after_campaign_service.py`
   Saída esperada: as portas `LeadRepository` e `Notifier` declaradas com `Protocol`.
   Critério de falha: ausência de `Protocol`, o que indicaria que a inversão de dependência não foi feita.

5. Mostre o construtor recebendo as abstrações.
   Comando: `grep -n "repo\|notifier" after_campaign_service.py`
   Saída esperada: atributos do serviço vindos de parâmetros, não de `psycopg2.connect`.
   Critério de falha: qualquer `connect(` dentro da classe de serviço.

6. Rode o teste do serviço.
   Comando: `python3 -m pytest after_campaign_service.py -q`
   Saída esperada: 1 coletado, 1 aprovado, em menos de 1 segundo.
   Critério de falha: teste pedindo rede, banco ou variável de ambiente.
   Se der errado: rode com `python3 after_campaign_service.py` para ver o erro de sintaxe completo e reporte, não esconda.

7. Prove que a suíte não toca em infraestrutura.
   Comando: `grep -n "psycopg2\|smtplib" after_campaign_service.py || echo "zero dependencia de infra"`
   Saída esperada: `zero dependencia de infra`.
   Critério de falha: aparecer import de driver no módulo refatorado, violação de DIP.

8. Rode o teste duas vezes e compare a saída.
   Comando: `python3 -m pytest after_campaign_service.py -q && python3 -m pytest after_campaign_service.py -q`
   Saída esperada: mesma contagem nas duas execuções, sem teste intermitente.
   Critério de falha: resultados diferentes entre execuções, sinal de dependência de relógio ou aleatoriedade não semeada.

9. Conte as responsabilidades do método legado.
   Comando: `grep -c "requests.post\|smtplib\|psycopg2\|print" before_campaign_service.py`
   Saída esperada: 4 ocorrências, batendo com 4 responsabilidades por classe.
   Critério de falha: contagem diferente de 4, o que obriga a ajustar a métrica de acoplamento citada no deck.

10. Meça o tamanho das classes do módulo novo.
    Comando: `python3 -c "import inspect, after_campaign_service as m; print(max(len(inspect.getsource(getattr(m, n)).splitlines()) for n in dir(m) if inspect.isclass(getattr(m, n))))"`
    Saída esperada: valor menor que 45 linhas para a maior classe.
    Critério de falha: classe acima de 45 linhas, o que derruba o teto do standard.

11. Abra o standard de adesão e percorra a tabela de decisão.
    Arquivo: `1-standards/SOLID-BEFORE-AFTER.md`
    Saída esperada: tabela "Se / E / Então" com sete linhas e a seção de anti-padrões.
    Critério de falha: tabela vazia ou seção de anti-padrões ausente.
    Se der errado: leia apenas a regra canônica e a tabela de decisão; são o núcleo defensável.

12. Mostre o exemplo numérico fechado.
    Arquivo: `1-standards/SOLID-BEFORE-AFTER.md`, seção "Exemplo numérico".
    Saída esperada: 14 classes mínimas, instabilidade de 0,8 para 0, 510 linhas a cobrir, ganho de 239 s por pull request.
    Critério de falha: conta sem parâmetro declarado.
    Se der errado: declare os parâmetros em voz alta, porque número sem parâmetro não é evidência.

13. Apresente o ADR-021 com as alternativas descartadas.
    Arquivo: `README.md`, seção "Decisão Arquitetural (ADR)".
    Saída esperada: três opções na matriz, sendo uma escolhida e duas rejeitadas com motivo.
    Critério de falha: matriz sem coluna de decisão.

14. Percorra os invariantes.
    Arquivo: `README.md`, seção "Invariantes".
    Saída esperada: dez invariantes, cada um com a violação correspondente.
    Critério de falha: invariante sem violação nomeada, o que impede teste.
    Se der errado: selecione os três primeiros, que já cobrem transação, injection e dependência de infraestrutura.

15. Mostre a tabela de modos de falha.
    Arquivo: `README.md`, seção "Modos de falha".
    Saída esperada: oito linhas com sintome, causa raiz, detecção, mitigação e tempo de recuperação.
    Critério de falha: linha sem detecção, que caracteriza falha surpresa.

16. Apresente o SLO e o orçamento de erro.
    Arquivo: `README.md`, seção "SLO e orçamento de erro".
    Saída esperada: três SLIs, janela de 30 dias e a conta de 120 campanhas por mês resultando em tolerância zero na prática.
    Critério de falha: SLI sem meta ou sem janela de medição.
    Se der errado: use apenas o SLI de consistência e o gate de cobertura.

17. Simule o rollback na fala.
    Comando: `grep -n "use_new_campaign_service" README.md`
    Saída esperada: menção da flag como única chave de corte, com retorno sem deploy.
    Critério de falha: rollback que exige deploy, o que derruba a promessa de recuperação em minutos.
    Se der errado: declare a limitação e registre como pendência antes da demonstração.

18. Aponte o plano de sombra e o corte.
    Arquivo: `README.md`, seção "Plano de Validação e Rollout".
    Saída esperada: 1 sprint de sombra, reconciliação diária, corte abaixo de 0,1 por cento com teto de 5 divergências por dia.
    Critério de falha: corte só percentual, sem teto absoluto.

19. Feche pelo checklist de domínio.
    Arquivo: `README.md`, seção "Checklist de domínio".
    Saída esperada: 15 itens verificáveis.
    Critério de falha: item subjetivo, do tipo "código limpo", que não pode ser verificado.

20. Encerre com as métricas e os próximos passos.
    Comando: `wc -w README.md 1-standards/SOLID-BEFORE-AFTER.md ../7-apresentacao/*.md`
    Saída esperada: contagem consistente com o material entregue.
    Critério de falha: arquivo faltando na contagem.
    Se der errado: apresente pelo menos README e standard, que são a base da defesa.

## Rollback da demo

Nenhum passo altera arquivo, cria serviço ou grava dado. Se qualquer passo corromper o material, restaure apenas com `git checkout -- _inbox/PDI/02-praticas-engenharia-clean-code/atividade-1/` e recomece pelo passo 1.

Material de apoio: pdi-praticas-engenharia-clean-code-a1-report.pdf (dossiê completo).
