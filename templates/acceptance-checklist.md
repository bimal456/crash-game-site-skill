# Acceptance matrix

Mark every row `passed`, `failed`, `blocked` or `n/a` with real evidence (path/URL, count). Never mark a planned check as passed. Copy to `ACCEPTANCE.md` in the project.

| Area | Required evidence | Status / count |
|---|---|---|
| Inputs | Game, sequel, geos + languages, tracking URL (or flagged placeholder) | |
| Research | Ahrefs matching-terms + overview + serp-overview per edition; DataForSEO live SERP per edition; 3-5 competitor outlines per edition | |
| Facts | facts.md + claim-ledger.json with sources; provider restricted-countries checked | |
| Localization | Regulator, legal truth, tax, helpline, self-exclusion, payments per edition, verified on official sources | |
| Structure | `/` + `/<code>/` per edition, same slugs, 10 pages each + 404 | |
| Word counts | home 2700-3000; demo/sequel/payments 1500-1800; others in range; prose 70%+ | |
| Positioning | 0 matches: guide, information/info site, independent, unofficial, not affiliated (all languages) | |
| Voice | 0 matches: review, verdict, editorial team (all languages); 0 we/our on game pages | |
| Byline / no disclosure | "Updated <date> · Sources" on every page; no author/team; and ZERO promotional-disclosure lines sitewide in any language (grep the build) | |
| Design | No TOC; one centered column; 5-6 designed home sections; RG plain; no Conclusion | |
| Meta | Titles <= 60, descriptions exactly 158, unique, keyword first, year | |
| Headings | One H1 per page; H2/H3 in native search phrasing | |
| Internal links | LINK_REQ met on every page of every edition; anchors varied; no broken links/anchors | |
| hreflang | Full reciprocal set + x-default on every page and in the sitemap; editions switcher in footer | |
| Schema | Parses; Org/WebSite/WebPage/Breadcrumb/Article(author org)/FAQPage/VideoGame; no Review/Rating | |
| CTA | Every CTA `https://<domain>/play`, `_blank`, `nofollow sponsored noopener` | |
| Cloak | `_redirects` /play 302, /login 301; tracking URL in 0 HTML files; /play noindex header + robots disallow; not in sitemap | |
| CSP | 0 inline style/handlers; 0 console/CSP errors live | |
| Images | Original illustrations, decode, alt in edition language, linked to demo/sequel | |
| Responsive | All pages + 404 at 360/768/1280: no overflow; 200% reflow OK | |
| Hard rules | 0 "guid", 0 em/en dash, 0 "18+", 0 KAP | |
| Packaging | ONE FINAL zip sent; SITE zip has index.html at root and no source | |
| Deploy | Correct Cloudflare account; owner clicked Save and deploy; custom domain Active; Always Use HTTPS on | |
| Live readback | All pages 200, http->https, real 404, /play 302, /login 301, banned-word scan on live HTML = 0, byte diff only expected Cloudflare changes | |
| Open owner decisions | Listed (e.g. India CTAs) | |
