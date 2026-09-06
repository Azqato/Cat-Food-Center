/* ==========================================================================
   The CFC Score.

   A pure, deterministic module: the same product always yields the same
   result, and nothing here touches the network or the DOM. It runs in the
   visitor's browser, which is deliberate; a sceptical reader can open
   devtools and watch a score being derived. See docs/PRD.md section 16.2.

   The methodology is published in PRD.md §6 and on methodology.html. This file
   is the implementation of that document; if the two disagree, the document is
   wrong until fixed, because it is what we tell people we do.

   ── The thing that shapes this file most ──

   docs/PRD.md section 12 measured the real database: about a fifth of products
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

/* Named animal proteins. A named source is the signal, "chicken" scores,
   "meat" does not, which is Pillar C's whole point. */
const ANIMAL_PROTEINS = [
  'chicken', 'turkey', 'duck', 'goose', 'quail', 'salmon', 'tuna', 'trout',
  'whitefish', 'herring', 'mackerel', 'sardine', 'anchovy', 'cod', 'beef',
  'lamb', 'pork', 'rabbit', 'venison', 'bison', 'liver', 'heart', 'kidney',
  'gizzard', 'egg', 'chicken meal', 'turkey meal', 'salmon meal', 'lamb meal',
  /* The same species in the other languages the database carries. A named
     species is the signal, and the signal does not stop at the Channel: an
     English-only list reported a French beef pate as having no identifiable
     protein source at all. Generic words for meat (viande, Fleisch, carne)
     are deliberately absent, because "meat" unnamed is exactly what this
     check is meant not to reward. */
  'poulet', 'dinde', 'canard', 'saumon', 'thon', 'boeuf', 'bœuf', 'agneau',
  'porc', 'lapin', 'foie', 'coeur', 'cœur', 'oeuf', 'œuf', 'poisson',
  'huhn', 'hahnchen', 'hähnchen', 'pute', 'truthahn', 'ente', 'lachs',
  'thunfisch', 'rind', 'rindfleisch', 'lamm', 'schwein', 'kaninchen', 'leber',
  'herz', 'ei',
  'pollo', 'pavo', 'pato', 'salmon', 'salmón', 'atun', 'atún', 'vacuno',
  'cordero', 'cerdo', 'conejo', 'higado', 'hígado', 'huevo',
  'tacchino', 'anatra', 'salmone', 'tonno', 'manzo', 'agnello', 'maiale',
  'coniglio', 'fegato', 'uovo',
  'kip', 'kalkoen', 'eend', 'zalm', 'tonijn', 'rundvlees', 'lam', 'varken',
  'konijn', 'lever',
];

/* Plant proteins inflate the crude-protein figure without supplying taurine or
   arginine at feline biological value (PRD §6.2). */
const PLANT_PROTEINS = [
  'pea protein', 'corn gluten', 'wheat gluten', 'soy protein', 'soybean meal',
  'potato protein', 'rice protein', 'pea flour', 'lentil', 'chickpea',
  'proteine de pois', 'protéine de pois', 'gluten de mais', 'gluten de maïs',
  'gluten de ble', 'gluten de blé', 'proteine de soja', 'protéine de soja',
  'erbsenprotein', 'maiskleber', 'weizengluten', 'sojaprotein',
  'proteina de guisante', 'proteína de guisante', 'gluten de trigo',
  'proteine di pisello', 'glutine di mais', 'erwteneiwit',
];

/* High-glycaemic starch sources. */
const STARCH_FILLERS = [
  'corn', 'maize', 'wheat', 'rice', 'potato', 'tapioca', 'sorghum', 'barley',
  'oat', 'soybean', 'cereal',
  'cereale', 'céréale', 'cereales', 'céréales', 'mais', 'maïs', 'ble', 'blé',
  'riz', 'pomme de terre', 'orge', 'avoine', 'soja',
  'getreide', 'weizen', 'reis', 'kartoffel', 'gerste', 'hafer',
  'trigo', 'arroz', 'patata', 'cebada', 'avena',
  'cereali', 'grano', 'riso', 'patate', 'orzo',
  'granen', 'tarwe', 'rijst', 'aardappel', 'gerst', 'haver',
];

/* Languages the additive aliases cover. Only about a tenth of records carry
   English ingredients (docs/PRD.md section 12), and the database is
   Europe-weighted, so an English-only matcher would silently report the other
   nine tenths as free of flagged additives: a false clean bill of health, and
   the worst direction for a trust product to be wrong in. */
export const MATCHED_LANGUAGES = ['en', 'fr', 'de', 'es', 'it', 'nl'];

/* ── Text matching ── */

/**
 * Whether `needle` appears in `haystack` as a whole word or phrase.
 *
 * Substring matching is not safe here: the alias "bha" would fire on
 * "bhakti", and "oat" on "coating". Both are real ingredient-label words.
 *
 * A trailing "s" is allowed, because aliases are written in the singular but
 * labels are usually plural, "meat by-products", "mixed tocopherols",
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
 * Carbohydrate by difference: nitrogen-free extract (learn-labels.html §5).
 * Needs all four other fractions, so it is often unavailable.
 */
export function carbsByDifference({ proteinDM, fatDM, fibreDM, ashDM }) {
  const parts = [proteinDM, fatDM, fibreDM, ashDM];
  if (parts.some((v) => typeof v !== 'number')) return undefined;
  const carbs = 100 - parts.reduce((a, b) => a + b, 0);
  // A negative result means the analysis does not add up, a data error, not a
  // food with negative carbohydrate.
  return carbs >= 0 && carbs <= 100 ? carbs : undefined;
}

/* ── Pillar A: nutritional quality (55%) ── */

/**
 * Each sub-factor contributes only if its data exists. The pillar score is the
 * points earned as a fraction of the points that were actually assessable, so
 * a product is never penalised for a figure nobody entered.
 */
function scoreNutrition(product, kb) {
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
  /* An unnamed source stays unnamed however it is annotated. "Viandes et
     sous-produits animaux (dont boeuf 4% et foie 4%)" names beef in a
     parenthetical, but the entry is still overwhelmingly unspecified meat, and
     reading that 4% as a named animal protein would award marks for the
     opposite of what the label shows. So any entry matching an unnamed-source
     term is judged on the part before its parenthesis, and this must apply to
     the whole leading window, not just the first entry: masking only the first
     one simply moved the same 4% down to the "appears in the first three"
     branch and scored it there instead. */
  const vagueAliases = (kb.vagueTerms || []).flatMap((v) => v.aliases);
  const named = ingredients.map((entry) => {
    const lower = entry.toLowerCase();
    return anyMatch(lower, vagueAliases) ? lower.replace(/[([].*/, '').trim() : lower;
  });
  const firstThree = named.slice(0, 3).join(' ');
  const first = named[0] || '';
  const firstIsUnnamed = anyMatch((ingredients[0] || '').toLowerCase(), vagueAliases);

  /* Animal-protein dominance: 35 points. */
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
    } else if (firstIsUnnamed) {
      /* Stated before the first-three branches, because "the main ingredient
         is meat of an unstated species" is the most important thing the list
         says, and it would otherwise be reported as whatever happened to
         appear second. It scores like a starch: the protein may well be fine,
         but nothing on the label lets anyone check. */
      earned += 6;
      reasons.push('The first ingredient is an animal protein whose species is not stated, so its quality cannot be assessed from the label.');
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

  /* Protein level on a dry-matter basis: 25 points, against the AAFCO adult
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

  /* Carbohydrate load: 20 points. Lower is better for an obligate carnivore. */
  if (typeof carbsDM === 'number') {
    possible += 20;
    const bands = [[10, 20], [20, 16], [30, 11], [40, 5]];
    const hit = bands.find(([ceiling]) => carbsDM < ceiling);
    earned += hit ? hit[1] : 0;
    analysisPoints += 20;
    reasons.push(`Carbohydrate by difference is about ${carbsDM.toFixed(0)}% of dry matter.`);
  }

  /* Moisture: 10 points. Wet formats support hydration and urinary health
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

  /* Taurine: 10 points. Only a positive figure is informative; its absence
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
  const readable = MATCHED_LANGUAGES.includes(product.ingredientsLang || 'en');

  const text = ingredients.join(' , ').toLowerCase();
  const flagged = [];

  for (const additive of kb.additives) {
    if (additive.tier === 0) continue;
    const alias = additive.aliases.find((a) => matchesTerm(text, a));
    if (alias) flagged.push({ ...additive, matchedOn: alias });
  }
  /* Beneficial (Tier 0) credit is awarded per ingredient entry, not against the
     whole list, and is withheld when that same entry is itself an unnamed
     source. "Named by-products" is the case that forced this: its aliases are
     bare stems ("by-product", "sous-produits") so "meat by-products" matched
     it and earned a bonus for being a named source while the transparency
     pillar was penalising the very same words for being unnamed. One product
     cannot be both. The knowledge base entry says as much itself: only named
     by-products are the nutrient-dense organ meats it describes. */
  const vagueAliases = (kb.vagueTerms || []).flatMap((v) => v.aliases);
  const isUnnamed = (entry) => anyMatch(entry, vagueAliases);
  const beneficial = kb.additives.filter((a) => a.tier === 0 && ingredients.some(
    (entry) => {
      const lower = entry.toLowerCase();
      return a.aliases.some((alias) => matchesTerm(lower, alias)) && !isUnnamed(lower);
    }));

  /* Penalties are per occurrence, so three Tier 3 additives cost more than
     one. The floor is zero; the pillar cannot go negative and drag an
     otherwise decent product below what the other pillars justify. */
  const PENALTY = { 3: 30, 2: 10 };
  let score = 100;
  for (const f of flagged) score -= PENALTY[f.tier] || 0;

  /* Natural preservatives and declared taurine are a positive formulation
     signal (PRD §6.3), worth a little but never enough to offset a flag. */
  const bonus = readable ? Math.min(beneficial.length * 3, 9) : 0;
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
  if (!flagged.length) {
    reasons.push(readable
      ? 'No flagged additives found in the ingredient list.'
      : 'No flagged additives were matched, but the ingredient list is in a language this checker does not cover, so nothing can be concluded from that.');
  }
  if (beneficial.length) {
    reasons.push(`Includes ${beneficial.map((b) => b.name.toLowerCase()).join(', ')}.`);
  }

  return { available: true, score, flagged, beneficial, reasons, readable };
}

/* ── Pillar C: ingredient quality and transparency (10%) ── */

function scoreTransparency(product, kb) {
  const ingredients = product.ingredients || [];
  if (!ingredients.length) return { available: false, reasons: [], vague: [] };
  const readable = MATCHED_LANGUAGES.includes(product.ingredientsLang || 'en');

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

  // A label we cannot read cannot earn full marks for naming its sources.
  if (!readable && !vague.length) score -= 25;
  score = Math.max(0, Math.min(100, score));

  const reasons = [];
  if (vague.length) {
    reasons.push(`Unnamed or catch-all label terms: ${vague.map((v) => v.name.toLowerCase()).join(', ')}.`);
  } else if (readable) {
    reasons.push('Ingredient sources are named rather than generic.');
  } else {
    reasons.push('Whether the ingredient sources are named could not be checked: the label is in a language this checker does not cover.');
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
 * @param {object} product Product shape (see docs/PRD.md section 16.5)
 * @param {object} kb      Parsed assets/data/additives.json
 * @returns {object} ScoreResult
 */
export function scoreProduct(product, kb) {
  const nutrition = scoreNutrition(product, kb);
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
    additives.readable === false ? 'low'
      : !nutrition.analysisAvailable ? 'low'
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
  if (additives.readable === false) {
    warnings.push(`The ingredient list is in ${product.ingredientsLang === 'unknown' ? 'an unrecognised language' : `'${product.ingredientsLang}'`}, which this additive checker does not fully cover. Flagged additives may have been missed, so treat the additive and transparency pillars as incomplete rather than clean.`);
  }
  if (product.aafcoComplete === undefined) {
    warnings.push('No AAFCO complete-and-balanced statement is on record. Check the packaging; this database does not capture it.');
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

/* ── Per-ingredient explanation ── */

/**
 * What the knowledge base has to say about one ingredient entry, or null.
 *
 * This is deliberately not a general ingredient dictionary. There is nothing
 * true this project can say about "chicken" that the word does not already
 * say, and a panel that padded every row with filler would make the rows that
 * matter harder to find rather than easier. It answers for exactly the entries
 * the scoring engine already reasons about: the 20 additives in
 * `additives.json` and the vague-term groups. Everything else returns null and
 * stays plain text.
 *
 * The same `matchesTerm` the engine uses, so an ingredient that the additive
 * pillar penalised cannot fail to explain itself, and one it ignored cannot
 * claim to have been counted.
 *
 * @param {string} entry  One ingredient, as printed on the label.
 * @param {object} kb     The additive knowledge base.
 * @returns {{kind: 'additive'|'vague', id: string, name: string, tier?: number,
 *            function?: string, healthImpact?: string, regulatory?: string,
 *            sources?: Array<{label: string, url: string}>,
 *            matchedOn: string} | null}
 */
export function explainIngredient(entry, kb) {
  if (!entry || !kb) return null;
  const text = String(entry).toLowerCase();

  /* Additives first, and the highest tier first within that. One entry can
     match more than one alias, and where it does the visitor should be shown
     the more serious of the two: "propylene glycol" appearing inside a longer
     phrase matters more than a humectant note. */
  const additives = (kb.additives || [])
    .map((a) => {
      const matchedOn = (a.aliases || []).find((alias) => matchesTerm(text, alias));
      return matchedOn ? { ...a, matchedOn } : null;
    })
    .filter(Boolean)
    .sort((a, b) => (b.tier || 0) - (a.tier || 0));

  const vague = (kb.vagueTerms || [])
    .map((term) => {
      const matchedOn = (term.aliases || []).find((alias) => matchesTerm(text, alias));
      return matchedOn ? { term, matchedOn } : null;
    })
    .find(Boolean);

  /* The engine withholds Tier 0 credit from an entry that is itself an
     unnamed source, because one ingredient cannot be both a named organ
     meat and an unnamed one. Viandes et sous-produits animaux is the case
     that forced it: the bare stem sous-produits matches the beneficial
     entry while the transparency pillar penalises the same words. The
     explanation has to make the same call, or the page would label a row
     Beneficial that the score treated as a transparency problem. A real
     additive still wins: being inside a vague entry does not make BHA less
     of an additive. */
  const best = additives[0];
  if (best && !(best.tier === 0 && vague)) {
    const a = best;
    return {
      kind: 'additive',
      id: a.id,
      name: a.name,
      tier: a.tier,
      function: a.function,
      healthImpact: a.healthImpact,
      regulatory: a.regulatory,
      sources: a.sources || [],
      matchedOn: a.matchedOn,
    };
  }

  if (vague) {
    return {
      kind: 'vague',
      id: vague.term.id,
      name: vague.term.name,
      healthImpact: vague.term.healthImpact || vague.term.why,
      sources: vague.term.sources || [],
      matchedOn: vague.matchedOn,
    };
  }

  return null;
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
