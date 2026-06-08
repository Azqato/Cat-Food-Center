'use client'

// TODO: replace MOCK_RESULTS with real Open Pet Food Facts text-search API call

import { useEffect, useState } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import Link from 'next/link'

const BAND_STYLES: Record<string, { bg: string; label: string }> = {
  excellent: { bg: 'bg-band-excellent', label: 'Excellent' },
  good:      { bg: 'bg-band-good',      label: 'Good' },
  poor:      { bg: 'bg-band-poor',      label: 'Poor' },
  bad:       { bg: 'bg-band-bad',       label: 'Bad' },
}

const MOCK_RESULTS = [
  {
    barcode: '0000000000000',
    name: "Instinct Original Grain-Free Recipe with Real Chicken",
    brand: "Nature's Variety",
    score: 61,
    band: 'good' as const,
  },
  {
    barcode: '0000000000000',
    name: "Instinct Original Grain-Free Recipe with Real Salmon",
    brand: "Nature's Variety",
    score: 58,
    band: 'good' as const,
  },
  {
    barcode: '0000000000000',
    name: "Instinct Original Grain-Free Recipe with Real Duck",
    brand: "Nature's Variety",
    score: 63,
    band: 'good' as const,
  },
]

export default function SearchView() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const q = searchParams.get('q') ?? ''
  const [query, setQuery] = useState(q)

  // Keep input in sync when navigating back/forward
  useEffect(() => { setQuery(q) }, [q])

  function handleSearch(e: React.FormEvent) {
    e.preventDefault()
    const trimmed = query.trim()
    if (trimmed) router.push(`/search?q=${encodeURIComponent(trimmed)}`)
  }

  return (
    <div className="flex flex-col gap-8">

      {/* Search bar */}
      <form onSubmit={handleSearch} className="flex gap-2" role="search">
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

      {/* Results */}
      <section aria-label="Search results">
        {q && (
          <p className="text-small text-ink-soft mb-4">
            Showing results for{' '}
            <span className="font-medium text-ink">&ldquo;{q}&rdquo;</span>
          </p>
        )}

        <ul className="flex flex-col gap-3" role="list">
          {MOCK_RESULTS.map((product, i) => {
            const band = BAND_STYLES[product.band]
            return (
              <li key={i}>
                <Link
                  href={`/product/${product.barcode}`}
                  className="flex items-center gap-4 bg-surface border border-hairline rounded-card p-4 hover:border-accent transition-colors focus:outline-none focus:ring-2 focus:ring-accent"
                >
                  {/* Score badge */}
                  <div
                    className={`${band.bg} w-14 h-14 rounded-card flex items-center justify-center shrink-0`}
                    aria-label={`Score ${product.score}, ${band.label}`}
                  >
                    <span className="text-white font-display text-h2 tabular-nums leading-none">
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

                  {/* Chevron */}
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
