/* Tests for the Open Pet Food Facts normaliser.
 *
 * Every fixture below is a real record shape observed while sampling the live
 * database (docs/DATA-COVERAGE.md). The implausible ones are real too — they
 * are the reason the plausibility gate exists. */
import { normalize, _internal as internal } from './opff.js';
import { suite } from './test-runner.js';

suite('splitIngredients', (t) => {
  t.equal(
    internal.splitIngredients(
      'Meat and animal derivatives (including chicken, 4%), cereals, minerals; oils and fats.'),
    ['Meat and animal derivatives (including chicken, 4%)', 'cereals', 'minerals', 'oils and fats'],
    'a comma inside parentheses does not split the ingredient');

  t.equal(internal.splitIngredients(''), [], 'empty text gives an empty list');
  t.equal(internal.splitIngredients(null), [], 'null text gives an empty list');
  t.equal(internal.splitIngredients('Chicken,,  ,Rice'), ['Chicken', 'Rice'],
    'empty fragments are dropped');
  t.equal(internal.splitIngredients('  Chicken  broth ,  Liver .'), ['Chicken broth', 'Liver'],
    'whitespace collapsed and trailing punctuation trimmed');
  t.equal(internal.splitIngredients('Fish [tuna, salmon], water'), ['Fish [tuna, salmon]', 'water'],
    'square brackets nest like parentheses');
});

suite('energy unit inference', (t) => {
  t.equal(internal.readEnergy({ 'energy-kcal_100g': 416 }), { value: 416, corrected: false },
    'a plausible dry-food figure is kept as-is');
  t.equal(internal.readEnergy({ 'energy-kcal_100g': 1774 }), { value: 177.4, corrected: true },
    "Hill's 1774 is per kilogram and is corrected to 177.4, flagged as corrected");
  t.equal(internal.readEnergy({ 'energy-kcal_100g': 8 }), null,
    'Sheba reporting 8 kcal/100g is discarded, not scored on');
  t.equal(internal.readEnergy({}), null, 'absent energy gives null');
  t.equal(internal.readEnergy({ 'energy-kcal_100g': 'not a number' }), null,
    'unparseable energy gives null');
});

suite('nutriment schema preference', (t) => {
  const both = { 'crude-protein_100g': 22, proteins_100g: 1.2 };
  t.equal(internal.readAnalysis(both, ['crude-protein'], ['proteins'], 'protein'),
    { value: 22, source: 'guaranteed-analysis' },
    'the guaranteed analysis wins when both schemas are present');

  t.equal(internal.readAnalysis({ proteins_100g: 1.2 }, ['crude-protein'], ['proteins'], 'protein'),
    null,
    'an implausible human-schema value is rejected rather than used as a fallback');

  t.equal(internal.readAnalysis({ proteins_100g: 28.7 }, ['crude-protein'], ['proteins'], 'protein'),
    { value: 28.7, source: 'human-schema' },
    'a plausible human-schema value is used, and says so');

  t.equal(internal.readAnalysis({ 'crude-protein_100g': 90 }, ['crude-protein'], ['proteins'], 'protein'),
    null,
    'even the guaranteed analysis is gated — 90% protein is not a cat food');

  t.equal(internal.readAnalysis({ fibre_100g: 2 }, ['crude-fibre'], ['fiber', 'fibre'], 'fibre'),
    { value: 2, source: 'human-schema' },
    'both spellings of fibre are read');
});

suite('format inference', (t) => {
  t.equal(internal.readFormat(['en:wet-cat-food'], undefined), 'wet', 'category tag wins');
  t.equal(internal.readFormat(['en:cat-treats'], undefined), 'treat', 'treats are identified');
  t.equal(internal.readFormat([], 84.5), 'wet', 'moisture infers wet when no tag exists');
  t.equal(internal.readFormat([], 8), 'dry', 'moisture infers dry when no tag exists');
  t.equal(internal.readFormat([], 35), 'semi-moist', 'mid-range moisture is semi-moist');
  t.equal(internal.readFormat([], undefined), 'unknown',
    'no tag and no moisture stays unknown rather than guessing');
});

suite('life stage inference', (t) => {
  t.equal(internal.readLifeStage([], [], 'Kitten Chicken Formula'), 'growth', 'kitten means growth');
  t.equal(internal.readLifeStage([], [], 'Senior 7+ Salmon'), 'adult', 'senior is an adult stage');
  t.equal(internal.readLifeStage([], [], 'All Life Stages Turkey'), 'all', 'all life stages');
  t.equal(internal.readLifeStage([], [], 'Ocean Whitefish'), 'unknown', 'nothing stated stays unknown');
});

suite('normalize — a well-populated wet food', (t) => {
  const product = normalize({
    code: '3065890154995',
    product_name: 'Whiskas Chicken in Jelly',
    brands: 'Mars, Waltham, Whiskas',
    quantity: '100 g',
    ingredients_text: 'Meat and animal derivatives (including chicken 4%), cereals, minerals.',
    nutriments: {
      'crude-protein_100g': 8.7, 'crude-fat_100g': 4, 'crude-fibre_100g': 0.25,
      'crude-ash_100g': 1.6, moisture_100g: 84.5,
    },
    categories_tags: ['en:cat-food'],
    last_modified_t: 1788447101,
  });

  t.equal(product.format, 'wet', 'format inferred from 84.5% moisture');
  t.equal(product.brand, 'Mars', 'only the first brand is kept');
  t.equal(product.nutrition.confidence, 'high', 'all-guaranteed-analysis data is high confidence');
  t.equal(product.dataCompleteness, 'full', 'ingredients plus five figures is full');
  t.equal(product.ingredients.length, 3, 'three ingredients parsed');
  t.equal(product.aafcoComplete, undefined,
    'AAFCO adequacy is unknown, never false — the API does not record it');
  t.equal(product.lastModified, '2026-09-03', 'last modified converted to an ISO date');
  t.ok(product.sourceUrl.includes('3065890154995'), 'source URL points back at the record');
});

suite('normalize — degraded and hostile input', (t) => {
  const bare = normalize({ code: '123456' });
  t.equal(bare.dataCompleteness, 'minimal', 'a record with only a barcode does not throw');
  t.equal(bare.nutrition.confidence, 'none', 'no figures means no confidence');
  t.equal(bare.name, 'Unnamed product', 'a missing name gets a placeholder, not undefined');
  t.equal(bare.ingredients, [], 'no ingredients gives an empty list');

  const mixed = normalize({ code: '1', nutriments: { 'crude-protein_100g': 30, fat_100g: 12 } });
  t.equal(mixed.nutrition.confidence, 'low',
    'one human-schema value drops the whole record to low confidence');

  const junk = normalize({
    code: '2',
    product_name: 'Gourmet Gold',
    nutriments: { proteins_100g: 1.2, fat_100g: 0.3, 'energy-kcal_100g': 2 },
  });
  t.equal(junk.nutrition.crudeProteinPct, undefined,
    'the real Gourmet record, whose figures are per-gram, yields no protein value');
  t.equal(junk.nutrition.kcalPer100g, undefined, 'and no energy value');
  t.equal(junk.nutrition.confidence, 'none', 'so it carries no confidence at all');
  t.equal(junk.dataCompleteness, 'minimal', 'and is not presented as having data');

  const taurineAbsent = normalize({ code: '3', nutriments: {} });
  t.equal(taurineAbsent.nutrition.taurinePresent, undefined,
    'no taurine figure means unknown, not absent — the distinction matters');
  const taurinePresent = normalize({ code: '4', nutriments: { taurine_100g: 0.15 } });
  t.equal(taurinePresent.nutrition.taurinePresent, true, 'a positive taurine figure is informative');
});
