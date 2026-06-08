# Design Document

**Product:** Cat Food Center
**Scope:** Visual language, design tokens, mobile-first layout, and UX flows.
**Companion docs:** `PRD.md` (behavior), `TRD.md` (implementation).

---

## 1. Design principles

* **Verdict first.** The score is the hero. An owner in an aisle should grasp the result in one glance, then drill down if they want.
* **Editorial, not clinical.** A calm, intelligent, magazine-like feel: confident typography, generous whitespace, restrained color. Trust comes from looking considered, not from looking like a lab report or a loud consumer app.
* **Mobile is the canvas.** Thumb-reachable controls, single-column reading, large tap targets. Desktop is an enhancement, never the primary design.
* **Honest signals.** Color reinforces meaning but never carries it alone. Every band has a label and an icon.

## 2. Aesthetic direction

Refined editorial. Think the quiet authority of a well-set reference page rather than a gamified tracker. A near-paper background, ink-dark text, one warm accent, and the four rating colors used sparingly and only where they mean something. The result should feel trustworthy, literate, and a little bit beautiful.

## 3. Typography

Distinctive, paired for contrast. Avoid generic system fonts.

* **Display / headings:** a characterful serif (for example Fraunces or Newsreader) for the wordmark, scores, and section titles. This carries the editorial voice.
* **Body / UI:** a clean, highly legible humanist sans (for example Söhne, or as an open fallback, Public Sans) for ingredients, labels, and controls.
* **Numerals:** tabular figures for the score and nutrition values so columns align.

Type scale (mobile, rem):

| Token | Size | Use |
| --- | --- | --- |
| display | 3.0 | The score number |
| h1 | 1.75 | Product name |
| h2 | 1.25 | Section titles |
| body | 1.0 | Default text |
| small | 0.875 | Captions, sources |
| micro | 0.75 | Metadata, last reviewed |

## 4. Color system

Neutral, paper-like base with ink text and a single warm accent. Rating colors are reserved strictly for ratings.

```
--bg:        #FAF7F2;  /* warm paper */
--surface:   #FFFFFF;  /* cards */
--ink:       #1C1A17;  /* primary text */
--ink-soft:  #56504A;  /* secondary text */
--accent:    #C2410C;  /* warm terracotta, links and primary actions */
--hairline:  #E7E1D8;  /* dividers */

/* Rating bands */
--band-excellent: #1B7A4B;  /* dark green */
--band-good:      #5FA855;  /* light green */
--band-poor:      #E08A1E;  /* orange */
--band-bad:       #C0392B;  /* red */
```

A dark theme mirrors these with an ink background, warm off-white text, and the same four band colors at adjusted lightness. Band colors are chosen to remain distinguishable for common color-vision deficiencies; pair each with an icon.

## 5. Iconography and band glyphs

Each band gets a glyph so the verdict reads without color:

* Excellent: filled check inside a circle
* Good: check
* Poor: caution chevron
* Bad: octagon with a slash

Additive tiers use the same logic: a small colored dot plus a tier label (High, Moderate, Low).

## 6. Layout system

* **Grid:** single column on mobile with 16px side gutters; max content width about 720px on larger screens, centered.
* **Spacing scale (px):** 4, 8, 12, 16, 24, 32, 48.
* **Radius:** 12px on cards, 999px on pills and the primary scan button.
* **Elevation:** subtle. One soft shadow level for cards; rely on hairlines and spacing rather than heavy drop shadows.

## 7. Key screens

### 7.0 Global chrome

**Header (present on all screens)**
* Fixed to the top of the viewport on mobile; sticky on desktop.
* Left: the wordmark in the display serif (links to `/`).
* Right: a **Support** button (pill style, accent color) that links to `https://azqato.github.io/support.html`.
* Minimal height; does not compete with page content.

**Footer (present on all screens)**
* Simple single-row footer at the bottom of every page.
* Contains the text "Built by [Azqato](https://azqato.github.io/index.html)" in the `small` type size, ink-soft color, centered.
* Separated from content by a hairline rule.

### 7.1 Home
* Wordmark in the display serif with the tagline beneath.
* A large, thumb-friendly circular **Scan** button as the primary action.
* A search field directly below for the no-camera path.
* A short strip of recently viewed products.

### 7.2 Scanner
* Full-bleed camera viewfinder with a centered alignment frame.
* Minimal chrome: a close control and a "type it instead" link.
* On a successful read, a brief haptic-style confirmation, then transition to the product page.

### 7.3 Product page (the centerpiece)
* **Score header:** the score number in the display serif, the band label, the band color as a slim bar or ring, the product image, brand, and format.
* **Verdict line:** one sentence, plus the top one to three reasons as chips.
* **Warning banner (conditional):** if a hard gate fires (for example propylene glycol) or the food is not complete and balanced, a prominent banner appears directly under the header.
* **Ingredients:** an ordered, readable list; tap any item to expand a plain-language explanation.
* **Additive flags:** grouped by tier, each card showing function, health impact, and a cited source link.
* **Nutrition snapshot:** protein, fat, moisture, and taurine presence, on a dry-matter basis where possible, with tabular figures.
* **AAFCO statement:** life stage and substantiation method.
* **Alternatives:** shown when the score is Poor or Bad, matched to the same format.
* **Footer metadata:** data completeness indicator and a "last reviewed" date.

### 7.4 Compare
* Two or three sticky column headers (score and image), with aligned rows for nutrition and flagged additives so differences pop.

### 7.5 Methodology
* A clean, readable long-form page mirroring `PRD.md`, so the scoring is never a black box.

## 8. Motion

Restraint over spectacle. One well-orchestrated moment matters more than scattered effects.

* **Score reveal:** the number counts up briefly and the band bar fills, on first load of a product page.
* **Ingredient expand:** a smooth height transition.
* **Transitions:** quick, eased fades between routes (about 150 to 200ms). Respect `prefers-reduced-motion` and disable non-essential motion when set.

## 9. Empty, loading, and error states

* **Loading:** skeleton placeholders shaped like the score header and list, not a spinner.
* **Not found:** a friendly prompt to submit the barcode and a label photo.
* **Partial data:** a clear, non-alarming note explaining which inputs were missing and that the score reflects available data.
* **No camera / permission denied:** graceful redirect to search with a one-line explanation.

## 10. Accessibility

* WCAG AA contrast across light and dark themes.
* Band meaning conveyed by label and glyph, not color alone.
* Logical focus order, visible focus rings, and a keyboard path through every flow.
* Tap targets at least 44 by 44px.

## 11. Tone of voice

Clear, warm, and factual. Plain language over jargon (say "synthetic preservative linked to organ concerns in studies," not a bare chemical name). Never alarmist, never preachy. We inform; the owner decides.

## 12. Assets

* App icon and maskable PWA icon set.
* Open Graph image for shared product links.
* A small set of band and tier glyphs as inline SVG.
