#!/usr/bin/env python3
"""Derive equipment AI resources from the published HTML. No invented offers."""
import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://ltsmarket.pl'

class Text(HTMLParser):
    def __init__(self, source):
        super().__init__(); self.parts = []; self.feed(source)
    def handle_data(self, data):
        if data.strip(): self.parts.append(data.strip())


def generate():
    products = []
    lines = ['# LTS Market', '', '> New and used aesthetic equipment. Prices are in PLN.', '',
             '## Used equipment', '', 'Product pages are the source of truth for condition, price and service scope.',
             'Warranty on MEDIflex US450 covers completed Laser Tech Service work only, not the entire device.', '']
    for lang, prefix in [('pl', ''), ('en', '/en'), ('ru', '/ru')]:
        catalog = (ROOT / (prefix.lstrip('/') + '/' if prefix else '') / 'uzywane.html').read_text()
        listing = next(json.loads(x) for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>', catalog, re.S) if json.loads(x).get('@type') == 'ItemList')
        lines.append(f'### {lang.upper()}')
        for entry in listing['itemListElement']:
            path = ROOT / entry['url'].removeprefix(BASE + '/')
            source = path.read_text()
            product = next(json.loads(x) for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>', source, re.S) if json.loads(x).get('@type') == 'Product')
            main = re.search(r'<main\b.*?</main>', source, re.S)[0]
            record = {'language': lang, 'position': entry['position'], 'product': product,
                      'pageText': '\n'.join(Text(main).parts)}
            if path.stem == 'mediflex-us450':
                record['verifiedFacts'] = {
                    'commercialName': 'MEDIflex US450', 'model': 'US450', 'equipmentType': 'Diode Laser Machine',
                    'wavelengthsNm': [755, 808, 1064], 'declaredLaserDiodePowerW': 2000,
                    'maximumElectricalPowerConsumptionW': 5000, 'powerSupply': 'AC 220 V, 50/60 Hz',
                    'yearOfManufacture': 2022, 'fullyOperational': True, 'technicalCondition': 'good',
                    'lastMaintenanceDate': '2026-10-15', 'serviceCompany': 'Laser Tech Service',
                    'serviceWorkWarrantyMonths': 6, 'warrantyScope': 'Completed service work only; not the entire device',
                    'documentationBookletIncluded': True,
                    'serviceWork': ['All cooling system filters replaced', 'Cooling fluid fully replaced',
                        'Internal dust and dirt cleaned', 'Working handpiece inspected',
                        'Cooling component replaced', 'Operation checked after maintenance']}
            products.append(record)
            lines.append(f'- [{product["name"]}]({entry["url"]}): {product["description"]}')
        lines.append('')
    lines += ['## New equipment', '', 'Alpha Mini starts at PLN 40,000. Configuration, availability and service terms are agreed individually.', '']
    for lang, route in [('pl', '/nowe/alpha-mini/'), ('en', '/en/new/alpha-mini/'), ('ru', '/ru/novye/alpha-mini/')]:
        source = (ROOT / route.lstrip('/') / 'index.html').read_text()
        product = next(json.loads(x) for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>', source, re.S) if json.loads(x).get('@type') == 'Product')
        main = re.search(r'<main\b.*?</main>', source, re.S)[0]
        products.append({'language': lang, 'product': product, 'pageText': '\n'.join(Text(main).parts)})
        lines.append(f'- [{lang.upper()} Alpha Mini]({BASE}{route}): {product["description"]}')
    lines.append('')
    lines += ['## Machine-readable catalogue', '', '- [AI catalogue](https://ltsmarket.pl/ai-catalog.json)',
              '- [Sitemap](https://ltsmarket.pl/sitemap.xml)', '']
    return {'ai-catalog.json': json.dumps({'site': BASE, 'scope': 'New and used equipment', 'products': products}, ensure_ascii=False, indent=2)+'\n', 'llms.txt': '\n'.join(lines)}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--check', action='store_true'); args = parser.parse_args()
    for name, content in generate().items():
        path = ROOT / name
        if args.check:
            assert path.exists() and path.read_text() == content, f'Stale {name}; run scripts/build-ai-catalog.py'
        else: path.write_text(content)
    print('PASS: AI catalogue and llms.txt ' + ('fresh' if args.check else 'generated'))
