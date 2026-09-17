"""Check site-wide analytics, structured data and local image references."""
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from html.parser import HTMLParser

class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.tags = []
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

pages = list(Path('.').rglob('*.html'))
products = catalogs = 0
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
    for data in schemas:
        items = [data] if data['@type'] == 'Product' else [x['item'] for x in data.get('itemListElement', []) if 'item' in x]
        for item in items:
            if item.get('@type') != 'Product':
                continue
            products += 1
            for field in ('@id', 'name', 'description', 'image', 'url', 'offers', 'itemCondition'):
                assert item.get(field), (path, field)
            assert item['offers'].get('price', item['offers'].get('lowPrice', 0)) > 0 and item['offers']['priceCurrency'] == 'PLN', path
            assert all(Path(url.removeprefix('https://ltsmarket.pl/')).is_file() for url in item['image']), path
        if path.name == 'uzywane.html' and data['@type'] == 'ItemList':
            catalogs += 1
            entries = data['itemListElement']
            assert data['numberOfItems'] == len(entries) == 4, path
            cards = re.findall(r'<a class="product-card" href="([^"]+)"', source)
            assert [x['url'] for x in entries] == ['https://ltsmarket.pl' + x for x in cards], path
            assert [x['position'] for x in entries] == [1, 2, 3, 4], path
assert catalogs == 3 and products == 24, (catalogs, products)
print(f'PASS: {len(pages)} HTML pages, GA4 coverage, 3 used ItemLists, 24 Products, image paths/dimensions')
