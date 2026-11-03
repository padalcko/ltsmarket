#!/usr/bin/env python3
"""Refresh AI resources from current HTML, then validate the static site.

Run the relevant product/blog generator first when editing its content source.
This command does not regenerate visible pages, commit or publish.
"""
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
for script in ['build-ai-search.py','build-ai-catalog.py','check-ai-search.py','audit-site.py','check-seo.py']:
    subprocess.run([sys.executable,str(ROOT/'scripts'/script)],cwd=ROOT,check=True)
