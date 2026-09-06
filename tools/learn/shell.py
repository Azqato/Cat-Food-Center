# -*- coding: utf-8 -*-
"""Static generator for the Cat Food Center Learn section.

Emits fully self-contained HTML files (no build step needed to deploy) that all
share one documentation shell: fixed top bar, sidebar, article, on-this-page
rail, prev/next, and site footer.
"""
import io
import os
import re
import sys

# The site chrome is shared with the application pages so the two families
# cannot drift apart: one navigation list, one footer, one top bar (M14).
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), 'site'))
import chrome  # noqa: E402

# Repository root, two levels up from tools/learn/.
OUT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PAW = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
       '<circle cx="6.6" cy="9.2" r="2.05"/><circle cx="11.2" cy="6.6" r="2.15"/>'
       '<circle cx="16.1" cy="7.6" r="2.05"/><circle cx="19.6" cy="11.6" r="1.85"/>'
       '<path d="M11.6 11.9c3.1 0 5.6 2.5 5.6 5 0 2-1.6 3.2-3.5 3.2-1.1 0-1.6-.45-2.1-.45'
       's-1 .45-2.1.45C7.6 20.1 6 18.9 6 16.9c0-2.5 2.5-5 5.6-5z"/></svg>')

# One toggle control, shared by the generated pages and hand-copied into the
# four Tailwind pages. Icons: sun (light), moon (dark), monitor (system).
THEME_TOGGLE = ('<button class="theme-toggle" type="button" data-theme-toggle aria-label="Toggle theme">'
  '<svg class="i-light" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
  '<circle cx="12" cy="12" r="4"/><path stroke-linecap="round" d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4'
  'M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
  '<svg class="i-dark" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
  '<path stroke-linecap="round" stroke-linejoin="round" d="M20 14.2A8.2 8.2 0 019.8 4a8.4 8.4 0 100 20 8.2 8.2 0 0010.2-9.8z"/></svg>'
  '<svg class="i-system" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
  '<rect x="2.5" y="4" width="19" height="13" rx="2"/><path stroke-linecap="round" d="M8.5 20.5h7"/></svg>'
  '</button>')

# Ordered: drives prev/next.
PAGES = [
    ("learn",                    "Overview"),
    ("learn-nutrition",          "Feline nutrition fundamentals"),
    ("learn-daily-requirements", "Daily nutrient requirements"),
    ("learn-labels",             "Reading a cat food label"),
    ("learn-food-types",         "Wet, dry, raw &amp; fresh"),
    ("learn-hydration",          "Hydration"),
    ("learn-additives",          "Additives to avoid"),
    ("learn-feeding",            "How much &amp; how often"),
    ("learn-life-stages",        "Life stages"),
    ("learn-toxic",              "Toxic foods &amp; hazards"),
    ("learn-health",             "Diet in common conditions"),
]

SIDEBAR = [
    ("Getting started", [("learn", "Overview")]),
    ("Fundamentals", [
        ("learn-nutrition", "Feline nutrition fundamentals"),
        ("learn-daily-requirements", "Daily nutrient requirements"),
        ("learn-labels", "Reading a cat food label"),
    ]),
    ("Food &amp; water", [
        ("learn-food-types", "Wet, dry, raw &amp; fresh"),
        ("learn-hydration", "Hydration"),
        ("learn-additives", "Additives to avoid"),
    ]),
    ("Feeding practice", [
        ("learn-feeding", "How much &amp; how often"),
        ("learn-life-stages", "Life stages"),
    ]),
    ("Health &amp; safety", [
        ("learn-toxic", "Toxic foods &amp; hazards"),
        ("learn-health", "Diet in common conditions"),
    ]),
]

TITLES = dict(PAGES)


def sidebar_html(slug):
    """The guide's own section list, emitted as the second level of the shared
    drawer. The site links sit above it, so a reader on a guide page can reach
    the rest of the site from the same control (M14)."""
    out = []
    for label, items in SIDEBAR:
        out.append('  <div class="sidebar-group">')
        out.append('    <p class="sidebar-label">%s</p>' % label)
        out.append('    <ul>')
        for s, name in items:
            cur = ' aria-current="page"' if s == slug else ''
            out.append('      <li><a href="./%s.html"%s>%s</a></li>' % (s, cur, name))
        out.append('    </ul>')
        out.append('  </div>')
    return chrome.drawer('./learn.html', sections="\n".join(out) + "\n")


HEADING_RE = re.compile(r'<h2 id="([^"]+)"[^>]*>(.*?)</h2>', re.S)
TAG_RE = re.compile(r"<[^>]+>")


def toc_html(body):
    items = HEADING_RE.findall(body)
    if not items:
        return ""
    out = ['<aside class="toc" aria-label="On this page">',
           '  <p class="toc-title">On this page</p>', '  <nav><ul>']
    for hid, text in items:
        text = TAG_RE.sub("", text).strip()
        # Drop the leading section number used in the visible heading.
        text = re.sub(r"^\d+\.\s*", "", text)
        out.append('    <li><a href="#%s">%s</a></li>' % (hid, text))
    out.append('  </ul></nav>')
    out.append('</aside>')
    return "\n".join(out)


def pagination_html(slug):
    slugs = [s for s, _ in PAGES]
    i = slugs.index(slug)
    prev_ = PAGES[i - 1] if i > 0 else None
    next_ = PAGES[i + 1] if i < len(PAGES) - 1 else None
    out = ['<nav class="pagination" aria-label="Guide pagination">']
    if prev_:
        out.append('  <a href="./%s.html" rel="prev"><span class="dir">Previous</span>'
                   '<span class="label">&larr; %s</span></a>' % prev_)
    else:
        out.append('  <span class="placeholder"></span>')
    if next_:
        out.append('  <a class="next" href="./%s.html" rel="next"><span class="dir">Next</span>'
                   '<span class="label">%s &rarr;</span></a>' % next_)
    else:
        out.append('  <span class="placeholder"></span>')
    out.append('</nav>')
    return "\n".join(out)


FOOTER = """<footer class="site-footer">
  <div class="site-footer-inner">
    <div>
      <a class="footer-brand" href="./index.html">%(paw)s Cat Food Center</a>
      <p class="footer-tagline">Science-based cat food reviews and a free, open guide to feeding a cat well.</p>
      <a class="footer-cta" href="https://azqato.github.io/support.html" target="_blank" rel="noopener noreferrer">Support</a>
    </div>
    <div class="footer-col">
      <h3>Fundamentals</h3>
      <ul>
        <li><a href="./learn-nutrition.html">Nutrition fundamentals</a></li>
        <li><a href="./learn-daily-requirements.html">Daily requirements</a></li>
        <li><a href="./learn-labels.html">Reading a label</a></li>
        <li><a href="./learn-feeding.html">How much to feed</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h3>Food &amp; water</h3>
      <ul>
        <li><a href="./learn-food-types.html">Wet, dry, raw &amp; fresh</a></li>
        <li><a href="./learn-hydration.html">Hydration</a></li>
        <li><a href="./learn-additives.html">Additives to avoid</a></li>
        <li><a href="./learn-life-stages.html">Life stages</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h3>Reference</h3>
      <ul>
        <li><a href="./learn.html">The Cat Care Guide</a></li>
        <li><a href="./learn-toxic.html">Toxic foods</a></li>
        <li><a href="./learn-health.html">Diet in disease</a></li>
        <li><a href="./methodology.html">CFC Score methodology</a></li>
      </ul>
    </div>
  </div>
  <div class="site-footer-base">
    <span>Educational content, not veterinary advice. Always consult your veterinarian about your own cat.</span>
    <span>Built by <a href="https://azqato.github.io/index.html" target="_blank" rel="noopener noreferrer">Azqato</a></span>
  </div>
</footer>""" % {"paw": PAW}


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>%(title)s - Cat Food Center</title>
  <meta name="description" content="%(description)s">
  <link rel="icon" href="./favicon.svg">
  <!-- Blocking on purpose: applies the stored theme before first paint. -->
  <script src="./assets/cfc-theme.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Public+Sans:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="./assets/cfc-tokens.css">
  <link rel="stylesheet" href="./assets/cfc.css">
</head>
<body>

%(topbar)s
<div class="shell">

%(sidebar)s
  <!-- ── Article ── -->
  <main class="article" id="main">

    <nav class="crumbs" aria-label="Breadcrumb">
      <a href="./index.html">Home</a>
      <span class="sep">/</span>
      <a href="./learn.html">The Cat Care Guide</a>
      <span class="sep">/</span>
      <span class="current">%(crumb)s</span>
    </nav>

    <h1>%(h1)s</h1>
    <p class="lede">%(lede)s</p>

%(body)s

%(pagination)s
  </main>

%(toc)s
</div>

%(footer)s

<script src="./assets/cfc-docs.js"></script>
</body>
</html>
"""


def build(slug, h1, description, lede, body, crumb=None, title=None):
    html = TEMPLATE % {
        "title": title or TAG_RE.sub("", h1),
        "description": description,
        "paw": PAW,
        "theme": THEME_TOGGLE,
        "topbar": chrome.topbar('./learn.html'),
        "sidebar": sidebar_html(slug),
        "crumb": crumb or TITLES.get(slug, h1),
        "h1": h1,
        "lede": lede,
        "body": body.rstrip() + "\n",
        "pagination": pagination_html(slug),
        "toc": toc_html(body),
        "footer": chrome.footer(),
    }
    path = os.path.join(OUT, slug + ".html")
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    return path
