# Multi-geo editions

## URL structure
- English global edition at the root `/` = hreflang `en` + `x-default`.
- Each country edition in its own folder: `/in/` (hi-IN), `/it/` (it-IT), `/de/` (de-DE), `/es/` (es-ES), `/fr/` (fr-FR), `/uk/` (en-GB), `/pl/` (pl-PL), `/nl/` (nl-NL), `/ca/` (en-CA), `/au/` (en-AU). Add others the same way (`/br/` pt-BR, `/fi/` fi-FI ...).
- Same page slugs in every edition (`/it/demo/`, `/it/payments/`), trailing slash everywhere.
- Every page carries hreflang alternates for all editions that have that page + x-default, a self canonical, `og:locale` + `og:locale:alternate`. The sitemap repeats the alternates with `xhtml:link`.
- Footer has an editions switcher (same page in every edition, `hreflang` on each link).
- English editions (global, UK, Canada, Australia) are written separately with local spelling, currency, law and payments. Never copy one English edition into another.
- Canada defaults to English (en-CA) unless the owner asks for fr-CA.

## Native language rules
- Each geo is written in its native language by a native-level writer pass, then reviewed by a separate native QA pass.
- India: Hindi in Devanagari, keep the game name in Latin script where natural, use local nicknames people search (e.g. मुर्गी वाला गेम / murgi game). Section ids stay ASCII.
- Phrase headings the way locals search (keyword map), e.g. IT "paga davvero / è una truffa", DE "seriös / echt oder fake", ES "es fiable", FR "avis / arnaque" (as player question only), PL "opinie / czy bezpieczna", NL "betrouwbaar / echt".

## Localization pack per geo (research and verify on official sources)
Regulator and the TRUE legal status, tax on winnings, national helpline, self-exclusion scheme, common payment methods and withdrawal times, and whether the provider restricts the country.

Legal truths seen on the Chicken Road build (re-verify every time, laws change):
| Geo | Key facts used |
|---|---|
| Global EN | depends on reader's country; examples UKGC/MGA/AGCO; Gambling Therapy (gamblingtherapy.org) |
| India | Promotion and Regulation of Online Gaming Act 2025 bans online money games and their advertising (in force 1 May 2026, challenge at Supreme Court); 30% tax on net winnings (TDS); GST 40% on deposits from 22 Sep 2025; Tele-MANAS 14416. Owner decides whether /in/ keeps CTAs. |
| Italy | ADM licence only; tax at source on ADM sites; Telefono Verde 800 558 822; self-exclusion via ADM; provider restricts Italy |
| Germany | GGL / GlüStV 2021, whitelist; crash games not expected at GGL operators; winnings tax-free; BIÖG Telefonberatung 0800 1 37 27 00; OASIS; provider restricts Germany |
| Spain | DGOJ .es licence; IRPF; FEJAR 900 200 225, Jugar Bien, RGIAJ; RD 958/2020 bonus ban partly annulled (2024); provider restricts Spain |
| France | ANJ licenses only betting, horse racing, poker: online casino games not authorised; winnings not taxed for players; Joueurs Info Service 09 74 75 13 13; provider restricts France |
| UK | UKGC register; credit-card ban; bonus wagering cap 10x from 19 Jan 2026; GamCare 0808 8020 133 (NI 0808 8010 320); GamStop; provider restricts UK |
| Poland | online casino is a state monopoly (Total Casino); offshore sites blocked, player liability; KCPU 801 889 880 (paid line, 17-22h); provider restricts Poland |
| Netherlands | Ksa / Koa, Cruks; kansspelbelasting 37.8% (2026) paid by licensed operator; help via OpenOverGokken (Loket Kansspel replaced Oct 2025); game not at legal Dutch casinos; provider restricts NL |
| Canada | provincial: iGaming Ontario/AGCO, Alberta open market live since 13 July 2026, Crown sites; Interac; winnings generally not taxed; ConnexOntario 1-866-531-2600 |
| Australia | Interactive Gambling Act 2001 bans offering online casino games; ACMA blocks; credit cards banned for online wagering (June 2024); Gambling Help Online 1800 858 858; BetStop; provider restricts Australia |

Where the game is not legal or the provider restricts the geo: say it plainly and calmly, keep the demo as the safe option, CTA texts say "only where online casino play is legal for you", and no operator table may imply availability (use a "licence checks" table instead).
