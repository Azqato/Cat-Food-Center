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

## Getting started

Node.js (LTS) is required. Download it from [nodejs.org](https://nodejs.org) if not already installed.

```bash
# install dependencies
npm install

# run the dev server (local preview at http://localhost:3000)
npm run dev

# build for production — outputs static files to out/
npm run build
```

Open `http://localhost:3000` in a browser, or use device emulation to test the mobile layout.

> **Note:** `npm run dev` serves the site without the `/Cat-Food-Center` base path, so all links work normally in local development. The base path only applies to the production `out/` build.

## Deploying to GitHub Pages

1. Run `npm run build` — this produces an `out/` directory.
2. Push the contents of `out/` to the `gh-pages` branch of the repository, or use a GitHub Actions workflow (recommended).
3. In **Settings → Pages**, set the source to the `gh-pages` branch, root (`/`).
4. The site will be live at `https://azqato.github.io/Cat-Food-Center/`.

A minimal GitHub Actions workflow example:

```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: lts/*
      - run: npm ci
      - run: npm run build
      - uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./out
```

## Status

MVP complete (Prompts 1–4). All code is in place and ready for deployment. Node.js was not available on the dev machine during scaffolding so `npm run build` has not been verified locally — run it after installing Node.js. All product data is hardcoded mock; real Open Pet Food Facts API wiring, the scoring engine, and the barcode scanner are the next phase.

Real API calls, barcode scanning, and the scoring engine are deferred to a later phase. `PRD.md` is the living spec; update `PATCHNOTES.md` on every meaningful change.

## A note on scope

Cat Food Center is an informational tool, not veterinary advice. Ratings help owners compare products and spot red flags. For cats with medical conditions (kidney disease, diabetes, urinary issues), always defer to a veterinarian.
