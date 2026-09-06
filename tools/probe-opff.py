# -*- coding: utf-8 -*-
"""Measure what Open Pet Food Facts actually contains for cat food.

Regenerates the numbers in docs/DATA-COVERAGE.md:

    python tools/probe-opff.py [pages]

Hits the public API (no key needed) and prints field coverage, the split
between the two competing nutriment schemas, and how many figures are
implausible. Re-run before relying on any coverage claim — the database is
crowd-sourced and moves.
"""
import collections
import json
import sys
import urllib.request

BASE = 'https://world.openpetfoodfacts.org/api/v2/search'
UA = 'CatFoodCenter/0.8 (https://azqato.github.io/Cat-Food-Center/)'
FIELDS = ('code,product_name,brands,quantity,ingredients_text,ingredients_text_en,'
          'nutriments,categories_tags,labels_tags,countries_tags,lang,image_front_url')

# A cat food as fed. Anything outside these ranges is a data-entry error, not an
# unusual product. See docs/DATA-COVERAGE.md.
PLAUSIBLE = {'protein': (3, 50), 'fat': (0.5, 40), 'moisture': (0, 90), 'kcal': (15, 600)}


def fetch(page):
    url = '%s?categories_tags_en=cat-food&page_size=100&page=%d&fields=%s' % (BASE, page, FIELDS)
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read().decode('utf-8'))


def value(nutriments, *keys):
    """First present value among keys, preferring the _100g variant."""
    for k in keys:
        v = nutriments.get(k + '_100g', nutriments.get(k))
        if v is not None:
            try:
                return float(v), k
            except (TypeError, ValueError):
                pass
    return None, None


def main(pages=6):
    products = {}
    for page in range(1, pages + 1):
        for p in fetch(page).get('products', []):
            products[p.get('code')] = p

    ps = list(products.values())
    n = len(ps)
    if not n:
        print('No products returned.')
        return 1

    have = collections.Counter()
    schema = collections.Counter()
    plausible = implausible = 0

    for p in ps:
        nm = p.get('nutriments') or {}
        ing = (p.get('ingredients_text_en') or p.get('ingredients_text') or '').strip()

        if (p.get('product_name') or '').strip():
            have['product_name'] += 1
        if (p.get('brands') or '').strip():
            have['brands'] += 1
        if p.get('image_front_url'):
            have['image'] += 1
        if len(ing) > 60:
            have['ingredients (>60ch)'] += 1
        if (p.get('ingredients_text_en') or '').strip():
            have['ingredients in English'] += 1
        if any(t in (p.get('categories_tags') or []) for t in ('en:wet-cat-food', 'en:dry-cat-food')):
            have['wet/dry known'] += 1
        for label, keys in (('moisture', ('moisture',)), ('fibre', ('crude-fibre', 'fiber')),
                            ('ash', ('crude-ash',)), ('taurine', ('taurine',))):
            if value(nm, *keys)[0] is not None:
                have[label] += 1

        crude = nm.get('crude-protein_100g') is not None
        human = nm.get('proteins_100g') is not None
        schema['both' if (crude and human) else 'crude only' if crude
               else 'human only' if human else 'neither'] += 1

        protein, _ = value(nm, 'crude-protein', 'proteins')
        if protein is None:
            continue
        have['any protein'] += 1
        fat, _ = value(nm, 'crude-fat', 'fat')
        kcal, _ = value(nm, 'energy-kcal')

        def ok(v, band):
            return v is None or PLAUSIBLE[band][0] <= v <= PLAUSIBLE[band][1]

        if ok(protein, 'protein') and ok(fat, 'fat') and ok(kcal, 'kcal'):
            plausible += 1
            have['plausible protein'] += 1
        else:
            implausible += 1
        if len(ing) > 60 and protein is not None and fat is not None:
            have['ingredients AND protein AND fat'] += 1

    print('Sampled %d unique cat food products\n' % n)
    for k in ('product_name', 'brands', 'image', 'wet/dry known', 'ingredients (>60ch)',
              'ingredients in English', 'any protein', 'plausible protein', 'moisture',
              'fibre', 'ash', 'taurine', 'ingredients AND protein AND fat'):
        print('  %-34s %4d  %5.1f%%' % (k, have[k], 100.0 * have[k] / n))

    print('\nNutriment schema split:')
    for k in ('crude only', 'human only', 'both', 'neither'):
        print('  %-34s %4d  %5.1f%%' % (k, schema[k], 100.0 * schema[k] / n))

    total = plausible + implausible
    if total:
        print('\nOf the %d products with a protein figure, %d (%.1f%%) are implausible.'
              % (total, implausible, 100.0 * implausible / total))
    return 0


if __name__ == '__main__':
    sys.exit(main(int(sys.argv[1]) if len(sys.argv) > 1 else 6))
