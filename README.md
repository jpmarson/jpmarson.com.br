# jpmarson.com.br

Site pessoal e blog de João Paulo Marson. HTML estático, sem dependências, publicado via GitHub Pages atrás da Cloudflare.

## Estrutura

```
index.html          home (PT/EN/ES, tema claro/escuro)
posts/              fonte dos artigos em Markdown  ← você escreve aqui
build.py            gerador do blog (só stdlib)
blog_theme.py       estilos e scripts compartilhados do blog
blog/               páginas geradas — não editar à mão
covers/             imagens de capa geradas — não editar à mão
cv/                 currículos em PDF (PT/EN)
rss.xml rss-en.xml  feeds gerados
sitemap.xml         gerado
```

## Escrever um artigo

Crie dois arquivos em `posts/`, um por idioma, usando o mesmo nome-base (o *slug*, que vira a URL):

```
posts/meu-artigo.pt.md
posts/meu-artigo.en.md
```

Cada arquivo começa com um cabeçalho:

```markdown
---
title: Título do artigo
date: 2026-09-27
tags: gestão de produto, vibe coding
summary: Uma ou duas frases. Aparecem no índice, no Google e no card do LinkedIn.
draft: false
---

Corpo em Markdown.
```

Campos:

| campo | obrigatório | observação |
|---|---|---|
| `title` | sim | título do artigo |
| `date` | sim | formato `AAAA-MM-DD`, define a ordem |
| `tags` | não | separadas por vírgula, viram filtros no índice |
| `summary` | sim | usado como meta description e resumo |
| `draft` | não | `true` esconde o artigo do site |

Markdown suportado: `##`/`###` títulos, `**negrito**`, `*itálico*`, `` `código` ``, blocos ```` ``` ````, listas `-` e `1.`, citações `>`, links `[texto](url)` e `---` para linha horizontal.

Só existe em um idioma? Tudo bem — o índice do outro idioma mostra o artigo marcado com o idioma disponível.

## Gerar e publicar

```bash
python3 build.py
git add -A && git commit -m "novo artigo" && git push
```

O `build.py` regenera `blog/`, `covers/`, os dois RSS e o `sitemap.xml`. Não requer instalação de nada — as capas em PNG usam `rsvg-convert`, ImageMagick ou Inkscape, se algum estiver instalado (sem eles, o site funciona, apenas a imagem de compartilhamento fica sem a versão PNG).

Depois do push, o GitHub Pages publica em cerca de um minuto. Se a Cloudflare ainda servir a versão antiga, limpe o cache em **Caching → Configuration → Purge Everything**.

## Likes e contagem de leituras

A interface já está pronta em cada artigo, mas desativada. Para ligar, suba o Worker da Cloudflare e preencha `API_BASE` em `blog_theme.py`:

```python
var API_BASE = "https://api.jpmarson.com.br";
```

Endpoints esperados: `POST /api/view/<slug>` → `{views}`, `GET|POST|DELETE /api/likes/<slug>` → `{likes}`.
