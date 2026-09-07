# -*- coding: utf-8 -*-
from shell import build
from bits import callout, table, h2, panel

PROFILE_ROWS = [
    "Protein and amino acids",
    ["Crude protein (%)", "30.0", "26.0", "-"],
    ["Arginine (%)", "1.25", "1.04", "-"],
    ["Histidine (%)", "0.31", "0.31", "-"],
    ["Isoleucine (%)", "0.52", "0.52", "-"],
    ["Leucine (%)", "1.25", "1.25", "-"],
    ["Lysine (%)", "1.20", "0.83", "-"],
    ["Methionine (%)", "0.62", "0.62", "1.5"],
    ["Methionine + cystine (%)", "1.10", "1.10", "-"],
    ["Phenylalanine (%)", "0.42", "0.42", "-"],
    ["Phenylalanine + tyrosine (%)", "0.88", "0.88", "-"],
    ["Threonine (%)", "0.73", "0.73", "-"],
    ["Tryptophan (%)", "0.25", "0.16", "-"],
    ["Valine (%)", "0.62", "0.62", "-"],
    ["<strong>Taurine, extruded / dry (%)</strong>", "0.10", "0.10", "-"],
    ["<strong>Taurine, canned / wet (%)</strong>", "0.20", "0.20", "-"],
    "Fat and fatty acids",
    ["Crude fat (%)", "9.0", "9.0", "-"],
    ["Linoleic acid (%)", "0.5", "0.5", "-"],
    ["Arachidonic acid (%)", "0.02", "0.02", "-"],
    "Minerals",
    ["Calcium (%)", "1.0", "0.6", "-"],
    ["Phosphorus (%)", "0.8", "0.5", "-"],
    ["Potassium (%)", "0.6", "0.6", "-"],
    ["Sodium (%)", "0.2", "0.2", "-"],
    ["Chloride (%)", "0.3", "0.3", "-"],
    ["Magnesium (%)", "0.08", "0.04", "-"],
    ["Iron (mg/kg)", "80", "80", "-"],
    ["Copper (mg/kg)", "5", "5", "-"],
    ["Manganese (mg/kg)", "7.5", "7.5", "-"],
    ["Zinc (mg/kg)", "75", "75", "2,000"],
    ["Iodine (mg/kg)", "0.35", "0.35", "-"],
    ["Selenium (mg/kg)", "0.1", "0.1", "-"],
    "Vitamins",
    ["Vitamin A (IU/kg)", "9,000", "5,000", "750,000"],
    ["Vitamin D (IU/kg)", "750", "500", "10,000"],
    ["Vitamin E (IU/kg)", "30", "30", "-"],
    ["Vitamin K (mg/kg)", "0.1", "0.1", "-"],
    ["Thiamine, B<sub>1</sub> (mg/kg)", "5.0", "5.0", "-"],
    ["Riboflavin, B<sub>2</sub> (mg/kg)", "4.0", "4.0", "-"],
    ["Pantothenic acid, B<sub>5</sub> (mg/kg)", "5.0", "5.0", "-"],
    ["Niacin, B<sub>3</sub> (mg/kg)", "60", "60", "-"],
    ["Pyridoxine, B<sub>6</sub> (mg/kg)", "4.0", "4.0", "-"],
    ["Folic acid (mg/kg)", "0.8", "0.8", "-"],
    ["Biotin (mg/kg)", "0.07", "0.07", "-"],
    ["Vitamin B<sub>12</sub> (mg/kg)", "0.02", "0.02", "-"],
    ["Choline (mg/kg)", "2,400", "2,400", "-"],
]

DAILY_ROWS = [
    "Energy, macronutrients and water",
    ["Metabolisable energy", "260 kcal"],
    ["Crude protein", "16.9 g"],
    ["Crude fat", "5.9 g"],
    ["Water (total, food + bowl)", "180–270 ml"],
    "Amino acids",
    ["Arginine", "676 mg"],
    ["Histidine", "202 mg"],
    ["Isoleucine", "338 mg"],
    ["Leucine", "813 mg"],
    ["Lysine", "540 mg"],
    ["Methionine", "403 mg"],
    ["Methionine + cystine", "715 mg"],
    ["Phenylalanine", "273 mg"],
    ["Phenylalanine + tyrosine", "572 mg"],
    ["Threonine", "475 mg"],
    ["Tryptophan", "104 mg"],
    ["Valine", "403 mg"],
    ["<strong>Taurine</strong>", "65 mg dry / 130 mg wet"],
    "Fatty acids",
    ["Linoleic acid", "325 mg"],
    ["Arachidonic acid", "13 mg"],
    "Minerals",
    ["Calcium", "390 mg"],
    ["Phosphorus", "325 mg"],
    ["Potassium", "390 mg"],
    ["Sodium", "130 mg"],
    ["Chloride", "195 mg"],
    ["Magnesium", "26 mg"],
    ["Iron", "5.2 mg"],
    ["Zinc", "4.9 mg"],
    ["Manganese", "0.49 mg"],
    ["Copper", "0.33 mg"],
    ["Iodine", "23 µg"],
    ["Selenium", "6.5 µg"],
    "Vitamins",
    ["Vitamin A", "325 IU"],
    ["Vitamin D", "33 IU"],
    ["Vitamin E", "2.0 IU"],
    ["Vitamin K", "6.5 µg"],
    ["Choline", "156 mg"],
    ["Niacin (B<sub>3</sub>)", "3.9 mg"],
    ["Thiamine (B<sub>1</sub>)", "0.33 mg"],
    ["Pantothenic acid (B<sub>5</sub>)", "0.33 mg"],
    ["Riboflavin (B<sub>2</sub>)", "0.26 mg"],
    ["Pyridoxine (B<sub>6</sub>)", "0.26 mg"],
    ["Folic acid", "52 µg"],
    ["Biotin", "4.6 µg"],
    ["Vitamin B<sub>12</sub>", "1.3 µg"],
]

BODY = "\n\n".join([

h2("bases", "1. The three ways requirements are written"),
"""<p>Nutrient requirements for cats are published as a <em>concentration in the food</em>, not as an
amount per cat. That trips people up constantly, so it is worth being precise about the three bases
you will encounter.</p>

<ul>
  <li><strong>Percent of dry matter (% DM).</strong> The concentration once all water is removed. This is
  the basis for the AAFCO profiles and the only fair way to compare a wet food against a dry food.</li>
  <li><strong>Units per 1,000&nbsp;kcal ME.</strong> An energy basis. Because a cat eats to meet its calorie
  needs, this is more biologically honest: a very energy-dense food is eaten in smaller amounts, so it
  must be more concentrated to deliver the same nutrients.</li>
  <li><strong>Amount per day.</strong> What you actually want to know. Multiply the concentration by how
  much dry matter the cat eats in a day.</li>
</ul>""",

panel("Converting between bases",
"""<p><code>% dry matter = (% as fed) &divide; (100 &minus; % moisture) &times; 100</code></p>
<p><code>amount per day = % DM &divide; 100 &times; grams of dry matter eaten per day</code></p>
<p class="note">The AAFCO cat profiles assume an energy density of 4&nbsp;kcal ME per gram of dry matter.
At that density <code>% DM &times; 250</code> gives grams per 1,000&nbsp;kcal, which is why the
26&nbsp;% protein minimum is also quoted as 65&nbsp;g per 1,000&nbsp;kcal. Foods denser than
4.5&nbsp;kcal/g must be corrected upward.</p>"""),

h2("energy", "2. Energy: how many calories per day"),
"""<p>Energy comes first, because every other requirement is expressed relative to it. Start with the
<strong>resting energy requirement (RER)</strong> (what the cat burns doing nothing) then apply a
life-stage factor to get the <strong>maintenance energy requirement (MER)</strong>.</p>""",

panel("The calorie formula",
"""<p><code>RER (kcal/day) = 70 &times; (ideal body weight in kg)<sup>0.75</sup></code></p>
<p><code>MER = RER &times; life-stage factor</code></p>"""),

table(
    "Life-stage factors applied to RER. Use <em>ideal</em> body weight, not current weight, for an overweight cat.",
    ["Cat", "Factor", "Notes"],
    [
        ["Kitten, 0–4 months", "2.5", "Roughly 200–250 kcal per kg body weight per day"],
        ["Kitten, 4–12 months", "2.0", "Tapering as growth slows"],
        ["Intact adult", "1.4", "Higher lean mass and activity"],
        ["Neutered adult", "1.2", "Neutering drops maintenance needs by roughly 20–30&nbsp;%"],
        ["Indoor, inactive, or obese-prone", "1.0", "The realistic default for most pet cats"],
        ["Weight loss", "0.8", "Of RER at <em>ideal</em> weight; supervise with a vet"],
        ["Gestation", "1.6–2.0", "Rising through pregnancy"],
        ["Peak lactation", "2.0–6.0", "Scales with litter size; feed free choice"],
    ],
    aligns=["", "num", ""]),

callout("warning", """<p>Treating the formula's answer as a fact. Individual cats vary from the
predicted value by 10–15&nbsp;% routinely and by up to 50&nbsp;% at the extremes. The formula sets your
opening portion; the cat's body condition over the following four to eight weeks tells you whether it
was right. Weigh monthly and adjust by 10&nbsp;% at a time.</p>"""),

h2("table", "3. The complete nutrient table"),
"""<p>These are the AAFCO Cat Food Nutrient Profiles, the standard that “complete and balanced” on a
US label is measured against. All values are on a <strong>dry-matter basis, per kilogram of food</strong>,
not per kilogram of cat. An em dash means no maximum has been set.</p>""",

table(
    "AAFCO Cat Food Nutrient Profiles, dry-matter basis, presuming 4&nbsp;kcal&nbsp;ME per gram of dry matter. “Growth &amp; reproduction” covers kittens, pregnancy and lactation; a food labelled “all life stages” must meet that column.",
    ["Nutrient", "Growth &amp; reproduction min", "Adult maintenance min", "Maximum"],
    PROFILE_ROWS,
    aligns=["", "num", "num", "num"]),

callout("note", """<p>AAFCO's vitamin&nbsp;K requirement applies where the diet contains more than
25&nbsp;% fish; healthy cats otherwise get vitamin&nbsp;K from intestinal bacterial synthesis. Biotin
is likewise only strictly required where the diet contains antimicrobials or raw egg white, which
contains avidin and binds biotin. Reputable complete diets supply both regardless.</p>""",
title="Note on vitamin K and biotin"),

callout("warning", """<p>Reading these as targets. A profile minimum is the concentration below which
deficiency becomes likely across a population of cats, a floor, not an optimum. Good wet foods commonly
run 40–55&nbsp;% protein on a dry-matter basis against a 26&nbsp;% floor, and there is decent evidence
cats do better nearer the top of that range than the bottom.</p>""",
title="These are minimums, not targets"),

h2("worked", "4. Worked example: a 4.5 kg adult cat"),
"""<p>Percentages are abstract. Here is the same table converted into an actual daily amount for a
neutered, indoor, 4.5&nbsp;kg (10&nbsp;lb) adult cat in good body condition.</p>""",

panel("Three steps from body weight to grams",
"""<p><strong>1: Resting energy.</strong> <code>RER = 70 &times; 4.5^0.75 = 70 &times; 3.09 = 216 kcal/day</code></p>
<p><strong>2: Maintenance.</strong> <code>MER = 216 &times; 1.2 = 260 kcal/day</code></p>
<p><strong>3: Dry matter eaten.</strong> <code>260 kcal &divide; 4 kcal/g = 65 g of dry matter per day</code></p>
<p class="note">65&nbsp;g of dry matter is roughly 70&nbsp;g of a typical kibble, or about 300&nbsp;g
, three to four standard 85&nbsp;g cans,  of a typical 78&nbsp;%-moisture wet food.</p>"""),

table(
    "Adult maintenance minimums &times; 65&nbsp;g of dry matter. This is what must arrive in the cat each day. A complete and balanced food delivers all of it without you counting anything.",
    ["Nutrient", "Minimum per day"],
    DAILY_ROWS,
    aligns=["", "num"]),

callout("tip", """<p>You do not need to hit 42 numbers by hand, and you should not try. Feed a food
whose label carries an AAFCO or FEDIAF complete-and-balanced statement for your cat's life stage, feed
the calorie amount from step 2, and keep fresh water available. That single choice discharges the whole
table. Home-prepared and unbalanced raw diets are where cats actually become deficient, recipes found
online frequently miss taurine, calcium, vitamin&nbsp;E, and trace minerals.</p>"""),

"""<h3>Scaling to your own cat</h3>
<p>Multiply the whole column by <code>your cat's daily dry matter &divide; 65</code>. A 3&nbsp;kg cat on
about 195&nbsp;kcal eats roughly 49&nbsp;g of dry matter, so every figure falls by about 25&nbsp;%.
A 6&nbsp;kg cat on about 325&nbsp;kcal eats roughly 81&nbsp;g, so every figure rises by about 25&nbsp;%.
Kittens use the growth column and eat far more per kilogram of body weight than any adult.</p>""",

h2("water", "5. Water: the nutrient everyone forgets"),
"""<p>Water is a required nutrient and the one a cat dies without fastest. Total daily intake, counting
moisture in food: should land around <strong>40–60&nbsp;ml per kilogram of body weight</strong>, so
roughly 180–270&nbsp;ml for a 4.5&nbsp;kg cat. A second common expression is about 1&nbsp;ml of water per
kilocalorie eaten, which for our example cat gives the same answer.</p>

<p>Where that water comes from matters enormously. A cat eating only dry food takes in perhaps
6&nbsp;g of water with 65&nbsp;g of food and must drink almost all the rest, which cats, descended from
desert animals with a blunt thirst response, reliably fail to do. A cat eating only wet food takes in
around 230&nbsp;ml from the food alone and arrives at adequate hydration without trying.</p>

<p><a href="{{root}}learn/hydration/">Full detail on hydration &rarr;</a></p>""",

h2("ceilings", "6. Upper limits: more is not better"),
"""<p>Deficiency gets the attention, but after obesity the most common nutritional problem in pet cats
is well-meaning oversupply. The AAFCO maximums exist because these nutrients cause disease at high
intakes.</p>""",

table(
    None,
    ["Nutrient", "Maximum", "What excess does"],
    [
        ["Vitamin A", "750,000 IU/kg DM",
         "Hypervitaminosis A: painful bony proliferation along the cervical vertebrae and forelimbs, fused joints, reluctance to groom or turn the head. Classically caused by feeding liver as a staple."],
        ["Vitamin D", "10,000 IU/kg DM",
         "Hypercalcaemia and soft-tissue mineralisation, including of the kidneys. Formulation errors have caused several pet food recalls."],
        ["Methionine", "1.5&nbsp;% DM",
         "Metabolic acidosis, Heinz body anaemia, and reduced food intake at high doses. Relevant because methionine is also used deliberately as a urinary acidifier."],
        ["Zinc", "2,000 mg/kg DM",
         "Interferes with copper and iron absorption; gastrointestinal signs and haemolysis at extremes."],
        ["Phosphorus", "No AAFCO cap",
         "Not capped for healthy cats, but high phosphorus (especially inorganic phosphate salts) is associated with kidney injury and is restricted in every therapeutic renal diet. A meaningful concern for any cat with CKD."],
        ["Iodine", "No AAFCO cap",
         "Wide swings in dietary iodine are one hypothesis for the high prevalence of feline hyperthyroidism. Unproven, but a reason to prefer consistently formulated diets over erratic ones."],
    ],
    aligns=["", "num", ""]),

callout("warning", """<p>Stacking supplements on top of a complete diet. A complete and balanced food is
formulated as a closed system. Adding calcium, a multivitamin, cod liver oil, or a large volume of liver
or tuna does not improve it; it unbalances it, usually by distorting the calcium-to-phosphorus ratio or
pushing vitamins A and D toward their ceilings. Omega-3 oils and joint supplements at label doses are the
usual reasonable exceptions, and even those are worth mentioning to your vet.</p>"""),

h2("check", "7. How to check a real product meets this"),
"""<ol>
  <li><strong>Find the AAFCO statement.</strong> Usually in small type near the feeding guide. You want
  wording like “formulated to meet the nutritional levels established by the AAFCO Cat Food Nutrient
  Profiles for maintenance of adult cats.” If a product says only “for intermittent or supplemental
  feeding,” it is not a complete diet and must not be the whole of what a cat eats.</li>

  <li><strong>Prefer feeding-trial substantiation.</strong> “Animal feeding tests using AAFCO procedures
  substantiate that <em>X</em> provides complete and balanced nutrition” is a stronger claim than
  formulation alone, because it demonstrates the nutrients are actually bioavailable rather than merely
  present on a spreadsheet.</li>

  <li><strong>Check the life stage matches your cat.</strong> Growth, all life stages, adult maintenance,
  or gestation and lactation. An adult-maintenance food fed to a kitten will not meet the growth column.</li>

  <li><strong>Convert the guaranteed analysis to dry matter</strong> before comparing anything above, or
  you will conclude every wet food is protein-deficient.
  <a href="{{root}}learn/labels/">How to do that &rarr;</a></li>

  <li><strong>Ask the manufacturer the WSAVA questions.</strong> Do they employ a full-time qualified
  nutritionist with a PhD in animal nutrition or ACVN/ECVCN board certification? Who formulates the diets?
  Do they own their manufacturing plants? What quality control and analytical testing runs on finished
  batches? Will they provide a complete nutrient analysis rather than just the guaranteed analysis? A
  company that cannot answer these is asking for a great deal of trust.</li>
</ol>""",

h2("sources", "Sources"),
"""<ul class="sources">
  <li>Association of American Feed Control Officials, <em>AAFCO Dog and Cat Food Nutrient Profiles</em>, Official Publication. <a href="https://www.aafco.org/" target="_blank" rel="noopener noreferrer">aafco.org</a></li>
  <li>National Research Council: <em>Nutrient Requirements of Dogs and Cats</em> (National Academies Press, 2006).</li>
  <li>Merck Veterinary Manual: <em>Nutritional Requirements of Small Animals</em>. <a href="https://www.merckvetmanual.com/management-and-nutrition/nutrition-small-animals/nutritional-requirements-of-small-animals" target="_blank" rel="noopener noreferrer">merckvetmanual.com</a></li>
  <li>Pet Nutrition Alliance: <em>Calculating Calories Based on Pet Needs</em> (RER and MER worksheets).</li>
  <li>FEDIAF: <em>Nutritional Guidelines for Complete and Complementary Pet Food</em>, the European counterpart to the AAFCO profiles.</li>
  <li>WSAVA Global Nutrition Committee: <em>Guidelines on Selecting Pet Foods</em>. <a href="https://wsava.org/global-guidelines/global-nutrition-guidelines/" target="_blank" rel="noopener noreferrer">wsava.org</a></li>
</ul>""",
])

build(
    slug="learn-daily-requirements",
    h1="Every nutrient a cat needs, every day",
    description="The complete AAFCO feline nutrient profile: all 42 essential nutrients with minimums and safe upper limits, converted into exact grams and milligrams per day for a real cat.",
    lede="A cat's daily requirement is not one number; it is 42 of them, plus energy and water. This page gives the complete list, the safe upper limits, and the arithmetic that turns a label percentage into grams in the bowl.",
    body=BODY,
)
