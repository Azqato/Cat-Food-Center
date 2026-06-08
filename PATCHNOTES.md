# Patch Notes

Running changelog for Cat Food Center. Add an entry to the top for every meaningful change. Keep `PRD.md` in sync whenever product behavior or the scoring model changes.

Format: newest first. Use semantic-ish version tags (major.minor.patch). Pre-launch work lives under 0.x.

---

## [0.4.0] - 2026-06-07

**Rebuilt as plain HTML/CSS/JS — no build step, runs directly in any browser.**

Changed
* Replaced the Next.js build-required deliverable with three self-contained HTML pages that work by opening a file in a browser or being served on GitHub Pages with no compilation step.
* `.github/workflows/deploy.yml`: removed all build steps (`npm ci`, `npm run build`). The workflow now uploads the repo root directly as the Pages artifact. No Node.js required.

Added
* `index.html`: home page — wordmark, disabled Scan button with tooltip, search form (GET to `search.html`), two hardcoded recently-viewed product cards. Tailwind CDN + custom CSS + Google Fonts (Fraunces, Public Sans). Zero JavaScript dependencies beyond the Tailwind CDN.
* `search.html`: search results — search bar pre-filled from `?q=` URL param (vanilla JS `URLSearchParams`), three hardcoded mock result cards linking to `product.html`. No server needed.
* `product.html`: full product page — score header (61, Good band, green bar), verdict + reason chips, 24-item ingredient list, two Tier 2 additive cards (Carrageenan, Guar Gum) with cited sources, 2×2 nutrition grid, AAFCO statement, footer metadata. Barcode shown from `?barcode=` param.
* `favicon.svg`: 😻 emoji SVG at repo root (GitHub Pages serves this correctly).
* `.nojekyll`: at repo root — prevents GitHub Pages from running Jekyll on the repo.

Architecture note
* The `app/`, `components/`, `next.config.ts`, `package.json`, etc. remain in the repo as the future Next.js migration path. They do not affect GitHub Pages serving. When transitioning to the full product, scaffold the Next.js build, add build steps back to the workflow, and retire the HTML pages.

---

## [0.3.0] - 2026-06-07

**MVP complete: GitHub Pages deployment config.**

Added
* `next.config.ts`: set `basePath` and `assetPrefix` to `/Cat-Food-Center` for deployment at `https://azqato.github.io/Cat-Food-Center/`. Both values are derived from a single `REPO` constant at the top of the file — change it there if the repo name changes.

Confirmed present (from earlier prompts)
* `public/.nojekyll`: prevents GitHub Pages from running Jekyll on the `out/` directory.
* `.gitignore`: `out/` excluded from version control; the built output is deployed separately.

Deployment steps (run after `npm install` with Node.js LTS installed)
1. `npm run build` → produces `out/`
2. Push `out/` contents to the `gh-pages` branch of `https://github.com/Azqato/Cat-Food-Center.git`, or configure a GitHub Actions workflow to do so on push to `main`.
3. In repo Settings → Pages, set source to the `gh-pages` branch, root (`/`).

Build verification
* Node.js was not present on the development machine during this session; `npm run build` could not be confirmed. Run it manually after installing Node.js LTS from nodejs.org. Expected output: a clean `out/` directory with `index.html`, `search/`, `product/0000000000000/`, `product/0000000000001/`, `product/0000000000002/`, and all static assets.

---

**MVP summary (prompts 1–4, versions 0.2.0–0.3.0)**

| What | Where |
| --- | --- |
| Next.js 14 scaffold, TypeScript strict, Tailwind CSS | `package.json`, `tsconfig.json`, `tailwind.config.ts` |
| Design tokens (colors, type scale, radius, max-width) | `tailwind.config.ts`, `app/globals.css` |
| Fraunces + Public Sans via `next/font/google` | `app/layout.tsx` |
| Global header (wordmark + Support button) | `components/Header.tsx` |
| Global footer ("Built by Azqato") | `components/Footer.tsx` |
| 😻 emoji favicon | `public/favicon.svg`, `app/layout.tsx` |
| Home page (scan button, search form, recently-viewed cards) | `app/page.tsx` |
| Mock product page (full visual per `DESIGN.md` §7.3) | `app/product/[barcode]/page.tsx` |
| Search page (pre-filled input, 3 mock result cards) | `app/search/page.tsx`, `app/search/SearchView.tsx` |
| Static export + GitHub Pages config | `next.config.ts` (`basePath`, `assetPrefix`) |
| `.nojekyll`, `out/` gitignore | `public/.nojekyll`, `.gitignore` |

---

## [0.2.2] - 2026-06-07

**Prompt 3: Mock product page, search page, emoji favicon.**

Added
* `app/product/[barcode]/page.tsx`: full product page layout per `DESIGN.md` section 7.3, populated with hardcoded mock data (Instinct Original Grain-Free with Real Chicken, score 61, Good band). Sections rendered:
  * Score header — 6px band-good color bar, 3rem score number, check glyph + band label, product image placeholder, product name (h1), brand / format / life-stage meta.
  * Verdict — one-sentence summary and three reason chips as pills.
  * Ingredients — numbered ordered list of 24 ingredients with a chevron hint; expand logic deferred (TODO comment).
  * Additive flags — Tier 2 Moderate Risk section with two cards (Carrageenan, Guar Gum), each showing function badge, health impact, and a cited source link.
  * Nutrition snapshot — 2×2 grid: Crude Protein 52% DM, Crude Fat 28% DM, Moisture 78% as-fed, Taurine Present (with check glyph). Tabular figures throughout.
  * AAFCO adequacy — quoted statement + substantiation method.
  * Footer metadata — data-completeness indicator and last-reviewed date.
* `app/search/SearchView.tsx` (`'use client'`): search input pre-filled from `?q=` param; on submit navigates to `/search?q=`; displays three hardcoded result cards (Instinct Chicken / Salmon / Duck variants, all score ~60, Good band) each linking to `/product/0000000000000`.
* `app/search/page.tsx`: rewritten as a server component that wraps `SearchView` in `<Suspense>` (required by Next.js static export when `useSearchParams` is used).
* `public/favicon.svg`: 😻 emoji as an SVG favicon.
* `app/layout.tsx`: wired `favicon.svg` via `metadata.icons`.

---

## [0.2.1] - 2026-06-07

**Prompt 2: Home page.**

Added
* `app/page.tsx`: full home page layout per `DESIGN.md` section 7.1.
  * Wordmark (`<h1>`) in Fraunces display serif with tagline.
  * 128px circular Scan button in accent color — disabled state with opacity, `cursor-not-allowed`, and a CSS tooltip ("Coming soon") on hover. Accessible via `aria-disabled` and `aria-describedby`.
  * Search form (`role="search"`) — text input + Submit button; on submit, navigates to `/search?q=<query>` via `useRouter`.
  * "Recently viewed" section with two hardcoded mock product cards: Weruva Paw Lickin' Chicken (score 81, Excellent) and Friskies Surfin' & Turfin' Favorites (score 28, Poor). Each card shows the score badge in band color, product name, brand, band pill, and a chevron.
* `app/product/[barcode]/page.tsx`: added mock barcodes `0000000000001` and `0000000000002` to `generateStaticParams` so the static export generates pages the recently-viewed links point to.

---

## [0.2.0] - 2026-06-07

**Prompt 1: Project scaffold, design tokens, global layout.**

Added
* `package.json`: Next.js 14, React 18, Tailwind CSS 3, TypeScript 5.
* `tsconfig.json`: strict mode, App Router moduleResolution.
* `next.config.ts`: `output: 'export'`, `trailingSlash`, `images.unoptimized` — static GitHub Pages build. `basePath`/`assetPrefix` left as TODO for Prompt 4.
* `tailwind.config.ts`: all design tokens from `DESIGN.md` wired as Tailwind theme extensions — colors (`bg`, `surface`, `ink`, `ink-soft`, `accent`, `hairline`, four band colors), font families (`font-display` → Fraunces, `font-body` → Public Sans), type scale (`text-display` through `text-micro`), border radius (`rounded-card`, `rounded-pill`), max-width (`max-w-content`).
* `postcss.config.mjs`: Tailwind + autoprefixer.
* `.eslintrc.json`: `next/core-web-vitals`.
* `.gitignore`: ignores `out/`, `.next/`, `node_modules/`, `next-env.d.ts`.
* `app/globals.css`: Tailwind directives plus `:root` CSS custom properties for all design tokens.
* `app/layout.tsx`: loads Fraunces (`--font-display`) and Public Sans (`--font-body`) via `next/font/google`; mounts `<Header>` and `<Footer>` around a flex-column `<body>`.
* `components/Header.tsx`: sticky header — wordmark in display serif linking to `/`, Support pill button linking to `https://azqato.github.io/support.html`.
* `components/Footer.tsx`: "Built by Azqato" centered footer with link to `https://azqato.github.io/index.html`.
* `app/page.tsx`, `app/search/page.tsx`, `app/product/[barcode]/page.tsx`: build-passing stubs; product route includes `generateStaticParams` required by static export.
* `public/.nojekyll`: prevents GitHub Pages Jekyll processing.

Next up
* Install Node.js (not present on dev machine), run `npm install`, verify `npm run build` produces a clean `out/`.
* Prompt 2: home page with scan button, search input, recently-viewed strip.
* Prompt 3: mock product page (full visual) and mock search results.
* Prompt 4: GitHub Pages `basePath`/`assetPrefix` config and final PATCHNOTES entry.

---

## [0.1.1] - 2026-06-07

**Documentation updates: global chrome and MVP strategy.**

Changed
* `DESIGN.md`: added section 7.0 defining a persistent header (wordmark + Support button linking to `https://azqato.github.io/support.html`) and footer ("Built by Azqato" linking to `https://azqato.github.io/index.html`) present on all screens.
* `PRD.md`: added section 4.1 capturing the header/footer as product requirements.
* `TRD.md`: added section 0 (MVP strategy) — static Next.js export targeting GitHub Pages with hardcoded mock data first, real API wiring later. Updated section 8 global layout spec.
* `README.md`: updated status to reflect MVP-first approach.
* `PATCHNOTES.md`: this entry.

---

## [0.1.0] - 2026-06-07

**Project kickoff: foundational documentation.**

Added
* `README.md`: project overview, feature summary, tech stack, quick start.
* `PRD.md`: living spec, including the full CFC Score rating methodology (three pillars, additive risk tiers, hard gates, score bands, worked example).
* `TRD.md`: architecture, TypeScript data model, scoring-engine pipeline, data sources, testing strategy.
* `DESIGN.md`: editorial visual language, design tokens, typography, color and band system, screen specs, accessibility.
* `PATCHNOTES.md`: this changelog.

Decisions captured
* Cats are obligate carnivores, so the rating engine is purpose-built for feline nutrition and does not use human scoring systems such as Nutri-Score.
* Scoring weights set to Nutrition 55%, Additives 35%, Transparency 10%.
* High-risk (Tier 3) additives cap the score at 49; propylene glycol triggers an automatic Bad band because it is FDA-prohibited in cat food.
* Primary product data source is Open Pet Food Facts, supplemented by an internal additive knowledge base and an AAFCO feline nutrient reference.
* Stack: Next.js (App Router) plus TypeScript plus Tailwind CSS, delivered as a mobile-first installable PWA with browser support.

Next up
* Scaffold the Next.js PWA and Tailwind theme tokens from `DESIGN.md`.
* Build the deterministic scoring engine and its golden-file test suite.
* Seed the additive knowledge base (Tier 1 to Tier 3 entries with sources).
* Wire the barcode scanner (BarcodeDetector with ZXing fallback) and Open Pet Food Facts lookup.

---

<!-- Template for new entries:

## [x.y.z] - YYYY-MM-DD

Added
*

Changed
*

Fixed
*

-->
