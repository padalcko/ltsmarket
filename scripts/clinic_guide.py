"""Static article fragments and progressively enhanced finance tools."""
from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / 'content/clinic-guide'
SCENARIOS = ((35000,3000,3000,2000,2000,1500,1500,12000),
             (70000,6000,12000,5000,3000,4000,2000,24000),
             (130000,12000,30000,10000,6000,8000,4000,40000))
FIXED = (2000,2500,600,1000,300,150,500,450)
SOURCE_URLS = (
 ('Biznes.gov.pl', 'https://www.biznes.gov.pl/'),
 ('Główny Urząd Statystyczny — PKD 2025', 'https://klasyfikacje.stat.gov.pl/static/pkd_25/pdf/KlasyfikacjaPKD2025.pdf'),
 ('Ministerstwo Zdrowia — komunikat 2026', 'https://www.gov.pl/web/zdrowie/komunikat-w-sprawie-wykonywania-procedur-medycyny-estetyczno-naprawczej'),
 ('Główny Inspektorat Sanitarny', 'https://www.gov.pl/web/gis/pytania-i-odpowiedzi2'),
 ('ZUS — składki', 'https://www.zus.pl/pl/firmy/rozliczenia-z-zus/skladki-na-ubezpieczenia'),
 ('Commission Implementing Regulation EU 2022/2347', 'https://eur-lex.europa.eu/eli/reg_impl/2022/2347/oj'),
 ('URPL', 'https://www.gov.pl/web/urpl'),
 ('Podatki.gov.pl — VAT', 'https://podatki.gov.pl/poradniki-i-informatory/zwolnienie-podmiotowe-od-podatku-vat'),
 ('LTS Market — katalog', 'https://ltsmarket.pl/nowe.html'),
 ('Laser Tech Service', 'https://lasertechservice.pl/'),
)
L = {
 'pl': {
  'check':'Checklista otwarcia gabinetu kosmetologicznego','reset':'Zresetuj','done':'Ukończono','complete':'Wszystkie kroki ukończone.',
  'items':['Przygotowanie biznesplanu.','Analiza lokalnej konkurencji.','Określenie budżetu.','Rejestracja działalności gospodarczej.','Wybór lokalu.','Weryfikacja wymagań sanitarnych i prawnych.','Wybór zakresu usług.','Zakup lub leasing urządzeń.','Weryfikacja dokumentacji urządzeń.','Szkolenie personelu.','Ubezpieczenie działalności.','Przygotowanie planu marketingowego.'],
  'cost':'Kalkulator kosztów otwarcia gabinetu','scenario':['Start ekonomiczny','Start profesjonalny','Rozbudowany biznes'],
  'cats':['Urządzenie','Czynsz i kaucja','Adaptacja lokalu','Meble','Szkolenia','Marketing','Koszty administracyjne','Rezerwa finansowa'],
  'total':'Inwestycja początkowa','other':'Pozostałe koszty','share':'Udział urządzenia','transfer':'Przenieś budżet do kalkulatora rentowności',
  'profit':'Kalkulator rentowności gabinetu depilacji laserowej',
  'fields':['Inwestycja początkowa','Średnia cena zabiegu','Zabiegi dziennie','Dni pracy w miesiącu','Koszt zmienny zabiegu','Wypłata dla właściciela','Rata finansowania'],
  'fixed':['Czynsz','ZUS i ubezpieczenie zdrowotne','Media','Marketing','Księgowość','Ubezpieczenie','Rezerwa serwisowa','Inne koszty'],
  'results':['Miesięczny przychód','Koszty operacyjne','Nadwyżka operacyjna','Środki po wypłacie właściciela i finansowaniu','Operacyjny próg rentowności','Próg pokrycia wypłaty i finansowania','Szacowany zwrot inwestycji'],
  'unreachable':'Próg nieosiągalny przy tej cenie i koszcie zmiennym','no_payback':'Brak dodatnich środków na zwrot','months':'mies.','treatments':'zabiegów/mies.',
  'chart':'Wykres rentowności','chart_desc':'Miesięczny przychód, nadwyżka operacyjna i dostępne środki w zależności od liczby zabiegów dziennie.','axis_x':'Zabiegi dziennie','axis_y':'PLN miesięcznie',
  'note':'Model nie uwzględnia PIT/CIT, pełnego rozliczenia VAT, sezonowości, inflacji ani nieprzewidzianych wydatków. Zakłada, że zabiegi wykonuje właściciel; koszt pracowników można dodać do innych kosztów. Przy leasingu inwestycja początkowa oznacza środki własne, a ratę wpisuje się osobno.',
  'model':'Modele demonstracyjne LTS Market, a nie statystyczne średnie ceny.','faq':'Najczęstsze pytania','sources':'Źródła i metodologia',
  'method':'Scenariusze są modelami demonstracyjnymi LTS Market. Ceny katalogowe odróżniono od założeń budżetowych. Kwoty ZUS z 2026 roku nie są stawkami zatwierdzonymi na 2027 rok. Kalkulatory nie gwarantują rentowności; materiał nie stanowi indywidualnej porady prawnej, podatkowej ani finansowej.',
  'cta':('Planujesz otworzyć własny gabinet?','Pomożemy Ci przeanalizować dostępne urządzenia, możliwości finansowania i koszty wyposażenia.','Skontaktuj się z nami','Zobacz urządzenia','Sprawdź leasing'),
  'links':{'nowe urządzenia':('Nowe urządzenia','/nowe.html'),'używane urządzenia':('Używane urządzenia','/uzywane.html'),'poradnik zakupu używanego lasera':('Poradnik zakupu używanego lasera','/blog/jak-kupic-uzywany-laser-do-depilacji-bez-ryzyka/'),'leasing LTS Market':('Leasing LTS Market','/leasing.html')},
 },
 'ru': {
  'check':'Чек-лист открытия косметологического кабинета','reset':'Сбросить','done':'Выполнено','complete':'Все шаги выполнены.',
  'items':['Подготовка бизнес-плана.','Анализ местных конкурентов.','Определение бюджета.','Регистрация бизнеса.','Выбор помещения.','Проверка санитарных и правовых требований.','Определение перечня услуг.','Покупка или лизинг оборудования.','Проверка документации оборудования.','Обучение персонала.','Страхование бизнеса.','Подготовка маркетингового плана.'],
  'cost':'Калькулятор стоимости открытия кабинета','scenario':['Экономный старт','Профессиональный старт','Расширенный бизнес'],
  'cats':['Оборудование','Аренда и депозит','Подготовка помещения','Мебель','Обучение','Маркетинг','Административные расходы','Финансовый резерв'],
  'total':'Начальные инвестиции','other':'Прочие расходы','share':'Доля оборудования','transfer':'Перенести бюджет в калькулятор окупаемости',
  'profit':'Калькулятор рентабельности кабинета лазерной эпиляции',
  'fields':['Начальные инвестиции','Средняя цена процедуры','Процедур в день','Рабочих дней в месяц','Переменные расходы на процедуру','Выплата владельцу','Платёж по финансированию'],
  'fixed':['Аренда','ZUS и медицинское страхование','Коммунальные услуги','Маркетинг','Бухгалтерия','Страхование','Резерв на сервис','Другие расходы'],
  'results':['Месячная выручка','Операционные расходы','Операционный остаток','Средства после выплаты владельцу и финансирования','Операционная безубыточность','Порог с учётом владельца и финансирования','Ориентировочная окупаемость'],
  'unreachable':'Безубыточность недостижима при этой цене и переменных расходах','no_payback':'Нет положительного остатка для окупаемости','months':'мес.','treatments':'процедур/мес.',
  'chart':'График рентабельности','chart_desc':'Месячная выручка, операционный остаток и доступные средства в зависимости от числа процедур в день.','axis_x':'Процедур в день','axis_y':'PLN в месяц',
  'note':'Модель не учитывает PIT/CIT, полный учёт VAT, сезонность, инфляцию и непредвиденные расходы. Предполагается, что процедуры выполняет владелец; расходы на персонал можно добавить к прочим расходам. При лизинге начальная инвестиция означает собственные вложенные средства, а платёж указывается отдельно.',
  'model':'Демонстрационные модели LTS Market, а не статистические средние цены.','faq':'Частые вопросы','sources':'Источники и методология',
  'method':'Сценарии являются демонстрационными моделями LTS Market. Каталожные цены отделены от бюджетных предположений. Суммы ZUS за 2026 год не являются утверждёнными ставками на 2027 год. Калькуляторы не гарантируют доходность; статья не заменяет индивидуальную юридическую, налоговую или финансовую консультацию.',
  'cta':('Планируете открыть собственный кабинет?','Поможем разобраться в оборудовании, возможностях финансирования и расходах на оснащение.','Связаться с нами','Посмотреть оборудование','Узнать о лизинге'),
  'links':{'новое оборудование':('Новое оборудование','/ru/nowe.html'),'подержанное оборудование':('Подержанное оборудование','/ru/uzywane.html'),'руководство по покупке подержанного лазера':('Руководство по покупке подержанного лазера','/ru/blog/kak-kupit-bu-lazer-dlya-epilyatsii-bez-riska/'),'лизинг LTS Market':('Лизинг LTS Market','/ru/leasing.html')},
 },
 'en': {
  'check':'Beauty Business Startup Checklist','reset':'Reset','done':'Completed','complete':'All steps completed.',
  'items':['Prepare a business plan.','Analyse local competitors.','Define the startup budget.','Register the business.','Select suitable premises.','Verify sanitary and legal requirements.','Define the service offering.','Purchase or lease equipment.','Verify equipment documentation.','Train staff.','Arrange business insurance.','Prepare a marketing plan.'],
  'cost':'Beauty Business Startup Cost Calculator','scenario':['Budget startup','Professional startup','Expanded business'],
  'cats':['Equipment','Rent and deposit','Premises adaptation','Furniture','Training','Marketing','Administrative expenses','Financial reserve'],
  'total':'Total startup investment','other':'Other costs','share':'Equipment share','transfer':'Transfer budget to profitability calculator',
  'profit':'Laser Hair Removal Business Profitability Calculator',
  'fields':['Initial investment','Average treatment price','Treatments per day','Working days per month','Variable cost per treatment','Owner withdrawal','Financing payment'],
  'fixed':['Rent','ZUS and health insurance','Utilities','Marketing','Accounting','Insurance','Service reserve','Other costs'],
  'results':['Monthly revenue','Operating expenses','Operating surplus','Cash after owner withdrawal and financing','Operating break-even','Cash break-even','Estimated investment payback'],
  'unreachable':'Break-even is unreachable at this price and variable cost','no_payback':'No positive cash available for payback','months':'months','treatments':'treatments/month',
  'chart':'Profitability chart','chart_desc':'Monthly revenue, operating surplus and available cash by treatments per day.','axis_x':'Treatments per day','axis_y':'PLN per month',
  'note':'The model excludes PIT/CIT, full VAT accounting, seasonality, inflation and unexpected costs. It assumes the owner performs treatments; staff costs can be added under other costs. Under leasing, initial investment means the owner’s own cash invested, with the financing payment entered separately.',
  'model':'Illustrative LTS Market models, not statistically established market averages.','faq':'Frequently asked questions','sources':'Sources and methodology',
  'method':'The scenarios are illustrative LTS Market models. Published catalogue prices are separate from budgeting assumptions. The 2026 ZUS figures are not approved 2027 rates. Calculators do not guarantee profitability; this article is not individual legal, tax or financial advice.',
  'cta':('Planning to open your own beauty studio?','We can help you explore equipment options, financing possibilities and startup equipment costs.','Contact us','Explore equipment','View leasing options'),
  'links':{'new equipment':('New equipment','/en/nowe.html'),'pre-owned equipment':('Pre-owned equipment','/en/uzywane.html'),'used laser buying guide':('Used laser buying guide','/en/blog/how-to-buy-a-used-hair-removal-laser-safely/'),'equipment leasing':('Equipment leasing','/en/leasing.html')},
 },
}

def money(n):
    return f'{n:,}'.replace(',', ' ')

def inline(s):
    return re.sub(r'\*\*(.+?)\*\*', lambda m: '<strong>'+m[1]+'</strong>', escape(s))

def checklist(lang):
    d=L[lang]
    items=''.join(f'<li><label><input type="checkbox" data-step="{i+1}"> {escape(v)}</label></li>' for i,v in enumerate(d['items']))
    return f'<div class="guide-tool" data-checklist><h3>{d["check"]}</h3><ol>{items}</ol><p role="status" data-check-status>{d["done"]}: 0/12 (0%)</p><progress value="0" max="12" aria-label="{d["check"]}"></progress><button type="button" data-check-reset>{d["reset"]}</button></div>'

def static_startup(lang):
    d=L[lang]
    heads=''.join(f'<th scope="col">{escape(v)}</th>' for v in d['scenario'])
    rows=''.join('<tr><th scope="row">'+escape(cat)+'</th>'+''.join(f'<td>{money(s[i])} PLN</td>' for s in SCENARIOS)+'</tr>' for i,cat in enumerate(d['cats']))
    rows+='<tr><th scope="row">'+d['total']+'</th>'+''.join(f'<td><strong>{money(sum(s))} PLN</strong></td>' for s in SCENARIOS)+'</tr>'
    bars=''.join(f'<div class="guide-budget-row"><span>{escape(label)} — {money(sum(s))} PLN</span><div class="guide-budget-bar" role="img" aria-label="{escape(label)}: {money(s[0])} PLN {d["cats"][0]}, {money(sum(s[1:]))} PLN {d["other"]}"><i style="width:{100*s[0]/240000:.2f}%"></i><b style="width:{100*sum(s[1:])/240000:.2f}%"></b></div></div>' for label,s in zip(d['scenario'],SCENARIOS))
    return f'<div class="guide-table"><table><thead><tr><th scope="col"></th>{heads}</tr></thead><tbody>{rows}</tbody></table></div><div class="guide-budget-static">{bars}</div><p class="guide-note">{d["model"]}</p>'

def cost_tool(lang):
    d=L[lang]
    buttons=''.join(f'<button type="button" data-scenario="{i}" aria-pressed="{str(i==0).lower()}">{escape(label)}</button>' for i,label in enumerate(d['scenario']))
    fields=''.join(f'<label>{escape(cat)}<input type="number" min="0" step="1" inputmode="decimal" data-cost="{i}" value="{SCENARIOS[0][i]}"></label>' for i,cat in enumerate(d['cats']))
    return f'<div class="guide-tool" data-cost-tool><h3>{d["cost"]}</h3><div class="guide-button-row">{buttons}</div><div class="guide-fields">{fields}</div><p class="guide-error" role="alert" data-cost-error></p><div class="guide-results"><p>{d["total"]}<strong data-cost-total>60 000 PLN</strong></p><p>{d["share"]}<strong data-cost-share>58%</strong></p><p>{d["other"]}<strong data-cost-other>25 000 PLN</strong></p></div><div class="guide-budget-bar guide-budget-live" role="img" aria-label="{d["total"]}"><i data-cost-equipment></i><b data-cost-rest></b></div><ul class="guide-legend">'+''.join(f'<li>{escape(v)}</li>' for v in d['cats'])+f'</ul><div class="guide-button-row"><button type="button" data-cost-reset>{d["reset"]}</button><button type="button" data-transfer>{d["transfer"]}</button></div></div>'

def profit_tool(lang):
    d=L[lang]
    defaults=(60000,200,3,22,20,4000,0)
    sliders={1:2000,2:30,3:31}
    fields=''
    for i,(name,value) in enumerate(zip(d['fields'],defaults)):
        slider=f'<input type="range" min="0" max="{sliders[i]}" step="1" data-range="{i}" value="{value}" aria-label="{escape(name)}">' if i in sliders else ''
        fields+=f'<label>{escape(name)}<input type="number" min="0" '+(f'max="{sliders[i]}" ' if i in sliders else '')+f'step="1" inputmode="decimal" data-profit="{i}" value="{value}">{slider}</label>'
    fields+='<fieldset class="guide-fixed"><legend>'+('Koszty stałe' if lang=='pl' else 'Постоянные расходы' if lang=='ru' else 'Fixed costs')+'</legend><div class="guide-fields">'
    fields+=''.join(f'<label>{escape(name)}<input type="number" min="0" step="1" inputmode="decimal" data-fixed="{i}" value="{value}"></label>' for i,(name,value) in enumerate(zip(d['fixed'],FIXED)))
    fields+='</div></fieldset>'
    results=''.join(f'<p>{escape(name)}<strong data-result="{i}">—</strong>'+('<small class="guide-result-state" data-cash-state></small>' if i==3 else '')+'</p>' for i,name in enumerate(d['results']))
    return f'<div class="guide-tool" data-profit-tool><h3>{d["profit"]}</h3><div class="guide-fields">{fields}</div><p class="guide-error" role="alert" data-profit-error></p><div class="guide-results">{results}</div><button type="button" data-profit-reset>{d["reset"]}</button><p class="guide-note">{d["note"]}</p></div>'

def static_profit(lang):
    d=L[lang]
    rows=''.join(f'<tr><th scope="row">{n}</th><td>{money(n*4400)} PLN</td><td>{money(n*3960-7500)} PLN</td><td>{money(n*3960-11500)} PLN</td></tr>' for n in range(1,8))
    return f'<div class="guide-table"><table><thead><tr><th scope="col">{d["axis_x"]}</th><th scope="col">{d["results"][0]}</th><th scope="col">{d["results"][2]}</th><th scope="col">{d["results"][3]}</th></tr></thead><tbody>{rows}</tbody></table></div><p class="guide-note">{d["model"]}</p>'

def chart(lang):
    d=L[lang]
    return f'<figure class="guide-tool guide-chart" data-chart><figcaption><h3>{d["chart"]}</h3><p data-chart-desc>{d["chart_desc"]}</p></figcaption><svg viewBox="0 0 640 360" role="img" aria-label="{d["chart_desc"]}" preserveAspectRatio="xMidYMid meet"><g data-chart-grid></g><path data-chart-line="revenue"></path><path data-chart-line="surplus"></path><path data-chart-line="cash"></path><text x="320" y="353" text-anchor="middle">{d["axis_x"]}</text><text x="8" y="20">{d["axis_y"]}</text></svg><div class="guide-chart-legend"><span>{d["results"][0]}</span><span>{d["results"][2]}</span><span>{d["results"][3]}</span></div></figure>'

def faq(lang):
    raw=(BASE / f'{lang}-faq.txt').read_text()
    pairs=[(h.strip(),a.strip()) for h,a in re.findall(r'^## (.+?)\n\n(.+?)(?=\n\n## |\Z)',raw,re.M|re.S)]
    html=''.join(f'<details><summary>{escape(h)}</summary><p>{escape(a)}</p></details>' for h,a in pairs)
    return pairs, '<div class="alpha-faq">'+html+'</div>'

def sources(lang):
    d=L[lang]
    links=''.join(f'<li><a href="{escape(url,quote=True)}" rel="noopener noreferrer">{escape(name)}</a></li>' for name,url in SOURCE_URLS)
    return f'<p>{escape(d["method"])}</p><ol>{links}</ol>'

def markdown_body(text):
    out=[]
    lines=text.strip().splitlines()
    i=0
    while i<len(lines):
        line=lines[i].strip()
        if not line:
            i+=1;continue
        if line.startswith('- '):
            items=[]
            while i<len(lines) and lines[i].startswith('- '):
                items.append('<li>'+inline(lines[i][2:])+'</li>');i+=1
            out.append('<ul>'+''.join(items)+'</ul>');continue
        out.append('<p>'+inline(line)+'</p>')
        i+=1
    return ''.join(out)

def article(lang):
    raw=(BASE/f'{lang}.txt').read_text()
    d=L[lang]
    raw=raw.split('\n',1)[1].strip()
    before,*chunks=re.split(r'(?=^## )',raw,flags=re.M)
    paragraphs=[p.strip() for p in before.split('\n\n') if p.strip()]
    lead=escape(paragraphs[0])
    intro=''.join('<p>'+escape(p)+'</p>' for p in paragraphs[1:])
    sections=[]
    for chunk in chunks:
        title,_,body=chunk.partition('\n')
        title=title[3:].strip()
        tokens=re.split(r'(\[(?:INTERACTIVE|STATIC TABLE|CONTEXTUAL LINK|CTA):[^\]]+\])',body)
        html=''
        for token in tokens:
            if token.startswith('[INTERACTIVE:'):
                kind=token[13:-1].strip()
                html+= {'startup-checklist':checklist,'startup-cost-calculator':cost_tool,'profitability-calculator':profit_tool,'profitability-chart':chart}[kind](lang)
            elif token.startswith('[STATIC TABLE:'):
                kind=token[14:-1].strip()
                html+= {'startup-scenarios':static_startup,'profitability-scenarios':static_profit}[kind](lang)
            elif token.startswith('[CONTEXTUAL LINK:'):
                key=token[17:-1].strip()
                if key.startswith('https://'):
                    label,url='Laser Tech Service',key
                else:
                    label,url=d['links'][key]
                html+=f'<p><a href="{escape(url,quote=True)}">{escape(label)} →</a></p>'
            elif token.startswith('[CTA:'):
                continue
            else:
                html+=markdown_body(token)
        sections.append((title,html))
    pairs,faq_html=faq(lang)
    sections.extend(((d['faq'],faq_html),(d['sources'],sources(lang))))
    return lead,intro,sections,pairs
