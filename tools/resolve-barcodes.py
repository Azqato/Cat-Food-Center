# -*- coding: utf-8 -*-
"""Ask an aggregator for a barcode for each top-100 SKU. Never choose one.

    python tools/resolve-barcodes.py --list cat-food
    python tools/resolve-barcodes.py --list cat-food --limit 20
    python tools/resolve-barcodes.py --review

Section 12.7 names the products this site should cover and `tools/top-skus.json`
holds them, with names and ranks and no barcodes, because no storefront
publishes a UPC. Section 12.10 needs one before a panel can become an entry.
This is the bridge, and it is the slowest part of the whole programme, so it is
built to run unattended and to be resumed rather than restarted.

**It proposes and a person decides.** Every candidate is written with the title
the aggregator files it under, and nothing is ever written to the catalogue
from here. That rule is section 12.10's and the reason is there: a wrong
barcode does not look wrong anywhere, it silently attaches one product's panel
to another product's scan, and no gate can catch it because both halves are
individually valid. On 2026-09-09 five listings were refused for exactly this,
having described a can size the manufacturer does not sell.

**On pacing, which is the whole engineering problem here.**

There are two meters and they are easy to confuse, because the endpoint
reports a different one depending on whether it is answering or refusing.

* **20 requests per hour.** Reported only on a 429, as `X-RateLimit-Limit: 20`
  with `Retry-After` counting down the rest of the hour.
* **100 requests per day.** Reported on every successful response, as
  `X-RateLimit-Limit: 100` with `X-RateLimit-Remaining` counting down.

Measured on 2026-09-10 rather than assumed, after two earlier readings that
were both wrong. On 2026-09-09 queries seven and twelve seconds apart drew
429s, and the conclusion recorded was that the endpoint rations lookups to
three or five a day; that made the top 100 look like twenty days of work and
made the barcode problem look structural, which reshaped the roadmap around a
constraint that does not exist. Then on 2026-09-10 eight queries at 22 seconds
all succeeded, and the conclusion drawn was 100 a day at any spacing, which is
also wrong: those eight were simply the tail of an hourly window that had room
in it. The twenty-first query of the hour was refused whatever the gap.

**So the constraint is 20 an hour, and the top 100 is about five hours
unattended rather than twenty days or forty minutes.** This paces one query
every three minutes, which is the hourly allowance spread evenly and never
trips the window, saves after every single query so a run can be stopped and
resumed at any point, and sleeps out the full `Retry-After` if it is throttled
anyway rather than retrying into a ban.
"""
import argparse
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKUS = os.path.join(ROOT, 'tools', 'data', 'top-skus.json')
OUT = os.path.join(ROOT, 'tools', 'data', 'barcode-candidates.json')
API = 'https://api.upcitemdb.com/prod/trial/search'
UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/140.0 Safari/537.36')

# Never spend the last of the day's allowance. A run that stops with headroom
# can be resumed; one that hits zero has also spent whatever anybody else
# needed the endpoint for today.
FLOOR = 5
# 20 an hour is one every 180 seconds. Spread evenly rather than spent in a
# burst and then waited out, because an even pace is resumable at any moment
# and a burst is only resumable on the hour.
GAP = 185
HOURLY = 20

# Words that describe the packaging rather than the product. A query naming the
# pack type returns nothing: on 2026-09-09 "Dr. Elsey's cleanprotein duck
# chicken kibble cat food" drew a 404 where "Dr. Elsey's cleanprotein duck"
# returned two rows. Brand, line and flavour, and no more.
NOISE = re.compile(
    r'\b(?:wet|dry|cat|food|cats|kitten|adult|cans?|can|pouch(?:es)?|bags?|tubs?|'
    r'count|ct|pack|packs|variety|multipack|oz|ounce|lb|lbs|pound|pounds|'
    r'with|and|for|the|in|of|made|no|artificial|colors?|colours?|preservatives?|'
    r'natural|premium|recipe|formula|flavor|flavour|value|size|each|pk)\b',
    re.I)


def significant(title, brand, keep=4):
    """A query short enough to match, specific enough to mean something."""
    head = re.split(r'[|,(]', title)[0]
    head = NOISE.sub(' ', head)
    words = [w for w in re.findall(r"[A-Za-z0-9'-]+", head) if len(w) > 2]
    brand_words = set(w.lower() for w in re.findall(r"[A-Za-z0-9']+", brand or ''))
    rest = [w for w in words if w.lower() not in brand_words]
    return ' '.join(([brand] if brand else []) + rest[:keep]).strip()


class Endpoint(object):
    """The aggregator, and what it says about how much is left."""

    def __init__(self):
        self.remaining = None     # of the day's 100, from successful responses
        self.limit = None
        self.wait = 0             # seconds the hourly window says to wait
        self.gap = GAP
        self.spent = 0

    def _note(self, headers, refused):
        def num(name):
            try:
                return int(float(headers.get(name)))
            except (TypeError, ValueError):
                return None
        # A refusal reports the hourly meter, a success reports the daily one.
        # Reading them into the same field is how a full hour looks like a
        # spent day and stops a run that had 80 queries left in it.
        if refused:
            self.wait = num('Retry-After') or 0
            return
        self.limit = num('X-RateLimit-Limit') or self.limit
        got = num('X-RateLimit-Remaining')
        if got is not None:
            self.remaining = got

    def exhausted(self):
        return self.remaining is not None and self.remaining <= FLOOR

    def search(self, query, limit=10):
        url = API + '?' + urllib.parse.urlencode(
            {'s': query, 'match_mode': '0', 'type': 'product'})
        request = urllib.request.Request(url, headers={'User-Agent': UA})
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                data = json.loads(response.read().decode('utf-8'))
                self._note(response.headers, refused=False)
            self.spent += 1
        except urllib.error.HTTPError as err:
            self._note(err.headers, refused=(err.code == 429))
            if err.code == 429:
                # The hourly window is spent. There is nothing to do but wait
                # it out; retrying sooner is how a rate limit becomes a ban.
                return None, 'hourly window spent, waiting %ds' % (self.wait or 3600)
            if err.code == 404:
                self.spent += 1
                return [], None      # a real answer: nothing filed under this
            return None, 'HTTP %s' % err.code
        except Exception as err:
            return None, str(err)[:80]

        rows = []
        for item in (data.get('items') or [])[:limit]:
            code = (item.get('upc') or item.get('ean') or '').strip()
            if code:
                rows.append({'barcode': code,
                             'title': item.get('title') or '',
                             'brand': item.get('brand') or ''})
        return rows, None


def load_done():
    if not os.path.exists(OUT):
        return {}
    try:
        data = json.loads(io.open(OUT, encoding='utf-8').read())
        return data.get('resolved') or {}
    except ValueError:
        return {}


def save(resolved, endpoint):
    io.open(OUT, 'w', encoding='utf-8', newline='\n').write(json.dumps({
        '_readme': [
            'Barcode candidates for the top-100 SKUs, written by tools/resolve-barcodes.py.',
            '',
            'CANDIDATES, NOT IDENTIFICATIONS. Nothing here has been chosen, and nothing here',
            'may be written into assets/data/catalogue.json without a person reading the title',
            'against the product first. See docs/PRD.md section 12.10: a wrong barcode does not',
            'look wrong anywhere, and no gate downstream can catch it.',
            '',
            'A row with an empty candidate list means the aggregator has nothing filed under',
            'that query. That is an answer, not a failure, and it is what provisional keys',
            'exist for (section 12.12).',
        ],
        'measured': time.strftime('%Y-%m-%d'),
        'endpoint': {'limit': endpoint.limit, 'remaining': endpoint.remaining,
                     'spentThisRun': endpoint.spent},
        'resolved': resolved,
    }, ensure_ascii=False, indent=1) + '\n')


def pick_list(name):
    data = json.loads(io.open(SKUS, encoding='utf-8').read())
    for capture in data['captures']:
        if capture['list'] == name:
            return capture
    raise SystemExit('No capture named %r. Have: %s'
                     % (name, ', '.join(c['list'] for c in data['captures'])))


def review():
    resolved = load_done()
    if not resolved:
        raise SystemExit('Nothing resolved yet.')
    none_found = [k for k, v in resolved.items() if not v['candidates']]
    print('%d SKU(s) queried, %d with no candidate at all.' % (len(resolved), len(none_found)))
    print('')
    for ref in sorted(resolved, key=lambda r: resolved[r]['position']):
        row = resolved[ref]
        print('%3d  %s' % (row['position'], row['title'][:92]))
        print('     query: %s' % row['query'])
        for candidate in row['candidates'][:4]:
            print('       %-14s %s' % (candidate['barcode'], candidate['title'][:78]))
        if not row['candidates']:
            print('       nothing filed under this query')
    return 0


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--list', default='cat-food')
    parser.add_argument('--limit', type=int, default=0)
    parser.add_argument('--review', action='store_true')
    args = parser.parse_args(argv)

    if args.review:
        return review()

    capture = pick_list(args.list)
    resolved = load_done()
    endpoint = Endpoint()

    todo = [item for item in capture['items'] if item['ref'] not in resolved]
    if args.limit:
        todo = todo[:args.limit]
    print('%d of %d already done. Querying %d, about %.1f hours at %d an hour.'
          % (len(resolved), len(capture['items']), len(todo),
             len(todo) * endpoint.gap / 3600.0, HOURLY))

    for index, item in enumerate(todo):
        if endpoint.exhausted():
            print('Stopping with %s left of %s, which is the floor. Resume tomorrow.'
                  % (endpoint.remaining, endpoint.limit))
            break
        query = significant(item['title'], item.get('brand'))
        if not query:
            continue
        rows, error = endpoint.search(query)
        if rows is None:
            print('%3d  %-44s %s' % (item['position'], query[:44], error))
            if endpoint.wait:
                time.sleep(endpoint.wait + 5)
                endpoint.wait = 0
            else:
                time.sleep(60)
            continue
        resolved[item['ref']] = {
            'position': item['position'],
            'title': item['title'],
            'brand': item.get('brand'),
            'query': query,
            'candidates': rows,
        }
        print('%3d  %-44s %d candidate(s), %s left'
              % (item['position'], query[:44], len(rows), endpoint.remaining))
        save(resolved, endpoint)
        if index < len(todo) - 1:
            time.sleep(endpoint.gap)

    save(resolved, endpoint)
    print('')
    print('%d of %d SKUs have candidates on file. %d queries spent this run, %s left today.'
          % (len(resolved), len(capture['items']), endpoint.spent, endpoint.remaining))
    print('Nothing has been chosen. `--review` prints them for a person to read.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
