#!/usr/bin/env python3
"""Refresh AI resources from current HTML, then validate the static site.

Run the relevant product/blog generator first when editing its content source.
This command does not regenerate visible pages, commit or publish.
"""
import argparse
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--generate-only', action='store_true', help='Build generated artifacts without running the full site/SEO audit')
args = parser.parse_args()
scripts = ['product_schema.py','build-gtm.py','build-ai-search.py','build-ai-catalog.py']
if not args.generate_only:
    scripts += ['check-ai-search.py','audit-site.py','check-seo.py']
for script in scripts:
    subprocess.run([sys.executable,str(ROOT/'scripts'/script)],cwd=ROOT,check=True)
