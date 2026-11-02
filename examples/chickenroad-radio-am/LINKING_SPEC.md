# Internal linking pass (contextual links inside the body copy)

Goal: every page of the edition links naturally, inside its prose, to the other pages of the SAME edition, so link equity and topical relevance flow through the site (the header nav, footer and "related pages" block already exist; this pass is about in-text links).

Edit only `content/<ed>/*.html` (not strings.json). Links use `<a href="{{BASE}}slug/">anchor</a>` (home = `{{BASE}}`), trailing slash, about method = `{{BASE}}about/#method`.

Minimum contextual links per page (checker enforces):
- home -> demo 2, chicken-road-2 2, payments 2, about 1 (prefer about/#method), responsible-gambling 1, contact 1
- demo -> home 2, chicken-road-2 1, payments 1, responsible-gambling 1, about 1
- chicken-road-2 -> home 2, demo 2, payments 1, responsible-gambling 1, about 1
- payments -> home 1, demo 1, chicken-road-2 1, responsible-gambling 1, about 1, terms 1
- about -> home, demo, chicken-road-2, payments, contact, responsible-gambling, privacy (1 each)
- contact -> home, about, responsible-gambling, privacy
- responsible-gambling -> home, demo, payments, contact
- privacy -> cookie-policy, terms, contact, about
- cookie-policy -> privacy, terms, contact
- terms -> privacy, cookie-policy, responsible-gambling, contact, about

Rules:
- Put links in paragraphs, list items or FAQ answers where the topic is actually discussed (e.g. "free demo" sentence -> demo page; tax/withdrawal sentence -> payments; Chicken Road 2 mention -> chicken-road-2; "how we check facts" -> about/#method; limits/helpline -> responsible-gambling). Never inside headings, never in the CTA markers, never a link to the page itself.
- Prefer wrapping an EXISTING phrase in a link (adds zero words). Only add a short clause where no suitable phrase exists. Word ranges must still pass (home max 3000).
- Anchor text: 2-6 descriptive words in the edition's language that tell what the target is, keyword-aware but varied (mix exact, partial and natural phrasing, e.g. "Chicken Road demo", "play the demo free first", "our free demo page"). Never "click here/here/read more" or local equivalents. Do not reuse the identical anchor text for the same target on one page. Max 4 links to one target per page.
- Spread links through the page (not all in one paragraph); about one in-text link per 100-150 words on content pages is plenty.
- Keep all other rules of CONTENT_SPEC.md and REVIEW_SPEC.md (meta 158 chars, 5-6 designed sections on home, RG plain, no em dashes, nothing with "guid", etc.).

Finish when `python3 /home/claude/chickenroad/tools/check_content.py <ed>` prints ALL OK. Reply with one line per page: number of in-text internal links and targets.
