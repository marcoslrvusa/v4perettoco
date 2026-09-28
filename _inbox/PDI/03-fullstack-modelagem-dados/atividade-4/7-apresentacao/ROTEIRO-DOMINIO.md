# ROTEIRO-DOMINIO: Otimizacao de Core Web Vitals (LCP/INP/CLS)

5 perguntas de coordenador + respostas curtas para defesa da atividade 4.

## 1. Por que otimizar LCP primeiro e deixar CLS por ultimo?

ADR-034, ordem por ROI: LCP de 4,1s afasta mais usuario e pesa mais no ranqueamento que o deslocamento de layout. CLS continua um ciclo, mas o ganho de LCP compensa primeiro.

## 2. Por que medir no CrUX e nao so no Lighthouse?

Lighthouse e laboratorio: ambiente controlado que nao captura gargalo real de dispositivo e rede. O CrUX traz campo (p75, janela de 28 dias); o script `field_cwv.py` coleta o baseline e o laboratorio guia o dia a dia.

## 3. Qual foi a causa do LCP em 4,1s e a correcao?

Hero sem `fetchpriority` nem preconnect, imagem pesada sem formato moderno. Correcao: `next/image` com `priority` so no hero, preconnect nas origens e AVIF.

## 4. Qual foi a causa do INP em 410ms e a correcao?

Handler sincrono bloqueando a thread no clique. Correcao: dynamic import com code splitting por rota para tirar chat e mapa do caminho critico, mais debounce nas acoes.

## 5. Como evitam regressao depois de atingir as metas?

Budget no CI barra regressao a cada merge, RUM proprio cobre rotas com pouco volume no CrUX, e a re-medicao de campo confirma LCP ate 2,5s, INP ate 200ms e CLS ate 0,1 em 75% das sessoes.
