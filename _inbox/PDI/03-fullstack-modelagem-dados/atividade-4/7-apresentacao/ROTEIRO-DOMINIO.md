# ROTEIRO-DOMINIO: Otimização de Core Web Vitals (LCP/INP/CLS)

5 perguntas de coordenador + respostas curtas para defesa da atividade 4.

## 1. Por que otimizar LCP primeiro e deixar CLS por último?

ADR-034, ordem por ROI: LCP de 4,1s afasta mais usuário e pesa mais no ranqueamento que o deslocamento de layout. CLS continua um ciclo, mas o ganho de LCP compensa primeiro.

## 2. Por que medir no CrUX e não só no Lighthouse?

Lighthouse e laboratório: ambiente controlado que não captura gargalo real de dispositivo e rede. O CrUX traz campo (p75, janela de 28 dias); o script `field_cwv.py` coleta o baseline e o laboratório guia o dia a dia.

## 3. Qual foi a causa do LCP em 4,1s e a correção?

Hero sem `fetchpriority` nem preconnect, imagem pesada sem formato moderno. Correção: `next/image` com `priority` só no hero, preconnect nas origens e AVIF.

## 4. Qual foi a causa do INP em 410ms e a correção?

Handler síncrono bloqueando a thread no clique. Correção: dynamic import com code splitting por rota para tirar chat e mapa do caminho crítico, mais debounce nas ações.

## 5. Como evitam regressão depois de atingir as metas?

Budget no CI barra regressão a cada merge, RUM próprio cobre rotas com pouco volume no CrUX, e a re-medicao de campo confirma LCP até 2,5s, INP até 200ms e CLS até 0,1 em 75% das sessões.
