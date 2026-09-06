# -*- coding: utf-8 -*-
"""End-to-end check against the live Open Pet Food Facts API.

    python tools/check-live.py

Loads the real search and product pages in headless Chromium, hits the real
API, and reports what rendered. Unlike tools/run-tests.py this needs network
and is not deterministic — the database is community-maintained and moves — so
it is a smoke check, not a gate.
"""
import asyncio
import http.server
import os
import socketserver
import sys
import threading

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Barcodes observed to carry different amounts of data, so each page state gets
# exercised: a full guaranteed analysis, a record with no ingredients, and a
# barcode that is not in the database at all.
CASES = [
    ('4008429158100', 'dry food with a full guaranteed analysis'),
    ('0050000102068', 'record with no ingredients and no nutriments'),
    ('9999999999999', 'barcode not in the database'),
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

  const scanner = await import('./assets/js/scanner.js');
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

def serve():
    handler = lambda *a, **kw: http.server.SimpleHTTPRequestHandler(*a, directory=ROOT, **kw)
    httpd = socketserver.TCPServer(('127.0.0.1', 0), handler)
    httpd.log_message = lambda *a: None
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, httpd.server_address[1]


async def main():
    from playwright.async_api import async_playwright

    httpd, port = serve()
    base = 'http://127.0.0.1:%d' % port
    failures = []
    # The eight page loads below, plus the four multi-page checks after them.
    total = 8

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            paths = (
                [('/product.html?barcode=%s' % code, desc) for code, desc in CASES]
                + [('/search.html?q=chicken', 'text search for "chicken"'),
                   ('/scan.html', 'scan page with no camera available'),
                   ('/index.html', 'home page'),
                   ('/submit.html?barcode=9999999999999', 'submit page for a missing barcode'),
                   ('/compare.html?a=0064992282189&b=3596710487455',
                    'compare two fully scorable products')])
            for path, description in paths:
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

                # Scope to the content area — otherwise this reads the top bar
                # wordmark and every page looks identical.
                heading = await page.evaluate(
                    "(document.querySelector('#product-article h1, #product-article .text-h2,"
                    " #results-list .text-h2, #results-label, main h1') || {}).textContent || ''")
                sections = await page.evaluate(
                    "document.querySelectorAll('main section, #results-list li').length")
                overflow = await page.evaluate(
                    'document.documentElement.scrollWidth > document.documentElement.clientWidth')

                ok = not errors and not overflow and heading.strip()
                if not ok:
                    failures.append(path)
                print('%s %-44s %s' % ('PASS' if ok else 'FAIL', description, heading.strip()[:52]))
                print('       sections=%d overflow=%s%s'
                      % (sections, overflow, ('  ERRORS: %s' % errors) if errors else ''))
                await page.close()

            total += 1
            # The recently-viewed list is the one thing that spans two pages, so
            # it needs one context that visits a product and then goes home.
            # Headless Chromium starts with empty storage, which is exactly the
            # first-visit state the section is supposed to hide itself in.
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(base + '/index.html')
            await page.wait_for_timeout(400)
            hidden_first = await page.evaluate(
                "document.getElementById('recent-section').hidden")

            await page.goto(base + '/product.html?barcode=%s' % CASES[0][0])
            await page.wait_for_function(
                "!document.body.textContent.includes('Loading')", timeout=25000)
            await page.wait_for_timeout(600)

            await page.goto(base + '/index.html')
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
            # camera works — nothing here can — but it does prove that a correct
            # frame produces the correct barcode rather than a plausible wrong one.
            page = await browser.new_page()
            await page.goto(base + '/scan.html')
            roundtrip = await page.evaluate(DECODE_ROUNDTRIP)
            ok = all(r['matches'] and r['valid'] for r in roundtrip.values())
            if not ok:
                failures.append('decode round-trip')
            print('%s %-44s %s' % ('PASS' if ok else 'FAIL', 'barcode decode round-trip',
                                   ', '.join('%s->%s' % (k, v['decoded'][:16])
                                             for k, v in roundtrip.items())))
            await page.close()

            total += 2
            # The service worker, end to end: install it, view a product, go
            # offline, and check the same product still renders *and says it is
            # a saved copy*. The label is the part that matters — an old score
            # shown as a current one is the failure this cache could introduce.
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(base + '/index.html')
            await page.wait_for_timeout(2500)
            shell_size = await page.evaluate(
                "caches.open('cfc-shell-v1').then(c => c.keys()).then(k => k.length)")

            await page.goto(base + '/product.html?barcode=%s' % CASES[0][0])
            await page.wait_for_function(
                "!document.body.textContent.includes('Loading')", timeout=25000)
            await page.wait_for_timeout(900)
            # The shell cache must not grow per product viewed: every product is
            # the same document under a different query string.
            shell_after = await page.evaluate(
                "caches.open('cfc-shell-v1').then(c => c.keys()).then(k => k.length)")

            installed = shell_size > 10 and shell_after == shell_size
            if not installed:
                failures.append('service worker install')
            print('%s %-44s %s' % ('PASS' if installed else 'FAIL', 'service worker precaches the shell',
                                   '%d entries, unchanged after a product view=%s'
                                   % (shell_size, shell_after == shell_size)))

            await context.set_offline(True)
            await page.goto(base + '/product.html?barcode=%s' % CASES[0][0])
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
            await browser.close()
    finally:
        httpd.shutdown()

    print('\n%d of %d checks OK' % (total - len(failures), total))
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
