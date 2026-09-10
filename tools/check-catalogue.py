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

It also checks the raw panel captures in tools/data/panels/, which hold what
the label printed rather than what this site scores. See PRD section 12.11 for
why they exist and why they are not part of an entry.

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
    # 65, not 50, since 2026-09-09. See the note beside PLAUSIBLE in
    # assets/js/opff.js: a manufacturer's published 59% was rejected as
    # impossible by a band drawn from supermarket food.
    'crudeProteinPct': (3, 65),
    'crudeFatPct': (0.5, 40),
    'crudeFibrePct': (0, 15),
    'ashPct': (0, 15),
    'moisturePct': (0, 92),
    'kcalPer100g': (15, 600),
}

# PRD 12.11: everything the panel prints is captured, including the figures
# nothing scores. It lives here rather than on the catalogue entry because
# catalogue.json is fetched by every visitor and precached by the service
# worker, and a hundred verbatim panels would be most of a megabyte of data no
# page reads. Nothing under tools/ is served, so the capture costs a visitor
# nothing and costs a future field nothing to backfill from.
PANELS = os.path.join(ROOT, 'tools', 'data', 'panels')
PANEL_REQUIRED = {'barcode', 'source', 'sourceKind', 'checked', 'text'}
PANEL_OPTIONAL = {'capturedFrom', 'analysis', 'statements'}
CAPTURE_KINDS = {'html', 'pdf', 'photo', 'manual'}

# A capture is a second reading of the panel the entry was read from, so the
# two can be compared, and a transcription error shows up as a disagreement
# between them. This is not the plausible bands by another name: the bands
# judge the label, and ask whether 59% protein can be true. This judges the
# transcription, and asks whether the entry says what the panel said. It is the
# only check in this project that can catch a right-looking wrong number.
CROSS_CHECK = {
    'crudeProteinPct': 'crude protein',
    'crudeFatPct': 'crude fat',
    'crudeFibrePct': 'crude fib',
    'moisturePct': 'moisture',
    'ashPct': 'crude ash',
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


def check_panel(panel, key, entry, problems):
    """Shape, not meaning.

    PRD 12.11 rule 3: the plausible bands exist to protect scores, and nothing
    in here is scored, so a figure this file holds is checked for being a
    string and not for being believable. The one thing that is enforced beyond
    shape is that a capture and its entry were the same reading of the same
    panel, because a record whose parsed fields are current and whose raw text
    is two years stale is worse than no record.
    """
    def bad(message):
        problems.append('panels/%s.json: %s' % (key, message))

    if not isinstance(panel, dict):
        bad('capture is not an object')
        return

    missing = PANEL_REQUIRED - set(panel)
    if missing:
        bad('missing %s' % ', '.join(sorted(missing)))
    unknown = set(panel) - PANEL_REQUIRED - PANEL_OPTIONAL
    if unknown:
        bad('unknown key(s): %s' % ', '.join(sorted(unknown)))

    if panel.get('barcode') != key:
        bad('barcode field %r does not match its filename' % panel.get('barcode'))

    text = panel.get('text')
    if not isinstance(text, str):
        bad('text must be a string')
    elif len(text.strip()) < 40:
        bad('text is too short to be a captured panel')

    if entry is None:
        bad('no catalogue entry for this barcode. A capture records the panel an '
            'entry was read from, so it does not stand alone')
    else:
        for field in ('source', 'sourceKind', 'checked'):
            if panel.get(field) != entry.get(field):
                bad('%s is %r and the catalogue entry says %r. One reading, one date'
                    % (field, panel.get(field), entry.get(field)))

    kind = panel.get('capturedFrom')
    if kind is not None and kind not in CAPTURE_KINDS:
        bad('capturedFrom must be one of %s' % ', '.join(sorted(CAPTURE_KINDS)))

    analysis = panel.get('analysis')
    if analysis is not None:
        if not isinstance(analysis, dict):
            bad('analysis must be an object of label to printed value')
        else:
            for label, value in analysis.items():
                if not isinstance(value, str) or not str(value).strip():
                    bad('analysis[%r] must be the value as printed, got %r' % (label, value))

    statements = panel.get('statements')
    if statements is not None:
        if not isinstance(statements, list):
            bad('statements must be a list of sentences as printed')
        elif not all(isinstance(s, str) and s.strip() for s in statements):
            bad('every statement is a non-empty string, as printed')




def cross_check(entry, panel, key, problems):
    """What the entry claims against what the capture recorded.

    Only where both hold the figure. A capture whose reader missed a line is a
    thinner record, not a contradiction, and failing the gate for it would
    punish the entry for the reader's gap. A disagreement is different: one of
    the two readings of one panel is wrong, and neither the score nor the
    record can be trusted until somebody says which.
    """
    def bad(message):
        problems.append('%s: %s' % (key, message))

    analysis = panel.get('analysis') or {}
    if not isinstance(analysis, dict):
        return
    for field, needle in CROSS_CHECK.items():
        if field not in entry:
            continue
        printed = [v for label, v in analysis.items()
                   if isinstance(label, str) and needle in label.lower()]
        if not printed:
            continue
        number = re.match(r'([\d.]+)', str(printed[0]).strip())
        if not number:
            continue
        if abs(float(number.group(1)) - entry[field]) > 0.001:
            bad('%s is %s and the captured panel prints %r. One of the two readings is wrong'
                % (field, entry[field], printed[0]))

    kcal = [v for v in analysis.values() if isinstance(v, str) and 'kcal/kg' in v]
    if kcal and 'kcalPer100g' in entry:
        number = re.match(r'([\d,]+)', kcal[0].strip())
        if number:
            perkg = float(number.group(1).replace(',', ''))
            if abs(entry['kcalPer100g'] - perkg / 10.0) > 0.05:
                bad('kcalPer100g is %s and the captured panel prints %r'
                    % (entry['kcalPer100g'], kcal[0]))


def read_panels(problems):
    """Every capture on disk, keyed by barcode."""
    found = {}
    if not os.path.isdir(PANELS):
        return found
    for name in sorted(os.listdir(PANELS)):
        if not name.endswith('.json'):
            continue
        key = name[:-len('.json')]
        try:
            found[key] = json.loads(io.open(os.path.join(PANELS, name), encoding='utf-8').read())
        except ValueError as exc:
            problems.append('panels/%s: not valid JSON: %s' % (name, exc))
    return found


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

    panels = read_panels(problems)
    for key in sorted(panels):
        check_panel(panels[key], key, products.get(key), problems)
        if isinstance(panels[key], dict) and key in products:
            cross_check(products[key], panels[key], key, problems)

    for key in sorted(products):
        entry = products[key]
        name = (entry.get('name') or entry.get('ingredientsText') or '')[:38]
        fields = sorted(set(entry) & DATA_FIELDS)
        print('  %-14s %-12s %-10s %s' % (key, entry.get('sourceKind', '?'),
                                          entry.get('checked', '?'), ', '.join(fields)))
        if name:
            print('  %-14s %s' % ('', name))
        panel = panels.get(key)
        if panel:
            print('  %-14s panel captured, %d characters%s' % (
                '', len(panel.get('text') or ''),
                ', %d figures' % len(panel['analysis']) if panel.get('analysis') else ''))

    print('')
    if problems:
        for p in problems:
            print('FAIL  %s' % p)
        print('\n%d entr%s, %d problem(s).'
              % (len(products), 'y' if len(products) == 1 else 'ies', len(problems)))
        return 1
    # Not a failure. Captures are backfilled as products are revisited, and an
    # entry written before PRD 12.11 existed is not wrong, only thinner.
    print('%d entr%s, all sourced, within the plausible bands, and agreeing with '
          'the %d raw panel(s) captured.'
          % (len(products), 'y' if len(products) == 1 else 'ies', len(panels)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
