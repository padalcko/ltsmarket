#!/usr/bin/env python3
"""Render supplied Alpha/Ray copy with the current, unchanged Lumos template."""
import argparse
import importlib.util
import json
import re
from pathlib import Path
from html import escape as e
from site_content import link_service_names
from lumos_visuals import ART

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://ltsmarket.pl'
PREFIXES = {'pl': '/nowe/', 'en': '/en/new/', 'ru': '/ru/novye/'}
spec = importlib.util.spec_from_file_location('lumos', ROOT / 'scripts/build-lumos.py')
lumos = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lumos)
plain, inline, section = lumos.plain, lumos.inline, lumos.alpha.section


def route(lang, product):
    return PREFIXES[lang] + product + '/'


def photo(product, lang, hero=False):
    alt = {'pl': f'{product.title()} — laser diodowy z panelem sterowania i głowicą',
           'en': f'{product.title()} diode laser with control panel and handpiece',
           'ru': f'Диодный лазер {product.title()} с панелью управления и манипулой'}[lang]
    base = '/assets/img/nowe/' + product
    loading = 'fetchpriority="high"' if hero else 'loading="lazy"'
    return f'<img src="{base}.webp" srcset="{base}-laser-diodowy-480.webp 480w, {base}-laser-diodowy-800.webp 800w, {base}.webp 1145w" sizes="(max-width: 767px) calc(100vw - 40px), (max-width: 1023px) 620px, 50vw" alt="{e(alt)}" width="1145" height="1374" {loading} decoding="async">'


def body(blocks, headings=False, dark=False):
    if headings:
        blocks = ['### ' + plain(b) if b.startswith('**') and b.endswith('**') else b for b in blocks]
    return lumos.body(blocks, dark)


def diagram(product, lang, kind, number):
    # Reuse Lumos vector language. All panels are explicitly conceptual.
    labels = {
        'pl': {'power':'Parametry głowicy', 'cooling':'Chłodzenie', 'fac':'FAC', 'software':'Android · CRM', 'tips':'4 wymienne końcówki', 'stack':'12 barów laserowych', 'handpiece':'Ekran dotykowy głowicy'},
        'en': {'power':'Handpiece parameters', 'cooling':'Cooling', 'fac':'FAC', 'software':'Android · CRM', 'tips':'4 interchangeable tips', 'stack':'12 laser bars', 'handpiece':'Handpiece touchscreen'},
        'ru': {'power':'Параметры манипулы', 'cooling':'Охлаждение', 'fac':'FAC', 'software':'Android · CRM', 'tips':'4 сменные насадки', 'stack':'12 лазерных баров', 'handpiece':'Сенсорный экран манипулы'},
    }[lang]
    art = ART[{'power':0, 'cooling':1, 'fac':2, 'software':4}.get(kind, 0)]
    if kind == 'tips':
        art = ''.join(f'<rect x="{80+i*120}" y="155" width="80" height="135" rx="12" class="panel"/><rect x="{90+i*120}" y="140" width="60" height="30" rx="4" class="lens"/><text x="{120+i*120}" y="235" text-anchor="middle" fill="currentColor" font-size="28">{i+1}</text>' for i in range(4))
    elif kind == 'stack':
        art = ''.join(f'<rect x="155" y="{50+i*30}" width="290" height="18" rx="3" class="lens"/>' for i in range(12))
    elif kind == 'handpiece':
        art = '<rect x="200" y="55" width="200" height="340" rx="50" class="panel"/><rect x="235" y="110" width="130" height="120" rx="12" class="halo"/><path d="M255 150h90m-90 40h90" class="beam"/><circle cx="300" cy="300" r="20" class="knob"/>'
    values = {'power': ['1600–2000 W','180–220 J / 200 ms','12×20 mm'] if product == 'alpha' else ['1200 W','150 J','200 ms'],
              'cooling': ['TEC 1200 W' if product == 'alpha' else 'Freon 300 W'],
              'fac': ['Fast Axis Collimation'], 'software': ['Android','CRM',{'pl':'Dermatoskop','en':'Dermatoscope','ru':'Дерматоскоп'}[lang]],
              'tips':['1','2','3','4'], 'stack':['12 bar'], 'handpiece':[labels['handpiece']]}[kind]
    note = {'pl':'Schemat poglądowy technologii', 'en':'Conceptual technology illustration', 'ru':'Условная схема технологии'}[lang]
    metrics = ''.join('<div><strong>' + e(v) + '</strong></div>' for v in values)
    return f'<figure class="lumos-diagram"><div class="lumos-diagram__heading"><span>{product.upper()} / {number:02}</span><strong>{e(labels[kind])}</strong></div><svg viewBox="0 0 600 460" aria-hidden="true" focusable="false">{art}</svg><div class="lumos-diagram__metrics" style="grid-template-columns: repeat({len(values)}, minmax(0, 1fr))">{metrics}</div><figcaption>{note}</figcaption></figure>'


def rows(product, lang, price):
    names = {
        'pl':['Model','Typ','Pozycjonowanie','Cena','Moc głowicy','Energia / czas impulsu','Chłodzenie','Optyka','Okno zabiegowe','Funkcje','Końcówki','Stos diodowy','Głowica'],
        'en':['Model','Type','Positioning','Price','Handpiece power','Energy / pulse duration','Cooling','Optics','Treatment window','Features','Tips','Diode stack','Handpiece'],
        'ru':['Модель','Тип','Позиционирование','Цена','Мощность манипулы','Энергия / длительность импульса','Охлаждение','Оптика','Рабочее окно','Функции','Насадки','Диодная сборка','Манипула'],
    }[lang]
    category = {'pl':'Profesjonalny laser diodowy','en':'Professional diode laser','ru':'Профессиональный диодный лазер'}[lang]
    values = [product.title(),category,'Business' if product == 'alpha' else 'Compact',plain(price)]
    if product == 'alpha':
        values += ['1600–2000 W','180–220 J / 200 ms','TEC 1200 W','FAC','12×20 mm',
                   {'pl':'Android, CRM, dermatoskop, automatyczny dobór parametrów','en':'Android, CRM, dermatoscope, automatic parameter selection','ru':'Android, CRM, дерматоскоп, автоматический подбор параметров'}[lang]]
        keys = names[:10]
    else:
        values += ['1200 W','150 J / 200 ms','Freon 300 W','FAC',
                   {'pl':'4 wymienne','en':'4 interchangeable','ru':'4 сменные'}[lang],
                   {'pl':'12 barów laserowych (nie ciśnienie)','en':'12 laser bars (not pressure)','ru':'12 лазерных баров (не давление)'}[lang],
                   {'pl':'Ergonomiczna, z ekranem dotykowym','en':'Ergonomic, with touchscreen','ru':'Эргономичная, с сенсорным экраном'}[lang]]
        keys = names[:8] + names[10:]
    return list(zip(keys, values))


def generate():
    data = json.loads((ROOT/'scripts/alpha-ray-content.json').read_text())
    meta = json.loads((ROOT/'scripts/alpha-ray-meta.json').read_text())
    for product, translations in data.items():
        name = product.title()
        for lang, blocks in translations.items():
            path = route(lang, product)
            source = (ROOT/lumos.ROUTES[lang].lstrip('/')/'index.html').read_text()
            head = re.sub(r'<script type="application/ld\+json">.*?</script>', '', source.split('</head>')[0], flags=re.S)
            title, desc = meta[product][lang]
            head = re.sub(r'<title>.*?</title>', '<title>'+e(title)+'</title>', head)
            alt = re.search(r'alt="([^"]+)"', photo(product,lang))[1]
            for key in ['description','og:description','twitter:description','og:title','twitter:title','og:image:alt','twitter:image:alt','og:url','og:image','twitter:image']:
                value = desc if 'description' in key else title if 'title' in key else alt if ':alt' in key else BASE+path if key=='og:url' else BASE+'/assets/img/nowe/'+product+'.webp'
                head = re.sub(r'(<meta (?:name|property)="'+key+r'" content=")[^"]*', lambda m:m[1]+e(value,quote=True), head)
            for l in PREFIXES: head = head.replace(BASE+lumos.ROUTES[l], BASE+route(l,product))
            schemas = [json.loads(x) for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>', source, re.S)]
            prod = next(x for x in schemas if x.get('@type')=='Product')
            prod.update({'@id':BASE+path+'#product','name':name,'model':name,'description':desc,'image':[BASE+'/assets/img/nowe/'+product+'.webp'],'url':BASE+path,'mainEntityOfPage':BASE+path})
            prod['offers'] = {'@type':'AggregateOffer' if product=='alpha' else 'Offer', 'lowPrice' if product=='alpha' else 'price':60000 if product=='alpha' else 55000, 'priceCurrency':'PLN','url':BASE+path,'seller':{'@type':'Organization','name':'LTS Market','url':BASE+'/'}}
            crumbs = next(x for x in schemas if x.get('@type')=='BreadcrumbList')
            crumbs['itemListElement'][-1].update(name=name,item=BASE+path)
            for obj in [prod, crumbs]: head += '<script type="application/ld+json">'+json.dumps(obj,ensure_ascii=False,indent=2)+'</script>\n'
            chrome = source.split('</head>')[1].split('<main')[0]
            tail = source[source.index('<footer'):]
            for l in PREFIXES:
                chrome = chrome.replace(lumos.ROUTES[l],route(l,product))
                tail = tail.replace(lumos.ROUTES[l],route(l,product))
            crumb = re.search(r'<nav class="used-breadcrumbs".*?</nav>',source,re.S)[0].replace('Lumos',name)
            hero = blocks[0]
            main = '<main id="main-content" class="alpha-page lumos-page">'
            main += f'<section class="nowe-hero"><div class="container nowe-hero__container"><div class="nowe-hero__content">{crumb}<p class="section-label nowe-hero__label">{inline(hero[0])}</p><h1 class="nowe-hero__title">{e(plain(hero[1]))}</h1><p class="nowe-hero__description">{inline(hero[2])}</p><p class="alpha-price">{inline(hero[3])}</p><div class="nowe-hero__actions"><a class="button button--primary" href="#contact-form">{e(plain(hero[4]))}</a><a class="button button--outline" href="#specification">{e(plain(hero[5]))}</a></div><p class="alpha-notice">{inline(hero[6])}</p></div><div class="nowe-hero__visual">{photo(product,lang,True)}</div></div></section>'
            main += section(plain(blocks[1][0]),body(blocks[1][1:]),'technology')
            features = ['power','cooling','fac','software'] if product=='alpha' else ['tips','power','stack','fac','cooling','handpiece']
            labels = [x.replace('Lumos',name) for x in lumos.LABELS[lang]]
            benefits = [blocks[i] for i in ([2,3,5] if product=='alpha' else [2,3,7])]
            main += section(labels[5],lumos.alpha.cards([(plain(b[0]),plain(b[1])) for b in benefits]),'benefits',True)
            for i, kind in enumerate(features, 2):
                block = blocks[i]
                reverse = ' lumos-feature--reverse' if i%2==0 else ''
                copy = f'<div class="alpha-split__text lumos-feature__copy"><h2 class="nowe-section-title">{e(plain(block[0]))}</h2>{body(block[1:],headings=kind=="software")}</div>'
                main += f'<section class="nowe-intro" id="{kind}"><div class="container alpha-split lumos-feature{reverse}">{copy}{diagram(product,lang,kind,i-1)}</div></section>'
            audience = blocks[-4]
            main += section(plain(audience[0]),body(audience[1:],headings=True,dark=True),'audience',True)
            table = f'<table class="alpha-spec"><caption>{e(labels[0])}</caption><thead><tr><th scope="col">{labels[1]}</th><th scope="col">{labels[2]}</th></tr></thead><tbody>'+''.join(f'<tr><th scope="row">{e(k)}</th><td>{e(v)}</td></tr>' for k,v in rows(product,lang,hero[3]))+'</tbody></table>'
            main += section(labels[0],table,'specification')
            main += section(labels[3],f'<figure class="alpha-figure"><a href="/assets/img/nowe/{product}.webp">{photo(product,lang)}</a><figcaption>{alt}</figcaption></figure>','gallery')
            service = blocks[-3]; url = service.index('https://lasertechservice.pl/')
            main += section(plain(service[0]),body(service[1:url-1],dark=True)+f'<a class="button button--primary" href="https://lasertechservice.pl/">{e(plain(service[url-1]))}</a>'+body(service[url+1:]),'service',True)
            price = blocks[-2]
            main += section(plain(price[0]),body(price[1:-2])+f'<div class="nowe-hero__actions"><a class="button button--primary" href="#contact-form">{e(plain(price[-2]))}</a><a class="button button--outline" href="#contact-form">{e(plain(price[-1]))}</a></div>','purchase')
            faq = blocks[-1]
            main += section(labels[6],'<div class="alpha-faq">'+''.join(f'<details><summary>{e(plain(q))}</summary><p>{inline(a)}</p></details>' for q,a in zip(faq[::2],faq[1::2]))+'</div>','faq')
            form = re.search(r'<section class="contact-form-section".*?</section>',source,re.S)[0].replace('Lumos',name).replace('lumos',product)
            form = re.sub(r'<p class="alpha-notice">.*?</p>','<p class="alpha-notice">'+inline(hero[6])+'</p>',form,flags=re.S)
            main += form
            yield ROOT/path.lstrip('/')/'index.html', link_service_names(head+'</head>'+chrome+main+'</main>\n'+tail)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for path, content in generate():
        if args.check:
            assert path.read_text() == content, f'Stale {path}'
        else:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(content)
    print('PASS: Alpha/Ray PL/EN/RU '+('fresh' if args.check else 'generated'))
