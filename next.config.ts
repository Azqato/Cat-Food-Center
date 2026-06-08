import type { NextConfig } from 'next'

// GitHub Pages repo: https://github.com/Azqato/Cat-Food-Center
// Deployed at: https://azqato.github.io/Cat-Food-Center/
// If the repo name changes, update both values below.
const REPO = '/Cat-Food-Center'

const nextConfig: NextConfig = {
  output: 'export',
  trailingSlash: true,
  basePath: REPO,
  assetPrefix: REPO,
  images: {
    unoptimized: true,
  },
}

export default nextConfig
