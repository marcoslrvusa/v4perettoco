# AIO-B3 — Google Business Profile: kit pronto-para-aplicar — Lola Aviamentos

**Task eKyte:** 10049813 — [AIO B3] Google Business Profile otimizado
**Data:** 09/10/2026 · **Executor:** Marcos Luciano · **Responsável:** André Bock
**Premissa:** sem acesso ao painel do Business Profile nesta etapa — todo o kit abaixo é copiar-colar para quem tiver acesso aplicar em ~30 min, mais os sinais locais que aplicamos no site.

---

## 1. Auditoria (achado → ação → quem aplica)

| # | Achado | Ação | Quem |
|---|---|---|---|
| 1 | Perfil existe mas sem otimização p/ AI Search local (gap auditoria) | Aplicar itens 2–6 | Cliente/GP com acesso |
| 2 | NAP disperso em bios e páginas | Fixar NAP canônico do item 6 em GBP, site, Instagram, Facebook, YouTube | Cliente/GP + TECH |
| 3 | Sem mapa incorporado no site | Colar snippet do item 4 em `/empresa/` e `/contato/` (bloco HTML Nuvemshop) | TECH com acesso à loja |
| 4 | Store/Organization JSON-LD já no ar via GTM (tags 67/68) | Manter; confere NAP idêntico ao item 6 | OK (verificado 30/09) |
| 5 | Zero avaliações direcionadas | Disparar modelo do item 5 no pós-compra via WhatsApp | Cliente |
| 6 | Sem posts no perfil | Calendário de 4 posts no item 7 | Cliente/GP |

---

## 2. Categorias (colar no painel)

- **Primária:** Loja de tecidos *(categoria GBP mais próxima de aviamentos/entretelas; validar "Atacadista" se o perfil for B2B puro)*
- **Secundárias:** Loja de artesanato · Atacadista · Loja de máquinas de costura *(se houver linha de máquinas)* · Fabricante de tecidos *(se aplicável)*

---

## 3. Descrição do perfil (750 caracteres — pronta)

> Lola Aviamentos — importação e distribuição de entretelas, insumos para bonés, aviamentos têxteis e máquinas para confecção em Apucarana, no polo têxtil do Norte do Paraná. Rasgáveis de 30–90 g/m², hidrossolúveis, termocolantes de 20–60 g/m², filmes e entretelas de memória de 220–330 g/m², além de abas plásticas, reguladores, viés, telas e suede — com gramatura impressa em cada rolo e suporte técnico de aplicação. Atendemos confecções de todos os portes em todo o Brasil, com retirada local na Av. Irati, 284 (Barra Funda).

---

## 4. Mapa no site (snippet + onde colar)

**Onde:** bloco HTML personalizado no final de `https://www.lolaaviamentos.com.br/empresa/` e de `/contato/`, após o endereço, com o título "Onde estamos".

```html
<div class="lola-map">
  <h2>Onde estamos</h2>
  <p>Lola Aviamentos — Av. Irati, 284, Barra Funda, Apucarana/PR, CEP 86800-000. Seg–Sáb, 8h–18h. Tel/WhatsApp: +55 43 99119-6727.</p>
  <iframe title="Mapa — Lola Aviamentos em Apucarana/PR"
    src="https://www.google.com/maps?q=Av.+Irati,+284,+Barra+Funda,+Apucarana,+PR&output=embed"
    width="100%" height="380" style="border:0" loading="lazy"
    referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
</div>
```

O parágrafo repetindo o NAP em texto (não só no mapa) é o que o Google e as IAs leem; o iframe é o que o cliente usa.

---

## 5. Produtos, perguntas e fotos (colar no painel)

**Produtos (nome + descrição curta):** Entretela rasgável 30–90 g/m² · Entretela hidrossolúvel e filme PVA · Entretela termocolante toque macio 20–60 g/m² · Filme papel termocolante p/ patchwork · Entretela de memória 220–330 g/m² · Aba plástica curva/reta · Regulador plástico · Viés de carneira · Tela poliéster e mesh · Suede 160 g/m² · Fita mágica termocolante · Máquinas p/ confecção.

**Perguntas e respostas (5, prontas):**
1. *Vocês vendem por atacado?* Sim, para confecções de todos os portes, com envio nacional e retirada em Apucarana.
2. *Qual entretela usar no meu bordado?* Depende do tecido e da densidade — temos o guia e o suporte técnico indica a gramatura certa.
3. *Entregam fora do Paraná?* Sim, para todo o Brasil via transportadora.
4. *Vocês têm loja física?* Sim, Av. Irati, 284 (Barra Funda), Apucarana/PR, seg–sáb 8h–18h.
5. *O que é entretela de memória (cavalinho)?* Base rígida termocolante de 220–330 g/m² para bonés e viseiras, nas cores branca, cinza e preta.

**Fotos (mínimo 10):** fachada com placa · balcão/estoque de rolos · close em etiqueta com gramatura · 3 produtos-âncora (rasgável, memória, filme papel) · equipe atendendo · mapa/fachada da rua · bastidor com bordado em produção.

**Mensagem pós-compra (WhatsApp, pedir avaliação):**
> Obrigado por comprar na Lola! Se o atendimento e o material te ajudaram, avalia a gente no Google em 1 min: [link do perfil]. Isso ajuda outras confecções a acharem entretela com gramatura garantida. 🙏

---

## 6. NAP canônico (usar byte-idêntico em tudo)

- **Nome:** Lola Aviamentos *(alt: Lola Soluções em Têxteis)*
- **Endereço:** Av. Irati, 284 - Barra Funda, Apucarana/PR, CEP 86800-000
- **Telefone/WhatsApp:** +55 43 99119-6727 · **E-mail:** vendas@lolaaviamentos.com.br
- **Horário:** Segunda a sábado, 8h–18h
- **Site:** https://www.lolaaviamentos.com.br · **Blog:** https://lolaaviamentos.com.br/blog
- **Sociais:** instagram.com/lolasolucoes · facebook.com/lolasolucoestexteis · youtube.com/@lolasolucoes

---

## 7. Calendário de posts do perfil (4 semanas)

1. **Entretela rasgável 30–90 g/m²** — foto dos rolos + "base do bordado em volume" + link categoria `/bordado1/rasgo-facil/`.
2. **Filme papel p/ patchwork** — foto do produto + "aplique de contorno exato" + link do [artigo patchwork](https://lolaaviamentos.com.br/blog/posts/patchwork-guia-completo-tecidos-entretelas-insumos-b6ef852e8d7c).
3. **Memória 220–330 g/m²** — foto das cores + "copa que memoriza o formato" + link `/entretela-de-memoria/`.
4. **Onde estamos** — foto da fachada + endereço + "retirada local no polo de Apucarana".

---

## 8. Artigos-localidade (briefs p/ B3 — alimentam o perfil e o local pack)

- **A1:** "Entretelas em Apucarana: guia de compra local" — mira `aviamentos apucarana`/`lola aviamentos apucarana` (60/mês), NAP + mapa + categorias locais.
- **A2:** "Polo têxtil do Norte do Paraná: guia de fornecedores" — Apucarana–Arapongas–Londrina–Maringá, Lola como âncora local + e-commerce nacional.
- Mira: local pack regional + citações de IA com intenção local ("onde comprar entretela em Apucarana").

---

## 9. Verificação (feita em 09/10/2026)

- NAP acima = idêntico ao Organization/Store JSON-LD no ar via GTM (tags 67/68, verificado 30/09).
- Glossário e artigo patchwork no ar com bloco regional "Norte do Paraná" (sinais on-site p/ local).
- Bateria de prompts de medição: "onde comprar entretela em Apucarana?", "melhor fornecedor de insumos para bonés", "o que é patchwork e que entretela usar?" — rodar antes/depois da aplicação e logar na apresentação de fechamento (task 10383917).
