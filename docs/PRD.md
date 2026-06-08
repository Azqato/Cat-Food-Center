# Product Requirements Document (PRD)

**Product:** Cat Food Center
**Tagline:** Trustworthy reviews for your purrfect companion!
**Document type:** Living specification. Treat this file as the source of truth for product behavior.

---

## 1. Vision

Choosing cat food is overwhelming. Labels are dense, marketing is loud, and the science that actually matters for cats is buried. Cat Food Center gives owners objective, science-based reviews so they can make informed decisions and keep their cats healthy and happy.

We analyze ingredients, nutritional value, and additives for cat food products, score each on a transparent scale, and present the result in seconds. Reviews are unbiased: no advertiser pays to change a score.

## 2. Goals and non-goals

### Goals

- Let an owner identify any cat food product (scan or search) and understand its quality in under 30 seconds.
- Produce a single, defensible health rating per product, plus the reasoning behind it.
- Flag additives with real health concerns for cats and explain why, with cited sources.
- Work on a phone in a store aisle, and equally well in a desktop browser.

### Non-goals (v1)

- No e-commerce or affiliate checkout.
- No personalized medical/diet plans (we surface warnings, not prescriptions).
- No user-generated reviews in v1 (editorial and algorithmic scoring only).
- No dog food (cats only, on purpose).

## 3. Target users

- **The aisle shopper:** standing in a store, deciding between two cans, wants a fast verdict.
- **The researcher:** comparing brands at home before a bulk order.
- **The concerned owner:** cat has a sensitive stomach or a new diagnosis, wants to avoid specific additives.

## 4. Core user flows

1. **Scan flow:** open app, tap scan, camera reads barcode, product page loads with score and breakdown.
2. **Search flow:** type brand or product name, pick from results, land on product page.
3. **Product page:** score header, ingredient list with explanations, additive flags, nutrition snapshot, AAFCO adequacy statement, alternatives.
4. **Not-found flow:** product missing from catalog, user can submit barcode plus a photo of the label to add it to the queue.
5. **Compare flow:** add two or three products to a side-by-side comparison.

## 4.1 Global UI

A persistent **header** on every screen contains the wordmark (links to `/`) and a **Support** button linking to `https://azqato.github.io/support.html`.

A persistent **footer** on every screen reads "Built by Azqato" with Azqato linking to `https://azqato.github.io/index.html`.

## 5. Platform requirements

- **Mobile first.** Every screen is designed for a phone first, then enhanced for larger viewports.
- **Browser option.** Full functionality in desktop browsers; search-driven when no camera is present.
- **Installable PWA.** Add to home screen, offline access to previously viewed products and the additive knowledge base.

## 6. The rating engine (CFC Score)

The CFC Score is a 0 to 100 number with a color band. It is purpose-built for cats, because cats are obligate carnivores: they need animal-based protein for taurine and arginine, which they cannot make from plants, plus arachidonic acid, which they cannot synthesize from linoleic acid. Human food-scoring systems (such as Nutri-Score) are not appropriate, and we do not use them.

### 6.1 Three pillars

| Pillar | Weight | What it measures |
|---|---|---|
| A. Nutritional quality | 55% | Species-appropriate nutrition for cats |
| B. Additives and safety | 35% | Presence and risk level of flagged additives |
| C. Ingredient quality and transparency | 10% | Sourcing honesty, named ingredients, recall history |

### 6.2 Pillar A: Nutritional quality (55%)

Scored on a dry-matter basis where data allows. Sub-factors:

- **Animal-protein dominance:** is a named animal protein (chicken, salmon, turkey) the first ingredient, and what is the animal-to-plant protein ratio. Plant proteins (pea protein, corn gluten meal, soy protein isolate, potato protein) inflate the crude-protein number but have lower biological value for cats, so they are discounted.
- **Essential nutrient sufficiency:** crude protein, taurine, arginine, arachidonic acid, crude fat, and key vitamins/minerals checked against the AAFCO feline nutrient profile for the stated life stage. Taurine is weighted heavily; deficiency is linked to dilated cardiomyopathy and retinal degeneration in cats.
- **Carbohydrate and filler load:** lower is better. Heavy grain or starch fillers (corn, wheat gluten) reduce the score.
- **Moisture:** wet/canned formats receive a small bonus for supporting hydration and urinary-tract health.
- **AAFCO life-stage adequacy:** "complete and balanced" for a defined life stage is required to score well. Products substantiated by feeding trials score higher than those substantiated by formulation alone.

### 6.3 Pillar B: Additives and safety (35%)

Each additive is matched against our knowledge base and assigned a risk tier based on recommendations from the FDA, EFSA, and the WHO/IARC, plus published veterinary studies. The product page shows, for every flagged additive: its function, its tier, a plain-language health impact, and the source.

- **Tier 3, high risk (triggers a score cap):**
  - Propylene glycol (prohibited by the FDA in cat food; linked to red blood cell damage and Heinz body anemia)
  - BHA, BHT, ethoxyquin (synthetic preservatives linked to organ and carcinogenicity concerns in animal studies)
  - Artificial dyes (Red 40, Yellow 5, Blue 2, or "color added") which serve no nutritional purpose for cats
- **Tier 2, moderate risk (point penalties):**
  - Carrageenan and certain gums (guar, cassia, xanthan) associated with intestinal inflammation
  - Menadione (synthetic vitamin K3)
  - Added sugars (caramel, corn syrup, dextrose) linked to obesity and diabetes
  - Unnamed "meat by-products," "animal digest," or rendered fat of unknown origin
- **Tier 1, low or no concern (no penalty, may earn a small positive):**
  - Mixed tocopherols (natural vitamin E), rosemary extract
  - Natural colorants (beet juice, turmeric)
  - Supplemental taurine

### 6.4 Pillar C: Ingredient quality and transparency (10%)

- Named versus unnamed protein and fat sources.
- Manufacturer transparency: sourcing, country of origin, who formulates the food.
- FDA recall history for the brand or product line.

We use this pillar instead of an "organic" bonus because organic certification matters far less to feline health than protein quality, transparency, and additive load.

### 6.5 Hard gates and caps

- **Propylene glycol detected:** automatic red flag; product is capped in the Bad band (0–24), regardless of nutrition.
- **Any Tier 3 additive present:** maximum possible score is 49 (Poor ceiling), regardless of nutrition.
- **Not complete and balanced:** if a product is not AAFCO complete and balanced for any life stage and is not labeled a treat, snack, or complementary food, the page shows a nutritional-adequacy warning banner.

### 6.6 Score bands

| Band | Range | Color |
|---|---|---|
| Excellent | 75–100 | Dark green (#1B7A4B) |
| Good | 50–74 | Light green (#5FA855) |
| Poor | 25–49 | Orange (#E08A1E) |
| Bad | 0–24 | Red (#C0392B) |

### 6.7 Worked example

A semi-moist food whose first ingredient is corn, with unnamed meat by-products, added caramel color, and propylene glycol: propylene glycol triggers the hard gate, so the product lands in Bad (red) with a "contains an ingredient prohibited in cat food" callout, even before the nutrition math runs.

## 7. Product page contents

- Score header (number, band, color, product image, brand).
- One-line verdict and the top one to three reasons.
- Ingredient list, each item expandable for an explanation.
- Additive flags, grouped by tier, each with source.
- Nutrition snapshot (protein, fat, moisture, taurine presence) on a dry-matter basis where possible.
- AAFCO statement and life stage.
- "Better alternatives" within the same format (wet, dry) when the score is Poor or Bad.

## 8. Trust and transparency requirements

- The methodology page is always reachable and matches this PRD.
- Every additive claim cites a source.
- No advertiser can alter a score. If sponsorship ever exists, it must be visually separated and never affect ratings.
- Scores and data carry a "last reviewed" date.

## 9. Accessibility and quality bar

- Color is never the only signal; bands always carry a text label and an icon (color-blind safe).
- Targets meet WCAG AA contrast.
- Camera permission has a graceful fallback to search.
- Product page interactive in under two seconds on a mid-range phone.

## 10. Success metrics

- Scan-to-result success rate above 90% for catalogued products.
- Median time from app open to a verdict under 30 seconds.
- Catalog coverage of the top mainstream cat food SKUs.
- Repeat usage: owners returning before purchases.

## 11. Open questions

- Localization beyond US barcodes and AAFCO (EU FEDIAF profiles later).
- Treat-specific scoring rules (treats are not complete diets and need a separate rubric).
- How aggressively to weight feeding-trial substantiation versus formulation.

## 12. References

- AAFCO model regulations and cat food nutrient profiles: https://www.aafco.org
- FDA Center for Veterinary Medicine (pet food, recalls): https://www.fda.gov/animal-veterinary
- Open Pet Food Facts (open product catalog): https://world.openpetfoodfacts.org
- Yuka methodology (inspiration for the scoring structure): https://help.yuka.io
