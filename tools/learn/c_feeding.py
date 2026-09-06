# -*- coding: utf-8 -*-
from shell import build
from bits import callout, table, h2, panel, compare

BODY = "\n\n".join([

h2("how-much", "1. How much - the calorie calculation"),
"""<p>Ignore the feeding guide on the bag as anything more than a starting hint. Those charts are
generic, are usually generous, and cannot know whether your cat is neutered, indoor, elderly, or
already overweight. Do the arithmetic instead; it takes a minute.</p>""",

panel("Three steps to a daily portion",
"""<p><strong>1.</strong> <code>RER = 70 &times; (ideal body weight in kg)<sup>0.75</sup></code></p>
<p><strong>2.</strong> <code>MER = RER &times; life-stage factor</code>, 1.2 for a neutered adult,
1.0 for an indoor or obesity-prone cat, 1.4 intact, 2.0–2.5 for kittens, 0.8 for weight loss.</p>
<p><strong>3.</strong> <code>Daily grams = MER &divide; kcal per gram of the food</code>, from the
calorie statement on the label.</p>"""),

table(
    "Typical daily calories for a neutered indoor adult cat at a healthy weight, and what that looks like in food. Wet-food figures assume roughly 0.9&nbsp;kcal/g; kibble roughly 3.9&nbsp;kcal/g.",
    ["Ideal weight", "RER", "MER (&times;1.2)", "Wet food/day", "Dry food/day"],
    [
        ["3.0 kg", "160 kcal", "192 kcal", "~213 g (2½ cans)", "~49 g"],
        ["3.5 kg", "179 kcal", "215 kcal", "~239 g (~3 cans)", "~55 g"],
        ["4.0 kg", "198 kcal", "238 kcal", "~264 g (~3 cans)", "~61 g"],
        ["4.5 kg", "216 kcal", "260 kcal", "~289 g (3½ cans)", "~67 g"],
        ["5.0 kg", "234 kcal", "281 kcal", "~312 g (~3¾ cans)", "~72 g"],
        ["5.5 kg", "251 kcal", "301 kcal", "~334 g (~4 cans)", "~77 g"],
        ["6.0 kg", "268 kcal", "322 kcal", "~358 g (~4¼ cans)", "~83 g"],
    ],
    aligns=["", "num", "num", "num", "num"]),

callout("warning", """<p>Feeding to <em>current</em> weight when the cat is overweight. Always calculate
from the cat's <strong>ideal</strong> weight, or you will simply maintain the excess. If you do not know
the ideal weight, your vet can estimate it from body condition score.</p>"""),

callout("note", """<p>Calorie density varies enormously between wet foods, roughly 0.7 to
1.3&nbsp;kcal per gram. Switching brands while keeping the same number of cans can change intake by
40&nbsp;% without anything looking different. Recalculate whenever you change product.</p>"""),

h2("weigh", "2. Weigh the food"),
"""<p>A £10 kitchen scale is the highest-return purchase in feline health care. Scoops and “cups” are
unreliable: kibble density varies by shape and coating, and the way a person fills a scoop varies with
mood and hurry. Measured against a scale, cup-based portioning routinely errs by 20&nbsp;% or more, 
enough, sustained over a year, to move a cat from lean to obese.</p>

<p>Weigh out the day's total each morning into a container, and feed from that. When the container is
empty, the cat has eaten. This also makes it obvious when someone else in the household has fed the cat
too.</p>""",

h2("how-often", "3. How often - meal timing"),
"""<p>A free-living cat eats ten to twenty small prey items across the day and night. Nothing about a
cat is built for two large meals, but nothing about a modern household is built for sixteen.
The practical options:</p>""",

table(
    None,
    ["Pattern", "Suits", "Watch out for"],
    [
        ["Two measured meals a day", "Most adult cats; the simplest workable default", "Long gaps can cause bile vomiting in some cats; add a small third portion if so"],
        ["Three to four small meals", "Kittens, seniors, diabetic cats, cats that vomit on an empty stomach", "Requires a timed feeder or a flexible schedule"],
        ["Free-feeding dry food", "Underweight cats, some multi-cat households", "The single most reliable route to obesity; impossible to monitor intake, which matters because appetite loss is often the first sign of illness"],
        ["Puzzle feeders and food-dispensing toys", "Almost every cat, as part of the ration", "Start easy or the cat gives up; count the calories inside as part of the daily total, not extra"],
        ["Timed automatic feeders", "Cats that wake you at 4&nbsp;a.m.; wet-food models exist with ice packs", "Breaks the association between you and food, which is the point"],
    ]),

callout("tip", """<p>If your cat wakes you before dawn demanding food, an automatic feeder set for
5&nbsp;a.m. solves it in about a week. The cat learns that the machine produces breakfast and you do
not. Feeding the cat yourself when it wakes you teaches the opposite lesson very efficiently.</p>"""),

h2("enrichment", "4. Making the cat work for it"),
"""<p>Indoor cats spend a few minutes a day eating food that took no effort to acquire, and the rest of
it with nothing to do. Food-based enrichment addresses both boredom and speed of eating.</p>

<ul>
  <li><strong>Puzzle feeders</strong>: rolling balls, sliding-tile boards, wet-food mazes. Start with an
  easy one that leaks food generously and make it harder over weeks.</li>
  <li><strong>Scatter feeding</strong>: distribute the dry allowance in five or six spots around the
  house so the cat hunts for it.</li>
  <li><strong>Vertical placement</strong>: put portions on cat trees and shelves so eating involves
  climbing.</li>
  <li><strong>Hunting before feeding</strong>: a five-minute wand toy session ending in a meal follows
  the natural hunt-eat-groom-sleep sequence and settles many cats markedly.</li>
</ul>

<p>In multi-cat households this is also a competition tool: separate, spread-out feeding stations reduce
the resource guarding that causes one cat to gain weight while another slowly loses it.</p>""",

h2("transition", "5. Changing food"),
"""<p>Cats are neophobic about food and their gut microbiome adapts slowly. A sudden switch commonly
produces diarrhoea or outright refusal, and a cat that refuses food is a serious problem rather than an
inconvenience. Go slowly.</p>""",

table(
    "A standard seven-day transition. Double the length of each step for a cat with a sensitive gut, or a cat you know to be fussy.",
    ["Days", "Old food", "New food"],
    [
        ["1–2", "75&nbsp;%", "25&nbsp;%"],
        ["3–4", "50&nbsp;%", "50&nbsp;%"],
        ["5–6", "25&nbsp;%", "75&nbsp;%"],
        ["7+", "0&nbsp;%", "100&nbsp;%"],
    ],
    aligns=["num", "num", "num"]),

"""<h3>When the cat refuses outright</h3>
<ul>
  <li>Warm wet food to just below body temperature. Aroma drives feline appetite far more than taste,
  and warmth releases it.</li>
  <li>Serve on a wide flat plate rather than a deep bowl.</li>
  <li>Put the new food alongside the old rather than mixed in, so the cat can investigate without
  contaminating a food it trusts.</li>
  <li>Try a different texture of the same protein: many refusals are about pâté versus shreds, not
  about chicken versus turkey.</li>
  <li>Do not starve a cat into accepting a food. It does not work, and it is dangerous.</li>
</ul>""",

callout("danger", """<p>A cat that eats nothing for 24 hours should be seen by a vet. A cat that eats
nothing for 48–72 hours is at real risk of <strong>hepatic lipidosis</strong>, in which the body
mobilises fat faster than the liver can process it and the liver fails. Overweight cats are at highest
risk, and it can be fatal. Never attempt to force a diet change by withholding food, and never assume a
cat is “just being fussy” for more than a day.</p>""",
title="Anorexia in cats is an emergency"),

h2("treats", "6. Treats and the 10 percent rule"),
"""<p>Treats should be at most 10&nbsp;% of daily calories, and those calories come <em>out</em> of the
meal portions rather than being added on top. For a 4.5&nbsp;kg cat on 260&nbsp;kcal that is 26&nbsp;kcal
, which is roughly three or four commercial treats, or one small cube of plain cooked chicken.</p>

<p>Two things reliably wreck a good feeding plan:</p>
<ul>
  <li><strong>Dairy.</strong> Most adult cats are lactose intolerant; the enzyme declines after weaning.
  A saucer of milk causes osmotic diarrhoea and adds significant calories.</li>
  <li><strong>Undeclared feeding by other household members.</strong> Everyone gives “just a couple”, and
  the cat gains a kilogram. Write the daily allowance on the fridge and have one person own it.</li>
</ul>

<p>Better treats: single-ingredient freeze-dried meat or fish, small pieces of plain cooked chicken or
turkey, a licked lid, or a few kibbles from the daily ration used as training rewards. Note that
<a href="./learn-toxic.html">a number of common human foods are toxic to cats</a>.</p>""",

h2("weight", "7. Weight management"),
"""<p>Obesity is the most common nutritional disorder in pet cats and roughly half the cats in developed
countries carry excess weight. It shortens life and drives diabetes, osteoarthritis, lower urinary tract
disease, hepatic lipidosis, and anaesthetic risk.</p>

<h3>Body condition score</h3>
<p>Weight alone is misleading, a 5&nbsp;kg Maine Coon and a 5&nbsp;kg Siamese are different cats. Use the
9-point body condition score, where 5 is ideal and every point above adds roughly 10&nbsp;% body weight.</p>""",

compare(
    "An ideal cat (BCS 4–5)",
    ["Ribs easily felt under a thin fat covering, like the back of your hand.",
     "A visible waist behind the ribs when viewed from above.",
     "The belly tucks up when viewed from the side.",
     "A minimal primordial pouch: the loose belly flap is normal in cats and is not fat."],
    "An overweight cat (BCS 7+)",
    ["Ribs difficult to feel through fat.",
     "No waist; the body is oval or rectangular from above.",
     "The belly is rounded and hangs, and the flank swings when walking.",
     "Fat deposits over the lumbar spine and at the base of the tail."]),

"""<h3>Losing weight safely</h3>
<ul>
  <li>Target <strong>0.5–2&nbsp;% of body weight per week</strong>, and no faster. For a 6&nbsp;kg cat
  that is 30–120&nbsp;g a week, slow, and it should be.</li>
  <li>Start at roughly <code>0.8 &times; RER at ideal weight</code>. Weigh weekly and adjust.</li>
  <li>Use a high-protein, high-moisture diet: protein preserves lean mass during restriction and water
  adds volume without calories.</li>
  <li>Feed more, smaller meals; use puzzle feeders to slow eating and add activity.</li>
  <li><strong>Do this with your vet.</strong> Crash dieting a cat causes hepatic lipidosis, and an
  overweight cat is the highest-risk group for it. This is the one area of feline feeding where
  enthusiasm without supervision does real harm.</li>
</ul>""",

callout("tip", """<p>Weigh the cat monthly on the same scale and write it down. A cat can lose
15&nbsp;% of its body weight before an owner who sees it every day notices, and unexplained weight loss
is the earliest sign of hyperthyroidism, chronic kidney disease, diabetes, and cancer. A £15 baby scale
catches problems months before they become visible.</p>"""),

h2("multi-cat", "8. Multi-cat households"),
"""<p>Cats are not communal feeders; they hunt alone. Feeding several cats from adjacent bowls creates
competition that is easy to miss because it plays out as body language rather than fighting.</p>

<ul>
  <li><strong>Separate stations, out of sight of one another</strong>, different rooms or different
  heights, not two bowls side by side.</li>
  <li><strong>One station per cat, plus one spare.</strong> The same rule as litter trays.</li>
  <li><strong>Feed measured meals rather than free-feeding</strong>, so you know who ate what.</li>
  <li><strong>Microchip-activated feeders</strong> solve the hard cases, one cat on a therapeutic diet,
  or a food thief with a weight problem.</li>
  <li><strong>Watch for the quiet loser.</strong> The cat that hangs back is often the one on the way to
  a weight problem, and a bullied cat may also avoid the water bowl and the litter tray.</li>
</ul>""",

h2("sources", "Sources"),
"""<ul class="sources">
  <li>Pet Nutrition Alliance: <em>Calculating Calories Based on Pet Needs</em> (RER and MER worksheets).</li>
  <li>Association for Pet Obesity Prevention: veterinary DER/MER calculator and prevalence surveys. <a href="https://www.petobesityprevention.org/veterinary-der-calculator" target="_blank" rel="noopener noreferrer">petobesityprevention.org</a></li>
  <li>AAHA: <em>Weight Management Guidelines for Dogs and Cats</em>.</li>
  <li>WSAVA Global Nutrition Committee: body condition score charts and the nutritional assessment toolkit. <a href="https://wsava.org/global-guidelines/global-nutrition-guidelines/" target="_blank" rel="noopener noreferrer">wsava.org</a></li>
  <li>AAFP and ISFM: <em>Feline Environmental Needs Guidelines</em> (feeding stations and resource distribution in multi-cat homes).</li>
  <li>Center P. et al., clinical literature on feline hepatic lipidosis and rapid weight loss.</li>
</ul>""",
])

build(
    slug="learn-feeding",
    h1="How much and how often to feed",
    description="Calorie maths, portioning, meal schedules, food transitions, treats, weight management and multi-cat feeding, with the numbers worked out for common cat weights.",
    lede="The feeding guide on the bag does not know your cat is neutered, indoor, eight years old, and already a kilogram over. Here is how to work out the actual portion, and how to deliver it in a way that suits an animal built to eat sixteen small meals a day.",
    body=BODY,
)
