"""Check site-wide analytics, structured data and local image references."""
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from html.parser import HTMLParser
from ai_resources import Parser
from product_schema import STATUSES, POLICIES, normalize_html

class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.tags = []
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

# Search Console ownership tokens are not content pages.
pages = [p for p in Path('.').rglob('*.html') if p.read_text().strip() != 'google-site-verification: ' + p.name]
products = catalogs = 0
product_pages = {}
catalog_products = []
languages = {"pl": 0, "ru": 0, "en": 0}
for path in pages:
    source = path.read_text()
    for svg in re.findall(r"<svg\b.*?</svg>", source, re.S):
        icon = ET.fromstring(svg)
        assert "viewBox" in icon.attrib, path
        for shape in icon.iter():
            if shape.tag.split("}")[-1] in {"path", "rect", "circle", "line", "polyline", "polygon", "ellipse"}:
                assert len(shape) == 0, (path, "Nested SVG shapes")
    tags = Page(source).tags
    assert sum(tag == 'script' and attrs.get('src') == '/js/analytics.js' for tag, attrs in tags) == 1, path
    assert 'privacy-settings' not in source and '/js/privacy.js' not in source, path
    for tag, attrs in tags:
        if tag == 'img':
            assert Path(attrs['src'].lstrip('/')).is_file(), (path, attrs)
            assert int(attrs['width']) > 0 and int(attrs['height']) > 0, path
    schemas = [json.loads(x) for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>', source, re.S)]
    standalone = [x for x in schemas if x.get('@type') == 'Product']
    assert len(standalone) <= 1, (path, 'Duplicate Product schemas')
    assert normalize_html(source) == source, (path, 'Schema generation is not idempotent')
    if standalone:
        product = standalone[0]
        lang = 'en' if path.parts[0] == 'en' else 'ru' if path.parts[0] == 'ru' else 'pl'
        languages[lang] += 1
        product_pages[product['url']] = product
        price_nodes = [n for n in Parser(source).root.all()
                       if n.has('alpha-price') or n.has('nowe-product__price')]
        amounts = [int(x.replace(' ', '').replace(',', '').replace('\u00a0', ''))
                   for n in price_nodes for x in re.findall(r'\d[\d ,\u00a0]*', n.text())]
        assert product['offers']['price'] in amounts, (path, 'Visible price mismatch', amounts)
        assert all('PLN' in n.text() or 'zł' in n.text() for n in price_nodes), path
    for data in schemas:
        items = [data] if data['@type'] == 'Product' else [x['item'] for x in data.get('itemListElement', []) if 'item' in x]
        for item in items:
            if not isinstance(item, dict) or item.get('@type') != 'Product':
                continue
            products += 1
            if data['@type'] != 'Product':
                catalog_products.append(item)
            offer = item['offers']
            expected = STATUSES['used' if item['itemCondition'].endswith('UsedCondition') else 'new']
            assert offer['@type'] == 'Offer', (path, offer)
            assert offer['availability'] == expected['availability'], path
            assert offer['itemCondition'] == expected['itemCondition'], path
            assert not any(k in offer for k in ('lowPrice', 'highPrice', 'offerCount')), path
            assert not any(k in item for k in ('aggregateRating', 'review')), path
            policy = offer['seller']['hasMerchantReturnPolicy']
            assert policy['@type'] == 'MerchantReturnPolicy', path
            assert policy['merchantReturnLink'] in ['https://ltsmarket.pl'+p for p in POLICIES.values()], path
            for field in ('@id', 'name', 'description', 'image', 'url', 'offers', 'itemCondition'):
                assert item.get(field), (path, field)
            assert item['offers'].get('price', item['offers'].get('lowPrice', 0)) > 0 and item['offers']['priceCurrency'] == 'PLN', path
            assert all(Path(url.removeprefix('https://ltsmarket.pl/')).is_file() for url in item['image']), path
        if path.name == 'uzywane.html' and data['@type'] == 'ItemList':
            catalogs += 1
            entries = data['itemListElement']
            assert data['numberOfItems'] == len(entries) == 5, path
            cards = re.findall(r'<a class="product-card" href="([^"]+)"', source)
            assert [x['url'] for x in entries] == ['https://ltsmarket.pl' + x for x in cards], path
            assert [x['position'] for x in entries] == [1, 2, 3, 4, 5], path
assert catalogs == 3 and products == 39, (catalogs, products)
assert len(product_pages) == 27 and languages == {'pl': 9, 'ru': 9, 'en': 9}, languages
for item in catalog_products:
    detail = product_pages[item['url']]
    for field in ('price', 'priceCurrency', 'availability', 'itemCondition'):
        assert item['offers'][field] == detail['offers'][field], (item['url'], field)
print('PASS: 9 models, 27 product pages, PL/RU/EN parity, visible prices, unique Product schemas and idempotence')
print(f'PASS: {len(pages)} HTML pages, GA4 coverage, 3 used ItemLists, 39 Products, image paths/dimensions')
