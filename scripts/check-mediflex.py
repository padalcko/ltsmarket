#!/usr/bin/env python3
"""Check the MEDIflex addition, image mapping, schema and listing order."""
import json
import re
from pathlib import Path
from html.parser import HTMLParser
from PIL import Image
from importlib.machinery import SourceFileLoader

ROOT=Path(__file__).resolve().parents[1]
BASE='https://ltsmarket.pl'
class Tags(HTMLParser):
    def __init__(self, source):
        super().__init__();self.tags=[];self.feed(source)
    def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))

images=json.loads((ROOT/'scripts/mediflex-images.json').read_text())
assert [i['source'] for i in images]==[f'IMG_{n}.heic' for n in [7722,7728,7736,7737,7738,7739,7740,7741,7742,7743]]
folder=ROOT/'assets/img/uzywane/mediflex-us450'
assert len(list(folder.glob('*.webp')))==21
for item in images:
    for key,w,h in [('file','width','height'),('thumbnail','thumb_width','thumb_height')]:
        with Image.open(folder/item[key]) as image:
            assert image.size==(item[w],item[h]);assert image.width/image.height==9/16
    assert item['width']==1080 and item['height']==1920
for lang,pre in [('pl',''),('en','/en'),('ru','/ru')]:
    source=(ROOT/(pre.lstrip('/')+'/' if pre else '')/'uzywane/mediflex-us450.html').read_text()
    tags=Tags(source).tags
    assert '6000' not in source and '5000 W' in source
    assert sum(t=='h1' for t,a in tags)==1
    assert len({x['alt'][lang] for x in images})==10
    assert [a['data-image'].split('/')[-1] for t,a in tags if 'data-image' in a]==[i['file'] for i in images]
    for t,a in tags:
        if t=='img':
            with Image.open(ROOT/a['src'].lstrip('/')) as im:assert im.size==(int(a['width']),int(a['height']))
    schemas=[json.loads(x) for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>',source,re.S)]
    product=next(x for x in schemas if x['@type']=='Product')
    assert product['model']=='US450' and len(product['image'])==10
    assert product['offers']['price']==40000 and product['offers']['priceCurrency']=='PLN'
    assert product['offers']['availability']=='https://schema.org/InStock'
    assert product['itemCondition']=='https://schema.org/UsedCondition'
    assert not any(key in json.dumps(product).lower() for key in ['warranty','rating','review'])
    assert len(next(x for x in schemas if x['@type']=='BreadcrumbList')['itemListElement'])==3
    lts=[a for t,a in tags if t=='a' and a.get('href')=='https://lasertechservice.pl'+pre+'/']
    assert lts and all('nofollow' not in a.get('rel','') for a in lts)
    for filename in ['index.html','uzywane.html']:
        text=(ROOT/(pre.lstrip('/')+'/' if pre else '')/filename).read_text()
        if filename=='index.html':text=text.split('id="uzywane"')[1].split('</section>')[0]
        cards=[a['href'].split('/')[-1] for t,a in Tags(text).tags if t=='a' and 'product-card' in a.get('class','').split()]
        assert cards==[x+'.html' for x in ['mediflex-us450','3d-contour','medilase-pro','ellisys-plus','daeyang-carbo-3000']]
ai=SourceFileLoader('ai',str(ROOT/'scripts/build-ai-catalog.py')).load_module()
for name,content in ai.generate().items():assert (ROOT/name).read_text()==content
catalog=json.loads((ROOT/'ai-catalog.json').read_text())
assert len(catalog['products'])==15
for record in catalog['products']:
    if record['product']['model']=='US450':
        assert record['position']==1
        facts=record['verifiedFacts'];assert facts['maximumElectricalPowerConsumptionW']==5000
        assert facts['lastMaintenanceDate']=='2026-10-15' and facts['serviceWorkWarrantyMonths']==6
print('PASS: 3 MEDIflex pages, 6 first-position cards, 10 photos + 10 thumbnails + card, Product/Offer/Breadcrumb, 15 AI entries')
