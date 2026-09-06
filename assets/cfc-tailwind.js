/* Shared Tailwind CDN theme for Cat Food Center.
   Must be loaded AFTER the Tailwind CDN script tag. */
tailwind.config = {
  theme: {
    extend: {
      colors: {
        bg: '#FAF7F2', surface: '#FFFFFF',
        ink: '#1C1A17', 'ink-soft': '#56504A',
        accent: '#C2410C', hairline: '#E7E1D8',
        'band-excellent': '#1B7A4B', 'band-good': '#5FA855',
        'band-poor': '#E08A1E', 'band-bad': '#C0392B',
      },
    },
  },
}
