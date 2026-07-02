# FCA — Perda de Registro MX por Conexão de Domínio via GHL

**Cliente:** [NOME DO CLIENTE]
**Data:** 20/06/2026
**Severidade:** 🔴 Crítica
**Ticket Ekyte:** #9539386

---

## FATO

Durante a publicação de uma landing page no GHL, o designer acionou o fluxo **Quick Connect** ao salvar a LP com domínio personalizado. O GHL aplicou um template DNS mínimo (A + CNAME) via provedor parceiro, sobrescrevendo a zona DNS inteira e **removendo os registros MX do Google Workspace**. O e-mail corporativo do cliente caiu por completo.

**Evidências:** LP publicada em [DATA/HORA]; queda de e-mail detectada em [DATA/HORA]; MX ausente confirmado em [DATA/HORA]; nenhuma alteração DNS externa ao GHL no período; nenhum membro do time de tecnologia acessou o DNS.

---

## CAUSA

O designer usou o **Quick Connect** do GHL — que pusha um template DNS proprietário apagando toda a zona anterior — em vez do caminho manual (inserir CNAME no provedor sem alterar os demais registros). A interface do GHL não alerta que MX existentes serão perdidos.

A causa raiz é **processual**: o template de task de criação de LP não possui:
1. Etapa de verificação de MX pré-publicação
2. Distinção entre domínio virgem vs domínio com e-mail ativo (Google Workspace)
3. Validação de MX pós-publicação
4. Documentação de que Quick Connect é destrutivo para DNS de e-mail

Nenhum destes gaps é técnico. São gaps da esteira de design.

---

## AÇÃO

### Sobre soluções técnicas — o caminho possível é uma gambiarra, e é complexa

Se a decisão for buscar uma barreira técnica, o único caminho é **desacoplar o e-mail do Wix e hospedar os registros MX em um provedor de DNS com lock de zona** (Cloudflare, AWS Route 53, etc.). Mas é importante entender o que isso significa na prática — não é uma configuração simples, é uma gambiarra logística com riscos reais. Segue o passo a passo do que teria que acontecer:

1. **Contratar um provedor de DNS separado** (Cloudflare pago ou Route 53) — nova conta, novo cadastro, nova fatura mensal que não existia antes.

2. **Migrar a zona DNS do domínio para fora do Wix** — isso exige trocar os nameservers do domínio no Registro.br (ou onde o domínio está registrado). Durante a propagação (que pode levar até 48h), tanto o site quanto o e-mail podem ficar instáveis.

3. **Recriar manualmente todos os registros no novo provedor**: A (site), CNAME (www), MX (Google Workspace), TXT (SPF, DKIM, DMARC, verificação do Google, verificação do Wix) — um a um. Qualquer registro esquecido quebra alguma coisa.

4. **Configurar o lock de zona nos registros MX** — no Cloudflare isso é feito via API com "Locked" no registro; no Route 53 é via IAM policy. Não é um checkbox no painel — precisa de acesso de admin e conhecimento da ferramenta.

5. **Reconfigurar o Wix** — o Wix vai perder o controle total do DNS. O site do Wix precisa ser reconfigurado para apontar via CNAME para o endereço do Wix (em vez de gerenciar o DNS direto). Cada provedor tem um fluxo diferente para isso.

6. **Testar tudo**: e-mail (envio + recebimento + SPF/DKIM/DMARC), site, validar que propagou, verificar se o Google Workspace continua aceitando e-mail, se o Wix não perdeu funcionalidades (alguns recursos do Wix dependem de DNS gerenciado por eles).

7. **Manutenção contínua** — toda vez que o cliente precisar de qualquer alteração (adicionar alias no Google Workspace, trocar provedor de site, etc.), alguém precisa destravar o MX no Cloudflare/Route 53, aplicar a mudança e travar de novo. Tech vira gatekeeper de toda alteração de e-mail do cliente.

**E mesmo assim, o risco residual existe.** O GHL Quick Connect pusha uma zona DNS inteira via API. Em alguns provedores, uma chamada de API com a chave certa consegue sobrescrever até registros locked, dependendo do escopo da permissão. A proteção não é absoluta — é apenas mais uma camada.

### Mitigação de riscos — se optarem pela gambiarra

Se mesmo com tudo isso a decisão for implementar, os riscos precisam ser mitigados:

| Risco                               | Mitigação                                                                                                                 |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Downtime de e-mail durante migração | Executar em janela agendada com cliente ciente. Deixar registros MX prontos no novo provedor antes de trocar nameservers. |
| Registro esquecido na migração      | Fazer dump completo da zona DNS antes de migrar. Conferir registro por registro com checklist.                            |
| Lock de MX não funcionar contra GHL | Testar: subir ambiente de homologação, simular Quick Connect, validar se MX resiste.                                      |
| Wix perder funcionalidades          | Validar no suporte Wix se o site mantém todas as funções com DNS externo.                                                 |
| Manutenção virar gargalo            | Documentar processo de unlock/relock dos MX. Deixar acesso configurado para pelo menos duas pessoas.                      |
| Cliente pagar conta                 | Deixar explícito no budget mensal. Não pode ser custo absorvido pela operação.                                            |

A pergunta que fica: **vale a pena toda essa cirurgia para resolver um problema que uma verificação de 30 segundos (`dig MX dominio.com.br`) antes de publicar a LP já elimina?**

### Caminho recomendado

**O único caminho simples, eficaz e sem custo é processo e cuidado humano na task de LP.** Não precisa de migração, não precisa de novo provedor, não precisa expor o cliente a risco de downtime:

| # | Ação | Responsável | Prazo |
|---|------|-------------|-------|
| 1 | Adicionar etapa obrigatória ao template de task de LP: verificar MX ativo com `dig MX dominio.com.br` antes de conectar domínio. Se houver MX, usar conexão manual com CNAME, nunca Quick Connect | Design Lead | 5 dias |
| 2 | Criar POP de Publicação de LP documentando os dois caminhos (Quick Connect destrói zona DNS inteira vs CNAME manual preserva registros) | Design Lead | 7 dias |
| 3 | Adicionar verificação de MX pós-publicação no check-list de fechamento da task — validar e-mail do cliente 30 min após publicar | Designer responsável | 5 dias |
| 4 | Treinamento de 30 min com o squad de design sobre o comportamento do Quick Connect e como identificar domínios com Google Workspace ativo | Design Lead | 10 dias |

**Dono da ação:** Design Lead — único e exclusivo. Tech já restaurou o MX e não tem mais envolvimento. O problema foi na publicação de LP, a correção é no processo de LP, o dono é quem faz LP.

---

**FCA registrada por:** [SEU NOME]
**Ticket Ekyte:** #9539386
