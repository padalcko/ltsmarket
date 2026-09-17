# Site inspection — 2026-09-17

Scope: current working tree, all 30 PL/EN/RU HTML pages, shared and localized
JavaScript, CSS, image references, structured data, manifests and sitemap.

## Fixed

- Removed an extra closing `div` in the financing section of all three `nowe.html` pages.
- Removed JavaScript that replaced the homepage hero icons with older SVGs after load.
- Moved runtime-injected hero styles into shared CSS, preserving their geometry.
- Homepage phone validation now requires 7–15 digits after removing common formatting;
  punctuation alone no longer passes.
- Polish form fallback messages now provide the public email and phone instead of
  describing implementation work.

## Verified

- `python3 scripts/audit-site.py`: 30 pages, zero errors for explicit tag nesting,
  IDs, title/H1/main counts, description/viewport/canonical presence, local links,
  anchors, assets, reciprocal language links, sitemap coverage, manifest JSON and
  CSS brace balance.
- `python3 scripts/check-seo.py`: GA4 loader coverage, SVG structure, image references
  and positive dimensions, three used ItemLists, 24 Product entries.
- All site JavaScript files parsed in JavaScriptCore.
- `scripts/test-analytics.js`: automatic GA4 setup, no consent UI/storage dependency,
  duplicate-load protection.
- `scripts/test-ui.js`: menu open/Escape, language open/outside click in PL/EN/RU;
  gallery race handling, selected state, dimensions and retaining the displayed
  image until the next load succeeds. These are mocked behavior tests, not browser QA.
- No unreferenced image files found. `market-directions` remains removed.
- Local homepage returned HTTP 200. `git diff --check` passed.

## Remaining limitations

- Contact forms do not send enquiries: `N8N_WEBHOOK_URL` is empty and the homepage
  has no sending backend. No backend URL or credentials were provided. Public email
  and phone remain the working contact paths.
- No browser is available through the connected UI tool. Desktop/mobile layout,
  actual browser rendering, focus behavior and console/network activity were not
  visually verified. No Lighthouse results are claimed.
- GA4 Realtime/DebugView, Google Rich Results Test, Search Console, external links,
  production HTTP responses and email delivery were not verified.
- No deployment or commit was performed. Existing uncommitted work was preserved.
