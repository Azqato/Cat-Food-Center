/* ==========================================================================
   Barcode scanning.

   The whole feature runs in the browser: camera frames never leave the device,
   and the only network call is the product lookup that any search would make
   anyway. This is what docs/PRD.md section 16.2 was written to establish, 
   scanning decomposes into camera access, decoding and lookup, and none of the
   three needs a server.

   Two decoders, in order of preference:

     1. `BarcodeDetector`, the platform API. Hardware-accelerated where it
        exists, no download, and on Android Chrome it is markedly faster than
        anything shipped as JavaScript.
     2. ZXing compiled to JavaScript, fetched from a CDN only when the platform
        API is missing. It costs a download, so it is never loaded speculatively.

   "In order of preference" undersells the second one. M17 measured the three
   engines directly: `BarcodeDetector` is absent from Gecko and from WebKit,
   not partial there. Every browser on iOS is WebKit, and tenet 7 says the
   phone in the aisle is the real use case, so for a large share of the people
   this feature exists for, ZXing is not the fallback. It is the whole feature.
   Treat its download cost and its failure modes accordingly, and see
   tools/check-engines.py, which decodes a known EAN-13 in all three.

   The hard constraint is the secure context. `getUserMedia` is unavailable
   outside HTTPS and localhost, which means testing over `http://<LAN-IP>` from
   a phone silently has no camera at all. GitHub Pages serves HTTPS, so
   production is fine; the failure is a local-development trap, and the page
   says so explicitly rather than showing a dead viewfinder.
   ========================================================================== */

/* EAN-13 and UPC-A cover essentially all retail food packaging. EAN-8 appears
   on small tins, and UPC-E on very small US packages. Restricting the format
   list makes decoding faster and, more usefully, stops the decoder reporting a
   QR code on the packaging as if it were the product's barcode. */
export const FORMATS = ['ean_13', 'ean_8', 'upc_a', 'upc_e'];

const ZXING_SRC = 'https://cdn.jsdelivr.net/npm/@zxing/library@0.21.3/umd/index.min.js';

/**
 * Why scanning cannot run here, or null if it can.
 *
 * Distinguishing these matters: "your browser has no camera API" and "this page
 * is not on HTTPS" produce the same silence from `getUserMedia`, and only one
 * of them is the visitor's problem.
 *
 * @returns {string | null}
 */
export function unsupportedReason() {
  if (!window.isSecureContext) {
    return 'Camera access needs a secure connection (HTTPS). This page is not on one, '
      + 'so the browser will not allow the camera. On the live site this does not happen.';
  }
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    return 'This browser does not offer camera access to web pages.';
  }
  return null;
}

/**
 * Expand a zero-suppressed UPC-E code to its full UPC-A form.
 *
 * UPC-E is UPC-A with runs of zeros squeezed out, and the last data digit says
 * where they were. Its check digit is computed over the *expanded* code, so a
 * UPC-E cannot be checksum-validated in place: without this, every 8-digit
 * UPC-E would be judged by the EAN-8 rule, fail, and be discarded in silence.
 * The scanner would appear to simply never see small US packages.
 *
 * @returns {string | null} the 12-digit UPC-A, or null if this is not a UPC-E
 */
export function expandUpcE(code) {
  if (!/^\d{8}$/.test(code)) return null;
  const system = code[0];
  if (system !== '0' && system !== '1') return null;   // only 0 and 1 are defined
  const d = code.slice(1, 7);
  const check = code[7];
  const last = d[5];
  let body;
  if ('012'.includes(last)) body = `${d[0]}${d[1]}${last}0000${d[2]}${d[3]}${d[4]}`;
  else if (last === '3') body = `${d[0]}${d[1]}${d[2]}00000${d[3]}${d[4]}`;
  else if (last === '4') body = `${d[0]}${d[1]}${d[2]}${d[3]}00000${d[4]}`;
  else body = `${d[0]}${d[1]}${d[2]}${d[3]}${d[4]}0000${last}`;
  return system + body + check;
}

/**
 * Digit-check an EAN-13, EAN-8, UPC-A or UPC-E barcode.
 *
 * Decoders do this themselves, but a misread that happens to satisfy the
 * checksum is exactly the failure worth catching before it becomes a lookup for
 * somebody else's product: a wrong product page is worse than no product page,
 * because nothing about it looks wrong.
 */
export function isValidBarcode(code) {
  if (!/^\d+$/.test(code)) return false;
  if (![8, 12, 13].includes(code.length)) return false;

  // An 8-digit code is ambiguous: EAN-8 or UPC-E. Accept it if either reading
  // checks out, rather than guessing which one the decoder meant.
  if (code.length === 8) {
    const expanded = expandUpcE(code);
    if (expanded && checksumOk(expanded)) return true;
  }
  return checksumOk(code);
}

function checksumOk(code) {
  const digits = code.split('').map(Number);
  const check = digits.pop();
  // Weights alternate 3 and 1 from the rightmost data digit leftwards, which is
  // the same rule for all three lengths once you count from the right.
  const sum = digits
    .reverse()
    .reduce((acc, d, i) => acc + d * (i % 2 === 0 ? 3 : 1), 0);
  return (10 - (sum % 10)) % 10 === check;
}

/** Load ZXing once, and only if we actually need it. */
let zxingPromise = null;
function loadZXing() {
  if (zxingPromise) return zxingPromise;
  zxingPromise = new Promise((resolve, reject) => {
    const el = document.createElement('script');
    el.src = ZXING_SRC;
    el.onload = () => (window.ZXing ? resolve(window.ZXing) : reject(new Error('ZXing loaded but did not register.')));
    el.onerror = () => reject(new Error('The barcode decoder could not be downloaded. Check your connection.'));
    document.head.appendChild(el);
  });
  return zxingPromise;
}

/**
 * Start the camera and decode until a barcode is found or `stop()` is called.
 *
 * @param {HTMLVideoElement} video
 * @param {{onResult: (code: string) => void, onError: (err: Error) => void,
 *          onDecoder?: (name: string) => void}} handlers
 * @returns {Promise<{stop: () => void}>}
 */
export async function startScanner(video, handlers) {
  const { onResult, onError, onDecoder = () => {} } = handlers;

  /* Rear camera, and a resolution high enough to resolve the bars of a barcode
     held at arm's length. `ideal` rather than `exact` throughout: a device with
     one camera should still work rather than throwing OverconstrainedError. */
  const constraints = {
    video: {
      facingMode: { ideal: 'environment' },
      width: { ideal: 1280 },
      height: { ideal: 720 },
    },
    audio: false,
  };

  const stream = await navigator.mediaDevices.getUserMedia(constraints);
  video.srcObject = stream;
  video.setAttribute('playsinline', '');   // iOS Safari fullscreens the video without this
  await video.play();

  let stopped = false;
  let rafId = null;
  let zxingReader = null;

  const stop = () => {
    if (stopped) return;
    stopped = true;
    if (rafId) cancelAnimationFrame(rafId);
    // ZXing's teardown is reset(), not stop(); it stops the decode loop and
    // releases the reader's own hold on the stream.
    if (zxingReader) { try { zxingReader.reset(); } catch { /* already reset */ } }
    // Releasing the tracks is what turns the device's camera light off. Leaving
    // it on after a scan reads as the page still watching, and it is worth
    // being visibly scrupulous about that.
    stream.getTracks().forEach((t) => t.stop());
    video.srcObject = null;
  };

  const settle = (code) => {
    if (stopped) return;
    if (!isValidBarcode(code)) return;   // keep scanning rather than acting on a misread
    stop();
    onResult(code);
  };

  if ('BarcodeDetector' in window) {
    let detector;
    try {
      const supported = await window.BarcodeDetector.getSupportedFormats();
      const formats = FORMATS.filter((f) => supported.includes(f));
      // A BarcodeDetector that exists but supports no retail format is worse
      // than none: it would scan forever finding nothing. Fall through instead.
      if (formats.length) detector = new window.BarcodeDetector({ formats });
    } catch { /* fall through to ZXing */ }

    if (detector) {
      onDecoder('BarcodeDetector');
      const tick = async () => {
        if (stopped) return;
        try {
          const codes = await detector.detect(video);
          if (codes.length) settle(codes[0].rawValue);
        } catch {
          /* A single dropped frame is normal; the video element is not always
             ready: and must not tear down the scanner. */
        }
        if (!stopped) rafId = requestAnimationFrame(tick);
      };
      rafId = requestAnimationFrame(tick);
      return { stop };
    }
  }

  try {
    const ZXing = await loadZXing();
    onDecoder('ZXing');
    const reader = new ZXing.BrowserMultiFormatReader();
    zxingReader = reader;
    reader.decodeFromStream(stream, video, (result) => {
      if (result) settle(result.getText());
    });
  } catch (err) {
    stop();
    onError(err);
  }

  return { stop };
}
