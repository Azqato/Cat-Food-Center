import Link from 'next/link'

export default function Header() {
  return (
    <header className="sticky top-0 z-50 bg-surface border-b border-hairline">
      <div className="max-w-content mx-auto px-4 h-14 flex items-center justify-between">
        <Link
          href="/"
          className="font-display text-h2 text-ink font-semibold tracking-tight hover:text-accent transition-colors"
        >
          Cat Food Center
        </Link>
        <Link
          href="https://azqato.github.io/support.html"
          target="_blank"
          rel="noopener noreferrer"
          className="rounded-pill bg-accent text-white text-small font-medium px-4 py-2 hover:opacity-90 transition-opacity focus:outline-none focus:ring-2 focus:ring-accent focus:ring-offset-2"
        >
          Support
        </Link>
      </div>
    </header>
  )
}
