# -*- coding: utf-8 -*-
"""Index Purina's own site, so a top-100 name can find its label deck.

    python tools/purina-index.py --crawl
    python tools/purina-index.py --decks
    python tools/purina-index.py --find "Fancy Feast Gravy Lovers"

Forty-seven of the hundred products in `tools/data/top-skus.json` are Nestle
Purina brands: Fancy Feast, Friskies, Purina ONE, Cat Chow and Pro Plan. That
is nearly half the coverage target sitting behind one manufacturer, and
`tools/label-deck.py` already reads that manufacturer's published panel. The
missing piece was never the parser. It was the URL: the label decks live under
purina.com/sites/default/files with opaque filenames like
`4762-a476220-pro-plan-hairball-chicken-entree-cat-food.pdf`, which cannot be
guessed from a product name and which no search engine has indexed. This walks
the site to build the mapping the guessing could not.

**purina.com wants a user agent, and that is the whole of it.** A plain urllib
request for any page returns 403, and so does Playwright driving Edge when the
context leaves the user agent at its default. Setting one explicitly gets 200
and the full document, headless, every time. It is not headless against headed:
that was the first reading here and it was wrong, because the headful run that
appeared to prove it differed in the user agent too. The file store under
/sites/default/files is the exception that made the earlier work possible at
all: it serves PDFs to anything, which is why tools/label-deck.py needs no
browser and this one does. Section 12.14 records both the measurement and the
correction.

**So this runs headless, like the test gate**, and opens no window. It is a
maintenance tool: nothing a visitor loads runs it, the site does not depend on
it, and it needs only Playwright and the Edge channel that section 19 already
requires, so it adds no dependency the project did not have.

**It proposes and a person decides**, which is section 12.10's rule. Matching
"Purina Fancy Feast Gravy Lovers Wet Cat Food, 3 oz Cans, 30-Pack" to a slug on
purina.com is an identification, and a wrong one attaches the wrong panel to
the right product exactly as a wrong barcode does, invisibly and past every
gate. `--find` prints ranked candidates with their titles. It never writes a
catalogue entry, and neither does anything else here.
"""
import argparse
import io
import json
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKUS = os.path.join(ROOT, 'tools', 'data', 'top-skus.json')
OUT = os.path.join(ROOT, 'tools', 'data', 'purina-index.json')

BASE = 'https://www.purina.com'
# Any stated user agent is served. This is the Edge the test gate drives,
# named honestly rather than disguised as something else.
UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0')
# The cat food categories. Wet and dry are the two that partition the range;
# the others (indoor, kitten, senior, natural) are filtered views of the same
# products and are crawled only because a product occasionally sits in one and
# not in the pair, at the cost of a few repeated pages.
CATEGORIES = [
    '/cats/cat-food/wet',
    '/cats/cat-food/dry',
    '/cats/cat-food/kitten-food',
    '/cats/cat-food/indoor',
    '/cats/cat-food/senior',
    '/cats/cat-food/natural',
]
# Listings run to about forty pages each. This is a stop, not an expectation:
# the crawl ends when the listing stops producing rows.
MAX_PAGES = 60
# How many consecutive pages may add no new product before a category is
# considered done. It is not one, and the reason is a bug this tool shipped
# with for an hour: a resumed crawl re-reads page 1, every product on it is
# already known, and "nothing new" ended the category before it began. A page
# that adds nothing is normal; several in a row means the listing is repeating.
STALE_PAGES = 4
# Politeness. Nothing here is urgent and the whole crawl is a few minutes
# either way, so there is no reason to lean on somebody else's server.
PAUSE = 2.0
SETTLE = 5000

DECK = re.compile(
    r'https?://[^"\'\\\s<>]*product-label-deck-file[^"\'\\\s<>]*\.pdf')

# Anchor text on a listing card is the product name. Some anchors on the card
# are the image or the button and carry no text, which is why a slug is only
# recorded once something has named it.
LISTING_JS = """() => {
  const out = [];
  document.querySelectorAll('a[href*="/cats/shop/"]').forEach(a => {
    const href = a.getAttribute('href') || '';
    const text = (a.innerText || '').trim().replace(/\\s+/g, ' ');
    if (href && text) out.push([href.split('?')[0], text.slice(0, 120)]);
  });
  return out;
}"""

# Words that say how a thing is packed rather than what it is. Matching a
# retail listing title against a manufacturer product name fails on these
# almost every time: the retailer says "30-Pack, 3 oz Cans" and the
# manufacturer says nothing at all about the case.
NOISE = re.compile(
    r'\b(?:wet|dry|cat|cats|food|kitten|adult|can|cans|pouch|pouches|bag|bags|'
    r'tub|tubs|tray|trays|count|ct|pk|pack|packs|variety|multipack|oz|ounce|lb|'
    r'lbs|pound|pounds|with|and|for|the|in|of|made|no|artificial|color|colors|'
    r'colour|colours|preservative|preservatives|natural|premium|recipe|formula|'
    r'flavor|flavors|flavour|flavours|value|size|each|entree|entrees|classic|'
    r'gourmet|savory|real|grain|free)\b',
    re.I)


def words(text):
    """The words that carry identity, lowercased."""
    text = re.split(r'[|]', text or '')[0]
    text = NOISE.sub(' ', text)
    return set(w for w in re.findall(r"[a-z0-9']+", text.lower()) if len(w) > 2)


def score(listing_title, purina_title):
    """How much of the manufacturer's name the retail listing accounts for.

    Deliberately not a similarity: the retail title is long and full of pack
    words, the manufacturer title is short, and what matters is whether the
    short one is contained in the long one. A symmetric measure punishes the
    right answer for the retailer's verbosity.
    """
    a, b = words(listing_title), words(purina_title)
    if not b:
        return 0.0
    return len(a & b) / float(len(b))


def load():
    if not os.path.exists(OUT):
        return {'products': {}}
    try:
        return json.loads(io.open(OUT, encoding='utf-8').read())
    except ValueError:
        return {'products': {}}


def save(data):
    data['_readme'] = [
        'Purina product slugs, titles and label-deck URLs, from tools/purina-index.py.',
        '',
        'The deck URL is a manufacturer-published panel and is a source in the sense of',
        'PRD section 16.5a. The mapping from a top-100 listing to a slug is NOT settled',
        'here: --find ranks candidates and a person chooses, because a wrong match',
        'attaches the wrong panel to the right product and no gate downstream sees it.',
    ]
    data['measured'] = time.strftime('%Y-%m-%d')
    io.open(OUT, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(data, ensure_ascii=False, indent=1, sort_keys=True) + '\n')


def browser(playwright):
    """Headless, with a user agent, which is the part that matters."""
    engine = playwright.chromium.launch(channel='msedge', headless=True)
    return engine, engine.new_context(
        user_agent=UA, locale='en-US', viewport={'width': 1440, 'height': 900})


def settle(page):
    """Let the page finish arriving.

    The deck link sits well down the document. Scrolling is cheap insurance
    against a component that renders when it comes into view, and costs a few
    seconds on a crawl that is already paced for politeness.
    """
    page.wait_for_timeout(SETTLE)
    for _ in range(6):
        page.mouse.wheel(0, 1500)
        page.wait_for_timeout(500)
    page.wait_for_timeout(1500)


def crawl(limit_pages):
    from playwright.sync_api import sync_playwright

    data = load()
    products = data.setdefault('products', {})
    started = len(products)
    with sync_playwright() as playwright:
        engine, context = browser(playwright)
        page = context.new_page()
        for category in CATEGORIES:
            stale = 0
            for number in range(1, (limit_pages or MAX_PAGES) + 1):
                url = BASE + category + ('' if number == 1 else '?page=%d' % number)
                try:
                    response = page.goto(url, timeout=60000, wait_until='domcontentloaded')
                    page.wait_for_timeout(SETTLE)
                    rows = page.evaluate(LISTING_JS)
                except Exception as err:
                    print('  %-46s ERR %s' % (url[-46:], str(err)[:60]))
                    break
                status = response.status if response else 0
                fresh = 0
                for href, title in rows:
                    slug = href.rsplit('/', 1)[-1]
                    if slug not in products:
                        products[slug] = {'path': href, 'title': title, 'deck': None}
                        fresh += 1
                    elif not products[slug].get('title'):
                        products[slug]['title'] = title
                print('  %-46s %s  %2d rows, %d new' % (url[-46:], status, len(rows), fresh))
                save(data)
                if not rows:
                    # The pagination has run out. Nothing ambiguous about it.
                    break
                stale = 0 if fresh else stale + 1
                if stale >= STALE_PAGES:
                    # Several pages running have added nothing, so the listing
                    # is repeating itself rather than advancing.
                    print('  %s: %d pages with nothing new, moving on.'
                          % (category, stale))
                    break
                time.sleep(PAUSE)
        engine.close()
    print('')
    print('%d products indexed, %d new this run.' % (len(products), len(products) - started))
    return 0


def decks(limit):
    from playwright.sync_api import sync_playwright

    data = load()
    products = data.get('products') or {}
    todo = [slug for slug in sorted(products) if not products[slug].get('deck')]
    if limit:
        todo = todo[:limit]
    if not todo:
        print('Every indexed product already has a deck URL, or none are indexed.')
        return 0
    print('%d product page(s) to read, about %.0f minutes.'
          % (len(todo), len(todo) * (PAUSE + SETTLE / 1000.0) / 60.0))
    found = 0
    with sync_playwright() as playwright:
        engine, context = browser(playwright)
        page = context.new_page()
        for slug in todo:
            url = BASE + products[slug]['path']
            try:
                page.goto(url, timeout=60000, wait_until='domcontentloaded')
                settle(page)
                html = page.content()
            except Exception as err:
                print('  %-52s ERR %s' % (slug[-52:], str(err)[:50]))
                continue
            hits = sorted(set(DECK.findall(html)))
            # More than one deck on a page would mean the page covers more
            # than one product, and choosing between them is not this tool's
            # business. Record none and let a person look.
            products[slug]['deck'] = hits[0] if len(hits) == 1 else None
            products[slug]['deckCount'] = len(hits)
            found += 1 if len(hits) == 1 else 0
            print('  %-52s %d deck(s)' % (slug[-52:], len(hits)))
            save(data)
            time.sleep(PAUSE)
        engine.close()
    print('')
    print('%d of %d read pages carried exactly one deck.' % (found, len(todo)))
    return 0


def find(query, top=6):
    data = load()
    products = data.get('products') or {}
    if not products:
        raise SystemExit('Nothing indexed yet. Run --crawl first.')
    ranked = sorted(
        ((score(query, row.get('title') or ''), slug) for slug, row in products.items()),
        reverse=True)
    print('%s' % query[:100])
    for value, slug in ranked[:top]:
        if value <= 0:
            break
        row = products[slug]
        print('  %.2f  %s' % (value, (row.get('title') or slug)[:88]))
        print('        %s%s' % (BASE, row.get('path')))
        if row.get('deck'):
            print('        %s' % row['deck'])
    print('')
    print('Candidates, not an identification. Read the title against the product.')
    return 0


def report():
    """How much of the top 100 this index can reach, and how much it cannot."""
    data = load()
    products = data.get('products') or {}
    skus = json.loads(io.open(SKUS, encoding='utf-8').read())
    items = skus['captures'][0]['items']
    strong, weak, none = [], [], []
    for item in items:
        best = max(
            ((score(item['title'], row.get('title') or ''), slug)
             for slug, row in products.items()),
            default=(0.0, None))
        (strong if best[0] >= 0.75 else weak if best[0] >= 0.4 else none).append(
            (best[0], item, best[1]))
    print('%d products indexed, %d with a deck URL.'
          % (len(products), sum(1 for r in products.values() if r.get('deck'))))
    print('Against the top 100: %d strong (>=0.75), %d worth reading (>=0.4), %d nothing.'
          % (len(strong), len(weak), len(none)))
    print('')
    print('A strong score is still a proposal. Nothing here has been chosen.')
    return 0


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--crawl', action='store_true')
    parser.add_argument('--decks', action='store_true')
    parser.add_argument('--find')
    parser.add_argument('--report', action='store_true')
    parser.add_argument('--limit', type=int, default=0)
    args = parser.parse_args(argv)

    if args.find:
        return find(args.find)
    if args.crawl:
        return crawl(args.limit)
    if args.decks:
        return decks(args.limit)
    if args.report:
        return report()
    parser.print_help()
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
