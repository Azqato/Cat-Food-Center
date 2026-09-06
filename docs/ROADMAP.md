# Roadmap

---

## Current phase: MVP — Static shell with mock data, plus the Cat Care Guide

The site is live on GitHub Pages. The three core pages (home, search, product detail) are built with a complete UI but mock data, and the methodology page is written. The Cat Care Guide — an eleven-page educational resource — is complete and is the first part of the site backed by real, sourced content rather than mock data.

Next up is dark mode (M5), then wiring the product pages to the Open Pet Food Facts API (M6) and the scoring engine (M7).

---

## Milestone table

| Milestone | Target | Status |
|---|---|---|
| M0: Project scaffold | 2026-06-07 | Complete |
| M1: MVP static shell | 2026-06-07 | Complete |
| M2: Documentation audit | 2026-06-08 | Complete |
| M3: Methodology page | 2026-06-08 | Complete |
| M4: Cat Care Guide (educational resource) | 2026-09-05 | Complete |
| M5: Dark mode with persisted preference | 2026-09 | Planned |
| M6: Data layer — Open Pet Food Facts | 2026-10 | Planned |
| M7: Scoring engine | 2026-10 | Planned |
| M8: Barcode scanner | 2026-11 | Planned |
| M9: Service worker / PWA offline | 2026-11 | Planned |
| M10: Not-found / submit flow | 2026-12 | Planned |
| M11: Compare page | 2026-12 | Planned |
| M12: Public beta | 2027-01 | Planned |

---

## Feature breakdown per milestone

### M0: Project scaffold (Complete)
- Next.js 14 App Router with TypeScript
- Tailwind CSS with design token theme
- GitHub Actions deploy pipeline to GitHub Pages
- ESLint configuration

### M1: MVP static shell (Complete)
- Global layout: Header (wordmark + Support button), Footer (Azqato link)
- Home page: search form, disabled Scan button, recently viewed section (mock)
- Search page: search bar, mock result list
- Product detail page: full mock product with score, verdict, ingredients, additives, nutrition snapshot, AAFCO adequacy

### M2: Documentation audit (Complete)
- Full `/docs` suite: PRD, TRD, DESIGN, PATCHNOTES, PRFAQ, TENETS, METRICS, ROADMAP, SECURITY, RUNBOOK
- README rewritten for developers

### M3: Methodology page (Complete)
- `/methodology` route
- Rendered from `PRD.md` §6 (or a derived MDX page)
- Always reachable from the footer

### M4: Cat Care Guide — educational resource (Complete)
- Eleven-page documentation section at `/learn.html` and `/learn-*.html`
- Documentation shell: fixed top bar, grouped sidebar, article column, "on this page" scroll-spy rail, prev/next pagination, four-column site footer
- Content: nutrition fundamentals, the complete AAFCO daily nutrient requirement (all 42 nutrients with worked per-day amounts), label reading, food formats, hydration, a tiered additive reference, feeding practice, life stages, toxic foods and hazards, and diet in common conditions
- Shared assets in `/assets` (`cfc.css`, `cfc-docs.js`, `cfc-tailwind.js`)
- Pages generated from `tools/learn/` so the shared chrome cannot drift between them

### M5: Dark mode with persisted preference
- Add a dark palette as a second set of values for the CSS custom properties already defined on `:root` in `assets/cfc.css` — no per-component rewrites needed
- Theme toggle control in the top bar (and in the header of the non-Learn pages), cycling light → dark → system
- Persist the choice in `localStorage` under a single key (e.g. `cfc-theme`) so it survives reloads and is remembered across visits
- Honour `prefers-color-scheme` when no explicit choice has been stored
- Apply the stored theme via a small inline script in `<head>`, before first paint, to avoid a flash of the wrong theme
- Re-check WCAG AA contrast for both palettes, including the four score bands and the callout accents
- Set `color-scheme` so form controls and scrollbars follow the theme

### M6: Data layer — Open Pet Food Facts
- Fetch product by barcode from the Open Pet Food Facts API
- Text search via the Open Pet Food Facts search endpoint
- Parse and normalize API response into the `Product` TypeScript shape
- Graceful degradation for missing fields (partial-data indicator)
- Replace all mock data in `product/[barcode]/page.tsx` and `SearchView.tsx`

### M7: Scoring engine
- Implement the pure TypeScript scoring module (`scoring.config.ts` for weights and thresholds)
- Pillar A: nutrition scoring (animal protein, taurine, carb load, moisture, AAFCO adequacy)
- Pillar B: additive matching with the Additive Knowledge Base JSON
- Pillar C: transparency scoring
- Hard gate logic: propylene glycol cap, Tier 3 additive cap
- Golden-file unit tests covering all bands, hard gates, and the worked example from PRD §6.7
- Replace hardcoded scores with live engine output

### M8: Barcode scanner
- Implement BarcodeDetector API with ZXing (@zxing/library) fallback
- Live camera viewfinder with alignment guide
- Permission request on user action with graceful fallback to search
- Throttled frame loop for decode performance
- `/scan` route

### M9: Service worker / PWA offline
- Web app manifest
- Service worker with stale-while-revalidate for product pages
- Cache-first strategy for the Additive KB and Nutrient Reference JSON
- Offline indicator when serving from cache

### M10: Not-found / submit flow
- 404 state when a barcode is not in the Open Pet Food Facts catalog
- `/submit/[barcode]` route: form to submit barcode + ingredient label photo
- Review queue (initially manual email/form; backend later)

### M11: Compare page
- `/compare` route
- Two or three sticky column headers (score + image)
- Aligned rows for nutrition values and additive flags
- Highlight differences

### M12: Public beta
- Lighthouse CI passing Core Web Vitals targets (LCP ≤ 2.5 s, CLS ≤ 0.1)
- WCAG AA contrast validated
- Top-100 SKU catalog coverage ≥ 80%
- Analytics instrumented (Plausible or equivalent)

---

## Explicitly deferred items

| Feature | Reason deferred |
|---|---|
| Dog food | Requires a separate scoring engine; cats first to ship a correct product before a broad one |
| User accounts | No user data in v1; adds infrastructure complexity with no v1 value |
| User-generated reviews | Trust risk; editorial and algorithmic scoring ships first |
| Personalized diet plans | Out of scope per PRD — we inform, not prescribe |
| E-commerce / affiliate links | Conflicts with the trust model; deferred indefinitely |
| Backend API | Not needed until submit queue or crowd-sourced data requires it |
| EU/FEDIAF nutrient profiles | US AAFCO first; EU localization is a separate compliance effort |
| Treat-specific scoring rubric | Treats are not complete diets; requires a different scoring model |
| Dark theme | No longer deferred — promoted to M5, with a toggle and a `localStorage`-persisted preference |
