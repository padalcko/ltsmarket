"""Static cross-page audit, run from repository root."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import collections, json, re, xml.etree.ElementTree as ET
class Page(HTMLParser):
 def __init__(self, source):
  super().__init__(); self.tags=[]; self.stack=[]; self.errors=[]; self.feed(source)
 def handle_startendtag(self,t,a): self.tags.append((t,dict(a)))
 def handle_starttag(self,t,a):
  self.tags.append((t,dict(a)))
  if t not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}: self.stack.append(t)
 def handle_endtag(self,t):
  if not self.stack or self.stack[-1]!=t: self.errors.append(('nesting',self.getpos(),t,self.stack[-4:]))
  if t in self.stack:
   while self.stack.pop()!=t: pass
pages={p:Page(p.read_text()) for p in Path('.').rglob('*.html')}
errors=[]
def check(ok,*msg):
 if not ok: errors.append(msg)
for p,page in pages.items():
 tags=page.tags; check(not page.errors,p,page.errors); check(not page.stack,p,'unclosed',page.stack)
 ids=[a['id'] for t,a in tags if 'id' in a];check(len(ids)==len(set(ids)),p,'duplicate IDs')
 for t in ['h1','title','main']: check(sum(tag==t for tag,a in tags)==1,p,'count',t)
 for attr,value in [('name','description'),('name','viewport'),('rel','canonical')]: check(sum(a.get(attr)==value for t,a in tags)==1,p,value)
 canon=next(a['href'] for t,a in tags if a.get('rel')=='canonical')
 expected='https://ltsmarket.pl/'+str(p).removesuffix('index.html');check(canon==expected,p,'canonical',canon)
 alts={a.get('hreflang'):a['href'] for t,a in tags if a.get('rel')=='alternate' and 'hreflang' in a};check(set(alts)=={'pl','en','ru','x-default'},p,'hreflang')
 for t,a in tags:
  if t=='img': check('alt' in a,p,'image alt')
  if t=='iframe': check(bool(a.get('title')),p,'iframe title')
  for key in ['href','src','data-image']:
   if key not in a: continue
   url=urlsplit(a[key]);
   if url.scheme or url.netloc: continue
   target=Path(unquote(url.path).lstrip('/')) if url.path.startswith('/') else p.parent/unquote(url.path) if url.path else p
   if target.is_dir(): target=target/'index.html'
   check(target.is_file(),p,'missing',a[key])
   if url.fragment and target in pages: check(any(x.get('id')==unquote(url.fragment) for _,x in pages[target].tags),p,'anchor',a[key])
 for lang,url in alts.items():
  target=Path(urlsplit(url).path.lstrip('/'))
  if target.is_dir(): target=target/'index.html'
  check(target in pages,p,'alternate missing',url)
  if target in pages: check(any(a.get('rel')=='alternate' and a.get('href')==canon for _,a in pages[target].tags),p,'alternate return',url)
site=ET.parse('sitemap.xml'); urls={el.text for el in site.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
check(urls=={'https://ltsmarket.pl/'+str(p).removesuffix('index.html') for p in pages},'sitemap mismatch')
for p in Path('.').rglob('*.webmanifest'): json.loads(p.read_text())
for p in Path('css').glob('*.css'):
 s=re.sub(r'/\*.*?\*/','',p.read_text(),flags=re.S);check(s.count('{')==s.count('}'),p,'CSS braces')
for e in errors: print('FAIL',*e)
print(f'{len(pages)} pages audited; {len(errors)} errors')
raise SystemExit(bool(errors))
