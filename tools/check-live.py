# -*- coding: utf-8 -*-
"""End-to-end check against the live Open Pet Food Facts API.

    python tools/check-live.py

Loads the real search and product pages in headless Edge, hits the real
API, and reports what rendered. Unlike tools/run-tests.py this needs network
and is not deterministic (the database is community-maintained and moves) so
it is a smoke check, not a gate.
"""
import asyncio
import http.server
import os
import socketserver
import sys
import threading

# Edge, never Chrome: Chrome is the maintainer's day-to-day browser and driving
# it would disturb a live session. Edge runs the same engine, is installed on
# Windows by default, and costs nothing to use. Playwright reaches it through
# the msedge channel rather than its own bundled Chromium build, so no browser
# download is needed. See docs/PRD.md, "Browser Testing".
EDGE_CHANNEL = 'msedge'

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Barcodes observed to carry different amounts of data, so each page state gets
# exercised: a full guaranteed analysis, a record with no ingredients, and a
# barcode that is not in the database at all.
# Barcode, description, and a string the rendered page can only contain if it
# genuinely worked. The third element is the M19 addition; see the note by the
# paths list below for why a non-empty heading was not enough.
#
# 4008429158100 sat in the first row until M19, described as a full guaranteed
# analysis. By then its ingredient list had been removed upstream and it
# rendered the same "no score" page as the second row, so the check exercised
# one page state twice and the scored page not at all. Nothing failed, because
# nothing asked. That is the point of the third element: a description is a
# claim about the data, and only an expectation tests it.
CASES = [
    ('3596710487455', 'wet food that scores, with its reasoning shown', 'How this score was reached'),
    ('0050000102068', 'record with no ingredients and no nutriments', 'Why there is no score'),
    ('9999999999999', 'barcode not in the database', 'Product not found'),
]


DECODE_ROUNDTRIP = r"""
async () => {
  await new Promise((res, rej) => { const s = document.createElement('script');
    s.src = 'https://cdn.jsdelivr.net/npm/@zxing/library@0.21.3/umd/index.min.js';
    s.onload = res; s.onerror = rej; document.head.appendChild(s); });

  // EAN-13 encoding tables. Drawing the bars here rather than loading a
  // fixture image keeps the check self-contained, and means the barcode under
  // test is one whose digits we chose.
  const L = ['0001101','0011001','0010011','0111101','0100011','0110001','0101111','0111011','0110111','0001011'];
  const G = ['0100111','0110011','0011011','0100001','0011101','0111001','0000101','0010001','0001001','0010111'];
  const R = L.map((s) => s.split('').map((c) => (c === '1' ? '0' : '1')).join(''));
  const P = ['LLLLLL','LLGLGG','LLGGLG','LLGGGL','LGLLGG','LGGLLG','LGGGLL','LGLGLG','LGLGGL','LGGLGL'];
  function bars(code) {
    const d = code.split('').map(Number);
    const par = P[d[0]];
    let bits = '101';
    for (let i = 1; i <= 6; i++) bits += (par[i - 1] === 'L' ? L : G)[d[i]];
    bits += '01010';
    for (let i = 7; i <= 12; i++) bits += R[d[i]];
    return bits + '101';
  }

  // Relative to the scan page, which is /scan/ since M19, so one level up.
  const scanner = await import('../assets/js/scanner.js');
  const out = {};
  for (const code of ['3596710487455', '5000159461122']) {
    const bits = bars(code), M = 3, quiet = 36;   // quiet zone, or nothing decodes
    const canvas = document.createElement('canvas');
    canvas.width = bits.length * M + quiet * 2;
    canvas.height = 180;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = '#000';
    for (let i = 0; i < bits.length; i++) if (bits[i] === '1') ctx.fillRect(quiet + i * M, 20, M, 120);

    const Z = window.ZXing;
    const reader = new Z.MultiFormatReader();
    const hints = new Map();
    hints.set(Z.DecodeHintType.POSSIBLE_FORMATS, [Z.BarcodeFormat.EAN_13, Z.BarcodeFormat.UPC_A]);
    reader.setHints(hints);
    const bitmap = new Z.BinaryBitmap(new Z.HybridBinarizer(new Z.HTMLCanvasElementLuminanceSource(canvas)));
    let text;
    try { text = reader.decode(bitmap).getText(); } catch (e) { text = 'FAILED: ' + e; }
    out[code] = { decoded: text, matches: text === code, valid: scanner.isValidBarcode(String(text)) };
  }
  return out;
}
"""

RAIL_JS = """() => ({
  hidden: document.querySelector('.toc[data-client-toc]').hidden,
  links: document.querySelectorAll('#toc-list a').length,
  headings: document.querySelectorAll('.article h2[id]').length,
  active: document.querySelectorAll('#toc-list a.is-active').length,
})"""


def serve():
    handler = lambda *a, **kw: http.server.SimpleHTTPRequestHandler(*a, directory=ROOT, **kw)
    httpd = socketserver.TCPServer(('127.0.0.1', 0), handler)
    httpd.log_message = lambda *a: None
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, httpd.server_address[1]


# Look the shell cache up by prefix rather than by full name. caches.open()
# creates an empty cache when the name is wrong, so hard-coding the version
# turned a version bump into a silent zero rather than a failure.
SHELL_COUNT_JS = (
    "caches.keys().then(ks => {"
    "  const n = ks.find(k => k.startsWith('cfc-shell-'));"
    "  return n ? caches.open(n).then(c => c.keys()).then(k => k.length) : 0;"
    "})")


async def main():
    from playwright.async_api import async_playwright

    httpd, port = serve()
    base = 'http://127.0.0.1:%d' % port
    failures = []
    # The twelve page loads below, plus the five behavioural checks after them.
    total = 12

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(channel=EDGE_CHANNEL)
            # Each page carries text it can only show if it actually worked.
            # Added in M19, after that milestone broke every score on the site
            # and this check passed all twelve pages anyway: it asked whether a
            # heading was non-empty, and "Could not load this product" is a
            # non-empty heading. The same lesson as M18, in a new place. An
            # expectation is a string the page cannot print while broken.
            paths = (
                [('/product/?barcode=%s' % code, desc, expect)
                 for code, desc, expect in CASES]
                + [('/search/?q=chicken', 'text search for "chicken"', 'can be scored'),
                   ('/scan/', 'scan page with no camera available', 'Scan a barcode'),
                   ('/', 'home page', 'Cat Food Center'),
                   ('/submit/?barcode=9999999999999', 'submit page for a missing barcode',
                    'Add a missing product'),
                   ('/compare/?a=0064992282189&b=3596710487455',
                    'compare two fully scorable products', 'Compare two foods'),
                   ('/brands/', 'brand index', 'Browse by brand'),
                   ('/search/?q=chicken&page=2', 'second page of text results', 'can be scored'),
                   ('/search/?brand=purina%7CPurina', 'brand-filtered results', 'can be scored'),
                   ('/search/?q=chicken&only=scorable',
                    'text results filtered to scorable only', 'that can be scored')])
            for path, description, expect in paths:
                page = await browser.new_page(viewport={'width': 1280, 'height': 900})
                errors = []

                def note_console(message):
                    # A 404 from the API is how an unknown barcode is detected, and
                    # the browser logs every failed request regardless of whether
                    # the page handled it. Only genuine script errors matter here.
                    if message.type == 'error' and 'Failed to load resource' not in message.text:
                        errors.append(message.text)

                page.on('console', note_console)
                page.on('pageerror', lambda e: errors.append(str(e)))

                await page.goto(base + path)
                # Every page state ends by replacing the placeholder, so wait for
                # the placeholder to go rather than for a fixed timeout.
                try:
                    await page.wait_for_function(
                        "!document.body.textContent.includes('Loading')", timeout=25000)
                except Exception:
                    pass
                await page.wait_for_timeout(1200)

                # Scope to the content area - otherwise this reads the top bar
                # wordmark and every page looks identical. The first *non-empty*
                # match wins rather than the first match: the search page now
                # carries an h1 that stays empty unless the results are a brand,
                # and querySelector would return that empty element and report a
                # working page as a failure.
                heading = await page.evaluate(
                    "[...document.querySelectorAll('#product-article h1, #product-article .text-h2,"
                    " #results-list .text-h2, main h1, #results-label')]"
                    ".map(el => (el.textContent || '').trim()).find(Boolean) || ''")
                sections = await page.evaluate(
                    "document.querySelectorAll('main section, #results-list li').length")
                overflow = await page.evaluate(
                    'document.documentElement.scrollWidth > document.documentElement.clientWidth')

                body = await page.evaluate(
                    "document.querySelector('main').textContent || ''")
                found = expect in body

                ok = not errors and not overflow and heading.strip() and found
                if not ok:
                    failures.append(path)
                print('%s %-44s %s' % ('PASS' if ok else 'FAIL', description, heading.strip()[:52]))
                print('       sections=%d overflow=%s expected=%s%s'
                      % (sections, overflow, 'yes' if found else 'NO (%r)' % expect,
                         ('  ERRORS: %s' % errors) if errors else ''))
                await page.close()

            total += 2
            # Does the search actually search? Nothing asked this until M18, and
            # for eleven milestones the answer was no: /api/v2/search accepted
            # search_terms, answered 200, and returned the entire cat-food
            # category whatever was typed. Every check here passed over it,
            # because every check asked whether results came back.
            #
            # Two assertions, and the first is the one that matters. A query
            # that cannot match anything must return nothing: it is the only
            # question whose right answer an ignored parameter cannot fake.
            page = await browser.new_page(viewport={'width': 1280, 'height': 900})
            await page.goto(base + '/search/?q=zzzzqqqxyw')
            await page.wait_for_function(
                "!document.body.textContent.includes('Loading')", timeout=25000)
            await page.wait_for_timeout(1000)
            # Counted by [data-scorable], not by li: the "No matches" panel is
            # itself an li, so a list item count of zero is not what an empty
            # result looks like here.
            nonsense = await page.evaluate(
                "({ cards: document.querySelectorAll('#results-list [data-scorable]').length,"
                "   body: (document.querySelector('main').textContent || '') })")
            ok = nonsense['cards'] == 0 and 'No matches' in nonsense['body']
            if not ok:
                failures.append('impossible query returns nothing')
            print('%s %-44s %s' % ('PASS' if ok else 'FAIL', 'a query that cannot match returns nothing',
                                   '%d cards' % nonsense['cards']))

            # And the second: a real query's results must be about the query.
            # Not every card will say "salmon" in its name, because the database
            # matches ingredients and descriptions too, so this asks for a
            # majority rather than for all of them. A result set that ignores
            # the query lands nowhere near half.
            await page.goto(base + '/search/?q=salmon')
            await page.wait_for_function(
                "!document.body.textContent.includes('Loading')", timeout=25000)
            await page.wait_for_timeout(1000)
            hits = await page.evaluate(
                "[...document.querySelectorAll('#results-list [data-scorable]')]"
                ".map(el => (el.textContent || '').toLowerCase())")
            matching = len([t for t in hits if 'salmon' in t])
            ok = bool(hits) and matching * 2 > len(hits)
            if not ok:
                failures.append('results are about the query')
            print('%s %-44s %s' % ('PASS' if ok else 'FAIL', 'results are about what was typed',
                                   '%d of %d cards mention salmon' % (matching, len(hits))))
            # M18b: the caveat has to travel with the number. Every card that
            # prints a score prints its confidence beside it, so a score read
            # in a list makes the same claim as the same score read on the
            # product page. Asserted on the search cards because they are the
            # surface that leaked: the product and compare pages have stated
            # confidence since M7 and M11 respectively.
            total += 1
            scored = await page.evaluate(
                "[...document.querySelectorAll('#results-list [data-scorable=\"yes\"]')]"
                ".map(el => (el.textContent || ''))")
            with_conf = len([t for t in scored if 'confidence' in t])
            ok = bool(scored) and with_conf == len(scored)
            if not ok:
                failures.append('confidence travels with the score')
            print('%s %-44s %s' % ('PASS' if ok else 'FAIL', 'every scored card states its confidence',
                                   '%d of %d scored cards' % (with_conf, len(scored))))
            await page.close()

            total += 1
            # The recently-viewed list is the one thing that spans two pages, so
            # it needs one context that visits a product and then goes home.
            # Headless Edge starts with empty storage, which is exactly the
            # first-visit state the section is supposed to hide itself in.
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(base + '/')
            await page.wait_for_timeout(400)
            hidden_first = await page.evaluate(
                "document.getElementById('recent-section').hidden")

            await page.goto(base + '/product/?barcode=%s' % CASES[0][0])
            await page.wait_for_function(
                "!document.body.textContent.includes('Loading')", timeout=25000)
            await page.wait_for_timeout(600)

            await page.goto(base + '/')
            await page.wait_for_timeout(600)
            shown_after = await page.evaluate(
                "!document.getElementById('recent-section').hidden"
                " && document.querySelectorAll('#recent-list li').length === 1")
            await context.close()

            ok = hidden_first and shown_after
            if not ok:
                failures.append('recently viewed')
            print('%s %-44s %s' % ('PASS' if ok else 'FAIL', 'recently viewed records a real visit',
                                   'hidden when empty=%s, shows after a visit=%s'
                                   % (hidden_first, shown_after)))
            total += 1
            # The decoder is the one part of scanning that a headless browser can
            # genuinely exercise: draw a known EAN-13, decode it back, and check
            # our own validator agrees with the result. It does not prove the
            # camera works - nothing here can - but it does prove that a correct
            # frame produces the correct barcode rather than a plausible wrong one.
            page = await browser.new_page()
            await page.goto(base + '/scan/')
            roundtrip = await page.evaluate(DECODE_ROUNDTRIP)
            ok = all(r['matches'] and r['valid'] for r in roundtrip.values())
            if not ok:
                failures.append('decode round-trip')
            print('%s %-44s %s' % ('PASS' if ok else 'FAIL', 'barcode decode round-trip',
                                   ', '.join('%s->%s' % (k, v['decoded'][:16])
                                             for k, v in roundtrip.items())))
            await page.close()

            total += 1
            # The product page is the only one whose "On this page" rail is not
            # in the HTML: the generator has no headings to index until the
            # fetch returns, so cfc-docs.js builds the list from the DOM. That
            # makes it the one rail that can silently ship empty.
            page = await browser.new_page()
            await page.goto(base + '/product/?barcode=%s' % CASES[0][0])
            await page.wait_for_function(
                "!document.body.textContent.includes('Loading')", timeout=25000)
            await page.wait_for_timeout(600)
            rail = await page.evaluate(RAIL_JS)
            ok = (rail['links'] > 0 and rail['links'] == rail['headings']
                  and not rail['hidden'] and rail['active'] == 1)
            if not ok:
                failures.append('product page rail')
            print('%s %-44s %s' % ('PASS' if ok else 'FAIL', 'product page builds its own toc rail',
                                   '%d links for %d headings, %d active'
                                   % (rail['links'], rail['headings'], rail['active'])))
            await page.close()

            total += 2
            # The service worker, end to end: install it, view a product, go
            # offline, and check the same product still renders *and says it is
            # a saved copy*. The label is the part that matters - an old score
            # shown as a current one is the failure this cache could introduce.
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(base + '/')
            await page.wait_for_timeout(2500)
            shell_size = await page.evaluate(
                SHELL_COUNT_JS)

            await page.goto(base + '/product/?barcode=%s' % CASES[0][0])
            await page.wait_for_function(
                "!document.body.textContent.includes('Loading')", timeout=25000)
            await page.wait_for_timeout(900)
            # The shell cache must not grow per product viewed: every product is
            # the same document under a different query string.
            shell_after = await page.evaluate(
                SHELL_COUNT_JS)

            installed = shell_size > 10 and shell_after == shell_size
            if not installed:
                failures.append('service worker install')
            print('%s %-44s %s' % ('PASS' if installed else 'FAIL', 'service worker precaches the shell',
                                   '%d entries, unchanged after a product view=%s'
                                   % (shell_size, shell_after == shell_size)))

            await context.set_offline(True)
            await page.goto(base + '/product/?barcode=%s' % CASES[0][0])
            await page.wait_for_function(
                "!document.body.textContent.includes('Loading')", timeout=25000)
            await page.wait_for_timeout(1000)
            body = await page.inner_text('#product-article')
            unknown_title = ''
            offline_ok = 'saved copy' in body and len(body) > 200
            if offline_ok:
                await page.goto(base + '/never-visited.html')
                await page.wait_for_timeout(700)
                unknown_title = await page.title()
                offline_ok = 'Offline' in unknown_title
            if not offline_ok:
                failures.append('offline behaviour')
            print('%s %-44s %s' % ('PASS' if offline_ok else 'FAIL', 'offline: cached product, labelled',
                                   'unvisited page falls back to "%s"' % unknown_title))
            await context.close()

            total += 1
            # Scope.
            #
            # A worker controls its own directory and everything below it, and
            # nothing above. Registering the wrong path is therefore not an
            # error: it succeeds, and offline support silently narrows to one
            # subtree with nothing logged anywhere. Before M19 every page sat at
            # the root, so any relative path was the root and this could not go
            # wrong; nothing checked it because nothing could. Now /search/ is a
            # directory, './sw.js' from there would mean /search/sw.js, and the
            # difference between that and working correctly is invisible until
            # somebody is offline.
            #
            # Registration happens from /search/ rather than from the deepest
            # page on the site because the guide pages do not load pwa.js at
            # all; see the note in that file. /search/ is the deepest page that
            # registers, and one level is all it takes for a relative path to be
            # wrong.
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(base + '/search/')
            scope = await page.evaluate(
                "navigator.serviceWorker.ready.then((r) => r.scope)")
            # Registered from a subdirectory, controlling the root: the half
            # that a scope-narrowed worker would fail.
            await page.goto(base + '/')
            await page.wait_for_timeout(600)
            controlled = await page.evaluate("!!navigator.serviceWorker.controller")
            scope_ok = scope == base + '/' and controlled
            if not scope_ok:
                failures.append('service worker scope')
            print('%s %-44s %s' % ('PASS' if scope_ok else 'FAIL',
                                   'service worker scope is the whole site',
                                   'registered from /search/ with scope %s, home controlled=%s'
                                   % (scope, controlled)))
            await context.close()
            await browser.close()
    finally:
        httpd.shutdown()

    print('\n%d of %d checks OK' % (total - len(failures), total))
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
