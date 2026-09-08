# -*- coding: utf-8 -*-
"""Gate: the curated catalogue is well formed and says where its data came from.

    python tools/check-catalogue.py

assets/data/catalogue.json carries product data transcribed by hand where Open
Pet Food Facts has none. That data is published under this site's name and
feeds the same scoring engine as everything else, so it is held to the same
standard as an upstream record and to one the upstream is not: every entry has
to say where it was read and when.

This is a gate rather than a review checklist because the failure it prevents
is quiet. A mistyped key is ignored by the merge and the figure simply never
appears; an implausible transcription produces a wrong score that looks exactly
like a right one. Neither shows up in a diff as anything but a number.

The bands and the reasoning behind them are docs/PRD.md sections 12.5 and 16.5a.
"""
import datetime
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, 'assets', 'data', 'catalogue.json')

# Mirrors DATA_FIELDS in assets/js/catalogue.js. A key outside this set is
# rejected rather than ignored: the merge would skip it in silence, and a
# curated figure that never reaches the page is indistinguishable from one
# nobody transcribed.
DATA_FIELDS = {
    'ingredientsText',
    'crudeProteinPct', 'crudeFatPct', 'crudeFibrePct', 'ashPct', 'moisturePct',
    'kcalPer100g', 'taurinePresent',
    'name', 'brand', 'quantity', 'format', 'lifeStage', 'aafcoComplete',
}
META_FIELDS = {'barcode', 'source', 'sourceKind', 'checked', 'note'}
# Not data in its own right: it says what language the list beside it is in.
# An entry carrying only this carries nothing.
MODIFIER_FIELDS = {'ingredientsLang'}
SOURCE_KINDS = {'manufacturer', 'retailer-listing'}

# The same plausibility gate the normaliser applies to upstream figures
# (PRD 12.5 item 2). Ours are not exempt: a transcription error is as wrong as
# a data-entry error, and being ours does not make it truer.
BANDS = {
    'crudeProteinPct': (3, 50),
    'crudeFatPct': (0.5, 40),
    'crudeFibrePct': (0, 15),
    'ashPct': (0, 15),
    'moisturePct': (0, 92),
    'kcalPer100g': (15, 600),
}

FORMATS = {'wet', 'dry', 'unknown'}
LIFE_STAGES = {'growth', 'adult', 'all', 'unknown'}


def check(entry, key, problems):
    def bad(message):
        problems.append('%s: %s' % (key, message))

    if not isinstance(entry, dict):
        bad('entry is not an object')
        return

    unknown = set(entry) - DATA_FIELDS - META_FIELDS - MODIFIER_FIELDS
    if unknown:
        bad('unknown key(s): %s' % ', '.join(sorted(unknown)))

    if entry.get('barcode') != key:
        bad('barcode field %r does not match its key' % entry.get('barcode'))
    if not re.match(r'^\d{6,14}$', str(key)):
        bad('key is not a 6 to 14 digit barcode')

    source = (entry.get('source') or '').strip()
    if not source:
        bad('no source. Every entry says where it was read')
    if entry.get('sourceKind') not in SOURCE_KINDS:
        bad('sourceKind must be one of %s' % ', '.join(sorted(SOURCE_KINDS)))

    checked = entry.get('checked')
    try:
        when = datetime.date.fromisoformat(str(checked))
    except (TypeError, ValueError):
        bad('checked must be an ISO date, got %r' % checked)
    else:
        if when > datetime.date.today():
            bad('checked date %s is in the future' % checked)

    data = set(entry) & DATA_FIELDS
    if not data:
        bad('carries no data. An entry that overrides nothing has no reason to exist')

    for field, (low, high) in BANDS.items():
        if field not in entry:
            continue
        value = entry[field]
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            bad('%s must be a number, got %r' % (field, value))
        elif not low <= value <= high:
            bad('%s is %s, outside the plausible band %s to %s' % (field, value, low, high))

    if 'ingredientsText' in entry:
        text = (entry['ingredientsText'] or '').strip()
        if len(text) < 20:
            bad('ingredientsText is too short to be a real list')
        # An entry that supplies a list without naming its language would be
        # read as unknown and treated as unreadable. That is the safe default,
        # but here it is almost certainly an omission, so it is refused.
        if not (entry.get('ingredientsLang') or '').strip():
            bad('ingredientsText without ingredientsLang. Say what language it is in')

    if 'ingredientsLang' in entry and 'ingredientsText' not in entry:
        bad('ingredientsLang without an ingredientsText for it to describe')

    if 'format' in entry and entry['format'] not in FORMATS:
        bad('format must be one of %s' % ', '.join(sorted(FORMATS)))
    if 'lifeStage' in entry and entry['lifeStage'] not in LIFE_STAGES:
        bad('lifeStage must be one of %s' % ', '.join(sorted(LIFE_STAGES)))
    if 'aafcoComplete' in entry and not isinstance(entry['aafcoComplete'], bool):
        bad('aafcoComplete must be true or false, or absent where it is unknown')
    if 'taurinePresent' in entry and entry['taurinePresent'] is not True:
        bad('taurinePresent records only a positive declaration, so it is true or absent')


def main():
    if not os.path.exists(PATH):
        print('No catalogue at %s.' % os.path.relpath(PATH, ROOT))
        return 1
    try:
        data = json.loads(io.open(PATH, encoding='utf-8').read())
    except ValueError as exc:
        print('FAIL  catalogue.json is not valid JSON: %s' % exc)
        return 1

    products = data.get('products')
    if not isinstance(products, dict):
        print('FAIL  no "products" object')
        return 1

    problems = []
    for key in sorted(products):
        check(products[key], key, problems)

    for key in sorted(products):
        entry = products[key]
        name = (entry.get('name') or entry.get('ingredientsText') or '')[:38]
        fields = sorted(set(entry) & DATA_FIELDS)
        print('  %-14s %-12s %-10s %s' % (key, entry.get('sourceKind', '?'),
                                          entry.get('checked', '?'), ', '.join(fields)))
        if name:
            print('  %-14s %s' % ('', name))

    print('')
    if problems:
        for p in problems:
            print('FAIL  %s' % p)
        print('\n%d entr%s, %d problem(s).'
              % (len(products), 'y' if len(products) == 1 else 'ies', len(problems)))
        return 1
    print('%d entr%s, all sourced and within the plausible bands.'
          % (len(products), 'y' if len(products) == 1 else 'ies'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
