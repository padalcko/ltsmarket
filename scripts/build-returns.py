#!/usr/bin/env python3
"""Build the supplied policy and add its link exclusively to existing legal footers."""
import json
import re
from html import escape
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'scripts/returns-content.json').read_text())
ROUTES = {'pl': '/zwroty-i-reklamacje/', 'ru': '/ru/vozvrat-i-garantiya/', 'en': '/en/returns-and-warranty/'}
TITLES = {lang: text.splitlines()[0][2:] for lang, text in DATA.items()}
DESCRIPTIONS = {
    'pl': 'Zasady zwrotów, reklamacji, napraw i gwarancji na nowe i używane urządzenia LTS Market. Kontakt i sposób zgłoszenia reklamacji.',
    'ru': 'Условия возврата, рекламаций, ремонта и гарантии на новое и бывшее в использовании оборудование LTS Market. Контакты для обращения.',
    'en': 'Returns, complaints, repairs and warranty terms for new and used LTS Market equipment. Contact details and how to submit a complaint.'}
BASE = 'https://ltsmarket.pl'

def linked(text):
    return escape(text).replace('sales@ltsmarket.pl', '<a href="mailto:sales@ltsmarket.pl">sales@ltsmarket.pl</a>').replace('+48 575 254 431', '<a href="tel:+48575254431">+48 575 254 431</a>').replace('\n', '<br>')

for lang, text in DATA.items():
    prefix = '' if lang == 'pl' else '/' + lang
    source = (ROOT / (prefix + '/polityka-prywatnosci.html').lstrip('/')).read_text()
    old_title = re.search(r'<title>(.*?)</title>', source)[1]
    old_desc = re.search(r'<meta name="description" content="(.*?)">', source)[1]
    source = source.replace(old_title, escape(TITLES[lang] + ' | LTS Market')).replace(old_desc, escape(DESCRIPTIONS[lang]))
    source = re.sub(r'<!-- AI resources: generated -->.*?<!-- /AI resources -->', '', source, flags=re.S)
    for other, route in ROUTES.items():
        old = ('' if other == 'pl' else '/' + other) + '/polityka-prywatnosci.html'
        # Metadata and language destinations only; retain the privacy link in the footer.
        source = re.sub(r'(<(?:link|meta)\b[^>]*)(?=>)', lambda m: m[0].replace(BASE + old, BASE + route), source)
        source = re.sub(r'<a\b[^>]*\blang="' + other + r'"[^>]*>', lambda m: m[0].replace(old, route), source)
    chunks = text.split('\n\n')
    main = ['<main id="main-content" class="used-detail"><div class="container">',
            f'<div class="used-breadcrumbs"><a href="{prefix or "/"}">LTS Market</a><span aria-hidden="true">/</span><span>{escape(TITLES[lang])}</span></div>',
            '<h1>' + escape(TITLES[lang]) + '</h1>']
    section = False
    for chunk in chunks[1:]:
        if chunk.startswith('## '):
            if section: main.append('</section>')
            main.append('<section class="nowe-intro"><h2>' + escape(chunk[3:]) + '</h2>')
            section = True
        else:
            main.append('<p class="nowe-financing__copy">' + linked(chunk) + '</p>')
    if section: main.append('</section>')
    main.append('</div></main>')
    source = re.sub(r'<main\b.*?</main>', '\n'.join(main), source, flags=re.S)
    url = BASE + ROUTES[lang]
    schemas = [ {'@context':'https://schema.org','@type':'WebPage','@id':url+'#webpage','url':url,'name':TITLES[lang],'description':DESCRIPTIONS[lang],'inLanguage':lang},
                {'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'LTS Market','item':BASE+(prefix+'/' if prefix else '/')},{'@type':'ListItem','position':2,'name':TITLES[lang],'item':url}]} ]
    source = source.replace('</head>', '\n'.join('<script type="application/ld+json">'+json.dumps(s,ensure_ascii=False)+'</script>' for s in schemas)+'\n</head>')
    path = ROOT / ROUTES[lang].strip('/') / 'index.html'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(source)

count = 0
for path in ROOT.rglob('*.html'):
    source = path.read_text()
    match = re.search(r'<html\b[^>]*lang="(pl|en|ru)"', source)
    if not match: continue
    lang = match[1]
    def footer(m):
        block = m[0]
        if f'href="{ROUTES[lang]}"' in block: return block
        return re.sub(r'(<a\b[^>]*href="[^"]*polityka-prywatnosci.html"[^>]*>.*?</a>)', r'\1\n            <a href="'+ROUTES[lang]+'"> '+TITLES[lang]+' </a>', block, count=1, flags=re.S)
    updated = re.sub(r'<div class="footer__legal">.*?</div>', footer, source, flags=re.S)
    if updated != source: path.write_text(updated); count += 1

# The localized 404 chrome is stored as JSON strings and replaces its HTML footer.
error_path = ROOT / 'js/error-404.js'
error_source = error_path.read_text()
def error_footer(match):
    block = json.loads(match[1])
    for lang, route in ROUTES.items():
        privacy = ('' if lang == 'pl' else '/' + lang) + '/polityka-prywatnosci.html'
        if f'href="{privacy}"' in block and f'href="{route}"' not in block:
            block = re.sub(r'(<a href="' + re.escape(privacy) + r'">.*?</a>)',
                           r'\1\n            <a href="' + route + '"> ' + TITLES[lang] + ' </a>', block, count=1)
    return '"footer": ' + json.dumps(block, ensure_ascii=False)
error_path.write_text(re.sub(r'"footer": ("(?:[^"\\]|\\.)*")', error_footer, error_source))

ns = 'http://www.sitemaps.org/schemas/sitemap/0.9'
xhtml = 'http://www.w3.org/1999/xhtml'
ET.register_namespace('', ns); ET.register_namespace('xhtml', xhtml)
tree = ET.parse(ROOT/'sitemap.xml'); root = tree.getroot()
for lang, route in ROUTES.items():
    if any(el.findtext('{'+ns+'}loc') == BASE+route for el in root): continue
    el = ET.SubElement(root, '{'+ns+'}url')
    ET.SubElement(el, '{'+ns+'}loc').text = BASE+route
    for code in ['pl','en','ru','x-default']:
        ET.SubElement(el, '{'+xhtml+'}link', rel='alternate', hreflang=code, href=BASE+ROUTES['pl' if code=='x-default' else code])
ET.indent(tree, space='  '); tree.write(ROOT/'sitemap.xml',encoding='utf-8',xml_declaration=True)
print(f'Built 3 policy pages; updated {count} legal footers.')
