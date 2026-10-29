#!/usr/bin/env python3
"""Render Alpha Mini in the existing catalogue design and localized contact form."""
import argparse
import html
import json
import re
from pathlib import Path
from site_content import link_service_names

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://ltsmarket.pl'
ROUTES = {'pl': '/nowe/alpha-mini/', 'en': '/en/new/alpha-mini/', 'ru': '/ru/novye/alpha-mini/'}
IMAGE = '/assets/img/nowe/alpha-mini.webp'
e = html.escape

def paragraphs(items):
    return '\n'.join(f'<p>{e(x)}</p>' for x in items)

def cards(items):
    return '<div class="nowe-support__grid">' + ''.join(f'<article class="nowe-support__card"><h3>{e(h)}</h3><p>{e(p)}</p></article>' for h,p in items) + '</div>'

def section(title, content, id, dark=False):
    return f'<section class="{"nowe-support" if dark else "nowe-intro"}" id="{id}"><div class="container"><div class="nowe-heading{" nowe-heading--dark" if dark else ""}"><h2 class="nowe-section-title">{e(title)}</h2></div>{content}</div></section>'

def cooling_diagram(d):
    # Component overview only: no claimed internal routing or model-specific dimensions.
    icons = [
        '<path d="M15 20h50v40H15z M25 10v10 M40 10v10 M55 10v10 M25 60v10 M40 60v10 M55 60v10 M25 30h30v20H25z"/>',
        '<path d="M40 8C32 23 17 34 17 47a23 23 0 0 0 46 0C63 34 48 23 40 8Z M28 48a12 12 0 0 0 12 12"/>',
        '<circle cx="40" cy="40" r="7"/><path d="M40 33C10 5 68 3 46 34 M47 40C78 16 80 72 47 46 M40 47C66 78 10 80 34 46 M33 40C3 66 1 10 34 34"/>',
        '<path d="m15 25 25-12 25 12v30L40 67 15 55Z M15 25l25 12 25-12 M40 37v30 M25 20l25 12"/>',
    ]
    blocks = ''
    for i,(label,note,icon) in enumerate(zip(d['labels'],d['notes'],icons)):
        y=118+i*116
        blocks += f'<g transform="translate(30 {y})"><rect width="540" height="98" rx="4" fill="#fff" stroke="#d7e1e8"/><g transform="translate(12 9)" fill="none" stroke="#168cff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{icon}</g><text x="108" y="40" font-size="21" font-weight="600" fill="#101b24">{e(label)}</text><text x="108" y="67" font-size="15" fill="#687784">{e(note)}</text></g>'
    return f'<figure class="alpha-figure alpha-cooling-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" role="img" aria-labelledby="cooling-diagram-title"><title id="cooling-diagram-title">{e(d["alt"])}</title><rect width="600" height="600" fill="#edf2f6"/><g font-family="Arial, sans-serif"><text x="30" y="64" font-size="32" font-weight="600" fill="#101b24">ICE Flow</text><path d="M30 86h540" stroke="#cbd8e1"/>{blocks}</g></svg><figcaption>{e(d["caption"])}</figcaption></figure>'

def generate():
    data = json.loads((ROOT/'scripts/alpha-mini-content.json').read_text())
    for lang,d in data.items():
        prefix = '' if lang == 'pl' else '/'+lang
        catalog = prefix+'/nowe.html'
        source = (ROOT/catalog.lstrip('/')).read_text()
        head = source.split('</head>')[0]
        head = re.sub(r'<script type="application/ld\+json">.*?</script>', '', head, flags=re.S)
        head = re.sub(r'<title>.*?</title>', '<title>'+e(d['title'])+'</title>', head)
        for key in ['description','og:description','twitter:description','og:title','twitter:title','og:image:alt','twitter:image:alt','og:url','og:image','twitter:image','og:image:width','og:image:height','og:type']:
            value = d['description'] if 'description' in key else d['title'] if 'title' in key else d['alt'] if ':alt' in key else BASE+ROUTES[lang] if key=='og:url' else '1145' if key.endswith(':width') else '1374' if key.endswith(':height') else 'product' if key=='og:type' else BASE+IMAGE
            head = re.sub(r'(<meta (?:name|property)="'+key+r'" content=")[^"]*', lambda m:m[1]+e(value,quote=True), head)
        head = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m:m[1]+BASE+ROUTES[lang], head)
        for l,route in {**ROUTES,'x-default':ROUTES['pl']}.items():
            head = re.sub(r'(<link rel="alternate" hreflang="'+l+r'" href=")[^"]*', lambda m:m[1]+BASE+route, head)
        head += '\n<link rel="stylesheet" href="/css/uzywane.css">\n<link rel="stylesheet" href="/css/kontakt.css">\n'
        product = {'@context':'https://schema.org','@type':'Product','@id':BASE+ROUTES[lang]+'#product','name':'Alpha Mini','model':'Alpha Mini','description':d['description'],'image':[BASE+IMAGE],'url':BASE+ROUTES[lang],'mainEntityOfPage':BASE+ROUTES[lang],'itemCondition':'https://schema.org/NewCondition','offers':{'@type':'AggregateOffer','lowPrice':40000,'priceCurrency':'PLN','url':BASE+ROUTES[lang],'seller':{'@type':'Organization','name':'LTS Market','url':BASE+'/'}}}
        crumbs = {'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':i+1,'name':name,'item':BASE+url} for i,(name,url) in enumerate([('LTS Market',prefix+'/'),(d['catalog'],catalog),('Alpha Mini',ROUTES[lang])])]}
        for obj in [product,crumbs]: head += '<script type="application/ld+json">\n'+json.dumps(obj,ensure_ascii=False,indent=2)+'\n</script>\n'
        # Reuse the catalogue header/footer verbatim except product language destinations.
        chrome_start = source.split('</head>')[1].split('<main')[0]
        footer = source[source.index('<footer'):source.index('</footer>')+len('</footer>')]
        def languages(text):
            return re.sub(r'(<a\b[^>]*href=")([^"]+)("[^>]*lang="(pl|en|ru)")',lambda m:m[1]+ROUTES[m[4]]+m[3],text)
        chrome_start,footer = languages(chrome_start),languages(footer)
        crumb = f'<nav class="used-breadcrumbs" aria-label="{e(d["catalog"])}"><a href="{prefix}/">Market</a><span aria-hidden="true">/</span><a href="{catalog}">{e(d["catalog"])}</a><span aria-hidden="true">/</span><span>Alpha Mini</span></nav>'
        main = '<main id="main-content" class="alpha-page">\n'
        main += f'<section class="nowe-hero"><div class="container nowe-hero__container"><div class="nowe-hero__content">{crumb}<p class="section-label nowe-hero__label">{e(d["label"])}</p><h1 class="nowe-hero__title">{e(d["h1"])}</h1><p class="nowe-hero__description">{e(d["lead"])}</p><p class="alpha-price">{e(d["price"])}</p><div class="nowe-hero__actions"><a class="button button--primary" href="#contact-form">{e(d["ask"])}</a><a class="button button--outline" href="#specification">{e(d["speccta"])}</a></div><div class="nowe-hero__stats"><div class="nowe-hero__stat"><strong>1000–1200 W</strong><span>{e(d["rows"][1][0])}</span></div><div class="nowe-hero__stat"><strong>12 × 12 mm</strong><span>{e(d["rows"][6][0])}</span></div><div class="nowe-hero__stat"><strong>ICE Flow</strong><span>{e(d["rows"][7][0])}</span></div></div><p class="alpha-notice">{e(d["heroSupport"])}</p></div><div class="nowe-hero__visual"><img src="{IMAGE}" alt="{e(d["alt"])}" width="1145" height="1374" fetchpriority="high" decoding="async"></div></div></section>\n'
        main += section(d['why'],cards(d['benefits']),'benefits',True)
        for i,(title,ps) in enumerate(d['sections']):
            content = '<div class="alpha-copy">'+paragraphs(ps)+'</div>'
            if i == 0:
                main += section(title,content,'technology')
            else:
                text = f'<div class="alpha-split__text"><h2 class="nowe-section-title">{e(title)}</h2>{content}</div>'
                if i == 1:
                    visual = cooling_diagram(d['coolingDiagram'])
                    layout = visual + text
                    id = 'cooling'
                else:
                    visual = f'<figure class="alpha-figure"><a href="{IMAGE}"><img src="{IMAGE}" alt="{e(d["alt"])}" width="1145" height="1374" loading="lazy" decoding="async"></a></figure>'
                    layout = text + visual
                    id = 'handpiece'
                main += f'<section class="nowe-intro" id="{id}"><div class="container alpha-split">{layout}</div></section>'
        main += section(d['audience'],cards(d['audiences']),'audience',True)
        table = f'<p class="alpha-copy">{e(d["specNote"])}</p><table class="alpha-spec"><caption>{e(d["spec"])}</caption><thead><tr><th scope="col">{e(d["parameter"])}</th><th scope="col">{e(d["value"])}</th></tr></thead><tbody>'+''.join(f'<tr><th scope="row">{e(k)}</th><td>{e(v)}</td></tr>' for k,v in d['rows'])+'</tbody></table>'
        main += section(d['spec'],table,'specification')
        main += section(d['gallery'],f'<figure class="alpha-figure"><a href="{IMAGE}"><img src="{IMAGE}" alt="{e(d["alt"])}" width="1145" height="1374" loading="lazy" decoding="async"></a><figcaption>{e(d["caption"])}</figcaption></figure>','gallery')
        main += section(d['serviceTitle'],'<div class="alpha-copy">'+paragraphs(d['service'])+'</div>'+cards(d['serviceCards'])+f'<p class="alpha-copy">{e(d["terms"])}</p><a class="button button--primary" href="https://lasertechservice.pl/">{e(d["serviceCta"])}</a>','service',True)
        main += section(d['buy'],'<ol class="alpha-steps">'+''.join('<li>'+e(x)+'</li>' for x in d['steps'])+'</ol>','purchase')
        main += section(d['faqTitle'],'<div class="alpha-faq">'+''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q,a in d['faq'])+'</div>','faq')
        contact = (ROOT/(prefix.lstrip('/')+'/' if prefix else '')/'kontakt.html').read_text()
        form = re.search(r'<form class="contact-form".*?</form>',contact,re.S)[0]
        form = form.replace('id="contact-form"','id="contact-form" data-product-name="Alpha Mini" data-product-url="'+BASE+ROUTES[lang]+'"')
        form = form.replace('value="kontakt"','value="alpha-mini"').replace('value="nowe-urzadzenie"','value="nowe-urzadzenie" selected')
        form = re.sub(r'(<textarea\b[^>]*>).*?</textarea>',r'\1Alpha Mini</textarea>',form,flags=re.S)
        main += f'<section class="contact-form-section" id="enquiry"><div class="container"><p class="alpha-notice">{e(d["reminder"])}</p><div class="contact-form-section__grid"><div class="contact-form-section__intro"><h2 class="contact-section-title">{e(d["formTitle"])}</h2><p>{e(d["formCopy"])}</p><p><a href="tel:+48575254431">+48 575 254 431</a><br><a href="mailto:sales@ltsmarket.pl">sales@ltsmarket.pl</a></p></div><div class="contact-form-wrapper">{form}</div></div></div></section>'
        main += '</main>'
        output = head+'</head>'+chrome_start+main+'\n'+footer+f'\n<script src="/js/lead-api.js" defer></script>\n<script src="/js/main.js" defer></script>\n<script src="{prefix}/js/kontakt.js" defer></script>\n</body>\n</html>\n'
        yield ROOT/ROUTES[lang].lstrip('/')/'index.html',link_service_names(output)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    for path,content in generate():
        if args.check: assert path.read_text()==content, f'Stale {path}'
        else: path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content)
    print('PASS: Alpha Mini PL/EN/RU '+('fresh' if args.check else 'generated'))
