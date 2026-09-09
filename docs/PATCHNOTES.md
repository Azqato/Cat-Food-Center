# Patch Notes

Running changelog for Cat Food Center. Add an entry to the top for every
meaningful change, and keep [PRD.md](PRD.md) in sync whenever product
behaviour, architecture or a stated rule changes.

Format: newest first, `major.minor.patch`. Pre-launch work lives under `0.x`.

**Entries are historical records and are never rewritten to match the present.**
An entry saying the offline shell held 23 files stays as it is even though it
holds 29 today. See PRD section 23.6.

**Two changelogs were merged here on 2026-09-06.** This file and one at the
repository root had been kept in parallel, numbering the same work
differently: the compare page is `[0.11.0]` in one history and `v0.10.0`
in the other. They could not be interleaved without inventing a reconciliation
that never happened, so the fuller history is the spine below and the second is
preserved in the appendix. Neither history was rewritten; the only change made
to either was the project-wide em-dash sweep described in `[0.13.0]`, which is
punctuation rather than content.

---

## [0.29.0] - 2026-09-09

**M22 is finished: top-100 coverage is measurable, and it is 0%.**

Added
* **`tools/measure-coverage.py`,** which answers M12's oldest criterion. Coverage is measured
  through the site's own search path, not through the catalogue: a visitor who wants a best-seller
  types its name, so the tool runs each SKU's name through the same endpoint, category filter and
  fields the search page uses, and asks whether the same product comes back with an ingredient
  list. The barcode gap that held this milestone open turned out to be a question about the
  catalogue's internals rather than about the criterion.
* **`tools/data/coverage.json`,** every decision with its evidence: the query, the best candidate,
  the words that matched, whether the brand was confirmed. `--review` prints the borderline calls.
* PRD section 12.9, the measurement and what it can get wrong in both directions.

Notes
* **0 of 100.** Four best-sellers matched a database record that holds no ingredient list, twelve
  were close enough to need a person and were different products on inspection, and 84 had no
  candidate. Five more carry ingredients but are not tagged `cat-food`, so the site's own filter
  hides them.
* This is not an empty database. It holds 13 Fancy Feast records, 32 Friskies, 27 Sheba, and 89 of
  the 100 best-sellers found a candidate of the right brand. What it does not hold is the specific
  products people buy: "meow mix original choice" is in there, is unmistakably the number-five
  best-seller, and cannot be scored.
* **The matcher was wrong twice before it was right, and both times it printed a confident
  percentage.** The first treated flavour words as noise, so every Fancy Feast matched every other
  Fancy Feast at 1.0 and coverage looked real. The second asked for the brand plus four words, and
  since every term narrows that endpoint, it found nothing at all and reported zero for the wrong
  reason. Reading the rows caught both; reading the total would have caught neither. Seventh
  instance, and the first where the same instrument failed in both directions inside an hour.
* M12's target is 80%. The gap is not a gap, and what to do about it is the project owner's call,
  recorded as an open decision rather than settled here.

## [0.28.0] - 2026-09-09

**M24b: the search asks Open Pet Food Facts a second earlier, because it stopped waiting for
three things it did not need to wait for.**

Changed
* **`<link rel="modulepreload">` for each page's whole module graph.** Eight modules used to
  arrive in three serial waves, because the browser cannot ask for `opff.js` until
  `search-page.js` has been parsed, or for `catalogue.js` until `opff.js` has. Naming the graph in
  the head collapses that into one wave. The list is computed by reading the imports out of the
  sources, never written down, so it cannot drift the way a hand-kept list does.
* **`loadCatalogue` caches its promise instead of its result.** A filtered search fans out into
  five concurrent page requests, all five awaited the catalogue in the same tick, all five found
  an empty cache, and `catalogue.json` was fetched five times on the critical path. It is fetched
  once now.
* **`searchProducts` and `fetchBrands` issue their request before reading the catalogue.**
  Neither URL depends on it. Both still merge curated data into the results exactly as before;
  only the order changed.
* Service worker `v9` to `v10`.

Added
* **A gate for duplicate local requests,** in `check-vitals.py`: no page may fetch the same file
  from this repository twice, on any page, gated or not. Every number that file already collected
  counted requests without ever asking whether two of them were for the same thing, which is why
  five fetches of one file sat on the critical path in plain sight.
* **A gate for the preload list,** in `check-live.py`: each built page's preloads must equal the
  graph computed from the module sources. 28 live checks to 29.

Fixed
* **The first version of the preload list was silently short by one file.** The import pattern was
  line-bounded and `opff.js` imports five names from `catalogue.js` across three lines, so the
  module holding the entire curated catalogue was left out. The page worked, the preloads looked
  right, and the waterfall it left behind was the one nobody would have gone looking for again.
  This is the sixth time the instrument was the thing that was wrong, and the first time it was an
  instrument built in the same commit as the fix it was measuring.

Notes
* Measured on the same throttle as the gate, `/search/?q=chicken`: **first API request 2271ms to
  1361ms**, search LCP 3452ms to 2596ms, product page LCP to 2284ms.
* The plan recorded in `[0.27.0]` was an inline head script that starts the fetch before any
  module loads. It was not built. It duplicates URL construction in a second place, and the day
  the two copies disagree the page issues two requests and nothing says so, because two requests
  look exactly like one slow one. The three ordinary fixes above got most of the way there and
  none of them add a second source of truth.
* The API pages are still over the LCP budget and are still not gated on it. What is left is Open
  Pet Food Facts' own response time, about a second on this throttle.

## [0.27.0] - 2026-09-09

**M24a: every page says which address it lives at. And the LCP number in `[0.25.0]` was
measuring the wrong thing.**

Added
* **`rel=canonical` on all twenty pages.** A `{{canonical}}` token sits beside `{{root}}` and is
  substituted by the same writer that already knows how deep each page is, so no page ever
  contains a hand-written absolute URL. `BASE` moved into `tools/site/chrome.py`, giving both
  generators one definition of the site's address, which is what makes the next rename a one-line
  change rather than the twenty-nine-file sweep of `[0.24.1]`.
* **A gate for it,** read off disk rather than over the wire: the value is a production URL and
  `check-live.py` serves from `127.0.0.1`, so a check that compared the tag to the page it fetched
  would pass while every page pointed at the wrong site. 27 live checks to 28.
* The canonical is a page's own directory, never a query string, so `/product/?barcode=X`
  canonicalises to `/product/`. There is one product document and it renders whatever the query
  asks for; saying otherwise in a tag would not make it two pages.

Changed
* **The filtered search paints page one as soon as it lands** instead of waiting for all five scan
  pages, and says "still checking further results" until the rest arrive. About 450ms of waiting
  removed. Service worker `v8` to `v9`.

Fixed
* **`[0.25.0]` said M26 "tripled LCP on a search", from about 1.0s to 3.3s. That was a
  misreading, and the site was never three times slower.** Instrumenting the throttled page to
  name the element behind the number: on `?only=all` the largest element is the filter checkbox
  label, static chrome that paints at 1080ms; on the filtered default it is a line inside a result
  card, at 3452ms. Both paths receive their first API response at the same moment, 3.1 to 3.3
  seconds. The metric changed which element it was measuring. The page did not change speed.
* Two changes were made on the strength of the wrong diagnosis before it was checked. The first,
  painting page one early, is worth keeping on its own merits and is above. The second, issuing
  the first request alone so it would not share bandwidth, was reverted: it cost a round trip and
  bought nothing, because bandwidth was never the constraint.

Notes
* **The real number, now that something is pointed at it: 2257ms pass before the first API
  request leaves the browser.** Stylesheets, fonts, a blocking theme script, six ES modules and
  two data files all load first. Everything after is quick, the search response lands a second
  later and the four extra scan pages add 450ms between them. So more than half of a four-second
  search is spent before the site has asked anybody anything. That is M24b, which is reopened
  and now aimed at the thing that is actually slow.
* **This is the fifth time a measurement turned out to be about the instrument.** M20a, M21a,
  M22, M25, M26. The new one is worth naming precisely, because it is subtler than the others: a
  correct number, honestly gathered, describing something other than what it was read as
  describing. "LCP got worse" was true. "The page got slower" did not follow, and nothing in the
  number said so either way until somebody asked which element it belonged to.

## [0.26.0] - 2026-09-09

**M24: the flag goes on the ingredient that earned it.**

Fixed
* **A twelve-item vitamin premix no longer reads as high risk because one of the twelve is.**
  Purina prints `VITAMINS [...]` and `MINERALS [...]`, the splitters kept bracketed groups whole,
  and the product page put the Tier 3 chip menadione earns on the entire block. Cat Chow Complete
  went from 28 ingredient rows to 38, and the chip now sits on `menadione sodium bisulfite complex
  (Vitamin K)` alone.

Added
* `assets/js/ingredients.js`, and 24 assertions in `ingredients.test.js` written before the
  change rather than after it, because a test written afterwards only records what the code does.
* Both splitters, in `opff.js` and `catalogue.js`, run the expansion. Service worker `v7` to `v8`,
  with the new module precached.

Notes
* **The rule is narrow, and the narrowest part is the point.** A group expands only when it uses
  square brackets, has two or more members, and its heading names a group rather than an
  ingredient. An earlier draft dropped every heading before a bracketed list. That is correct for
  the two Purina prints in the catalogue and it silently deletes chicken fat the first time a
  label writes `chicken fat [preserved with mixed tocopherols, rosemary extract]`. That case is
  now a test, and the heading list contains words seen on labels rather than words that seemed
  likely.
* **This moved no scores, and it was measured rather than assumed.** All four catalogue products
  scored the same after as before. Tier 2 and Tier 3 matching runs against the joined text of the
  whole list, so menadione was found before and is found after, and the Tier 3 cap at 49 is
  untouched. Only the Tier 0 beneficial credit is per entry, so the one way expansion can move a
  score is upward. That is asserted in a test, not left as a paragraph.
* The milestone was queued as "it moves scores, so write the tests first". It turned out to move
  the page and not the scores, which is only knowable in that order.

## [0.25.0] - 2026-09-09

**M26: the search page hides what it cannot score, and says so every time it does.**

Changed
* **The scorable-only filter is on by default.** Two thirds of Open Pet Food Facts carries no
  ingredient list, so a search used to open on a column of grey "Not scored" tiles. That was an
  honest view of the database and a useless view of cat food.
* **The label says what is missing, wherever anything is.** "Showing 1-24 of the 51 products in
  all 83 results for "chicken" that can be scored - 32 with no ingredient list are hidden - Show
  everything". The count and the way out are in the same sentence as the results, addressed to
  somebody who never touched the control and may not know it exists. This was the condition the
  milestone shipped under, not a nicety: it was queued behind the coverage number on the grounds
  that hiding a gap before measuring it is the wrong order, and what that argument actually asks
  for is disclosure rather than delay.
* **The choice is remembered,** in `localStorage` under `cfc-only`. Fourth thing this site
  stores, and the first that is not the visitor's own history. Unreadable storage means the
  default, as everywhere else here.
* **`only` in the URL always wins over what is stored,** and `urlFor` now always writes it. A
  link whose meaning depends on the recipient's browser storage is not a link somebody can send,
  and section 16.7 says every view is one.
* The first-visit empty state and the "None of these can be scored" state both now say the page
  filters by default, rather than describing a filter the visitor is assumed to have chosen.
* Service worker `v6` to `v7`.

Added
* **Three live checks, because the existing ones could not see this.** All three search checks
  passed unchanged after the default flipped: they assert the substring "can be scored", which
  the filtered and the unfiltered label both contain, so the gate was blind to exactly the thing
  the milestone changed. The new checks assert that an unqualified search filters and discloses
  the hidden count, that `only=all` overrides the stored preference, and that turning the filter
  off survives a navigation to a different search. 24 live checks to 27.

Known cost
* **This tripled LCP on a search.** The filtered path fetches five pages of results in parallel
  and renders nothing until all five have landed, so making it the default made that the normal
  experience: `search results (API)` measured about 1.0s before and 3.3s after, repeatably, on
  the same machine and network. It is not a gate failure, because API pages sit outside the
  vitals budget on the grounds that upstream latency is not ours. That reasoning is what let a
  self-inflicted regression through, and it is worth revisiting rather than leaning on. Recorded
  in section 16.11 with the fix, which is to render the first page's results as they land instead
  of waiting for the fifth, and which should happen before the beta.

Notes
* **Fourth time a gate has been blind to the change under it,** after M20a, M21a and M25. The
  pattern is now specific enough to name: a check that asserts a substring both branches of a
  decision produce is not checking the decision. Worth a sweep of the other loose assertions
  before the next milestone that changes a default.

## [0.24.2] - 2026-09-09

**Two things `[0.24.1]` said an hour ago are not true. Corrected here rather than there,
because section 23.6 means an entry is not edited to match what was later learned.**

Fixed
* **"Canonical tags on all twenty pages" describes something this site does not have.** There is
  no `<link rel="canonical">` anywhere on it, verified by fetching the live home page and finding
  none. What each of the twenty pages actually carries is one occurrence of the absolute URL, the
  "Report a problem" link in the footer, written by `tools/site/chrome.py`. The rename was still
  applied correctly and completely; the entry described the right work with the wrong noun.
* **"GitHub redirects the old repository and Pages path" is half right.**
  `https://github.com/Azqato/Cat-Food-Center` answers 301 to the new repository.
  `https://azqato.github.io/Cat-Food-Center/` answers **404**. GitHub redirects the repository and
  not the Pages path. Every link to the old site that exists anywhere is dead, not forwarded.
* **The stale service worker is therefore a worse problem than `[0.24.1]` recorded, not a
  smaller one.** That entry said the old worker "cannot serve stale pages here", which is true
  and beside the point. A worker at the old path serves *that* path from its own cache, so a
  returning visitor who opens the old URL gets a working copy of the site as it stood in early
  September, served past a 404, with no way to notice. The site is pre-beta and has no such
  visitors, so this is still recorded rather than fixed, but it is recorded as what it is.

Notes
* **Found by checking, which is the only reason it was found.** The rename commit passed 217
  tests and 24 live checks, because no gate knows what the production URL is: `check-live.py`
  drives a local server on `127.0.0.1`. Both errors were in prose, and prose is the part of this
  repository nothing gates. The verification that caught them was three `curl` calls that could
  have been skipped, on the grounds that the deploy was obviously fine, which it was.
* **A canonical tag is worth adding and is not in this entry.** A site that has moved once and
  has no canonical tag is a site that cannot tell a crawler which address is the real one. It is
  a change to the page head on twenty pages rather than a URL correction, so it belongs in a
  milestone of its own rather than in a chore.

## [0.24.1] - 2026-09-09

**The repository was renamed, so the site moved.**

Changed
* `Cat-Food-Center` to `catfoodcenter`, everywhere the absolute URL had to be written down:
  canonical tags on all twenty pages, `sitemap.xml`, `robots.txt`, the `Sitemap:` line inside it,
  the probe user agent in `tools/probe-opff.py`, the base in `tools/site/build.py`, the "Report a
  problem" link in `tools/site/chrome.py`, `README.md`, `LICENSE.md` and the PRD. Both page
  generators were re-run rather than the output being edited by hand.
* Live site is now **https://azqato.github.io/catfoodcenter/**, repository
  **https://github.com/Azqato/catfoodcenter**. The git remote was repointed.
* **PATCHNOTES was deliberately left alone.** Every earlier entry still names the old URL, and
  section 23.6 says entries are historical records and are never rewritten to match the present.
  GitHub redirects the old repository and Pages path, so those links still resolve.

Notes
* **Twenty pages carried the old path in exactly one tag each, and no page carried it in a link.**
  That is ADR-001 working: every internal path on this site is relative, so a change of subpath
  touched only the places that are required to state an absolute URL. A site with absolute
  internal paths would have needed all twenty pages rewritten rather than one line each.
* **A visitor who used the site before today keeps a service worker registered at the old path.**
  A worker controls its own path and below, and the old scope no longer matches anything the new
  site serves, so it cannot serve stale pages here; it will sit inert against a path that now
  redirects. It is recorded rather than fixed because the site is pre-beta and has no such
  visitors to strand. If that changes before launch, the fix is a one-line unregister on the old
  path, not a cache version bump, because a bump only reaches a worker that is still in scope.

## [0.24.0] - 2026-09-08

**M25: the catalogue is consulted everywhere it is needed, not in one place.**

Added
* **Search reads the curated catalogue.** `applyCurated` merges catalogue data over every
  product a search returns, and `searchCatalogue` finds curated products the API cannot return
  at all, matching on name, brand and pack size. Curated-only matches are put first: there are
  few of them, they are the records this project vouches for by name, and the alternative is
  burying them under a ranking that has never heard of them.
* **Catalogue brands join the brand index,** exempt from the minimum-product threshold. That
  threshold hides the database's long tail of one-product transcription noise; a brand entered
  by hand is the opposite of noise, because entering it was a decision.
* **"Recorded by hand" on the search card,** and the result line now says how many of the
  results are. The card is where a score is first read, and a caveat that stays behind on the
  product page is a caveat that does not exist. Same argument M18b made for confidence.
* **A live check that a card and a page cannot disagree.** `check-live.py` reads the score off
  `/product/?barcode=0017800150149` and off that product's search card and fails unless they
  match. It asserts agreement rather than a number: pinning 49 would fail every time the engine
  legitimately moved, and would not have caught this.
* Nineteen assertions in `catalogue.test.js` covering the three new functions, including the
  two rules most likely to be simplified away later: only named entries are findable this way,
  and the ingredient list is not searched.

Fixed
* **The site contradicted itself, on production, in public.** A search for "Cat Chow Complete"
  returned a card reading "No ingredient list on record. Not scored", under a count line saying
  "0 of these can be scored", while the product page for the same barcode scored it 49 off a
  transcribed manufacturer panel and listed every ingredient. Both views came from this site,
  from the same data, in the same minute. Section 16.5b had recorded the discoverability half of
  this the day before and missed this half, which was the visible one.
* **A search no longer loses local data when the database is unreachable.** Curated matches are
  returned under a warning instead of being replaced by a failure message. The one path where
  the catalogue is the only source there is was the one path that threw it away.
* **Result numbering across pages.** Curated matches are counted on every page and shown on the
  first, so a search no longer reports 1579 results on page one and 1578 on page two, and page
  two's numbering steps over the entries page one added.

Changed
* Service worker `v5` to `v6`.
* **PRD section 16.5b** rewritten from an open defect to what was built, with the route table
  now showing before and after and the five decisions worth keeping.
* **M26 added to the roadmap:** hide unscored products by default. The scorable-only control
  already exists; what is new is the default, making it survive a navigation, and saying plainly
  that it hides most of the database. Queued behind the coverage number, because it hides the
  evidence of the gap that number measures.

## [0.23.1] - 2026-09-08

**A curated product resolves, and nothing leads anybody to it.**

Changed
* **PRD section 16.5b, new, and M25 on the roadmap.** `loadCatalogue` and `mergeCurated` are
  called from `fetchProduct` and from nowhere else, so a product the API has never heard of can
  be reached by scanning its barcode or by following a direct link, and cannot be found by
  typing its name into search or by browsing brands. Merge rule 4 in 16.5a said such a product
  "still resolves", which is true of the product page and of nothing else; the rule now says so.
* Found by being asked why Dr. Elsey's was missing from the brand index. It is missing because
  Open Pet Food Facts holds no Dr. Elsey's food, only their cat litter, and the brand index is
  the API's own facet. The question was about a brand that was never added; the answer exposed a
  gap that would have applied to one that was.
* **Why it had gone unnoticed:** all four curated entries so far fill gaps in records the
  database already holds, so every one of them is searchable and browsable for reasons that have
  nothing to do with the catalogue. The failure only appears for an API-absent product, and none
  exists yet.
* M25 is a prerequisite for M22's coverage number, not a refinement of it. "The site can score
  this product" and "a visitor can find this product" are different numbers, and M12's criterion
  means the second.

---

## [0.23.0] - 2026-09-08

**The product library, captured (M22, partial).**

Added
* `tools/capture-rankings.py` and `tools/data/top-skus.json`: 300 ranked rows from Amazon's cat
  food, dry cat food and wet cat food best-seller lists. The first written answer this project
  has had to "which products should the site cover?". Every capture is dated and appended, never
  replaced, because a product falling off a best-seller list is information about the market.

Changed
* **Section 12.7 said the capture had to be done by hand. It was wrong, and the correction is
  the interesting part.** That conclusion rested on Amazon returning HTTP 503 and Chewy 429,
  which were facts about the fetching tool rather than about the storefronts. Driven through
  Edge, the way every other tool here drives a browser, Amazon serves its best-seller pages
  normally. An instrument's failure had been read as a fact about the world, which is the same
  error section 24 has been collecting since M18.
* Storefront access, measured by pointing a real browser at each: Amazon loads with real rank
  numbers. Chewy returns 403 with a bot-detection reference, Walmart serves a "Robot or human?"
  interstitial, and Petco returns 403 to every URL tried. PetSmart loads but carries no usable
  product name in any anchor.
* Section 24.1's row is narrower: the list exists now, and what is still missing is the coverage
  number.

Removed
* Twenty-four Target rows, captured and then deleted. Target's link text runs the promotional
  line, the price, the product name and the star rating into one string. A partly cleaned name
  looks usable and is not, and the name is the only thing a person can match against a
  manufacturer's label deck.

Known and stated
* **The list is Amazon-only, so it is supermarket food.** Chewy was named in section 12.7
  precisely because a pet-specialist channel ranks premium brands that barely register
  elsewhere, and every specialist source refuses. Anything chosen purely from these rankings
  inherits that bias, which is why Dr. Elsey's is a milestone rather than a ranking row.
* **A captured row cannot become a catalogue entry.** Rows carry names; the catalogue is keyed
  by barcode; no storefront publishes a UPC. Amazon hides it, and Target's pages do not show it
  either. M12's coverage criterion is defined and still unmeasured.

---

## [0.22.0] - 2026-09-08

**The catalogue grows (M21). An additive pill that could never wrap (M21a).**

Added
* Three curated entries, transcribed from Purina label decks: Cat Chow Complete `0017800150149`,
  Fancy Feast Kitten Tender Turkey Feast `0050000575008`, and Friskies Sea Captain's Pate
  `0050000425648`. All three are `sourceKind: "manufacturer"`, all three filled records that had
  neither an ingredient list nor an analysis, and each one records in its note why that barcode
  is believed to describe that deck.
* `tools/label-deck.py`. Give it the URL of a manufacturer label deck and it prints a proposed
  catalogue entry: guaranteed analysis, ingredient list, AAFCO statement, life stage and format.
  It prints rather than writes, because the parser can misread a layout it has not met and the
  reviewer is the last check there is. It needs PyMuPDF, the only library dependency any tool in
  this repository has, and says so plainly if it is missing.
* PRD section 12.7, which for the first time says which hundred SKUs "top-100 coverage" means:
  the Amazon and Chewy rankings, merged, with a quarterly refresh procedure and a rule that a
  previous capture is kept rather than overwritten.
* PRD section 12.8, which measures where a label panel can actually be read. Purina publishes a
  PDF deck per product as text. Mars publishes the panel as an image, so Sheba, Temptations,
  Whiskas and Iams cannot be transcribed at all.
* Roadmap entries M22 (capture the list, measure coverage), M23 (Dr. Elsey's) and M24 (premix
  groups).

Changed
* **The United States cat-food category in Open Pet Food Facts is 86 records, 48 of them with no
  ingredient list.** Measured 2026-09-08. The coverage target had been written as though the
  database held the common products and merely lacked their details; it does not hold them.
  Merge rule 4 in section 16.5a, the barcode the API has never heard of, was written as an edge
  case and is the main case.
* PRD sections 13, 15.4, 16.4 and 16.11, and DESIGN section 9.

Fixed
* **`.additive-fn` could not wrap or shrink.** `white-space: nowrap` plus `flex-shrink: 0` on a
  pill whose text comes from the knowledge base. The inorganic phosphates entry reads "moisture
  retention, dental tartar control, acidifier", which took the product page to 420px at a 320px
  viewport and failed WCAG 1.4.10. Every product flagging that additive had been failing reflow
  since the additive cards shipped; none of the 25 fixed page states the accessibility gate
  audits happened to be one of them.
* Three defects in `label-deck.py`, all found by reading its first output against the PDF. It
  was about to record Purina's label revision code "D662122" as an ingredient; it began the
  AAFCO statement at "Louis, MO 63164 USA", because the address contains "St." and the sentence
  match anchored there; and it labelled Friskies Sea Captain's Choice as kitten food when the
  label says "for growth of kittens and maintenance of adult cats", because it tested for growth
  before it tested for both. A tool built to remove transcription error introduced three of its
  own within ten minutes.

Investigated, and not a defect
* All three new products score exactly 49. Three different foods landing on one number is the
  shape of a cap, and it is one: a Tier 3 additive caps a score at 49 regardless of nutrition,
  and every one of these labels lists menadione sodium bisulfite complex. Cat Chow Complete has
  32% protein and scores 49. That is section 6 working as written.

Known, recorded rather than fixed
* Purina prints premixes as `VITAMINS [...]` and `MINERALS [...]`. The splitter keeps bracketed
  groups whole so that "chicken (4%)" survives, so a twelve-item premix arrives as one
  ingredient wearing the Tier 3 flag its menadione earns. The flag is true; its placement says
  the whole premix is high risk. The fix moves ingredient counts and therefore scores, so it is
  M24 with its own tests rather than a footnote here.

---

## [0.21.0] - 2026-09-08

**The curated catalogue, built (M20). Status colours get an ink (M20a).**

Added
* `assets/data/catalogue.json`, `assets/js/catalogue.js` and the disclosure on the product page.
  Product data transcribed by hand where Open Pet Food Facts has none, merged over the
  normalised record field by field, with every curated field named in words directly under the
  score. `mergeCurated` is pure: a product and an entry in, a new product out. It neither
  fetches nor scores.
* `tools/check-catalogue.py`, the seventh gate. Schema, a source and a checked date on every
  entry, the same plausibility bands the normaliser applies to upstream figures, and no unknown
  keys. A misspelled key is rejected rather than ignored, because the merge would skip it in
  silence and a curated figure that never reaches the page looks exactly like one nobody
  transcribed.
* `sourceKind` on every entry, which was not in the design. The first product attempted forced
  it: for UPC 050000102068, two retailer listings gave incompatible ingredient lists for the
  same tin, one with soy protein concentrate, added colour and Red 3, one with soy flour and
  glycine and no colours. There is no way to tell from outside which is stale, so that product
  got no entry and the disagreement became a rule. A retailer listing may fill a gap; only a
  manufacturer panel may overwrite a figure the database already has.
* `assets/js/catalogue.test.js`, seven suites. The unit suite is 198 assertions.
* One seeded entry, `4008429158100`, supplying a Danish ingredient list to a record that has a
  guaranteed analysis and no list. The additive matcher cannot read Danish, so the page says the
  ingredients were not checked. That is section 11.5 working: an unnamed or unreadable language
  is marked unknown rather than assumed to be English, which is exactly how section 12.4
  happened.
* `--excellent-ink`, `--good-ink`, `--poor-ink` and `--bad-ink`. The band colours are fills and
  borders; the inks carry text. In dark the two are the same values, which already passed.

Changed
* **`tools/check-contrast.py` had never checked a status colour against a page background.** It
  had run green over 38 pairs for six milestones while `--good` rendered as text at 2.72:1 on
  `--bg` and 2.91:1 on `--surface`, `--poor` at 2.51:1 and 2.68:1, and `--warning-ink` at
  4.28:1. The gate is 52 pairs now, 11 of them status inks against both backgrounds. Rendering
  a band word inside the new disclosure exposed a failure that was already shipping.
* `--warning-ink` darkened from `#A9660D` to `#9D5E0C`.
* `sw.js` to `v5`, with `catalogue.js` and `catalogue.json` in `SHELL_ASSETS`. Not optional:
  `opff.js` imports `catalogue.js`, so a device holding `v4` would fail offline without it.
* `tools/check-live.py` is 23 checks, the newest loading the seeded barcode from the live API
  and requiring the disclosure to name the field and its source.
* PRD sections 13, 16.5, 16.5a, 15.4 and 26.4, and DESIGN sections 2.2, 7, 8 and 9.
* PRD section 24.1 loses the row that said none of this existed. It was written to be deleted
  the day the feature shipped, and not before.

Fixed
* A merge that changes nothing now claims no provenance. `ingredientsLang` had been counted as a
  curated field, so an entry that only restated the language of a list already present announced
  a curated origin for data that was entirely upstream. It is a modifier now, not data. Two
  tests failed on this before anybody noticed it by reading.
* The disclosure panel pushed the article to 454px at a 320px viewport, from a single unbroken
  source URL. `overflow-wrap: anywhere`. The accessibility gate caught it; a desktop browser
  never would have.

Considered and rejected
* Four gate rows requiring the band fills themselves to reach 3:1 against `--bg`. They were
  added, they failed, and the reasoning was wrong: WCAG 1.4.11 governs graphics that carry
  meaning on their own, and every chip here carries its own text while the 6px band rule is
  `aria-hidden` beside the word "Good". The rows were replaced by a comment recording the
  measurement and the condition that would require them.
* Seeding the catalogue with a hundred products. The mechanism first, deliberately. See open
  question 2.

---

## [0.20.4] - 2026-09-07

**The curated catalogue, designed (M20). Open question 2 answered.**

Added
* PRD section 16.5a: the design for `assets/data/catalogue.json`, the file that carries product
  data transcribed by hand where Open Pet Food Facts has none. The schema, the merge rules, the
  required source and checked-date on every entry, and the gate that enforces them.
* The governing rule, which shaped everything else: a curated figure is never presented as an
  Open Pet Food Facts figure, and neither is silently preferred over the other. A local file
  that quietly overwrote upstream data would break this project's one real claim, that a number
  can be traced to where it came from, in the least visible way available.
* PRD section 24.1 carries a row saying none of it is built. Section 16.5a says the same in its
  first line. A design document is exactly the kind of thing that quietly becomes a description
  of reality, and this project has a history of that, which is what section 24 exists for.

Changed
* Open question 2, whether a curated catalogue is in scope for the MVP, is answered: yes, and
  the mechanism gets built before the hundred products. A hundred hand-entered records with
  nothing to check them would publish wrong scores under this site's name, and the interesting
  case, a curated figure disagreeing with an API figure, would be met at scale rather than
  designed for.
* M20 is on the roadmap as designed and not built. M12 waits on it.

---

## [0.20.3] - 2026-09-07

**No analytics, decided rather than pending.**

Changed
* **"Analytics instrumented" is no longer a condition of public beta.** The criterion had sat in
  the M12 list since before the data in PRD section 12 was measured, and it contradicted section
  14 directly, which gave "no analytics means no visitor data to protect" as the reason for
  having none. A milestone cannot require closing a gap the same document defends. M12 now has
  three criteria, two of them met, and coverage is the only one still open.
* Section 14 says what that costs instead of leaving it implicit. Every acquisition, engagement
  and retention target, and the north star with them, is marked unmeasured permanently: not
  deferred, not pending instrumentation, but never going to be reported. Each row now names what
  would be needed to know it. They are kept because they still say what this project would count
  as success.
* Interaction to Next Paint is marked unmeasurable here rather than merely unmeasured. It needs
  a real session; Total Blocking Time is gated and stands in for it.
* The reporting cadence table stopped promising weekly and monthly reports that nothing produces.
  Performance is every push, coverage is monthly by probe and audit, and the rest is never.

Not changed
* No third-party script was added, and none will be. It would put every visitor's activity into
  the hands of a company neither this project nor its readers control, and add a pinned runtime
  dependency two milestones after M14 removed the last one.

---

## [0.20.2] - 2026-09-07

**The probe measures language, and open question 9 gets a number.**

Added
* `tools/probe-opff.py` reports which languages the ingredient lists are written in, using the
  rule from `assets/js/opff.js` rather than a rule of its own, so it measures what the site
  believes rather than something adjacent to it. It ranks the languages the engine cannot read
  by how many lists each would reach, which is the shape open question 9 asked for on
  2026-09-07: how many products the next language buys, rather than an intuition about which
  languages matter.
* The findings, in PRD section 12.4. The six languages in `MATCHED_LANGUAGES` read 90.2% of the
  ingredient lists that exist. The seventh candidate is Norwegian, 20 lists, which would take
  coverage to 96.2%; every language after that is worth four lists or fewer. French is the
  largest single language at 47.9%, nearly twice English.
* A note in section 12.6: anonymous pagination stops after page 10. `page=11` answers HTTP 401
  with an HTML login page, which reads as a credentials failure and is a paging limit, since the
  endpoint takes no key. The largest sample obtainable is therefore 1000 products of about 1580,
  in the API's own order rather than at random.

Changed
* The probe clamps to page 10 and says so, pauses a second between pages against an API this
  project pays nothing for, and retries only genuinely transient codes. It now prints the sample
  size beside the percentages it derives, because a percentage with an unstated denominator is
  the kind of figure that gets quoted later as a fact about the database.

Not changed
* `MATCHED_LANGUAGES` is still six languages. The standing rule decides the order: aliases
  first, the constant after, never ahead of them. Adding `nb` without Norwegian aliases would
  make the engine report twenty labels as read when it had read none of them, which is the exact
  failure section 12.4 exists to describe.

---

## [0.20.1] - 2026-09-07

**Offline support reaches the Cat Care Guide (M19a).**

Fixed
* **The eleven guide pages register the service worker.** They never loaded `assets/js/pwa.js`,
  because the guide generator and the application generator had drifted apart, so a visitor whose
  first page was a guide got no worker and no offline banner until they opened an application
  page. Recorded in PRD section 24.6 during M19 and closed the same day.
* **A guide page that has been read stays readable offline.** Registering the worker was only
  half of it: navigations were network-first and wrote nothing to any cache, so a guide read a
  minute ago vanished with the signal. A successful navigation is now kept when its address
  carries no query string. That condition is deliberate. Every product is the same document under
  a different query, so caching those would add a byte-identical entry per product viewed and
  grow the shell cache without bound, which is why navigations were not cached at all before.
  Guide pages have no query string, and neither will most pages added later.

Changed
* `tools/check-live.py` is 22 checks. The scope check registers from `/learn/nutrition/` now,
  the deepest page on the site, rather than from `/search/`, which was as deep as M19 could
  manage because no guide page would register anything. A new check reads a guide page, goes
  offline, and requires that page back and an unread one to fall through to the offline page.

Not changed
* `sw.js` stays at `v4`. The version lever exists to retire cached content that has become
  wrong, and nothing under `v4` is wrong. Bumping it as a changelog gesture would re-download
  the shell on every device for nothing.
* The guide pages are still not precached. Eleven documents is about 290 kB on install, on a
  connection this project assumes is bad, for pages a visitor may never open.

---

## [0.20.0] - 2026-09-07

**Every page is a directory now (M19).**

The repository root holds eight files: `index.html`, `sw.js`, `robots.txt`, `sitemap.xml`,
`manifest.webmanifest`, `favicon.svg`, `README.md` and `LICENSE.md`, plus `.nojekyll` and the
git and GitHub files. Each is there because something outside this project requires it to be,
and PRD section 16.4 says which of the four requirements applies to each one. Everything else
moved.

Changed
* **Nineteen page addresses changed.** `/search.html` is `/search/`, `/learn-nutrition.html` is
  `/learn/nutrition/`, and so on for every page but the home page. The old addresses 404. They
  were retired without tombstones, which section 23.3 normally requires, under a pre-beta
  exception written the same day: no inbound link to any of them is known, the sitemap listing
  them was a day old, and nineteen stub files at the root would have defeated the milestone that
  created them. The exception expires at public beta and is not renewable. All nineteen are
  listed in PRD section 24.6.
* `tests.html` moved to `tools/tests.html`, beside the script that drives it. Its `noindex`
  travelled with it.
* Around 140 paths were rewritten, and not one of them is a hand-written `../` prefix. The
  chrome, the content fragments and the guide modules write the token `{{root}}`; each generator
  substitutes `./`, `../` or `../../` for the depth it is writing into. Nothing upstream of that
  substitution knows how deep its output will sit, which is the property that makes this
  survivable: a wrong prefix works from one directory, 404s from another, and looks identical in
  a diff.
* Scripts measure their own location instead of assuming it. `assets/js/site.js` derives the
  site root from `import.meta.url` and `assets/js/pwa.js` derives the service worker path from
  `document.currentScript.src`, because a file in `assets/js/` is two levels below the root
  whichever page loaded it.
* The service worker is `v4`. A device holding `v3` has nine documents cached under addresses
  that no longer exist, so the caches are replaced rather than migrated.
* `sitemap.xml` is generated by `tools/site/build.py` from the same page lists that write the
  pages. It had gone stale by hand twice, and a sitemap advertising addresses the site does not
  serve is worse than none.

Fixed
* **Every score on the site.** `scoring.js` loaded its additives knowledge base from
  `./assets/data/additives.json`, resolved against the page, so from `/product/` it requested
  `/product/assets/data/additives.json` and every product read "Could not load this product".
  It now resolves against the module.
* **A gate that could not fail.** `tools/check-live.py` passed all twelve page-load checks while
  the site was in exactly that state, because it asked only whether a heading was non-empty and
  "Could not load this product" is a non-empty heading. Each page-load check now asserts a string
  the page cannot print unless it worked. This is the M18 lesson in a second place: a check that
  cannot fail is not a check.
* The first product case in that file claimed to exercise a full guaranteed analysis. Its record
  had lost its ingredient list upstream, so it had quietly become a duplicate of the case below
  it and the scored page was not being checked at all.

Added
* A twenty-first live check: a worker registered from `/search/` must have the whole site in
  scope and must control the home page. A wrongly scoped registration does not fail, it
  succeeds and narrows offline support to one directory with nothing logged anywhere.

Documented
* PRD section 16.4, the root policy, no longer carries the banner saying the repository did not
  satisfy it yet. Section 15.5 records the rule this milestone established: a change whose
  intermediate states are broken ships as one push, gated locally first, because `main` deploys
  on push.
* PRD section 24.6 gained a second row. The eleven guide pages do not load `assets/js/pwa.js`,
  so arriving on one registers no service worker. That is long-standing rather than new, it was
  found while writing the scope check above, and it is recorded rather than fixed here: adding a
  worker registration to eleven pages is a behaviour change, and this milestone is about where
  files live.

---

## [0.19.0] - 2026-09-07

**Confidence travels with the score (M18b).**

Changed
* **Every card that prints a score now prints its confidence.** The band pill reads "Good ·
  medium confidence" rather than "Good", on search results, brand-filtered results and the
  recently-viewed list, and the same text is in the score tile's accessible name. The product
  page and the compare page have stated confidence since M7 and M11; the cards printed a bare
  number, which is the surface the number actually travels on.
* Shown at every confidence level, not only the poor ones. A marker that appears selectively
  makes its absence into a claim.

Added
* Recently-viewed entries store `confidence` beside the score, because the home page redraws
  that card from `localStorage` with no network round-trip. An entry saved before this release
  has none and says "confidence not recorded" rather than guessing; opening the product again
  rewrites it.
* A twentieth check in `tools/check-live.py`: every scored card on a page of results states
  its confidence.

Noted
* Withholding the number below a threshold was considered and rejected. It is the strictest
  reading of tenet 2, but the engine already refuses outright where it knows too little
  (`scorable: false`), and a second quieter refusal on top of that would have cost usability
  without buying honesty. Closes PRD open question 1.

---

## [0.18.3] - 2026-09-07

**Six decisions recorded (no code).**

Four open questions were answered and two rules were set for M19. None of this changes what
the site does today; it changes what the next change is allowed to do.

Answered
* **Open question 1: a low-confidence score is shown, and never without its confidence.** The
  problem was never that the caveat was too quiet, it was that it did not travel: the product
  and compare pages state confidence and the search and brand cards print a bare number. M18b
  will put it on every surface that prints a score, always rather than only when it is poor.
  Not built yet.
* **Open question 3: feeding-trial substantiation is deferred to M12.** The database has no
  such field, so weighting it now would score how well a product was catalogued rather than
  the food itself.
* **Open question 8: the tombstone mechanism gets written when first used.** The first case
  arrived the same day and declined to use one, which is the answer working rather than
  dodging it.
* **Open question 9 stays open, on purpose.** `tools/probe-opff.py` will be extended to report
  the language distribution of ingredient lists first. Nothing is added to `MATCHED_LANGUAGES`
  until that number exists.

Added
* **A pre-beta exception in PRD section 23.3.** An address may be retired without a tombstone
  only when the site is pre-beta, no inbound link is known, the address is under a month old,
  and the retirement is listed in the new section 24.6. It expires at public beta and is not
  renewable, because a carve-out taken once on good grounds is exactly what gets cited a year
  later on none. Used once: the nineteen addresses M19 retires.
* **Section 24.6, deliberate departures from a written policy.** Not errors and not
  discrepancies: rules this project wrote and then knowingly did not follow in a named case,
  with the reason and the bound attached.
* **A deploy rule in section 15.5.** A change whose intermediate states are broken ships as
  one push, gated locally first. The usual rhythm here is commit-and-push per step so that
  stopping anywhere leaves a working site; that assumes each step is independently correct,
  and M19 is not divisible that way.

---

## [0.18.2] - 2026-09-07

**A policy for the repository root (M19, adopted).**

**Nothing moved in this release.** This is the rule being written down before the work,
rather than after it, so the move can be checked against something.

Added
* **PRD section 16.4 now governs the root rather than describing it.** A file may sit at
  the repository root only when something outside this project requires it there: a
  specification, the hosting platform, a GitHub repository convention, or a client that
  probes a fixed path without reading the HTML first. The section lists every permitted
  file with the requirement that earns it its place and what breaks if it moves.
* Two entries in the "Never do these" table: do not add a file to the root, and do not
  create a page as a root `.html` file.
* M19 in the milestone table, marked as adopted and not started, and a roadmap entry saying
  what it will move and why now is the moment.

Noted
* The root holds eight files that the policy permits and twenty-one that it does not. The
  gap is stated at the top of section 16.4 and in the milestone table rather than left for
  a reader to notice, because a target tree that reads as a description is exactly the
  failure section 24 exists to record.
* Moving nineteen pages changes nineteen public URLs on a host with no redirect mechanism,
  so section 23.3 applies to every one of them. That decision is not made here.

---

## [0.18.1] - 2026-09-07

**The test page asks not to be listed (M18a).**

Added
* `tests.html` carries `<meta name="robots" content="noindex, follow">`. It is a developer
  artifact, and a search result pointing at a wall of assertion output under this site's name
  is a worse answer than no result at all.

Unchanged, deliberately
* `robots.txt` is still fully open. A `Disallow` line is the wrong instrument here: it stops
  the fetch rather than the listing, and a URL a crawler may not read can still be indexed
  from a link alone, with no description because nothing was permitted to read it. `noindex`
  says what is meant, and it works only because the crawler is let in to see it. The comment
  in `robots.txt` now records that this is a decision rather than an omission. Closes PRD open
  question 10.

---

## [0.18.0] - 2026-09-07

**Search that searches, and a filter that scans (M18).**

Fixed
* **Text search never searched.** `/api/v2/search` accepts `search_terms`, answers 200 with a
  well-formed body, and ignores the parameter. `chicken`, `salmon`, `zzzzqqq` and no query at
  all returned the same `count` of 1578, the same products, in the same order: the entire
  cat-food category, every time, since M6. Text queries now go to
  `/cgi/search.pl?action=process&json=1`, which returns 32 for salmon, 22 for tuna, 83 for
  chicken and nothing at all for a string that cannot match. Brand-only browses stay on v2,
  whose tag filters were never affected: a brand browse still returns the same 126 it did.
* **The scorable-only filter no longer implies it saw everything.** It filtered the twenty-four
  results on screen, so it could show three and look like an answer. It now fetches the first
  five pages of the query in parallel, dedupes by barcode, filters, and paginates locally. This
  closes PRD open question 4.

Added
* Two checks in `tools/check-live.py`, which is 19 now. A query that cannot match anything must
  render no cards, and a majority of the cards on a `salmon` search must mention salmon. The
  first is the one that matters: an ignored parameter can fake every other answer this suite
  asks for, but it cannot fake an empty result.

Changed
* The count line states its scope. "Showing 1 to 12 of the 12 products in all 32 results for
  “salmon” that can be scored" when the scan reached the end of the query, and "the first 120
  of 1578 results" when it did not, with a note at the foot of the last page saying so again.

Noted
* Two of M15a's five diagnoses were readings of this bug from outside. Results that ignore the
  query look exactly like results ranked badly, and a category size looks exactly like a match
  count. Those entries below are left as they were written; PRD section 24.1 carries the
  correction. Nothing in six gates and 178 assertions caught this, because every check asked
  whether results came back and none asked whether they were the right ones.

---

## [0.17.0] - 2026-09-07

**The site, in all three browser engines (M17).**

Added
* **`tools/check-engines.py`.** The unit suite, all 12 page states and the
  barcode decode round-trip, in Blink (through Edge), Gecko and WebKit. It also
  prints a feature-support matrix so the differences are recorded rather than
  assumed. Playwright's own browser builds, so nothing here drives a browser
  the maintainer is using: `python -m playwright install webkit firefox` once.

Findings
* **Nothing is broken.** 178 assertions pass in all three engines, every page
  renders its expected content in all three, and nothing overflows at 1280px or
  320px anywhere. That is the whole point of the tool: before it, no evidence
  existed either way, and "works on an iPhone" was an assumption.
* **`BarcodeDetector` exists in neither Gecko nor WebKit.** `scanner.js` had
  this roughly right already, calling support "partial, Safari and Firefox
  largely not". Measured, it is not partial on those engines, it is absent, so
  on every browser on iOS ZXing is not the fallback but the whole feature. The
  comment now says the measured thing, and the decode round-trip runs in all
  three engines and passes in all three.
* **CLS can only be measured in Blink.** The Layout Instability API is
  Chromium-only, so M16b's layout reservation is taken on faith for the other
  two engines. It is a `min-height` rather than an engine trick, so the faith
  is reasonable; `check-vitals.py` now says so in as many words rather than
  implying its numbers are universal.
* **What this still cannot test:** headless WebKit exposes no `getUserMedia`,
  which is Playwright's build and not Safari. The camera path in real Safari
  is untested by anything, and no tool in this repository can change that. It
  is recorded rather than glossed.

Closes PRD open question 7, which had stood since the M13 audit.

---

## [0.16.1] - 2026-09-07

**Core Web Vitals, measured under a throttle (M16b).**

Added
* **`tools/check-vitals.py`.** LCP, CLS and Total Blocking Time for 12 pages,
  CPU slowed 4x on a slow-4G connection, 412px viewport, cold cache. Budgets
  are 2500ms, 0.1 and 200ms. Exits non-zero. `--report` names the elements
  that shifted.
* **`preconnect` for the two Open Pet Food Facts origins**, so the handshake
  overlaps with parsing on the pages that call the API. It costs nothing on the
  pages that never do.

Fixed
* **Almost every page dropped its footer when the content arrived.** Six of the
  nine application pages render their body from a fetch, so each is briefly a
  placeholder in a short page with the footer visible under it. The brand index
  measured a CLS of 0.60 against a 0.10 budget, a page of search results 0.86,
  the product page 0.64. `.shell` now has `min-height: 100vh`, which keeps the
  footer below the fold until there is content to push it there. The brand list
  also reserves a screen of height while loading and gives it back in
  `render()`, because its own list is what moves the note underneath it.
  Every gated page is now at or below 0.07, and most read 0.000.

Changed
* **`sw.js` to `v3`.** The shell is served stale-while-revalidate, so M16a's
  stylesheet fixes would have reached a returning device one visit late. A
  contrast fix that arrives on the second visit has not really been deployed.

Ten of the twelve pages are gated. `product.html` and a page of search results
are measured and printed but cannot fail the build: neither can paint until
Open Pet Food Facts answers, and no commit here controls how fast that is. The
product page reads about 2.5s LCP under this throttle, essentially all of it
the API round trip.

Worth recording why this went eleven milestones unnoticed: CLS is invisible on
a fast connection, because the placeholder and the content arrive close enough
together that nothing appears to move. It takes a throttle to see, and there
was no throttled measurement in this project until now.

---

## [0.16.0] - 2026-09-06

**WCAG 2.1 AA, enforced (M16a).**

Added
* **`tools/check-a11y.py`.** axe-core over all 25 page states, each in both
  themes, plus two checks axe does not do: reflow at a 320px viewport and the
  skip link from a cold keyboard. 100 audits, all clean, exits non-zero.
  `--report` prints every violation with its selector.
* **One site-wide focus ring.** There was none before this: the site left it to
  the browser while shipping two palettes and custom card components.
  `:focus-visible`, 2px accent, 2px offset, so it appears for the keyboard and
  not for a mouse click.
* **A blanket `prefers-reduced-motion: reduce` block.** Exactly one component
  honoured the preference before. Smooth scrolling off, every transition and
  animation reduced to nothing.

Fixed
* **Links in running text are underlined.** Colour alone identifies a link
  under WCAG 1.4.1 only at 3:1 against the surrounding text, and accent on body
  copy is 1.53:1 in light, 1.16:1 in dark. This was on all 25 pages, in prose,
  in the footer's closing sentence and on `.prose-link`. An underline that
  appears only on hover is no use to somebody reading rather than pointing.
* **The search pager's unavailable direction** carried `opacity: .45`, which
  put it at 2.11:1: the one piece of text on the site below AA. It is told
  apart from the live control by having no border and no card, which was always
  the real signal.
* **The compare page needed 490 pixels in a 320 viewport.** A bare `1fr` grid
  track has `min-width: auto` and will not shrink below its content, so
  `.cmp-row` uses `minmax(0, 1fr)`; `.cmp-cell` adds `overflow-wrap: anywhere`,
  because a product name from a community database can be one unbroken token
  wider than the cell. Below 380px the cells tighten and the thumbnail drops to
  40px.
* **The top bar's support button** pushed the bar past 320px. It hides below
  400px. It is the one thing in the bar nobody came for, and the same link is
  in every footer.

Two failures the tool reported that were not real, kept here because the next
person to add a gate will meet them: setting `data-theme` and auditing in the
same tick measures colours part-way through a 150ms transition, which reported
the entire top bar as a dark-mode contrast failure; and tabbing to the skip
link and reading its box in the same tick catches it mid-slide, which reported
it as off-screen on all 25 pages. Both were the tool. A new gate's first red is
as likely to be the gate as the code.

Documentation now says what the gate does not cover. axe finds the
machine-checkable third of WCAG; PRD section 19.1 lists what was checked by
hand alongside it, with the answers, so a green run is never read as "the site
is accessible". No screen reader has been run against this site, and that is
still true.

---

## [0.15.3] - 2026-09-06

**Stale claims swept out of the documentation and the source comments.**

Fixed
* **Four source comments still described a site with Tailwind pages in it.**
  `cfc.css` called itself the Learn section's stylesheet and said the palette
  file was loaded by "the Tailwind pages that do not load this file";
  `cfc-tokens.css` named index, search, product and methodology as Tailwind CDN
  pages; `sw.js` routed "fonts, Tailwind, ZXing" to the network; and
  `tools/learn/shell.py` said the theme toggle was hand-copied into four pages.
  M14 removed all of that four milestones ago. A comment that describes an
  architecture the reader cannot find is worse than no comment: it sends them
  looking for something that is not there.
* **The milestone table had no M15d row**, though it shipped the same day.
* **Two debt rows described shortcuts that no longer exist.** "Product page
  rail" was closed by M15d and "Per-page `<style>` blocks" by M14.
* **The dangerous-to-change table warned about Tailwind opacity modifiers**, a
  hazard that cannot be reached from any file in the tree.
* **"Eight hand-copied page chromes" was the wrong fragility to name.** M14
  ended that edit and created a different one: `chrome.py` is the only copy
  now, so a mistake in it is a mistake on all twenty pages at once. The row
  says that instead.
* **The unpinned-CDN row named Tailwind**, which is gone. ZXing is the one
  still fetched at runtime.
* **Section 25.4 read as a status section but held a snapshot** from the M13
  audit, saying M14 was unbuilt and M15b planned. Both shipped.

---

## [0.15.2] - 2026-09-06

**The product page builds its own "On this page" rail (M15d).**

Added
* **A third column on `product.html`**, listing the sections of the breakdown
  and highlighting the one in view, the same rail the guide and the methodology
  page have had since M4. It is the only chrome on the site assembled in the
  browser, and it is confined to the one page whose content is also assembled
  in the browser.
* **A third state in `build.py`'s `PAGES` table.** The rail column was a
  boolean; it now takes `False`, `True` (the generator reads the headings out
  of the fragment, and the build fails if there are none) and `'client'` (the
  column ships empty, hidden and marked `data-client-toc`). A page still cannot
  claim a rail it has nothing to put in.
* A live check that the rail has one link per heading and one active link.
  17 of 17.

Changed
* **The scroll spy in `cfc-docs.js` is re-runnable rather than one-shot.** It
  used to bail on an empty rail and never look again, which is exactly the
  state a client-rendered page is in at load. Each run now disconnects the
  observer and scroll listener the previous one installed, so a redrawn article
  cannot leave a spy watching elements that have been replaced.
* **Every draw of the product article goes through one `paint()` function**,
  which assigns the HTML and dispatches `cfc:content`. Routing all four draws
  through it is what makes the "not found" case correct: that draw has no
  sections, and the rail hides itself again rather than keeping the last
  product's list.

Closes PRD open question 11.

---

## [0.15.1] - 2026-09-06

**Ingredient rows that explain themselves (M15c).**

Added
* **An ingredient the additive knowledge base recognises now opens** to show
  its function, its health impact on a cat, the regulatory position and the
  sources, plus the alias the match fired on. Native `<details>`, so keyboard
  support, screen-reader announcement and open state all come for free and none
  of it has to be rebound when the page redraws itself.
* **`explainIngredient(entry, kb)`** in `scoring.js`, using the same
  `matchesTerm` the engine scores with. An ingredient the additive pillar
  penalised cannot fail to explain itself, and one it ignored cannot claim to
  have been counted.
* A count under the list, so the page only claims rows expand where some do.
* Eighteen assertions covering the matcher, the tier ordering, the vague-term
  fallback and the case below. 178 passing.

Fixed
* **The explanation could contradict the score.** The engine withholds Tier 0
  credit from an entry that is itself an unnamed source, because one ingredient
  cannot be both a named organ meat and an unnamed one. "Viandes et
  sous-produits animaux" matches the beneficial named-by-products entry on a
  bare stem while the transparency pillar penalises the very same words. The
  first build of this labelled that row "Beneficial" while the score was
  marking it down. It now makes the same call the engine made.

Notes
* **This is not a general ingredient dictionary and is not meant to become one
  by accident.** It answers for the 20 additives and 3 vague-term groups in
  `additives.json` and returns nothing for anything else. There is no true
  thing this project can add to the word "chicken", and padding every row with
  filler would bury the rows that matter.
* **A documentation correction.** PRD section 24.1 and DESIGN section 13 had
  both recorded, since M2, that "the chevron is rendered and does nothing". No
  chevron was ever rendered: the string appears in no commit's code. The entry
  was not stale, it was wrong, and it survived three milestones because nobody
  checks a claim that sounds like a confession. Both documents now say so.

---

## [0.15.0] - 2026-09-06

**A picture of the tin, everywhere a product is listed (M15b).**

Added
* **Photos on search results, on recently viewed, and on both sides of the
  compare page.** `opff.js` had been fetching `image_front_url` since M6 and
  only the product page rendered it, so this is rendering work rather than
  plumbing. It answers the last unaddressed half of the owner's feedback on the
  live site: "There's no photo either."
* **`assets/js/thumb.js`**, the one copy of the thumbnail. Three surfaces show
  the same 56px box and none of them should own the rules for it.
* **A placeholder for products with no photo**, a paw outline in the same box.
  Coverage is good but not complete, and a list where some rows carry an image
  and some carry nothing is visibly ragged in a way that reads as a rendering
  fault rather than as missing data. A photo that fails to load is replaced
  with the same placeholder.
* **`product.thumbUrl`**, the 200px rendition. The 56px box does not need the
  400px file; `product.imageUrl` keeps the larger one for the product page.
* `thumbUrl` is stored with a recently-viewed entry, so a card can be redrawn
  from this device with no network. It is a URL on the catalogue's own image
  host, not a copy of the picture.

Changed
* **The product row is now photo, name, score.** The score tile moved to the
  right edge and the chevron that used to sit there is gone: two glyphs on the
  same edge of the same link is one more than the row needs, and the whole row
  was always the link. The compare page keeps the photo and the tile together,
  because its column is narrow and stacks below 700px.
* `assets/js/thumb.js` joins the precached shell, so the placeholder renders
  offline.

Fixed
* **The service worker was routing product images to the wrong cache.** It
  asked `isApi(url)` before `isImage(request)`, and photos are served from
  `images.openpetfoodfacts.org`, which `isApi` matches. Every image took the
  network-first path into the API cache: revalidated on every view when the
  bytes never change, and counted against the wrong cache. It was invisible
  while one photo existed on one page. Putting a photo on every card is what
  made the ordering matter.

Notes
* 23 of 24 results in a live search for "chicken" carry a photo, and none of
  the 24 rendered a broken image.
* The failure path is one delegated listener in the capture phase, not an
  `onerror` attribute. There is no inline event handler anywhere else in this
  codebase, and the first one would be the only thing standing between the site
  and a Content-Security-Policy header.
* 160 browser assertions, 16 of 16 live checks, contrast audit clean.

---

## [0.14.0] - 2026-09-06

**One interface across the whole site, and the nine application pages stop
being hand-written (M14).**

Added
* **`tools/site/chrome.py`**, the single copy of the head, top bar, drawer and
  footer. `tools/learn/shell.py` imports it, so the guide pages and the
  application pages cannot drift apart. `NAV` is one list of seven
  destinations; adding a link is one edit rather than nine.
* **`tools/site/build.py`**, which wraps that chrome around a body fragment
  per page from `tools/site/content/`. The generated pages are committed, so
  deployment still needs no build step (ADR-001). This is the pattern the
  Cat Care Guide has used since M4.
* **`assets/cfc-app.css`**, roughly 330 lines: the utilities the page modules
  actually emit and the components they build. It replaces the Tailwind CDN
  and nine per-page `<style>` blocks.
* **`.topbar-nav`**, the inline site navigation above 900px, with
  `aria-current="page"` on the current destination.
* **A site menu in the drawer** below 900px, on every page. On a guide page the
  guide's own section list is nested beneath it: one control, two levels.
* **An "On this page" rail on `methodology.html`**, built by the generator from
  the `<h2 id="...">` elements in the fragment.

Changed
* All nine application pages are now generated. **Do not hand-edit
  `index.html`, `search.html`, `brands.html`, `product.html`, `scan.html`,
  `submit.html`, `compare.html`, `methodology.html` or `offline.html`**: edit
  the fragment in `tools/site/content/` and rerun the generator.
* `sw.js`: `SHELL_ASSETS` picks up `cfc.css`, `cfc-app.css` and `cfc-docs.js`
  and drops `cfc-tailwind.js`. `VERSION` is `v2`, so the new shell installs
  over the old one rather than being merged into it.
* `tools/check-live.py` looks the shell cache up by its `cfc-shell-` prefix
  instead of by full name. `caches.open()` creates an empty cache when the name
  is wrong, so the hard-coded `cfc-shell-v1` turned a version bump into a
  silent zero rather than into a failure. It failed loudly first, which is how
  it was found.
* The top-bar search field is hidden on `index.html` and `search.html`, which
  carry a search input in the body. Two routes to the same place inside one
  viewport is a papercut. Closes PRD open question 6.
* A page with no headings to index collapses to one column rather than showing
  an empty rail, and the generator decides that per page by reading the
  fragment. Closes PRD open question 5.

Fixed
* **`.article a` outranked every component that colours its own anchor.** The
  rule is `.article a:not([class])` now, which is prose only. The visible
  symptom was the home page's round scan button rendering as accent text on an
  accent circle, invisible until you clicked it.
* **The drawer took a grid column on `.shell-app-toc`** and pushed the article
  onto the next row, which rendered `methodology.html` as a blank screen at
  every width above 900px. Both application shells are named in the rule now.
* **`.text-display` lost its size in the port**, so a product's score rendered
  at body size instead of 3rem. It had been defined identically in nine files;
  consolidating nine copies into one is exactly where a value goes missing. The
  whole port was then re-checked by diffing every rule in the old inline blocks
  against the new stylesheet.
* `tools/learn/shell.py` emitted a `</nav>` with no opening tag while the
  drawer was being rewired, so the guide pages briefly shipped an unbalanced
  sidebar.

Removed
* `https://cdn.tailwindcss.com` and `assets/cfc-tailwind.js`, from every page
  and from the repository. It was a render-blocking third-party script,
  unpinned, whose content could change without a commit here. It was the
  project's last unpinned runtime dependency and the one item that made
  Lighthouse numbers unstable enough to be worth deferring M12's gates over.
* The nine per-page `<style>` blocks.
* `.footer-link`, which had one user left and duplicated `.prose-link`.

Notes
* 160 browser assertions pass, 16 of 16 live checks pass, and the contrast
  audit passes on both palettes.
* The product page has headings worth indexing but they are written by
  `product-page.js` after the fetch returns, so the generator cannot see them.
  It has no rail. Carried as PRD open question 11.

---

## [0.13.0] - 2026-09-06

**Search that reaches past the first page, a brand index, and a full
documentation audit.**

Added
* **Pagination on search.** `searchProducts()` already accepted a `page`
  argument and the page never passed it, so 24 of 1571 results were reachable
  and nothing led to result 25. Page state lives in `?page=`, so a position in
  a result set is a link somebody can send.
* **Brand browse** at `brands.html`: an A to Z index of every cat food brand
  with more than one product, filtered locally as you type. The list comes from
  the facet endpoint at
  `world.openpetfoodfacts.org/facets/categories/Cat%20food/brands.json`, which
  is outside the v2 API but is CORS-enabled and lists 439 brands with counts.
* **Brand-filtered results** via `?brand=`, using `brands_tags`.
* **A scorable-only filter** on search, written to the URL as `?only=scorable`.
* `mergeBrandTags()`, which folds case-variant duplicates. Nine brands in the
  facet collide on case alone: `purina` at 110 products and `Purina` at 15 are
  the same brand shown twice with split counts. The merged brand is queried in
  one request as `brands_tags=purina|Purina`, because `|` is OR in a v2 tag
  filter and a comma is AND. That was measured against the live API, not read
  in documentation: the comma form returns 0.
* Thirteen assertions covering brand merging and display names, using the real
  measured facet as fixtures. The suite is now 160 assertions.
* Four end-to-end checks: the brand index, a second page of results, a
  brand-filtered search, and the scorable filter. `tools/check-live.py` is now
  16 checks.
* `LICENSE.md`, `robots.txt` and `sitemap.xml` at the repository root. The
  project had no licence of any kind before this release.

Changed
* **Search results are ordered by relevance again.** A scorable-first re-sort
  had been discarding the API's ranking, so the closest match to what somebody
  typed could sit below a loosely related product that happened to score well.
  Scorability is now an opt-in filter rather than a hidden sort key, which
  answers the question that was asked instead of a different one.
* The scorable-only filter is honest about acting on the page you are looking
  at rather than on the query. The API cannot filter on scorability, and
  pretending otherwise would misreport the result count.
* **Eleven documents in `/docs` consolidated into three.** `docs/PRD.md`
  absorbed TRD, RUNBOOK, METRICS, TENETS, SECURITY, PRFAQ, ROADMAP, ADR-001 and
  DATA-COVERAGE, and is now the single source of truth. `docs/DESIGN.md` was
  rewritten around the guide's design system, which is what M14 ports the rest
  of the site onto. `README.md` was rewritten for a general reader, with the
  stack, prerequisites, commands and deploy steps moved into the PRD.
* **`tools/run-tests.py` and `tools/check-live.py` now drive Edge, never
  Chrome**, through Playwright's `msedge` channel. Chrome is the maintainer's
  day-to-day browser and driving it disturbs a live session. Verified against
  Edge 152 before the rule was written down, so it was true on arrival rather
  than aspirational.
* Em dashes removed across the project in all three forms: the literal
  character, the `, ` entity, and a double hyphen used as punctuation. The
  guide pages were fixed at their `tools/learn/c_*.py` sources and regenerated,
  not edited in place.

Fixed
* **The live check would have started reporting a working search page as
  broken.** It read the first heading with `querySelector`, which returns the
  first match in *document order* rather than in selector order, and the new
  `#results-heading` stays empty unless the results are a brand. It now takes
  the first non-empty match.
* Five documentation claims that a reader would have acted on, the worst being
  an instruction to run the test suite under `node --test` in a project that
  has no Node.js by decision, and a security document asserting that React's
  JSX handling escapes all rendered content. There is no React; escaping is
  hand-rolled `esc()` calls, and that is now recorded as the highest-risk area
  in the codebase.

Removed
* `docs/TRD.md`, `docs/RUNBOOK.md`, `docs/METRICS.md`, `docs/TENETS.md`,
  `docs/SECURITY.md`, `docs/PRFAQ.md`, `docs/ROADMAP.md`,
  `docs/ADR-001-static-first.md`, `docs/DATA-COVERAGE.md`, and `PATCHNOTES.md`
  at the repository root. Every one is folded into a named section of the PRD
  or into this file, and PRD section 23.5 records where each went.

Notes
* **What the search feedback actually turned out to be.** The owner's note was
  "the search doesn't really work at all; just see what catfooddb is like;
  that's a lot better; there's no photo either". Five separate causes were
  confirmed, and the most useful observation was about the reference site:
  CatFoodDB is organised brand-first, with an A to Z of over 150 brands and
  curated best-of lists, and **its own free-text search is disabled**, with a
  notice on the site saying so. The site that was preferred is better *without*
  working search, which inverted the fix from "build a better ranker" to "build
  a browse structure".
* **The missing photo is a rendering gap, not a data gap**, and is not fixed
  here. `opff.js` already requests `image_front_url` and exposes
  `product.imageUrl`, and 23 of 24 live results carry one. Only
  `product-page.js` draws it. Held until after M14 so the result card is not
  built twice.
* The offline shell is 29 entries, up from 27, having gained `brands.html` and
  its page module.
* **The em dash sweep, in numbers.** 64 files carried at least one of the three
  forms. 568 literal characters and 26 `&mdash;` entities were replaced across
  49 hand-written files, and the eleven generated guide pages picked up the
  rest when they were rebuilt from their swept sources. The replacement was
  chosen per instance rather than applied uniformly: a hyphen in titles and
  headings, a colon after a label, a semicolon between two independent clauses,
  parentheses around a short aside or a trailing citation, and a comma
  everywhere else. A blanket comma would have introduced a comma splice
  wherever the dash was joining two complete sentences.
* **Two instances were left in place because the text needs them.** A regular
  expression character class in `opff.js` strips leading punctuation, em dash
  included, from ingredient text arriving from the API: removing the character
  would stop it working. And PRD section 18 has to name `&mdash;` in order to
  prohibit it. Everything else that a naive search still reports is a `--` that
  was never punctuation: HTML comment delimiters, `var(--token)`, ASCII
  diagrams, and `--noEmit`.

---

## [0.12.2] - 2026-09-05

**Owner feedback on the live site recorded as a milestone (M15).**

Added
* `docs/ROADMAP.md` M15: make search work, and show the product. The feedback is quoted verbatim, and the entry records what was measured on the day rather than the complaint alone. Planned, not scheduled, not started.

Notes
* **The missing photo is a rendering gap, not a data gap.** `opff.js` already requests `image_front_url` and exposes it as `product.imageUrl`, and 23 of 24 results in a live "chicken" search carry one. Only `product-page.js` draws it; the search cards, the compare page and the recently-viewed list all have the URL in hand and render nothing.
* **Five confirmed causes for search.** No pagination, and the page never passes the `page` argument `searchProducts()` already accepts, so 24 of 1571 results are reachable. API relevance is discarded by a deliberate scorable-first re-sort. The match is not restricted to name or brand, so a chicken query returns ocean fish above real chicken products. The records themselves are poor, with brands stored as numeric ids and names left untranslated, and the cards render them faithfully. And there is no filter, facet, sort or brand browse to compensate.
* **The reference site inverts the request, which is the useful part.** CatFoodDB's homepage was read on the day: it is organised brand-first with an A-Z of 150-plus brands and curated best-of lists by food type, and **its own free-text search is disabled**, with a notice saying so. It is better without working search, which suggests the answer is a browse structure rather than a better ranker. Its product-entry layout was not verified: two guessed URLs returned 404, and the entry says so rather than describing a page nobody opened.

---

## [0.12.1] - 2026-09-05

**Documentation brought back in line with the code, and two milestones planned.**

Added
* `docs/ROADMAP.md` M13: a documentation consolidation audit. Collapses the eleven files in `/docs` to `PRD.md`, `DESIGN.md` and `PATCHNOTES.md` plus the root README, and adds the root-only files the project has never had (`LICENSE.md`, `robots.txt`, `sitemap.xml`). The full method, the target structure, the merge-rather-than-overwrite rule, and the defaults for writing style, browser testing, verification environment, licensing and removal policy are written out in the milestone so the scope survives the session that requested it. Planned, not scheduled, not started.
* `docs/ROADMAP.md` M14: move the whole site onto the interface built for the Cat Care Guide. The blocker is recorded as the first thing to solve rather than a detail, the guide top bar has no page navigation at all, while the app top bar has the six-link nav but neither the search affordance nor the sidebar control, so the merged bar has to carry both on a 360px phone. Four open design questions and six codebase constraints are listed. Planned, not scheduled, not started.

Fixed
* **Stale counts.** `docs/TRD.md` claimed the precached shell was 23 entries; `sw.js` has held 27 since M10 and M11 added pages. The TRD tree described `tools/check-live.py` as eight end-to-end checks; it has been twelve since M11.
* **Stale version.** `docs/TRD.md` §0 was headed "Current implementation state (v0.7.0)" five releases after v0.7.0, and its list of what is implemented omitted the compare page, the submit page and offline support.
* **"Four Tailwind pages" was wrong in five places** across `README.md` and `docs/TRD.md`. There are eight. The TRD's advice that a fifth would be the trigger to move them under the generator has been rewritten, since that threshold was crossed without anyone noticing and the duplication is now real debt rather than a hypothetical.
* **A testing instruction that could not work.** `docs/TRD.md` §12 described the scoring tests as runnable "under `node --test`". There is no Node.js in this project by decision ([ADR-001](docs/ADR-001-static-first.md)), and the suite is browser-hosted only.
* `docs/TRD.md` §8 routing table was missing `offline.html` and `tests.html`.

Notes
* Historical changelog entries were left alone. The "23 entries" in the v0.10.0 notes was accurate when written, and rewriting it would turn a record of what happened into a claim about the present. The roadmap's M9 entry now reads "23 entries at the time, 27 today" for the same reason.
* No code changed in this release.

---

## [0.12.0] - 2026-09-05

**Side-by-side comparison (M11).**

Added
* `compare.html?a=X&b=Y`: two products next to each other. The URL carries the comparison, so it can be shared and reloaded. Products already viewed are offered in a picker; anything else goes in by barcode.
* Figures converted to a **dry-matter basis**. Without that a wet food at 11% protein reads as worse than a dry food at 32%, when it is in fact the more protein-dense of the two; the wet food is mostly water.
* A `Compare` entry in the top navigation.

Notes
* **The page never declares a winner on the overall score, and that is the point of it.** A 72 worked out from three pillars and a 72 worked out from one are different claims wearing the same number. Only about a fifth of products carry enough data for all three pillars, so this is the normal case rather than an edge case. Where the two products were scored on different pillars, the page says so before showing anything else, and the comparison is pillar by pillar, only across pillars both products actually have.
* **Where only one product publishes a figure, neither cell is highlighted.** Marking the one that happens to have data would be a comment on the database rather than on the food.
* Fat is shown without a "better" direction. More fat is not simply better, and pretending a single number has an obvious direction is how a comparison tool starts lying.

---

## [0.11.0] - 2026-09-05

**A real answer for a product that is not in the database (M10).**

Added
* `submit.html?barcode=X`, reached from the not-found state on any product page.
  * **Rules out a typo first.** A mistyped digit looks exactly like a missing product, and it is the only cause the visitor can fix in five seconds. The page checks the barcode against its own check digit and re-queries the database before sending anyone off to photograph a tin. If the product turns out to be there after all, it links straight to its page.
  * **Names the two panels that matter.** The ingredient list (without it there is no score at all, not a low one) and the guaranteed analysis including moisture, without which a wet food cannot honestly be compared to a dry one.
  * **Deep-links the contribution** to Open Pet Food Facts with the barcode filled in, and says plainly that the form is hosted on Open Food Facts, the project's main site, so the hand-off is not a surprise.

Changed
* The not-found state now links here rather than dropping the visitor straight onto an unexplained external form.
* `docs/ADR-001-static-first.md` updated: the "no server-side writes" row predicted a hosted form or a GitHub issue as the workaround. Building it showed the workaround was the wrong shape, and the ADR now records why.

Notes
* **There is no submission queue of our own, by choice.** A private queue (hosted form, GitHub issue, serverless endpoint, any of them) would fork the catalogue. The product would sit in our queue and still be missing from the database every score on this site actually reads, which would make us the bottleneck for our own corrections. Sending it upstream means it works here, in the next tool built on the same database, and for the next person who scans the same tin.
* The general lesson, recorded in the ADR: not every limitation of static hosting needs a workaround. This one was better answered by not holding the data at all.

---

## [0.10.0] - 2026-09-05

**Offline support, and installability (M9). The app works in the aisle where the signal does not.**

Added
* `sw.js`: a hand-written service worker. No build step means no Workbox, and that turned out to be the better outcome: every caching decision is one of three strategies, chosen per resource, with the reason written next to it.
  * App shell precached (23 entries), so every page renders with no network at all.
  * API responses **network-first**: a cached answer is a fallback, never a preference.
  * Images cache-first; they are large and never change under a URL.
  * Third-party CDNs left alone. They set their own cache headers, and second-guessing them from here would mean owning their invalidation too.
* `offline.html`: for a page never opened on this device. It says what still works rather than showing the browser's own error page.
* `manifest.webmanifest` and generated icons at 192, 512 and 512-maskable. The app installs to a home screen and opens standalone.
* `assets/js/pwa.js`: registration (on `load`, so it never competes with rendering) and an offline banner.
* Two more checks in `tools/check-live.py`: the worker precaches and does not grow per product viewed, and an offline product still renders **and is labelled**.

Changed
* A product page served from cache now says so, with the time it was saved. The worker stamps the response, `opff.js` carries the stamp through, and the page renders a notice.

Notes
* **A cached score must never be presented as a current one.** The scoring engine changes and the database changes, so a stale score rendered as fresh is the same failure as the English-only matcher, confidently wrong, with nothing about it looking wrong. That rule is why the stamp exists, and it is written at the top of `sw.js` so the next change to that file has to reckon with it.
* **Navigations are deliberately not cached.** Every product is `product.html` under a different query string, so caching responses would add one byte-identical entry per product viewed and grow the shell cache without bound. The precached document is found with `ignoreSearch` instead, and without that flag an offline product page would fall through to `offline.html` despite the document being cached.
* **A 404 is never cached.** It is how an unknown barcode is detected, and caching it would keep reporting "not found" after the product is added to the database.
* `navigator.onLine` is trusted only in the negative direction. It reports a network interface, not reachability, so a false "you are online" shows nothing rather than a wrong reassurance.

---

## [0.9.0] - 2026-09-05

**The scanner (M8), and a home page that shows your own history instead of two invented products.**

Added
* `scan.html` and `assets/js/scanner.js`, barcode scanning, entirely client-side. Frames are decoded on the device and never uploaded; the only thing that leaves is the barcode number, to look the product up. `BarcodeDetector` is used where the platform provides it, and ZXing is downloaded only when it does not,  never speculatively.
* `assets/js/scan-page.js`: the part that has to be kind about failure. Declined permission, no camera, camera held by another app, a browser with no camera API and a page not on HTTPS each get their own sentence and their own suggested next step.
* Manual barcode entry on the same page, always visible. On a desktop browser it is the primary path, not a consolation prize. Entries are checksum-validated before navigating, so a typo is reported as a typo rather than as a gap in the database.
* `assets/js/history.js`, `assets/js/home-page.js`, "Recently viewed", kept in `localStorage` on the device and nowhere else. There is no account and no sync, which is a feature of the static architecture rather than a limitation of it: what someone feeds their cat is not information we have any reason to hold. Only barcode, name, brand and the last score are stored, and opening a product recomputes the score rather than trusting the stored one.
* A `Scan` entry in the top navigation of every page.
* `assets/js/scanner.test.js`: 17 assertions on barcode validation. The full suite is now 147.
* `tools/check-live.py` grew to 8 checks: the scan page, the home page, a recently-viewed round-trip across two page loads, and a decode round-trip that draws a known EAN-13 and reads it back.

Changed
* The home page Scan button is a real link. It was disabled with a "Coming soon" tooltip.

Removed
* The two invented "Recently viewed" products (Weruva and Friskies, with hardcoded scores). The section now hides itself until there is something real to show, an empty list on a home page reads as something broken.

Notes
* **UPC-E cannot be checksum-validated in place.** Its check digit is computed over the expanded UPC-A form, so validating an 8-digit UPC-E under the EAN-8 rule rejects it. That failure is silent: the scanner would keep scanning and simply never see small US packages. `expandUpcE` exists for this, and an 8-digit code is accepted if either reading checks out.
* **`getUserMedia` needs a secure context.** `http://<LAN-IP>` is not one, so testing from a phone on the local network gives no camera at all, with no error that says why. The page distinguishes that case from a real fault.
* QR codes are deliberately excluded from the format list. Packaging carries them, and a QR code is not the product's barcode.

---

## [0.8.0] - 2026-09-05

**The scoring engine, the API client, and the two pages that use them. The product is now real: enter a barcode and get a derived score with its reasoning.**

Added
* `assets/js/opff.js`: Open Pet Food Facts client and normaliser. Reads both nutriment schemas (preferring the pet-food guaranteed analysis over Open Food Facts' human-food keys) and records which was used; gates every figure against a plausible range for cat food; infers per-kilogram energy values and corrects them; splits ingredient strings on depth-aware commas so a parenthetical stays with its parent ingredient.
* `assets/js/scoring.js`: the CFC Score. Pure and deterministic: no network, no DOM, runs in the visitor's browser so a sceptical reader can watch a score being derived. Renormalises pillar weights across the pillars that could be computed, applies the two hard gates, and returns `scorable: false` rather than a number when too little is known.
* `assets/js/product-page.js`, `assets/js/search-page.js`, replace the mock render blocks. `product.html` went 475 → 102 lines, `search.html` 166 → 99.
* `assets/data/additives.json`: 20 additives across three tiers plus three catch-all label terms, each with function, tier, plain-language health impact, regulatory note and sources. Tiers mirror the guide.
* `tests.html`, `assets/js/test-runner.js`, `tools/run-tests.py`, 130 assertions run headlessly in a real browser. No Node, no build step, consistent with ADR-001.
* `tools/probe-opff.py`, `tools/check-live.py`, the measurement script behind `docs/DATA-COVERAGE.md`, and an end-to-end check of four page states against the live API.
* `docs/DATA-COVERAGE.md`: what the database actually contains, measured across 600 products.
* **methodology.html: "What the score cannot see."** The limits are now published alongside the method, because a score that does not state what it could not check is overclaiming.

Fixed
* **A French product scored 77 / Excellent with a perfect transparency pillar and the reason "Ingredient sources are named rather than generic." Its first ingredient was unnamed meat by-products and its last was sugar.** Only 9.5% of records carry English ingredients, and the alias matcher was English-only, so on ~90% of labels it matched nothing, and nothing matched was being reported as clean. Four distinct defects sat behind that single score, and three of them were live in English too; they had simply never fired, because the test fixtures were written in the same language as the matcher. Full write-up in `docs/DATA-COVERAGE.md`.
  * Aliases extended to French, German, Spanish, Italian and Dutch, in `additives.json` and in the animal-protein, plant-protein and starch lists.
  * `MATCHED_LANGUAGES` guard: where the label is in a language the aliases do not cover, the engine says the list could not be read, withholds the clean-formulation bonus and the "no flagged additives" finding, caps confidence at low, and warns. **Silence is not evidence.**
  * The Tier 0 "named by-products" credit had bare stems as aliases, so *"meat by-products"* earned a bonus for being a named source while the transparency pillar penalised the identical words for being unnamed. Tier 0 credit is now matched per ingredient entry and withheld where that entry is itself an unnamed source.
  * A parenthetical could rename an unnamed source: `(dont boeuf 4%)` made "viandes et sous-produits animaux" read as a named beef first ingredient, worth full marks. Such entries are now judged on the text before the parenthesis, across the whole first-three window.
  * The nutrition pillar now has an explicit branch for an unnamed leading protein, so the most important thing the list says is what gets reported, rather than whatever happened to appear second.
* Alias matching missed plurals (aliases are written singular, labels are plural) so the unnamed-source penalty never fired on a real label.
* The animal-protein check ran on the first three ingredients before the plant-protein check ran on the first, so a list led by pea protein scored as animal-protein-first the moment chicken fat appeared third.

Notes
* `docs/DATA-COVERAGE.md` overturned the M6/M7 assumption that most products carry a full guaranteed analysis. About a fifth are scoreable on all three pillars, and a quarter of the products carrying a protein figure carry an implausible one. Partial data is the normal path, not an error path, and both modules are built around that.
* The unit suite was 109 green while all four scoring defects above were live. Rendering one real product page found what the whole suite could not.

---

## [0.7.0] - 2026-09-05

**Light/dark theming across the whole site, and the end of the Next.js fork in the repository.**

Added
* `assets/cfc-tokens.css`, the palette, split out of `cfc.css` so both page families share one source of truth: the four Tailwind CDN pages and the eleven generated guide pages. Carries the light values, the dark values (twice,  once for an explicit choice, once for `prefers-color-scheme`), the theme toggle component, and the chip component.
* `assets/cfc-theme.js`, three-state theme control: system → light → dark. Persists under `localStorage` key `cfc-theme`; `system` stores nothing and lets the media query decide. Loaded as a **blocking** `<script>` in `<head>`, which is what prevents a flash of the wrong palette. A `storage` listener keeps other open tabs in step, and a blocked-site-data failure falls back to the system theme rather than throwing.
* Theme toggle in the top bar of all fifteen pages.
* `tools/check-contrast.py`: audits all 38 foreground/background pairs in both palettes against WCAG AA, and fails if the two duplicated dark blocks have drifted apart.
* `docs/ADR-001-static-first.md`: records static HTML as the target architecture rather than an interim state, with the reasoning per planned feature and, more usefully, the list of what static hosting genuinely cannot do and the escape hatch for each.

Changed
* Tailwind colour names now resolve to `var(--...)` instead of hex literals, so `bg-surface` and `text-ink` follow the theme with no `dark:` variants in the markup. **Trade-off:** Tailwind opacity modifiers (`bg-surface/50`) no longer work on those colours, add a token instead.
* Every hardcoded colour on the four Tailwind pages, including the ones generated by JavaScript in `product.html`, now goes through a token.
* The green and amber score chips previously used white text at 2.8:1 and 2.3:1. They now use dark ink. **This changes the light theme's appearance**; it was a pre-existing accessibility defect that building the second palette surfaced rather than caused.
* `README.md`, `docs/TRD.md`, `docs/RUNBOOK.md` and `docs/DESIGN.md` rewritten to describe the stack that actually ships. They previously documented Next.js, npm scripts, `next.config.ts` and a build pipeline, none of which existed in the deployed site.
* `.github/workflows/deploy.yml`: the "when transitioning to Next.js" comment replaced with a pointer to ADR-001.

Removed
* The unused Next.js 14 application: `app/`, `components/`, `public/`, `next.config.ts`, `package.json`, `postcss.config.mjs`, `tailwind.config.ts`, `tsconfig.json`, `.eslintrc.json`. It was never built and never deployed, `deploy.yml` has always uploaded the repository root,  but it was documented as the stack, which made the repository actively misleading. It remains in git history if it is ever wanted back.

Notes
* Confirmed while writing ADR-001: the planned barcode scanner needs no server. `getUserMedia` + `BarcodeDetector` (ZXing WASM fallback) + the keyless, CORS-enabled Open Pet Food Facts API all run in the browser. The only hard requirement is HTTPS, which GitHub Pages provides. One consequence worth remembering: `http://<LAN-IP>` is not a secure context, so testing the scanner on a phone means using the deployed URL or an HTTPS tunnel.

---

## [0.6.0] - 2026-09-05

**Added The Cat Care Guide: an eleven-page educational resource, built as a documentation site.**

Added
* `learn.html`: guide overview, the five rules that matter most, and the map of all topics.
* `learn-nutrition.html`: obligate carnivore metabolism, the five adaptations that define feline nutrition, protein/fat/carbohydrate/fibre, and the eight nutrients cats cannot synthesise (taurine, arginine, arachidonic acid, retinol, niacin, vitamin D3, B12, thiamine).
* `learn-daily-requirements.html`: the complete AAFCO Cat Food Nutrient Profiles table (42 nutrients, growth and adult minimums plus maximums), the RER/MER formulas with a life-stage factor table, and a full worked conversion into grams and milligrams per day for a 4.5 kg neutered indoor cat.
* `learn-labels.html`: reading order, AAFCO adequacy statements ranked by strength, the dry-matter conversion with a worked wet-vs-dry comparison, carbohydrate by difference, ingredient splitting, the 95/25/3 naming rules, and marketing terms with no regulatory meaning.
* `learn-food-types.html`: seven formats compared on moisture, carbohydrate, calorie density, cost and safety; includes the current FDA position on H5N1 in raw pet food and the evidence on home-prepared recipes failing nutrient analysis.
* `learn-hydration.html`: water requirements by body weight, a diet-by-diet water balance table, dehydration checks, and eleven ranked ways to increase intake.
* `learn-additives.html`: three-tier additive reference covering 30+ compounds (propylene glycol, ethoxyquin, BHA, BHT, artificial colours, titanium dioxide, menadione, carrageenan, gums, glutamates, inorganic phosphates and more), each with its regulatory position and evidence, plus a section on commonly criticised ingredients that are not actually a problem.
* `learn-feeding.html`: calorie tables for seven body weights, portioning, meal timing patterns, food-based enrichment, a seven-day transition schedule, the 10% treat rule, body condition scoring, and multi-cat feeding.
* `learn-life-stages.html`: weaning through geriatric, the kitten-vs-adult requirement table, the post-neutering weight-gain window, pregnancy and lactation energy factors, and why senior cats need more protein rather than less.
* `learn-toxic.html`: toxic foods, plants (lilies flagged as a same-hour emergency), medications, and household hazards, with poison-line numbers and first-ten-minutes steps at the top of the page.
* `learn-health.html`: diet in obesity, CKD, FLUTD, diabetes, hyperthyroidism, IBD, food allergy, hepatic lipidosis, dental disease and constipation.
* `assets/cfc.css`: design tokens plus the three-column documentation shell (top bar, sidebar, article, on-this-page rail), callouts, data tables, entry cards, panels, comparison grids, pagination and site footer. Responsive: the right rail drops below 1180px, the sidebar becomes a drawer below 900px.
* `assets/cfc-docs.js`: mobile navigation drawer (hamburger, backdrop, Escape to close) and the "on this page" scroll spy. Both are progressive enhancements; pages are fully readable without JavaScript.
* `assets/cfc-tailwind.js`: the Tailwind CDN theme, extracted from the inline per-page configs.
* `tools/learn/`: static generator (`build.py`, `shell.py`, `bits.py`, and one `c_*.py` content module per page) so the eleven pages share one shell and cannot drift apart. Generated HTML is committed, so deployment still needs no build step.
* Home page: a Cat Care Guide entry card above "Recently viewed".

Changed
* All pages: **Learn** link added to the header nav between Search and Methodology, linking to `./learn.html`.
* All pages: header nav now scrolls horizontally on narrow viewports instead of overflowing, now that it carries four items.
* `docs/ROADMAP.md`: milestones renumbered into chronological order; the Cat Care Guide recorded complete as M4; dark mode promoted out of the deferred list to M5, specified with a header toggle and a `localStorage`-persisted preference that falls back to `prefers-color-scheme`.
* `README.md`: documents the guide, the generator workflow, and the shared assets.

---

## [0.5.3] - 2026-06-07

**Removed Methodology from footers: now accessible via header nav.**

Changed
* All pages: removed the "· Methodology" link from the footer. Footer now contains only "Built by Azqato". Methodology remains reachable via the header nav on every page.

---

## [0.5.2] - 2026-06-07

**Added Search to header navigation.**

Changed
* All pages: **Search** link added to the nav between Home and Methodology, linking to `./search.html`. Search is highlighted (accent color, bold) when on `search.html`.

---

## [0.5.1] - 2026-06-07

**Added Home and Methodology links to the header navigation.**

Changed
* All pages (`index.html`, `search.html`, `product.html`, `methodology.html`): header now contains a `<nav>` element with three links (**Home**, **Search**, and **Methodology**) between the wordmark and the Support button.
* The link for the currently visited page is highlighted in accent color and bold via `aria-current="page"`, Home on `index.html`, Search on `search.html`, Methodology on `methodology.html`; none highlighted on `product.html`.

---

## [0.5.0] - 2026-06-07

**MVP completion: all documented sections built out.**

Added
* `methodology.html`: public scoring explanation page mirroring `PRD.md` §6, always reachable from the footer. Covers: why cats need a dedicated system, the three-pillar model and weights, Pillar A sub-factors (protein dominance, taurine, carb load, moisture, AAFCO adequacy), Pillar B additive risk tiers (Tier 1–3 with examples), Pillar C transparency factors, hard gates and caps, score bands with color swatches, a worked example, and data sources.
* All pages: "Methodology" link added to footer alongside "Built by Azqato".

Changed
* `product.html`: fully rewritten as a JS-driven page. All content is now rendered from embedded product data objects keyed by barcode, different barcodes produce different products. Changes include:
  * Three distinct products: Instinct Original Grain-Free with Real Chicken (0000000000000, 61, Good), Weruva Paw Lickin' Chicken (0000000000001, 81, Excellent), Friskies Surfin' & Turfin' Favorites (0000000000002, 28, Poor).
  * Band-appropriate glyphs per `DESIGN.md §5`: Excellent = circle-check, Good = check, Poor = exclamation-triangle, Bad = X-circle. Each rendered in the band color.
  * Warning banner (conditional): fires for products with Tier 3 additives (Friskies shows amber banner: "Tier 3 additives, score capped at 49").
  * Alternatives section (conditional): shown for Poor and Bad products; Friskies lists Weruva and Instinct as better options.
  * Additive flags grouped by tier descending (Tier 3 first, then Tier 2); Weruva shows a "No flagged additives detected" positive message.
  * Taurine "Not listed" state (red X glyph) for products that don't declare taurine (Friskies).
  * Not-found state: unknown barcodes show a friendly message and a link back to home.
  * Dynamic page title set from product name via `document.title`.
* `search.html`: updated result cards 2 and 3 to match the real product catalog, Weruva (81, Excellent, barcode 0000000000001) and Friskies (28, Poor, barcode 0000000000002). All cards now link to their correct product pages.

---

## [0.4.0] - 2026-06-07

**Rebuilt as plain HTML/CSS/JS: no build step, runs directly in any browser.**

Changed
* Replaced the Next.js build-required deliverable with three self-contained HTML pages that work by opening a file in a browser or being served on GitHub Pages with no compilation step.
* `.github/workflows/deploy.yml`: removed all build steps (`npm ci`, `npm run build`). The workflow now uploads the repo root directly as the Pages artifact. No Node.js required.

Added
* `index.html`: home page, wordmark, disabled Scan button with tooltip, search form (GET to `search.html`), two hardcoded recently-viewed product cards. Tailwind CDN + custom CSS + Google Fonts (Fraunces, Public Sans). Zero JavaScript dependencies beyond the Tailwind CDN.
* `search.html`: search results, search bar pre-filled from `?q=` URL param (vanilla JS `URLSearchParams`), three hardcoded mock result cards linking to `product.html`. No server needed.
* `product.html`: full product page, score header (61, Good band, green bar), verdict + reason chips, 24-item ingredient list, two Tier 2 additive cards (Carrageenan, Guar Gum) with cited sources, 2×2 nutrition grid, AAFCO statement, footer metadata. Barcode shown from `?barcode=` param.
* `favicon.svg`: 😻 emoji SVG at repo root (GitHub Pages serves this correctly).
* `.nojekyll`: at repo root, prevents GitHub Pages from running Jekyll on the repo.

Architecture note
* The `app/`, `components/`, `next.config.ts`, `package.json`, etc. remain in the repo as the future Next.js migration path. They do not affect GitHub Pages serving. When transitioning to the full product, scaffold the Next.js build, add build steps back to the workflow, and retire the HTML pages.

---

## [0.3.0] - 2026-06-07

**MVP complete: GitHub Pages deployment config.**

Added
* `next.config.ts`: set `basePath` and `assetPrefix` to `/Cat-Food-Center` for deployment at `https://azqato.github.io/Cat-Food-Center/`. Both values are derived from a single `REPO` constant at the top of the file, change it there if the repo name changes.

Confirmed present (from earlier prompts)
* `public/.nojekyll`: prevents GitHub Pages from running Jekyll on the `out/` directory.
* `.gitignore`: `out/` excluded from version control; the built output is deployed separately.

Deployment steps (run after `npm install` with Node.js LTS installed)
1. `npm run build` → produces `out/`
2. Push `out/` contents to the `gh-pages` branch of `https://github.com/Azqato/Cat-Food-Center.git`, or configure a GitHub Actions workflow to do so on push to `main`.
3. In repo Settings → Pages, set source to the `gh-pages` branch, root (`/`).

Build verification
* Node.js was not present on the development machine during this session; `npm run build` could not be confirmed. Run it manually after installing Node.js LTS from nodejs.org. Expected output: a clean `out/` directory with `index.html`, `search/`, `product/0000000000000/`, `product/0000000000001/`, `product/0000000000002/`, and all static assets.

---

**MVP summary (prompts 1–4, versions 0.2.0–0.3.0)**

| What | Where |
| --- | --- |
| Next.js 14 scaffold, TypeScript strict, Tailwind CSS | `package.json`, `tsconfig.json`, `tailwind.config.ts` |
| Design tokens (colors, type scale, radius, max-width) | `tailwind.config.ts`, `app/globals.css` |
| Fraunces + Public Sans via `next/font/google` | `app/layout.tsx` |
| Global header (wordmark + Support button) | `components/Header.tsx` |
| Global footer ("Built by Azqato") | `components/Footer.tsx` |
| 😻 emoji favicon | `public/favicon.svg`, `app/layout.tsx` |
| Home page (scan button, search form, recently-viewed cards) | `app/page.tsx` |
| Mock product page (full visual per `DESIGN.md` §7.3) | `app/product/[barcode]/page.tsx` |
| Search page (pre-filled input, 3 mock result cards) | `app/search/page.tsx`, `app/search/SearchView.tsx` |
| Static export + GitHub Pages config | `next.config.ts` (`basePath`, `assetPrefix`) |
| `.nojekyll`, `out/` gitignore | `public/.nojekyll`, `.gitignore` |

---

## [0.2.2] - 2026-06-07

**Prompt 3: Mock product page, search page, emoji favicon.**

Added
* `app/product/[barcode]/page.tsx`: full product page layout per `DESIGN.md` section 7.3, populated with hardcoded mock data (Instinct Original Grain-Free with Real Chicken, score 61, Good band). Sections rendered:
  * Score header: 6px band-good color bar, 3rem score number, check glyph + band label, product image placeholder, product name (h1), brand / format / life-stage meta.
  * Verdict: one-sentence summary and three reason chips as pills.
  * Ingredients: numbered ordered list of 24 ingredients with a chevron hint; expand logic deferred (TODO comment).
  * Additive flags: Tier 2 Moderate Risk section with two cards (Carrageenan, Guar Gum), each showing function badge, health impact, and a cited source link.
  * Nutrition snapshot, 2×2 grid: Crude Protein 52% DM, Crude Fat 28% DM, Moisture 78% as-fed, Taurine Present (with check glyph). Tabular figures throughout.
  * AAFCO adequacy: quoted statement + substantiation method.
  * Footer metadata: data-completeness indicator and last-reviewed date.
* `app/search/SearchView.tsx` (`'use client'`): search input pre-filled from `?q=` param; on submit navigates to `/search?q=`; displays three hardcoded result cards (Instinct Chicken / Salmon / Duck variants, all score ~60, Good band) each linking to `/product/0000000000000`.
* `app/search/page.tsx`: rewritten as a server component that wraps `SearchView` in `<Suspense>` (required by Next.js static export when `useSearchParams` is used).
* `public/favicon.svg`: 😻 emoji as an SVG favicon.
* `app/layout.tsx`: wired `favicon.svg` via `metadata.icons`.

---

## [0.2.1] - 2026-06-07

**Prompt 2: Home page.**

Added
* `app/page.tsx`: full home page layout per `DESIGN.md` section 7.1.
  * Wordmark (`<h1>`) in Fraunces display serif with tagline.
  * 128px circular Scan button in accent color: disabled state with opacity, `cursor-not-allowed`, and a CSS tooltip ("Coming soon") on hover. Accessible via `aria-disabled` and `aria-describedby`.
  * Search form (`role="search"`): text input + Submit button; on submit, navigates to `/search?q=<query>` via `useRouter`.
  * "Recently viewed" section with two hardcoded mock product cards: Weruva Paw Lickin' Chicken (score 81, Excellent) and Friskies Surfin' & Turfin' Favorites (score 28, Poor). Each card shows the score badge in band color, product name, brand, band pill, and a chevron.
* `app/product/[barcode]/page.tsx`: added mock barcodes `0000000000001` and `0000000000002` to `generateStaticParams` so the static export generates pages the recently-viewed links point to.

---

## [0.2.0] - 2026-06-07

**Prompt 1: Project scaffold, design tokens, global layout.**

Added
* `package.json`: Next.js 14, React 18, Tailwind CSS 3, TypeScript 5.
* `tsconfig.json`: strict mode, App Router moduleResolution.
* `next.config.ts`: `output: 'export'`, `trailingSlash`, `images.unoptimized`, static GitHub Pages build. `basePath`/`assetPrefix` left as TODO for Prompt 4.
* `tailwind.config.ts`: all design tokens from `DESIGN.md` wired as Tailwind theme extensions, colors (`bg`, `surface`, `ink`, `ink-soft`, `accent`, `hairline`, four band colors), font families (`font-display` → Fraunces, `font-body` → Public Sans), type scale (`text-display` through `text-micro`), border radius (`rounded-card`, `rounded-pill`), max-width (`max-w-content`).
* `postcss.config.mjs`: Tailwind + autoprefixer.
* `.eslintrc.json`: `next/core-web-vitals`.
* `.gitignore`: ignores `out/`, `.next/`, `node_modules/`, `next-env.d.ts`.
* `app/globals.css`: Tailwind directives plus `:root` CSS custom properties for all design tokens.
* `app/layout.tsx`: loads Fraunces (`--font-display`) and Public Sans (`--font-body`) via `next/font/google`; mounts `<Header>` and `<Footer>` around a flex-column `<body>`.
* `components/Header.tsx`: sticky header, wordmark in display serif linking to `/`, Support pill button linking to `https://azqato.github.io/support.html`.
* `components/Footer.tsx`: "Built by Azqato" centered footer with link to `https://azqato.github.io/index.html`.
* `app/page.tsx`, `app/search/page.tsx`, `app/product/[barcode]/page.tsx`: build-passing stubs; product route includes `generateStaticParams` required by static export.
* `public/.nojekyll`: prevents GitHub Pages Jekyll processing.

Next up
* Install Node.js (not present on dev machine), run `npm install`, verify `npm run build` produces a clean `out/`.
* Prompt 2: home page with scan button, search input, recently-viewed strip.
* Prompt 3: mock product page (full visual) and mock search results.
* Prompt 4: GitHub Pages `basePath`/`assetPrefix` config and final PATCHNOTES entry.

---

## [0.1.1] - 2026-06-07

**Documentation updates: global chrome and MVP strategy.**

Changed
* `DESIGN.md`: added section 7.0 defining a persistent header (wordmark + Support button linking to `https://azqato.github.io/support.html`) and footer ("Built by Azqato" linking to `https://azqato.github.io/index.html`) present on all screens.
* `PRD.md`: added section 4.1 capturing the header/footer as product requirements.
* `TRD.md`: added section 0 (MVP strategy), static Next.js export targeting GitHub Pages with hardcoded mock data first, real API wiring later. Updated section 8 global layout spec.
* `README.md`: updated status to reflect MVP-first approach.
* `PATCHNOTES.md`: this entry.

---

## [0.1.0] - 2026-06-07

**Project kickoff: foundational documentation.**

Added
* `README.md`: project overview, feature summary, tech stack, quick start.
* `PRD.md`: living spec, including the full CFC Score rating methodology (three pillars, additive risk tiers, hard gates, score bands, worked example).
* `TRD.md`: architecture, TypeScript data model, scoring-engine pipeline, data sources, testing strategy.
* `DESIGN.md`: editorial visual language, design tokens, typography, color and band system, screen specs, accessibility.
* `PATCHNOTES.md`: this changelog.

Decisions captured
* Cats are obligate carnivores, so the rating engine is purpose-built for feline nutrition and does not use human scoring systems such as Nutri-Score.
* Scoring weights set to Nutrition 55%, Additives 35%, Transparency 10%.
* High-risk (Tier 3) additives cap the score at 49; propylene glycol triggers an automatic Bad band because it is FDA-prohibited in cat food.
* Primary product data source is Open Pet Food Facts, supplemented by an internal additive knowledge base and an AAFCO feline nutrient reference.
* Stack: Next.js (App Router) plus TypeScript plus Tailwind CSS, delivered as a mobile-first installable PWA with browser support.

Next up
* Scaffold the Next.js PWA and Tailwind theme tokens from `DESIGN.md`.
* Build the deterministic scoring engine and its golden-file test suite.
* Seed the additive knowledge base (Tier 1 to Tier 3 entries with sources).
* Wire the barcode scanner (BarcodeDetector with ZXing fallback) and Open Pet Food Facts lookup.

---

---

# Appendix: the second history

What this file held before the merge, from 2026-06-07 to 2026-09-05, with no
change to its content. It is the shorter of the two histories and is
written in a more reader-facing voice, and it carries detail the spine does
not, notably the page-by-page contents of the Cat Care Guide. Its version
numbers are its own and do not line up with the spine above.

---

## v0.10.1 - 2026-09-05

### Fixed
- Documentation corrected against the code: the offline cache size, the number of end-to-end checks, the count of pages using Tailwind, and a testing instruction that referred to a runtime this project does not use.

### Added
- Two milestones written into the roadmap: a consolidation of the documentation set, and moving the whole site onto the interface built for the Cat Care Guide. Both are planned rather than started.

### Notes
- Nothing about the site itself changed in this release.

---

## v0.10.0 - 2026-09-05

### Added
- **Compare two foods side by side.** Figures are converted to a dry-matter basis, so a wet food and a dry food can be read on the same scale rather than the wetter one looking worse for containing water. The comparison is in the URL, so it can be shared.

### Notes
- The page compares pillar by pillar and never declares an overall winner. Two scores built from different amounts of data are not the same claim, and the page says so rather than letting the bigger number settle it.

---

## v0.9.0 - 2026-09-05

### Added
- **A page for products that are not in the database.** It checks the barcode for a typo and re-queries first (a mistyped digit looks exactly like a missing product) then explains which two panels to photograph and links the contribution straight to Open Pet Food Facts with the barcode filled in.

### Notes
- Contributions go to the open database the scores are derived from, not to a queue of ours. That way a product added once works here, in every other tool built on the same data, and for the next person who scans the same tin.

---

## v0.8.0 - 2026-09-05

### Added
- **Works offline.** A product you have already opened stays readable with no connection, and the app installs to a home screen. Pages you have never opened show a page explaining what still works, rather than the browser's error screen.
- An offline banner, and a notice on any product page that is being shown from a saved copy; including when it was saved.

### Notes
- A cached score is always labelled as one. The scoring engine and the database both change, so an old score shown as current would be wrong in exactly the way this project exists to avoid.

---

## v0.7.0 - 2026-09-05

### Added
- **Barcode scanning.** Point the camera at the packaging and the product page opens. Decoding happens on the device; only the barcode number is sent anywhere. Uses the platform's `BarcodeDetector` where available and downloads ZXing only where it is not.
- Manual barcode entry alongside the camera, always available and checksum-validated before it navigates.
- **Recently viewed**, kept on the device in `localStorage`. No account, no sync, and a Clear button.
- A `Scan` entry in the top navigation.

### Changed
- The home page Scan button now works. It was disabled with a "Coming soon" tooltip.

### Removed
- The two invented "Recently viewed" products. The section stays hidden until there is something real in it.

---

## v0.6.0 - 2026-09-05

### Added
- **Live product scoring.** `assets/js/opff.js` fetches and normalises Open Pet Food Facts records; `assets/js/scoring.js` derives the CFC Score from them. Both run in the browser, with no build step and no server.
- `assets/data/additives.json`, the additive knowledge base: 20 entries across three risk tiers, plus three catch-all label terms, each with sources.
- Real `product.html` and `search.html`, replacing the mock markup.
- A 130-assertion test suite (`tests.html`), run headlessly by `tools/run-tests.py`.
- `docs/DATA-COVERAGE.md`: a measured survey of what the database actually holds.
- A "What the score cannot see" section on the methodology page.

### Fixed
- **Non-English labels were scored as clean.** The alias matcher was English-only, and only 9.5% of records carry English ingredients, so on most labels it matched nothing, and reported that silence as an absence of problems. A French product with unnamed meat by-products and added sugar scored 77 / Excellent. Aliases now cover six languages, and a label outside that set is explicitly reported as unchecked rather than clean, with confidence capped. See `docs/DATA-COVERAGE.md`.
- The Tier 0 "named by-products" credit was awarded to *unnamed* by-products, contradicting the transparency pillar on the same words.
- A parenthetical naming 4% beef could make an unnamed meat entry score as a named animal protein.

---

## v0.5.0 - 2026-09-05

### Added
- **Dark mode with a persisted preference.** A three-state control (system, light, dark) in the top bar of every page. The choice is stored under the `localStorage` key `cfc-theme`; `system` stores nothing and defers to `prefers-color-scheme`. Open tabs stay in step via a `storage` listener.
- `assets/cfc-tokens.css`: the palette extracted from `cfc.css` so that both page families share it: the Tailwind CDN pages and the generated guide pages.
- `assets/cfc-theme.js`: theme application and persistence. Loaded synchronously in `<head>` so the stored theme applies before first paint.
- `tools/check-contrast.py`: WCAG AA audit of every foreground/background pair in both palettes.
- `docs/ADR-001-static-first.md`: the decision that the site is static HTML by design, what that enables (the barcode scanner needs no server), and what it forecloses.

### Changed
- Tailwind colour names map to CSS variables rather than hex literals, so utility classes follow the theme without `dark:` variants. Opacity modifiers cannot be used on those colours as a result.
- The green and amber score chips now use dark ink instead of white. They failed AA at 2.8:1 and 2.3:1 in the light theme; this is an accessibility fix, and it changes how the light theme looks.
- `README.md`, `TRD.md`, `RUNBOOK.md` and `DESIGN.md` now describe the static stack that actually ships rather than the Next.js application that did not.

### Removed
- The unused Next.js 14 application and its toolchain. It was never built or deployed; `deploy.yml` has always served the repository root directly.

### Verified
- All 38 token pairs pass WCAG AA in both palettes.
- Chromium check across all fifteen pages: the theme applies, the toggle cycles, the choice survives a reload with no flash, and no console errors.

---

## v0.4.0 - 2026-09-05

### Added
- **The Cat Care Guide**: an eleven-page educational resource at `/learn.html` and `/learn-*.html`, grounded in the AAFCO nutrient profiles, NRC research, FDA and EFSA guidance, WSAVA's nutrition toolkit, and the peer-reviewed veterinary literature. Every page carries a sources list.
  - `learn.html`: overview, the five rules, and the guide map
  - `learn-nutrition.html`: obligate carnivore metabolism; protein, fat, carbohydrate and fibre; the eight nutrients cats cannot synthesise
  - `learn-daily-requirements.html`: the complete AAFCO cat food nutrient profile (all 42 nutrients with growth minimums, adult minimums and maximums), the RER/MER calorie formulas, and a worked conversion into exact grams and milligrams per day for a 4.5 kg cat
  - `learn-labels.html`: AAFCO adequacy statements, the dry-matter conversion, carbohydrate by difference, ingredient splitting, the 95/25/3 naming rules, and the marketing terms with no regulatory meaning
  - `learn-food-types.html`: seven formats compared, including the current FDA position on H5N1 in raw pet food
  - `learn-hydration.html`: water requirements by body weight, dehydration checks, and eleven ways to increase intake
  - `learn-additives.html`: a three-tier additive reference covering 30+ compounds with the regulatory position and evidence for each, plus the commonly criticised ingredients that are not actually a problem
  - `learn-feeding.html`: calorie tables by body weight, portioning, meal timing, transitions, treats, weight management, and multi-cat feeding
  - `learn-life-stages.html`: weaning through geriatric, including the post-neutering weight gain window and why senior cats need more protein, not less
  - `learn-toxic.html`: toxic foods, plants (lilies flagged as a same-hour emergency), medications and household hazards, with poison-line numbers and first-ten-minutes steps
  - `learn-health.html`: diet in obesity, CKD, FLUTD, diabetes, hyperthyroidism, IBD, food allergy, hepatic lipidosis, dental disease and constipation
- Documentation-site layout for the guide: fixed top bar with product search, grouped sticky sidebar, article column, "on this page" scroll-spy rail, prev/next pagination, and a four-column site footer
- Shared front-end assets in `/assets`: `cfc.css` (design tokens and the documentation shell), `cfc-docs.js` (mobile navigation drawer and scroll spy), `cfc-tailwind.js` (Tailwind CDN theme extracted from the inline page configs)
- `tools/learn/` static generator so the eleven pages share one shell and cannot drift apart; generated output is committed, so deployment still needs no build step
- "Learn" entry in the main navigation on the home, search, product and methodology pages
- Cat Care Guide entry card on the home page

### Changed
- Main navigation now scrolls horizontally on narrow viewports rather than overflowing, since it carries a fourth item
- `docs/ROADMAP.md` renumbered into true chronological order; the Cat Care Guide recorded as complete, and dark mode promoted out of the deferred list into a planned milestone (M5) with a toggle and a `localStorage`-persisted preference
- README documents the guide, the generator workflow, and the shared assets

### Notes
- The guide is educational content and is not veterinary advice; every page says so, and the pages covering disease and toxicity say so prominently.

---

## v0.3.0 - 2026-06-08

### Added
- Full documentation suite: PRD, TRD, DESIGN, PATCHNOTES, PRFAQ, TENETS, METRICS, ROADMAP, SECURITY, RUNBOOK
- `/docs` directory consolidating all project documentation
- README.md rewritten for developer audience with install, dev, build, and deploy instructions

### Changed
- PRD.md, TRD.md, DESIGN.md moved from project root into `/docs`
- TRD.md updated to reflect actual current implementation state (mock data, deferred features catalogued in known technical debt table)
- DESIGN.md updated with precise Tailwind token references, accessibility ARIA patterns, and component implementation details

---

## v0.2.0 - 2026-06-07

### Added
- Next.js 14 App Router with TypeScript and static export configured for GitHub Pages (`basePath: /Cat-Food-Center`)
- Tailwind CSS with full design token theme: colors (`bg`, `surface`, `ink`, `ink-soft`, `accent`, `hairline`, four band colors), typography scale (`display`, `h1`, `h2`, `body`, `small`, `micro`), border radius (`card`, `pill`), max-width (`content`)
- Fraunces (display serif) and Public Sans (body sans) loaded via `next/font/google`
- Global layout (`app/layout.tsx`): sticky header with wordmark and Support pill button linking to `https://azqato.github.io/support.html`; footer with Azqato link
- Home page (`app/page.tsx`): wordmark, tagline, disabled Scan button with "coming soon" tooltip, search form routing to `/search`, recently viewed section with two mock product cards and score badges
- Search page (`app/search/`): search bar pre-filled from `?q=` param, mock result list of three products with score badges and band labels
- Product detail page (`app/product/[barcode]/page.tsx`): score header with band color bar and checkmark glyph, verdict section with reason chips, numbered ingredient list, additive flags section with tier dot and cited source links, 2×2 nutrition snapshot grid (dry-matter basis), AAFCO adequacy quote, footer metadata row with data completeness and last reviewed date
- GitHub Actions workflow (`.github/workflows/deploy.yml`): builds with `npm ci && npm run build` and deploys `out/` to GitHub Pages on every push to `main`
- `public/.nojekyll` to prevent GitHub Pages from ignoring underscore-prefixed directories

### Changed
- Replaced earlier plain HTML/CSS/JS implementation with Next.js App Router static export

---

## v0.1.0 - 2026-06-07

### Added
- Initial Next.js App Router scaffold with TypeScript, Tailwind CSS, ESLint, and PostCSS
- `next.config.ts` with `output: 'export'`, `trailingSlash: true`, `basePath`, and `assetPrefix` for GitHub Pages
- `PRD.md`, `TRD.md`, `DESIGN.md` specification documents
- `.gitattributes` and `.gitignore`
