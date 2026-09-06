/* ==========================================================================
   Recently viewed products.

   Kept in `localStorage`, which means it lives on the visitor's device and
   nowhere else. There is no account, no sync and no server, and that is a
   feature rather than a limitation of the static architecture
   (docs/PRD.md section 16.2): a list of what someone feeds their cat is
   not information we have any reason to hold.

   What is stored is the minimum needed to redraw a card without a network
   round-trip: barcode, name, brand, score, band. Not the full product: the
   score is derived, the engine changes, and a stale score rendered as current
   would be a quiet lie. Anything shown from here is labelled as a past view,
   and clicking through recomputes it.
   ========================================================================== */

const KEY = 'cfc-recent';
const LIMIT = 6;

/* Every access is wrapped: localStorage throws outright in some privacy modes,
   and a home page that fails to render because of a convenience feature would
   be a poor trade. */
function read() {
  try {
    const raw = window.localStorage.getItem(KEY);
    const parsed = raw ? JSON.parse(raw) : [];
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function write(entries) {
  try {
    window.localStorage.setItem(KEY, JSON.stringify(entries));
  } catch {
    /* Quota or blocked storage. The visit still happened; we just cannot
       remember it, which is not worth interrupting anyone over. */
  }
}

/** Most recent first. */
export function recentProducts() {
  return read().filter((e) => e && typeof e.barcode === 'string');
}

/**
 * Record a product view, moving it to the front if it is already there.
 *
 * @param {{barcode: string, name: string, brand?: string,
 *          score?: number, band?: string, bandLabel?: string}} entry
 */
export function recordView(entry) {
  if (!entry || !entry.barcode) return;
  const rest = read().filter((e) => e && e.barcode !== entry.barcode);
  const next = [{ ...entry, viewedAt: Date.now() }, ...rest].slice(0, LIMIT);
  write(next);
}

export function clearRecent() {
  try { window.localStorage.removeItem(KEY); } catch { /* nothing to do */ }
}
