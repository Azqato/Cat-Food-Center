# Runbook

---

## Local setup

The site is static HTML, CSS, and vanilla JavaScript with no dependencies. See
[ADR-001](./ADR-001-static-first.md) for why.

### Prerequisites

- **Git** — check with `git --version`.
- **Python 3.8+** — check with `python --version`. Only needed to regenerate the
  Cat Care Guide pages or to run the contrast checker; not needed to view or
  edit the site.

There is no Node.js, no `npm install`, no lockfile, and no environment variables.

### Steps

```bash
git clone https://github.com/Azqato/Cat-Food-Center.git
cd Cat-Food-Center
python -m http.server 8000
```

The site is now at **http://localhost:8000**.

Notes:
- There is no basePath to worry about locally. Every link in the site is
  relative (`./learn.html`), which is what lets the same files work at the
  repository root locally and under `/Cat-Food-Center/` on GitHub Pages.
- There is no hot reload. Refresh the browser.
- Opening files via `file://` works for most pages but breaks two things:
  `fetch` of local JSON is blocked by CORS, and the barcode scanner needs a
  secure context. Use the server.

---

## Build

**There is no build step for deployment.** What is committed is what is served.

Two generators exist, and both run on a developer machine with their output
committed:

```bash
python tools/learn/build.py      # regenerates the eleven learn*.html pages
python tools/check-contrast.py   # audits both palettes against WCAG AA
```

`build.py` overwrites every `learn*.html`. Never hand-edit those files —
edit `tools/learn/c_<page>.py` and rerun. Run `check-contrast.py` after any
change to `assets/cfc-tokens.css`; it fails if a pair drops below AA, or if the
two duplicated dark-palette blocks have drifted apart.

---

## Deploy

### Automatic deploy (normal workflow)

Every push to the `main` branch triggers `.github/workflows/deploy.yml`, which:
1. Checks out the repo
2. Uploads the repository root as a GitHub Pages artifact
3. Deploys to GitHub Pages

There is no build. This is worth knowing during an incident: the deploy cannot
fail from a compile error, a lockfile conflict, or a dependency change, because
none of those exist. If a deploy fails, the cause is GitHub Pages itself or the
workflow configuration.

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
3. Push to `main`. Nothing needs configuring for the repository name — every path in the site is relative.

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
| Local dev | http://localhost:8000 | `python -m http.server 8000` | None — the same files, served from a different root |
| Production | https://azqato.github.io/Cat-Food-Center/ | GitHub Actions on push to `main` | None |

The two environments are configuration-identical, which is the main practical
benefit of having no build: a page that works locally works in production.

There is no staging environment. Test changes locally before pushing to `main`.

---

## Common errors

| Error | Likely cause | Fix |
|---|---|---|
| A `learn*.html` edit disappeared | Those files are generated; `tools/learn/build.py` overwrote it | Make the edit in `tools/learn/c_<page>.py` and rerun the generator |
| Assets return 404 on GitHub Pages | An absolute path (`/assets/...`) was used instead of a relative one | Use `./assets/...`. GitHub Pages serves this repo under `/Cat-Food-Center/`, so absolute paths resolve to the wrong root |
| A page flashes light before going dark | `cfc-theme.js` was moved out of `<head>`, or given `defer`/`async` | It must be a blocking `<script>` in `<head>`. That is the whole mechanism |
| Tailwind colour renders as transparent | An opacity modifier was used on a themed colour (`bg-surface/50`) | Tailwind cannot compute an opacity variant of a `var()`. Add a token to `cfc-tokens.css` instead |
| Contrast checker reports "dark blocks have drifted apart" | A token was changed in `:root[data-theme="dark"]` but not in the `prefers-color-scheme` block, or vice versa | Apply the change to both. The duplication is deliberate — see the comment at the top of `cfc-tokens.css` |
| Camera does not start on a phone | The page was opened over `http://<LAN-IP>`, which is not a secure context | Test against the deployed HTTPS URL or an HTTPS tunnel |
| `fetch` of a local JSON file fails with a CORS error | The page was opened with `file://` | Serve over `python -m http.server` |
| GitHub Pages shows an old version | Deploy succeeded but the CDN cache has not cleared | Hard-refresh (`Ctrl+Shift+R` / `Cmd+Shift+R`); the Pages CDN typically clears within a few minutes |

---

## Monitoring

| What to check | Where |
|---|---|
| Deploy status and build logs | https://github.com/Azqato/Cat-Food-Center/actions |
| GitHub Pages uptime and status | https://www.githubstatus.com |
| Core Web Vitals (Lighthouse) | Run `npx lighthouse https://azqato.github.io/Cat-Food-Center/ --view` locally, or use PageSpeed Insights |
| JavaScript errors in production | Browser DevTools console (no error reporting service configured in v1) |
| Dependency vulnerabilities | Not applicable — the site has no dependencies. The only third-party code is the Tailwind CDN script on four pages, pinned to nothing; replacing it with committed CSS is tracked for M12 |

There is no server-side logging, error tracking service (e.g. Sentry), or uptime monitor configured in v1. These are planned additions for M12 (public beta).
