# Technical Requirements Document (TRD)

**Product:** Cat Food Center
**Scope:** Architecture, data model, scoring implementation, and engineering requirements for v1.
**Companion docs:** [`PRD.md`](PRD.md) (what to build), [`DESIGN.md`](DESIGN.md) (how it looks).

---

## 0. Current implementation state (v0.2.0)

The project is a Next.js 14 App Router application built as a fully static export (`output: 'export'`), deployed to GitHub Pages. All pages are live with mock data. The real data integrations (Open Pet Food Facts API, scoring engine, barcode scanner, service worker) are deferred to the next phase.

What is implemented:
- Global layout: sticky header (wordmark + Support button), footer (Built by Azqato)
- Home page: search form, disabled Scan button with "coming soon" state, recently viewed section (mock data)
- Search page: search bar, mock result list with score badges
- Product detail page: score header, verdict, ingredient list, additive flags with cited sources, nutrition snapshot (dry-matter basis), AAFCO adequacy section, footer metadata
- GitHub Actions CI/CD for automatic deploy on push to `main`

What is deferred:
- Open Pet Food Facts API integration
- Scoring engine (TypeScript module)
- Barcode scanner (BarcodeDetector / ZXing)
- Service worker and offline caching
- Compare page
- Submit-missing-product flow
- Methodology page

## 1. Architecture overview

```
Client (PWA)
  - Next.js App Router (React, TypeScript)
  - Tailwind CSS
  - Camera barcode scanner (BarcodeDetector API, ZXing fallback)  [deferred]
  - Service worker (offline cache: viewed products + additive KB)  [deferred]
        |
        v
Data layer
  - Product catalog: Open Pet Food Facts API                       [deferred]
  - Internal Additive Knowledge Base (versioned JSON)              [deferred]
  - Internal Nutrient Reference (AAFCO feline profiles, JSON)      [deferred]
  - Scoring engine (pure TypeScript module, client-side)           [deferred]
```

The scoring engine will be a pure, deterministic TypeScript module. The same input always yields the same score, and it can run client-side or in a build step.

## 2. Technology requirements

| Tool | Version | Purpose |
|---|---|---|
| Next.js | 14.2.x | App Router, static export |
| React | 18.x | UI rendering |
| TypeScript | 5.x | Strict-mode types throughout |
| Tailwind CSS | 3.4.x | Design token-based styling |
| Fraunces | Google Fonts | Display / heading serif |
| Public Sans | Google Fonts | Body / UI sans-serif |
| ESLint | 8.x | Linting (CI fails on errors) |
| GitHub Actions | — | CI/CD and GitHub Pages deployment |

Additional libraries (deferred until the relevant feature ships):
- `@zxing/library` — ZXing barcode scanning fallback
- Service worker tooling (Workbox or custom)

## 3. Folder structure

```
Cat-Food-Center/
├── app/
│   ├── globals.css          # Tailwind base + CSS custom properties
│   ├── layout.tsx           # Root layout: Header, Footer, font variables
│   ├── page.tsx             # Home page (search + recently viewed)
│   ├── product/
│   │   └── [barcode]/
│   │       └── page.tsx     # Product detail page (mock data)
│   └── search/
│       ├── page.tsx         # Search page shell (Suspense boundary)
│       └── SearchView.tsx   # Client component: search bar + results (mock data)
├── components/
│   ├── Header.tsx           # Sticky header: wordmark + Support pill
│   └── Footer.tsx           # Footer: Built by Azqato
├── public/
│   ├── favicon.svg
│   └── .nojekyll            # Prevents GitHub Pages from ignoring _ directories
├── docs/                    # All project documentation
├── .github/
│   └── workflows/
│       └── deploy.yml       # Build and deploy to GitHub Pages on push to main
├── next.config.ts           # Static export, basePath, assetPrefix for GitHub Pages
├── tailwind.config.ts       # Design token theme
├── tsconfig.json
├── postcss.config.mjs
├── .eslintrc.json
└── package.json
```

## 4. Data models (TypeScript shapes)

These types define the full contract for the scoring engine and product data. They are not yet wired to live data but the UI is structured around them.

```ts
type RiskTier = 1 | 2 | 3; // 1 low/none, 2 moderate, 3 high

interface AdditiveRecord {
  id: string;
  name: string;
  aliases: string[];
  function: string;          // e.g. "synthetic preservative"
  tier: RiskTier;
  healthImpact: string;      // plain-language, cat-specific
  sources: Source[];
}

interface Source {
  label: string;             // e.g. "FDA CVM"
  url: string;
}

type LifeStage = "growth" | "adult" | "all" | "unknown";
type Format    = "wet" | "dry" | "semi-moist" | "treat" | "unknown";

interface NutritionFacts {
  crudeProteinPct?: number;  // as-fed; engine converts to dry matter
  crudeFatPct?: number;
  moisturePct?: number;
  taurinePresent?: boolean;
  ashPct?: number;
}

interface Product {
  barcode: string;
  name: string;
  brand?: string;
  imageUrl?: string;
  format: Format;
  lifeStage: LifeStage;
  aafcoComplete: boolean;
  substantiation?: "feeding-trial" | "formulation" | "unknown";
  ingredients: string[];     // ordered, as listed on label
  nutrition: NutritionFacts;
  dataCompleteness: "full" | "partial";
  lastReviewed: string;      // ISO date
}

interface PillarScores {
  nutrition: number;    // 0–100 pre-weight
  additives: number;    // 0–100 pre-weight
  transparency: number; // 0–100 pre-weight
}

interface ScoreResult {
  score: number;                   // 0–100 final
  band: "excellent" | "good" | "poor" | "bad";
  pillars: PillarScores;
  flaggedAdditives: AdditiveRecord[];
  hardGates: string[];             // human-readable gate reasons
  reasons: string[];               // top drivers of the score
  warnings: string[];              // e.g. not complete and balanced
}
```

## 5. API design

The MVP is entirely static with no network calls. When the data layer ships, the following flows will be implemented:

| Flow | Source | Notes |
|---|---|---|
| Barcode lookup | `GET https://world.openpetfoodfacts.org/api/v0/product/{barcode}.json` | Fields: product_name, brands, image_url, ingredients_text, nutriments, additives_tags |
| Text search | `GET https://world.openpetfoodfacts.org/cgi/search.pl?search_terms={q}&json=1` | Filtered to pet food category |
| Additive KB | Bundled versioned JSON | Loaded once, cached for offline use |
| Nutrient reference | Bundled versioned JSON | AAFCO feline profiles by life stage |
| Scoring | Pure TS module, runs client-side | No network call; deterministic |

All network calls are over HTTPS. Open Pet Food Facts is attributed as required by their terms.

Error states:
- Product not found (404 from OPFF): route to the submit flow
- Network unavailable: serve from service worker cache; show "offline, showing cached data"
- Partial data (missing ingredients or nutrition): score on available fields; show data-completeness indicator

## 6. Scoring engine specification

The engine is pure and deterministic. Pipeline:

1. **Normalize input.** Parse the ingredients text into an ordered array; convert nutrition to a dry-matter basis where moisture is known.
2. **Match additives.** For each ingredient, resolve against the additive KB using alias matching; collect `flaggedAdditives`.
3. **Score Pillar A (nutrition, 0–100).** Combine animal-protein dominance, nutrient sufficiency vs the AAFCO profile for `lifeStage` (taurine weighted heavily), carbohydrate/filler load, a moisture bonus for wet formats, and an adequacy/substantiation factor.
4. **Score Pillar B (additives, 0–100).** Start at 100; subtract per-tier penalties for Tier 2 additives; Tier 3 presence forces this pillar low and arms the hard cap.
5. **Score Pillar C (transparency, 0–100).** Reward named ingredients, sourcing disclosure, and a clean recall history.
6. **Weight and combine:** `0.55 × A + 0.35 × B + 0.10 × C`.
7. **Apply hard gates:**
   - If propylene glycol is present, set band to Bad, cap score 0–24.
   - If any Tier 3 additive is present, cap score at 49.
   - If `aafcoComplete` is false and `format` is not `treat`, push a warning.
8. **Assign band** from the final score (75–100 Excellent, 50–74 Good, 25–49 Poor, 0–24 Bad).
9. **Build reasons and warnings** for display.

All weights, tier penalties, and thresholds live in a single `scoring.config.ts` so the model can be tuned without touching logic. Every change to that file must be reflected in `PRD.md` and logged in `PATCHNOTES.md`.

## 7. Handling missing data

- If ingredients are missing, Pillar A nutrient scoring runs on whatever is present and the product is marked `partial`; the page states which inputs were unavailable.
- The engine never fabricates values. Unknown fields are treated as unknown, not as zero or pass.
- Partial-data products display a reduced-confidence indicator.

## 8. Routing and pages (App Router)

| Route | Status | Description |
|---|---|---|
| `/` | Built (mock) | Home: search form, disabled Scan, recently viewed |
| `/search` | Built (mock) | Search results list |
| `/product/[barcode]` | Built (mock) | Product detail and score |
| `/scan` | Deferred | Camera barcode scanner |
| `/compare` | Deferred | Side-by-side product comparison |
| `/methodology` | Deferred | Public scoring explanation (mirrors PRD §6) |
| `/submit/[barcode]` | Deferred | Submit a missing product |

Global layout (`app/layout.tsx`): every route is wrapped with `<Header>` and `<Footer>`.

- **Header:** sticky top, wordmark linking to `/`, Support pill button linking to `https://azqato.github.io/support.html`.
- **Footer:** centered "Built by [Azqato](https://azqato.github.io/index.html)" in small ink-soft text.

## 9. Performance and offline

- Target Largest Contentful Paint under 2.5 s on a mid-range phone over 4G.
- Cache the additive KB and Nutrient Reference for offline use (deferred with service worker).
- Cache viewed product pages stale-while-revalidate (deferred).

## 10. Privacy and security

- No account required in v1; no personal data collected.
- Camera frames are processed on-device and never uploaded.
- All network calls over HTTPS.
- Open Pet Food Facts attributed per their terms.

## 11. Accessibility

- Semantic HTML, focus management on route changes, keyboard-operable scanner fallback.
- Band communicated by label and icon, not color alone.
- WCAG AA contrast (validated in CI where feasible).

## 12. Testing strategy

- **Scoring engine:** golden-file tests covering each band, each hard gate, partial data, and the worked example in `PRD.md §6.7`. Suite must stay green.
- **Additive matching:** alias-resolution tests (e.g. "color added" maps to the artificial-dye record).
- **Flows:** scan success, scan fallback to search, product not found, compare.

## 13. Build and deployment

```bash
npm run build          # outputs to out/
```

CI (`.github/workflows/deploy.yml`) runs on every push to `main`:
1. `actions/checkout@v4`
2. `npm ci`
3. `npm run build`
4. `actions/upload-pages-artifact@v3` — uploads `out/`
5. `actions/deploy-pages@v4` — deploys to GitHub Pages

The `basePath` and `assetPrefix` are both set to `/Cat-Food-Center` in `next.config.ts`. If the repo is renamed, update both values there.

## 14. Known technical debt

| Area | Shortcut taken | Correct solution |
|---|---|---|
| Product data | All hardcoded mock objects | Replace with Open Pet Food Facts API calls |
| Search | Returns the same mock list regardless of query | Wire real text-search API |
| Barcode scanner | Button disabled with "coming soon" tooltip | Implement BarcodeDetector / ZXing |
| Scoring | No engine; scores are hardcoded in mock data | Implement the TypeScript scoring module |
| Offline | No service worker | Add Workbox or custom SW |
| Recently viewed | Hardcoded mock array | Read from localStorage |
| Ingredient expand | Chevron rendered but non-interactive | Add expandable explanation panel |

## 15. Future technical work

- EU/FEDIAF nutrient profiles and non-US barcode support.
- Lightweight backend for crowd-submitted products and editorial review.
- Image-based label OCR to fill gaps when Open Pet Food Facts lacks ingredients.

## 16. References

- AAFCO: https://www.aafco.org
- FDA Center for Veterinary Medicine: https://www.fda.gov/animal-veterinary
- Open Pet Food Facts: https://world.openpetfoodfacts.org
- BarcodeDetector API (MDN): https://developer.mozilla.org/en-US/docs/Web/API/BarcodeDetector
