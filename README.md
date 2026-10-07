# jpmarson.com.br

Site pessoal e blog de João Paulo Marson. HTML estático publicado via GitHub Pages atrás da Cloudflare; os posts do blog ficam num banco Supabase.

## Como funciona o blog

```
 /admin/  ──salva──▶  Supabase (tabela posts)
    │                        ▲
    └─ Publicar ─▶ Edge Function "publish" ─▶ GitHub Action "Publicar blog"
                                                   │
                         build.py lê os posts publicados ◀┘
                         gera blog/, covers/, RSS, sitemap
                         commit ─▶ GitHub Pages ─▶ jpmarson.com.br
```

O site continua 100% estático: o Google e o LinkedIn enxergam cada post com título, resumo e capa. O banco só é consultado na hora de gerar as páginas.

## Escrever

Acesse **https://jpmarson.com.br/admin/**, entre pelo link mágico enviado para jpmarson@gmail.com e use o editor:

- **Salvar rascunho** — guarda no banco, nada vai ao ar.
- **Publicar** / **Salvar e atualizar site** — salva e dispara a geração do site (1 a 2 minutos).
- **Despublicar** — tira o post do ar e o devolve a rascunho. Nada é apagado.
- Imagens: botão 🖼, colar (Cmd+V) ou arrastar para o texto. Vão para o Supabase Storage.
- Inglês é opcional: sem título e texto em inglês, o post aparece no índice EN marcado como "em português".
- O editor guarda no navegador o que ainda não foi salvo e oferece recuperar se a aba fechar.

Markdown suportado: `##`/`###` títulos, `**negrito**`, `*itálico*`, `` `código` ``, blocos ```` ``` ````, listas `-` e `1.`, citações `>`, links `[texto](url)`, imagens `![legenda](url)` e `---`.

## Estrutura

```
index.html              home (PT/EN/ES, tema claro/escuro)
admin/                  painel de escrita (não indexado)
blog-config.json        URL e chave pública do Supabase (valores públicos)
build.py                gerador do blog (só biblioteca padrão do Python)
blog_theme.py           estilos e scripts compartilhados do blog
supabase/migrations/    esquema do banco, segurança (RLS) e bucket de imagens
supabase/seed/          carga inicial dos 5 posts do antigo blog Ciclo de PO
supabase/functions/     Edge Function "publish"
.github/workflows/      GitHub Action "Publicar blog"
posts/                  CÓPIA DE SEGURANÇA dos posts, gerada a cada publicação
blog/ covers/           páginas e capas geradas — não editar à mão
rss.xml rss-en.xml      feeds gerados
sitemap.xml             gerado
cv/                     currículos em PDF (PT/EN)
```

## Segurança

- Leitura pública: apenas posts com status `published`.
- Escrita: apenas o usuário autenticado `jpmarson@gmail.com` (políticas RLS em `supabase/migrations/001_blog.sql`).
- Não existe política de exclusão: posts são despublicados, nunca apagados pelo site.
- A chave em `blog-config.json` é a *publishable*, feita para ficar no navegador. A chave secreta do Supabase não é usada em lugar nenhum deste repositório.
- O token do GitHub usado para disparar a publicação fica só no Supabase (segredo `GH_DISPATCH_TOKEN`) e tem permissão apenas de "Actions" neste repositório.

## Gerar localmente

```bash
python3 build.py              # lê do Supabase
python3 build.py --markdown   # lê da cópia em posts/ (sem internet)
```

Se o banco devolver zero posts, o build para sem alterar nada (proteção contra derrubar o blog por engano).
