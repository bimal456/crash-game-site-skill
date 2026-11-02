# Voice and positioning (owner rules, highest priority)

These rules came from the owner's direct corrections on chickenroad.radio.am. They override the older skill text that asked for an "independence line", an "info / review" framing, an editorial team and a "how we review" method.

## What the site IS
A site about the game, written directly about the game and to the player:
- "Chicken Road is a crash game from InOut Games. You lead a hen across lanes ..."
- "Pick Easy if you want long sessions; Hardcore if you accept losing most rounds."
- "Try the free demo first, then play only where online casino play is legal for you."

Confident, money-forward, cautious on facts, second person for the player. The provider is the maker in third person. The site never claims to be the official game site and never writes as the provider or as a casino.

## What the site must NEVER say (any language)
| Category | Banned (examples, not exhaustive) |
|---|---|
| Positioning | independent, unofficial, not affiliated, no affiliation, "we are not the operator / a casino", "no games hosted here", information site, info site, informational, sito informativo, Informationsseite, sitio informativo, site d'information, serwis informacyjny, informatiesite, जानकारी साइट, स्वतंत्र, unabhängig, indipendente, independiente, indépendant, niezależny, onafhankelijk |
| Review voice | review(s), reviewed, reviewer, verdict, recensione/recensioni, Rezension, Testbericht, reseña, recenzja, recensie, beoordeling, समीक्षा, रिव्यू, verdetto, veredicto, werdykt, oordeel, "our opinion", "in our view", "our take" |
| Editorial voice | editorial team, redazione, Redaktion, redacción, rédaction, redakcja, redactie, संपादकीय टीम, "we tested", "our test", "tested by", getestet, abbiamo testato, hemos probado, nous avons testé, przetestowaliśmy |
| Guide | guide, guidance, guida, gids, guía, Leitfaden, Ratgeber, przewodnik, poradnik, गाइड, मार्गदर्शिका (zero "guid" matches) |
| Other | em dash, en dash as dash, 18+, KAP / KAP Digital, star ratings, x/10 scores |

First person plural is banned on game pages (home, demo, sequel, payments) and in strings shown sitewide (descriptor, footer_about, CTA texts, captions):
EN we/our/us, IT noi/nostro, DE wir/unser, ES nosotros/nuestro, FR nous/notre/nos, PL my/nasz/nam/nas, NL wij/we/ons/onze, HI हम/हमारा/हमारी/हमारे/हमने.
Legal/trust pages (about, contact, privacy, cookie, terms, RG) may use "we" as the site operator ("we do not set cookies").

Note: German "unseriös" contains "unser", Polish verbs ending in -my are first person: rephrase.

## What replaces the old elements
| Old (removed) | New |
|---|---|
| Opening "independence line" + footer "Independent site, not affiliated ..." | Nothing. Round 4 removed the replacement too: no disclosure line at all (see below). Footer legal is the trademark sentence only: "<Game> is a trademark of <Provider>." |
| footer_about "An independent information site ..." | "<Game> explained in plain terms: how the crash game by <Provider> works, the demo, payments and where to play it safely." style sentence, no we/our, no review |
| Byline "By the editorial team · Updated · How we review" | "Updated <date> · Sources" (link to about#method) |
| Home section "Review and opinions / our verdict" + verdict box | "<Game> pros and cons" section with a pros-cons box; player opinions only as "what players say" |
| Eyebrow "Independent game review" | "<Game> crash game" (localized) |
| About "Who we are (independent editorial team)", "Our independence", "How we test and review" | "About <domain>": what the site covers; `#method` "How the pages are kept up to date" (facts from provider page and regulators, specs checked against the in-game info panel, pages re-dated); `#sources-we-use` |
| editorial@<domain> | contact@<domain> (owner may not create a mailbox; do not push him to) |
| Organization author "editorial team" in schema | author = the Organization (@id) |

## Disguised review/information voice (passes a literal word-checker, still the same spirit)

A literal banned-word pass can come back clean while About/Contact/Terms
pages still read as a review or information site. Watch for these five
patterns specifically — they are owner-confirmed as the ways this drift
happens, found on a full manual read of the live site, not from a checker
run:
1. **Origin-story justification** — "why this site exists" sections ("a
   small group of writers...", "the market was crowded with clone apps so
   we..."). Delete; state what the site covers, not why it was started.
2. **Editorial-independence boasts** — the owner removed "no payment could
   change what we publish", "we do not sell advertising space, sponsored
   articles or paid placements", and scene-setting like "running a
   multi-language site costs money, and we prefer to be upfront about it".
   What he KEPT, depersonalized, is the plain factual version: "Commissions
   never change the facts published: the RTP, the risks, the scam warnings
   and the legal notes stay the same." So: one flat factual sentence is
   fine; anything that performs integrity, lists what the site refuses to
   sell, or asks for credit is not.
3. **Self-deprecating editorial tone** — "we make mistakes like anyone
   else", "we're only human". State the corrections mechanism plainly, no
   self-deprecation.
4. **"Small team" framing** — "we are a small team, so busy periods can take
   longer". State response-time facts without describing team size.
5. **"We rank/judge our own sources" meta-commentary** — "we rank our
   sources by how neutral they are". List the method as facts; never frame
   the site as grading its own neutrality.

Also: the word **"information"** used to describe what the site itself
publishes ("general information about...", "Information only, not advice"
as a heading, "we publish information, not advice") is the same positioning
problem as "information site" even without that exact phrase — it is what
triggered the owner's original complaint ("how dare you use the word
information"). Treat bare "information"-as-self-description the same as the
literal "information site" ban above; legal disclaimer language should say
what the content is NOT (not advice, not a guarantee) without using
"information" to describe what it IS.

## No disclosure line at all (round 4, owner rule, zero tolerance)

The owner's instruction: "ye nahi honi chahiye kisi bhi keemat pe kisi bhi
page pe" — the promotional-disclosure line must not appear on any page, at
any cost, in any language. This replaces the earlier rule that allowed a
short "Contains promotional links." line.

Banned everywhere (opening block, footer, `strings.json`, meta, alt text):
"Contains promotional links", "Contains promotional links for adults",
"Enthält Werbelinks", "Contiene enlaces promocionales", "Contiene link
promozionali", "Contient des liens promotionnels", "Bevat promotielinks",
"Zawiera linki promocyjne", "इसमें प्रमोशनल लिंक हैं", and any other
localized equivalent. There is no `independence` string, no
`<p class="disclosure">` and no `.disclosure` CSS class. `check_content.py`
fails the build on all of these.

What stays, and is not the same thing:
- `rel="nofollow sponsored noopener"` on every CTA (machine-readable, invisible).
- The affiliate-disclosure SECTION in the about and terms body copy
  ("Some buttons on this site are affiliate links..."). That is page
  content in a legal page, not a site-wide banner line.
- `cta_note` under play boxes ("Promotional link. Opens the operator in a
  new tab.") is a different sentence serving a different purpose. The owner
  has not asked for it to go; confirm with him before removing it on a new
  site.

## Honest facts still required
Keep: legal status per geo (including "not legal here" where true), provider restricted-countries notes, RTP as long-run average, operator-dependent caps, clone/fake-app warnings, responsible gambling with the national helpline, tax notes with "not tax advice". Voice rules change how things are said, not whether the facts are true.
