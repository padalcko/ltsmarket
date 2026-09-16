"""Build EN/RU product pages from PL markup and reviewed translations.
Run after changing a Polish product page or product-translations.json.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import html, json, posixpath, re
ROOT = Path(__file__).resolve().parents[1]
TRANSLATIONS = json.loads((ROOT / 'scripts/product-translations.json').read_text())
BASE = 'https://ltsmarket.pl'

def translate(text, lang):
    normalized = ' '.join(text.split())
    if normalized not in TRANSLATIONS: return text
    return re.sub(r'\S(?:[\s\S]*\S)?', lambda _: TRANSLATIONS[normalized][lang], text, count=1)

def alternates(slug):
    urls = {lang: f'{BASE}/{"" if lang == "pl" else lang + "/"}uzywane/{slug}.html' for lang in ('pl','en','ru')}
    return '\n'.join(f'    <link rel="alternate" hreflang="{lang}" href="{url}" />' for lang,url in list(urls.items())+[('x-default',urls['pl'])])

class LocalizedPage(HTMLParser):
    def __init__(self, lang, slug):
        super().__init__(convert_charrefs=False)
        self.lang = lang
        self.slug = slug
        self.output = []
        self.in_json = False
    def url(self, value, asset=False):
        parts = urlsplit(value)
        if parts.scheme or parts.netloc or not parts.path: return value
        if value.startswith('/'):
            # Explicit language-switcher targets must retain their language.
            if asset or re.match(r'/(?:en|ru)/uzywane/',value) or value == f'/uzywane/{self.slug}.html': return value
            if value == '/prywatnosc.html': return f'/{self.lang}/prywatnosc.html'
            return value
        resolved = posixpath.normpath(posixpath.join('uzywane',parts.path))
        if resolved.startswith('assets/'): return '/' + resolved
        if resolved == 'index.html': return f'/{self.lang}/'
        return f'/{self.lang}/' + resolved + ('?' + parts.query if parts.query else '') + ('#' + parts.fragment if parts.fragment else '')
    def tag(self, tag, attrs, closed=False):
        original = dict(attrs)
        result = []
        if tag == 'script': self.in_json = original.get('type') == 'application/ld+json'
        for key,value in attrs:
            if value is None: result.append(key);continue
            if tag == 'html' and key == 'lang': value = self.lang
            elif key in ('alt','data-alt','aria-label'): value = translate(value,self.lang)
            elif key == 'content' and tag == 'meta':
                if original.get('property') == 'og:locale': value = {'en':'en_GB','ru':'ru_RU'}[self.lang]
                elif original.get('property') == 'og:url': value = f'{BASE}/{self.lang}/uzywane/{self.slug}.html'
                else: value = translate(value,self.lang)
            elif key == 'href' and tag == 'link' and original.get('rel') == 'canonical': value = f'{BASE}/{self.lang}/uzywane/{self.slug}.html'
            elif key in ('href','src','data-image'): value = self.url(value,key in ('src','data-image'))
            elif key == 'srcset': value = ', '.join(self.url(item.strip().split()[0],True)+' '+item.strip().split()[1] for item in value.split(','))
            elif tag == 'a' and key == 'class' and original.get('hreflang'):
                classes = [c for c in value.split() if c != 'active']
                if original['hreflang'] == self.lang: classes.append('active')
                value = ' '.join(classes)
            result.append(f'{key}="{html.escape(value,quote=True)}"')
        if tag == 'a' and original.get('hreflang') == self.lang and 'class' not in original: result.append('class="active"')
        self.output.append('<'+tag+(' '+' '.join(result) if result else '')+(' />' if closed else '>'))
    def handle_starttag(self,t,a): self.tag(t,a)
    def handle_startendtag(self,t,a): self.tag(t,a,True)
    def handle_endtag(self,t):
        self.output.append('</'+t+'>')
        if t == 'script': self.in_json = False
    def handle_data(self,text):
        if self.in_json:
            data = json.loads(text)
            def localize(value,key=''):
                if isinstance(value,dict):return {k:localize(v,k) for k,v in value.items()}
                if isinstance(value,list):return [localize(v,key) for v in value]
                if not isinstance(value,str):return value
                if key in ('description','name'):return translate(value,self.lang)
                if key in ('url','@id','item'):
                    if value.startswith(BASE+'/uzywane/'):return value.replace(BASE+'/',BASE+'/'+self.lang+'/',1)
                    if key == 'item' and value in (BASE+'/',BASE+'/uzywane.html'):return value.replace(BASE+'/',BASE+'/'+self.lang+'/',1)
                return value
            self.output.append('\n'+json.dumps(localize(data),ensure_ascii=False,indent=2)+'\n')
        else:self.output.append(html.escape(translate(html.unescape(text),self.lang),quote=False))
    def handle_comment(self,text):self.output.append('<!--'+text+'-->')
    def handle_decl(self,text):self.output.append('<!'+text+'>')
    def handle_entityref(self,name):self.output.append('&'+name+';')
    def handle_charref(self,name):self.output.append('&#'+name+';')

for source in sorted((ROOT/'uzywane').glob('*.html')):
    slug = source.stem
    text = source.read_text()
    text = re.sub(r'\s*<link\s+rel="alternate"[^>]*>', '', text)
    text = text.replace('</head>',alternates(slug)+'\n  </head>')
    text = text.replace(f'href="{slug}.html"',f'href="/uzywane/{slug}.html"')
    for lang in ('en','ru'):
        text = text.replace(f'href="../{lang}/uzywane.html"',f'href="/{lang}/uzywane/{slug}.html"')
    # The footer uses language names without hreflang; retain their explicit URLs.
    source.write_text(text)
    for lang in ('en','ru'):
        parser = LocalizedPage(lang,slug)
        parser.feed(text)
        target = ROOT/lang/'uzywane'/source.name
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(''.join(parser.output))
        print(target.relative_to(ROOT))
