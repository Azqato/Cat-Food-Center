# -*- coding: utf-8 -*-
"""Run tools/tests.html headlessly and report the result.

    python tools/run-tests.py

The suite itself lives in the browser (there is no Node.js in this project and
no build step (see docs/PRD.md section 16.2). This script serves the)
repository, loads tools/tests.html in headless Edge, and reads back
window.__testResults. Exits non-zero if anything failed.
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


def serve():
    """Serve the repo on an ephemeral port. ES modules need a real origin."""
    handler = lambda *a, **kw: http.server.SimpleHTTPRequestHandler(*a, directory=ROOT, **kw)
    httpd = socketserver.TCPServer(('127.0.0.1', 0), handler)
    httpd.log_message = lambda *a: None
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, httpd.server_address[1]


async def main():
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print('Playwright is not installed. Open tools/tests.html in a browser instead:')
        print('  python -m http.server 8000   →   http://localhost:8000/tools/tests.html')
        return 2

    httpd, port = serve()
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(channel=EDGE_CHANNEL)
            page = await browser.new_page()
            errors = []
            page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
            page.on('pageerror', lambda e: errors.append(str(e)))

            await page.goto('http://127.0.0.1:%d/tools/tests.html' % port)
            try:
                await page.wait_for_function('window.__testResults', timeout=15000)
            except Exception:
                print('The suite never finished. Console output:')
                for e in errors:
                    print('  ' + e)
                await browser.close()
                return 1

            results = await page.evaluate('window.__testResults')
            await browser.close()
    finally:
        httpd.shutdown()

    for failure in results['failures']:
        print('FAIL  ' + failure)
    if errors:
        print('\nConsole errors:')
        for e in errors:
            print('  ' + e)

    print('\n%d passing, %d failing' % (results['passed'], results['failed']))
    return 1 if (results['failed'] or errors) else 0


if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
