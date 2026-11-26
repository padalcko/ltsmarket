"""FAQPage data derived from the visible question and answer pairs."""
import html
import json
import re


def plain(value):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', value))).strip()


def script(pairs):
    data = {'@context': 'https://schema.org', '@type': 'FAQPage',
            'mainEntity': [{'@type': 'Question', 'name': plain(question),
                            'acceptedAnswer': {'@type': 'Answer', 'text': plain(answer)}}
                           for question, answer in pairs]}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + '</script>\n'
