# -*- coding: utf-8 -*-
from shell import build
from bits import callout, table, h2, panel, entry

def E(name, tier, meta, body):
    chips = {
        3: ("bad", "Tier 3 · High risk"),
        2: ("poor", "Tier 2 · Moderate"),
        1: ("good", "Tier 1 · Low"),
        0: ("excellent", "No concern"),
    }[tier]
    return entry(name, [chips], body, meta=meta)


BODY = "\n\n".join([

h2("tiers", "1. How we tier additives"),
"""<p>“Additive” covers a lot of ground: preservatives, colours, thickeners, humectants, palatants,
and processing aids. Some are unambiguously useful, some are unambiguously best avoided, and a
sizeable middle group is genuinely contested. Lumping them together as “chemicals” is not useful,
so this page sorts them into three tiers by the strength of the evidence for harm and the severity
of the outcome.</p>""",

table(
    "The tiers used throughout this page and in the CFC Score.",
    ["Tier", "Meaning", "What we do with it"],
    [
        ["<span class=\"chip chip-bad\">Tier 3: High risk</span>",
         "Documented harm in cats, a regulatory prohibition, or a credible carcinogenicity or organ-toxicity signal with no species-specific safe dose established.",
         "Avoid. In the CFC Score these cap the product's total."],
        ["<span class=\"chip chip-poor\">Tier 2: Moderate</span>",
         "Plausible mechanism and some supporting evidence, but the picture is incomplete or the effect is limited to susceptible individuals.",
         "Prefer products without them, especially for a cat with existing gut, kidney, or skin problems."],
        ["<span class=\"chip chip-good\">Tier 1: Low</span>",
         "No meaningful safety signal. Usually flagged by marketing rather than by evidence, or a quality-of-formulation issue rather than a safety one.",
         "Not a reason to reject a food."],
    ]),

callout("note", """<p>Absence of evidence is doing real work in several entries below. A recurring
theme in the regulatory literature is that many pet food additives were assessed without
<em>species-specific</em> feline data: the EFSA opinion on BHA, for instance, concluded that for cats
a safe dose could not be established from the available tolerance data. That is not the same as
evidence of harm, but for an animal with a liver as idiosyncratic as a cat's it is not reassuring
either.</p>"""),

h2("tier3", "2. Tier 3 - avoid these"),

E("Propylene glycol", 3,
  "Humectant · <strong>Prohibited in cat food by the US FDA</strong> · 21 CFR 589.1001",
  """<p>Used to keep semi-moist foods soft and chewy. In controlled studies it caused Heinz body
  formation and shortened red blood cell survival in cats (a haemolytic anaemia) at doses that did
  not affect other species. The FDA specifically prohibited it in cat food as a result; it remains
  legal in dog food.</p>
  <dl>
    <dt>Why cats specifically</dt>
    <dd>Feline haemoglobin has eight reactive sulfhydryl groups against two to four in most mammals,
    making cat red cells unusually vulnerable to oxidative damage. This same quirk underlies the
    onion, garlic, and paracetamol toxicities.</dd>
    <dt>Where you might still meet it</dt>
    <dd>Dog treats shared with a cat, and some imported or poorly regulated products. Read treat labels,
    not just food labels.</dd>
  </dl>"""),

E("Ethoxyquin", 3,
  "Synthetic antioxidant preservative · Originally registered as a pesticide · Banned in the EU and Australia for pet food",
  """<p>Very effective at preventing fat oxidation, which is why it persists. It is approved by the
  FDA for pet food at up to 75&nbsp;ppm, but the EU withdrew its authorisation and Australia has
  restricted it. The published toxicology is genuinely inconclusive: concerns centre on liver enzyme
  changes and haemoglobin effects, and the EU withdrawal cited insufficient data to complete the safety
  assessment rather than a demonstrated harm.</p>
  <dl>
    <dt>The labelling trap</dt>
    <dd>Ethoxyquin is often added to fish meal at the supplier stage, as a legally required stabiliser
    for shipping. Because the pet food manufacturer did not add it, it may not appear on the ingredient
    list at all. A food containing fish meal may contain ethoxyquin without saying so.</dd>
    <dt>What to do</dt>
    <dd>If it matters to you, ask the manufacturer directly whether their fish meal is ethoxyquin-free.
    Brands that use naturally preserved fish meal generally say so.</dd>
  </dl>"""),

E("BHA: butylated hydroxyanisole", 3,
  "Synthetic antioxidant · IARC Group 2B, possibly carcinogenic to humans · No safe feline dose established by EFSA",
  """<p>BHA produced forestomach tumours in rats and hamsters at high doses, which is the basis for the
  IARC Group 2B classification and for California's Proposition 65 listing. Regulators generally hold
  that at permitted levels it presents no concern for consumer safety, but the EFSA opinion on BHA as
  a feed additive concluded that <em>for cats a safe dose could not be established from the tolerance
  data available</em>. Additional concerns raised in the literature include endocrine disruption and
  liver and kidney effects.</p>
  <p>The practical point is that BHA is entirely avoidable. Mixed tocopherols and rosemary extract do
  the same job; they simply give a shorter shelf life, which is a cost to the manufacturer rather than
  to your cat.</p>"""),

E("BHT: butylated hydroxytoluene", 3,
  "Synthetic antioxidant · Frequently used alongside BHA",
  """<p>Shares BHA's profile: effective, cheap, long-standing consumer-advocacy concern over
  carcinogenicity, endocrine disruption, and liver injury, and the same gap in species-specific feline
  tolerance data. Assessed as safe at permitted levels by regulators, avoidable in practice.</p>"""),

E("Artificial colours: Red 40, Yellow 5, Yellow 6, Blue 2", 3,
  "Azo and triarylmethane dyes · Zero nutritional function",
  """<p>Cats have dichromatic vision and choose food by smell and texture. Colour exists solely so the
  product looks like meat chunks or “varied kibble” to the person paying. That matters because it means
  the risk-benefit calculation has a zero on the benefit side: any level of uncertainty is uncompensated.</p>
  <p>The specific signals are modest but real, Red 40 and Yellow 5 carry contamination limits for
  benzidine and other aromatic amines; Yellow 5 (tartrazine) is associated with hypersensitivity
  reactions in a small subset of people; Blue 2 has been associated with tumour findings in some rodent
  studies. None of this is established in cats. But there is no reason to accept it.</p>"""),

E("Titanium dioxide", 3,
  "Whitening pigment · <strong>Banned as a food additive in the EU since 2022</strong>",
  """<p>EFSA concluded in 2021 that titanium dioxide could no longer be considered safe as a food
  additive, because genotoxicity could not be ruled out for the nanoparticle fraction. The EU ban
  followed. It is still permitted in US pet food, where it appears in white or pale “gravy” and
  “cream” products for visual effect only.</p>"""),

E("Menadione: vitamin K3, “menadione sodium bisulfite complex”", 3,
  "Synthetic vitamin K precursor · Banned from human supplements in the US",
  """<p>The FDA prohibits menadione in human over-the-counter supplements because high parenteral doses
  caused haemolysis, hyperbilirubinaemia, and liver toxicity. It remains permitted in animal feed and
  turns up in pet food as a cheap vitamin&nbsp;K source. Cats rarely need supplemental vitamin&nbsp;K at
  all: AAFCO only requires it when the diet is more than 25&nbsp;% fish, because gut bacteria supply
  the rest. Natural phylloquinone (K1) is available and is what better formulations use.</p>"""),

E("Sodium nitrite as a colour fixative", 3,
  "Curing salt · Distinct from its legitimate use as an antibotulinal in some products",
  """<p>Used in some semi-moist and treat products to keep a red, meaty appearance. Two concerns: at high
  intake it can cause methaemoglobinaemia, and under heat it can form nitrosamines with secondary amines
  in meat. Cats' oxidatively fragile haemoglobin makes the first concern more relevant than it would be
  in other species. Where a food needs no colour fixative, it should not have one.</p>"""),

h2("tier2", "3. Tier 2 - prefer to avoid, particularly in sensitive cats"),

E("Carrageenan", 2,
  "Seaweed-derived thickener and stabiliser · Genuinely contested",
  """<p>The most argued-about ingredient in wet cat food, and the one where it is most important to be
  precise. Two forms exist. <strong>Degraded carrageenan (poligeenan)</strong> is a recognised intestinal
  inflammatory agent used deliberately to induce colitis in laboratory animal models, but it is not a
  permitted food ingredient. <strong>Undegraded, food-grade carrageenan</strong> is what is actually in
  pet food, and its safety is contested rather than settled: JECFA and EFSA have repeatedly concluded it
  is acceptable at food-use levels, while some researchers argue that partial degradation occurs in the
  acidic stomach and during processing, and that low-grade intestinal inflammation results.</p>
  <dl>
    <dt>Honest summary</dt>
    <dd>There is no good evidence of harm to cats at the levels used. There is also no nutritional
    benefit: it is a texture ingredient. Given cats eat the same formulation every day for a decade or
    more, and given that guar gum, xanthan gum, cassia, and locust bean gum do the same job, avoiding it
    is a low-cost precaution rather than a scientific necessity.</dd>
    <dt>When it matters more</dt>
    <dd>Cats with inflammatory bowel disease, chronic diarrhoea, or food-responsive enteropathy. In that
    population it is worth eliminating as a trial.</dd>
  </dl>"""),

E("Guar gum, xanthan gum, cassia gum, locust bean gum", 2,
  "Thickeners and gelling agents · Generally well tolerated",
  """<p>The usual carrageenan substitutes. No meaningful safety signal, but they are fermentable and in
  quantity can loosen stools in sensitive cats. If a cat develops diarrhoea after switching to a gravy-
  or jelly-style product, the gum system is a reasonable suspect. Pâté formats usually use less.</p>"""),

E("MSG and hidden glutamates: “natural flavour”, “animal digest”, “hydrolysed protein”, “yeast extract”", 2,
  "Palatants · Extremely effective; poorly disclosed",
  """<p>Cats respond strongly to free amino acids, so hydrolysates and glutamate-rich extracts are
  powerful palatants. There is no established toxicity in cats at food levels. The problem is different:
  <strong>they work too well.</strong> A heavily palatant-coated food can drive overeating in a species
  that is already the most obesity-prone pet in the developed world, and it can make a cat unwilling to
  accept a plainer therapeutic diet later. “Animal digest” also does not name a species.</p>"""),

E("Added sugars: corn syrup, sucrose, molasses, caramel colour", 2,
  "Humectants, palatants, and colour · Nutritionally pointless in cats",
  """<p>Cats cannot taste sweetness (the sweet-receptor gene is a pseudogene) so sugar is not there
  for the cat's benefit. It softens semi-moist products, browns them appealingly, and adds empty
  calories to an animal predisposed to obesity and diabetes. There is no argument for it.</p>"""),

E("Propyl gallate and TBHQ", 2,
  "Synthetic antioxidants · Less studied than BHA and BHT",
  """<p>Alternative synthetic antioxidants that appear when a manufacturer avoids BHA and BHT but still
  wants a long shelf life. Both are permitted; both have thinner safety datasets than the compounds they
  replace, and neither has meaningful feline-specific data. Natural alternatives exist.</p>"""),

E("Inorganic phosphates: sodium tripolyphosphate, phosphoric acid, sodium hexametaphosphate", 2,
  "Emulsifiers, acidulants, and tartar-control agents · Relevant to kidney health",
  """<p>Not toxic, but they raise dietary phosphorus in its most rapidly absorbed form. High phosphorus
  intake (particularly from inorganic salts rather than from bone and meat) is associated with kidney
  injury in cats, and phosphorus restriction is the single best-evidenced dietary intervention in chronic
  kidney disease. For a healthy young cat this is a minor point; for a senior cat, or any cat with even
  early CKD, it is worth attention.</p>"""),

E("Garlic and onion powder", 2,
  "Flavouring · Should not be in cat food at all",
  """<p>Occasionally found in low-quality treats, table-food-styled products, and broths marketed as
  toppers. The organosulfur compounds in <em>Allium</em> species cause oxidative damage to feline red
  blood cells and Heinz body anaemia; cats are more sensitive than dogs. The amounts in a flavouring are
  usually small, but the effect is cumulative and there is no reason to accept any.
  <a href="{{root}}learn/toxic/">More on Allium toxicity &rarr;</a></p>"""),

h2("tier1", "4. Tier 1 - commonly criticised, not actually a problem"),
"""<p>A lot of ingredient-list anxiety is aimed at the wrong targets. These come up constantly in
“ingredients to avoid” listicles and mostly do not deserve it.</p>""",

E("Named by-products and by-product meals", 0,
  "“Chicken by-product meal”, “turkey by-products”",
  """<p>By-products are the non-skeletal-muscle parts of the animal: liver, heart, kidney, spleen, lung.
  These are not waste; they are the organs a wild cat eats first, and heart is the best natural taurine
  source available. AAFCO's definition specifically excludes hair, horn, teeth, and hooves. The
  legitimate criticism is about <em>unnamed</em> by-products, where you cannot verify the species or the
  batch-to-batch consistency, not about by-products as a category.</p>"""),

E("Named meals", 0, "“Chicken meal”, “salmon meal”, “lamb meal”",
  """<p>Rendered and water-removed, so protein-dense by weight. A named meal high in an ingredient list
  is a genuinely good sign; it reflects real contribution to the finished food rather than the
  pre-cooking water weight of fresh meat. Unnamed meals are the ones to question.</p>"""),

E("Mixed tocopherols, rosemary extract, ascorbic acid, citric acid", 0, "Natural preservatives",
  """<p>These are the alternatives to BHA, BHT, and ethoxyquin, and there is no safety concern with them.
  The trade-off is a shorter shelf life, which is why you should buy bag sizes you will finish within
  about six weeks. The occasional claim that rosemary extract triggers seizures in epileptic pets is not
  supported by evidence.</p>"""),

E("Supplemental taurine", 0, "“Taurine” in the ingredient list",
  """<p>Should be there. Processing and storage degrade taurine, canned diets lose more of it, and
  deficiency causes irreversible blindness and heart failure. Seeing supplemental taurine on a label is
  a mark of a formulation that understands cats: not a sign that the food is deficient in real meat.</p>"""),

E("Beet pulp, cellulose, psyllium, inulin", 0, "Fibre sources",
  """<p>Beet pulp in particular is often attacked as “filler”. It is a moderately fermentable fibre that
  supports stool quality and colonic health, and it contains negligible sugar. Fibre is not an essential
  nutrient for cats but it is functionally useful for constipation, hairballs, and satiety in weight-loss
  diets.</p>"""),

E("Synthetic vitamins and chelated minerals", 0, "The long chemical-sounding tail of any ingredient list",
  """<p>“Thiamine mononitrate”, “pyridoxine hydrochloride”, “zinc proteinate”, “sodium selenite”, these
  are the vitamins and minerals from the AAFCO profile, in the forms that survive processing and are
  absorbed. Their presence is what makes a food complete. Chelated (“proteinated”, “amino acid complex”)
  minerals are generally better absorbed than inorganic sulfates and oxides.</p>"""),

h2("fillers", "5. Fillers and low-value bulk"),
"""<p>Not additives strictly speaking, but the same judgement applies: these are ingredients that occupy
calories a cat would use better elsewhere. None is dangerous. All are reasons to prefer a different
product when they sit high in the ingredient list.</p>""",

table(
    None,
    ["Ingredient", "What it is doing", "Concern"],
    [
        ["Corn, ground corn, whole grain corn", "Cheap energy and extrusion structure", "High starch load, low biological value for an obligate carnivore"],
        ["Corn gluten meal", "Inflates crude protein cheaply", "Amino acid profile poorly matched to feline needs; low in taurine"],
        ["Wheat, wheat gluten", "Binder and protein booster", "Same as corn gluten; also the vehicle in the 2007 melamine adulteration"],
        ["Soy, soybean meal, soy protein isolate", "Plant protein", "Low biological value in cats; contains phytoestrogens and trypsin inhibitors"],
        ["Pea protein, pea starch, pea fibre", "Grain-free protein and structure", "Frequently split across several list entries to appear lower; same carbohydrate load as grain"],
        ["Rice bran, brewers rice", "Milling by-products used as cheap bulk", "Low nutritional contribution; brewers rice is the broken fragments left after milling"],
        ["Powdered cellulose", "Non-fermentable bulk fibre", "Legitimate in weight-control and hairball diets; pure bulk anywhere else"],
    ]),

h2("shopping", "6. A practical shopping rule"),
callout("tip", """<p>You do not need to memorise thirty compounds. Three questions do most of the work:</p>
<ul>
  <li><strong>Is there a colour in it?</strong> If yes, put it back. Colour is for you, not the cat, and
  a manufacturer willing to add pointless dye has told you something about its priorities.</li>
  <li><strong>Which antioxidant preserves the fat?</strong> Mixed tocopherols and rosemary extract are
  good; BHA, BHT, and ethoxyquin are the ones to avoid.</li>
  <li><strong>What are the first five ingredients?</strong> You want named animal proteins, not plant
  protein concentrates or starch.</li>
</ul>"""),

"""<p>Everything past that is refinement. And it is worth keeping perspective: an under-fed, obese, or
chronically dehydrated cat on an additive-free food is in far worse shape than a well-fed, lean,
well-hydrated cat eating a food with guar gum in it. Additives matter, but they are not the biggest
lever you have.</p>""",

h2("sources", "Sources"),
"""<ul class="sources">
  <li>US FDA: 21 CFR 589.1001, prohibition of propylene glycol in cat food.</li>
  <li>EFSA FEEDAP Panel: <em>Safety and efficacy of butylated hydroxyanisole (BHA) for use in cats</em>. <a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8290245/" target="_blank" rel="noopener noreferrer">ncbi.nlm.nih.gov</a></li>
  <li>EFSA: 2021 opinion on titanium dioxide (E171) as a food additive, and the subsequent EU ban.</li>
  <li>Craig J.M., “Additives in pet food: are they safe?” <em>Journal of Small Animal Practice</em> (2021).</li>
  <li><em>Veterinary Practice News</em>, “Pet food additives: concerning, or no big deal?” <a href="https://www.veterinarypracticenews.com/pet-food-additives-evidence/" target="_blank" rel="noopener noreferrer">veterinarypracticenews.com</a></li>
  <li>IARC: Monograph classification of butylated hydroxyanisole (Group 2B).</li>
  <li>JECFA and EFSA evaluations of carrageenan (E407) as a food additive.</li>
  <li>Association of American Feed Control Officials, ingredient definitions, <em>Official Publication</em>.</li>
</ul>""",
])

build(
    slug="learn-additives",
    h1="Additives and ingredients to avoid",
    description="A tiered reference to preservatives, colours, thickeners, palatants and fillers in cat food, with the regulatory position and published evidence behind each one.",
    lede="Some additives are documented hazards to cats, some are contested, and a good many are attacked online without cause. This page sorts them into three tiers by the strength of the evidence, and says plainly where the evidence runs out.",
    body=BODY,
)
