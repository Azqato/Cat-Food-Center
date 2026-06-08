# Technical Requirements Document (TRD)

**Product:** Cat Food Center
**Scope:** Architecture, data model, scoring implementation, and engineering requirements for v1.
**Companion docs:** `PRD.md` (what to build), `DESIGN.md` (how it looks).

---

## 0. MVP strategy

The first deployable version is a static placeholder that runs on GitHub Pages with no backend. It uses Next.js (App Router) with `output: 'export'` so the build produces pure HTML/CSS/JS with no server required. All product data is hardcoded mock data. The file and component structure mirrors the full product so that replacing mock data with real API calls and enabling server features is a matter of filling in logic, not restructuring the project.

What the MVP includes: global layout (header, footer), home page, one hardcoded product page (full visual), search page (UI only, no live results). What it defers: real Open Pet Food Facts API calls, barcode scanner, service worker, compare page, submit flow, scoring engine tests.

## 1. Architecture overview

Cat Food Center is a Next.js (App Router) Progressive Web App written in TypeScript and styled with Tailwind CSS. It is mobile-first, installable, and works in any modern desktop browser. The build targets static and edge-friendly output so it can deploy to Vercel or a GitHub Pages compatible pipeline.

```
Client (PWA)
  - Next.js App Router (React, TypeScript)
  - Tailwind CSS
  - Camera barcode scanner (BarcodeDetector API, ZXing fallback)
  - Service worker (offline cache: viewed products + additive KB)
        |
        v
Data layer
  - Product catalog: Open Pet Food Facts API
  - Internal Additive Knowledge Base (versioned JSON)
  - Internal Nutrient Reference (AAFCO feline profiles, versioned JSON)
  - Scoring engine (pure TypeScript module, runs client-side)
```

The scoring engine is a pure, deterministic TypeScript module. The same input always yields the same score, and it can run client-side or in a build step.

## 2. Technology requirements

* **Language:** TypeScript, strict mode on.
* **Framework:** Next.js (App Router).
* **Styling:** Tailwind CSS with a tokenized theme (see `DESIGN.md`).
* **State:** React server components for data fetching; lightweight client state (React hooks) for scan/compare UI.
* **PWA:** web app manifest, service worker, offline caching strategy (stale-while-revalidate for catalog reads, cache-first for the additive KB).
* **Testing:** unit tests for the scoring engine (high coverage required), component tests for key flows.
* **Lint/format:** ESLint plus Prettier; CI fails on lint errors.

## 3. Barcode scanning

* **Primary:** the native BarcodeDetector API where supported (reads EAN-13, EAN-8, UPC-A, UPC-E).
* **Fallback:** ZXing (@zxing/library) for browsers without BarcodeDetector.
* **Permissions:** request camera only on user action; if denied or unavailable, route to search with a clear message.
* **Performance:** decode on a throttled frame loop; show a live viewfinder with an alignment guide.

## 4. Data sources

### 4.1 Open Pet Food Facts (primary catalog)
* Look up by barcode and by text search.
* Fields consumed: product name, brand, image, ingredients text, nutrition facts, and any additive tags.
* **Reality check:** completeness varies by product. The app must degrade gracefully when ingredients or nutrition are missing, and must clearly mark partial data.

### 4.2 Internal Additive Knowledge Base (KB)
* Versioned JSON, the heart of Pillar B. Each entry is keyed by canonical additive name with alias matching (so "BHA" and "butylated hydroxyanisole" map to one record).
* Each record stores: name, aliases, function, risk tier (1 to 3), a plain-language health impact for cats, and one or more sources.

### 4.3 Internal Nutrient Reference
* Versioned JSON encoding AAFCO feline nutrient profiles by life stage (Growth and Reproduction, Adult Maintenance, All Life Stages), with minimums and any maximums for crude protein, key amino acids (including taurine and arginine), crude fat (including arachidonic acid), and core vitamins and minerals.

## 5. Data model (TypeScript shapes)

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
type Format = "wet" | "dry" | "semi-moist" | "treat" | "unknown";

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
  aafcoComplete: boolean;          // complete and balanced for lifeStage
  substantiation?: "feeding-trial" | "formulation" | "unknown";
  ingredients: string[];           // ordered, as listed on label
  nutrition: NutritionFacts;
  dataCompleteness: "full" | "partial";
  lastReviewed: string;            // ISO date
}

interface PillarScores {
  nutrition: number;   // 0 to 100 (pre-weight)
  additives: number;   // 0 to 100 (pre-weight)
  transparency: number;// 0 to 100 (pre-weight)
}

interface ScoreResult {
  score: number;                 // 0 to 100, final
  band: "excellent" | "good" | "poor" | "bad";
  pillars: PillarScores;
  flaggedAdditives: AdditiveRecord[];
  hardGates: string[];           // human-readable gate reasons
  reasons: string[];             // top drivers of the score
  warnings: string[];            // e.g. not complete and balanced
}
```

## 6. Scoring engine specification

The engine is pure and deterministic. Pipeline:

1. **Normalize input.** Parse the ingredients text into an ordered array; convert nutrition to a dry-matter basis where moisture is known.
2. **Match additives.** For each ingredient, resolve against the additive KB using alias matching; collect `flaggedAdditives`.
3. **Score Pillar A (nutrition, 0 to 100).** Combine animal-protein dominance, nutrient sufficiency versus the AAFCO profile for `lifeStage` (taurine weighted heavily), carbohydrate/filler load, a moisture bonus for wet formats, and an adequacy/substantiation factor.
4. **Score Pillar B (additives, 0 to 100).** Start at 100; subtract per-tier penalties for Tier 2 additives; Tier 3 presence forces this pillar low and arms the hard cap.
5. **Score Pillar C (transparency, 0 to 100).** Reward named ingredients, sourcing disclosure, and a clean recall history.
6. **Weight and combine:** `0.55*A + 0.35*B + 0.10*C`.
7. **Apply hard gates:**
   * If propylene glycol is present, set band to Bad and cap the score in the 0 to 24 range; add a gate reason.
   * If any Tier 3 additive is present, cap the final score at 49.
   * If `aafcoComplete` is false and `format` is not `treat`, push a warning (does not by itself cap, but is surfaced prominently).
8. **Assign band** from the final score (75 to 100 Excellent, 50 to 74 Good, 25 to 49 Poor, 0 to 24 Bad).
9. **Build reasons and warnings** for display.

All weights, tier penalties, and thresholds live in a single `scoring.config.ts` so the model can be tuned without touching logic. Every change to that file must be reflected in `PRD.md` and logged in `PATCHNOTES.md`.

## 7. Handling missing data

* If ingredients are missing, Pillar A nutrient scoring runs on whatever is present and the product is marked `partial`; the page states which inputs were unavailable.
* The engine never fabricates values. Unknown fields are treated as unknown, not as zero or pass.
* Partial-data products display a reduced-confidence indicator.

## 8. Routing and pages (App Router)

**Global layout** (`app/layout.tsx`): wraps every route with a shared `<Header>` and `<Footer>`.
* Header contains the wordmark (links to `/`) and a Support link (`https://azqato.github.io/support.html`) styled as a pill button.
* Footer contains "Built by [Azqato](https://azqato.github.io/index.html)" in small ink-soft text, centered.

* `/` home: scan button plus search.
* `/scan` camera scanner.
* `/search` results.
* `/product/[barcode]` product detail and score.
* `/compare` side-by-side.
* `/methodology` the public, always-current scoring explanation (must match `PRD.md`).
* `/submit/[barcode]` add a missing product to the review queue.

## 9. Performance and offline

* Target Largest Contentful Paint under 2.5s on a mid-range phone over 4G.
* Cache the additive KB and Nutrient Reference for offline use.
* Cache viewed product pages (stale-while-revalidate).

## 10. Privacy and security

* No account required in v1; no personal data collected.
* Camera frames are processed on-device and never uploaded.
* All network calls over HTTPS; respect Open Pet Food Facts usage terms and attribute the source.

## 11. Accessibility (engineering)

* Semantic HTML, focus management on route changes, keyboard-operable scanner fallback.
* Band communicated by label and icon, not color alone.
* Meet WCAG AA contrast (validated in CI where feasible).

## 12. Testing strategy

* **Scoring engine:** golden-file tests covering each band, each hard gate, partial data, and the worked example in `PRD.md`. This suite must stay green.
* **Additive matching:** alias-resolution tests (for example "color added" maps to the artificial-dye record).
* **Flows:** scan success, scan fallback to search, product not found, compare.

## 13. Build and deployment

* `npm run build` produces a deployable PWA.
* CI runs lint, type-check, and tests on every push.
* Deploy target is static/edge friendly (Vercel or a GitHub Pages compatible export).

## 14. Future technical work

* EU/FEDIAF nutrient profiles and non-US barcode support.
* A lightweight backend for crowd-submitted products and editorial review.
* Image-based label OCR to fill gaps when Open Pet Food Facts lacks ingredients.

## 15. References

* AAFCO: https://www.aafco.org
* FDA Center for Veterinary Medicine: https://www.fda.gov/animal-veterinary
* Open Pet Food Facts: https://world.openpetfoodfacts.org
* BarcodeDetector API (MDN): https://developer.mozilla.org/en-US/docs/Web/API/BarcodeDetector
