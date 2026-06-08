# Roadmap

---

## Current phase: MVP — Static shell with mock data

The Next.js app is live on GitHub Pages. All three core pages (home, search, product detail) are built with a complete UI but mock data. The goal of this phase is to validate the design, routing, and deployment pipeline before wiring in real data.

---

## Milestone table

| Milestone | Target | Status |
|---|---|---|
| M0: Project scaffold | 2026-06-07 | Complete |
| M1: MVP static shell | 2026-06-07 | Complete |
| M2: Documentation audit | 2026-06-08 | Complete |
| M3: Data layer — Open Pet Food Facts | 2026-07 | Planned |
| M4: Scoring engine | 2026-07 | Planned |
| M5: Barcode scanner | 2026-08 | Planned |
| M6: Service worker / PWA offline | 2026-08 | Planned |
| M7: Methodology page | 2026-08 | Planned |
| M8: Not-found / submit flow | 2026-09 | Planned |
| M9: Compare page | 2026-09 | Planned |
| M10: Public beta | 2026-10 | Planned |

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

### M3: Data layer — Open Pet Food Facts
- Fetch product by barcode from the Open Pet Food Facts API
- Text search via the Open Pet Food Facts search endpoint
- Parse and normalize API response into the `Product` TypeScript shape
- Graceful degradation for missing fields (partial-data indicator)
- Replace all mock data in `product/[barcode]/page.tsx` and `SearchView.tsx`

### M4: Scoring engine
- Implement the pure TypeScript scoring module (`scoring.config.ts` for weights and thresholds)
- Pillar A: nutrition scoring (animal protein, taurine, carb load, moisture, AAFCO adequacy)
- Pillar B: additive matching with the Additive Knowledge Base JSON
- Pillar C: transparency scoring
- Hard gate logic: propylene glycol cap, Tier 3 additive cap
- Golden-file unit tests covering all bands, hard gates, and the worked example from PRD §6.7
- Replace hardcoded scores with live engine output

### M5: Barcode scanner
- Implement BarcodeDetector API with ZXing (@zxing/library) fallback
- Live camera viewfinder with alignment guide
- Permission request on user action with graceful fallback to search
- Throttled frame loop for decode performance
- `/scan` route

### M6: Service worker / PWA offline
- Web app manifest
- Service worker with stale-while-revalidate for product pages
- Cache-first strategy for the Additive KB and Nutrient Reference JSON
- Offline indicator when serving from cache

### M7: Methodology page
- `/methodology` route
- Rendered from `PRD.md` §6 (or a derived MDX page)
- Always reachable from the footer

### M8: Not-found / submit flow
- 404 state when a barcode is not in the Open Pet Food Facts catalog
- `/submit/[barcode]` route: form to submit barcode + ingredient label photo
- Review queue (initially manual email/form; backend later)

### M9: Compare page
- `/compare` route
- Two or three sticky column headers (score + image)
- Aligned rows for nutrition values and additive flags
- Highlight differences

### M10: Public beta
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
| Dark theme | Design is specified; deferred until post-beta to keep scope tight |
