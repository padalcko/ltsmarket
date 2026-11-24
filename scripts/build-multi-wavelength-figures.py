#!/usr/bin/env python3
"""Generate localized conceptual diagrams for the multi-wavelength article."""
from pathlib import Path
from html import escape
from math import pi
ROOT=Path(__file__).resolve().parents[1]/'assets/img/blog/multi-wavelength'
C=['#D25D4B','#C09A54','#6386BA']
T={
'pl':{'selective-photothermolysis':['Selektywna fototermoliza','Naskórek','Skóra właściwa','Mieszek włosowy','Melanina','Promieniowanie laserowe','Rozprzestrzenianie ciepła'],'wavelength-penetration':['Względny rozkład promieniowania','Schemat poglądowy. Penetracja zależy od właściwości tkanek i parametrów urządzenia. Kolory umowne.'],'multi-wavelength-diode-stack':['Wielofalowy moduł diodowy','Grupy diod','Elementy optyczne','Wspólna powierzchnia robocza','Odprowadzanie ciepła','Schemat koncepcyjny; nie przedstawia konkretnego modelu.'],'laser-source-comparison':['Źródło promieniowania określa typ lasera','Laser aleksandrytowy','Laser diodowy','Laser Nd:YAG','Kryształ aleksandrytu i rezonator','Struktura półprzewodnikowa','Kryształ Nd:YAG i rezonator','Ta sama długość fali nie oznacza tego samego typu źródła.'],'wavelength-power-distribution':['Rozkład mocy optycznej','Głowica A','Głowica B','Hipotetyczny przykład matematyczny. Dane nie dotyczą konkretnego urządzenia.'],'clinical-research-results':['Wyniki badań klinicznych','2021 · 22 uczestników','2023 · 36 osób · bikini','2023 · 36 osób · pachy','2024 · 23 osoby','Wyniki odrębnych badań klinicznych. Różnice w protokołach, uczestnikach i okresach obserwacji uniemożliwiają bezpośrednie porównanie skuteczności urządzeń.']},
'ru':{'selective-photothermolysis':['Селективный фототермолиз','Эпидермис','Дерма','Волосяной фолликул','Меланин','Лазерное излучение','Распространение тепла'],'wavelength-penetration':['Относительное распределение излучения','Условная схема. Проникновение зависит от свойств тканей и параметров аппарата. Цвета условные.'],'multi-wavelength-diode-stack':['Многоволновой диодный модуль','Группы диодов','Оптические элементы','Общая рабочая поверхность','Отвод тепла','Концептуальная схема; не изображает конкретную модель.'],'laser-source-comparison':['Источник излучения определяет тип лазера','Александритовый лазер','Диодный лазер','Лазер Nd:YAG','Кристалл александрита и резонатор','Полупроводниковая структура','Кристалл Nd:YAG и резонатор','Одинаковая длина волны не означает одинаковый источник.'],'wavelength-power-distribution':['Распределение оптической мощности','Манипула A','Манипула B','Условный математический пример. Данные не относятся к конкретному аппарату.'],'clinical-research-results':['Результаты клинических исследований','2021 · 22 участника','2023 · 36 человек · бикини','2023 · 36 человек · подмышки','2024 · 23 участника','Результаты отдельных клинических исследований. Различия в протоколах, участниках и периодах наблюдения не позволяют напрямую сравнивать эффективность аппаратов.']},
'en':{'selective-photothermolysis':['Selective photothermolysis','Epidermis','Dermis','Hair follicle','Melanin','Laser radiation','Heat distribution'],'wavelength-penetration':['Relative light distribution','Conceptual illustration. Penetration depends on tissue properties and device parameters. Colours are illustrative.'],'multi-wavelength-diode-stack':['Multi-wavelength diode module','Diode groups','Optical elements','Shared treatment surface','Heat dissipation','Conceptual diagram; no specific device is shown.'],'laser-source-comparison':['The source determines the laser type','Alexandrite laser','Diode laser','Nd:YAG laser','Alexandrite crystal and resonator','Semiconductor structure','Nd:YAG crystal and resonator','The same wavelength does not mean the same laser source.'],'wavelength-power-distribution':['Optical power distribution','Handpiece A','Handpiece B','Hypothetical mathematical example. The figures do not represent a specific device.'],'clinical-research-results':['Clinical research results','2021 · 22 participants','2023 · 36 people · bikini','2023 · 36 people · axilla','2024 · 23 participants','Results from separate clinical studies. Differences in protocols, participants and follow-up periods prevent direct comparisons of device effectiveness.']}}
def txt(x,y,s,size=26,fill='#111923',weight=400,anchor='start'):
 return f'<text x="{x}" y="{y}" fill="{fill}" font-family="Arial,Helvetica,sans-serif" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(s)}</text>'
def shell(title,desc,body,h=720):
 return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 {h}" role="img" aria-labelledby="t d"><title id="t">{escape(title)}</title><desc id="d">{escape(desc)}</desc><rect width="1200" height="{h}" fill="#f4f7fa"/><rect x="24" y="24" width="1152" height="{h-48}" rx="24" fill="#fff" stroke="#dce2e8"/><path d="M56 113H1144" stroke="#dce2e8"/>{txt(60,82,title,34,'#111923',700)}{body}</svg>'''
for lang,D in T.items():
 dest=ROOT/lang;dest.mkdir(parents=True,exist_ok=True)
 # 1: skin layers and selective target
 a=D['selective-photothermolysis'];b='<defs><radialGradient id="heat"><stop stop-color="#D25D4B" stop-opacity=".65"/><stop offset="1" stop-color="#D25D4B" stop-opacity="0"/></radialGradient></defs>'
 b+='<rect x="80" y="205" width="680" height="90" rx="8" fill="#edd7bf"/><rect x="80" y="295" width="680" height="320" rx="8" fill="#f5e5d5"/><ellipse cx="405" cy="440" rx="155" ry="150" fill="url(#heat)"/><path d="M385 155 Q400 270 405 510 Q425 560 450 510 Q440 350 420 155Z" fill="#513c35"/><ellipse cx="426" cy="514" rx="47" ry="74" fill="none" stroke="#815d50" stroke-width="16"/><circle cx="420" cy="470" r="15" fill="#593c36"/><path d="M365 140V315" stroke="#168cff" stroke-width="14" stroke-dasharray="24 15" marker-end="url(#arrow)"/><defs><marker id="arrow" markerWidth="12" markerHeight="12" refX="6" refY="6" orient="auto"><path d="M0 0L12 6L0 12Z" fill="#168cff"/></marker></defs>'
 for y,s in zip([235,345,450,522,575,625],[a[1],a[2],a[6],a[3],a[4],a[5]]):b+=txt(800,y,s,24)
 (dest/'selective-photothermolysis.svg').write_text(shell(a[0],a[0],b))
 # 2: relative distribution (smooth fades, common follicles)
 a=D['wavelength-penetration'];b='<defs>'
 for i,c in enumerate(C):b+=f'<linearGradient id="g{i}" x2="0" y2="1"><stop stop-color="{c}" stop-opacity=".66"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></linearGradient>'
 b+='</defs>'
 for i,(x,depth) in enumerate(zip([75,435,795],[225,290,355])):
  b+=f'<rect x="{x}" y="210" width="300" height="355" rx="16" fill="#f5e5d5" stroke="#dce2e8"/><rect x="{x}" y="210" width="300" height="55" rx="14" fill="#edd7bf"/><ellipse cx="{x+150}" cy="285" rx="100" ry="{depth}" fill="url(#g{i})"/><path d="M{x+150} 220V440" stroke="#6b4b3d" stroke-width="13"/><ellipse cx="{x+150}" cy="452" rx="30" ry="55" fill="none" stroke="#6b4b3d" stroke-width="8"/>'
  b+=txt(x+150,170,['755 nm','808 nm','1064 nm'][i],31,C[i],700,'middle')
 b+=txt(600,628,a[1],18,'#485563',400,'middle') if len(a[1])<100 else txt(600,610,a[1][:85],18,'#485563',400,'middle')+txt(600,638,a[1][85:],18,'#485563',400,'middle')
 (dest/'wavelength-penetration.svg').write_text(shell(a[0],a[1],b))
 # 3: diode groups converging into shared optics
 a=D['multi-wavelength-diode-stack'];b=''
 for i,(y,c,label) in enumerate(zip([200,315,430],C,['755 nm','808 nm','1064 nm'])):
  b+=f'<rect x="115" y="{y}" width="250" height="72" rx="12" fill="{c}" fill-opacity=".12" stroke="{c}" stroke-width="3"/>'+txt(240,y+46,label,30,c,700,'middle')
  b+=f'<path d="M365 {y+36}L670 350" stroke="{c}" stroke-width="8" stroke-dasharray="18 10"/>'
 b+='<rect x="590" y="310" width="175" height="80" rx="16" fill="#e7f3ff" stroke="#168cff" stroke-width="4"/><rect x="870" y="240" width="90" height="220" rx="18" fill="#dce2e8" stroke="#68727d" stroke-width="4"/><path d="M765 350H870" stroke="#168cff" stroke-width="20"/><rect x="105" y="535" width="870" height="32" rx="8" fill="#9da9b5"/>'
 for x,y,s in [(115,165,a[1]),(590,285,a[2]),(815,495,a[3]),(130,605,a[4])]:b+=txt(x,y,s,22)
 b+=txt(600,680,a[5],20,'#485563',400,'middle')
 (dest/'multi-wavelength-diode-stack.svg').write_text(shell(a[0],a[5],b,h=720))
 # 4: source cards
 a=D['laser-source-comparison'];b=''
 for i,x in enumerate([65,440,815]):
  b+=f'<rect x="{x}" y="175" width="320" height="390" rx="20" fill="#f4f7fa" stroke="#dce2e8"/>'
  b+=txt(x+160,230,a[1+i],26,'#111923',700,'middle')+txt(x+160,285,['755 nm','755 / 808 / 1064 nm','1064 nm'][i],23,C[i],700,'middle')
  if i!=1:b+=f'<rect x="{x+120}" y="340" width="80" height="90" fill="{C[i]}" fill-opacity=".35" stroke="{C[i]}"/><path d="M{x+65} 385H{x+255}" stroke="{C[i]}" stroke-width="7"/>'
  else:b+=f'<path d="M{x+90} 355h140v80H{x+90}Z" fill="{C[i]}" fill-opacity=".25" stroke="{C[i]}"/><path d="M{x+105} 375h110M{x+105} 395h110M{x+105} 415h110" stroke="{C[i]}" stroke-width="6"/>'
  b+=txt(x+160,505,a[4+i],19,'#485563',400,'middle')
 b+=txt(600,638,a[7],22,'#485563',400,'middle')
 (dest/'laser-source-comparison.svg').write_text(shell(a[0],a[7],b,h=700))
 # 5: precise donut segments
 a=D['wavelength-power-distribution'];b=''
 for j,(cx,values) in enumerate([(315,[20,60,20]),(870,[10,50,40])]):
  r=112;circ=2*pi*r;offset=0
  b+=txt(cx,168,a[1+j],28,'#111923',700,'middle')
  for pct,c in zip(values,C):
   b+=f'<circle cx="{cx}" cy="338" r="{r}" fill="none" stroke="{c}" stroke-width="49" stroke-dasharray="{circ*pct/100:.5f} {circ*(100-pct)/100:.5f}" stroke-dashoffset="{-circ*offset/100:.5f}" transform="rotate(-90 {cx} 338)"/>'
   offset+=pct
  b+=txt(cx,350,'3000 W',33,'#111923',700,'middle')
  for i,(pct,w) in enumerate(zip(values,([600,1800,600] if j==0 else [300,1500,1200]))):
   b+=f'<circle cx="{cx-120}" cy="{520+i*34}" r="10" fill="{C[i]}"/>'+txt(cx-95,527+i*34,f'{[755,808,1064][i]} nm · {w} W · {pct}%',19)
 b+=txt(600,637,a[3],20,'#485563',400,'middle')
 (dest/'wavelength-power-distribution.svg').write_text(shell(a[0],a[3],b,h=680))
 # 6: 0-100 horizontal bars; chronology retained
 a=D['clinical-research-results'];b=''
 for i,(label,value) in enumerate(zip(a[1:5],[75.6,48.1,41.5,66])):
  y=205+i*95;b+=txt(70,y,label,22)
  b+=f'<rect x="410" y="{y-27}" width="600" height="32" rx="6" fill="#e9eef3"/><rect x="410" y="{y-27}" width="{600*value/100}" height="32" rx="6" fill="#6386BA"/>'+txt(1035,y,f'{value:g}%',24,'#111923',700)
 b+=txt(410,577,'0%',18)+txt(1010,577,'100%',18,'#111923',400,'end')
 from textwrap import wrap
 for line_no,line in enumerate(wrap(a[5],100)):
  b+=txt(600,615+line_no*20,line,16,'#485563',400,'middle')
 (dest/'clinical-research-results.svg').write_text(shell(a[0],a[5],b,h=680))
 print(lang,'6 SVG')
