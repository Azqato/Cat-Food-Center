# -*- coding: utf-8 -*-
from shell import build
from bits import callout, table, entry, h2, panel, compare

BODY = "\n\n".join([

h2("obligate", "1. What “obligate carnivore” actually means"),
"""<p>The phrase gets used loosely. Precisely, it means that over roughly ten million years of eating
nothing but other animals, the cat lineage lost metabolic machinery it no longer needed. Those losses
are permanent and they are the reason feline nutrition is not simply canine nutrition scaled down.</p>

<p>A dog is a facultative carnivore: it thrives on meat but retains the enzymes to make do with a
mixed diet. A cat did not keep those options. Five specific adaptations do most of the work:</p>""",

table(
    "The five metabolic adaptations that define feline nutrition.",
    ["Adaptation", "Consequence"],
    [
        ["<strong>No dietary need for carbohydrate</strong>",
         "Cats have no minimum carbohydrate requirement at all. They have low intestinal amylase, low disaccharidase activity, and lack hepatic glucokinase, relying instead on hexokinase. They handle a large starch load poorly and slowly."],
        ["<strong>Constitutively high protein turnover</strong>",
         "The hepatic transaminase and urea-cycle enzymes that break protein down for energy run at a high, largely fixed rate. A cat cannot dial them down when protein is scarce, so it keeps degrading body protein for glucose even while starving. This is why a low-protein diet costs a cat muscle much faster than it would a dog."],
        ["<strong>Loss of specific synthetic pathways</strong>",
         "No meaningful synthesis of taurine, arachidonic acid, or retinol from beta-carotene; too little delta-6-desaturase; too little vitamin D from skin; tryptophan-to-niacin conversion largely blocked. Each becomes an absolute dietary requirement."],
        ["<strong>Blunted thirst response</strong>",
         "Descended from the African wildcat, a desert animal that took its water from prey. A cat does not compensate fully for a dry diet by drinking more, so total water intake falls when the food is dry."],
        ["<strong>Sensory wiring for meat</strong>",
         "Cats cannot taste sweetness: the <em>Tas1r2</em> sweet-receptor gene is a non-functional pseudogene. They are instead strongly responsive to amino acids and to the nucleotides and free amino acids released by animal tissue, which is why palatants in commercial food are animal digest."],
    ]),

callout("note", """<p>None of this makes a cat unable to <em>digest</em> cooked starch. A well-processed,
gelatinised starch in a commercial diet is digested reasonably efficiently. The argument is not that
carbohydrate is poison; it is that carbohydrate is not <em>required</em>, that it displaces protein
and fat from a fixed calorie budget, and that a cat's glucose handling is not built for a large,
sustained starch load.</p>"""),

h2("protein", "2. Protein"),
"""<p>Protein is the nutrient a cat is least able to economise on. AAFCO sets the adult minimum at
26&nbsp;% of dry matter and the growth minimum at 30&nbsp;%, but those are floors designed to prevent
deficiency, not targets. Most good wet foods land between 40 and 55&nbsp;% protein on a dry-matter
basis, and the evidence suggests cats do better in that range than at the floor.</p>

<h3>Quantity is not the whole story</h3>
<p>“Crude protein” on a label is not measured by finding protein. It is measured by burning the sample,
measuring nitrogen, and multiplying by 6.25. Anything nitrogenous counts. That has two practical
consequences:</p>

<ul>
  <li><strong>Plant protein concentrates inflate the number cheaply.</strong> Pea protein, corn gluten meal,
  potato protein, and soy protein isolate all raise crude protein without supplying a feline-appropriate
  amino acid profile. They are typically short on taurine, methionine, and arginine relative to what a cat
  needs, and their digestibility in cats is lower.</li>
  <li><strong>Adulteration is possible in principle.</strong> The 2007 melamine recall, melamine and cyanuric
  acid added to wheat gluten to fake a higher crude-protein reading, killed and injured a large number of
  cats and dogs and is the reason manufacturer quality control matters as much as ingredient lists.</li>
</ul>

<h3>Biological value</h3>
<p>What actually matters is whether the protein supplies all eleven essential amino acids plus taurine
in usable proportions, and whether the cat can digest it. Roughly ranked for cats:</p>""",

table(
    None,
    ["Tier", "Sources", "Notes"],
    [
        ["<span class=\"chip chip-excellent\">Excellent</span>",
         "Named muscle meat and organ: chicken, turkey, rabbit, salmon, beef, liver, heart",
         "Complete amino acid profile, high digestibility, naturally taurine-rich. Heart is the single richest practical taurine source."],
        ["<span class=\"chip chip-good\">Good</span>",
         "Named meals: “chicken meal”, “salmon meal”; whole egg",
         "A meal is rendered and water-removed, so it is protein-dense by weight. A <em>named</em> meal is a legitimate, concentrated ingredient. Egg is the reference protein for biological value."],
        ["<span class=\"chip chip-poor\">Watch</span>",
         "Unnamed “meat meal”, “poultry by-product meal”, “animal fat”",
         "By-products are not inherently bad (organ meat is a by-product and is excellent) but an unnamed source means you cannot verify species or consistency between batches."],
        ["<span class=\"chip chip-bad\">Discount</span>",
         "Pea protein, corn gluten meal, soy protein isolate, potato protein, wheat gluten",
         "Raise crude protein on the label without matching the amino acid needs of an obligate carnivore. Fine as a minor component; a problem when they sit high in the ingredient list."],
    ]),

callout("warning", """<p>Reading crude protein straight off a wet food label and concluding it is
protein-poor. A can showing 10&nbsp;% protein and 78&nbsp;% moisture is 45&nbsp;% protein on a dry-matter
basis: considerably richer than a kibble showing 32&nbsp;%. You must convert to dry matter before
comparing anything.
<a href="./learn-labels.html">How to do the conversion &rarr;</a></p>"""),

h2("fat", "3. Fat"),
"""<p>Fat is the cat's preferred energy substrate, the carrier for vitamins A, D, E, and K, and the
source of two fatty acids they cannot make. It also drives palatability more than any other component.
AAFCO's minimum is 9&nbsp;% of dry matter; typical good diets run 15–25&nbsp;%.</p>

<h3>The essential fatty acids</h3>
<ul>
  <li><strong>Linoleic acid (omega-6), minimum 0.5&nbsp;% DM.</strong> Required for skin barrier integrity
  and coat quality. Widely available in poultry fat and vegetable oils.</li>
  <li><strong>Arachidonic acid (omega-6), minimum 0.02&nbsp;% DM.</strong> The one that makes cats unusual.
  Dogs and humans build arachidonic acid from linoleic acid using delta-6-desaturase; cats have almost none
  of that enzyme, so it must arrive pre-formed from animal fat. It is required for platelet aggregation,
  inflammatory signalling, wound healing, and reproduction.</li>
</ul>

<h3>Omega-3s: not strictly required, genuinely useful</h3>
<p>EPA and DHA are not on the AAFCO required list for adult cats, but the evidence for them is among the
better evidence in feline nutrition. DHA supports neural and retinal development in kittens and is
required in the diet of queens during gestation and lactation for that reason. In adults, marine-source
omega-3s have reasonable support for reducing osteoarthritis signs and are used adjunctively in chronic
kidney disease. Note the source: cats convert plant-source ALA (flaxseed) to EPA and DHA very poorly,
so flax is close to useless here. Fish oil, krill oil, or green-lipped mussel are the practical sources.</p>""",

callout("note", """<p>Fat is 9&nbsp;kcal per gram against 4 for protein and carbohydrate, so a
high-fat food is calorie-dense and a small measuring error becomes a large calorie error. This is a
common route into obesity when someone switches a cat to a richer food and keeps the portion size the
same.</p>"""),

h2("carbs", "4. Carbohydrate"),
"""<p>The genuinely contested area. Here is what is well supported and what is not.</p>""",

compare(
    "Reasonably well established",
    ["Cats have no dietary carbohydrate requirement, the NRC sets no minimum.",
     "Cats digest and absorb large starch loads less efficiently than dogs, and excess reaches the colon.",
     "Reduced-carbohydrate, higher-protein diets improve glycaemic control in diabetic cats and increase the rate of diabetic remission.",
     "Carbohydrate displaces protein and fat within a fixed calorie budget; extruded dry food generally cannot be made below roughly 25&nbsp;% carbohydrate because starch is needed for the kibble to hold together."],
    "Not established, despite frequent claims",
    ["That dietary carbohydrate <em>causes</em> feline diabetes in otherwise healthy cats. The dominant risk factors are obesity, inactivity, and being a neutered male; total calories matter more than macronutrient split.",
     "That grain-free is nutritionally superior. Grain-free products routinely replace grain with potato, tapioca, or pea starch at a similar or higher carbohydrate level. “Grain-free” is a marketing category, not a nutritional one.",
     "That carbohydrate causes urinary crystals. Urine pH, mineral load, and above all urine concentration drive that, not starch.",
     "That any specific carbohydrate percentage is a threshold for harm. There is no validated cut-off."]),

"""<p>The honest summary: carbohydrate is not the villain it is sometimes made out to be, but there is
no argument for wanting more of it. Where two products are otherwise comparable, the lower-carbohydrate
one gives the cat more of what it actually uses.</p>

<h3>Finding the carbohydrate figure</h3>
<p>Manufacturers are not required to declare it, and almost none do. Estimate it from the guaranteed
analysis by difference:</p>""",

panel("Nitrogen-free extract (carbohydrate by difference)",
"""<p><code>Carbohydrate % = 100 &minus; protein &minus; fat &minus; moisture &minus; ash &minus; crude fibre</code></p>
<p class="note">All figures as-fed, from the guaranteed analysis. If ash is not declared, assume about
2&nbsp;% for wet food and 6–8&nbsp;% for dry. Convert the result to a dry-matter basis to compare across
formats. The answer is an estimate, not an analysis, because guaranteed-analysis figures are minimums
and maximums rather than actual values.</p>"""),

h2("fibre", "5. Fibre"),
"""<p>Not an essential nutrient for cats, but functionally useful. Fermentable fibres such as beet pulp,
psyllium, and inulin feed colonic bacteria and produce short-chain fatty acids that nourish the colonic
lining; insoluble fibres add bulk and speed transit. In practice fibre earns its place in three
situations: constipation and megacolon, hairball management, and weight-loss diets where it adds
satiety without calories. In a healthy cat on a good diet it is unremarkable, neither a benefit to
chase nor a problem to avoid.</p>""",

h2("essential", "6. The nutrients cats cannot make themselves"),
"""<p>These are the hard constraints. Each is a documented deficiency syndrome, not a theoretical
concern, and each is the reason a cat cannot simply eat what a dog or a person eats.</p>""",

entry("Taurine", [("bad", "Fatal if deficient")],
"""<p>A sulfonic amino acid found almost exclusively in animal tissue. Cats have very low activity of
cysteine dioxygenase and cysteine sulfinic acid decarboxylase, the enzymes that build taurine from
cysteine, and they obligately conjugate bile acids with taurine, so they lose it continuously in bile
whether or not they can spare it. There is no glycine fallback as there is in dogs.</p>
<dl>
  <dt>Deficiency causes</dt>
  <dd>Dilated cardiomyopathy (a dilated, failing heart), central retinal degeneration progressing to
  irreversible blindness, reproductive failure, and poor kitten growth. The cardiac and early retinal
  changes are reversible if caught and supplemented in time; advanced retinal loss is not.</dd>
  <dt>Why canned food needs twice as much</dt>
  <dd>AAFCO sets 0.20&nbsp;% DM for canned against 0.10&nbsp;% for extruded, because heat processing and
  the greater gut microbial degradation associated with wet diets increase losses.</dd>
  <dt>Best food sources</dt>
  <dd>Heart, dark poultry meat, shellfish, and mice. Cooking leaches taurine into the cooking water,
  which is one reason home-prepared diets so often come up short.</dd>
</dl>"""),

entry("Arginine", [("bad", "Fatal within hours")],
"""<p>Cats cannot synthesise enough ornithine or citrulline to keep the urea cycle running without
dietary arginine. A <em>single</em> arginine-free meal can produce hyperammonaemia, salivation,
vomiting, ataxia, tetany, and death within hours. This is the fastest-acting nutritional deficiency
described in any domestic species, and it is why feeding a cat a plant-based diet is dangerous rather
than merely suboptimal. Arginine is abundant in all animal protein, so a cat eating meat never
encounters this.</p>"""),

entry("Arachidonic acid", [("neutral", "Essential fatty acid")],
"""<p>Cats have negligible delta-6-desaturase activity and cannot convert linoleic acid into
arachidonic acid. It must come pre-formed from animal fat. Deficiency impairs skin barrier function,
platelet aggregation, wound healing, and reproduction.</p>"""),

entry("Pre-formed vitamin A (retinol)", [("neutral", "Animal sources only")],
"""<p>Cats lack the intestinal dioxygenase that cleaves beta-carotene into retinol. Carrots do nothing
for a cat. Vitamin A must arrive as retinyl esters from liver, fish oil, or supplementation. It is also
one of the few nutrients where oversupply is a genuine clinical problem: hypervitaminosis A from a
liver-heavy diet causes painful bony proliferation along the neck and forelimbs.</p>"""),

entry("Niacin (vitamin B<sub>3</sub>)", [("neutral", "Unusually high requirement")],
"""<p>Most mammals make niacin from tryptophan. In cats a competing enzyme, picolinic carboxylase,
runs at high activity and diverts the pathway, so conversion is far too slow to meet requirements.
The dietary requirement is roughly four times a dog's, which is why the profile figure of
60&nbsp;mg/kg looks so high next to other B vitamins.</p>"""),

entry("Vitamin D<sub>3</sub>", [("neutral", "Dietary only")],
"""<p>Cats have very little 7-dehydrocholesterol in their skin and cannot make useful vitamin&nbsp;D from
sunlight. A cat sunbathing on a windowsill is thermoregulating, not synthesising. All of it must be
eaten: and it has a defined AAFCO maximum, because excess causes hypercalcaemia and soft-tissue
mineralisation including of the kidneys.</p>"""),

entry("Vitamin B<sub>12</sub> (cobalamin)", [("neutral", "Animal sources only")],
"""<p>Available in usable form only from animal tissue. Cats also have an unusually short cobalamin
half-life (around 13 days, against weeks to years in other species) so intestinal disease that
impairs absorption produces clinical deficiency quickly. Low cobalamin is a common, easily missed,
and readily treatable finding in cats with chronic diarrhoea, weight loss, or chronic enteropathy.</p>"""),

entry("Thiamine (vitamin B<sub>1</sub>)", [("poor", "Easily destroyed")],
"""<p>Cats require roughly three to four times as much thiamine as dogs, and it is the least stable
vitamin in pet food: degraded by heat processing, by prolonged storage, and by thiaminase enzymes
present in raw fish and raw shellfish. Deficiency causes anorexia, then a characteristic ventroflexion
of the neck, ataxia, dilated pupils, seizures, and death. Historic thiamine-deficiency recalls of
canned cat food are the reason this vitamin is watched closely, and the reason an all-raw-fish diet
is a known way to injure a cat.</p>"""),

callout("danger", """<p>A cat cannot be safely fed a diet free of animal-source nutrients without
synthetic supplementation of taurine, arginine, arachidonic acid, retinol, vitamin&nbsp;D<sub>3</sub>,
and B<sub>12</sub> at minimum. Commercial products exist that attempt this; the published evidence on
long-term outcomes is thin, and case reports of taurine-deficient cardiomyopathy on home-made plant
diets exist. If this matters to you, it is a conversation to have with a board-certified veterinary
nutritionist, not a decision to make from a label.</p>""",
title="Vegan and vegetarian diets"),

h2("summary", "7. What good looks like"),
"""<p>Pulling the above together, a species-appropriate diet for a healthy adult cat looks roughly
like this on a dry-matter basis. These are not regulatory requirements; they are what the biology
above points at.</p>""",

table(
    "Target ranges for a healthy adult cat, dry-matter basis. Compare with the AAFCO minimums, which are lower by design.",
    ["Component", "Reasonable target", "AAFCO adult minimum"],
    [
        ["Protein", "40–55&nbsp;%", "26&nbsp;%"],
        ["Fat", "15–25&nbsp;%", "9&nbsp;%"],
        ["Carbohydrate", "under 15&nbsp;% where practical", "no requirement"],
        ["Moisture (as fed)", "70&nbsp;%+ for most of the calories", "not specified"],
        ["Taurine", "0.2&nbsp;%+", "0.10&nbsp;% dry / 0.20&nbsp;% canned"],
        ["Phosphorus", "as low as the life stage allows", "0.5&nbsp;%"],
    ]),

callout("tip", """<p>A food that hits those numbers, carries an AAFCO complete-and-balanced statement
for the right life stage, names its animal proteins, and comes from a manufacturer that can answer
the <a href="./learn-daily-requirements.html#check">WSAVA questions</a> is a good food. Almost
everything else on the packaging is marketing.</p>"""),

h2("sources", "Sources"),
"""<ul class="sources">
  <li>National Research Council: <em>Nutrient Requirements of Dogs and Cats</em> (National Academies Press, 2006).</li>
  <li>Association of American Feed Control Officials, <em>AAFCO Dog and Cat Food Nutrient Profiles</em>, Official Publication. <a href="https://www.aafco.org/" target="_blank" rel="noopener noreferrer">aafco.org</a></li>
  <li>Merck Veterinary Manual: <em>Nutritional Requirements of Small Animals</em>. <a href="https://www.merckvetmanual.com/management-and-nutrition/nutrition-small-animals/nutritional-requirements-of-small-animals" target="_blank" rel="noopener noreferrer">merckvetmanual.com</a></li>
  <li>Li X. et al., “Pseudogenization of a sweet-receptor gene accounts for cats' indifference toward sugar,” <em>PLoS Genetics</em> (2005).</li>
  <li>Morris J.G., “Idiosyncratic nutrient requirements of cats appear to be diet-induced evolutionary adaptations,” <em>Nutrition Research Reviews</em> (2002).</li>
  <li>WSAVA Global Nutrition Committee: <em>Global Nutrition Guidelines</em>. <a href="https://wsava.org/global-guidelines/global-nutrition-guidelines/" target="_blank" rel="noopener noreferrer">wsava.org</a></li>
</ul>""",
])

build(
    slug="learn-nutrition",
    h1="Feline nutrition fundamentals",
    description="Why cats are obligate carnivores, what protein, fat, carbohydrate and fibre actually do in a cat, and the eight nutrients cats cannot synthesise for themselves.",
    lede="Cats are not small dogs and they are certainly not small people. Ten million years of eating nothing but other animals left them with metabolic constraints that determine everything else in this guide.",
    body=BODY,
)
