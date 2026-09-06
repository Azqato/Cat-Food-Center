# -*- coding: utf-8 -*-
from shell import build
from bits import callout, table, h2, panel, entry, cards

BODY = "\n\n".join([

callout("danger", """<p>This page describes the dietary principles used in each condition so that you
can have a better conversation with your vet. It is not a treatment plan. Every condition here requires
diagnosis (several of them look identical from the outside) and several require a prescription
therapeutic diet whose formulation cannot be replicated by choosing carefully in a supermarket.
Do not diagnose from a web page, and do not change the diet of a cat with kidney, liver, heart, or
endocrine disease without veterinary direction.</p>""",
title="Read this first"),

h2("obesity", "1. Obesity"),
"""<p>The most common nutritional disorder in pet cats, affecting roughly half the cats in developed
countries, and the gateway to several of the conditions below. An overweight cat is three to five times
more likely to develop diabetes mellitus, and carries elevated risk of osteoarthritis, lower urinary
tract disease, hepatic lipidosis, skin disease from impaired grooming, and anaesthetic complications.
Excess weight measurably shortens life.</p>

<h3>Dietary principles</h3>
<ul>
  <li><strong>High protein, controlled calories.</strong> Protein preserves lean body mass during
  restriction, which matters because weight lost as muscle is not the weight you wanted to lose.</li>
  <li><strong>High moisture.</strong> Water adds volume and satiety without calories, and wet food is
  harder to over-serve than kibble.</li>
  <li><strong>Start at about <code>0.8 &times; RER calculated at ideal weight</code></strong>, then adjust
  from the weekly weight trend.</li>
  <li><strong>Cap the rate at 0.5–2&nbsp;% of body weight per week.</strong> Faster is not better; faster
  is how cats get hepatic lipidosis.</li>
  <li><strong>Split into more, smaller meals</strong> and use puzzle feeders to add activity and slow
  consumption.</li>
</ul>""",

callout("warning", """<p>Crash-dieting a cat. Rapid calorie restriction in an overweight cat is the
classic trigger for hepatic lipidosis, which is potentially fatal. Weight loss in cats must be slow and
supervised. This is the single most important reason to run a weight-loss plan through your vet rather
than improvising.</p>"""),

h2("ckd", "2. Chronic kidney disease"),
"""<p>Extremely common in older cats: a large proportion of cats over fifteen have some degree of it.
It is progressive and not curable, but diet is the intervention with the best evidence for extending
both survival and quality of life. Cats fed a therapeutic renal diet live significantly longer than
those maintained on standard food.</p>""",

table(
    "The elements of a renal diet, roughly in order of evidence strength.",
    ["Element", "Rationale"],
    [
        ["<strong>Phosphorus restriction</strong>", "The best-evidenced component. Reduces renal secondary hyperparathyroidism and slows progression. Inorganic phosphate salts are absorbed most readily and are restricted first."],
        ["<strong>Moderately restricted, high-quality protein</strong>", "Reduces the uraemic toxin burden. The restriction must be moderate: over-restricting protein accelerates muscle loss in an animal already prone to it, and inappetence is a bigger threat than azotaemia in many of these cats."],
        ["<strong>High moisture</strong>", "Damaged kidneys cannot concentrate urine, so these cats lose water continuously and live close to dehydration. Wet food is standard; many benefit from home subcutaneous fluids."],
        ["<strong>Potassium supplementation</strong>", "Hypokalaemia is common and causes weakness and further renal injury."],
        ["<strong>Alkalinising, with added B vitamins</strong>", "Metabolic acidosis is common; water-soluble vitamins are lost in the increased urine volume."],
        ["<strong>Omega-3 fatty acids (EPA/DHA)</strong>", "Reasonable evidence for reduced glomerular injury and inflammation."],
    ]),

callout("note", """<p>Appetite is the limiting factor. A therapeutic renal diet that the cat refuses
does nothing. It is better to have a cat eating a less-ideal food than a perfect food it will not touch,
and inappetence in CKD needs to be addressed actively, appetite stimulants such as mirtazapine,
anti-nausea medication, and treating gastric acidity all have a role. Introduce a renal diet slowly,
ideally before the cat feels unwell, and never during a hospital stay where the cat may form a food
aversion.</p>"""),

h2("flutd", "3. FLUTD, cystitis and urinary stones"),
"""<p>Feline lower urinary tract disease is an umbrella term. The commonest form by far is
<strong>feline idiopathic cystitis</strong>, which is a stress-associated inflammatory condition rather
than an infection: bacterial urinary infection is actually uncommon in cats under ten. The rest is
mostly urolithiasis: struvite and calcium oxalate stones.</p>""",

callout("danger", """<p>A cat straining in the litter tray, making repeated trips producing nothing,
crying while urinating, or licking excessively at the genitals may have a urethral obstruction. In a
male cat this kills within 24–48 hours through acute kidney failure and hyperkalaemia. Go to an
emergency vet immediately. Do not wait overnight to see if it improves.</p>""",
title="Urethral obstruction is a life-threatening emergency"),

"""<h3>Dietary and environmental management</h3>
<ul>
  <li><strong>Dilute the urine. This is the primary intervention</strong> for every form of FLUTD.
  Wet food, added water, multiple water stations. Target a urine specific gravity below about 1.035;
  your vet can measure it.</li>
  <li><strong>Struvite stones can be dissolved by diet</strong>, a therapeutic diet that acidifies urine
  and restricts magnesium and phosphorus typically dissolves them over weeks.</li>
  <li><strong>Calcium oxalate stones cannot be dissolved</strong> and must be removed surgically or, for
  small ones, managed by dilution and by avoiding over-acidification. Note that these two stone types
  need opposite urinary pH, which is exactly why the stone must be identified before the diet is chosen.</li>
  <li><strong>For idiopathic cystitis, stress is the driver.</strong> Multimodal environmental
  modification: more litter trays (one per cat plus one), more vertical space, hiding places, predictable
  routine, reducing conflict between cats, has as much evidence behind it as any diet. Some therapeutic
  diets add tryptophan and alpha-casozepine for this reason.</li>
</ul>""",

h2("diabetes", "4. Diabetes mellitus"),
"""<p>Feline diabetes is closest to human type 2: insulin resistance driven by obesity and inactivity,
with amyloid deposition in the pancreatic islets. Neutered, overweight, indoor, middle-aged male cats
are the classic patients. Burmese cats are over-represented.</p>

<p>Unlike in humans and dogs, <strong>remission is a realistic goal.</strong> A substantial fraction of
newly diagnosed cats can come off insulin entirely if treated promptly and aggressively, and the diet
is central to that.</p>

<h3>Dietary principles</h3>
<ul>
  <li><strong>Low carbohydrate, high protein</strong>, typically under about 12&nbsp;% of calories from
  carbohydrate. This lowers post-meal glucose excursions, reduces insulin requirements, and increases
  remission rates.</li>
  <li><strong>Wet food</strong> is the practical way to achieve that carbohydrate level; extruded kibble
  generally cannot go that low.</li>
  <li><strong>Weight loss</strong> where the cat is overweight, which is most of them.</li>
  <li><strong>Consistent meal timing</strong> coordinated with insulin dosing.</li>
</ul>""",

callout("danger", """<p>Switching a diabetic cat to a low-carbohydrate diet dramatically reduces insulin
requirements, sometimes within a day. Doing this without simultaneously adjusting the insulin dose can
cause life-threatening hypoglycaemia. The diet change and the dose change must be planned together with
your vet, with glucose monitoring.</p>""",
title="Never change a diabetic cat's diet without adjusting insulin"),

h2("hyperthyroidism", "5. Hyperthyroidism"),
"""<p>The most common endocrine disease of older cats, usually caused by a benign functional adenoma of
the thyroid. The picture is a cat that is losing weight while eating ravenously, often with vomiting,
increased thirst, restlessness, and a poor coat.</p>

<p>Treatment options are medication (methimazole), radioactive iodine (curative), surgery, or an
<strong>iodine-restricted therapeutic diet</strong>. The dietary route works; thyroid hormone cannot be
made without iodine: but it has a hard condition attached: <strong>the cat must eat absolutely nothing
else.</strong> No treats, no other food, no hunting, no stealing from another cat's bowl. That makes it
impractical in most multi-cat and indoor-outdoor households, and it is generally reserved for cats that
cannot tolerate the other options.</p>""",

callout("note", """<p>Hyperthyroidism masks chronic kidney disease. The elevated thyroid hormone
increases renal blood flow and makes kidney values look better than they are. Treating the thyroid often
unmasks CKD that was there all along, which is not a reason to leave the thyroid untreated, but is a
reason your vet will recheck kidney values after starting treatment.</p>"""),

h2("gi", "6. Inflammatory bowel disease and chronic enteropathy"),
"""<p>Chronic vomiting, diarrhoea, weight loss, or a combination. The differential includes food-responsive
enteropathy, inflammatory bowel disease, and small-cell intestinal lymphoma, which can be difficult to
distinguish without biopsy, and which is why chronic GI signs deserve a proper workup rather than a
succession of food changes.</p>

<h3>Dietary approaches</h3>
<ul>
  <li><strong>A hydrolysed protein diet</strong>, in which protein is broken into fragments too small to
  trigger an immune response. Often the first therapeutic trial.</li>
  <li><strong>A novel protein diet</strong> using a protein the cat has genuinely never eaten, rabbit,
  venison, duck. Its usefulness depends entirely on a complete dietary history.</li>
  <li><strong>Highly digestible, moderate fat</strong> formulations to reduce the digestive workload.</li>
  <li><strong>Cobalamin (B<sub>12</sub>) supplementation.</strong> Cats have an unusually short cobalamin
  half-life and deficiency is common in chronic enteropathy; it is easily measured and easily corrected,
  and correcting it often improves the response to everything else.</li>
  <li><strong>Fibre modification</strong>, and probiotics with reasonable but not overwhelming evidence.</li>
</ul>

<p>A therapeutic diet trial needs to be strict: the target diet and nothing else, including flavoured
medications and dental chews: and needs six to eight weeks before you can judge it.</p>""",

h2("allergy", "7. Food allergy and adverse food reaction"),
"""<p>Less common than the internet suggests: most itchy cats are reacting to fleas or environmental
allergens, not food. True cutaneous adverse food reaction typically presents as non-seasonal itching
around the head and neck, miliary dermatitis, eosinophilic lesions, or over-grooming, sometimes with GI
signs.</p>

<p>The offending allergens are almost always <em>proteins the cat has eaten a lot of</em>, beef, fish,
chicken, and dairy head the published lists. Grain allergy in cats is rare, despite the marketing.</p>

<p>Diagnosis is by <strong>elimination diet trial</strong>: a strict hydrolysed or genuinely novel protein
diet for eight to twelve weeks, followed by rechallenge with the original food to confirm. Blood and
saliva allergy tests for food in cats are not reliable and should not be used to make this diagnosis.</p>""",

callout("warning", """<p>Abandoning an elimination trial after two weeks, or letting the cat have one
flavoured treat. A single lapse invalidates the trial. Strictness for the full duration is the whole
method, and half a trial gives you no information at all.</p>"""),

h2("lipidosis", "8. Hepatic lipidosis"),
"""<p>Uniquely feline, and the reason “my cat has stopped eating” is an emergency rather than an
observation. When a cat stops eating, it mobilises peripheral fat faster than the liver can process it;
triglyceride accumulates in the hepatocytes and the liver fails.</p>

<ul>
  <li><strong>Risk factors:</strong> obesity above all, plus any cause of anorexia, stress, a house move,
  dental pain, a rapid diet change, another illness, or an ill-judged crash diet.</li>
  <li><strong>Timeline:</strong> risk becomes real after 48–72 hours without adequate intake.</li>
  <li><strong>Treatment:</strong> aggressive nutritional support, very often via an oesophagostomy feeding
  tube, which sounds drastic and is in fact well tolerated and frequently life-saving. With prompt
  treatment the prognosis is good; without it, poor.</li>
</ul>""",

callout("danger", """<p>A cat that has not eaten for 24 hours should be seen by a vet. A cat that has not
eaten for 48 hours needs to be seen urgently. Never withhold food to force a diet change, and never
assume an overweight cat can afford to skip meals; it is precisely the overweight cat that is most at
risk.</p>"""),

h2("dental", "9. Dental disease"),
"""<p>Periodontal disease and tooth resorption are extremely common and painful, and cats show it by
eating less, favouring one side, or dropping food rather than by any obvious sign of pain.</p>

<p>Diet plays a limited role. Ordinary kibble does <em>not</em> clean teeth; it shatters on contact and
does little at the gum line where disease begins. Genuine <strong>dental diets</strong> with enlarged
kibble and an engineered fibre matrix do work, and several carry the Veterinary Oral Health Council seal;
so do some dental treats and additives. But none of it substitutes for professional cleaning under
anaesthesia and, where indicated, tooth extraction. A cat with painful teeth eats better after treatment,
which is often the biggest nutritional intervention available.</p>""",

h2("constipation", "10. Constipation and megacolon"),
"""<p>Common in older cats, and frequently driven by dehydration. Management combines increasing dietary
moisture aggressively, adding fibre (psyllium or a fibre-enhanced therapeutic diet) and laxatives such
as lactulose or polyethylene glycol under veterinary direction. Because dehydration is so often the
underlying driver, the hydration measures on the <a href="./learn-hydration.html">hydration page</a> are
the first thing to fix. Untreated recurrent constipation can progress to megacolon, where the colon
loses motility permanently and surgery becomes the option.</p>""",

h2("next", "Related pages"),
cards([
    ("./learn-hydration.html", None, "Hydration",
     "The measures behind the moisture advice on this page."),
    ("./learn-feeding.html", None, "How much and how often",
     "Portion maths, weight management, and body condition scoring."),
]),

h2("sources", "Sources"),
"""<ul class="sources">
  <li>International Renal Interest Society (IRIS): staging and treatment guidelines for feline chronic kidney disease. <a href="http://www.iris-kidney.com/" target="_blank" rel="noopener noreferrer">iris-kidney.com</a></li>
  <li>AAFP and ISFM: <em>Consensus Guidelines on the Diagnosis and Management of Feline Idiopathic Cystitis</em> and the <em>Feline Environmental Needs Guidelines</em>.</li>
  <li>ISFM: <em>Consensus Guidelines on the Practical Management of Diabetes Mellitus in Cats</em>.</li>
  <li>AAHA: <em>Weight Management Guidelines</em> and <em>Dental Care Guidelines for Dogs and Cats</em>.</li>
  <li>Merck Veterinary Manual: feline hepatic lipidosis, hyperthyroidism, chronic enteropathy, and urolithiasis.</li>
  <li>Veterinary Oral Health Council: accepted products for plaque and tartar control in cats. <a href="https://vohc.org/" target="_blank" rel="noopener noreferrer">vohc.org</a></li>
  <li>Tufts Cummings School <em>Petfoodology</em>: clinical nutrition reviews. <a href="https://sites.tufts.edu/petfoodology/" target="_blank" rel="noopener noreferrer">tufts.edu</a></li>
</ul>""",
])

build(
    slug="learn-health",
    h1="Diet in common conditions",
    description="How nutrition is used in feline obesity, chronic kidney disease, FLUTD, diabetes, hyperthyroidism, IBD, food allergy, hepatic lipidosis, dental disease and constipation.",
    lede="Diet is a genuine treatment in several feline diseases and a dangerous thing to improvise in others. This page covers the principles behind each therapeutic approach so you can have a better-informed conversation with your vet.",
    body=BODY,
)
