# Cat Food Center

**Trustworthy reviews for your purrfect companion!**

Cat Food Center is a mobile-first web app (with full browser support) that does for cat food what Yuka does for groceries. Scan a barcode or search the catalog, and get a clear breakdown of what is actually in the product: every ingredient, every additive, the health impact of those additives, and a single overall health rating from 0 to 100.

We believe every cat deserves the best nutrition. Cats are obligate carnivores with needs (taurine, arginine, arachidonic acid, high animal protein) that human nutrition labels were never built to judge, so our rating engine is purpose-built for feline biology and grounded in published standards from AAFCO, the FDA, EFSA, and the WHO/IARC.

## What it does

* **Scan or search.** Point your phone camera at a barcode, or type a product or brand name.
* **Ingredient breakdown.** Plain-language explanation of each ingredient and what it is doing in the recipe.
* **Additive flags.** Each additive is tagged by risk tier, with the health concern and the scientific source behind it.
* **Overall rating.** A 0 to 100 "CFC Score" with a color band: Excellent, Good, Poor, or Bad.
* **Unbiased by design.** No paid placements, no advertiser influence on scores. The methodology is open and documented.

## How the rating works (summary)

The CFC Score blends three pillars:

* **Nutritional quality (55%):** animal-protein dominance, carbohydrate/filler load, moisture, and sufficiency against the AAFCO feline nutrient profile for the stated life stage.
* **Additives and safety (35%):** presence of flagged additives, weighted by evidence-based risk tier. A high-risk additive caps the maximum score.
* **Ingredient quality and transparency (10%):** named versus unnamed proteins, sourcing disclosure, and recall history.

Full scoring logic lives in `PRD.md` and `TRD.md`.

## Tech stack

* **Framework:** Next.js (App Router) with TypeScript
* **Styling:** Tailwind CSS
* **Delivery:** Progressive Web App (installable, offline catalog cache, mobile-first)
* **Barcode scanning:** in-browser camera via the BarcodeDetector API, with a ZXing fallback
* **Product data:** Open Pet Food Facts as the primary catalog, supplemented by an internal additive and nutrient knowledge base
* **Hosting target:** static and edge friendly (Vercel or GitHub Pages compatible build)

## Repository documents

* `README.md` (this file): project overview and quick start
* `PRD.md`: product requirements and the full rating methodology
* `TRD.md`: technical requirements, architecture, and data model
* `DESIGN.md`: visual system, mobile-first layout, and UX flows
* `PATCHNOTES.md`: running changelog, updated after every change

## Running locally

No build step, no Node.js needed. Just open `index.html` in any browser:

```
# Windows
start index.html

# Mac
open index.html
```

Or serve with any static server for a more realistic experience:
```bash
# Python (if installed)
python -m http.server 8080
# then open http://localhost:8080
```

The three pages — `index.html`, `search.html`, `product.html` — link to each other with relative URLs and work identically from `file://` or any static server.

## Deploying to GitHub Pages

The repo already includes `.github/workflows/deploy.yml`. On every push to `main`, GitHub Actions uploads the repo root and deploys it to Pages. **No build step required.**

One-time setup:
1. Push to `main` (already done).
2. In the repo: **Settings → Pages → Source → GitHub Actions**.
3. The site goes live at `https://azqato.github.io/Cat-Food-Center/`.

## Project structure

| Path | Purpose |
| --- | --- |
| `index.html` | Home page (MVP, served directly) |
| `search.html` | Search results (MVP, served directly) |
| `product.html` | Product detail (MVP, served directly) |
| `app/` | Future Next.js App Router source |
| `components/` | Future Next.js components |
| `package.json` etc. | Future Next.js build config |
| `PRD.md` / `TRD.md` / `DESIGN.md` | Living specs |

The `app/` and `components/` directories are the planned Next.js migration path. They don't affect GitHub Pages. When ready to transition to a full server-rendered product, add the build steps back to the workflow and retire the HTML pages.

## Status

MVP live on GitHub Pages. All three pages (home, search, product) are plain HTML running entirely client-side with no server. All product data is hardcoded mock. Real Open Pet Food Facts API wiring, the CFC scoring engine, and the barcode scanner are the next phase. `PRD.md` is the living spec; update `PATCHNOTES.md` on every meaningful change.

## A note on scope

Cat Food Center is an informational tool, not veterinary advice. Ratings help owners compare products and spot red flags. For cats with medical conditions (kidney disease, diabetes, urinary issues), always defer to a veterinarian.
