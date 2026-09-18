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
  open the matching section on `nowe.html`. Market blog links open the local
  PL/EN/RU blog. The separately labelled Laser Tech Service blog link remains external.

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

The SEO check covers all 39 HTML pages, the shared GA4 loader, image paths and
sizes, three used-equipment ItemLists and 24 Product entries. The JavaScript
check covers immediate startup and protection against duplicate loading.
These checks do not replace Google Rich Results Test or GA4 Realtime verification.

GA4 uses `G-1Z98BZS3WW` through `js/analytics.js` on all 39 pages. Analytics
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

## Blog: editing and publishing

The blog has a listing and two articles in Polish, English and Russian:

- `/blog/depilacja-laserowa-jako-biznes/`
- `/en/blog/laser-hair-removal-business/`
- `/ru/blog/lazernaya-epilyaciya-kak-biznes/`
- `/blog/modelowanie-sylwetki-kawitacja-rf/`
- `/en/blog/body-contouring-cavitation-rf/`
- `/ru/blog/modelirovanie-figury-kavitaciya-rf/`

1. Edit `scripts/blog-posts.json`: `site` holds shared labels and `posts` contains
   articles with matching `pl`, `en` and `ru` editions. Append another complete
   article to `posts` to add it to all listings and the sitemap. Paragraphs support
   HTML links; `{prefix}` resolves to the current language root. Optional `image`,
   `image_alt`, `image_width` and `image_height` fields supply images inside articles only
   and article social metadata. Blog cards contain no images. Keep existing slugs stable.
2. Run `python3 scripts/build-blog.py`. It generates the nine static blog pages,
   using each language's current leasing-page header/footer, and updates the sitemap
   and generic Market blog navigation. Do not hand-edit generated blog HTML.
3. Run `python3 scripts/audit-site.py` and `python3 scripts/check-seo.py`.
4. Preview with `python3 -m http.server 8000`. Check `/blog/`, `/en/blog/` and
   `/ru/blog/`, including mobile menus, article language switches and contact links.
5. Publish the generated HTML, `css/blog.css`, updated navigation pages and
   `sitemap.xml` together through the site's usual hosting workflow. No server-side
   build is required. The generator and JSON source should remain in the repository.
6. After deployment, verify the nine public URLs and sitemap on `ltsmarket.pl`.

The first article includes catalogue, leasing, service and contact links. Blog pages
have canonical URLs, reciprocal hreflang, social metadata, Blog/BlogPosting and
BreadcrumbList structured data. Publication dates are omitted until confirmed.
This change has not been committed or deployed. Browser visual QA could not run
because no browser was available; static checks are not a visual review.

The cavitation/RF article uses the supplied `assets/img/blog/rf-article.webp`
(1080 × 1080) without altering it. Each edition links to an FDA overview for
general technology context; this is not a product-specific approval claim.
