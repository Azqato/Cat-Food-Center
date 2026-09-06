# -*- coding: utf-8 -*-
from shell import build
from bits import callout, table, h2, panel, entry

BODY = "\n\n".join([

callout("danger", """<p>If you believe your cat has eaten something toxic, call a veterinarian or a
poison line <strong>now</strong>: do not wait for symptoms, and do not search for home remedies first.
For many of these, treatment started early is straightforward and treatment started late is not.</p>
<ul>
  <li><strong>ASPCA Animal Poison Control (US):</strong> (888) 426-4435, 24/7, consultation fee applies</li>
  <li><strong>Pet Poison Helpline (US &amp; Canada):</strong> (855) 764-7661, 24/7, fee applies</li>
  <li><strong>Animal PoisonLine (UK):</strong> 01202 509000</li>
</ul>
<p><strong>Never induce vomiting in a cat at home.</strong> Hydrogen peroxide causes severe
haemorrhagic gastritis in cats, salt is dangerous, and for corrosives and petroleum products vomiting
makes the injury worse. Emesis in cats is a veterinary procedure.</p>""",
title="If this is happening right now"),

h2("why-sensitive", "1. Why cats are unusually vulnerable"),
"""<p>Cats are not simply smaller. Two specific quirks of feline physiology explain most of the entries
on this page.</p>

<ul>
  <li><strong>Deficient glucuronidation.</strong> Cats have very little UDP-glucuronosyltransferase, the
  liver enzyme most mammals use to conjugate and excrete drugs and plant compounds. Substances that other
  species clear routinely accumulate in a cat. This is why paracetamol (acetaminophen) is lethal to cats
  at doses a person takes without thinking.</li>
  <li><strong>Oxidatively fragile haemoglobin.</strong> Feline haemoglobin carries eight reactive
  sulfhydryl groups where most mammals have two to four, so cat red blood cells are easily damaged by
  oxidants. This underlies onion, garlic, propylene glycol, and paracetamol toxicity, all of which
  produce Heinz body anaemia.</li>
</ul>

<p>Add a small body mass, a 4&nbsp;kg animal,  and the dose that matters is very small.</p>""",

h2("foods", "2. Foods that are toxic to cats"),

entry("Onion, garlic, leeks, chives, shallots (Allium species)", [("bad", "Severe")],
"""<p>Organosulfur compounds (thiosulfates and related species) oxidise feline haemoglobin, forming
Heinz bodies and destroying red blood cells. The result is haemolytic anaemia, which may appear days
after ingestion rather than immediately.</p>
<dl>
  <dt>Dose</dt>
  <dd>Cats are considerably more sensitive than dogs. Around 5&nbsp;g of onion per kilogram of body
  weight can cause clinically significant changes; that is roughly a tablespoon for an average cat.
  Concentrated forms are the real hazard: <strong>garlic and onion powder are many times more potent by
  weight than the fresh vegetable</strong>, so baby food, gravy, stock, soup, and seasoned meat matter
  more than a scrap of raw onion.</dd>
  <dt>Signs</dt>
  <dd>Lethargy, weakness, pale or yellow gums, rapid breathing, dark or reddish urine, collapse. Often
  delayed by one to five days.</dd>
  <dt>Note</dt>
  <dd>Garlic is <em>not</em> a safe flea remedy. That advice circulates persistently and is wrong.</dd>
</dl>"""),

entry("Chocolate, coffee, tea, caffeine, energy drinks", [("bad", "Severe")],
"""<p>Methylxanthines (theobromine and caffeine) that cats metabolise slowly. Toxicity rises with
cocoa concentration: baking chocolate and cocoa powder are far more dangerous than milk chocolate, and
white chocolate is essentially fat and sugar. Causes vomiting, hyperexcitability, tremors, tachycardia
and arrhythmias, hyperthermia, and seizures. Cats seek chocolate less than dogs because they cannot
taste sweetness, but they do get into cocoa powder, coffee grounds, and discarded tea bags.</p>"""),

entry("Alcohol and raw yeast dough", [("bad", "Severe")],
"""<p>Ethanol depresses the central nervous system profoundly in a small animal; even small amounts
cause vomiting, disorientation, hypothermia, respiratory depression, and coma. Raw bread dough is a
double hazard: it expands in the warm stomach causing painful distension, and fermentation produces
ethanol internally. Also relevant: rum-soaked fruit, liqueur chocolates, and unbaked dough left to
prove on a counter.</p>"""),

entry("Grapes, raisins, sultanas, currants", [("poor", "Uncertain but treat as toxic")],
"""<p>Well documented to cause acute kidney injury in dogs, with the mechanism now believed to involve
tartaric acid. The evidence in cats is thin (mostly because cats rarely eat grapes) so the risk is
uncertain rather than established. Given the severity of the outcome in dogs, the standard veterinary
advice is to treat any ingestion in a cat as potentially serious and call for advice.</p>"""),

entry("Raw fish, raw egg white, and raw shellfish", [("poor", "Chronic risk")],
"""<p>Three separate problems. Raw fish and shellfish contain <strong>thiaminase</strong>, which destroys
thiamine and, fed regularly, causes thiamine deficiency, anorexia, ventroflexion of the neck, ataxia,
seizures, and death. Raw egg white contains <strong>avidin</strong>, which binds biotin. Both raw fish
and raw egg also carry <em>Salmonella</em> risk. Cooked fish in modest amounts is fine; an all-fish diet
is not, for this reason and because of vitamin&nbsp;E depletion and iodine load.</p>"""),

entry("Milk, cream, cheese", [("good", "Not toxic, but a bad idea")],
"""<p>Not poisonous, but most adult cats are lactose intolerant, intestinal lactase declines sharply
after weaning. A saucer of milk produces osmotic diarrhoea and adds a substantial number of empty
calories to an animal prone to obesity. Lactose-free “cat milk” avoids the diarrhoea but not the
calories.</p>"""),

entry("Xylitol and other sugar alcohols", [("poor", "Cautious avoidance")],
"""<p>In dogs, xylitol causes catastrophic insulin release, hypoglycaemia, and liver failure. In cats
the picture is different: in the studies that exist, cats fed xylitol did not develop the hypoglycaemia
and liver injury seen in dogs. That said, the data are limited, the substance has no business in a cat,
and xylitol-containing gum, sweets, peanut butter, and toothpaste should be kept away from all pets.</p>"""),

entry("Bones, fat trimmings, and cooked bone", [("poor", "Mechanical injury")],
"""<p>Cooked bone splinters and can perforate the gut or lodge in the oesophagus. Large fat trimmings
can trigger pancreatitis. Small cooked bones from a chicken carcass are a common emergency.</p>"""),

entry("Dog food", [("good", "Not toxic, but inadequate")],
"""<p>A stolen mouthful is harmless. As a diet it is dangerous: dog food is not formulated for feline
taurine, arachidonic acid, retinol, or niacin requirements, and long-term feeding causes exactly the
deficiency syndromes described in this guide.</p>"""),

table(
    "Other foods to keep away, in brief.",
    ["Food", "Problem"],
    [
        ["Macadamia nuts", "Documented toxicity in dogs; avoid in cats"],
        ["Avocado", "Persin; mostly a bird and large-animal problem, but the pit is an obstruction hazard"],
        ["Citrus oils and peel", "Essential oils cause GI upset and CNS depression in quantity"],
        ["Coconut and coconut oil", "Not toxic; causes diarrhoea in quantity"],
        ["Nutmeg", "Myristicin; tremors and seizures at high doses"],
        ["Salt and salty snacks", "Sodium ion toxicosis at high intake"],
        ["Raw potato and green tomato", "Solanine in the green parts"],
        ["Liver, in quantity", "Chronic excess causes hypervitaminosis A and painful skeletal disease"],
        ["Tuna, as a staple", "Mercury accumulation, vitamin&nbsp;E depletion and steatitis, and a strong preference that crowds out balanced food"],
    ]),

h2("plants", "3. Plants - and one that is a genuine emergency"),

callout("danger", """<p>All parts of true lilies (<em>Lilium</em>) and daylilies (<em>Hemerocallis</em>)
cause acute kidney failure in cats. That includes the petals, leaves, stem, pollen, and <strong>the water
in the vase</strong>. A cat that brushes past a lily and grooms pollen from its coat can receive a lethal
dose. Toxicity can be fatal within 72 hours, and treatment must begin within about 18 hours to give the
best chance: so this is a same-hour emergency, not a wait-and-see.</p>
<p>Easter lily, tiger lily, Asiatic and Oriental lilies, stargazer, Japanese show lily, and daylily are
all implicated. Peace lily, calla lily, and lily of the valley are different plants with different (and
still real) toxicities. <strong>The safest policy is simply to keep no lilies in a house with a
cat</strong>, and to check bouquets you are given.</p>""",
title="Lilies"),

table(
    "Other common houseplants and garden plants that are toxic to cats. This is not exhaustive, check the ASPCA plant database before bringing a new plant home.",
    ["Plant", "Effect"],
    [
        ["Sago palm (<em>Cycas revoluta</em>)", "Acute liver failure; extremely dangerous, seeds worst"],
        ["Azalea and rhododendron", "Grayanotoxins; vomiting, cardiac arrhythmia, collapse"],
        ["Oleander", "Cardiac glycosides; potentially fatal arrhythmias"],
        ["Yew (<em>Taxus</em>)", "Cardiotoxic; sudden death possible"],
        ["Dieffenbachia, philodendron, pothos, monstera", "Insoluble calcium oxalate crystals; intense oral pain, drooling, swelling"],
        ["Peace lily, calla lily", "Calcium oxalate, not the kidney toxicity of true lilies, but painful"],
        ["Autumn crocus (<em>Colchicum</em>)", "Colchicine; severe GI and multi-organ effects"],
        ["Cyclamen", "Saponins concentrated in the tuber"],
        ["Tulip and hyacinth bulbs", "Concentrated toxins in the bulb"],
        ["Amaryllis, daffodil, narcissus", "Lycorine and alkaloids; vomiting, hypotension"],
        ["Kalanchoe", "Cardiac glycosides"],
        ["Aloe vera", "Saponins; vomiting and lethargy"],
        ["English ivy", "Saponins; GI upset and dermatitis"],
        ["Marijuana / cannabis", "Ataxia, hypothermia, prolonged sedation; edibles compound the risk with chocolate or xylitol"],
    ]),

"""<p><strong>Safe alternatives</strong> if you want greenery: cat grass (oat, wheat, or barley),
catnip, spider plant, Boston fern, areca palm, calathea, and most true bromeliads.</p>""",

h2("household", "4. Household and medical hazards"),

entry("Human medications", [("bad", "The single largest category")],
"""<p>Cats poison themselves on medication more than on anything else in the house.</p>
<dl>
  <dt>Paracetamol / acetaminophen</dt>
  <dd>The most dangerous common drug for a cat. A single regular-strength tablet can kill an average cat
  through methaemoglobinaemia and liver necrosis, because cats cannot glucuronidate it. Signs include
  brown or muddy gums, facial and paw swelling, laboured breathing, and dark urine. Never give a cat
  human painkillers under any circumstances.</dd>
  <dt>NSAIDs: ibuprofen, naproxen, aspirin</dt>
  <dd>Cause gastric ulceration and acute kidney injury at low doses. Aspirin has occasional veterinary
  use at very low, carefully spaced doses, which is a decision for a vet, not an owner.</dd>
  <dt>Antidepressants, ADHD medication, sleep aids, decongestants</dt>
  <dd>Pseudoephedrine, amphetamines, and SSRIs cause agitation, hyperthermia, tremors, and seizures.
  Cats are attracted to some tablet coatings.</dd>
  <dt>Vitamin D supplements</dt>
  <dd>High-dose human vitamin&nbsp;D causes hypercalcaemia and kidney injury.</dd>
</dl>"""),

entry("Permethrin and “dog-only” flea products", [("bad", "Very common, very serious")],
"""<p>Permethrin-based spot-on flea treatments made for dogs are severely toxic to cats, causing tremors,
hyperthermia, and prolonged seizures that can be fatal. Cats lack the metabolic capacity to clear
pyrethroids at canine concentrations. This happens most often when a well-meaning owner applies a dog
product to a cat, but also when a treated dog and a cat sleep together in the days after application.
Only use flea products labelled for cats, and separate treated dogs from cats until the application site
is dry.</p>"""),

entry("Ethylene glycol antifreeze", [("bad", "Rapidly fatal")],
"""<p>Sweet-tasting and readily lapped from a garage floor or a driveway puddle. As little as a
teaspoon can kill a cat through calcium oxalate crystal deposition in the kidneys. The window for
effective treatment is very short (hours, not days) so any suspicion of exposure is an immediate
emergency. Propylene-glycol-based antifreeze is a much safer alternative product.</p>"""),

entry("Essential oils and diffusers", [("poor", "Under-recognised")],
"""<p>Cats cannot glucuronidate phenols and monoterpenes efficiently. Tea tree (melaleuca), pine, citrus,
wintergreen, peppermint, eucalyptus, cinnamon, pennyroyal, and ylang-ylang are the frequently implicated
ones. Both direct contact and prolonged exposure to an active diffuser in an unventilated room can cause
drooling, ataxia, tremors, respiratory irritation, and liver injury. If you use a diffuser, do it in a
ventilated room the cat can leave, and never apply oils to a cat's skin.</p>"""),

table(
    "Other household hazards.",
    ["Hazard", "Problem"],
    [
        ["Rodenticides", "Anticoagulant, bromethalin, or cholecalciferol types, all serious, and cats are also poisoned by eating poisoned rodents"],
        ["Slug and snail bait (metaldehyde)", "Severe tremors and seizures"],
        ["Insecticides and organophosphates", "Cholinergic crisis"],
        ["Fabric softener sheets and concentrated detergents", "Cationic detergents cause severe oral and oesophageal ulceration"],
        ["Batteries", "Alkaline burns from chewing; button batteries are an emergency"],
        ["String, tinsel, hair ties, dental floss", "Linear foreign bodies that saw through the intestine, a classic and frequently fatal feline emergency"],
        ["Zinc: coins, hardware, zinc oxide cream", "Haemolytic anaemia"],
        ["Lead: old paint, weights, some imported ceramics", "Neurological and GI signs"],
        ["Glow sticks", "Dibutyl phthalate; intense drooling and mouth pain, rarely serious"],
    ]),

h2("emergency", "5. What to do in the first ten minutes"),
"""<ol>
  <li><strong>Get the cat away from the substance.</strong> Confine it somewhere safe and quiet where you
  can watch it.</li>
  <li><strong>Do not induce vomiting</strong> and do not give milk, salt, oil, or any home remedy.</li>
  <li><strong>Collect the evidence.</strong> The packet, the plant, the tablet blister, the vomit, 
  photograph it or bag it. Identifying the exact substance changes the treatment.</li>
  <li><strong>Estimate the amount and the time.</strong> How much, and how long ago. Both matter more than
  the symptoms at this stage.</li>
  <li><strong>Call the vet or a poison line immediately.</strong> Numbers are at the top of this page.
  Call even if the cat looks completely well: with lilies, paracetamol, and antifreeze in particular,
  the cat looks fine during precisely the window in which treatment works.</li>
  <li><strong>If there is contamination on the coat</strong> (a spilled chemical, a permethrin spot-on)
  ask the poison line whether to wash it off before travelling, and prevent grooming meanwhile.</li>
</ol>""",

callout("tip", """<p>Put your vet's number, the out-of-hours emergency clinic's number, and a poison
line number on the fridge and in your phone <em>today</em>, before you need them. In an actual emergency
nobody finds them quickly.</p>"""),

h2("sources", "Sources"),
"""<ul class="sources">
  <li>ASPCA Animal Poison Control Center: <em>People Foods to Avoid Feeding Your Pets</em> and the toxic plant database. <a href="https://www.aspca.org/pet-care/animal-poison-control" target="_blank" rel="noopener noreferrer">aspca.org</a></li>
  <li>ASPCApro: <em>Top Tips for Treating Feline Intoxications</em>. <a href="https://www.aspcapro.org/resource/top-tips-treating-feline-intoxications" target="_blank" rel="noopener noreferrer">aspcapro.org</a></li>
  <li>Pet Poison Helpline: feline toxin monographs. <a href="https://www.petpoisonhelpline.com/" target="_blank" rel="noopener noreferrer">petpoisonhelpline.com</a></li>
  <li>Cortinovis C. &amp; Caloni F., “Household food items toxic to dogs and cats,” <em>Frontiers in Veterinary Science</em> (2016). <a href="https://www.frontiersin.org/articles/10.3389/fvets.2016.00026/full" target="_blank" rel="noopener noreferrer">frontiersin.org</a></li>
  <li>Merck Veterinary Manual: toxicology sections on Allium species, methylxanthines, lilies, ethylene glycol, permethrin, and paracetamol.</li>
  <li>International Cat Care: lily toxicity and household hazards guidance. <a href="https://icatcare.org/" target="_blank" rel="noopener noreferrer">icatcare.org</a></li>
</ul>""",
])

build(
    slug="learn-toxic",
    h1="Toxic foods and household hazards",
    description="Foods, plants, medications and household substances that poison cats, with the mechanism, the rough dose that matters, and what to do in the first ten minutes.",
    lede="Two quirks of feline physiology (a liver that cannot glucuronidate and haemoglobin that oxidises easily) make cats vulnerable to things other animals shrug off. This page covers what is genuinely dangerous and what to do about it.",
    body=BODY,
)
