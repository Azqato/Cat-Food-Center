# -*- coding: utf-8 -*-
"""Check every foreground/background token pair in assets/cfc-tokens.css
against WCAG AA (4.5:1 for text).

Run after any palette change:

    python tools/check-contrast.py

Exits non-zero if a pair fails, so it can gate a change.
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS = os.path.join(ROOT, 'assets', 'cfc-tokens.css')

# (label, foreground token, background token, required ratio).
# The hairline is a non-text separator; 1.2 is the bar for "visible", not AA.
CHECKS = [
    ('body text',            'ink',        'bg',      4.5),
    ('body text on surface', 'ink',        'surface', 4.5),
    ('muted text',           'ink-soft',   'bg',      4.5),
    ('muted on surface',     'ink-soft',   'surface', 4.5),
    ('link / accent',        'accent',     'bg',      4.5),
    ('accent on surface',    'accent',     'surface', 4.5),
    ('accent on accent-sub', 'accent',     'accent-sub', 4.5),
    ('on-accent on accent',  'on-accent',  'accent',  4.5),
    ('hairline vs bg',       'hairline',   'bg',      1.2),
    # Status text, on both backgrounds, added 2026-09-08 in M20a.
    #
    # These rows are the gate's own bug fix. It used to check 'excellent' and
    # 'bad' against 'surface' alone, under the names of the callouts that
    # happened to use them, and it never checked 'good' or 'poor' as text at
    # all. So --good at 2.7:1 and --poor at 2.5:1 sat in the light theme for
    # six milestones while both were being rendered as words, and this file
    # reported zero failing pairs the whole time. It also missed --warning-ink
    # failing on --bg while passing on --surface, because only one of the two
    # was ever asked about.
    #
    # Every status colour is now checked as text under its own name, against
    # both backgrounds. A pair that is not listed here is a pair nobody is
    # checking, which is the only way this gate can be wrong.
    ('excellent text',       'excellent-ink', 'bg',      4.5),
    ('excellent on surface', 'excellent-ink', 'surface', 4.5),
    ('good text',            'good-ink',      'bg',      4.5),
    ('good on surface',      'good-ink',      'surface', 4.5),
    ('poor text',            'poor-ink',      'bg',      4.5),
    ('poor on surface',      'poor-ink',      'surface', 4.5),
    ('bad text',             'bad-ink',       'bg',      4.5),
    ('bad on surface',       'bad-ink',       'surface', 4.5),
    ('warning callout text', 'warning-ink',   'bg',      4.5),
    ('warning on surface',   'warning-ink',   'surface', 4.5),
    ('warn banner text',     'warn-ink',      'warn-bg', 4.5),
    # The fills are deliberately NOT listed, and the reason is worth writing
    # down because the obvious row is the wrong one.
    #
    # Measured 2026-09-08: against --bg, --good is 2.72:1 and --poor is 2.51:1,
    # both under the 3:1 that WCAG 1.4.11 asks of a graphic. Adding those rows
    # was the first instinct and it was wrong. 1.4.11 covers graphics that are
    # *required to understand the content*, and neither of these is. Every chip
    # carries its own text on top, and that text is what is judged and what
    # states the band. The 6px rule above the score is aria-hidden and sits
    # directly beside the word "Good", so nothing is conveyed by that colour
    # alone. Asserting 3:1 here would force a palette change that buys no
    # reader anything, and a gate that fails for a reason nobody believes is a
    # gate people start editing to make quiet.
    #
    # The rule this leaves behind: if a status fill ever becomes the only thing
    # saying which band a product is in, it needs 3:1 and it needs a row here.
    ('chip excellent',       'chip-excellent-ink', 'chip-excellent-bg', 4.5),
    ('chip good',            'chip-good-ink',      'chip-good-bg',      4.5),
    ('chip poor',            'chip-poor-ink',      'chip-poor-bg',      4.5),
    ('chip bad',             'chip-bad-ink',       'chip-bad-bg',       4.5),
    ('chip accent',          'chip-accent-ink',    'chip-accent-bg',    4.5),
    ('chip neutral',         'chip-neutral-ink',   'chip-neutral-bg',   4.5),
]


def palettes():
    s = io.open(CSS, encoding='utf-8').read()

    def block(sel):
        i = s.index(sel)
        return dict(re.findall(r'(--[a-z-]+):\s*(#[0-9A-Fa-f]{6})', s[i:s.index('}', i)]))

    light = block(':root {')
    dark = block(':root[data-theme="dark"] {')
    media = block('@media (prefers-color-scheme: dark)')
    # The two dark lists are duplicated by necessity; catch them drifting apart.
    if dark != media:
        diff = {k: (dark.get(k), media.get(k)) for k in set(dark) | set(media)
                if dark.get(k) != media.get(k)}
        print('ERROR: the two dark blocks have drifted apart: %s' % diff)
        sys.exit(2)
    return [('LIGHT', light), ('DARK', dark)]


def luminance(h):
    c = [int(h[i:i + 2], 16) / 255.0 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def ratio(a, b):
    la, lb = luminance(a), luminance(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def main():
    fails = 0
    for name, pal in palettes():
        print('\n== %s ==' % name)
        for label, fg, bg, need in CHECKS:
            f, b = pal.get('--' + fg), pal.get('--' + bg)
            if not f or not b:
                print('  ??   %-22s missing token' % label)
                fails += 1
                continue
            r = ratio(f, b)
            ok = r >= need
            fails += 0 if ok else 1
            print('  %s %-22s %5.2f:1 (need %.1f)  %s on %s'
                  % ('OK  ' if ok else 'FAIL', label, r, need, f, b))
    print('\n%d failing pair(s)' % fails)
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
