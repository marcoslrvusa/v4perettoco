# AG-01 — Guia de Implementação JSON-LD (Organization + Store)

## Lola Aviamentos — https://www.lolaaviamentos.com.br/

**Plataforma:** Nuvemshop (Tema Amazonas)
**GTM Container:** GTM-MQW27G8G (já instalado no site)
**Status do structured data atual:** 17 blocos JSON-LD na home (todos Product, injetados pela Nuvemshop). ZERO Organization e ZERO Store.

---

## Opção 1 — Injeção Direta no Nuvemshop (PREFERIDA)

Se o plano Nuvemshop permite customização do tema (todos os planos pagos permitem):

### Passo 1 — Acessar o painel Nuvemshop
1. Login em https://admin.nuvemshop.com.br
2. Ir em **Loja Virtual → Tema → Personalizar → Código** (ou **Configurações → Código personalizado**)
3. Localizar o campo **"Código <head> adicional"** ou **"Scripts no <head>"**

### Passo 2 — Inserir o Organization JSON-LD (na home)
Colar o conteúdo de `AG-01-jsonld-organization.json` dentro de:
```html
<script type="application/ld+json">
{ ... conteúdo do arquivo Organization ... }
</script>
```

### Passo 3 — Inserir o Store JSON-LD (na página /empresa/)
Para a página institucional, usar o campo de código customizado da página /empresa/ no editor Nuvemshop, ou inserir via **Páginas → Empresa → Editar → Código customizado no head**.

Colar o conteúdo de `AG-01-jsonld-store.json` dentro de:
```html
<script type="application/ld+json">
{ ... conteúdo do arquivo Store ... }
</script>
```

### Passo 4 — Salvar e publicar

### Passo 5 — Validar
- Abrir https://search.google.com/test/rich-results e testar a URL da home
- Abrir https://validator.schema.org/ e colar cada JSON-LD
- Verificar que não há erros nem warnings

---

## Opção 2 — Fallback via GTM (se dependência de dev Nuvemshop)

Se a Nuvemshop não permite injeção direta no <head> (plano gratuito ou restrições de tema):

### Passo 1 — Acessar o Google Tag Manager
1. Login em https://tagmanager.google.com/
2. Selecionar o container **GTM-MQW27G8G**
3. Ir em **Tags → Novo**

### Passo 2 — Criar Tag de Organization (Home)
1. **Tipo de tag:** Custom HTML
2. **HTML:**
```html
<script type="application/ld+json">
{ ... conteúdo do arquivo Organization ... }
</script>
```
3. **Acionamento:** All Pages → Configure para disparar apenas na homepage
   - Criar um acionamento **Page View** com condição: `Page URL` contém `lolaaviamentos.com.br/` (sem path adicional)
   - OU usar um acionamento de **Custom Event** se preferir

### Passo 3 — Criar Tag de Store (Página Institucional)
1. **Tipo de tag:** Custom HTML
2. **HTML:**
```html
<script type="application/ld+json">
{ ... conteúdo do arquivo Store ... }
</script>
```
3. **Acionamento:** Page View → `Page URL` contém `lolaaviamentos.com.br/empresa/`

### Passo 4 — Publicizar o container GTM
1. Clicar em **Enviar** (Submit)
2. Nome da versão: `AG-01 JSON-LD Organization + Store`
3. Descrição: `Implantação de JSON-LD Organization na home e Store na página institucional`

### Passo 5 — Validar
1. Usar o **Tag Assistant** (ícone de tag no GTM) para preview
2. Abrir a home em modo incógnito e verificar se o JSON-LD Organization aparece no `<head>`
3. Abrir a página /empresa/ e verificar se o JSON-LD Store aparece no `<head>`
4. Validar em https://search.google.com/test/rich-results
5. Validar em https://validator.schema.org/

---

## Verificação Pós-Implantação

| Verificação | Ferramenta | Critério |
|-------------|-----------|----------|
| JSON-LD Organization presente na home | View Source | `<script type="application/ld+json">` com `@type: Organization` |
| JSON-LD Store presente em /empresa/ | View Source | `<script type="application/ld+json">` com `@type: Store` |
| Sem erros de schema | Schema Markup Validator | 0 errors, 0 warnings |
| Rich Results válidos | Google Rich Results Test | Organization e Store reconhecidos |
| Não duplica com dados existentes | View Source | Organization/Store não repetidos em outras páginas |

---

## Dados Usados nos JSON-LD

| Campo | Valor |
|-------|-------|
| Nome | Lola Aviamentos |
| Nome alternativo | Lola Soluções em Têxteis |
| URL | https://www.lolaaviamentos.com.br |
| Logo | Logo da Nuvemshop (CDN) |
| Endereço | Av. Irati, 284 - Barra Funda, Apucarana - PR, 86800-000 |
| Telefone | +55-43-99119-6727 |
| Email | vendas@lolaaviamentos.com.br |
| CNPJ | 16.833.189/0001-33 |
| Horário | Seg-Sex 08:00-18:00, Sáb 08:00-13:00 |
| Área de atendimento | Brasil (BR) |
| SameAs | Instagram @lolasolucoes, Facebook lolasolucoestexteis, YouTube @lolasolucoes |

---

## ⚠️ Pontos de Atenção

1. **Horário de atendimento:** O site não exibe horário. Os horários nos JSON-LD são estimativas (Seg-Sex 08h-18h, Sáb 08h-13h). **Confirmar com o cliente antes de publicar.**

2. **CEP:** Usado 86800-000 (CEP geral de Apucarana). O CEP exato da Av. Irati, 284 pode ser diferente. Recomenda-se confirmar.

3. **Facebook:** O link `https://www.facebook.com/lolasolucoestexteis` foi inferido do nome da empresa. Verificar se o URL real é `lolasolucoestexteis` ou outro.

4. **Não duplicar:** A Nuvemshop já injeta JSON-LD de Product na home. Os novos schemas Organization e Store devem ser adicionados SEM remover os existentes.

5. **GTM vs direto:** Se possível, usar injeção direta no Nuvemshop (Opção 1). GTM é o fallback. Via GTM, o JSON-LD pode ter latência de propagação de até 24h para o Google indexar.