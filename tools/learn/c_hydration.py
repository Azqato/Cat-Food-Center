# -*- coding: utf-8 -*-
from shell import build
from bits import callout, table, h2, panel

BODY = "\n\n".join([

h2("why", "1. Why cats are built to be under-hydrated"),
"""<p>The domestic cat descends from <em>Felis lybica</em>, the African wildcat, an animal of arid North
Africa and the Near East that met essentially all its water needs from prey. A mouse is about 70&nbsp;%
water. An animal eating mice does not need a strong thirst drive, and evolution does not maintain
machinery that is not being used.</p>

<p>The result is a species with an unusually blunt thirst response and exceptionally efficient kidneys
that concentrate urine to a degree few mammals match. Both were advantages in the desert. Both are
liabilities in a house where the food arrives at 8&nbsp;% moisture in a bowl.</p>

<p>The critical experimental finding, repeated across studies, is this: <strong>when a cat is fed dry
food, it does not drink enough extra water to compensate.</strong> It drinks more than a wet-fed cat,
but not enough more. Total daily water intake ends up meaningfully lower, and urine ends up more
concentrated.</p>""",

callout("note", """<p>Concentrated urine is not a benign curiosity. It is the central modifiable risk
factor in feline lower urinary tract disease, and in struvite and calcium oxalate stone formation.
Dilute urine means more frequent urination, lower mineral supersaturation, and less time for crystals
to aggregate.</p>"""),

h2("how-much", "2. How much water a cat actually needs"),
"""<p>Two equivalent rules of thumb, both counting moisture in food as well as what is drunk:</p>""",

panel("Daily water requirement",
"""<p><code>40–60 ml per kg of body weight per day</code></p>
<p><code>&asymp; 1 ml of water per kcal of food eaten</code></p>
<p class="note">For a 4.5&nbsp;kg adult cat eating 260&nbsp;kcal a day, both give roughly
<strong>180–270&nbsp;ml</strong> per day.</p>"""),

table(
    "Total daily water needs by body weight. Total means food plus bowl.",
    ["Cat weight", "Daily water need", "Supplied by an all-wet diet", "Must be drunk"],
    [
        ["3 kg", "120–180 ml", "~150 ml", "little to none"],
        ["4 kg", "160–240 ml", "~205 ml", "little to none"],
        ["4.5 kg", "180–270 ml", "~230 ml", "little to none"],
        ["5 kg", "200–300 ml", "~255 ml", "little to none"],
        ["6 kg", "240–360 ml", "~305 ml", "little to none"],
    ],
    aligns=["", "num", "num", ""]),

table(
    "The same 4.5&nbsp;kg cat on different diets. Requirement is about 180–270&nbsp;ml per day.",
    ["Diet", "Water from food", "Cat must drink"],
    [
        ["All wet (78&nbsp;% moisture)", "~230 ml", "~0–40 ml <span class=\"chip chip-excellent\">Easy</span>"],
        ["Half wet, half dry", "~118 ml", "~62–150 ml <span class=\"chip chip-good\">Achievable</span>"],
        ["All dry (8&nbsp;% moisture)", "~6 ml", "~174–264 ml <span class=\"chip chip-bad\">Rarely achieved</span>"],
    ],
    aligns=["", "num", ""]),

callout("tip", """<p>You cannot easily make a cat drink more, but you can make its food wetter. Changing
the diet is a far more reliable lever than any fountain, bowl, or additive, those help at the margin.
The diet does the heavy lifting.</p>"""),

h2("evidence", "3. What the research actually shows"),
"""<ul>
  <li>Increasing dietary moisture increases <strong>total</strong> daily water intake and urine volume,
  and lowers urine specific gravity: cats do not simply drink less to offset it.</li>
  <li>The benefit appears across a broad moisture band. Work on urine supersaturation found meaningful
  effects between roughly <strong>53&nbsp;% and 73&nbsp;% dietary moisture</strong>, which is why even
  adding water to food helps rather than needing an all-canned diet.</li>
  <li>Higher moisture reduces relative supersaturation for both struvite and calcium oxalate, the two
  common feline stone types.</li>
  <li>Increased dietary water has also been associated with increased voluntary activity in cats, likely
  through more frequent litter box trips and general movement.</li>
  <li>In chronic kidney disease, where the kidneys lose the ability to concentrate urine, maintaining
  hydration is one of the few genuinely modifiable factors, and wet food is a standard part of
  management for exactly this reason.</li>
</ul>""",

h2("signs", "4. Recognising dehydration"),
"""<p>Cats hide illness well, and mild dehydration is nearly invisible. Check these:</p>""",

table(
    None,
    ["Check", "Normal", "Concerning"],
    [
        ["Skin tent: lift the scruff and release", "Snaps back immediately", "Returns slowly or stays tented (note: unreliable in thin or elderly cats)"],
        ["Gums", "Moist and slick", "Tacky or dry to the touch"],
        ["Capillary refill: press the gum, release", "Colour returns in under 2 seconds", "Over 2 seconds"],
        ["Eyes", "Full, bright", "Sunken into the sockets"],
        ["Urine clumps in the litter tray", "Several clumps daily, reasonable size", "Very few, very small, or very dark and strong-smelling"],
        ["Energy and appetite", "Normal", "Lethargy, hiding, off food"],
    ]),

callout("danger", """<p>Straining in the litter tray, crying while urinating, repeated trips producing
nothing, or blood in the urine is an emergency in any cat and a <em>life-threatening</em> emergency in a
male cat: a blocked urethra can kill within 24–48 hours. Go to a veterinarian immediately; do not wait
to see whether it settles overnight. Likewise, a cat that has eaten nothing for 24 hours needs to be
seen, and one that has eaten nothing for 48 hours is at real risk of hepatic lipidosis.</p>""",
title="When this becomes an emergency"),

h2("increase", "5. Eleven ways to get more water into a cat"),
"""<p>Ordered roughly by how much difference they make.</p>

<ol>
  <li><strong>Switch some or all calories to wet food.</strong> Nothing else on this list comes close.
  Even replacing one dry meal a day with a can moves total intake substantially.</li>

  <li><strong>Add water to the wet food.</strong> Two to four tablespoons stirred into a can turns it into
  a loose soup most cats accept readily. Start with a splash and increase over a week or two.</li>

  <li><strong>Rehydrate freeze-dried or air-dried food</strong> rather than serving it dry. It is drier
  than kibble otherwise.</li>

  <li><strong>Move the water bowl away from the food.</strong> In the wild, water near a carcass is water
  near contamination. Many cats show a strong preference for drinking away from where they eat, and away
  from the litter tray.</li>

  <li><strong>Use wide, shallow bowls.</strong> Whisker fatigue is real enough to matter: cats dislike
  their whiskers brushing the sides of a deep, narrow bowl. Ceramic, glass, or stainless steel; plastic
  scratches, harbours bacteria, and can taint the taste.</li>

  <li><strong>Add more water stations.</strong> One per cat plus one, spread across floors and rooms. Cats
  drink opportunistically as they pass, so availability drives intake.</li>

  <li><strong>Try a fountain.</strong> Cats are drawn to moving water, again, a wild-instinct heuristic
  that running water is safer than standing. Fountains help many cats and are ignored by others. Clean
  it weekly and change the filter; a slimy fountain is worse than a clean bowl.</li>

  <li><strong>Fill bowls to the brim.</strong> A full bowl lets the cat drink without pushing its face and
  whiskers down into the rim.</li>

  <li><strong>Offer low-sodium bone broth or the water from a tin of springwater tuna</strong> as a
  flavoured water, in small amounts. Make sure any broth contains no onion or garlic, which are toxic
  to cats.</li>

  <li><strong>Refresh the water at least daily.</strong> Cats are sensitive to staleness, dust, and
  biofilm. If you would not drink it, neither will they.</li>

  <li><strong>Try ice cubes or a dripping tap</strong> for cats that treat water as entertainment. Novelty
  works on some cats and is free to test.</li>
</ol>""",

callout("warning", """<p>Never restrict water to manage litter box problems or overnight urination.
Free access to fresh water is non-negotiable for a cat, and restricting it risks urinary obstruction and
kidney injury. If a cat is suddenly drinking a great deal more than usual, that is also a reason to see a
vet: polydipsia is an early sign of chronic kidney disease, diabetes mellitus, and hyperthyroidism.</p>"""),

h2("special", "6. Cats that need extra attention"),
"""<ul>
  <li><strong>Chronic kidney disease.</strong> Damaged kidneys cannot concentrate urine, so these cats
  lose water continuously and live close to dehydration. Wet food is standard, and many benefit from
  subcutaneous fluids given at home: a routine, learnable procedure your vet can teach you.</li>
  <li><strong>History of FLUTD, cystitis, or urinary stones.</strong> Dilute urine is the primary
  preventive measure, alongside stress reduction. Aim for a urine specific gravity below about 1.035;
  your vet can check this.</li>
  <li><strong>Male cats.</strong> A narrower urethra makes obstruction far more likely. Take hydration
  seriously as prevention, not treatment.</li>
  <li><strong>Diabetic cats.</strong> High blood glucose drives osmotic water loss through the urine;
  intake requirements go up.</li>
  <li><strong>Senior cats.</strong> Reduced thirst perception and reduced mobility to reach the bowl.
  Put water where an arthritic cat does not have to climb or jump to get it.</li>
  <li><strong>Hot weather, or any cat that is vomiting or has diarrhoea.</strong> Losses rise quickly and
  a small cat has little reserve.</li>
</ul>""",

h2("sources", "Sources"),
"""<ul class="sources">
  <li>Royal Canin Academy: <em>Water requirements and drinking habits of cats</em>. <a href="https://academy.royalcanin.com/en/veterinary/the-water-requirements-and-drinking-habits-of-cats" target="_blank" rel="noopener noreferrer">royalcanin.com</a></li>
  <li>WALTHAM Petcare Science Institute: <em>Cats can benefit from increased dietary moisture</em>. <a href="https://www.waltham.com/news-events/nutrition/cats-can-benefit-from-increased-dietary-moisture" target="_blank" rel="noopener noreferrer">waltham.com</a></li>
  <li>“Starch to protein ratio and food moisture content influence water balance and urine supersaturation in cats,” <em>Frontiers in Veterinary Science / PMC</em>. <a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11654968/" target="_blank" rel="noopener noreferrer">ncbi.nlm.nih.gov</a></li>
  <li>Purina Institute: <em>Maintaining Hydration in Cats with CKD</em>. <a href="https://www.purinainstitute.com/centresquare/therapeutic-nutrition/maintaining-hydration-in-cats-with-ckd" target="_blank" rel="noopener noreferrer">purinainstitute.com</a></li>
  <li>American Animal Hospital Association, <em>Wet cat food: more than a meal</em>. <a href="https://www.aaha.org/newstat/publications/wet-cat-food-more-than-a-meal-a-key-ingredient-for-feline-wellbeing/" target="_blank" rel="noopener noreferrer">aaha.org</a></li>
  <li>International Society of Feline Medicine / AAFP, consensus guidelines on feline lower urinary tract disease.</li>
</ul>""",
])

build(
    slug="learn-hydration",
    h1="Hydration",
    description="Why cats are chronically under-hydrated, exactly how much water they need per day, how to spot dehydration, and eleven practical ways to increase intake.",
    lede="Cats descend from a desert animal that got its water from prey. They kept the efficient kidneys and the weak thirst drive, and then we started feeding them food that is eight percent water. This is the easiest health lever most owners never pull.",
    body=BODY,
)
