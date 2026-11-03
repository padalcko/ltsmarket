#!/usr/bin/env python3
"""Check all supplied copy, product context, SEO and retained-template boundaries."""
import importlib.util
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from site_content import unlink_service_headings
from ai_resources import strip_integration

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('products', ROOT/'scripts/build-alpha-ray.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__(); self.parts=[]; self.tags=[]; self.feed(source)
    def handle_data(self, data): self.parts.append(data)
    def handle_starttag(self, tag, attrs): self.tags.append((tag,dict(attrs)))


def visible(source):
    return re.sub(r'\s+', '', ''.join(Page(source).parts))


def original(path):
    return subprocess.check_output(['git','show','HEAD:'+str(path)],cwd=ROOT)


data = json.loads((ROOT/'scripts/alpha-ray-content.json').read_text())
catalog = json.loads((ROOT/'ai-catalog.json').read_text())['products']
sitemap = ET.parse(ROOT/'sitemap.xml')
locs = [x.text for x in sitemap.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
assert len(locs)==len(set(locs))
paragraphs = 0
for product, translations in data.items():
    for lang, blocks in translations.items():
        route = m.route(lang,product); source = (ROOT/route.lstrip('/')/'index.html').read_text()
        main = re.search(r'<main\b.*?</main>',source,re.S)[0]
        text = visible(main); tags = Page(source).tags
        for block in blocks:
            for paragraph in block:
                if paragraph.startswith('https:'): continue
                assert visible(m.inline(m.plain(paragraph))) in text, (product,lang,paragraph)
                paragraphs += 1
        assert sum(t=='h1' for t,a in tags)==1
        assert sum(t=='details' for t,a in tags)==(10 if product=='alpha' else 11)
        assert not re.search(r'\b(?:alis|alvi|alibaba)\b',text,re.I)
        for unexpected in ['ICE Flow','NeoDez','755','808','940','1064']:
            assert unexpected not in main, (product,lang,unexpected)
        assert next(a['href'] for t,a in tags if a.get('rel')=='canonical')==m.BASE+route
        assert {a['hreflang']:a['href'] for t,a in tags if a.get('hreflang')}=={**{l:m.BASE+m.route(l,product) for l in m.PREFIXES},'x-default':m.BASE+m.route('pl',product)}
        for t,a in tags:
            if t=='a' and a.get('lang') in m.PREFIXES: assert a['href']==m.route(a['lang'],product)
            if t=='img':
                assert a.get('alt') and a.get('srcset') and a.get('width') and a.get('height')
                assert '/'+product in a['src']
                for candidate in a['srcset'].split(','):
                    assert (ROOT/candidate.strip().split()[0].lstrip('/')).is_file()
        schemas=[json.loads(x) for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>',source,re.S)]
        prod=next(x for x in schemas if x['@type']=='Product')
        assert prod['name']==product.title() and prod['url']==m.BASE+route
        assert prod['offers']['lowPrice' if product=='alpha' else 'price']==(60000 if product=='alpha' else 55000)
        assert not any(k in json.dumps(prod) for k in ['aggregateRating','review','availability','gtin','sku','warranty'])
        crumb=next(x for x in schemas if x['@type']=='BreadcrumbList')
        assert crumb['itemListElement'][-1]['item']==m.BASE+route
        form=next(a for t,a in tags if t=='form')
        assert form['data-product-name']==product.title() and form['data-product-url']==m.BASE+route
        assert m.BASE+route in locs
        entries=[x for x in catalog if x['product']['url']==m.BASE+route]
        assert len(entries)==1 and entries[0]['language']==lang
        assert m.BASE+route in (ROOT/'llms.txt').read_text()
        reference=(ROOT/m.lumos.ROUTES[lang].lstrip('/')/'index.html').read_text()
        for tag in ['header','footer']:
            chrome=re.search(fr'<{tag}\b.*?</{tag}>',reference,re.S)[0]
            for l in m.PREFIXES: chrome=chrome.replace(m.lumos.ROUTES[l],m.route(l,product))
            assert chrome==re.search(fr'<{tag}\b.*?</{tag}>',source,re.S)[0]
        print('PASS',product,lang,'copy, schema, metadata, links, images, form context, shared chrome')

# Only Alpha/Ray card markup and their structured URLs may change in the catalogue.
for lang in m.PREFIXES:
    path=Path(('' if lang=='pl' else lang+'/')+'nowe.html')
    current=strip_integration((ROOT/path).read_text()); before=strip_integration(original(path).decode())
    for product in data:
        card=re.search(r'<article[^>]+id="'+product+r'">.*?</article>',current,re.S)[0]
        assert card.count('href="'+m.route(lang,product)+'"')==3
        pattern=r'<article[^>]+id="'+product+r'">.*?</article>'
        current=re.sub(pattern,'',current,flags=re.S); before=re.sub(pattern,'',before,flags=re.S)
        before=before.replace(m.BASE+('' if lang=='pl' else '/'+lang)+'/nowe.html#'+product+'"',m.BASE+m.route(lang,product)+'"')
    assert current==before, path

protected=['index.html','en/index.html','ru/index.html','robots.txt','scripts/build-lumos.py','scripts/lumos-content.json','scripts/lumos_visuals.py','scripts/build-alpha-mini.py','scripts/alpha-mini-content.json']
for lang in m.PREFIXES:
    for product in ['lumos','alpha-mini']: protected.append(m.route(lang,product).lstrip('/')+'index.html')
for folder in ['css','js','en/js','ru/js']:
    protected += [str(p.relative_to(ROOT)) for p in (ROOT/folder).glob('*') if p.is_file()]
for path in protected:
    expected = original(path)
    if path.endswith('.html'):
        expected = unlink_service_headings(expected.decode()).encode()
    current = (ROOT/path).read_bytes()
    if path.endswith('.html'):
        current = strip_integration(current.decode()).encode()
        expected = strip_integration(expected.decode()).encode()
    assert current==expected,path
print(f'PASS: {paragraphs} supplied text blocks preserved; protected files unchanged except requested removal of service links from headings')
