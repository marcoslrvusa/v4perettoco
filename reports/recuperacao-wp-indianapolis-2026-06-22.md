# Relatório de Recuperação — WordPress Metal Indianápolis

**Data:** 22/06/2026
**Site:** https://preview.indianapolis.com.br
**Hospedagem:** Hostinger (subdomínio provisório: lightblue-loris-222364.hostingersite.com)
**Status:** ✅ Resolvido

---

## Histórico do Problema

Na sessão anterior (17h38), o domínio `preview.indianapolis.com.br` apresentava erro 403 + SSL_ERROR. As URLs do WordPress haviam sido alteradas manualmente no `wp-config.php`, e o admin ficou inacessível. A soleração na época ficou pendente por falta de acesso ao hPanel.

## Problema Atual

O usuário tentou resolver via File Manager do hPanel da Hostinger e acabou cometendo typos:

1. **`.htaccess`** — escreveu um redirect errado (comeu uma letra na URL)
2. **`wp-config.php`** — escreveu `WP_HOME` e `WP_SITEURL` com a URL errada

Resultado: redirect loop infinito, impossibilitando acesso ao `/wp-admin/`.

---

## Passo a Passo da Recuperação

### 1. Acesso via FTP (FileZilla)

O File Manager do hPanel não foi localizado pelo usuário. A saída foi conectar via FTP.

**Dica (.htaccess invisível no FileZilla):** Por padrão, o FileZilla não mostra arquivos que começam com ponto (`.htaccess`). Para forçar a exibição:

- **Servidor → Forçar exibição de arquivos ocultos**
- Ou atalho **Ctrl+Alt+H**
- Ou **Visualizar → Mostrar arquivos ocultos**

### 2. Correção do `wp-config.php`

Pelo FTP, localizamos o `wp-config.php` na raiz do site e **comentamos** (ou removemos) as linhas:

```php
// define('WP_HOME', 'https://preview.indianapolis...');
// define('WP_SITEURL', 'https://preview.indianapolis...');
```

Isso fez o WordPress voltar a ler a URL diretamente do banco de dados.

### 3. Verificação do `.htaccess`

O arquivo `.htaccess` foi revisado e **estava limpo** — sem redirects manuais. Continha apenas regras geradas pelo plugin LiteSpeed Cache e as regras padrão do WordPress:

```apache
# BEGIN LSCACHE
# ... regras do LiteSpeed ...
# END LSCACHE

# BEGIN WordPress
<IfModule mod_rewrite.c>
RewriteEngine On
RewriteBase /
RewriteRule ^index\.php$ - [L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.php [L]
</IfModule>
# END WordPress

# Security
<Files wp-config.php>
Require all denied
</Files>
# ... regras de cache e gzip ...
```

**Conclusão:** O `.htaccess` não era o culpado. O redirect loop era causado exclusivamente pelo `wp-config.php` com URL errada.

### 4. Acesso ao Admin

Após corrigir o `wp-config.php`, o `/wp-admin/` voltou a funcionar normalmente.

### 5. Ajustes Finais no Admin

- **Settings → General:**
  - "WordPress Address (URL)" → `https://preview.indianapolis.com.br`
  - "Site Address (URL)" → `https://preview.indianapolis.com.br`
- **Settings → Permalinks:**
  - Apenas clicou "Save Changes" para regenerar o `.htaccess` automaticamente
- **LiteSpeed Cache → Purge → Purge All**
  - Limpeza completa de cache

### 6. Teste

Home carregando normalmente em `https://preview.indianapolis.com.br`.

---

## Pendências

1. **SSL** — Instalar certificado SSL para o domínio `preview.indianapolis.com.br` no hPanel (Segurança → SSL → Instalar SSL → Forçar HTTPS)
2. **Domínio definitivo** — O site ainda está em subdomínio. Para SEO efetivo, migrar para domínio próprio (`indianapolis.com.br` ou similar)

---

## Lições Aprendidas

- Nunca editar `WP_HOME` e `WP_SITEURL` manualmente no `wp-config.php` — isso sobrescreve o banco e pode travar o admin. Use o Settings do WordPress.
- Se travar, a sequência de resgate é: (1) FTP, (2) comentar as defines no wp-config, (3) renomear .htaccess se necessário, (4) acessar admin e corrigir URLs pelo Settings.
- O `.htaccess` gerado pelo WordPress + LiteSpeed é seguro — não precisa mexer nele manualmente.

---

**Participantes:** Marcos (usuário) + Assistente IA
**Duração:** ~1h
**Desfecho:** ✅ Resolvido
