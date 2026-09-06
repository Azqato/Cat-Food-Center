# ADR-001: Static HTML is the architecture, not a placeholder

- **Status:** Accepted
- **Date:** 2026-09-05
- **Deciders:** Azqato

---

## Context

The repository has been carrying two implementations at once. `.github/workflows/deploy.yml` uploads the repository root to GitHub Pages with no build step, so what ships is the plain HTML at the root: `index.html`, `search.html`, `product.html`, `methodology.html`, and the eleven `learn*.html` pages. Alongside those sits an unused Next.js 14 App Router application (`app/`, `components/`, `next.config.ts`, `tailwind.config.ts`) that is never built and never deployed. `README.md` described Next.js as the stack, which was wrong about the thing users actually load.

That fork had to be resolved before building the data layer, the scoring engine, or the scanner, because those three features are where the choice of architecture actually bites.

The specific question raised was whether committing to static HTML forecloses the barcode scanner (M8). It does not, and the reasoning generalises.

## Decision

**Static HTML, CSS, and vanilla JavaScript, served directly from the repository root, is the target architecture for Cat Food Center — not an interim state to be migrated away from.**

Consequences of accepting this:

1. The unused Next.js application is deleted. Keeping a second, stale implementation of the same pages is a maintenance tax with no payoff, and it actively misleads anyone reading the repository.
2. Where a page needs to be generated rather than hand-written — as the eleven-page Cat Care Guide does — a small Python generator under `tools/` emits committed HTML. The build runs on a developer's machine, never in CI. What is in the repository is exactly what is served.
3. Application logic (scoring, normalisation, the additive knowledge base) is written as plain ES modules under `assets/js/`, loaded with `<script type="module">`. No bundler, no transpile step.
4. Data that we own ships as static JSON under `assets/data/`, fetched at runtime.

## Why this works for the planned features

### Barcode scanning (M8) — fully client-side, no server needed

Scanning decomposes into three parts, all of which run in the browser:

| Part | Mechanism | Static-compatible |
|---|---|---|
| Camera access | `navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })` | Yes — requires a **secure context** (HTTPS), which GitHub Pages provides |
| Decode | `BarcodeDetector` where available; ZXing WASM fallback elsewhere | Yes — both run entirely in-page |
| Product lookup | `fetch` to the Open Pet Food Facts API | Yes — the API is public, CORS-enabled, and needs no key |

The one hard requirement is HTTPS, and we already have it. Note that this also means **the scanner cannot be tested over `http://localhost`'s sibling `http://<LAN-IP>`** on a phone — `localhost` itself is treated as a secure context, but a bare LAN IP is not. Testing on a real phone means testing against the deployed Pages URL or a tunnelled HTTPS origin.

### Data layer (M6) — a public, keyless, CORS-enabled API

Open Pet Food Facts requires no API key and sets permissive CORS headers, so the browser can call it directly. There is no secret to protect and therefore no reason to proxy through a server. The cost is that every visitor's browser makes the call itself, which the service worker in M9 will cache.

### Scoring engine (M7) — pure functions over fetched data

Scoring is deterministic computation on a product object. It has no reason to run anywhere but the client, and running it client-side makes it auditable: a sceptical reader can open devtools and watch the score being derived, which serves the transparency tenet better than a server-computed number would.

## What static HTML genuinely cannot do

These are the roadblocks. They are recorded here so that hitting one is a recognised trigger for revisiting this decision rather than a surprise.

| Limitation | Affects | Mitigation within static hosting | Escape hatch if the mitigation fails |
|---|---|---|---|
| **No server-side writes.** There is nowhere to POST to. | M10 submit flow — a user reporting a missing barcode or uploading a label photo | **Resolved differently than expected — see below.** Contributions go to Open Pet Food Facts itself, deep-linked with the barcode | A single serverless function (Cloudflare Worker / Netlify Function) alongside Pages; does not require abandoning static hosting |
| **No secrets.** Anything shipped to the browser is public. | Any future API that requires a key | Prefer keyless public APIs; Open Pet Food Facts is one | Same serverless function acting as a signing proxy |
| **No server-side rendering or dynamic routes.** `product.html?barcode=X` works; `/product/X` as a real path does not, without pre-generating a file per barcode. | M6 product pages, share links, SEO | Query-string routing, rendered client-side. Accept that per-product pages are not individually indexed in v1. | Pre-generate HTML for the top-100 SKU catalog at build time via `tools/` — this is the likely M12 move, and it fits the generator pattern we already use |
| **No rate-limit shielding.** Every visitor hits the upstream API directly under our referrer. | M6 at scale | Service worker caching (M9), plus a local JSON cache for the top-100 catalog | Proxy + cache layer, if Open Pet Food Facts ever objects to our traffic |
| **Client-side rendering hurts crawlability.** | Discoverability | The Cat Care Guide — our main SEO surface — is fully static HTML with content in the markup, so this cost lands on product pages only | Pre-generation, as above |
| **No build step means no type checking.** JSDoc types in editors, but nothing enforces them in CI. | Scoring engine correctness | Keep scoring pure and cover it with golden-file tests runnable in the browser and in Node | Add a type-check-only CI job (`tsc --checkJs --noEmit`) without changing what is served |

### How M10 actually resolved (2026-09-05)

This row anticipated linking out to a hosted form, or opening a pre-filled GitHub issue, as a workaround for not being able to accept writes. Building it made clear that the workaround was the wrong shape.

Every score on this site is derived from Open Pet Food Facts. A private submission queue — hosted form, GitHub issue, serverless endpoint, any of them — would fork the catalogue: the product would exist in our queue and still be missing from the database that every score actually reads, and this site would become the bottleneck for its own corrections. Sending the contribution upstream instead means it works here, in the next tool built on the same database, and for the next person who scans the same tin.

So `submit.html` hands off, and its job is to hand off *well*: name the two panels that decide whether a product can be scored at all, and rule out a mistyped barcode — by far the most common cause of "not in the database", and the only one the visitor can fix in five seconds — before sending anyone off to photograph a tin.

**The general lesson, worth keeping:** not every limitation in the table above needs a workaround. This one was better answered by not holding the data at all. Check whether that applies before reaching for the escape hatch.

## Alternatives considered

**Finish the Next.js app and deploy its static export.** Rejected. `next export` would produce a static site anyway, so the runtime capabilities would be identical to what we have — the same client-side scanner, the same client-side fetch. The only real gains are typed components and per-barcode pre-rendering, neither of which is needed in the MVP, and both bought at the price of a build step, a `node_modules` tree, and a CI pipeline that can break the deploy. The current pipeline cannot break the deploy, because it does not build anything.

**Keep both.** Rejected — this is the status quo that caused the confusion.

## Revisit this when

- Contributing upstream stops being the right answer — for instance if Open Pet Food Facts closes to public contribution, or if we need to hold data it will not accept. (M10 did *not* trigger this: see above.)
- We want per-product URLs indexed by search engines, and pre-generation proves insufficient.
- The scoring engine grows past roughly 1,500 lines, where the absence of enforced types starts costing more than the build step would.

Any one of those is a reason to add a build step or a serverless function. None of them is a reason to move off static hosting wholesale.
