# Cat Food Center - Design System

**Scope:** the visual and interaction system for the whole site.
**Companion documents:** [PRD.md](PRD.md) for product, architecture and policy; [PATCHNOTES.md](PATCHNOTES.md) for history; [README.md](../README.md) for the general reader.
**Last full audit:** 2026-09-06

**Read this first.** The site currently runs **two different implementations of one design**. The guide pages are the reference: everything in section 4 describes what the site is converging on, and the eight application pages described in section 5 are the ones that have not converged yet. M14 is that convergence, and this document is written so that it can be carried out by reading it rather than by reading eight files.

---

## Table of contents

1. [Design principles](#1-design-principles)
2. [Tokens](#2-tokens)
3. [Typography](#3-typography)
4. [The reference system: guide pages](#4-the-reference-system-guide-pages)
5. [The other system: application pages](#5-the-other-system-application-pages)
6. [M14: converging the two](#6-m14-converging-the-two)
7. [Components](#7-components)
8. [Score presentation](#8-score-presentation)
9. [Accessibility](#9-accessibility)
10. [Motion](#10-motion)
11. [Responsive behaviour](#11-responsive-behaviour)
12. [Iconography and assets](#12-iconography-and-assets)
13. [Not built](#13-not-built)

---

## 1. Design principles

1. **The verdict is the page.** On a product page, the score, its band and a one-line reason come before everything else in the source order and in the visual hierarchy. Nothing animates in front of them.
2. **Colour is never the only signal.** Every band carries a text label as well as a colour. Roughly one man in twelve has a colour vision deficiency, and a red-green scale with no text is unreadable to them.
3. **The score palette is reserved.** `--excellent`, `--good`, `--poor` and `--bad` are used for ratings and nothing else. A green button would teach the reader that green means "action" on one page and "good food" on another.
4. **Never hardcode ink on a fill.** `text-white` on `--accent` is wrong even where it happens to be legible, because the dark theme flips it. Every fill has a paired ink token, and the pair is what gets used.
5. **Warm, not clinical.** Cream ground, a serif display face, and an ember accent rather than the blue-grey of a dashboard. The subject is somebody's pet.
6. **Density serves reading.** Long-form pages cap their measure at 62 to 68 characters. A full-width paragraph on a 1440px screen is not more information, it is a worse one.
7. **Mobile is the canvas.** Every layout is designed at 360px first. Nothing may scroll horizontally at that width, and `tools/check-live.py` asserts it on every page it loads.

---

## 2. Tokens

Every colour on the site comes from a custom property in [`assets/cfc-tokens.css`](../assets/cfc-tokens.css). That file is loaded by **both** page families, which is what lets one theme choice apply across a site built two different ways.

Tokens are named for their **role**, never their value. There is no `--orange`.

### 2.1 Core palette

| Token | Light | Dark | Role |
|---|---|---|---|
| `--bg` | `#FAF7F2` | `#14120F` | Page ground, warm off-white |
| `--surface` | `#FFFFFF` | `#1C1916` | Cards, top bar, panels |
| `--ink` | `#1C1A17` | `#EFEAE2` | Body text |
| `--ink-soft` | `#56504A` | `#A49B90` | Secondary text, labels |
| `--accent` | `#C2410C` | `#FB8B4C` | Links, primary actions, active state |
| `--accent-sub` | `#FBEDE6` | `#2C1D13` | Tinted accent ground |
| `--hairline` | `#E7E1D8` | `#332D26` | Borders and rules |
| `--on-accent` | `#FFFFFF` | `#2A1206` | Ink on an accent fill. **Never substitute `white`** |
| `--shadow` | `rgba(28,26,23,.08)` | `rgba(0,0,0,.55)` | Elevation |
| `--scrim` | `rgba(28,26,23,.28)` | `rgba(0,0,0,.62)` | Drawer backdrop |

### 2.2 Score palette

Used as **text and border** colours, so they must contrast against `--bg` and `--surface`.

| Token | Light | Dark | Band |
|---|---|---|---|
| `--excellent` | `#1B7A4B` | `#4ADE80` | 75 to 100 |
| `--good` | `#5FA855` | `#86C46F` | 50 to 74 |
| `--poor` | `#E08A1E` | `#F0B45E` | 25 to 49 |
| `--bad` | `#C0392B` | `#F1786A` | 0 to 24 |
| `--warning-ink` | `#A9660D` | `#F0B45E` | A darkened `--poor` for callout text, because `--poor` is a fill colour and is too light to read as text on cream |

### 2.3 Chip tokens

Chips are **fills with text on top**, so each fill carries its own ink. This is not decoration: **amber and mid-green cannot carry white text at AA**, which is why those two use dark ink in the light theme. Dark mode did not cause that problem, it exposed it. The chips had been shipping at 2.8:1 and 2.3:1.

| Fill | Light | Ink | Dark | Ink |
|---|---|---|---|---|
| `--chip-excellent-bg` | `#1B7A4B` | `#FFFFFF` | `#4ADE80` | `#06240F` |
| `--chip-good-bg` | `#5FA855` | `#0E2109` | `#86C46F` | `#0E2109` |
| `--chip-poor-bg` | `#E08A1E` | `#2A1C05` | `#F0B45E` | `#2A1C05` |
| `--chip-bad-bg` | `#C0392B` | `#FFFFFF` | `#F1786A` | `#2A0D0A` |
| `--chip-accent-bg` | `#C2410C` | `#FFFFFF` | `#FB8B4C` | `#2A1206` |
| `--chip-neutral-bg` | `#56504A` | `#FFFFFF` | `#A49B90` | `#14120F` |

Plus `--warn-bg` / `--warn-ink` for the warning callout ground.

### 2.4 Layout tokens

| Token | Value | Used by |
|---|---|---|
| `--topbar-h` | `56px` | The fixed bar, the shell's top padding, and `scroll-margin-top` on every anchor |
| `--sidebar-w` | `264px` | Guide sidebar, and the mobile drawer width via `min(84vw, ...)` |
| `--toc-w` | `240px` | The "On this page" column |

### 2.5 The duplicated dark block, and why

The dark values appear **twice** in `cfc-tokens.css`: once under `:root[data-theme="dark"]` for an explicit choice, and once under `@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) }` for a visitor who has not chosen. CSS cannot express "this media query, unless an attribute says otherwise" in a single declaration block without either a preprocessor or a level of nesting the project does not use.

**The two lists must stay in sync**, and `tools/check-contrast.py` fails if they drift. Removing that check makes the duplication a silent hazard rather than a managed one.

### 2.6 Theming mechanism

Three states: `light`, `dark`, `system`. The choice is stored in `localStorage` under `cfc-theme`; `system` stores nothing and lets the media query decide.

[`assets/cfc-theme.js`](../assets/cfc-theme.js) is a **blocking script in `<head>`** on every page. That position is the entire mechanism: it sets `data-theme` on `<html>` before first paint, so there is no flash of the wrong palette. Adding `defer` or `async`, or moving it to the end of the body, breaks it on every page at once and is listed in the PRD as a change never to make.

One button with three icons, `.theme-toggle`. CSS picks which icon is visible from `data-theme-state`, so the script only sets an attribute. Before the script runs, the system icon shows rather than nothing.

---

## 3. Typography

| Face | Use | Loaded |
|---|---|---|
| **Fraunces** | Display: the wordmark, `h1` to `h3`, card and entry titles | Google Fonts, weights 400/600/700 |
| **Public Sans** | Everything else | Google Fonts, weights 400/500/600 |

Both fall back to `Georgia, serif` and `system-ui, sans-serif` respectively. `.font-display` is the class that applies Fraunces in both page families.

Base size is **15px** on guide pages, with the scale below. Application pages set their own equivalents in a per-page `<style>` block, which is one of the duplications M14 removes.

| Role | Size | Line height | Notes |
|---|---|---|---|
| `h1` | 1.75rem (1.625rem below 900px) | 1.2 | Fraunces |
| `h2` | 1.375rem (1.1875rem below 900px) | 1.3 | Fraunces, with a short accent rule via `::before` |
| `h3` | 1.0625rem | 1.4 | Fraunces |
| `h4` | .9375rem | 1.4 | 600 weight |
| Lede | 1rem | 1.7 | `--ink-soft`, capped at 62ch |
| Body | .9375rem | 1.6 to 1.7 | Capped at 68ch |
| Small | .875rem | 1.5 | Table and callout body |
| Micro | .75rem | 1.4 | Footnotes, footer, meta |
| Chip | .6875rem | 1.5 | 500 weight |

Numeric columns use `font-variant-numeric: tabular-nums` so figures line up down a table.

---

## 4. The reference system: guide pages

Eleven pages (`learn.html` and ten `learn-*.html`), generated by `tools/learn/build.py` from `tools/learn/shell.py` plus one `c_*.py` content module each, styled by [`assets/cfc.css`](../assets/cfc.css) and driven by `assets/cfc-docs.js`. **This is the look the project is standardising on.**

### 4.1 The shell

```
┌──────────────────────────────────────────────────────────────┐
│ .topbar   fixed, 56px, --surface, hairline bottom            │
│  [paw] Cat Food Center      ·spacer·   [search] [theme] [CTA]│
├───────────────┬──────────────────────────┬───────────────────┤
│ .sidebar      │ .article                 │ .toc              │
│ 264px         │ minmax(0,1fr)            │ 240px, sticky     │
│ sticky        │ crumbs, h1, lede, body   │ "On this page"    │
│ section list  │ max 68ch measure         │ scroll-spy links  │
└───────────────┴──────────────────────────┴───────────────────┘
                 .site-footer, four columns
```

`.shell` is a CSS grid, `max-width: 1440px`, `padding-top: var(--topbar-h)` to clear the fixed bar. `gap: 0 40px`.

### 4.2 The top bar

`.topbar` is **`position: fixed`** at every width. (An earlier version of this document said the header was fixed on mobile and sticky on desktop. That was never true of either family. Guide pages are fixed at every width; application pages are sticky at every width.)

Contents, left to right:

- `.nav-toggle`, a hamburger. `display: none` above 900px, shown below it.
- `.topbar-brand`: paw glyph plus the wordmark, in Fraunces.
- `.topbar-spacer`, `flex: 1`.
- `.topbar-search`: a 260px **link styled as a search field**, with a magnifier, the word Search, and a `/` key hint in a `.kbd`. It navigates to `search.html`; it is not an input. Hidden below 900px.
- `.theme-toggle`.
- `.topbar-cta`: the pill-shaped Support link.

**The gap that blocked M14:** this bar carries no page navigation at all. There are no links to Home, Scan, Search, Brands, Compare or Methodology in it. A reader on a guide page can reach the rest of the site only through the footer or the sidebar's own list.

### 4.3 The sidebar

`.sidebar`, 264px, sticky, holding the eleven-page section list grouped under `.sidebar-label` headings. The current page carries `aria-current="page"` and renders in `--accent` on `--accent-sub`.

Below 900px it becomes a **drawer**: `position: fixed`, `width: min(84vw, 264px)`, translated off-canvas by `translateX(-102%)` and brought back by `body.nav-open`. A `.sidebar-backdrop` fills the rest of the viewport at `--scrim` and closes on click. `cfc-docs.js` owns the open and close, including Escape.

### 4.4 The article column

Breadcrumbs (`.crumbs`), `h1`, `.lede`, then body. `h2` carries a short accent rule drawn with `::before`. Measure is capped at 68ch for prose and lists, 62ch for the lede. Every `h2[id]`, `h3[id]` and `section[id]` gets `scroll-margin-top: calc(var(--topbar-h) + 20px)` so an anchor does not land under the fixed bar.

`.pagination` closes each page with previous and next cards, using a `.placeholder` with no border where one direction does not exist.

### 4.5 The "On this page" column

`.toc`, 240px, sticky, a left hairline rule with the active link marked by `.is-active` in accent. Scroll-spy is in `cfc-docs.js`. **Hidden entirely below 1180px**, which is the right call: a table of contents that is not visible alongside the text it indexes is a second navigation with no advantage over scrolling.

### 4.6 The footer

`.site-footer`, four columns at `1.4fr 1fr 1fr 1fr`, collapsing to two below 900px and one below 560px. Brand, tagline, a dashed `.footer-cta`, three link columns, and a `.site-footer-base` strip. This is a full site footer and is the richest navigation the guide pages have.

---

## 5. The other system: application pages

Nine pages: `index`, `search`, `brands`, `product`, `scan`, `submit`, `compare`, `methodology`, `offline`. Styled by **Tailwind loaded from a CDN**, themed through `assets/cfc-tailwind.js` which maps Tailwind colour names onto the same `var(--...)` tokens, plus a **per-page `<style>` block** that redefines the same handful of utilities in every file.

Documented here as the current state, not as a pattern to extend.

### 5.1 Structure

- `<header class="sticky top-0 z-50 bg-surface border-b border-hairline">`, 56px tall, inside a `max-w-content` (720px) container. **Sticky, not fixed**, at every width.
- Wordmark, then a `<nav aria-label="Main navigation">` of seven `.nav-link` items (Home, Scan, Search, Brands, Compare, Learn, Methodology), then the theme toggle, then the Support pill.
- The nav scrolls horizontally on narrow screens (`overflow-x: auto`, `scrollbar-width: none`). It is the weakest part of the current chrome: on a 360px screen most of the links are off-screen with no visible indication that they exist.
- `<main class="flex-1 w-full max-w-content mx-auto px-4 py-8">`.
- A single-line footer with a `Built by Azqato` credit.

### 5.2 What these pages have that the guide does not

- Page navigation in the bar.
- A real search form on `search.html` and `index.html`, rather than a link.
- Narrow measure by container (720px) rather than by `ch`.

### 5.3 What they lack

- The sidebar, the "On this page" column, the drawer, and the full footer.
- Any generated chrome. **All nine headers and footers are hand-copied.** Adding one nav link is a nine-file edit, which is exactly how a link comes to be missing from one page.
- Consistency of the type scale, which is redefined per page.

### 5.4 Tailwind rules that still apply until M14 removes it

- **Never use an opacity modifier on a themed colour.** `bg-surface/50` renders transparent, because Tailwind cannot compute an opacity variant of a `var()`. Add a token to `cfc-tokens.css` instead.
- **Never write `text-white` on an accent fill.** Use `text-on-accent`. (An earlier version of this document prescribed `bg-accent text-white` in its button and badge patterns while also forbidding it three sections earlier. The prohibition is correct and the code follows it.)
- Colour utilities resolve through `cfc-tailwind.js`, so `bg-surface`, `text-ink`, `border-hairline` and the score names are all available.

---

## 6. M14: converging the two

**Decision, 2026-09-06: the application pages move onto the guide's system.** Two parts, both agreed.

### 6.1 Navigation: inline, with a drawer on mobile

The blocker was that the guide bar has no page navigation and the app bar has navigation but neither a search affordance nor a drawer control. The resolution:

- **Above roughly 900px:** the page links sit inline in `.topbar`, between the brand and the spacer, styled as the current `.nav-link` (small, `--ink-soft`, accent and 600 weight for `aria-current`). The `.topbar-search` field, the theme toggle and the Support pill keep their places on the right.
- **Below 900px:** the links move into the existing `.nav-toggle` drawer, which stops being a guide-only control and becomes the site menu. On a guide page the drawer shows the site links first and the guide's section list nested beneath them. **One control, two levels**, rather than a hamburger next to a scrolling link strip.
- The `.topbar-search` link continues to disappear below 900px, where the search page itself is one tap away in the drawer.

This is chosen over the alternatives because it keeps the desktop bar shallow (no dropdown to discover) and because the drawer already exists, is already accessible, and is already tested.

### 6.2 Tailwind is dropped

The port moves the application pages onto `cfc.css` and removes `https://cdn.tailwindcss.com` and `cfc-tailwind.js` from all nine.

The reason is not tidiness. It is a **render-blocking third-party script on every application page**, unpinned, whose content can change without a commit in this repository. It is the project's only real supply-chain exposure and it is the largest single item M12 will measure. Since the port rewrites the markup of those pages anyway, doing it in utility classes that are about to be deleted would be work done twice.

The cost is real and is stated plainly: nine pages of utility-class markup rewritten by hand, and a set of app-specific components (result cards, the pager, the score header, the compare table, the scanner viewport) that currently exist only as Tailwind class strings and will need real class names in `cfc.css`.

### 6.3 What the port must preserve

- The seven navigation destinations, and `aria-current="page"` on the current one.
- The theme toggle in the bar on every page, with `cfc-theme.js` still blocking in `<head>`.
- The search form on `search.html` and `index.html` as a real form, not a link.
- Every `esc()` call in the page modules. The port is markup, not rendering logic.
- `SHELL_ASSETS` in `sw.js` updated for any file added or removed.

### 6.4 Open questions, unresolved

1. **What fills the third column on a page with no headings to index?** A product page has a natural "On this page"; a scan page does not. Options are collapsing to two columns per page type, or repurposing the column (recently viewed on a product page, filters on search). Not decided.
2. **Does the `/` search affordance stay on pages that already carry a search input in the body?** Two routes to the same place inside one viewport. Not decided.

Both are carried in PRD section 25.5 as open questions 5 and 6.

---

## 7. Components

Defined in `cfc.css` and available to any page loading it. After M14 these are the site's whole component vocabulary.

| Component | Class | Notes |
|---|---|---|
| **Chip** | `.chip` plus `.chip-<band>` | The one component already shared by both families, because it lives in `cfc-tokens.css`. Pill, .6875rem, fill plus paired ink |
| **Callout** | `.callout` plus `.callout-note` / `-tip` / `-warning` / `-danger` | Left border in the state colour, an icon, an optional `.callout-title`. Warning uses `--warning-ink` for its text, not `--poor` |
| **Panel** | `.panel`, `.panel-head`, `.panel-body` | Formulae, worked examples, quoted blocks. Tabular numerals in the body |
| **Data table** | `.table-wrap` wrapping `table.data` | The wrapper is what scrolls horizontally. A `caption` is expected. `.num` for figures, `tr.grp` for a group heading row |
| **Entry card** | `.entry`, `.entry-head`, `.entry-name`, `.entry-meta` plus a `dl` | Additive and nutrient definitions. The `dl` is the pattern for Function, Health impact, Source |
| **Two-up** | `.compare` | A 1fr 1fr grid, single column below 900px |
| **Card grid** | `.card-grid` with `.card`, `.card-eyebrow`, `.card-title`, `.card-desc` | Hub links and next steps. Border turns accent on hover |
| **Checklist** | `.checklist` | Drawn box via `::before`, not a checkbox input. Presentational |
| **Sources** | `ul.sources` | Hairline-separated citation list, `--ink-soft` |
| **Prev / next** | `.pagination` with `.dir` and `.label` | `.placeholder` for a missing direction |
| **Skip link** | `.skip-link` | Off-screen until focused, then 8px from the top |
| **Visually hidden** | `.sr-only` | |

**Buttons** are currently expressed as Tailwind utility strings on application pages and as `.topbar-cta` / `.footer-cta` in the guide. A shared button component is part of the M14 port and does not exist yet.

**Lists of products** use `<ul style="list-style:none;padding:0">` with an `<a>` card per item, carrying `data-scorable` so the scorable-only filter can act on the rendered page. They are plain anchors: an earlier version of this document specified `<Link>` cards, which is a React component in a project that has no React.

---

## 8. Score presentation

The single most important thing on the site, so its rules are strict.

- **Score, band label and one-line verdict come first**, in source order and visually.
- **The number is large and the band label is adjacent**, never implied by colour alone.
- **Band colours are `--excellent` / `--good` / `--poor` / `--bad` and are used nowhere else.**
- **A partial score is marked as partial.** Where a pillar could not be computed, the page says which, because a 72 from three pillars and a 72 from one are different claims wearing the same number.
- **Confidence is shown alongside the score**, not folded into it.
- **An unscorable product shows no number at all.** It shows what is missing. There is no grey placeholder score and no zero.
- **A hard gate is stated as a gate.** Propylene glycol produces a callout saying it is prohibited in cat food in the United States, rather than a quietly lower number.
- **A cached answer is labelled a saved copy, with its date.** This is a design requirement, not only a technical one: an old score presented as a current one is the worst failure the cache could cause.

On the compare page, a cell is highlighted only where both products publish a figure. Where one is missing, neither is highlighted, because the difference would be a comment on the database rather than on the food. No overall winner is declared.

---

## 9. Accessibility

Target: **WCAG 2.1 AA**.

- **Contrast is enforced, not asserted.** `tools/check-contrast.py` checks 38 foreground and background pairs across both palettes and fails the build if any falls below AA. It is the reason the chip inks are what they are.
- **Colour is never the only signal.** Every band, tier and state carries text.
- **Focus is always visible.** `input[type=search]:focus` takes a 2px accent outline; interactive elements keep a visible focus ring. Never set `outline: none` without a replacement.
- **A skip link** is the first focusable element on guide pages.
- **Landmarks:** one `<header>`, one `<main>`, one `<footer>`, `<nav>` with an `aria-label` where more than one exists on a page.
- **`aria-current="page"`** on the active navigation and sidebar link.
- **Icon-only controls carry `aria-label`.** The theme toggle and the nav toggle both do.
- **The drawer traps nothing but closes on Escape** and on a backdrop click, and the backdrop is a real `<button>` so it is reachable.
- **Headings descend in order.** One `h1` per page.
- **Tables carry a `caption`**, and the wrapper scrolls rather than the page.
- **Touch targets are at least 34px**, which is the height of every control in the top bar.
- **Not tested:** no screen reader has been run against the site, and no automated accessibility audit runs in CI. Contrast is the only enforced dimension.

---

## 10. Motion

Deliberately minimal. Transitions are 150 to 200ms and are limited to colour, border colour, opacity and the drawer's `transform`.

| Element | Transition |
|---|---|
| Links, cards, buttons | `border-color` or `color`, 150ms |
| `.topbar-cta`, `.btn-link` | `opacity`, 150ms |
| Drawer | `transform`, 200ms ease |
| Anchors | `scroll-behavior: smooth` on `html` |

**No `prefers-reduced-motion` block exists.** The smooth scroll in particular ignores that preference, which is a real gap and the one motion defect worth fixing. Everything else is a colour fade under 200ms and is unlikely to trouble anyone.

Nothing animates in front of the score.

---

## 11. Responsive behaviour

Breakpoints, from `cfc.css`:

| Width | What changes |
|---|---|
| **Above 1180px** | Full three-column shell |
| **1180px** | `.toc` hidden; shell drops to sidebar plus article |
| **900px** | Single column. `.nav-toggle` appears, `.topbar-search` hides, `.sidebar` becomes a drawer, `.compare` / `.card-grid` / `.pagination` go single-column, the footer drops to two columns, `h1` and `h2` step down |
| **560px** | Top bar padding tightens, wordmark to .9375rem, footer to one column |

Application pages use Tailwind's own breakpoints inside a 720px container, which is a second, differently-placed set. Unifying them is part of M14.

**The hard rule:** nothing may scroll horizontally at 360px. Wide content scrolls inside its own container (`.table-wrap`), never the page. This is asserted by `tools/check-live.py` on every page it loads, at 1280px today; a 360px assertion would be a worthwhile addition.

A `@media print` block hides the top bar, sidebar, table of contents, pagination and footer, and collapses the shell to a block.

---

## 12. Iconography and assets

- **Icons are inline SVG**, 24x24 viewBox, `stroke="currentColor"`, `stroke-width="2"`, `fill="none"`, sized by CSS (14 to 20px). No icon font and no icon library.
- **Every decorative icon carries `aria-hidden="true"`.** An icon that conveys meaning gets a label on its control instead.
- **`favicon.svg` is at the repository root**, not in a `public/` directory, because there is no build step and nothing to copy. (An earlier version of this document gave the path as `public/favicon.svg`, which is a Next.js convention from an application that was deleted in M5.5.)
- **PWA icons** live in `assets/icons/` at 192px, 512px and a maskable variant, referenced from `manifest.webmanifest`.
- **`theme-color` is `#C2410C`** on every page, matching the light accent.
- **No Open Graph image exists.** A link to any page shares with no preview card.

---

## 13. Not built

Recorded so that nobody reads a specification as a description. Each of these appeared in an earlier version of this document, some marked "planned" and some not marked at all.

| Item | Status |
|---|---|
| Score reveal count-up animation | Not built. Would conflict with "nothing animates in front of the score" and is unlikely ever to be built |
| Ingredient row expansion | **The chevron is rendered and does nothing.** Either build the panel or remove the affordance; a control that does not respond is worse than no control |
| Route transition fades | Not built. Full page navigations, so there is nothing to transition |
| Skeleton loaders | Not built. Pages show a "Loading" line, which `tools/check-live.py` waits on |
| Tier glyphs distinguishing additive tiers without colour | Not built. Tiers currently carry text labels, which satisfies the accessibility requirement, so this is a refinement rather than a gap |
| Open Graph image | Not built |
| Shared button component | Not built. Blocked on M14 |
| `prefers-reduced-motion` support | Not built |
| A disabled scan button with a tooltip | **Obsolete, not pending.** The scanner shipped in M8. There is no disabled button and no `role="tooltip"` anywhere in the codebase |
