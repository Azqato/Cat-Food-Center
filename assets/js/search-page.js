/* ==========================================================================
   search.html: live search against Open Pet Food Facts, by text or by brand.

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

   ── Why the filter is honest about being partial ──

   The API cannot filter on scorability: whether a product can be scored is
   something only this engine knows, and it knows it only after fetching the
   record. So the filter hides cards on the page you are looking at rather than
   asking the database for a different page, and the label says exactly that.
   A filter that silently returned "3 results" for a query with 1571 matches
   would be lying about the database.
   ========================================================================== */
import { searchProducts, brandDisplayName } from './opff.js';
import { scoreProduct, loadKnowledgeBase } from './scoring.js';

const BAND_TOKEN = {
  excellent: ['var(--chip-excellent-bg)', 'var(--chip-excellent-ink)'],
  good: ['var(--chip-good-bg)', 'var(--chip-good-ink)'],
  poor: ['var(--chip-poor-bg)', 'var(--chip-poor-ink)'],
  bad: ['var(--chip-bad-bg)', 'var(--chip-bad-ink)'],
};

const FORMAT_LABEL = { wet: 'Wet', dry: 'Dry', 'semi-moist': 'Semi-moist', treat: 'Treat' };

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
  const badge = result.scorable
    ? `<span class="inline-block text-micro px-2 rounded-pill mt-1" style="background:${bg};color:${ink};padding-top:2px;padding-bottom:2px">${result.bandLabel}</span>`
    : '<span class="inline-block text-micro px-2 rounded-pill mt-1" style="border:1px solid var(--hairline);color:var(--ink-soft);padding-top:2px;padding-bottom:2px">No ingredient list on record</span>';

  const meta = [product.brand, FORMAT_LABEL[product.format], product.quantity]
    .filter(Boolean).join(' · ');

  const ariaLabel = result.scorable
    ? `Score ${result.score}, ${result.bandLabel}`
    : 'Not scored';

  return `<li data-scorable="${result.scorable ? 'yes' : 'no'}">
    <a href="./product.html?barcode=${esc(product.barcode)}"
       class="card-link items-center gap-4 bg-surface border border-hairline rounded-card p-4">
      <div class="w-14 h-14 rounded-card flex items-center justify-center shrink-0"
           style="background:${bg}" aria-label="${esc(ariaLabel)}">${tile}</div>
      <div class="min-w-0 flex-1">
        <p class="text-ink font-medium text-small truncate">${esc(product.name)}</p>
        <p class="text-ink-soft text-micro">${esc(meta || 'Brand not recorded')}</p>
        ${badge}
      </div>
      <svg aria-hidden="true" class="w-5 h-5 text-ink-soft shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/>
      </svg>
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
  return './search.html' + (qs ? '?' + qs : '');
}

function go(state) {
  window.location.href = urlFor(state);
}

function renderPager(state, total, pageSize, shown) {
  const lastPage = Math.max(1, Math.ceil(total / pageSize));
  if (lastPage <= 1) { pager.hidden = true; return; }

  const button = (targetPage, text, disabled) => (disabled
    ? `<span class="text-small text-ink-soft" style="padding:8px 14px;opacity:.45">${text}</span>`
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
      'Type a brand or product name above, or <a href="./brands.html" class="text-accent">browse by brand</a>. '
      + 'Results come from Open Pet Food Facts, a community-maintained database, and are scored live.');
    return;
  }

  setLabel('Searching…');
  list.innerHTML = '';

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
  const visible = state.scorableOnly ? scored.filter((s) => s.result.scorable) : scored;

  controls.hidden = false;
  list.innerHTML = visible.map(({ product, result }) => card(product, result)).join('');

  if (state.scorableOnly && !visible.length) {
    list.innerHTML = `<li style="list-style:none">
      <div class="text-center py-10">
        <p class="text-small text-ink-soft" style="max-width:46ch;margin:0 auto">
          None of the ${scored.length} results on this page carry an ingredient list, so none can be scored.
          Try the next page, or <a href="${esc(urlFor({ ...state, scorableOnly: false }))}" class="text-accent">show everything</a>.
        </p>
      </div></li>`;
  }

  const subject = brandName
    ? `${esc(brandName)}`
    : `&ldquo;${esc(state.q)}&rdquo;`;
  const first = (state.page - 1) * pageSize + 1;
  const last = first + scored.length - 1;
  setLabel(state.scorableOnly
    ? `Showing the ${visible.length} of ${scored.length} on this page that can be scored · `
      + `results ${first}&ndash;${last} of ${total} for ${subject}`
    : `Results ${first}&ndash;${last} of ${total} for ${subject} · ${scorableCount} of these can be scored`);

  renderPager(state, total, pageSize, scored.length);
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
