# Cat Food Center

Science-based cat food reviews: scan a barcode or search the catalog to get an ingredient breakdown, additive risk flags, and a 0–100 CFC Score.

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

## Project status

MVP live on GitHub Pages. Home, search, and product detail pages are fully built with mock data. The Open Pet Food Facts integration, scoring engine, and barcode scanner are planned next. See [`docs/ROADMAP.md`](docs/ROADMAP.md) for the milestone plan.

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
