# Core Web Vitals: Diagnóstico e Plano

## Linha de base

| Métrica | Valor | Limite | Status |
|--------|-------|--------|--------|
| LCP | 4.1s | 2.5s | FAIL |
| INP | 410ms | 200ms | FAIL |
| CLS | 0.22 | 0.1 | FAIL |

Leitura: as três estão reprovadas ao mesmo tempo, o que indica que não existe um único gargalo comum. Cada métrica tem causalidade própria e, por isso, o diagnóstico é conduzido em três trilhas paralelas com verificação independente.

## Plano

1. LCP: preconnect + fetchpriority=high + AVIF.
2. INP: chunks + debounce.
3. CLS: aspect-ratio + min-height.

## Método de diagnóstico

Ordem obrigatória de execução, porque cada passo alimenta o próximo:

1. **Congelar a linha de base em campo.** Rodar `field_cwv.py` para a URL e formato de aparelho de interesse e registrar os percentis 75. Sem esse número, qualquer comparação posterior é opinião.
2. **Reproduzir em laboratório.** Abrir a rota no Lighthouse com dispositivo móvel e conexão simulada lenta, anotando o elemento apontado como LCP e a lista de `long task`.
3. **Atribuir causa.** Para cada métrica, caminhar a árvore de decisão abaixo até chegar a uma causa acionável.
4. **Corrigir em ordem de ROI (ADR-034).** LCP primeiro, depois INP, depois CLS, uma frente por release para o campo conseguir isolar o efeito.
5. **Confirmar em campo.** Re-rodar a coleta após o ciclo de 28 dias e comparar com a linha de base congelada.

## Árvore de decisão por métrica

### LCP

```text
LCP > 2500 ms
  |
  +-- TTFB > 800 ms?
  |     +-- sim: problema de servidor (cache, render, cascata de API)
  |     +-- não: baixo risco de rede, ir para o próximo ramo
  |
  +-- elemento LCP é imagem?
  |     +-- sim: há priority + preconnect + formato moderno?
  |     |        +-- sim: medir decode/render e conferir sizes/srcset
  |     |        +-- não: aplicar prioridade e preconnect (correção principal)
  |     +-- não: é texto ou fundo? conferir bloqueio por CSS/JS
  |
  +-- recurso compete com script não crítico?
        +-- sim: adiar script e devolver banda ao elemento LCP
        +-- não: revisar CDN e tamanho do recurso
```

### INP

```text
INP > 200 ms
  |
  +-- existe long task > 50 ms no caminho do clique?
  |     +-- sim: handler longo? fatiar com yield
  |     |        import estático de componente pesado? dynamic import
  |     +-- não: checar input delay (evento registrado tardiamente)
  |
  +-- o atraso vem de layout thrash ou de trabalho de terceiro?
  |     +-- sim: agrupar leituras/escritas de DOM e adiar terceiro
  |     +-- não: checar debounce e trabalhos de rede disparados no handler
  |
  +-- efeito aparece só em dispositivo básico?
        +-- sim: é esperado; tratar pelo orçamento de CPU, não só pelo bundle
```

### CLS

```text
CLS > 0,1
  |
  +-- há elemento acima do fold sem dimensão declarada?
  |     +-- sim: adicionar width/height ou aspect-ratio
  |     +-- não: checar inserção tardia de conteúdo
  |
  +-- há banner/card inserido via JS depois do paint?
  |     +-- sim: reservar espaço com min-height antes da injeção
  |     +-- não: checar troca de fonte e scrollbar
  |
  +-- o shift é provocado pelo usuário?
        +-- sim: deslocamento logo após interação não deve ser contado;
        |        se for, revisar o componente que responde ao clique
        +-- não: contar na janela e corrigir a origem geométrica
```

## Roteiro de coleta

`field_cwv.py` consulta a API de CrUX e devolve os percentis 75 para as três métricas no formato de aparelho informado. O script é a fonte da linha de base e da confirmação final; sua saída alimenta a tabela de linha de base deste documento e o registro histórico no banco.

Pontos de atenção operacional:

- A consulta é por URL exata; variação de `www`, barra final ou `http`/`https` gera série diferente e invalida a comparação.
- Resposta sem métrica significa volume de amostra insuficiente na origem. Nesse caso, o diagnóstico passa a usar RUM próprio, e isso precisa ficar registrado na conclusão.
- A janela de 28 dias faz a série ter memória longa: melhorias recentes demoram a aparecer por completo. O gate de regressão usa laboratório por esse motivo.

## Registro histórico do diagnóstico

Para que o diagnóstico não seja um PDF perdido, a linha de base e cada medição posterior são persistidas:

```sql
insert into public.cwv_metric_sample
  (url_id, collected_on, form_factor, lcp_p75_ms, inp_p75_ms, cls_p75, sample_count, source)
values
  ($1, current_date, $2, $3, $4, $5, $6, 'crux')
on conflict (url_id, collected_on, form_factor, source)
do update set lcp_p75_ms   = excluded.lcp_p75_ms,
              inp_p75_ms   = excluded.inp_p75_ms,
              cls_p75      = excluded.cls_p75,
              sample_count = excluded.sample_count;
```

A cláusula `on conflict` existe porque a coleta pode ser reexecutada no mesmo dia (script agendado mais execução manual). Sem a chave única, a série duplicaria e a leitura de tendência mentiria.

Consulta de tendência usada no relatório:

```sql
select collected_on,
       lcp_p75_ms,
       inp_p75_ms,
       cls_p75,
       case when lcp_p75_ms <= 2500 and inp_p75_ms <= 200 and cls_p75 <= 0.1
            then 'bom' else 'fora do limite' end as status
  from public.cwv_metric_sample
 where url_id = $1
   and collected_on >= current_date - 28
 order by collected_on desc;
```

Consulta de cobertura, para responder "a rota crítica tem amostra suficiente?":

```sql
select form_factor,
       count(*) as dias_com_dado,
       max(sample_count) as maior_amostra
  from public.cwv_metric_sample
 where url_id = $1
   and collected_on >= current_date - 28
 group by form_factor
 order by dias_com_dado desc;
```

Interpretação: menos de 20 dias com dado em 28 (Exemplo numérico com os parâmetros declarados) significa série fraca; a conclusão do diagnóstico precisa dizer isso em voz alta em vez de apresentar p75 como se fosse estável.

## Orçamento de descoberta: o que medir em cada passo

| Passo | Métrica do passo | Saída esperada | Se falhar |
| --- | --- | --- | --- |
| Linha de base | p75 das três métricas | tabela preenchida | sem campo: usar RUM e registrar |
| Auditoria de lab | elemento LCP apontado | nome do elemento culpado | sem apontamento: revisar escopo da auditoria |
| Perfil de JS | maior `long task` | duração em ms | perfil vazio: revisar coletor |
| Diff de HTML | atributos de prioridade e dimensão | diff mínimo entre versões | diff enorme: isolar template |
| Pós-deploy | orçamento no CI | gate verde | gate vermelho: não mesclar |
| Confirmação | p75 em 28 dias | comparação com base | sem melhoria: reabrir causa |

## Conclusão do diagnóstico (status atual)

As três métricas reprovadas têm causa atribuída e correção mapeada: LCP por ausência de prioridade e de conexão pré-aberta mais imagem pesada, INP por handler síncrono no caminho do clique, CLS por cards sem reserva de geometria. A ordem de execução é a do ADR-034 e a confirmação é sempre em campo, após o ciclo de 28 dias, com a linha de base congelada como referência.

Nenhuma correção é considerada fechada sem três evidências: o gate verde no CI, a leitura de laboratório apontando o alvo esperado e a comparação de campo dentro dos limites de 2,5 s, 200 ms e 0,1.
