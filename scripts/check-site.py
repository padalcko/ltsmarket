"""Dependency-free structural checks: python3 scripts/check-site.py."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json, re, collections, xml.etree.ElementTree as ET
ROOT = Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.tags = []
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs), self.getpos()[0]))
pages = {p: Page(p.read_text()) for p in ROOT.rglob('*.html') if p.name != 'favicon-head-snippet.html'}
errors = []
def check(ok, message):
    if not ok: errors.append(message)
def target(file, url):
    parsed = urlsplit(url)
    if parsed.scheme not in ('', 'http', 'https') or parsed.netloc not in ('', 'ltsmarket.pl'): return None, parsed
    result = file if not parsed.path else ((ROOT / parsed.path.lstrip('/')) if parsed.path.startswith('/') else file.parent / parsed.path).resolve()
    if result.is_dir(): result = result / 'index.html'
    return result, parsed
for file, page in pages.items():
    relative = file.relative_to(ROOT)
    text = file.read_text()
    tags = page.tags
    check(sum(t == 'title' for t,a,l in tags) == 1, f'{relative}: title')
    check(sum(t == 'h1' for t,a,l in tags) == 1, f'{relative}: H1')
    for name in ('description', 'viewport'):
        check(any(a.get('name') == name for t,a,l in tags), f'{relative}: {name}')
    check(any(a.get('charset') == 'UTF-8' for t,a,l in tags), f'{relative}: charset')
    if file.name != '404.html':check(any(a.get('rel') == 'canonical' for t,a,l in tags), f'{relative}: canonical')
    ids = [a['id'] for t,a,l in tags if 'id' in a]
    check(len(ids) == len(set(ids)), f'{relative}: duplicate IDs')
    check('gtag("config"' not in text and 'googletagmanager.com/gtag/js' not in text, f'{relative}: analytics bypasses consent')
    check(sum(a.get('src') == '/assets/js/privacy.js' for t,a,l in tags) == 1, f'{relative}: privacy script')
    for tag, attrs, line in tags:
        urls = [attrs[k] for k in ('src','href','data-image') if k in attrs]
        if 'srcset' in attrs: urls += [part.strip().split()[0] for part in attrs['srcset'].split(',')]
        for url in urls:
            dest, parsed = target(file, url)
            if dest is None:continue
            check(dest.exists(), f'{relative}:{line}: missing {url}')
            if parsed.fragment and dest in pages:
                check(any(a.get('id') == unquote(parsed.fragment) for t,a,l in pages[dest].tags), f'{relative}:{line}: broken anchor {url}')
        if tag == 'img':
            check(all(k in attrs for k in ('alt','width','height')), f'{relative}:{line}: image attributes')
        if 'aria-controls' in attrs:
            check(attrs['aria-controls'] in ids, f'{relative}:{line}: aria-controls target')
    for data in re.findall(r'<script type="application/ld\+json">(.*?)</script>',text,re.S):
        try:json.loads(data)
        except ValueError as e:errors.append(f'{relative}: JSON-LD {e}')
    if file.name == 'uzywane.html':
        check(text.count('class="used-product-card"') == 4, f'{relative}: static catalogue')
    if file.name == 'index.html':
        check(text.count('class="product-card"') >= 3, f'{relative}: static homepage products')
    if file.parent.name == 'uzywane':
        for script in ('main.js','produkt-uzywany.js'):
            check(any(a.get('src','').endswith('/'+script) for t,a,l in tags), f'{relative}: missing {script}')
    if file.name == 'kontakt.html':
        forms = [a for t,a,l in tags if t == 'form']
        check(len(forms) == 1 and forms[0].get('method') == 'post', f'{relative}: unsafe form fallback')
sitemap = ET.parse(ROOT / 'sitemap.xml')
for loc in sitemap.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
    dest,_ = target(ROOT/'index.html',loc.text)
    check(dest in pages, f'sitemap: {loc.text}')
if errors:
    print('\n'.join(errors))
    raise SystemExit(1)
print(f'PASS: {len(pages)} pages; metadata, local links, anchors, images, structured data, static catalogues and consent loading.')
