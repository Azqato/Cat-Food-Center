/* Tests for the barcode validation in scanner.js.
 *
 * Only the pure parts are testable headlessly — `getUserMedia` needs a camera
 * and a user gesture. That is fine, because the pure parts are where the
 * silent failures live: a validator that rejects a whole barcode family does
 * not throw, it just never finds anything, which looks exactly like a camera
 * that cannot see. */
import { isValidBarcode, expandUpcE, FORMATS } from './scanner.js';
import { suite } from './test-runner.js';

suite('isValidBarcode — real codes', (t) => {
  // Real EAN-13s: the Auchan pate from docs/DATA-COVERAGE.md, and a Dreamies tub.
  t.ok(isValidBarcode('3596710487455'), 'accepts a real EAN-13');
  t.ok(isValidBarcode('5000159461122'), 'accepts a second real EAN-13');
  t.ok(isValidBarcode('036000291452'), 'accepts a real UPC-A');
  t.ok(isValidBarcode('96385074'), 'accepts a real EAN-8');

  t.ok(!isValidBarcode('3596710487456'), 'rejects a wrong check digit');
  t.ok(!isValidBarcode('359671048745'), 'rejects a dropped digit');
  t.ok(!isValidBarcode('35967104874555'), 'rejects an over-long code');
  t.ok(!isValidBarcode('359671O487455'), 'rejects a letter O read as a zero');
  t.ok(!isValidBarcode(''), 'rejects an empty string');
});

suite('UPC-E is expanded before it is checked', (t) => {
  // 04252614 expands to 042100005264, a documented UPC-E/UPC-A pair.
  t.equal(expandUpcE('04252614'), '042100005264', 'expands a UPC-E to its UPC-A form');
  t.ok(isValidBarcode('04252614'),
    'so a UPC-E validates — under the EAN-8 rule it would be silently discarded, '
    + 'and the scanner would appear never to see small US packages');

  t.equal(expandUpcE('01234565')?.length, 12, 'expansion is always 12 digits');
  t.ok(expandUpcE('12345670'), 'number system 1 is valid UPC-E, if rare');
  t.equal(expandUpcE('22345670'), null, 'a system digit other than 0 or 1 is not UPC-E');
  t.equal(expandUpcE('123456789'), null, 'and a non-8-digit code is not UPC-E either');
});

suite('scan formats', (t) => {
  t.ok(!FORMATS.includes('qr_code'),
    'QR codes are excluded — packaging carries them, and they are not the product barcode');
  t.ok(FORMATS.includes('ean_13') && FORMATS.includes('upc_a'),
    'the two formats that cover essentially all retail food packaging are included');
});
