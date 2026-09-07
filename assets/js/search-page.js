/* ==========================================================================
   /search/: live search against Open Pet Food Facts, by text or by brand.

   Results are scored on the fly with the same engine the product page uses,
   so a card and a product page can never disagree.

   ── Why the ordering changed ──

   This page used to re-sort every result scorable-first, then by score. The
   reasoning was that docs/PRD.md section 12 found most records too thin to
   score, and a page of "not scored" tiles is useless. That was true, and the
   fix was still wrong: it threw away the database's relevance ranking, so a
   search for a specific product could put a loosely related food above the
   exact match because the loose one happened to score well. The visitor asked
   for one thing and was answered with another, silently.

   So relevance is the spine now. Scorability is still surfaced, but as a badge
   on the card and an optional filter the visitor chooses, not as a hidden sort
   key applied on their behalf.

   ── Why the filter scans, and why it stops ──

   The API cannot filter on scorability: whether a product can be scored is
   something only this engine knows, and it knows it only after fetching the
   record. The filter used to hide cards on the page you were looking at, which
   could show 3 results for a query with 1571 matches. That was honest, and it
   was also close to useless.

   So it scans instead: SCAN_PAGES pages of results in one go, scores all of
   them, and shows every scorable product it found. What it will not do is
   pretend that is the database. Three rules keep it straight:

     1. The number it reports is always "N of the first S results", never "N
        results". S and the true total are both on screen.
     2. When the scan stops short of the total, the page says so, in the label
        and again at the end of the last page. A filter that quietly ended at
        120 of 1571 would be the same lie in a new place.
     3. Nothing here re-ranks. Relevance is still the API's, and the scan takes
        results in the order it was given them.

   The bound is what makes this safe to ship. A filter that kept fetching until
   it had enough would hammer a volunteer-run database on behalf of a query
   that may have no scorable results at all.
   ========================================================================== */
import { SITE } from './site.js';
import { searchProducts, brandDisplayName } from './opff.js';
import { scoreProduct, loadKnowledgeBase } from './scoring.js';
import { thumbHtml } from './thumb.js';

const BAND_TOKEN = {
  excellent: ['var(--chip-excellent-bg)', 'var(--chip-excellent-ink)'],
  good: ['var(--chip-good-bg)', 'var(--chip-good-ink)'],
  poor: ['var(--chip-poor-bg)', 'var(--chip-poor-ink)'],
  bad: ['var(--chip-bad-bg)', 'var(--chip-bad-ink)'],
};

const FORMAT_LABEL = { wet: 'Wet', dry: 'Dry', 'semi-moist': 'Semi-moist', treat: 'Treat' };

/* Five pages of 24 is 120 records, fetched in parallel, and about a fifth of
   them score (PRD section 12.1), so a typical scan finds twenty-odd. Raising
   this buys more results for a linearly larger burden on a database nobody is
   paid to run. It is a deliberate ceiling, not a technical limit. */
const SCAN_PAGES = 5;

const input = document.getElementById('search-input');
const label = document.getElementById('results-label');
const list = document.getElementById('results-list');
const heading = document.getElementById('results-heading');
const controls = document.getElementById('results-controls');
const onlyScorable = document.getElementById('only-scorable');
const pager = document.getElementById('pager');

function esc(value) {
  return String(value)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function card(product, result) {
  const [bg, ink] = result.scorable ? BAND_TOKEN[result.band] : ['var(--hairline)', 'var(--ink-soft)'];
  const tile = result.scorable
    ? `<span class="font-display text-h2 leading-none" style="color:${ink};font-variant-numeric:tabular-nums">${result.score}</span>`
    : `<span class="text-micro" style="color:${ink};text-align:center;line-height:1.2">Not<br>scored</span>`;
  /* The band pill carries the confidence with it, and always, not only when
     confidence is poor. A 72 built from three pillars and a full label and a
     72 built from an ingredient list alone are different claims wearing the
     same number, and until M18b the difference was stated on the product page
     and on the compare page while these cards printed the bare digit. The
     number is the part that travels: it is what gets scanned, remembered and
     repeated, and a caveat that stays behind on another page is a caveat that
     does not exist. Showing it only for low confidence would make its absence
     the claim, which is exactly the reading tenet 2 refuses. */
  const badge = result.scorable
    ? `<span class="inline-block text-micro px-2 rounded-pill mt-1" style="background:${bg};color:${ink};padding-top:2px;padding-bottom:2px">${result.bandLabel} · ${result.confidence} confidence</span>`
    : '<span class="inline-block text-micro px-2 rounded-pill mt-1" style="border:1px solid var(--hairline);color:var(--ink-soft);padding-top:2px;padding-bottom:2px">No ingredient list on record</span>';

  const meta = [product.brand, FORMAT_LABEL[product.format], product.quantity]
    .filter(Boolean).join(' · ');

  const ariaLabel = result.scorable
    ? `Score ${result.score}, ${result.bandLabel}, ${result.confidence} confidence`
    : 'Not scored';

  /* Photo left, score right, name between. The chevron that used to close the
     row is gone: the score tile now sits where it was, and two glyphs on the
     same edge of the same link is one more than the row needs. The whole row
     was always the link. */
  return `<li data-scorable="${result.scorable ? 'yes' : 'no'}">
    <a href="${SITE}product/?barcode=${esc(product.barcode)}"
       class="card-link items-center gap-4 bg-surface border border-hairline rounded-card p-4">
      ${thumbHtml(product.thumbUrl)}
      <div class="min-w-0 flex-1">
        <p class="text-ink font-medium text-small truncate">${esc(product.name)}</p>
        <p class="text-ink-soft text-micro">${esc(meta || 'Brand not recorded')}</p>
        ${badge}
      </div>
      <div class="w-14 h-14 rounded-card flex items-center justify-center shrink-0"
           style="background:${bg}" aria-label="${esc(ariaLabel)}">${tile}</div>
    </a>
  </li>`;
}

function setLabel(html) {
  label.innerHTML = html;
  label.hidden = !html;
}

function empty(title, body) {
  controls.hidden = true;
  pager.hidden = true;
  list.innerHTML = `<li style="list-style:none">
    <div class="text-center py-12">
      <p class="font-display text-h2 text-ink mb-3">${esc(title)}</p>
      <p class="text-small text-ink-soft" style="max-width:46ch;margin:0 auto">${body}</p>
    </div>
  </li>`;
}

/* ── The URL is the state ──
   Every control on this page writes to the query string and re-reads it, so a
   filtered page 3 of a brand is a link somebody can send. */
function readState() {
  const params = new URLSearchParams(window.location.search);
  return {
    q: (params.get('q') || '').trim(),
    brand: (params.get('brand') || '').trim(),
    page: Math.max(1, parseInt(params.get('page') || '1', 10) || 1),
    scorableOnly: params.get('only') === 'scorable',
  };
}

function urlFor(state) {
  const params = new URLSearchParams();
  if (state.q) params.set('q', state.q);
  if (state.brand) params.set('brand', state.brand);
  if (state.page > 1) params.set('page', String(state.page));
  if (state.scorableOnly) params.set('only', 'scorable');
  const qs = params.toString();
  return SITE + 'search/' + (qs ? '?' + qs : '');
}

function go(state) {
  window.location.href = urlFor(state);
}

function renderPager(state, total, pageSize, shown) {
  const lastPage = Math.max(1, Math.ceil(total / pageSize));
  if (lastPage <= 1) { pager.hidden = true; return; }

  /* The unavailable direction is a span rather than a link, and it is told
     apart from the live one by having no border and no card: it does not need
     to be faded as well. It used to carry opacity .45, which put it at 2.11:1
     and made "Previous" on page 1 the one piece of text on the site below AA.
     WCAG exempts genuinely inactive controls; this is a span of text, and
     dimming text is not what makes a control read as unavailable anyway. */
  const button = (targetPage, text, disabled) => (disabled
    ? `<span class="text-small text-ink-soft" style="padding:8px 14px">${text}</span>`
    : `<a href="${esc(urlFor({ ...state, page: targetPage }))}"
          class="btn-link text-small text-ink border border-hairline rounded-card"
          style="padding:8px 14px">${text}</a>`);

  pager.innerHTML = `
    ${button(state.page - 1, '&larr; Previous', state.page <= 1)}
    <span class="text-small text-ink-soft">Page ${state.page} of ${lastPage}</span>
    ${button(state.page + 1, 'Next &rarr;', state.page >= lastPage || !shown)}`;
  pager.hidden = false;
}

async function run() {
  const state = readState();
  if (input) input.value = state.q;
  if (onlyScorable) onlyScorable.checked = state.scorableOnly;

  const brandName = state.brand ? brandDisplayName(state.brand) : '';
  if (brandName) {
    heading.textContent = brandName;
    heading.hidden = false;
    document.title = `${brandName}: Cat Food Center`;
  } else {
    heading.hidden = true;
  }

  if (!state.q && !state.brand) {
    setLabel('');
    controls.hidden = true;
    pager.hidden = true;
    empty('Search the catalogue',
      `Type a brand or product name above, or <a href="${SITE}brands/" class="text-accent">browse by brand</a>. `
      + 'Results come from Open Pet Food Facts, a community-maintained database, and are scored live.');
    return;
  }

  setLabel('Searching…');
  list.innerHTML = '';

  if (state.scorableOnly) {
    await runFiltered(state, brandName);
    return;
  }

  const [{ products, total, pageSize, error }, kb] = await Promise.all([
    searchProducts(state.q, { page: state.page, brand: state.brand }),
    loadKnowledgeBase(),
  ]);

  if (error) {
    setLabel('');
    empty('Could not reach the database', esc(error) + ' Check your connection and try again.');
    return;
  }
  if (!products.length) {
    setLabel('');
    const what = brandName ? `${esc(brandName)} products` : `&ldquo;${esc(state.q)}&rdquo;`;
    empty(state.page > 1 ? 'No more results' : 'No matches',
      state.page > 1
        ? `There is no page ${state.page} for this search. <a href="${esc(urlFor({ ...state, page: 1 }))}" class="text-accent">Back to the first page</a>.`
        : `Nothing in the cat food catalogue matches ${what}. The database is far from complete, so a miss says more about its coverage than about the product.`);
    return;
  }

  // Relevance order is the API's, and it is kept. Scoring adds a badge, not a
  // rank.
  const scored = products.map((product) => ({ product, result: scoreProduct(product, kb) }));
  const scorableCount = scored.filter((s) => s.result.scorable).length;

  controls.hidden = false;
  list.innerHTML = scored.map(({ product, result }) => card(product, result)).join('');

  const first = (state.page - 1) * pageSize + 1;
  const last = first + scored.length - 1;
  setLabel(`Results ${first}&ndash;${last} of ${total} for ${subjectOf(state, brandName)}`
    + ` · ${scorableCount} of these can be scored`);

  renderPager(state, total, pageSize, scored.length);
}

function subjectOf(state, brandName) {
  return brandName ? esc(brandName) : `&ldquo;${esc(state.q)}&rdquo;`;
}

/* ── The scorable-only path ──

   Fetches SCAN_PAGES pages at once, scores everything it got, and paginates
   the scorable ones locally. Paginating locally is what keeps `page` in the
   URL meaning the same thing in both modes: the page of the list in front of
   you. It also means page 3 of a filtered search costs the same as page 1
   rather than re-scanning further each time.

   Deduplicated by barcode, because paged API results can repeat a record and
   a duplicate card would inflate the count this page is trying to state
   accurately. */
async function runFiltered(state, brandName) {
  const [pages, kb] = await Promise.all([
    Promise.all(Array.from({ length: SCAN_PAGES }, (_, i) =>
      searchProducts(state.q, { page: i + 1, brand: state.brand }))),
    loadKnowledgeBase(),
  ]);

  const failed = pages.find((p) => p.error);
  if (failed) {
    setLabel('');
    empty('Could not reach the database', esc(failed.error) + ' Check your connection and try again.');
    return;
  }

  const total = pages[0].total;
  const pageSize = pages[0].pageSize;
  const seen = new Map();
  for (const p of pages) {
    for (const product of p.products) {
      if (!seen.has(product.barcode)) seen.set(product.barcode, product);
    }
  }
  const scanned = seen.size;
  const subject = subjectOf(state, brandName);

  if (!scanned) {
    setLabel('');
    const what = brandName ? `${esc(brandName)} products` : `&ldquo;${esc(state.q)}&rdquo;`;
    empty('No matches',
      `Nothing in the cat food catalogue matches ${what}. The database is far from complete, `
      + 'so a miss says more about its coverage than about the product.');
    return;
  }

  const scorable = [...seen.values()]
    .map((product) => ({ product, result: scoreProduct(product, kb) }))
    .filter((s) => s.result.scorable);

  // "Everything there was" versus "as far as we looked" are different claims,
  // and the page has to know which one it is making.
  const exhausted = scanned >= total;
  const scope = exhausted
    ? `all ${total} results for ${subject}`
    : `the first ${scanned} of ${total} results for ${subject}`;

  controls.hidden = false;

  if (!scorable.length) {
    pager.hidden = true;
    setLabel('');
    empty('None of these can be scored',
      `No product in ${scope} carries an ingredient list, so none can be scored. `
      + (exhausted
        ? 'That is the whole of what the database holds for this search.'
        : 'There may be scorable products further down the results; this page checked the first '
          + `${scanned}, because whether a product can be scored is only knowable after fetching it.`)
      + ` <a href="${esc(urlFor({ ...state, scorableOnly: false }))}" class="text-accent">Show everything</a>.`);
    // empty() hides the controls, which is right for a failed search and wrong
    // here: the visitor's next move is almost certainly to untick the box, and
    // it has to be there to untick.
    controls.hidden = false;
    return;
  }

  const lastPage = Math.max(1, Math.ceil(scorable.length / pageSize));
  const page = Math.min(state.page, lastPage);
  const slice = scorable.slice((page - 1) * pageSize, page * pageSize);

  list.innerHTML = slice.map(({ product, result }) => card(product, result)).join('');

  const first = (page - 1) * pageSize + 1;
  setLabel(`Showing ${first}&ndash;${first + slice.length - 1} of the ${scorable.length} `
    + `products in ${scope} that can be scored`);

  renderPager({ ...state, page }, scorable.length, pageSize, slice.length);

  // On the last page, say the scan stopped. The label already says it, but by
  // the time somebody has read to the bottom of the results they have earned a
  // reminder that "no more" means "no more that were looked at".
  if (!exhausted && page === lastPage) {
    pager.insertAdjacentHTML('afterend',
      `<p class="text-micro text-ink-soft" style="max-width:52ch;margin:14px auto 0;text-align:center">
         That is every scorable product in the first ${scanned} results. The search matched
         ${total} in all, and the rest were not checked.
         <a href="${esc(urlFor({ ...state, scorableOnly: false }))}" class="text-accent">Show everything</a>
         to page through them yourself.
       </p>`);
  }
}

if (onlyScorable) {
  // Filtering changes which results are shown, so it belongs in the URL and
  // starts again from page 1: page 3 of an unfiltered list has no meaning once
  // the list changes.
  onlyScorable.addEventListener('change', () => {
    const state = readState();
    go({ ...state, scorableOnly: onlyScorable.checked, page: 1 });
  });
}

run().catch((err) => {
  setLabel('');
  empty('Something went wrong', esc(err.message));
});
