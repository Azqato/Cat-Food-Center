/* ==========================================================================
   index.html: the "Recently viewed" list.

   Read from this device's own storage (history.js). Until someone has looked
   at a product there is nothing to show, so the section removes itself rather
   than standing there empty: an empty list on a home page reads as something
   broken.
   ========================================================================== */
import { recentProducts, clearRecent } from './history.js';
import { thumbHtml } from './thumb.js';

const BAND_TOKEN = {
  excellent: ['var(--chip-excellent-bg)', 'var(--chip-excellent-ink)'],
  good: ['var(--chip-good-bg)', 'var(--chip-good-ink)'],
  poor: ['var(--chip-poor-bg)', 'var(--chip-poor-ink)'],
  bad: ['var(--chip-bad-bg)', 'var(--chip-bad-ink)'],
};

const section = document.getElementById('recent-section');
const list = document.getElementById('recent-list');
const clearBtn = document.getElementById('recent-clear');

function esc(value) {
  return String(value)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function card(entry) {
  const scored = typeof entry.score === 'number' && entry.band;
  const [bg, ink] = scored ? BAND_TOKEN[entry.band] || BAND_TOKEN.good : ['var(--hairline)', 'var(--ink-soft)'];
  const tile = scored
    ? `<span class="font-display text-h2 leading-none" style="color:${ink};font-variant-numeric:tabular-nums">${entry.score}</span>`
    : `<span class="text-micro" style="color:${ink};text-align:center;line-height:1.2">Not<br>scored</span>`;
  const badge = scored
    ? `<span class="inline-block text-micro px-2 rounded-pill mt-1" style="background:${bg};color:${ink};padding-top:2px;padding-bottom:2px">${esc(entry.bandLabel || '')}</span>`
    : '';

  /* Same row as a search result, deliberately: the two lists sit one scroll
     apart and a card that means the same thing should look the same. The photo
     is whatever was stored at the time of the visit, so an entry saved before
     M15b simply shows the placeholder. */
  return `<li>
    <a href="./product.html?barcode=${esc(entry.barcode)}"
       class="card-link items-center gap-4 bg-surface border border-hairline rounded-card p-4">
      ${thumbHtml(entry.thumbUrl)}
      <div class="min-w-0 flex-1">
        <p class="text-ink font-medium text-small truncate">${esc(entry.name || entry.barcode)}</p>
        <p class="text-ink-soft text-micro">${esc(entry.brand || 'Brand not recorded')}</p>
        ${badge}
      </div>
      <div class="w-14 h-14 rounded-card flex items-center justify-center shrink-0"
           style="background:${bg}" aria-label="${scored ? `Score ${entry.score}, ${esc(entry.bandLabel || '')}` : 'Not scored'}">${tile}</div>
    </a>
  </li>`;
}

function render() {
  const entries = recentProducts();
  if (!entries.length) {
    section.hidden = true;
    return;
  }
  section.hidden = false;
  list.innerHTML = entries.map(card).join('');
}

clearBtn.addEventListener('click', () => {
  clearRecent();
  render();
});

render();
