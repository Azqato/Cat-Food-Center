import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        bg: '#FAF7F2',
        surface: '#FFFFFF',
        ink: '#1C1A17',
        'ink-soft': '#56504A',
        accent: '#C2410C',
        hairline: '#E7E1D8',
        band: {
          excellent: '#1B7A4B',
          good: '#5FA855',
          poor: '#E08A1E',
          bad: '#C0392B',
        },
      },
      fontFamily: {
        display: ['var(--font-display)', 'Georgia', 'serif'],
        body: ['var(--font-body)', 'system-ui', 'sans-serif'],
      },
      fontSize: {
        display: ['3rem', { lineHeight: '1.1' }],
        h1: ['1.75rem', { lineHeight: '1.2' }],
        h2: ['1.25rem', { lineHeight: '1.3' }],
        body: ['1rem', { lineHeight: '1.5' }],
        small: ['0.875rem', { lineHeight: '1.5' }],
        micro: ['0.75rem', { lineHeight: '1.4' }],
      },
      borderRadius: {
        card: '12px',
        pill: '999px',
      },
      maxWidth: {
        content: '720px',
      },
    },
  },
  plugins: [],
}

export default config
