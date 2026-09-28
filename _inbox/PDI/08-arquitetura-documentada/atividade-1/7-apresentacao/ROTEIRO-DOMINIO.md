# ROTEIRO-DOMINIO: 5 Perguntas que Podem Cair

## 1. Por que C4 e não UML tradicional?
Resposta: UML tem 14 diagramas e ninguém concorda qual usar; C4 tem 4 níveis com público definido e regra de zoom único, o que cabe no ritmo de automação onde quem desenha e quem opera são as mesmas pessoas.

## 2. Manter DSL e Mermaid duplicados não apodrece?
Resposta: apodrece se não houver regra. A regra aqui: PR que muda container exige os dois atualizados, e o checklist de revisão cobra isso. DSL e fonte, Mermaid e espelho.

## 3. Por que nível 4 só em uma função?
Resposta: código muda todo dia e doc de código vira lixo em uma semana. Documentamos só onde bug custa dinheiro: o retry da coleta que decide verba de tráfego nos relatórios.

## 4. Onde fica o deploy (VPS, Docker)?
Resposta: fora desta atividade de propósito. Infra hoje e VPS única, então o diagrama de deploy seria trivial e falso. Entra quando houver segundo ambiente.

## 5. Como isso reduz incidente na prática?
Resposta: em falha de coleta, o operador abre o container, vê que workers chamam Meta via webhook e gravam no Supabase, e checa fila de erros em vez de perguntar no chat. Caminho de diagnóstico de minutos, não de horas.
