/* ==========================================================================
   Service worker registration, and the offline banner.

   A classic script rather than a module: it has no imports, and it needs to run
   on the guide pages too, which are generated and do not use modules.

   Registration is deliberately late (on `load`) so that installing the worker
   and warming its cache never competes with rendering the page the visitor is
   actually waiting for.
   ========================================================================== */
(function () {
  'use strict';

  if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () {
      // A relative path, so the worker's scope is the site's directory. On
      // GitHub Pages the site lives under a repository subpath, and '/sw.js'
      // would point at the domain root and fail to register.
      navigator.serviceWorker.register('./sw.js').catch(function () {
        /* Registration fails on an insecure origin, in some private modes, and
           where the user has disabled it. None of that should surface: the site
           works without a worker, which is the whole point of a progressive
           enhancement. */
      });
    });
  }

  /* ── Offline banner ──
     Shown when the browser reports no connection. It is a statement of fact
     about the network, not a claim about what is cached, so its wording says
     what the visitor can still expect rather than promising anything. */
  var banner;

  function ensureBanner() {
    if (banner) return banner;
    banner = document.createElement('div');
    banner.setAttribute('role', 'status');
    banner.hidden = true;
    banner.style.cssText = [
      'position:fixed', 'left:0', 'right:0', 'bottom:0', 'z-index:60',
      'background:var(--warn-bg)', 'color:var(--warn-ink)',
      'border-top:1px solid var(--hairline)',
      'padding:10px 16px', 'text-align:center',
      'font-size:.75rem', 'line-height:1.4',
    ].join(';');
    banner.textContent = 'You are offline. Products you have already opened are still readable; '
      + 'anything new needs a connection.';
    document.body.appendChild(banner);
    return banner;
  }

  function sync() {
    // navigator.onLine is famously optimistic; it reports a network interface,
    // not reachability: so it is trusted only in the negative direction, where
    // it is reliable. A false "you are online" simply shows nothing.
    if (navigator.onLine) {
      if (banner) banner.hidden = true;
    } else {
      ensureBanner().hidden = false;
    }
  }

  window.addEventListener('online', sync);
  window.addEventListener('offline', sync);
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', sync);
  } else {
    sync();
  }
})();
