/* ==========================================================================
   Cat Food Center: theme (light / dark / system).

   Load this SYNCHRONOUSLY in <head>, before any markup:

       <script src="./assets/cfc-theme.js"></script>

   A blocking script in the head runs before the body is painted, so the stored
   theme is applied with no flash of the wrong palette. It is deliberately a
   file rather than an inline snippet duplicated into fifteen pages: one source
   of truth is worth more here than the one small same-origin request, and the
   file is served from cache after the first page.

   Preference model: three states, cycled in this order:

       system  →  light  →  dark  →  system

   "system" stores nothing and removes the attribute, so the stylesheet's
   prefers-color-scheme block takes over. "light" and "dark" stamp
   data-theme on <html>, which wins over the media query.
   ========================================================================== */
(function () {
  'use strict';

  var KEY = 'cfc-theme';
  var ORDER = ['system', 'light', 'dark'];
  var root = document.documentElement;

  function stored() {
    try {
      var v = localStorage.getItem(KEY);
      return ORDER.indexOf(v) > 0 ? v : 'system';
    } catch (e) {
      // Private mode or blocked site data: fall back to the system theme.
      return 'system';
    }
  }

  function apply(theme) {
    if (theme === 'system') root.removeAttribute('data-theme');
    else root.setAttribute('data-theme', theme);
  }

  // ── Runs immediately, before first paint. ──
  var current = stored();
  apply(current);

  function save(theme) {
    try {
      if (theme === 'system') localStorage.removeItem(KEY);
      else localStorage.setItem(KEY, theme);
    } catch (e) { /* Not persisting is survivable; the page still themes. */ }
  }

  /* ── Toggle wiring, once the button exists ── */
  var LABEL = {
    system: 'Theme: system. Switch to light.',
    light: 'Theme: light. Switch to dark.',
    dark: 'Theme: dark. Switch to system.'
  };

  function paintButtons(theme) {
    var buttons = document.querySelectorAll('[data-theme-toggle]');
    for (var i = 0; i < buttons.length; i++) {
      buttons[i].setAttribute('data-theme-state', theme);
      buttons[i].setAttribute('aria-label', LABEL[theme]);
      buttons[i].setAttribute('title', LABEL[theme]);
    }
  }

  function cycle() {
    current = ORDER[(ORDER.indexOf(current) + 1) % ORDER.length];
    apply(current);
    save(current);
    paintButtons(current);
  }

  function init() {
    paintButtons(current);
    document.addEventListener('click', function (e) {
      var btn = e.target.closest && e.target.closest('[data-theme-toggle]');
      if (btn) cycle();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Keep other tabs in step.
  window.addEventListener('storage', function (e) {
    if (e.key !== KEY) return;
    current = stored();
    apply(current);
    paintButtons(current);
  });
})();
