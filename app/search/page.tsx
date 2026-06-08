import { Suspense } from 'react'
import SearchView from './SearchView'

// SearchView uses useSearchParams, which requires a Suspense boundary
// during static export so Next.js can defer query-param reading to the client.
export default function SearchPage() {
  return (
    <Suspense>
      <SearchView />
    </Suspense>
  )
}
