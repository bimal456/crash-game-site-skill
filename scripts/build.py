#!/usr/bin/env python3
"""Static multi-edition site generator (crash-game-site skill).

CONFIG: edit DOMAIN, TRACKING_URL, ORG_NAME, GAME, GAME_SEQUEL, PROVIDER, PROVIDER_URL and the EDITIONS list below for each new site.
Originally built for chickenroad.radio.am.

Usage:
  python3 tools/build.py                       # real build: content/ -> dist/
  python3 tools/build.py --content DIR --out DIR   # alternate roots (testing)
"""
import argparse, hashlib, html, json, os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = 'https://chickenroad.radio.am'
DATE = '2026-10-29'
TRACKING_URL = 'https://REPLACE-ME.example/go/<game>'  # CONFIG: the real affiliate link; lives ONLY in _redirects
ORG_NAME = 'chickenroad.radio.am'
GAME = 'Chicken Road'
GAME_SEQUEL = 'Chicken Road 2.0'
SEQUEL_SLUG = 'chicken-road-2'
PROVIDER = 'InOut Games'
PROVIDER_URL = 'https://inout.games/'

# code, base path, html lang, hreflang, og:locale
EDITIONS = [
    ('en', '/', 'en', 'en', 'en_US'),
    ('in', '/in/', 'hi', 'hi-IN', 'hi_IN'),
    ('it', '/it/', 'it', 'it-IT', 'it_IT'),
    ('de', '/de/', 'de', 'de-DE', 'de_DE'),
    ('es', '/es/', 'es', 'es-ES', 'es_ES'),
    ('fr', '/fr/', 'fr', 'fr-FR', 'fr_FR'),
    ('uk', '/uk/', 'en-GB', 'en-GB', 'en_GB'),
    ('pl', '/pl/', 'pl', 'pl-PL', 'pl_PL'),
    ('nl', '/nl/', 'nl', 'nl-NL', 'nl_NL'),
    ('ca', '/ca/', 'en-CA', 'en-CA', 'en_CA'),
    ('au', '/au/', 'en-AU', 'en-AU', 'en_AU'),
]
PAGES = ['home', 'demo', SEQUEL_SLUG, 'payments', 'about', 'contact', 'responsible-gambling', 'privacy', 'cookie-policy', 'terms']
SLUG = {p: ('' if p == 'home' else p + '/') for p in PAGES}
NAV_PAGES = PAGES  # all 10 in the primary nav
FOOTER_PAGES = PAGES
GAME_PAGES = {'home', 'demo', SEQUEL_SLUG, 'payments'}
ARTICLE_PAGES = GAME_PAGES
RELATED_PAGES = ['home', 'demo', SEQUEL_SLUG, 'payments', 'about', 'responsible-gambling']
PRIORITY = {'home': '1.0', 'demo': '0.8', SEQUEL_SLUG: '0.8', 'payments': '0.8', 'about': '0.5', 'contact': '0.5',
            'responsible-gambling': '0.5', 'privacy': '0.3', 'cookie-policy': '0.3', 'terms': '0.3'}
IMG = {'logo': (512, 512), 'gameplay': (1200, 675), 'mascot': (1200, 900), 'sequel': (1200, 675), 'og': (1200, 630)}
FIG_TARGET = {'gameplay': 'demo', 'mascot': SEQUEL_SLUG, 'sequel': 'demo'}

esc = lambda s: html.escape(html.unescape(str(s)), quote=True)


def strip_tags(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()


def read_page(path):
    raw = open(path, encoding='utf-8').read().replace('\r\n', '\n')
    m = re.match(r'---\n(.*?)\n---\n(.*)', raw, re.S)
    if not m:
        raise ValueError(f'front matter missing in {path}')
    meta = {}
    for line in m.group(1).split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            meta[k.strip()] = v.strip()
    return meta, m.group(2)


def load_editions(content_root):
    eds = []
    for code, base, lang, hreflang, ogl in EDITIONS:
        d = os.path.join(content_root, code)
        missing = [p for p in PAGES if not os.path.exists(os.path.join(d, p + '.html'))]
        if not os.path.exists(os.path.join(d, 'strings.json')):
            missing.append('strings.json')
        if missing:
            print(f'WARNING: skipping edition {code}: missing {", ".join(missing)}', file=sys.stderr)
            continue
        s = json.load(open(os.path.join(d, 'strings.json'), encoding='utf-8'))
        pages = {p: read_page(os.path.join(d, p + '.html')) for p in PAGES}
        eds.append(dict(code=code, base=base, lang=lang, hreflang=hreflang, ogl=ogl, s=s, pages=pages))
    return eds


def url(ed, page):
    return DOMAIN + ed['base'] + SLUG[page]


def path_of(ed, page):
    return ed['base'] + SLUG[page]


def cta_box(ed, key):
    s = ed['s']
    c = s.get(key) or s['cta']
    return (f'<aside class="cta-box" aria-label="{esc(c["title"])}">'
            f'<p class="cta-title">{esc(c["title"])}</p>'
            f'<p class="cta-text">{esc(c["text"])}</p>'
            f'<div class="cta-actions">'
            f'<a class="button button-primary" href="{DOMAIN}/play" target="_blank" rel="nofollow sponsored noopener">{esc(c["button"])} <span aria-hidden="true">&#8599;</span></a>'
            f'<a class="button button-ghost" href="{path_of(ed, "demo")}">{esc(c["demo"])}</a>'
            f'</div><p class="cta-note">{esc(s["cta_note"])}</p></aside>')


def figure(ed, kind):
    f = ed['s']['fig']
    w, h = IMG[kind]
    target = path_of(ed, FIG_TARGET[kind])
    return (f'<figure class="fig"><a href="{target}" aria-label="{esc(f[kind + "_aria"])}">'
            f'<img src="/assets/img/{kind}.webp" width="{w}" height="{h}" alt="{esc(f[kind + "_alt"])}" loading="lazy" decoding="async"></a>'
            f'<figcaption>{esc(f[kind + "_caption"])}</figcaption></figure>')


def render_body(ed, body):
    body = body.replace('{{BASE}}', ed['base'])
    body = re.sub(r'<!--CTA-->', lambda m: cta_box(ed, 'cta'), body)
    body = re.sub(r'<!--CTA2-->', lambda m: cta_box(ed, 'cta2'), body)
    body = re.sub(r'<!--CTA3-->', lambda m: cta_box(ed, 'cta3'), body)
    body = re.sub(r'<!--FIG:(gameplay|mascot|sequel)-->', lambda m: figure(ed, m.group(1)), body)
    # external links: ensure noopener
    return body


def toc_items(body):
    return [(sid, strip_tags(h)) for sid, h in re.findall(r'<section id="([^"]+)">\s*<h2>(.*?)</h2>', body, re.S)]


def faq_items(body):
    out = []
    for q, a in re.findall(r'<details>\s*<summary>(.*?)</summary>(.*?)</details>', body, re.S):
        out.append({'@type': 'Question', 'name': strip_tags(q), 'acceptedAnswer': {'@type': 'Answer', 'text': strip_tags(a)}})
    return out


def jsonld(ed, page, meta, body, editions):
    s = ed['s']
    u = url(ed, page)
    org = {'@type': 'Organization', '@id': DOMAIN + '/#org', 'name': ORG_NAME, 'url': DOMAIN + '/',
           'logo': {'@type': 'ImageObject', 'url': DOMAIN + '/assets/img/logo.webp', 'width': 512, 'height': 512}}
    site = {'@type': 'WebSite', '@id': DOMAIN + ed['base'] + '#website', 'url': DOMAIN + ed['base'], 'name': s['site_name'],
            'inLanguage': ed['hreflang'], 'publisher': {'@id': DOMAIN + '/#org'}}
    ptype = {'about': 'AboutPage', 'contact': 'ContactPage'}.get(page, 'WebPage')
    crumbs = [{'@type': 'ListItem', 'position': 1, 'name': s['nav']['home'], 'item': url(ed, 'home')}]
    if page != 'home':
        crumbs.append({'@type': 'ListItem', 'position': 2, 'name': strip_tags(meta.get('crumb') or s['nav'][page]), 'item': u})
    bc = {'@type': 'BreadcrumbList', '@id': u + '#breadcrumb', 'itemListElement': crumbs}
    wp = {'@type': ptype, '@id': u + '#webpage', 'url': u, 'name': strip_tags(meta['title']), 'description': strip_tags(meta['description']),
          'inLanguage': ed['hreflang'], 'isPartOf': {'@id': site['@id']}, 'breadcrumb': {'@id': bc['@id']},
          'datePublished': DATE, 'dateModified': DATE,
          'primaryImageOfPage': {'@type': 'ImageObject', 'url': DOMAIN + '/assets/img/og.webp', 'width': 1200, 'height': 630}}
    if page in GAME_PAGES:
        game = GAME_SEQUEL if page == SEQUEL_SLUG else GAME
        wp['about'] = {'@type': 'VideoGame', 'name': game, 'genre': 'Crash game', 'gamePlatform': ['Web browser', 'Mobile browser'],
                       'publisher': {'@type': 'Organization', 'name': PROVIDER, 'url': PROVIDER_URL}}
    graph = [org, site, wp, bc]
    if page in ARTICLE_PAGES:
        graph.append({'@type': 'Article', '@id': u + '#article', 'headline': strip_tags(meta['h1'])[:110], 'description': strip_tags(meta['description']),
                      'inLanguage': ed['hreflang'], 'mainEntityOfPage': {'@id': wp['@id']}, 'datePublished': DATE, 'dateModified': DATE,
                      'image': DOMAIN + '/assets/img/og.webp',
                      'author': {'@id': DOMAIN + '/#org'},
                      'publisher': {'@id': DOMAIN + '/#org'}})
    faqs = faq_items(body)
    if faqs:
        graph.append({'@type': 'FAQPage', '@id': u + '#faq', 'inLanguage': ed['hreflang'], 'mainEntity': faqs})
    data = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, separators=(',', ':'))
    return data.replace('</', '<\\/')


def head(ed, page, meta, body, editions, css_v, js_v):
    s = ed['s']
    u = url(ed, page)
    title, desc = esc(meta['title']), esc(meta['description'])
    alts = ''.join(f'<link rel="alternate" hreflang="{e["hreflang"]}" href="{url(e, page)}">' for e in editions)
    xdef = next((e for e in editions if e['code'] == 'en'), editions[0])
    alts += f'<link rel="alternate" hreflang="x-default" href="{url(xdef, page)}">'
    ogalt = ''.join(f'<meta property="og:locale:alternate" content="{e["ogl"]}">' for e in editions if e is not ed)
    ogtype = 'article' if page in ARTICLE_PAGES else 'website'
    img = DOMAIN + '/assets/img/og.webp'
    return f'''<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{u}">
{alts}
<meta property="og:type" content="{ogtype}">
<meta property="og:site_name" content="{esc(ORG_NAME)}">
<meta property="og:locale" content="{ed['ogl']}">{ogalt}
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{u}">
<meta property="og:image" content="{img}">
<meta property="og:image:type" content="image/webp">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(s['logo_alt'])}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{img}">
<meta name="theme-color" content="#14213d">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="stylesheet" href="/assets/style.css?v={css_v}">
<script src="/assets/site.js?v={js_v}" defer></script>
<script type="application/ld+json">{jsonld(ed, page, meta, body, editions)}</script>
</head>'''


def header(ed, page):
    s = ed['s']
    nav = ''.join(f'<a href="{path_of(ed, p)}"{" aria-current=\"page\"" if p == page else ""}>{esc(s["nav"][p])}</a>' for p in NAV_PAGES)
    return f'''<a class="skip" href="#main">{esc(s['skip'])}</a>
<header class="site-header"><div class="wrap">
<a class="brand" href="{ed['base']}" aria-label="{esc(s['site_name'])}: {esc(s['nav']['home'])}"><img src="/assets/img/logo.webp" width="512" height="512" alt="{esc(s['logo_alt'])}"><span class="brand-text"><span class="brand-name">{esc(s['site_name'])}</span><span class="brand-desc">{esc(s['descriptor'])}</span></span></a>
<input type="checkbox" id="nav-check" class="nav-check" aria-label="{esc(s['menu'])}">
<label for="nav-check" class="nav-toggle" aria-controls="primary-nav"><span class="burger" aria-hidden="true"></span>{esc(s['menu'])}</label>
<nav class="primary-nav" id="primary-nav" aria-label="{esc(s['nav_aria'])}">{nav}</nav>
</div></header>'''


def breadcrumb(ed, page, meta):
    s = ed['s']
    if page == 'home':
        items = f'<li><span aria-current="page">{esc(s["nav"]["home"])}</span></li>'
    else:
        items = (f'<li><a href="{ed["base"]}">{esc(s["nav"]["home"])}</a></li>'
                 f'<li><span aria-current="page">{esc(meta.get("crumb") or s["nav"][page])}</span></li>')
    return f'<nav class="breadcrumb wrap" aria-label="{esc(s["breadcrumb_aria"])}"><ol>{items}</ol></nav>'


def opening(ed, meta):
    s = ed['s']
    return f'''<div class="opening wrap"><div class="opening-inner">
<span class="eyebrow">{esc(meta['eyebrow'])}</span>
<h1>{esc(meta['h1'])}</h1>
<p class="lead">{meta['lead']}</p>
<p class="byline">{esc(s['updated'])} <time datetime="{DATE}">{esc(s['date_human'])}</time> · <a href="{path_of(ed, 'about')}#method">{esc(s['method_link'])}</a></p>
</div></div>'''


def related(ed, page):
    s = ed['s']
    cards = ''.join(f'<a class="related-card" href="{path_of(ed, p)}"><strong>{esc(s["nav"][p])}</strong><span>{esc(s["related_desc"].get(p, ""))}</span></a>'
                    for p in RELATED_PAGES if p != page)
    return f'<section class="related wrap" aria-labelledby="related-title"><h2 id="related-title">{esc(s["related_title"])}</h2><div class="related-grid">{cards}</div></section>'


def footer(ed, page, editions):
    s = ed['s']
    nav = ''.join(f'<li><a href="{path_of(ed, p)}">{esc(s["nav"][p])}</a></li>' for p in FOOTER_PAGES)
    target = page if page else 'home'
    eds = ''.join(f'<li><a href="{path_of(e, target)}" hreflang="{e["hreflang"]}" lang="{e["lang"]}"{" aria-current=\"true\"" if e is ed else ""}>{esc(e["s"]["edition_name"])} ({esc(e["s"]["lang_name"])})</a></li>'
                  for e in editions)
    return f'''<footer class="site-footer"><div class="wrap">
<div class="footer-grid">
<div><a class="footer-brand" href="{ed['base']}"><img src="/assets/img/logo.webp" width="512" height="512" alt="{esc(s['logo_alt'])}" loading="lazy">{esc(s['site_name'])}</a><p>{esc(s['footer_about'])}</p></div>
<div><p class="footer-title">{esc(s['nav_aria'])}</p><ul class="footer-nav">{nav}</ul></div>
<div><p class="footer-title">{esc(s['editions_label'])}</p><ul class="editions">{eds}</ul></div>
</div>
<div class="footer-rg"><p>{esc(s['footer_rg'])}</p><p>{esc(s['footer_legal'])}</p><p class="footer-copy">{esc(s['footer_copy'])}</p></div>
</div></footer>'''


def render_page(ed, page, editions, css_v, js_v):
    meta, raw_body = ed['pages'][page]
    body = render_body(ed, raw_body)
    toc_html = ''  # no table of contents (owner rule)
    return f'''<!doctype html>
<html lang="{ed['lang']}">
{head(ed, page, meta, body, editions, css_v, js_v)}
<body>
{header(ed, page)}
{breadcrumb(ed, page, meta)}
<main id="main">
{opening(ed, meta)}
<div class="layout wrap">
{toc_html}
<article class="content">
{body}
</article>
</div>
{related(ed, page)}
</main>
{footer(ed, page, editions)}
</body>
</html>
'''


def render_404(editions, css_v, js_v):
    ed = next((e for e in editions if e['code'] == 'en'), editions[0])
    s = ed['s']
    links = ''.join(f'<li><a href="{e["base"]}" hreflang="{e["hreflang"]}" lang="{e["lang"]}">{esc(e["s"]["edition_name"])} ({esc(e["s"]["lang_name"])})</a></li>' for e in editions)
    return f'''<!doctype html>
<html lang="{ed['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(s['notfound_title'])} | {esc(ORG_NAME)}</title>
<meta name="robots" content="noindex, follow">
<meta name="theme-color" content="#14213d">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="stylesheet" href="/assets/style.css?v={css_v}">
<script src="/assets/site.js?v={js_v}" defer></script>
</head>
<body>
{header(ed, None)}
<main id="main" class="notfound wrap">
<p class="big" aria-hidden="true">404</p>
<h1>{esc(s['notfound_title'])}</h1>
<p class="lead">{esc(s['notfound_text'])}</p>
<p><a class="button button-primary" href="/">{esc(s['back_home'])}</a></p>
<h2>{esc(s['editions_label'])}</h2>
<ul class="edition-list">{links}</ul>
</main>
{footer(ed, 'home', editions)}
</body>
</html>
'''


LOGIN_HTML = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow, noarchive, nosnippet, noimageindex">
<meta name="googlebot" content="noindex, nofollow, noarchive, nosnippet">
<meta name="referrer" content="no-referrer">
<meta http-equiv="refresh" content="0; url={TRACKING_URL}">
<title>Redirecting</title>
<script>(function(){{var u="{TRACKING_URL}";try{{window.location.replace(u);}}catch(e){{window.location.href=u;}}}})();</script>
</head>
<body>
<p>Redirecting to the operator. <a href="{TRACKING_URL}" rel="nofollow sponsored noopener">Continue</a></p>
</body>
</html>
'''


def sitemap(editions):
    xdef = next((e for e in editions if e['code'] == 'en'), editions[0])
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for ed in editions:
        for p in PAGES:
            alts = ''.join(f'<xhtml:link rel="alternate" hreflang="{e["hreflang"]}" href="{url(e, p)}"/>' for e in editions)
            alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{url(xdef, p)}"/>'
            out.append(f'<url><loc>{url(ed, p)}</loc><lastmod>{DATE}</lastmod><priority>{PRIORITY[p]}</priority>{alts}</url>')
    out.append('</urlset>')
    return '\n'.join(out) + '\n'


ROBOTS = f'''User-agent: *
Allow: /
Disallow: /login
Disallow: /play

Sitemap: {DOMAIN}/sitemap.xml
'''

CSP = "default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; font-src 'self'; connect-src 'self'; frame-ancestors 'none'; object-src 'none'; base-uri 'self'; form-action 'none'"
LOGIN_CSP = "default-src 'none'; script-src 'unsafe-inline'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'"
HEADERS = f'''/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: DENY
  Permissions-Policy: camera=(), microphone=(), geolocation=(), interest-cohort=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  Content-Security-Policy: {CSP}

/assets/*
  Cache-Control: public, max-age=31536000, immutable

/play
  X-Robots-Tag: noindex, nofollow, noarchive
  Referrer-Policy: no-referrer
  Cache-Control: no-store

/play/*
  X-Robots-Tag: noindex, nofollow, noarchive
  Referrer-Policy: no-referrer
  Cache-Control: no-store
'''

REDIRECTS = f'''# Affiliate cloak: /play -> tracking link (302). The tracking URL lives only in this file.
/play {TRACKING_URL} 302
/play/ {TRACKING_URL} 302
/play/* {TRACKING_URL} 302
/login /play 301
/login/ /play 301
/login/* /play 301
'''


def short_hash(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()[:10]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--content', default=os.path.join(ROOT, 'content'))
    ap.add_argument('--out', default=os.path.join(ROOT, 'dist'))
    a = ap.parse_args()
    editions = load_editions(a.content)
    if not editions:
        sys.exit('No complete editions found.')
    out = a.out
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(os.path.join(out, 'assets', 'img'))
    src_assets = os.path.join(ROOT, 'assets')
    shutil.copy(os.path.join(src_assets, 'style.css'), os.path.join(out, 'assets', 'style.css'))
    shutil.copy(os.path.join(src_assets, 'site.js'), os.path.join(out, 'assets', 'site.js'))
    shutil.copy(os.path.join(src_assets, 'favicon.ico'), os.path.join(out, 'favicon.ico'))
    for f in os.listdir(os.path.join(src_assets, 'img')):
        shutil.copy(os.path.join(src_assets, 'img', f), os.path.join(out, 'assets', 'img', f))
    css_v, js_v = short_hash(os.path.join(src_assets, 'style.css')), short_hash(os.path.join(src_assets, 'site.js'))
    n = 0
    for ed in editions:
        for p in PAGES:
            d = os.path.join(out, (ed['base'] + SLUG[p]).strip('/'))
            os.makedirs(d, exist_ok=True)
            open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(render_page(ed, p, editions, css_v, js_v))
            n += 1
    open(os.path.join(out, '404.html'), 'w', encoding='utf-8').write(render_404(editions, css_v, js_v))
    open(os.path.join(out, 'robots.txt'), 'w').write(ROBOTS)
    open(os.path.join(out, 'sitemap.xml'), 'w', encoding='utf-8').write(sitemap(editions))
    open(os.path.join(out, '_headers'), 'w').write(HEADERS)
    open(os.path.join(out, '_redirects'), 'w').write(REDIRECTS)
    print(f'Built {n} pages for {len(editions)} editions ({", ".join(e["code"] for e in editions)}) -> {out}')


if __name__ == '__main__':
    main()
