# -*- coding: utf-8 -*-
from shell import build
from bits import callout, table, h2, panel

BODY = "\n\n".join([

h2("order", "1. Read the label in this order"),
"""<p>A pet food label has eight regulated parts and a great deal of unregulated marketing wrapped
around them. Reading it in the order below gets you to a decision quickly and stops the front of the
bag from doing your thinking.</p>

<ol>
  <li><strong>The AAFCO nutritional adequacy statement.</strong> Is this a complete diet, and for which
  life stage? If the answer is wrong, nothing else matters.</li>
  <li><strong>The guaranteed analysis.</strong> Convert to dry matter, then judge.</li>
  <li><strong>The ingredient list.</strong> What the food is made of, in descending order by weight.</li>
  <li><strong>The product name.</strong> The naming rules tell you how much of the named meat is
  actually in there.</li>
  <li><strong>Calorie content.</strong> Needed to work out a portion.</li>
  <li><strong>Feeding directions, manufacturer, and lot code.</strong> Context, accountability, and
  recall traceability.</li>
</ol>""",

h2("aafco-statement", "2. The AAFCO statement - the most important sentence"),
"""<p>Usually set in small type near the feeding guide, sometimes on the back or side panel. It comes in
a few forms, and they are not equivalent.</p>""",

table(
    "The four things an adequacy statement can tell you, from strongest to weakest.",
    ["Wording", "What it means"],
    [
        ["“Animal feeding tests using AAFCO procedures substantiate that <em>X</em> provides complete and balanced nutrition for…”",
         "<span class=\"chip chip-excellent\">Strongest</span> The food was fed to real cats in a controlled trial and they stayed healthy on measured blood parameters. This demonstrates the nutrients are actually bioavailable, not merely present."],
        ["“<em>X</em> is formulated to meet the nutritional levels established by the AAFCO Cat Food Nutrient Profiles for…”",
         "<span class=\"chip chip-good\">Good</span> The recipe calculates out, or a laboratory analysis of the finished food meets the profile. No animal was fed it to confirm absorption. This covers most products on the shelf and is perfectly acceptable."],
        ["“…is intended for intermittent or supplemental feeding only.”",
         "<span class=\"chip chip-poor\">Not a diet</span> A treat, a topper, or a therapeutic food designed to be used under veterinary supervision. It must not be the whole of what a cat eats."],
        ["No adequacy statement at all",
         "<span class=\"chip chip-bad\">Avoid as a staple</span> Common on toppers, broths, and freeze-dried treats. Fine as a garnish, dangerous as a diet."],
    ]),

callout("note", """<p>The statement also names a life stage: <em>growth</em>, <em>gestation and
lactation</em>, <em>maintenance</em> of adult cats, or <em>all life stages</em>. “All life stages” means
the food meets the growth column, which is the more demanding one; it is safe for an adult but is
higher in calories, calcium, and phosphorus than an adult strictly needs. There is no AAFCO “senior”
life stage; senior foods are formulated to the adult maintenance profile with marketing on top.</p>"""),

h2("guaranteed-analysis", "3. The guaranteed analysis and dry-matter maths"),
"""<p>The guaranteed analysis declares minimum crude protein, minimum crude fat, maximum crude fibre,
and maximum moisture. Note the words <em>minimum</em> and <em>maximum</em>; these are regulatory
guarantees, not measurements. The actual protein content is usually a little above the stated minimum.</p>

<p>Because the figures are “as fed”, a wet food's numbers are diluted by water and cannot be compared
directly with a dry food's. Convert both to dry matter first. This is the single most useful piece of
arithmetic in this guide.</p>""",

panel("The dry-matter conversion",
"""<p><code>Dry matter % = 100 &minus; moisture %</code></p>
<p><code>Nutrient on DM basis = (nutrient as fed &divide; dry matter %) &times; 100</code></p>"""),

panel("Worked comparison: a can that looks weak against a kibble that looks strong",
"""<p><strong>Wet food</strong>: 10&nbsp;% protein, 78&nbsp;% moisture.<br>
Dry matter = 100 &minus; 78 = <strong>22&nbsp;%</strong>.<br>
Protein DM = (10 &divide; 22) &times; 100 = <strong>45.5&nbsp;% protein</strong>.</p>
<p><strong>Dry food</strong>: 32&nbsp;% protein, 10&nbsp;% moisture.<br>
Dry matter = 100 &minus; 10 = <strong>90&nbsp;%</strong>.<br>
Protein DM = (32 &divide; 90) &times; 100 = <strong>35.6&nbsp;% protein</strong>.</p>
<p class="note">The can that appeared to have a third of the protein actually has considerably more.
Every cross-format comparison you make must go through this step.</p>"""),

"""<h3>Estimating carbohydrate</h3>
<p>Carbohydrate is almost never declared. Estimate it by difference:</p>""",

panel("Carbohydrate by difference (nitrogen-free extract)",
"""<p><code>Carbohydrate % = 100 &minus; protein &minus; fat &minus; moisture &minus; ash &minus; crude fibre</code></p>
<p class="note">All as-fed. If ash is not declared (it often is not) assume roughly 2&nbsp;% for wet
food and 6–8&nbsp;% for dry. Convert the answer to dry matter before comparing. This is an estimate
built on minimums and maximums, so treat it as a range rather than a number.</p>"""),

callout("warning", """<p>Comparing a wet food's guaranteed analysis directly with a dry food's and
concluding the wet food is protein-poor. It is the most common mistake made in front of a pet food
shelf, and it is exactly backwards.</p>"""),

h2("ingredients", "4. The ingredient list"),
"""<p>Ingredients are listed in descending order by weight <em>as they go into the batch</em>, before
cooking. That single detail creates most of the ways an ingredient list can mislead.</p>

<h3>Ingredient splitting</h3>
<p>A manufacturer that wants chicken at the top of the list can split a single ingredient into several
lighter entries. “Chicken, pea protein, pea fibre, pea starch, peas” puts chicken first, but if you
recombined the pea fractions they might outweigh it. Read the whole list and mentally recombine
related entries.</p>

<h3>The whole-meat weight trick</h3>
<p>Fresh chicken is around 70&nbsp;% water. Listed pre-cooking, it outweighs a dry ingredient of the
same final contribution by a factor of three or so. So “Chicken, corn gluten meal, …” in a kibble may
end up delivering less chicken protein than corn protein in the finished food. A <em>named meal</em>
 (“chicken meal”) is already water-removed, so its position in the list reflects its real
contribution more honestly. Meals are not a red flag; unnamed meals are.</p>""",

table(
    "How to read common ingredient terms.",
    ["Term", "What it actually is", "Verdict"],
    [
        ["“Chicken”, “Salmon”, “Turkey”", "Clean flesh, with or without accompanying skin and bone, from the named species.", "<span class=\"chip chip-excellent\">Good</span>"],
        ["“Chicken meal”", "Rendered chicken with water and most fat removed. Protein-dense and species-identified.", "<span class=\"chip chip-good\">Fine</span>"],
        ["“Chicken by-product meal”", "Rendered organs, bone, and other non-flesh parts, liver, heart, lungs, spleen. Nutritionally excellent in principle; heart is the best taurine source there is.", "<span class=\"chip chip-good\">Acceptable</span>"],
        ["“Meat and bone meal”, “Animal by-product meal”, “Poultry fat”", "Species not identified. Not necessarily poor quality, but batch-to-batch consistency and sourcing cannot be verified.", "<span class=\"chip chip-poor\">Watch</span>"],
        ["“Corn gluten meal”, “Pea protein”, “Soy protein isolate”", "Plant protein concentrates. Raise crude protein on the label without matching feline amino acid needs.", "<span class=\"chip chip-poor\">Discount</span>"],
        ["“Animal digest”", "Enzymatically hydrolysed animal tissue, sprayed on kibble as a palatant. Very effective; species usually unnamed.", "<span class=\"chip chip-poor\">Neutral</span>"],
        ["“Added colour”, “Red 40”, “Yellow 5”, “Titanium dioxide”", "Purely for the human buying it. Cats do not care what colour the food is.", "<span class=\"chip chip-bad\">Avoid</span>"],
        ["“BHA”, “BHT”, “Ethoxyquin”", "Synthetic antioxidant preservatives. See the additives page.", "<span class=\"chip chip-bad\">Avoid</span>"],
        ["“Mixed tocopherols”, “Rosemary extract”, “Ascorbic acid”", "Natural preservatives. Shorter shelf life, no safety questions.", "<span class=\"chip chip-excellent\">Good</span>"],
    ]),

"""<p><a href="./learn-additives.html">Full additive reference &rarr;</a></p>""",

h2("naming", "5. The 95 / 25 / 3 naming rules"),
"""<p>US product names are regulated, and the wording tells you the minimum proportion of the named
ingredient. This is genuinely useful once you know the code.</p>""",

table(
    "AAFCO product naming rules. Percentages exclude added water; the second figure is the minimum including water in a wet food.",
    ["Name form", "Rule", "Minimum named ingredient"],
    [
        ["“Chicken Cat Food”", "The 95&nbsp;% rule", "95&nbsp;% of the product excluding water; 70&nbsp;% including it"],
        ["“Chicken Dinner”, “…Entrée”, “…Formula”, “…Platter”, “…Recipe”", "The 25&nbsp;% (“dinner”) rule", "25&nbsp;% excluding water; 10&nbsp;% including it"],
        ["“Cat Food <em>with</em> Chicken”", "The 3&nbsp;% (“with”) rule", "3&nbsp;%"],
        ["“Chicken <em>Flavour</em> Cat Food”", "The flavour rule", "No minimum, only enough to be detectable"],
    ]),

callout("tip", """<p>One small word changes the recipe by a factor of thirty. “Chicken Cat Food” is
at least 95&nbsp;% chicken; “Cat Food with Chicken” is at least 3&nbsp;%. When two products look
similar and one is much cheaper, the name is usually where the difference is hiding.</p>"""),

h2("calories", "6. Calorie content"),
"""<p>Expressed as kcal ME per kilogram and usually also per can or per cup. You need it to portion the
food properly (see <a href="./learn-feeding.html">how much and how often</a>. Two cautions:)</p>

<ul>
  <li><strong>“Per cup” is unreliable.</strong> Kibble density varies by shape, and how you scoop varies
  by mood. Weigh dry food on a kitchen scale; a cheap scale is the single best-value piece of feline
  health equipment you can buy.</li>
  <li><strong>Calorie density varies enormously between wet foods</strong>, from roughly 0.7 to
  1.3&nbsp;kcal per gram: so switching brands at the same can count can change intake by 40&nbsp;%.</li>
</ul>""",

h2("marketing", "7. Words that mean nothing"),
"""<p>These terms have no regulatory definition for pet food in the US and no agreed nutritional meaning.
They are not necessarily signs of a bad product, but they carry no information.</p>

<ul>
  <li><strong>“Premium”, “super-premium”, “gourmet”, “ultra”</strong>, undefined.</li>
  <li><strong>“Holistic”</strong>: undefined.</li>
  <li><strong>“Human-grade”</strong>: meaningful only if <em>every</em> ingredient and the entire plant
  meet human food manufacturing standards; frequently used more loosely than that.</li>
  <li><strong>“Natural”</strong>: loosely defined by AAFCO as free of chemically synthetic ingredients,
  with a specific exemption for added vitamins and minerals. Says nothing about quality.</li>
  <li><strong>“Grain-free”</strong>: a marketing category, not a nutritional one. Grain is usually
  replaced with potato, tapioca, or pea starch at a similar carbohydrate level.</li>
  <li><strong>“Ancestral”, “biologically appropriate”, “prey-model”</strong>, descriptive language, not
  a standard.</li>
  <li><strong>“Veterinarian recommended”</strong>: unverifiable unless a specific study is cited.</li>
</ul>""",

h2("checklist", "8. A shelf-side checklist"),
"""<ul class="checklist">
  <li>AAFCO complete-and-balanced statement present, for the right life stage</li>
  <li>Feeding-trial substantiation if you can get it</li>
  <li>A named animal protein first, and ideally second</li>
  <li>Protein on a dry-matter basis in the 40–55&nbsp;% range</li>
  <li>Estimated carbohydrate below roughly 15&nbsp;% DM where the format allows</li>
  <li>No artificial colours, BHA, BHT, ethoxyquin, or propylene glycol</li>
  <li>Ingredient splitting recombined and reconsidered</li>
  <li>Calorie content noted so you can portion it</li>
  <li>Manufacturer contactable, with a named nutritionist and owned plants</li>
  <li>Lot code and best-before date legible, in case of a recall</li>
</ul>""",

h2("sources", "Sources"),
"""<ul class="sources">
  <li>Association of American Feed Control Officials, <em>Official Publication</em>, model pet food regulations (labelling, naming, and adequacy statements). <a href="https://www.aafco.org/" target="_blank" rel="noopener noreferrer">aafco.org</a></li>
  <li>US Food and Drug Administration, Center for Veterinary Medicine, <em>Pet Food Labels</em> guidance. <a href="https://www.fda.gov/animal-veterinary/animal-health-literacy/pet-food-labels-general" target="_blank" rel="noopener noreferrer">fda.gov</a></li>
  <li>WSAVA Global Nutrition Committee: <em>Guidelines on Selecting Pet Foods</em>. <a href="https://wsava.org/global-guidelines/global-nutrition-guidelines/" target="_blank" rel="noopener noreferrer">wsava.org</a></li>
</ul>""",
])

build(
    slug="learn-labels",
    h1="How to read a cat food label",
    description="The AAFCO adequacy statement, guaranteed analysis and dry-matter conversion, ingredient splitting, the 95/25/3 naming rules, and the marketing terms that mean nothing.",
    lede="A pet food label has eight regulated parts wrapped in a great deal of unregulated marketing. Here is how to get to a decision in about ninety seconds, and the one piece of arithmetic that makes wet and dry food comparable.",
    body=BODY,
)
