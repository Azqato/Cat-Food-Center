/* ==========================================================================
   Cat Food Center — Learn section behaviour.

   Two small enhancements, both optional: the page is fully readable and
   navigable with JavaScript disabled.

     1. Mobile sidebar drawer (hamburger toggle, backdrop, Escape to close).
     2. "On this page" scroll spy that highlights the section in view.
   ========================================================================== */
(function () {
  'use strict';

  /* ── 1. Sidebar drawer ── */
  var toggle = document.querySelector('.nav-toggle');
  var backdrop = document.querySelector('.sidebar-backdrop');
  var sidebar = document.querySelector('.sidebar');

  function setNav(open) {
    document.body.classList.toggle('nav-open', open);
    if (toggle) toggle.setAttribute('aria-expanded', String(open));
  }

  if (toggle) {
    toggle.addEventListener('click', function () {
      setNav(!document.body.classList.contains('nav-open'));
    });
  }
  if (backdrop) backdrop.addEventListener('click', function () { setNav(false); });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && document.body.classList.contains('nav-open')) {
      setNav(false);
      if (toggle) toggle.focus();
    }
  });

  // Following a link inside the drawer should close it.
  if (sidebar) {
    sidebar.addEventListener('click', function (e) {
      if (e.target.closest('a')) setNav(false);
    });
  }

  /* ── 2. Scroll spy ── */
  var tocLinks = Array.prototype.slice.call(document.querySelectorAll('.toc a[href^="#"]'));
  if (!tocLinks.length) return;

  var targets = tocLinks
    .map(function (link) {
      var el = document.getElementById(decodeURIComponent(link.hash.slice(1)));
      return el ? { link: link, el: el } : null;
    })
    .filter(Boolean);

  if (!targets.length) return;

  function activate(entry) {
    tocLinks.forEach(function (l) { l.classList.remove('is-active'); });
    if (entry) entry.link.classList.add('is-active');
  }

  if ('IntersectionObserver' in window) {
    var visible = new Set();
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) visible.add(e.target); else visible.delete(e.target);
      });
      // Highlight the topmost heading currently in the viewport band; if none
      // are visible (mid-section scrolling), keep the last one passed.
      var current = targets.filter(function (t) { return visible.has(t.el); })[0];
      if (!current) {
        var passed = targets.filter(function (t) {
          return t.el.getBoundingClientRect().top <= 120;
        });
        // At the very top of the page nothing has been passed yet; point at
        // the first section rather than leaving the rail blank.
        current = passed[passed.length - 1] || targets[0];
      }
      activate(current);
    }, { rootMargin: '-72px 0px -70% 0px', threshold: 0 });

    targets.forEach(function (t) { observer.observe(t.el); });
  } else {
    // Fallback for browsers without IntersectionObserver.
    var ticking = false;
    window.addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(function () {
        var passed = targets.filter(function (t) {
          return t.el.getBoundingClientRect().top <= 120;
        });
        activate(passed[passed.length - 1] || targets[0]);
        ticking = false;
      });
    }, { passive: true });
  }
})();
