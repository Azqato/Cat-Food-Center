# -*- coding: utf-8 -*-
from shell import build
from bits import callout, table, h2, panel, compare, entry

BODY = "\n\n".join([

h2("overview", "1. The formats at a glance"),
"""<p>Seven formats are widely sold. They differ far more in moisture and carbohydrate than in anything
the marketing talks about.</p>""",

table(
    "Typical values. Individual products vary; always check the label.",
    ["Format", "Moisture", "Carb (DM)", "kcal/g", "Cost", "Verdict"],
    [
        ["Canned / pouch wet", "75–82&nbsp;%", "3–15&nbsp;%", "0.7–1.3", "Medium", "<span class=\"chip chip-excellent\">Best default</span>"],
        ["Extruded dry (kibble)", "6–10&nbsp;%", "25–50&nbsp;%", "3.5–4.5", "Low", "<span class=\"chip chip-poor\">Convenient, dehydrating</span>"],
        ["Freeze-dried raw", "2–5&nbsp;%", "2–10&nbsp;%", "4.5–5.5", "High", "<span class=\"chip chip-good\">Good rehydrated</span>"],
        ["Air-dried / dehydrated", "8–14&nbsp;%", "5–20&nbsp;%", "4.0–5.0", "High", "<span class=\"chip chip-good\">Good rehydrated</span>"],
        ["Frozen raw", "65–75&nbsp;%", "2–8&nbsp;%", "1.2–2.0", "High", "<span class=\"chip chip-poor\">Pathogen risk</span>"],
        ["Gently cooked / fresh", "70–78&nbsp;%", "5–20&nbsp;%", "1.0–1.8", "Very high", "<span class=\"chip chip-good\">Good if complete</span>"],
        ["Home-prepared", "varies", "varies", "varies", "Varies", "<span class=\"chip chip-bad\">Only with a formulated recipe</span>"],
    ],
    aligns=["", "num", "num", "num", "", ""]),

callout("tip", """<p>The format argument is mostly a moisture argument. If you take nothing else from
this page: get the majority of your cat's calories from something with 70&nbsp;%+ moisture, and the
rest of the choice matters much less than the internet suggests.</p>"""),

h2("wet", "2. Canned and pouch wet food"),
"""<p>The default recommendation for most cats, for one dominant reason: it delivers water the cat would
otherwise not drink.</p>""",

compare(
    "Strengths",
    ["70–82&nbsp;% moisture — roughly 230&nbsp;ml of water per day for an average cat, without the cat choosing to drink it.",
     "Naturally low in carbohydrate; no starch is needed to hold the product together.",
     "Typically higher protein on a dry-matter basis than kibble.",
     "Portion control is built in — a can is a defined amount.",
     "Retorting (heat sterilisation in the sealed can) makes it commercially sterile, so pathogen risk is very low.",
     "Easier for cats with dental disease, and more palatable to inappetent or senior cats."],
    "Weaknesses",
    ["Costs more per calorie.",
     "Spoils within about four hours at room temperature; opened cans keep 3–5 days refrigerated.",
     "Cannot be left out for a cat that grazes while you are at work.",
     "Some products use thickeners — guar gum, xanthan, carrageenan — that a minority of cats tolerate poorly.",
     "Needs a higher taurine specification (0.20&nbsp;% DM) because processing and gut losses are greater."]),

callout("note", """<p>Pâté-style products are usually lower in carbohydrate than gravy or “in jelly”
styles, because the gravy needs a starch or gum to thicken it. If you are minimising carbohydrate, pâté
is the reliable choice.</p>"""),

h2("dry", "3. Extruded dry food (kibble)"),
"""<p>The most-sold format, and the one whose drawbacks are most often glossed over. It is not poison —
enormous numbers of cats live long lives on it — but it has a structural problem that cannot be
formulated away.</p>

<h3>The moisture problem</h3>
<p>A cat on dry food alone must drink almost its entire daily water requirement. Cats descend from the
African wildcat, a desert animal that obtained water from prey, and their thirst response does not fully
compensate. Studies consistently show that total water intake — food plus drinking — is lower on dry
diets than wet, producing more concentrated urine. Concentrated urine is the central risk factor in
feline lower urinary tract disease and struvite and oxalate stone formation.</p>

<h3>The starch problem</h3>
<p>Extrusion requires starch to gelatinise and hold the kibble together. That sets a practical floor of
roughly 25&nbsp;% carbohydrate on a dry-matter basis, and many products run far higher. “Grain-free”
kibble substitutes potato, tapioca, or pea starch and lands in the same place.</p>""",

callout("warning", """<p>Believing dry food cleans teeth. Standard kibble shatters on contact and does
little for the gum line, where periodontal disease actually starts. The exception is a genuine
<em>dental</em> diet with an enlarged kibble and a fibre matrix engineered to scrape the tooth surface,
several of which carry the Veterinary Oral Health Council seal — those do work. Ordinary kibble does
not, and dental disease is not a reason to feed it.</p>"""),

compare(
    "Where dry food earns its place",
    ["Cost per calorie, by a wide margin.",
     "Can be left out safely, which suits puzzle feeders and food-dispensing toys.",
     "Long shelf life and simple storage.",
     "Useful as a small measured portion inside an enrichment device even for a mostly-wet-fed cat."],
    "How to use it well if you do",
    ["Make it the minority of calories, not the majority.",
     "Weigh it rather than scooping — density varies and eyeballing overfeeds.",
     "Buy bag sizes you will finish within about six weeks of opening; fat oxidises and vitamins degrade.",
     "Store in the original bag, rolled shut, inside an airtight container — the bag is a fat barrier the container is not.",
     "Never store it in a warm garage."]),

h2("freeze-dried", "4. Freeze-dried and air-dried"),
"""<p>Raw or lightly cooked ingredients with the water removed, sold as nuggets or shreds. Freeze-drying
sublimates water at low temperature; air-drying uses gentle warm airflow that provides some, though not
complete, pathogen reduction.</p>

<p>Nutritionally these can be excellent: very low carbohydrate, high animal protein, minimal processing
damage. Two caveats matter. First, <strong>they are extremely dry</strong> — 2–5&nbsp;% moisture, drier
than kibble — so feeding them without rehydration is worse for water balance than feeding kibble.
Rehydrate with warm water and the problem disappears. Second, freeze-drying does not reliably kill
<em>Salmonella</em> or <em>Listeria</em>; the pathogen considerations under raw food apply to
freeze-dried raw products too.</p>""",

callout("tip", """<p>Freeze-dried raw is at its best as a rehydrated meal or as a high-value topper to
tempt an inappetent cat, not as dry nuggets from the bag.</p>"""),

h2("raw", "5. Raw feeding"),
"""<p>The most contested topic in pet nutrition, and the one where it is most important to separate the
nutritional argument from the microbiological one.</p>

<h3>The nutritional case is reasonable</h3>
<p>A properly formulated raw diet is high in animal protein, near-zero in carbohydrate, high in moisture,
and free of extrusion damage to heat-labile nutrients. Owners commonly report better coat condition and
smaller stools. None of that is implausible.</p>

<h3>The safety case against is stronger than most owners realise</h3>""",

entry("Bacterial contamination", [("bad", "Well documented")],
"""<p>Surveys repeatedly culture <em>Salmonella</em>, <em>Listeria monocytogenes</em>, <em>E.&nbsp;coli</em>,
and <em>Campylobacter</em> from commercial raw pet foods at rates far above cooked products. A Cornell
study found live bacteria culturable from many raw cat foods and none from the cooked comparators.
Cats can shed <em>Salmonella</em> in faeces while appearing entirely healthy, which turns the litter tray
into a household exposure route. The FDA advises against feeding raw or undercooked meat to pets, and
the risk is concentrated in immunocompromised people, infants, and the elderly in the home.</p>"""),

entry("H5N1 avian influenza", [("bad", "Cats have died")],
"""<p>Since 2024 this has moved from theoretical to documented. Cats have become severely ill and died
after eating raw pet food and unpasteurised milk contaminated with highly pathogenic avian influenza.
The FDA has notified owners of H5N1 contamination in specific lots of raw cat food, multiple voluntary
recalls have followed, and the agency now requires cat and dog food manufacturers using uncooked poultry
or cattle material to address H5N1 as a hazard in their food safety plans. Cats appear unusually
susceptible to severe neurological disease from H5N1. This is a live, current risk, not a historical
footnote.</p>"""),

entry("Nutritional imbalance in home-made raw", [("bad", "Very common")],
"""<p>Published analyses of home-prepared raw recipes find a majority are deficient in one or more
essential nutrients — most often calcium, taurine, vitamin&nbsp;E, zinc, or the calcium-to-phosphorus
ratio. All-meat, no-bone diets cause nutritional secondary hyperparathyroidism. Whole-bone diets risk
obstruction, perforation, and fractured teeth. Raw fish adds thiaminase and a route to thiamine
deficiency.</p>"""),

callout("danger", """<p>If you have decided to feed raw despite the above, reduce the risk rather than
ignoring it: use a commercially formulated complete raw diet from a manufacturer that applies
high-pressure processing or an equivalent validated kill step, never a home recipe you found online;
avoid raw poultry entirely while H5N1 is circulating; handle it like raw chicken for humans — separate
board, hot wash, no kitchen-surface contact; do not feed raw in a household with an infant, a pregnant
person, an elderly person, or anyone immunocompromised; and tell your vet, because it changes how they
interpret a diarrhoea case.</p>""",
title="If you feed raw anyway"),

h2("fresh", "6. Gently cooked and fresh-delivery diets"),
"""<p>Human-grade ingredients cooked at low temperature, sold refrigerated or frozen by subscription.
They occupy sensible middle ground: high moisture, low carbohydrate, minimal processing damage, and
cooking removes the pathogen argument that dominates raw.</p>

<p>The questions to ask are exactly the WSAVA ones. Is it formulated by a board-certified veterinary
nutritionist or someone with a PhD in animal nutrition? Does the label carry an AAFCO complete and
balanced statement for the right life stage — many small fresh brands are “supplemental feeding only”
and are not safe as a sole diet? Is the finished product analysed, not just calculated? Cost is
typically two to four times canned food.</p>""",

h2("homemade", "7. Home-prepared diets"),
"""<p>There is one safe way to do this and many unsafe ways.</p>""",

callout("danger", """<p>Do not use a recipe from a book, a blog, or a video. Peer-reviewed evaluations
of publicly available home-made cat food recipes have found that essentially none met all AAFCO nutrient
requirements, with taurine, calcium, iron, zinc, copper, vitamin&nbsp;E, and choline the usual failures.
The safe route is a recipe formulated for your individual cat by a board-certified veterinary
nutritionist (ACVN or ECVCN), including the specific supplement products and amounts, followed exactly,
and rechecked if you change any ingredient. Services such as BalanceIT and Petdiets exist for this.</p>""",
title="Home-made diets fail nutrient analysis far more often than not"),

h2("mixing", "8. Mixed feeding — usually the right answer"),
"""<p>Formats are not a loyalty test. A pragmatic pattern that works for most households:</p>

<ul>
  <li><strong>Two measured wet meals a day</strong> as the nutritional backbone and the water supply.</li>
  <li><strong>A small weighed dry allowance</strong> — say 10–20&nbsp;% of calories — loaded into a puzzle
  feeder or food-dispensing toy for enrichment and slow grazing.</li>
  <li><strong>Treats capped at 10&nbsp;% of daily calories</strong>, deducted from the meal portions rather
  than added on top.</li>
</ul>

<p>This keeps moisture high, keeps cost manageable, gives the cat something to work for, and preserves
your ability to switch if a product is recalled. It also means the cat is used to more than one texture,
which matters enormously the day it needs a therapeutic diet.</p>""",

callout("tip", """<p>Expose kittens and young cats to several textures and protein sources early. Cats
form strong food preferences young, and a cat that has only ever eaten one dry food is genuinely hard
to transition when illness later requires a specific therapeutic diet.</p>"""),

h2("sources", "Sources"),
"""<ul class="sources">
  <li>US Food and Drug Administration, Center for Veterinary Medicine — H5N1 in raw pet food notices and manufacturer requirements. <a href="https://www.fda.gov/animal-veterinary/cvm-updates/cat-and-dog-food-manufacturers-required-consider-h5n1-food-safety-plans" target="_blank" rel="noopener noreferrer">fda.gov</a></li>
  <li>American Veterinary Medical Association — reporting on cat deaths linked to H5N1-contaminated raw pet food. <a href="https://www.avma.org/news/cat-deaths-linked-bird-flu-contaminated-raw-pet-food-sparking-voluntary-recall" target="_blank" rel="noopener noreferrer">avma.org</a></li>
  <li>Tufts Cummings School <em>Petfoodology</em> — “Raw Pet Food Risks: A Research Update” (2025). <a href="https://sites.tufts.edu/petfoodology/2025/10/27/raw-pet-food-research-update/" target="_blank" rel="noopener noreferrer">tufts.edu</a></li>
  <li>WALTHAM Petcare Science Institute — research on dietary moisture and water balance in cats. <a href="https://www.waltham.com/news-events/nutrition/cats-can-benefit-from-increased-dietary-moisture" target="_blank" rel="noopener noreferrer">waltham.com</a></li>
  <li>Veterinary Oral Health Council — accepted products for plaque and tartar control. <a href="https://vohc.org/" target="_blank" rel="noopener noreferrer">vohc.org</a></li>
  <li>Wilson S.A. et al. — “Evaluation of the nutritional adequacy of recipes for home-prepared maintenance diets for cats,” <em>JAVMA</em> (2019).</li>
</ul>""",
])

build(
    slug="learn-food-types",
    h1="Wet, dry, raw &amp; everything else",
    description="Seven cat food formats compared on moisture, carbohydrate load, safety, dental effect and cost — including the current evidence on raw feeding and H5N1.",
    lede="The format argument is mostly a moisture argument. Here is what each of the seven common formats actually does for a cat, where the evidence is solid, and where it is genuinely contested.",
    body=BODY,
)
