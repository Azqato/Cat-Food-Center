/* Shared Tailwind CDN theme for Cat Food Center.

   Must be loaded AFTER the Tailwind CDN script tag.

   The colour values are CSS variables rather than hex literals, so that
   `bg-surface`, `text-ink` and friends follow the theme chosen in
   cfc-theme.js without any dark: variants in the markup. The variables
   themselves are defined in cfc-tokens.css.

   One constraint this creates: Tailwind's opacity modifiers (`bg-surface/50`)
   cannot work on these colours, because Tailwind would have to rewrite the
   value into a colour-mix it cannot compute from a variable. Use a separate
   token instead of an opacity modifier. */
tailwind.config = {
  theme: {
    extend: {
      colors: {
        bg: 'var(--bg)', surface: 'var(--surface)',
        ink: 'var(--ink)', 'ink-soft': 'var(--ink-soft)',
        accent: 'var(--accent)', hairline: 'var(--hairline)',
        'band-excellent': 'var(--excellent)', 'band-good': 'var(--good)',
        'band-poor': 'var(--poor)', 'band-bad': 'var(--bad)',
        'on-accent': 'var(--on-accent)',
      },
    },
  },
}
