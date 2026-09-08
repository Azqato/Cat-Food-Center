/* Tests for the curated catalogue merge.
 *
 * The rules being tested are docs/PRD.md section 16.5a. The one that needed
 * tests most is the source ranking: a retailer listing fills gaps and a
 * manufacturer panel outranks the database. It is the rule most likely to be
 * "simplified" later by somebody who reads the code without the reason. */
import { mergeCurated } from './catalogue.js';
import { suite } from './test-runner.js';

const API_PRODUCT = {
  barcode: '4008429158100',
  name: 'Dreamies Mega Tub',
  ingredients: [],
  ingredientsText: '',
  nutrition: {
    crudeProteinPct: 22,
    crudeFatPct: 22,
    kcalPer100g: 416,
    confidence: 'high',
  },
  dataCompleteness: 'partial',
};

const RETAILER = {
  barcode: '4008429158100',
  source: 'https://example.invalid/listing',
  sourceKind: 'retailer-listing',
  checked: '2026-09-07',
  ingredientsText: 'Meat and animal derivatives (including 4% chicken), cereals, minerals',
  ingredientsLang: 'en',
};

suite('curated merge: filling a gap', (t) => {
  const merged = mergeCurated(API_PRODUCT, RETAILER);

  t.equal(merged.ingredients.length, 3, 'the curated list is split like an upstream one');
  t.equal(merged.curated.fields, ['ingredientsText'],
    'only the field that actually changed is named');
  t.equal(merged.curated.sourceKind, 'retailer-listing', 'the source kind travels with it');
  t.equal(merged.curated.source, 'https://example.invalid/listing', 'so does the source');
  t.equal(merged.nutrition.crudeProteinPct, 22, 'an upstream figure is left alone');
  t.equal(API_PRODUCT.ingredients.length, 0, 'the input product is not mutated');
  t.equal(merged.dataCompleteness, 'full',
    'a list plus three figures is a complete record, however the list arrived');
});

suite('curated merge: a retailer listing never overwrites', (t) => {
  const contradicting = { ...RETAILER, crudeProteinPct: 31 };
  const merged = mergeCurated(API_PRODUCT, contradicting);

  t.equal(merged.nutrition.crudeProteinPct, 22,
    'the database figure stands: two sources disagree and the weaker one must not win quietly');
  t.equal(merged.curated.fields.includes('crudeProteinPct'), false,
    'and the page is not told a figure changed when it did not');
});

suite('curated merge: a manufacturer panel outranks the database', (t) => {
  const panel = {
    ...RETAILER, sourceKind: 'manufacturer', crudeProteinPct: 31,
  };
  const merged = mergeCurated(API_PRODUCT, panel);

  t.equal(merged.nutrition.crudeProteinPct, 31, 'the transcribed panel figure wins');
  t.equal(merged.curated.fields.includes('crudeProteinPct'), true, 'and is declared as curated');
});

suite('curated merge: a product the database does not have', (t) => {
  const merged = mergeCurated(null, {
    ...RETAILER, name: 'Something the API never heard of',
  });

  t.equal(merged.barcode, '4008429158100', 'the barcode comes from the entry');
  t.equal(merged.name, 'Something the API never heard of', 'so does everything else');
  t.equal(merged.curated.fields.includes('name'), true,
    'and every field is declared, because every field is curated');
  t.equal(merged.dataCompleteness, 'partial', 'completeness is recomputed, not inherited');
});

suite('curated merge: nothing to say', (t) => {
  const sameAsApi = {
    ...RETAILER, ingredientsText: undefined, name: 'Dreamies Mega Tub',
  };
  const merged = mergeCurated(API_PRODUCT, sameAsApi);

  t.equal(merged.curated, undefined,
    'a merge that changes nothing claims no provenance, or the page would announce '
    + 'a curated origin for data that is entirely upstream');
  t.equal(mergeCurated(API_PRODUCT, null), API_PRODUCT, 'no entry, no change');
});

suite('curated merge: an unnamed language is not English', (t) => {
  const noLang = { ...RETAILER, ingredientsLang: undefined };
  const merged = mergeCurated(API_PRODUCT, noLang);

  t.equal(merged.ingredientsLang, 'unknown',
    'assuming English is exactly how section 12.4 happened');
});

suite('curated merge: confidence', (t) => {
  const bare = { ...API_PRODUCT, nutrition: {} };
  const listing = mergeCurated(bare, { ...RETAILER, crudeProteinPct: 31 });
  t.equal(listing.nutrition.confidence, 'low',
    'a figure off a shop listing is not a guaranteed analysis');

  const panel = mergeCurated(bare, {
    ...RETAILER, sourceKind: 'manufacturer', crudeProteinPct: 31,
  });
  t.equal(panel.nutrition.confidence, 'high',
    'a figure read off the manufacturer panel is, which is the point of transcribing it');
});
