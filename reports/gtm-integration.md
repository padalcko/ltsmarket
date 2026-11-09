# GTM integration — 2026-11-09

## Implementation and audit

Static HTML site, no SSR or shared runtime layout. Central build step:
`scripts/build-gtm.py`, invoked first by `scripts/build-site.py`. Standard async
snippet immediately after `<head>`; noscript immediately after `<body>` with an
additional iframe title required by the accessibility audit. Content generators
inherit the installed snippets; the final build normalizes them idempotently.

Coverage: PL 20, EN 20, RU 20, plus shared 404 (Polish default). Search Console
verification file is not a page and stays unchanged. Every HTML diff was compared
against HEAD: only the shared GTM insertion differs. Header/footer, navigation,
forms, WhatsApp, SEO metadata, JSON-LD, sitemap, robots, CSS and existing JS remain
unchanged. All 91 telephone anchors already use `tel:+48575254431`.

Existing tags: only GA4 G-1Z98BZS3WW in js/analytics.js, guarded against repeated
initialization. Contact handlers send the existing generate_lead event. No prior
GTM, Ads ID, phone_click handler, analytics consent UI or Consent Mode found.
Form consent is unrelated to analytics. No repository CSP was found; production
headers were not checked. Consent behavior remains immediate loading, as before.

The public GTM-T9T228H6 script was fetched successfully. Its resource version is 1,
with empty tags, predicates and rules. This snapshot can change after publication.
It adds no GA4 page_view tag at this time. Never add a second automatic Google tag
configuration/page_view for the existing measurement ID without coordinating a
migration of the original loader. Do not duplicate the existing generate_lead.

## Validation

- PASS build-site: 61 HTML pages, audit (0 errors), SEO, AI resources.
- PASS build-gtm --check, repeated build idempotency and 91 telephone links.
- PASS analytics startup/duplicate guard, UI tests, six localized form tests.
- PASS AI search/catalog freshness; Alpha Mini and Lumos freshness.
- PASS git diff --check; HTML changes limited exactly to GTM snippets.
- PASS Chrome mobile viewport 390x844 on home, new, used, leasing, contact and
  blog in all three languages (18 routes): single GTM request/start, single
  existing GA4 config, tel click target, no JavaScript exceptions. Google scripts
  mocked; this verifies site integration, not real GA4 delivery or container code.
  Reproducible test: scripts/check-gtm-browser.cjs, using PLAYWRIGHT_MODULE,
  CHROME_PATH and TEST_BASE_URL if needed. No production leads/events sent.
- Alpha/Ray --check reports six stale pages; reproduced using the original HEAD
  source HTML, so this predates the GTM change. Unrelated pages not regenerated.
- No package.json or separate lint task. No physical-phone dialer test, Tag
  Assistant session, real GA4 page_view capture, production consent check or
  measured CWV comparison. Async loading preserves rendering flow but does not
  prove unchanged field performance; future GTM tags affect performance.

## Later manual configuration (not performed)

1. In GTM enable Click URL and create a Just Links trigger with Click URL starts
   with tel:. Keep one phone trigger/event path.
2. Configure GA4 Event phone_click for the existing measurement ID; avoid a new
   automatic page_view/configuration alongside the site's existing GA4 loader.
3. Use Preview/Tag Assistant after deployment on PL/EN/RU: one container, one
   page_view per load, one phone_click per click; inspect consent state and errors.
4. Verify GA4 DebugView/Realtime, then publish the GTM changes and mark phone_click
   as a key event if desired. A click measures intent, not a completed phone call.
5. If an analytics consent mechanism is introduced, coordinate both the direct
   GA4 loader and GTM, including the no-JavaScript fallback.

No commit, push or deploy. GA4 phone events are not configured or verified.

## Changed files

- `404.html`
- `README.md`
- `blog/bezpieczne-usuwanie-tatuazu-laser-nd-yag/index.html`
- `blog/depilacja-laserowa-jako-biznes/index.html`
- `blog/index.html`
- `blog/lumos-nowoczesny-laser-diodowy-dla-salonu/index.html`
- `blog/modelowanie-sylwetki-kawitacja-rf/index.html`
- `en/blog/body-contouring-cavitation-rf/index.html`
- `en/blog/index.html`
- `en/blog/laser-hair-removal-business/index.html`
- `en/blog/lumos-modern-diode-laser-for-salons/index.html`
- `en/blog/safe-tattoo-removal-nd-yag-laser/index.html`
- `en/index.html`
- `en/kontakt.html`
- `en/leasing.html`
- `en/new/alpha-mini/index.html`
- `en/new/alpha/index.html`
- `en/new/lumos/index.html`
- `en/new/ray/index.html`
- `en/nowe.html`
- `en/polityka-prywatnosci.html`
- `en/uzywane.html`
- `en/uzywane/3d-contour.html`
- `en/uzywane/daeyang-carbo-3000.html`
- `en/uzywane/ellisys-plus.html`
- `en/uzywane/mediflex-us450.html`
- `en/uzywane/medilase-pro.html`
- `index.html`
- `kontakt.html`
- `leasing.html`
- `nowe.html`
- `nowe/alpha-mini/index.html`
- `nowe/alpha/index.html`
- `nowe/lumos/index.html`
- `nowe/ray/index.html`
- `polityka-prywatnosci.html`
- `reports/gtm-integration.md`
- `ru/blog/bezopasnoe-udalenie-tatu-lazer-nd-yag/index.html`
- `ru/blog/index.html`
- `ru/blog/lazernaya-epilyaciya-kak-biznes/index.html`
- `ru/blog/lumos-sovremennyy-diodnyy-lazer-dlya-salona/index.html`
- `ru/blog/modelirovanie-figury-kavitaciya-rf/index.html`
- `ru/index.html`
- `ru/kontakt.html`
- `ru/leasing.html`
- `ru/novye/alpha-mini/index.html`
- `ru/novye/alpha/index.html`
- `ru/novye/lumos/index.html`
- `ru/novye/ray/index.html`
- `ru/nowe.html`
- `ru/polityka-prywatnosci.html`
- `ru/uzywane.html`
- `ru/uzywane/3d-contour.html`
- `ru/uzywane/daeyang-carbo-3000.html`
- `ru/uzywane/ellisys-plus.html`
- `ru/uzywane/mediflex-us450.html`
- `ru/uzywane/medilase-pro.html`
- `scripts/build-gtm.py`
- `scripts/build-site.py`
- `scripts/check-gtm-browser.cjs`
- `uzywane.html`
- `uzywane/3d-contour.html`
- `uzywane/daeyang-carbo-3000.html`
- `uzywane/ellisys-plus.html`
- `uzywane/mediflex-us450.html`
- `uzywane/medilase-pro.html`
