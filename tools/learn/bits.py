# -*- coding: utf-8 -*-
"""Reusable content components for the Learn pages."""

ICONS = {
    "note": '<svg class="callout-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path stroke-linecap="round" d="M12 11v5M12 7.6v.6"/></svg>',
    "tip": '<svg class="callout-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.5 10.9c.5.4.8 1 .8 1.6v.5h5.4v-.5c0-.6.3-1.2.8-1.6A6 6 0 0 0 12 3z"/></svg>',
    "warning": '<svg class="callout-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linejoin="round" d="M12 4.5 2.8 20h18.4L12 4.5z"/><path stroke-linecap="round" d="M12 10v4.2M12 17.2v.4"/></svg>',
    "danger": '<svg class="callout-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path stroke-linejoin="round" d="M8.2 3h7.6L21 8.2v7.6L15.8 21H8.2L3 15.8V8.2L8.2 3z"/><path stroke-linecap="round" d="M12 8v4.6M12 15.8v.4"/></svg>',
}

LABELS = {"note": "Note", "tip": "Rule of thumb", "warning": "Common mistake", "danger": "Danger"}


def callout(kind, body, title=None):
    return (
        '<div class="callout callout-%s" role="note">\n'
        '  %s\n'
        '  <div class="callout-body">\n'
        '    <p class="callout-title">%s</p>\n'
        '%s\n'
        '  </div>\n'
        '</div>'
    ) % (kind, ICONS[kind], title or LABELS[kind], _indent(body, 4))


def panel(head, body):
    return (
        '<div class="panel">\n'
        '  <div class="panel-head"><span>%s</span></div>\n'
        '  <div class="panel-body">\n%s\n  </div>\n'
        '</div>'
    ) % (head, _indent(body, 4))


def table(caption, headers, rows, aligns=None):
    """rows: list of either a string (group header) or a list of cells."""
    n = len(headers)
    aligns = aligns or [""] * n
    out = ['<div class="table-wrap">', '<table class="data">']
    if caption:
        out.append('  <caption>%s</caption>' % caption)
    out.append('  <thead><tr>')
    for h, a in zip(headers, aligns):
        cls = ' class="num"' if a == "num" else ""
        out.append('    <th scope="col"%s>%s</th>' % (cls, h))
    out.append('  </tr></thead>')
    out.append('  <tbody>')
    for r in rows:
        if isinstance(r, str):
            out.append('    <tr class="grp"><td colspan="%d">%s</td></tr>' % (n, r))
            continue
        out.append('    <tr>')
        for c, a in zip(r, aligns):
            cls = ' class="num"' if a == "num" else ""
            out.append('      <td%s>%s</td>' % (cls, c))
        out.append('    </tr>')
    out.append('  </tbody>')
    out.append('</table>')
    out.append('</div>')
    return "\n".join(out)


def entry(name, chips, body, meta=None):
    """chips: list of (css-suffix, label)."""
    chip_html = "".join(
        '<span class="chip chip-%s">%s</span>' % (c, t) for c, t in chips
    )
    out = ['<div class="entry">',
           '  <div class="entry-head"><span class="entry-name">%s</span>%s</div>' % (name, chip_html)]
    if meta:
        out.append('  <p class="entry-meta">%s</p>' % meta)
    out.append(_indent(body, 2))
    out.append('</div>')
    return "\n".join(out)


def cards(items):
    """items: list of (href, eyebrow_or_None, title, desc)."""
    out = ['<div class="card-grid">']
    for href, eyebrow, title, desc in items:
        out.append('  <a class="card" href="%s">' % href)
        if eyebrow:
            out.append('    <span class="card-eyebrow">%s</span>' % eyebrow)
        out.append('    <span class="card-title">%s</span>' % title)
        out.append('    <span class="card-desc">%s</span>' % desc)
        out.append('  </a>')
    out.append('</div>')
    return "\n".join(out)


def compare(left_title, left_items, right_title, right_items):
    def col(t, items):
        lis = "".join("      <li>%s</li>\n" % i for i in items)
        return '    <div>\n      <h4>%s</h4>\n      <ul>\n%s      </ul>\n    </div>' % (t, lis)
    return ('<div class="compare">\n%s\n%s\n</div>'
            % (col(left_title, left_items), col(right_title, right_items)))


def h2(hid, text):
    return '<h2 id="%s">%s</h2>' % (hid, text)


def _indent(s, n):
    pad = " " * n
    return "\n".join(pad + line if line.strip() else line for line in s.split("\n"))
