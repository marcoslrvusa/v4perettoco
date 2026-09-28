# STANDARD: Core Web Vitals (Next.js)

## Escopo e não-escopo

**Escopo**: regras obrigatórias de performance para qualquer rota publicada no portal em Next.js, cobrindo as três métricas de Core Web Vitals (LCP, INP e CLS), o orçamento de entrega por rota, a verificação em laboratório e a confirmação em campo.

**Não-escopo**: SEO on-page, acessibilidade, custo de servidor, padrão visual de componentes e regras de cache de API. Esses temas têm standard próprio; aqui só se entra quando a decisão afetar diretamente uma das três métricas.

## Termos

- **LCP (Largest Contentful Paint)**: tempo até o maior elemento visível do primeiro viewport ser renderizado. Limite bom: 2.500 ms.
- **INP (Interaction to Next Paint)**: latência entre entrada do usuário e pintura seguinte, resumida como percentil 75 das interações. Limite bom: 200 ms.
- **CLS (Cumulative Layout Shift)**: soma dos deslocamentos de layout não provocados, pior janela de sessão. Limite bom: 0,1.
- **Main thread**: única thread de execução do navegador para JavaScript, layout e pintura.
- **`long task`**: task de mais de 50 ms; bloqueia resposta a novas entradas.
- **Campo versus laboratório**: medição com usuários reais (CrUX, RUM) versus medição controlada (Lighthouse). Campo dá o veredito, laboratório dá a causa.
- **Orçamento de performance**: limite quantitativo de bytes, tempo ou pontuação que o pipeline não deixa passar.
- **Elemento LCP**: `img`, `image` de `svg`, `video` com pôster ou primeiro quadro, bloco de texto ou fundo com `url()`.

## Regra canônica

A regra que governa todas as demais: **nenhum commit entra em produção se piorar o orçamento da rota e nenhuma otimização é considerada fechada antes da confirmação em campo.**

Fórmulas de referência:

$LCP = TTFB + t_{fetch} + t_{decode/render}$

$INP \approx t_{input\_delay} + t_{processing} + t_{presentation}$

$CLS = \min\left(1,\ \sum_{janela} \frac{distância}{viewport} \times \frac{área\ afetada}{viewport}\right)$

$t_{rede} = \frac{bytes \times 8}{bandwidth}$

**Exemplo numérico:** rota com TTFB de 1.100 ms, download de 1.200 ms e render de 1.800 ms soma 4.100 ms de LCP. Cortando o TTFB para 400 ms com cache na borda, o download para 500 ms com AVIF e conexão pré-aberta, e o render para 700 ms com dimensão declarada, o total fica 1.600 ms, dentro do limite de 2.500 ms com 900 ms de folga.

## Tabela de decisão

| Se | E | Então | Nunca |
| --- | --- | --- | --- |
| O elemento é o maior do primeiro viewport | ele é imagem | `priority` no `next/image` e `fetchpriority="high"` | aplicar `loading="lazy"` nele |
| O elemento está fora do primeiro viewport | é imagem ou iframe | `loading="lazy"` e dimensão declarada | gastar prioridade de descoberta com ele |
| O recurso vem de outra origem | a origem será usada logo no início | `preconnect` no `<head>` | abrir a origem com request tardio |
| O componente só aparece após interação | chat, mapa, gráfico pesado | `dynamic(() => import(...))` | importar de forma estática no bundle da rota |
| O handler passa de 50 ms de CPU | há trabalho repetível | fatiar com `yield` entre blocos | rodar o trabalho inteiro em uma task |
| O layout tem elemento de altura variável | chega depois do paint | `aspect-ratio` ou `min-height` reservado | inserir acima do fold via JS sem reserva |
| A fonte tem swap de métrica | há risco de troca de caixa | `size-adjust` e estratégia de exibição explícita | deixar o browser escolher por padrão |
| A rota mudou | o CI tem orçamento configurado | rodar a asserção de orçamento | confiar em "parece rápido" |
| O p75 de campo cruzou o limite | existe deploy recente | mitigar primeiro (rollback ou flag) | esperar a janela de 28 dias sem ação |

## Regras por métrica

### LCP

- `next/image` com `priority` apenas no herói; `sizes` precisa refletir o layout real, senão o navegador baixa a imagem errada.
- `preconnect` nas origens de CDN já conhecidas no primeiro paint.
- TTFB tratado no servidor: rota crítica em cache ou render estático; nada de depender de chamada de API cascata no servidor.
- Formato moderno (AVIF com queda para WebP) e dimensões explícitas para evitar redimensionamento no cliente.
- Nenhum script não crítico no caminho do parse até a imagem herói.

### INP

- Code splitting por rota; componentes pesados com `dynamic import`.
- Handlers com debounce (trailing) nas ações digitadas, por exemplo 250 ms.
- Trabalho longo fatiado: `scheduleChunked(work, 8)` em `cwv_fixes.html` mantém fatias de 8 ms, muito abaixo do limiar de 50 ms.
- Em React, uso de `startTransition`/`useDeferredValue` para atualizações que não precisam ser urgentes.
- Leituras e escritas de DOM agrupadas, sem alternância que provoque layout thrash.
- Terceiros (tag manager, chat) carregados com `defer` ou depois do idle.

### CLS

- Toda `<img>` acima do fold com `width`/`height` ou `aspect-ratio`.
- Espaço reservado para cards, anúncios e slots com `min-height`, inclusive quando o dado demora.
- Nada de conteúdo acima do fold injetado por JS tardio sem reserva prévia.
- Fontes com estratégia explícita de exibição e `size-adjust` quando a métrica da fonte difere da fallback.
- Elementos que exigem resposta do usuário (banners) posicionados sem empurrar conteúdo já visível.

## Exemplo numérico de orçamento por rota

**Exemplo numérico:** rota crítica com orçamento de 170 kB gzip de JavaScript e 40 kB de CSS. Bundle atual de 420 kB gzip: excede em 250 kB, que em rede de 1,6 Mbit/s custa 250 × 8 / 1.600 = 1,25 s de transferência adicional. Removendo import estático do componente de chat (180 kB) e adiando biblioteca de gráfico (90 kB), o bundle cai para 150 kB, dentro do orçamento com 20 kB de folga. Folga inferior a 10% do orçamento é considerada zona de risco: qualquer dependência nova estoura o gate.

## Anti-padrões (o que o sênior reprovaria)

1. Marcar tudo como `loading="lazy"`, inclusive o elemento LCP.
2. Declarar `priority` em mais de um elemento por página.
3. Otimizar com base em pontuação de Lighthouse sem nenhum número de campo.
4. Escrever debounce sem limite de tempo (ex.: 2 s), transformando interação em espera.
5. Mover trabalho pesado para `setTimeout(fn, 0)` sem `yield`: ainda é uma task longa.
6. Inserir banner ou card acima do fold por JS sem reserva de espaço.
7. Aceitar melhoria sem re-medir em campo; laboratório não fecha entrega.
8. Criar índice no banco para toda coluna "por via das dúvidas", sem olhar `EXPLAIN`.
9. Publicar métrica sem dizer fonte, formato de aparelho e janela.
10. Deixar orçamento de performance como relatório de dashboard em vez de asserção de pipeline.
11. Usar `offset` profundo para paginar histórico de métrica.
12. Escrever na tabela de métricas direto do cliente sem RLS nem chave de idempotência.

## Telemetria

| Métrica | Fonte | Cardinalidade | Alerta |
| --- | --- | --- | --- |
| LCP p75 (ms) | CrUX e RUM | por origem e formato de aparelho | acima de 2.500 ms em 2 janelas seguidas |
| INP p75 (ms) | CrUX e RUM | por rota (RUM) e por origem (CrUX) | acima de 200 ms em qualquer rota crítica |
| CLS p75 (adimensional) | CrUX e RUM | por rota | acima de 0,1 |
| `long task` por minuto | API de performance no navegador | por rota | acima da linha de base da rota |
| Peso do bundle por rota (kB) | build do CI | por rota | orçamento estourado |
| TTFB p75 (ms) | servidor e RUM | por rota | acima do orçamento de servidor |

Regra de cardinalidade: nunca agrupar evento de RUM por identificador de usuário ou por URL com parâmetro de consulta; a cardinalidade explode e o custo de agregação acompanha. A chave analítica é (rota normalizada, formato de aparelho, dia).

## Plano de teste

| Caso | Passo | Critério de aceite |
| --- | --- | --- |
| Imagem herói sem prioridade | remover `priority` e rodar auditoria | gate falha apontando o elemento LCP |
| Imagem acima do fold sem dimensão | remover `width`/`height` | asserção de CLS falha |
| Import estático de componente pesado | trocar `dynamic` por import direto | orçamento de bundle falha |
| Handler longo | inserir trabalho de 400 ms sem `yield` | perfil mostra `long task` acima de 50 ms |
| Reenvio de lote de RUM | repetir o mesmo `POST` | segunda resposta não altera a contagem |
| Paginação de histórico | pedir 3 páginas de 50 itens | sem repetição e sem omissão entre páginas |
| Rollback | aplicar regressão proposital e reverter | rota volta ao orçamento em 1 execução |
| CrUX sem resposta | consultar origem sem amostra | script sinaliza ausência sem quebrar |

Critério de aceite geral: os sete casos acima rodam no CI ou em script automatizado e todos passam antes da marcação de pronto.

## Checklist de adesão

1. Escopo e não-escopo lidos antes de propor mudança na rota.
2. Linha de base de campo registrada antes da primeira alteração.
3. Um único `fetchpriority="high"` por rota.
4. `sizes` conferido junto com o `srcset`, não só a imagem.
5. `preconnect` limitado às origens realmente usadas no início.
6. Componente pesado em `dynamic import`, com `loading` definido.
7. Handlers com debounce e fatiamento quando passam de 50 ms.
8. Reserva de espaço em todo elemento de altura variável.
9. Orçamento de bundle configurado como asserção de CI.
10. RUM com chave de idempotência e RLS ativo.
11. Leitura de histórico paginada por cursor.
12. `EXPLAIN (ANALYZE, BUFFERS)` anexado para a consulta principal.
13. Métrica publicada com fonte, aparelho e janela declarados.
14. Rollback testado com regressão proposital.
15. Confirmação em campo antes de encerrar a entrega.

## Modelo de dados de suporte

As medições desta atividade são persistidas no banco provisionado. Esquema de referência:

```sql
create table public.page_url (
  id            bigint generated always as identity primary key,
  route_key     text not null unique,
  origin        text not null,
  path          text not null,
  critical      boolean not null default false,
  created_at    timestamptz not null default now()
);

create table public.cwv_metric_sample (
  id            bigint generated always as identity primary key,
  url_id        bigint not null references public.page_url (id),
  collected_on  date not null,
  form_factor   text not null check (form_factor in ('PHONE', 'TABLET', 'DESKTOP')),
  lcp_p75_ms    integer not null check (lcp_p75_ms > 0),
  inp_p75_ms    integer check (inp_p75_ms is null or inp_p75_ms > 0),
  cls_p75       numeric(4, 3) not null check (cls_p75 >= 0),
  sample_count  integer not null default 0,
  source        text not null default 'crux'
    check (source in ('crux', 'rum')),
  created_at    timestamptz not null default now()
);

-- chave de idempotência da ingestão: o mesmo lote reenviado não duplica
create unique index cwv_metric_sample_unq
  on public.cwv_metric_sample (url_id, collected_on, form_factor, source);

-- leitura padrão do dashboard: intervalo de tempo recente
create index cwv_metric_sample_recent_idx
  on public.cwv_metric_sample (collected_on desc, url_id);

-- BRIN: barato em escrita e eficiente em tabela append-only ordenada no tempo
create index cwv_metric_sample_time_brin
  on public.cwv_metric_sample using brin (collected_on) with (pages_per_range = 32);
```

Justificativa de modelagem: `page_url` normaliza a URL (3FN) para não repetir string de origem em cada amostra; `cwv_metric_sample` guarda o agregado já calculado (denormalização deliberada) porque a leitura de dashboard é sempre p75 por intervalo, e recalculá-lo a cada acesso custaria varredura da tabela de eventos.

Índice parcial para alerta:

```sql
create index cwv_metric_sample_breach_idx
  on public.cwv_metric_sample (url_id, collected_on)
  where lcp_p75_ms > 2500;
```

Restrição de acesso:

```sql
alter table public.cwv_metric_sample enable row level security;

create policy "leitura autenticada das amostras"
  on public.cwv_metric_sample for select
  to authenticated
  using (true);

create policy "escrita apenas pelo servico de ingestao"
  on public.cwv_metric_sample for insert
  to authenticated
  with check (false);
```

## Verificação de consulta

```sql
explain (analyze, buffers)
select percentile_cont(0.75) within group (order by lcp_p75_ms) as lcp_p75,
       percentile_cont(0.75) within group (order by inp_p75_ms) as inp_p75,
       percentile_cont(0.75) within group (order by cls_p75)    as cls_p75
  from public.cwv_metric_sample
 where url_id = $1
   and collected_on >= current_date - 28
   and form_factor = $2;
```

Aceitar o plano somente se: usar índice no filtro de tempo, reduzir as linhas lidas antes da agregação e não apresentar `Seq Scan` em tabela de eventos. Se apresentar, o próximo passo é conferir estatísticas (`analyze`) e a seletividade real do filtro antes de criar mais índice.

## Migração segura de schema

Padrão expandir e contrair, para não bloquear a escrita durante a janela de pico:

```sql
-- 1. expandir: coluna nova e opcional
alter table public.cwv_metric_sample
  add column if not exists device_class text;

-- 2. default para as linhas antigas
update public.cwv_metric_sample
   set device_class = 'unknown'
 where device_class is null;

-- 3. restringir sem lock longo: constraint validada depois
alter table public.cwv_metric_sample
  alter column device_class set not null;

-- 4. índice criado sem travar escrita
create index concurrently if not exists cwv_metric_sample_device_idx
  on public.cwv_metric_sample (device_class, collected_on desc);

-- 5. em release seguinte: remover a coluna antiga quando não houver leitor
```

## Referências verificadas

- Curso: Learn Performance (web.dev, Google)
- Vídeo: Core Web Vitals (Google Chrome Developers, YouTube)
- Doc oficial: Web Vitals, https://web.dev/vitals/ (verificada em 2026-09-28)
- Doc oficial: PageSpeed Insights, https://developers.google.com/speed/docs/insights/v5/about (verificada em 2026-09-28)
