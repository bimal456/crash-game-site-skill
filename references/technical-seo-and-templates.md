# Technical SEO and templates

`scripts/build.py` generates all of this. This file documents what it outputs, so you can check it or adapt it to another host. Placeholders: `{{DOMAIN}}` (https://example.com), `{{BASE}}` (edition prefix: `/` or `/it/`), `{{PATH}}`, `{{HL}}` (hreflang, e.g. it-IT), `{{GAME}}`, `{{PROVIDER}}`, `{{ORG}}` (site name = the domain, e.g. chickenroad.radio.am), `{{YEAR}}`.

## build.py CONFIG (set at the top before the first build)
`DOMAIN`, `DATE`, `TRACKING_URL`, `ORG_NAME`, `GAME`, `GAME_SEQUEL`, `SEQUEL_SLUG`, `PROVIDER`, `PROVIDER_URL`, `EDITIONS` (code, folder, hreflang, og locale), `PAGES`. Also set `DOMAIN`/`CONTACT_EMAIL` in `check_content.py` and `qa_site.py`.

## Head (every page)
```html
<title>{{<=60 chars, primary keyword first, year}}</title>
<meta name="description" content="{{exactly 158 chars, keyword first, year, unique wording}}">
<link rel="canonical" href="{{DOMAIN}}{{PATH}}">
<link rel="alternate" hreflang="en" href="{{DOMAIN}}/demo/">
<link rel="alternate" hreflang="it-IT" href="{{DOMAIN}}/it/demo/">
... one per edition that has the page ...
<link rel="alternate" hreflang="x-default" href="{{DOMAIN}}/demo/">
<meta property="og:locale" content="it_IT"> + og:locale:alternate for the other editions
og:type / og:title / og:description / og:url / og:image (+ width/height), twitter:card summary_large_image + twitter:image
```
Same hreflang set on every page of the cluster and repeated in `sitemap.xml` with `xhtml:link`. Self canonical always.

## Page header / opening (no author, no TOC)
```html
<p class="eyebrow">...</p><h1>...</h1><p class="lead">...</p>
<p class="byline">Updated <time datetime="{{DATE}}">29 October 2026</time> · <a href="{{BASE}}about/#method">Sources</a></p>
```
- No "By editorial team / Redazione / Redaktion", no "Independent site", no "Review" byline.
- **No disclosure line at all** (owner rule, round 4): no `<p class="disclosure">`, no `independence` string. The opening block is eyebrow, H1, lead, byline. Nothing else.
- **No table of contents.** `.layout` is one column, `max-width:900px`, centered.

## JSON-LD (never Review / AggregateRating / Rating)
One `@graph` per page:
- `Organization` `{{DOMAIN}}/#org` name `{{ORG}}`
- `WebSite` (inLanguage per edition, publisher #org)
- `WebPage` (about: `VideoGame` {{GAME}}, publisher Organization {{PROVIDER}})
- `BreadcrumbList`
- `Article` on game pages, `author: {"@id": "{{DOMAIN}}/#org"}` (organization, no invented person), `dateModified`
- `FAQPage` mirroring the visible FAQ exactly
- `AboutPage` / `ContactPage` on those pages

## Nav / footer
- Header: logo image links to the edition home; primary nav with all pages of the edition, `aria-current="page"` on the active one; mobile menu button (site.js).
- Footer: nav, cookie link, **editions switcher** (same page in every edition, `hreflang` + `lang` on each link), `footer_about` (what the site covers, plain), `footer_rg` (helpline), `footer_legal` (trademarks belong to their owners, promotional links). No "independent / not affiliated / information site" sentence.

## CTA (all editions, all buttons)
```html
<a class="button button-primary" href="{{DOMAIN}}/play" target="_blank" rel="nofollow sponsored noopener">Play {{GAME}}</a>
```
Full absolute `{{DOMAIN}}/play` on every CTA in every edition (owner rule: "domain/play"). Hover shows the domain, never the tracking link.

## _redirects (Cloudflare Pages)
```
# Affiliate cloak: /play -> tracking link (302). The tracking URL lives only in this file.
/play {{TRACKING_URL}} 302
/play/ {{TRACKING_URL}} 302
/play/* {{TRACKING_URL}} 302
/login /play 301
/login/ /play 301
/login/* /play 301
```
No HTML page is generated at /play or /login. `qa_site.py` fails if the tracking URL appears in any HTML file.

## _headers
```
/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: DENY
  Permissions-Policy: camera=(), microphone=(), geolocation=(), interest-cohort=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; font-src 'self'; connect-src 'self'; frame-ancestors 'none'; object-src 'none'; base-uri 'self'; form-action 'none'

/assets/*
  Cache-Control: public, max-age=31536000, immutable

/play
  X-Robots-Tag: noindex, nofollow, noarchive
  Referrer-Policy: no-referrer
  Cache-Control: no-store
/play/*
  (same)
```
`style-src 'self'` and `script-src 'self'`: zero inline `style=`, zero inline `<script>` code except JSON-LD, zero `on*` handlers. Assets are cached as immutable; build.py adds a content-hash query (`style.css?v=...`) so CSS/JS changes reach visitors after a redeploy.

## robots.txt
```
User-agent: *
Allow: /
Disallow: /play
Disallow: /login

Sitemap: {{DOMAIN}}/sitemap.xml
```

## sitemap.xml
Every indexable page of every edition with `lastmod` and `xhtml:link` alternates. Never /play, /login, 404.

## 404.html
Real 404 status (Cloudflare Pages serves `404.html` automatically), `noindex, follow`, same header/footer, links back to every edition home.

## Images
- Original illustrations from `scripts/make_images.py` (gameplay, mascot, sequel, og). Never provider character art, screenshots or in-game illustrations.
- **Logo is the one exception**, and only for the header/footer brand mark that identifies the game: the provider's official logo may be used if it can be sourced cleanly from their own page or press kit, unaltered, with the trademark notice in the footer. If it cannot, render an original text wordmark in the researched brand colors instead. Never redraw or imitate the real mark. See `references/brand-design-research.md`. The placeholder `logo.webp` that `make_images.py` draws is a stand-in until one of those two is in place.
- Gameplay figure links to demo, mascot to the sequel page (`FIG_TARGET`). Alt text descriptive and in the edition language; captions say "Illustration".
- `width`/`height` on every `<img>`, `loading="lazy"` below the fold.

## Canonical form
https only (zone "Always Use HTTPS"), trailing slash on every internal link (`{{BASE}}demo/`), apex domain only.
