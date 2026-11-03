"""AI representations of canonical Market HTML, following Laser Tech Service's approach.

Standard library only. Sitemap discovers routes; HTML supplies content and metadata.
"""
import json
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://ltsmarket.pl'
LANGUAGES = {'pl':'Polski', 'en':'English', 'ru':'Русский'}
BEGIN, END = '<!-- AI resources: generated -->', '<!-- /AI resources -->'
VOID = set('area base br col embed hr img input link meta param source track wbr'.split())
SKIP = set('script style nav footer noscript form input select textarea button svg iframe'.split())
SCHEMA = re.compile(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', re.S)


class Node:
    def __init__(self, tag='', attrs=(), parent=None, data=''):
        self.tag, self.attrs, self.parent, self.data = tag, dict(attrs), parent, data
        self.children = []

    def all(self, tag=None):
        for child in self.children:
            if tag is None or child.tag == tag:
                yield child
            yield from child.all(tag)

    def text(self):
        return re.sub(r'\s+', ' ', self.raw()).strip()

    def raw(self):
        return self.data + ''.join(c.raw() for c in self.children)

    def has(self, cls):
        return cls in self.attrs.get('class', '').split()


class Parser(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.root = Node(); self.current = self.root
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.current)
        self.current.children.append(node)
        if tag not in VOID:
            self.current = node

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        node = self.current
        while node.parent:
            if node.tag == tag:
                self.current = node.parent
                return
            node = node.parent

    def handle_data(self, data):
        self.current.children.append(Node(parent=self.current, data=data))


def markdown_url(canonical):
    return canonical + 'index.md' if canonical.endswith('/') else canonical.removesuffix('.html') + '.md'


def strip_integration(source):
    return re.sub(re.escape(BEGIN)+r'.*?'+re.escape(END)+r'\n?', '', source, flags=re.S)


def integration(source):
    source = strip_integration(source)
    canonical = re.search(r'<link rel="canonical" href="([^"]+)"', source)
    if not canonical or not canonical[1].startswith(BASE+'/'):
        return source
    block = BEGIN+'\n'
    block += f'    <link rel="alternate" type="text/markdown" href="{markdown_url(canonical[1])}">\n'
    block += '    <link rel="describedby" href="/llms.txt">\n'+END+'\n'
    return source.replace('</head>', block+'</head>', 1)


def discover():
    ns = {'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = [x.text for x in ET.parse(ROOT/'sitemap.xml').findall('s:url/s:loc',ns)]
    assert len(urls)==len(set(urls)), 'Duplicate sitemap URL'
    pages = []
    for url in sorted(urls):
        assert url.startswith(BASE+'/') and (url.endswith('/') or url.endswith('.html')), url
        path = ROOT/urlsplit(url).path.lstrip('/')
        if url.endswith('/'): path = path/'index.html'
        source = path.read_text()
        tree = Parser(source).root; tags = list(tree.all())
        canonical = [n.attrs.get('href') for n in tags if n.tag=='link' and n.attrs.get('rel')=='canonical']
        assert canonical == [url], (path,canonical)
        meta = {n.attrs.get('name',n.attrs.get('property')):n.attrs.get('content','') for n in tags if n.tag=='meta'}
        assert 'noindex' not in meta.get('robots','').lower(), path
        lang = next(n.attrs['lang'] for n in tags if n.tag=='html')
        assert lang in LANGUAGES, (path,lang)
        h1 = [n for n in tags if n.tag=='h1']; assert len(h1)==1, path
        main = [n for n in tags if n.tag=='main']; assert len(main)==1,path
        schemas = [json.loads(x) for x in SCHEMA.findall(source)]
        product = next((x for x in schemas if x.get('@type')=='Product'), None)
        article = next((x for x in schemas if x.get('@type') in ['Article','BlogPosting']),None)
        kind = 'used-equipment' if product and product.get('itemCondition','').endswith('UsedCondition') else 'new-equipment' if product else 'articles' if article else 'main-pages'
        alternates = {n.attrs['hreflang']:n.attrs['href'] for n in tags if n.tag=='link' and n.attrs.get('hreflang')}
        assert set(alternates)=={'pl','en','ru','x-default'},path
        pages.append(dict(path=path,source=source,tree=tree,tags=tags,meta=meta,canonical=url,lang=lang,
                          title=h1[0].text(),main=main[0],schemas=schemas,product=product,kind=kind,
                          alternates=alternates,md=markdown_url(url)))
    lookup={p['canonical']:p for p in pages}
    for p in pages:
        for lang,url in p['alternates'].items():
            assert url in lookup, (p['canonical'],url)
            assert p['canonical'] in lookup[url]['alternates'].values(),url
    return pages


def excluded(node):
    classes = node.attrs.get('class','').split()
    return (node.tag in SKIP or node.attrs.get('aria-hidden')=='true' or 'hidden' in node.attrs
            or any('breadcrumb' in c for c in classes) or node.has('lumos-diagram')
            or node.has('alpha-cooling-diagram') or node.has('button'))


def render(node, page, images=None):
    if images is None: images=set()
    if excluded(node) or node.tag=='h1': return ''
    if not node.tag: return re.sub(r'\s+',' ',node.data)
    if node.tag=='img':
        src,alt=node.attrs.get('src',''),node.attrs.get('alt','')
        if not src or not alt or src in images: return ''
        images.add(src)
        return '\n\n!['+alt.replace('[','\\[').replace(']','\\]')+']('+urljoin(page['canonical'],src)+')\n\n'
    if node.tag=='table':
        rows=[]
        for row in node.all('tr'):
            cells=[clean(render(c,page,images)).replace('|','\\|').replace('\n','<br>') for c in row.children if c.tag in ['th','td']]
            if cells: rows.append(cells)
        if not rows:return ''
        width=max(map(len,rows)); rows=[r+['']*(width-len(r)) for r in rows]
        lines=['| '+' | '.join(r)+' |' for r in rows]
        lines.insert(1,'| '+' | '.join(['---']*width)+' |')
        return '\n\n'+'\n'.join(lines)+'\n\n'
    body=''.join(render(c,page,images) for c in node.children)
    if node.tag=='a':
        href=node.attrs.get('href','')
        if not href or href.startswith(('javascript:','#')) or '![' in body: return body
        label=re.sub(r'\s+',' ',body).strip()
        return '['+label+']('+urljoin(page['canonical'],href)+')' if label else ''
    if node.tag in ['h2','h3','h4','h5','h6']:
        return '\n\n'+'#'*int(node.tag[1])+' '+body.strip()+'\n\n'
    if node.tag=='summary': return '\n\n### '+body.strip()+'\n\n'
    if node.tag in ['strong','b']: return '**'+body.strip()+'**' if body.strip() else ''
    if node.tag in ['em','i']: return '*'+body.strip()+'*' if body.strip() else ''
    if node.tag=='br': return '\n'
    if node.tag=='li':return '\n- '+body.strip()+'\n'
    if node.tag=='ol':
        items=[clean(render(c,page,images)).removeprefix('- ') for c in node.children if c.tag=='li']
        return '\n\n'+'\n'.join(f'{i}. {item}' for i,item in enumerate(items,1))+'\n\n'
    if node.tag=='div' and node.parent and node.parent.has('nowe-specs'):
        return '\n- '+': '.join(c.text() for c in node.children if c.tag and c.text())+'\n'
    if node.tag in ['p','div','section','header','main','article','aside','figure','figcaption','address','details','ul','dl','dt','dd']:
        return '\n\n'+body.strip()+'\n\n' if body.strip() else ''
    return body


def clean(text):
    text=re.sub(r'[ \t]+\n','\n',text)
    text=re.sub(r'\n[ \t]+','\n',text)
    return re.sub(r'\n{3,}','\n\n',text).strip()


def markdown(page):
    labels={'pl':('Źródło HTML','Język','Inne wersje językowe'), 'en':('HTML source','Language','Other languages'), 'ru':('Источник HTML','Язык','Другие языковые версии')}[page['lang']]
    out=f'# {page["title"]}\n\n{labels[0]}: [{page["title"]}]({page["canonical"]})\n\n{labels[1]}: {LANGUAGES[page["lang"]]}\n\n'
    out+=labels[2]+': '+', '.join(f'[{LANGUAGES[l]}]({u})' for l,u in page['alternates'].items() if l in LANGUAGES and l!=page['lang'])+'\n\n'
    out+='> '+page['meta'].get('description','')+'\n\n'
    return out+clean(render(page['main'],page))+'\n'


def llms(pages):
    out='# LTS Market\n\n> New and used aesthetic equipment. Prices are in PLN.\n\n'
    out+='The site is available in Polish, English and Russian. Canonical HTML pages are the source of truth. Markdown versions preserve their language, specifications, prices and service qualifications. LTS Market is the seller; Laser Tech Service is the service provider named on the pages. Service scope and financing terms must be read from the relevant HTML page, not inferred from another product.\n\n'
    for kind,title in [('main-pages','Main pages'),('new-equipment','New equipment'),('used-equipment','Used equipment'),('articles','Articles')]:
        out+='## '+title+'\n\n'
        for p in pages:
            if p['kind']==kind:
                out+=f'- [{p["lang"].upper()} — {p["title"]}]({p["canonical"]}): {p["meta"].get("description", "")} [Markdown]({p["md"]})\n'
        out+='\n'
    out+='## Machine-readable resources\n\n- [Full text](https://ltsmarket.pl/llms-full.txt)\n- [AI catalogue](https://ltsmarket.pl/ai-catalog.json)\n- [Sitemap](https://ltsmarket.pl/sitemap.xml)\n'
    return out


def outputs(pages):
    generated={p['path'].with_suffix('.md'):markdown(p) for p in pages}
    generated[ROOT/'llms.txt']=llms(pages)
    full='# LTS Market — full text\n\nCanonical HTML is the source of truth. Each section links to its source and language equivalents.\n'
    for p in pages:
        full+='\n---\n\n'+re.sub(r'^(#{1,6}) ',lambda m:'#'*min(len(m[1])+1,6)+' ',markdown(p),flags=re.M)
    generated[ROOT/'llms-full.txt']=full
    for p in pages: generated[p['path']]=integration(p['source'])
    start,end='# BEGIN GENERATED AI HEADERS','# END GENERATED AI HEADERS'
    headers=start+'\n# Generated by scripts/build-ai-search.py\n'
    for p in pages:
        headers+=f'\n{urlsplit(p["md"]).path}\n  Content-Type: text/markdown; charset=utf-8\n  X-Content-Type-Options: nosniff\n  Link: <{p["canonical"]}>; rel="canonical", <{BASE}/llms.txt>; rel="describedby"\n'
    for name,mime in [('llms.txt','text/plain'),('llms-full.txt','text/plain'),('ai-catalog.json','application/json')]:
        headers+=f'\n/{name}\n  Content-Type: {mime}; charset=utf-8\n  X-Content-Type-Options: nosniff\n'
    headers+=end+'\n'
    target=ROOT/'_headers'; existing=target.read_text() if target.exists() else ''
    generated[target]=re.sub(re.escape(start)+r'.*?'+re.escape(end)+r'\n?',lambda m:headers,existing,flags=re.S) if start in existing else existing+('\n' if existing else '')+headers
    return generated
