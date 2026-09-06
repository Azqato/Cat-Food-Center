# Roadmap

---

## Current phase: MVP — from mock data to a working product

The site is live on GitHub Pages. The Cat Care Guide (M4) and the theme system (M5) are done, and [ADR-001](./ADR-001-static-first.md) settled the architecture question that was blocking everything after them: the site is static HTML by decision, not by default, and the unused Next.js application has been removed.

The mock data is gone. `search.html` and `product.html` now run on live Open Pet Food Facts records scored by a real engine (M6, M7), which is the point at which this stopped being a shell and became a product.

Two things learned in building them shape everything after:

- **The database is thinner than the PRD assumed.** About a fifth of products carry enough data to score all three pillars. Partial data is the normal path, and the engine refuses to score rather than guessing. See [DATA-COVERAGE.md](./DATA-COVERAGE.md).
- **The database is not English.** Only 9.5% of records carry English ingredients, and an English-only matcher reported the rest as clean. Any text check added from here is a language check too.

The barcode scanner (M8) is done — the feature ADR-001 was written to make sure static hosting could still support, and it needed no server, as predicted. So is offline support (M9): the app installs, and a product already looked at stays readable with no signal.

So is the not-found / submit flow (M10). Next is the compare page (M11).

---

## Milestone table

| Milestone | Target | Status |
|---|---|---|
| M0: Project scaffold | 2026-06-07 | Complete |
| M1: MVP static shell | 2026-06-07 | Complete |
| M2: Documentation audit | 2026-06-08 | Complete |
| M3: Methodology page | 2026-06-08 | Complete |
| M4: Cat Care Guide (educational resource) | 2026-09-05 | Complete |
| M5: Dark mode with persisted preference | 2026-09-05 | Complete |
| M5.5: Architecture decision + Next.js removal | 2026-09-05 | Complete |
| M6: Data layer — Open Pet Food Facts | 2026-09-05 | Complete |
| M7: Scoring engine | 2026-09-05 | Complete |
| M8: Barcode scanner | 2026-09-05 | Complete |
| M9: Service worker / PWA offline | 2026-09-05 | Complete |
| M10: Not-found / submit flow | 2026-09-05 | Complete |
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

### M5: Dark mode with persisted preference (Complete)
- `assets/cfc-tokens.css` — the palette, extracted from `cfc.css` so that **both** page families share it: the Tailwind CDN pages and the generated Learn pages
- Dark values supplied twice, once for `:root[data-theme="dark"]` and once under `prefers-color-scheme` for visitors who have expressed no preference; `tools/check-contrast.py` fails the build if the two lists drift apart
- `assets/cfc-theme.js` — loaded **synchronously in `<head>`** so the stored theme applies before first paint, with no flash. Cycles system → light → dark; persists under `localStorage` key `cfc-theme`; `system` stores nothing and lets the media query take over
- Theme toggle in the top bar of all fifteen pages; a `storage` listener keeps other open tabs in step
- `color-scheme` set on both palettes so form controls and scrollbars follow the theme
- Tailwind colour names now resolve to CSS variables rather than hex literals, so `bg-surface` and `text-ink` follow the theme with no `dark:` variants in the markup. **Constraint:** Tailwind opacity modifiers (`bg-surface/50`) cannot be used on these colours — add a token instead
- WCAG AA verified across 38 foreground/background pairs in both palettes by `tools/check-contrast.py`
- **Light-theme appearance changed as part of this:** the "good" (green) and "poor" (amber) chips previously used white text at 2.8:1 and 2.3:1. They now use dark ink. This was an accessibility defect that dark mode surfaced rather than caused

### M5.5: Architecture decision and Next.js removal (Complete)
- [ADR-001](./ADR-001-static-first.md) records static HTML as the target architecture rather than an interim state, with the reasoning for each planned feature and — importantly — the list of things static hosting genuinely cannot do, each with its escape hatch
- Confirmed the barcode scanner (M8) is fully client-side and needs no server: `getUserMedia` + `BarcodeDetector` (ZXing WASM fallback) + a keyless CORS-enabled API. The only hard requirement is HTTPS, which GitHub Pages provides
- Deleted the unused Next.js application (`app/`, `components/`, `next.config.ts`, `tailwind.config.ts`, `postcss.config.mjs`, `tsconfig.json`, `.eslintrc.json`, `package.json`) — it was never built and never deployed, and `README.md` described it as the stack, which was wrong about what users actually load

### M6: Data layer — Open Pet Food Facts — Complete 2026-09-05
- Barcode lookup and text search against the v2 API, keyless and CORS-enabled, straight from the browser
- `assets/js/opff.js` normalises a raw record into the `Product` shape in TRD §4
- Reads both nutriment schemas and records which was used; rejects implausible figures; corrects per-kilogram energy values
- Partial data handled as the normal case rather than an error — `normalize` never throws for missing fields
- Mock data removed from `product.html` and `search.html`

### M7: Scoring engine — Complete 2026-09-05
- `assets/js/scoring.js`: pure, deterministic, no network and no DOM
- All three pillars, both hard gates, weights renormalised across the pillars that could be computed, `scorable: false` where too little is known
- 130 assertions in `tests.html`, run headlessly by `tools/run-tests.py` — a browser-hosted suite, because ADR-001 rules out a build step
- `tools/check-live.py` renders four page states against the live API

**What was not in the plan and had to be:** the plan assumed English labels. Only 9.5% of records are. The matcher's silence on the other 90% was being reported as a clean bill of health, and a French product with unnamed meat by-products and added sugar scored 77/Excellent. Aliases now cover six languages, and a label outside that set is stated as unchecked rather than clean. See [DATA-COVERAGE.md](./DATA-COVERAGE.md) — the write-up covers three further defects that the English-only matcher had been hiding.

### M8: Barcode scanner — Complete 2026-09-05
- `scan.html` and `assets/js/scanner.js`: `BarcodeDetector` where the platform has it, ZXing downloaded on demand where it does not
- Live viewfinder with a reticle; camera starts only on a click, and is released on stop, on tab-hide and on navigation
- Every failure mode gets its own sentence — declined permission, no camera, camera busy, no HTTPS — because "could not start camera" would be accurate and useless
- Manual barcode entry alongside, not beneath: on a desktop browser it is the primary path
- EAN-13 / EAN-8 / UPC-A / UPC-E, checksum-validated before navigating

**Two things worth recording.** UPC-E has its own checksum rule — it must be expanded to UPC-A before it can be checked — and validating it as if it were EAN-8 would have made the scanner appear to simply never see small US packages, with no error anywhere. And the secure-context requirement means `http://<LAN-IP>` has no camera at all, so testing from a phone on the local network fails in a way that looks like broken code; the page names that case explicitly rather than showing a dead viewfinder.

### M9: Service worker / PWA offline — Complete 2026-09-05
- `manifest.webmanifest` and generated icons; the app installs to a home screen
- `sw.js`, written by hand — there is no build step, and a cache nobody can read is worse than no cache. Three strategies, each chosen per resource with the reason stated in the file
- Precached shell (23 entries) so every page renders with no network; `offline.html` for anything never visited
- API responses network-first, so a cached answer is only ever a fallback, never a preference
- Offline banner via `assets/js/pwa.js`

**The rule that shaped it: a cached score must never be presented as a current one.** The engine changes and the database changes, so an old score rendered as fresh is the same class of failure as reporting an unreadable label as clean — confidently wrong, with nothing about it looking wrong. The worker stamps any response it serves from cache, `opff.js` carries the stamp through, and the product page says it is showing a saved copy and when it was saved.

Two details worth keeping: navigations are deliberately **not** cached, because every product is the same document under a different query string and caching the response would add one identical entry per product viewed — the precached document is found with `ignoreSearch` instead. And a 404 from the API is never cached, because it is how an unknown barcode is detected, and caching it would keep reporting "not found" after the product is added to the database.

### M10: Not-found / submit flow — Complete 2026-09-05
- `submit.html?barcode=X`, reached from the not-found state on any product page
- Checks the barcode against its own check digit, and re-queries the database, before sending anyone off to photograph a tin — a typo looks exactly like a missing product, and is the only cause of "not in the database" the visitor can fix in five seconds
- Names the two panels that decide whether a product can be scored at all: the ingredient list, and the guaranteed analysis with moisture
- Deep-links the contribution to Open Pet Food Facts with the barcode filled in, and says plainly that the form is hosted on Open Food Facts, the project's main site

**No submission queue of our own, and that is the design rather than a limitation.** A private queue would fork the catalogue: the product would sit in our queue and still be missing from the database every score actually reads, making this site the bottleneck for its own corrections. Contributing upstream means it works here, in the next tool built on the same data, and for the next person who scans the same tin. [ADR-001](./ADR-001-static-first.md) predicted a hosted form as the workaround for not accepting writes; the record now says why the workaround was the wrong shape.

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
| Dark theme | Shipped in M5 — no longer deferred |
