/* ==========================================================================
   The CFC Score.

   A pure, deterministic module: the same product always yields the same
   result, and nothing here touches the network or the DOM. It runs in the
   visitor's browser, which is deliberate — a sceptical reader can open
   devtools and watch a score being derived. See docs/ADR-001-static-first.md.

   The methodology is published in PRD.md §6 and on methodology.html. This file
   is the implementation of that document; if the two disagree, the document is
   wrong until fixed, because it is what we tell people we do.

   ── The thing that shapes this file most ──

   docs/DATA-COVERAGE.md measured the real database: about a fifth of products
   carry enough data to score all three pillars, and a quarter of the products
   with a protein figure carry an implausible one. So partial data is the
   normal path, not an error path, and the engine is built around three rules:

     1. A pillar that cannot be computed is reported as unavailable rather
        than scored as zero. Scoring an unknown as zero would punish products
        for the database's gaps.
     2. Weights are renormalised across the pillars that could be computed,
        and the result says which those were.
     3. If too little is known to be meaningful, the engine returns
        scorable:false rather than a number. Refusing to score is a valid,
        and often the honest, outcome.
   ========================================================================== */

/* PRD §6.1. These must stay in sync with methodology.html. */
export const WEIGHTS = { nutrition: 0.55, additives: 0.35, transparency: 0.10 };

/* PRD §6.6. */
export const BANDS = [
  { band: 'excellent', min: 75, label: 'Excellent' },
  { band: 'good', min: 50, label: 'Good' },
  { band: 'poor', min: 25, label: 'Poor' },
  { band: 'bad', min: 0, label: 'Bad' },
];

/* AAFCO adult maintenance minimum, dry-matter basis. The guide's
   learn-daily-requirements.html carries the full 42-nutrient table; these are
   the two the API can ever supply. */
const AAFCO_ADULT_MIN = { proteinDM: 26, fatDM: 9 };

/* Named animal proteins. A named source is the signal — "chicken" scores,
   "meat" does not, which is Pillar C's whole point. */
const ANIMAL_PROTEINS = [
  'chicken', 'turkey', 'duck', 'goose', 'quail', 'salmon', 'tuna', 'trout',
  'whitefish', 'herring', 'mackerel', 'sardine', 'anchovy', 'cod', 'beef',
  'lamb', 'pork', 'rabbit', 'venison', 'bison', 'liver', 'heart', 'kidney',
  'gizzard', 'egg', 'chicken meal', 'turkey meal', 'salmon meal', 'lamb meal',
];

/* Plant proteins inflate the crude-protein figure without supplying taurine or
   arginine at feline biological value (PRD §6.2). */
const PLANT_PROTEINS = [
  'pea protein', 'corn gluten', 'wheat gluten', 'soy protein', 'soybean meal',
  'potato protein', 'rice protein', 'pea flour', 'lentil', 'chickpea',
];

/* High-glycaemic starch sources. */
const STARCH_FILLERS = [
  'corn', 'maize', 'wheat', 'rice', 'potato', 'tapioca', 'sorghum', 'barley',
  'oat', 'soybean', 'cereal',
];

/* ── Text matching ── */

/**
 * Whether `needle` appears in `haystack` as a whole word or phrase.
 *
 * Substring matching is not safe here: the alias "bha" would fire on
 * "bhakti", and "oat" on "coating". Both are real ingredient-label words.
 *
 * A trailing "s" is allowed, because aliases are written in the singular but
 * labels are usually plural — "meat by-products", "mixed tocopherols",
 * "artificial colours". Without this the unnamed-source penalty never fires on
 * a real label, which is exactly the bug the tests caught.
 */
export function matchesTerm(haystack, needle) {
  const escaped = needle.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  return new RegExp('(^|[^a-z0-9])' + escaped + 's?($|[^a-z0-9])', 'i').test(haystack);
}

function anyMatch(text, terms) {
  return terms.some((t) => matchesTerm(text, t));
}

/* ── Dry-matter conversion ── */

/**
 * Convert an as-fed percentage to dry matter (learn-labels.html §3).
 *
 *     dry matter % = as fed % ÷ (100 − moisture %) × 100
 *
 * Without this, a wet food at 8% protein looks worse than a dry food at 30%
 * when the wet food is in fact the more protein-dense of the two.
 */
export function toDryMatter(asFedPct, moisturePct) {
  if (typeof asFedPct !== 'number') return undefined;
  if (typeof moisturePct !== 'number') return undefined;
  const solids = 100 - moisturePct;
  if (solids <= 0) return undefined;
  return (asFedPct / solids) * 100;
}

/**
 * Carbohydrate by difference — nitrogen-free extract (learn-labels.html §5).
 * Needs all four other fractions, so it is often unavailable.
 */
export function carbsByDifference({ proteinDM, fatDM, fibreDM, ashDM }) {
  const parts = [proteinDM, fatDM, fibreDM, ashDM];
  if (parts.some((v) => typeof v !== 'number')) return undefined;
  const carbs = 100 - parts.reduce((a, b) => a + b, 0);
  // A negative result means the analysis does not add up — a data error, not a
  // food with negative carbohydrate.
  return carbs >= 0 && carbs <= 100 ? carbs : undefined;
}

/* ── Pillar A: nutritional quality (55%) ── */

/**
 * Each sub-factor contributes only if its data exists. The pillar score is the
 * points earned as a fraction of the points that were actually assessable, so
 * a product is never penalised for a figure nobody entered.
 */
function scoreNutrition(product) {
  const n = product.nutrition || {};
  const reasons = [];
  let earned = 0;
  let possible = 0;
  // Points that came from a published analysis rather than from ingredient
  // order. A pillar built only on ingredient order is a much weaker claim.
  let analysisPoints = 0;

  const proteinDM = toDryMatter(n.crudeProteinPct, n.moisturePct);
  const fatDM = toDryMatter(n.crudeFatPct, n.moisturePct);
  const fibreDM = toDryMatter(n.crudeFibrePct, n.moisturePct);
  const ashDM = toDryMatter(n.ashPct, n.moisturePct);
  const carbsDM = carbsByDifference({ proteinDM, fatDM, fibreDM, ashDM });

  const ingredients = product.ingredients || [];
  const firstThree = ingredients.slice(0, 3).join(' ').toLowerCase();
  const first = (ingredients[0] || '').toLowerCase();

  /* Animal-protein dominance — 35 points. */
  if (ingredients.length) {
    possible += 35;
    if (anyMatch(first, ANIMAL_PROTEINS)) {
      earned += 35;
      reasons.push('A named animal protein is the first ingredient.');
    } else if (anyMatch(first, PLANT_PROTEINS)) {
      earned += 6;
      reasons.push('A plant protein is the first ingredient. Plant proteins inflate the crude-protein figure without supplying taurine or arginine at feline biological value.');
    } else if (anyMatch(first, STARCH_FILLERS)) {
      earned += 4;
      reasons.push('A starch source is the first ingredient rather than an animal protein.');
    } else if (anyMatch(firstThree, ANIMAL_PROTEINS)) {
      earned += 22;
      reasons.push('A named animal protein appears in the first three ingredients, but is not first.');
    } else if (anyMatch(firstThree, PLANT_PROTEINS)) {
      earned += 6;
      reasons.push('A plant protein leads the ingredient list. Plant proteins inflate the crude-protein figure without supplying taurine or arginine at feline biological value.');
    } else if (anyMatch(firstThree, STARCH_FILLERS)) {
      earned += 4;
      reasons.push('A starch source leads the ingredient list rather than an animal protein.');
    } else {
      earned += 10;
      reasons.push('The leading ingredients could not be identified as either a named animal protein or a known plant source.');
    }
  }

  /* Protein level on a dry-matter basis — 25 points, against the AAFCO adult
     minimum of 26% DM. */
  if (typeof proteinDM === 'number') {
    possible += 25;
    const bands = [[45, 25], [40, 22], [35, 18], [30, 13], [26, 8]];
    const hit = bands.find(([threshold]) => proteinDM >= threshold);
    earned += hit ? hit[1] : 0;
    analysisPoints += 25;
    reasons.push(
      proteinDM >= AAFCO_ADULT_MIN.proteinDM
        ? `Crude protein is ${proteinDM.toFixed(1)}% on a dry-matter basis, against the AAFCO adult minimum of ${AAFCO_ADULT_MIN.proteinDM}%.`
        : `Crude protein is ${proteinDM.toFixed(1)}% dry matter, below the AAFCO adult minimum of ${AAFCO_ADULT_MIN.proteinDM}%.`);
  }

  /* Carbohydrate load — 20 points. Lower is better for an obligate carnivore. */
  if (typeof carbsDM === 'number') {
    possible += 20;
    const bands = [[10, 20], [20, 16], [30, 11], [40, 5]];
    const hit = bands.find(([ceiling]) => carbsDM < ceiling);
    earned += hit ? hit[1] : 0;
    analysisPoints += 20;
    reasons.push(`Carbohydrate by difference is about ${carbsDM.toFixed(0)}% of dry matter.`);
  }

  /* Moisture — 10 points. Wet formats support hydration and urinary health
     (learn-hydration.html). */
  if (product.format && product.format !== 'unknown') {
    possible += 10;
    const points = { wet: 10, 'semi-moist': 5, dry: 2, treat: 2 }[product.format] ?? 2;
    earned += points;
    if (product.format === 'wet') {
      reasons.push('A wet format contributes meaningfully to daily water intake.');
    } else if (product.format === 'dry') {
      reasons.push('A dry format leaves the cat to make up its water intake by drinking, which cats do incompletely.');
    }
  }

  /* Taurine — 10 points. Only a positive figure is informative; its absence
     from the database does not mean it is absent from the food. */
  if (n.taurinePresent === true) {
    possible += 10;
    earned += 10;
    reasons.push('Supplemental taurine is declared.');
  }

  if (possible === 0) return { available: false, analysisAvailable: false, reasons: [] };
  return {
    available: true,
    analysisAvailable: analysisPoints > 0,
    score: Math.round((earned / possible) * 100),
    reasons,
  };
}

/* ── Pillar B: additives and safety (35%) ── */

function scoreAdditives(product, kb) {
  const ingredients = product.ingredients || [];
  if (!ingredients.length) return { available: false, flagged: [], reasons: [] };

  const text = ingredients.join(' , ').toLowerCase();
  const flagged = [];

  for (const additive of kb.additives) {
    if (additive.tier === 0) continue;
    const alias = additive.aliases.find((a) => matchesTerm(text, a));
    if (alias) flagged.push({ ...additive, matchedOn: alias });
  }
  const beneficial = kb.additives.filter(
    (a) => a.tier === 0 && a.aliases.some((alias) => matchesTerm(text, alias)));

  /* Penalties are per occurrence, so three Tier 3 additives cost more than
     one. The floor is zero — the pillar cannot go negative and drag an
     otherwise decent product below what the other pillars justify. */
  const PENALTY = { 3: 30, 2: 10 };
  let score = 100;
  for (const f of flagged) score -= PENALTY[f.tier] || 0;

  /* Natural preservatives and declared taurine are a positive formulation
     signal (PRD §6.3), worth a little but never enough to offset a flag. */
  const bonus = Math.min(beneficial.length * 3, 9);
  score = Math.max(0, Math.min(100, score + bonus));

  const reasons = [];
  const tier3 = flagged.filter((f) => f.tier === 3);
  const tier2 = flagged.filter((f) => f.tier === 2);
  if (tier3.length) {
    reasons.push(`${tier3.length} high-risk (Tier 3) additive${tier3.length > 1 ? 's' : ''}: ${tier3.map((f) => f.name).join(', ')}.`);
  }
  if (tier2.length) {
    reasons.push(`${tier2.length} moderate-risk (Tier 2) additive${tier2.length > 1 ? 's' : ''}: ${tier2.map((f) => f.name).join(', ')}.`);
  }
  if (!flagged.length) reasons.push('No flagged additives found in the ingredient list.');
  if (beneficial.length) {
    reasons.push(`Includes ${beneficial.map((b) => b.name.toLowerCase()).join(', ')}.`);
  }

  return { available: true, score, flagged, beneficial, reasons };
}

/* ── Pillar C: ingredient quality and transparency (10%) ── */

function scoreTransparency(product, kb) {
  const ingredients = product.ingredients || [];
  if (!ingredients.length) return { available: false, reasons: [], vague: [] };

  const text = ingredients.join(' , ').toLowerCase();
  const vague = kb.vagueTerms
    .map((term) => {
      const alias = term.aliases.find((a) => matchesTerm(text, a));
      return alias ? { ...term, matchedOn: alias } : null;
    })
    .filter(Boolean);

  let score = 100;
  score -= vague.length * 22;

  // A very short list usually means the label was transcribed incompletely
  // rather than that the food has four ingredients.
  if (ingredients.length < 4) score -= 15;

  score = Math.max(0, Math.min(100, score));

  const reasons = [];
  if (vague.length) {
    reasons.push(`Unnamed or catch-all label terms: ${vague.map((v) => v.name.toLowerCase()).join(', ')}.`);
  } else {
    reasons.push('Ingredient sources are named rather than generic.');
  }
  if (ingredients.length < 4) {
    reasons.push('The ingredient list is unusually short, which often means the label was only partly recorded.');
  }
  return { available: true, score, vague, reasons };
}

/* ── Bands and gates ── */

export function bandFor(score) {
  return BANDS.find((b) => score >= b.min) || BANDS[BANDS.length - 1];
}

/* ── The engine ── */

/**
 * Score a normalised Product against the additive knowledge base.
 *
 * @param {object} product Product shape — see docs/TRD.md §4
 * @param {object} kb      Parsed assets/data/additives.json
 * @returns {object} ScoreResult
 */
export function scoreProduct(product, kb) {
  const nutrition = scoreNutrition(product);
  const additives = scoreAdditives(product, kb);
  const transparency = scoreTransparency(product, kb);

  const pillars = { nutrition, additives, transparency };
  const available = Object.entries(pillars).filter(([, p]) => p.available);
  const flagged = additives.flagged || [];
  const warnings = [];

  /* Refusing to score. The additives and transparency pillars both need an
     ingredient list, so without one only 55% of the model could ever run, and
     in practice usually none of it. A number here would be a guess wearing the
     costume of a measurement. */
  if (!additives.available) {
    return {
      scorable: false,
      reason: 'No ingredient list is on record for this product, so it cannot be scored.',
      pillars,
      flaggedAdditives: [],
      hardGates: [],
      warnings: ['Open Pet Food Facts has no ingredient list for this barcode. Anyone can add one.'],
      confidence: 'none',
    };
  }

  /* Renormalise across the pillars that could be computed. A product whose
     nutrition is unknown is scored on additives and transparency alone, and
     the result says so rather than implying the full model ran. */
  const totalWeight = available.reduce((sum, [key]) => sum + WEIGHTS[key], 0);
  let score = Math.round(
    available.reduce((sum, [key, p]) => sum + p.score * (WEIGHTS[key] / totalWeight), 0));

  /* Hard gates (PRD §6.5). Applied after the arithmetic, because their whole
     purpose is to override it. */
  const hardGates = [];
  const gateAdditive = flagged.find((f) => f.hardGate);
  if (gateAdditive) {
    score = Math.min(score, 24);
    hardGates.push(`${gateAdditive.name} is prohibited in cat food by the US FDA. The product is capped in the Bad band regardless of its nutrition.`);
  }
  if (flagged.some((f) => f.tier === 3)) {
    score = Math.min(score, 49);
    hardGates.push('A Tier 3 additive is present, so the score is capped at 49 (the Poor ceiling) regardless of nutrition.');
  }

  /* Confidence. A score built on a plausibility-gated fallback figure, or on
     half the model, is not the same claim as one built on a full label. */
  const nutritionConfidence = (product.nutrition || {}).confidence || 'none';
  const confidence =
    !nutrition.analysisAvailable ? 'low'
      : nutritionConfidence === 'high' && available.length === 3 ? 'high'
        : 'medium';

  if (!nutrition.analysisAvailable) {
    warnings.push('No usable nutritional analysis is on record. The nutrition pillar was assessed from the ingredient list alone, and this score reflects additives and label transparency more than nutrition.');
  } else if (nutritionConfidence === 'low') {
    warnings.push('Some nutrition figures come from fields intended for human food, which are frequently mis-entered. Treat them as indicative.');
  }
  if ((product.nutrition || {}).energyCorrected) {
    warnings.push('The published energy figure was implausible per 100 g and has been read as a per-kilogram value.');
  }
  if (product.aafcoComplete === undefined) {
    warnings.push('No AAFCO complete-and-balanced statement is on record. Check the packaging — this database does not capture it.');
  }
  if (product.format === 'treat') {
    warnings.push('This is a treat, not a complete diet. It is scored on the same scale, but should be under 10% of daily calories.');
  }

  const reasons = [
    ...(nutrition.reasons || []),
    ...(additives.reasons || []),
    ...(transparency.reasons || []),
  ];

  return {
    scorable: true,
    score,
    band: bandFor(score).band,
    bandLabel: bandFor(score).label,
    pillars,
    pillarsUsed: available.map(([key]) => key),
    flaggedAdditives: flagged,
    beneficialAdditives: additives.beneficial || [],
    vagueTerms: transparency.vague || [],
    hardGates,
    reasons,
    warnings,
    confidence,
  };
}

/* ── Knowledge base loading ── */

let kbPromise = null;

/** Fetch and cache the additive knowledge base. */
export function loadKnowledgeBase(url = './assets/data/additives.json') {
  if (!kbPromise) {
    kbPromise = fetch(url).then((r) => {
      if (!r.ok) throw new Error('Could not load the additive knowledge base.');
      return r.json();
    });
  }
  return kbPromise;
}

export const _internal = { scoreNutrition, scoreAdditives, scoreTransparency, ANIMAL_PROTEINS };
