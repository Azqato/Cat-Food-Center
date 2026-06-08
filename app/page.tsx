'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

// TODO: replace with localStorage reads when real product data exists
const RECENTLY_VIEWED = [
  {
    barcode: '0000000000001',
    name: "Weruva Paw Lickin' Chicken",
    brand: 'Weruva',
    score: 81,
    band: 'excellent' as const,
  },
  {
    barcode: '0000000000002',
    name: "Friskies Surfin' & Turfin' Favorites",
    brand: 'Purina Friskies',
    score: 28,
    band: 'poor' as const,
  },
]

const BAND_STYLES: Record<string, { bg: string; label: string }> = {
  excellent: { bg: 'bg-band-excellent', label: 'Excellent' },
  good:      { bg: 'bg-band-good',      label: 'Good' },
  poor:      { bg: 'bg-band-poor',      label: 'Poor' },
  bad:       { bg: 'bg-band-bad',       label: 'Bad' },
}

export default function HomePage() {
  const router = useRouter()
  const [query, setQuery] = useState('')

  function handleSearch(e: React.FormEvent) {
    e.preventDefault()
    const q = query.trim()
    if (q) router.push(`/search?q=${encodeURIComponent(q)}`)
  }

  return (
    <div className="flex flex-col items-center gap-12 pt-8">

      {/* Wordmark and tagline */}
      <div className="text-center">
        <h1 className="font-display text-h1 text-ink">Cat Food Center</h1>
        <p className="text-ink-soft text-body mt-2">
          Trustworthy reviews for your purrfect companion!
        </p>
      </div>

      {/* Scan button */}
      <div className="flex flex-col items-center gap-3">
        <div className="relative group">
          <button
            disabled
            aria-disabled="true"
            aria-describedby="scan-tooltip"
            className="w-32 h-32 rounded-pill bg-accent text-white font-display text-h2 flex items-center justify-center shadow-md opacity-60 cursor-not-allowed select-none"
          >
            Scan
          </button>
          <span
            id="scan-tooltip"
            role="tooltip"
            className="absolute -bottom-9 left-1/2 -translate-x-1/2 bg-ink text-white text-micro px-3 py-1 rounded-pill whitespace-nowrap pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity"
          >
            Coming soon
          </span>
        </div>
        <p className="text-ink-soft text-small">Point at a barcode</p>
      </div>

      {/* Search form */}
      <form onSubmit={handleSearch} className="w-full max-w-sm flex gap-2" role="search">
        <input
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Brand or product name…"
          aria-label="Search cat food products"
          className="flex-1 min-w-0 border border-hairline rounded-card px-4 py-3 text-body text-ink bg-surface placeholder:text-ink-soft focus:outline-none focus:ring-2 focus:ring-accent"
        />
        <button
          type="submit"
          className="rounded-card bg-accent text-white font-medium text-body px-5 py-3 hover:opacity-90 transition-opacity focus:outline-none focus:ring-2 focus:ring-accent focus:ring-offset-2 shrink-0"
        >
          Search
        </button>
      </form>

      {/* Recently viewed */}
      <section className="w-full" aria-label="Recently viewed products">
        <h2 className="font-display text-h2 text-ink mb-4">Recently viewed</h2>
        <ul className="flex flex-col gap-3" role="list">
          {RECENTLY_VIEWED.map((product) => {
            const band = BAND_STYLES[product.band]
            return (
              <li key={product.barcode}>
                <Link
                  href={`/product/${product.barcode}`}
                  className="flex items-center gap-4 bg-surface border border-hairline rounded-card p-4 hover:border-accent transition-colors focus:outline-none focus:ring-2 focus:ring-accent"
                >
                  {/* Score badge */}
                  <div
                    className={`${band.bg} w-14 h-14 rounded-card flex flex-col items-center justify-center shrink-0`}
                    aria-label={`Score ${product.score}, ${band.label}`}
                  >
                    <span className="text-white font-display text-h2 leading-none tabular-nums">
                      {product.score}
                    </span>
                  </div>

                  {/* Product info */}
                  <div className="min-w-0 flex-1">
                    <p className="text-ink font-medium text-body truncate">{product.name}</p>
                    <p className="text-ink-soft text-small">{product.brand}</p>
                    <span
                      className={`inline-block ${band.bg} text-white text-micro px-2 py-0.5 rounded-pill mt-1`}
                    >
                      {band.label}
                    </span>
                  </div>

                  {/* Chevron hint */}
                  <svg
                    aria-hidden="true"
                    className="w-5 h-5 text-ink-soft shrink-0"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth={2}
                    viewBox="0 0 24 24"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
                  </svg>
                </Link>
              </li>
            )
          })}
        </ul>
      </section>

    </div>
  )
}
