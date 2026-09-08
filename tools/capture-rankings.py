# -*- coding: utf-8 -*-
"""Capture retailer best-seller rankings into tools/data/top-skus.json.

    python tools/capture-rankings.py            capture every reachable source
    python tools/capture-rankings.py amazon     just one

This answers "which products should the site cover?", which section 12.7 says
is decided by what people actually buy rather than by what happens to be in the
database. It writes a dated capture per source and **keeps every previous
capture**: a product falling off a best-seller list is information about the
market, and a file that overwrites its history cannot show it.

**This captures names and ranks, not barcodes.** Retailers do not publish the
UPC, and the catalogue in assets/data/catalogue.json is keyed by barcode, so a
row here is a statement that a product is worth covering, not an entry. Barcode
resolution is a separate problem and is tracked in section 12.8.

**Which storefronts work, measured 2026-09-08 by driving Edge at each one:**

| Storefront | Result |
|---|---|
| Amazon Best Sellers | Loads, and publishes real rank numbers. The best source by a distance |
| Target | Loads and sorts by best selling, but its link text runs the promotional line, the price, the product name and the star rating together. Disabled: a half-cleaned name looks usable and is not |
| PetSmart | Loads, but its product grid is built so that no link carries a usable product name. Nothing was extractable, so it contributes nothing until somebody writes a selector for it |
| Chewy | HTTP 403 to a real browser, with a bot-detection reference number |
| Walmart | Serves a "Robot or human?" interstitial |
| Petco | HTTP 403 to every category and search URL tried |

Chewy was the pet-specialist source section 12.7 originally named, and the
intent behind naming it was a channel where premium brands rank that barely
register on Amazon. That intent is currently unmet: Chewy refuses outright,
Petco and Walmart refuse, and PetSmart loads but yields nothing to this
extractor. So the capture is Amazon-weighted, and a list built from it will
under-represent premium and specialist brands. That is a known bias, recorded
in section 12.7 rather than papered over, and it is the reason Dr. Elsey's is
its own milestone rather than something the rankings would have surfaced.

**On being a well-behaved client.** This loads a handful of listing pages a
quarter, at human speed, reading public rankings. It is not a crawl, it does not
touch product pages in bulk, and it writes nothing anywhere. Section 20 forbids
pointing a state-changing check at somebody else's production system; reading a
best-seller page is neither state-changing nor frequent. If a storefront starts
refusing, the answer is to record that in the table above and drop the source,
never to work around the refusal.

Edge, never Chrome, per section 19.
"""
import asyncio
import datetime
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'tools', 'data', 'top-skus.json')
EDGE_CHANNEL = 'msedge'
TODAY = datetime.date.today().isoformat()

SOURCES = {
    'amazon': {
        'kind': 'ranked',
        'lists': {
            'cat-food': 'https://www.amazon.com/Best-Sellers-Cat-Food/zgbs/pet-supplies/2975265011',
            'dry-cat-food': 'https://www.amazon.com/Best-Sellers-Dry-Cat-Food/zgbs/pet-supplies/2975266011',
            'wet-cat-food': 'https://www.amazon.com/Best-Sellers-Wet-Canned-Cat-Food/zgbs/pet-supplies/2975267011',
        },
    },
    'petsmart': {
        'kind': 'listing',
        'lists': {
            'dry-cat-food': 'https://www.petsmart.com/cat/food-and-treats/dry-food/',
            'wet-cat-food': 'https://www.petsmart.com/cat/food-and-treats/wet-food/',
        },
    },
    # Target is deliberately absent. It loads and sorts by best selling, but its
    # link text is the product name run together with a promotional line, the
    # price and the star rating: "Buy 14 for $12 Purina Friskies cat
    # foodFriskies Purina Friskies Pate with Fish ... 1.1oz4.74.66 out". The
    # name is what a person matches against a manufacturer's site, and a
    # half-cleaned name is worse than no row, because it looks usable. Restore
    # this source when somebody writes a selector against the card structure
    # rather than the anchor text.
}

# Amazon numbers its own ranks in a badge, which is the only true ranking here.
AMAZON_JS = r"""() => {
  const out = [];
  document.querySelectorAll('div#gridItemRoot, div.zg-grid-general-faceout').forEach(card => {
    const badge = card.querySelector('.zg-bdg-text');
    const link = card.querySelector('a.a-link-normal[href*="/dp/"]');
    const title = card.querySelector('div[class*="line-clamp"]');
    const href = link ? link.getAttribute('href') : '';
    const m = href.match(/[/]dp[/]([A-Z0-9]{10})/);
    const text = title ? title.textContent.trim() : (link ? link.textContent.trim() : '');
    if (badge && text) {
      out.push({rank: parseInt(badge.textContent.replace(/\D/g, ''), 10), title: text, ref: m ? m[1] : null});
    }
  });
  return out;
}"""

# The other two publish a sorted grid with no numbers on it. Position in the
# grid is the rank, and it is recorded as position rather than rank so that
# nothing here pretends to a precision the page does not offer.
GRID_JS = r"""() => {
  const seen = new Set();
  const out = [];
  document.querySelectorAll('a[href]').forEach(a => {
    const href = a.getAttribute('href') || '';
    if (!/[/](p|product|shop)[/]/.test(href)) return;
    const text = (a.textContent || '').replace(/\s+/g, ' ').trim();
    if (text.length < 18 || seen.has(text)) return;
    seen.add(text);
    out.push({title: text.slice(0, 160), ref: href.split('?')[0].slice(-80)});
  });
  return out;
}"""

BRANDS = [
    "Dr. Elsey's", 'Fancy Feast', 'Friskies', 'Purina ONE', 'Purina Pro Plan', 'Pro Plan',
    'Cat Chow', 'Purina', 'Meow Mix', 'Sheba', 'Temptations', 'Whiskas', 'Iams', 'Blue Buffalo',
    'Hill’s', "Hill's", 'Science Diet', 'Royal Canin', 'Wellness', 'Tiki Cat', 'Weruva',
    'Instinct', 'Merrick', 'Nulo', 'Smalls', 'Open Farm', 'Rachael Ray', '9Lives', 'Special Kitty',
    'Pure Balance', 'Kirkland', 'Fromm', 'Orijen', 'Acana', 'Applaws', 'Fussie Cat', 'Solid Gold',
    'Natural Balance', 'American Journey', 'Tiny Tiger', 'Crave', 'Cat Person', 'Stella',
]


# Target puts the price and any merchandising badge inside the same link text
# as the product name, so a raw capture reads "$1.39 ($1.26/ounce)New at Fancy
# Feast Light Meat Tuna". Stripped here rather than left for the reader,
# because the name is what a person matches against a manufacturer's site.
NOISE = re.compile(
    r'^(?:\$[\d.,]+(?:\s*\([^)]*\))?\s*)+|^(?:New at|Bestseller|Highly rated|Sponsored|Only at)\s*',
    re.I)


def clean_title(title):
    previous = None
    while previous != title:
        previous = title
        title = NOISE.sub('', title).strip()
    return title


def brand_of(title):
    """The brand, where the title starts with one this project has met.

    A guess is worse than nothing here: the list is used to decide what to
    transcribe, and a wrong brand sends somebody to the wrong manufacturer's
    label deck. Unknown stays unknown, and the name is still readable by a
    person.
    """
    low = title.lower()
    for brand in BRANDS:
        if low.startswith(brand.lower()) or (' ' + brand.lower()) in low[:60]:
            return brand
    return None


async def capture(page, name, spec):
    out = []
    for list_name, url in spec['lists'].items():
        rows = {}
        pages = (1, 2) if spec['kind'] == 'ranked' else (1,)
        for page_no in pages:
            target = url + ('?_encoding=UTF8&pg=%d' % page_no) if spec['kind'] == 'ranked' else url
            try:
                response = await page.goto(target, wait_until='domcontentloaded', timeout=60000)
            except Exception as exc:
                print('  %s/%s FAILED %s' % (name, list_name, type(exc).__name__))
                continue
            status = response.status if response else 0
            body = await page.evaluate('document.body.innerText')
            if status >= 400 or re.search(r'robot or human|restricted access|captcha', body, re.I):
                print('  %s/%s REFUSED (HTTP %s)' % (name, list_name, status))
                break
            # Lazily loaded grids need scrolling, at reading speed rather than
            # as fast as the loop will go.
            for _ in range(9):
                await page.mouse.wheel(0, 2200)
                await page.wait_for_timeout(700)
            await page.wait_for_timeout(1200)
            found = await page.evaluate(AMAZON_JS if spec['kind'] == 'ranked' else GRID_JS)
            for index, row in enumerate(found):
                position = row.get('rank') or (len(rows) + index + 1)
                rows.setdefault(position, {'position': position, 'title': clean_title(row['title']),
                                           'ref': row.get('ref')})
        items = [rows[k] for k in sorted(rows)]
        items = [i for i in items if len(i['title']) >= 12]
        for item in items:
            item['brand'] = brand_of(item['title'])
        if items:
            out.append({
                'source': name,
                'list': list_name,
                'url': spec['lists'][list_name],
                'captured': TODAY,
                'ranked': spec['kind'] == 'ranked',
                'items': items,
            })
            print('  %s/%s %d items' % (name, list_name, len(items)))
    return out


async def run(which):
    from playwright.async_api import async_playwright
    captures = []
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(channel=EDGE_CHANNEL)
        context = await browser.new_context(locale='en-US', viewport={'width': 1366, 'height': 900})
        page = await context.new_page()
        for name, spec in SOURCES.items():
            if which and name not in which:
                continue
            print('%s ...' % name)
            captures.extend(await capture(page, name, spec))
        await browser.close()
    return captures


README = [
    'Retailer best-seller captures, the answer to "which products should this site cover?".',
    'Written by tools/capture-rankings.py; the reasoning is docs/PRD.md section 12.7.',
    '',
    'Every capture is kept. A product falling off a best-seller list is information about',
    'the market, and a file that overwrites its history cannot show it. Append, never replace.',
    '',
    'These rows carry names and ranks, never barcodes: no storefront publishes the UPC.',
    'A row here says a product is worth covering. It is not a catalogue entry, and',
    'assets/data/catalogue.json is keyed by barcode, so something has to resolve one before',
    'a row here can become an entry. That gap is section 12.8.',
    '',
    '"ranked": true means the storefront published rank numbers of its own. Where it is false,',
    '"position" is the order the products appeared in a best-selling sort, which is weaker.',
]


def main(argv):
    which = set(argv)
    unknown = which - set(SOURCES)
    if unknown:
        print('Unknown source(s): %s. Known: %s' % (', '.join(sorted(unknown)), ', '.join(sorted(SOURCES))))
        return 2

    captures = asyncio.run(run(which))
    if not captures:
        print('Nothing captured. Nothing written.')
        return 1

    document = {'_readme': README, 'captures': []}
    if os.path.exists(OUT):
        document = json.loads(io.open(OUT, encoding='utf-8').read())
        document['_readme'] = README
    # A repeat capture of the same source, list and day replaces that day's
    # attempt rather than stacking duplicates. Any earlier date stays.
    keys = {(c['source'], c['list'], c['captured']) for c in captures}
    document['captures'] = [c for c in document.get('captures', [])
                            if (c['source'], c['list'], c['captured']) not in keys] + captures
    document['captures'].sort(key=lambda c: (c['captured'], c['source'], c['list']))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(document, ensure_ascii=False, indent=1) + '\n')

    total = sum(len(c['items']) for c in captures)
    print('\n%d row(s) across %d capture(s) -> %s' % (total, len(captures), os.path.relpath(OUT, ROOT)))
    return 0


if __name__ == '__main__':
    if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    raise SystemExit(main(sys.argv[1:]))
