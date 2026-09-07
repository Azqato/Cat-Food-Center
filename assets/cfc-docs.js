/* ==========================================================================
   Cat Food Center: Learn section behaviour.

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

  /* ── 2. "On this page" rail ──

     Two kinds of page use this rail, and they fill it at different times.

     The guide pages and the methodology page ship theirs in the HTML: the
     generator reads the headings out of the source fragment and writes the
     list. The product page cannot work that way, because its headings are
     written by product-page.js after the fetch returns, so at build time there
     is nothing to index. That page ships an empty rail marked
     data-client-toc, hidden, and dispatches "cfc:content" once the article is
     painted; the list is then read back out of the DOM here.

     So the spy has to be re-runnable rather than one-shot. Each call drops the
     observer and scroll listener the previous one installed before wiring up
     the new headings, or a redrawn article would leave a spy pointing at
     elements that are no longer on the page.
  */
  var observer = null;
  var onScroll = null;

  function buildRail() {
    var aside = document.querySelector('.toc[data-client-toc]');
    var list = aside && aside.querySelector('#toc-list');
    if (!list) return;

    var headings = Array.prototype.slice.call(
      document.querySelectorAll('.article h2[id]')
    );
    list.innerHTML = '';
    headings.forEach(function (h) {
      var li = document.createElement('li');
      var a = document.createElement('a');
      a.href = '#' + h.id;
      a.textContent = (h.textContent || '').replace(/\s+/g, ' ').trim();
      li.appendChild(a);
      list.appendChild(li);
    });

    // A rail with nothing in it is worse than no rail: an empty column reads
    // as a page whose sections failed to load. A product that is not in the
    // database renders no sections at all, and gets no rail.
    aside.hidden = headings.length === 0;
  }

  function spy() {
    if (observer) { observer.disconnect(); observer = null; }
    if (onScroll) { window.removeEventListener('scroll', onScroll); onScroll = null; }

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
      observer = new IntersectionObserver(function (entries) {
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
      onScroll = function () {
        if (ticking) return;
        ticking = true;
        window.requestAnimationFrame(function () {
          var passed = targets.filter(function (t) {
            return t.el.getBoundingClientRect().top <= 120;
          });
          activate(passed[passed.length - 1] || targets[0]);
          ticking = false;
        });
      };
      window.addEventListener('scroll', onScroll, { passive: true });
    }
  }

  spy();

  // Dispatched by a page that paints its own article. Rebuilding the rail and
  // restarting the spy is cheap, and doing both keeps the two in step.
  document.addEventListener('cfc:content', function () {
    buildRail();
    spy();
  });
})();
