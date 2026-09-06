# -*- coding: utf-8 -*-
"""Regenerate every page in the Learn section.

    python tools/learn/build.py

Each c_*.py module holds the article body for one page and calls shell.build()
on import. shell.py owns the documentation chrome shared by all of them: the
top bar, sidebar, breadcrumb, on-this-page rail, prev/next, and site footer.
Output is plain static HTML written to the repository root, so deployment
still needs no build step -- this script exists so the eleven pages cannot
drift apart, not because the site requires it.

Edit content in tools/learn/c_*.py and rerun. Do not hand-edit learn*.html;
those files are generated and your changes will be overwritten.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

MODULES = [
    "c_overview", "c_nutrition", "c_daily", "c_labels", "c_foodtypes",
    "c_hydration", "c_additives", "c_feeding", "c_lifestages", "c_toxic",
    "c_health",
]

if __name__ == "__main__":
    for name in MODULES:
        __import__(name)
        print("built", name)
    print("\n%d pages written." % len(MODULES))
