# Design Document

**Product:** Cat Food Center
**Scope:** Visual language, design tokens, mobile-first layout, and UX flows.
**Companion docs:** [`PRD.md`](PRD.md) (behavior), [`TRD.md`](TRD.md) (implementation).

---

## 1. Design philosophy

Verdict first, editorial feel, mobile as the canvas. An owner in a store aisle should grasp the score in one glance, then drill down if they want. The visual language is calm, magazine-like, and confident — trustworthy because it looks considered, not because it shouts.

## 2. Color palette

All tokens are defined in `app/globals.css` as CSS custom properties and in `tailwind.config.ts` as Tailwind color extensions.

| Token | Hex | Tailwind class | Use |
|---|---|---|---|
| `--bg` | `#FAF7F2` | `bg-bg` | Page background (warm paper) |
| `--surface` | `#FFFFFF` | `bg-surface` | Cards and elevated surfaces |
| `--ink` | `#1C1A17` | `text-ink` | Primary text |
| `--ink-soft` | `#56504A` | `text-ink-soft` | Secondary text, captions, metadata |
| `--accent` | `#C2410C` | `bg-accent` / `text-accent` | Links, primary buttons, focus rings |
| `--hairline` | `#E7E1D8` | `border-hairline` | Dividers and borders |
| `--band-excellent` | `#1B7A4B` | `bg-band-excellent` | Score band: Excellent (75–100) |
| `--band-good` | `#5FA855` | `bg-band-good` | Score band: Good (50–74) |
| `--band-poor` | `#E08A1E` | `bg-band-poor` | Score band: Poor (25–49) |
| `--band-bad` | `#C0392B` | `bg-band-bad` | Score band: Bad (0–24) |

Band colors are reserved strictly for ratings. They do not appear in navigation, decoration, or other UI contexts. Each band is also communicated by a text label and an icon, never by color alone.

A dark theme mirrors these tokens with an ink-dark background and warm off-white text at adjusted lightness values. Band colors remain perceptually distinguishable for common color-vision deficiencies.

## 3. Typography

Font families are loaded via `next/font/google` in `app/layout.tsx` and exposed as CSS variables.

| Variable | Font | Tailwind class | Role |
|---|---|---|---|
| `--font-display` | Fraunces | `font-display` | Wordmark, score number, section headings |
| `--font-body` | Public Sans | `font-body` | Ingredients, labels, UI text, body copy |

Fraunces is a variable optical-size serif that carries the editorial voice. Public Sans is a humanist sans optimized for legibility at small sizes. Tabular figures (`tabular-nums`) are used on score numbers and nutrition values.

Type scale (defined in `tailwind.config.ts`):

| Token | Size | Line height | Tailwind class | Use |
|---|---|---|---|---|
| `display` | 3rem | 1.1 | `text-display` | The CFC Score number |
| `h1` | 1.75rem | 1.2 | `text-h1` | Product name |
| `h2` | 1.25rem | 1.3 | `text-h2` | Section titles |
| `body` | 1rem | 1.5 | `text-body` | Default text |
| `small` | 0.875rem | 1.5 | `text-small` | Captions, sources, footer |
| `micro` | 0.75rem | 1.4 | `text-micro` | Metadata, "last reviewed" dates |

## 4. Spacing system

Base unit is **4px**. All spacing uses the default Tailwind scale (multiples of 4px via `p-1`, `gap-2`, etc.). Common values in use:

| Step | px | Use |
|---|---|---|
| 1 | 4 | Tight internal padding |
| 2 | 8 | Icon-to-label gap |
| 3 | 12 | Compact row padding |
| 4 | 16 | Standard side gutters, row padding |
| 6 | 24 | Between sections within a card |
| 8 | 32 | Between major page sections |
| 12 | 48 | Between large top-level blocks |

## 5. Breakpoints

The default Tailwind breakpoint scale applies. The design is single-column on mobile; the max content width is 720px (`max-w-content`) centered on larger screens.

| Breakpoint | Width | What changes |
|---|---|---|
| (default) | 0px+ | Single column, 16px side gutters, full-width controls |
| `sm` | 640px+ | No major layout changes; minor padding adjustments |
| `md` | 768px+ | Content constrained to `max-w-content` (720px) centered |
| `lg`+ | 1024px+ | No further layout changes; the 720px cap holds |

The header is `fixed` on mobile (stays on screen while scrolling) and `sticky` on desktop.

## 6. Component patterns

### Buttons

- **Primary action (e.g. Search, Scan):** `bg-accent text-white rounded-card px-5 py-3`. Hover: `opacity-90`. Focus: `ring-2 ring-accent ring-offset-2`.
- **Pill button (e.g. Support):** `bg-accent text-white rounded-pill px-4 py-2 text-small`. Same hover/focus.
- **Disabled:** `opacity-60 cursor-not-allowed` applied directly; `aria-disabled="true"` on the element.

### Cards

- Background: `bg-surface`, border: `border border-hairline`, radius: `rounded-card` (12px).
- Hover state for clickable cards: `hover:border-accent transition-colors`.
- Focus state: `focus:ring-2 focus:ring-accent`.
- Shadow: `shadow-sm` used sparingly on elevated surfaces like the score header card.

### Score badge

- Square tile: `w-14 h-14 rounded-card` with the band background color.
- Score number in `font-display text-h2 text-white tabular-nums leading-none`.
- Band label as a pill below or beside: `text-micro text-white rounded-pill px-2 py-0.5` with band background.

### Forms

- Input: `border border-hairline rounded-card px-4 py-3 text-body bg-surface`. Focus: `ring-2 ring-accent outline-none`.
- Placeholder text: `text-ink-soft`.
- Search form uses `role="search"` on the `<form>` element.

### Lists

- Product lists: `<ul role="list">` with `<li>` items wrapping `<Link>` cards.
- Ingredient lists: `<ol>` with numbered items inside a bordered container (`rounded-card border border-hairline divide-y divide-hairline`).
- Additive tier groups: labeled with a colored dot (`w-2 h-2 rounded-full`) plus tier text.

## 7. Accessibility standards

- Target: **WCAG AA** across light and dark themes.
- Color contrast: all text combinations meet the 4.5:1 ratio. `ink` on `bg` and `surface` exceed it comfortably.
- Band meaning is never conveyed by color alone — every band has a text label (`Excellent`, `Good`, `Poor`, `Bad`) and an icon glyph.
- Focus rings: visible `ring-2 ring-accent` on all interactive elements; `focus:outline-none` is only used when a custom ring replaces the default outline.
- Tap targets: minimum 44×44px for all interactive elements.
- ARIA: `role="search"` on search forms, `aria-label` on score badges, `aria-hidden="true"` on decorative SVGs, `role="tooltip"` and `aria-describedby` on the disabled Scan button.
- Keyboard navigation: all flows operable without a mouse.

## 8. Iconography and band glyphs

Each band uses an inline SVG glyph so the verdict reads without color:

| Band | Glyph | SVG path used |
|---|---|---|
| Excellent / Good | Checkmark | `M5 13l4 4L19 7` |
| Poor | Caution (planned) | — |
| Bad | Octagon slash (planned) | — |

Additive tiers use a small colored dot (`w-2 h-2 rounded-full`) plus a tier label ("Tier 2 — Moderate Risk"). Tier-specific glyphs are planned.

Navigation uses a `chevron-right` SVG (`M9 5l7 7-7 7`) as a directional hint on list items.

## 9. Animation and motion

Restraint over spectacle.

- **Score reveal:** the number counts up briefly and the band bar fills on first load of a product page (planned).
- **Ingredient expand:** smooth height transition when expanding a plain-language explanation (planned).
- **Route transitions:** quick eased fades (~150–200ms) between routes.
- **Tooltips:** `transition-opacity` on the Scan button tooltip.
- **All motion:** respects `prefers-reduced-motion`. Non-essential animations are disabled when the media query is set.
- **Hover/focus feedback:** `transition-colors` and `transition-opacity` on interactive elements for instant tactile feedback.

## 10. Key screens

### Global chrome

**Header** (all screens): sticky/fixed top bar with `bg-surface border-b border-hairline`. Left: wordmark in `font-display text-h2` linking to `/`. Right: Support pill button in `bg-accent`.

**Footer** (all screens): `border-t border-hairline py-6 text-center`. Contains "Built by [Azqato]" in `text-small text-ink-soft`.

### Home (`/`)

Wordmark and tagline centered at top. Large circular Scan button as the primary CTA (disabled with tooltip in MVP). Search form below. Recently viewed product cards at the bottom.

### Search (`/search`)

Search bar at the top (pre-filled with the `?q=` param). Result list of product cards with score badge, name, brand, and band label.

### Product detail (`/product/[barcode]`)

1. **Score header card:** band color bar at top, score number in `text-display`, band label + check icon, product image placeholder, product name in `text-h1`, brand/format/life stage metadata.
2. **Verdict section:** one-sentence verdict, reason chips as bordered pills.
3. **Warning banner (conditional):** shown when a hard gate fires or the food is not AAFCO complete.
4. **Ingredients:** numbered ordered list; chevron on each row (expand planned).
5. **Additive flags:** tier heading with dot, then cards per additive with function badge, health impact text, and source link.
6. **Nutrition snapshot:** 2×2 grid of stat cards (Crude Protein DM, Crude Fat DM, Moisture as-fed, Taurine presence).
7. **AAFCO adequacy:** quoted statement in italics with substantiation method.
8. **Footer metadata:** data completeness + last reviewed date.

### Empty, loading, and error states

- **Loading:** skeleton placeholders shaped like the score header and list (planned).
- **Not found:** prompt to submit barcode and a label photo (planned).
- **Partial data:** note explaining which inputs were missing (planned).
- **No camera / permission denied:** redirect to search with a one-line explanation (planned).

## 11. Tone of voice

Clear, warm, and factual. Plain language over jargon. Never alarmist, never preachy. We inform; the owner decides.

## 12. Assets

- `public/favicon.svg`: current app icon.
- App icon and maskable PWA icon set (planned).
- Open Graph image for shared product links (planned).
- Band and tier glyphs as inline SVG (partially implemented; full set planned).
