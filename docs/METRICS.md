# Metrics

---

## North star metric

**Scan-to-verdict completions per week** — the number of times a user successfully reaches a product page with a score, whether via barcode scan or search. This is the single number that best represents whether Cat Food Center is delivering value: an owner got an answer.

---

## Acquisition metrics

| Metric | Description | Target | Timeframe | Tool |
|---|---|---|---|---|
| Weekly active users | Unique visitors per week | 500 WAU | 3 months post-launch | Google Analytics / Plausible |
| Organic search traffic | Sessions from search engines | 40% of total traffic | 6 months | Google Search Console |
| Direct / share traffic | Sessions from direct URL or shared links | 20% of total | 3 months | Analytics |
| PWA installs | "Add to home screen" events | 100 installs | 3 months | Web Vitals / beforeinstallprompt event |

---

## Engagement metrics

| Metric | Description | Target | Timeframe | Tool |
|---|---|---|---|---|
| Scan-to-verdict completions | Successful product page loads (core north star) | 1,000/week | 3 months | Analytics (product page views) |
| Scan success rate | Barcode scans that resolve to a product page (once scanner ships) | ≥ 90% | Post-scanner launch | Custom event tracking |
| Time to verdict | Median seconds from app open to product score visible | ≤ 30 s | Post-scanner launch | Custom timing event |
| Search-to-result rate | Searches that result in a product page click | ≥ 60% | 3 months | Analytics (search → product page funnel) |
| Product pages per session | Average pages viewed per visit | ≥ 1.5 | 3 months | Analytics |

---

## Retention metrics

| Metric | Description | Target | Timeframe | Tool |
|---|---|---|---|---|
| Week-1 retention | Users who return within 7 days of first visit | ≥ 20% | 3 months | Analytics cohort |
| Pre-purchase return visits | Users who visit 2+ times within a 2-week window | ≥ 15% of WAU | 6 months | Analytics (session patterns) |
| PWA session rate | Proportion of sessions that come from installed PWA | ≥ 10% of mobile sessions | 6 months | Analytics (standalone display mode) |

---

## Performance metrics

| Metric | Description | Target | Tool |
|---|---|---|---|
| Largest Contentful Paint (LCP) | Time for the main content to render | ≤ 2.5 s on a mid-range phone over 4G | Chrome UX Report / Lighthouse |
| First Input Delay (FID) / INP | Responsiveness to first interaction | ≤ 100 ms | Core Web Vitals |
| Cumulative Layout Shift (CLS) | Visual stability | ≤ 0.1 | Core Web Vitals |
| Pages uptime | GitHub Pages availability | ≥ 99.9% | GitHub status / updown.io |
| Successful builds | CI/CD build success rate | ≥ 99% | GitHub Actions |

---

## Catalog coverage metrics

| Metric | Description | Target | Timeframe | Tool |
|---|---|---|---|---|
| Top-100 SKU coverage | Percentage of the top 100 US cat food SKUs (by sales volume) in the catalog | ≥ 80% | 6 months | Manual audit vs. Nielsen/retail data |
| Submit queue processing | Submitted-but-unreviewed products waiting in the queue | ≤ 50 | Ongoing | Internal queue dashboard |

---

## Reporting cadence

| Metric group | Cadence | Owner |
|---|---|---|
| North star + engagement | Weekly | Product |
| Acquisition + retention | Monthly | Product |
| Performance (CWV) | Monthly (automated Lighthouse CI) | Engineering |
| Catalog coverage | Monthly | Editorial |
| Security / dependency audit | Quarterly | Engineering |
