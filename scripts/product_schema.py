"""Shared Product/Offer normalization; no changes to visible content or SEO tags.

Base configurations at the published minimum prices were confirmed by the owner.
Shipping uses a truthful maximum rate, not a rate inferred from product price.
The basket-level free-shipping threshold must also be configured in Merchant Center.
New-device delivery times omit the incomplete handling/transit-only estimate.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://ltsmarket.pl'
SCHEMA = 'https://schema.org/'
STATUSES = {
    'used': {'availability': SCHEMA+'InStock', 'itemCondition': SCHEMA+'UsedCondition',
             'labels': {'pl': 'Dostępny od ręki', 'ru': 'В наличии', 'en': 'In stock'}},
    'new': {'availability': SCHEMA+'PreOrder', 'itemCondition': SCHEMA+'NewCondition',
            'labels': {'pl': 'Dostępny na zamówienie', 'ru': 'Доступен под заказ', 'en': 'Available to order'}},
}
POLICIES = {'pl': '/zwroty-i-reklamacje/', 'en': '/en/returns-and-warranty/',
            'ru': '/ru/vozvrat-i-garantiya/'}
NEW_ROUTES = {'pl': '/nowe/', 'en': '/en/new/', 'ru': '/ru/novye/'}
JSON_LD = re.compile(r'(<script\b[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)', re.S)


# Total business days, NOT carrier transit times. Do not infer a zero handling time.
SHIPPING = {'country': 'PL', 'currency': 'PLN', 'free_from': 35000,
            'total_business_days': {'used': (3, 7), 'new': (14, 30)},
            'handling_time': (2, 4), 'transit_time': (1, 3), 'rate_below_threshold': 700}
SHIPPING_COPY = {
    'pl': {
        'used': 'Urządzenia używane: 3–7 dni roboczych.',
        'new': 'Urządzenia nowe: 14–30 dni roboczych.',
        'free': 'Darmowa dostawa od 35 000 zł.',
        'below': 'Dostawa na terenie Polski: 700 zł dla zamówień poniżej 35 000 zł.'},
    'ru': {
        'used': 'Б/у оборудование: 3–7 рабочих дней.',
        'new': 'Новое оборудование: 14–30 рабочих дней.',
        'free': 'Бесплатная доставка от 35 000 zł.',
        'below': 'Доставка по Польше: 700 zł для заказов менее 35 000 zł.'},
    'en': {
        'used': 'Used equipment: 3–7 business days.',
        'new': 'New equipment: 14–30 business days.',
        'free': 'Free delivery for orders of PLN 35,000 or more.',
        'below': 'Delivery within Poland: PLN 700 for orders below PLN 35,000.'},
}


def shipping_cost(order_total, currency='PLN', country='PL'):
    """Confirmed order-level cost; None means unknown, never free by default."""
    if currency != SHIPPING['currency'] or country != SHIPPING['country']:
        return None
    return 0 if order_total >= SHIPPING['free_from'] else SHIPPING['rate_below_threshold']


def shipping_details(kind):
    """Google-supported upper bound; never derive basket value from offer.price.

    Direct OfferShippingDetails has no supported basket-value condition. Configure
    the exact 700/0 PLN rule in Merchant Center (or a separate ShippingService).
    New devices also wait for supply: do not publish 3-7 days as their full cycle.
    Weekdays/cutoff hours have not been confirmed, so no businessDays is invented.
    """
    details = {
        '@type': 'OfferShippingDetails',
        'shippingDestination': {'@type': 'DefinedRegion', 'addressCountry': SHIPPING['country']},
        'shippingRate': {'@type': 'MonetaryAmount', 'maxValue': SHIPPING['rate_below_threshold'],
                         'currency': SHIPPING['currency']},
    }
    if kind == 'used':
        def duration(bounds):
            return {'@type': 'QuantitativeValue', 'minValue': bounds[0],
                    'maxValue': bounds[1], 'unitCode': 'DAY'}
        details['deliveryTime'] = {
            '@type': 'ShippingDeliveryTime',
            'handlingTime': duration(SHIPPING['handling_time']),
            'transitTime': duration(SHIPPING['transit_time']),
        }
    return details


def shipping_copy(source, lang):
    products = [json.loads(m[2]) for m in JSON_LD.finditer(source)
                if json.loads(m[2]).get('@type') == 'Product']
    if len(products) != 1:
        return source
    kind = 'used' if products[0]['itemCondition'] == SCHEMA+'UsedCondition' else 'new'
    copy = SHIPPING_COPY[lang]
    cls = 'nowe-product__lead' if kind == 'used' else 'alpha-notice'
    block = '<p class="'+cls+'" data-shipping-info="true">'+'<br>'.join(copy[k] for k in (kind, 'free', 'below'))+'</p>'
    existing = r'<p\b[^>]*data-shipping-info="true"[^>]*>.*?</p>'
    if re.search(existing, source, re.S):
        return re.sub(existing, lambda _: block, source, flags=re.S)
    # Reuse the existing product information block and typography, without new sections.
    anchor = r'(<p class="'+cls+r'">.*?</p>)'
    source, count = re.subn(anchor, lambda m: m[0]+block, source, count=1, flags=re.S)
    if count != 1:
        raise ValueError('No existing product information block for delivery copy')
    return source


def seller(lang):
    # Google supports merchantReturnLink alone (Organization policy, option B).
    # The linked full policy preserves consumer exceptions and B2B distinctions.
    return {'@type': 'Organization', '@id': BASE+'/#organization',
            'name': 'LTS Market', 'url': BASE+'/',
            'hasMerchantReturnPolicy': {'@type': 'MerchantReturnPolicy',
                                        'merchantReturnLink': BASE+POLICIES[lang]}}


def normalize_node(node, lang):
    if isinstance(node, list):
        for item in node:
            normalize_node(item, lang)
    elif isinstance(node, dict):
        if node.get('@type') == 'Product':
            condition = node.get('itemCondition', node.get('offers', {}).get('itemCondition'))
            kind = 'used' if condition == SCHEMA+'UsedCondition' else 'new' if condition == SCHEMA+'NewCondition' else None
            if kind is None:
                raise ValueError('Product has no known condition: '+node.get('name', ''))
            offer = node['offers']
            if offer['@type'] == 'AggregateOffer':
                # One seller, confirmed purchasable base configuration, no independent offers.
                if node['name'] not in ('Alpha Mini', 'Alpha', 'Lumos'):
                    raise ValueError('Unconfirmed aggregate offer: '+node['name'])
                offer['price'] = offer.pop('lowPrice')
                offer.pop('highPrice', None)
                offer.pop('offerCount', None)
                offer['@type'] = 'Offer'
            if kind == 'new' and node['name'] == 'Lumos':
                # Old catalogue schema used an anchor instead of the actual product page.
                node['url'] = BASE+NEW_ROUTES[lang]+'lumos/'
                node['@id'] = node['url']+'#product'
                offer['url'] = node['url']
            node['itemCondition'] = STATUSES[kind]['itemCondition']
            offer.update({k: STATUSES[kind][k] for k in ('availability', 'itemCondition')})
            offer['seller'] = seller(lang)
            offer['shippingDetails'] = shipping_details(kind)
        for value in list(node.values()):
            normalize_node(value, lang)


def normalize_html(source):
    match = re.search(r'<html\b[^>]*lang="([^"]+)"', source)
    lang = match[1].split('-')[0] if match else 'pl'
    if lang not in POLICIES:
        return source
    def replace(match):
        obj = json.loads(match[2])
        original = json.dumps(obj, ensure_ascii=False)
        normalize_node(obj, lang)
        if json.dumps(obj, ensure_ascii=False) == original:
            return match[0]
        return match[1]+'\n'+json.dumps(obj, ensure_ascii=False, indent=2)+'\n'+match[3]
    source = JSON_LD.sub(replace, source)
    canonical = re.search(r'<link rel="canonical" href="([^"]+)"', source)
    if canonical and canonical[1] == BASE+POLICIES[lang]:
        marker = '<script type="application/ld+json" id="merchant-return-policy">'
        block = marker+json.dumps({'@context': SCHEMA.rstrip('/'), **seller(lang)}, ensure_ascii=False, indent=2)+'</script>\n'
        if marker in source:
            source = re.sub(re.escape(marker)+r'.*?</script>\n?', lambda _: block, source, flags=re.S)
        else:
            source = source.replace('</head>', block+'</head>')
    return shipping_copy(source, lang)


if __name__ == '__main__':
    changed = 0
    for path in ROOT.rglob('*.html'):
        source = path.read_text()
        updated = normalize_html(source)
        if source != updated:
            path.write_text(updated)
            changed += 1
    print(f'Product schema: updated {changed} HTML files')
