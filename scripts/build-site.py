#!/usr/bin/env python3
"""Regenerate scoped blog, product, SEO and AI resources, then optionally validate.

This command does not commit or publish.
"""
import argparse
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--generate-only', action='store_true', help='Build generated artifacts without running the full site/SEO audit')
args = parser.parse_args()
scripts = ['build-blog.py','build-alpha-mini.py','build-lumos.py','build-alpha-ray.py',
           'build-seo-fixes.py','product_schema.py','build-gtm.py','build-ai-search.py','build-ai-catalog.py']
if not args.generate_only:
    scripts += ['check-ai-search.py','audit-site.py','check-seo.py']
for script in scripts:
    subprocess.run([sys.executable,str(ROOT/'scripts'/script)],cwd=ROOT,check=True)
