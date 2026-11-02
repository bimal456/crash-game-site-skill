# Internal linking (contextual, in the body copy)

Nav, footer, breadcrumb and the "related pages" cards exist on every page, but the owner expects real in-text links too. A first build had 0-5 in-text links per page (payments and RG had none): not acceptable.

## Minimum contextual links per page (same edition; checker enforces)
| Page | Must link in text to |
|---|---|
| home | demo x2, sequel x2, payments x2, about (prefer about/#method) x1, responsible-gambling x1, contact x1 |
| demo | home x2, sequel x1, payments x1, responsible-gambling x1, about x1 |
| sequel | home x2, demo x2, payments x1, responsible-gambling x1, about x1 |
| payments | home, demo, sequel, responsible-gambling, about, terms (x1 each) |
| about | home, demo, sequel, payments, contact, responsible-gambling, privacy |
| contact | home, about, responsible-gambling, privacy |
| responsible-gambling | home, demo, payments, contact |
| privacy | cookie-policy, terms, contact, about |
| cookie-policy | privacy, terms, contact |
| terms | privacy, cookie-policy, responsible-gambling, contact, about |

## Rules
- Links sit in paragraphs, list items or FAQ answers where the topic is discussed. Never in headings, never on CTA markers, never to the page itself.
- Prefer wrapping an existing phrase (adds zero words; home is usually at its 3000-word cap).
- Anchor text 2-6 descriptive words in the edition's language, keyword-aware but varied (exact, partial, natural). Never "click here / here / read more" or local equivalents. No identical anchor for the same target twice on one page. Max 4 links to one target per page.
- Spread them through the page, roughly one per 100-150 words on content pages.
- Links always use the edition base + trailing slash (`{{BASE}}demo/`), so ranking never splits across URL variants.
- In-page anchors (`#section-id`) and section links (`{{BASE}}#legal-status`) must point to ids that exist.
