# Patch Notes

All notable changes to Cat Food Center are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/). Versions follow [Semantic Versioning](https://semver.org/).

---

## v0.3.0 — 2026-06-08

### Added
- Full documentation suite: PRD, TRD, DESIGN, PATCHNOTES, PRFAQ, TENETS, METRICS, ROADMAP, SECURITY, RUNBOOK
- `/docs` directory consolidating all project documentation
- README.md rewritten for developer audience with install, dev, build, and deploy instructions

### Changed
- PRD.md, TRD.md, DESIGN.md moved from project root into `/docs`
- TRD.md updated to reflect actual current implementation state (mock data, deferred features catalogued in known technical debt table)
- DESIGN.md updated with precise Tailwind token references, accessibility ARIA patterns, and component implementation details

---

## v0.2.0 — 2026-06-07

### Added
- Next.js 14 App Router with TypeScript and static export configured for GitHub Pages (`basePath: /Cat-Food-Center`)
- Tailwind CSS with full design token theme: colors (`bg`, `surface`, `ink`, `ink-soft`, `accent`, `hairline`, four band colors), typography scale (`display`, `h1`, `h2`, `body`, `small`, `micro`), border radius (`card`, `pill`), max-width (`content`)
- Fraunces (display serif) and Public Sans (body sans) loaded via `next/font/google`
- Global layout (`app/layout.tsx`): sticky header with wordmark and Support pill button linking to `https://azqato.github.io/support.html`; footer with Azqato link
- Home page (`app/page.tsx`): wordmark, tagline, disabled Scan button with "coming soon" tooltip, search form routing to `/search`, recently viewed section with two mock product cards and score badges
- Search page (`app/search/`): search bar pre-filled from `?q=` param, mock result list of three products with score badges and band labels
- Product detail page (`app/product/[barcode]/page.tsx`): score header with band color bar and checkmark glyph, verdict section with reason chips, numbered ingredient list, additive flags section with tier dot and cited source links, 2×2 nutrition snapshot grid (dry-matter basis), AAFCO adequacy quote, footer metadata row with data completeness and last reviewed date
- GitHub Actions workflow (`.github/workflows/deploy.yml`): builds with `npm ci && npm run build` and deploys `out/` to GitHub Pages on every push to `main`
- `public/.nojekyll` to prevent GitHub Pages from ignoring underscore-prefixed directories

### Changed
- Replaced earlier plain HTML/CSS/JS implementation with Next.js App Router static export

---

## v0.1.0 — 2026-06-07

### Added
- Initial Next.js App Router scaffold with TypeScript, Tailwind CSS, ESLint, and PostCSS
- `next.config.ts` with `output: 'export'`, `trailingSlash: true`, `basePath`, and `assetPrefix` for GitHub Pages
- `PRD.md`, `TRD.md`, `DESIGN.md` specification documents
- `.gitattributes` and `.gitignore`
