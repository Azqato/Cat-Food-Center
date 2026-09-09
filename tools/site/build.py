# -*- coding: utf-8 -*-
"""Generate the nine application pages.

    python tools/site/build.py

Each page is its body content in tools/site/content/<name>.html, wrapped in the
shared chrome from chrome.py. The generated files are committed, so deployment
still needs no build step; the generator runs on a developer machine only.

Since M19 a page is a directory holding an index.html, served as /search/
rather than /search.html. index.html is the only page file the repository root
is permitted to hold; the rule and the reasons are in PRD section 16.4.

Do not hand-edit the generated pages. Edit the content fragment and rerun, the
same rule the Cat Care Guide has had since M4.
"""
import datetime
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chrome  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONTENT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'content')

# name, title, description, nav href it marks, module, wants a toc rail,
# wants the top-bar search field.
#
# The two pages that carry a search input in the body do not repeat it in the
# bar. The pages that index their own headings get the third column; the rest
# collapse to one, rather than showing an empty rail. Both decisions are in
# docs/DESIGN.md section 6.
#
# The toc column takes three values, not two:
#   False      no rail, two columns.
#   True       the generator reads the h2 ids out of the fragment and writes
#              the list. The fragment must have some, or the build fails.
#   'client'   the rail ships empty and hidden, and cfc-docs.js fills it from
#              the DOM when the page dispatches "cfc:content". For a page whose
#              headings do not exist until a fetch returns.
PAGES = [
    ('index',       'Cat Food Center',
     'Scan a barcode or search to get an honest 0 to 100 score for any cat food, with the reasoning shown.',
     '{{root}}', 'home-page.js', False, False),
    ('search',      'Search',
     'Search cat food by brand or product name and see a score for each result.',
     '{{root}}search/', 'search-page.js', False, False),
    ('brands',      'Browse by brand',
     'Every cat food brand in the database, A to Z, with the number of products for each.',
     '{{root}}brands/', 'brands-page.js', False, True),
    # A client-built rail: the product page's headings are written by
    # product-page.js after the fetch returns, so the generator ships the
    # column empty and the script fills it.
    ('product',     'Product',
     'The full breakdown for one cat food: score, ingredients, additive flags and nutrition.',
     '{{root}}search/', 'product-page.js', 'client', True),
    ('scan',        'Scan a barcode',
     'Point your camera at the barcode on a tin of cat food to open its page.',
     '{{root}}scan/', 'scan-page.js', False, True),
    ('submit',      'Add a missing product',
     'The product is not in the database yet. Here is how to add it so it works for everyone.',
     '{{root}}search/', 'submit-page.js', False, True),
    ('compare',     'Compare two foods',
     'Two cat foods side by side on a dry-matter basis, pillar by pillar.',
     '{{root}}compare/', 'compare-page.js', False, True),
    ('methodology', 'Methodology',
     'How the CFC Score is calculated, what it weighs, and what it cannot see.',
     '{{root}}methodology/', None, True, True),
    ('offline',     'Offline',
     'You are offline. Here is what still works.',
     None, None, False, False),
]


# The same shape tools/learn/shell.py indexes: an h2 carrying an id. A page
# whose fragment has none gets no rail rather than an empty one.
HEADING_RE = re.compile(r'<h2 id="([^"]+)"[^>]*>(.*?)</h2>', re.S)
TAG_RE = re.compile(r'<[^>]+>')


def toc_items(body):
    out = []
    for hid, raw in HEADING_RE.findall(body):
        text = ' '.join(TAG_RE.sub('', raw).split())
        out.append('      <li><a href="#%s">%s</a></li>' % (hid, text))
    return out


def build(name, title, description, current, module, want_toc, want_search):
    body = io.open(os.path.join(CONTENT, name + '.html'), encoding='utf-8').read().rstrip()
    client_toc = want_toc == 'client'
    items = toc_items(body) if want_toc is True else []
    if want_toc is True and not items:
        raise SystemExit('%s wants a toc but its fragment has no h2 with an id' % name)
    toc = ''
    if client_toc:
        # Hidden until it has something in it, so a product that fails to load
        # does not leave a labelled empty column standing there.
        toc = ('\n  <aside class="toc" aria-label="On this page" data-client-toc hidden>\n'
               '    <p class="toc-title">On this page</p>\n'
               '    <nav><ul id="toc-list"></ul></nav>\n'
               '  </aside>\n')
    elif items:
        toc = ('\n  <aside class="toc" aria-label="On this page">\n'
               '    <p class="toc-title">On this page</p>\n'
               '    <nav><ul id="toc-list">\n%s\n    </ul></nav>\n'
               '  </aside>\n' % '\n'.join(items))
    shell_class = 'shell shell-app-toc' if toc else 'shell shell-app'
    out = (
        chrome.head(title, description)
        + '<body>\n\n'
        + chrome.topbar(current, show_search=want_search)
        + '\n<div class="%s">\n\n' % shell_class
        + chrome.drawer(current)
        + '\n  <main class="article" id="main">\n\n'
        + body + '\n\n  </main>\n'
        + toc
        + '</div>\n\n'
        + chrome.footer()
        + '\n' + chrome.scripts(module)
        + '\n</body>\n</html>\n')
    # The home page is the site root's own index. Every other page is a
    # directory containing one, served as /search/ rather than /search.html,
    # under the root policy in PRD section 16.4: index.html is the only page
    # file the repository root is permitted to hold.
    if name == 'index':
        out_dir, depth = ROOT, 0
    else:
        out_dir, depth = os.path.join(ROOT, name), 1

    # The one place a depth becomes a path. The chrome and every content
    # fragment write {{root}}, so nothing upstream has to know how deep the
    # page it is being written into will sit. A hand-written prefix is the
    # failure mode this exists to remove: it works from one directory, 404s
    # from another, and the two are indistinguishable in a diff.
    out = out.replace('{{root}}', './' if depth == 0 else '../' * depth)

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    path = os.path.join(out_dir, 'index.html')
    io.open(path, 'w', encoding='utf-8', newline='\n').write(out)
    return path


BASE = 'https://azqato.github.io/catfoodcenter/'

# path, changefreq, priority. Ordered as the sitemap reads.
#
# offline/ is deliberately absent: it is reached only by the service worker,
# for a page never opened on this device, and has nothing to index. So is
# tools/tests.html, which is unlinked, carries noindex, and is not an address
# this project promises to keep.
#
# product/ is listed without a barcode. Every product is that one document
# under a different query string, so there is one address to crawl rather than
# one per SKU. See PRD section 16.2.
SITEMAP = [
    ('', 'weekly', '1.0'),
    ('search/', 'weekly', '0.8'),
    ('brands/', 'weekly', '0.8'),
    ('scan/', 'monthly', '0.8'),
    ('compare/', 'monthly', '0.7'),
    ('methodology/', 'monthly', '0.7'),
    ('product/', 'weekly', '0.5'),
    ('submit/', 'yearly', '0.3'),
    ('learn/', 'monthly', '0.9'),
]

SITEMAP_HEAD = """<?xml version="1.0" encoding="UTF-8"?>
<!--
  Cat Food Center sitemap.

  GENERATED by tools/site/build.py. Do not hand-edit.

  It is generated because it went stale twice by hand, and a sitemap that
  lists an address the site no longer serves is worse than no sitemap: it
  invites a crawler to spend its budget on 404s. The page lists here and the
  ones that write the pages are now the same lists.

  Every public page with content of its own. Deliberately omitted: the offline
  page, reached only by the service worker for a page never opened on this
  device, and tools/tests.html, which is unlinked, noindex, and not an address
  this project promises to keep.

  product/ is listed without a barcode. Every product is that one document
  under a different query string, so there is one address to crawl rather than
  one per SKU. Per-barcode pages would need pre-generating; see docs/PRD.md,
  section 16.2.

  Scope: this sitemap sits under a subpath of a domain this project does not
  own, so it is trusted only for URLs beneath its own path unless the host-level
  robots.txt names it. See robots.txt.
-->
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""


def write_sitemap(lastmod):
    """The sitemap, from the same page lists that generate the pages."""
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), 'learn'))
    import shell  # noqa: E402  the guide's page list and slug-to-URL rule

    entries = list(SITEMAP)
    for slug, _label in shell.PAGES:
        if slug == 'learn':
            continue  # already above, at its own priority
        entries.append((shell.href(slug).replace('{{root}}', ''), 'monthly', '0.7'))

    out = [SITEMAP_HEAD]
    for path, freq, priority in entries:
        out.append('  <url>\n    <loc>%s%s</loc>\n    <lastmod>%s</lastmod>\n'
                   '    <changefreq>%s</changefreq>\n    <priority>%s</priority>\n  </url>\n'
                   % (BASE, path, lastmod, freq, priority))
    out.append('</urlset>\n')
    path = os.path.join(ROOT, 'sitemap.xml')
    io.open(path, 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return len(entries)


if __name__ == '__main__':
    for row in PAGES:
        print('built %s' % ('index.html' if row[0] == 'index' else row[0] + '/index.html'))
        build(*row)
    print('\n%d pages written.' % len(PAGES))
    n = write_sitemap(datetime.date.today().isoformat())
    print('sitemap.xml written, %d urls.' % n)
