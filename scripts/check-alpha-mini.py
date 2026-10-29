#!/usr/bin/env python3
"""Check Alpha Mini content, SEO, source boundaries and integration contracts."""
import importlib.util
import json
import re
import subprocess
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
class Tags(HTMLParser):
    def __init__(self,s):super().__init__();self.tags=[];self.feed(s)
    def handle_starttag(self,t,a):self.tags.append((t,dict(a)))
routes={'pl':'/nowe/alpha-mini/','en':'/en/new/alpha-mini/','ru':'/ru/novye/alpha-mini/'}
data=json.loads((ROOT/'scripts/alpha-mini-content.json').read_text())
for lang,route in routes.items():
    source=(ROOT/route.lstrip('/')/'index.html').read_text(); tags=Tags(source).tags
    assert sum(t=='h1' for t,a in tags)==1
    assert sum(t=='details' for t,a in tags)==10
    for section in ['benefits','technology','cooling','handpiece','software','audience','specification','gallery','service','purchase','faq','enquiry','related']:
        assert any(a.get('id')==section for t,a in tags),section
    assert len(data[lang]['benefits'])==5 and len(data[lang]['audiences'])==3 and len(data[lang]['serviceCards'])==4
    assert data[lang]['heroSupport'] in source and data[lang]['reminder'] in source
    for paragraph in data[lang]['service']:assert paragraph in source
    imgs=[a for t,a in tags if t=='img'];assert len(imgs)==3 and len({i['src'] for i in imgs})==1
    assert imgs[0].get('fetchpriority')=='high' and 'loading' not in imgs[0]
    assert all(i.get('loading')=='lazy' for i in imgs[1:])
    for t,a in tags:
        if t=='a' and a.get('lang') in routes:assert a['href']==routes[a['lang']]
    product=next(json.loads(x) for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>',source,re.S) if json.loads(x).get('@type')=='Product')
    assert product['offers']['lowPrice']==40000 and product['offers']['priceCurrency']=='PLN'
    assert 'availability' not in product['offers'] and 'aggregateRating' not in product and 'review' not in product
    form=next(a for t,a in tags if t=='form');assert form['data-product-name']=='Alpha Mini' and form['data-product-url']=='https://ltsmarket.pl'+route
    prefix='' if lang=='pl' else lang+'/'
    assert f'<script src="/{prefix}js/kontakt.js" defer>' in source and '/js/lead-api.js' in source
    # Existing catalogue/home changes are limited to Alpha Mini linking.
    for file in ['index.html','nowe.html']:
        path=prefix+file;old=subprocess.check_output(['git','show','HEAD:'+path],cwd=ROOT,text=True);new=(ROOT/path).read_text()
        if file=='index.html':assert new==old.replace('/'+prefix+'nowe.html#alpha-mini',route)
        else:
            strip=lambda x:re.sub(r'<article class="nowe-product" id="alpha-mini">.*?</article>','',x,flags=re.S).replace('/'+prefix+'nowe.html#alpha-mini',route)
            assert strip(new)==strip(old)
assert 'Allow: /' in (ROOT/'robots.txt').read_text()
assert (ROOT/'assets/img/nowe/alpha-mini.webp').stat().st_size==76162
print('PASS: Alpha Mini PL/EN/RU sections, localized service copy, photos, schema, forms, catalogue edit boundaries')
