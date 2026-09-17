# LTS Market — redesigned multilingual site

Static site using the original design in `css/main.css`, `css/nowe.css`,
`css/leasing.css` and `css/kontakt.css`. No framework or runtime translation.

## Pages

- Polish: `/`, `/nowe.html`, `/uzywane.html`, `/leasing.html`, `/kontakt.html`.
- English and Russian: the same routes under `/en/` and `/ru/`.
- Four pre-owned product pages per language under `uzywane/`, with the unique
  supplied photos, price, year (when supplied), condition and service information.
- Privacy information in all three languages.
- Language switches keep the current page/product. New-equipment home cards
  open the matching section on `nowe.html`. Blog links open the existing
  Laser Tech Service blog; there is no local blog in this checkout.

## Editing and checks

Edit the checked-in HTML pages directly and keep PL/EN/RU counterparts in sync.
Shared styles and scripts live in `css/` and `js/`. The template generators
mentioned in earlier documentation are not present in this checkout.

```sh
python3 scripts/audit-site.py
python3 scripts/check-seo.py
/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Helpers/jsc scripts/test-analytics.js
/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Helpers/jsc scripts/test-ui.js
python3 -m http.server 8000
```

The SEO check covers all 30 HTML pages, the shared GA4 loader, image paths and
sizes, three used-equipment ItemLists and 24 Product entries. The JavaScript
check covers immediate startup and protection against duplicate loading.
These checks do not replace Google Rich Results Test or GA4 Realtime verification.

GA4 uses `G-1Z98BZS3WW` through `js/analytics.js` on all 30 pages. Analytics
starts automatically on page load, without a consent dialog or footer settings.
The privacy information pages describe this behavior in PL, EN and RU.

Product prices match the displayed PLN prices. Starting prices and ranges use
AggregateOffer; availability, shipping, ratings and return policies are omitted
because they have not been confirmed. Used-product lists follow the visible card
order and link to the matching language's detail pages.

Images use compressed WebP, with 240 px gallery thumbnails and 640 px catalogue
variants. Large used-product photos are limited to 1920 px on the longest side.
The homepage uses WebP; the optimized JPEG remains available for social metadata.
Image width/height attributes match the files. Original photos can be recovered
from Git history if needed for print or larger exports.

Serve the repository at the domain root; URLs are root-relative and production
canonical URLs use `https://ltsmarket.pl`. Hosting does not require a build step.

## Existing integration boundaries

The contact forms have no configured sending backend. They validate input and
show a localized unavailable message; no successful delivery is claimed.
`js/kontakt.js` retains the empty `N8N_WEBHOOK_URL` configuration. The homepage
form has its separate existing integration placeholder in `js/main.js`.
A product enquiry fills in the selected model and pre-owned enquiry category.

Google Fonts and embedded maps connect to Google when their resources load.

The confirmed LTS Market address is `Rybacka 7, Wrocław`. Homepage and
contact text, embedded maps and structured data use this address in all three
languages.

No deployment was performed. Browser visual/mobile QA was unavailable in the
editing environment; the checks above do not substitute for a visual review.

See `SITE-AUDIT.md` for the latest inspection scope, fixes and verification limits.
