# -*- coding: utf-8 -*-
"""The chrome every page shares: head, top bar, drawer and footer.

Before M14 the header and footer were hand-copied across nine application
pages. Adding one navigation link meant a nine-file edit, and any one of them
could be missed, which is exactly how a link comes to be present on eight pages
and absent from the ninth. This module is the single copy.

The guide pages get their chrome from tools/learn/shell.py, which imports the
same NAV and FOOTER definitions from here so the two cannot drift.
"""

# Site navigation. One list, used inline in the bar above 900px and inside the
# drawer below it.
NAV = [
    ('{{root}}',       'Home'),
    ('{{root}}scan/',        'Scan'),
    ('{{root}}search/',      'Search'),
    ('{{root}}brands/',      'Brands'),
    ('{{root}}compare/',     'Compare'),
    ('{{root}}learn/',       'Learn'),
    ('{{root}}methodology/', 'Methodology'),
]

SUPPORT_URL = 'https://azqato.github.io/support.html'
AUTHOR_URL = 'https://azqato.github.io/index.html'

PAW = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
       '<ellipse cx="7" cy="8.5" rx="2.1" ry="2.8"/><ellipse cx="12" cy="6.6" rx="2.1" ry="2.9"/>'
       '<ellipse cx="17" cy="8.5" rx="2.1" ry="2.8"/><ellipse cx="19.6" cy="13.4" rx="1.9" ry="2.3"/>'
       '<path d="M12 12.4c2.8 0 5.2 2.2 5.2 4.6 0 1.7-1.3 2.6-3 2.6-1 0-1.6-.4-2.2-.4s-1.2.4-2.2.4'
       'c-1.7 0-3-.9-3-2.6 0-2.4 2.4-4.6 5.2-4.6z"/></svg>')

THEME_TOGGLE = (
    '<button class="theme-toggle" type="button" data-theme-toggle aria-label="Toggle theme">'
    '<svg class="i-light" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
    '<circle cx="12" cy="12" r="4"/><path stroke-linecap="round" d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4'
    'M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
    '<svg class="i-dark" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
    '<path stroke-linecap="round" stroke-linejoin="round" d="M20 14.2A8.2 8.2 0 019.8 4a8.4 8.4 0 100 20 8.2 8.2 0 0010.2-9.8z"/></svg>'
    '<svg class="i-system" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
    '<rect x="2.5" y="4" width="19" height="13" rx="2"/><path stroke-linecap="round" d="M8.5 20.5h7"/></svg>'
    '</button>')

FOOTER_LINKS = [
    ('Find a food', [('{{root}}scan/', 'Scan a barcode'), ('{{root}}search/', 'Search'),
                     ('{{root}}brands/', 'Browse brands'), ('{{root}}compare/', 'Compare two foods')]),
    ('The guide', [('{{root}}learn/', 'Overview'), ('{{root}}learn/nutrition/', 'Nutrition'),
                   ('{{root}}learn/additives/', 'Additives'), ('{{root}}learn/toxic/', 'Toxic foods')]),
    ('About', [('{{root}}methodology/', 'How scoring works'),
               ('https://world.openpetfoodfacts.org/', 'Open Pet Food Facts'),
               ('https://github.com/Azqato/catfoodcenter/issues', 'Report a problem'),
               ('{{root}}LICENSE.md', 'Licence')]),
]


def head(title, description, page_css=True, extra=''):
    """The <head>. cfc-theme.js is deliberately a blocking script here: that
    position is what applies the stored theme before first paint, and moving it
    or adding defer reintroduces a flash of the wrong palette on every page."""
    app_css = ('  <link rel="stylesheet" href="{{root}}assets/cfc-app.css">\n' if page_css else '')
    # The home page is already called Cat Food Center. Suffixing it would make
    # the browser tab read "Cat Food Center - Cat Food Center".
    full = title if title == 'Cat Food Center' else title + ' - Cat Food Center'
    return (
        '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
        '  <meta charset="UTF-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '  <title>%s</title>\n'
        '  <meta name="description" content="%s">\n'
        '  <link rel="icon" href="{{root}}favicon.svg">\n'
        '  <link rel="manifest" href="{{root}}manifest.webmanifest">\n'
        '  <meta name="theme-color" content="#C2410C">\n'
        '  <link rel="apple-touch-icon" href="{{root}}assets/icons/icon-192.png">\n'
        '  <!-- Blocking on purpose: applies the stored theme before first paint. -->\n'
        '  <script src="{{root}}assets/cfc-theme.js"></script>\n'
        '  <link rel="stylesheet" href="{{root}}assets/cfc-tokens.css">\n'
        '  <link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        # Six of the nine application pages cannot paint until Open Pet Food
        # Facts answers, and on a slow connection the handshake is a real part
        # of that wait. Opening it while the document is still parsing costs
        # nothing on the pages that never call the API.
        '  <link rel="preconnect" href="https://world.openpetfoodfacts.org" crossorigin>\n'
        '  <link rel="preconnect" href="https://images.openpetfoodfacts.org" crossorigin>\n'
        '  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;'
        '9..144,600;9..144,700&family=Public+Sans:wght@400;500;600&display=swap" rel="stylesheet">\n'
        '  <link rel="stylesheet" href="{{root}}assets/cfc.css">\n'
        '%s%s</head>\n' % (full, description, app_css, extra))


def topbar(current, show_search=True):
    """The top bar. `current` is the href of the page, so it can mark itself.

    show_search is False on pages that already carry a search input in the
    body: two routes to the same place inside one viewport is a papercut.
    See docs/DESIGN.md section 6."""
    links = ''.join(
        '\n    <a href="%s"%s>%s</a>' % (href, ' aria-current="page"' if href == current else '', label)
        for href, label in NAV)
    search = ''
    if show_search:
        search = (
            '\n  <a class="topbar-search" href="{{root}}search/">'
            '\n    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
            '<circle cx="11" cy="11" r="7"/><path stroke-linecap="round" d="M20 20l-3.5-3.5"/></svg>'
            '\n    Search products\n    <span class="kbd">/</span>\n  </a>')
    return (
        '<a class="skip-link" href="#main">Skip to content</a>\n\n'
        '<!-- Generated by tools/site/chrome.py. Do not hand-edit. -->\n'
        '<header class="topbar">\n'
        '  <button class="nav-toggle" type="button" aria-label="Open navigation"'
        ' aria-controls="sidebar" aria-expanded="false">\n'
        '    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
        '<path stroke-linecap="round" d="M4 7h16M4 12h16M4 17h16"/></svg>\n'
        '  </button>\n'
        '  <a class="topbar-brand" href="{{root}}">%s Cat Food Center</a>\n'
        '  <nav class="topbar-nav" aria-label="Main navigation">%s\n  </nav>\n'
        '  <span class="topbar-spacer"></span>%s\n'
        '  %s\n'
        '  <a class="topbar-cta" href="%s" target="_blank" rel="noopener noreferrer">Support</a>\n'
        '</header>\n' % (PAW, links, search, THEME_TOGGLE, SUPPORT_URL))


def drawer(current, sections=''):
    """The mobile drawer. It holds the site menu, and on a guide page the
    section list is nested under it: one control, two levels."""
    links = ''.join(
        '\n      <li><a href="%s"%s>%s</a></li>' % (href, ' aria-current="page"' if href == current else '', label)
        for href, label in NAV)
    return (
        '<nav class="sidebar" id="sidebar" aria-label="Site">\n'
        '  <div class="sidebar-group sidebar-site">\n'
        '    <p class="sidebar-label">Cat Food Center</p>\n'
        '    <ul>%s\n    </ul>\n'
        '  </div>\n%s</nav>\n'
        '  <button class="sidebar-backdrop" type="button" tabindex="-1" aria-hidden="true"></button>\n'
        % (links, sections))


def footer():
    cols = ''
    for heading, links in FOOTER_LINKS:
        items = ''.join(
            '\n        <li><a href="%s"%s>%s</a></li>'
            % (href, ' target="_blank" rel="noopener noreferrer"' if href.startswith('http') else '', label)
            for href, label in links)
        cols += ('    <div class="footer-col">\n      <h3>%s</h3>\n      <ul>%s\n      </ul>\n    </div>\n'
                 % (heading, items))
    return (
        '<footer class="site-footer">\n'
        '  <div class="site-footer-inner">\n'
        '    <div>\n'
        '      <a class="footer-brand" href="{{root}}">%s Cat Food Center</a>\n'
        '      <p class="footer-tagline">Trustworthy reviews for your purrfect companion. '
        'No ads, no affiliate links, no brand deals.</p>\n'
        '      <a class="footer-cta" href="%s" target="_blank" rel="noopener noreferrer">Support this project</a>\n'
        '    </div>\n%s'
        '  </div>\n'
        '  <div class="site-footer-base">\n'
        '    <span>Informational only, and not veterinary advice.</span>\n'
        '    <span>Built by <a href="%s" target="_blank" rel="noopener noreferrer">Azqato</a>. '
        'Product data from <a href="https://world.openpetfoodfacts.org/" target="_blank" '
        'rel="noopener noreferrer">Open Pet Food Facts</a>.</span>\n'
        '  </div>\n'
        '</footer>\n' % (PAW, SUPPORT_URL, cols, AUTHOR_URL))


def scripts(module=None, docs_js=True):
    out = ''
    if docs_js:
        out += '<script src="{{root}}assets/cfc-docs.js"></script>\n'
    if module:
        out += '<script type="module" src="{{root}}assets/js/%s"></script>\n' % module
    out += '<script src="{{root}}assets/js/pwa.js"></script>\n'
    return out
