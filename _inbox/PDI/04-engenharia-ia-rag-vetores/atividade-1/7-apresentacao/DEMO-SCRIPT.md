# Roteiro de Demo: Fundamentos de IA Generativa (NVIDIA DLI) aplicados a RAG

Abra o deck (index.html) e percorra os slides na ordem.

Duração estimada: 12 minutos de fala, 5 minutos de evidência no terminal. Pré-requisito: repositório clonado, dependências instaladas e corpus de teste já indexado uma vez.

1. Slide de Resumo: abra com o problema de negócio e o blast radius.
   - Comando: nenhum, é fala.
   - Saída esperada: o coordenador entende que o entregável é baseline reproduzível, não protótipo.
   - Se falhar: se pedirem número, cite faithfulness >= 0,8 (meta) e golden set de 50 pares.

2. Slide do ADR: defenda a opção escolhida vs as rejeitadas (trade-offs).
   - Comando: nenhum.
   - Saída esperada: ADR-041 com chunk 512, overlap 64, top-20 e rerank para 5.
   - Se falhar: se questionarem o overlap, mostre a conta de 14 por cento a mais de vetores paga uma vez na indexação.

3. Slide de Modelo mental: percorra os 5 passos do pipeline.
   - Comando: nenhum.
   - Saída esperada: a plateia descreve o caminho do texto até a resposta sem usar jargão.
   - Se falhar: use a analogia da biblioteca do relatório: token é a letra, embedding é o cartão de endereço, similaridade é a régua.

4. Slide de Arquitetura: aponte a separação entre caminho frio (fila de ingestão) e caminho quente (consulta).
   - Comando: nenhum.
   - Saída esperada: pergunta sobre SLO de ingestão é respondida com "não afeta a consulta".
   - Se falhar: reforce que fila existe justamente para isolar os dois SLO.

5. Slide de Matemática: feche a conta do índice na lousa.
   - Comando: `python3 -c "print(1000000//(512-64), 1000000//512)"`
   - Saída esperada: `2232 1953`.
   - Critério de falha: número diferente do slide.
   - Se falhar: recalcule ao vivo e corrija o slide depois da apresentação.

6. Slide de Validação/Rollout: mostre como provamos em produção.
   - Comando: `python3 2-code/rag_baseline.py --self-test`
   - Saída esperada: todos os casos de borda aprovados (texto vazio, mínimo, limite, acentuação).
   - Critério de falha: qualquer caso reprovado.
   - Se falhar: não siga para a comparação, porque a base do pipeline está quebrada.

7. Execução do pipeline: rode a busca em corpus de teste.
   - Comando: `python3 2-code/rag_baseline.py --pergunta "como funciona o chunking"`
   - Saída esperada: lista de trechos com score e a resposta citando o trecho.
   - Critério de falha: resposta sem citação de trecho.
   - Se falhar: mostre o prompt de `answer()` e a instrução de citação obrigatória.

8. Comparação com similaridade pura: rode o modo sem rerank.
   - Comando: `python3 2-code/rag_baseline.py --pergunta "como funciona o chunking" --sem-rerank`
   - Saída esperada: os mesmos 20 candidatos em ordem bruta, com ruído entre os 5 primeiros.
   - Critério de falha: se a ordem for idêntica, o rerank não está sendo aplicado.
   - Se falhar: verifique se o parâmetro `--sem-rerank` está chegando até `retrieve()`.

9. Slide de Métricas: apresente o gate de CI.
   - Comando: `python3 2-code/rag_baseline.py --golden-set`
   - Saída esperada: faithfulness média e aprovação ou reprovação do build.
   - Critério de falha: média abaixo de 0,8.
   - Se falhar: o build não publica, é fail-closed, e a investigação abre em cima da pergunta que regrediu.

10. Slide de Falha e recuperação: escolha um modo de falha da tabela e percorra detecção, mitigação e tempo de recuperação.
    - Comando: nenhum.
    - Saída esperada: a plateia consegue nomear a métrica que detecta cada falha.
    - Se falhar: cite idade da fila para documento invisível e variância do score para vetor congelado.

11. Slide de Invariantes: leia as quatro invariantes e a violação de cada uma.
    - Comando: nenhum.
    - Saída esperada: consenso de que vetor sem normalização invalida o threshold 0,82.
    - Se falhar: rode a demonstração de cosseno com vetor não normalizado e mostre o score subindo por comprimento.

12. Slide de Riscos: apresente o plano de mitigação.
    - Comando: nenhum.
    - Saída esperada: cada risco com controle e dono nomeados.
    - Se falhar: não avance, risco sem dono é a objeção mais comum de coordenação.

13. Slide de Esforço e custo: mostre os quatro parâmetros da planilha.
    - Comando: nenhum.
    - Saída esperada: custo por consulta derivado, não estimado por palpite.
    - Se falhar: deixe a planilha em anexo no dossiê e reagende a sessão de custo.

14. Slide de Riscos: retome apenas se houver objeção de negócio.
    - Comando: nenhum.
    - Saída esperada: aceite da mitigação de contexto irrelevante com rerank.
    - Se falhar: registre a objeção como pendência da ADR-041.

15. Slide de Próximos Passos: ligue a atividade 04-A2 ao baseline entregue.
    - Comando: nenhum.
    - Saída esperada: percepção de que híbrido e avaliação RAGAS herdam golden set e runbook.
    - Se falhar: reforce que nada desta atividade será retrabalhado na seguinte.

16. Fecho: retome métricas e pendência de homologação.
    - Comando: nenhum.
    - Saída esperada: status final entendido como desenvolvido e em homologação.
    - Se falhar: repita que publicação só ocorre após aprovação de revisão.

17. Backup técnico: abra o standard `1-standards/DATA-PIPELINE-AI.md` se pedirem detalhe de indexação.
    - Comando: `wc -l _inbox/PDI/04-engenharia-ia-rag-vetores/atividade-1/1-standards/DATA-PIPELINE-AI.md`
    - Saída esperada: linha contando o standard completo.
    - Se falhar: mostre a seção de SQL com índice HNSW direto do arquivo.

18. Encerramento: confirme as entregas listadas no README.
    - Comando: `ls 1-standards 2-code`
    - Saída esperada: `DLI-NOTES.md`, `DATA-PIPELINE-AI.md` e `rag_baseline.py` presentes.
    - Critério de falha: qualquer entrega ausente.
    - Se falhar: não encerre a demo sem a entrega no disco.

Material de apoio: pdi-engenharia-ia-rag-vetores-a1-report.pdf (dossiê completo).
