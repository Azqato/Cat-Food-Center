/* ==========================================================================
   Service worker registration, and the offline banner.

   A classic script rather than a module: it has no imports, and nothing here
   needs one.

   It is loaded by the nine application pages only. The eleven guide pages do
   not include it, so arriving on one registers no worker and shows no offline
   banner; a visitor who then reaches an application page gets both. That is
   long-standing behaviour rather than a decision anybody made, and it is
   recorded in docs/PRD.md section 24.6 rather than changed inside M19, whose
   subject is where files live.

   Registration is deliberately late (on `load`) so that installing the worker
   and warming its cache never competes with rendering the page the visitor is
   actually waiting for.
   ========================================================================== */
(function () {
  'use strict';

  /* Where sw.js is, measured rather than assumed.

     This used to register './sw.js', which was correct while every page sat
     at the repository root. Since M19 a page is a directory, so from /search/
     that string means /search/sw.js. It would 404, and the more dangerous
     half is what happens if it ever did not: a worker's scope comes from its
     own path, so a worker registered under /search/ controls /search/ and
     nothing else. Offline support would narrow to one directory with no error
     anywhere, which is the failure PRD section 16.4 names.

     '/sw.js' is not the fix either: the site is served from a repository
     subpath and that points at the domain root.

     document.currentScript is this file's own <script> element, and this file
     is always assets/js/pwa.js, exactly two levels below the site root, on
     every page at every depth. It is read here at top level because
     currentScript is only defined during initial execution, not inside the
     load callback below. */
  var SW = new URL('../../sw.js', document.currentScript.src).href;

  if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () {
      navigator.serviceWorker.register(SW).catch(function () {
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
