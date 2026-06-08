# PR/FAQ

---

## Press Release

**FOR IMMEDIATE RELEASE**

### Cat Food Center Gives Pet Owners the Honest Ingredient Breakdown They've Always Wanted

*New app scores every cat food product on a transparent 0–100 scale — so owners know exactly what they're feeding their cats*

**[City, Date]** — Cat Food Center today launched a free web app that takes the guesswork out of buying cat food. Point your phone at a barcode in the store aisle, and in seconds you'll see a plain-English breakdown of every ingredient, a flag for any additives linked to health concerns, and a single CFC Score from 0 to 100 that tells you whether the food is Excellent, Good, Poor, or Bad for your cat.

Unlike star ratings written by other pet owners, the CFC Score is built on science. Cat Food Center's rating engine is purpose-built for cats — obligate carnivores with specific nutritional needs that standard food labels were never designed to address. The scoring system weighs three things: whether the food actually delivers the protein cats need, whether it contains additives with documented health concerns, and whether the ingredient list is honest and traceable.

"I was standing in the pet food aisle and had no idea if the food I was buying was actually good," said Sarah M., a cat owner who tested an early version. "Now I can scan it and know in ten seconds."

Cat Food Center is free, works in any modern browser, and requires no account or app download. The methodology is public and fully documented.

---

## Internal FAQ

**1. What problem are we actually solving?**
Cat food marketing is loud and largely misleading. "Grain-free," "natural," and "premium" are marketing terms with no regulatory definition. Meanwhile, the ingredients that genuinely matter for feline health — named animal protein as the first ingredient, taurine sufficiency, absence of prohibited additives like propylene glycol — are buried in fine print most owners can't evaluate. We make that evaluation instant and accessible.

**2. Why build this for cats specifically instead of all pets?**
Cats have unique nutritional constraints that dogs do not share. Cats cannot synthesize taurine, arginine, or arachidonic acid from plant precursors. A scoring system that works for dog food or human food will produce wrong answers for cat food. Starting with cats lets us build a genuinely accurate, defensible engine rather than a generic one. Dogs are a future vertical.

**3. What is the core technical risk?**
Catalog completeness. Open Pet Food Facts coverage of cat food SKUs is inconsistent — many products have no ingredients or nutrition data. The app must degrade gracefully and never fabricate values. The "partial data" indicator and the not-found/submit flow are critical to trust.

**4. How do we stay unbiased if the product grows?**
The scoring algorithm is public and documented. No advertiser can change a score. Any future sponsorship or partnership is visually separated and explicitly excluded from affecting ratings. This is a hard product tenet, not a policy preference.

**5. What does success look like at six months?**
Users completing a scan-to-result flow successfully in under 30 seconds for catalogued products, with a scan success rate above 90%. Secondary signal: repeat visits before a purchase. If owners come back before buying, the tool is working.

**6. What assumptions must be true for this to work?**
- Open Pet Food Facts has usable data for the top-selling cat food SKUs.
- The BarcodeDetector API is supported on enough mobile browsers to make scanning viable (ZXing covers the fallback).
- Cat owners make informed purchasing decisions when given clear information. (If they don't, no rating app helps.)

**7. What is explicitly out of scope for v1?**
E-commerce, affiliate links, personalized diet plans, user-generated reviews, dog food, and any backend that requires us to manage a server. The goal is a trusted information tool, not a marketplace.

**8. How do we handle regulatory or scientific disputes?**
Every additive flag cites a published source (FDA, EFSA, WHO/IARC, peer-reviewed study). If new evidence emerges that contradicts a rating, we update the knowledge base and log the change in PATCHNOTES.md. We do not claim certainty where there is legitimate scientific debate — we reflect the current consensus and cite it.

**9. What happens when a product is missing from the catalog?**
The not-found flow prompts the user to submit the barcode and a photo of the ingredient label. This feeds a review queue for editorial processing. The goal is to crowd-source catalog completeness without crowd-sourcing the scoring itself.

**10. How does the project make money?**
It doesn't, currently. The v1 goal is product-market fit and catalog coverage. Revenue options (subscription for advanced features, B2B data licensing, non-affiliate brand partnerships) are deferred until the product has meaningful usage.

---

## External FAQ

**1. What is Cat Food Center?**
A free website and installable app that analyzes cat food products and gives each one a score from 0 to 100. Scan the barcode at the store or search by brand name at home. You get an instant breakdown of the ingredients, any additives that might be harmful to cats, the nutrition picture, and an overall verdict.

**2. How does the scoring work?**
The CFC Score combines three things: how good the nutrition is for cats (55% of the score), whether the food contains concerning additives (35%), and how transparent and traceable the ingredients are (10%). Cats are obligate carnivores, so the scoring is built around their specific needs — not a generic pet food scale.

**3. Is it free?**
Yes, entirely. No account needed, no app download required, no ads.

**4. How accurate is the data?**
Product data comes from Open Pet Food Facts, an open database of food products. Coverage varies by brand. When data is incomplete, the app clearly flags it and adjusts the score's confidence accordingly — it never makes up values.

**5. Does Cat Food Center have deals with any pet food brands?**
No. No brand pays to appear, and no brand pays to improve or hide a score. The methodology is fully public and documented.

**6. Can I use it on my phone in a store?**
Yes. The site is designed mobile-first. The barcode scanner uses your phone's camera. If your browser doesn't support camera scanning, the search bar works just as well.

**7. My cat has kidney disease / diabetes / a urinary condition — can I rely on this for medical decisions?**
No. Cat Food Center is an informational tool, not veterinary advice. The ratings help you compare products and spot red flags. For cats with medical conditions, always defer to your veterinarian. The scores are based on population-level nutritional science, not individual health needs.

**8. A product I'm looking for isn't in the app. What do I do?**
Use the submit flow to send us the barcode and a photo of the ingredient label. We'll add it to the review queue.

**9. What data does Cat Food Center collect about me?**
None. There's no account, no login, and no tracking. The barcode scanner runs entirely on your device — your camera feed is never uploaded.

**10. Why cats only? What about dogs?**
Cats and dogs have very different nutritional requirements. Building one scoring engine that's accurate for both is harder than building one that's right for each. We're starting with cats, where the science of obligate carnivore nutrition gives us a strong, defensible foundation. Dogs are planned for a future phase.
