#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador do blog de jpmarson.com.br — sem dependências externas (só stdlib).

Uso:
    python3 build.py

Lê os arquivos de posts/ e gera:
    blog/index.html            índice em português
    blog/en/index.html         índice em inglês
    blog/<slug>/index.html     post em português
    blog/en/<slug>/index.html  post em inglês
    covers/<slug>.svg          imagem de capa (compartilhamento)
    rss.xml, rss-en.xml        feeds
    sitemap.xml                mapa do site (home + CVs + posts)

Formato do post — posts/<slug>.pt.md e posts/<slug>.en.md:

    ---
    title: Título do post
    date: 2026-09-27
    tags: gestão de produto, vibe coding
    summary: Uma ou duas frases que aparecem no índice e no Google.
    draft: false
    ---

    Corpo em Markdown.
"""

import os, re, html, shutil, subprocess, xml.sax.saxutils as sx
from datetime import datetime, timezone

import blog_theme as T

ROOT = os.path.dirname(os.path.abspath(__file__))
POSTS_DIR = os.path.join(ROOT, "posts")
SITE = "https://jpmarson.com.br"
AUTHOR = "João Paulo Marson"

LANGS = ["pt", "en"]

STR = {
    "pt": {
        "code": "pt-BR", "ogloc": "pt_BR",
        "blog_title": "Artigos",
        "blog_tag": "// notas sobre produto, tecnologia e times",
        "blog_sub": "Escrevo sobre gestão de produtos digitais, liderança de times de engenharia e o que a IA está mudando na forma como construímos software. Textos curtos, do que vivo na prática.",
        "meta_desc": "Artigos de João Paulo Marson sobre gestão de produtos digitais, liderança de times de desenvolvimento, vibe coding e tecnologia no mercado financeiro.",
        "all": "todos", "back": "← todos os artigos", "empty": "Nenhum artigo publicado ainda.",
        "min": "min de leitura", "views": "leituras", "like": "Curtir",
        "share": "Compartilhar", "prev": "Anterior", "next": "Próximo",
        "home": "início", "blog_nav": "artigos",
        "by": "por", "published": "Publicado em",
        "months": ["jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"],
    },
    "en": {
        "code": "en", "ogloc": "en_US",
        "blog_title": "Writing",
        "blog_tag": "// notes on product, technology and teams",
        "blog_sub": "I write about digital product management, leading engineering teams, and what AI is changing in the way we build software. Short pieces, drawn from practice.",
        "meta_desc": "Articles by João Paulo Marson on digital product management, engineering team leadership, vibe coding and technology in financial services.",
        "all": "all", "back": "← all articles", "empty": "No articles published yet.",
        "min": "min read", "views": "reads", "like": "Like",
        "share": "Share", "prev": "Previous", "next": "Next",
        "home": "home", "blog_nav": "writing",
        "by": "by", "published": "Published on",
        "months": ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
    },
}


# --------------------------------------------------------------------------
# Markdown (subconjunto suficiente para posts)
# --------------------------------------------------------------------------

def _inline(t):
    """Formatação inline. O texto já deve vir escapado."""
    t = re.sub(r'`([^`]+)`', lambda m: "<code>%s</code>" % m.group(1), t)
    t = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)',
               lambda m: '<a href="%s"%s>%s</a>' % (
                   m.group(2),
                   ' target="_blank" rel="noopener"' if m.group(2).startswith("http") else "",
                   m.group(1)), t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<![\w*])\*([^*\n]+)\*(?![\w*])', r'<em>\1</em>', t)
    return t


def markdown(src):
    """Converte um subconjunto de Markdown em HTML."""
    out, lines, i = [], src.split("\n"), 0
    while i < len(lines):
        ln = lines[i]

        # bloco de código
        if ln.startswith("```"):
            i += 1
            buf = []
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(html.escape(lines[i]))
                i += 1
            i += 1
            out.append("<pre><code>%s</code></pre>" % "\n".join(buf))
            continue

        # linha horizontal
        if re.match(r'^\s*---+\s*$', ln):
            out.append("<hr>")
            i += 1
            continue

        # títulos
        m = re.match(r'^(#{2,4})\s+(.*)$', ln)
        if m:
            lvl = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (lvl, _inline(html.escape(m.group(2).strip())), lvl))
            i += 1
            continue

        # citação
        if ln.startswith("> "):
            buf = []
            while i < len(lines) and lines[i].startswith("> "):
                buf.append(html.escape(lines[i][2:]))
                i += 1
            out.append("<blockquote><p>%s</p></blockquote>" % _inline(" ".join(buf)))
            continue

        # listas
        if re.match(r'^\s*[-*]\s+', ln) or re.match(r'^\s*\d+\.\s+', ln):
            ordered = bool(re.match(r'^\s*\d+\.\s+', ln))
            items = []
            pat = r'^\s*\d+\.\s+' if ordered else r'^\s*[-*]\s+'
            while i < len(lines) and re.match(pat, lines[i]):
                items.append(_inline(html.escape(re.sub(pat, "", lines[i]))))
                i += 1
            tag = "ol" if ordered else "ul"
            out.append("<%s>%s</%s>" % (tag, "".join("<li>%s</li>" % x for x in items), tag))
            continue

        # parágrafo
        if ln.strip():
            buf = []
            while i < len(lines) and lines[i].strip() and not lines[i].startswith(("#", ">", "```")) \
                    and not re.match(r'^\s*([-*]\s+|\d+\.\s+|---+\s*$)', lines[i]):
                buf.append(html.escape(lines[i].strip()))
                i += 1
            out.append("<p>%s</p>" % _inline(" ".join(buf)))
            continue

        i += 1
    return "\n".join(out)


# --------------------------------------------------------------------------
# Leitura dos posts
# --------------------------------------------------------------------------

def parse_post(path):
    raw = open(path, encoding="utf-8").read().lstrip()
    meta, body = {}, raw
    if raw.startswith("---"):
        end = raw.find("\n---", 3)
        if end != -1:
            for line in raw[3:end].strip().split("\n"):
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip().lower()] = v.strip()
            body = raw[end + 4:].lstrip("\n")
    meta["tags"] = [t.strip() for t in meta.get("tags", "").split(",") if t.strip()]
    meta["draft"] = str(meta.get("draft", "")).lower() in ("true", "1", "yes", "sim")
    meta["body_md"] = body
    meta["words"] = len(re.findall(r'\w+', body))
    meta["minutes"] = max(1, round(meta["words"] / 200))
    return meta


def load_posts():
    """{slug: {'pt': meta, 'en': meta}} — ordenado da data mais recente para a mais antiga."""
    posts = {}
    if not os.path.isdir(POSTS_DIR):
        return []
    for fn in sorted(os.listdir(POSTS_DIR)):
        m = re.match(r'^(.+)\.(pt|en)\.md$', fn)
        if not m:
            continue
        slug, lang = m.group(1), m.group(2)
        meta = parse_post(os.path.join(POSTS_DIR, fn))
        if meta["draft"]:
            continue
        posts.setdefault(slug, {"slug": slug})[lang] = meta
    items = [p for p in posts.values() if "pt" in p or "en" in p]
    for p in items:
        any_meta = p.get("pt") or p.get("en")
        p["date"] = any_meta.get("date", "1970-01-01")
    items.sort(key=lambda p: p["date"], reverse=True)
    return items


def fmt_date(iso, lang):
    try:
        d = datetime.strptime(iso, "%Y-%m-%d")
    except ValueError:
        return iso
    mon = STR[lang]["months"][d.month - 1]
    return "%d de %s de %d" % (d.day, mon, d.year) if lang == "pt" else "%s %d, %d" % (mon, d.day, d.year)


def post_url(slug, lang, absolute=False):
    p = "/blog/%s/" % slug if lang == "pt" else "/blog/en/%s/" % slug
    return (SITE + p) if absolute else p


def index_url(lang, absolute=False):
    p = "/blog/" if lang == "pt" else "/blog/en/"
    return (SITE + p) if absolute else p


# --------------------------------------------------------------------------
# Blocos de template
# --------------------------------------------------------------------------

def header(lang, depth, other_href):
    """depth = quantos níveis acima está a raiz do site."""
    up = "../" * depth
    s = STR[lang]
    btns = ""
    for l in LANGS:
        active = ' class="active"' if l == lang else ""
        href = "#" if l == lang else other_href
        btns += '<a href="%s"%s><button%s>%s</button></a>' % (href, "" if l != lang else "", active, l.upper())
    return """<header>
    <a class="logo" href="%(up)s">jp<span>.</span>marson</a>
    <div class="hdr-right">
      <a class="navlink" href="%(up)s">%(home)s</a>
      <nav class="lang" aria-label="Idioma">%(btns)s</nav>
      <button class="theme-btn" id="themeBtn" aria-label="Tema claro/escuro" title="Tema claro/escuro">&#9790;</button>
    </div>
  </header>""" % dict(up=up, home=s["home"], btns=btns)


def footer(lang, depth):
    up = "../" * depth
    feed = "rss.xml" if lang == "pt" else "rss-en.xml"
    return """<footer>
    <span>&copy; %(year)d <a href="%(up)s">jpmarson.com.br</a></span>
    <span><a href="%(up)s%(feed)s">RSS</a> &middot; <a href="https://www.linkedin.com/in/jpmarson" target="_blank" rel="noopener">LinkedIn</a></span>
  </footer>""" % dict(year=datetime.now().year, up=up, feed=feed)


def page(lang, title, desc, canonical, body, depth, jsonld="", og_image=None, extra_head=""):
    s = STR[lang]
    og = og_image or (SITE + "/og-image.png")
    return """<!DOCTYPE html>
<html lang="%(code)s">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<meta name="author" content="%(author)s">
<link rel="canonical" href="%(canonical)s">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta property="og:type" content="article">
<meta property="og:locale" content="%(ogloc)s">
<meta property="og:site_name" content="JP Marson">
<meta property="og:url" content="%(canonical)s">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:image" content="%(og)s">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%(title)s">
<meta name="twitter:description" content="%(desc)s">
<meta name="twitter:image" content="%(og)s">
<link rel="alternate" type="application/rss+xml" title="JP Marson" href="%(site)s/%(feed)s">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='20' fill='%%230a66ff'/><text x='50' y='68' font-size='48' fill='white' text-anchor='middle' font-family='monospace' font-weight='bold'>jp</text></svg>">
%(extra_head)s%(jsonld)s
<style>%(css)s</style>
</head>
<body>
%(boot)s
<div class="wrap">
%(body)s
</div>
<script>%(theme_js)s%(engage_js)s</script>
</body>
</html>""" % dict(
        code=s["code"], ogloc=s["ogloc"], title=html.escape(title), desc=html.escape(desc),
        author=AUTHOR, canonical=canonical, og=og, site=SITE,
        feed="rss.xml" if lang == "pt" else "rss-en.xml",
        extra_head=extra_head, jsonld=jsonld, css=T.CSS, boot=T.THEME_BOOT,
        body=body, theme_js=T.THEME_JS, engage_js=T.ENGAGE_JS)


# --------------------------------------------------------------------------
# Páginas
# --------------------------------------------------------------------------

def build_index(posts, lang):
    s = STR[lang]
    other = "en" if lang == "pt" else "pt"
    cards, tags = [], []
    for p in posts:
        meta = p.get(lang) or p.get(other)
        if not meta:
            continue
        fallback = "" if p.get(lang) else ' <span class="ptag">%s</span>' % (
            "em português" if lang == "en" else "in English")
        url = post_url(p["slug"], lang if p.get(lang) else other)
        for t in meta["tags"]:
            if t not in tags:
                tags.append(t)
        cards.append("""<a class="pcard" href="%(url)s" data-tags="%(dt)s">
      <div class="pmeta"><span>%(date)s</span><span class="dot">&middot;</span><span>%(min)d %(minlbl)s</span>%(fb)s</div>
      <h2>%(title)s</h2>
      <p>%(summary)s</p>
      <div class="ptags">%(tags)s</div>
    </a>""" % dict(
            url=html.escape(url, quote=True),
            dt=html.escape("|".join(meta["tags"]), quote=True),
            date=fmt_date(meta.get("date", ""), lang), min=meta["minutes"], minlbl=s["min"],
            fb=fallback, title=html.escape(meta.get("title", "")),
            summary=html.escape(meta.get("summary", "")),
            tags="".join('<span class="ptag">%s</span>' % html.escape(t) for t in meta["tags"])))

    filters = '<button class="filter on" data-t="">%s</button>' % html.escape(s["all"])
    filters += "".join('<button class="filter" data-t="%s">%s</button>'
                       % (html.escape(t, quote=True), html.escape(t)) for t in tags)

    body = """%(header)s
  <main>
    <div class="page-tag">%(tag)s</div>
    <h1 class="page-title">%(title)s</h1>
    <p class="page-sub">%(sub)s</p>
    %(filters)s
    <div class="postlist" id="list">%(cards)s</div>
  </main>
%(footer)s
<script>
document.querySelectorAll(".filter").forEach(function(b){
  b.addEventListener("click",function(){
    document.querySelectorAll(".filter").forEach(function(x){x.classList.remove("on");});
    b.classList.add("on");
    var t=b.dataset.t;
    document.querySelectorAll(".pcard").forEach(function(c){
      var has=!t||(c.dataset.tags||"").split("|").indexOf(t)>=0;
      c.style.display=has?"":"none";
    });
  });
});
</script>""" % dict(
        header=header(lang, 2 if lang == "en" else 1, index_url("en" if lang == "pt" else "pt")),
        tag=html.escape(s["blog_tag"]), title=html.escape(s["blog_title"]),
        sub=html.escape(s["blog_sub"]),
        filters=('<div class="filters">%s</div>' % filters) if tags else "",
        cards="".join(cards) or '<p class="empty">%s</p>' % html.escape(s["empty"]),
        footer=footer(lang, 2 if lang == "en" else 1))

    jsonld = """
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Blog","name":"%s — %s","url":"%s",
 "inLanguage":"%s",
 "author":{"@type":"Person","name":"%s","url":"%s/"},
 "description":"%s"}
</script>""" % (AUTHOR, s["blog_title"], index_url(lang, True), s["code"], AUTHOR, SITE,
                html.escape(s["meta_desc"]))

    return page(lang, "%s — %s" % (s["blog_title"], AUTHOR), s["meta_desc"],
                index_url(lang, True), body, 2 if lang == "en" else 1, jsonld)


def build_post(p, lang, prev, nxt):
    meta = p[lang]
    s = STR[lang]
    slug = p["slug"]
    depth = 3 if lang == "en" else 2
    other = "en" if lang == "pt" else "pt"
    other_href = post_url(slug, other) if p.get(other) else index_url(other)

    url = post_url(slug, lang, True)
    cover = "%s/covers/%s.png" % (SITE, slug)

    share_txt = "%s %s" % (meta.get("title", ""), url)
    share = """<div class="share">
        <a href="https://www.linkedin.com/sharing/share-offsite/?url=%s" target="_blank" rel="noopener">LinkedIn</a>
        <a href="https://api.whatsapp.com/send?text=%s" target="_blank" rel="noopener">WhatsApp</a>
      </div>""" % (html.escape(url, quote=True),
                   html.escape(share_txt.replace(" ", "%20"), quote=True))

    engage = """<div class="engage" id="engage" data-slug="%(slug)s">
      <button class="like" id="likeBtn"><span class="heart">&#9829;</span><span id="likeCount">0</span></button>
      <span class="views" id="viewsBox" style="visibility:hidden">&#128065; <span id="viewCount">0</span> %(views)s</span>
      %(share)s
    </div>""" % dict(slug=html.escape(slug, quote=True), views=html.escape(s["views"]), share=share)

    np = ""
    if prev or nxt:
        cards = ""
        if prev and prev.get(lang):
            cards += '<a class="np" href="%s"><span class="k">%s</span><strong>%s</strong></a>' % (
                html.escape("../../" + ("en/" if lang == "en" else "") + prev["slug"] + "/", quote=True),
                html.escape(s["prev"]), html.escape(prev[lang].get("title", "")))
        if nxt and nxt.get(lang):
            cards += '<a class="np" href="%s"><span class="k">%s</span><strong>%s</strong></a>' % (
                html.escape("../../" + ("en/" if lang == "en" else "") + nxt["slug"] + "/", quote=True),
                html.escape(s["next"]), html.escape(nxt[lang].get("title", "")))
        if cards:
            np = '<div class="nextprev">%s</div>' % cards

    body = """%(header)s
  <main>
    <a class="back" href="%(back_href)s">%(back)s</a>
    <article>
      <h1>%(title)s</h1>
      <div class="amet"><span>%(date)s</span><span class="dot">&middot;</span><span>%(min)d %(minlbl)s</span>%(tags)s</div>
      %(lede)s
      <div class="body">%(content)s</div>
      %(engage)s
      %(np)s
    </article>
  </main>
%(footer)s""" % dict(
        header=header(lang, depth, other_href),
        back_href=html.escape("../" if lang == "pt" else "../", quote=True),
        back=html.escape(s["back"]),
        title=html.escape(meta.get("title", "")),
        date=fmt_date(meta.get("date", ""), lang), min=meta["minutes"], minlbl=s["min"],
        tags="".join('<span class="ptag">%s</span>' % html.escape(t) for t in meta["tags"]),
        lede=('<p class="lede">%s</p>' % html.escape(meta["summary"])) if meta.get("summary") else "",
        content=markdown(meta["body_md"]),
        engage=engage, np=np, footer=footer(lang, depth))

    alts = ""
    for l in LANGS:
        if p.get(l):
            alts += '\n<link rel="alternate" hreflang="%s" href="%s">' % (STR[l]["code"], post_url(slug, l, True))
    alts += '\n<link rel="alternate" hreflang="x-default" href="%s">' % post_url(slug, "pt" if p.get("pt") else "en", True)

    jsonld = """
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BlogPosting",
 "headline":%(title)s,
 "description":%(desc)s,
 "image":"%(cover)s",
 "datePublished":"%(date)s","dateModified":"%(date)s",
 "inLanguage":"%(code)s",
 "wordCount":%(words)d,
 "keywords":%(kw)s,
 "mainEntityOfPage":{"@type":"WebPage","@id":"%(url)s"},
 "author":{"@type":"Person","name":"%(author)s","url":"%(site)s/",
   "sameAs":["https://www.linkedin.com/in/jpmarson","https://github.com/jpmarson"]},
 "publisher":{"@type":"Person","name":"%(author)s","url":"%(site)s/"},
 "isPartOf":{"@type":"Blog","name":"%(author)s","url":"%(bidx)s"}}
</script>""" % dict(
        title=_json_str(meta.get("title", "")), desc=_json_str(meta.get("summary", "")),
        cover=cover, date=meta.get("date", ""), code=s["code"], words=meta["words"],
        kw="[%s]" % ",".join(_json_str(t) for t in meta["tags"]),
        url=url, author=AUTHOR, site=SITE, bidx=index_url(lang, True))

    return page(lang, "%s — %s" % (meta.get("title", ""), AUTHOR),
                meta.get("summary", ""), url, body, depth, jsonld,
                og_image=cover, extra_head=alts)


def _json_str(s):
    return '"%s"' % s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


# --------------------------------------------------------------------------
# Capa, RSS e sitemap
# --------------------------------------------------------------------------

def build_cover(p):
    """SVG de capa (1200x630). Convertido para PNG se o ImageMagick estiver disponível."""
    meta = p.get("pt") or p.get("en")
    title = meta.get("title", "")
    tags = " · ".join(meta["tags"][:3])
    # quebra o título em até 4 linhas de ~30 caracteres
    words, lines, cur = title.split(), [], ""
    for w in words:
        if len(cur + " " + w) > 30 and cur:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    lines = lines[:4]
    y0 = 300 - (len(lines) - 1) * 32
    tspans = "".join('<text x="90" y="%d" font-family="DejaVu Sans, sans-serif" font-size="56" '
                     'font-weight="bold" fill="#0f172a">%s</text>'
                     % (y0 + i * 66, sx.escape(l)) for i, l in enumerate(lines))
    return """<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <rect width="1200" height="630" fill="#fafbfd"/>
  <rect x="0" y="0" width="1200" height="10" fill="#0a66ff"/>
  <text x="90" y="120" font-family="DejaVu Sans Mono, monospace" font-size="24" fill="#0a66ff">jp.marson</text>
  <text x="90" y="168" font-family="DejaVu Sans Mono, monospace" font-size="19" fill="#5b6b83">%s</text>
  %s
  <rect x="90" y="500" width="120" height="5" rx="2" fill="#0a66ff"/>
  <text x="90" y="556" font-family="DejaVu Sans, sans-serif" font-size="24" fill="#5b6b83">%s</text>
  <text x="1110" y="556" font-family="DejaVu Sans Mono, monospace" font-size="21" fill="#93a3bd" text-anchor="end">jpmarson.com.br</text>
</svg>""" % (sx.escape(tags), tspans, sx.escape(AUTHOR))


def build_rss(posts, lang):
    s = STR[lang]
    other = "en" if lang == "pt" else "pt"
    items = []
    for p in posts:
        meta = p.get(lang)
        if not meta:
            continue
        try:
            d = datetime.strptime(meta.get("date", ""), "%Y-%m-%d").replace(tzinfo=timezone.utc)
            pub = d.strftime("%a, %d %b %Y 00:00:00 +0000")
        except ValueError:
            pub = ""
        items.append("""  <item>
    <title>%s</title>
    <link>%s</link>
    <guid isPermaLink="true">%s</guid>
    <description>%s</description>
    <pubDate>%s</pubDate>
    %s
  </item>""" % (sx.escape(meta.get("title", "")), post_url(p["slug"], lang, True),
                post_url(p["slug"], lang, True), sx.escape(meta.get("summary", "")), pub,
                "".join("<category>%s</category>" % sx.escape(t) for t in meta["tags"])))
    return """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>%s — %s</title>
  <link>%s</link>
  <atom:link href="%s/%s" rel="self" type="application/rss+xml"/>
  <description>%s</description>
  <language>%s</language>
  <lastBuildDate>%s</lastBuildDate>
%s
</channel>
</rss>
""" % (AUTHOR, s["blog_title"], index_url(lang, True), SITE,
       "rss.xml" if lang == "pt" else "rss-en.xml", sx.escape(s["meta_desc"]), s["code"],
       datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000"), "\n".join(items))


def build_sitemap(posts):
    today = datetime.now().strftime("%Y-%m-%d")
    urls = ["""  <url><loc>%s/</loc><lastmod>%s</lastmod><changefreq>monthly</changefreq><priority>1.0</priority>
    <xhtml:link rel="alternate" hreflang="pt-BR" href="%s/"/>
    <xhtml:link rel="alternate" hreflang="en" href="%s/"/>
    <xhtml:link rel="alternate" hreflang="es" href="%s/"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="%s/"/></url>""" % (SITE, today, SITE, SITE, SITE, SITE)]
    for lang in LANGS:
        urls.append("  <url><loc>%s</loc><lastmod>%s</lastmod><changefreq>weekly</changefreq>"
                    "<priority>0.9</priority></url>" % (index_url(lang, True), today))
    for p in posts:
        for lang in LANGS:
            if not p.get(lang):
                continue
            alt = "".join('\n    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>'
                          % (STR[l]["code"], post_url(p["slug"], l, True)) for l in LANGS if p.get(l))
            urls.append("  <url><loc>%s</loc><lastmod>%s</lastmod><changefreq>monthly</changefreq>"
                        "<priority>0.8</priority>%s</url>"
                        % (post_url(p["slug"], lang, True), p.get("date", today), alt))
    for cv in ("cv/joao-paulo-marson-cv-pt.pdf", "cv/joao-paulo-marson-resume-en.pdf"):
        urls.append("  <url><loc>%s/%s</loc><lastmod>%s</lastmod><priority>0.7</priority></url>"
                    % (SITE, cv, today))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
            '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n%s\n</urlset>\n' % "\n".join(urls))


# --------------------------------------------------------------------------

def svg_to_png(svg_rel, png_rel):
    """Converte a capa para PNG (redes sociais não renderizam SVG).
    Usa rsvg-convert, ImageMagick ou Inkscape — o que estiver instalado."""
    svg, png = os.path.join(ROOT, svg_rel), os.path.join(ROOT, png_rel)
    for cmd in (["rsvg-convert", "-w", "1200", "-h", "630", svg, "-o", png],
                ["convert", "-density", "96", "-background", "none", svg,
                 "-resize", "1200x630", png],
                ["inkscape", svg, "--export-type=png", "-w", "1200", "-h", "630",
                 "--export-filename=" + png]):
        if shutil.which(cmd[0]):
            try:
                subprocess.run(cmd, check=True, capture_output=True)
                return True
            except subprocess.CalledProcessError:
                continue
    print("  (aviso) capa PNG não gerada para %s — instale librsvg ou imagemagick" % svg_rel)
    return False


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def main():
    posts = load_posts()
    written = []

    for lang in LANGS:
        written.append(write("blog/index.html" if lang == "pt" else "blog/en/index.html",
                             build_index(posts, lang)))

    for i, p in enumerate(posts):
        prev = posts[i + 1] if i + 1 < len(posts) else None   # mais antigo
        nxt = posts[i - 1] if i > 0 else None                  # mais recente
        for lang in LANGS:
            if p.get(lang):
                sub = "blog/%s/index.html" % p["slug"] if lang == "pt" else "blog/en/%s/index.html" % p["slug"]
                written.append(write(sub, build_post(p, lang, prev, nxt)))
        written.append(write("covers/%s.svg" % p["slug"], build_cover(p)))
        if svg_to_png("covers/%s.svg" % p["slug"], "covers/%s.png" % p["slug"]):
            written.append("covers/%s.png" % p["slug"])

    written.append(write("rss.xml", build_rss(posts, "pt")))
    written.append(write("rss-en.xml", build_rss(posts, "en")))
    written.append(write("sitemap.xml", build_sitemap(posts)))

    print("%d post(s) · %d arquivo(s) gerado(s)" % (len(posts), len(written)))
    for w in written:
        print("  " + w)


if __name__ == "__main__":
    main()
