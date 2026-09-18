"""Build the three static blog editions from blog-posts.json and existing site chrome."""
from pathlib import Path
from html import escape
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
CONTENT = json.loads((ROOT / 'scripts/blog-posts.json').read_text())
DATA = CONTENT['site']
POSTS = CONTENT['posts']
DOMAIN = 'https://ltsmarket.pl'

def prefix(lang):
    return '/' if lang == 'pl' else f'/{lang}/'

def route(lang, article=False):
    return prefix(lang) + 'blog/' + (POSTS[article - 1][lang]['slug'] + '/' if article else '')

def image_tag(entry):
    if not entry.get('image'):
        return ''
    css = 'blog-article__image'
    loading = 'fetchpriority="high"'
    return f'<img class="{css}" src="{escape(entry["image"], quote=True)}" alt="{escape(entry["image_alt"], quote=True)}" width="{entry["image_width"]}" height="{entry["image_height"]}" {loading} decoding="async">'

def build(lang, article):
    d = {**DATA[lang], **(POSTS[article - 1][lang] if article else {})}
    source = (ROOT / (prefix(lang).strip('/') + '/leasing.html').lstrip('/')).read_text()
    head, rest = source.split('  <body>', 1)
    before, rest = rest.split('    <main id="main-content">', 1)
    _, after = rest.split('    </main>', 1)
    title = d['seo'] if article else d['blog'] + ' | ' + {'pl':'Poradniki dla gabinetów','en':'Guides for salon owners','ru':'Статьи для владельцев кабинетов'}[lang]
    desc = d['description'] if article else d['intro']
    head = re.sub(r'<title>.*?</title>', '<title>'+escape(title)+'</title>', head)
    for key in ['description', 'og:description', 'twitter:description']:
        head = re.sub(r'((?:name|property)="'+key+r'" content=")[^"]*', lambda m:m[1]+escape(desc,quote=True), head)
    for key in ['og:title', 'twitter:title']:
        head = re.sub(r'(property="'+key+r'" content="|name="'+key+r'" content=")[^"]*',lambda m:m[1]+escape(title,quote=True),head)
    for other in DATA:
        head = head.replace(DOMAIN+prefix(other)+'leasing.html',DOMAIN+route(other,article))
    head = head.replace('/css/leasing.css','/css/blog.css')
    if article:
        head = head.replace('property="og:type" content="website"','property="og:type" content="article"')
    if article and d.get('image'):
        replacements = {'og:image': DOMAIN+d['image'], 'twitter:image': DOMAIN+d['image'],
                        'og:image:alt': d['image_alt'], 'twitter:image:alt': d['image_alt'],
                        'og:image:width': str(d['image_width']), 'og:image:height': str(d['image_height'])}
        for key, value in replacements.items():
            head = re.sub(r'((?:name|property)="'+re.escape(key)+r'" content=")[^"]*', lambda m: m[1]+escape(value, quote=True), head)
    crumbs = [{'@type':'ListItem','position':1,'name':d['home'],'item':{'@id':DOMAIN+prefix(lang)}}, {'@type':'ListItem','position':2,'name':d['blog'],'item':{'@id':DOMAIN+route(lang)}}]
    if article:
        crumbs.append({'@type':'ListItem','position':3,'name':d['title'],'item':{'@id':DOMAIN+route(lang,article)}})
    schema = {'@context':'https://schema.org','@type':'BlogPosting' if article else 'Blog','@id':DOMAIN+route(lang,article)+'#'+('article' if article else 'blog'),'url':DOMAIN+route(lang,article),'name':d['title'] if article else d['blog'],'description':desc,'inLanguage':lang,'publisher':{'@type':'Organization','name':'LTS Market','url':DOMAIN+'/'}}
    if article:
        schema.update(headline=d['title'],mainEntityOfPage=DOMAIN+route(lang,article),image=DOMAIN+d.get('image', '/assets/img/hero-lts-market.jpg'))
    else:
        schema['blogPost']=[{'@type':'BlogPosting','headline':post[lang]['title'],'url':DOMAIN+route(lang,i)} for i,post in enumerate(POSTS,1)]
    structured = '\n'.join('<script type="application/ld+json">'+json.dumps(s,ensure_ascii=False)+'</script>' for s in [schema,{'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':crumbs}])
    head = re.sub(r'<script type="application/ld\+json">.*?</script>',lambda m:structured,head,flags=re.S)
    # Only language links change to the equivalent blog page; commercial links stay intact.
    def languages(m):
        tag=m[0]
        for other in DATA:
            tag=tag.replace('href="'+prefix(other)+'leasing.html"','href="'+route(other,article)+'"')
        return tag
    before=re.sub(r'<a\b[^>]*\blang="[^"]+"[^>]*>',languages,before)
    after=re.sub(r'<a\b[^>]*\blang="[^"]+"[^>]*>',languages,after)
    before=before.replace('class="desktop-nav__link is-active" href="'+prefix(lang)+'leasing.html" aria-current="page"','class="desktop-nav__link" href="'+prefix(lang)+'leasing.html"')
    before=before.replace('class="desktop-nav__link" href="'+route(lang)+'"','class="desktop-nav__link is-active" href="'+route(lang)+'"'+(' aria-current="page"' if not article else ''))
    breadcrumb=f'<nav class="blog-breadcrumb" aria-label="{escape(d["home"])}"><a href="{prefix(lang)}">{d["home"]}</a><span aria-hidden="true"> / </span>'
    breadcrumb += f'<a href="{route(lang)}">{d["blog"]}</a>' if article else f'<span aria-current="page">{d["blog"]}</span>'
    breadcrumb+='</nav>'
    if article:
        toc='<nav class="blog-toc" aria-label="'+d['toc']+'"><h2>'+d['toc']+'</h2><ol>'+''.join(f'<li><a href="#section-{i}">{escape(h)}</a></li>' for i,(h,p) in enumerate(d['sections'],1))+'</ol></nav>'
        sections=''.join(f'<section aria-labelledby="section-{i}"><h2 id="section-{i}">{escape(h)}</h2>'+''.join('<p>'+p.format(prefix=prefix(lang))+'</p>' for p in text.split('\n'))+'</section>' for i,(h,text) in enumerate(d['sections'],1))
        main=f'<article class="blog-article"><header class="blog-heading"><p class="section-label">{d["blog"]}</p><h1>{escape(d["title"])}</h1><p class="blog-lead">{d["lead"]}</p></header>{image_tag(d)}{toc}<div class="blog-prose">{sections}</div><aside class="blog-cta"><h2>{d["cta"]}</h2><a class="button button--primary" href="{prefix(lang)}kontakt.html">{d["contact"]}</a></aside><a class="blog-back" href="{route(lang)}">← {d["back"]}</a></article>'
    else:
        cards = []
        for i, post in reversed(list(enumerate(POSTS, 1))):
            entry = post[lang]
            cards.append(f'<article class="blog-card"><p class="section-label">LTS Market</p><h2><a href="{route(lang,i)}">{escape(entry["title"])}</a></h2><p>{escape(entry["description"])}</p><a class="button button--primary" href="{route(lang,i)}">{d["read"]}</a></article>')
        main=f'<header class="blog-heading"><p class="section-label">LTS Market</p><h1>{d["blog"]}</h1><p class="blog-lead">{d["intro"]}</p></header><div class="blog-grid">'+''.join(cards)+'</div>'
    output=head+'  <body>'+before+'<main id="main-content" class="blog-main"><div class="container">'+breadcrumb+main+'</div></main>'+after
    dest=ROOT / route(lang,article).lstrip('/') / 'index.html'
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(output)

# Route Market's generic blog links locally; retain the explicitly named service blog.
for path in ROOT.rglob('*.html'):
    lang=path.relative_to(ROOT).parts[0]
    lang=lang if lang in ('en','ru') else 'pl'
    source=path.read_text()
    source=re.sub(r'(<a\b[^>]*href=")https://lasertechservice.pl/blog/("[^>]*>\s*(?:Blog|Блог)\s*</a>)',lambda m:m[1]+route(lang)+m[2],source)
    if source != path.read_text():
        path.write_text(source)
for lang in DATA:
    for article in range(len(POSTS) + 1):
        build(lang,article)

# Preserve existing sitemap entries and refresh just the blog routes.
ns='http://www.sitemaps.org/schemas/sitemap/0.9'
xhtml='http://www.w3.org/1999/xhtml'
ET.register_namespace('',ns)
ET.register_namespace('xhtml',xhtml)
tree=ET.parse(ROOT/'sitemap.xml')
base=tree.getroot()
blog_urls={DOMAIN+route(lang,a) for lang in DATA for a in range(len(POSTS) + 1)}
for node in list(base):
    if node.findtext('{'+ns+'}loc') in blog_urls:
        base.remove(node)
for article in range(len(POSTS) + 1):
    for lang in DATA:
        node=ET.SubElement(base,'{'+ns+'}url')
        ET.SubElement(node,'{'+ns+'}loc').text=DOMAIN+route(lang,article)
        for alt in (*DATA,'x-default'):
            ET.SubElement(node,'{'+xhtml+'}link',{'rel':'alternate','hreflang':alt,'href':DOMAIN+route('pl' if alt=='x-default' else alt,article)})
ET.indent(tree,space='  ')
tree.write(ROOT/'sitemap.xml',encoding='utf-8',xml_declaration=True)
print(f'Built {len(DATA) * (len(POSTS) + 1)} blog pages and updated navigation and sitemap.')
