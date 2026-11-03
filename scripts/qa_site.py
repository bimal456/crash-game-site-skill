#!/usr/bin/env python3
"""Small-stuff scan of the built site. Usage: python3 tools/qa_site.py [dist_dir]

CONFIG: set DOMAIN and TRACKING_URL below for each new site before the first run.
TRACKING_URL must be the real affiliate link used in _redirects: this script fails the
build if that URL appears anywhere in the crawlable HTML, so a stale value silently
disables that check."""
import json, os, re, sys, html
from html.parser import HTMLParser
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'dist')
DOMAIN = 'https://example.com'                      # CONFIG
TRACKING_URL = 'https://REPLACE-ME.example/go/<game>'  # CONFIG: must match _redirects
BAD_TYPES = {'Review', 'AggregateRating', 'Rating'}


class Scan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.h1 = 0; self.title = ''; self._in_title = False; self.meta = {}; self.links = []; self.canon = None
        self.hreflang = {}; self.hrefs = []; self.ids = set(); self.imgs = []; self.inline = []; self.ld = []; self._in_ld = False; self._buf = ''
        self.scripts_inline = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.add(a['id'])
        for k in a:
            if k == 'style' or k.startswith('on'):
                self.inline.append(f'{tag}[{k}]')
        if tag == 'h1': self.h1 += 1
        if tag == 'title': self._in_title = True
        if tag == 'meta':
            key = a.get('name') or a.get('property')
            if key: self.meta[key] = a.get('content', '')
        if tag == 'link':
            if a.get('rel') == 'canonical': self.canon = a.get('href')
            if a.get('rel') == 'alternate' and a.get('hreflang'): self.hreflang[a['hreflang']] = a.get('href')
            if a.get('href'): self.hrefs.append(a['href'])
        if tag == 'a' and a.get('href') is not None: self.hrefs.append(a['href'])
        if tag == 'img': self.imgs.append((a.get('src', ''), a.get('alt', '')))
        if tag == 'script':
            if a.get('type') == 'application/ld+json':
                self._in_ld = True; self._buf = ''
            elif 'src' in a:
                self.hrefs.append(a['src'])
            else:
                self.scripts_inline += 1

    def handle_endtag(self, tag):
        if tag == 'title': self._in_title = False
        if tag == 'script' and self._in_ld:
            self._in_ld = False; self.ld.append(self._buf)

    def handle_data(self, d):
        if self._in_title: self.title += d
        if self._in_ld: self._buf += d


def types_in(o):
    if isinstance(o, dict):
        t = o.get('@type')
        if t: yield from ([t] if isinstance(t, str) else t)
        for v in o.values(): yield from types_in(v)
    elif isinstance(o, list):
        for v in o: yield from types_in(v)


def resolve(path):
    """Map a site path to a dist file."""
    p = path.split('?')[0]
    f = os.path.join(DIST, p.lstrip('/'))
    if p.endswith('/'):
        f = os.path.join(f, 'index.html')
    return f


def main():
    pages = []
    for d, _, fs in os.walk(DIST):
        for f in fs:
            if f.endswith('.html'):
                pages.append(os.path.join(d, f))
    pages.sort()
    fails = []
    scans = {}
    for fp in pages:
        rel = '/' + os.path.relpath(fp, DIST).replace(os.sep, '/')
        site_path = rel[:-len('index.html')] if rel.endswith('index.html') else rel
        raw = open(fp, encoding='utf-8').read()
        s = Scan(); s.feed(raw); s.close()
        scans[site_path] = s
        is_login = site_path == '/login/'
        is_404 = site_path == '/404.html'
        if re.search(r'guid', raw, re.I): fails.append(f'{site_path}: contains "guid"')
        if re.search(r'[—–]', raw): fails.append(f'{site_path}: em/en dash')
        if re.search(r'18\s*\+', raw): fails.append(f'{site_path}: "18+"')
        if re.search(r'\bKAP\b', raw): fails.append(f'{site_path}: "KAP"')
        # Owner rule: no '#' in any URL a reader can click. Allowed: the keyboard skip
        # link (#main) and JSON-LD @id node identifiers, neither of which is navigable.
        body_only = re.sub(r'<script[^>]*>.*?</script>', '', raw, flags=re.S | re.I)
        for href in re.findall(r'<a\b[^>]*href="([^"]*#[^"]*)"', body_only, re.I):
            if href == '#main':
                continue
            fails.append(f'{site_path}: link to a fragment (owner rule: no # in any URL): {href}')
        # Owner rule: no pop-up / modal / overlay / age gate of any kind.
        for pat in (r'class="[^"]*\b(modal|overlay|popup|pop-up|interstitial|age-gate|agegate)\b',
                    r'<dialog\b', r'\bshowModal\s*\('):
            if re.search(pat, body_only, re.I):
                fails.append(f'{site_path}: pop-up/modal/overlay markup matched /{pat}/')
        if TRACKING_URL in raw: fails.append(f'{site_path}: tracking URL in crawlable HTML')
        if ' style="' in raw: fails.append(f'{site_path}: inline style=')
        if s.inline: fails.append(f'{site_path}: inline attrs {sorted(set(s.inline))}')
        if s.scripts_inline and not is_login: fails.append(f'{site_path}: inline <script>')
        if is_login:
            if 'noindex' not in s.meta.get('robots', ''): fails.append('/login/: not noindex')
            continue
        if s.h1 != 1: fails.append(f'{site_path}: {s.h1} h1')
        for src, alt in s.imgs:
            if not alt.strip(): fails.append(f'{site_path}: img without alt {src}')
            if not os.path.exists(resolve(src)): fails.append(f'{site_path}: missing img {src}')
        if is_404:
            if 'noindex' not in s.meta.get('robots', ''): fails.append('/404.html: not noindex')
            continue
        t = html.unescape(s.title.strip())
        d = s.meta.get('description', '')
        if len(t) > 60: fails.append(f'{site_path}: title {len(t)} > 60')
        if not (150 <= len(d) <= 160): fails.append(f'{site_path}: description {len(d)} chars')
        if s.canon != DOMAIN + site_path: fails.append(f'{site_path}: canonical {s.canon}')
        if 'x-default' not in s.hreflang: fails.append(f'{site_path}: no x-default hreflang')
        if DOMAIN + site_path not in s.hreflang.values(): fails.append(f'{site_path}: hreflang lacks self')
        for k in ('og:image', 'og:title', 'og:description', 'og:url', 'og:type', 'og:locale', 'twitter:card', 'twitter:image', 'og:image:width'):
            if not s.meta.get(k): fails.append(f'{site_path}: missing {k}')
        if 'noindex' in s.meta.get('robots', ''): fails.append(f'{site_path}: noindex on indexable page')
        if not s.ld: fails.append(f'{site_path}: no JSON-LD')
        for block in s.ld:
            try:
                data = json.loads(block)
                bad = BAD_TYPES & set(types_in(data))
                if bad: fails.append(f'{site_path}: banned schema {bad}')
            except Exception as e:
                fails.append(f'{site_path}: JSON-LD invalid {e}')
    # links
    nlinks = 0
    for site_path, s in scans.items():
        if site_path == '/login/': continue
        for h in s.hrefs:
            if h.startswith(('mailto:', 'tel:')): continue
            u = urlparse(h)
            if u.scheme in ('http', 'https'):
                if u.netloc != urlparse(DOMAIN).netloc: continue
                h = u.path + (('#' + u.fragment) if u.fragment else '')
            nlinks += 1
            path, _, frag = h.partition('#')
            if not path:
                target = site_path
            else:
                target = path.split('?')[0]
            if target in ('/play', '/play/'):
                if '/play ' not in open(os.path.join(DIST, '_redirects')).read():
                    fails.append(f'{site_path}: /play cloak missing in _redirects')
                continue
            f = resolve(target)
            if not os.path.exists(f):
                fails.append(f'{site_path}: broken link {h}')
                continue
            if frag:
                key = target if target.endswith('/') or target.endswith('.html') else target
                ts = scans.get(key)
                if ts is not None and frag not in ts.ids:
                    fails.append(f'{site_path}: missing anchor {h}')
    # sitemap / robots
    sm = os.path.join(DIST, 'sitemap.xml')
    n_sm = 0
    try:
        tree = ET.parse(sm)
        ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        for loc in tree.getroot().findall('s:url/s:loc', ns):
            n_sm += 1
            p = urlparse(loc.text).path
            if p.startswith('/login') or p.endswith('404.html'): fails.append(f'sitemap lists {p}')
            if not os.path.exists(resolve(p)): fails.append(f'sitemap lists missing {p}')
            elif 'noindex' in scans.get(p, Scan()).meta.get('robots', ''): fails.append(f'sitemap lists noindex {p}')
    except Exception as e:
        fails.append(f'sitemap invalid: {e}')
    robots = open(os.path.join(DIST, 'robots.txt')).read()
    for need in ('Disallow: /login', 'Disallow: /play', f'Sitemap: {DOMAIN}/sitemap.xml'):
        if need not in robots: fails.append(f'robots.txt missing "{need}"')
    if re.search(r'^Disallow:\s*/\s*$', robots, re.M): fails.append('robots.txt disallows everything')
    hdr = open(os.path.join(DIST, '_headers')).read()
    if re.search(r'^/\*[\s\S]*?X-Robots-Tag', hdr.split('/assets/*')[0]): fails.append('_headers: X-Robots-Tag on /*')
    for f in ('_redirects', '404.html', 'favicon.ico', 'assets/style.css'):
        if not os.path.exists(os.path.join(DIST, f)): fails.append(f'missing {f}')
    # any non-html file containing tracking URL other than _redirects (should be none)
    for d, _, fs in os.walk(DIST):
        for f in fs:
            fp = os.path.join(d, f)
            if f.endswith(('.css', '.js', '.xml', '.txt')) and TRACKING_URL in open(fp, encoding='utf-8', errors='ignore').read():
                fails.append(f'tracking URL in {fp}')
    print(f'Scanned {len(pages)} html files, {nlinks} internal links, {n_sm} sitemap URLs.')
    if fails:
        print(f'FAIL ({len(fails)}):')
        for f in fails[:400]: print('  - ' + f)
        if len(fails) > 400: print(f'  ... {len(fails) - 400} more')
        sys.exit(1)
    print('ALL OK')


if __name__ == '__main__':
    main()
