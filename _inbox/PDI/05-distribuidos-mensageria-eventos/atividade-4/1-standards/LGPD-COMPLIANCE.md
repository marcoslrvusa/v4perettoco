# STANDARD: Conformidade LGPD (Dados Distribuídos)

## Princípios aplicados
- **Trânsito:** TLS 1.2+ obrigatório; mTLS entre serviços internos.
- **Repouso:** AES-256 em campos sensíveis (CPF, e-mail) no banco.
- **Minimização:** só transmite o necessário no evento.
- **Consentimento:** `consent_id` carregado no cabeçalho da mensagem.
- **Auditoria:** log imutável de acesso a PII.

## Checklist
- [ ] TLS em todos os tópicos/filas
- [ ] Criptografia de colunas PII
- [ ] Máscara em logs
- [ ] Retenção e direito ao esquecimento documentados

---

## Escopo e não-escopo

**Escopo**

- Camada de transporte entre produtor, broker e consumidor (tópico, fila, webhook, API interna).
- Proteção em repouso: colunas sensíveis no banco, arquivos de exportação, tópicos com
  retenção longa e réplicas de leitura.
- Cadeia de chaves: geração, guarda, rotação e revogação usadas pelo `encrypt_pii.py`.
- Trilha de auditoria de quem leu, escreveu ou apagou dado pessoal.
- Comportamento em incidente: o que fica exposto e o que não fica.

**Não-escopo**

- Definição de quais campos são pessoais e qual é a finalidade: isso vive no `LGPD-DATA.md`.
- Segredos de aplicação (token de API de terceiro): seguem o padrão de gestão de segredos.
- Criptografia de backup: entra aqui só a exigência de janela de retenção declarada e mídia
  criptografada com chave própria.

## Termos

| Termo | Sentido neste standard |
| --- | --- |
| TLS 1.2+ | versão mínima aceita em qualquer conexão que carregue evento ou PII; `TLS 1.0/1.1` são recusadas |
| mTLS | mutual TLS: o consumidor também apresenta certificado; impede serviço não autorizado de ler o tópico |
| AES-256 | algoritmo simétrico usado nas colunas sensíveis em repouso |
| Fernet | implementação usada em `encrypt_pii.py`: cifra o valor e autentica o token, qualquer adulteração quebra na leitura |
| Chave de dado (DEK) | chave que cifra um registro; trocada com mais frequência |
| Chave-mestra (KEK) | chave que protege as DEKs; vive no cofre, nunca no código |
| `pii:true` | marca no schema que aciona o codificador; ausência da marca é falha de build |
| Tokenização | troca do valor por token reversível só pelo dono da chave |
| Auditoria imutável | linha de log que não pode ser editada nem apagada por quem tem acesso de escrita comum |

## Princípios ampliados (o porquê de cada um)

**Trânsito.** TLS com versão mínima porque `TLS 1.0` e `1.1` têm falhas de implementação
conhecidas e são desligadas por política, não por gosto. O mTLS existe por um motivo de
arquitetura: num tópico compartilhado, quem assina é quem lê; sem certificado de cliente, um
serviço comprometido lê todos os eventos de todos os domínios, e o evento com `subject_id`
vira exposição de todo o histórico daquele titular.

**Repouso.** AES-256 nas colunas sensíveis protege o cenário de disco extraviado e de dump de
banco vazado, que é exatamente o cenário que transforma uma brecha pequena em processo
administrativo grande. Repouso inclui também a fila com retenção longa: dado parado em tópico é
dado em repouso, mesmo que a ferramenta chame de "trânsito".

**Minimização.** É a proteção mais barata e a mais eficiente: campo que não entra não vaza.
Quando o Analytics precisa de `score`, ele não precisa do e-mail para calcular; precisa do
`subject_id` para cruzar. Cada campo que você remove do payload elimina toda a cadeia de
criptografia, cache e exclusão daquele campo.

**Consentimento.** O `consent_id` vai no **cabeçalho** da mensagem, não só no corpo, porque
cabeçalho é enriquecido e validado pelo middleware de todos os consumidores, incluindo os que
não conhecem o schema do corpo. Com isso, um consumidor novo herda a checagem sem escrever
código próprio.

**Auditoria.** A trilha registra `quem`, `quando`, `qual subject_id`, `qual finalidade` e
`qual resultado`, e não registra o dado em si. A prova da leitura não pode conter o conteúdo
lido.

## Regra canônica (proteção em camadas)

```text
exposicao_efetiva = PII_em_claro * (1 - TLS) * (1 - AES) * (1 - minimização)
```

- `PII_em_claro` = quantidade de campos pessoais presentes no formato original (cru);
- `TLS` = 1 se o transporte é TLS 1.2+ autenticado, 0 caso contrário;
- `AES` = 1 se a coluna está cifrada com chave fora do banco, 0 caso contrário;
- `minimização` = 1 se o campo nem entra no payload daquela etapa, 0 caso contrário.

A leitura correta é que **a minimização multiplica a exposição por zero**, enquanto TLS e AES
só a reduzem: eles protegem enquanto a chave está em mãos certas. Um campo que não circula
precisa de nenhuma das outras três defesas.

### Tabela de decisão: qual proteção aplicar

| Situação | Transporte | Repouso | Formato no payload | Auditoria |
| --- | --- | --- | --- | --- |
| Campo sem `pii:true` e sem identificação | TLS padrão do ambiente | sem exigência | valor normal | sem exigência |
| Campo identificável dentro do domínio dono do dado | TLS + mTLS | AES na coluna | valor cifrado (Fernet) | leitura e escrita |
| Campo identificável em domínio downstream | TLS + mTLS | AES na coluna | `subject_id` ou hash | escrita e qualquer leitura |
| Log, trace ou métrica | TLS | arquivos criptografados na mídia | `anon:` + hash de 12 hex | escrita |
| Exportação para fora da empresa | TLS + canal dedicado | arquivo cifrado com chave própria | somente o mínimo aprovado | autorização nominal + registro |
| Pedido de exclusão em andamento | TLS + mTLS | n/a | comando com `subject_id`, sem PII | criação e conclusão da cascata |

## Exemplo numérico: custo de rotação de chave

**Exemplo numérico:** a base tem `12 milhões` de linhas com `2 campos cifrados` cada, ou
`24 milhões` de valores (Exemplo numérico com parâmetros declarados). Rodo a rotação a
`2.000 valores/s` (chave em memória, sem bloqueio de escrita de negócio):
`24.000.000 / 2.000 = 12.000 s`, ou `3,3 horas`. Com `500 valores/s` (escrita na transação
normal), seriam `48.000 s = 13,3 horas`. A conta justifica duas decisões: rotação programada
fora da janela de pico, e **criptografia por coluna com formato token** (o valor cifrado tem
prefixo e versão), que permite reescrever em lote sem destravar a tabela inteira. Se a rotação
demorar mais que a janela de manutenção, o padrão é trocar só a chave-mestra (KEK), que protege
as chaves de dado sem reescrever nenhuma linha: reescrita zero, minuto de operação. O custo da
rotação é o que define a frequência real, e não a recomendação genérica de "troque sempre".

## Cadeia de chaves

1. **Geração**: chave gerada no cofre, nunca por `Fernet.generate_key()` em tempo de import.
2. **Guarda**: cofre (KMS/secrets) com acesso restrito a serviços nominados; nenhuma chave em
   repositório, em log, em variável de ambiente de aplicação ou em payload.
3. **Uso**: o serviço busca a chave no início, mantém em memória e não a escreve em lugar
   algum; erro de busca interrompe a publicação com dado pessoal (falha fechada).
4. **Rotação**: KEK anual (meta), DEK por janela definida no `mapa-dados.md`; rotação em lote
   conforme o exemplo numérico acima.
5. **Revogação**: incidente com credencial revoga a chave e força re-cifração; tokens emitidos
   com a chave revogada deixam de ser legíveis, o que é o efeito desejado.
6. **Prova**: teste periódico de `decrypt` em amostra, para nunca descobrir a perda da chave
   no momento do atendimento ao titular.

Aqui está o ponto que a revisão precisa pegar em `encrypt_pii.py`: a chave é gerada no import
do módulo. Em produção, cada processo reiniciado gera uma chave nova e **não consegue ler o que
o anterior cifrou**. O padrão exige chave vinda do cofre, com versão embutida no token.

## Modos de falha e recuperação

| Sintome | Causa raiz | Como detecta | Como mitiga | Recuperação |
| --- | --- | --- | --- | --- |
| Handshake TLS recusado | certificado vencido ou versão abaixo de 1.2 | `tls_handshake_failures_total` subindo | renovar certificado e forçar versão mínima na política do broker | minutos, com rotação de certificado |
| Consumidor sem certificado lendo o tópico | mTLS não obrigatório no tópico compartilhado | tentativa de consumo sem certificado na auditoria | exigir `require tls-verify=verify_peer` no broker | imediato ao aplicar a política |
| `decrypt` falha após reinício | chave gerada em tempo de import | `crypto_decrypt_failures_total` com `versao_chave` nova | trocar a chave por cofre com versão embutida no token | leitura antiga restaurada só com backup da chave |
| Token adulterado | alteração de 1 byte no banco | erro de integridade do Fernet | manter autenticação do token e investigar escrita fora do padrão | dado reemitido a partir da origem |
| Payload sai cru com o cofre fora | aplicação cai para modo de falha aberta | `pii_field_unmasked_total > 0` | falha fechada obrigatória no cliente de cofre | correção imediata, evento reprocessado minimizado |
| Auditoria parando de gravar | destino da trilha indisponível | `audit_log_lag_seconds > 60` | fila local com regra de não sobrescrever | backlog drenado, com lacuna registrada |
| Chave acima da janela de rotação | rotação atrasada por dependência | `key_age_days` acima do limite | trocar KEK sem reescrever linhas | minutos |
| Log de exceção com payload completo | logger em nível `DEBUG` em produção | varredura diária com `anon.py` | nível `INFO` por padrão e `log_safe` no handler | histórico reprocessado com anonimização |
| Exportação vazada | canal sem cifra e sem autorização nominal | auditoria de saída sem `action = 'export'` | exportação só por canal cifrado com aprovação registrada | revogação de acesso e notificação conforme política |
| Backup com a mesma chave do banco | cópia de segurança sem chave própria | revisão de política de backup | chave separada para mídia, com acesso nominal | cópia re-cifrada na próxima janela |

## Conflitos frequentes em revisão

1. **"Cifrar atrasa a publicação."** Custo medido na Fórmula 3 do README: `p95_crypto ≈ 2 ms`
   (Exemplo numérico) frente a `p95_consent ≈ 12 ms` e `p95_broker ≈ 8 ms`. A cifra não é o
   gargalo; a consulta de consentimento é, e por isso ela tem cache local.
2. **"Minimizar quebra o relatório do time de dados."** O relatório usa `subject_id`, que
   continua estável entre eventos. O que o relatório perde é o e-mail, que ele não deveria
   estar cruzando de qualquer forma.
3. **"Falha fechada para o negócio em incidente."** Sim, e é a troca declarada: em incidente do
   gateway os eventos saem minimizados (dados entram depois com consentimento resolvido), nunca
   completos sem base legal. Disponibilidade de dado pessoal não é negociável; atraso de dado
   agregado é.
4. **"Exclusão não alcança backup, então não funciona."** Não alcança, e isso está na matriz de
   riscos com impacto alto. A mitigação é janela de retenção declarada, mídia criptografada com
   chave própria e acesso nominal: dado em backup é dado sob chave, mesmo que ainda exista.
5. **"Basta apagar a origem."** É o erro que gera autuação: o titular apagado no CRM vive no
   Analytics, no cache e no índice. Cascata por `subject_id` com prova em `audit_log` é a única
   resposta aceitável.

## Anti-padrões

1. `Fernet.generate_key()` em tempo de import de módulo de produção.
2. Chave em variável de ambiente de aplicação (vaza em dump de memória e em log de startup).
3. TLS desligado "porque é ambiente interno".
4. AES só no banco, com a fila e o arquivo de exportação sem criptografia.
5. Reutilizar a mesma chave para dado pessoal e para segredo de infraestrutura.
6. Auditoria gravada no mesmo destino editável pelo serviço que acessa o dado.
7. Log de exceção que imprime o payload completo (o caminho clássico de vazamento).
8. Cabeçalho `consent_id` presente no corpo e ausente no cabeçalho: consumidores antigos
   não validam.
9. Máscara de coluna usada como se fosse cifra: máscara é apresentação, não proteção.
10. Backup com a mesma chave do banco em produção: se a chave vazar junto, o backup não
    protege nada.

## Telemetria

| Métrica | Rótulos | Alerta |
| --- | --- | --- |
| `tls_handshake_failures_total` | `servico`, `motivo` | `> 0` sustentado por 5 min: investigar certificado |
| `crypto_decrypt_failures_total` | `servico`, `versao_chave` | `> 0`: chave incompatível ou dado adulterado, P1 |
| `pii_field_unmasked_total` | `schema`, `campo` | `> 0`: build falha, deploy bloqueado |
| `audit_log_lag_seconds` | `destino` | `> 60 s`: auditoria deixando de ser síncrona |
| `key_age_days` | `tipo` (KEK/DEK) | acima da janela: rotação atrasada |
| `consent_header_missing_total` | `topico` | `> 0`: consumidor não validando cabeçalho |

Cardinalidade proibida em qualquer métrica: `subject_id`, `cpf`, `email`, `nome`. Idade de
chave e falha de handshake são baratas e suficientes para operar.

## Plano de teste

| Caso | Procedimento | Critério de aceite |
| --- | --- | --- |
| C1 Transporte | conectar sem TLS 1.2 e tentar consumir o tópico | conexão recusada |
| C2 mTLS | consumidor sem certificado tenta assinar | recusado, com linha de auditoria do motivo |
| C3 Repouso | `SELECT` direto na coluna sensível | valor com prefixo do token, ilegível sem chave |
| C4 Integridade | alterar 1 byte de um token cifrado | `decrypt` falha com erro claro, sem dado parcial |
| C5 Chave reiniciada | reiniciar o serviço e tentar ler dado antigo | falha explícita (expõe o bug da chave de import) |
| C6 Log | provocar exceção com payload completo em nível `DEBUG` | varredura `0` de e-mail/CNPJ cru |
| C7 Auditoria | leitura de dado pessoal por usuário nominal | linha em `audit_log` com quem, quando, qual `subject_id` |
| C8 Rotação | rodar a rotação em lote e medir duração | dentro da janela de manutenção, sem erro de decrypt |
| C9 Falha fechada | parar o cofre de chaves e publicar evento com PII | evento sai minimizado ou é recusado, nunca cru |

## Checklist de adesão

- [ ] TLS 1.2+ em todos os tópicos, filas, webhooks e APIs internas.
- [ ] mTLS entre serviços internos que trocam evento com dado pessoal.
- [ ] AES em coluna para todo campo com `pii:true`, com token versionado.
- [ ] Chave fora do repositório e fora de variável de ambiente de aplicação.
- [ ] KEK no cofre, DEK versionada, rotação programada e testada.
- [ ] `consent_id` no cabeçalho da mensagem e validado por middleware do consumidor.
- [ ] Minimização aplicada antes da cifra, não depois (campo removido não é cifrado).
- [ ] Trilha de auditoria imutável para leitura, escrita e exclusão de dado pessoal.
- [ ] Auditoria sem PII, com `subject_id` como chave de investigação.
- [ ] Exportação fora da empresa com autorização nominal e registro.
- [ ] Janela de retenção de backup declarada e mídia com chave própria.
- [ ] Testes C1 a C9 executados nesta versão.
- [ ] Runbook de incidente com o passo "revogar chave" e o passo "notificar titular".
- [ ] Nenhuma métrica com rótulo identificador.

## Fronteira com o LGPD-DATA.md

Os dois standards se dividem por pergunta, não por tema:

- **LGPD-DATA.md** responde "quais dados, para qual finalidade, por quanto tempo e quem apaga".
  É a fonte do `mapa-dados.md`, da tabela de decisão por campo e da cascata de exclusão.
- **LGPD-COMPLIANCE.md** (este) responde "como o dado é protegido no trânsito, no repouso e na
  cadeia de chaves, e o que fica registrado quando alguém o lê". É a fonte do TLS/mTLS, do
  cofre, da auditoria e do runbook de incidente.
- A sobreposição é uma só, e é intencional: a marcação `pii:true` no schema. Ela é a entrada do
  codificador (aqui) e o gatilho da tabela de decisão (lá). Se o campo não estiver marcado, os
  dois standards falham ao mesmo tempo, e por isso o gate de schema é o teste que fecha os dois.

A divisão evita o erro comum de escrever um documento gigante que ninguém revisa: quem cuida de
criptografia lê este, quem cuida de finalidade e prazo lê o outro, e a esteira de build é o ponto
onde os dois se encontram com um veredito binário.

## Referências

- Documento oficial: Lei n. 13.709/2018 (planalto.gov.br).
- Documento oficial: Guia Orientativo da ANPD (gov.br/anpd).
- Curso: "LGPD na Prática" (Udemy).
- Vídeo: "O que é a LGPD?" (YouTube, SEBRAE).
