"""Lumos supplied photography and localized commercial sections."""
import json
from pathlib import Path
from html import escape as e
ROOT=Path(__file__).resolve().parents[1]
IMAGES=json.loads((ROOT/'scripts/lumos-images.json').read_text())
def photo(index,lang,hero=False):
 item=IMAGES[index];v=item['variants'];large=v[-1]
 return f'<img src="{v[2]["src"]}" srcset="'+', '.join(f'{x["src"]} {x["width"]}w' for x in v)+f'" sizes="(max-width: 767px) calc(100vw - 40px), 600px" width="{large["width"]}" height="{large["height"]}" alt="{e(item["alt"][lang])}" '+('fetchpriority="high"' if hero else 'loading="lazy"')+' decoding="async">'
def gallery(lang):
 labels={'pl':['Poprzednie zdjęcie','Następne zdjęcie','Zamknij'],'en':['Previous image','Next image','Close'],'ru':['Предыдущее фото','Следующее фото','Закрыть']}[lang]
 items=''.join(f'<a href="{x["variants"][-1]["src"]}" data-lumos-image="{i}" aria-label="{e(x["alt"][lang])}">{photo(i,lang)}</a>' for i in [0,10,11,12,13,9,4,8,5,6,7,1,2,3,14,15] for x in [IMAGES[i]])
 return '<div class="lumos-gallery">'+items+'</div><dialog class="lumos-lightbox" aria-label="Lumos"><button type="button" data-close>'+labels[2]+'</button><figure>'+photo(0,lang)+'<figcaption></figcaption></figure><div><button type="button" data-prev>'+labels[0]+'</button><span data-count aria-live="polite"></span><button type="button" data-next>'+labels[1]+'</button></div></dialog>'
def extra(lang,alpha):
 post=next(p for p in json.loads((ROOT/'scripts/blog-posts.json').read_text())['posts'] if p['pl']['slug'].startswith('lumos-'))[lang]
 titles={
 'pl':['Lumos pamięta historię Twoich klientów','Nowoczesne oprogramowanie, które rozwija się razem z salonem','Dermatoskop — dodatkowe narzędzie pracy kosmetologa','Kupujesz Lumos. Otrzymujesz więcej niż laser.'],
 'en':['Lumos keeps your client history organised','Modern software designed to evolve with your clinic','Dermatoscope — an additional tool for beauty professionals','Buy Lumos. Get more than a laser.'],
 'ru':['Lumos помогает сохранять историю каждого клиента','Современное программное обеспечение, которое развивается вместе с салоном','Дерматоскоп — дополнительный инструмент косметолога','Покупая Lumos, вы получаете больше, чем лазер.']}[lang]
 result=''
 for n,(key,index) in enumerate([('CRM',3),('Android',14),('Derm',6)]):
  section=next(s for s in post['sections'] if key.lower() in s[0].lower() or key=='Derm' and s[0].startswith('Дерматоскоп'))
  parts=section[1].split('\n')
  selected=parts[-5:] if key=='CRM' else [parts[0],*parts[-2:]] if key=='Android' else parts[:4]
  paragraphs=''.join('<p>'+p+'</p>' for p in selected)
  result+=alpha.section(titles[n],'<div class="alpha-split lumos-photo-feature"><div class="alpha-copy">'+paragraphs+'</div><figure class="alpha-figure">'+photo(index,lang)+'</figure></div>',['crm','updates','dermatoscope'][n])
 prefix='' if lang=='pl' else '/'+lang
 benefits={
 'pl':['24 miesiące gwarancji i dostawa','Serwis i wsparcie techniczne','Strona wizytówkowa w prezencie','Leasing i finansowanie'],
 'en':['24-month warranty and delivery','Servicing and technical support','Complimentary business website','Leasing and financing'],
 'ru':['Гарантия 24 месяца и доставка','Сервис и техническая поддержка','Сайт-визитка в подарок','Лизинг и финансирование']}[lang]
 notes={
 'pl':['Gwarancja na warunkach umowy i dostawa pod drzwi w całej Polsce.','Laser Tech Service: diagnostyka, konserwacja i naprawy. Wsparcie również w weekendy, zgodnie z uzgodnionymi zasadami.','Raccoon Studio — od pomysłu do realizacji. Strona na pierwszy rok; pierwsze 3 miesiące wsparcia i promocji bezpłatnie. Dalsze wsparcie i promocja ze zniżkami na uzgodnionych warunkach.','Porozmawiaj o finansowaniu wybranej konfiguracji Lumos. Dostępność i warunki wymagają indywidualnego uzgodnienia.'],
 'en':['Warranty under the contract terms and door-to-door delivery across Poland.','Laser Tech Service: diagnostics, maintenance and repairs. Support including weekends, under the agreed arrangements.','Raccoon Studio — from concept to delivery. Website for the first year; free support and promotion for the first 3 months. Subsequent support and promotion at discounts on agreed terms.','Discuss financing for your chosen Lumos configuration. Availability and terms are agreed individually.'],
 'ru':['Гарантия на условиях договора и доставка до дверей по всей Польше.','Laser Tech Service: диагностика, обслуживание и ремонт. Поддержка также в выходные по согласованным правилам.','Raccoon Studio — от идеи до реализации. Сайт на первый год; первые 3 месяца поддержка и продвижение бесплатно. Дальнейшая поддержка и продвижение со скидками на согласованных условиях.','Обсудите финансирование выбранной комплектации Lumos. Доступность и условия согласовываются индивидуально.']}[lang]
 cards=alpha.cards(zip(benefits,notes)).replace('Raccoon Studio','<a href="https://raccoon-studio.com.ua/pl/">Raccoon Studio</a>')
 cards=cards.replace(e(benefits[3]),f'<a href="{prefix}/leasing.html">{e(benefits[3])}</a>')
 cards+=f'<p><a href="{prefix}/blog/{post["slug"]}/">{e(post["title"])}</a></p>'
 return result,alpha.section(titles[3],cards,'offer-benefits',True)
