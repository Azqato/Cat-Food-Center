# Roadmap

---

## Current phase: MVP — from mock data to a working product

The site is live on GitHub Pages. The Cat Care Guide (M4) and the theme system (M5) are done, and [ADR-001](./ADR-001-static-first.md) settled the architecture question that was blocking everything after them: the site is static HTML by decision, not by default, and the unused Next.js application has been removed.

The mock data is gone. `search.html` and `product.html` now run on live Open Pet Food Facts records scored by a real engine (M6, M7), which is the point at which this stopped being a shell and became a product.

Two things learned in building them shape everything after:

- **The database is thinner than the PRD assumed.** About a fifth of products carry enough data to score all three pillars. Partial data is the normal path, and the engine refuses to score rather than guessing. See [DATA-COVERAGE.md](./DATA-COVERAGE.md).
- **The database is not English.** Only 9.5% of records carry English ingredients, and an English-only matcher reported the rest as clean. Any text check added from here is a language check too.

The barcode scanner (M8) is done — the feature ADR-001 was written to make sure static hosting could still support, and it needed no server, as predicted. So is offline support (M9): the app installs, and a product already looked at stays readable with no signal.

So are the not-found / submit flow (M10) and the compare page (M11). What remains before public beta (M12) is coverage: the API alone will not carry a top-100 SKU catalogue.

Two planned but unscheduled pieces of work sit alongside it: a documentation consolidation audit (M13) and a sitewide move onto the Cat Care Guide's interface (M14).

M13 is not started. It collapses the eleven files in `/docs` to three plus the README, and its full scope is written out below so it survives the session that requested it.

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
| M11: Compare page | 2026-09-05 | Complete |
| M12: Public beta | 2027-01 | Next |
| M13: Documentation consolidation audit | Not scheduled | Planned |
| M14: Unify the site on the Cat Care Guide interface | Not scheduled | Planned |

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
- Precached shell (23 entries at the time, 27 today after M10 and M11 added pages) so every page renders with no network; `offline.html` for anything never visited
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

### M11: Compare page — Complete 2026-09-05
- `compare.html?a=X&b=Y`, sharable and reloadable; products already viewed are offered in a picker, anything else by barcode
- Figures on a dry-matter basis, because that is the only way a wet food at 11% protein and a dry food at 32% can be read against each other
- Pillar-by-pillar, and only where **both** products carry that pillar; the rest are named as not compared

**The thing this page had to get right.** Two scores are not always comparable: a 72 from three pillars and a 72 from one are different claims wearing the same number, and only about a fifth of products carry enough data for all three ([DATA-COVERAGE.md](./DATA-COVERAGE.md)). So the page never declares a winner on the overall score, and where the two were scored on different pillars it says so before showing anything else. Where only one product publishes a figure, neither cell is highlighted — that would be a comment on the database, not on the food.

Two items from the original plan were dropped: sticky column headers (the page is short enough not to need them) and a third column (two products already strain a phone's width, and the honest-comparison rules get harder to state with three).

### M12: Public beta
- Lighthouse CI passing Core Web Vitals targets (LCP ≤ 2.5 s, CLS ≤ 0.1)
- WCAG AA contrast validated
- Top-100 SKU catalog coverage ≥ 80%
- Analytics instrumented (Plausible or equivalent)


### M13: Documentation consolidation audit (Planned, not started)

Requested 2026-09-05. Not scheduled against a date, and deliberately not started: it is recorded here so the scope survives the session it was written in.

**Goal.** Every document in `/docs` accurately reflects the codebase, with no gaps, no stale instructions and no missing coverage, and the whole doc set collapses from eleven files to three plus the README.

**Method, in order.** Steps 1 to 3 are strictly read-only: no writes, no renames, no deletes, no moves, no installers, no formatters, no build that writes output, and no version-control command that changes state. Reads and searches are encouraged. Writing begins at step 4 and is confined to the documentation files named below. No step is skipped for looking obvious, and a step that turns up nothing says so explicitly rather than going quiet.

1. Crawl the whole codebase and build a complete picture: files, features, routes, configs, logic.
2. Open every document in `/docs` and read each one in full.
3. For each document, compare it against the code and identify what is outdated, missing, inaccurate or incomplete.
4. Rewrite or update each document so it is accurate and comprehensive against the current site.
5. Review every file. No document is skipped.
6. Summarise what changed in each file and why.

**Target structure.**

```
/project-root
|-- README.md          <- root only, never inside /docs
|-- LICENSE.md         <- root only, never moved
|-- robots.txt         <- root only
|-- sitemap.xml        <- root by default
`-- /docs
    |-- PRD.md
    |-- DESIGN.md
    `-- PATCHNOTES.md
```

`README.md`, `LICENSE.md`, `robots.txt` and `sitemap.xml` stay at the root and are exempt from the move-into-`/docs` rule. `robots.txt` is root-only as a hard requirement rather than a convention: crawlers fetch it from the origin root and nowhere else, so a copy under `/docs` is an unreferenced text file. A sitemap is scope-limited by its own location, so the root is the position that is always correct; a sitemap elsewhere is valid only where `robots.txt` names it on a `Sitemap:` line, and an audit that finds one elsewhere checks for that line rather than assuming it is broken or moving it. Both apply only because this project actually serves a site.

An existing licence, under any name and in any location, stays exactly where it is and is documented in place. `LICENSE.md` is created only where no licence exists.

**What each of the four documents carries.**

- `README.md` - the public front door, written for a general reader rather than a developer. Name and a one or two sentence description, a link to the live site, what the site offers in plain language, who it is for, current status, and a pointer to `/docs`. No install steps, commands, ports, env vars, build instructions, version numbers or dependency lists: those live in the PRD. It is the one document where brevity wins a tie, because everything it omits is one link away.
- `docs/DESIGN.md` - design philosophy, the full colour palette with hex values and intended use, typography per text role, the spacing scale, every breakpoint and what changes at each, component patterns, accessibility standards, animation and motion rules, and anything else a model needs to understand the design reasoning.
- `docs/PATCHNOTES.md` - semantic version, `YYYY-MM-DD` date, and Added / Changed / Fixed / Removed sections, each line one change in past tense.
- `docs/PRD.md` - the document that absorbs everything else, detailed enough that the whole project is understandable without reading code. Problem statement, target users, goals, non-goals, user stories, MVP and future feature split, constraints, assumptions and success criteria, plus these sections consolidated from the files being retired: Tenets (3 to 7, ordered, each opinionated enough to settle a real tradeoff), Roadmap, Metrics, Runbook, Technical Requirements, Conventions, Writing Style, Browser Testing, Verification Environment, Security, Licensing, Deprecation and Removal, Documentation Versus Reality, Risks and Open Questions, Working Practice, Press Release, and FAQ.

**The rules that govern the rewrite.**

- *Merge, do not overwrite.* Documentation holds intent and rationale that cannot be reconstructed from code. Where a document and the code agree, leave the text alone. Where they contradict, keep the original text, add the observed reality beside it, and mark it as a discrepancy for the author to resolve. Code goes stale as easily as prose does.
- *Every policy below is a default.* Where this project already states a rule on that topic, in its docs, in a consistent code pattern, or in the changelog, document that rule and leave it alone. Adopt a default only where no rule exists, and where a rule and a default differ, keep the rule and flag the difference.
- *Read files rather than inferring from their names.* A guess presented as fact fails the task. Uncertainty is marked as uncertain in the document rather than smoothed over, because a confident sentence outlives the session that produced it.
- *Thorough means more facts, not more words.* A section that restates context to stand on its own is doing its job, because a reader may arrive at it directly. No marketing language, no filler, no sentence that carries nothing the reader did not already have. The README is the exception and stays tight.

**Defaults to adopt where no project rule already exists.**

- *Writing style.* Em dashes prohibited in all three forms: the Unicode character, the `&mdash;` entity, and the double hyphen used as punctuation. The character and the entity must be searched independently, because a search for one will not find the other. CSS custom properties are syntax, not punctuation, and are never touched. Replace each with a comma, colon, semicolon, parentheses, a period, or a single hyphen. The single hyphen is permitted and is the best fit in titles, headings and version lines. Leave any instance a line needs in order to mean anything, such as a rule naming the character it prohibits. Tone is direct and functional. Apply to every document written in the audit, then sweep the rest of the project's text and record in the patch notes how many were found and where. **Note for whoever runs this:** the current doc set uses em dashes heavily and states no rule of its own, so this default applies and the sweep will be large.
- *Browser testing.* Drive Microsoft Edge, never Chrome, and record the resolved binary path in the Runbook, since it differs by platform and is the first thing to break on a new machine. The rule covers ad hoc headless invocations from a script, not only the browser named in a config file. **Note:** `tools/run-tests.py` and `tools/check-live.py` currently launch Playwright Chromium, so this is a change to make, not a rule to document.
- *Verification environment.* Verify locally, never against production, unless the request explicitly asks for a production check. Testing against production means the change has already shipped, so the test can only report what users are already seeing. Confirming a deploy landed is a separate step done after the push, and it is a comparison rather than a test. Never point a destructive or state-changing check at production. Name in the Runbook what differs between local and production and what class of bug can therefore only appear once deployed. **Note:** this project has a real gap of that kind already: `getUserMedia` needs a secure context, so the scanner cannot be exercised over plain `http`, and the site is served from a repository subpath, which a local server at the root does not reproduce.
- *Licensing.* All rights reserved, source-available rather than open source, with a `LICENSE.md` at the root that grants nothing. Required sections: NO LICENCE IS GRANTED (express, implied and estoppel), AI, SEARCH, AND AUTOMATED ACCESS, NO WAIVER, PERMISSION, the platform-terms note, the third-party-data note, NO WARRANTY, and any domain-specific disclaimer. The NO WAIVER clause is load-bearing: declining to act against one use is not a licence, not a precedent and not a waiver, delay does not waive, and any waiver must be written, signed and scoped to the use it names. Referencing is granted to search engines and AI assistants, substitution is not, and training data routes to the request path with a note that it is not usually refused. The licence must not purport to override platform terms, must not claim third-party data, and must not restrict rights that cannot be restricted such as fair use. Never assert a licence without the licence text behind it. **Note:** this project has no licence file at all, so the default applies, and the third-party-data carve-out is not theoretical here: every score is derived from Open Pet Food Facts, which is not ours to license. A veterinary disclaimer is the domain-specific clause this project needs. Permission requests route to the GitHub issue tracker rather than to private email. A `robots.txt` that stays fully open needs a comment marking that as deliberate, with `LICENSE.md` named as authoritative if the two ever disagree.
- *Deprecation and removal.* Whether a removal needs a redirect is decided by whether the thing is public-facing, not by the fact of removal. Public-facing means the deployed artifact and the addresses it serves, and retiring one keeps the old address resolving behind a redirect or equivalent shim. Internal source is a plain delete: no redirect, no alias, no stub, no tombstone, because nothing external points at it. The PRD states where this project puts the deploy boundary, lists the public surface item by item, states whether compatibility entries exist and that they are permanent, never chained and never reused, and records retired items with what replaced them. Historical changelog entries are never rewritten when something is removed.

**Known discrepancies this audit will have to resolve.** Recorded now so they are not rediscovered:

1. Two changelogs exist, `PATCHNOTES.md` at the root and `docs/PATCHNOTES.md`, on different version numbering. The target structure has one, in `/docs`.
2. Eleven documents in `/docs` against a target of three. `TRD`, `RUNBOOK`, `METRICS`, `TENETS`, `SECURITY`, `PRFAQ` and this `ROADMAP` fold into `PRD.md`. `ADR-001-static-first.md` and `DATA-COVERAGE.md` carry findings that exist nowhere else in the project and must be merged rather than dropped.
3. No `LICENSE.md`, no `robots.txt` and no `sitemap.xml` exist.
4. The site is served from a repository subpath on GitHub Pages, which the PRD must state, since the `robots.txt` governing a subpath belongs to the domain owner rather than to this project.

Finally, the audit adds its own changes to `docs/PATCHNOTES.md` and writes this process, and how it is handled going forward, into `docs/PRD.md`.


### M14: Unify the site on the Cat Care Guide interface (Planned, not started)

Requested 2026-09-05. Not scheduled, not started.

**Goal.** Bring the rest of the site onto the interface built for the Cat Care Guide (`learn.html` and the ten `learn-*.html` pages). That look is the one the project wants: the fixed top bar, the grouped sidebar, the article column, the on-this-page rail, the card grid, the callouts, and the four-column footer. The app pages (`index`, `search`, `product`, `scan`, `submit`, `compare`, `methodology`, `offline`) should read as the same site rather than as a second one wearing the same palette.

**The blocker to solve first: the guide top bar has no page navigation.** This is the one thing that has to be ironed out before the chrome can go sitewide, and it is not a detail that can be deferred to the end, because it changes the shape of the bar every page will inherit.

The two bars carry different things today:

| | Guide pages (`cfc.css`) | App pages (Tailwind CDN) |
|---|---|---|
| Sidebar toggle | Yes, hamburger, mobile only | No |
| Brand | Paw mark plus wordmark | Wordmark only |
| Page navigation | **None** | Home / Scan / Search / Compare / Learn / Methodology |
| Search | A link styled as a search field, with a `/` key hint | No |
| Theme toggle | Yes | Yes |
| Support | Yes | Yes |

So the guide bar is better looking and the app bar is better connected, and the merged bar has to be both. Open questions that need an answer before anything is built:

- Where the six destinations sit in a bar that already carries a hamburger, a brand, a search field, a theme toggle and a Support button. That is a lot for a phone at 360px.
- Whether the guide's hamburger and a new primary nav can coexist, or whether one control has to serve both, given the hamburger currently means "guide sections" specifically and would mean something different on a product page.
- Whether the `/` search-field affordance stays on pages that already have a search input in the body, where it would be a second route to the same place.
- What fills the guide shell's three-column grid on a page with no sidebar and no headings to index. A product page has neither a section list nor an on-this-page rail, so it either collapses to one column, which loses the look, or the columns get a purpose, which is a design decision rather than a port.

**Constraints that will shape the work.** These are facts about the codebase, recorded so they are not rediscovered:

- **There are two styling systems, not one.** The eleven guide pages load `assets/cfc.css`, 418 hand-written lines, plus `assets/cfc-docs.js`. The eight app pages load the Tailwind CDN script and `assets/cfc-tailwind.js`, and each one carries its own inline `<style>` block with near-identical utility definitions. Unifying means picking one, and the guide's CSS is the side that already produces the look being adopted.
- **They already share the palette.** `assets/cfc-tokens.css` is loaded by both families, so colour and theme are not part of this problem. `tools/check-contrast.py` covers both and must still pass.
- **The guide pages are generated.** `tools/learn/shell.py` holds the shared chrome and `tools/learn/build.py` writes the eleven files, so the top bar is edited in one place for the guide and in eight places for the app. Whether the app pages join the generator, or the chrome moves into a runtime include, or the duplication is simply accepted, is a decision this milestone has to make and record.
- **There is no build step.** [ADR-001](./ADR-001-static-first.md) still holds, so a shared header cannot be a component import. The realistic options are a Python generator like `tools/learn/`, or an injected header in JavaScript, which costs a flash of unstyled chrome and hurts the pages a crawler reads.
- **`sw.js` precaches an explicit asset list.** Any file added, removed or renamed has to be reflected in `SHELL_ASSETS`, and `tools/check-live.py` asserts the shell cache size, so it will catch a drift but only after the fact.
- **Dropping the Tailwind CDN is on the table and is a real win if taken.** It removes a third-party script from the critical path of every app page, which M12 will be measuring for Core Web Vitals. It is also a large rewrite of eight pages of utility-class markup, so it should be a stated decision rather than a side effect.

**Definition of done.** Every page on the site shares one top bar with working navigation to every destination, one footer, one stylesheet family, and one set of component patterns. `docs/DESIGN.md` describes what was actually built rather than what preceded it. `tools/check-contrast.py`, `tools/run-tests.py` and `tools/check-live.py` all pass, and no page scrolls horizontally at 360px.

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
