---
name: crash-game-affiliate-site
description: Use when building, fixing or deploying a static HTML affiliate site for a crash or instant-win casino game (Chicken Road, Aviator, Ice Fishing, Tower Rush, etc.) for one country OR many country editions (domain/it/, domain/de/ ...). Ask only the game name, the geo(s) + language(s) and the affiliate URL, then follow this skill for research, multi-edition content in native languages, voice rules, internal linking, brand-researched design (real colors, not a default palette), technical SEO, /play cloak, QA and Cloudflare Pages deploy.
---

# Crash game affiliate site (single geo or multi-geo editions)

Builds a money-forward, SEO-optimized affiliate site about ONE crash game. The site talks directly about the game and to the player, answers the commercial-intent questions people type before depositing, and sends traffic to the partner operator through a cloaked `/play` link.

It is a static multi-page HTML site generated from one source (no CMS), deployable to Cloudflare Pages or any static host. It can be one country, or many country editions on one domain.

This version (v2) includes every correction the owner made on chickenroad.radio.am across three rounds — initial build, disguised review/information voice, and brand-accurate design (see `references/changelog-chickenroad-radio-am.md`). Those corrections are rules now. Read them before writing a single line.

## Ask only these, then proceed

1. **Game / brand name** (exact game, plus its sequel if one exists).
2. **Geo(s) + language(s).** One geo, or a list of editions (e.g. "English global + India Hindi + Italy + Germany + Spain + France + UK + Poland + Netherlands + Canada + Australia"). Each geo is written in its native language.
3. **Affiliate / tracking URL** (one for all editions, or one per geo). If missing, use a flagged placeholder.
4. Hosting is asked only at deploy time (Cloudflare account / project). Never guess it from another site.

Everything else (tone, structure, word counts, pages, schema, CTAs, design) is fixed below. Do not ask about it.

## Hard rules (zero tolerance, the checker enforces them)

Voice and positioning (owner rules, these override anything else in this skill):
- The site must NOT position itself as a **guide**, an **information / info / informational site**, a **review site**, **independent**, **unofficial** or **not affiliated**. No disclaimer voice like "independent site", "not affiliated with <provider> or any casino", "we are not the operator / not a casino", "no games hosted here", in ANY language.
- No **review** wording at all: review, verdict, recensione, Rezension, reseña, recenzja, recensie, समीक्षा, रिव्यू, "our verdict", "our opinion", "editorial team", "redazione/Redaktion/rédaction/redakcja/redactie/संपादकीय", "we tested". Player-intent keywords (avis, opinie, Erfahrungen, opiniones) may appear only as the player's question, never as the site's judgement.
- No third-party reviewer narration on game pages: no "we/our/us" (and local equivalents) on home, demo, sequel and payments pages. Write directly about the game ("Chicken Road is ...") and to the player ("you"). Legal pages may say "we" as the site operator.
- Never claim to be the official game site and never write as the provider or as a casino. The provider stays the game's maker in third person.
- **No visible promotional-disclosure line anywhere, at all, in any language, on any page** (owner rule, round 4). No "Contains promotional links." / "Enthält Werbelinks." / "Contiene link promozionali." / "इसमें प्रमोशनल लिंक हैं।" and no localized equivalent, not in the opening block, not in the footer, not in `strings.json`. There is no `independence` string and no `.disclosure` paragraph. The machine-readable disclosure stays: every CTA keeps `rel="nofollow sponsored noopener"`, and the affiliate-disclosure SECTION in the about/terms body copy stays (that is page content, not a site-wide banner line).
- No "guide" or local equivalents (guida, gids, guía, Leitfaden, Ratgeber, przewodnik, poradnik, गाइड): zero matches for "guid".
- No em dash or en dash. No "18+" badge, filter or age gate. No agency name (never "KAP" / "KAP Digital"). No Review / AggregateRating / Rating schema. No fake reviews, testimonials, ratings, win data, "1200 rounds tested" claims. No promised wins, no working "tricks".

Design:
- **The site must look like a game/brand site, never a blog, magazine, review or informational site.** Before any CSS or image work, research the actual game/provider's official colors and visual mood (`references/brand-design-research.md`) and build the palette from that — never ship the skill's placeholder chicken-yolk-yellow/navy colors on a new brand. If the official brand is light/pale, use light colors; match what is actually official, don't invent "bold" colors that aren't the brand's.
- **No table of contents** ("On this page" box). Content runs full width, centered (~900px).
- Designed blocks (callout, cards, steps, pros-cons) on only **5-6 main sections** of the home page, varied styles, spread out. Responsible-gambling section and page stay **plain**. Never design or add a "Conclusion" section.
- No inline `style=` and no inline `on*` handlers (CSP `style-src 'self'`). All hover effects in the stylesheet.
- Breadcrumb plain (no box), slightly indented.

CTA / affiliate:
- **Every** play CTA links to the full URL `https://<domain>/play` with `target="_blank" rel="nofollow sponsored noopener"`.
- `/play` (and `/play/`, `/play/*`) is a **302 in `_redirects`** to the tracking URL. The tracking URL lives only in `_redirects`, never in crawlable HTML. `/login` 301 to `/play` if an old cloak existed.
- `/play` is `Disallow`-ed in robots.txt, gets `X-Robots-Tag: noindex, nofollow, noarchive`, never in the sitemap.

SEO formatting:
- Title 60 characters max, primary keyword first, includes the year.
- Meta description **exactly 158 characters**, focus keyword first, includes the year, wording varied on every page (no template), no listicle words, no learn/discover/explained or local equivalents (scopri, entdecken, descubre, découvrez, ontdek, odkryj, जानें ...).
- One H1 per page. FAQ answers 30-70 words. Prose 70%+, bullets + tables 30% max.
- Every site: http to https, one trailing-slash URL form, working 404, hreflang, EEAT signals that are real (sources, update dates), never invented people.

## Workflow (follow in order)

### 1. Research first (`references/research-and-keywords.md`)
- Ahrefs per geo: `keywords-explorer-matching-terms`, `keywords-explorer-overview`, `serp-overview`. One intent = one keyword, one primary keyword per edition, secondaries mapped to sections/pages.
- Live SERP per geo: DataForSEO `/v3/serp/google/organic/live/regular` with the geo location + language for the primary money query ("<game> paga davvero", "<game> seriös", "<game> avis" ...). Save the informational competitor URLs to `research/serp-<ed>.md`.
- Mine 3-5 competitor outlines per edition (H2/H3, FAQ, tables vs prose, word count) into `research/outlines-<ed>.md`. Cover what leaders share plus the gaps. Never copy text or their false claims.
- Game facts with sources into `research/facts.md` and `claim-ledger.json`: provider page, RTP, modes, lanes, max win, release, sequel specs. Mark third-party numbers as operator-dependent.
- **Check the provider's restricted-countries page.** (InOut Games lists UK, France, Australia, Netherlands, Spain, Italy, Germany, Poland, USA ... as restricted.) Where the geo is restricted, never imply the game is available at locally licensed operators.
- Localization pack per geo (`references/multi-geo-editions.md`): regulator, legal truth, tax, helpline, self-exclusion, payment methods. Verify on official sources.

### 1b. Research the brand/design (`references/brand-design-research.md`) — mandatory, before any CSS or image work
- Find the game/provider's own official colors (their page, app listing, press/media kit, social banners) and the overall visual mood (playful, dark/intense, neon, premium...). Save to `research/brand-palette.md` with sources.
- **Copy `scripts/` and `assets/` into the project now** (step 4's first line, pulled forward) and recolor the PROJECT's copies, never the skill's own files.
- Replace the placeholder hex values in the project's `assets/style.css` — all of `:root`, including the derived `--primary-100..700`, `--accent-light`, `--accent-border`, `--primary-rgb`, `--accent-rgb`, `--link*`, `--deco` tokens, not just `--primary`/`--accent` — and the whole CONFIG block of `scripts/make_images.py` (every hex, plus `GAME_TITLE*` and `EDITION_LABEL`, which are drawn as text into the logo and og image). Then render and look at `og.webp` and `logo.webp`. No official signal found anywhere → pick your own, but it must still be bold/game-appropriate and themed to the game, never a reused generic palette.
- The result must read as a game/brand site, not a blog/article/review/informational site — hero-style opening, high-contrast CTAs, on-theme illustration (see the notice in `make_images.py` for drawing a new game's actual subject instead of the hen/egg example art).
- Logo: show the official game/provider logo in the header when it can be sourced cleanly from an official page or press kit, with the usual trademark footer notice; otherwise use an original text wordmark in the researched colors, never a redrawn imitation of the real logo.

### 2. Structure (`references/multi-geo-editions.md`)
- Single geo: pages at the root. Multi-geo: English global at `/` (x-default), each country at `/<code>/` (`/in/`, `/it/`, `/de/`, `/es/`, `/fr/`, `/uk/`, `/pl/`, `/nl/`, `/ca/`, `/au/`), same page slugs in every edition.
- Pages per edition: home, demo, `<sequel-slug>` (if a sequel exists), payments (+ tax), about, contact, responsible-gambling, privacy, cookie-policy, terms, plus the 404.
- Word targets: home 2700-3000 (never over 3000), demo/sequel/payments 1500-1800, about 900-1300, contact 400-700, RG 800-1200, privacy/terms 700-1100, cookie 400-700.

### 3. Content (`references/content-blueprint.md`, `references/voice-and-positioning.md`)
- One writer per edition in the native language (Hindi in Devanagari etc.), using `examples/chickenroad-radio-am/CONTENT_SPEC.md` as the file-format contract (front matter + `<section id>` bodies, `{{BASE}}` links, `<!--CTA-->`, `<!--FIG:...-->` markers, strings.json schema).
- Then an independent reviewer per edition (`examples/.../REVIEW_SPEC.md`): SERP mining, fact check on official sources, native QA, claim ledger.
- Then the internal-linking pass (`references/internal-linking.md`).
- Voice rules from the start (`examples/.../POSITIONING_SPEC.md` + `VOICE_SPEC.md` are the final rules; do not wait for the owner to ask).
- Run `scripts/check_content.py <ed>` until ALL OK for every edition.

### 4. Build (`references/technical-seo-and-templates.md`)
- Copy `scripts/` to the project `tools/` and `assets/` to the project `assets/`. Set the CONFIG constants at the top of `build.py`, `check_content.py`, `qa_site.py`.
- `python3 tools/build.py && python3 tools/qa_site.py` must print ALL OK.
- Byline on every page: "Updated <date> · Sources" (links to about#method). No author/editorial-team byline.
- Original illustrations only (`scripts/make_images.py`), labelled as illustrations. Never copy provider character art. Illustration subject must match the actual game (see step 1b) and use the researched brand colors, not the skill's placeholder palette.

### 5. QA (`references/quality-and-release.md`)
- Browser test every page + 404 at 360/768/1280 under the real CSP: no overflow, images decode, 0 console errors, 200% text reflow, keyboard skip link / menu / FAQ.
- Grep the build for every banned word list (guide, positioning, voice, em dash, 18+, KAP). `preview` contains "review": use word boundaries.

### 6. Package and deploy (`references/deploy-cloudflare-pages.md`)
- Two artifacts: `<site>-SITE-upload.zip` (contents of dist at the zip root, nothing else) for deploying, and ONE `<site>-FINAL.zip` (site/ + source/) for the owner. Never upload the source folder: it becomes public.
- Cloudflare Pages: project > Create deployment > upload the SITE zip > owner clicks "Save and deploy" > Custom domains > add domain > Activate domain > zone SSL/TLS > Always Use HTTPS on.
- Live readback on the exact domain: every page 200, http to https, 404, `/play` 302, banned-word scan on live HTML, byte comparison against the build (Cloudflare email obfuscation and its injected script are expected differences).

## Final report shape
What changed, what was verified (with counts), what is still open (owner decisions only). Short, no recap of every step.
