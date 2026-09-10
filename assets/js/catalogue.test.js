/* Tests for the curated catalogue merge.
 *
 * The rules being tested are docs/PRD.md section 16.5a. The one that needed
 * tests most is the source ranking: a retailer listing fills gaps and a
 * manufacturer panel outranks the database. It is the rule most likely to be
 * "simplified" later by somebody who reads the code without the reason. */
import {
  mergeCurated, applyCurated, searchCatalogue, catalogueBrands, isProvisional, PROVISIONAL_KEY,
} from './catalogue.js';
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
  t.equal(merged.curated.only, true,
    'and the entry says there was no upstream record, because the disclosure on the '
    + 'product page otherwise credits the rest of the page to a record that does not exist');
});

suite('curated merge: an entry that fills gaps in a real record', (t) => {
  const merged = mergeCurated(API_PRODUCT, RETAILER);

  t.equal(merged.curated.only, false,
    'there was an upstream record, so the page may say the rest came from it');
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


/* ── Reaching a curated product (section 16.5b, M25) ──

   These three exist because the merge rules above were correct and consulted in
   one place. The bug they lock down is not a wrong number, it is the site
   disagreeing with itself: a search card reading "No ingredient list on record.
   Not scored" for a barcode whose own page scored it 49 off a transcribed
   panel. ── */

const CATALOGUE = {
  '4008429158100': RETAILER,
  '0017800150149': {
    barcode: '0017800150149',
    source: 'https://example.invalid/label-deck.pdf',
    sourceKind: 'manufacturer',
    checked: '2026-09-08',
    name: 'Cat Chow Complete',
    brand: 'Purina',
    quantity: '3.15lbs',
    ingredientsText: 'Poultry by-product meal, corn meal, soybean meal',
    ingredientsLang: 'en',
    crudeProteinPct: 32,
  },
  '9999999999999': {
    barcode: '9999999999999',
    source: 'https://example.invalid/gap',
    sourceKind: 'manufacturer',
    checked: '2026-09-08',
    crudeFatPct: 11,
  },
};

suite('applyCurated: a card and a page cannot disagree', (t) => {
  const bare = { ...API_PRODUCT, barcode: '0017800150149', ingredients: [], nutrition: {} };
  const [merged] = applyCurated([bare], CATALOGUE);

  t.equal(merged.ingredients.length, 3,
    'the list the product page already showed is now on the search result too');
  t.equal(merged.nutrition.crudeProteinPct, 32, 'and so is the panel figure');
  t.equal(merged.curated.sourceKind, 'manufacturer', 'with its provenance attached');

  const untouched = { ...API_PRODUCT, barcode: '1111111111111' };
  t.equal(applyCurated([untouched], CATALOGUE)[0], untouched,
    'a product the catalogue says nothing about is passed through unchanged');
  t.equal(applyCurated(null, CATALOGUE).length, 0, 'and no products is not an error');
});

suite('searchCatalogue: only named entries are findable', (t) => {
  const hits = searchCatalogue(CATALOGUE, { query: 'cat chow' });
  t.equal(hits.length, 1, 'a name match is found');
  t.equal(hits[0].barcode, '0017800150149', 'and it is the right product');

  t.equal(searchCatalogue(CATALOGUE, { query: 'poultry' }).length, 0,
    'the ingredient list is not searched: somebody searching chicken means the food');
  t.equal(searchCatalogue(CATALOGUE, { query: 'fat' }).length, 0,
    'an entry with no name of its own is a gap-filler, already findable through the API, '
    + 'and adding it here would put the same product on the page twice');
  t.equal(searchCatalogue(CATALOGUE, { query: '' }).length, 0,
    'an empty search is not a request for everything');
});

suite('searchCatalogue: brands, and not showing a product twice', (t) => {
  t.equal(searchCatalogue(CATALOGUE, { brandTags: 'Purina' }).length, 1, 'a brand browse matches');
  t.equal(searchCatalogue(CATALOGUE, { brandTags: 'purina|Purina' })[0].brand, 'Purina',
    'and the OR syntax the API filter uses is understood here too');
  t.equal(searchCatalogue(CATALOGUE, { brandTags: 'Whiskas' }).length, 0, 'a miss is a miss');

  const excluded = searchCatalogue(CATALOGUE, {
    query: 'cat chow', exclude: new Set(['0017800150149']),
  });
  t.equal(excluded.length, 0,
    'a product the API already returned is not added a second time');
});

suite('catalogueBrands: a brand entered by hand is not noise', (t) => {
  const brands = catalogueBrands(CATALOGUE);
  t.equal(brands.length, 1, 'only named entries carry a brand worth listing');
  t.equal(brands[0].name, 'Purina', 'the brand is the one on the entry');
  t.equal(brands[0].products, 1, 'counted');
  t.equal(brands[0].curated, true,
    'and flagged, so fetchBrands can exempt it from the minimum-product threshold '
    + 'that exists to hide the database long tail');
  t.equal(catalogueBrands(null).length, 0, 'no catalogue, no brands, no error');
});

suite('a provisional key is never something a scanner can produce', (t) => {
  t.equal(isProvisional('CFC-drelseys-pork-recipe-kibble'), true, 'the shape the tools write');
  t.equal(isProvisional('CFC-a-b'), true, 'two segments is enough');

  // The whole safety property. Every string of 6 to 14 digits belongs to some
  // real product, so a numeric placeholder could be scanned into by a visitor
  // holding an unrelated tin, who would be shown this product's panel and this
  // product's score with nothing anywhere saying otherwise. A scanner emits
  // digits and only digits.
  t.equal(isProvisional('000338026604'), false, 'a real barcode is not provisional');
  t.equal(isProvisional('0000000000'), false, 'and neither is a placeholder made of digits');
  t.equal(isProvisional('9999999999999'), false, 'however unlikely the digits look');
  t.equal(PROVISIONAL_KEY.test('CFC-'), false, 'a bare prefix names no product');
  t.equal(PROVISIONAL_KEY.test('CFC-Pork-Kibble'), false, 'capitals are refused, so one product has one key');
  t.equal(PROVISIONAL_KEY.test('cfc-pork-kibble'), false, 'and the prefix is not optional');
  t.equal(isProvisional(''), false, 'empty is not a key');
  t.equal(isProvisional(null), false, 'and neither is nothing at all');
});

suite('a provisional entry is searchable, and merges like any other', (t) => {
  const entry = {
    barcode: 'CFC-drelseys-pork-recipe-kibble',
    source: 'https://example.invalid/pork',
    sourceKind: 'manufacturer',
    checked: '2026-09-09',
    name: 'cleanprotein Pork Recipe Kibble',
    brand: "Dr. Elsey's",
    crudeProteinPct: 57,
    ingredientsText: 'Hydrolyzed Pork, Pork Plasma, Dried Chicken, Gelatin, Salt',
    ingredientsLang: 'en',
  };
  const catalogue = { 'CFC-drelseys-pork-recipe-kibble': entry };

  const found = searchCatalogue(catalogue, { query: 'pork' });
  t.equal(found.length, 1, 'a visitor searching by name finds it');
  t.equal(found[0].barcode, 'CFC-drelseys-pork-recipe-kibble', 'under its provisional key');

  const merged = mergeCurated(null, entry);
  t.equal(merged.curated.only, true,
    'and the page still says the whole record is ours, because it is');
  t.equal(merged.nutrition.crudeProteinPct, 57, 'the panel is merged as usual');
});
