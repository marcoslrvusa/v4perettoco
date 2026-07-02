# Instrução GTM — Form1 Telefone (Brinks V11)

## O que fazer

Criar **tag nova** + **trigger novo** no GTM `GTM-N67NTS8L` (LP Brinks Cofres).

Não mexe em nada do que já existe.

---

## Passo 1 — Criar Trigger

| Campo           | Valor                                         |
| --------------- | --------------------------------------------- |
| Nome            | `-[V4] Click Form1 Telefone`                  |
| Tipo            | **Click — Todos os Elementos**                |
| Disparar quando | `{{Click Text}}` **contém** `Nós te chamamos` |

> Apenas o botão do Form 1 tem o texto "Nós te chamamos". Os forms 2/3 têm "Enviar Contato". Então esse trigger SÓ pega o Form 1.

---

## Passo 2 — Criar Tag

| Campo   | Valor                        |
| ------- | ---------------------------- |
| Nome    | `-[V4] FORM1 Telefone`       |
| Tipo    | **Custom HTML**              |
| Trigger | `-[V4] Click Form1 Telefone` |

**Código HTML da tag:**

```html
<script>
(function() {
  var form = document.querySelector('.e_formulario');
  if (!form) return;

  setTimeout(function() {
    var tel = form.querySelector('input[type="tel"]');
    var cb = form.querySelector('input[type="checkbox"]');

    if (!tel) return;

    fetch('COLE_AQUI_A_URL_DO_N8N/webhook/brinks-form1', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        telefone: tel.value || '',
        consentimento_lgpd: (cb && cb.checked) ? 'sim' : 'nao',
        url: window.location.href
      })
    });
  }, 300);
})();
</script>
```

**Trocar** `COLE_AQUI_A_URL_DO_N8N` pela URL do webhook do n8n tecnologia.

---

## Passo 3 — Publicar

1. Salva a tag e o trigger
2. Vai em **Versions** → cria nova versão
3. Publica

---

## Fluxo final

```
Form 1 (telefone) → Click "Nós te chamamos" → TAG NOVA → n8n tecnologia → Planilha
Forms 2/3 (completo) → GTM antigo → peretton8n (inalterado)
Script inline (linha 5) → n8n pessoal (pode ignorar ou remover depois)
```
