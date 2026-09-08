/* ==========================================================================
   /compare/: two products side by side.

   ── The problem this page has to solve honestly ──

   Two scores are not always comparable. A 72 derived from all three pillars
   and a 72 derived from ingredients alone are different claims wearing the
   same number, and putting them next to each other in a big font invites a
   comparison the data does not support. docs/PRD.md section 12 makes this the
   normal case rather than an edge case: only about a fifth of products carry
   enough data to score all three pillars.

   So this page never declares a winner on the overall score. It compares
   pillar by pillar, and only where *both* products have that pillar; anywhere
   they were scored on different pillars it says so before showing anything
   else. The comparison people actually want (this food versus that food) is
   still there, just not overstated.

   Figures are shown on a dry-matter basis, because that is the only way a wet
   food at 11% protein and a dry food at 32% can be read against each other.
   ========================================================================== */
import { SITE } from './site.js';
import { fetchProduct } from './opff.js';
import { scoreProduct, loadKnowledgeBase, toDryMatter, carbsByDifference } from './scoring.js';
import { recentProducts } from './history.js';
import { isValidBarcode } from './scanner.js';
import { thumbHtml } from './thumb.js';

const BAND_TOKEN = {
  excellent: ['var(--chip-excellent-bg)', 'var(--chip-excellent-ink)'],
  good: ['var(--chip-good-bg)', 'var(--chip-good-ink)'],
  poor: ['var(--chip-poor-bg)', 'var(--chip-poor-ink)'],
  bad: ['var(--chip-bad-bg)', 'var(--chip-bad-ink)'],
};

const PILLAR_LABEL = {
  nutrition: 'Nutrition',
  additives: 'Additives & safety',
  transparency: 'Transparency',
};

const FORMAT_LABEL = { wet: 'Wet', dry: 'Dry', 'semi-moist': 'Semi-moist', treat: 'Treat' };

const pickers = document.getElementById('pickers');
const notice = document.getElementById('compare-notice');
const body = document.getElementById('compare-body');

function esc(value) {
  return String(value)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

const params = new URLSearchParams(window.location.search);
const slots = [params.get('a') || '', params.get('b') || ''];

/* ── Pickers ── */

function renderPickers() {
  const recent = recentProducts();
  pickers.innerHTML = ['a', 'b'].map((key, i) => {
    const options = recent.map((r) => `<option value="${esc(r.barcode)}"${
      r.barcode === slots[i] ? ' selected' : ''}>${esc(r.name || r.barcode)}</option>`).join('');
    return `<div>
      <label class="cmp-label" for="pick-${key}" style="display:block;margin-top:0">Product ${key.toUpperCase()}</label>
      ${recent.length ? `<select id="pick-${key}" data-slot="${i}"
        class="w-full border border-hairline rounded-card px-3 py-3 text-small text-ink bg-surface"
        style="margin-bottom:8px">
        <option value="">Choose a product you have viewed…</option>${options}
      </select>` : ''}
      <input type="text" inputmode="numeric" data-slot="${i}" data-barcode-input
        value="${esc(slots[i])}" placeholder="…or enter a barcode"
        aria-label="Barcode for product ${key.toUpperCase()}"
        class="w-full border border-hairline rounded-card px-3 py-3 text-small text-ink bg-surface" />
    </div>`;
  }).join('');

  pickers.querySelectorAll('select').forEach((el) => {
    el.addEventListener('change', () => setSlot(Number(el.dataset.slot), el.value));
  });
  pickers.querySelectorAll('[data-barcode-input]').forEach((el) => {
    el.addEventListener('change', () => setSlot(Number(el.dataset.slot), el.value.replace(/[\s-]/g, '')));
  });
}

function setSlot(index, value) {
  slots[index] = value;
  // The URL carries the comparison, so it can be shared and reloaded. There is
  // no router here: replaceState is the whole of it.
  const next = new URLSearchParams();
  if (slots[0]) next.set('a', slots[0]);
  if (slots[1]) next.set('b', slots[1]);
  const qs = next.toString();
  window.history.replaceState({}, '', qs ? `?${qs}` : window.location.pathname);
  run();
}

/* ── Rendering ── */

function scoreTile(entry) {
  if (!entry) return '<div class="cmp-cell"><p class="text-small text-ink-soft">Not selected.</p></div>';
  if (entry.error) {
    return `<div class="cmp-cell"><p class="text-small" style="color:var(--bad-ink)">${esc(entry.error)}</p></div>`;
  }
  const { product, result } = entry;
  const [bg, ink] = result.scorable ? BAND_TOKEN[result.band] : ['var(--hairline)', 'var(--ink-soft)'];
  const meta = [product.brand, FORMAT_LABEL[product.format], product.quantity].filter(Boolean).join(' · ');
  /* The photo goes first and the score tile keeps its place beside it. This
     column is narrow and stacks below 700px, so pushing the score to the far
     edge the way a search row does would leave the two halves of one product
     at opposite ends of a phone screen. */
  return `<div class="cmp-cell">
    <div class="flex items-center gap-3">
      ${thumbHtml(product.thumbUrl)}
      <div class="w-14 h-14 rounded-card flex items-center justify-center shrink-0" style="background:${bg}">
        ${result.scorable
    ? `<span class="font-display text-h2 leading-none" style="color:${ink};font-variant-numeric:tabular-nums">${result.score}</span>`
    : `<span class="text-micro" style="color:${ink};text-align:center;line-height:1.2">Not<br>scored</span>`}
      </div>
      <div class="min-w-0">
        <a href="${SITE}product/?barcode=${esc(product.barcode)}" class="text-ink font-medium text-small" style="text-decoration:none">${esc(product.name)}</a>
        <p class="text-ink-soft text-micro">${esc(meta || 'Brand not recorded')}</p>
        ${result.scorable ? `<p class="text-micro" style="color:${ink === '#FFFFFF' ? 'var(--ink-soft)' : 'var(--ink-soft)'}">${esc(result.bandLabel)} · ${esc(result.confidence)} confidence</p>` : ''}
      </div>
    </div>
  </div>`;
}

/**
 * A row comparing one number.
 *
 * `better` is 'high' or 'low' or null. Where it is null, or where either side
 * is missing; nothing is highlighted, because an arrow pointing at the only
 * product that happened to publish a figure would read as a verdict on the
 * food rather than on the database.
 */
function numberRow(label, a, b, unit, better, note, decimals = 1) {
  const fmt = (v) => (typeof v === 'number' ? `${v.toFixed(decimals)}${unit}` : 'not published');
  let winner = null;
  if (better && typeof a === 'number' && typeof b === 'number' && a !== b) {
    winner = (better === 'high') === (a > b) ? 0 : 1;
  }
  const cell = (v, i) => `<div class="cmp-cell${winner === i ? ' cmp-better' : ''}">
    <span class="text-ink font-medium text-small" style="font-variant-numeric:tabular-nums">${fmt(v)}</span>
  </div>`;
  return `<p class="cmp-label">${esc(label)}${note ? ` <span style="text-transform:none;letter-spacing:0">· ${esc(note)}</span>` : ''}</p>
    <div class="cmp-row">${cell(a, 0)}${cell(b, 1)}</div>`;
}

function dryMatter(product) {
  const n = product.nutrition || {};
  const proteinDM = toDryMatter(n.crudeProteinPct, n.moisturePct);
  const fatDM = toDryMatter(n.crudeFatPct, n.moisturePct);
  const fibreDM = toDryMatter(n.crudeFibrePct, n.moisturePct);
  const ashDM = toDryMatter(n.ashPct, n.moisturePct);
  return {
    proteinDM, fatDM, fibreDM, ashDM,
    carbsDM: carbsByDifference({ proteinDM, fatDM, fibreDM, ashDM }),
    moisture: n.moisturePct,
  };
}

function renderComparison(entries) {
  const [x, y] = entries;
  const px = x.product;
  const py = y.product;
  const dx = dryMatter(px);
  const dy = dryMatter(py);

  const shared = (x.result.pillarsUsed || []).filter((p) => (y.result.pillarsUsed || []).includes(p));
  const onlyX = (x.result.pillarsUsed || []).filter((p) => !shared.includes(p));
  const onlyY = (y.result.pillarsUsed || []).filter((p) => !shared.includes(p));

  const pillarRows = shared.map((key) => {
    const a = x.result.pillars[key].score;
    const b = y.result.pillars[key].score;
    return numberRow(PILLAR_LABEL[key], a, b, '', 'high', null, 0);
  }).join('');

  const noDryMatter = [dx, dy].some((d) => typeof d.proteinDM !== 'number');

  return `
    <p class="cmp-label" style="margin-top:24px">Pillars both products could be scored on</p>
    ${shared.length ? pillarRows : '<p class="text-small text-ink-soft">None in common, so there is nothing here that can be compared like for like.</p>'}
    ${(onlyX.length || onlyY.length) ? `<p class="text-ink-soft text-micro" style="margin-top:8px">
      Not compared, because only one product had the data: ${
  esc([...onlyX, ...onlyY].map((k) => PILLAR_LABEL[k]).join(', '))}.</p>` : ''}

    <p class="cmp-label" style="margin-top:28px">Guaranteed analysis, dry-matter basis</p>
    ${noDryMatter
    ? `<p class="text-small text-ink-soft">A dry-matter comparison needs a protein figure and a moisture figure from both products, and ${
      typeof dx.proteinDM !== 'number' && typeof dy.proteinDM !== 'number' ? 'neither has both' : 'one of them does not'
    }. Comparing the as-fed percentages instead would make the wetter food look worse for containing water.</p>`
    : [
      numberRow('Protein', dx.proteinDM, dy.proteinDM, '%', 'high', 'AAFCO adult minimum 26%'),
      numberRow('Fat', dx.fatDM, dy.fatDM, '%', null, 'AAFCO adult minimum 9%; more is not simply better'),
      numberRow('Carbohydrate by difference', dx.carbsDM, dy.carbsDM, '%', 'low'),
      numberRow('Moisture, as fed', dx.moisture, dy.moisture, '%', 'high', 'cats under-drink; water in food counts'),
    ].join('')}

    <p class="cmp-label" style="margin-top:28px">First ingredient</p>
    <div class="cmp-row">
      <div class="cmp-cell"><span class="text-small text-ink">${esc(px.ingredients[0] || 'not listed')}</span></div>
      <div class="cmp-cell"><span class="text-small text-ink">${esc(py.ingredients[0] || 'not listed')}</span></div>
    </div>

    <p class="cmp-label" style="margin-top:28px">Flagged additives</p>
    <div class="cmp-row">
      ${[x, y].map((e) => `<div class="cmp-cell"><span class="text-small text-ink-soft">${
    e.result.flaggedAdditives && e.result.flaggedAdditives.length
      ? esc(e.result.flaggedAdditives.map((f) => `${f.name} (Tier ${f.tier})`).join(', '))
      : 'None matched'}</span></div>`).join('')}
    </div>

    <p class="text-ink-soft text-micro" style="margin-top:24px">
      Highlighted cells mark the higher or lower figure, not a verdict; a single number is
      not a food. Where only one product publishes a figure, neither is highlighted, because that
      would be a comment on the database rather than on the food.
      <a href="${SITE}methodology/" class="text-accent">Full methodology</a>.
    </p>`;
}

/* ── Loading ── */

async function load(barcode, kb) {
  if (!barcode) return null;
  if (!isValidBarcode(barcode)) {
    return { error: `${barcode} is not a valid barcode; it fails its own check digit.` };
  }
  const { found, product, error } = await fetchProduct(barcode);
  if (error) return { error };
  if (!found) return { error: `No record for ${barcode}. It may be missing from the database.` };
  return { product, result: scoreProduct(product, kb) };
}

async function run() {
  notice.innerHTML = '';
  if (!slots[0] || !slots[1]) {
    body.innerHTML = `<p class="text-small text-ink-soft" style="margin-top:12px">
      Choose two products above. Products you have opened before are listed; anything else can be
      entered by barcode.</p>`;
    return;
  }

  body.innerHTML = '<p class="text-small text-ink-soft" style="margin-top:12px">Loading…</p>';
  const kb = await loadKnowledgeBase();
  const entries = await Promise.all(slots.map((code) => load(code, kb)));

  const header = `<div class="cmp-row" style="margin-top:8px">${entries.map(scoreTile).join('')}</div>`;

  if (entries.some((e) => !e || e.error)) {
    body.innerHTML = header;
    return;
  }
  if (entries.some((e) => !e.result.scorable)) {
    body.innerHTML = header + `<p class="text-small text-ink-soft" style="margin-top:16px">
      One of these has no ingredient list on record, so it cannot be scored at all and there is
      nothing to compare it on. That is a gap in the database, not a finding about the food.</p>`;
    return;
  }

  /* The honesty check, before anything else is shown. Two scores computed from
     different pillars are different claims wearing the same number, and this
     page must not let a big number invite a comparison the data cannot carry. */
  const usedX = entries[0].result.pillarsUsed.slice().sort().join(',');
  const usedY = entries[1].result.pillarsUsed.slice().sort().join(',');
  if (usedX !== usedY) {
    notice.innerHTML = `<div role="status" style="background:var(--warn-bg);border-left:4px solid var(--poor);border-radius:8px;padding:12px 16px">
      <p class="text-small" style="color:var(--warn-ink);margin:0">
        These two scores were worked out from different pillars, so the overall numbers are not
        directly comparable: they are answers to slightly different questions. Compare the
        individual pillars below instead.
      </p></div>`;
  }

  body.innerHTML = header + renderComparison(entries);
}

renderPickers();
run().catch((err) => {
  body.innerHTML = `<p class="text-small" style="color:var(--bad-ink)">${esc(err.message)}</p>`;
});
