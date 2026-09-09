/* ==========================================================================
   Premix groups (M24, docs/PRD.md section 16.11).

   A label prints its vitamin and mineral premix as a heading followed by a
   bracketed list:

     ... taurine, MINERALS [zinc sulfate, ferrous sulfate, ...], VITAMINS
     [Vitamin E supplement, niacin, ..., menadione sodium bisulfite complex]

   The splitters in opff.js and catalogue.js keep bracketed groups whole, and
   they are right to: "meat and animal derivatives (including chicken, 4%)" is
   one ingredient and splitting it would invent three. The cost was that a
   twelve-item premix arrived as a single ingredient, and the product page put
   the Tier 3 chip menadione earns on the whole group. The flag was true and its
   placement was not: the page said twelve vitamins were high risk when one of
   them was.

   ── The rule, and why it is this narrow ──

   A group is expanded only when both of these hold:

     1. It is written with square brackets. Round brackets qualify an
        ingredient ("chicken (4%)", "fish oil (source of DHA)"); square
        brackets, on every label measured for this project, group a premix.
     2. Its heading is a word for a group of ingredients rather than an
        ingredient. `MINERALS [...]` expands. `chicken meal [preserved with
        mixed tocopherols, rosemary extract]` does not, because dropping that
        heading would delete chicken meal from the list.

   Condition 2 is the one that matters. An earlier draft of this dropped every
   heading before a bracketed list, which is correct for the two Purina prints
   in the catalogue and silently deletes a real ingredient the first time a
   label writes a preservative note that way. A rule that is right about the
   examples in front of it and wrong about the ones that are not is the failure
   this project keeps finding in its own instruments, so this one is a list of
   words that mean "group", and anything else keeps its entry whole.

   ── What this moves ──

   Scores, slightly, and always upward when it moves them. `scoreAdditives`
   matches tiers against the joined text of the whole list, so menadione was
   found before this change and is found after it: nothing gains or loses a
   Tier 2 or Tier 3 flag, and the Tier 3 cap at 49 is unaffected. Tier 0
   beneficial credit is awarded per entry, and an entry that was one opaque
   block is now eleven readable ones, so a taurine or a vitamin E inside a
   premix can now earn the credit it always deserved.
   ========================================================================== */

/* Headings that name a group rather than an ingredient. Deliberately short:
   every word here has been seen introducing a bracketed premix on a real
   label. Add to it from labels, never from imagination. */
const GROUP_HEADINGS = [
  'vitamins', 'vitamin', 'added vitamins', 'vitamin supplements',
  'minerals', 'mineral', 'added minerals', 'trace minerals', 'trace elements',
  'vitamin and mineral premix', 'premix', 'vitamin premix', 'mineral premix',
  'vitamins and minerals', 'nutritional additives', 'technological additives',
];

const GROUP_RE = new RegExp(
  '^(?:' + GROUP_HEADINGS.map((h) => h.replace(/ /g, '\\s+')).join('|') + ')$', 'i');

/**
 * Is this text a heading for a group of ingredients?
 *
 * Punctuation and case are stripped first, because a label may print
 * "VITAMINS:", "Vitamins" or "added vitamins" and all three mean the same
 * thing to a reader.
 */
function isGroupHeading(text) {
  return GROUP_RE.test(String(text || '').replace(/[:\-–—.,]+$/, '').trim());
}

/**
 * Split the inside of a group on top-level commas.
 *
 * Nesting is tracked so that "pyridoxine hydrochloride (Vitamin B-6)" survives
 * as one entry, which is the same reason the outer splitters track it.
 */
function splitInner(text) {
  const out = [];
  let depth = 0;
  let current = '';
  for (const ch of String(text || '')) {
    if ('(['.includes(ch)) depth += 1;
    if (')]'.includes(ch)) depth = Math.max(0, depth - 1);
    if ((ch === ',' || ch === ';') && depth === 0) {
      out.push(current);
      current = '';
    } else {
      current += ch;
    }
  }
  out.push(current);
  return out.map((s) => s.replace(/\s+/g, ' ').trim().replace(/[.;]+$/, '').trim()).filter(Boolean);
}

/**
 * Expand premix groups in a split ingredient list.
 *
 * Entries that are not groups are returned untouched and in place, so this is
 * safe to run over every list: a label with no premix comes back identical.
 *
 * @param {string[]} entries ingredients, already split on top-level commas
 * @returns {string[]} a new array, with group members in the group's position
 */
export function expandGroups(entries) {
  const out = [];
  for (const entry of entries || []) {
    const match = /^(.*?)\[([^\]]*)\]\s*$/.exec(String(entry || '').trim());
    if (!match) {
      out.push(entry);
      continue;
    }
    const [, heading, inside] = match;
    const members = splitInner(inside);
    // One member is not a list, it is a note: "chicken fat [preserved with
    // mixed tocopherols]" says something about the fat rather than replacing
    // it. Two members with a heading that names a group is a premix.
    if (members.length < 2 || !isGroupHeading(heading)) {
      out.push(entry);
      continue;
    }
    out.push(...members);
  }
  return out;
}

/** Exported for the test suite only. */
export const _internal = { isGroupHeading, splitInner, GROUP_HEADINGS };
