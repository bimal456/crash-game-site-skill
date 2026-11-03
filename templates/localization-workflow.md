# Multi-edition content workflow (agents)

Each stage gets: PROJECT.json, the spec files from `examples/chickenroad-radio-am/` (adapted to the new game), `research/facts.md`, the edition's research files and exact output paths. Agents do not inherit context: put the rules in the prompt and verify the returned files with the checker, not the agent's "done".

Voice rules (`references/voice-and-positioning.md`) go into EVERY stage prompt from the start. On chickenroad.radio.am they were added late and cost two full rewrite passes across 11 editions.

## Stage 1: Writer (one agent per edition, parallel)
- Writes every page in the edition's researched page set (the five trust pages + the content pages from the SERP inventory) + strings.json directly in the native language (not translated from English). English editions (global, UK, CA, AU) written separately with local law, spelling, currency, payments.
- Follows CONTENT_SPEC (front matter, `<section id>`, `{{BASE}}` links, CTA/FIG markers) and the content blueprint.
- Talks about the game and to "you". No we/our on game pages. No review/guide/information/independent wording. Byline/disclosure come from strings.json.
- Runs `check_content.py <ed>` until ALL OK.

## Stage 2: Independent reviewer (one per edition, a different agent)
- Follows REVIEW_SPEC: live SERP + 3-5 competitor outlines, fills missing high-intent sections/FAQ, fact-checks every legal/tax/helpline claim on official sources, native-language QA (grammar, idiom, search phrasing), writes `research/ledger-<ed>.json`.
- Re-runs the checker.

## Stage 3: Internal linking (one per edition, or one agent for all)
- Follows LINKING_SPEC / `references/internal-linking.md`. Wraps existing phrases, no word-count growth on home.

## Stage 4: Voice and positioning sweep
- Follows POSITIONING_SPEC + VOICE_SPEC. Greps every edition for the banned lists and first person, rewrites the sentence (not just deletes the word), keeps facts and word ranges.
- Should find nothing if stages 1-2 had the rules. Run it anyway.

## Stage 5: Build + QA (main agent)
- Merge ledgers into `claim-ledger.json`, `build.py`, `qa_site.py`, browser QA, banned-word scan, zips.

## If no subagents
Do the stages yourself in order and label the review as self-review.
