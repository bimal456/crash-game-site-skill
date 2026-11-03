#!/usr/bin/env python3
"""CONFIG: set CONTACT_EMAIL, SEQUEL_SLUG and ROOT (project folder) for each site.
Validate one edition's content files against CONTENT_SPEC.md. Usage: check_content.py <edition>"""
import sys, os, re, json, html, collections
from html.parser import HTMLParser

CONTACT_EMAIL = 'contact@chickenroad.radio.am'   # CONFIG
SEQUEL_SLUG = 'chicken-road-2'                  # CONFIG: the sequel page slug for this site
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = {
    'home': (2700, 3000), 'demo': (1500, 1800), SEQUEL_SLUG: (1500, 1800), 'payments': (1500, 1800),
    'about': (900, 1300), 'contact': (400, 700), 'responsible-gambling': (800, 1200),
    'privacy': (700, 1100), 'cookie-policy': (400, 700), 'terms': (700, 1100),
}
CONTENT_PAGES = {'home', 'demo', SEQUEL_SLUG, 'payments'}
LINK_REQ = {
    'home': {'demo': 2, SEQUEL_SLUG: 2, 'payments': 2, 'about': 1, 'responsible-gambling': 1, 'contact': 1},
    'demo': {'home': 2, SEQUEL_SLUG: 1, 'payments': 1, 'responsible-gambling': 1, 'about': 1},
    SEQUEL_SLUG: {'home': 2, 'demo': 2, 'payments': 1, 'responsible-gambling': 1, 'about': 1},
    'payments': {'home': 1, 'demo': 1, SEQUEL_SLUG: 1, 'responsible-gambling': 1, 'about': 1, 'terms': 1},
    'about': {'home': 1, 'demo': 1, SEQUEL_SLUG: 1, 'payments': 1, 'contact': 1, 'responsible-gambling': 1, 'privacy': 1},
    'contact': {'home': 1, 'about': 1, 'responsible-gambling': 1, 'privacy': 1},
    'responsible-gambling': {'home': 1, 'demo': 1, 'payments': 1, 'contact': 1},
    'privacy': {'cookie-policy': 1, 'terms': 1, 'contact': 1, 'about': 1},
    'cookie-policy': {'privacy': 1, 'terms': 1, 'contact': 1},
    'terms': {'privacy': 1, 'cookie-policy': 1, 'responsible-gambling': 1, 'contact': 1, 'about': 1},
}
SLUG2PAGE = {'': 'home', 'demo/': 'demo', SEQUEL_SLUG + '/': SEQUEL_SLUG, 'payments/': 'payments', 'about/': 'about', 'contact/': 'contact',
             'responsible-gambling/': 'responsible-gambling', 'privacy/': 'privacy', 'cookie-policy/': 'cookie-policy', 'terms/': 'terms'}
BAD_ANCHORS = re.compile(r'^(click here|here|this page|read more|clicca qui|qui|hier|klicke hier|aquí|haz clic aquí|cliquez ici|ici|tutaj|kliknij tutaj|klik hier|यहाँ|यहां क्लिक करें)$', re.I)
SLUGS = {'', 'demo/', SEQUEL_SLUG + '/', 'payments/', 'about/', 'contact/', 'responsible-gambling/', 'privacy/', 'cookie-policy/', 'terms/'}
ALLOWED_TAGS = {'section', 'h2', 'h3', 'p', 'a', 'strong', 'em', 'ul', 'ol', 'li', 'table', 'thead', 'tbody', 'tr', 'th', 'td',
                'details', 'summary', 'div', 'br', 'abbr'}
DIV_CLASSES = {'table-wrap', 'callout', 'callout callout-warn', 'callout callout-tip', 'cards', 'card', 'pros-cons', 'pros', 'cons', 'highlight'}
BANNED_ANY = [r'guid', r'leitfaden', r'ratgeber', r'przewodnik', r'poradnik', r'गाइड', r'मार्गदर्शिका', r'\bguía\b', r'\bguia\b', r'\bgids\b',
              r'18\s*\+', r'\bKAP\b', r'—', r'–', r'\b\d+(?:[.,]\d)?\s*/\s*(?:5|10)\b', r'\bstars?\b']
BANNED_META = [r'\blearn', r'\bdiscover', r'\bexplained', r'scopri', r'impara', r'spiegat', r'entdeck', r'\blern', r'erklärt', r'descubr', r'aprend',
               r'explicad', r'découvr', r'apprene', r'expliqu', r'ontdek', r'\bleer\b', r'uitgelegd', r'odkryj', r'dowiedz', r'wyjaśn', r'जानें', r'सीखें',
               r'समझाया', r'\btop\s?\d', r'\bbest\s?\d', r'\blist\b']
# Site must not position itself as independent / unofficial / not-affiliated / an "information site" (owner preference)
BANNED_POSITIONING = [r'independ', r'unabh[äa]ngig', r'indipendent', r'ind[ée]pendan', r'niezale[żz]n', r'onafhankelijk', r'स्वतंत्र',
    r'unofficial', r'non[- ]official', r'inoffiziell', r'non ufficial', r'no oficial', r'non officiel', r'nieoficjaln', r'niet officieel', r'अनौपचारिक', r'अनधिकृत साइट',
    r'not affiliated', r'no affiliation', r'non affiliat', r'nicht (mit [^.<]{0,40} )?verbunden', r'nicht offiziell', r'no (est[aá] )?afiliad', r'sin afiliaci', r'pas affili',
    r'aucune affiliation', r'niepowi[ąa]zan', r'nie jest powi[ąa]zan', r'niet (gelieerd|verbonden)', r'geen banden', r'नहीं जुड़', r'संबद्ध नहीं',
    r'info(rmation(al)?)? site', r'informational', r'info-?seite', r'informationsseite', r'informationsportal', r'sito (di )?informa', r'sito informativo',
    r'portale informativo', r'sitio (de )?informaci', r'sitio informativo', r'portal informativo', r'site d.info', r'site informatif', r'site d.information',
    r'serwis informacyjn', r'strona informacyjn', r'portal informacyjn', r'informatie-?site', r'informatieve (site|website)', r'informatiewebsite', r'जानकारी (वाली )?साइट',
    r'we are not (the|a|an) (casino|operator)', r'no games (are )?hosted',
    # Owner rule (round 2, item 16): "information" as a description of what the site itself publishes.
    # Narrow phrases only, so legitimate uses survive ("the game's info panel", "tax information", "personal information").
    r'(?:only |general |for general )information about (?:this|the|our) (?:site|game|pages)',
    r'information only, not advice', r'we publish information', r'publishes information',
    r'(?:this site|the site) (?:is|provides|offers) (?:general )?information',
    r'nur information', r'solo informaci[oó]n', r'(?:solo|soltanto) informazioni',
    r'uniquement (?:de l.)?information', r'charakter informacyjny', r'alleen informatie', r'केवल जानकारी']
# Owner rule (round 4): NO visible promotional-disclosure line, in any language, on any page.
# Scoped to strings.json values and the disclosure markup, NOT to page body prose: the
# affiliate-disclosure SECTION inside about/terms legitimately says "the site contains
# promotional links to casinos ...", and that is page content, not the banner line.
BANNED_DISCLOSURE = [r'contains promotional links', r'promotional links for adults', r'enth[äa]lt werbelinks', r'werbelinks f[üu]r',
    r'contiene enlaces promocionales', r'enlaces promocionales para', r'link promozionali rivolti', r'contiene link promozionali\.',
    r'contient des liens promotionnels', r'liens promotionnels destin', r'bevat promotielinks\.', r'promotielinks voor',
    r'zawiera linki promocyjne\.', r'linki promocyjne dla', r'प्रमोशनल लिंक हैं।', r'class="disclosure"', r'"independence"\s*:']

# No reviewer / third-party voice (owner rule): no review words, verdicts, editorial team, "we tested"
BANNED_VOICE = [r'\breview', r'reviewer', r'\bverdict', r'recension', r'rezension', r'testbericht', r'veredicto', r'rese[ñn]a', r'recenzj', r'recenzent',
    r'recensie', r'beoordeling', r'समीक्षा', r'रिव्यू', r'editorial', r'redazion', r'redaktion', r'redacci[oó]n', r'r[ée]daction', r'redakcj', r'redactie',
    r'संपादकीय', r'we tested', r'our test', r'tested by', r'getestet', r'abbiamo testato', r'hemos probado', r'nous avons test', r'przetestowali', r'verdetto',
    r'werdykt', r'oordeel', r'our opinion', r'in our view', r'our take', r'हमने टेस्ट', r'हमारी राय']
FIRST_PERSON = {
    'en': r'\b(we|we\'re|we\'ve|our|ours|us)\b', 'uk': r'\b(we|we\'re|we\'ve|our|ours|us)\b', 'ca': r'\b(we|we\'re|we\'ve|our|ours|us)\b', 'au': r'\b(we|we\'re|we\'ve|our|ours|us)\b',
    'it': r'\b(noi|nostr[oaie])\b', 'de': r'\b(wir|unser\w*)\b', 'es': r'\b(nosotros|nuestr[oa]s?)\b', 'fr': r'\b(nous|notre|nos)\b',
    'pl': r'\b(my|nasz\w*|nam|nas)\b', 'nl': r'\b(wij|we|ons|onze)\b', 'in': r'(हम |हमारा|हमारी|हमारे|हमने)'}
CTA_MARKERS = re.compile(r'<!--(CTA|CTA2|CTA3|FIG:(gameplay|mascot|sequel))-->')


def words(text):
    return [w for w in re.split(r'\s+', text) if re.search(r'\w', w)]


class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.errors, self.ids, self.anchors, self.links = [], [], [], [], []
        self.total, self.listw, self.h1 = 0, 0, 0
        self.h2_in_section = 0
        self.faq, self.in_summary = 0, False
        self.ext_links = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag not in ALLOWED_TAGS:
            self.errors.append(f'disallowed tag <{tag}>')
        for k in a:
            if k == 'style' or k.startswith('on'):
                self.errors.append(f'inline {k}= attribute on <{tag}>')
        if tag == 'a' and '#' in (a.get('href') or ''):
            # Owner rule: no '#' in any URL. Link the page, not a fragment of it.
            self.errors.append(f'link to a fragment (owner rule: no # in any URL): {a.get("href")}')
        if tag == 'div' and a.get('class') not in DIV_CLASSES:
            self.errors.append(f'div with bad class {a.get("class")!r}')
        if tag == 'ol' and a.get('class') not in (None, 'steps'):
            self.errors.append(f'ol bad class {a.get("class")!r}')
        if tag == 'section':
            sid = a.get('id', '')
            if not re.fullmatch(r'[a-z0-9-]+', sid):
                self.errors.append(f'section id not ascii slug: {sid!r}')
            self.ids.append(sid)
        if tag == 'a':
            href = a.get('href', '')
            if href.startswith('#'):
                self.anchors.append(href[1:])
            elif href.startswith('{{BASE}}'):
                self.links.append(href[len('{{BASE}}'):])
            elif href.startswith('mailto:'):
                pass
            elif href.startswith('https://') or href.startswith('tel:'):
                self.ext_links.append(href)
                if href.startswith('https://') and (a.get('rel') != 'noopener' or a.get('target') != '_blank'):
                    self.errors.append(f'external link missing rel="noopener" target="_blank": {href}')
            else:
                self.errors.append(f'bad href {href!r}')
        if tag in ('h1',):
            self.h1 += 1
        if tag == 'details':
            self.faq += 1
        if tag in ('br',):
            return
        self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag == 'br':
            return
        if tag in self.stack:
            while self.stack and self.stack.pop() != tag:
                pass

    def handle_data(self, data):
        w = len(words(data))
        self.total += w
        if any(t in ('li', 'td', 'th') for t in self.stack):
            self.listw += w


def parse_page(path):
    raw = open(path, encoding='utf-8').read()
    m = re.match(r'---\n(.*?)\n---\n(.*)', raw, re.S)
    if not m:
        return None, None, raw
    meta = {}
    for line in m.group(1).split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            meta[k.strip()] = v.strip()
    return meta, m.group(2), raw


def main(ed):
    d = os.path.join(ROOT, 'content', ed)
    fails, report = [], []
    sj = os.path.join(d, 'strings.json')
    if not os.path.exists(sj):
        fails.append('strings.json missing')
    else:
        try:
            raw_sj = open(sj, encoding='utf-8').read()
            s = json.load(open(sj, encoding='utf-8'))
            for k in ['lang_name', 'edition_name', 'site_name', 'descriptor', 'logo_alt', 'skip', 'menu', 'nav_aria', 'nav', 'breadcrumb_aria',
                      'team', 'updated', 'date_human', 'method_link', 'cta', 'cta2', 'cta3', 'cta_note',
                      'fig', 'related_title', 'related_desc', 'editions_label', 'footer_about', 'footer_rg', 'footer_legal', 'footer_copy',
                      'back_home', 'notfound_title', 'notfound_text']:
                if k not in s:
                    fails.append(f'strings.json missing key {k}')
            for k in PAGES:
                if k not in s.get('nav', {}):
                    fails.append(f'strings.nav missing {k}')
            for c in ('cta', 'cta2', 'cta3'):
                for kk in ('title', 'text', 'button', 'demo'):
                    if kk not in s.get(c, {}):
                        fails.append(f'strings.{c} missing {kk}')
                if len(s.get(c, {}).get('button', '')) > 26:
                    fails.append(f'strings.{c}.button longer than 26 chars')
            blob = json.dumps(s, ensure_ascii=False)
            def _vals(o):
                if isinstance(o, dict):
                    return ' '.join(_vals(v) for v in o.values())
                if isinstance(o, list):
                    return ' '.join(_vals(v) for v in o)
                return str(o)
            vblob = _vals(s).replace(CONTACT_EMAIL, '')
            for b in BANNED_VOICE:
                if re.search(b, vblob, re.I):
                    fails.append(f'strings.json reviewer-voice wording /{b}/: ' + re.search('.{0,40}' + b + '.{0,40}', vblob, re.I).group(0))
            for k in ('descriptor', 'footer_about', 'cta', 'cta2', 'cta3', 'cta_note', 'fig', 'related_desc', 'logo_alt'):
                v = _vals(s.get(k, ''))
                if re.search(FIRST_PERSON[ed], v, re.I):
                    fails.append(f'strings.json {k}: first-person reviewer voice: ' + re.search('.{0,30}' + FIRST_PERSON[ed] + '.{0,30}', v, re.I).group(0))
            for b in BANNED_POSITIONING:
                if re.search(b, vblob, re.I):
                    fails.append(f'strings.json positioning wording /{b}/: ' + re.search('.{0,40}' + b + '.{0,40}', vblob, re.I).group(0))
            for b in BANNED_DISCLOSURE:
                if re.search(b, raw_sj, re.I):
                    fails.append(f'strings.json disclosure line /{b}/ (owner rule: no disclosure line on any page): '
                                 + re.search('.{0,40}' + b + '.{0,40}', raw_sj, re.I).group(0))
            for b in BANNED_ANY:
                if re.search(b, blob, re.I):
                    fails.append(f'strings.json banned pattern {b}')
        except Exception as e:
            fails.append(f'strings.json invalid: {e}')
    titles, descs = set(), set()
    for page, (lo, hi) in PAGES.items():
        path = os.path.join(d, page + '.html')
        if not os.path.exists(path):
            fails.append(f'{page}: file missing')
            continue
        meta, body, raw = parse_page(path)
        if meta is None:
            fails.append(f'{page}: front matter missing/invalid')
            continue
        for k in ['title', 'description', 'eyebrow', 'h1', 'lead', 'crumb']:
            if not meta.get(k):
                fails.append(f'{page}: front matter key {k} missing')
        t, ds = meta.get('title', ''), meta.get('description', '')
        if len(t) > 60:
            fails.append(f'{page}: title {len(t)} chars > 60: {t}')
        if '2026' not in t:
            fails.append(f'{page}: title lacks 2026')
        if len(ds) != 158:
            fails.append(f'{page}: description {len(ds)} chars (need exactly 158)')
        if '2026' not in ds:
            fails.append(f'{page}: description lacks 2026')
        if t in titles: fails.append(f'{page}: duplicate title')
        if ds in descs: fails.append(f'{page}: duplicate description')
        titles.add(t); descs.add(ds)
        for b in BANNED_META:
            if re.search(b, t + ' ' + ds, re.I):
                fails.append(f'{page}: banned meta word /{b}/ in title/description')
        for b in BANNED_ANY:
            mm = re.search(b, raw, re.I)
            if mm:
                ctx = raw[max(0, mm.start() - 40):mm.end() + 40].replace('\n', ' ')
                fails.append(f'{page}: banned pattern /{b}/ near: ...{ctx}...')
        for b in BANNED_POSITIONING:
            for mm in re.finditer(b, raw, re.I):
                ctx = raw[max(0, mm.start() - 50):mm.end() + 50].replace('\n', ' ')
                fails.append(f'{page}: positioning wording /{b}/ near: ...{ctx}...')
        rawv = raw.replace(CONTACT_EMAIL, '')
        for b in BANNED_VOICE:
            for mm in re.finditer(b, rawv, re.I):
                ctx = rawv[max(0, mm.start() - 50):mm.end() + 50].replace('\n', ' ')
                fails.append(f'{page}: reviewer-voice wording /{b}/ near: ...{ctx}...')
        if page in CONTENT_PAGES:
            txt = re.sub('<[^>]+>', ' ', raw)
            for mm in re.finditer(FIRST_PERSON[ed], txt, re.I):
                ctx = txt[max(0, mm.start() - 50):mm.end() + 50].replace('\n', ' ')
                fails.append(f'{page}: first-person (we/our) voice near: ...{ctx}...')
        body_nomark = CTA_MARKERS.sub('', body)
        for mk in re.findall(r'<!--(.*?)-->', body):
            if not CTA_MARKERS.fullmatch(f'<!--{mk}-->'):
                fails.append(f'{page}: unknown marker <!--{mk}-->')
        p = P()
        p.feed(html.unescape(meta.get('lead', '')) and '')
        p.feed(body_nomark)
        p.close()
        lead_w = len(words(meta.get('lead', '')))
        total = p.total + lead_w
        for e in sorted(set(p.errors)):
            fails.append(f'{page}: {e}')
        if p.h1:
            fails.append(f'{page}: <h1> in body')
        if len(set(p.ids)) != len(p.ids):
            fails.append(f'{page}: duplicate section ids')
        for a in p.anchors:
            if a not in p.ids:
                fails.append(f'{page}: anchor #{a} has no section')
        for l in p.links:
            base = l.split('#')[0]
            if base not in SLUGS:
                fails.append(f'{page}: internal link to unknown page {{BASE}}{l}')
        if not (lo <= total <= hi):
            fails.append(f'{page}: {total} words (need {lo}-{hi})')
        ratio = p.listw / max(1, total)
        if ratio > 0.30:
            fails.append(f'{page}: list/table words {ratio:.0%} > 30%')
        secs = re.findall(r'<section id="([^"]+)">\s*<h2>', body)
        if len(secs) != len(p.ids):
            fails.append(f'{page}: every <section> must start with <h2> ({len(secs)}/{len(p.ids)})')
        if page in CONTENT_PAGES:
            if 'faq' not in p.ids: fails.append(f'{page}: no section id="faq"')
            if 'sources' not in p.ids: fails.append(f'{page}: no section id="sources"')
            elif p.ids[-1] != 'sources': fails.append(f'{page}: sources must be last section')
            need = (10, 12) if page == 'home' else (6, 8)
            if not (need[0] <= p.faq <= need[1]):
                fails.append(f'{page}: FAQ items {p.faq} (need {need[0]}-{need[1]})')
            n_cta = len(re.findall(r'<!--CTA[23]?-->', body))
            if n_cta < 1: fails.append(f'{page}: no CTA marker')
        if page == 'home':
            for mk in ('<!--CTA-->', '<!--CTA2-->', '<!--CTA3-->', '<!--FIG:gameplay-->', '<!--FIG:mascot-->'):
                if mk not in body: fails.append(f'home: missing {mk}')
            for sl in ['demo/', SEQUEL_SLUG + '/', 'payments/', 'about/', 'responsible-gambling/']:
                if sl not in [x.split('#')[0] for x in p.links]:
                    fails.append(f'home: body should link to {{BASE}}{sl}')
        DESIGN = re.compile(r'class="(callout[^"]*|cards|pros-cons|highlight|steps)"')
        sec_bodies = re.findall(r'<section id="([^"]+)">(.*?)</section>', body, re.S)
        designed = [sid for sid, sb in sec_bodies if DESIGN.search(sb)]
        if page == 'home':
            if not (5 <= len(designed) <= 6):
                fails.append(f'home: {len(designed)} sections carry designed blocks (callout/cards/steps/pros-cons/highlight); need 5-6 main sections: {designed}')
            if 'responsible-gambling' not in [x for x, _ in sec_bodies]:
                fails.append('home: responsible gambling section must have id="responsible-gambling"')
        for sid in designed:
            if 'respons' in sid or 'conclu' in sid:
                fails.append(f'{page}: section #{sid} must not carry designed blocks (responsible gambling / conclusion stay plain)')
        if page == 'responsible-gambling' and designed:
            fails.append(f'responsible-gambling: page must stay plain, designed blocks in {designed}')
        for q, a in re.findall(r'<summary>(.*?)</summary>\s*<p>(.*?)</p>', body, re.S):
            n = len(words(re.sub('<[^>]+>', ' ', a)))
            if not (30 <= n <= 70):
                fails.append(f'{page}: FAQ answer {n} words (need 30-70): {q[:60]}')
        # internal linking (contextual, in-body)
        links = re.findall(r'<a href="\{\{BASE\}\}([^"#]*)(?:#[^"]*)?"[^>]*>(.*?)</a>', body, re.S)
        cnt = collections.Counter(SLUG2PAGE.get(l, '?') for l, _ in links)
        for tgt, need in LINK_REQ[page].items():
            if cnt[tgt] < need:
                fails.append(f'{page}: needs >= {need} contextual link(s) to {tgt} (has {cnt[tgt]})')
        for tgt, n in cnt.items():
            if n > 4 and tgt != page:
                fails.append(f'{page}: {n} links to {tgt} (max 4)')
        if cnt.get(page, 0) and page != 'home':
            fails.append(f'{page}: links to itself')
        seen = collections.Counter()
        for l, txt in links:
            t = re.sub('<[^>]+>', '', txt).strip()
            if BAD_ANCHORS.match(t) or len(words(t)) < 2 and not re.search(r'[\u0900-\u097F]', t):
                fails.append(f'{page}: weak anchor text {t!r} -> {l}')
            seen[(l, t.lower())] += 1
        for (l, t), n in seen.items():
            if n > 1:
                fails.append(f'{page}: same anchor {t!r} used {n}x for {l} (vary it)')
        if re.search(r'<h[23][^>]*>[^<]*<a ', body):
            fails.append(f'{page}: link inside a heading')
        if page == 'demo' and '<!--FIG:gameplay-->' not in body: fails.append('demo: missing <!--FIG:gameplay-->')
        if page == SEQUEL_SLUG and '<!--FIG:sequel-->' not in body: fails.append(f'{SEQUEL_SLUG}: missing <!--FIG:sequel-->')
        if page == 'about':
            for i in ('method', 'sources-we-use'):
                if i not in p.ids: fails.append(f'about: needs section id="{i}"')
        if page == 'contact' and CONTACT_EMAIL not in body:
            fails.append('contact: email missing')
        report.append(f'{page:22s} words={total:5d} list%={ratio:4.0%} faq={p.faq:2d} sections={len(p.ids):2d} title={len(t)} desc={len(ds)}')
    print('\n'.join(report))
    if fails:
        print('\nFAIL:')
        print('\n'.join('  - ' + f for f in fails))
        sys.exit(1)
    print('\nALL OK')


if __name__ == '__main__':
    main(sys.argv[1])
