# Cat Food Center - Product Requirements Document

**Product:** Cat Food Center
**Tagline:** Trustworthy reviews for your purrfect companion!
**Live site:** https://azqato.github.io/Cat-Food-Center/
**Repository:** https://github.com/Azqato/Cat-Food-Center
**Document type:** Living specification, and the single source of truth for this project. Where this file and the code disagree, that disagreement is recorded in "Documentation Versus Reality" rather than silently resolved.
**Last full audit:** 2026-09-06

This document is deliberately long. It absorbed nine separate documents in the 2026-09-06 audit (TRD, RUNBOOK, METRICS, TENETS, SECURITY, PRFAQ, ROADMAP, ADR-001, DATA-COVERAGE) so that a new contributor, human or model, can understand the entire project without reading code. Sections restate context where a reader might arrive directly. Only three companion documents remain: [README.md](../README.md) at the repository root, [DESIGN.md](DESIGN.md), and [PATCHNOTES.md](PATCHNOTES.md).

---

## Table of contents

1. [Problem statement](#1-problem-statement)
2. [Target users](#2-target-users)
3. [Goals](#3-goals)
4. [Non-goals](#4-non-goals)
5. [User stories](#5-user-stories)
6. [Feature list](#6-feature-list)
7. [Constraints](#7-constraints)
8. [Assumptions](#8-assumptions)
9. [Success criteria](#9-success-criteria)
10. [Tenets](#10-tenets)
11. [The CFC Score](#11-the-cfc-score)
12. [What the data actually contains](#12-what-the-data-actually-contains)
13. [Roadmap](#13-roadmap)
14. [Metrics](#14-metrics)
15. [Runbook](#15-runbook)
16. [Technical requirements](#16-technical-requirements)
17. [Conventions](#17-conventions)
18. [Writing style](#18-writing-style)
19. [Browser testing](#19-browser-testing)
20. [Verification environment](#20-verification-environment)
21. [Security](#21-security)
22. [Licensing](#22-licensing)
23. [Deprecation and removal](#23-deprecation-and-removal)
24. [Documentation versus reality](#24-documentation-versus-reality)
25. [Risks and open questions](#25-risks-and-open-questions)
26. [Working practice](#26-working-practice)
27. [Press release](#27-press-release)
28. [Frequently asked questions](#28-frequently-asked-questions)

---

## 1. Problem statement

Choosing cat food is hard in a way that is not the shopper's fault. The labels are dense and use regulated terms that do not mean what they appear to mean. The marketing is loud and largely unregulated: "grain-free", "natural", "holistic" and "premium" have no binding definitions in pet food. The facts that actually predict feline health are buried in fine print, and evaluating them requires knowing things a shopper has no reason to know, such as that cats cannot synthesise taurine, that a guaranteed analysis is quoted as-fed rather than on a dry-matter basis so a wet food and a dry food cannot be compared directly, or that propylene glycol is prohibited in cat food in the United States but permitted in dog food.

The result is that a person standing in a supermarket aisle with two tins has no practical way to tell which is better, and the sources that promise to tell them are usually selling something.

Cat Food Center answers that question in seconds, shows its work, and refuses to answer when it does not know. It exists for the shopper in the aisle first and the researcher at home second.

The problem it does **not** solve is individual veterinary care. A cat with a diagnosis needs a plan from a veterinarian, and no scoring engine substitutes for that.

---

## 2. Target users

### Persona 1: the aisle shopper (primary)

Standing in a shop, phone in one hand, tin in the other, deciding between two products in under a minute. Cares about a verdict, not a lecture. Often on poor supermarket connectivity, sometimes on none. May never have visited the site before and will not create an account to get an answer.

**Needs:** a fast, legible verdict; a reason attached to it; the ability to scan rather than type; the page to work with a weak signal.

**Design consequences:** mobile is the canvas, not a breakpoint. The barcode scanner exists for this person. Offline support exists for this person, because supermarket aisles have the worst connectivity in the building. The score has to be readable at a glance and at arm's length.

### Persona 2: the researcher (secondary)

At home, comparing several brands before a bulk order, willing to read. Wants the reasoning, the sources, and the ability to put two products side by side. This is the person who reads the methodology page and the Cat Care Guide.

**Needs:** comparison, citations, an explanation of how the score was derived, and enough transparency to disagree with it.

**Design consequences:** the compare page, the methodology page, and the eleven-page Cat Care Guide. Every additive flag cites a source.

### Persona 3: the concerned owner (secondary)

Has a cat with a sensitive stomach, a new diagnosis, or a suspected reaction, and is trying to avoid something specific. Arrives with a question narrower than "is this good".

**Needs:** to find whether a named additive is present; to understand what it does; to be told clearly when the site cannot answer and a veterinarian should.

**Design consequences:** additive flags carry a function, a tier, a plain-language health impact and a source. Every page that touches health carries the veterinary disclaimer. The engine refuses to score rather than guessing, because this reader is the one most damaged by a confident wrong answer.

### Non-user: the brand

Manufacturers are not a user of this product and have no channel to influence a score. This is stated here so that a future "brand portal" idea is recognised as a change to the product's purpose rather than a feature addition.

---

## 3. Goals

1. **A verdict in under 30 seconds** from opening the site to reading a score, for any product in the catalogue, by scanning or searching.
2. **One defensible number per product**, on a 0 to 100 scale, with the reasoning shown and the methodology published.
3. **Honest refusal.** Where the data does not support a score, say so and explain what is missing, rather than producing a number that looks like the others.
4. **Additive flags with evidence.** Every flagged additive carries its function, a risk tier, a plain-language health impact, and a citation.
5. **Work in a shop.** On a phone, one-handed, on a poor connection, and on a product already viewed even with no connection at all.
6. **Educate independently of the score.** The Cat Care Guide is useful to somebody who never looks up a single product.

---

## 4. Non-goals

These are decisions, not gaps. Each is a thing the project has chosen not to do.

- **No e-commerce, affiliate links, or "buy" buttons.** A revenue path that depends on purchases cannot coexist with an honest score. Deferred indefinitely rather than to a version.
- **No personalised diet plans or medical prescriptions.** The site informs; the owner and their veterinarian decide.
- **No user-generated reviews or star ratings.** The value of the score is that it is derived from published evidence rather than sentiment.
- **No dog food.** Cats are obligate carnivores and the scoring model is built on that. A model that works for both would be worse for each.
- **No user accounts, no login, no profiles.** There is nothing the site needs to know about a visitor.
- **No private submission queue.** Contributions go upstream to Open Pet Food Facts. See section 13, M10.
- **No backend service** until a feature genuinely requires one. See section 16 and ADR-001, folded into that section.
- **No EU or FEDIAF nutrient profiles in v1.** United States AAFCO first; EU localisation is a separate compliance effort.
- **No treat-specific scoring rubric in v1.** Treats are not complete diets and need a different model.

---

## 5. User stories

**Scanning and lookup**

- As an aisle shopper, I want to point my camera at a barcode so that I get a verdict without typing anything.
- As an aisle shopper on a desktop or a phone without a working camera, I want to type the barcode digits so that the scanner's absence does not block me.
- As a shopper, I want a mistyped barcode to be identified as a typo so that I do not conclude a product is missing when I entered it wrongly.
- As a shopper, I want a product I have already opened to still be readable with no signal so that walking into a chiller aisle does not lose my answer.

**Searching and browsing**

- As a researcher, I want to search by brand or product name so that I can find a product without its barcode.
- As a researcher, I want to see more than the first page of results so that a search reporting 83 matches gives me access to more than 24 of them.
- As a researcher, I want results ordered by how well they match what I typed so that the ranking answers my question rather than a different one.
- As a researcher, I want to browse by brand so that I can find products without guessing how the database spelled a name.
- As a researcher, I want to hide products that cannot be scored so that I can concentrate on the ones with an answer, while still knowing how many I hid.

**Understanding a product**

- As any visitor, I want the score, the band and a one-line verdict at the top of the page so that I get the answer before I scroll.
- As a concerned owner, I want each flagged additive to carry a function, a tier, a health impact and a source so that I can judge the claim myself.
- As a researcher, I want nutrition figures on a dry-matter basis so that a wet food and a dry food are comparable.
- As a sceptic, I want the methodology published so that I can disagree with the score on its merits.
- As any visitor, I want to be told when the label could not be read so that silence is never presented to me as a clean result.

**Comparing**

- As a researcher, I want two products side by side so that I can see which is stronger and where.
- As a researcher, I want to be told when two scores are not comparable so that I do not read a difference that is not there.

**Contributing**

- As a shopper who found nothing, I want to be told where the data comes from and how to add the product so that the gap can be closed.

**Learning**

- As a new cat owner, I want a sourced guide to feeding a cat so that I can understand the subject rather than only look up products.

---

## 6. Feature list

### MVP: shipped and live

| Feature | Where | Notes |
|---|---|---|
| Home | `index.html` | Scan call to action, search, recently viewed, guide entry point |
| Text search | `search.html` | Live Open Pet Food Facts query, scored on the fly, relevance ordered, paginated |
| Scorable-only filter | `search.html` | Filters the current page and says so; the API cannot filter on scorability |
| Brand browse | `brands.html` | Every cat food brand with more than one product, case variants merged |
| Brand-filtered results | `search.html?brand=` | Uses the `brands_tags` filter with `\|` as OR |
| Product detail | `product.html?barcode=` | Score, verdict, ingredients, additive flags, nutrition, AAFCO adequacy |
| Barcode scanner | `scan.html` | `BarcodeDetector` with a ZXing fallback, plus manual entry |
| Compare | `compare.html?a=&b=` | Two products, pillar by pillar, dry-matter basis |
| Missing product hand-off | `submit.html?barcode=` | Typo check, re-query, then a deep link to Open Pet Food Facts |
| Methodology | `methodology.html` | Public scoring explanation, including what the score cannot see |
| Cat Care Guide | `learn.html` plus ten more | Eleven generated pages |
| Recently viewed | `index.html` | `localStorage` only, never leaves the device |
| Offline and installable | `sw.js`, `manifest.webmanifest` | Precached shell, cached answers labelled as saved copies |
| Light, dark and system theming | Every page | Persisted, applied before first paint |

### Future: not built

| Feature | Milestone | Why not yet |
|---|---|---|
| Curated top-100 SKU catalogue | M12 | The only route to meaningful coverage of common United States products |
| Analytics | M12 | Nothing is measured today. See section 14 |
| "Better alternatives" on a poor product | Backlog | Specified in the original PRD, never built. Needs a same-format query the API supports poorly |
| Pre-generated per-barcode pages | Backlog | For search indexing. The generator pattern already exists |
| EU and FEDIAF profiles | Backlog | Separate compliance effort |
| Treat rubric | Backlog | Treats are not complete diets |
| Dog food | Never in this product | Would need a different engine |

---

## 7. Constraints

**Platform**

- **Static hosting only.** GitHub Pages serves the repository root verbatim. There is no server, no server-side rendering, no dynamic routes, and nowhere to POST. This is a decision, recorded in full in section 16.
- **No build step.** What is committed is exactly what is served. The deploy cannot fail from a compile error because nothing compiles.
- **No Node.js on the maintenance machine.** No npm, no lockfile, no `node_modules`, no bundler, no transpiler. Tooling is Python 3 plus Playwright.
- **Served from a repository subpath**, `https://azqato.github.io/Cat-Food-Center/`, so every path in the site must be relative. An absolute path resolves to the domain root and 404s in production while working locally.
- **Secure context required for the camera.** `getUserMedia` needs HTTPS. `http://localhost` qualifies; `http://<LAN-IP>` does not, so a phone on the local network cannot test the scanner.

**Data**

- **The catalogue is not ours.** Every product fact comes from Open Pet Food Facts, a community-maintained database. Coverage, spelling, and language are outside this project's control.
- **About one product in five carries enough data to score all three pillars.** Partial data is the normal path. See section 12.
- **Only about one record in ten carries English ingredients.** Every text check is therefore a language check. See section 12.
- **No API key exists and none may be introduced** without revisiting the architecture, because anything shipped to a static page is public.

**Budget and staffing**

- Single maintainer, no budget, no paid services. Hosting, the API, and the fonts are all free tiers. Any proposal with a recurring cost needs a reason that survives that fact.

---

## 8. Assumptions

Recorded as assumptions because they are believed rather than proven, and because each one, if false, changes the product.

1. **Open Pet Food Facts will keep serving a public, keyless, CORS-enabled API.** If it closes or starts requiring a key, the browser-direct architecture breaks and a proxy becomes necessary.
2. **Contributing upstream is better than holding our own queue.** Believed strongly, argued in section 13 under M10, and the reason no submission queue exists.
3. **Cat owners act on clear information.** If they do not, no scoring product helps, and this one has no fallback.
4. **AAFCO nutrient profiles are an adequate proxy for feline nutritional adequacy** at the population level. They are the best available public standard, not a guarantee for an individual cat.
5. **A single 0 to 100 number is worth the loss of nuance** it involves, provided the reasoning is one tap away and the refusal path is honest.
6. **The database's coverage of common United States products will not improve on its own** fast enough to reach the M12 target, which is why a curated catalogue is planned.
7. **Scanning is worth building even though most visits will not use it.** It is the defining interaction for the primary persona even if it is a minority of sessions.
8. **Nobody needs an account.** The only per-device state is a recently-viewed list, which `localStorage` holds adequately.

---

## 9. Success criteria

A product-level definition of working. Section 14 carries the measurable targets and how each would be captured.

- A visitor can go from opening the site to a scored product page in under 30 seconds, on a phone, on a supermarket connection.
- The score for a given product is reproducible: the same record produces the same number, and the derivation can be followed on the methodology page.
- Where the engine cannot score, the page says what is missing, and no such product is ever presented with a number.
- No product with a Tier 3 additive can display an Excellent or Good band, regardless of its nutrition.
- The additive knowledge base and the Cat Care Guide agree on every tier. A disagreement between them is a bug.
- The site is usable with no network for any product already viewed, and every cached answer is labelled as a saved copy.
- Nothing about the product's presentation depends on a payment, a partnership, or a brand relationship, because none exist.

---

## 10. Tenets

Ordered. When two conflict, the higher wins. Each is meant to settle a real argument, so each is stated in a form somebody could disagree with.

### 1. Trustworthy before comprehensive

An inaccurate score on ten thousand products is worse than an accurate score on one thousand. Where the data will not support a score, the engine says so and shows a partial-data indicator rather than filling the gap with an assumption. Coverage grows over time; credibility does not come back.

*Settles:* ship a large catalogue quickly, or a smaller verified one. Smaller and verified.

### 2. Silence is not evidence

Where the engine cannot read a label, it says so rather than reporting the absence of a match as the absence of a problem. This is the most important rule in the scoring module, and it was learned expensively: an English-only matcher rated a French product with unnamed meat by-products and added sugar at 77 out of 100 and told the reader its ingredient sources were named. A trust product that confidently misreports is worse than one that admits ignorance.

*Settles:* whether to score a label the engine cannot parse. Never. Say it is unchecked.

### 3. Science beats marketing

The score reflects what matters for feline health: animal protein dominance, taurine sufficiency, additive risk. "Grain-free", "natural", "holistic" and "premium" are ignored entirely unless they correlate with a measurable outcome. A product with excellent marketing and propylene glycol in the list scores Bad.

*Settles:* pressure to treat premium branding as a positive signal. It is not one.

### 4. No revenue path touches the score

No advertiser, sponsor, partner or brand may influence a CFC Score or an additive flag. If money ever enters, it is visually separated and has zero algorithmic effect. This is a hard rule, not a preference revisited when revenue is tight.

*Settles:* "featured" or "boosted" placements. Never.

### 5. The verdict in one second, the reasoning behind it

The score and band are the headline, and every product page decision prioritises showing them before anything else renders. The reasoning is always available and never required in order to get a useful answer.

*Settles:* more data on screen, or a faster verdict. The faster verdict, with the data one scroll away.

### 6. Inform, never prescribe

The site says what is in a product and what the evidence says about it. It does not say what to feed a particular cat. Owners of cats with medical conditions are directed to a veterinarian rather than to a recommendation.

*Settles:* whether to add "best for your cat" personalisation. Not in this product.

### 7. Mobile is the real use case

A rating consulted only at a desk does not change a purchase. Features are designed for store conditions: one hand, poor signal, low patience. If something is comfortable only on a large screen it is a nice-to-have; if it is comfortable only on a phone it ships first.

*Settles:* desktop-only capability versus a mobile-first flow. Mobile first.

---

## 11. The CFC Score

The CFC Score is a 0 to 100 number with a colour band. It is purpose-built for cats, because cats are obligate carnivores: they require animal-sourced taurine and arginine, which they cannot make from plant precursors, and arachidonic acid, which they cannot synthesise from linoleic acid. Human food scoring systems such as Nutri-Score are not appropriate and are not used.

The engine lives in [`assets/js/scoring.js`](../assets/js/scoring.js) and is pure: no network, no DOM, no clock. Given the same product and the same knowledge base it returns the same result, which is what makes it testable and auditable.

### 11.1 Three pillars

| Pillar | Weight | What it measures |
|---|---|---|
| A. Nutritional quality | 55% | Species-appropriate nutrition for cats |
| B. Additives and safety | 35% | Presence and risk tier of flagged additives |
| C. Ingredient quality and transparency | 10% | Named sources, honest labelling |

Weights are declared in `WEIGHTS` in `scoring.js` and must stay in sync with `methodology.html`.

**Renormalisation is the important part.** Where a pillar cannot be computed, its weight is redistributed across the pillars that could be, and the result records which pillars contributed. This is why two scores are not always comparable, and why the compare page refuses to declare an overall winner.

Where too little is known for any honest score, the engine returns `scorable: false` with an explanation. That path is normal, not exceptional: only about a fifth of products carry enough data for all three pillars.

### 11.2 Pillar A: nutritional quality (55%)

Scored on a dry-matter basis wherever moisture is known, because a wet food at 11% protein as-fed is more protein-dense than a dry food at 32%, and comparing the as-fed figures says the opposite.

- **Animal protein dominance.** Whether a named animal protein leads the ingredient list, and the animal-to-plant protein balance. Plant protein concentrates (pea protein, corn gluten meal, soy protein isolate, potato protein) raise the crude protein number without matching biological value for a cat, so they are discounted.
- **A first ingredient whose species is not stated** earns partial credit only, with the reason given. "Meat and animal derivatives" is not the same claim as "chicken", and a parenthetical such as "(including beef 4%)" does not convert one into the other.
- **Essential nutrient sufficiency.** Crude protein and crude fat are checked against the AAFCO adult maintenance minimum on a dry-matter basis (`AAFCO_ADULT_MIN`: 26% protein, 9% fat). Those two are the only profile values the API can ever supply; the full 42-nutrient table lives in the Cat Care Guide.
- **Carbohydrate and filler load.** Lower is better. Heavy grain and starch fillers reduce the score.
- **Moisture.** Wet formats earn a small bonus for supporting hydration and urinary tract health.

### 11.3 Pillar B: additives and safety (35%)

Each ingredient is matched against the knowledge base in [`assets/data/additives.json`](../assets/data/additives.json), version 1.1.0, which currently holds 20 additives and 3 catch-all vague terms. Tiers and evidence match `learn-additives.html` exactly; changing one without the other is a defect.

| Tier | Meaning | Count | Effect |
|---|---|---|---|
| 3 | Documented harm in cats, a regulatory prohibition, or a credible toxicity signal with no established feline safe dose | 8 | Caps the score at 49, the Poor ceiling |
| 2 | A plausible mechanism with incomplete evidence | 7 | Point penalty |
| 1 | Flagged by marketing rather than by evidence | 0 | No penalty |
| 0 | Explicitly benign, so the engine stops penalising things that merely sound synthetic | 5 | Small positive, withheld from unnamed sources |

Propylene glycol carries an additional hard gate: it is prohibited in cat food by the United States FDA, and its presence caps the product in the Bad band (0 to 24) regardless of nutrition.

**Tier 0 credit is matched per ingredient entry and withheld where that entry is itself an unnamed source.** Without that rule, "meat by-products" earned a beneficial bonus for being a named source while the transparency pillar simultaneously penalised the same words for being unnamed.

### 11.4 Pillar C: ingredient quality and transparency (10%)

Named versus unnamed protein and fat sources, and honest labelling. This pillar exists instead of an organic bonus, because organic certification matters far less to feline health than protein quality, transparency and additive load.

### 11.5 Language, and the limits of matching

`MATCHED_LANGUAGES` in `scoring.js` is currently `['en', 'fr', 'de', 'es', 'it', 'nl']`. It is a record of which languages the aliases actually cover and must be extended *with* them, never ahead of them.

Where a label is in a language outside that list, the engine does not report a clean result. It states that the additive and transparency pillars are unchecked, withholds the clean-formulation bonus, caps confidence at low, and emits a warning. Section 12 carries the full account of why.

### 11.6 Hard gates and caps

- **Propylene glycol detected:** capped in the Bad band (0 to 24), regardless of nutrition.
- **Any Tier 3 additive present:** maximum possible score 49, regardless of nutrition.
- **Not complete and balanced:** where a product is not AAFCO complete and balanced for any life stage and is not labelled a treat, snack or complementary food, an adequacy warning is shown.

### 11.7 Score bands

| Band | Range | Light-theme colour |
|---|---|---|
| Excellent | 75 to 100 | `#1B7A4B` |
| Good | 50 to 74 | `#5FA855` |
| Poor | 25 to 49 | `#E08A1E` |
| Bad | 0 to 24 | `#C0392B` |

Colour is never the only signal. Every band carries a text label, and the bands are reserved strictly for ratings.

### 11.8 Confidence

Separate from the score, and reported alongside it:

- **high:** all three pillars computed, from guaranteed-analysis figures.
- **medium:** the default where some but not all conditions for high are met.
- **low:** no usable analysis, or a label in a language the aliases do not cover.

### 11.9 Worked example

A semi-moist food whose first ingredient is corn, with unnamed meat by-products, added caramel colour and propylene glycol: the propylene glycol gate fires, so the product lands in Bad with a "prohibited in cat food" callout before the nutrition arithmetic runs at all.

---

## 12. What the data actually contains

Measured 2026-09-05 by sampling 600 unique products from `categories_tags_en=cat-food` through the v2 search API, six pages of one hundred, fields requested explicitly. Reproduce with `python tools/probe-opff.py`.

> The database is crowd-sourced and moves. Re-run the probe before relying on any number here.

This section exists because M6 and M7 were specified on the assumption that a typical product would carry an ingredient list and a guaranteed analysis, and that the engine would mostly be doing arithmetic. That assumption was wrong in ways that changed the design rather than the error handling.

### 12.1 Headline numbers

| Field | Present | Note |
|---|---|---|
| Product name | 92.2% | Often a brand fragment ("fancy feast") |
| Brand | 88.0% | Sometimes a numeric identifier instead of a name |
| Front image | 96.8% | The best-covered field in the database |
| Quantity | 80.2% | |
| Wet or dry known from category tags | 34.0% | Dry-matter conversion depends on it |
| **Ingredients, any language, over 60 characters** | **38.2%** | |
| Ingredients in English | 9.5% | The database is Europe-weighted |
| **Any protein figure** | **30.8%** | |
| **Protein figure that is plausible** | **23.0%** | |
| Moisture | 15.2% | Required for dry-matter conversion |
| Fibre, either spelling | 24.7% | `crude-fibre` or `fiber` |
| Crude ash | 20.8% | Only via `crude-ash`; `ash` is never used |
| Taurine | 4.3% | |
| **Ingredients and protein and fat together** | **22.3%** | Both schemas counted |

About one product in five carries enough data to score the way section 11 describes.

### 12.2 Two competing nutriment schemas

Open Pet Food Facts inherits Open Food Facts' human-food nutriment keys, but pet food uses guaranteed-analysis keys. Both appear, and mostly not together.

| Schema | Keys | Products |
|---|---|---|
| Guaranteed analysis | `crude-protein`, `crude-fat`, `crude-fibre`, `crude-ash`, `moisture` | 116 crude only |
| Human food | `proteins`, `fat`, `fiber`, `carbohydrates`, `salt` | 55 human only |
| Both | | 14 |
| Neither | | 415 |

`ash` does not exist; it is always `crude-ash`. `fibre` is British-spelled in the crude schema and American-spelled in the human one. A normaliser must read both spellings of both schemas.

### 12.3 Implausible values

Twenty-five per cent of products carrying a protein figure carry an implausible one (47 of 185), and the failure is systematic rather than random: human-food keys are frequently filled with per-serving or per-can values while labelled `_100g`.

| Product | Protein/100g | Fat/100g | kcal/100g | What is wrong |
|---|---|---|---|---|
| Gourmet `7613034452481` | 1.2 | 0.3 | 2 | A wet cat food is roughly 8 to 12% protein and 70 to 90 kcal/100g. These are per-gram |
| Sheba `4770608247027` | 1.6 | 0.9 | 8 | Same pattern |
| Hill's `0052742869605` | 28.7 | 22.05 | **1774** | Composition right for a dry food; energy is per kilogram |
| Vitakraft `4008239352873` | 0.75 | 2.05 | 48.3 | Fat exceeds protein threefold, which is not a cat food |

The `crude-*` values are consistently sane because they are transcribed from the packaging panel. Trust `crude-*`; treat human-food keys as a low-confidence fallback that must pass a plausibility gate.

### 12.4 Language is a correctness problem, not a translation problem

Only 9.5% of records carry `ingredients_text_en`, so the ingredient list is usually French, German, Spanish, Italian or Dutch.

Every text check in the engine is alias matching against an ingredient string. An English-only alias list does not fail on a French label. It matches nothing, and matching nothing is indistinguishable, to the code, from a clean label.

Barcode `3596710487455` (Auchan, French) exposed this:

```
Viandes et sous-produits animaux (dont boeuf 4% et foie 4%), céréales,
légumes (3% de carottes et 2% de haricots verts), substances minérales, sucres
```

Unnamed meat by-products as the main ingredient, and added sugar at the end. It scored **77 / Excellent**, with a transparency pillar of 100 and the reason "Ingredient sources are named rather than generic". Every word of that was wrong, in the most damaging possible direction. It now scores **70 / Good**, flags the sugar, flags the unnamed source, and states that the species of the first ingredient is not given.

Four defects sat behind that one score, and three were not about language at all:

| Defect | Fix |
|---|---|
| Aliases were English-only, so roughly 90% of labels silently matched nothing | French, German, Spanish, Italian and Dutch aliases in `additives.json` and in the protein and starch lists in `scoring.js` |
| A label in an uncovered language was still reported as clean | The `MATCHED_LANGUAGES` guard: silence is stated as unchecked, the bonus is withheld, confidence is capped at low, and a warning explains it |
| `named-by-products`, a Tier 0 beneficial entry, had bare stems as aliases, so "meat by-products" earned a bonus for being a named source while transparency penalised the same words for being unnamed | Tier 0 credit is matched per ingredient entry and withheld where that entry is itself an unnamed source |
| A parenthetical renamed an unnamed source: "(dont boeuf 4%)" made the entry read as a named beef first ingredient | Entries matching an unnamed-source term are judged on the text before the parenthesis, across the whole leading window |

The third and fourth were live in English too. They had never fired because no English product had reached the renderer.

### 12.5 Consequences for the design

1. **The normaliser reads both schemas**, prefers `crude-*`, and records which it used. Provenance is not optional.
2. **A plausibility gate runs before scoring.** Protein 3 to 50%, fat 0.5 to 40%, fibre 0 to 15%, ash 0 to 15%, moisture 0 to 92%, energy 15 to 600 kcal/100g. Outside those, the figure is discarded rather than scored.
3. **Energy needs unit inference.** A kcal/100g value above 600 is almost certainly per kilogram; it is corrected and flagged.
4. **Partial scoring is the primary path**, not a degraded one.
5. **A 0 to 100 score is not comparable across products with different completeness.** Either show which pillars were computed, or show confidence alongside the number. The compare page does both.
6. **Wet versus dry is known for only 34% of products.** Where moisture is present it can be inferred; where neither is present, dry-matter comparison is impossible.
7. **The M12 top-100 target will not be met by the API alone.** It requires a curated local catalogue under `assets/data/`.
8. **Any text check is a language check.** A new alias list is not complete when it is complete in English.
9. **Silence is not evidence.** See tenet 2.
10. **Render real products early.** The unit suite was 109 assertions green while all four defects were live, because every fixture was English and written by the same person who wrote the matcher. One real page found what the whole suite could not.

### 12.6 Practical API notes

- Base: `https://world.openpetfoodfacts.org/api/v2/`
- No API key. CORS is permissive, so the browser calls it directly.
- A descriptive `User-Agent` is the documented courtesy, but it is a forbidden header in browser `fetch`, so only `tools/probe-opff.py` sends one.
- Always pass `fields=`. A full record is 103 keys, mostly editorial metadata.
- `GET /product/<barcode>.json` returns HTTP 404 with `status: 0` for an unknown barcode. A miss is common and is not an error.
- The brand facet at `https://world.openpetfoodfacts.org/facets/categories/Cat%20food/brands.json` is CORS-enabled and lists 439 cat food brands with counts. Nine of those collide on case alone (`purina` at 110 products and `Purina` at 15 are the same brand).
- In v2 tag filters, a comma means AND and `|` means OR. `brands_tags=purina|Purina` returns 125, which is how merged brands are queried in one request.
- **`/api/v2/search` accepts `search_terms` and ignores it.** Verified 2026-09-07: `search_terms=chicken`, `search_terms=salmon`, `search_terms=zzzzqqq` and no search terms at all return the same `count` of 1578 and the same products in the same order, which is the whole cat-food category. There is no error and no warning; the response is well formed and simply unrelated to the query. Tag filters on the same endpoint work correctly, which is why a brand-only browse still uses it.
- **`/cgi/search.pl?action=process&json=1` is the endpoint that actually searches text.** It honours `fields`, `page` and `page_size`, returns a truthful `count` (`salmon` 32, `tuna` 22, `chicken` 83), serves consecutive pages without overlap, and sends `Access-Control-Allow-Origin: *`. Its tag filters are numbered rather than named: `tagtype_0=categories&tag_contains_0=contains&tag_0=cat-food`, with a brand as pair 1.

---

## 13. Roadmap

### Current phase

MVP, live and running on real data. Search, brand browse, product pages, scanning, comparison, offline support and the Cat Care Guide are all shipped. What stands between here and a public beta is coverage: the API alone will not carry a top-100 SKU catalogue.

### Milestone table

| Milestone | Target | Status |
|---|---|---|
| M0: Project scaffold | 2026-06-07 | Complete |
| M1: MVP static shell | 2026-06-07 | Complete |
| M2: Documentation audit | 2026-06-08 | Complete |
| M3: Methodology page | 2026-06-08 | Complete |
| M4: Cat Care Guide | 2026-09-05 | Complete |
| M5: Dark mode with a persisted preference | 2026-09-05 | Complete |
| M5.5: Architecture decision and Next.js removal | 2026-09-05 | Complete |
| M6: Data layer, Open Pet Food Facts | 2026-09-05 | Complete |
| M7: Scoring engine | 2026-09-05 | Complete |
| M8: Barcode scanner | 2026-09-05 | Complete |
| M9: Service worker and PWA offline | 2026-09-05 | Complete |
| M10: Not-found and submit flow | 2026-09-05 | Complete |
| M11: Compare page | 2026-09-05 | Complete |
| M13: Documentation consolidation audit | 2026-09-06 | Complete |
| M15a: Search logic and brand browse | 2026-09-06 | Complete |
| M14: One interface across the whole site | 2026-09-06 | Complete |
| M15b: Product photos on cards | 2026-09-06 | Complete |
| M15c: Ingredient explanations | 2026-09-06 | Complete |
| M15d: Client-built product page rail | 2026-09-06 | Complete |
| M16a: WCAG 2.1 AA gate | 2026-09-06 | Complete |
| M16b: Core Web Vitals gate | 2026-09-07 | Complete |
| M17: Blink, Gecko and WebKit | 2026-09-07 | Complete |
| M18: Search that searches | 2026-09-07 | Complete |
| M12: Public beta | 2027-01 | Planned |

### What shipped, and what was learned

**M0 to M3.** Next.js scaffold, static shell, the first documentation suite, and the methodology page.

**M4: the Cat Care Guide.** Eleven pages at `learn.html` and `learn-*.html`, generated from `tools/learn/` so the shared chrome cannot drift. Content covers nutrition fundamentals, the complete AAFCO daily requirement for all 42 nutrients with worked per-day amounts, label reading, food formats, hydration, a tiered additive reference, feeding practice, life stages, toxic foods, and diet in common conditions.

**M5: theming.** Palette extracted to `assets/cfc-tokens.css` so both page families share it. Dark values are written twice, once under `[data-theme="dark"]` and once under `prefers-color-scheme`, and `tools/check-contrast.py` fails if the two drift apart. The theme script is blocking in `<head>` so the stored preference applies before first paint.

*Learned:* dark mode surfaced an existing accessibility defect rather than causing one. The green and amber chips had been using white text at 2.8:1 and 2.3:1 in the light theme. They now use dark ink.

**M5.5: ADR-001, static HTML is the architecture.** The repository had been carrying an unused Next.js application alongside the HTML that actually shipped, and the README described Next.js as the stack, which was wrong about what users load. The full decision is in section 16.

**M6 and M7: the data layer and the scoring engine.**

*Learned, and it changed the product:* the plan assumed English labels. Only 9.5% are. Section 12.4 carries the full account. Four defects, one live score of 77/Excellent on a product that deserved 70/Good with three flags.

**M8: the barcode scanner.** `BarcodeDetector` where the platform has it, ZXing downloaded on demand where it does not. Every failure mode gets its own sentence, because "could not start camera" would be accurate and useless.

*Learned:* UPC-E has its own checksum rule and must be expanded to UPC-A before validation. Checking it as if it were EAN-8 would have made the scanner appear never to see small United States packages, with no error anywhere. And the secure-context requirement means `http://<LAN-IP>` has no camera at all, so testing from a phone on the local network fails in a way that looks like broken code.

**M9: offline and installable.** Hand-written service worker, three strategies, each chosen per resource with the reason in the file.

*The rule that shaped it:* a cached score must never be presented as a current one. The worker stamps anything served from cache, `opff.js` carries the stamp through, and the page says it is showing a saved copy. Navigations are deliberately not cached, because every product is the same document under a different query string; the precached document is found with `ignoreSearch` instead. A 404 is never cached, because it is how an unknown barcode is detected.

**M10: the missing-product hand-off.** Checks the barcode against its own check digit and re-queries the database before sending anyone off to photograph a tin.

*The decision worth keeping:* there is no submission queue of our own, by choice. A private queue would fork the catalogue: the product would sit in our queue and still be missing from the database every score actually reads, making this site the bottleneck for its own corrections. ADR-001 had predicted a hosted form as the workaround for not accepting writes; building it showed the workaround was the wrong shape. The general lesson: not every limitation needs a workaround, and this one was better answered by not holding the data at all.

**M11: the compare page.** Two products, dry-matter basis, pillar by pillar.

*What it had to get right:* a 72 from three pillars and a 72 from one are different claims wearing the same number, and only about a fifth of products carry all three. So the page never declares a winner on the overall score, and where only one product publishes a figure, neither cell is highlighted, because that would be a comment on the database rather than on the food. Sticky column headers and a third column were dropped: the page is short enough not to need the first, and the honest-comparison rules get harder to state with the second.

**M13: this audit.** Eleven documents in `/docs` consolidated to three plus the README, with `LICENSE.md`, `robots.txt` and `sitemap.xml` added at the root for the first time.

**M15a: search logic and brand browse.** Prompted by owner feedback on the live site: "The search doesn't really work at all. Just see what catfooddb is like. That's a lot better. There's no photo either."

Five separate causes were confirmed. There was no pagination at all, so 24 of 1571 results were reachable and nothing led to result 25. The API's relevance ranking was discarded by a scorable-first re-sort, so the closest match to what somebody typed could sit below a loosely related product that happened to score well. The match is not restricted to name or brand, so "chicken" returned ocean fish above real chicken products. The records themselves carry numeric brand identifiers and untranslated names, rendered faithfully. And there was no filter, facet, sort or brand browse to compensate.

Pagination, relevance ordering and a scorable-only filter shipped, along with `brands.html`.

*Two of those five diagnoses were wrong, and M18 found out why.* The 1571 figure and the "chicken returns ocean fish" observation were both readings of a result set that had nothing to do with the query: `/api/v2/search` was ignoring `search_terms` entirely and returning the whole cat-food category every time. The ranking was not loose, it was absent, and the count was not the number of matches, it was the size of the category. The paragraph above is left as it was written because it is an accurate record of what was believed in M15a; section 24.1 carries the correction.

*The useful observation about the reference site:* CatFoodDB is organised brand-first, with an A to Z of over 150 brands and curated best-of lists by food type, and its own free-text search is disabled, with a notice on the site saying so. The site the owner preferred is better *without* working search, which suggests the answer is a browse structure rather than a better ranker. Its individual product entry layout has not been verified: two attempts at brand and best-of URLs returned 404.

**M14: one interface across the whole site.** The nine application pages moved onto the interface built for the Cat Care Guide, and stopped being hand-written.

`tools/site/chrome.py` is now the single copy of the head, top bar, drawer and footer, and `tools/learn/shell.py` imports it, so the two page families cannot drift. `tools/site/build.py` wraps that chrome around a body fragment per page. The Tailwind CDN, `assets/cfc-tailwind.js` and the nine per-page `<style>` blocks are gone, replaced by `assets/cfc-app.css`, which defines only the utilities the page modules actually emit and the components they build.

The navigation question that had blocked the milestone was answered as decided: links inline in the bar above 900px, folded into the existing drawer below it, with a guide page's section list nested beneath the site links. One control, two levels.

*Learned, and it is the reason to port rather than restyle:* the defects the port exposed were not in the pages being ported, they were in the shell those pages moved into, and both were invisible while only guide pages used it. `.article a { color: var(--accent) }` outranks any component that colours its own anchor from a single class, which rendered the home page's round scan button as accent text on an accent circle. And the drawer is a grid child, so hiding it on only one of the two application shells left it holding a column on the other and pushing the article onto the next grid row, which rendered `methodology.html` as a blank screen. A shell used by one kind of page has not been tested, it has been exercised.

*The smaller lesson:* `.text-display` was defined in nine places and meant 3rem in all of them. Consolidating nine copies into one is where a value silently becomes something else, so the port was checked by diffing every rule in the old inline blocks against the new stylesheet rather than by reading the pages.

**M15b: product photos.** A picture of the tin on every result card, on each
side of the compare page, and on recently viewed. It closes the last unanswered
half of the owner's feedback on the live site: "There's no photo either."

`opff.js` had been fetching `image_front_url` since M6 and only
`product-page.js` rendered it, so this was rendering work rather than plumbing.
The 200px rendition is used for the 56px boxes; the 400px one stays on the
product page.

*The decision that shaped it:* every card gets a box whether or not the product
has a photo, and the empty box holds a paw outline. Coverage is good but not
complete, and a list where some rows carry an image and some carry nothing is
visibly ragged in a way that reads as a rendering fault rather than as missing
data. The same placeholder is what a photo that fails to load is replaced with,
through one delegated listener rather than an `onerror` attribute: there is no
inline event handler anywhere else in this codebase, and adding the first one
would be the only thing standing between the site and a Content-Security-Policy
header.

*Found while building it:* the service worker asked `isApi(url)` before
`isImage(request)`, and product photos are served from
`images.openpetfoodfacts.org`, which `isApi` matches. Every image was therefore
taking the network-first path into the API cache: revalidated on every view
when the bytes never change, and counted against the wrong cache. It was
invisible while one photo existed on one page. Putting a photo on every card is
what made the ordering matter, and the fix is one swapped block.

**M15c: ingredient rows that explain themselves.** An ingredient the additive
knowledge base recognises opens to show what it is for, what it does to a cat,
what the regulator says, and the sources. Everything else stays a plain row.

*What the documentation got wrong:* both this document and DESIGN.md had
recorded, for three milestones, that "the chevron is rendered but inert" and
that a control which does not respond is worse than no control. The chevron was
never rendered. The string does not appear in any commit's code. The entry was
not stale, it was wrong in a direction that made the project look worse than it
was, and it survived because nobody checked a claim that sounded like a
confession. Section 26.1 already says never to assume a documented behaviour
exists; it is worth saying that the same applies to documented defects.

*The scope decision:* this is not a general ingredient dictionary. It answers
for the 20 additives and 3 vague-term groups the scoring engine already reasons
about, and returns nothing for everything else. There is no true thing this
project can add to the word "chicken", and padding every row with filler would
bury the rows that matter.

*What it had to get right:* the explanation and the score cannot disagree. The
engine withholds Tier 0 credit from an entry that is itself an unnamed source,
because one ingredient cannot be both a named organ meat and an unnamed one.
"Viandes et sous-produits animaux" matches the beneficial named-by-products
entry on a bare stem while the transparency pillar penalises the very same
words. The first build of this feature labelled that row "Beneficial" while the
score was penalising it, which is the exact failure the page exists to avoid. It
now reports the same call the engine made, and a test pins it.

**M16a: the WCAG 2.1 AA gate.** `tools/check-a11y.py`, described in section 19.1. Four real defects, and a lesson about the tool rather than the site.

*The defects:* every link in running text was accent-coloured with no underline, which is WCAG 1.4.1 and was on all 25 pages, because accent against body copy is 1.53:1 in light and 1.16:1 in dark and colour alone needs 3:1. The search pager's unavailable direction carried `opacity: .45`, putting it at 2.11:1, the one piece of text on the site below AA. The compare page needed 490 pixels at a 320px viewport, because a bare `1fr` grid track will not shrink below its content and a product name from a community database can be one unbroken token. And there was no site-wide focus ring or reduced-motion rule at all: both had been left to the browser on a site with two palettes and custom card components.

*The lesson:* the first two runs of the tool reported failures that did not exist. Setting `data-theme` and auditing in the same tick measures colours part-way through a 150ms transition, so the whole top bar came back as a dark-mode contrast failure; tabbing and reading the skip link's box in the same tick catches it mid-slide, so it came back off-screen on every page. Both were the tool, not the site. A new gate's first red is as likely to be the gate as the code, and shipping a "fix" for either of those would have been a change made to satisfy a measurement error.

*What the gate deliberately does not claim:* axe covers the machine-checkable third of WCAG. Section 19.1 lists what was checked by hand alongside it, with the answers, so that a green run is never read as "the site is accessible".

**M16b: the Core Web Vitals gate.** `tools/check-vitals.py`, described in section 19.2. One defect, and it was on most of the site.

*The defect:* six of the nine application pages render their body from a fetch, so each is briefly a placeholder in a short page with the footer visible underneath it. When the content arrived the footer dropped, and that is a layout shift of something the visitor was already looking at. The brand index measured 0.60 against a 0.10 budget, a page of search results 0.86, the product page 0.64. `.shell` now has `min-height: 100vh`, which keeps the footer below the fold until there is content to push it there, and the brand list reserves a screen of height while it loads and gives it back in `render()`. Every gated page is now at or below 0.07, and most are at 0.000.

*Why this was invisible for eleven milestones:* CLS is not visible on a fast connection, because the placeholder and the content arrive close enough together that nothing appears to move. It needs a throttle to see at all, and the project had no throttled measurement until this one.

*Also added:* `preconnect` for the two Open Pet Food Facts origins, so the handshake overlaps with parsing on the pages that call the API, and `sw.js` went to `v3` because M16a's stylesheet fixes were served stale-while-revalidate and would otherwise have reached returning devices one visit late. A contrast fix that arrives on the second visit has not really been deployed.

**M17: Blink, Gecko and WebKit.** `tools/check-engines.py`, described in section 19.3. It closes open question 7, which had stood since the M13 audit.

*What it found:* nothing broken, and one thing understated. Every page renders in all three engines, the unit suite is 178 passing in all three, and nothing overflows at either width anywhere. `scanner.js` already called `BarcodeDetector` support "partial, Safari and Firefox largely not", which was the right instinct; measured, it is absent from both engines rather than partial, so on every browser on iOS ZXing is not a fallback but the whole feature. The decode round-trip now runs in all three engines and passes in all three.

*What it cannot say:* headless WebKit exposes no `getUserMedia`, which is a property of Playwright's build rather than of Safari. Real Safari camera behaviour is still untested by anything, and no tool in this repository can change that.

*Why this was worth doing before the catalogue:* the coverage gap was not that a defect was suspected, it was that no evidence existed either way. A green result is a finding.

**M18: search that searches, and a filter that scans.** Two changes, and the second uncovered the first.

*The intended change* was open question 4: the scorable-only filter acted on the twenty-four results already on screen, so it could show three products and imply that was all there were. It now scans the first five pages of the query in parallel, dedupes by barcode, filters, and paginates what it holds locally. The count it prints says exactly what it scanned: "the 12 products in all 32 results" when the scan reached the end, and "the first 120 of 1578 results" when it did not, with a note at the foot of the last page saying the scan stopped there. Five pages is a deliberate ceiling: it is one round of parallel fetches, and a filter that hunted until it found enough would take an unbounded number of requests to produce a number nobody could state honestly.

*What testing it uncovered* is the larger finding. `zzzzqqq` returned 1578 products. `/api/v2/search` accepts `search_terms`, returns HTTP 200, and ignores the parameter: every query returned the entire cat-food category in the same order. Text search on this site had never searched anything since M6, and M15a diagnosed the symptoms of that as a ranking problem and a field-matching problem, which is what they look like from outside. Text queries now go to `/cgi/search.pl`, verified against the same three probes; brand-only browses stay on v2, whose tag filters were never affected.

*Learned:* a well-formed 200 with plausible data is the hardest kind of wrong to notice. Six gates, 178 assertions and a live check all passed over this for eleven milestones, because every one of them asked whether results came back rather than whether they were the right results. The assertion that would have caught it is the one nobody writes: search for a string that cannot match, and require nothing back. `tools/check-live.py` now writes it, along with a second asking that a majority of the cards on a `salmon` search mention salmon. A result set that ignores the query lands nowhere near either bar, and no other check in this repository would have noticed.

### Next

**M12: public beta.** Core Web Vitals targets met (done, M16b), WCAG AA validated (done, M16a), top-100 SKU coverage at 80% or better, and analytics instrumented. Coverage is the only one of the four that is still open, and it is the one the API cannot deliver on its own.

### Explicitly deferred

| Feature | Reason |
|---|---|
| Dog food | Requires a separate engine; cats first, to ship a correct product rather than a broad one |
| User accounts | No user data in v1; infrastructure with no v1 value |
| User-generated reviews | Trust risk; editorial and algorithmic scoring ships first |
| Personalised diet plans | Out of scope by tenet 6: we inform, we do not prescribe |
| E-commerce and affiliate links | Conflicts with tenet 4; deferred indefinitely |
| Backend API | Not needed until something genuinely requires a write |
| EU and FEDIAF profiles | AAFCO first; EU localisation is a separate compliance effort |
| Treat-specific rubric | Treats are not complete diets |
| Sticky compare headers, third compare column | Dropped in M11; see above |

---

## 14. Metrics

**Nothing on this list is currently instrumented.** The site has no analytics, no error reporting and no uptime monitor. Every target below is a stated intention for M12, not a measurement, and this section should not be read as reporting on anything. That gap is deliberate for now (no analytics means no visitor data to protect) but it does mean the product's actual usage is unknown.

### North star

**Scan-to-verdict completions per week:** the number of times a visitor reaches a product page carrying a score, whether by scan or by search. It is the single number that best represents the product working, because it means somebody got an answer.

### Acquisition

| Metric | Target | Timeframe | Method |
|---|---|---|---|
| Weekly active users | 500 | 3 months post-launch | Plausible or equivalent |
| Organic search traffic | 40% of sessions | 6 months | Google Search Console |
| Direct and shared traffic | 20% of sessions | 3 months | Analytics |
| PWA installs | 100 | 3 months | `beforeinstallprompt` event |

### Engagement

| Metric | Target | Timeframe | Method |
|---|---|---|---|
| Scan-to-verdict completions | 1,000 per week | 3 months | Product page views with a score |
| Scan success rate | 90% or better | Post-launch | Custom event |
| Time to verdict | 30 seconds or less, median | Post-launch | Custom timing event |
| Search-to-result rate | 60% or better | 3 months | Search to product funnel |
| Product pages per session | 1.5 or better | 3 months | Analytics |

### Retention

| Metric | Target | Timeframe | Method |
|---|---|---|---|
| Week-1 retention | 20% or better | 3 months | Analytics cohort |
| Pre-purchase return visits | 15% of weekly actives | 6 months | Session patterns |
| PWA session rate | 10% of mobile sessions | 6 months | `display-mode: standalone` |

### Performance

| Metric | Target | Method |
|---|---|---|
| Largest Contentful Paint | 2.5 s or less, mid-range phone on 4G | `tools/check-vitals.py`, throttled. **Measured**, section 19.2 |
| Total Blocking Time | 200 ms or less | `tools/check-vitals.py`. **Measured.** Stands in for INP, which needs a real session |
| Interaction to Next Paint | 200 ms or less | Field data only. Nothing measures this; there is no analytics |
| Cumulative Layout Shift | 0.1 or less | `tools/check-vitals.py`. **Measured**, section 19.2 |
| Uptime | 99.9% or better | GitHub status |
| Deploy success rate | 99% or better | GitHub Actions |

### Coverage

| Metric | Target | Timeframe | Method |
|---|---|---|---|
| Top-100 United States SKU coverage | 80% or better | 6 months | Manual audit against retail data |

### Reporting cadence

| Group | Cadence |
|---|---|
| North star and engagement | Weekly |
| Acquisition and retention | Monthly |
| Performance | Monthly, automated once Lighthouse CI exists |
| Coverage | Monthly |
| Documentation against reality | Every audit; see section 24 |

---

## 15. Runbook

Everything needed to run the project. The README deliberately carries none of it. Assume the reader has just cloned the repository and has nothing else.

### 15.1 Prerequisites

| Requirement | Version | Needed for |
|---|---|---|
| A browser | Any modern one | Viewing and editing the site. Nothing else is required for this |
| Git | Any | Cloning and deploying |
| Python | 3.8 or newer | The guide generator, the contrast checker, and the test runners |
| Playwright for Python | Any recent | `run-tests.py` and `check-live.py` only |
| Microsoft Edge | Any current | The browser those two tools drive. See section 19 |

There is no Node.js, no npm, no lockfile, no `node_modules` and no environment variables. Installing Playwright is the only package step:

```bash
pip install playwright
```

Playwright's own browser download is **not** needed, because both tools drive the installed Edge through the `msedge` channel rather than a bundled Chromium.

### 15.2 Local setup

```bash
git clone https://github.com/Azqato/Cat-Food-Center.git
cd Cat-Food-Center
python -m http.server 8000
```

The site is then at **http://localhost:8000**. Default port 8000; nothing depends on that number.

There is no hot reload. Refresh the browser.

Opening the files with `file://` works for most pages but breaks two things: `fetch` of local JSON is blocked by CORS, so anything reading `assets/data/` needs the server, and the barcode scanner needs a secure context.

### 15.3 Build

**There is no build step for deployment.** What is committed is what is served.

Three generators run locally with their output committed:

```bash
python tools/site/build.py       # regenerates the nine application pages
python tools/learn/build.py      # regenerates the eleven learn*.html pages
python tools/check-contrast.py   # audits both palettes against WCAG AA
```

**Every HTML page at the root except `tests.html` is generated, and hand-edits to any of them are silently undone on the next build.** For a guide page, edit `tools/learn/c_<page>.py`. For an application page, edit `tools/site/content/<name>.html`. For anything in the head, the bar, the drawer or the footer of either family, edit `tools/site/chrome.py`, which both generators import.

### 15.4 Commands

| Command | What it does |
|---|---|
| `python -m http.server 8000` | Serve the site locally |
| `python tools/run-tests.py` | Run the browser-hosted suite headlessly. 178 assertions. Exits non-zero on failure, so it works as a gate |
| `python tools/check-live.py` | 19 end-to-end checks against the live API, two of them added in M18 to ask whether the search searches. Needs network. Not deterministic, so it is a smoke check rather than a gate |
| `python tools/check-contrast.py` | Verify 38 foreground and background pairs against WCAG AA in both palettes |
| `python tools/check-a11y.py` | WCAG 2.1 AA audit of all 25 page states in both themes, plus reflow at 320px and the skip link. 100 audits. Exits non-zero, so it works as a gate |
| `python tools/check-a11y.py --report` | The same audit, printing every violation with its selector, and exiting 0 |
| `python tools/check-vitals.py` | LCP, CLS and TBT for 12 pages, CPU throttled 4x on a slow-4G connection. Exits non-zero, so it works as a gate |
| `python tools/check-vitals.py --report` | The same run, naming the elements that shifted, and exiting 0 |
| `python tools/check-engines.py` | The unit suite, all 12 page states and the barcode decode round-trip in Blink, Gecko and WebKit. Needs network, and `python -m playwright install webkit firefox` once |
| `python tools/site/build.py` | Regenerate the nine application pages |
| `python tools/learn/build.py` | Regenerate the eleven Cat Care Guide pages |
| `python tools/probe-opff.py` | Re-measure the database behind section 12 |

### 15.5 Deploy

Every push to `main` triggers `.github/workflows/deploy.yml`:

1. `actions/checkout@v4`
2. `actions/upload-pages-artifact@v3` with `path: .`, uploading the repository root
3. `actions/deploy-pages@v4`

It builds nothing, so it cannot fail the way a build pipeline can. If a deploy fails, the cause is GitHub Pages or the workflow configuration, not the code.

Live URL: **https://azqato.github.io/Cat-Food-Center/**
Deploy log: **https://github.com/Azqato/Cat-Food-Center/actions**

**Manual redeploy** without a code change: Actions, then the "Deploy to GitHub Pages" workflow, then Run workflow. The `workflow_dispatch` trigger exists for this.

**One-time setup for a fork:** create the repository, set Settings, Pages, Source to GitHub Actions, and push to `main`. Nothing needs configuring for the repository name, because every path in the site is relative.

### 15.6 Rollback

**Preferred: revert the commit.**

```bash
git log --oneline -10
git revert <bad-commit-hash>
git push origin main
```

The revert push triggers a new deploy automatically.

**There is no "redeploy the previous run" button.** Reverting the code is the mechanism.

**Force-push is an emergency measure only** (`git reset --hard <good>` then `git push --force origin main`), acceptable only where a revert will not apply cleanly and losing history is acceptable.

### 15.7 Environments

| Environment | URL | Deployed by | Differences |
|---|---|---|---|
| Local | http://localhost:8000 | `python -m http.server` | Served from the domain root, not a subpath. No HTTPS |
| Production | https://azqato.github.io/Cat-Food-Center/ | GitHub Actions on push to `main` | Served from a repository subpath, over HTTPS |

There is no staging environment.

**Where local and production genuinely differ**, which matters because a bug can hide in the gap:

| Difference | Class of bug it hides |
|---|---|
| Local serves from `/`, production from `/Cat-Food-Center/` | An absolute path (`/assets/...`) works locally and 404s in production. This is the single most likely production-only failure |
| Local is `http://localhost`, production is HTTPS | `localhost` is a secure context, so the camera works locally. A LAN IP is not, so a phone on the local network cannot test the scanner at all |
| The service worker caches aggressively in production over many visits | A stale shell can persist on a real device in a way a fresh local profile never reproduces. `VERSION` in `sw.js` is the lever |
| Local has no CDN | A Pages CDN cache can serve an old file for a few minutes after a successful deploy |

### 15.8 Environment variable reference

**There are none, by design.** Anything shipped to a static page is public, so the project uses only keyless APIs. If a future feature needs a secret, that is a trigger to revisit the architecture (section 16), not to add a variable.

### 15.9 Common errors

| Error | Likely cause | Fix |
|---|---|---|
| An edit to a page at the root disappeared | Every root page but `tests.html` is generated and a build overwrote it | Edit `tools/site/content/<name>.html` or `tools/learn/c_<page>.py`, or `tools/site/chrome.py` for the chrome, and rerun |
| Assets 404 on GitHub Pages but work locally | An absolute path was used | Use `./assets/...`. Pages serves this repository under a subpath |
| A page flashes light before going dark | `cfc-theme.js` was moved out of `<head>` or given `defer`/`async` | It must be a blocking script in `<head>`. That is the whole mechanism |
| A component inside `.article` loses its own colour | `.article a:not([class])` is prose only, so a classed anchor must set its own colour | Give the component a colour on its class in `cfc-app.css`. See docs/DESIGN.md section 6.5 |
| Contrast checker says the dark blocks drifted | A token changed in `[data-theme="dark"]` but not in the `prefers-color-scheme` block, or the reverse | Apply it to both. The duplication is deliberate |
| The camera does not start on a phone | The page was opened over `http://<LAN-IP>`, not a secure context | Use the deployed HTTPS URL or an HTTPS tunnel |
| `fetch` of local JSON fails with a CORS error | The page was opened with `file://` | Serve it over `python -m http.server` |
| Pages shows an old version after a successful deploy | CDN cache | Hard-refresh. It typically clears within minutes |
| A live check fails with no code change | The community database moved | Expected. `check-live.py` is a smoke check, not a gate. Confirm against the live API before treating it as a regression |
| `p.chromium.launch(channel='msedge')` fails | Edge is not installed, or is not at the expected path | Install Edge. Do not switch the tool to Chrome; see section 19 |

### 15.10 Monitoring

| What | Where |
|---|---|
| Deploy status and logs | https://github.com/Azqato/Cat-Food-Center/actions |
| Pages uptime | https://www.githubstatus.com |
| Core Web Vitals | PageSpeed Insights against the live URL. No CI gate yet |
| JavaScript errors in production | Browser DevTools only. There is no error reporting service |
| Dependency vulnerabilities | Not applicable. There are no dependencies to audit; see section 21 |

There is no server-side logging, error tracking or uptime monitor. All three are M12 items.

---

## 16. Technical requirements

### 16.1 System architecture

A **static site**: hand-written HTML, CSS custom properties and vanilla ES modules, served directly from the repository root by GitHub Pages with no build step. There is no server in the path for anything.

```
Browser (static page, no server)
  |
  |-- HTML + CSS custom properties + ES modules
  |-- assets/js/opff.js ------> world.openpetfoodfacts.org (public, keyless, CORS)
  |-- assets/js/scoring.js ---> pure computation, no I/O
  |-- assets/data/*.json -----> committed knowledge base
  |-- sw.js ------------------> cache, and the "saved copy" stamp
  `-- localStorage -----------> recently viewed, this device only
```

### 16.2 ADR-001: static HTML is the architecture, not a placeholder

**Status:** Accepted. **Date:** 2026-09-05. **Decider:** Azqato.

**Context.** The repository carried two implementations at once: the plain HTML that actually shipped, and an unused Next.js 14 application that was never built and never deployed. The README described Next.js as the stack, which was wrong about what users load. The fork had to be resolved before building the data layer, the engine or the scanner, because those are where the architecture choice bites. The specific question was whether committing to static HTML forecloses the barcode scanner. It does not.

**Decision.** Static HTML, CSS and vanilla JavaScript, served directly from the repository root, is the target architecture, not an interim state.

Consequences:

1. The unused Next.js application was deleted.
2. Where a page needs generating rather than hand-writing, a small Python generator under `tools/` emits committed HTML. The build runs on a developer machine, never in CI.
3. Application logic is plain ES modules under `assets/js/`, loaded with `<script type="module">`. No bundler, no transpile.
4. Data we own ships as static JSON under `assets/data/`.

**Why it works for the planned features.** Scanning decomposes into camera access (`getUserMedia`), decoding (`BarcodeDetector`, ZXing fallback) and lookup (`fetch`), all of which run in the browser. The only hard requirement is HTTPS, which Pages provides. The API is public, keyless and CORS-enabled, so there is no secret to protect and no reason to proxy. Scoring is deterministic computation that is *better* client-side, because a sceptical reader can open devtools and watch the score being derived.

**What static hosting genuinely cannot do.** Recorded so that hitting one is a recognised trigger rather than a surprise.

| Limitation | Affects | Mitigation | Escape hatch |
|---|---|---|---|
| No server-side writes | Submitting a missing product | Resolved differently: contributions go upstream to Open Pet Food Facts | A single serverless function alongside Pages |
| No secrets | Any API needing a key | Prefer keyless APIs | The same function as a signing proxy |
| No dynamic routes | `product.html?barcode=X` works, `/product/X` does not | Query-string routing, rendered client-side | Pre-generate a file per SKU for the top-100 catalogue |
| No rate-limit shielding | Every visitor hits the upstream API directly | Service worker caching, plus a local catalogue | A proxy and cache layer, if the upstream ever objects |
| Client-side rendering hurts crawlability | Product page discoverability | The Cat Care Guide, the main search surface, is fully static HTML with its content in the markup | Pre-generation |
| No build step means no type checking | Engine correctness | Keep scoring pure and cover it with browser-hosted tests | A type-check-only CI job (`tsc --checkJs --noEmit`) that changes nothing served |

**How M10 actually resolved.** The first row anticipated a hosted form as the workaround. Building it showed the workaround was the wrong shape, for the reason given in section 13. The general lesson: not every limitation needs a workaround. Check whether the honest answer is to not hold the data at all.

**Alternatives considered.** Finishing the Next.js app and deploying its static export was rejected: the runtime capabilities would be identical, and the only real gains (typed components, per-barcode pre-rendering) are not needed in the MVP and cost a build step, a dependency tree, and a pipeline that can break the deploy. The current pipeline cannot break the deploy because it does not build anything. Keeping both was rejected as the status quo that caused the confusion.

**Revisit this when:** contributing upstream stops being the right answer; per-product URLs need search indexing and pre-generation proves insufficient; or the engine grows past roughly 1,500 lines, where the absence of enforced types starts costing more than a build step would.

### 16.3 Tech stack

| Layer | Tool | Version |
|---|---|---|
| Markup | HTML generated by `tools/site/` and `tools/learn/`, committed to the repository | n/a |
| Styling, guide pages | `assets/cfc.css`, hand-written | n/a |
| Styling, app pages | `assets/cfc.css` plus `assets/cfc-app.css`, hand-written | n/a |
| Design tokens | `assets/cfc-tokens.css`, CSS custom properties | n/a |
| Scripting | Vanilla ES modules, no bundler | n/a |
| Barcode decoding | `BarcodeDetector` where available, else ZXing | `@zxing/library@0.21.3`, pinned |
| Fonts | Fraunces, Public Sans, from Google Fonts | n/a |
| Generator and tooling | Python 3 | 3.8+ |
| Test driver | Playwright for Python, driving Edge | n/a |
| Hosting | GitHub Pages | n/a |
| CI | GitHub Actions, no build step | `checkout@v4`, `upload-pages-artifact@v3`, `deploy-pages@v4` |

There is no unpinned third-party runtime dependency left. M14 removed the last one, the Tailwind CDN. ZXing is pinned to an exact version and is fetched only where `BarcodeDetector` is missing.

### 16.4 Folder structure

Everything at the repository root is served verbatim. `tools/` and `docs/` are the exceptions: they run or are read on a developer machine.

```
Cat-Food-Center/
├── README.md                # Public front door, general reader
├── LICENSE.md               # All rights reserved, plus the AI and search carve-out
├── robots.txt               # Fully open, deliberately
├── sitemap.xml              # Every public page
├── index.html               # Home. GENERATED by tools/site/build.py, as are the eight below
├── search.html              # Text and brand results; ?q= ?brand= ?page= ?only=
├── brands.html              # Brand index
├── product.html             # Product detail; ?barcode=
├── scan.html                # Camera scanner and manual entry
├── submit.html              # Missing-product hand-off; ?barcode=
├── compare.html             # Two products; ?a= and ?b=
├── methodology.html         # Public scoring explanation
├── offline.html             # Shown for a page never opened on this device
├── learn.html               # The Cat Care Guide. GENERATED by tools/learn/build.py
├── learn-*.html             # Ten more guide pages. GENERATED
├── tests.html               # Browser-hosted test suite; run by tools/run-tests.py
├── sw.js                    # Service worker. MUST stay at the root for scope
├── manifest.webmanifest     # PWA manifest
├── favicon.svg
├── .nojekyll                # Stops Pages ignoring underscore directories
├── assets/
│   ├── cfc-tokens.css       # Palette, light and dark. Every page
│   ├── cfc-theme.js         # Theme switching. MUST be blocking in <head>
│   ├── cfc.css              # The shell: bar, drawer, article, rail. Every page
│   ├── cfc-app.css          # Components only the application pages use
│   ├── cfc-docs.js          # Drawer and scroll spy. Every page
│   ├── icons/               # PWA icons, 192, 512, maskable
│   ├── js/                  # 16 application ES modules
│   │   ├── opff.js          #   API client, normaliser, brand facet
│   │   ├── scoring.js       #   The CFC Score. Pure: no network, no DOM
│   │   ├── scanner.js       #   Camera, BarcodeDetector/ZXing, checksums
│   │   ├── history.js       #   Recently viewed, localStorage only
│   │   ├── pwa.js           #   SW registration and offline banner (classic script)
│   │   ├── *-page.js        #   Per-page rendering
│   │   ├── test-runner.js   #   Minimal assertion runner
│   │   └── *.test.js        #   Tests, loaded by tests.html
│   └── data/
│       └── additives.json   # Additive knowledge base, v1.1.0
├── tools/
│   ├── run-tests.py         # Drives tests.html headlessly in Edge
│   ├── check-live.py        # 19 end-to-end checks against the live API
│   ├── check-contrast.py    # WCAG AA audit of both palettes
│   ├── probe-opff.py        # Regenerates the numbers in section 12
│   ├── site/                # Application page generator: chrome.py, build.py, content/
│   └── learn/               # Guide generator: shell.py, bits.py, c_*.py
├── docs/
│   ├── PRD.md               # This file
│   ├── DESIGN.md
│   └── PATCHNOTES.md
└── .github/workflows/
    └── deploy.yml           # Upload and deploy. No build step
```

### 16.5 Data models

Written as TypeScript interfaces because that is the clearest notation for a shape, **not** because TypeScript is in the stack. It is not; nothing enforces these.

```ts
interface Product {
  barcode: string;
  name?: string;
  brand?: string;
  quantity?: string;
  imageUrl?: string;              // 400px front image. Present on ~97% of records
  thumbUrl?: string;              // The 200px rendition of the same photo, for 56px boxes
  ingredientsText?: string;
  ingredients: string[];          // Split on commas outside brackets
  ingredientsLang: string;        // 'en' where an English text existed, else the record's lang, else 'unknown'
  format?: 'wet' | 'dry' | 'semi-moist' | 'treat';
  lifeStage?: string;
  nutrition: Nutrition;
  dataCompleteness: 'full' | 'partial' | 'minimal';
  lastModified?: number;
}

interface Nutrition {
  crudeProteinPct?: number;       // As fed, plausibility-gated
  crudeFatPct?: number;
  crudeFibrePct?: number;
  crudeAshPct?: number;
  moisturePct?: number;
  kcalPer100g?: number;
  taurinePresent?: boolean;       // undefined means unknown, not absent
  schema: 'crude' | 'human' | 'mixed' | 'none';
  confidence: 'high' | 'low' | 'none';
  energyCorrected?: boolean;      // A per-kilogram figure was divided by 10
}

interface ScoreResult {
  scorable: boolean;              // false where too little is known
  score?: number;                 // 0 to 100
  band?: 'excellent' | 'good' | 'poor' | 'bad';
  bandLabel?: string;
  pillars: { nutrition?: Pillar; additives?: Pillar; transparency?: Pillar };
  flagged: FlaggedAdditive[];
  hardGates: string[];
  warnings: string[];
  confidence: 'high' | 'medium' | 'low';
}

interface Brand {                 // From the facet, after merging case variants
  name: string;                   // The spelling used by the most products
  tags: string[];                 // Every raw tag, because the filter needs them all
  count: number;                  // Summed across variants
}
```

### 16.6 API design

There is no API of our own. Two upstream endpoints and one internal data file.

| Call | Purpose | Inputs | Failure handling |
|---|---|---|---|
| `GET /api/v2/product/<barcode>.json?fields=` | One product | Barcode, 6 to 14 digits | 404 with `status: 0` is a normal miss, returned as `{found:false}`, never as an error |
| `GET /cgi/search.pl?action=process&json=1&...` | Text results | `search_terms`, `tag_0=cat-food`, an optional brand tag, `page`, `page_size`, `fields` | Network failure returns an empty result plus an error string; the page renders the error |
| `GET /api/v2/search?categories_tags_en=cat-food&...` | Brand-only browse | `brands_tags`, `page`, `page_size`, `fields` | Same |
| `GET /facets/categories/Cat%20food/brands.json` | The brand index | None | Same |
| `GET ./assets/data/additives.json` | The knowledge base | None | A failure means no scoring; the page says so |

**Internal data flow**, which matters more here than endpoint shapes:

```
URL query string
  -> page module reads it
  -> opff.js fetch --> normalize() --> Product
  -> scoring.js scoreProduct(Product, KnowledgeBase) --> ScoreResult
  -> page module renders
  -> history.js records the visit (product pages only)
```

`scoring.js` never fetches and never touches the DOM. `opff.js` never scores. That separation is what makes the engine testable without a network.

### 16.7 State management

There is no state library and no global store. State lives in exactly four places, each chosen deliberately:

| State | Where | Lifetime | Notes |
|---|---|---|---|
| What the visitor is looking at | The URL query string | The navigation | Every view is a link somebody can send. Search carries `q`, `brand`, `page` and `only` |
| Recently viewed | `localStorage`, key `cfc-recent`, 6 items | This device | Never synced, never uploaded. Every access is wrapped in try/catch, because storage throws in some private modes |
| Theme preference | `localStorage`, key `cfc-theme` | This device | `system` stores nothing and lets the media query decide |
| Cached responses | Cache Storage, via `sw.js` | Until the cache version changes | Three caches: `cfc-shell-v1`, `cfc-api-v1`, `cfc-images-v1` |

In-page state (a fetch in flight, the current result list) is local to the page module and dies with the navigation. This is a deliberate consequence of having no framework: there is nothing to hydrate and nothing to keep in sync.

### 16.8 Caching strategy

Three strategies, chosen per resource, all in `sw.js`:

| Resource | Strategy | Why |
|---|---|---|
| API responses | Network first | Being current matters more than being fast. A cached answer is a fallback, never a preference |
| Images | Cache first | Large, and never change under a URL |
| Same-origin CSS, JS, JSON | Stale while revalidate | Instant from cache, updated in the background, so a deploy lands on the visit after next |
| Navigations | Network, then the precached document | Deliberately **not** cached: every product is the same document under a different query string, so caching would add one identical entry per product viewed. `ignoreSearch` finds the precached document whatever the query |

**The governing rule: a cached score must never be presented as a current one.** Anything served from cache is stamped with `x-cfc-cached`, `opff.js` carries the stamp through, and the page says it is showing a saved copy. A 404 is never cached, because it is how an unknown barcode is detected and caching it would keep reporting "not found" after the product is added.

The `SHELL_ASSETS` list is currently 31 entries and the installed cache holds 32. `tools/check-live.py` asserts it and also asserts it does not grow per product viewed.

### 16.9 Third-party integrations

| Service | What it does | Authentication | What it receives |
|---|---|---|---|
| Open Pet Food Facts | The entire product catalogue | None. Public and keyless | Barcode numbers, search terms, brand tags, and the visitor's IP as a normal request property |
| Google Fonts | Fraunces and Public Sans | None | The visitor's IP and user agent |
| jsDelivr | ZXing, only when a browser lacks `BarcodeDetector` and only on the scan page | None | The visitor's IP and user agent |
| GitHub Pages | Hosting | None | The visitor's IP and user agent |

### 16.10 Performance requirements

- Largest Contentful Paint at or below 2.5 s, Cumulative Layout Shift at or below 0.1, Total Blocking Time at or below 200 ms. Enforced by `tools/check-vitals.py` on every page the repository serves in full; see section 19.2 for which pages are gated and why the rest are not.
- No page may scroll horizontally at 320px. `tools/check-a11y.py` asserts this on all 25 page states, and `tools/check-live.py` asserts the desktop case.
- No bundle budget exists, because there is no bundle. The nearest equivalent is the shell precache size, which is asserted.

### 16.11 Known technical debt

| Area | Shortcut taken | Correct solution |
|---|---|---|
| Product coverage | Whatever the database holds; about a fifth of products score on all three pillars | Curate a local catalogue for common SKUs under `assets/data/` (M12) |
| Alias languages | Six covered; anything else is reported as unchecked | Extend the alias lists, and `MATCHED_LANGUAGES` with them, never ahead of them |
| Search relevance | Delegated wholly to `/cgi/search.pl`, whose ranking is not documented and cannot be tuned or inspected | A curated catalogue, or a local index over it |
| Scorable-only filter | Scans the first five pages of the query and filters those, because the API cannot filter on scorability. Beyond 120 results it is a sample, and says so | Only a local catalogue can fix this properly |
| Product image quality | Contributor photographs at whatever angle and lighting they had, shown as they are | Nothing to do inside this architecture. The catalogue is the source, and a photo of the real tin is worth more than a tidy one |
| Ingredient explanations | Only entries in the additive knowledge base explain themselves, which is 20 additives and 3 vague-term groups | A general ingredient dictionary, if one can be sourced without inventing claims. Nothing true can be added to "chicken" today |
| "Better alternatives" | Specified in the original PRD, never built | Needs a same-format query the API supports poorly |
| Types | Nothing enforces the shapes in 16.5 | Optional `tsc --checkJs --noEmit` job with JSDoc types |

---

## 17. Conventions

Derived from the code as it stands, not from any style guide. Where usage is inconsistent, the dominant form is named.

### 17.1 Naming

| Thing | Convention | Examples |
|---|---|---|
| HTML pages | lowercase, hyphenated, `.html` | `search.html`, `learn-daily-requirements.html` |
| Page modules | `<page>-page.js` | `search-page.js`, `brands-page.js` |
| Library modules | A single noun | `opff.js`, `scoring.js`, `scanner.js`, `history.js` |
| Test modules | `<module>.test.js`, beside the module | `scoring.test.js` |
| Python tools | lowercase, hyphenated | `check-live.py`, `run-tests.py` |
| Guide content modules | `c_<topic>.py` | `c_daily.py`, `c_toxic.py` |
| Functions and variables | `camelCase` in JS, `snake_case` in Python | `scoreProduct`, `check_pair` |
| Module-level constants | `SCREAMING_SNAKE_CASE` | `WEIGHTS`, `MATCHED_LANGUAGES`, `SHELL_ASSETS` |
| CSS custom properties | `--kebab-case`, semantic not literal | `--ink-soft`, `--chip-good-bg` |
| Storage keys | `cfc-` prefixed | `cfc-recent`, `cfc-theme` |
| Cache names | `cfc-<area>-<version>` | `cfc-shell-v1` |

Colour tokens are named for their role, never their value. There is no `--orange`.

### 17.2 Formatting

- Two-space indentation in HTML, CSS and JavaScript. Four in Python.
- Single quotes in JavaScript, double only to avoid escaping. Python follows the same habit.
- Semicolons always, in JavaScript.
- Roughly 100 columns in JavaScript, 79 in Python. Neither is enforced by a tool.
- Imports at the top of a module, standard library first in Python.
- Trailing commas in multi-line JavaScript literals.
- There is no formatter and no linter. Match the file you are in.

### 17.3 Organisation

- One page, one module. A page module owns its DOM and is loaded with `<script type="module">` at the end of the body.
- Modules export named functions. There are no default exports anywhere.
- `_internal` is the established name for an export that exists only so tests can reach a private function. Anything under it is not a public interface.
- Modules run to roughly 500 lines at the top end (`scoring.js`). A module past that is a signal to split.
- Logic is split out when a second page needs it, not before. `history.js` exists because two pages read the same list.

### 17.4 Comments

Comment density here is **high by ordinary standards, and deliberately so.** Every module opens with a block comment explaining why it exists and what decision shaped it, often citing the document that records the decision. This is the dominant pattern and new files should follow it.

What earns a comment:

- A decision that looks wrong without context. `sw.js` explains why navigations are not cached; `scan-page.js` explains why each camera failure gets its own message.
- A workaround for something outside our control, such as `User-Agent` being a forbidden header in browser `fetch`.
- A rule the code depends on, such as `cfc-theme.js` needing to be blocking.
- A measured fact behind a constant, such as the plausibility ranges.

What does not: restating the code.

Section markers use box-drawing characters (`/* ── Offline banner ── */`). Those are `─`, U+2500, and are not affected by the em dash prohibition.

### 17.5 Error handling

- **Absence is not an error.** A barcode that is not in the database returns `{found: false}`. A missing field yields an absent value and an honest completeness rating.
- **A rejected value is discarded, not repaired.** A protein figure outside the plausibility band is dropped rather than clamped.
- **Every user-facing failure gets its own sentence.** The scanner distinguishes a denied permission, no camera, a busy camera and an insecure origin, because a single generic message would be accurate and useless.
- **`localStorage` access is always wrapped in try/catch**, because it throws in some private modes rather than returning null.
- **Nothing is logged in production.** There is no console noise and no error reporting service.

### 17.6 Validation

Input arrives from three places and each is checked at the boundary: the query string (parsed, ranged, defaulted), the API (normalised through `normalize()`, plausibility-gated), and the barcode field (digits only, then a check digit). Everything rendered from the API is escaped through a local `esc()` helper, because there is no framework doing it.

### 17.7 Commits and branching

Read from the history rather than from a guide.

- **Trunk-based.** Work goes to `main`. There are no long-lived branches and no pull requests in the history.
- **Conventional-commit prefixes** are the dominant form: `feat:`, `fix:`, `docs:`, `refactor:`.
- **A short imperative subject**, lowercase after the prefix, no trailing period: `feat: compare two foods side by side (M11)`.
- **A milestone reference in parentheses** where the commit completes one.
- **A body that explains why**, often several paragraphs, and frequently recording what was learned rather than only what changed. This is the strongest convention in the history and the most valuable one.
- Every commit is expected to leave `main` deployable, because every push to `main` deploys.

---

## 18. Writing style

The project had no stated rule before the 2026-09-06 audit. This is the rule now, and it applies to documentation, UI copy and code comments alike.

**Em dashes are prohibited in all three forms:**

1. The literal Unicode character, U+2014.
2. The `&mdash;` HTML entity.
3. A double hyphen used as punctuation.

The character and the entity must be searched **independently**, because a search for one will not find the other.

CSS custom properties (`--color-bg`) are valid syntax, not punctuation, and are never touched. Nor are command-line flags (`--noEmit`), HTML comment delimiters, or the box-drawing character `─` (U+2500) used in section markers, which is a different character entirely.

**Replace each instance** with whichever fits: a comma (most often), a colon (introducing a list or an elaboration after a complete clause), a semicolon (joining two closely related independent clauses), parentheses (asides), a period (splitting one sentence into two), or a single hyphen.

**The single hyphen is permitted and encouraged** where context justifies it: document titles, section headings, and version lines such as `## v1.2.0 - 2026-01-01`, where a comma or colon reads awkwardly. In running prose the other replacements are usually better.

**Leave any instance the text needs in order to mean anything**, such as a rule, a table or an example naming the character it prohibits. This section is itself an example.

**Tone:** direct and functional. Plain declarative sentences. No marketing language, no filler openings, no restating the obvious. Thorough means more facts, not more words around the same facts.

---

## 19. Browser testing

The project had no stated rule before the 2026-09-06 audit. This is the rule now.

**Drive Microsoft Edge, never Chrome.** There is no JavaScript runtime on the maintenance machine, so end-to-end testing is done by driving a headless browser directly from Python, and Chrome is the owner's day-to-day browser. Driving it would disturb a live session. Edge runs the same engine and is free to use.

This applies to **every** browser a test drives, not only one named in a configuration file. An ad hoc headless invocation from a script or a shell command is testing and falls under the same rule.

**Resolved binary path** (Windows, as of 2026-09-06):

```
C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe
```

Playwright reaches it through `channel='msedge'` rather than its own bundled Chromium, so no browser download is required:

```python
browser = await p.chromium.launch(channel='msedge')
```

`tools/run-tests.py`, `tools/check-live.py`, `tools/check-a11y.py` and `tools/check-vitals.py` all do this, through the `EDGE_CHANNEL` constant each defines. Version verified working: Edge 152.

**Edge is the default, not the only engine.** Every gate above drives Blink through Edge, because that is the fastest thing to run and Blink is the majority engine. `tools/check-engines.py` additionally drives Gecko and WebKit; see section 19.3. It uses Playwright's own browser builds rather than any browser installed on this machine, which is the same reasoning that keeps Chrome out of the loop.

### 19.1 The accessibility gate

`tools/check-a11y.py` runs axe-core 4.10.2 against all 25 page states, each in both themes, and adds two checks axe does not perform: reflow at a 320px viewport (WCAG 1.4.10) and the skip link from a cold keyboard (2.4.1). 100 audits, all clean. It exits non-zero, so it is a gate rather than a report; `--report` prints every violation with its selector and exits 0.

**Only WCAG 2.1 A and AA rules run.** axe ships best-practice rules alongside the standard. They are worth reading, but a gate that fails the build on them is failing it on somebody's style preference.

**What this does not cover.** axe finds roughly a third to a half of WCAG issues, all of them the machine-checkable ones. It cannot tell whether alternative text is *correct*, whether the tab order is sensible, whether a heading structure matches the document's actual shape, or whether an error message helps. Those were checked by hand and are recorded below, because a green gate that is read as "the site is accessible" is worse than no gate.

**Checked by hand, and the answers:**

| Question | Answer |
|---|---|
| Is `alt=""` on product photos right? | Yes. The photo sits beside the product name in text. A screen reader that announced both would say the name twice, and the photograph carries no information the name does not. It is decorative *in that position*, which is what the empty alt says |
| Is the focus ring visible on every surface? | It is now. There was no site-wide `:focus-visible` rule at all before this pass, only the browser default. The site has two palettes and custom card components, so it defines its own: 2px accent with a 2px offset |
| Does the tab order match reading order? | Yes. Nothing on any page uses a positive `tabindex`, and the DOM order is the visual order in every layout, because the shell is a grid and the source is skip link, bar, drawer, article, rail, footer |
| Is motion optional? | It is now. `prefers-reduced-motion: reduce` was honoured by exactly one component before this pass. It is now a blanket rule: smooth scrolling off, every transition and animation reduced to nothing. Nothing on the site conveys meaning through motion, so this costs the design nothing |
| Are the two search inputs labelled? | Yes, and axe confirms it. They carry visible labels rather than placeholder text standing in for one |

**Why not Lighthouse.** It requires Node, and ADR-001 keeps this project free of npm. axe-core is the engine Lighthouse's accessibility category wraps, and it loads from a CDN into a page Playwright already has open, so the standard is checked with the same tool and one less dependency.

### 19.2 The performance gate

`tools/check-vitals.py` loads 12 pages with the CPU slowed 4x and the network held to roughly a slow 4G connection, in a 412px viewport with a cold cache, and reads LCP, CLS and Total Blocking Time out of the browser's own performance timeline.

**The throttling is the point.** From a loopback server on this machine every page renders in under 400ms, every budget passes, and the gate says nothing. The throttle is what makes a regression visible. It is not a claim about any particular visitor's device.

**Budgets:** LCP 2500ms, CLS 0.1, TBT 200ms. The first two are Google's "good" thresholds and are what section 14 already stated; TBT has no official threshold, and 200ms is Lighthouse's own boundary. TBT stands in for INP, which cannot be measured without a real session.

**Ten of the twelve pages are gated. Two are not**, and the distinction is the honest part of this tool. A page the repository serves in full is a property of the code, so a regression in it is real and fails the build. `product.html` and a page of search results cannot paint until Open Pet Food Facts answers, and no commit here controls how fast that is. They are measured and printed on every run, because the numbers are worth seeing, but they cannot fail the build for something outside the repository. The product page currently measures about 2.5s LCP under this throttle, essentially all of it the API round trip.

**What it does not measure:**

- **Time to first byte from GitHub Pages.** Pages are served from `127.0.0.1`, per section 20. Hosting latency is real and is not in these numbers.
- **INP.** It needs real interaction over a real session, and there is no analytics. See section 14.
- **Any real device.** A 4x CPU throttle on this machine is not a mid-range phone. It is a fixed, repeatable handicap, which is what a gate needs.

**Why not Lighthouse:** the same reason as 19.1. Lighthouse reads these three numbers out of the same browser timeline.

### 19.3 The three engines

`tools/check-engines.py` runs the unit suite, all 12 page states and the barcode decode round-trip in Blink (through Edge), Gecko and WebKit. Before it existed, nothing in this project had ever loaded a page in anything but Blink, which made "works on an iPhone" an assumption rather than a finding. Tenet 7 says mobile is the real use case, and every browser on iOS runs WebKit whatever its name is.

**Playwright's own builds, not installed browsers.** Section 19's rule is that a test must not drive the browser the maintainer is using. Playwright downloads its Gecko and WebKit builds into its own cache, so nothing here touches an installed Firefox. `python -m playwright install webkit firefox` once, about 180MB.

**What it found:**

| Feature | Blink | Gecko | WebKit |
|---|---|---|---|
| `BarcodeDetector` | yes | **no** | **no** |
| `serviceWorker` | yes | yes | yes |
| `IntersectionObserver` | yes | yes | yes |
| `largest-contentful-paint` | yes | yes | yes |
| `layout-shift` | yes | **no** | **no** |
| `:has()`, CSS nesting | yes | yes | yes |

Three consequences follow, and only the first was expected:

1. **ZXing is not a fallback on two of the three engines.** `scanner.js` already suspected this, calling support "partial, Safari and Firefox largely not". It is not partial: on Gecko and WebKit, which is every browser on iOS, the platform API does not exist, and ZXing is the whole feature rather than a fallback. The decode round-trip now runs in all three engines and passes in all three, which is the check that matters most in this file.
2. **CLS can only be measured in Blink.** The Layout Instability API is Chromium-only. `check-vitals.py` therefore measures one engine, and M16b's layout reservation is taken on faith to help the other two. It is a `min-height` rather than an engine trick, so that faith is reasonable, but it is faith and section 19.2 says so.
3. **Nothing else differed.** The unit suite is 178 passing in all three, every page renders its expected content, and nothing overflows at 1280px or 320px anywhere. That is a finding worth stating plainly, because the value of this tool is mostly that it can now say so.

**One entry in the matrix is not about the shipping browser.** Headless WebKit reports no `getUserMedia`, which is a property of Playwright's build and not of Safari. It means this tool exercises the no-camera path in WebKit and cannot exercise the camera path there at all. Real Safari camera behaviour remains untested by anything, and that is the honest residue of open question 7.

---

## 20. Verification environment

The project had no stated rule before the 2026-09-06 audit. This is the rule now.

**Verify locally. Never against production**, unless the request explicitly asks for a production check.

Run the change on a local copy: the file opened from disk, `python -m http.server`, whatever the local setup produces. Production is where a change is confirmed to have arrived, not where it is tested.

**The reason is not caution for its own sake.** Testing against production means the change has already shipped, so the test can only report what users are already seeing. It also puts load onto a live system, and it turns a failing test into something to roll back rather than something to fix before pushing.

**Two things that are easy to conflate:**

- **Verifying functionality is local.** `python tools/run-tests.py`, `python tools/check-live.py`, `python tools/check-contrast.py`, `python tools/check-a11y.py`, `python tools/check-vitals.py` and `python tools/check-engines.py` all run against a local server, including the two that reach the live *API* but serve the *pages* from `127.0.0.1`.
- **Confirming a deploy landed is a separate step**, done against production after the push, and it is a comparison rather than a test: fetch the deployed artifact and check it matches what was verified locally. That is legitimate and is not an exception to this rule.

**Never point a destructive or state-changing check at production.** In this project that mostly means never writing to Open Pet Food Facts from a test, and never seeding records there to exercise the submit flow. `submit.html` deep-links a human to the upstream form and writes nothing itself, which is the property that keeps this simple. If a future feature can only be exercised against a live system, stop and ask.

The local and production differences that can hide a bug are tabulated in section 15.7.

---

## 21. Security

### 21.1 Authentication

**There is none, and that is the design.** No accounts, no login, no sessions, no cookies set by this site. The app is a read-only information tool. If accounts are ever added, this section is where the mechanism gets recorded.

### 21.2 Authorization

**No roles exist.** All content is public and identical for every visitor. Authorization does not apply until a backend and accounts exist.

### 21.3 Data storage

| Data | Where | Protection |
|---|---|---|
| Product catalogue | Open Pet Food Facts, external, read-only | No user data involved |
| Additive knowledge base | Committed JSON in the repository | Public, no sensitive content |
| Recently viewed | Browser `localStorage`, key `cfc-recent` | Never leaves the device. Not synced, not uploaded, not readable by this project |
| Theme preference | Browser `localStorage`, key `cfc-theme` | Same |
| Cached pages and responses | Browser Cache Storage | Same |
| Camera frames | Processed in-page, never stored, never uploaded | On-device only. The video stream is stopped and released on stop, on tab hide and on navigation |
| Submitted products | Not held. The submit page hands off upstream | There is no queue and no database |

**No personally identifiable information is collected or stored, anywhere, by any part of this project.** There is no database, no analytics and no logging.

### 21.4 Environment variables and secrets

There are none, and no secret is hardcoded anywhere. Every API in use is public and keyless.

Should one ever be needed, it must not be committed, must not be shipped to the browser, and its arrival is a trigger to revisit ADR-001 rather than a routine addition.

### 21.5 Third-party trust

Every service that receives anything about a visitor:

| Service | What it receives | Why |
|---|---|---|
| Open Pet Food Facts | Barcode numbers, search terms, brand tags, and the visitor's IP as an ordinary request property | The catalogue |
| Google Fonts | IP and user agent | Two typefaces |
| jsDelivr | IP and user agent, only on the scan page and only where `BarcodeDetector` is missing | The ZXing fallback |
| GitHub Pages | IP and user agent | Hosting |

No service receives user-identifying data, because none is collected. **Every one of these does see a visitor's IP**, which is unavoidable for any resource loaded from another origin. M14 removed the Tailwind CDN, which shortened this list by one.

Barcodes and search terms do leave the device, which is worth stating plainly: they go to Open Pet Food Facts as part of the lookup, and that request cannot be made without them.

### 21.6 Known attack surface

| Area | Risk | Mitigation |
|---|---|---|
| Rendering API responses | Community-edited product text is injected into pages. There is no framework escaping it | Every page module escapes through a local `esc()` helper before interpolation. **This is hand-rolled and is the highest-risk area in the codebase**, because one missed call is an injection |
| External links | Referrer leakage, tab-nabbing | Every external anchor carries `rel="noopener noreferrer"` |
| Barcode scanner | A scanned code containing a URL | Only EAN-13, EAN-8, UPC-A and UPC-E are accepted, each checksum-validated. The decoded value is used as a barcode string and never navigated to |
| Service worker | A bad worker persisting on a device we cannot reach | `VERSION` in `sw.js` retires every cache at once, and is the only reliable lever |
| Static hosting | No server-side execution at all | The attack surface is limited to the static files themselves |
| Third-party scripts | The Tailwind CDN script is unpinned, so its content can change without a commit here | Removed in M14. Until then this is a real supply-chain exposure, accepted knowingly |

### 21.7 Dependency policy

**There are no runtime dependencies to audit** in the conventional sense: no npm, no lockfile, no `node_modules`, no transitive tree. `npm audit` and Dependabot do not apply and are not configured.

What does apply:

- **Third-party scripts loaded at runtime are the dependency surface.** Today that is the Tailwind CDN (unpinned, on eight pages) and ZXing (pinned to `0.21.3`, loaded on demand). Pinning is the rule; Tailwind is the exception and is being removed.
- **A new third-party script needs a concrete justification.** Convenience is not one.
- **Python tooling** (Playwright) never runs in CI and never touches the deployed artifact.
- **GitHub Actions are pinned to major versions** (`@v4`, `@v3`).

---

## 22. Licensing

The project had no licence at all before the 2026-09-06 audit: no `LICENSE.md`, no licence line, nothing. The default posture below was therefore adopted and written into [`LICENSE.md`](../LICENSE.md) at the repository root.

**Posture: all rights reserved. Source-available, not open source.** The repository is published so it can be read, and publishing is not a grant.

### 22.1 Why a grants-nothing licence

- **Grant nothing by default.** A permission given to everyone cannot easily be withdrawn from one person. The goal here is not to stop copying; it is to retain the ability to act against a specific bad actor, and broad grants defeat that.
- **The NO WAIVER clause is load-bearing.** Choosing not to act against one use is not a licence, not a precedent and not a waiver against that person or anyone else. Delay does not waive. Any waiver must be written, signed and scoped to the use it names. Without this, a long history of tolerated copying is the first thing an infringer points at.
- **Asymmetry.** Widening a grant is one sentence; narrowing a granted right is not. When in doubt, grant less and offer the request route.
- **Never assert a licence without the licence text.** A bare "MIT" line in a README with no file behind it is not a grant, it is an ambiguity.

### 22.2 The AI and search carve-out

Search engines, AI assistants, answer engines and other automated systems are **explicitly permitted** to crawl, index, store for retrieval, quote, summarise, link to and cite this work. Attribution is requested, not required. No permission needs to be asked for.

Being cited in an AI answer is the modern equivalent of ranking: it costs the project nothing and gains it distribution, and enforcing against a citation would work against the project's own purpose. The line is drawn at three distinct things:

- **Referencing is granted.**
- **Substitution is not**, meaning reproducing the work as a replacement for visiting it.
- **Training data is not granted by default**, and is routed to the request path with a note that it is not usually refused. Retrieval-and-cite is what actually produces the citations, so this keeps the benefit without handing over a training licence.

### 22.3 What the licence does not claim

- **It does not override platform terms.** A public repository on GitHub already gives GitHub's users whatever view and fork rights its terms grant. Those operate independently and are not enlarged by the licence.
- **It does not claim third-party data.** This is not theoretical here: every product fact on the site comes from Open Pet Food Facts and is not ours to license. Nor are the AAFCO profiles, the fonts, or ZXing.
- **It does not restrict rights that cannot be restricted**, such as fair use or fair dealing.

### 22.4 Permission requests

Route to the public issue tracker rather than to private email:

**https://github.com/Azqato/Cat-Food-Center/issues**

A visible record of what has and has not been permitted suits a posture whose enforcement depends on permissions being specific and traceable rather than assumed.

### 22.5 The machine-readable layer

`robots.txt` is **fully open** (`User-agent: *`, `Allow: /`) and carries a comment marking that as deliberate, so a future tightening is a decision rather than an accident. It names `LICENSE.md` as authoritative if the two ever appear to disagree. A grants-nothing licence beside an open `robots.txt` is a contradiction a cautious crawler operator could resolve the wrong way, and the comment exists to stop that.

`sitemap.xml` sits at the repository root and lists every public page.

**A note on scope that the audit had to check:** this site is served from a subpath of `azqato.github.io`, a domain this project does not own. The `robots.txt` that actually governs crawler behaviour for that host is the one at `https://azqato.github.io/robots.txt`, which belongs to the domain owner. The `robots.txt` committed here is served at `https://azqato.github.io/Cat-Food-Center/robots.txt` and is **not** the authoritative robots policy for the host. It is committed anyway because it is correct if the site ever moves to its own domain, and because it documents the intent. The sitemap is subject to the same limitation: it is only trusted for URLs under its own path unless a host-level `robots.txt` names it.

---

## 23. Deprecation and removal

The project had no stated removal rule before the 2026-09-06 audit, though its behaviour was already consistent with the default below: the M5.5 deletion of the Next.js application was a plain delete with no shims, and it was correct.

**The rule.** Whether a removal needs a redirect is decided by whether the thing is public-facing, not by the fact that it is being removed.

### 23.1 The deploy boundary

Everything uploaded by `actions/upload-pages-artifact@v3` with `path: .` is public-facing. That is the whole repository root, which makes the boundary unusually wide here and worth stating precisely:

- **Public-facing:** every `.html` file at the root, `sw.js`, `manifest.webmanifest`, `favicon.svg`, everything under `assets/`, `robots.txt`, `sitemap.xml`, `LICENSE.md`, `README.md`, and `docs/`. All of it is fetchable at a real URL.
- **Internal:** `tools/` and `.github/`. These are uploaded too, and are technically fetchable, but nothing outside the repository is meant to link to them and they are not addresses this project promises to keep.

The distinction that matters: a name being derived from a source file does not make that source file public-facing. `tools/learn/c_toxic.py` produces `learn-toxic.html`. The **HTML** is the contract; the Python is not.

### 23.2 Public surface, item by item

| Address | Kind | Notes |
|---|---|---|
| `/` and `/index.html` | Page | |
| `/search.html` | Page | Accepts `q`, `brand`, `page`, `only` |
| `/brands.html` | Page | |
| `/product.html` | Page | Accepts `barcode` |
| `/scan.html` | Page | |
| `/submit.html` | Page | Accepts `barcode` |
| `/compare.html` | Page | Accepts `a`, `b` |
| `/methodology.html` | Page | |
| `/offline.html` | Page | Reached only by the service worker |
| `/learn.html` and ten `/learn-*.html` | Pages | Generated. The main search surface |
| `/tests.html` | Page | Public but unlinked. Not a promised address |
| `/sw.js` | Script | **Must stay at the root.** Its scope is its path |
| `/manifest.webmanifest`, `/favicon.svg`, `/assets/icons/*` | Assets | Referenced by installed PWAs |
| `/assets/*.css`, `/assets/*.js`, `/assets/js/*` | Assets | Referenced by every page and precached by the worker |
| `/assets/data/additives.json` | Data | Fetched at runtime |
| `/robots.txt`, `/sitemap.xml`, `/LICENSE.md`, `/README.md`, `/docs/*` | Documents | |

**Query parameters are part of the public surface too.** A change that renames `?barcode=` breaks every shared link and every scan result in somebody's history, and is a breaking change in the sense this section means.

### 23.3 Retiring a public address

The project has **no redirect mechanism at all.** GitHub Pages serves static files and this project has no server, no rewrite rules and no router. That is the constraint, so the mechanism is a **tombstone page**: leave an HTML file at the old address containing a `<meta http-equiv="refresh">` to the new one plus a `<link rel="canonical">` and a visible line of text explaining the move.

Where a *parameter* is retired rather than a page, the page keeps reading the old name and maps it to the new one in JavaScript, because the address still resolves.

Compatibility entries, once created, are permanent. They are never chained: a tombstone points at a real page in one hop, never at another tombstone. They are never reused to point at different content later, because a reused address silently serves the wrong thing, which is worse than a broken link.

### 23.4 Removing internal source

A plain delete. No redirect, no alias, no stub file, no tombstone. Nothing external points at it, so there is no address to preserve, and a permanent compatibility entry would be maintenance in exchange for nothing.

### 23.5 Retired items

| Item | Removed | Replaced by |
|---|---|---|
| The Next.js application (`app/`, `components/`, `next.config.ts`, `tailwind.config.ts`, `postcss.config.mjs`, `tsconfig.json`, `.eslintrc.json`, `package.json`) | 2026-09-05, M5.5 | Nothing. It was never built or deployed, so it had no public address. A plain delete, correct under this rule |
| Mock product data in `product.html` and `search.html` | 2026-09-05, M6 | Live Open Pet Food Facts records |
| `docs/TRD.md` | 2026-09-06, M13 | Section 16 of this document |
| `docs/RUNBOOK.md` | 2026-09-06, M13 | Section 15 |
| `docs/METRICS.md` | 2026-09-06, M13 | Section 14 |
| `docs/TENETS.md` | 2026-09-06, M13 | Section 10 |
| `docs/SECURITY.md` | 2026-09-06, M13 | Section 21 |
| `docs/PRFAQ.md` | 2026-09-06, M13 | Sections 27 and 28 |
| `docs/ROADMAP.md` | 2026-09-06, M13 | Section 13 |
| `docs/ADR-001-static-first.md` | 2026-09-06, M13 | Section 16.2 |
| `docs/DATA-COVERAGE.md` | 2026-09-06, M13 | Section 12 |
| `PATCHNOTES.md` at the repository root | 2026-09-06, M13 | Merged into `docs/PATCHNOTES.md` |
| The scorable-first result sort | 2026-09-06, M15a | Relevance ordering plus an opt-in filter |

Those documents were public-facing by the definition in 23.1, since `docs/` is uploaded and fetchable. They were deleted without tombstones, which is a **knowing exception** to 23.3: they were referenced only from within this repository, every reference was updated in the same commit, and a tombstone for a documentation file nobody links to externally would be maintenance in exchange for nothing. Recorded here so the exception is visible rather than silent.

### 23.6 Historical records

Changelog entries and version history are **not rewritten** when something is removed. They record what happened at the time rather than describing the current state. An entry saying the shell precache was 23 files stays as it is even though it is 29 today.

---

## 24. Documentation versus reality

Every discrepancy found in the 2026-09-06 audit, kept rather than silently fixed, with the source that was trusted and why. The code is treated as the truth about what **is**; the documentation is treated as the truth about what was **intended**.

### 24.1 Documented features that do not exist

| Claim | Where it was | Reality | Resolution |
|---|---|---|---|
| "User can submit barcode plus a photo of the label to add it to the queue"; "This feeds a review queue for editorial processing" | PRD §4.4, PRFAQ internal 9 and external 8 | **There is no queue and never will be.** M10 decided contributions go upstream | Trusted the code. The decision is deliberate and better-argued than the plan it replaced. Rewritten in sections 4, 13 and 28 |
| "Compare two or three products" | PRD §4.5 | Two only. A third column was dropped in M11 | Trusted the code; the reasoning is recorded in section 13 |
| "Better alternatives within the same format when the score is Poor or Bad" | PRD §7 | Never built | Kept as intent. Moved to the Future table in section 6 and the debt table in 16.11 |
| "Ingredient list, each item expandable for an explanation" | PRD §7, DESIGN §10 | **The chevron was never rendered.** Both documents said it was built and inert; the string never appears in any commit's code. The claim was wrong twice over | Built in M15c, for the rows the knowledge base can actually speak to. The documentation error is left here because a document that said "inert" for three milestones is the more useful record |
| "Submit queue processing, 50 or fewer waiting, internal queue dashboard" | METRICS | No queue exists, so the metric is unmeasurable | Deleted. It measured a feature that was cancelled |
| Score reveal count-up, ingredient expand transition, route transition fades, skeleton loaders, tier glyphs, Open Graph image | DESIGN §8, §9, §10, §12, all marked "planned" | None built | Kept, still marked as not built, in DESIGN.md |
| Scan button "disabled with tooltip in MVP", `role="tooltip"` on it | DESIGN §7, §10 | The scanner shipped in M8. There is no disabled button and no tooltip | Trusted the code. Removed |
| "Search by brand or product name", and every count and ranking claim that followed from it | PRD §6 and §13, DESIGN §5, PATCHNOTES M6 onward | **Text search never searched.** `/api/v2/search` ignored `search_terms` and returned the whole cat-food category for every query, including one that cannot match anything. The feature existed, was tested, and was documented; what it did was unrelated to what was typed | Fixed in M18 by moving text queries to `/cgi/search.pl`. The M15a entry that misread this as a ranking defect is left standing in §13 and in PATCHNOTES, with the correction recorded here |

### 24.2 Implemented features absent from the documentation

| Feature | Where it should have been | Now in |
|---|---|---|
| Brand browse, brand-filtered search, pagination, scorable-only filter | PRD, TRD, DESIGN | Sections 6, 11, 16, and DESIGN.md |
| The `MATCHED_LANGUAGES` guard and the whole language-correctness story | PRD | Sections 11.5 and 12.4 |
| Tier 0 of the additive knowledge base | PRD §6.3, which documented Tiers 1 to 3 only | Section 11.3 |
| Confidence levels on a score | PRD | Section 11.8 |
| The `scorable: false` refusal path | PRD | Sections 11.1 and 9 |
| Theme toggle and dark mode in the global chrome | PRD §4.1, DESIGN §10 | Section 16, DESIGN.md |
| Main navigation in the header | PRD §4.1 described only a wordmark and a Support button | Section 16, DESIGN.md |
| Offline behaviour, the cache stamp, `offline.html` | TRD had one line | Section 16.8 |
| Recently viewed as a real feature rather than a mock | PRD | Section 6 |
| The `esc()` escaping pattern as the injection defence | SECURITY claimed React did it | Section 21.6 |

### 24.3 Instructions that were wrong or stale

| Instruction | Where | Problem | Fixed to |
|---|---|---|---|
| "All rendered content is escaped by React's default JSX handling" | SECURITY | **There is no React.** Escaping is hand-rolled `esc()` calls. This was the most dangerous line in the documentation: it claimed a safety property the code does not get for free | Section 21.6, which names it as the highest-risk area |
| "`npm audit` is run as part of the local development workflow"; "Dependabot alerts"; "production dependencies are limited to Next.js, React, and React DOM" | SECURITY | No npm, no lockfile, no dependencies. None of it could run | Section 21.7 |
| "Set as GitHub Actions secrets and as `NEXT_PUBLIC_*` environment variables" | SECURITY | Next.js-specific guidance in a project with no Next.js | Section 21.4 |
| "Golden-file tests runnable in the browser and under `node --test`" | TRD §12, ADR-001 | There is no Node.js. The suite is browser-hosted only | Section 16.2 and 15.4 |
| "Analytics added in M10" | SECURITY | M10 was the submit flow. Analytics is M12 | Section 14 |
| "`npx lighthouse ...`" as the monitoring command | RUNBOOK | `npx` requires Node, which the prerequisites correctly say is absent | Section 15.10, PageSpeed Insights |
| "Precached shell, 23 entries" | TRD, ROADMAP | 29 today | Section 16.8. The historical changelog entry was left alone |
| "check-live.py, eight end-to-end checks" | TRD | 16 | Section 15.4 |
| "The four Tailwind pages" | README, TRD, in five places | Eight, now nine with `brands.html` | Throughout |
| "Current implementation state (v0.7.0)" | TRD §0 | Five releases stale | This document carries an audit date instead of a version |
| "The header is `fixed` on mobile and `sticky` on desktop" | DESIGN §5 | App pages are `sticky` at every width; guide pages are `fixed` at every width | DESIGN.md, corrected |
| "`bg-accent text-white`" in the button and badge patterns | DESIGN §6 | The code uses `text-on-accent`, and DESIGN §2 says never to hardcode `text-white` on an accent fill | DESIGN.md. The document contradicted itself; the token is right |
| "Product lists use `<ul role="list">` wrapping `<Link>` cards" | DESIGN §6 | `<Link>` is a React component. The code uses `<a>` | DESIGN.md |
| "`public/favicon.svg`" | DESIGN §12 | There is no `public/` directory. It is at the root | DESIGN.md |
| Routes written as `/search`, `/product/[barcode]` | DESIGN §10, PRD | Static hosting has no dynamic routes. They are `search.html` and `product.html?barcode=` | Throughout |

### 24.4 Contradictions between documents

| Contradiction | Resolution |
|---|---|
| PRD §6.3 defined **Tier 1** as "low or no concern, may earn a small positive". `additives.json` defines **Tier 0** as the benign tier and **Tier 1** as "flagged by marketing rather than evidence" | Trusted the code, which is also what `learn-additives.html` and `methodology.html` say. The PRD was the only document using the old meaning. Section 11.3 documents four tiers, 0 to 3 |
| Two changelogs existed, `PATCHNOTES.md` at the root at `[0.12.2]` and `docs/PATCHNOTES.md` at `v0.10.1`, describing the same work under different version numbers | Merged into `docs/PATCHNOTES.md`, keeping the root file's more detailed entries and its numbering, which tracked reality more closely. Both histories are preserved |
| DESIGN §2 forbids hardcoding `text-white` on an accent fill; DESIGN §6 prescribes `bg-accent text-white` | The prohibition is right and the code follows it |
| ADR-001 said tests are runnable "in the browser and in Node"; the RUNBOOK correctly said there is no Node | The RUNBOOK was right |

### 24.5 Structure that no longer matched

- Eleven files in `/docs` against a target of three. Resolved; see section 23.5.
- `README.md` was written for developers, carrying the stack, prerequisites, commands and deploy steps. Rewritten for a general reader, with all of that moved here.
- No `LICENSE.md`, `robots.txt` or `sitemap.xml` existed. All three created.

---

## 25. Risks and open questions

### 25.1 What was not fully verified in this audit

- **The eleven generated guide pages were not read line by line.** Their content modules under `tools/learn/` were treated as the source of truth and the generator was assumed to be faithful, on the evidence that `build.py` reproduces the committed HTML. The nutritional claims in that content have not been re-checked against their sources in this audit.
- **`assets/cfc.css`, 418 lines, was read for structure rather than rule by rule.** DESIGN.md describes its system accurately at the level of tokens and components; individual selector behaviour was not exhaustively catalogued.
- **CatFoodDB's product-entry layout is unverified.** Two guessed URLs returned 404 and no further attempt was made.
- **The 600-product sample behind section 12 was measured on 2026-09-05 and not re-measured.** The database moves.

### 25.2 Fragile areas

| Area | Why it is fragile |
|---|---|
| **`esc()` call sites** | Hand-rolled escaping with no framework behind it. One missed interpolation of community-edited text is an injection. There is no test that would catch a missing call |
| **`scoring.js`, roughly 500 lines** | The most complex logic in the project, and the place where a wrong answer does the most damage. Well covered by tests, but the tests are written by the same person as the matcher, which is precisely how the language defects survived 109 green assertions |
| **`sw.js`** | Caching bugs are invisible locally and persist on devices that cannot be reached. `VERSION` is the only reliable lever |
| **The duplicated dark palette** | Deliberate duplication in `cfc-tokens.css`, guarded by `check-contrast.py`. Remove the guard and the two copies drift silently |
| **Two generators over one chrome** | M14 ended the eight-file navigation edit, and replaced it with a single point of failure: `tools/site/chrome.py` is the only copy of the head, top bar, drawer and footer, and both generators import it. A mistake there is now a mistake on all twenty pages at once |
| **`tools/learn/` and `tools/site/` generation** | Editing a generated page directly appears to work and is silently reverted on the next build |
| **Unpinned ZXing CDN** | Third-party code that can change without a commit here. M14 removed the Tailwind CDN, which was the render-blocking one; the scanner library is still fetched at runtime |
| **The `|` OR syntax in `brands_tags`** | Verified empirically against the live API, not from documentation. If the upstream changes it, brand pages silently under-report |

No `TODO`, `FIXME` or `HACK` markers exist anywhere in the codebase.

### 25.3 Dangerous to change without context

| Change | What breaks |
|---|---|
| Making `cfc-theme.js` non-blocking, or moving it out of `<head>` | A flash of the wrong palette on every load. The blocking position is the entire mechanism |
| Moving `sw.js` out of the repository root | The worker's scope narrows and offline support silently stops covering the site |
| Using an absolute path anywhere | Works locally, 404s in production |
| Changing a tier in `additives.json` without changing `learn-additives.html` | The engine and the guide disagree, which is a trust failure rather than a bug |
| Extending `MATCHED_LANGUAGES` ahead of the aliases | Re-creates the exact defect of section 12.4: labels reported as clean because nothing matched |
| Renaming a query parameter | Breaks every shared link |

### 25.4 Work in progress

The working tree is clean and `main` is deployed. M14 and all four parts of M15 are shipped. Nothing is half-finished in the tree. The next work is the M12 run-up: the accessibility and performance gates, then the curated catalogue that coverage actually depends on.

### 25.5 Open questions

Numbered so they can be answered by reference. Answering one folds the answer into the relevant section and marks it answered here.

1. **Should a low-confidence score be visually distinct from a high-confidence one, or withheld?** Currently it is shown with a warning. Tenet 2 might argue for withholding.
2. **Is a curated local catalogue in scope for the MVP?** Section 12.5 says it is the only route to the M12 coverage target, which makes M12 unreachable without it.
3. **How aggressively should feeding-trial substantiation outweigh formulation?** The original PRD raised this; the engine currently does not distinguish them at all.
4. ~~**Should the scorable-only filter page-hunt?**~~ **Answered in M18:** it scans, which is the bounded half of hunting. Five pages are fetched in parallel, deduped and filtered once; the page then states what it scanned rather than implying it saw everything. An unbounded hunt was rejected for the reason the question raised: the friendlier version is the one whose number cannot be stated honestly.
5. ~~**What fills the guide shell's third column on a page with no headings?**~~ **Answered in M14:** nothing. The page collapses to one column, and `tools/site/build.py` decides per page by reading the fragment for headings rather than from a flag. See docs/DESIGN.md section 6.4.
6. ~~**Does the `/` search affordance stay on pages that already have a search input?**~~ **Answered in M14:** no. `index.html` and `search.html` are built with `show_search=False`.
7. ~~**Should Safari and Firefox be driven by any automated check?**~~ **Answered in M17:** yes, and they now are. `tools/check-engines.py` runs the unit suite, all 12 page states and the barcode decode round-trip in Blink, Gecko and WebKit. The answer to the `BarcodeDetector` worry is that neither Gecko nor WebKit has it at all, so ZXing is not a fallback on those engines, it is the only path scanning has, and the decode round-trip passes in all three. See section 19.3.
8. **Should the tombstone mechanism in 23.3 be built before it is needed, or written when first used?** It is currently a policy with no implementation.
9. **Is the six-language alias list the right stopping point?** It covers most of the database, but the honest-refusal path means every uncovered language is a product that cannot be fully scored.
10. **Should `tests.html` be excluded from the sitemap and from crawling?** It is public and unlinked. It is currently omitted from `sitemap.xml` but not disallowed in `robots.txt`, since that file is deliberately fully open.
11. ~~**Should the product page build its own "On this page" rail?**~~ **Answered in M15d:** yes. `tools/site/build.py` ships the column empty, hidden and marked `data-client-toc`; `assets/cfc-docs.js` fills it from `.article h2[id]` when the page dispatches `cfc:content`, and hides it again when a draw produces no sections. It is the only chrome the browser assembles, and it stays optional: with JavaScript off the product page has no content either, so there is nothing the rail could have indexed. See docs/DESIGN.md section 6.4.

---

## 26. Working practice

Concrete instructions for whoever works on this next, human or model.

### 26.1 Before editing anything

1. **Read this document's section 24** if you are about to change something the documentation describes. A discrepancy may already be recorded.
2. **Check whether the file is generated.** Every HTML page at the root except `tests.html` is: the guide pages by `tools/learn/build.py`, the other nine by `tools/site/build.py`. Editing one directly is silently undone.
3. **Check whether the change is public-facing** by the definition in section 23.1, because that decides whether a removal needs a tombstone.
4. **Never assume a documented behaviour exists.** This project has a history of documented features that were never built; section 24.1 lists them.

### 26.2 Never do these

| Never | Because |
|---|---|
| Use an absolute path (`/assets/...`) | The site is served from a repository subpath. It works locally and 404s in production |
| Hand-edit any root page but `tests.html` | All generated. Your change disappears on the next build |
| Move `cfc-theme.js` out of `<head>`, or add `defer`/`async` | The blocking position is what prevents a flash of the wrong palette |
| Move `sw.js` out of the root | Scope is derived from path. Offline support silently narrows |
| Add a Tailwind opacity modifier to a themed colour | It renders transparent. Add a token instead |
| Interpolate API text into HTML without `esc()` | There is no framework escaping it. This is the injection surface |
| Extend `MATCHED_LANGUAGES` before the aliases exist | Recreates the defect that made a bad product score 77/Excellent |
| Change a tier in `additives.json` alone | It must change in `learn-additives.html` too, or the site contradicts itself |
| Test against production | Section 20. Production is where you confirm a deploy, not where you test |
| Drive Chrome in an automated check | Section 19. Use Edge |
| Introduce a secret or a keyed API | Section 16.2. It is a trigger to revisit the architecture, not a routine addition |
| Rewrite a historical changelog entry to match today | Section 23.6 |

### 26.3 Where to look first

| Kind of work | Open first |
|---|---|
| Changing what a score means | `assets/js/scoring.js`, then section 11, then `methodology.html`, then `learn-additives.html` |
| Adding or retiring an additive | `assets/data/additives.json` and `learn-additives.html`, together |
| Anything touching API data | `assets/js/opff.js` and section 12 |
| Search, brands, pagination | `assets/js/search-page.js`, `assets/js/brands-page.js`, `opff.js` |
| A visual or layout change | `docs/DESIGN.md`, then `assets/cfc-tokens.css`, then the page |
| Palette or theming | `assets/cfc-tokens.css`, both dark blocks, then run `check-contrast.py` |
| Guide content | `tools/learn/c_<topic>.py`, never the HTML |
| Guide chrome | `tools/learn/shell.py` |
| Caching or offline behaviour | `sw.js`, and section 16.8 |
| Scanner behaviour | `assets/js/scanner.js` and `assets/js/scan-page.js` |
| Deploy or CI | `.github/workflows/deploy.yml` and section 15.5 |
| Anything about direction or priority | Section 13 |

### 26.4 How to verify a change

Run all three locally, in this order. All are local; none touches production.

```bash
python tools/run-tests.py        # 160 assertions. Must be green. This is the gate
python tools/check-contrast.py   # 38 pairs, both palettes. Required after any token change
python tools/check-live.py       # 19 end-to-end checks. Needs network. A smoke check, not a gate
```

Then look at the page in a browser at `http://localhost:8000`. Two of the four defects in section 12.4 were found by rendering a real product, not by a test.

If you changed the guide, run `python tools/learn/build.py`. If you changed an application page or the shared chrome, run `python tools/site/build.py` as well, because the chrome is in both. Commit the regenerated HTML.

If you added, renamed or removed any file the site loads, update `SHELL_ASSETS` in `sw.js`.

### 26.5 After a change

1. **Update `docs/PATCHNOTES.md`** with a versioned entry: Added, Changed, Fixed, Removed, each line one change in past tense.
2. **Update this document** where the change alters behaviour, architecture, the public surface, or a stated rule. Section 13 for direction, 16 for architecture, 23.2 for a new address, 23.5 for a removal.
3. **Update `docs/DESIGN.md`** for anything visual.
4. **Update `sitemap.xml`** if you added or removed a public page.
5. **Commit** in the house style: a `feat:`/`fix:`/`docs:` prefix, an imperative subject, and a body explaining why rather than what.
6. **Push to `main`**, which deploys.
7. **Confirm the deploy landed** by fetching the deployed file and comparing it to the local one. That is a comparison, not a test, and it is the one thing that legitimately happens against production.

---

## 27. Press release

*Written as if the product has just launched publicly. It has not: the site is live but has had no launch, and nothing in this section should be read as a claim about adoption. The customer quote is fictional and is labelled as such.*

### Cat Food Center puts an honest score on every cat food, free and without an account

**A scan of the barcode gives an owner a 0 to 100 rating, the reasoning behind it, and a straight answer when the data is not good enough to judge**

**Leeds, United Kingdom, 6 September 2026** - Cat Food Center today opened a free website that tells cat owners what is actually in the food they are buying. Point a phone at the barcode on a tin, and the site returns a plain-language breakdown of the ingredients, a flag on any additive linked to health concerns in cats, and a single score from 0 to 100 with a verdict: Excellent, Good, Poor or Bad. It runs in any modern browser, needs no account and no download, and works on a product already viewed even when the shop has no signal.

**The problem.** Cat food packaging is designed to be reassuring rather than informative. "Grain-free", "natural" and "premium" have no binding definitions. The facts that genuinely predict a cat's health, whether the first ingredient is a named animal protein, whether taurine is present, whether the food contains an additive prohibited in cat food, are printed in small type in a form most owners have no way to evaluate. Owners are left choosing between two tins with nothing to go on but the picture on the front.

**The solution.** Cat Food Center reads the label so the owner does not have to. It scores three things: whether the food delivers the protein a cat actually needs (55% of the score), whether it contains additives with documented concerns (35%), and whether the ingredient list is honest about where things came from (10%). Cats are obligate carnivores and cannot make taurine, arginine or arachidonic acid from plants, so the engine is built for cats specifically rather than adapted from a human or all-pets scale.

The part the project is most careful about is the opposite of scoring: refusing to. Roughly one product in five in the underlying open database carries enough information to judge on all three counts. Where the data is not there, the site says exactly what is missing instead of producing a number that looks like all the others. Where the ingredient list is in a language the checker does not fully cover, it says the label was not read rather than reporting silence as a clean result.

**"I stopped buying the expensive one."** *(Fictional, illustrative.)* "I'd been buying the same food for four years because the bag looked serious," said Priya Raman, a fictional cat owner representing the primary audience. "I scanned it in the shop and it came back Poor, with the reason written out: unnamed meat by-products first, added sugar near the end. The one next to it, half the price, came back Good. That is not something I could have worked out from the packaging."

**Try it.** Visit https://azqato.github.io/Cat-Food-Center/ and scan a tin, or search by brand. Nothing to install and nothing to sign up for.

**About Cat Food Center.** Cat Food Center is an independent, single-maintainer project built by Azqato. It takes no advertising, has no affiliate links, and has no commercial relationship with any pet food manufacturer. Its scoring methodology is published in full, its product data comes from the open Open Pet Food Facts database, and it also publishes a free eleven-page Cat Care Guide covering feline nutrition from AAFCO requirements to diet in disease. It is an information tool and not veterinary advice.

---

## 28. Frequently asked questions

### External

**1. What is Cat Food Center?**
A free website, installable as an app, that analyses cat food products and scores each from 0 to 100. Scan a barcode in a shop or search by brand at home, and you get the ingredients explained, any concerning additives flagged, a nutrition summary and an overall verdict.

**2. Who is it for?**
Anyone choosing cat food. It is built first for somebody standing in a shop with a tin in their hand, and second for somebody comparing brands at home before a bigger order.

**3. How do I use it?**
Open the site. Either tap Scan and point the camera at the barcode, or type a brand or product name into the search box, or browse by brand. Pick a result and you land on its page: score at the top, reasoning underneath. To compare two foods, open the Compare page and pick two.

**4. How does the scoring work?**
Three parts: nutrition for a cat specifically (55%), additives with documented concerns (35%), and how honest and traceable the ingredient list is (10%). Cats are obligate carnivores, so the model is built around their needs rather than a generic pet or human scale. The full method is published on the methodology page.

**5. What does it cost?**
Nothing. There is no paid tier, no subscription and no advertising. It is available anywhere with a browser.

**6. What do I need to run it?**
Any modern browser. Scanning needs a camera and a secure (HTTPS) connection, which the live site provides. If your browser cannot scan, typing the barcode works just as well. You can add it to your home screen, after which previously viewed products stay readable with no connection.

**7. Are there any deals with pet food brands?**
No. No brand pays to appear, and none can change or hide a score. There are no affiliate links and no advertising, and the method is public so anyone can check.

**8. How accurate is the data?**
The product data comes from Open Pet Food Facts, a community-maintained open database, and coverage varies a lot by brand. About one product in five carries enough information to score fully. When data is missing, the site says so and adjusts or withholds the score rather than inventing values.

**9. Why does a product say it cannot be scored?**
Because the database has no ingredient list for it, or nothing usable in the nutrition panel. That is a statement about the record, not about the food. Anyone can add the missing information at Open Pet Food Facts, and the submit page explains how.

**10. Why does it sometimes say it could not read the label?**
Only about one record in ten has an English ingredient list. The additive checker covers English, French, German, Spanish, Italian and Dutch. Outside those, it tells you the label was not checked instead of reporting a clean result, because finding nothing in a language you cannot read is not the same as finding nothing.

**11. How is this different from other cat food sites?**
Three things. The score is computed from the label rather than assigned by a reviewer, so it is reproducible and the method is published. There is no revenue path that touches it: no ads, no affiliate links, no sponsorship. And it refuses to score when it cannot, where most comparison sites rate everything.

**12. What does it not do, in this version?**
No dog food. No personalised diet plans or medical advice. No user reviews or star ratings. No shopping or price comparison. No accounts. It compares two products at a time, not three. Product photos appear on the product page but not yet on result cards.

**13. My cat has kidney disease, diabetes or a urinary condition. Can I rely on this?**
No. It is an informational tool, not veterinary advice. It helps you compare products and spot red flags, but the scores reflect population-level nutrition science, not your cat. For a cat with a diagnosis, follow your veterinarian, ideally with input from a board-certified veterinary nutritionist.

**14. What data do you collect about me?**
None. There is no account, no login, no analytics and no tracking of any kind. Recently viewed products are stored in your own browser and never leave your device. The camera runs entirely on your device and no frame is uploaded. The barcodes and search terms you look up are sent to Open Pet Food Facts, because that is the lookup, and your browser's IP is visible to that service and to the hosting and font providers, as with any website.

**15. Can I use it offline?**
Partly. Once installed, any product you have already opened stays readable with no connection, and every cached answer is clearly labelled as a saved copy with the date. Anything new needs a connection.

**16. What is the Cat Care Guide?**
A free eleven-page guide covering feline nutrition fundamentals, the complete AAFCO daily nutrient requirement for all 42 nutrients, reading a label, food formats, hydration, additives, feeding practice, life stages, toxic foods, and diet in common conditions. It is useful on its own, without looking up a single product.

**17. A product I want is not there. What do I do?**
The site checks first whether you have mistyped the barcode, which is the most common cause. If it really is missing, it links you to Open Pet Food Facts with the barcode filled in and tells you which two panels to photograph: the ingredient list and the guaranteed analysis including moisture.

**18. Why send me to another site to add it?**
Because every score here comes from that database. Adding it there means it works here, in any other tool built on the same data, and for the next person who scans the same tin. A private queue of our own would leave the product missing from the database that the scores actually read.

**19. Why cats only?**
Cats and dogs have genuinely different nutritional requirements, and one engine accurate for both is harder than one that is right for each. Starting with cats, where obligate-carnivore nutrition gives a firm foundation, produces a defensible engine rather than a generic one.

**20. Can I trust a score on a product with missing data?**
Read the confidence level and the warnings, which are shown with it. A score built on all three pillars from a full guaranteed analysis is a stronger claim than one built on the ingredient list alone, and the site tells you which you are looking at. On the compare page, two products scored on different pillars are never ranked against each other.

**21. Where do the additive claims come from?**
Each carries a source: FDA, EFSA, WHO or IARC positions, or peer-reviewed veterinary literature. Where the evidence is genuinely contested, such as carrageenan, the guide says so instead of picking a side.

**22. How do I get help, or report a mistake?**
Open an issue at https://github.com/Azqato/Cat-Food-Center/issues. For a wrong product fact rather than a wrong score, correcting it at Open Pet Food Facts fixes it everywhere.

### Internal

**23. What is the return on this, and what would tell us it is working?**
There is no revenue and no plan for one, so the return is a working, credible public tool. The measure is the north star in section 14: scan-to-verdict completions per week, meaning somebody actually got an answer. Nothing is instrumented yet, which is an M12 gap and means current usage is unknown.

**24. What is the core technical risk?**
Catalogue completeness. Section 12 measured it: about one product in five is fully scorable and under one in ten has English ingredients. Degrading gracefully and never fabricating a value is what keeps this a credibility-neutral problem rather than a credibility-destroying one.

**25. What would make us abandon the static architecture?**
Three things, listed in section 16.2: upstream contribution stops being viable, per-product pages need search indexing and pre-generation is insufficient, or the engine outgrows the absence of type checking. None has happened.

**26. How do we stay unbiased as it grows?**
Tenet 4, and the fact that the method is published and computed in the reader's own browser. A sceptic can watch the score being derived in devtools.

**27. What is the direction from here?**
Section 13: one interface across the whole site (M14, decided), photos on result cards (M15b), then a curated catalogue and instrumentation for a public beta (M12).
