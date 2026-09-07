# -*- coding: utf-8 -*-
"""Core Web Vitals, measured on a throttled browser.

    python tools/check-vitals.py            # fails the build on any breach
    python tools/check-vitals.py --report   # prints the numbers and exits 0

Loads each page in headless Edge with the CPU slowed 4x and the network held to
roughly a slow 4G connection, and reads LCP, CLS and total blocking time out of
the browser's own performance timeline.

Why the throttling is the whole point: without it every page on this site
renders in under 400ms from a loopback server, every measurement passes, and
the gate tells you nothing. The throttle is what makes a regression visible.
It is not a claim about any particular visitor's device.

What this does NOT measure:

  * Time to first byte from GitHub Pages. The pages are served from 127.0.0.1
    here, per PRD section 20: verification is local. Hosting latency is real
    and is not in these numbers.
  * INP. It needs real interaction over a real session. TBT is the standard
    lab proxy and is what is measured instead.
  * Anything about the Open Pet Food Facts API's own speed on a given day. The
    pages that wait on it are measured, but their numbers move with the
    database's mood, so they are reported and not gated. Section 19.2 of
    docs/PRD.md says which pages are gated and why.
  * Layout shift in any engine but this one. The Layout Instability API is
    Chromium-only; Gecko and WebKit expose no layout-shift entry type at all,
    as tools/check-engines.py reports. A CLS number can only be had from
    Blink, so the fix for one is taken on faith to help the others. It is a
    layout reservation rather than an engine trick, so that faith is not
    unreasonable, but it is faith.

Why not Lighthouse: it needs Node, and ADR-001 keeps this project free of npm.
Lighthouse reads the same three numbers out of the same browser timeline.
"""
import asyncio
import http.server
import os
import socketserver
import sys
import threading

EDGE_CHANNEL = 'msedge'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Google's "good" thresholds, which are the targets PRD section 14 states.
# TBT has no official threshold; 200ms is Lighthouse's own "good" boundary.
BUDGET = {'lcp': 2500.0, 'cls': 0.1, 'tbt': 200.0}

# Roughly a slow 4G connection, and a CPU four times slower than this machine.
THROTTLE_NET = {'offline': False, 'downloadThroughput': 1_600_000 // 8,
                'uploadThroughput': 750_000 // 8, 'latency': 150}
THROTTLE_CPU = 4

# gated: the page is served entirely from this repository, so its numbers are
# a property of the code and a regression is real. Not gated: the page cannot
# paint until Open Pet Food Facts answers, and that is not something a commit
# here controls. Both are measured; only the first can fail the build.
PAGES = [
    ('/', 'home', True),
    ('/search/', 'search, no query', True),
    ('/brands/', 'brand index', True),
    ('/scan/', 'scan', True),
    ('/compare/', 'compare, empty', True),
    ('/methodology/', 'methodology', True),
    ('/offline/', 'offline', True),
    ('/learn/', 'guide index', True),
    ('/learn/daily-requirements/', 'guide: the largest page', True),
    ('/learn/additives/', 'guide: additives', True),
    ('/product/?barcode=4008429158100', 'product (API)', False),
    ('/search/?q=chicken', 'search results (API)', False),
]

# Installed before the document, so the observers are watching from the first
# paint rather than from whenever the script tag runs. buffered: true would
# catch earlier entries anyway, but only for the observers that support it.
COLLECT = """
window.__cfc = { lcp: 0, cls: 0, tbt: 0, shifts: [] };
new PerformanceObserver((list) => {
  for (const e of list.getEntries()) window.__cfc.lcp = e.startTime;
}).observe({ type: 'largest-contentful-paint', buffered: true });

new PerformanceObserver((list) => {
  for (const e of list.getEntries()) {
    // Shifts the visitor caused by interacting are excluded from CLS by
    // definition. Nothing here clicks, so every shift seen is layout's own.
    if (e.hadRecentInput) continue;
    window.__cfc.cls += e.value;
    window.__cfc.shifts.push({ value: e.value,
      node: (e.sources && e.sources[0] && e.sources[0].node
             && e.sources[0].node.nodeName) || '?' });
  }
}).observe({ type: 'layout-shift', buffered: true });

new PerformanceObserver((list) => {
  for (const e of list.getEntries()) {
    // Total blocking time: everything a long task spends beyond 50ms is time
    // the main thread could not answer a tap in.
    if (e.duration > 50) window.__cfc.tbt += e.duration - 50;
  }
}).observe({ type: 'longtask', buffered: true });
"""

READ = """() => ({
  lcp: window.__cfc.lcp,
  cls: window.__cfc.cls,
  tbt: window.__cfc.tbt,
  shifts: window.__cfc.shifts.sort((a, b) => b.value - a.value).slice(0, 3),
  transferred: performance.getEntriesByType('resource')
    .reduce((n, r) => n + (r.transferSize || 0), 0)
    + (performance.getEntriesByType('navigation')[0] || {}).transferSize || 0,
  requests: performance.getEntriesByType('resource').length + 1,
})"""


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serve():
    handler = lambda *a, **kw: Quiet(*a, directory=ROOT, **kw)
    httpd = socketserver.TCPServer(('127.0.0.1', 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, httpd.server_address[1]


async def measure(browser, base, path):
    # A fresh context per page, so one page's service worker and caches cannot
    # make the next one look fast. Every number here is a cold first visit.
    context = await browser.new_context(viewport={'width': 412, 'height': 915})
    page = await context.new_page()
    client = await context.new_cdp_session(page)
    await client.send('Network.enable')
    await client.send('Network.emulateNetworkConditions', THROTTLE_NET)
    await client.send('Emulation.setCPUThrottlingRate', {'rate': THROTTLE_CPU})
    await page.add_init_script(COLLECT)

    await page.goto(base + path, wait_until='load')
    try:
        await page.wait_for_function(
            "!document.body.textContent.includes('Loading')", timeout=30000)
    except Exception:
        pass
    # LCP is not final until the page stops changing; give the observers room
    # to see a late image or a fetch-driven repaint before reading them.
    await page.wait_for_timeout(2500)
    result = await page.evaluate(READ)
    await context.close()
    return result


async def main(report_only):
    from playwright.async_api import async_playwright

    httpd, port = serve()
    base = 'http://127.0.0.1:%d' % port
    breaches = []
    rows = []

    print('CPU throttled %dx, network at roughly slow 4G, 412px viewport, '
          'cold cache.\n' % THROTTLE_CPU)
    print('%-28s %9s %7s %8s %8s %5s' % ('page', 'LCP', 'CLS', 'TBT', 'weight', 'reqs'))
    print('-' * 74)
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(channel=EDGE_CHANNEL)
            for path, label, gated in PAGES:
                m = await measure(browser, base, path)
                bad = [k for k, limit in BUDGET.items() if m[k] > limit]
                if gated and bad:
                    breaches.append((label, {k: m[k] for k in bad}))
                rows.append((label, gated, m, bad))
                mark = '' if not bad else (' FAIL' if gated else ' over (not gated)')
                print('%-28s %8.0fms %7.3f %7.0fms %7.0fkB %5d%s' % (
                    label, m['lcp'], m['cls'], m['tbt'],
                    m['transferred'] / 1024.0, m['requests'], mark))
            await browser.close()
    finally:
        httpd.shutdown()

    print('\nBudget: LCP %.0fms, CLS %.2f, TBT %.0fms'
          % (BUDGET['lcp'], BUDGET['cls'], BUDGET['tbt']))

    if report_only:
        for label, gated, m, bad in rows:
            if m['shifts']:
                print('\n%s shifted: %s' % (label, ', '.join(
                    '%s %.3f' % (s['node'], s['value']) for s in m['shifts'])))

    if breaches:
        print('\n%d page(s) over budget:' % len(breaches))
        for label, over in breaches:
            print('  %s: %s' % (label, ', '.join(
                '%s %.3f' % (k, v) for k, v in over.items())))
    else:
        print('\nEvery gated page inside budget.')

    return 0 if report_only else (1 if breaches else 0)


if __name__ == '__main__':
    sys.exit(asyncio.run(main('--report' in sys.argv)))
