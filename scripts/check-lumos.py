#!/usr/bin/env python3
"""Validate Lumos author copy, SEO, links and strict unchanged-template boundaries."""
import importlib.util
import json
import re
import subprocess
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('lumos',ROOT/'scripts/build-lumos.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Text(HTMLParser):
    def __init__(self,s):super().__init__();self.parts=[];self.tags=[];self.feed(s)
    def handle_data(self,d):self.parts.append(d)
    def handle_starttag(self,t,a):self.tags.append((t,dict(a)))
def visible(s):return re.sub(r'\s+','',''.join(Text(s).parts))
data=json.loads((ROOT/'scripts/lumos-content.json').read_text())
for lang,route in m.ROUTES.items():
    path=ROOT/route.lstrip('/')/'index.html';source=path.read_text();tags=Text(source).tags
    text=visible(source)
    for block in data[lang]:
        for paragraph in block:
            if paragraph.startswith('https:'):continue
            assert visible(m.inline(m.plain(paragraph))) in text,(lang,paragraph)
    assert 'id="reading"' not in source
    assert source.count('<figure class="lumos-diagram">')==6
    assert sum(t=='h1' for t,a in tags)==1
    assert sum(t=='details' for t,a in tags)==13
    for id in ['technology','benefits','wavelengths','power','cooling','fac','neodez','software','audience','specification','gallery','service','purchase','faq','enquiry']:
        assert any(a.get('id')==id for t,a in tags),(lang,id)
    assert 'Alpha Mini' not in source and 'alpha-mini.webp' not in source
    assert not re.search(r'\b(?:alis|alvi|alibaba)\b',text,re.I)
    assert next(a['href'] for t,a in tags if a.get('rel')=='canonical')==m.BASE+route
    alts={a['hreflang']:a['href'] for t,a in tags if a.get('hreflang')}
    assert alts=={**{l:m.BASE+r for l,r in m.ROUTES.items()},'x-default':m.BASE+m.ROUTES['pl']}
    for t,a in tags:
        if t=='a' and a.get('lang') in m.ROUTES:assert a['href']==m.ROUTES[a['lang']]
    product=next(json.loads(x) for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>',source,re.S) if json.loads(x).get('@type')=='Product')
    assert product['offers']['lowPrice']==68000 and product['offers']['highPrice']==100000
    assert not any(k in json.dumps(product) for k in ['aggregateRating','review','availability','gtin','sku','warranty'])
    form=next(a for t,a in tags if t=='form')
    assert form['data-product-name']=='Lumos' and form['data-product-url']==m.BASE+route
    for t,a in tags:
        if t=='img':assert a.get('alt') and a.get('width') and a.get('height') and a.get('srcset')
    prefix='' if lang=='pl' else lang+'/'
    catalog=(ROOT/(prefix+'nowe.html')).read_text()
    card=re.search(r'<article[^>]+id="lumos">.*?</article>',catalog,re.S)[0]
    assert card.count('href="'+route+'"')==3
    # Every other catalogue card and all shared chrome remain byte-for-byte identical.
    old=subprocess.check_output(['git','show','HEAD:'+prefix+'nowe.html'],cwd=ROOT,text=True)
    strip=lambda s:re.sub(r'<article[^>]+id="lumos">.*?</article>','',s,flags=re.S)
    assert strip(catalog)==strip(old)
    original=(ROOT/m.alpha.ROUTES[lang].lstrip('/')/'index.html').read_text()
    for tag in ['header','footer']:
        chrome=re.search(fr'<{tag}\b.*?</{tag}>',original,re.S)[0]
        for l in m.ROUTES:chrome=chrome.replace(m.alpha.ROUTES[l],m.ROUTES[l])
        assert chrome==re.search(fr'<{tag}\b.*?</{tag}>',source,re.S)[0]
for path in ['nowe/alpha-mini/index.html','en/new/alpha-mini/index.html','ru/novye/alpha-mini/index.html','scripts/build-alpha-mini.py','scripts/alpha-mini-content.json','index.html','en/index.html','ru/index.html']+[str(p.relative_to(ROOT)) for d in ['css','js','en/js','ru/js'] for p in (ROOT/d).glob('*') if p.is_file() and p.name != 'lumos.css']:
    assert (ROOT/path).read_bytes()==subprocess.check_output(['git','show','HEAD:'+path],cwd=ROOT),path
print('PASS: Lumos original copy, 15 sections, 13 FAQs, schema, language links, images, form context; Alpha Mini, existing CSS, JS, homepages and non-Lumos catalogue content unchanged')
