# Runbook

---

## Local setup

Complete steps to get the project running from a fresh machine.

### Prerequisites

- **Node.js 18 or higher** — check with `node --version`. Install from https://nodejs.org or via a version manager (`nvm`, `fnm`, `volta`).
- **npm** — bundled with Node.js. Check with `npm --version`.
- **Git** — check with `git --version`.

No other tools, accounts, or environment variables are required.

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/Azqato/Cat-Food-Center.git
cd Cat-Food-Center

# 2. Install dependencies
npm install

# 3. Start the development server
npm run dev
```

The app is now running at **http://localhost:3000**.

Notes:
- The dev server does not apply the `/Cat-Food-Center` basePath used in production. Routes are available at `/`, not `/Cat-Food-Center/`.
- Hot reload is enabled — changes to `app/` and `components/` take effect immediately without restarting.

---

## Build

Produces a fully static site in the `out/` directory.

```bash
npm run build
```

The build uses `output: 'export'` in `next.config.ts`. Output:
- `out/` — static HTML, CSS, and JS files ready to serve
- `basePath: /Cat-Food-Center` and `assetPrefix: /Cat-Food-Center` are applied so asset paths work on GitHub Pages

To preview the production build locally:
```bash
# Serve out/ with any static server, e.g.:
npx serve out
# Then open http://localhost:3000
```

Note that `npm run start` is not used — it starts a Node server, which is incompatible with the static export.

---

## Deploy

### Automatic deploy (normal workflow)

Every push to the `main` branch triggers `.github/workflows/deploy.yml`, which:
1. Checks out the repo
2. Runs `npm ci` to install dependencies
3. Runs `npm run build` to produce `out/`
4. Uploads `out/` as a GitHub Pages artifact
5. Deploys to GitHub Pages

The live URL is: **https://azqato.github.io/Cat-Food-Center/**

Monitor the deploy at: `https://github.com/Azqato/Cat-Food-Center/actions`

### Manual deploy trigger

If you need to redeploy without a code change:
1. Go to `Actions` in the GitHub repo.
2. Select the **Deploy to GitHub Pages** workflow.
3. Click **Run workflow** → **Run workflow** (uses the `workflow_dispatch` trigger).

### One-time setup for a new fork

1. Fork or create the repository on GitHub.
2. Go to **Settings → Pages → Source** and select **GitHub Actions**.
3. Update `REPO` in `next.config.ts` to match the new repository name.
4. Push to `main`.

---

## Rollback

### Option 1: Revert the commit (recommended)

```bash
# Find the last good commit hash
git log --oneline -10

# Revert the bad commit (creates a new commit — safe for shared branches)
git revert <bad-commit-hash>
git push origin main
```

The revert push triggers a new deploy automatically.

### Option 2: Re-deploy a previous workflow run

1. Go to `Actions` → **Deploy to GitHub Pages**.
2. Find the last successful run before the bad deploy.
3. There is no native "re-deploy previous run" button — you must revert the code to redeploy the older build.

### Option 3: Force-push (use only in emergencies)

```bash
git reset --hard <last-good-commit>
git push --force origin main
```

Only use this if the commit cannot be reverted cleanly and the risk of losing history is acceptable. Confirm with the team before force-pushing.

---

## Environment configs

| Environment | URL | How deployed | Config differences |
|---|---|---|---|
| Local dev | http://localhost:3000 | `npm run dev` | No basePath applied; hot reload active; no static export |
| Production | https://azqato.github.io/Cat-Food-Center/ | GitHub Actions on push to `main` | `basePath: /Cat-Food-Center`, `assetPrefix: /Cat-Food-Center`, `output: 'export'` |

There is no staging environment. Test changes locally before pushing to `main`.

---

## Common errors

| Error | Likely cause | Fix |
|---|---|---|
| `Error: Image Optimization using the default loader is not compatible with next export` | A Next.js `<Image>` component was used without `unoptimized: true` | Add `unoptimized: true` to `images` in `next.config.ts`, or use a plain `<img>` tag |
| `useSearchParams() should be wrapped in a suspense boundary` | A component using `useSearchParams` is not inside a `<Suspense>` boundary | Wrap the component in `<Suspense>` in its parent page (see `app/search/page.tsx` for the pattern) |
| Assets return 404 on GitHub Pages | `basePath` or `assetPrefix` misconfigured | Check that both are set to `/Cat-Food-Center` in `next.config.ts`; check that `REPO` const matches the exact GitHub repo name |
| Fonts not loading | Google Fonts blocked or `next/font` config issue | Verify `Fraunces` and `Public_Sans` imports in `app/layout.tsx`; check browser network tab for font request errors |
| Deploy workflow fails at `npm run build` | TypeScript error or lint error introduced | Run `npm run lint` and `tsc --noEmit` locally to identify and fix before pushing |
| GitHub Pages shows old version | Deploy succeeded but CDN cache not cleared | Hard-refresh the browser (`Ctrl+Shift+R` / `Cmd+Shift+R`); GitHub Pages CDN typically clears within a few minutes |
| `Module not found` after `npm install` | Lockfile out of sync or Node version mismatch | Delete `node_modules` and `package-lock.json`, then run `npm install` again |

---

## Monitoring

| What to check | Where |
|---|---|
| Deploy status and build logs | https://github.com/Azqato/Cat-Food-Center/actions |
| GitHub Pages uptime and status | https://www.githubstatus.com |
| Core Web Vitals (Lighthouse) | Run `npx lighthouse https://azqato.github.io/Cat-Food-Center/ --view` locally, or use PageSpeed Insights |
| JavaScript errors in production | Browser DevTools console (no error reporting service configured in v1) |
| Dependency vulnerabilities | `npm audit` locally; Dependabot alerts on the GitHub repo |

There is no server-side logging, error tracking service (e.g. Sentry), or uptime monitor configured in v1. These are planned additions for M10 (public beta).
