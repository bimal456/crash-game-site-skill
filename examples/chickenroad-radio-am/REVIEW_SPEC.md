# Review pass spec (skill Stage B independent review + Stage C native QA, plus SERP mining)

You are an INDEPENDENT reviewer for ONE edition of chickenroad.radio.am. Another agent wrote it; you did not. Your job is to make the edition fully follow the crash-game-site skill. Read first:
- `/home/claude/chickenroad/CONTENT_SPEC.md` (the content contract; still valid)
- `/home/claude/chickenroad/research/facts.md` (read it fully, including the "Added 2026-10-29" section at the end)
- `/home/claude/chickenroad/research/<ed>.md` (keywords, Ahrefs overview, localization pack) and `/home/claude/chickenroad/research/serp-<ed>.md` (live top-10 SERP)
- all 11 files in `/home/claude/chickenroad/content/<ed>/`

## Step 1: SERP structure mining (skill research step)
WebFetch 3 to 5 of the informational competitor pages in `research/serp-<ed>.md` (skip app stores, YouTube, TikTok, Trustpilot; if a page fails, try the next; you may WebSearch the edition's primary money query in the local language to find replacements). For each page you manage to read, record: H1, H2/H3 outline, which intent clusters it covers, tables vs prose, FAQ questions, rough word count. Save to `/home/claude/chickenroad/research/outlines-<ed>.md`. Then compare with the edition's home/demo/chicken-road-2/payments pages: any high-intent section or FAQ question that the leaders share and we lack must be added (as an H3 or FAQ item), while staying inside the word caps. Do not copy competitor text, and do not import their false claims (fake "testing 1200 rounds", star ratings, user testimonials, wrong RTPs, "3 risk levels").

## Step 2: Stage B, independent review of accuracy
Check every factual statement against facts.md and the localization pack:
- Numbers: RTP, lanes, risk per step, max win, bet range, release dates, Chicken Road 2 data, comparison table. Operator-dependent numbers must say so.
- Legal status, tax, regulator, helplines, self-exclusion schemes: verify each one for the edition's country with WebSearch/WebFetch on an OFFICIAL or authoritative source (regulator, government, helpline organisation). Fix anything wrong. If you cannot verify a detail, soften it to what you can verify or remove it. Unknown stays unknown.
- Provider restrictions (NEW, mandatory where relevant): InOut Games' restricted-countries page lists Australia, France, Germany, Italy, Netherlands, Poland, Spain, United Kingdom and USA (not India, not Canada). For an edition whose country is on that list, the legal-status section and the operator/availability section must say this plainly and calmly, and nothing on the site (title, description, headings, tables, CTA strings) may imply the game is available at locally licensed operators. Operator tables must not suggest availability; reword the availability column honestly (e.g. "not expected: provider lists <country> as restricted; check the lobby") or convert the table into a licence-check table. Never recommend VPNs. Global English edition: mention that the provider restricts several countries (e.g. UK, USA, Australia, much of the EU) and tells readers to check. India and Canada: you may state the country is not on the provider's list, but local law still applies (India: 2025 Act).
- Keep the money-forward but cautious voice: the CTA boxes stay (they are markers), the "does it pay" answer stays plain, demo first, deposit only what you can afford, only where legal for you.
- Remove unsupported claims, fabricated-sounding detail, repetition and scope drift. Invented "worked examples" are fine only if clearly labelled as hypothetical.

## Step 3: Stage C, native-language QA
Read every page as a native editor of the edition's language: grammar, idiom, natural local search phrasing, consistent register (tu/vous/du etc.), local spelling (British/Canadian/Australian English editions), terminology, translated table/FAQ labels, captions and every string in strings.json. No calques, no English left in non-English editions except names (Chicken Road, InOut Games, RTP, KYC, demo where locals use it).

## Step 4: Preference and skill rules the checker now enforces (fix until ALL OK)
- Meta `description`: EXACTLY 158 characters, focus keyword at the start, includes 2026, wording varied across the 10 pages (no shared template), no listicle words, no learn/discover/explained or local equivalents. Count with Python: `python3 -c "print(len('...'))"` or rely on the checker.
- Home page: exactly 5 or 6 sections carry designed blocks (`callout*`, `cards`, `pros-cons`, `verdict`, `ol class="steps"`); choose the 5-6 main sections and keep the designs varied (not the same box style everywhere) and spread across the page; other sections become plain prose (convert boxes to paragraphs, keep the words). Tables (`table-wrap`) do not count and stay where the outline needs them.
- Home: the responsible gambling section must have `id="responsible-gambling"` and stay plain (no designed blocks). No section may be named or designed as a "conclusion".
- The responsible-gambling page stays plain: no designed blocks at all (plain h2/h3/p/ul only).
- FAQ answers 30-70 words each.
- Everything else from CONTENT_SPEC.md (word ranges, 30% list cap, banned words, links, markers).
After any id change, fix in-page `#anchors` that point to it.

## Step 5: Claim ledger
Write `/home/claude/chickenroad/research/ledger-<ed>.json`:
`{"edition":"<ed>","claims":[{"claim":"...","value":"...","source_url":"...","source_type":"provider|regulator|government|helpline|tax-authority|game-database|trade-press","date_checked":"2026-10-29","verified_by_fetch":true|false,"limitation":"..."}],"unknowns":["..."]}` covering every number, legal/regulator statement, tax statement, helpline/self-exclusion detail and operator/availability statement used in the edition.

## Finish
Run `python3 /home/claude/chickenroad/tools/check_content.py <ed>` until it prints ALL OK. Only edit files in `content/<ed>/` and write `research/outlines-<ed>.md` and `research/ledger-<ed>.json`. Reply briefly: (1) pages mined and what you added from them, (2) factual corrections made, (3) native QA changes (summary), (4) facts you could not verify, (5) final checker table.
