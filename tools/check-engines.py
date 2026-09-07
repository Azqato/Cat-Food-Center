# -*- coding: utf-8 -*-
"""The site in all three browser engines: Blink, Gecko and WebKit.

    python tools/check-engines.py

Every other tool in this directory drives one engine. This one exists because
tenet 7 says mobile is the real use case, and every browser on iOS runs WebKit
whatever its name is. Until this was written, nothing in the project had ever
loaded a page in WebKit or Gecko, which made "works on iPhone" an assumption
rather than a finding. That gap was PRD open question 7.

Three things run per engine:

  1. The unit suite from tests.html. It is the same 178 assertions the Edge
     gate runs, and the point is not that the logic might differ but that it
     is cheap to prove it does not.
  2. Every page state, checked for its expected content, for script errors,
     and for horizontal overflow at 1280px and at 320px.
  3. The barcode decode round-trip: an EAN-13 drawn onto a canvas here and
     decoded back. This matters most of the three, because `BarcodeDetector`
     does not exist in Gecko or WebKit, so the ZXing fallback is not a
     fallback there. It is the only path scanning has.

It also prints a feature-support matrix, so the differences between the
engines are recorded rather than assumed.

Two entries in that matrix need reading carefully, because neither is a
statement about the shipping browser:

  * `getUserMedia=NO` under WebKit is a property of the headless build, not of
    Safari. Safari has had it for years. What it means here is that this tool
    cannot exercise the camera path in WebKit, only the no-camera path, and the
    no-camera path is what it checks.
  * `layout-shift=NO` under Gecko and WebKit is real: the Layout Instability
    API is Chromium-only. That is why check-vitals.py measures in one engine.

**Engine choice, and the rule in PRD section 19.** That rule says drive Edge
and never Chrome, because Chrome is the maintainer's day-to-day browser and
driving it would disturb a live session. The same reasoning permits Firefox
here: Playwright's Gecko and WebKit builds are its own, downloaded into its
cache, and are not the browsers the maintainer uses. Nothing here touches an
installed Firefox. Run `python -m playwright install webkit firefox` once.

Needs network: the pages call Open Pet Food Facts and the decode test fetches
ZXing from a CDN. Like check-live.py this is a smoke check, not a gate on the
database's contents, but the engine differences it reports are deterministic.
"""
import asyncio
import http.server
import os
import socketserver
import sys
import threading

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EDGE_CHANNEL = 'msedge'

# Expected text rather than "a heading rendered". Two pages have no heading to
# find: the search page's h1 stays empty unless the results are a brand, and a
# missing product renders a card rather than a section.
PAGES = [
    ('/index.html', 'home', 'The Cat Care Guide'),
    ('/search.html?q=chicken', 'search results', 'can be scored'),
    ('/brands.html', 'brand index', 'Browse by brand'),
    ('/product.html?barcode=4008429158100', 'product, scored', 'Ingredients'),
    ('/product.html?barcode=0050000102068', 'product, thin record', 'Nutrition'),
    ('/product.html?barcode=9999999999999', 'product, not found', 'Product not found'),
    ('/scan.html', 'scan', 'Scan a barcode'),
    ('/submit.html?barcode=9999999999999', 'submit', 'Add a missing product'),
    ('/compare.html?a=0064992282189&b=3596710487455', 'compare', 'Compare two foods'),
    ('/methodology.html', 'methodology', 'Methodology'),
    ('/offline.html', 'offline', 'You are offline'),
    ('/learn-nutrition.html', 'guide page', 'Feline nutrition fundamentals'),
]

FEATURES = """() => ({
  BarcodeDetector: 'BarcodeDetector' in window,
  serviceWorker: 'serviceWorker' in navigator,
  IntersectionObserver: 'IntersectionObserver' in window,
  getUserMedia: !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia),
  'layout-shift': (() => { try {
      return PerformanceObserver.supportedEntryTypes.includes('layout-shift');
    } catch (e) { return false; } })(),
  'largest-contentful-paint': (() => { try {
      return PerformanceObserver.supportedEntryTypes.includes('largest-contentful-paint');
    } catch (e) { return false; } })(),
  ':has()': (() => { try { return CSS.supports('selector(:has(a))'); } catch (e) { return false; } })(),
  'CSS nesting': (() => { try { return CSS.supports('selector(&)'); } catch (e) { return false; } })(),
})"""

STATE = """() => ({
  text: (document.querySelector('.article') || document.body).innerText,
  scrollWidth: document.documentElement.scrollWidth,
  viewport: window.innerWidth,
})"""

# Draws a known EAN-13 and decodes it back. Lifted from check-live.py, which
# runs it in one engine; the whole point here is the other two.
DECODE = r"""
async () => {
  await new Promise((res, rej) => { const s = document.createElement('script');
    s.src = 'https://cdn.jsdelivr.net/npm/@zxing/library@0.21.3/umd/index.min.js';
    s.onload = res; s.onerror = rej; document.head.appendChild(s); });

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
    const bits = bars(code), M = 3, quiet = 36;
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


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serve():
    handler = lambda *a, **kw: Quiet(*a, directory=ROOT, **kw)
    httpd = socketserver.TCPServer(('127.0.0.1', 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, httpd.server_address[1]


def engines(p):
    """Blink through Edge (never Chrome, section 19), then Playwright's own
    Gecko and WebKit builds."""
    return [
        ('Blink (Edge)', lambda: p.chromium.launch(channel=EDGE_CHANNEL)),
        ('Gecko (Firefox)', lambda: p.firefox.launch()),
        ('WebKit (Safari)', lambda: p.webkit.launch()),
    ]


def ignorable(text):
    """Console noise that is not a defect in this site.

    A 404 from the API is how an unknown barcode is detected. A corrupt image
    is a real file in the community database and is exactly what thumb.js's
    fallback exists for, so seeing it proves the handler works rather than
    that something broke."""
    lowered = text.lower()
    return ('failed to load resource' in lowered
            or 'status of 404' in lowered
            or 'image corrupt or truncated' in lowered
            or 'ns_error_' in lowered)


async def run_engine(p, name, launch, base, failures):
    browser = await launch()
    print('\n%s' % name)
    print('-' * 74)

    page = await browser.new_page(viewport={'width': 1280, 'height': 900})

    await page.goto(base + '/index.html')
    features = await page.evaluate(FEATURES)
    print('  features: %s' % ', '.join(
        '%s=%s' % (k, 'yes' if v else 'NO') for k, v in features.items()))

    # 1. The unit suite.
    errors = []
    page.on('console', lambda m: errors.append(m.text)
            if m.type == 'error' and not ignorable(m.text) else None)
    page.on('pageerror', lambda e: errors.append(str(e)))
    await page.goto(base + '/tests.html')
    try:
        await page.wait_for_function('window.__testResults', timeout=30000)
        results = await page.evaluate('window.__testResults')
        ok = results['failed'] == 0
        print('  %s unit suite: %d passing, %d failing'
              % ('PASS' if ok else 'FAIL', results['passed'], results['failed']))
        if not ok:
            failures.append('%s: unit suite' % name)
            for f in results['failures'][:6]:
                print('        %s' % f)
    except Exception:
        print('  FAIL unit suite never finished')
        failures.append('%s: unit suite did not finish' % name)

    # 2. Every page state, at both widths.
    for path, label, expected in PAGES:
        errors.clear()
        await page.set_viewport_size({'width': 1280, 'height': 900})
        await page.goto(base + path)
        try:
            await page.wait_for_function(
                "!document.body.textContent.includes('Loading')", timeout=30000)
        except Exception:
            pass
        # The API-backed pages settle late, and a wait that is too short
        # reports a slow database as a broken engine.
        await page.wait_for_timeout(1800)
        wide = await page.evaluate(STATE)

        await page.set_viewport_size({'width': 320, 'height': 640})
        await page.wait_for_timeout(400)
        narrow = await page.evaluate(STATE)

        rendered = expected in wide['text']
        # One pixel of slack: sub-pixel rounding is not a two-direction scroll.
        overflow = [w for w in (wide, narrow) if w['scrollWidth'] - w['viewport'] > 1]
        bad = (not rendered) or overflow or errors
        if bad:
            failures.append('%s: %s' % (name, label))
        note = 'ok'
        if not rendered:
            note = 'expected %r not on the page' % expected
        elif overflow:
            note = 'overflows at %s' % ', '.join(
                '%dpx (scrollWidth %d)' % (w['viewport'], w['scrollWidth']) for w in overflow)
        elif errors:
            note = errors[0][:90]
        print('  %s %-22s %s' % ('FAIL' if bad else 'PASS', label, note))

    # 3. The decode round-trip. In two of the three engines this is not a
    #    fallback path, it is the only one.
    await page.goto(base + '/scan.html')
    try:
        decoded = await page.evaluate(DECODE)
        ok = all(r['matches'] and r['valid'] for r in decoded.values())
    except Exception as err:
        decoded, ok = {}, False
        print('        %s' % str(err).splitlines()[0][:120])
    if not ok:
        failures.append('%s: barcode decode' % name)
    print('  %s barcode decode%s   %s' % (
        'PASS' if ok else 'FAIL',
        '' if features['BarcodeDetector'] else ' (ZXing is the only path here)',
        ', '.join('%s->%s' % (k, v['decoded'][:16]) for k, v in decoded.items())))

    await page.close()
    await browser.close()


async def main():
    from playwright.async_api import async_playwright

    httpd, port = serve()
    base = 'http://127.0.0.1:%d' % port
    failures = []
    try:
        async with async_playwright() as p:
            for name, launch in engines(p):
                try:
                    await run_engine(p, name, launch, base, failures)
                except Exception as err:
                    line = str(err).splitlines()[0]
                    if "Executable doesn't exist" in str(err):
                        print('\n%s\n  SKIP not installed. '
                              'Run: python -m playwright install webkit firefox' % name)
                        failures.append('%s: not installed' % name)
                    else:
                        print('\n%s\n  FAIL %s' % (name, line[:140]))
                        failures.append('%s: %s' % (name, line[:60]))
    finally:
        httpd.shutdown()

    print('\n' + '=' * 74)
    if failures:
        print('%d check(s) failed:' % len(failures))
        for f in failures:
            print('  %s' % f)
        return 1
    print('All three engines agree.')
    return 0


if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
