#!/usr/bin/env python3
"""Apply the shared GTM snippets to static pages; --check never writes."""
import argparse
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
HEAD = """<!-- Google Tag Manager -->
<script>
(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;
j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;
f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-T9T228H6');
</script>
<!-- End Google Tag Manager -->"""
BODY = """<!-- Google Tag Manager (noscript) -->
<noscript>
<iframe src="https://www.googletagmanager.com/ns.html?id=GTM-T9T228H6"
height="0" width="0" title="Google Tag Manager"
style="display:none;visibility:hidden"></iframe>
</noscript>
<!-- End Google Tag Manager (noscript) -->"""


def render(source):
    for snippet, tag in ((HEAD, 'head'), (BODY, 'body')):
        start, end = snippet.splitlines()[0], snippet.splitlines()[-1]
        source = re.sub(r'\n?' + re.escape(start) + r'.*?' + re.escape(end), '', source, flags=re.S)
        source, count = re.subn(r'<' + tag + r'\b[^>]*>', lambda m: m[0] + '\n' + snippet, source, count=1, flags=re.I)
        assert count == 1, f'Missing {tag}'
    assert source.count('GTM-T9T228H6') == 2, 'Unexpected duplicate GTM installation'
    return source


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    counts = {'pl': 0, 'en': 0, 'ru': 0}
    phones = 0
    for path in sorted(ROOT.rglob('*.html')):
        if any(part.startswith('.') for part in path.relative_to(ROOT).parts):
            continue
        source = path.read_text()
        if not re.search(r'<html\b', source, re.I):
            continue  # Search Console verification token is not a site page.
        output = render(source)
        assert output.count('src="/js/analytics.js"') == 1, path
        links = re.findall(r'href=[\"\'](tel:[^\"\']+)', output, re.I)
        assert all(link == 'tel:+48575254431' for link in links), path
        phones += len(links)
        lang = re.search(r'<html\s+lang="(\w+)"', source)[1]
        counts[lang] += 1
        if args.check:
            assert source == output, f'Run scripts/build-gtm.py: {path}'
        elif source != output:
            path.write_text(output)
    print(f'GTM: {counts}; {phones} valid telephone links; single GTM and existing GA4 per page')


if __name__ == '__main__':
    main()
