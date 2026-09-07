/* ==========================================================================
   Where the site root is, worked out rather than assumed.

   Every page used to sit at the repository root, so a link written as
   './product.html' was correct from everywhere and no module had to think
   about it. Since M19 a page is a directory (docs/PRD.md section 16.4), so
   the same string means '/search/product.html' when the search page renders
   a card and '/learn/nutrition/product.html' from a guide page. Both 404.

   The fix is not to write '../' in the modules, because a module does not
   know which page loaded it: search-page.js runs one level down, and any of
   these could be imported from a page at any depth in future.

   `import.meta.url` is the module's own address, and a module in assets/js/
   is exactly two levels below the site root no matter who imported it. So
   the root is derivable, once, here, and every other module asks. It cannot
   drift, because it is not a written-down fact: it is a measurement.

   The result is absolute (https://host/Cat-Food-Center/), which is correct
   and is not the thing PRD section 26.2 prohibits. That rule forbids
   *hard-coded* absolute paths like '/assets/...', which assume the site is
   served from a domain root and 404 under a repository subpath. This is
   computed from where the code actually is, so it is right under a subpath,
   at a domain root, and on 127.0.0.1 alike.
   ========================================================================== */

export const SITE = new URL('../../', import.meta.url).href;

/**
 * A URL for a path relative to the site root.
 *
 * @param {string} path e.g. 'product/?barcode=123' or 'learn/labels/#aafco'
 * @returns {string} an absolute URL
 */
export function url(path) {
  return SITE + path;
}
