/* ==========================================================================
   The product thumbnail, in one place.

   Three surfaces show a small picture of a tin: search results, recently
   viewed on the home page, and each side of the compare page. They had no
   picture at all before M15b, and the owner's feedback on the live site was
   exactly that: "There's no photo either."

   Two things this has to get right, both of which are why it is a module
   rather than three copies of an <img> tag:

   1. **A missing photo must not change the shape of a row.** Coverage is good
      but not complete, and a list where some rows have a 56px image and some
      do not is visibly ragged. Every row gets a box; where there is no photo
      the box holds a paw outline instead.

   2. **A photo is never the reason a page looks broken.** The image is
      decorative: the product's name sits beside it and carries the meaning,
      so `alt` is empty on purpose rather than repeating the name to a screen
      reader. If the file 404s or the host is unreachable, the broken-image
      glyph is replaced with the same placeholder the missing case uses.

   The failure path is a single delegated listener rather than an `onerror`
   attribute. There is no inline event handler anywhere else in this codebase
   and this is not the place to introduce the first one: it would be the only
   thing standing between the site and a Content-Security-Policy header.
   `error` does not bubble, so the listener is registered in the capture phase.

   The image comes from images.openpetfoodfacts.org, the same project the
   catalogue comes from, at the 200px "small" size rather than the 400px
   default: the box is 56px, so 400px is three times more bytes than even a
   high-density screen can use.
   ========================================================================== */

/* Inline rather than a file: it is a few hundred bytes, it has to render with
   no network at all on the offline page, and it inherits the ink colour so it
   themes for free. */
const PAW = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
  + '<ellipse cx="7" cy="8.5" rx="2.1" ry="2.8"/><ellipse cx="12" cy="6.6" rx="2.1" ry="2.9"/>'
  + '<ellipse cx="17" cy="8.5" rx="2.1" ry="2.8"/><ellipse cx="19.6" cy="13.4" rx="1.9" ry="2.3"/>'
  + '<path d="M12 12.4c2.8 0 5.2 2.2 5.2 4.6 0 1.7-1.3 2.6-3 2.6-1 0-1.6-.4-2.2-.4s-1.2.4-2.2.4'
  + 'c-1.7 0-3-.9-3-2.6 0-2.4 2.4-4.6 5.2-4.6z"/></svg>';

function esc(value) {
  return String(value)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

/** The placeholder, which is also what a failed photo is replaced with. */
export function thumbPlaceholder() {
  return `<span class="thumb thumb-empty" aria-hidden="true">${PAW}</span>`;
}

/**
 * A thumbnail for a product, or the placeholder where there is no photo.
 *
 * @param {string|undefined} url  A product image URL, usually product.thumbUrl.
 * @returns {string} HTML for exactly one 56px box.
 */
export function thumbHtml(url) {
  if (!url) return thumbPlaceholder();
  return `<img class="thumb" src="${esc(url)}" alt="" loading="lazy" decoding="async">`;
}

/* Registered once, on import, for the lifetime of the page. Every list here is
   redrawn by assigning innerHTML, so per-image listeners would have to be
   reattached on every redraw and would be forgotten exactly once. */
let installed = false;

export function installThumbFallback() {
  if (installed || typeof document === 'undefined') return;
  installed = true;
  document.addEventListener('error', (event) => {
    const el = event.target;
    if (!el || el.tagName !== 'IMG' || !el.classList.contains('thumb')) return;
    const span = document.createElement('span');
    span.className = 'thumb thumb-empty';
    span.setAttribute('aria-hidden', 'true');
    span.innerHTML = PAW;
    el.replaceWith(span);
  }, true);
}

installThumbFallback();
