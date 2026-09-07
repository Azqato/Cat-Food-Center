# -*- coding: utf-8 -*-
"""WCAG 2.1 AA audit of every page, in both themes.

    python tools/check-a11y.py            # fails the build on any violation
    python tools/check-a11y.py --report   # prints every violation and exits 0

Drives axe-core in headless Edge over all twenty pages plus the states that
only exist after a fetch (a scored product, a product with no ingredients, a
barcode that is not in the database, a page of search results). A page is
audited twice, once light and once dark, because the palette is duplicated in
cfc-tokens.css and a contrast failure can exist in one copy alone. Two checks
axe does not perform run alongside it on every page: reflow at a 320px viewport
(WCAG 1.4.10) and the skip link from a cold keyboard (2.4.1).

This is not the whole of accessibility and does not claim to be. axe-core
catches roughly a third to a half of WCAG issues, all of them machine-checkable
ones; keyboard order, focus visibility and whether alternative text is
*correct* rather than merely present are judgements no tool makes. Section 19
of docs/PRD.md records what was checked by hand alongside this.

Why not Lighthouse: it needs Node, and ADR-001 keeps this project free of npm.
axe-core is the engine Lighthouse's accessibility category wraps anyway, and it
loads from a CDN into a page Playwright already has open.
"""
import asyncio
import http.server
import os
import socketserver
import sys
import threading

EDGE_CHANNEL = 'msedge'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AXE = 'https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.2/axe.min.js'

# Every page, plus the query strings that put a page into a state it cannot
# reach on its own. The product and search pages render nothing until a fetch
# returns, so auditing them bare would audit a loading spinner.
PATHS = [
    ('/', 'home'),
    ('/search/', 'search, no query'),
    ('/search/?q=chicken', 'search results'),
    ('/search/?brand=purina%7CPurina', 'brand-filtered results'),
    ('/brands/', 'brand index'),
    ('/product/?barcode=4008429158100', 'product, fully scored'),
    ('/product/?barcode=0050000102068', 'product, no ingredients'),
    ('/product/?barcode=9999999999999', 'product, not in database'),
    ('/scan/', 'scan'),
    ('/submit/?barcode=9999999999999', 'submit'),
    ('/compare/', 'compare, empty'),
    ('/compare/?a=0064992282189&b=3596710487455', 'compare, two products'),
    ('/methodology/', 'methodology'),
    ('/offline/', 'offline'),
    ('/learn/', 'guide index'),
    ('/learn/nutrition/', 'guide: nutrition'),
    ('/learn/daily-requirements/', 'guide: daily requirements'),
    ('/learn/labels/', 'guide: labels'),
    ('/learn/food-types/', 'guide: food types'),
    ('/learn/hydration/', 'guide: hydration'),
    ('/learn/additives/', 'guide: additives'),
    ('/learn/feeding/', 'guide: feeding'),
    ('/learn/life-stages/', 'guide: life stages'),
    ('/learn/toxic/', 'guide: toxic foods'),
    ('/learn/health/', 'guide: health'),
]

# Setting the theme and running the audit are two steps with a wait between
# them, and the wait is not optional: .topbar-nav a and most of the other
# themed rules carry `transition: color 150ms`, so an audit that runs the
# instant the attribute changes measures colours part-way between the two
# palettes. The first version of this tool did exactly that and reported the
# entire top bar as a dark-mode contrast failure that does not exist.
SET_THEME = "(theme) => document.documentElement.setAttribute('data-theme', theme)"

# WCAG 2.1 A and AA only. axe ships best-practice rules too; they are worth
# reading but they are not the standard, and a gate that fails on them would be
# failing on somebody's style preference.
RUN_AXE = """
async () => {
  const results = await axe.run(document, {
    runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'] },
  });
  return results.violations.map((v) => ({
    id: v.id,
    impact: v.impact,
    help: v.help,
    nodes: v.nodes.slice(0, 4).map((n) => ({
      target: n.target.join(' '),
      summary: (n.failureSummary || '').split('\\n').filter(Boolean).slice(1).join(' '),
    })),
    count: v.nodes.length,
  }));
}
"""


# WCAG 1.4.10 Reflow: at 320 CSS pixels, content must not require scrolling in
# two directions. axe does not test this, and it is the success criterion a
# desktop-built site fails most often. Tenet 7 says mobile is the real use
# case, so a horizontal scrollbar at 320px is a product failure here, not just
# a standards one.
REFLOW = """() => ({
  docWidth: document.documentElement.scrollWidth,
  viewport: window.innerWidth,
})"""

# WCAG 2.4.1 Bypass Blocks and 2.4.7 Focus Visible. Tab once from the top of
# the document: the first stop must be the skip link, it must become visible
# when focused (it is off-screen until then), and it must point at #main.
SKIP_LINK = """() => {
  const el = document.activeElement;
  const box = el.getBoundingClientRect();
  return {
    tag: el.tagName,
    cls: el.className,
    href: el.getAttribute('href'),
    onScreen: box.top >= 0 && box.left >= 0,
    target: !!document.querySelector(el.getAttribute('href') || '#nothing'),
  };
}"""


class Quiet(http.server.SimpleHTTPRequestHandler):
    # log_message has to be overridden on the handler, not set on the server:
    # setting it on the server is silently ignored and every request is logged
    # over the report, which is the whole output of this tool.
    def log_message(self, *args):
        pass


def serve():
    handler = lambda *a, **kw: Quiet(*a, directory=ROOT, **kw)
    httpd = socketserver.TCPServer(('127.0.0.1', 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, httpd.server_address[1]


async def main(report_only):
    from playwright.async_api import async_playwright

    httpd, port = serve()
    base = 'http://127.0.0.1:%d' % port
    findings = []
    audited = 0
    failed_audits = 0

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(channel=EDGE_CHANNEL)
            # One page, reused. Opening twenty-five of them killed the browser
            # part-way through a run, and every audit after that point was
            # simply not performed, which a gate must never do quietly.
            page = await browser.new_page(viewport={'width': 1280, 'height': 900})
            for path, label in PATHS:
                await page.goto(base + path)
                # Same wait the live check uses: every page state ends by
                # replacing the placeholder.
                try:
                    await page.wait_for_function(
                        "!document.body.textContent.includes('Loading')", timeout=25000)
                except Exception:
                    pass
                await page.wait_for_timeout(800)
                await page.add_script_tag(url=AXE)

                for theme in ('light', 'dark'):
                    await page.evaluate(SET_THEME, theme)
                    await page.wait_for_timeout(400)
                    violations = await page.evaluate(RUN_AXE)
                    audited += 1
                    status = 'PASS' if not violations else 'FAIL'
                    print('%s %-28s %-6s %s' % (
                        status, label, theme,
                        'clean' if not violations
                        else ', '.join('%s (%d)' % (v['id'], v['count']) for v in violations)))
                    if violations:
                        failed_audits += 1
                    for v in violations:
                        findings.append((label, theme, v))

                await page.evaluate(SET_THEME, 'light')

                # Reflow at 320px, the narrowest viewport WCAG names.
                await page.set_viewport_size({'width': 320, 'height': 640})
                await page.wait_for_timeout(300)
                r = await page.evaluate(REFLOW)
                audited += 1
                # One pixel of slack: sub-pixel layout rounding is not a
                # two-direction scroll.
                overflow = r['docWidth'] - r['viewport'] > 1
                if overflow:
                    failed_audits += 1
                    findings.append((label, '320px', {
                        'id': 'reflow', 'impact': 'serious', 'count': 1,
                        'help': 'Content is wider than a 320px viewport (WCAG 1.4.10)',
                        'nodes': [{'target': 'document', 'summary':
                                   'scrollWidth %d for a %d viewport'
                                   % (r['docWidth'], r['viewport'])}]}))
                print('%s %-28s %-6s %s' % (
                    'FAIL' if overflow else 'PASS', label, '320px',
                    'scrollWidth %d' % r['docWidth'] if overflow else 'no sideways scroll'))

                # The skip link, from a cold keyboard.
                await page.set_viewport_size({'width': 1280, 'height': 900})
                await page.keyboard.press('Tab')
                # The skip link slides in on a transition, like everything else
                # on this site. Reading its box straight after the Tab catches
                # it part-way up and reports it as off-screen on every page.
                await page.wait_for_timeout(400)
                sk = await page.evaluate(SKIP_LINK)
                audited += 1
                bad = not (sk['tag'] == 'A' and 'skip-link' in (sk['cls'] or '')
                           and sk['onScreen'] and sk['target'])
                if bad:
                    failed_audits += 1
                    findings.append((label, 'keyboard', {
                        'id': 'skip-link', 'impact': 'serious', 'count': 1,
                        'help': 'First tab stop must be a visible skip link to #main',
                        'nodes': [{'target': sk['tag'], 'summary': repr(sk)}]}))
                print('%s %-28s %-6s %s' % (
                    'FAIL' if bad else 'PASS', label, 'kbd',
                    repr(sk) if bad else 'first tab stop is the skip link, visible, %s resolves'
                    % sk['href']))
            await page.close()
            await browser.close()
    finally:
        httpd.shutdown()

    if findings and report_only:
        print('\n' + '=' * 74)
        for label, theme, v in findings:
            print('\n%s [%s] %s: %s' % (label, theme, v['id'], v['help']))
            print('  impact: %s, %d node(s)' % (v['impact'], v['count']))
            for n in v['nodes']:
                print('  - %s' % n['target'])
                if n['summary']:
                    print('      %s' % n['summary'][:300])

    print('\n%d of %d page-theme audits clean, %d violation(s)'
          % (audited - failed_audits, audited, len(findings)))
    if report_only:
        return 0
    return 1 if findings else 0


if __name__ == '__main__':
    sys.exit(asyncio.run(main('--report' in sys.argv)))
