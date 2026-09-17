# LTS Market — redesigned multilingual site

Static site using the original design in `css/main.css`, `css/nowe.css`,
`css/leasing.css` and `css/kontakt.css`. No framework or runtime translation.

## Pages

- Polish: `/`, `/nowe.html`, `/uzywane.html`, `/leasing.html`, `/kontakt.html`.
- English and Russian: the same routes under `/en/` and `/ru/`.
- Four pre-owned product pages per language under `uzywane/`, with all 33
  supplied photos, price, year (when supplied), condition and service information.
- Privacy information in all three languages.
- Language switches keep the current page/product. New-equipment home cards
  open the matching section on `nowe.html`. Blog links open the existing
  Laser Tech Service blog; there is no local blog in this checkout.

## Editing and rebuilding

The four original Polish page templates are in `scripts/templates/*.html.in`.
The shared header and footer live in `scripts/templates/header.html.in` and
`scripts/templates/footer.html.in`; all pages use these same components.
Edit those templates rather than their generated HTML copies. Shared styles
and Polish JavaScript remain in `css/` and `js/`.

- `scripts/translations.json`: EN/RU translations of the existing pages and live JS messages.
- `scripts/used-products.json`: catalogue data, retrieved on 2026-09-17 from
  https://github.com/padalcko/ltsmarket/blob/main/assets/js/used-products.js.
  Prices and condition are the source listing's claims; confirm availability with the seller.
- `scripts/build-icons.py`: matching font-independent SVG, ICO and PNG icons; no dependencies.
- `scripts/build-site.py`: new catalogue/detail markup, its translations,
  metadata, manifests and sitemap. Uses Python's standard library only.

```sh
python3 scripts/build-icons.py
python3 scripts/build-site.py
python3 scripts/check-site.py
python3 -m http.server 8000
```

Open `http://localhost:8000/`. Serve the repository at the domain root; URLs
are root-relative. Production canonical URLs currently use `https://ltsmarket.pl`.
Change `BASE` in the generator when deploying to a different canonical domain.
All generated files are included; hosting does not need Python or a build step.

`site.webmanifest`, language-specific manifests, favicon, Apple touch icon,
192/512 px app icons, `robots.txt` and `sitemap.xml` are included.

## Behavior checks

On macOS, from the repository root:

```sh
/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Helpers/jsc scripts/test-behavior.js
```

Checks cover consent/revocation, unavailable storage, gallery load races,
retaining the current image on a failed load, and separate form handlers.
Structural checks cover all 30 pages, assets, anchors, language counterparts,
metadata, product JSON-LD, manifests and sitemap coverage.
Rebuilding twice produces identical files.

## Existing integration boundaries

The contact forms have no configured sending backend. They validate input and
show a localized unavailable message; no successful delivery is claimed.
`js/kontakt.js` retains the empty `N8N_WEBHOOK_URL` configuration. The homepage
form has its separate existing integration placeholder in `js/main.js`.
A product enquiry fills in the selected model and pre-owned enquiry category.

Analytics is disabled until enabled through the existing footer privacy button.
The choice is stored locally. Revocation disables subsequent analytics; it does
not delete data already sent. Google Fonts and embedded maps still connect to
Google when their resources load.

The confirmed LTS Market address is `Rybacka 7, Wrocław`. Homepage and
contact text, embedded maps and structured data use this address in all three
languages.

No deployment was performed. Browser visual/mobile QA was unavailable in the
editing environment; the checks above do not substitute for a visual review.
