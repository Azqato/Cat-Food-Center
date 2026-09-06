/* Tests for the CFC Score.
 *
 * The engine is pure, so these are golden-file tests: fixed input, fixed
 * expected output. They cover each band, both hard gates, the partial-data
 * paths that docs/PRD.md section 12 showed are the normal case, and the worked
 * example published in PRD.md §6.7. */
import {
  scoreProduct, toDryMatter, carbsByDifference, bandFor, matchesTerm, WEIGHTS,
} from './scoring.js';
import { suite } from './test-runner.js';

/* A trimmed knowledge base. Using a fixture rather than the real JSON keeps
   these tests from failing when an additive's wording is edited, while the
   ids, tiers and hardGate flags mirror assets/data/additives.json exactly. */
const KB = {
  additives: [
    { id: 'propylene-glycol', name: 'Propylene glycol', tier: 3, hardGate: true,
      aliases: ['propylene glycol'], sources: [] },
    { id: 'bha', name: 'BHA (butylated hydroxyanisole)', tier: 3, hardGate: false,
      aliases: ['butylated hydroxyanisole', 'bha'], sources: [] },
    { id: 'artificial-colours', name: 'Artificial colours', tier: 3, hardGate: false,
      aliases: ['red 40', 'color added'], sources: [] },
    { id: 'carrageenan', name: 'Carrageenan', tier: 2, hardGate: false,
      aliases: ['carrageenan'], sources: [] },
    { id: 'added-sugars', name: 'Added sugars and caramel colour', tier: 2, hardGate: false,
      aliases: ['corn syrup', 'caramel color'], sources: [] },
    { id: 'natural-preservatives', name: 'Mixed tocopherols', tier: 0, hardGate: false,
      aliases: ['mixed tocopherols', 'rosemary extract'], sources: [] },
    { id: 'supplemental-taurine', name: 'Supplemental taurine', tier: 0, hardGate: false,
      aliases: ['taurine'], sources: [] },
  ],
  vagueTerms: [
    { id: 'unnamed-meat', name: 'Unnamed protein source',
      aliases: ['meat by-product', 'meat and animal derivative', 'animal fat'], why: '' },
    { id: 'unnamed-flavour', name: 'Unspecified flavouring',
      aliases: ['natural flavor', 'artificial flavor'], why: '' },
  ],
};

/** A product with everything present, overridable per test. */
function product(overrides = {}) {
  return {
    barcode: '0000000000000',
    name: 'Test food',
    format: 'wet',
    lifeStage: 'adult',
    aafcoComplete: undefined,
    ingredients: ['Chicken', 'chicken broth', 'chicken liver', 'mixed tocopherols'],
    nutrition: {
      crudeProteinPct: 11, crudeFatPct: 5, crudeFibrePct: 0.5,
      ashPct: 2, moisturePct: 78, taurinePresent: true, confidence: 'high',
      energyCorrected: false,
    },
    dataCompleteness: 'full',
    ...overrides,
  };
}

suite('matchesTerm: word boundaries', (t) => {
  t.ok(matchesTerm('preserved with bha', 'bha'), 'matches BHA as its own word');
  t.ok(!matchesTerm('bhakti blend', 'bha'), 'does not match BHA inside another word');
  t.ok(!matchesTerm('sugar coating', 'oat'), 'does not match "oat" inside "coating"');
  t.ok(matchesTerm('rolled oat flour', 'oat'), 'matches "oat" as a word');
  t.ok(matchesTerm('Chicken, Corn Syrup, Salt', 'corn syrup'), 'matches a multi-word alias');
  t.ok(matchesTerm('colour: red 40', 'red 40'), 'matches an alias containing a digit');
});

suite('dry-matter conversion', (t) => {
  t.close(toDryMatter(11, 78), 50, 0.01, '11% protein at 78% moisture is 50% dry matter');
  t.close(toDryMatter(30, 10), 33.33, 0.01, '30% protein at 10% moisture is 33.3% dry matter');
  t.equal(toDryMatter(11, undefined), undefined, 'no moisture figure means no conversion');
  t.equal(toDryMatter(undefined, 78), undefined, 'no as-fed figure means no conversion');
  t.equal(toDryMatter(11, 100), undefined, '100% moisture would divide by zero');
});

suite('carbohydrate by difference', (t) => {
  t.close(carbsByDifference({ proteinDM: 50, fatDM: 22, fibreDM: 2, ashDM: 9 }), 17, 0.01,
    'the four fractions subtract from 100');
  t.equal(carbsByDifference({ proteinDM: 50, fatDM: 22, fibreDM: 2 }), undefined,
    'a missing fraction means no carbohydrate figure, not a guess');
  t.equal(carbsByDifference({ proteinDM: 70, fatDM: 30, fibreDM: 5, ashDM: 10 }), undefined,
    'fractions summing past 100 are a data error and yield nothing');
});

suite('bands', (t) => {
  t.equal(bandFor(100).band, 'excellent', '100 is Excellent');
  t.equal(bandFor(75).band, 'excellent', '75 is the bottom of Excellent');
  t.equal(bandFor(74).band, 'good', '74 is the top of Good');
  t.equal(bandFor(50).band, 'good', '50 is the bottom of Good');
  t.equal(bandFor(49).band, 'poor', '49 is the top of Poor');
  t.equal(bandFor(25).band, 'poor', '25 is the bottom of Poor');
  t.equal(bandFor(24).band, 'bad', '24 is the top of Bad');
  t.equal(bandFor(0).band, 'bad', '0 is Bad');
  t.equal(WEIGHTS.nutrition + WEIGHTS.additives + WEIGHTS.transparency, 1,
    'the three pillar weights sum to 1');
});

suite('a good product scores well', (t) => {
  const result = scoreProduct(product(), KB);
  t.ok(result.scorable, 'it is scorable');
  t.ok(result.score >= 75, `a named-meat-first wet food with no flags reaches Excellent (got ${result.score})`);
  t.equal(result.hardGates, [], 'no hard gates fire');
  t.equal(result.flaggedAdditives.length, 0, 'nothing is flagged');
  t.equal(result.confidence, 'high', 'full guaranteed-analysis data gives high confidence');
  t.equal(result.pillarsUsed, ['nutrition', 'additives', 'transparency'], 'all three pillars ran');
});

suite('hard gate: propylene glycol (PRD §6.5)', (t) => {
  const result = scoreProduct(product({
    ingredients: ['Chicken', 'chicken broth', 'propylene glycol', 'mixed tocopherols'],
  }), KB);
  t.ok(result.score <= 24, `capped into the Bad band (got ${result.score})`);
  t.equal(result.band, 'bad', 'the band is Bad');
  t.ok(result.hardGates.some((g) => /prohibited in cat food/.test(g)),
    'the gate explains that the FDA prohibits it');
  t.ok(result.flaggedAdditives.some((f) => f.id === 'propylene-glycol'), 'the additive is listed');
});

suite('hard gate: any Tier 3 caps at 49 (PRD §6.5)', (t) => {
  const result = scoreProduct(product({
    ingredients: ['Chicken', 'chicken liver', 'chicken fat preserved with BHA'],
  }), KB);
  t.ok(result.score <= 49, `capped at the Poor ceiling (got ${result.score})`);
  t.ok(result.band === 'poor' || result.band === 'bad', 'the band is Poor or below');
  t.ok(result.hardGates.some((g) => /capped at 49/.test(g)), 'the cap is explained');
  t.equal(result.hardGates.length, 1, 'only the Tier 3 cap fires, not the propylene glycol gate');
});

suite('the worked example from PRD §6.7', (t) => {
  // "A semi-moist food whose first ingredient is corn, with unnamed meat
  //  by-products, added caramel color, and propylene glycol."
  const result = scoreProduct(product({
    format: 'semi-moist',
    ingredients: ['Ground yellow corn', 'meat by-products', 'caramel color', 'propylene glycol'],
    nutrition: {
      crudeProteinPct: 26, crudeFatPct: 8, crudeFibrePct: 3, ashPct: 6,
      moisturePct: 25, confidence: 'high', energyCorrected: false,
    },
  }), KB);

  t.equal(result.band, 'bad', 'it lands in Bad, as the PRD says it must');
  t.ok(result.hardGates.length >= 1, 'the propylene glycol gate fires before nutrition matters');
  t.ok(result.flaggedAdditives.some((f) => f.id === 'propylene-glycol'), 'propylene glycol flagged');
  t.ok(result.flaggedAdditives.some((f) => f.id === 'added-sugars'), 'caramel colour flagged');
  t.ok(result.vagueTerms.some((v) => v.id === 'unnamed-meat'), 'meat by-products flagged as unnamed');
});

suite('partial data: the normal case', (t) => {
  const noNutrition = scoreProduct(product({
    nutrition: { confidence: 'none', energyCorrected: false },
    format: 'unknown',
  }), KB);
  t.ok(noNutrition.scorable, 'a product with ingredients but no analysis is still scorable');
  t.equal(noNutrition.pillars.nutrition.available, true,
    'the nutrition pillar still runs: animal-protein dominance comes from the ingredient list');
  t.equal(noNutrition.pillars.nutrition.analysisAvailable, false,
    'but it records that no published analysis contributed');
  t.equal(noNutrition.confidence, 'low',
    'confidence drops to low when the nutrition pillar rests on ingredient order alone');
  t.ok(noNutrition.warnings.some((w) => /ingredient list alone/.test(w)),
    'and the result says so rather than implying the full model ran');

  const noIngredients = scoreProduct(product({ ingredients: [] }), KB);
  t.equal(noIngredients.scorable, false,
    'with no ingredient list the engine refuses to score rather than guessing');
  t.ok(!('score' in noIngredients), 'and returns no number at all');
  t.ok(/cannot be scored/.test(noIngredients.reason), 'it explains why');

  const lowConfidence = scoreProduct(product({
    nutrition: { ...product().nutrition, confidence: 'low' },
  }), KB);
  t.equal(lowConfidence.confidence, 'medium',
    'human-schema figures cap confidence at medium even with all pillars present');
  t.ok(lowConfidence.warnings.some((w) => /intended for human food/.test(w)),
    'and the reason is surfaced');
});

suite('unavailable pillars are not scored as zero', (t) => {
  const withNutrition = scoreProduct(product(), KB);
  const withoutNutrition = scoreProduct(product({
    nutrition: { confidence: 'none', energyCorrected: false }, format: 'unknown',
  }), KB);
  t.ok(withoutNutrition.score > 50,
    `a clean-label product with no analysis still scores on its merits (got ${withoutNutrition.score})`);
  t.ok(withNutrition.pillars.nutrition.analysisAvailable,
    'the comparison case did have a published analysis');
  t.ok(!withoutNutrition.pillars.nutrition.analysisAvailable,
    'and the other did not');
});

suite('nutrition sub-factors', (t) => {
  const plantFirst = scoreProduct(product({
    ingredients: ['Pea protein', 'corn gluten meal', 'chicken fat'],
  }), KB);
  const meatFirst = scoreProduct(product(), KB);
  t.ok(plantFirst.pillars.nutrition.score < meatFirst.pillars.nutrition.score,
    'a plant protein leading the list scores below a named animal protein');
  t.ok(plantFirst.pillars.nutrition.reasons.some((r) => /biological value/.test(r)),
    'and the reason explains why');

  const dry = scoreProduct(product({ format: 'dry' }), KB);
  t.ok(dry.pillars.nutrition.score < meatFirst.pillars.nutrition.score,
    'a dry format scores below an otherwise identical wet one');

  const noTaurine = scoreProduct(product({
    nutrition: { ...product().nutrition, taurinePresent: undefined },
  }), KB);
  t.equal(noTaurine.pillars.nutrition.score, meatFirst.pillars.nutrition.score,
    'an undeclared taurine figure is neutral, not a penalty; absence of data is not absence of taurine');
});

suite('transparency pillar', (t) => {
  const vague = scoreProduct(product({
    ingredients: ['Meat and animal derivatives', 'cereals', 'natural flavor', 'minerals'],
  }), KB);
  const named = scoreProduct(product(), KB);
  t.ok(vague.pillars.transparency.score < named.pillars.transparency.score,
    'unnamed sources score below named ones');
  t.equal(vague.vagueTerms.length, 2, 'both catch-all terms are identified');

  const short = scoreProduct(product({ ingredients: ['Chicken', 'water'] }), KB);
  t.ok(short.pillars.transparency.reasons.some((r) => /unusually short/.test(r)),
    'a suspiciously short list is called out as likely incomplete');
});

suite('determinism', (t) => {
  const p = product();
  const a = scoreProduct(p, KB);
  const b = scoreProduct(p, KB);
  t.equal(a.score, b.score, 'the same input yields the same score');
  t.equal(a.reasons, b.reasons, 'and the same reasons, in the same order');
});

/* The bug this guards against was found by rendering a real product, not by a
   test: barcode 3596710487455 has a French label reading "Viandes et
   sous-produits animaux" and "sucres": unnamed meat by-products and added
   sugar: and the English-only matcher scored it 77/Excellent with a perfect
   transparency pillar and the reason "Ingredient sources are named rather than
   generic". Silence from a matcher that cannot read the label must never be
   reported as a clean result. */
suite('language guard', (t) => {
  const unreadable = product({
    ingredientsLang: 'pl',
    ingredients: ['Mieso i produkty pochodzenia zwierzecego', 'zboza', 'cukry'],
  });
  const english = product({
    ingredientsLang: 'en',
    ingredients: ['Meat and animal derivatives', 'cereals', 'sugars'],
  });

  const r = scoreProduct(unreadable, KB);
  t.ok(r.pillars.transparency.reasons.some((x) => /language this checker does not cover/.test(x)),
    'an unreadable label is stated as unchecked, not as clean');
  t.ok(!r.pillars.transparency.reasons.some((x) => /named rather than generic/.test(x)),
    'and is never told its sources are named');
  t.ok(!r.pillars.additives.reasons.some((x) => /^No flagged additives found/.test(x)),
    'nor that no flagged additives were found');
  t.equal(r.confidence, 'low', 'confidence is capped at low');
  t.ok(r.warnings.some((x) => /does not fully cover/.test(x)),
    'and a warning says so in plain words');

  t.ok(r.score < scoreProduct(product({ ingredientsLang: 'en' }), KB).score,
    'an unreadable clean-looking label scores below a readable clean one');

  const eng = scoreProduct(english, KB);
  t.ok(eng.pillars.transparency.reasons.some((x) => /Unnamed or catch-all/.test(x)),
    'the English equivalent has its catch-all term named outright');
  t.ok(eng.pillars.transparency.score < 100,
    'and is penalised on merit rather than for its language');

  const fr = scoreProduct(product({ ingredientsLang: 'fr' }), KB);
  t.ok(fr.confidence !== 'low', 'a language the aliases cover is not confidence-capped');
  t.equal(fr.score, scoreProduct(product({ ingredientsLang: 'en' }), KB).score,
    'French, which the aliases cover, scores identically to English');

  const missing = scoreProduct(product(), KB);
  t.equal(missing.score, scoreProduct(product({ ingredientsLang: 'en' }), KB).score,
    'an absent language field is treated as English rather than as unreadable');
});

suite('beneficial credit is not awarded to unnamed sources', (t) => {
  const KB2 = {
    ...KB,
    additives: [...KB.additives, {
      id: 'named-by-products', name: 'Named by-products and by-product meals',
      tier: 0, hardGate: false, aliases: ['by-product', 'sous-produits'], sources: [],
    }],
  };
  // Both lists carry carrageenan so the pillar sits below its ceiling, where a
  // difference in the beneficial bonus is actually visible.
  const unnamed = scoreProduct(product({
    ingredients: ['Meat by-products', 'cereals', 'carrageenan', 'minerals'],
  }), KB2);
  t.ok(!unnamed.pillars.additives.reasons.some((x) => /Named by-products/i.test(x)),
    'an unnamed by-product earns no credit for being a named one');
  t.ok(unnamed.pillars.transparency.reasons.some((x) => /Unnamed or catch-all/.test(x)),
    'and is still penalised as unnamed; a product cannot be both');

  const named = scoreProduct(product({
    ingredients: ['Chicken by-product meal', 'chicken broth', 'carrageenan', 'minerals'],
  }), KB2);
  t.ok(named.pillars.additives.reasons.some((x) => /named by-products/i.test(x)),
    'a named by-product still earns the credit it deserves');
  t.ok(named.pillars.additives.score > unnamed.pillars.additives.score,
    'so naming the species is worth more than not naming it');
});

suite('a parenthetical does not rename an unnamed source', (t) => {
  const annotated = scoreProduct(product({
    ingredients: [
      'Viandes et sous-produits animaux (dont boeuf 4% et foie 4%)',
      'cereales', 'substances minerales', 'sucres',
    ],
    ingredientsLang: 'fr',
  }), {
    ...KB,
    vagueTerms: [{ id: 'unnamed-meat', name: 'Unnamed protein source',
      aliases: ['sous-produits animaux', 'meat by-product'], why: '' }],
  });
  t.ok(!annotated.pillars.nutrition.reasons.some((x) => /named animal protein is the first/.test(x)),
    'a 4% beef parenthetical does not make unnamed meat a named first ingredient');
  t.ok(!annotated.pillars.nutrition.reasons.some((x) => /first three ingredients/.test(x)),
    'and does not score one branch lower as "appears in the first three" either');

  const genuine = scoreProduct(product({
    ingredients: ['Boeuf (65%)', 'bouillon', 'foie', 'substances minerales'],
    ingredientsLang: 'fr',
  }), KB);
  t.ok(genuine.pillars.nutrition.reasons.some((x) => /named animal protein is the first/.test(x)),
    'while a genuinely named French protein is recognised as one');
  t.ok(genuine.pillars.nutrition.score > annotated.pillars.nutrition.score,
    'so naming the species outscores hiding it behind a percentage');
});

suite('an unnamed leading protein is reported as such', (t) => {
  const r = scoreProduct(product({
    ingredients: ['Meat and animal derivatives (including beef 4%)', 'cereals', 'minerals'],
  }), KB);
  t.ok(r.pillars.nutrition.reasons.some((x) => /species is not stated/.test(x)),
    'the nutrition pillar names the actual problem with the first ingredient');
  t.ok(!r.pillars.nutrition.reasons.some((x) => /starch source/.test(x)),
    'rather than reporting whatever happened to appear second');
});
