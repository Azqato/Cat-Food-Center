# Security

---

## Authentication model

Cat Food Center has no authentication in v1. There are no user accounts, no login flows, and no session management. The app is a fully static, read-only information tool. If user accounts are added in a future phase, this section will be updated with the authentication mechanism (e.g., OAuth provider, JWT lifetime, session storage strategy).

---

## Authorization model

There are no user roles in v1. All content is publicly readable. The concept of "authorization" does not apply until a backend and user accounts exist.

---

## Data storage

| Data type | Where stored | Protection |
|---|---|---|
| Product catalog | Open Pet Food Facts (external, read-only API) | No user data involved |
| Additive Knowledge Base | Bundled versioned JSON in the repository | Public; no sensitive content |
| Nutrient Reference | Bundled versioned JSON in the repository | Public; no sensitive content |
| Recently viewed products | Browser `localStorage` (client-side only) | Never leaves the device |
| Camera frames (barcode scanner) | Processed in-browser; never stored or uploaded | On-device only |
| User-submitted product data | Not implemented in v1 | N/A |

No personally identifiable information (PII) is collected or stored. There is no database.

---

## Environment variables

No secrets are hardcoded in the repository. The project has no API keys, tokens, or credentials of any kind in v1. The Open Pet Food Facts API is a public, unauthenticated API — no key required.

When API keys are introduced (e.g., analytics service, future data provider), they must be:
- Set as GitHub Actions secrets for CI/CD and as `NEXT_PUBLIC_*` environment variables (if client-exposed) or server-side only
- Never committed to the repository
- Documented here with their name, purpose, and required/optional status
- Rotated immediately if accidentally committed

---

## Third-party services

| Service | What data it receives | Purpose |
|---|---|---|
| Open Pet Food Facts (world.openpetfoodfacts.org) | Barcode number, search query string | Product catalog lookup |
| Google Fonts (fonts.googleapis.com) | Client IP, browser user-agent (standard font request) | Loading Fraunces and Public Sans |
| GitHub Pages (azqato.github.io) | Client IP, browser user-agent (standard web request) | Hosting the static site |

No user PII is sent to any third party. Open Pet Food Facts is accessed read-only and attributed per their terms. When analytics are added (planned in M10), the chosen tool (preference: Plausible, a privacy-first analytics provider with no PII collection) will be added to this table.

---

## Known attack surface

| Area | Risk | Mitigation |
|---|---|---|
| Open Pet Food Facts API responses | Malicious or malformed product data rendered in the UI | All rendered content is escaped by React's default JSX handling; external URLs (additive source links) use `rel="noopener noreferrer"` |
| External links | `target="_blank"` links could expose referrer info | All external `<a>` tags use `rel="noopener noreferrer"` |
| Barcode scanner (future) | QR codes / barcodes pointing to malicious URLs | Scanner reads EAN/UPC product codes only; decoded value is treated as a product barcode string, not as a URL to navigate to |
| Static file serving | GitHub Pages serves raw files; no server-side execution | No server-side code; attack surface is limited to the static HTML/JS/CSS files themselves |
| Dependency vulnerabilities | npm packages may have known CVEs | See dependency policy below |

---

## Dependency policy

- Dependencies are reviewed at the time of addition. New packages must be justified by a concrete feature need — no convenience packages.
- `npm audit` is run as part of the local development workflow. Any high-severity vulnerabilities block merging.
- A dependency audit is conducted quarterly (see `METRICS.md` reporting cadence).
- Dependabot alerts on the GitHub repository are monitored and addressed within 7 days for critical/high severity, 30 days for moderate.
- The project targets a minimal dependency footprint. Current production dependencies are limited to Next.js, React, and React DOM.
