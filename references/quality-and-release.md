# Quality, testing and release

## Gates (run in this order, all must print ALL OK)
1. `python3 tools/check_content.py <ed>` for every edition. It checks:
   - word ranges per page, prose ratio of at least 70%
   - banned words: "guid", em/en dash, "18+", KAP
   - `BANNED_POSITIONING` (information/info site, independent, unofficial, not affiliated, "not a casino", ... in all languages)
   - `BANNED_VOICE` (review, verdict, editorial team, redazione, Redaktion, समीक्षा, "we tested" ...) with word boundaries (`preview` must not match)
   - `FIRST_PERSON` per language on game pages and on sitewide strings (we/our/us, noi/nostro, wir/unser, nosotros, nous/notre, my/nasz, wij/onze, हम/हमारा)
   - meta description exactly 158 chars, title 60 max, one H1
   - `LINK_REQ` contextual internal links, anchor rules
   - FAQ answers 30-70 words
   - home has 5-6 designed sections, RG section/page plain, no "Conclusion"
   - contact page contains `CONTACT_EMAIL`
   - JSON values of strings.json are scanned, not key names
2. `python3 tools/build.py && python3 tools/qa_site.py`: every file exists, every internal href and `#id` resolves, JSON-LD parses, no Review schema, hreflang sets are complete and reciprocal, sitemap valid, tracking URL in no HTML file, `/play` links accepted only if `_redirects` has the `/play` rule, zero inline styles/handlers.

## Browser QA (real CSP, local server)
- Serve `dist/` with a small server that sends the `_headers` CSP. Write the server script to a file and run it with nohup. Never `pkill -f python`: it kills your own shell.
- Every page of every edition + 404 at **360, 768, 1280** px: `scrollWidth <= clientWidth`, images decode, 0 console errors, CSP violations = 0.
- **200% text reflow**: set the root font size with JS `document.documentElement.style.setProperty('font-size','200%')` (an injected `<style>` tag is blocked by the CSP). Fixes that were needed: footer grids `minmax(0,1fr)`, headings `overflow-wrap:anywhere; hyphens:auto` (long German/Dutch compounds).
- Keyboard: skip link, mobile menu, FAQ `details`.
- Visual check that the TOC is gone and the content column is centered.

## Banned-word scan on the build (and later on live HTML)
Strip `<script>` and tags first, then search case-insensitive with word boundaries for every list in `check_content.py`. Also grep for: `On this page`, `independence`, `Independent`, `review`, `information site`, `KAP`, `—`, `–`, `18+`.

## Version discipline
- One source (`content/`, `tools/`, `assets/`); never hand-edit `dist/`.
- Rebuild, re-run both gates and re-zip after EVERY edit, however small. Never send an older zip as current.

## Packaging (two zips, send only one)
- `<site>-SITE-upload.zip`: the contents of `dist/` at the zip root. Used for the deploy only.
- `<site>-FINAL.zip`: `site/` (= dist) + `source/` (content, research, tools, specs, ledger) + README. This is the one deliverable sent to the owner. The owner asked for "one final zip only": do not send several.
- Verify both zips: file count, index.html at the SITE zip root, no source/research in the SITE zip.

## Live readback (after every deploy)
See `deploy-cloudflare-pages.md`. Report counts (e.g. "110 pages 200, /play 302, 0 banned words") and the expected Cloudflare diffs.

## Honest reporting
Say separately: built locally, packaged, uploaded, deployed (owner clicked), live verified. If a step waits on the owner's click, say so in one line.
