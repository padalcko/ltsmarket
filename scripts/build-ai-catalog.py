#!/usr/bin/env python3
"""Derive the AI catalogue from sitemap-listed HTML, never from invented offers."""
import argparse
import hashlib
import json
from ai_resources import ROOT, BASE, discover, llms, markdown, render, clean


def generate():
    pages = discover()
    products = []
    records = []
    positions = {}
    for page in pages:
        if page['path'].name == 'uzywane.html':
            for schema in page['schemas']:
                if schema.get('@type') == 'ItemList':
                    for entry in schema['itemListElement']:
                        positions[entry['url']] = entry['position']
    for page in pages:
        source_text = clean(render(page['main'], page))
        records.append({
            'url': page['canonical'], 'markdownUrl': page['md'],
            'language': page['lang'], 'type': page['kind'], 'title': page['title'],
            'description': page['meta'].get('description', ''),
            'languageAlternates': page['alternates'],
            'contentSha256': hashlib.sha256(markdown(page).encode()).hexdigest(),
            'structuredData': page['schemas']})
        if not page['product']:
            continue
        record = {'language': page['lang'], 'product': page['product'],
                  'sourceUrl': page['canonical'], 'markdownUrl': page['md'],
                  'pageText': source_text}
        if page['canonical'] in positions:
            record['position'] = positions[page['canonical']]
        # Preserve the pre-existing nameplate/owner-confirmed MEDIflex facts.
        if page['path'].stem == 'mediflex-us450':
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
    data = {'site': BASE, 'scope': 'Canonical multilingual site pages and equipment',
            'sourceOfTruth': 'Canonical HTML listed in sitemap.xml',
            'languages': ['pl', 'en', 'ru'], 'pages': records, 'products': products}
    return {'ai-catalog.json': json.dumps(data, ensure_ascii=False, indent=2)+'\n',
            'llms.txt': llms(pages)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--check', action='store_true'); args = parser.parse_args()
    for name, content in generate().items():
        path = ROOT / name
        if args.check:
            assert path.exists() and path.read_text() == content, f'Stale {name}; run scripts/build-ai-catalog.py'
        else: path.write_text(content)
    print('PASS: AI catalogue and llms.txt ' + ('fresh' if args.check else 'generated'))
