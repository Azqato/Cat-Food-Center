# Patch Notes

All notable changes to Cat Food Center are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/). Versions follow [Semantic Versioning](https://semver.org/).

---

## v0.9.0 — 2026-09-05

### Added
- **A page for products that are not in the database.** It checks the barcode for a typo and re-queries first — a mistyped digit looks exactly like a missing product — then explains which two panels to photograph and links the contribution straight to Open Pet Food Facts with the barcode filled in.

### Notes
- Contributions go to the open database the scores are derived from, not to a queue of ours. That way a product added once works here, in every other tool built on the same data, and for the next person who scans the same tin.

---

## v0.8.0 — 2026-09-05

### Added
- **Works offline.** A product you have already opened stays readable with no connection, and the app installs to a home screen. Pages you have never opened show a page explaining what still works, rather than the browser's error screen.
- An offline banner, and a notice on any product page that is being shown from a saved copy — including when it was saved.

### Notes
- A cached score is always labelled as one. The scoring engine and the database both change, so an old score shown as current would be wrong in exactly the way this project exists to avoid.

---

## v0.7.0 — 2026-09-05

### Added
- **Barcode scanning.** Point the camera at the packaging and the product page opens. Decoding happens on the device; only the barcode number is sent anywhere. Uses the platform's `BarcodeDetector` where available and downloads ZXing only where it is not.
- Manual barcode entry alongside the camera, always available and checksum-validated before it navigates.
- **Recently viewed**, kept on the device in `localStorage`. No account, no sync, and a Clear button.
- A `Scan` entry in the top navigation.

### Changed
- The home page Scan button now works. It was disabled with a "Coming soon" tooltip.

### Removed
- The two invented "Recently viewed" products. The section stays hidden until there is something real in it.

---

## v0.6.0 — 2026-09-05

### Added
- **Live product scoring.** `assets/js/opff.js` fetches and normalises Open Pet Food Facts records; `assets/js/scoring.js` derives the CFC Score from them. Both run in the browser, with no build step and no server.
- `assets/data/additives.json` — the additive knowledge base: 20 entries across three risk tiers, plus three catch-all label terms, each with sources.
- Real `product.html` and `search.html`, replacing the mock markup.
- A 130-assertion test suite (`tests.html`), run headlessly by `tools/run-tests.py`.
- `docs/DATA-COVERAGE.md` — a measured survey of what the database actually holds.
- A "What the score cannot see" section on the methodology page.

### Fixed
- **Non-English labels were scored as clean.** The alias matcher was English-only, and only 9.5% of records carry English ingredients, so on most labels it matched nothing — and reported that silence as an absence of problems. A French product with unnamed meat by-products and added sugar scored 77 / Excellent. Aliases now cover six languages, and a label outside that set is explicitly reported as unchecked rather than clean, with confidence capped. See `docs/DATA-COVERAGE.md`.
- The Tier 0 "named by-products" credit was awarded to *unnamed* by-products, contradicting the transparency pillar on the same words.
- A parenthetical naming 4% beef could make an unnamed meat entry score as a named animal protein.

---

## v0.5.0 — 2026-09-05

### Added
- **Dark mode with a persisted preference.** A three-state control — system, light, dark — in the top bar of every page. The choice is stored under the `localStorage` key `cfc-theme`; `system` stores nothing and defers to `prefers-color-scheme`. Open tabs stay in step via a `storage` listener.
- `assets/cfc-tokens.css` — the palette extracted from `cfc.css` so that both page families share it: the Tailwind CDN pages and the generated guide pages.
- `assets/cfc-theme.js` — theme application and persistence. Loaded synchronously in `<head>` so the stored theme applies before first paint.
- `tools/check-contrast.py` — WCAG AA audit of every foreground/background pair in both palettes.
- `docs/ADR-001-static-first.md` — the decision that the site is static HTML by design, what that enables (the barcode scanner needs no server), and what it forecloses.

### Changed
- Tailwind colour names map to CSS variables rather than hex literals, so utility classes follow the theme without `dark:` variants. Opacity modifiers cannot be used on those colours as a result.
- The green and amber score chips now use dark ink instead of white. They failed AA at 2.8:1 and 2.3:1 in the light theme; this is an accessibility fix, and it changes how the light theme looks.
- `README.md`, `TRD.md`, `RUNBOOK.md` and `DESIGN.md` now describe the static stack that actually ships rather than the Next.js application that did not.

### Removed
- The unused Next.js 14 application and its toolchain. It was never built or deployed; `deploy.yml` has always served the repository root directly.

### Verified
- All 38 token pairs pass WCAG AA in both palettes.
- Chromium check across all fifteen pages: the theme applies, the toggle cycles, the choice survives a reload with no flash, and no console errors.

---

## v0.4.0 — 2026-09-05

### Added
- **The Cat Care Guide** — an eleven-page educational resource at `/learn.html` and `/learn-*.html`, grounded in the AAFCO nutrient profiles, NRC research, FDA and EFSA guidance, WSAVA's nutrition toolkit, and the peer-reviewed veterinary literature. Every page carries a sources list.
  - `learn.html` — overview, the five rules, and the guide map
  - `learn-nutrition.html` — obligate carnivore metabolism; protein, fat, carbohydrate and fibre; the eight nutrients cats cannot synthesise
  - `learn-daily-requirements.html` — the complete AAFCO cat food nutrient profile (all 42 nutrients with growth minimums, adult minimums and maximums), the RER/MER calorie formulas, and a worked conversion into exact grams and milligrams per day for a 4.5 kg cat
  - `learn-labels.html` — AAFCO adequacy statements, the dry-matter conversion, carbohydrate by difference, ingredient splitting, the 95/25/3 naming rules, and the marketing terms with no regulatory meaning
  - `learn-food-types.html` — seven formats compared, including the current FDA position on H5N1 in raw pet food
  - `learn-hydration.html` — water requirements by body weight, dehydration checks, and eleven ways to increase intake
  - `learn-additives.html` — a three-tier additive reference covering 30+ compounds with the regulatory position and evidence for each, plus the commonly criticised ingredients that are not actually a problem
  - `learn-feeding.html` — calorie tables by body weight, portioning, meal timing, transitions, treats, weight management, and multi-cat feeding
  - `learn-life-stages.html` — weaning through geriatric, including the post-neutering weight gain window and why senior cats need more protein, not less
  - `learn-toxic.html` — toxic foods, plants (lilies flagged as a same-hour emergency), medications and household hazards, with poison-line numbers and first-ten-minutes steps
  - `learn-health.html` — diet in obesity, CKD, FLUTD, diabetes, hyperthyroidism, IBD, food allergy, hepatic lipidosis, dental disease and constipation
- Documentation-site layout for the guide: fixed top bar with product search, grouped sticky sidebar, article column, "on this page" scroll-spy rail, prev/next pagination, and a four-column site footer
- Shared front-end assets in `/assets`: `cfc.css` (design tokens and the documentation shell), `cfc-docs.js` (mobile navigation drawer and scroll spy), `cfc-tailwind.js` (Tailwind CDN theme extracted from the inline page configs)
- `tools/learn/` static generator so the eleven pages share one shell and cannot drift apart; generated output is committed, so deployment still needs no build step
- "Learn" entry in the main navigation on the home, search, product and methodology pages
- Cat Care Guide entry card on the home page

### Changed
- Main navigation now scrolls horizontally on narrow viewports rather than overflowing, since it carries a fourth item
- `docs/ROADMAP.md` renumbered into true chronological order; the Cat Care Guide recorded as complete, and dark mode promoted out of the deferred list into a planned milestone (M5) with a toggle and a `localStorage`-persisted preference
- README documents the guide, the generator workflow, and the shared assets

### Notes
- The guide is educational content and is not veterinary advice; every page says so, and the pages covering disease and toxicity say so prominently.

---

## v0.3.0 — 2026-06-08

### Added
- Full documentation suite: PRD, TRD, DESIGN, PATCHNOTES, PRFAQ, TENETS, METRICS, ROADMAP, SECURITY, RUNBOOK
- `/docs` directory consolidating all project documentation
- README.md rewritten for developer audience with install, dev, build, and deploy instructions

### Changed
- PRD.md, TRD.md, DESIGN.md moved from project root into `/docs`
- TRD.md updated to reflect actual current implementation state (mock data, deferred features catalogued in known technical debt table)
- DESIGN.md updated with precise Tailwind token references, accessibility ARIA patterns, and component implementation details

---

## v0.2.0 — 2026-06-07

### Added
- Next.js 14 App Router with TypeScript and static export configured for GitHub Pages (`basePath: /Cat-Food-Center`)
- Tailwind CSS with full design token theme: colors (`bg`, `surface`, `ink`, `ink-soft`, `accent`, `hairline`, four band colors), typography scale (`display`, `h1`, `h2`, `body`, `small`, `micro`), border radius (`card`, `pill`), max-width (`content`)
- Fraunces (display serif) and Public Sans (body sans) loaded via `next/font/google`
- Global layout (`app/layout.tsx`): sticky header with wordmark and Support pill button linking to `https://azqato.github.io/support.html`; footer with Azqato link
- Home page (`app/page.tsx`): wordmark, tagline, disabled Scan button with "coming soon" tooltip, search form routing to `/search`, recently viewed section with two mock product cards and score badges
- Search page (`app/search/`): search bar pre-filled from `?q=` param, mock result list of three products with score badges and band labels
- Product detail page (`app/product/[barcode]/page.tsx`): score header with band color bar and checkmark glyph, verdict section with reason chips, numbered ingredient list, additive flags section with tier dot and cited source links, 2×2 nutrition snapshot grid (dry-matter basis), AAFCO adequacy quote, footer metadata row with data completeness and last reviewed date
- GitHub Actions workflow (`.github/workflows/deploy.yml`): builds with `npm ci && npm run build` and deploys `out/` to GitHub Pages on every push to `main`
- `public/.nojekyll` to prevent GitHub Pages from ignoring underscore-prefixed directories

### Changed
- Replaced earlier plain HTML/CSS/JS implementation with Next.js App Router static export

---

## v0.1.0 — 2026-06-07

### Added
- Initial Next.js App Router scaffold with TypeScript, Tailwind CSS, ESLint, and PostCSS
- `next.config.ts` with `output: 'export'`, `trailingSlash: true`, `basePath`, and `assetPrefix` for GitHub Pages
- `PRD.md`, `TRD.md`, `DESIGN.md` specification documents
- `.gitattributes` and `.gitignore`
