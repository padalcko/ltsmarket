"""Rebuild sitemap from indexable canonical pages and their language alternates."""
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
import xml.etree.ElementTree as ET
ROOT = Path(__file__).resolve().parents[1]
NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'
XHTML = 'http://www.w3.org/1999/xhtml'
class Head(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonical = None
        self.alternates = []
        self.noindex = False
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'link' and attrs.get('rel') == 'canonical': self.canonical = attrs['href']
        if tag == 'link' and attrs.get('rel') == 'alternate' and attrs.get('hreflang'): self.alternates.append((attrs['hreflang'],attrs['href']))
        if tag == 'meta' and attrs.get('name') == 'robots' and 'noindex' in attrs.get('content',''): self.noindex = True
pages = []
for file in ROOT.rglob('*.html'):
    page = Head()
    page.feed(file.read_text())
    if page.canonical and not page.noindex: pages.append((page,file))
urls = {page.canonical for page,file in pages}
assert len(urls) == len(pages), 'Duplicate canonical URL'
ET.register_namespace('',NS)
ET.register_namespace('xhtml',XHTML)
root = ET.Element(f'{{{NS}}}urlset')
for page,file in sorted(pages,key=lambda item:item[0].canonical):
    node = ET.SubElement(root,f'{{{NS}}}url')
    ET.SubElement(node,f'{{{NS}}}loc').text = page.canonical
    ET.SubElement(node,f'{{{NS}}}lastmod').text = date.fromtimestamp(file.stat().st_mtime).isoformat()
    for lang,url in page.alternates:
        assert url in urls, f'Alternate target missing: {url}'
        ET.SubElement(node,f'{{{XHTML}}}link',{'rel':'alternate','hreflang':lang,'href':url})
ET.indent(root,space='  ')
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n'+ET.tostring(root,encoding='unicode')+'\n')
print(f'Sitemap: {len(pages)} canonical pages')
