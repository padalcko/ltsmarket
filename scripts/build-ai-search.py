#!/usr/bin/env python3
"""Generate/check multilingual Markdown, discovery links and LLM resources."""
import argparse
from ai_resources import discover, outputs

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args(); pages=discover(); stale=[]
    expected_markdown={p['path'].with_suffix('.md') for p in pages}
    from ai_resources import ROOT
    for path in ROOT.rglob('*.md'):
        if '.git' in path.parts or path in expected_markdown: continue
        text=path.read_text()
        if any(label in text for label in ['\nŹródło HTML: [','\nHTML source: [','\nИсточник HTML: [']):
            raise SystemExit(f'Orphan Markdown requires review (not deleted): {path}')
    for path,content in outputs(pages).items():
        if not path.exists() or path.read_text()!=content:
            stale.append(str(path))
            if not args.check: path.write_text(content)
    if args.check and stale: raise SystemExit('Stale AI resources:\n'+'\n'.join(stale))
    print(f'PASS: {len(pages)} multilingual Markdown pages; '+('fresh' if args.check else f'{len(stale)} resources updated'))
