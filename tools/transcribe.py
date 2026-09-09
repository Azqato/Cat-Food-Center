# -*- coding: utf-8 -*-
"""Transcribe one product into the curated catalogue, from wherever its panel is.

    python tools/transcribe.py <url> [--barcode 000338022002]
    python tools/transcribe.py <url> --find-barcode "Dr. Elsey's cleanprotein chicken"
    python tools/transcribe.py <url> --barcode N --name "..." --brand "..." --write
    python tools/transcribe.py --batch tools/data/batch.json

`tools/label-deck.py` reads a Purina PDF and nothing else. This is the general
form of the same job, and it is the procedure docs/PRD.md section 12.10
describes rather than a second way of doing it: the parsing is imported from
label-deck.py, so a fix to either lands in both.

**What it adds over the PDF tool.**

*HTML panels.* Dr. Elsey's, and every manufacturer that publishes the panel as
page text rather than as a PDF. The page is reduced to text and handed to the
same parsers, because a panel is a panel wherever it is printed.

*A barcode.* The catalogue is keyed by barcode and manufacturers do not print
UPCs on their websites, which is the blocker that held M23 from 2026-09-08.
`--find-barcode` asks UPCitemdb, which aggregates them, and **prints candidates
for a person to choose rather than picking one**. A wrong barcode is the worst
error this project can make: it does not look wrong anywhere, it silently
attaches one product's panel to another product's scan, and no gate can catch
it, because both halves are individually valid. So the tool proposes and a
person decides, every time.

*Writing.* `--write` puts the entry in assets/data/catalogue.json and runs
check-catalogue.py, refusing to leave a file the gate rejects. Without it,
nothing is written and the proposal is printed for review, which is the default
for the same reason label-deck.py's is.

**Both sources are claims, and the entry says which kind.** A manufacturer's own
panel is `sourceKind: "manufacturer"`. A barcode from an aggregator is neither
the manufacturer nor a retailer listing, so an entry carrying one records where
it came from in `note` and keeps the `sourceKind` of the panel: the panel is
what the score is computed from, and it is what the visitor is being asked to
trust. The barcode is the key it is filed under.
"""
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOGUE = os.path.join(ROOT, 'assets', 'data', 'catalogue.json')
UPC_API = 'https://api.upcitemdb.com/prod/trial/search'
UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/140.0 Safari/537.36')

_spec = importlib.util.spec_from_file_location(
    'label_deck', os.path.join(ROOT, 'tools', 'label-deck.py'))
deck = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(deck)


def fetch_text(url):
    """The page or the deck, as text, whichever this URL is."""
    request = urllib.request.Request(
        url, headers={'User-Agent': UA, 'Accept': 'text/html,application/pdf,*/*'})
    with urllib.request.urlopen(request, timeout=60) as response:
        body = response.read()
        kind = response.headers.get('Content-Type', '')
    if 'pdf' in kind.lower() or url.lower().endswith('.pdf'):
        return deck.text_of(body), 'pdf'
    return html_text(body.decode('utf-8', 'replace')), 'html'


def html_text(source):
    """Page markup to readable text, panel intact.

    Scripts and styles go first: a page's JSON-LD contains the ingredient list
    a second time, in a different order, and a parser that meets both cannot
    tell which one the label printed. Tags become newlines rather than being
    deleted, so two cells of a nutrition table do not run into one number.
    """
    text = re.sub(r'<(script|style|noscript)\b.*?</\1>', ' ', source, flags=re.S | re.I)
    text = re.sub(r'<br\s*/?>|</(p|div|li|tr|td|th|h\d)>', '\n', text, flags=re.I)
    text = re.sub(r'<[^>]+>', ' ', text)
    try:
        import html as html_module
        text = html_module.unescape(text)
    except Exception:
        pass
    text = text.replace('’', "'").replace('‘', "'")
    text = re.sub(r'[ \t\xa0]+', ' ', text)
    return re.sub(r'\n\s*\n+', '\n', text)


def find_ingredients_html(text):
    """The ingredient list on a page that never writes the word "Ingredients:".

    A PDF label prints "INGREDIENTS: chicken, ..." and label-deck.py keys off
    that. Dr. Elsey's puts "Ingredients" in a tab heading and the list in an
    unlabelled paragraph three lines below, so the colon the PDF parser needs
    is nowhere on the page.

    The rule here: after a line that is exactly the tab heading, take the first
    line that reads like a list, meaning at least five commas. Falling back to
    the labelled form when that finds nothing, so a page that does print the
    label is still read the way the deck is.

    Both halves refuse rather than guess. An ingredient list is the input to
    every score this site prints, and a paragraph of marketing copy mistaken
    for one would be scored, displayed and believed.
    """
    lines = [line.strip() for line in text.split(chr(10))]
    for index, line in enumerate(lines):
        if not re.fullmatch(r'ingredients?', line, re.I):
            continue
        for candidate in lines[index + 1:index + 12]:
            if candidate.count(',') >= 5:
                return candidate.rstrip('.').strip()
    return deck.find_ingredients(text)


def find_kcal(flat):
    """Calories per kilogram or per cup, as the label states them.

    Recorded only when the label says so. Section 16.5a's rule is that a
    curated figure is a published figure, and a kcal/kg computed from the
    guaranteed analysis is a calculation this project would be inventing.
    """
    match = re.search(r'([\d,]{3,6})\s*(?:kcal|calories)\s*(?:ME\s*)?(?:/|per\s*)\s*kg',
                      flat, re.I)
    return float(match.group(1).replace(',', '')) if match else None


def resolve_barcode(query, limit=8):
    """Ask an aggregator what UPC this product carries. Never decide.

    UPCitemdb's trial endpoint takes no key, is rate limited, and aggregates
    from retailers rather than from manufacturers, so a hit is evidence and not
    a fact. It is printed with the title it is filed under, which is the only
    thing a reviewer can check it against.
    """
    url = UPC_API + '?' + urllib.parse.urlencode(
        {'s': query, 'match_mode': '0', 'type': 'product'})
    request = urllib.request.Request(url, headers={'User-Agent': UA})
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            data = json.loads(response.read().decode('utf-8'))
    except Exception as err:
        return [], str(err)
    rows = []
    for item in (data.get('items') or [])[:limit]:
        code = (item.get('upc') or item.get('ean') or '').strip()
        if code:
            rows.append({'barcode': code, 'title': item.get('title') or '',
                         'brand': item.get('brand') or ''})
    return rows, None


def propose(url, barcode, raw, kind, meta=None):
    """The entry this panel supports, and nothing it does not.

    `meta` carries the name, brand and quantity, which no panel states and
    every entry for a product the database has never heard of needs. A curated
    entry filling a gap in an existing record inherits its name from upstream;
    an entry for a product upstream does not hold has no name at all unless one
    is given here, and a product page headed by a blank line is not a product
    page. `searchCatalogue` could not find it either, so the entry would exist
    and be unreachable, which M25 spent a milestone making impossible.
    """
    flat = deck.flatten(raw)
    entry = {
        'barcode': barcode,
        'source': url,
        'sourceKind': 'manufacturer',
        'checked': __import__('time').strftime('%Y-%m-%d'),
    }
    for field, label in deck.GA_FIELDS:
        value = deck.find_percent(flat, label)
        if value is not None:
            entry[field] = value
    if re.search(r'\btaurine\b', raw, re.I):
        entry['taurinePresent'] = True
    kcal = find_kcal(flat)
    if kcal is not None:
        entry['kcalPer100g'] = round(kcal / 10.0, 1)

    listing = find_ingredients_html(raw) if kind == 'html' else deck.find_ingredients(raw)
    if listing:
        entry['ingredientsText'] = listing
        entry['ingredientsLang'] = 'en'

    title = first_title(raw, kind)
    fmt = deck.product_format(title, url)
    if fmt:
        entry['format'] = fmt
    for field in ('name', 'brand', 'quantity'):
        value = (meta or {}).get(field)
        if value:
            entry[field] = value
    note = (meta or {}).get('note')
    if note:
        entry['note'] = note

    aafco = deck.find_aafco(raw)
    if aafco:
        entry['aafcoComplete'] = True
        stage = deck.life_stage(aafco, title)
        if stage:
            entry['lifeStage'] = stage
    return entry, title, aafco


def first_title(raw, kind):
    if kind == 'pdf':
        return raw.strip().split('\n')[0].strip()
    for line in raw.split('\n'):
        line = line.strip()
        if 20 < len(line) < 90 and not line.startswith('http'):
            return line
    return ''


def write_entry(entry):
    """Into the catalogue, and only if the gate still passes afterwards."""
    data = json.load(io.open(CATALOGUE, encoding='utf-8'))
    before = json.dumps(data, ensure_ascii=False, indent=1)
    if entry['barcode'] in data['products']:
        print('# %s is already in the catalogue. Nothing written.' % entry['barcode'])
        return 1
    data['products'][entry['barcode']] = entry
    io.open(CATALOGUE, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(data, ensure_ascii=False, indent=1) + '\n')
    gate = subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'check-catalogue.py')],
                          capture_output=True, text=True)
    print(gate.stdout.strip()[-800:])
    if gate.returncode != 0:
        io.open(CATALOGUE, 'w', encoding='utf-8', newline='\n').write(before + '\n')
        print('# The gate refused this entry, so the catalogue is unchanged.')
        return 1
    print('# Written. %d entries.' % len(data['products']))
    return 0


def one(url, barcode, find, write, meta=None):
    raw, kind = fetch_text(url)
    if find:
        rows, error = resolve_barcode(find)
        if error:
            print('# Barcode lookup failed: %s' % error)
        for row in rows:
            print('#   %-14s %s  [%s]' % (row['barcode'], row['title'][:60], row['brand'][:20]))
        print('# Pick one and rerun with --barcode. Nothing here is chosen for you.')
        if not barcode:
            return 2
    entry, title, aafco = propose(url, barcode or 'PUT-THE-BARCODE-HERE', raw, kind, meta)
    print('# %s' % title)
    print('# AAFCO: %s' % (aafco or 'not found on this page'))
    print('# Read every figure against the source before this is trusted.')
    print(json.dumps({entry['barcode']: entry}, ensure_ascii=False, indent=1))
    missing = [f for f, _ in deck.GA_FIELDS if f not in entry]
    if missing:
        print('# Not found, which may be correct for this product: %s' % ', '.join(missing))
    if write:
        if not barcode:
            print('# Refusing to write without a barcode.')
            return 2
        return write_entry(entry)
    return 0


def main(argv):
    if not argv:
        print(__doc__.strip().split('\n\n')[1])
        return 2
    if argv[0] == '--batch':
        rows = json.load(io.open(argv[1], encoding='utf-8'))
        worst = 0
        for row in rows:
            print('\n# ---- %s' % row['url'])
            worst = max(worst, one(row['url'], row.get('barcode'), row.get('find'),
                                   '--write' in argv, row))
        return worst
    url = argv[0]

    def option(name):
        return argv[argv.index(name) + 1] if name in argv else None

    meta = {'name': option('--name'), 'brand': option('--brand'),
            'quantity': option('--quantity'), 'note': option('--note')}
    return one(url, option('--barcode'), option('--find-barcode'),
               '--write' in argv, meta)


if __name__ == '__main__':
    if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    raise SystemExit(main(sys.argv[1:]))
