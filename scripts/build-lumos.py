#!/usr/bin/env python3
"""Render supplied Lumos copy using the unchanged Alpha Mini page components."""
import argparse
import html
import importlib.util
import json
import re
from pathlib import Path
from site_content import link_service_names
from lumos_visuals import illustration, wavelength_illustration

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://ltsmarket.pl'
ROUTES = {'pl':'/nowe/lumos/', 'en':'/en/new/lumos/', 'ru':'/ru/novye/lumos/'}
IMAGE = '/assets/img/nowe/lumos.webp'
spec = importlib.util.spec_from_file_location('alpha', ROOT/'scripts/build-alpha-mini.py')
alpha = importlib.util.module_from_spec(spec)
spec.loader.exec_module(alpha)
e = html.escape
META = {
 'pl': ('Lumos – laser diodowy 4 fale z serwisem | LTS Market', 'Lumos – profesjonalny laser diodowy 755/808/940/1064 nm. Moc głowicy 2000–4000 W, ICE Flow, FAC i wsparcie Laser Tech Service. Poznaj ofertę.'),
 'en': ('Lumos – Four-Wavelength Diode Laser | LTS Market', 'Discover Lumos, a professional four-wavelength diode laser with ICE Flow cooling, FAC optics and technical support from Laser Tech Service.'),
 'ru': ('Lumos – диодный лазер 4 волны | LTS Market', 'Lumos – профессиональный диодный лазер 755/808/940/1064 нм с охлаждением ICE Flow, технологией FAC и поддержкой Laser Tech Service.')}
LABELS = {
 'pl': ['Specyfikacja Lumos','Parametr','Wartość','Galeria Lumos','Lumos — laser diodowy z panelem sterowania i głowicą','Możliwości Lumos','Najczęstsze pytania','Zapytaj o Lumos','Konfiguracja i zakres funkcji wymagają potwierdzenia w indywidualnej ofercie oraz dokumentacji urządzenia.','Czytaj więcej o Lumos'],
 'en': ['Lumos Specifications','Parameter','Value','Lumos Gallery','Lumos diode laser with control panel and handpiece','Lumos Features','Frequently Asked Questions','Request a Lumos Quote','Configuration and feature availability must be confirmed in the individual quotation and device documentation.','Read more about Lumos'],
 'ru': ['Характеристики Lumos','Параметр','Значение','Галерея Lumos','Диодный лазер Lumos с панелью управления и манипулой','Возможности Lumos','Частые вопросы','Запросить предложение Lumos','Комплектацию и доступность функций необходимо подтвердить в индивидуальном предложении и документации аппарата.','Подробнее о Lumos']}
ROW_NAMES = {
 'pl':['Model','Kategoria','Pozycjonowanie','Cena','Moc głowicy','Długości fal','Energia','Częstotliwość','Czas impulsu','Chłodzenie','Optyka','Technologia higieniczna','Interfejs','CRM','Dermatoskop'],
 'en':['Model','Category','Positioning','Price','Handpiece power','Wavelengths','Energy','Frequency','Pulse duration','Cooling','Optics','Hygiene technology','Interface','CRM','Dermatoscope'],
 'ru':['Модель','Категория','Позиционирование','Цена','Мощность манипулы','Длины волн','Энергия','Частота','Длительность импульса','Охлаждение','Оптика','Гигиеническая технология','Интерфейс','CRM','Дерматоскоп']}

def plain(s): return re.sub(r'^#+ ', '', s).replace('**','')
def inline(s): return re.sub(r'\*\*(.*?)\*\*',r'<strong>\1</strong>',e(s))
def body(blocks, dark=False):
    out=''; i=0
    while i<len(blocks):
        b=blocks[i]
        if b.startswith('### ') and dark:
            entries=[]
            while i<len(blocks) and blocks[i].startswith('### '):
                entries.append((plain(blocks[i]),plain(blocks[i+1]))); i+=2
            out+=alpha.cards(entries); continue
        if b.startswith('### '): out+='<h3>'+inline(plain(b))+'</h3>'
        else: out+=('<p class="alpha-copy">' if dark else '<p>')+inline(b)+'</p>'
        i+=1
    return '<div class="alpha-copy">'+out+'</div>' if not dark else out

def photo(alt, hero=False):
    attrs='fetchpriority="high"' if hero else 'loading="lazy"'
    return f'<img src="{IMAGE}" srcset="/assets/img/nowe/lumos-laser-diodowy-4-fale-480.webp 480w, /assets/img/nowe/lumos-laser-diodowy-4-fale-800.webp 800w, {IMAGE} 1145w" sizes="(max-width: 767px) calc(100vw - 40px), (max-width: 1023px) 620px, 50vw" alt="{e(alt)}" width="1145" height="1374" {attrs} decoding="async">'

def generate():
    data=json.loads((ROOT/'scripts/lumos-content.json').read_text())
    for lang,blocks in data.items():
        prefix='' if lang=='pl' else '/'+lang
        source=(ROOT/alpha.ROUTES[lang].lstrip('/')/'index.html').read_text()
        head=source.split('</head>')[0]
        head=re.sub(r'<script type="application/ld\+json">.*?</script>','',head,flags=re.S)
        head+='\n<link rel="stylesheet" href="/css/lumos.css">\n'
        title,desc=META[lang]; labels=LABELS[lang]; hero=blocks[0]
        head=re.sub(r'<title>.*?</title>','<title>'+e(title)+'</title>',head)
        for key in ['description','og:description','twitter:description','og:title','twitter:title','og:image:alt','twitter:image:alt','og:url','og:image','twitter:image']:
            value=desc if 'description' in key else title if 'title' in key else labels[4] if ':alt' in key else BASE+ROUTES[lang] if key=='og:url' else BASE+IMAGE
            head=re.sub(r'(<meta (?:name|property)="'+key+r'" content=")[^"]*',lambda m:m[1]+e(value,quote=True),head)
        for l in ROUTES: head=head.replace(BASE+alpha.ROUTES[l],BASE+ROUTES[l])
        product={'@context':'https://schema.org','@type':'Product','@id':BASE+ROUTES[lang]+'#product','name':'Lumos','model':'Lumos','description':desc,'image':[BASE+IMAGE],'url':BASE+ROUTES[lang],'mainEntityOfPage':BASE+ROUTES[lang],'itemCondition':'https://schema.org/NewCondition','offers':{'@type':'AggregateOffer','lowPrice':68000,'highPrice':100000,'priceCurrency':'PLN','url':BASE+ROUTES[lang],'seller':{'@type':'Organization','name':'LTS Market','url':BASE+'/'}}}
        crumbjson=next(json.loads(x) for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>',source,re.S) if json.loads(x).get('@type')=='BreadcrumbList')
        crumbjson['itemListElement'][-1].update(name='Lumos',item=BASE+ROUTES[lang])
        for obj in [product,crumbjson]: head+='<script type="application/ld+json">'+json.dumps(obj,ensure_ascii=False,indent=2)+'</script>\n'
        chrome=source.split('</head>')[1].split('<main')[0]
        tail=source[source.index('<footer'):]
        for l in ROUTES:
            chrome=chrome.replace(alpha.ROUTES[l],ROUTES[l]); tail=tail.replace(alpha.ROUTES[l],ROUTES[l])
        crumb=re.search(r'<nav class="used-breadcrumbs".*?</nav>',source,re.S)[0].replace('Alpha Mini','Lumos')
        main='<main id="main-content" class="alpha-page lumos-page">'
        main+=f'<section class="nowe-hero"><div class="container nowe-hero__container"><div class="nowe-hero__content">{crumb}<p class="section-label nowe-hero__label">{inline(hero[0])}</p><h1 class="nowe-hero__title">{e(plain(hero[1]))}</h1><p class="nowe-hero__description">{inline(hero[2])}</p><p class="alpha-price">{inline(hero[3])}</p><p>{inline(hero[4])}</p><div class="nowe-hero__actions"><a class="button button--primary" href="#contact-form">{e(plain(hero[5]))}</a><a class="button button--outline" href="#specification">{e(plain(hero[6]))}</a></div><p class="alpha-notice">{inline(hero[7])}</p></div><div class="nowe-hero__visual">{photo(labels[4],True)}</div></div></section>'
        main+=alpha.section(plain(blocks[1][0]),body(blocks[1][1:]),'technology')
        # Reuse supplied headings and full descriptions for the reference benefit cards.
        benefits=[(plain(blocks[i][0]),plain(blocks[i][1])) for i in (3,4,5)]
        main+=alpha.section(labels[5],alpha.cards(benefits),'benefits',True)
        for i,id in [(2,'wavelengths'),(3,'power'),(4,'cooling'),(5,'fac'),(6,'neodez'),(7,'software'),(8,'audience')]:
            if 2 <= i <= 7:
                reverse=' lumos-feature--reverse' if i % 2 == 0 else ''
                copy=f'<div class="alpha-split__text lumos-feature__copy"><h2 class="nowe-section-title">{e(plain(blocks[i][0]))}</h2>{body(blocks[i][1:])}</div>'
                main+=f'<section class="nowe-intro" id="{id}"><div class="container alpha-split lumos-feature{reverse}">{copy}{wavelength_illustration(lang) if i==2 else illustration(lang,i-3)}</div></section>'
            else:
                main+=alpha.section(plain(blocks[i][0]),body(blocks[i][1:],dark=i==8),id,dark=i==8)
        note={'pl':'zależnie od konfiguracji','en':'depending on configuration','ru':'в зависимости от комплектации'}[lang]
        software={'pl':'zależnie od wersji oprogramowania','en':'depending on software version','ru':'в зависимости от версии ПО'}[lang]
        values=['Lumos',{'pl':'Profesjonalny laser diodowy','en':'Professional diode laser','ru':'Профессиональный диодный лазер'}[lang],'Premium','68 000–100 000 PLN','2000–4000 W — '+note,'755 / 808 / 940 / 1064 nm','10–240 J','1–30 Hz',{'pl':'Od 5 ms','en':'From 5 ms','ru':'От 5 мс'}[lang],'ICE Flow','FAC','NeoDez — '+note,'Android — '+software,software,note]
        table='<p class="alpha-copy">'+e(labels[8])+'</p><table class="alpha-spec"><caption>'+e(labels[0])+'</caption><thead><tr><th scope="col">'+labels[1]+'</th><th scope="col">'+labels[2]+'</th></tr></thead><tbody>'+''.join(f'<tr><th scope="row">{e(k)}</th><td>{e(v)}</td></tr>' for k,v in zip(ROW_NAMES[lang],values))+'</tbody></table>'
        main+=alpha.section(labels[0],table,'specification')
        main+=alpha.section(labels[3],f'<figure class="alpha-figure"><a href="{IMAGE}">{photo(labels[4])}</a><figcaption>{e(labels[4])}</figcaption></figure>','gallery')
        service=blocks[9]; url=service.index('https://lasertechservice.pl/')
        main+=alpha.section(plain(service[0]),body(service[1:url-1],True)+f'<a class="button button--primary" href="https://lasertechservice.pl/">{e(plain(service[url-1]))}</a>'+body(service[url+1:]),'service',True)
        price=blocks[10]
        main+=alpha.section(plain(price[0]),body(price[1:-2])+f'<div class="nowe-hero__actions"><a class="button button--primary" href="#contact-form">{e(plain(price[-2]))}</a><a class="button button--outline" href="#contact-form">{e(plain(price[-1]))}</a></div>','purchase')
        faq=blocks[11]
        main+=alpha.section(labels[6],'<div class="alpha-faq">'+''.join(f'<details><summary>{e(plain(q))}</summary><p>{inline(a)}</p></details>' for q,a in zip(faq[::2],faq[1::2]))+'</div>','faq')
        # Keep the same contact markup and localized handlers, including explicit product context.
        formsection=re.search(r'<section class="contact-form-section".*?</section>',source,re.S)[0]
        formsection=formsection.replace('Alpha Mini','Lumos').replace('alpha-mini','lumos')
        formsection=re.sub(r'<p class="alpha-notice">.*?</p>', '<p class="alpha-notice">'+inline(hero[7])+'</p>',formsection,flags=re.S)
        main+=formsection
        yield ROOT/ROUTES[lang].lstrip('/')/'index.html',link_service_names(head+'</head>'+chrome+main+'</main>\n'+tail)

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--check',action='store_true'); args=parser.parse_args()
    for path,content in generate():
        if args.check: assert path.read_text()==content, f'Stale {path}'
        else: path.parent.mkdir(parents=True,exist_ok=True); path.write_text(content)
    print('PASS: Lumos PL/EN/RU '+('fresh' if args.check else 'generated'))
