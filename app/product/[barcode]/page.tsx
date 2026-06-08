// TODO: replace with real Open Pet Food Facts API fetch + scoring engine

// ── Mock data ──────────────────────────────────────────────────────────────
const PRODUCT = {
  name: "Instinct Original Grain-Free Recipe with Real Chicken",
  brand: "Nature's Variety",
  format: "Wet",
  lifeStage: "Adult Maintenance",
  score: 61,
  band: 'good' as const,
  verdict:
    "A protein-forward wet food with real chicken as the first ingredient, held back by two moderate-risk gelling agents.",
  reasons: [
    "Named animal protein leads ingredient list",
    "High moisture supports urinary tract health",
    "Contains carrageenan (Tier 2 additive)",
  ],
  ingredients: [
    "Chicken",
    "Chicken Broth",
    "Chicken Liver",
    "Pea Protein",
    "Natural Flavor",
    "Carrageenan",
    "Guar Gum",
    "Zinc Sulfate",
    "Iron Amino Acid Chelate",
    "Copper Amino Acid Chelate",
    "Manganese Amino Acid Chelate",
    "Potassium Iodide",
    "Sodium Selenite",
    "Vitamin E Supplement",
    "Thiamine Mononitrate",
    "Niacin",
    "Calcium Pantothenate",
    "Riboflavin Supplement",
    "Biotin",
    "Vitamin B12 Supplement",
    "Folic Acid",
    "Vitamin D3 Supplement",
    "Mixed Tocopherols",
    "Taurine",
  ],
  additives: [
    {
      name: "Carrageenan",
      function: "Gelling agent / thickener",
      tier: 2 as const,
      healthImpact:
        "Associated with intestinal inflammation and disruption of the gut lining in animal studies. Some research suggests links to inflammatory bowel conditions.",
      source: {
        label: "Tobacman — Gastrointestinal Effects of Carrageenan (PubMed)",
        url: "https://pubmed.ncbi.nlm.nih.gov/11895129/",
      },
    },
    {
      name: "Guar Gum",
      function: "Gelling agent / thickener",
      tier: 2 as const,
      healthImpact:
        "High amounts may contribute to digestive discomfort and loose stools in sensitive cats when consumed regularly.",
      source: {
        label: "EFSA Panel — Scientific Opinion on guar gum safety",
        url: "https://efsa.onlinelibrary.wiley.com/doi/10.2903/j.efsa.2017.4669",
      },
    },
  ],
  nutrition: {
    crudeProteinDM: 52,
    crudeFatDM: 28,
    moistureAsFed: 78,
    taurinePresent: true,
  },
  aafcoStatement:
    "Instinct Original Grain-Free Recipe with Real Chicken is formulated to meet the nutritional levels established by the AAFCO Cat Food Nutrient Profiles for maintenance of adult cats.",
  substantiation: "formulation" as const,
  dataCompleteness: "full" as const,
  lastReviewed: "June 7, 2026",
}

// ── Static params (all barcodes that need a pre-rendered page) ─────────────
export function generateStaticParams() {
  return [
    { barcode: '0000000000000' },
    { barcode: '0000000000001' }, // mock: Weruva Paw Lickin' Chicken (recently viewed)
    { barcode: '0000000000002' }, // mock: Friskies Surfin' & Turfin' Favorites (recently viewed)
  ]
}

// ── Shared SVG glyphs ──────────────────────────────────────────────────────
function CheckIcon({ className }: { className?: string }) {
  return (
    <svg
      aria-hidden="true"
      className={className}
      fill="none"
      stroke="currentColor"
      strokeWidth={2.5}
      viewBox="0 0 24 24"
    >
      <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
    </svg>
  )
}

function ChevronRightIcon({ className }: { className?: string }) {
  return (
    <svg
      aria-hidden="true"
      className={className}
      fill="none"
      stroke="currentColor"
      strokeWidth={2}
      viewBox="0 0 24 24"
    >
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
    </svg>
  )
}

// ── Page ───────────────────────────────────────────────────────────────────
export default function ProductPage({ params }: { params: { barcode: string } }) {
  const p = PRODUCT // TODO: fetch real product by params.barcode
  void params

  return (
    <article className="flex flex-col gap-10">

      {/* ── Score header ── */}
      <div className="bg-surface rounded-card shadow-sm overflow-hidden">
        {/* Band color bar */}
        <div className="h-1.5 bg-band-good" aria-hidden="true" />

        <div className="p-5">
          {/* Score + image row */}
          <div className="flex items-start justify-between gap-4 mb-4">
            {/* Score number + band label */}
            <div className="flex items-end gap-3">
              <span className="font-display text-display text-ink tabular-nums leading-none">
                {p.score}
              </span>
              <div className="flex items-center gap-1.5 pb-1">
                <CheckIcon className="w-6 h-6 text-band-good" />
                <span className="font-medium text-body text-band-good">Good</span>
              </div>
            </div>

            {/* Product image placeholder */}
            <div
              className="w-20 h-20 rounded-card bg-hairline flex items-center justify-center shrink-0"
              aria-label="Product image not available"
            >
              <span className="text-ink-soft text-micro text-center leading-tight px-1">
                No<br />image
              </span>
            </div>
          </div>

          {/* Product name and meta */}
          <h1 className="font-display text-h1 text-ink mb-2">{p.name}</h1>
          <div className="flex flex-wrap gap-x-3 gap-y-1 items-center text-small text-ink-soft">
            <span>{p.brand}</span>
            <span aria-hidden="true">·</span>
            <span>{p.format}</span>
            <span aria-hidden="true">·</span>
            <span>{p.lifeStage}</span>
          </div>
        </div>
      </div>

      {/* ── Verdict ── */}
      <section aria-labelledby="verdict-heading">
        <h2 id="verdict-heading" className="font-display text-h2 text-ink mb-3">
          Verdict
        </h2>
        <p className="text-body text-ink mb-4">{p.verdict}</p>
        <ul className="flex flex-wrap gap-2" aria-label="Top reasons">
          {p.reasons.map((reason) => (
            <li
              key={reason}
              className="text-small text-ink border border-hairline rounded-pill px-3 py-1"
            >
              {reason}
            </li>
          ))}
        </ul>
      </section>

      {/* ── Ingredients ── */}
      <section aria-labelledby="ingredients-heading">
        <h2 id="ingredients-heading" className="font-display text-h2 text-ink mb-4">
          Ingredients
        </h2>
        <ol className="overflow-hidden rounded-card border border-hairline divide-y divide-hairline">
          {p.ingredients.map((ingredient, i) => (
            <li
              key={i}
              className="flex items-center gap-3 bg-surface px-4 py-3 text-small text-ink"
            >
              <span className="tabular-nums text-ink-soft w-6 shrink-0 text-right">
                {i + 1}.
              </span>
              <span className="flex-1">{ingredient}</span>
              {/* TODO: expand to plain-language explanation on tap */}
              <ChevronRightIcon className="w-4 h-4 text-hairline shrink-0" />
            </li>
          ))}
        </ol>
        <p className="text-micro text-ink-soft mt-2">
          Tap an ingredient for a plain-language explanation — coming soon.
        </p>
      </section>

      {/* ── Additive flags ── */}
      <section aria-labelledby="additives-heading">
        <h2 id="additives-heading" className="font-display text-h2 text-ink mb-4">
          Additive flags
        </h2>

        <div className="flex items-center gap-2 mb-3">
          <span
            className="w-2 h-2 rounded-full bg-band-poor shrink-0"
            aria-hidden="true"
          />
          <span className="text-small font-medium text-band-poor">
            Tier 2 — Moderate Risk
          </span>
        </div>

        <div className="flex flex-col gap-3">
          {p.additives.map((additive) => (
            <div
              key={additive.name}
              className="bg-surface border border-hairline rounded-card p-4"
            >
              <div className="flex items-start justify-between gap-2 mb-2">
                <span className="font-medium text-body text-ink">{additive.name}</span>
                <span className="text-micro text-ink-soft bg-hairline rounded-pill px-2 py-0.5 shrink-0 ml-2 whitespace-nowrap">
                  {additive.function}
                </span>
              </div>
              <p className="text-small text-ink-soft mb-3">{additive.healthImpact}</p>
              <a
                href={additive.source.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-small text-accent hover:underline focus:underline focus:outline-none"
              >
                Source: {additive.source.label} ↗
              </a>
            </div>
          ))}
        </div>
      </section>

      {/* ── Nutrition snapshot ── */}
      <section aria-labelledby="nutrition-heading">
        <h2 id="nutrition-heading" className="font-display text-h2 text-ink mb-4">
          Nutrition snapshot
        </h2>
        <div className="grid grid-cols-2 gap-3">
          <div className="bg-surface border border-hairline rounded-card p-4">
            <p className="text-micro text-ink-soft mb-1">Crude Protein (DM)</p>
            <p className="font-display text-h1 text-ink tabular-nums leading-none mt-2">
              {p.nutrition.crudeProteinDM}
              <span className="text-h2">%</span>
            </p>
          </div>
          <div className="bg-surface border border-hairline rounded-card p-4">
            <p className="text-micro text-ink-soft mb-1">Crude Fat (DM)</p>
            <p className="font-display text-h1 text-ink tabular-nums leading-none mt-2">
              {p.nutrition.crudeFatDM}
              <span className="text-h2">%</span>
            </p>
          </div>
          <div className="bg-surface border border-hairline rounded-card p-4">
            <p className="text-micro text-ink-soft mb-1">Moisture (as-fed)</p>
            <p className="font-display text-h1 text-ink tabular-nums leading-none mt-2">
              {p.nutrition.moistureAsFed}
              <span className="text-h2">%</span>
            </p>
          </div>
          <div className="bg-surface border border-hairline rounded-card p-4">
            <p className="text-micro text-ink-soft mb-1">Taurine</p>
            <div className="flex items-center gap-2 mt-3">
              <CheckIcon className="w-5 h-5 text-band-excellent" />
              <span className="text-body font-medium text-band-excellent">Present</span>
            </div>
          </div>
        </div>
        <p className="text-micro text-ink-soft mt-2">DM = dry-matter basis.</p>
      </section>

      {/* ── AAFCO adequacy ── */}
      <section aria-labelledby="aafco-heading">
        <h2 id="aafco-heading" className="font-display text-h2 text-ink mb-3">
          AAFCO adequacy
        </h2>
        <div className="bg-surface border border-hairline rounded-card p-4">
          <p className="text-small text-ink italic mb-3">
            &ldquo;{p.aafcoStatement}&rdquo;
          </p>
          <p className="text-micro text-ink-soft">
            Substantiated by: {p.substantiation}
          </p>
        </div>
      </section>

      {/* ── Footer metadata ── */}
      <div className="border-t border-hairline pt-4 flex flex-wrap gap-4 justify-between items-center">
        <div className="flex items-center gap-1.5">
          <CheckIcon className="w-4 h-4 text-band-excellent" />
          <span className="text-micro text-ink-soft capitalize">
            {p.dataCompleteness} data
          </span>
        </div>
        <span className="text-micro text-ink-soft">
          Last reviewed: {p.lastReviewed}
        </span>
      </div>

    </article>
  )
}
