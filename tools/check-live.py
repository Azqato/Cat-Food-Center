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

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            for path, description in (
                    [('/product.html?barcode=%s' % code, desc) for code, desc in CASES]
                    + [('/search.html?q=chicken', 'text search for "chicken"')]):
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
                    " #results-list .text-h2, #results-label') || {}).textContent || ''")
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
            await browser.close()
    finally:
        httpd.shutdown()

    print('\n%d of %d page states OK' % (4 - len(failures), 4))
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
