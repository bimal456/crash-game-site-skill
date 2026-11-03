# Research and keyword mapping

Research first, build second. For multi-geo sites, do every step per edition.

## Step 1 - Ahrefs (per country)
- `keywords-explorer-matching-terms` for the game name (and local nicknames / native script, e.g. "चिकन रोड गेम", "murgi game") in the country. Sort by volume.
- `keywords-explorer-overview` for the primary and the strongest secondaries (volume, KD, traffic potential, parent topic).
- `serp-overview` for the primary keyword (who ranks, traffic).
- Drop off-topic noise (e.g. "why did the chicken cross the road", restaurant names, spam keywords with emoji domains).
- Monetary values from Ahrefs are USD cents.

## Step 2 - Clean the list
One intent = one keyword (word-order flips and synonyms are the same keyword). One primary keyword per edition; secondaries grouped by intent directly under it.

## Step 3 - Intent clusters -> sections/pages
| Intent cluster | Lands on |
|---|---|
| what it is / how it works / rules / cash out | Home |
| spec sheet (provider, RTP, max win, modes, devices, demo) | Home table |
| does it pay / scam / legit / real or fake | Home (longest money section) |
| demo / free / no registration | Demo page + home teaser |
| RTP / volatility / max win | Home |
| legal status in the country (+ provider restrictions) | Home |
| where to play / which casino | Home + CTA |
| local operators | Home table (or licence-check table where not legal/restricted) |
| register / start | Home steps |
| bonus / code / free spins / no deposit | Home (rollover example, labelled hypothetical) |
| app / download / APK | Home (fake APK warning) |
| sequel (e.g. Chicken Road 2) | Own page + home teaser |
| payments / withdrawals / tax | Own page |
| tricks / strategy / predictor | Home (honest: none work) |
| game vs other crash games | Home comparison table |
| player opinions (avis, opinie, Erfahrungen, opiniones) | Home "pros and cons / what players say" (NO review voice) |

## Step 4 - Live SERP mining
- DataForSEO `POST /v3/serp/google/organic/live/regular` with `location_code` + `language_code` for each geo, keyword = the strongest money query (e.g. "chicken road paga davvero", "chicken road seriös", "chicken road es fiable", "chicken road avis", "chicken road opinie", "is chicken road legit"). The plain game keyword is often just app stores and social.
- Keep informational competitor URLs in `research/serp-<ed>.md`; skip app stores, YouTube, TikTok, Trustpilot clone listings.
- WebFetch 3-5 of them; record H1/H2/H3, FAQ questions, tables vs prose, word count in `research/outlines-<ed>.md`. Add the shared high-intent sections and FAQ the edition lacks. Many SERPs are parasite spam: note it and move on.
- Never import competitor errors (wrong RTP, "3 risk levels", invented tests, scores, ratings, operator rankings).

## Step 5 - Facts and restrictions
- Provider page for RTP, release, modes. Game databases (e.g. SlotCatalog) for lanes, risk per step, max win, bet range: label as third-party / operator-dependent.
- Provider restricted-countries page: record which geos are restricted and use it in the legal sections.
- Per-geo legal/tax/helpline facts verified on regulator / government / helpline sites, recorded in `research/ledger-<ed>.json`, merged into `claim-ledger.json`. Unknown stays unknown.

## Output before building
Per edition: primary keyword + mapped secondaries, Ahrefs overview numbers, live SERP list, competitor outlines, localization pack, provider restriction status. Shared: facts.md + claim ledger.

## Page inventory (decides what gets built)

While mining competitor outlines, record WHICH PAGES each ranking site has for this game, not only their headings. One row per page type, one column per competitor, plus a count.

The five trust pages (`about`, `contact`, `responsible-gambling`, `terms`, `privacy`) are built on every site regardless of what competitors do. Everything else is decided here: a page type that most ranking sites have gets built, one that none of them have does not. Different games produce different sets, so never carry a page list over from the previous build.

Hand the finished inventory to step 2, where it becomes `PAGES` in `build.py` and the matching `WORD_RANGE` / `LINK_REQ` entries in `check_content.py`.
