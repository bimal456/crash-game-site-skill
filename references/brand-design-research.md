# Brand and design research (owner rule, mandatory, before any CSS/image work)

The owner's correction: sites built from this skill were defaulting to the
same chicken-yolk-yellow/navy palette and a calm, article-like layout on
every build, regardless of what game or brand the site actually covers. His
rule now: **research the real brand first, design second.** This is the same
discipline `references/research-and-keywords.md` already requires for
content (facts before writing) — apply it to color and visual style too.

This step is **mandatory for every new site this skill builds**, and it is
specific to crash/instant-win games: the output must read as a game site,
never as a blog, magazine, review site or "informational" page.

## 1. Research the brand before touching colors

For the game/provider named in the brief, before writing any CSS or
generating any image:
- Open the provider's own official page for the game (the same page already
  used for RTP/specs in `research-and-keywords.md`) and its app
  store/Play Store listing if one exists. Note the dominant colors used in
  their own hero art, buttons and logo lockup.
- Check the provider's official social banners (X/Twitter header, Facebook
  page) and any official press/media kit page for stated brand colors.
- Check 2-3 of the biggest third-party pages about the same game (casino
  lobby listing pages, the provider's own blog) for which colors they use to
  represent it — this corroborates what you saw on the provider's own page,
  it is not a style to copy wholesale.
- Write down: primary color (hex), one or two accent colors (hex), whether
  the overall mood is bright/playful, dark/intense, neon/arcade, or
  minimal/premium. Save this to `research/brand-palette.md` alongside the
  other research files, with the source URL(s) for each color decision.
- **No official color signal found anywhere?** Then, and only then, choose
  your own palette — but it must still follow the house rule below (bold,
  game-appropriate, high contrast) and should fit the theme of the game
  itself (e.g. a river/ice game leans cold blues; a fire/lava game leans hot
  reds and blacks) rather than reusing another site's palette out of
  convenience.

## 2. Apply the researched palette

**Copy the skill's `assets/` and `scripts/` into the project first** (that is
step 4 of SKILL.md, but for a recolor you do it now) and edit the PROJECT's
copies. Never edit the skill's own files: every later site would inherit
this brand's colors.

- In the project's `assets/style.css`, replace the placeholder hex values in
  `:root` with the researched colors. Keep the same variable roles (one
  strong dark `--primary` for header/text, one loud `--accent` for every CTA
  and highlight, one secondary `--accent-2` for variety) so the rest of the
  stylesheet keeps working — only the hues change.
- **`:root` is not the whole job.** `:root` also carries derived tokens that
  are tints of the same two colors: `--primary-rgb`, `--accent-rgb`,
  `--primary-100/200/300/400/500/700`, `--accent-light`, `--accent-border`,
  `--link`, `--link-2`, `--deco`. Re-derive all of them from the new palette.
  If you only swap `--primary` and `--accent`, the site ships a correctly
  colored header above a footer, CTA glow and button-hover still tinted in
  the old brand's colors. A few neutral greys remain as raw hex in the
  stylesheet body; grep for `#` after recoloring and judge each one.
- Do the same in the project's `scripts/make_images.py` CONFIG block: every
  hex there, not only the first six, plus `GAME_TITLE`, `GAME_TITLE_L1`,
  `GAME_TITLE_L2` and `EDITION_LABEL`, which are burned into the logo,
  gameplay board and og image as text.
- Then render and LOOK at the output (`assets/img/og.webp`, `logo.webp`,
  `gameplay.webp`). The og image is what gets shared and the favicon is what
  sits in the tab: a half-swapped palette or another game's name is most
  visible exactly there.
- If the official brand uses light/pale colors rather than saturated ones,
  use light colors — match what is actually official, do not darken or
  saturate it to force a "bold" look. "Bold" here means confident and
  game-like in its use of color and shape, not necessarily dark or neon.

## 3. House rule: it must look like a game site, not a blog

Independent of which exact colors research turns up, every build must avoid
the visual tells of a blog/article/review/informational site:
- A hero-style opening (the existing `.opening-inner` block) with a strong
  color block, not a plain white "article intro" look.
- CTA buttons that are large, high-contrast and placed like a game's "Play"
  button, not a muted text link.
- Illustration/iconography on-theme for the actual game (lanes, multipliers,
  the game's real subject — see the notice at the top of
  `scripts/make_images.py`), not generic stock-photo-style imagery.
- Cards, callouts and the pros/cons box (already required by the Design hard
  rules in SKILL.md) keep their hover lift and color-coded top borders —
  this is what reads as "product/game site" rather than "magazine article."
- What stays the same regardless of brand: no table of contents, the long-
  form SEO prose itself, and the designed-sections-only rule (5-6 sections,
  Responsible Gambling and Conclusion stay plain) — the content and
  structure rules are unchanged. Only the color system and the
  illustration subject are brand-specific; the page skeleton is not.

## 4. Logo

- Treat the provider/game's name and wordmark the same way this skill
  already treats trademarks elsewhere (see `voice-and-positioning.md`:
  "`<Game>` is a trademark of `<Provider>`, used only to identify the
  game"): the site may show the official game/provider logo in the header
  for identification, sourced from the provider's own official page or
  press/media kit, exactly as published, with that trademark notice in the
  footer. Do not alter, recolor or "improve" a sourced logo.
- If no official logo asset can be sourced cleanly (no press kit, a rights
  question comes up, or the only copies available are low-resolution
  screenshots of in-game art), do not improvise a lookalike. Fall back to an
  original text wordmark for the site's own name, set in the researched
  brand colors and a bold display font — never a redraw or close imitation
  of the provider's actual logo mark.
- This is narrower than the "never copy provider art" rule in
  `technical-seo-and-templates.md`, which still applies in full to in-game
  illustrations, mascots and screenshots used as the site's own decorative
  artwork (those stay original, per `scripts/make_images.py`). The logo
  exception above is only for the single header/footer brand mark used to
  identify the game being covered, and that file states the same exception,
  so the two agree.
- `build.py` currently hardcodes `width="512" height="512"` on the header
  and footer logo `<img>`. A real logo or a wordmark is rarely square:
  set those attributes to the asset's true dimensions, or the page ships a
  wrong intrinsic aspect ratio and the image is squashed.

## Where this fits in the workflow

Run this step once per site, right after the facts/keyword research in
`references/research-and-keywords.md` and before the build in
`references/technical-seo-and-templates.md`. See SKILL.md step 1b.
