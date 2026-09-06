# -*- coding: utf-8 -*-
from shell import build
from bits import callout, cards, h2

BODY = "\n\n".join([

h2("start", "Start here"),
"""<p>The guide is written to be read in order, but every page stands on its own. If you want
the single densest page, go straight to the daily nutrient requirements; it is the reference
everything else is built around.</p>""",

cards([
    ("./learn-daily-requirements.html", "The core answer",
     "Every nutrient a cat needs, every day",
     "All 42 essential nutrients with minimums and safe upper limits, converted into grams and milligrams per day for a real 4.5&nbsp;kg cat."),
    ("./learn-nutrition.html", "Foundations",
     "Why cats are different",
     "Obligate carnivore metabolism, and what protein, fat and carbohydrate actually do in a cat."),
]),

h2("five-rules", "The short version"),
"""<p>If you never read another page here, these five decisions capture most of the benefit
available to a healthy cat.</p>

<ol>
  <li><strong>Feed a food that carries an AAFCO or FEDIAF “complete and balanced” statement for your cat's life stage.</strong>
  That one sentence in small print is what separates a diet from a snack, and it is the only practical
  guarantee that all 42 essential nutrients are present in the right ratios.</li>

  <li><strong>Get most calories in as wet food.</strong> Cats descend from desert animals, have a weak thirst
  drive, and do not reliably drink enough to make up for a dry diet. Dietary moisture is the single easiest
  lever you have on urinary and kidney health.</li>

  <li><strong>Keep the cat lean.</strong> Obesity is the most common nutritional disorder in pet cats and
  multiplies the risk of diabetes, osteoarthritis, and lower urinary tract disease. Measure portions.
  Do not free-feed dry food to a cat that is already carrying weight.</li>

  <li><strong>Prefer named animal proteins high in the ingredient list.</strong> Treat plant protein
  concentrates, artificial colours, and synthetic antioxidants as reasons to look at the next product
  on the shelf.</li>

  <li><strong>Transition food slowly, and never let a cat go without eating for more than 48&nbsp;hours.</strong>
  A cat that stops eating is a genuine emergency, not a fussy phase (see hepatic lipidosis).</li>
</ol>""",

callout("tip", """<p>Almost every difficult question in feline nutrition resolves to the same test:
<em>would this nutrient reach the cat if it were eating a whole animal?</em> Cats did not evolve
to eat grain, and they did not evolve to drink from a bowl. The exceptions to that heuristic are
worth knowing, but it gets you most of the way.</p>"""),

h2("how-to-read", "How this guide is organised"),
"""<p>Five groups, matching the sidebar.</p>""",

cards([
    ("./learn-nutrition.html", "Fundamentals", "Feline nutrition fundamentals",
     "Obligate carnivore metabolism, macronutrients, and the nutrients cats cannot synthesise."),
    ("./learn-daily-requirements.html", "Fundamentals", "Daily nutrient requirements",
     "The complete AAFCO profile table, plus the arithmetic that turns a percentage into a portion."),
    ("./learn-labels.html", "Fundamentals", "Reading a cat food label",
     "The AAFCO statement, guaranteed analysis, ingredient splitting, and the 95/25/3 naming rules."),
    ("./learn-food-types.html", "Food &amp; water", "Wet, dry, raw &amp; fresh",
     "Seven formats compared on moisture, carbohydrate load, safety, dental effect, and cost."),
    ("./learn-hydration.html", "Food &amp; water", "Hydration",
     "How much water a cat needs, why they under-drink, and eleven ways to get more in."),
    ("./learn-additives.html", "Food &amp; water", "Additives to avoid",
     "A tiered reference to preservatives, dyes, thickeners, and fillers, with the evidence for each."),
    ("./learn-feeding.html", "Feeding practice", "How much &amp; how often",
     "Calorie maths, portioning, meal timing, food transitions, and multi-cat households."),
    ("./learn-life-stages.html", "Feeding practice", "Life stages",
     "Weaning, kittenhood, adulthood, pregnancy, and the senior and super-senior years."),
    ("./learn-toxic.html", "Health &amp; safety", "Toxic foods &amp; hazards",
     "What is genuinely dangerous, at roughly what dose, and what to do in the first ten minutes."),
    ("./learn-health.html", "Health &amp; safety", "Diet in common conditions",
     "Obesity, CKD, FLUTD, diabetes, IBD, hyperthyroidism, food allergy, and hepatic lipidosis."),
]),

h2("scope", "What this guide is and is not"),
"""<p>Everything here describes population-level nutrition for healthy cats, drawn from the AAFCO
nutrient profiles, the NRC's <em>Nutrient Requirements of Dogs and Cats</em>, FDA and EFSA guidance,
WSAVA's nutrition toolkit, and the peer-reviewed veterinary literature. Where the evidence is genuinely
contested (carrageenan, grain-free diets, raw feeding) the page says so rather than picking a side
and pretending the argument is settled.</p>""",

callout("danger", """<p>This is educational content, not veterinary advice, and it cannot account for
your individual cat. Any cat that is unwell, losing weight, straining in the litter box, vomiting
repeatedly, or has a diagnosed condition needs a plan from a veterinarian, ideally with input from a
board-certified veterinary nutritionist (ACVN or ECVCN). Never change the diet of a cat with kidney,
liver, heart, or endocrine disease on the strength of a web page.</p>""",
title="Please read this before you change anything"),

h2("related", "Related on this site"),
cards([
    ("./methodology.html", None, "The CFC Score methodology",
     "How we turn this science into a 0–100 score for a specific product."),
    ("./search.html", None, "Search the catalogue",
     "Look up a product by brand or name and see its ingredient and additive breakdown."),
]),
])

build(
    slug="learn",
    h1="The Cat Care Guide",
    title="The Cat Care Guide",
    crumb="Overview",
    description="A free, science-based guide to feeding and raising a cat: exact daily nutrient requirements, additives to avoid, hydration, food types, life stages, label reading, and diet in disease.",
    lede="Everything you need to feed and raise a cat well, grounded in AAFCO nutrient profiles, NRC research, FDA and EFSA guidance, and the published veterinary literature. Free, open, and updated as the science moves.",
    body=BODY,
)
