#!/usr/bin/env python3
"""Check AI freshness, source fidelity, discovery, local links and crawler access."""
import argparse
import collections
import hashlib
import importlib.util
import json
import re
from urllib.parse import urlsplit, unquote
from urllib.request import urlopen
from urllib.robotparser import RobotFileParser
import ai_resources as ai


def norm(text):
    return re.sub(r'[^\w]+','',text).casefold()


def excluded_ancestor(node):
    while node:
        if ai.excluded(node): return True
        node=node.parent
    return False


def check(http=None):
    pages=ai.discover(); counts=collections.Counter(); expected=ai.outputs(pages)
    spec=importlib.util.spec_from_file_location('catalog',ai.ROOT/'scripts/build-ai-catalog.py')
    catalog_module=importlib.util.module_from_spec(spec);spec.loader.exec_module(catalog_module)
    expected.update({ai.ROOT/k:v for k,v in catalog_module.generate().items()})
    for path,content in expected.items():
        assert path.is_file() and path.read_text()==content, ('stale',path)
    robot=RobotFileParser();robot.parse((ai.ROOT/'robots.txt').read_text().splitlines())
    catalog=json.loads((ai.ROOT/'ai-catalog.json').read_text())
    assert len(catalog['pages'])==len(pages)
    assert len({p['url'] for p in catalog['pages']})==len(pages)
    products=[p for p in pages if p['product']]
    assert len(catalog['products'])==len(products)
    assert len({p['product']['url'] for p in catalog['products']})==len(products)
    headers=(ai.ROOT/'_headers').read_text()
    markdown_paths={p['path'].with_suffix('.md') for p in pages}
    # Discovery comes from sitemap, never README, report or verification files.
    assert not any('reports' in p.parts or 'scripts' in p.parts for p in markdown_paths)
    for p in pages:
        md=(p['path'].with_suffix('.md')).read_text(); normalized=norm(md)
        assert md.startswith('# '+p['title']+'\n'),p['canonical']
        assert md.count('\n# ')==0,p['canonical']
        links=[n for n in p['tags'] if n.tag=='link']
        assert [n.attrs.get('href') for n in links if n.attrs.get('type')=='text/markdown']==[p['md']]
        assert [n.attrs.get('href') for n in links if n.attrs.get('rel')=='describedby']==['/llms.txt']
        assert p['canonical'] in md
        for lang,url in p['alternates'].items():
            if lang in ai.LANGUAGES and lang!=p['lang']:assert url in md
        # Every visible prose block/heading/table cell/FAQ question is represented.
        for n in p['main'].all():
            if n.tag in ['p','h1','h2','h3','h4','h5','h6','th','td','summary','li'] and not excluded_ancestor(n):
                if any(ai.excluded(child) for child in n.all()):continue
                value=norm(n.text())
                # Markdown link targets interrupt text; strip targets before comparing.
                body_text=re.sub(r'\]\([^\n]*?\)',']',md)
                assert not value or value in norm(body_text),(p['canonical'],'missing content',n.text())
                counts['content_blocks']+=1
        assert not re.search(r'<(?:input|form|script|textarea)\b',md,re.I),p['canonical']
        expected_header=f'{urlsplit(p["md"]).path}\n  Content-Type: text/markdown; charset=utf-8\n  X-Content-Type-Options: nosniff\n  Link: <{p["canonical"]}>; rel="canonical"'
        assert expected_header in headers,p['md']
        record=next(x for x in catalog['pages'] if x['url']==p['canonical'])
        assert record['contentSha256']==hashlib.sha256(md.encode()).hexdigest()
        assert record['structuredData']==p['schemas']
        if p['product']:
            product=next(x for x in catalog['products'] if x['product']['url']==p['canonical'])
            assert product['product']==p['product']
        for agent in ['Googlebot','Bingbot','OAI-SearchBot','ChatGPT-User','PerplexityBot']:
            for url in [p['canonical'],p['md']]:
                assert robot.can_fetch(agent,url),(agent,url)
                counts['crawler_checks']+=1
        counts['pages']+=1;counts[p['lang']]+=1
    for path,content in expected.items():
        if path.suffix not in ['.md','.txt']:continue
        for url in re.findall(r'\]\(([^\s]+)\)',content):
            parsed=urlsplit(url)
            if parsed.netloc!=urlsplit(ai.BASE).netloc:continue
            local=ai.ROOT/unquote(parsed.path).lstrip('/')
            if local.is_dir():local=local/'index.html'
            assert local.is_file(),(path,url)
            if parsed.fragment and local.suffix=='.html':
                ids={n.attrs.get('id') for n in ai.Parser(local.read_text()).root.all()}
                assert unquote(parsed.fragment) in ids,(path,url)
            counts['local_links']+=1
    for agent in ['Googlebot','OAI-SearchBot','ChatGPT-User','PerplexityBot']:
        for name in ['llms.txt','llms-full.txt','ai-catalog.json']:
            assert robot.can_fetch(agent,ai.BASE+'/'+name)
    if http:
        # Byte-level serving checks only. Generic local servers do not emulate _headers.
        for path,content in expected.items():
            if path.name=='_headers':continue
            relative=path.relative_to(ai.ROOT).as_posix()
            with urlopen(http.rstrip('/')+'/'+relative,timeout=10) as response:
                assert response.status==200 and response.read()==content.encode(),relative
            counts['http_resources']+=1
    print('PASS: AI resources '+json.dumps(counts,ensure_ascii=False))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--http',help='Optional local static server URL')
    check(parser.parse_args().http)
