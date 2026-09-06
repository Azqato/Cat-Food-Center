# Patch Notes

Running changelog for Cat Food Center. Add an entry to the top for every meaningful change. Keep `PRD.md` in sync whenever product behavior or the scoring model changes.

Format: newest first. Use semantic-ish version tags (major.minor.patch). Pre-launch work lives under 0.x.

---

## [0.12.1] - 2026-09-05

**Documentation brought back in line with the code, and two milestones planned.**

Added
* `docs/ROADMAP.md` M13: a documentation consolidation audit. Collapses the eleven files in `/docs` to `PRD.md`, `DESIGN.md` and `PATCHNOTES.md` plus the root README, and adds the root-only files the project has never had (`LICENSE.md`, `robots.txt`, `sitemap.xml`). The full method, the target structure, the merge-rather-than-overwrite rule, and the defaults for writing style, browser testing, verification environment, licensing and removal policy are written out in the milestone so the scope survives the session that requested it. Planned, not scheduled, not started.
* `docs/ROADMAP.md` M14: move the whole site onto the interface built for the Cat Care Guide. The blocker is recorded as the first thing to solve rather than a detail — the guide top bar has no page navigation at all, while the app top bar has the six-link nav but neither the search affordance nor the sidebar control, so the merged bar has to carry both on a 360px phone. Four open design questions and six codebase constraints are listed. Planned, not scheduled, not started.

Fixed
* **Stale counts.** `docs/TRD.md` claimed the precached shell was 23 entries; `sw.js` has held 27 since M10 and M11 added pages. The TRD tree described `tools/check-live.py` as eight end-to-end checks; it has been twelve since M11.
* **Stale version.** `docs/TRD.md` §0 was headed "Current implementation state (v0.7.0)" five releases after v0.7.0, and its list of what is implemented omitted the compare page, the submit page and offline support.
* **"Four Tailwind pages" was wrong in five places** across `README.md` and `docs/TRD.md`. There are eight. The TRD's advice that a fifth would be the trigger to move them under the generator has been rewritten, since that threshold was crossed without anyone noticing and the duplication is now real debt rather than a hypothetical.
* **A testing instruction that could not work.** `docs/TRD.md` §12 described the scoring tests as runnable "under `node --test`". There is no Node.js in this project by decision ([ADR-001](docs/ADR-001-static-first.md)), and the suite is browser-hosted only.
* `docs/TRD.md` §8 routing table was missing `offline.html` and `tests.html`.

Notes
* Historical changelog entries were left alone. The "23 entries" in the v0.10.0 notes was accurate when written, and rewriting it would turn a record of what happened into a claim about the present. The roadmap's M9 entry now reads "23 entries at the time, 27 today" for the same reason.
* No code changed in this release.

---

## [0.12.0] - 2026-09-05

**Side-by-side comparison (M11).**

Added
* `compare.html?a=X&b=Y` — two products next to each other. The URL carries the comparison, so it can be shared and reloaded. Products already viewed are offered in a picker; anything else goes in by barcode.
* Figures converted to a **dry-matter basis**. Without that a wet food at 11% protein reads as worse than a dry food at 32%, when it is in fact the more protein-dense of the two — the wet food is mostly water.
* A `Compare` entry in the top navigation.

Notes
* **The page never declares a winner on the overall score, and that is the point of it.** A 72 worked out from three pillars and a 72 worked out from one are different claims wearing the same number. Only about a fifth of products carry enough data for all three pillars, so this is the normal case rather than an edge case. Where the two products were scored on different pillars, the page says so before showing anything else, and the comparison is pillar by pillar — only across pillars both products actually have.
* **Where only one product publishes a figure, neither cell is highlighted.** Marking the one that happens to have data would be a comment on the database rather than on the food.
* Fat is shown without a "better" direction. More fat is not simply better, and pretending a single number has an obvious direction is how a comparison tool starts lying.

---

## [0.11.0] - 2026-09-05

**A real answer for a product that is not in the database (M10).**

Added
* `submit.html?barcode=X`, reached from the not-found state on any product page.
  * **Rules out a typo first.** A mistyped digit looks exactly like a missing product, and it is the only cause the visitor can fix in five seconds. The page checks the barcode against its own check digit and re-queries the database before sending anyone off to photograph a tin. If the product turns out to be there after all, it links straight to its page.
  * **Names the two panels that matter.** The ingredient list — without it there is no score at all, not a low one — and the guaranteed analysis including moisture, without which a wet food cannot honestly be compared to a dry one.
  * **Deep-links the contribution** to Open Pet Food Facts with the barcode filled in, and says plainly that the form is hosted on Open Food Facts, the project's main site, so the hand-off is not a surprise.

Changed
* The not-found state now links here rather than dropping the visitor straight onto an unexplained external form.
* `docs/ADR-001-static-first.md` updated: the "no server-side writes" row predicted a hosted form or a GitHub issue as the workaround. Building it showed the workaround was the wrong shape, and the ADR now records why.

Notes
* **There is no submission queue of our own, by choice.** A private queue — hosted form, GitHub issue, serverless endpoint, any of them — would fork the catalogue. The product would sit in our queue and still be missing from the database every score on this site actually reads, which would make us the bottleneck for our own corrections. Sending it upstream means it works here, in the next tool built on the same database, and for the next person who scans the same tin.
* The general lesson, recorded in the ADR: not every limitation of static hosting needs a workaround. This one was better answered by not holding the data at all.

---

## [0.10.0] - 2026-09-05

**Offline support, and installability (M9). The app works in the aisle where the signal does not.**

Added
* `sw.js` — a hand-written service worker. No build step means no Workbox, and that turned out to be the better outcome: every caching decision is one of three strategies, chosen per resource, with the reason written next to it.
  * App shell precached (23 entries), so every page renders with no network at all.
  * API responses **network-first** — a cached answer is a fallback, never a preference.
  * Images cache-first; they are large and never change under a URL.
  * Third-party CDNs left alone. They set their own cache headers, and second-guessing them from here would mean owning their invalidation too.
* `offline.html` — for a page never opened on this device. It says what still works rather than showing the browser's own error page.
* `manifest.webmanifest` and generated icons at 192, 512 and 512-maskable. The app installs to a home screen and opens standalone.
* `assets/js/pwa.js` — registration (on `load`, so it never competes with rendering) and an offline banner.
* Two more checks in `tools/check-live.py`: the worker precaches and does not grow per product viewed, and an offline product still renders **and is labelled**.

Changed
* A product page served from cache now says so, with the time it was saved. The worker stamps the response, `opff.js` carries the stamp through, and the page renders a notice.

Notes
* **A cached score must never be presented as a current one.** The scoring engine changes and the database changes, so a stale score rendered as fresh is the same failure as the English-only matcher — confidently wrong, with nothing about it looking wrong. That rule is why the stamp exists, and it is written at the top of `sw.js` so the next change to that file has to reckon with it.
* **Navigations are deliberately not cached.** Every product is `product.html` under a different query string, so caching responses would add one byte-identical entry per product viewed and grow the shell cache without bound. The precached document is found with `ignoreSearch` instead — and without that flag an offline product page would fall through to `offline.html` despite the document being cached.
* **A 404 is never cached.** It is how an unknown barcode is detected, and caching it would keep reporting "not found" after the product is added to the database.
* `navigator.onLine` is trusted only in the negative direction. It reports a network interface, not reachability, so a false "you are online" shows nothing rather than a wrong reassurance.

---

## [0.9.0] - 2026-09-05

**The scanner (M8), and a home page that shows your own history instead of two invented products.**

Added
* `scan.html` and `assets/js/scanner.js` — barcode scanning, entirely client-side. Frames are decoded on the device and never uploaded; the only thing that leaves is the barcode number, to look the product up. `BarcodeDetector` is used where the platform provides it, and ZXing is downloaded only when it does not — never speculatively.
* `assets/js/scan-page.js` — the part that has to be kind about failure. Declined permission, no camera, camera held by another app, a browser with no camera API and a page not on HTTPS each get their own sentence and their own suggested next step.
* Manual barcode entry on the same page, always visible. On a desktop browser it is the primary path, not a consolation prize. Entries are checksum-validated before navigating, so a typo is reported as a typo rather than as a gap in the database.
* `assets/js/history.js`, `assets/js/home-page.js` — "Recently viewed", kept in `localStorage` on the device and nowhere else. There is no account and no sync, which is a feature of the static architecture rather than a limitation of it: what someone feeds their cat is not information we have any reason to hold. Only barcode, name, brand and the last score are stored, and opening a product recomputes the score rather than trusting the stored one.
* A `Scan` entry in the top navigation of every page.
* `assets/js/scanner.test.js` — 17 assertions on barcode validation. The full suite is now 147.
* `tools/check-live.py` grew to 8 checks: the scan page, the home page, a recently-viewed round-trip across two page loads, and a decode round-trip that draws a known EAN-13 and reads it back.

Changed
* The home page Scan button is a real link. It was disabled with a "Coming soon" tooltip.

Removed
* The two invented "Recently viewed" products (Weruva and Friskies, with hardcoded scores). The section now hides itself until there is something real to show — an empty list on a home page reads as something broken.

Notes
* **UPC-E cannot be checksum-validated in place.** Its check digit is computed over the expanded UPC-A form, so validating an 8-digit UPC-E under the EAN-8 rule rejects it. That failure is silent: the scanner would keep scanning and simply never see small US packages. `expandUpcE` exists for this, and an 8-digit code is accepted if either reading checks out.
* **`getUserMedia` needs a secure context.** `http://<LAN-IP>` is not one, so testing from a phone on the local network gives no camera at all, with no error that says why. The page distinguishes that case from a real fault.
* QR codes are deliberately excluded from the format list. Packaging carries them, and a QR code is not the product's barcode.

---

## [0.8.0] - 2026-09-05

**The scoring engine, the API client, and the two pages that use them. The product is now real: enter a barcode and get a derived score with its reasoning.**

Added
* `assets/js/opff.js` — Open Pet Food Facts client and normaliser. Reads both nutriment schemas (preferring the pet-food guaranteed analysis over Open Food Facts' human-food keys) and records which was used; gates every figure against a plausible range for cat food; infers per-kilogram energy values and corrects them; splits ingredient strings on depth-aware commas so a parenthetical stays with its parent ingredient.
* `assets/js/scoring.js` — the CFC Score. Pure and deterministic: no network, no DOM, runs in the visitor's browser so a sceptical reader can watch a score being derived. Renormalises pillar weights across the pillars that could be computed, applies the two hard gates, and returns `scorable: false` rather than a number when too little is known.
* `assets/js/product-page.js`, `assets/js/search-page.js` — replace the mock render blocks. `product.html` went 475 → 102 lines, `search.html` 166 → 99.
* `assets/data/additives.json` — 20 additives across three tiers plus three catch-all label terms, each with function, tier, plain-language health impact, regulatory note and sources. Tiers mirror the guide.
* `tests.html`, `assets/js/test-runner.js`, `tools/run-tests.py` — 130 assertions run headlessly in a real browser. No Node, no build step, consistent with ADR-001.
* `tools/probe-opff.py`, `tools/check-live.py` — the measurement script behind `docs/DATA-COVERAGE.md`, and an end-to-end check of four page states against the live API.
* `docs/DATA-COVERAGE.md` — what the database actually contains, measured across 600 products.
* **methodology.html: "What the score cannot see."** The limits are now published alongside the method, because a score that does not state what it could not check is overclaiming.

Fixed
* **A French product scored 77 / Excellent with a perfect transparency pillar and the reason "Ingredient sources are named rather than generic." Its first ingredient was unnamed meat by-products and its last was sugar.** Only 9.5% of records carry English ingredients, and the alias matcher was English-only — so on ~90% of labels it matched nothing, and nothing matched was being reported as clean. Four distinct defects sat behind that single score, and three of them were live in English too; they had simply never fired, because the test fixtures were written in the same language as the matcher. Full write-up in `docs/DATA-COVERAGE.md`.
  * Aliases extended to French, German, Spanish, Italian and Dutch — in `additives.json` and in the animal-protein, plant-protein and starch lists.
  * `MATCHED_LANGUAGES` guard: where the label is in a language the aliases do not cover, the engine says the list could not be read, withholds the clean-formulation bonus and the "no flagged additives" finding, caps confidence at low, and warns. **Silence is not evidence.**
  * The Tier 0 "named by-products" credit had bare stems as aliases, so *"meat by-products"* earned a bonus for being a named source while the transparency pillar penalised the identical words for being unnamed. Tier 0 credit is now matched per ingredient entry and withheld where that entry is itself an unnamed source.
  * A parenthetical could rename an unnamed source: `(dont boeuf 4%)` made "viandes et sous-produits animaux" read as a named beef first ingredient, worth full marks. Such entries are now judged on the text before the parenthesis, across the whole first-three window.
  * The nutrition pillar now has an explicit branch for an unnamed leading protein, so the most important thing the list says is what gets reported, rather than whatever happened to appear second.
* Alias matching missed plurals — aliases are written singular, labels are plural — so the unnamed-source penalty never fired on a real label.
* The animal-protein check ran on the first three ingredients before the plant-protein check ran on the first, so a list led by pea protein scored as animal-protein-first the moment chicken fat appeared third.

Notes
* `docs/DATA-COVERAGE.md` overturned the M6/M7 assumption that most products carry a full guaranteed analysis. About a fifth are scoreable on all three pillars, and a quarter of the products carrying a protein figure carry an implausible one. Partial data is the normal path, not an error path, and both modules are built around that.
* The unit suite was 109 green while all four scoring defects above were live. Rendering one real product page found what the whole suite could not.

---

## [0.7.0] - 2026-09-05

**Light/dark theming across the whole site, and the end of the Next.js fork in the repository.**

Added
* `assets/cfc-tokens.css` — the palette, split out of `cfc.css` so both page families share one source of truth: the four Tailwind CDN pages and the eleven generated guide pages. Carries the light values, the dark values (twice — once for an explicit choice, once for `prefers-color-scheme`), the theme toggle component, and the chip component.
* `assets/cfc-theme.js` — three-state theme control: system → light → dark. Persists under `localStorage` key `cfc-theme`; `system` stores nothing and lets the media query decide. Loaded as a **blocking** `<script>` in `<head>`, which is what prevents a flash of the wrong palette. A `storage` listener keeps other open tabs in step, and a blocked-site-data failure falls back to the system theme rather than throwing.
* Theme toggle in the top bar of all fifteen pages.
* `tools/check-contrast.py` — audits all 38 foreground/background pairs in both palettes against WCAG AA, and fails if the two duplicated dark blocks have drifted apart.
* `docs/ADR-001-static-first.md` — records static HTML as the target architecture rather than an interim state, with the reasoning per planned feature and, more usefully, the list of what static hosting genuinely cannot do and the escape hatch for each.

Changed
* Tailwind colour names now resolve to `var(--...)` instead of hex literals, so `bg-surface` and `text-ink` follow the theme with no `dark:` variants in the markup. **Trade-off:** Tailwind opacity modifiers (`bg-surface/50`) no longer work on those colours — add a token instead.
* Every hardcoded colour on the four Tailwind pages, including the ones generated by JavaScript in `product.html`, now goes through a token.
* The green and amber score chips previously used white text at 2.8:1 and 2.3:1. They now use dark ink. **This changes the light theme's appearance** — it was a pre-existing accessibility defect that building the second palette surfaced rather than caused.
* `README.md`, `docs/TRD.md`, `docs/RUNBOOK.md` and `docs/DESIGN.md` rewritten to describe the stack that actually ships. They previously documented Next.js, npm scripts, `next.config.ts` and a build pipeline, none of which existed in the deployed site.
* `.github/workflows/deploy.yml` — the "when transitioning to Next.js" comment replaced with a pointer to ADR-001.

Removed
* The unused Next.js 14 application: `app/`, `components/`, `public/`, `next.config.ts`, `package.json`, `postcss.config.mjs`, `tailwind.config.ts`, `tsconfig.json`, `.eslintrc.json`. It was never built and never deployed — `deploy.yml` has always uploaded the repository root — but it was documented as the stack, which made the repository actively misleading. It remains in git history if it is ever wanted back.

Notes
* Confirmed while writing ADR-001: the planned barcode scanner needs no server. `getUserMedia` + `BarcodeDetector` (ZXing WASM fallback) + the keyless, CORS-enabled Open Pet Food Facts API all run in the browser. The only hard requirement is HTTPS, which GitHub Pages provides. One consequence worth remembering: `http://<LAN-IP>` is not a secure context, so testing the scanner on a phone means using the deployed URL or an HTTPS tunnel.

---

## [0.6.0] - 2026-09-05

**Added The Cat Care Guide — an eleven-page educational resource, built as a documentation site.**

Added
* `learn.html` — guide overview, the five rules that matter most, and the map of all topics.
* `learn-nutrition.html` — obligate carnivore metabolism, the five adaptations that define feline nutrition, protein/fat/carbohydrate/fibre, and the eight nutrients cats cannot synthesise (taurine, arginine, arachidonic acid, retinol, niacin, vitamin D3, B12, thiamine).
* `learn-daily-requirements.html` — the complete AAFCO Cat Food Nutrient Profiles table (42 nutrients, growth and adult minimums plus maximums), the RER/MER formulas with a life-stage factor table, and a full worked conversion into grams and milligrams per day for a 4.5 kg neutered indoor cat.
* `learn-labels.html` — reading order, AAFCO adequacy statements ranked by strength, the dry-matter conversion with a worked wet-vs-dry comparison, carbohydrate by difference, ingredient splitting, the 95/25/3 naming rules, and marketing terms with no regulatory meaning.
* `learn-food-types.html` — seven formats compared on moisture, carbohydrate, calorie density, cost and safety; includes the current FDA position on H5N1 in raw pet food and the evidence on home-prepared recipes failing nutrient analysis.
* `learn-hydration.html` — water requirements by body weight, a diet-by-diet water balance table, dehydration checks, and eleven ranked ways to increase intake.
* `learn-additives.html` — three-tier additive reference covering 30+ compounds (propylene glycol, ethoxyquin, BHA, BHT, artificial colours, titanium dioxide, menadione, carrageenan, gums, glutamates, inorganic phosphates and more), each with its regulatory position and evidence, plus a section on commonly criticised ingredients that are not actually a problem.
* `learn-feeding.html` — calorie tables for seven body weights, portioning, meal timing patterns, food-based enrichment, a seven-day transition schedule, the 10% treat rule, body condition scoring, and multi-cat feeding.
* `learn-life-stages.html` — weaning through geriatric, the kitten-vs-adult requirement table, the post-neutering weight-gain window, pregnancy and lactation energy factors, and why senior cats need more protein rather than less.
* `learn-toxic.html` — toxic foods, plants (lilies flagged as a same-hour emergency), medications, and household hazards, with poison-line numbers and first-ten-minutes steps at the top of the page.
* `learn-health.html` — diet in obesity, CKD, FLUTD, diabetes, hyperthyroidism, IBD, food allergy, hepatic lipidosis, dental disease and constipation.
* `assets/cfc.css` — design tokens plus the three-column documentation shell (top bar, sidebar, article, on-this-page rail), callouts, data tables, entry cards, panels, comparison grids, pagination and site footer. Responsive: the right rail drops below 1180px, the sidebar becomes a drawer below 900px.
* `assets/cfc-docs.js` — mobile navigation drawer (hamburger, backdrop, Escape to close) and the "on this page" scroll spy. Both are progressive enhancements; pages are fully readable without JavaScript.
* `assets/cfc-tailwind.js` — the Tailwind CDN theme, extracted from the inline per-page configs.
* `tools/learn/` — static generator (`build.py`, `shell.py`, `bits.py`, and one `c_*.py` content module per page) so the eleven pages share one shell and cannot drift apart. Generated HTML is committed, so deployment still needs no build step.
* Home page: a Cat Care Guide entry card above "Recently viewed".

Changed
* All pages: **Learn** link added to the header nav between Search and Methodology, linking to `./learn.html`.
* All pages: header nav now scrolls horizontally on narrow viewports instead of overflowing, now that it carries four items.
* `docs/ROADMAP.md`: milestones renumbered into chronological order; the Cat Care Guide recorded complete as M4; dark mode promoted out of the deferred list to M5, specified with a header toggle and a `localStorage`-persisted preference that falls back to `prefers-color-scheme`.
* `README.md`: documents the guide, the generator workflow, and the shared assets.

---

## [0.5.3] - 2026-06-07

**Removed Methodology from footers — now accessible via header nav.**

Changed
* All pages: removed the "· Methodology" link from the footer. Footer now contains only "Built by Azqato". Methodology remains reachable via the header nav on every page.

---

## [0.5.2] - 2026-06-07

**Added Search to header navigation.**

Changed
* All pages: **Search** link added to the nav between Home and Methodology, linking to `./search.html`. Search is highlighted (accent color, bold) when on `search.html`.

---

## [0.5.1] - 2026-06-07

**Added Home and Methodology links to the header navigation.**

Changed
* All pages (`index.html`, `search.html`, `product.html`, `methodology.html`): header now contains a `<nav>` element with three links — **Home**, **Search**, and **Methodology** — between the wordmark and the Support button.
* The link for the currently visited page is highlighted in accent color and bold via `aria-current="page"` — Home on `index.html`, Search on `search.html`, Methodology on `methodology.html`; none highlighted on `product.html`.

---

## [0.5.0] - 2026-06-07

**MVP completion: all documented sections built out.**

Added
* `methodology.html`: public scoring explanation page mirroring `PRD.md` §6 — always reachable from the footer. Covers: why cats need a dedicated system, the three-pillar model and weights, Pillar A sub-factors (protein dominance, taurine, carb load, moisture, AAFCO adequacy), Pillar B additive risk tiers (Tier 1–3 with examples), Pillar C transparency factors, hard gates and caps, score bands with color swatches, a worked example, and data sources.
* All pages: "Methodology" link added to footer alongside "Built by Azqato".

Changed
* `product.html`: fully rewritten as a JS-driven page. All content is now rendered from embedded product data objects keyed by barcode — different barcodes produce different products. Changes include:
  * Three distinct products: Instinct Original Grain-Free with Real Chicken (0000000000000, 61, Good), Weruva Paw Lickin' Chicken (0000000000001, 81, Excellent), Friskies Surfin' & Turfin' Favorites (0000000000002, 28, Poor).
  * Band-appropriate glyphs per `DESIGN.md §5`: Excellent = circle-check, Good = check, Poor = exclamation-triangle, Bad = X-circle. Each rendered in the band color.
  * Warning banner (conditional): fires for products with Tier 3 additives (Friskies shows amber banner: "Tier 3 additives — score capped at 49").
  * Alternatives section (conditional): shown for Poor and Bad products; Friskies lists Weruva and Instinct as better options.
  * Additive flags grouped by tier descending (Tier 3 first, then Tier 2); Weruva shows a "No flagged additives detected" positive message.
  * Taurine "Not listed" state (red X glyph) for products that don't declare taurine (Friskies).
  * Not-found state: unknown barcodes show a friendly message and a link back to home.
  * Dynamic page title set from product name via `document.title`.
* `search.html`: updated result cards 2 and 3 to match the real product catalog — Weruva (81, Excellent, barcode 0000000000001) and Friskies (28, Poor, barcode 0000000000002). All cards now link to their correct product pages.

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
