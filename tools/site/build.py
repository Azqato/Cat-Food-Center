# -*- coding: utf-8 -*-
"""Generate the nine application pages.

    python tools/site/build.py

Each page is its body content in tools/site/content/<name>.html, wrapped in the
shared chrome from chrome.py. The generated files at the repository root are
committed, so deployment still needs no build step; the generator runs on a
developer machine only.

Do not hand-edit the generated pages. Edit the content fragment and rerun, the
same rule the Cat Care Guide has had since M4.
"""
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
     './index.html', 'home-page.js', False, False),
    ('search',      'Search',
     'Search cat food by brand or product name and see a score for each result.',
     './search.html', 'search-page.js', False, False),
    ('brands',      'Browse by brand',
     'Every cat food brand in the database, A to Z, with the number of products for each.',
     './brands.html', 'brands-page.js', False, True),
    # A client-built rail: the product page's headings are written by
    # product-page.js after the fetch returns, so the generator ships the
    # column empty and the script fills it.
    ('product',     'Product',
     'The full breakdown for one cat food: score, ingredients, additive flags and nutrition.',
     './search.html', 'product-page.js', 'client', True),
    ('scan',        'Scan a barcode',
     'Point your camera at the barcode on a tin of cat food to open its page.',
     './scan.html', 'scan-page.js', False, True),
    ('submit',      'Add a missing product',
     'The product is not in the database yet. Here is how to add it so it works for everyone.',
     './search.html', 'submit-page.js', False, True),
    ('compare',     'Compare two foods',
     'Two cat foods side by side on a dry-matter basis, pillar by pillar.',
     './compare.html', 'compare-page.js', False, True),
    ('methodology', 'Methodology',
     'How the CFC Score is calculated, what it weighs, and what it cannot see.',
     './methodology.html', None, True, True),
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
    path = os.path.join(ROOT, name + '.html')
    io.open(path, 'w', encoding='utf-8', newline='\n').write(out)
    return path


if __name__ == '__main__':
    for row in PAGES:
        print('built %s.html' % row[0])
        build(*row)
    print('\n%d pages written.' % len(PAGES))
