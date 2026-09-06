# Cat Food Center

Science-based cat food reviews: scan a barcode or search the catalog to get an ingredient breakdown, additive risk flags, and a 0–100 CFC Score. Plus **The Cat Care Guide** — a free, sourced, eleven-page educational resource on feeding and raising a cat.

**Live site:** https://azqato.github.io/Cat-Food-Center/

---

## Tech stack

| Layer | Tool | Version |
|---|---|---|
| Framework | Next.js (App Router, static export) | 14.2.x |
| Language | TypeScript | 5.x |
| UI | React | 18.x |
| Styling | Tailwind CSS | 3.4.x |
| Fonts | Fraunces, Public Sans | Google Fonts (next/font) |
| Hosting | GitHub Pages | — |
| CI/CD | GitHub Actions | — |

## Prerequisites

- **Node.js 18 or higher** — Next.js 14 requires it
- **npm** — bundled with Node.js

No accounts, API keys, or environment variables are needed to run the project locally.

## Installation

```bash
git clone https://github.com/Azqato/Cat-Food-Center.git
cd Cat-Food-Center
npm install
```

## Running locally

```bash
npm run dev
```

The dev server starts at **http://localhost:3000**.

The local dev server does not apply the `/Cat-Food-Center` basePath used in production — all routes resolve from `/`. If you need to test with the basePath applied, run `npm run build` and serve the `out/` directory instead.

## Commands

| Command | What it does |
|---|---|
| `npm run dev` | Start dev server at localhost:3000 |
| `npm run build` | Static export to `out/` |
| `npm run lint` | Run ESLint |

`npm run start` is not used — the project uses static export, not a Node server.

## Environment variables

None required. The project is a fully static site with no backend.

When the Open Pet Food Facts API integration ships, any required variables will be added here.

## Build

```bash
npm run build
```

Output goes to `out/`. The build is configured with `output: 'export'`, `basePath: '/Cat-Food-Center'`, and `trailingSlash: true` for GitHub Pages compatibility.

## Deploy

Every push to `main` triggers `.github/workflows/deploy.yml`, which runs `npm run build` and deploys `out/` to GitHub Pages automatically.

One-time setup for a new fork:
1. Push the repo to GitHub.
2. Go to **Settings → Pages → Source** and select **GitHub Actions**.
3. The site deploys to `https://<your-username>.github.io/Cat-Food-Center/`.

## The Cat Care Guide

The `/learn` section is an eleven-page educational resource, built as a documentation site with a fixed sidebar, an "on this page" rail, and prev/next navigation.

| Page | Covers |
|---|---|
| [`learn.html`](learn.html) | Overview and the five rules that matter most |
| [`learn-nutrition.html`](learn-nutrition.html) | Obligate carnivore metabolism; protein, fat, carbohydrate, fibre; the nutrients cats cannot synthesise |
| [`learn-daily-requirements.html`](learn-daily-requirements.html) | The complete AAFCO nutrient profile — all 42 nutrients, with minimums, upper limits, and a worked per-day conversion |
| [`learn-labels.html`](learn-labels.html) | AAFCO statements, dry-matter maths, ingredient splitting, the 95/25/3 naming rules |
| [`learn-food-types.html`](learn-food-types.html) | Wet, dry, freeze-dried, air-dried, raw, fresh, home-prepared |
| [`learn-hydration.html`](learn-hydration.html) | Water requirements, dehydration signs, eleven ways to increase intake |
| [`learn-additives.html`](learn-additives.html) | Tiered reference to preservatives, colours, thickeners, palatants, fillers |
| [`learn-feeding.html`](learn-feeding.html) | Calorie maths, portioning, meal timing, transitions, weight management, multi-cat |
| [`learn-life-stages.html`](learn-life-stages.html) | Kitten, neutering, adult, pregnancy, senior, geriatric |
| [`learn-toxic.html`](learn-toxic.html) | Toxic foods, plants, medications, household hazards, emergency steps |
| [`learn-health.html`](learn-health.html) | Diet in obesity, CKD, FLUTD, diabetes, hyperthyroidism, IBD, allergy, hepatic lipidosis |

### Editing the guide

The eleven pages share one documentation shell, so they are **generated** rather than hand-written:

```bash
python tools/learn/build.py
```

Edit the article body in `tools/learn/c_<page>.py` and rerun. `tools/learn/shell.py` owns the shared chrome (top bar, sidebar, breadcrumb, on-this-page rail, pagination, footer) and `tools/learn/bits.py` holds the content components (callouts, tables, entry cards, panels).

Do not hand-edit `learn*.html` — those files are generated and your changes will be overwritten on the next build. The generated output is committed, so **deployment still requires no build step**.

Shared front-end assets live in [`assets/`](assets/): `cfc.css` (the design tokens and the documentation shell), `cfc-docs.js` (mobile drawer and the scroll spy), and `cfc-tailwind.js` (the Tailwind CDN theme used by the non-guide pages).

## Project status

MVP live on GitHub Pages. Home, search, and product detail pages are fully built with mock data; the methodology page and the Cat Care Guide are complete and content-backed. Dark mode with a persisted preference is next, followed by the Open Pet Food Facts integration, scoring engine, and barcode scanner. See [`docs/ROADMAP.md`](docs/ROADMAP.md) for the milestone plan.

## Documentation

Full specifications are in [`/docs`](docs/):

| File | Contents |
|---|---|
| [`PRD.md`](docs/PRD.md) | Product requirements and CFC scoring methodology |
| [`TRD.md`](docs/TRD.md) | Architecture, data model, and engineering spec |
| [`DESIGN.md`](docs/DESIGN.md) | Visual system, color tokens, and UX flows |
| [`PATCHNOTES.md`](docs/PATCHNOTES.md) | Changelog |
| [`PRFAQ.md`](docs/PRFAQ.md) | Press release and FAQ |
| [`TENETS.md`](docs/TENETS.md) | Product principles |
| [`METRICS.md`](docs/METRICS.md) | Success metrics and targets |
| [`ROADMAP.md`](docs/ROADMAP.md) | Milestone plan |
| [`SECURITY.md`](docs/SECURITY.md) | Security model |
| [`RUNBOOK.md`](docs/RUNBOOK.md) | Operations and troubleshooting |
