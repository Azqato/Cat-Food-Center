# Open Pet Food Facts: what the data actually contains

- **Measured:** 2026-09-05
- **Method:** 600 unique products sampled from `categories_tags_en=cat-food` via the v2 search API (6 pages × 100), fields requested explicitly.
- **Reproduce:** `python tools/probe-opff.py` (defaults to the same 6 pages)

> The database is crowd-sourced and moves. Re-run the probe before relying on any
> number here rather than citing this document as current.

---

## Why this document exists

M6 and M7 were specified on the assumption that Open Pet Food Facts would supply
an ingredient list and a guaranteed analysis for a typical product, and that the
scoring engine would mostly be doing arithmetic. That assumption is wrong, and it
is wrong in ways that change the design rather than just the error handling.

Measuring first was cheap. Discovering this after building a scoring engine that
assumes complete input would not have been.

## Headline numbers

Of 600 cat food products:

| Field | Present | Note |
|---|---|---|
| Product name | 92.2% | Often just a brand fragment ("fancy feast") |
| Brand | 88.0% | Sometimes a numeric ID instead of a name |
| Front image | 96.8% | The best-covered field in the database |
| Quantity | 80.2% | |
| Wet/dry known from category tags | 34.0% | Matters — dry-matter conversion depends on it |
| **Ingredients (any language, >60 chars)** | **38.2%** | |
| Ingredients in English | 9.5% | The database is Europe-weighted |
| **Any protein figure** | **30.8%** | |
| **Protein figure that is plausible** | **23.0%** | See "Implausible values" below |
| Moisture | 15.2% | Required for dry-matter conversion |
| Fibre (either spelling) | 24.7% | `crude-fibre` or `fiber` |
| Crude ash | 20.8% | Only via the `crude-ash` key; `ash` is never used |
| Taurine | 4.3% | |
| **Ingredients AND protein AND fat together** | **22.3%** | Counting both schemas |

**About one product in five carries enough data to score the way PRD §6
describes** — and only 23% have a protein figure that survives a plausibility
check. Partial data is not an edge case here. It is the normal case.

## Two competing nutriment schemas

This is the most important structural finding. Open Pet Food Facts inherits Open
Food Facts' human-food nutriment keys, but pet food uses guaranteed-analysis
keys. Both appear, and mostly not together:

| Schema | Keys | Products |
|---|---|---|
| Guaranteed analysis (pet food) | `crude-protein`, `crude-fat`, `crude-fibre`, `crude-ash`, `moisture` | 116 crude-only |
| Human food | `proteins`, `fat`, `fiber`, `carbohydrates`, `salt` | 55 human-only |
| Both | — | 14 |
| Neither | — | 415 |

Note also that **`ash` does not exist** — it is always `crude-ash`, and `fibre`
is British-spelled in the crude schema but American-spelled (`fiber`) in the
human one. Any normaliser must read both spellings of both schemas.

## Implausible values

**25% of the products that have a protein figure at all have an implausible
one** (47 of 185). The failure is systematic, not random noise: the human-food
keys are frequently filled in with *per-serving* or *per-can* values while being
labelled `_100g`.

Real examples:

| Product | Protein/100g | Fat/100g | kcal/100g | What is wrong |
|---|---|---|---|---|
| Gourmet `7613034452481` | 1.2 | 0.3 | 2 | A wet cat food is ~8–12% protein and ~70–90 kcal/100 g. These look like per-gram values |
| Sheba `4770608247027` | 1.6 | 0.9 | 8 | Same pattern |
| Hill's `0052742869605` | 28.7 | 22.05 | **1774** | Protein and fat are right for a dry food; the energy figure is per **kilogram**, not per 100 g |
| Vitakraft `4008239352873` | 0.75 | 2.05 | 48.3 | Fat exceeds protein by 3× — not a cat food composition |

By contrast, the `crude-*` schema values are consistently sane, because they are
transcribed from the guaranteed-analysis panel on the packaging:

```
Dreamies (dry)   protein 22   fat 22   fibre 2     ash 8     416 kcal/100g
Whiskas (wet)    protein 8.7  fat 4    fibre 0.25  ash 1.6   moisture 84.5
```

**Conclusion: trust `crude-*`; treat the human-food keys as a low-confidence
fallback that must pass a plausibility gate before use.**

## What this means for the design

1. **The normaliser reads both schemas**, preferring `crude-*`, and records
   which one it used. Provenance is not optional — a score derived from a
   low-confidence fallback must be labelled as such.

2. **A plausibility gate runs before scoring.** A cat food as fed is roughly
   3–50% protein, 0.5–40% fat, 0–90% moisture, and 15–600 kcal/100 g. Values
   outside those ranges are rejected as data errors rather than scored. Rejecting
   a figure is better than publishing a score built on `2 kcal/100 g`.

3. **Energy needs unit inference.** A `kcal/100g` value above 600 is almost
   certainly per kilogram; it can be divided by 10 and flagged, or dropped. Do
   not silently trust the label.

4. **Partial scoring is the primary path, not a degraded one.** The UI must lead
   with what is known and be explicit about what is missing. A product with
   ingredients but no analysis can still be scored on additives and transparency;
   it cannot be scored on nutrition, and the score must say so rather than
   quietly assuming an average.

5. **Do not report a 0–100 score as though it were comparable across products
   with different data completeness.** Either show the pillars that could be
   computed, or show a confidence level alongside the number. This is a PRD
   question, not an implementation detail — see "Open questions".

6. **Wet vs dry is only known for 34% of products**, and dry-matter conversion
   depends on it. Where moisture is present, it can be inferred (>60% moisture is
   wet). Where neither is present, dry-matter comparisons cannot be made.

7. **The top-100 SKU catalog target in M12 will not be met by the API alone.**
   Hitting 80% coverage of common US SKUs means curating a local JSON catalog for
   those products, which the static architecture supports well
   ([ADR-001](./ADR-001-static-first.md)) — committed data under `assets/data/`,
   with the API as the fallback for everything outside the catalog.

## Language is a correctness problem, not a translation problem

Added 2026-09-05, after rendering real product pages.

Only **9.5%** of records carry `ingredients_text_en`. The database is
Europe-weighted, so the ingredient list you actually get is usually French,
German, Spanish, Italian or Dutch.

Every text check in the scoring engine — flagged additives, catch-all terms,
whether the first ingredient is a named animal protein — is alias matching
against an ingredient string. An English-only alias list does not *fail* on a
French label. It matches nothing, and matching nothing is indistinguishable, to
the code, from a clean label.

The product that exposed this was barcode `3596710487455` (Auchan, French):

```
Viandes et sous-produits animaux (dont boeuf 4% et foie 4%), céréales,
légumes (3% de carottes et 2% de haricots verts), substances minérales, sucres
```

That is unnamed meat by-products as the main ingredient and added sugar at the
end. It scored **77 / Excellent**, with a transparency pillar of 100 and the
reason *"Ingredient sources are named rather than generic."* Every word of that
was wrong, and it was wrong in the most damaging possible direction: a trust
product telling someone that a food it could not read is a good one.

It now scores **70 / Good**, flags the sugar, flags the unnamed source, and says
the species of the first ingredient is not stated.

**Four separate defects sat behind that one score. Three were not about
language at all — the English-only matcher was hiding them.**

| Defect | Fix |
| --- | --- |
| Aliases were English-only, so ~90% of labels silently matched nothing | French, German, Spanish, Italian and Dutch aliases in `additives.json`, and in the animal-protein, plant-protein and starch lists in `scoring.js` |
| A label in a language the aliases do not cover was still reported as clean | `MATCHED_LANGUAGES` guard: silence from an unreadable label is stated as unchecked, the clean-formulation bonus is withheld, confidence is capped at low, and a warning says so |
| `named-by-products` (a Tier 0 *beneficial* entry) has bare stems as aliases — `by-product`, `sous-produits` — so **"meat by-products" earned a bonus for being a named source while the transparency pillar penalised the very same words for being unnamed** | Tier 0 credit is matched per ingredient entry and withheld when that entry is itself an unnamed source |
| A parenthetical renamed an unnamed source: `(dont boeuf 4%)` made "viandes et sous-produits animaux" read as a named beef first ingredient, worth full marks | Entries matching an unnamed-source term are judged on the text before the parenthesis, across the whole first-three window |

The third and fourth were live in English too. They had simply never fired,
because no English product had reached the renderer.

### Consequences

8. **Any text check is a language check.** A new alias list is not complete
   when it is complete in English. `MATCHED_LANGUAGES` in `scoring.js` is the
   record of which languages the aliases actually cover, and it must be updated
   with them, not ahead of them.

9. **Silence is not evidence.** Where the engine cannot read a label it says so,
   rather than reporting the absence of a match as the absence of a problem.
   This is the single most important rule in the scoring module.

10. **Render real products early.** The unit suite was 109 green while all four
    of these defects were live, because every fixture was English and written by
    the same person who wrote the matcher. One real page found what the whole
    suite could not.

## Open questions for the PRD

- Should a product with no nutrition data receive a partial score, or no score
  and an explanation? The tenets argue against implying precision we do not have.
- Should a low-confidence score be visually distinct from a high-confidence one,
  or withheld entirely?
- Is a curated local catalog for common SKUs in scope for the MVP, given it is
  the only route to meaningful coverage?

## Practical API notes

- Base: `https://world.openpetfoodfacts.org/api/v2/`
- No API key. CORS is permissive, so the browser can call it directly.
- Send a descriptive `User-Agent` — it is the documented courtesy and it is how
  the project is identified in their logs.
- Always pass `fields=` — a full product record is 103 keys and most are
  editorial metadata (`correctors_tags`, `interface_version_modified`).
- `GET /product/<barcode>.json` returns HTTP 404 with `status: 0` for an unknown
  barcode. A miss is common and is not an error condition.
