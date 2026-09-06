/* ==========================================================================
   Service worker.

   Written by hand rather than generated, because there is no build step
   (docs/ADR-001-static-first.md) and because a cache that behaves in ways
   nobody can read is worse than no cache. Every decision here is one of three
   strategies, chosen per resource for a stated reason.

   The point of caching is not speed. It is that the phone in a supermarket
   aisle — exactly where this app is used — has the worst connectivity in the
   building, and a product someone has already looked at should still be
   readable when the signal goes.

   ── The rule that governs everything below ──

   A cached score must never be presented as a current one. The scoring engine
   changes, the database changes, and a stale answer rendered as fresh is the
   same failure as the English-only matcher: confidently wrong, with nothing
   about it looking wrong. So cached API responses are served *and labelled*,
   and the page says what it is showing.
   ========================================================================== */

/* Bump this to retire every old cache at once. It is the only lever that
   reliably clears a bad deploy from a device we cannot reach. */
const VERSION = 'v1';
const SHELL = `cfc-shell-${VERSION}`;
const API = `cfc-api-${VERSION}`;
const IMAGES = `cfc-images-${VERSION}`;

/* The app shell: everything needed to render a page with no network at all.
   Relative paths, because the site is served from a repository subpath on
   GitHub Pages and absolute ones would point at the domain root. */
const SHELL_ASSETS = [
  './',
  './index.html',
  './search.html',
  './product.html',
  './scan.html',
  './submit.html',
  './methodology.html',
  './offline.html',
  './favicon.svg',
  './assets/cfc-tokens.css',
  './assets/cfc-theme.js',
  './assets/cfc-tailwind.js',
  './assets/js/opff.js',
  './assets/js/scoring.js',
  './assets/js/scanner.js',
  './assets/js/history.js',
  './assets/js/product-page.js',
  './assets/js/search-page.js',
  './assets/js/scan-page.js',
  './assets/js/submit-page.js',
  './assets/js/home-page.js',
  './assets/js/pwa.js',
  './assets/data/additives.json',
  './manifest.webmanifest',
  './assets/icons/icon-192.png',
];

self.addEventListener('install', (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open(SHELL);
    // addAll is atomic: one 404 fails the whole install and the old worker
    // stays. That is the behaviour we want — a half-populated shell would
    // break pages offline in ways that are very hard to diagnose.
    await cache.addAll(SHELL_ASSETS);
    await self.skipWaiting();
  })());
});

self.addEventListener('activate', (event) => {
  event.waitUntil((async () => {
    const keep = [SHELL, API, IMAGES];
    const names = await caches.keys();
    await Promise.all(names.filter((n) => !keep.includes(n)).map((n) => caches.delete(n)));
    await self.clients.claim();
  })());
});

const isApi = (url) => url.hostname.endsWith('openpetfoodfacts.org');
const isImage = (request) => request.destination === 'image';

/**
 * Network-first, falling back to cache.
 *
 * For HTML and for API data, where being current matters more than being fast.
 * A stale product page is acceptable when the alternative is no page; a stale
 * one served in preference to a fresh one is not.
 */
async function networkFirst(request, cacheName) {
  const cache = await caches.open(cacheName);
  try {
    const response = await fetch(request);
    // Only successful responses are cached. A 404 from the API is meaningful —
    // it is how an unknown barcode is detected — but caching it would keep
    // reporting "not found" after the product is added to the database.
    if (response.ok) cache.put(request, response.clone());
    return response;
  } catch (err) {
    const cached = await cache.match(request);
    if (!cached) throw err;
    // Stamp it, so the page can say it is showing a saved copy. A Response's
    // headers are immutable, so this is a rebuild rather than a mutation.
    // Without the stamp the page has no way to tell a cached answer from a
    // fresh one, and would present an old score as current — the same class of
    // failure as reporting an unreadable label as clean.
    const headers = new Headers(cached.headers);
    headers.set('x-cfc-cached', String(cached.headers.get('date') || 'yes'));
    return new Response(await cached.blob(), {
      status: cached.status,
      statusText: cached.statusText,
      headers,
    });
  }
}

/** Cache-first. For images, which are large and never change under a URL. */
async function cacheFirst(request, cacheName) {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(request);
  if (cached) return cached;
  const response = await fetch(request);
  if (response.ok) cache.put(request, response.clone());
  return response;
}

/**
 * Stale-while-revalidate. For the shell: instant from cache, updated in the
 * background, so a deploy reaches the device on the visit after next rather
 * than blocking this one.
 */
async function staleWhileRevalidate(request, cacheName) {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(request);
  const fetching = fetch(request)
    .then((response) => {
      if (response.ok) cache.put(request, response.clone());
      return response;
    })
    .catch(() => null);
  return cached || (await fetching) || Promise.reject(new Error('offline'));
}

self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.method !== 'GET') return;

  const url = new URL(request.url);

  if (isApi(url)) {
    event.respondWith(networkFirst(request, API));
    return;
  }

  if (isImage(request)) {
    event.respondWith(cacheFirst(request, IMAGES).catch(() => Response.error()));
    return;
  }

  /* Navigations: straight to the network, so a deploy is picked up
     immediately, falling back to the precached page and then to offline.html.

     Deliberately not cached here. Every product is a different query string on
     the same document — product.html?barcode=X — so caching the response would
     add one entry per product viewed, all of them byte-identical, and grow the
     shell cache without bound. The document is already precached, so
     `ignoreSearch` finds it whatever the query, and the barcode is read from
     the URL by the page itself. Without that flag an offline product page
     would fall through to offline.html even though the document was cached. */
  if (request.mode === 'navigate') {
    event.respondWith((async () => {
      const cache = await caches.open(SHELL);
      try {
        return await fetch(request);
      } catch {
        return (await cache.match(request, { ignoreSearch: true }))
          || (await cache.match('./offline.html'))
          || Response.error();
      }
    })());
    return;
  }

  // Same-origin sub-resources — CSS, JS, JSON.
  if (url.origin === self.location.origin) {
    event.respondWith(staleWhileRevalidate(request, SHELL));
  }

  // Everything else (fonts, Tailwind, ZXing) goes to the network untouched.
  // Third-party CDNs set their own cache headers, and second-guessing them
  // from here would mean owning their invalidation too.
});
