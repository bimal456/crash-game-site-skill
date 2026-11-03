> **Updated after owner corrections.** This spec was the writer contract on chickenroad.radio.am. POSITIONING_SPEC.md and VOICE_SPEC.md (and `references/voice-and-positioning.md`) override anything here: no guide/information/review/independent/not-affiliated wording, no we/our on game pages, no TOC, CTAs to https://<domain>/play.

# Content spec for chickenroad.radio.am (one edition = one locale folder)

You write ALL public text for ONE edition, in that edition's native language, as plain files. A Python generator (not you) wraps your files in the header, nav, breadcrumbs, byline, related-pages block, footer, schema, hreflang and meta tags. Read this whole spec, then `research/facts.md` (shared game facts) and `research/<edition>.md` (keywords, SERP, localization pack).

Site: https://chickenroad.radio.am  - a money-forward but cautious site about the crash game **Chicken Road** by InOut Games, with 11 editions:
`en` (/ global English, x-default), `in` (/in/ Hindi), `it` (/it/), `de` (/de/), `es` (/es/), `fr` (/fr/), `uk` (/uk/ British English), `pl` (/pl/), `nl` (/nl/), `ca` (/ca/ Canadian English), `au` (/au/ Australian English).
Today is 29 October 2026. Year to use: 2026.

## Files you must create in `content/<edition>/`

| File | Page URL | Body word target |
|---|---|---|
| `home.html` | `<base>` | **2700-3000 words (never over 3000)** |
| `demo.html` | `<base>demo/` | 1500-1800 |
| `chicken-road-2.html` | `<base>chicken-road-2/` | 1500-1800 |
| `payments.html` | `<base>payments/` | 1500-1800 |
| `about.html` | `<base>about/` | 900-1300 |
| `contact.html` | `<base>contact/` | 400-700 |
| `responsible-gambling.html` | `<base>responsible-gambling/` | 800-1200 |
| `privacy.html` | `<base>privacy/` | 700-1100 |
| `cookie-policy.html` | `<base>cookie-policy/` | 400-700 |
| `terms.html` | `<base>terms/` | 700-1100 |
| `strings.json` | UI strings (schema below) | - |

Word count = words of `lead` + body (tags stripped). Run the checker (below) and fix until it passes.

## Page file format

```
---
title: <title tag, primary keyword FIRST, includes 2026, MAX 60 characters>
description: <meta description, primary/focus keyword at the START, includes 2026, 150-160 characters, unique wording per page>
eyebrow: <short kicker above the H1, 2-5 words>
h1: <the single H1 of the page>
lead: <opening paragraph, plain-spoken, casual-ish tone (about 8% of the page), answers the main question directly>
crumb: <short breadcrumb label for this page>
---
<section id="some-id">
<h2>...</h2>
<p>...</p>
...
</section>
<!--CTA-->
<section id="another-id">
...
</section>
```

Rules for the body:
- Body = a sequence of `<section id="ascii-slug">` blocks. Each section starts with ONE `<h2>`. Use `<h3>` inside sections where useful. NEVER write `<h1>` in the body. Section ids: lowercase ASCII letters, digits and hyphens, unique on the page (Hindi edition too: use English/transliterated ASCII ids).
- Allowed tags: section, h2, h3, p, a, strong, em, ul, ol, li, table, thead, tbody, tr, th, td, details, summary, div (only with the classes listed below), br, abbr. Nothing else. NO `style="..."` attributes, NO `on...=` handlers, NO script, NO images (images come from markers).
- Internal links: `<a href="{{BASE}}demo/">`, `{{BASE}}chicken-road-2/`, `{{BASE}}payments/`, `{{BASE}}about/`, `{{BASE}}contact/`, `{{BASE}}responsible-gambling/`, `{{BASE}}privacy/`, `{{BASE}}cookie-policy/`, `{{BASE}}terms/`, home = `{{BASE}}`. NEVER link to a fragment: no `#section-id`, no `about/#method`. Always a plain page URL with a trailing slash.
- External links: ONLY to sources (InOut official page, regulator, helpline organisation, tax authority, government). Write them as `<a href="https://..." rel="noopener" target="_blank">`. NEVER link to any casino, operator or tracking URL. NEVER write a casino URL as text.
- Markers (each on its own line, between sections, not inside a section):
  - `<!--CTA-->`, `<!--CTA2-->`, `<!--CTA3-->` insert a styled play box (texts come from strings.json `cta`, `cta2`, `cta3`). Use: home 3 boxes (after the demo teaser, in/after "where to play", after bonus), demo 1-2, chicken-road-2 2, payments 1-2. Never on legal pages except none.
  - `<!--FIG:gameplay-->` (illustration linking to the demo page) and `<!--FIG:mascot-->` (illustration linking to the Chicken Road 2 page): put both on home (gameplay near "how it works", mascot near the sequel teaser). `<!--FIG:gameplay-->` once on demo. `<!--FIG:sequel-->` once on chicken-road-2.
- Design classes you may use on `div` (vary them across the page, do not repeat the same box everywhere, but keep them spread across the page: home 6-9 designed blocks, other content pages 3-5):
  - `<div class="table-wrap"><table>...</table></div>` every table MUST be wrapped like this. Use `<thead>` with `<th>`.
  - `<div class="callout">` neutral highlight (an `<h3>` or `<p><strong>` first, then text)
  - `<div class="callout callout-warn">` warning (scams, fake apps, legal)
  - `<div class="callout callout-tip">` practical tip
  - `<ol class="steps">` numbered step boxes (register, deposit, how to play)
  - `<div class="cards"><div class="card"><h3>..</h3><p>..</p></div> ... </div>` 2-4 cards grid
  - `<div class="pros-cons"><div class="pros"><h3>..</h3><ul>..</ul></div><div class="cons"><h3>..</h3><ul>..</ul></div></div>`
  - `<div class="verdict">` short summary box (CSS class name only; never the word "verdict" in visible text)
- FAQ: one `<section id="faq">` near the end with `<h2>` then items `<details><summary>Question?</summary><p>Answer.</p></details>`. Home 10-12 items, demo/chicken-road-2/payments 6-8 items. Each answer 30-70 words, factual. Legal pages: no FAQ needed (responsible-gambling may have 4-6).
- Sources: the LAST section of every content page (home, demo, chicken-road-2, payments) is `<section id="sources">` with `<h2>` and a `<ul>` of source links (official InOut page labelled as the provider's commercial page, regulator, helpline organisation, tax authority if used). About page also has its sources list.

## Content style (hard requirements)
- Native, idiomatic language of the edition, phrased the way locals search (use the keyword map phrasing in H2/H3). Not a translation calque. Indian edition: Hindi in Devanagari, keep "Chicken Road" in Latin script where natural and use the local nicknames (मुर्गी वाला गेम / murgi game) naturally.
- Prose 70%+ of words. Words inside `<li>`, `<td>`, `<th>` must be at most 30% of the page's words (checker enforces).
- Voice: money-forward but cautious and trustworthy. Answer the money question first and plainly (it can pay real winnings, only with real money at a serious licensed operator, no round is guaranteed). Separate the game (real software by InOut Games) from the risk (clone apps, fake sites, fake predictors, inflated videos, unlicensed operators): "the risk is where you play, not what you play". Outcomes are random. Never promise wins, never describe a working trick or system. When a number depends on the operator (RTP build, bet limits, max win), say so and tell the reader to check the game's info panel.
- Legal status must be TRUE for the edition (see the localization pack). Where online casino play is not legal locally (India, France, Poland outside Total Casino, Australia, Germany outside the GGL whitelist), say so plainly and calmly; never claim legality; still explain the free demo and how to verify a licence.
- Only use numbers from `research/facts.md` and your localization pack. Unknown stays unknown. No invented statistics, no fake player reviews or testimonials, no star ratings, no "live results", no fake win data, no claimed tests you did not do (you may describe the editorial method in general terms: "we play the demo, read the info panel, compare declared specs").
- The home "pros and cons" section states strengths and weaknesses directly (no review, verdict or editorial wording).
- Open each main page with a short plain-tone lead, then professional tone.

## Banned (checker enforces; zero tolerance)
- The em dash character and the en dash used as a dash. Use commas, colons, brackets or a plain hyphen.
- The word "guide" in any form or language: guide, guides, guidance, guida, guía, guia, gids, Leitfaden, Ratgeber, przewodnik, poradnik, गाइड, मार्गदर्शिका. (Anything containing "guid" fails.)
- "18+" anywhere, any age-gate wording like "only 18+". (You may say "for adults" / "adult players" in general text.)
- Any agency/company name of the site owner (e.g. "KAP"). Do not mention who owns the site; the site name is simply "chickenroad.radio.am".
- In title and description: no listicle words (top, best 10, list), and not "learn", "discover", "explained" or local equivalents (scopri, impara, spiegato, entdecken, lernen, erklärt, descubre, aprende, explicado, découvrez, apprenez, expliqué, ontdek, leer, uitgelegd, odkryj, dowiedz, wyjaśnion, जानें, सीखें, समझाया).
- Review / rating language that implies star scores ("5/5", "9.2/10", "stars").

## Required section outlines (translate/localize headings; add H3s; keep this order)

### home.html (2700-3000 words) primary keyword page: "<Chicken Road>: how it works, if it really pays, where to play"
1. what is Chicken Road (the cash-out mechanic, crash/instant game family, InOut Games)
2. name clash / originals vs clones (Crossy Road, Chicken Cross apps, Mission Uncrossable, Chicken Route; verify "InOut Games" in the info panel)
3. how Chicken Road works (steps) + difficulty table (mode | lanes | risk per step | profile)  + `<!--FIG:gameplay-->`
4. spec sheet table (provider, type, release, declared RTP, max win per round, bet range, modes, devices, demo)
5. demo teaser (1 paragraph, link to demo page) then `<!--CTA-->`
6. does Chicken Road really pay / is it a scam / is it legit (the top money section, longest one)
7. legal status in <country> (regulator, licensed vs international, what it means)
8. RTP, volatility and payouts (RTP = long-run average; difficulty changes volatility; max-win cap)
9. where to play in <country> (how to pick a trustworthy operator, licence check) then `<!--CTA2-->`
10. Chicken Road on <local operators> availability table (operator | licence | Chicken Road in lobby? -> write "check the lobby" style values, never claim certainty you do not have). Editions where no legal local operator exists: replace with a table of "licence checks" (what to check | where | why).
11. how to register and start (`<ol class="steps">`, 5 steps: pick operator, create account, verify KYC, set limits + deposit, open the game and start on demo/low stake)
12. bonus / bonus code / free spins / no deposit (a bonus is not free money; rollover with a worked numeric example; bonus does not change RTP; many crash games contribute differently to wagering) then `<!--CTA3-->`
13. app / download / APK (no official standalone real-money app from InOut; HTML5 in browser; use only the operator's official app; warning against third-party APKs and Play Store clones)
14. Chicken Road 2 teaser (1 paragraph, link to the chicken-road-2 page) + `<!--FIG:mascot-->`
15. Chicken Road vs other crash games (comparison table from facts.md + short text: all luck-based)
16. tricks and strategy (honest: no tricks win; habits that manage risk)
17. pros and cons (`pros-cons` box, "what players say" allowed; weaknesses are the ecosystem, not the software)
18. responsible gambling (short, helpline, link to the RG page)
19. FAQ (10-12)
20. sources

### demo.html (1500-1800)
what the demo is -> how to play free (no registration, no deposit) -> what you can test (+ difficulty table) -> demo on mobile -> what to test before betting real money -> demo vs real money (table) -> Chicken Road 2 demo (link to chicken-road-2 page) -> fake "demo" sites and apps warning -> moving to real money (`<!--CTA-->`) -> FAQ (6-8) -> sources. Put `<!--FIG:gameplay-->` near the top.

### chicken-road-2.html (1500-1800)
what Chicken Road 2 / 2.0 is -> differences from the original (comparison table: RTP, lanes per mode, max win, release) -> how it works -> spec table -> does it pay / is it legit -> demo -> app / which to download -> where to play (`<!--CTA-->`) -> bonus and registration -> tricks/strategy (honest) -> FAQ (6-8) -> sources. `<!--FIG:sequel-->` near the top. Second `<!--CTA2-->` after the demo section.

### payments.html (1500-1800)  "payments, withdrawals and tax"
payment methods overview + methods table (method | type | deposit time | withdrawal time) -> how to deposit -> withdrawals and timing -> account verification (KYC) -> recognising safe payments (red flags: "pay a fee to unlock your withdrawal", crypto-only unknown sites, Telegram agents) -> bonus and payment-linked rules (rollover) -> tax on winnings in <country> (from the pack, "we are not tax advisors, confirm with a professional") -> `<!--CTA-->` -> FAQ (6-8) -> sources.

### about.html (900-1300)
what chickenroad.radio.am covers (the 11 editions and pages) -> `<section id="method">` how the pages are kept up to date (facts from the provider page and regulators, specs checked against the in-game info panel and game databases, regulator registers, pages re-dated; no fake reviews or invented win data) -> `<section id="sources-we-use">` sources (provider page, regulator, helpline institution, tax authority, game databases as secondary) -> how the site makes money (promotional links marked nofollow sponsored; facts never change; demo first) -> corrections (write to the contact email). No team, no review, no independence wording.

### contact.html (400-700)
the email `contact@chickenroad.radio.am` (write it as a mailto link) -> what to write to us about (corrections, outdated info, partnership questions) -> what we cannot do (no account support for casinos, no payout disputes: contact the operator and the regulator; give the regulator/complaint route for the country) -> response time (we aim to reply within a few working days, no promise) -> if you need help with gambling: helpline.

### responsible-gambling.html (800-1200)
honest harm message (gambling is entertainment that costs money; crash games are fast) -> warning signs -> practical limits (budget, time, loss limit, cash-out target, no chasing losses, no borrowing) -> tools: deposit limits, time-outs, self-exclusion scheme of the country -> national helpline(s) with number and website -> help for family and friends -> minors: gambling is for adults only and how to block gambling sites on devices (do not write "18+") -> optional short FAQ.

### privacy.html (700-1100) / cookie-policy.html (400-700) / terms.html (700-1100)
Must be mutually consistent with this reality: the site is static HTML, sets NO cookies, runs NO analytics, NO tracking pixels, NO ads, NO forms (only a mailto email). The hosting/CDN provider (Cloudflare) processes technical data such as IP address in server logs for security and delivery. If a visitor emails us we keep the email only to answer. Affiliate links lead to third-party operator sites which have their own privacy and cookie policies; once you leave our site their rules apply. Because we set no cookies there is no cookie banner. Terms: not legal/financial/tax advice, no guarantee of winnings, check local law, affiliate disclosure, intellectual property (trademarks belong to their owners, Chicken Road is a trademark of InOut Games), limitation of liability, external links, changes to terms, contact. Data controller identity: "chickenroad.radio.am, contact: contact@chickenroad.radio.am". Do not invent a company name, street address or registration number.

## strings.json schema (all values in the edition's language; keep keys exactly)

```json
{
  "lang_name": "English",
  "edition_name": "Global",
  "site_name": "Chicken Road",
  "descriptor": "Real info: how it works, if it pays, where to play",
  "logo_alt": "Chicken Road info site logo, cartoon hen",
  "skip": "Skip to content",
  "menu": "Menu",
  "nav_aria": "Main menu",
  "nav": {"home": "Home", "demo": "Demo", "chicken-road-2": "Chicken Road 2", "payments": "Payments", "about": "About us", "contact": "Contact", "responsible-gambling": "Responsible gambling", "privacy": "Privacy", "cookie-policy": "Cookie policy", "terms": "Terms"},
  "breadcrumb_aria": "Breadcrumb",
  "byline_by": "By",
  "team": "chickenroad.radio.am",
  "updated": "Updated",
  "date_human": "29 October 2026",
  "method_link": "Sources",
  "cta":  {"title": "...", "text": "... (demo first, deposit only what you can afford)", "button": "Play Chicken Road", "demo": "Try the free demo first"},
  "cta2": {"title": "...", "text": "...", "button": "...", "demo": "..."},
  "cta3": {"title": "...", "text": "...", "button": "...", "demo": "..."},
  "cta_note": "Promotional link. Opens the operator in a new tab. Play responsibly.",
  "fig": {
    "gameplay_alt": "Illustration of the Chicken Road game board: hen, lanes and multipliers",
    "gameplay_caption": "Illustrative diagram, not an in-game screenshot. Tap to open the free demo page.",
    "gameplay_aria": "Open the Chicken Road demo page",
    "mascot_alt": "Cartoon hen crossing a road, artwork for Chicken Road 2",
    "mascot_caption": "Original artwork. Tap for the Chicken Road 2 page.",
    "mascot_aria": "Open the Chicken Road 2 page",
    "sequel_alt": "Illustration of Chicken Road 2 with longer lanes",
    "sequel_caption": "Illustrative artwork, not an in-game screenshot. Tap to open the demo page.",
    "sequel_aria": "Open the Chicken Road demo page"
  },
  "related_title": "Related pages",
  "related_desc": {"home": "...", "demo": "...", "chicken-road-2": "...", "payments": "...", "about": "...", "responsible-gambling": "..."},
  "editions_label": "Editions",
  "footer_about": "One or two plain sentences on what the site covers (game, demo, sequel, payments, legal status). No we/our, no review, no independent/information wording.",
  "footer_rg": "Gambling involves risk of loss. Set limits and stop if it stops being fun. Help: <helpline name> <number>.",
  "footer_legal": "Chicken Road is a trademark of InOut Games. Trademarks belong to their owners.",
  "footer_copy": "© 2026 chickenroad.radio.am",
  "back_home": "Back to home",
  "notfound_title": "Page not found",
  "notfound_text": "..."
}
```
`edition_name` is the country name in the edition's language (Global edition: "Global"). Keep `cta*.button` short (max 26 characters). For editions where real-money play is not legal locally, the CTA texts must stay honest (e.g. stress the free demo, and "only where online casino play is legal for you").

## Self-check (mandatory before you finish)
Run: `python3 /home/claude/chickenroad/tools/check_content.py <edition>` and fix every FAIL until it prints `ALL OK`. Then report back: per-page word counts and list-word %, and any facts you could not verify.
