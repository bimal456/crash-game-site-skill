# Deploy to Cloudflare Pages (what actually worked)

## Before deploy
- Confirm the account that holds the domain zone (the owner gives the dashboard link). Never assume the account from another site.
- Build two zips:
  - `<site>-SITE-upload.zip`: the CONTENTS of `dist/` at the zip root (index.html, _headers, _redirects, robots.txt, sitemap.xml, 404.html, assets/, edition folders). Nothing else.
  - `<site>-FINAL.zip`: `site/` + `source/` + README for the owner. Send only this one to the owner as "the" deliverable. Never deploy it.

## Lesson: wrong folder = broken site + public source
Uploading the whole unzipped package put the site under `/chickenroad-radio-am/site/`: root 404, CSS and absolute links broken, `_headers`/`_redirects` ignored, and `source/` (content, research, tracking link) publicly readable. Always deploy the SITE zip with index.html at its root. A new production deployment replaces the old files; verify old paths 404 with a cache-buster.

## Steps (dashboard)
1. Workers & Pages > use the legacy Pages flow ("Continue to Pages") > Drag and drop your files > project name (e.g. `chickenroad-radio-am`) > Create project. Do NOT use the new "Upload your static files" Worker flow (it creates a random Worker name and failed).
2. Project > Create deployment > Production > upload the SITE zip (file input accepts .zip) > wait for "N/N files uploaded" > the owner clicks **Save and deploy** (or Claude, if he asks).
3. Custom domains > Set up a custom domain > `<domain>` > Continue > owner clicks **Activate domain**. Cloudflare creates `CNAME <domain> -> <project>.pages.dev` (proxied) when the zone is in the same account. Status goes Verifying -> Active in a few minutes.
4. Zone > SSL/TLS > Edge Certificates > **Always Use HTTPS** on (HSTS is already sent by `_headers`; no need for the zone HSTS button).

## Known problem: dashboard upload blocked
On some networks/browser sessions Cloudflare's own WAF blocks the dashboard asset calls (`/api/v4/pages/assets/check-missing` returns a 403 "Sorry, you have been blocked" page; the Workers flow returns 401). Symptoms: upload stuck at "2/126 files", "Failed to upload". It is not the files. Fix: switch network (mobile hotspot / no VPN), try again later, or use another browser; Wrangler from the owner's own terminal with his own API token also bypasses it. Do not try to extract tokens from the dashboard.

## Live readback (always, after every deploy)
- Deployment list shows the new production deployment as success.
- Every page of every edition returns 200 (fetch with `cache: 'no-store'`), unknown path returns the real 404 page, `http://` redirects to `https://`, `/play` returns a redirect, `/login` (if old) redirects.
- Headers: CSP, HSTS, X-Robots-Tag on /play, none on normal pages.
- Banned-word scan on live HTML (strip scripts/tags first; `preview` contains "review").
- Byte comparison against the build: expected differences only (Cloudflare injects a script tag on pages; Email Address Obfuscation rewrites pages that contain an email address; the mailto still works).
- If the container cannot reach the domain (egress allowlist), do the readback in the browser.
