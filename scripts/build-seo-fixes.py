#!/usr/bin/env python3
"""Keep scoped static SEO and English price fixes reproducible."""
import json
import re
from pathlib import Path
from faq_schema import plain

ROOT = Path(__file__).resolve().parents[1]
SERVICE = {
    'en': ('Leasing and financing of professional beauty equipment',
           'Leasing and financing options for professional beauty equipment, including diode lasers and cosmetology devices. Financing applications are also available to newly established businesses, subject to individual assessment by the financing partner.'),
    'ru': ('Лизинг и финансирование профессионального косметологического оборудования',
           'Лизинг и финансирование профессионального косметологического оборудования, включая диодные лазеры и косметологические аппараты. Возможность подачи заявки на финансирование доступна также новым предприятиям. Окончательное решение зависит от индивидуальной оценки финансового партнёра.'),
}
PRICE = re.compile(r'(?<![\d,])([\d]{1,3}(?:[ \u00a0]\d{3})+)(?:([–-])([\d]{1,3}(?:[ \u00a0]\d{3})+))?\s*zł\b')
SCRIPT = re.compile(r'(<script\b[^>]*>.*?</script>)', re.S)


def english_prices(source):
    if '<body' not in source: return source
    head, body = source.split('<body', 1)
    def format_price(match):
        number = lambda value: f'{int(value.replace(" ", "").replace(chr(160), "")):,}'
        return 'PLN ' + number(match[1]) + (match[2] + number(match[3]) if match[3] else '')
    return head + '<body' + ''.join(part if part.startswith('<script') else PRICE.sub(format_price, part)
                                    for part in SCRIPT.split(body))


def schema(source, kind, update):
    def replace(match):
        data = json.loads(match[2])
        if data.get('@type') != kind: return match[0]
        update(data)
        return match[1] + json.dumps(data, ensure_ascii=False) + match[3]
    return re.sub(r'(<script\b[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)', replace, source, flags=re.S)


def write(path, transform):
    old = path.read_text()
    new = transform(old)
    if new != old: path.write_text(new)


home = ROOT/'en/index.html'
def clean_home(source):
    source = source.replace('<p>Використовувати наявні посилання на відповідні мовні версії сайту:</p><p>https://lasertechservice.pl/</p>', '')
    source = re.sub(r'<p>Не додавати вигаданих відгуків, рейтингів, Review або AggregateRating JSON-LD\.</p>', '', source)
    return english_prices(source)
write(home, clean_home)
write(ROOT/'index.html', lambda source: source.replace('<span>Technologie</span>\n            <span>które rozwijają</span>', '<span>Technologie,</span>\n            <span>które rozwijają</span>'))

for lang, (name, description) in SERVICE.items():
    write(ROOT/lang/'leasing.html', lambda source: schema(source, 'Service', lambda obj: obj.update(name=name, description=description)))

for lang in ('pl', 'ru'):
    path = ROOT/('index.html' if lang=='pl' else 'ru/index.html')
    write(path, lambda source: schema(source, 'FAQPage', lambda obj: [q.update(name=plain(q['name'])) for q in obj['mainEntity']]))

for path in (ROOT/'en').rglob('*.html'):
    if path != home: write(path, english_prices)
