/* ==========================================================================
   brands.html: every brand in the cat food category, biggest first.

   This page exists because free-text search is the wrong primary tool for this
   database. The records are thin and inconsistently named, brands stored as
   numeric ids, product names left untranslated, "fancy feast" filed under the
   brand "fancy": so typing a product name is the hardest possible way to find
   something. Picking a brand from a list is the easiest, and the brand facet is
   the one axis Open Pet Food Facts indexes well.

   The filter box here is deliberately client-side. The whole brand list is a
   single request and a few hundred entries, so filtering it locally is instant
   and works offline once cached, where a round trip per keystroke would be
   neither.
   ========================================================================== */
import { fetchBrands, brandTagExpression } from './opff.js';

const listEl = document.getElementById('brand-list');
const filterEl = document.getElementById('brand-filter');
const countEl = document.getElementById('brand-count');

let allBrands = [];

function esc(value) {
  return String(value)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function tile(brand) {
  const expression = brandTagExpression(brand);
  const products = brand.count === 1 ? '1 product' : `${brand.count} products`;
  return `<li>
    <a href="./search.html?brand=${encodeURIComponent(expression)}"
       class="card-link items-center justify-between gap-3 bg-surface border border-hairline rounded-card px-4 py-3">
      <span class="text-ink text-small font-medium truncate">${esc(brand.name)}</span>
      <span class="text-ink-soft text-micro shrink-0">${products}</span>
    </a>
  </li>`;
}

function render(brands) {
  // Whatever the outcome, the list is no longer waiting, and the height it
  // reserved to keep the page from jumping is no longer wanted.
  listEl.classList.remove('is-loading');
  if (!brands.length) {
    listEl.innerHTML = `<li style="list-style:none" class="text-small text-ink-soft py-6">
      No brand matches that. The list holds every brand with more than one cat food on record.
    </li>`;
    countEl.textContent = '';
    return;
  }
  listEl.innerHTML = brands.map(tile).join('');
  const total = brands.reduce((sum, b) => sum + b.count, 0);
  countEl.textContent = `${brands.length} brands · ${total} products`;
}

function applyFilter() {
  const needle = (filterEl.value || '').trim().toLowerCase();
  render(needle
    ? allBrands.filter((b) => b.name.toLowerCase().includes(needle))
    : allBrands);
}

async function load() {
  const { brands, error } = await fetchBrands();
  if (error) {
    listEl.innerHTML = `<li style="list-style:none" class="text-small text-ink-soft py-6">
      ${esc(error)} The brand list needs a connection the first time; after that it is cached on this device.
    </li>`;
    return;
  }
  allBrands = brands;
  applyFilter();
}

filterEl.addEventListener('input', applyFilter);
load().catch((err) => {
  listEl.innerHTML = `<li style="list-style:none" class="text-small text-ink-soft py-6">${esc(err.message)}</li>`;
});
