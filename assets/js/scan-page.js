/* ==========================================================================
   scan.html: camera, permission, and the manual fallback.

   The scanner itself lives in scanner.js. This file is the part that has to be
   kind about failure, which is most of the work: a camera feature fails for
   half a dozen unrelated reasons: no HTTPS, no camera, permission denied,
   another app holding the device, a browser without the API, and each one
   needs a different sentence and a different suggested next step. A single
   "Could not start camera" would be accurate and useless.

   The manual barcode field is not a consolation prize. It is always visible,
   it works everywhere, and on a desktop browser it is the primary path.
   ========================================================================== */
import { startScanner, unsupportedReason, isValidBarcode } from './scanner.js';

const idle = document.getElementById('scan-idle');
const live = document.getElementById('scan-live');
const video = document.getElementById('scan-video');
const status = document.getElementById('scan-status');
const startBtn = document.getElementById('scan-start');
const stopBtn = document.getElementById('scan-stop');
const message = document.getElementById('scan-message');
const messageTitle = document.getElementById('scan-message-title');
const messageBody = document.getElementById('scan-message-body');
const manualForm = document.getElementById('manual-form');
const manualInput = document.getElementById('manual-input');
const manualError = document.getElementById('manual-error');

let active = null;

function show(el, visible) { el.hidden = !visible; }

function notice(title, body) {
  messageTitle.textContent = title;
  messageBody.textContent = body;
  show(message, true);
}

function toProduct(code) {
  window.location.href = `./product.html?barcode=${encodeURIComponent(code)}`;
}

/**
 * Turn a getUserMedia rejection into something worth reading.
 *
 * The DOMException names are the only reliable signal here, the messages
 * differ per browser: and the distinction that matters most to the visitor is
 * "you said no" versus "something else is wrong", because only the first one is
 * theirs to undo.
 */
function explain(err) {
  switch (err && err.name) {
    case 'NotAllowedError':
    case 'SecurityError':
      return ['Camera permission was declined',
        'Nothing was captured. If you changed your mind, allow camera access for this site in '
        + 'your browser settings and start again: or type the barcode number in below.'];
    case 'NotFoundError':
    case 'OverconstrainedError':
      return ['No camera found',
        'This device does not appear to have a camera the browser can use. Type the barcode '
        + 'number in below, or search by name.'];
    case 'NotReadableError':
      return ['The camera is in use',
        'Another app or tab is holding the camera. Close it and try again, or type the '
        + 'barcode number in below.'];
    default:
      return ['The camera could not be started',
        (err && err.message ? err.message : 'An unknown error occurred.')
        + ' You can type the barcode number in below instead.'];
  }
}

async function start() {
  show(message, false);
  const blocked = unsupportedReason();
  if (blocked) {
    notice('Scanning is not available here', blocked
      + ' You can still type the barcode number in below.');
    return;
  }

  startBtn.disabled = true;
  startBtn.textContent = 'Starting…';
  try {
    active = await startScanner(video, {
      onResult: (code) => {
        status.textContent = `Found ${code}. Opening…`;
        toProduct(code);
      },
      onError: (err) => {
        stop();
        const [title, body] = explain(err);
        notice(title, body);
      },
      onDecoder: (name) => {
        // Named on purpose. Which decoder ran is the first thing worth knowing
        // when someone reports that scanning is slow on their phone.
        status.textContent = name === 'BarcodeDetector'
          ? 'Scanning… hold the barcode inside the box.'
          : 'Scanning… hold the barcode inside the box. (Using the fallback decoder, which is slower.)';
      },
    });
    show(idle, false);
    show(live, true);
    stopBtn.focus();
  } catch (err) {
    const [title, body] = explain(err);
    notice(title, body);
  } finally {
    startBtn.disabled = false;
    startBtn.textContent = 'Start camera';
  }
}

function stop() {
  if (active) { active.stop(); active = null; }
  show(live, false);
  show(idle, true);
  status.textContent = '';
}

startBtn.addEventListener('click', start);
stopBtn.addEventListener('click', () => { stop(); startBtn.focus(); });

/* Leaving the page, or backgrounding the tab, must release the camera. A tab
   left holding a camera in the background is both a battery cost and, more to
   the point, a thing the visitor did not agree to. */
document.addEventListener('visibilitychange', () => { if (document.hidden) stop(); });
window.addEventListener('pagehide', stop);

manualForm.addEventListener('submit', (event) => {
  event.preventDefault();
  const code = manualInput.value.replace(/[\s-]/g, '');
  if (!code) return;
  if (!isValidBarcode(code)) {
    // Checked before navigating, because a barcode that fails its own check
    // digit is a typo, and "no product found" would send the visitor looking
    // for a gap in the database instead of at their own typing.
    manualError.textContent = /^\d+$/.test(code)
      ? 'That number does not check out as a barcode, one of the digits is probably wrong. '
        + 'Barcodes carry a check digit, so a single mistyped number is detectable.'
      : 'A barcode is digits only, 8 to 13 of them.';
    show(manualError, true);
    manualInput.focus();
    return;
  }
  show(manualError, false);
  toProduct(code);
});

manualInput.addEventListener('input', () => show(manualError, false));

/* Say up front when the camera cannot work, rather than after a click that
   goes nowhere. The manual field below is then plainly the thing to use. */
const blocked = unsupportedReason();
if (blocked) {
  startBtn.disabled = true;
  startBtn.style.opacity = '.6';
  startBtn.style.cursor = 'not-allowed';
  notice('Scanning is not available here', blocked + ' Type the barcode number in below instead.');
}
