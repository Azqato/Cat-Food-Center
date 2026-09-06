/* ==========================================================================
   submit.html: what to do when a product is not in the database.

   There is no submission queue of our own, and that is a decision rather than
   a gap. A static site cannot accept writes (docs/PRD.md section 16.2),
   but the more important reason is that we do not want to hold a private copy
   of the catalogue: every score here is derived from Open Pet Food Facts, so a
   product added *there* works here, in the next tool built on it, and for the
   next person who scans the same tin. A private queue would fork the data and
   make this site the bottleneck for its own corrections.

   So this page's job is to hand off well: say where the data goes, name the
   two panels that actually decide whether a product can be scored, and rule
   out the most common false alarm (a mistyped barcode) before sending
   anybody off to fill in a form.
   ========================================================================== */
import { isValidBarcode } from './scanner.js';
import { fetchProduct } from './opff.js';

const ADD_URL = 'https://world.openpetfoodfacts.org/cgi/product.pl?type=add&code=';

const barcodeLine = document.getElementById('barcode-line');
const addLink = document.getElementById('add-link');
const verifyForm = document.getElementById('verify-form');
const verifyInput = document.getElementById('verify-input');
const verifyResult = document.getElementById('verify-result');

const barcode = (new URLSearchParams(window.location.search).get('barcode') || '').trim();

function esc(value) {
  return String(value)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

if (barcode) {
  barcodeLine.innerHTML = `Open Pet Food Facts has no record for barcode <code>${esc(barcode)}</code>. `;
  addLink.href = ADD_URL + encodeURIComponent(barcode);
  verifyInput.value = barcode;
  document.title = `Add ${barcode}: Cat Food Center`;
} else {
  // Reached directly rather than from a failed lookup.
  addLink.href = 'https://world.openpetfoodfacts.org/cgi/product.pl?type=add';
}

function say(text, tone) {
  verifyResult.textContent = text;
  verifyResult.style.color = tone === 'bad' ? 'var(--bad)'
    : tone === 'good' ? 'var(--excellent)' : 'var(--ink-soft)';
  verifyResult.hidden = false;
}

verifyForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const code = verifyInput.value.replace(/[\s-]/g, '');
  if (!code) return;

  if (!isValidBarcode(code)) {
    // The single most likely explanation for "not in the database", and the
    // only one the visitor can fix in five seconds. Worth ruling out before
    // sending anyone off to photograph a tin.
    say(/^\d+$/.test(code)
      ? 'That number fails its own check digit, so one of the digits is probably wrong. '
        + 'Barcodes carry a check digit precisely so a single mistyped number is detectable.'
      : 'A barcode is digits only, 8 to 13 of them.', 'bad');
    return;
  }

  say('Checking the database…');
  const { found, error } = await fetchProduct(code);
  if (error) {
    say(error + ' The barcode itself checks out, so this is a connection problem rather than a missing product.', 'bad');
    return;
  }
  if (found) {
    // Worth catching: the visitor may have arrived here from a typo, or the
    // record may have been added since.
    say('That product is in the database after all.', 'good');
    verifyResult.innerHTML += ` <a href="./product.html?barcode=${esc(code)}" class="text-accent">Open its page</a>.`;
    return;
  }

  say('The barcode checks out and there is no record for it. It is genuinely missing, worth adding.', null);
  addLink.href = ADD_URL + encodeURIComponent(code);
  if (!barcode) barcodeLine.innerHTML = `Open Pet Food Facts has no record for barcode <code>${esc(code)}</code>. `;
});

verifyInput.addEventListener('input', () => { verifyResult.hidden = true; });
