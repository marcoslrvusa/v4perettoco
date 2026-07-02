# Imagens para Blog Metal Indianápolis v3 (FINAL)

Apenas Hero (background do cabecalho). Body images removidas.

## Hero (mesma para todos)
Sugestao de URL (confirme/substitua na biblioteca de midia do WordPress):

```
https://preview.indianapolis.com.br/wp-content/uploads/2026/05/fundicao-metal-indianapolis-hero.webp
```

Atualmente o JSON esta com `id: 356`. Se o ID real for diferente, o upload ainda funciona — o background usa a URL direta, nao o ID. O ID aparece no schema.image como referencia.

## Organizacao dos arquivos

| Pasta                      | Conteudo      | Status                                                                         |
| -------------------------- | ------------- | ------------------------------------------------------------------------------ |
| `raw-files-v3/retrabalho/` | Artigos 01-23 | **Substituir** os que estao no ar (conteudo 100% original, zero IP de agencia) |
| `raw-files-v3/novos/`      | Artigos 24-58 | **Novos** — sobe direto                                                        |

## Estrutura de cada artigo
- **Hero:** background com overlay escuro, H1, texto de introducao
- **Body:** secoes com H2 original + texto tecnico 100% original (zero texto da agencia)
- **CTA:** bloco no meio do artigo com botao "Solicitar Cotacao →" para /contato/
- **FAQ:** perguntas e respostas tecnicas especificas da categoria
- **Schema:** Article + BreadcrumbList + FAQPage em JSON-LD
- **Nenhuma imagem inline** inserida
