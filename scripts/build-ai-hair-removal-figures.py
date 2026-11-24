#!/usr/bin/env python3
"""Generate localized conceptual diagrams for the AI hair-removal article."""
from pathlib import Path
from html import escape
from textwrap import wrap
ROOT=Path(__file__).resolve().parents[1]/'assets/img/blog/ai-hair-removal'
LANG={
'pl':{
 'photo':['Fototyp i pomiar pigmentacji','Fototyp skóry','Reakcja na słońce','Pomiar optyczny','Indeks melaniny','Fototyp nie jest dokładnym pomiarem melaniny.'],
 'optical':['Optyczna analiza skóry','Źródło światła','Detektor','Pochłanianie i rozpraszanie','Światło powracające','Analiza sygnału'],
 'temp':['Punkty pomiaru temperatury','Moduł diodowy','Ciecz chłodząca','Okno szafirowe','Powierzchnia skóry','Sterownik','Schemat możliwych punktów pomiaru. Konstrukcja zależy od urządzenia.'],
 'auto':['Poziomy automatyzacji','Programy fabryczne','Algorytmy regułowe','Sprzężenie zwrotne','Uczenie maszynowe','Automatyzacja nie zawsze oznacza AI.'],
 'loop':['System wsparcia operatora','Ocena skóry i włosów','Analiza danych','Rekomendacja parametrów','Decyzja operatora','Wykonanie zabiegu','Dokumentacja','Czujniki','Kontrola parametrów','Ostrzeżenie lub blokada','Koncepcja systemu wspomagającego operatora.']},
'ru':{
 'photo':['Фототип и измерение пигментации','Фототип кожи','Реакция на солнце','Оптическое измерение','Индекс меланина','Фототип не является точным измерением меланина.'],
 'optical':['Оптический анализ кожи','Источник света','Детектор','Поглощение и рассеивание','Возвращающийся свет','Анализ сигнала'],
 'temp':['Точки измерения температуры','Диодный модуль','Охлаждающая жидкость','Сапфировое окно','Поверхность кожи','Контроллер','Схема возможных точек измерения. Конструкция зависит от аппарата.'],
 'auto':['Уровни автоматизации','Заводские программы','Алгоритмы на основе правил','Обратная связь','Машинное обучение','Автоматизация не всегда означает AI.'],
 'loop':['Система поддержки оператора','Оценка кожи и волос','Анализ данных','Рекомендация параметров','Решение оператора','Выполнение процедуры','Документация','Датчики','Контроль параметров','Предупреждение или блокировка','Концепция системы поддержки оператора.']},
'en':{
 'photo':['Phototype and pigmentation measurement','Skin phototype','Sun response','Optical measurement','Melanin index','Phototype is not an exact melanin measurement.'],
 'optical':['Optical skin analysis','Light source','Detector','Absorption and scattering','Returning light','Signal analysis'],
 'temp':['Temperature measurement points','Diode module','Coolant','Sapphire window','Skin surface','Controller','Possible measurement points. Architecture depends on the device.'],
 'auto':['Levels of automation','Factory presets','Rule-based algorithms','Feedback control','Machine learning','Automation does not always mean AI.'],
 'loop':['Operator support system','Skin and hair assessment','Data analysis','Parameter recommendation','Operator decision','Treatment','Documentation','Sensors','Parameter monitoring','Warning or interlock','Conceptual operator support system.']}}
BLUE='#168cff';INK='#111923';MUTED='#485563';BORDER='#dce2e8';LIGHT='#f4f7fa'
def text(x,y,s,size=23,weight=400,anchor='start',fill=INK):return f'<text x="{x}" y="{y}" fill="{fill}" font-family="Arial,Helvetica,sans-serif" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(s)}</text>'
def wrapped(x,y,s,limit=21,size=22,anchor='middle'):
 lines=wrap(s,limit,break_long_words=False)
 return ''.join(text(x,y+i*28,line,size,400,anchor) for i,line in enumerate(lines))
def panel(x,y,w,h):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{LIGHT}" stroke="{BORDER}" stroke-width="2"/>'
def shell(title,desc,body,h):return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 {h}" role="img" aria-labelledby="t d"><title id="t">{escape(title)}</title><desc id="d">{escape(desc)}</desc><rect width="1200" height="{h}" fill="{LIGHT}"/><rect x="24" y="24" width="1152" height="{h-48}" rx="24" fill="#fff" stroke="{BORDER}"/><path d="M56 113H1144" stroke="{BORDER}"/>{text(60,82,title,34,700)}{body}</svg>'
def save(lang,name,title,desc,body,h):
 p=ROOT/lang;p.mkdir(parents=True,exist_ok=True);(p/(name+'.svg')).write_text(shell(title,desc,body,h))
for lang,d in LANG.items():
 # 1: no fixed mapping from phototype to measured melanin.
 a=d['photo'];b=panel(60,155,510,390)+panel(630,155,510,390)
 b+=text(315,203,a[1],27,700,'middle')+text(885,203,a[3],27,700,'middle')
 shades=['#f2d7c7','#e8c1a8','#d6a181','#b77d5b','#8e5b43','#633f33']
 for i,(roman,colour) in enumerate(zip(['I','II','III','IV','V','VI'],shades)):
  x=90+i*75;b+=f'<rect x="{x}" y="260" width="62" height="125" rx="12" fill="{colour}" stroke="#986f5d"/>'+text(x+31,420,roman,22,700,'middle')
 b+=text(315,485,a[2],23,400,'middle',MUTED)
 b+=f'<rect x="845" y="240" width="80" height="55" rx="12" fill="#e7f3ff" stroke="{BLUE}" stroke-width="3"/><path d="M865 295L805 365M905 295L985 365" stroke="{BLUE}" stroke-width="5"/>'
 for i,(x,w) in enumerate([(710,130),(930,90)]):
  b+=f'<rect x="{x}" y="358" width="120" height="65" rx="10" fill="#c69370"/><rect x="{x}" y="448" width="180" height="18" rx="9" fill="#e0e8ef"/><rect x="{x}" y="448" width="{w}" height="18" rx="9" fill="{BLUE}"/>'
 b+=text(885,505,a[4],22,400,'middle',MUTED)+text(600,582,a[5],20,400,'middle',MUTED)
 save(lang,'phototype-vs-melanin',a[0],a[5],b,620)
 # 2: sensor, skin layers, paths, analysis block.
 a=d['optical'];b='<defs><marker id="arr" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0 0L10 5L0 10Z" fill="'+BLUE+'"/></marker></defs>'
 b+=panel(80,185,650,160)+panel(830,220,280,260)
 b+=f'<circle cx="240" cy="260" r="35" fill="#e7f3ff" stroke="{BLUE}" stroke-width="4"/><circle cx="550" cy="260" r="35" fill="#e7f3ff" stroke="{BLUE}" stroke-width="4"/>'
 b+=text(240,213,a[1],22,400,'middle')+text(550,213,a[2],22,400,'middle')
 b+='<rect x="80" y="430" width="650" height="65" rx="8" fill="#edd7bf"/><rect x="80" y="495" width="650" height="120" rx="8" fill="#f5e5d5"/>'
 b+=f'<path d="M240 295L310 470" stroke="{BLUE}" stroke-width="7" marker-end="url(#arr)"/><path d="M370 500L550 295" stroke="{BLUE}" stroke-width="7" stroke-dasharray="15 10" marker-end="url(#arr)"/><path d="M585 260H830" stroke="{BLUE}" stroke-width="7" marker-end="url(#arr)"/>'
 b+=wrapped(360,565,a[3],24,21)+wrapped(605,390,a[4],20,21)+wrapped(970,345,a[5],18,24)
 save(lang,'skin-optical-analysis',a[0],a[0],b,700)
 # 3: each point has an independent route to controller.
 a=d['temp'];b=panel(70,175,700,450)+panel(845,275,270,255)
 ys=[230,335,440,545];fills=['#e7f3ff','#e3eef3','#dce8f3','#f5e5d5']
 for i,(y,fill) in enumerate(zip(ys,fills)):
  b+=f'<rect x="105" y="{y}" width="620" height="75" rx="12" fill="{fill}" stroke="{BORDER}"/><circle cx="160" cy="{y+37}" r="20" fill="{BLUE}"/>'+text(160,y+44,f'T{i+1}',18,700,'middle','#fff')
  b+=text(210,y+46,a[1+i],23)+f'<path d="M725 {y+37}H800V{360+i*32}H845" fill="none" stroke="{BLUE}" stroke-width="3"/>'
 b+=wrapped(980,390,a[5],15,25)+text(600,698,a[6],19,400,'middle',MUTED)
 save(lang,'temperature-monitoring',a[0],a[6],b,750)
 # 4: equal information cards; no hierarchy/ranking.
 a=d['auto'];b=''
 for i,x in enumerate([55,345,635,925]):
  b+=panel(x,185,220,375)
  if i==0:b+=f'<path d="M{x+55} 290h115M{x+55} 330h115M{x+55} 370h115" stroke="{BLUE}" stroke-width="9" stroke-linecap="round"/>'
  elif i==1:b+=f'<rect x="{x+73}" y="273" width="74" height="45" rx="8" fill="#e7f3ff" stroke="{BLUE}"/><path d="M{x+110} 318v47m-38 0h76" stroke="{BLUE}" stroke-width="6"/><circle cx="{x+72}" cy="385" r="12" fill="{BLUE}"/><circle cx="{x+148}" cy="385" r="12" fill="{BLUE}"/>'
  elif i==2:b+=f'<circle cx="{x+110}" cy="335" r="62" fill="none" stroke="{BLUE}" stroke-width="8" stroke-dasharray="240 150"/><circle cx="{x+110}" cy="335" r="20" fill="{BLUE}"/>'
  else:
   for dx,dy in [(65,300),(110,270),(155,300),(65,375),(110,405),(155,375)]:b+=f'<circle cx="{x+dx}" cy="{dy}" r="9" fill="{BLUE}"/>'
   b+=f'<path d="M{x+65} 300L{x+110} 270L{x+155} 300M{x+65} 300L{x+110} 405L{x+155} 300M{x+65} 375L{x+110} 270L{x+155} 375M{x+65} 375L{x+110} 405L{x+155} 375" stroke="{BLUE}" stroke-width="3"/>'
  b+=wrapped(x+110,472,a[1+i],18,21)
 b+=text(600,625,a[5],22,400,'middle',MUTED)
 save(lang,'automation-levels',a[0],a[5],b,700)
 # 5: two-row process with operator as a distinct, mandatory step.
 a=d['loop'];b='<defs><marker id="arr" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0 0L10 5L0 10Z" fill="'+BLUE+'"/></marker></defs>'
 coords=[(65,180),(435,180),(805,180),(805,365),(435,365),(65,365)]
 for i,(x,y) in enumerate(coords):
  b+=f'<rect x="{x}" y="{y}" width="330" height="125" rx="18" fill="{"#e7f3ff" if i==3 else LIGHT}" stroke="{BLUE if i==3 else BORDER}" stroke-width="{4 if i==3 else 2}"/>'
  b+=wrapped(x+165,y+55,a[1+i],22,22)
 for x1,y1,x2,y2 in [(395,242,435,242),(765,242,805,242),(970,305,970,365),(805,427,765,427),(435,427,395,427)]:b+=f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{BLUE}" stroke-width="5" marker-end="url(#arr)"/>'
 for i,(x,s) in enumerate(zip([65,435,805],a[7:10])):
  b+=panel(x,595,330,90)+wrapped(x+165,648,s,25,21)
 for x1,x2 in [(395,435),(765,805)]:b+=f'<path d="M{x1} 640H{x2}" stroke="{BLUE}" stroke-width="4" marker-end="url(#arr)"/>'
 b+=f'<path d="M970 595V520H970" fill="none" stroke="{BLUE}" stroke-width="4" stroke-dasharray="12 9" marker-end="url(#arr)"/>'
 b+=text(600,785,a[10],20,400,'middle',MUTED)
 save(lang,'intelligent-control-loop',a[0],a[10],b,850)
 print(lang,'5 SVG')
