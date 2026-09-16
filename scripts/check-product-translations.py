"""Check translation coverage, product parity, routes and reciprocal language links."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import json,re,xml.etree.ElementTree as ET
ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://ltsmarket.pl'
translations = json.loads((ROOT/'scripts/product-translations.json').read_text())
class Page(HTMLParser):
    def __init__(self,file):
        super().__init__()
        self.tags=[];self.text=[];self.script=False
        self.source=file.read_text();self.feed(self.source)
    def handle_starttag(self,t,a):
        a=dict(a);self.tags.append((t,a))
        if t=='script':self.script=True
        for key in ('alt','data-alt','aria-label'):
            if key in a:self.text.append(' '.join(a[key].split()))
        if t=='meta' and a.get('name') in ('description','twitter:description','twitter:title'):self.text.append(a.get('content',''))
    def handle_endtag(self,t):
        if t=='script':self.script=False
    def handle_data(self,s):
        if not self.script and s.strip():self.text.append(' '.join(s.split()))
    def product(self):
        for text in re.findall(r'<script type="application/ld\+json">(.*?)</script>',self.source,re.S):
            value=json.loads(text)
            if value.get('@type')=='Product':return value
    def alternates(self):return {a['hreflang']:a['href'] for t,a in self.tags if t=='link' and a.get('rel')=='alternate'}
    def images(self):return [a['src'].split('assets/')[-1] for t,a in self.tags if t=='img']
for file in sorted((ROOT/'uzywane').glob('*.html')):
    pl=Page(file);original=pl.product()
    expected={lang:f'{BASE}/{"" if lang=="pl" else lang+"/"}uzywane/{file.name}' for lang in ('pl','en','ru')}
    expected['x-default']=expected['pl']
    for lang in ('pl','en','ru'):
        page=pl if lang=='pl' else Page(ROOT/lang/'uzywane'/file.name)
        assert page.alternates()==expected,(file,lang,'alternates')
        assert page.images()==pl.images(),(file,lang,'images')
        data=page.product()
        for key in ('price','priceCurrency','availability','itemCondition'):
            assert data['offers'][key]==original['offers'][key],(file,lang,key)
        assert data['offers']['url']==expected[lang]
        assert any(t=='html' and a.get('lang')==lang for t,a in page.tags)
        assert any(t=='link' and a.get('rel')=='canonical' and a.get('href')==expected[lang] for t,a in page.tags)
        switchers=[a for t,a in page.tags if t=='a' and a.get('hreflang') in ('pl','en','ru')]
        assert len(switchers)==6,(file,lang,'desktop and mobile switchers')
        for a in switchers:
            assert a['href']==urlsplit(expected[a['hreflang']]).path
            assert ('active' in a.get('class','').split())==(a['hreflang']==lang)
        if lang=='pl':continue
        for text in page.text:
            assert text not in translations or translations[text][lang]==text,(file,lang,'untranslated',text)
        expected_contact=f'/{lang}/kontakt.html'
        assert any(t=='a' and a.get('href')==expected_contact for t,a in page.tags)
        assert any(t=='a' and a.get('href')==f'/{lang}/prywatnosc.html' for t,a in page.tags)
        assert len([1 for t,a in page.tags if t=='p'])==len([1 for t,a in pl.tags if t=='p']),(file,lang,'paragraph parity')
for lang in ('pl','en','ru'):
    prefix='' if lang=='pl' else lang+'/'
    for filename in ('index.html','uzywane.html'):
        page=Page(ROOT/prefix/filename)
        links=[a['href'] for t,a in page.tags if t=='a' and re.search(r'/uzywane/[^/]+\.html$',a.get('href',''))]
        assert links and all(href.startswith('/'+prefix+'uzywane/') for href in links),(lang,filename,'catalogue routes')
        assert 'Polish page' not in page.source and 'на польском' not in page.source
locs={node.text for node in ET.parse(ROOT/'sitemap.xml').findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
for file in (ROOT/'uzywane').glob('*.html'):
    for lang in ('pl','en','ru'):
        assert BASE+'/'+('' if lang=='pl' else lang+'/')+'uzywane/'+file.name in locs
print('PASS: 12 product pages; translated content, matching images and prices, canonical URLs, language switches, catalogue routes and sitemap.')
