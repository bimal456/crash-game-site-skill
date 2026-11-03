# Changelog: chickenroad.radio.am (October-November 2026)

Every change the owner asked for while the site was built, one by one, plus the technical fixes found along the way. Each one is now a rule in this skill. Read it so the next site is right on the first try.

## Owner corrections (content, voice, design, CTA)

| # | Owner said (short) | What was wrong | Rule now | Where enforced |
|---|---|---|---|---|
| 1 | "Make sure to follow the skill" / "everything you followed exactly?" | First pass skipped SERP mining, competitor outlines, claim ledger and native QA | Research + independent reviewer per edition are mandatory, not optional | SKILL.md workflow, REVIEW_SPEC |
| 2 | "Geo-wise like domain/fr, domain/it" | Needed confirmation of the folder structure | English global at `/` (x-default), each country at `/<code>/`, same slugs | multi-geo-editions.md, build.py EDITIONS |
| 3 | "Don't send two zips, send one final with everything" | Several zips were sent | ONE `<site>-FINAL.zip` for the owner; the SITE zip is only for deploying | quality-and-release.md |
| 4 | "Internal linking not done properly" | 0-5 in-text links per page; payments and RG had none | `LINK_REQ` minimums per page, descriptive varied anchors, spread through the text | internal-linking.md, check_content.py |
| 5 | "How dare you use the word information" (footer) | Footer and about said "independent information site", "not affiliated with InOut Games or any casino", "we are not a casino" | No information/info/independent/unofficial/not-affiliated positioning in any language. Only disclosure: "Contains promotional links." | voice-and-positioning.md, BANNED_POSITIONING |
| 6 | "Why is review mentioned? ... you can't use review, independent ... no 3rd party and 2nd party voices" | "Review" in titles/headings/schema-like wording, "our verdict", "editorial team" byline, "we tested", we/our narration on game pages | No review/verdict/editorial voice; game pages talk directly about the game and to "you"; byline is "Updated <date> · Sources"; Article author is the Organization; home section renamed "pros and cons" | VOICE_SPEC, BANNED_VOICE, FIRST_PERSON, build.py byline |
| 7 | "Remove it" (screenshot of "On this page") | Sticky table of contents in a side column | No TOC; content one column, centered, max ~900px | build.py (`toc = []`), style.css `.layout` |
| 8 | "Play and all other CTAs to domain/play" | CTAs went to `/login` HTML redirect page | Every CTA `href="https://<domain>/play"`; `/play` 302 in `_redirects`; `/login` 301 to `/play`; no login page generated | build.py REDIRECTS/HEADERS, qa_site.py |
| 9 | "I don't want to create a mail, leave the console work" | Was pushing for mailbox setup and Search Console | Do not push mailbox / Search Console / analytics setup. Keep `contact@<domain>` on the contact page as given; only make sure the site shows on the URL | SKILL.md final report |
| 10 | "Just make sure the site shows on the URL" | Focus | Live readback on the exact domain is the finish line | deploy-cloudflare-pages.md |

## Replacements made sitewide (all 11 editions)
- footer_about "Independent information site about Chicken Road" -> what the site covers, plainly ("How the Chicken Road crash game by InOut Games works, the free demo, Chicken Road 2, payments and where it is legal to play, with scam warnings and safe-play tips.").
- "Not affiliated with InOut Games or any casino" -> removed. footer_legal now: "Chicken Road is a trademark of InOut Games. Trademarks belong to their owners. Contains promotional links for adults."
- "Independence: no casino pays for editorial content" -> "Contains promotional links."
- "Editorial team / Redazione / Redaktion" byline -> "Updated <date> · Sources".
- "Chicken Road review / our verdict" section -> "Chicken Road pros and cons" (and local: pro e contro, Vor- und Nachteile, ventajas y desventajas, avantages et inconvénients, zalety i wady, voor- en nadelen, फायदे और नुकसान).
- "We checked / we tested / in our opinion" on game pages -> facts stated directly ("The in-game info panel shows RTP 98%.") and advice to the player ("Check the provider name in the info panel.").
- About page: "About our team / independence" -> "About <domain>", "#method: How the pages are kept up to date", "How the site makes money".

## Technical fixes found during the build
- Python lists with stray trailing commas became tuples and broke JSON output: unwrap before `json.dump`.
- `pkill -f` killed the agent's own shell (exit 144): start the preview server with nohup from a script file, stop it by PID.
- Injected `<style>` for the 200% text test is blocked by CSP: use `style.setProperty` from JS.
- 200% reflow overflow: footer grids `minmax(0,1fr)`, long headings `overflow-wrap:anywhere; hyphens:auto`.
- `preview` matched the banned word "review": use `\b` word boundaries.
- Checker flagged the strings.json key name `independence`: the checker now scans values only (the key stays, its value is "Contains promotional links."); the CSS class became `disclosure`.
- Cloudflare dashboard upload blocked by Cloudflare's own WAF on the owner's network (403 on `pages/assets/check-missing`, 401 on the Workers flow). Fix was retrying the legacy Pages flow via the browser file input; never extract API tokens from the dashboard.
- Owner uploaded the whole FINAL package: site appeared under `/chickenroad-radio-am/site/` and `source/` was public. Fixed by deploying the SITE zip (index.html at the root); old paths verified 404.
- Cloudflare Email Address Obfuscation rewrites pages that contain an email, and Cloudflare injects a script tag: expected byte differences in the live readback.

## Facts confirmed during the build (re-verify on the next site)
- InOut Games restricted countries page lists UK, France, Australia, Netherlands, Spain, Italy, Germany, Poland, USA (and others). Legal sections in those editions say so plainly; operator tables became licence-check tables.
- India: Promotion and Regulation of Online Gaming Act 2025. Owner decision still open on whether /in/ keeps CTAs.

## Round 2 (November 2026): disguised "independent/review site" voice

The literal banned-word checker passed, but the About and Contact pages had
drifted back into review-site/information-site *spirit* using wording that
evades the literal word list. The owner's instruction: scan the whole live
site, not a list of flagged lines, and fix the spirit of it everywhere,
using judgement per line on whether to reword or delete.

| # | What was found | Rule now |
|---|---|---|
| 11 | About pages had a "why this site exists" origin story ("a small group of writers...", "crowded with clone apps") | No origin-story/justification section. State what the site covers, nothing about why it was started. |
| 12 | "No payment could change what we publish" / "we do not sell advertising space, sponsored articles or paid placements" / "running a multi-language site costs money, and we prefer to be upfront" in the funding section | Cut the performed-integrity lines and the list of what the site refuses to sell. One flat factual sentence is allowed and was kept live: "Commissions never change the facts published: the RTP, the risks, the scam warnings and the legal notes stay the same." |
| 13 | "We make mistakes like anyone else" self-deprecating tone in the corrections section | State the corrections mechanism plainly (how to report, what gets fixed). No self-deprecating "we're human too" framing. |
| 14 | "We are a small team, so busy periods can take longer" (About and Contact) | No "small team" framing anywhere. State response-time facts without describing the team's size. |
| 15 | "We rank our sources by how neutral they are" meta-commentary about the site's own sourcing method | List the sources/method as facts (what is checked against what). Never add meta-commentary that frames the site as judging or ranking its own neutrality — that is reviewer/editorial voice. |
| 16 | Terms pages ("Information only, not advice" heading + "we publish information, not advice" lead), across EN/AU/DE/FR/UK and translated equivalents in ES/IN/IT/NL/PL, describe the site's own output as "information" | Add "information" (self-describing what the site publishes) to the banned-positioning list even outside the literal phrase "information site" — e.g. "general information about...", "Information only, not advice" as a heading. Reword to state the legal disclaimer (not advice, consult a professional, figures can depend on the operator) without using "information" to describe the site itself. This was found but **not yet fixed on the live site** as of this changelog entry — re-check and fix on the next pass if not already done. |

General pattern for future sites: run a full read of every About/Contact
(and Terms, which shares the same "informational" framing risk) page, not
just a checker pass, looking for: origin-story justification, editorial-
independence boasts, self-deprecating editorial tone, "small team" framing,
and "we rank/judge our own sources" meta-commentary. These five categories
are the ones that reliably evade a literal word-list checker while keeping
the review-site spirit the owner rejects.

## Round 4 (November 2026): no promotional-disclosure line, at any cost

The owner asked whether "Contains promotional links." was on the site. It
was: on all 110 pages, as `<p class="disclosure">` in the opening block AND
again inside every page's `footer_legal` ("Contains promotional links for
adults."), localized per edition. His instruction: "ye nahi honi chahiye
kisi bhi keemat pe kisi bhi page pe."

| # | What was found | Rule now |
|---|---|---|
| 17 | `<p class="disclosure">{independence}</p>` in the opening block of every page | Removed from `build.py`. The opening block is eyebrow, H1, lead, byline. |
| 18 | The same phrase a second time in the footer of every page, via `footer_legal` and a second `{independence}` print in the footer brand column | Both removed. `footer_legal` keeps the trademark sentence plus any country legal note (France's "jeux de casino en ligne interdits en France", India's 2025 Act note stay). |
| 19 | The `independence` key itself in all 11 `strings.json` files, required by `check_content.py` | Key deleted everywhere; the checker no longer requires or scans it, and now FAILS on the phrase family in nine languages. |

Kept deliberately, because they are not the banner line: `rel="nofollow
sponsored noopener"` on all 77 CTAs, the affiliate-disclosure section in the
about/terms body copy, and `cta_note` ("Promotional link. Opens the operator
in a new tab."). Flagged to the owner rather than removed on my own.

## Round 6 (November 2026): the page set is researched, not fixed

Owner: the five mandatory pages are about us, contact us, responsible gambling, T&C and privacy policy; after that, build the pages the sites ranking in the SERP for that game actually have.

Before this round the skill shipped ONE hardcoded page list (home, demo, sequel, payments, about, contact, responsible-gambling, privacy, cookie-policy, terms) and nothing anywhere tied the page set to research. Every game got Chicken Road's pages.

| # | Rule now | Where enforced |
|---|---|---|
| 23 | Five trust pages in every edition, always: `about`, `contact`, `responsible-gambling`, `terms`, `privacy`. Plus `home` and the 404. | SKILL.md step 2, multi-geo-editions.md, acceptance checklist |
| 24 | Content pages come from the SERP page inventory for THAT game, recorded during step 1 alongside the competitor outlines. A page type most ranking sites have gets built; one none of them have does not. Never carry a page list from the previous build. | SKILL.md steps 1 and 2, research-and-keywords.md, project.json |
| 25 | `cookie-policy` is not one of the five: add it only when something actually sets a cookie or an EU edition's privacy page links one. | SKILL.md step 2, multi-geo-editions.md |
| 26 | The researched list goes into `PAGES` (build.py) and needs a `WORD_RANGE` and `LINK_REQ` entry per page (check_content.py), or the checker does not know the page exists. | SKILL.md step 2, acceptance checklist |

## Round 5 (November 2026): CTA hover target, no "#" in URLs, no pop-ups

Owner: "jab CTA pe lgao toh front pe hover krne pe har CTA pe aana chaiye -
domain/play & kisi bhi URL pe # nhi hona chaiye koi 18+ ka pop up bhi nhi
chahiye mereko."

| # | Rule now | Where enforced |
|---|---|---|
| 20 | Hovering ANY CTA must show `<domain>/play` in the status bar. Not `/play`, not a relative path, never the tracking link. Hover-check a CTA on the home page, a game page and the footer before calling a build done. | SKILL.md CTA rules, build.py (absolute `{DOMAIN}/play`), qa_site.py (tracking URL must not appear in HTML) |
| 21 | **No `#` in any URL.** No `href` points at a fragment: the byline links to `about/`, not `about/#method`; no in-page jump links; no `{{BASE}}#legal-status`. Link the page and let the sentence say what is there. Section `id` attributes stay on sections; nothing links to them. | build.py byline, check_content.py (per-link failure), qa_site.py (fails the build) |
| 22 | **No pop-up, modal, overlay, interstitial or age gate**, and no "18+" anywhere. Nothing is ever layered over the page. | SKILL.md hard rules, qa_site.py (matches `modal`/`overlay`/`popup`/`interstitial`/`age-gate` classes, `<dialog>`, `showModal(`) |

Two deliberate exceptions to rule 21, both invisible to the reader and
neither a navigable URL: the keyboard skip link (`href="#main"`, required
for accessibility, and the skill's own QA tests it) and the JSON-LD `@id`
node identifiers (`/#org`, `#faq`), which are schema.org plumbing. Both are
whitelisted in `qa_site.py`; everything else fails the build.

NOTE: chickenroad.radio.am's own content files still carry ~65 fragment
links (`about/#method`, `about/#corrections`, `#legal-espana`,
`#bharat-mein-kanoon` and similar) plus the byline fix that build.py now
applies automatically. Those content links were NOT rewritten in this round
and the checker will fail on them until they are.

## Round 3 (November 2026): design was never researched per brand

The owner's correction: every site built from this skill shipped with the
same chicken-yolk-yellow/navy palette regardless of what game/brand it
covered, and the overall feel read as an article/blog rather than a game
site. Rule now: research the real game/provider's official colors and
visual mood before any CSS or illustration work — see
`references/brand-design-research.md`, wired into SKILL.md as step 1b.
`assets/style.css` and `scripts/make_images.py` variable names were
genericized (`--navy`→`--primary`, `--yolk`→`--accent`, etc.) so a new
brand's real colors drop in cleanly instead of reusing chicken-theme names.
