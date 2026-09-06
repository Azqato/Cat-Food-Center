/* ==========================================================================
   search.html — live text search against Open Pet Food Facts.

   Results are scored on the fly with the same engine the product page uses,
   so a card and a product page can never disagree.

   Scoring in a list is the interesting constraint. docs/DATA-COVERAGE.md found
   that most records are too thin to score, and a list of "not scored" tiles
   would be useless. So results are ordered by whether they could be scored at
   all, then by score — the useful ones first, the rest still reachable.
   ========================================================================== */
import { searchProducts } from './opff.js';
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

  return `<li>
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

function setLabel(text) {
  label.textContent = text;
  label.hidden = !text;
}

function empty(heading, body) {
  list.innerHTML = `<li style="list-style:none">
    <div class="text-center py-12">
      <p class="font-display text-h2 text-ink mb-3">${esc(heading)}</p>
      <p class="text-small text-ink-soft" style="max-width:46ch;margin:0 auto">${body}</p>
    </div>
  </li>`;
}

async function run(query) {
  if (!query) {
    setLabel('');
    empty('Search the catalogue',
      'Type a brand or product name above. Results come from Open Pet Food Facts, a community-maintained database, and are scored live.');
    return;
  }

  setLabel('Searching…');
  list.innerHTML = '';

  const [{ products, total, error }, kb] = await Promise.all([
    searchProducts(query),
    loadKnowledgeBase(),
  ]);

  if (error) {
    setLabel('');
    empty('Could not reach the database', esc(error) + ' Check your connection and try again.');
    return;
  }
  if (!products.length) {
    setLabel('');
    empty('No matches',
      `Nothing in the cat food catalogue matches &ldquo;${esc(query)}&rdquo;. The database is far from complete, so a miss says more about its coverage than about the product.`);
    return;
  }

  // Scorable results first, then by score. A page of "not scored" tiles would
  // be technically accurate and practically useless.
  const scored = products
    .map((product) => ({ product, result: scoreProduct(product, kb) }))
    .sort((a, b) => {
      if (a.result.scorable !== b.result.scorable) return a.result.scorable ? -1 : 1;
      return (b.result.score || 0) - (a.result.score || 0);
    });

  const scorableCount = scored.filter((s) => s.result.scorable).length;
  setLabel(
    `${products.length} of ${total} result${total === 1 ? '' : 's'} for “${query}” · `
    + `${scorableCount} could be scored`);

  list.innerHTML = scored.map(({ product, result }) => card(product, result)).join('');
}

const query = (new URLSearchParams(window.location.search).get('q') || '').trim();
if (input) input.value = query;
run(query).catch((err) => {
  setLabel('');
  empty('Something went wrong', esc(err.message));
});
