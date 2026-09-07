# -*- coding: utf-8 -*-
from shell import build
from bits import callout, table, h2, panel

BODY = "\n\n".join([

h2("stages", "1. The life stages"),
"""<p>AAFCO recognises only three nutritional life stages: <strong>growth and reproduction</strong>,
<strong>adult maintenance</strong>, and <strong>all life stages</strong> (which simply means the food
meets the growth profile). There is no AAFCO “senior” category; senior foods are formulated to the
adult maintenance profile with marketing attached.</p>

<p>Clinically, though, the 2021 AAFP–AAHA feline life stage guidelines use a more useful five-stage
framework, because what changes with age is monitoring and disease risk more than the nutrient
profile.</p>""",

table(
    "Clinical life stages, and what actually changes nutritionally at each.",
    ["Stage", "Age", "Nutritional priority"],
    [
        ["Kitten", "birth – 1 year", "Growth profile; energy-dense, high protein, DHA, calcium and phosphorus in a controlled ratio"],
        ["Young adult", "1 – 6 years", "Adult maintenance; the critical period for preventing obesity, which usually starts within a year of neutering"],
        ["Mature adult", "7 – 10 years", "Maintenance, but start watching weight, muscle mass, and phosphorus intake"],
        ["Senior", "10 – 14 years", "Highly digestible protein, adequate calories, monitoring for CKD, hyperthyroidism and diabetes"],
        ["Geriatric", "15+ years", "Maintaining intake and body weight becomes the priority; energy needs rise again"],
    ]),

h2("kitten", "2. Kittens: birth to twelve months"),
"""<h3>Nought to four weeks - milk only</h3>
<p>Queen's milk, or if orphaned, a proper <strong>kitten milk replacer</strong>. Never cow's milk: it is
too low in protein and fat for a kitten and its lactose causes osmotic diarrhoea. Orphaned kittens need
feeding every two to three hours around the clock at first, kept warm, a chilled neonatal kitten cannot
digest: and stimulated to toilet after each feed. This is a job to do with veterinary guidance.</p>

<h3>Four to eight weeks - weaning</h3>
<p>Introduce wet kitten food mixed with kitten milk replacer to a gruel, thickening it over two to three
weeks. Most kittens are fully weaned by seven to eight weeks. Weaning is also the window in which food
preferences form, so expose kittens to several textures and protein sources now: it costs nothing and
may save you enormous difficulty when the cat is twelve and needs a therapeutic diet.</p>

<h3>Two to six months - the fast growth phase</h3>""",

table(
    "Kitten requirements against adult, dry-matter basis.",
    ["Nutrient", "Kitten (growth) minimum", "Adult minimum", "Why"],
    [
        ["Crude protein", "30&nbsp;%", "26&nbsp;%", "Rapid tissue accretion; good kitten diets run 40–50&nbsp;%"],
        ["Calcium", "1.0&nbsp;%", "0.6&nbsp;%", "Skeletal growth"],
        ["Phosphorus", "0.8&nbsp;%", "0.5&nbsp;%", "Must stay in a Ca:P ratio of roughly 1.1:1 to 1.5:1"],
        ["Arginine", "1.25&nbsp;%", "1.04&nbsp;%", "Urea cycle capacity under high protein turnover"],
        ["Lysine", "1.20&nbsp;%", "0.83&nbsp;%", "Growth-limiting amino acid"],
        ["Tryptophan", "0.25&nbsp;%", "0.16&nbsp;%", "Growth and neurotransmitter synthesis"],
        ["Vitamin A", "9,000 IU/kg", "5,000 IU/kg", "Growth and immune function"],
        ["Vitamin D", "750 IU/kg", "500 IU/kg", "Calcium handling and bone mineralisation"],
        ["DHA", "not on the AAFCO list", ", ", "Strong evidence for neural and retinal development; look for it in the ingredients"],
    ]),

"""<p><strong>Energy.</strong> A kitten needs roughly 200–250&nbsp;kcal per kilogram of body weight per
day at two to four months: two and a half times an adult's rate per kilo. Feed four small meals a day
to twelve weeks, then three, then two by around six months. Kittens under six months should generally
have food available fairly freely; they have small stomachs and enormous requirements.</p>

<p><strong>Food.</strong> Use a food labelled for <em>growth</em> or <em>all life stages</em> until
twelve months. Large breeds (Maine Coon, Ragdoll, Norwegian Forest) grow until eighteen months to two
years and should stay on kitten food correspondingly longer.</p>""",

callout("warning", """<p>Feeding adult maintenance food to a kitten. It does not meet the growth profile
for protein, calcium, phosphorus, or several amino acids and vitamins, and the consequences, 
skeletal abnormalities, poor growth, are not always reversible. Check the AAFCO statement says
growth or all life stages.</p>"""),

callout("danger", """<p>Do not supplement a complete kitten diet with calcium. Adding calcium to a
balanced food distorts the calcium-to-phosphorus ratio and can cause skeletal disease in a growing
kitten. The most common route to this is a well-meaning owner adding a supplement, or feeding an
all-meat home-made diet that is calcium-deficient and then over-correcting.</p>"""),

h2("neutering", "3. The neutering cliff"),
"""<p>The most predictable weight gain in a cat's life happens in the six to twelve months after
neutering, usually between six months and two years of age. Removing the gonads reduces resting energy
expenditure by roughly 20–30&nbsp;% and simultaneously increases food intake. Studies consistently show
free-fed cats gain substantial weight in the months following the procedure.</p>

<p>The fix is straightforward and almost nobody does it: <strong>recalculate the portion at the time of
neutering</strong>, cutting to about 75–80&nbsp;% of the previous intake, and move from free-feeding to
measured meals. Weigh monthly for the next year. Preventing this weight gain is far easier than
reversing it, and it is probably the single highest-leverage intervention in a young cat's life.</p>""",

h2("adult", "4. Adult maintenance: one to seven years"),
"""<p>The steady state, and the stage where the main risk is complacency. A neutered indoor adult needs
roughly <code>RER &times; 1.0–1.2</code> (see <a href="{{root}}learn/feeding/">how much to feed</a> for)
the numbers. The nutritional targets are those on the
<a href="{{root}}learn/daily-requirements/">daily requirements page</a>.</p>

<p>What matters at this stage is monitoring rather than formulation:</p>
<ul>
  <li>Weigh monthly and record it. A trend is visible in the numbers long before it is visible in the cat.</li>
  <li>Body condition score every few months.</li>
  <li>Keep dietary moisture high: this is the stage where urinary disease commonly first appears,
  particularly in neutered male cats.</li>
  <li>Annual veterinary examination, moving to twice yearly from about seven.</li>
</ul>""",

h2("pregnancy", "5. Pregnancy and lactation"),
"""<p>The most nutritionally demanding period in a cat's life, and the one people most often get wrong
by waiting too long to increase intake.</p>

<ul>
  <li><strong>Switch to a growth or all-life-stages food at breeding</strong>, not at birth. The
  gestation and lactation requirements match the growth profile.</li>
  <li><strong>Cats gain weight steadily from early gestation</strong>, unlike dogs, storing reserves for
  lactation. Expect roughly a 40&nbsp;% increase in body weight by term. Energy intake rises from about
  <code>RER &times; 1.6</code> early to <code>&times; 2.0</code> at term.</li>
  <li><strong>Lactation is the peak.</strong> Requirements reach <code>RER &times; 2.0</code> to
  <code>&times; 6.0</code> depending on litter size, a queen with six kittens at three to four weeks of
  lactation may need four to six times maintenance. Feed free choice throughout; it is very difficult to
  overfeed a lactating queen.</li>
  <li><strong>Taurine matters especially here.</strong> Deficiency in the queen causes fetal resorption,
  low birth weight, poor kitten survival, and developmental abnormalities.</li>
  <li><strong>DHA</strong> in the maternal diet supports neural and retinal development in the kittens.</li>
  <li><strong>Water intake rises sharply</strong> during lactation. Make it easy.</li>
</ul>""",

h2("senior", "6. Senior and geriatric: ten years and up"),
"""<p>The received wisdom that old cats need less protein is wrong, and it has probably harmed a great
many cats. It was imported from human and canine nutrition and does not survive contact with the feline
data.</p>

<h3>What actually changes</h3>
<ul>
  <li><strong>Digestive efficiency falls.</strong> Roughly a fifth of geriatric cats show reduced ability
  to digest protein, and about a third show a significant reduction in fat digestion. So the same food
  delivers fewer usable nutrients.</li>
  <li><strong>Energy needs rise again after about eleven or twelve.</strong> Unusually among species,
  older cats need <em>more</em> calories per kilogram, not fewer, partly from that reduced digestibility.
  Many geriatric cats are underweight, not overweight.</li>
  <li><strong>Lean muscle is lost (sarcopenia).</strong> Cats lose muscle mass progressively from about
  eleven, and loss of lean body mass is associated with shorter survival.</li>
  <li><strong>Senses dull.</strong> Reduced smell and taste depress appetite; warming food helps.</li>
  <li><strong>Disease prevalence climbs steeply</strong>: chronic kidney disease, hyperthyroidism,
  diabetes, dental disease, osteoarthritis.</li>
</ul>""",

callout("tip", """<p>Older cats need <em>more</em> highly digestible protein, not less, figures around
5–6&nbsp;g of protein per kilogram of body weight per day are cited for maintaining lean mass, against
roughly 4&nbsp;g for a young adult. Restricting protein in a healthy senior cat accelerates muscle loss.
Protein restriction is appropriate only in specific diagnosed disease, chiefly advanced chronic kidney
disease, and then under veterinary direction.</p>"""),

"""<h3>Practical senior feeding</h3>
<ul>
  <li>High-quality, highly digestible animal protein, not less protein.</li>
  <li>Wet food, warmed, in several small meals, supports hydration, appetite, and easier eating with
  dental disease.</li>
  <li>Watch phosphorus, because chronic kidney disease is extremely common in this age group. Once CKD is
  diagnosed, phosphorus restriction is the best-evidenced dietary intervention there is.</li>
  <li>Omega-3 fatty acids (EPA and DHA) for joint comfort and renal support.</li>
  <li>Raise the bowls slightly and put food and water where an arthritic cat does not have to jump.
  Osteoarthritis is present radiographically in the large majority of cats over twelve and is
  under-diagnosed because cats do not limp, they simply stop jumping.</li>
  <li>Weigh monthly without fail, and see the vet twice a year with bloodwork including thyroid and
  renal panels. Weight loss in an older cat is never “just age”.</li>
</ul>""",

callout("warning", """<p>Assuming weight loss in an old cat is normal ageing. It is the presenting sign
of hyperthyroidism, chronic kidney disease, diabetes, intestinal disease, and cancer; all of which are
common in this age group and several of which are very treatable if caught early. An old cat losing
weight needs bloodwork, not a bigger bowl.</p>"""),

h2("sources", "Sources"),
"""<ul class="sources">
  <li>AAFP and AAHA: <em>Feline Life Stage Guidelines</em> (2021). <a href="https://catvets.com/" target="_blank" rel="noopener noreferrer">catvets.com</a></li>
  <li>Association of American Feed Control Officials, Cat Food Nutrient Profiles, growth and reproduction column.</li>
  <li>Canadian Veterinary Medical Association: <em>Meeting the Nutritional Needs of Senior Cats</em> (2023). <a href="https://www.canadianveterinarians.net/media/towjnjzy/meeting-the-nutritional-needs-of-senior-cats-march-2023.pdf" target="_blank" rel="noopener noreferrer">canadianveterinarians.net</a></li>
  <li>Perez-Camargo G., “Cat nutrition: what is new in the old?” <em>Compendium on Continuing Education</em> (2004), on geriatric digestibility and energy needs.</li>
  <li>National Research Council: <em>Nutrient Requirements of Dogs and Cats</em> (2006), gestation and lactation chapters.</li>
  <li>Merck Veterinary Manual: nutrition of growing and reproducing cats.</li>
</ul>""",
])

build(
    slug="learn-life-stages",
    h1="Kitten, adult, senior &amp; pregnancy",
    description="How feline nutrient requirements shift from weaning through kittenhood, neutering, adulthood, pregnancy and the senior and geriatric years.",
    lede="Requirements are not constant across a cat's life, and two moments matter more than any other: the growth phase, and the day the cat is neutered. Getting those two right prevents most of the diet-related problems a cat will ever have.",
    body=BODY,
)
