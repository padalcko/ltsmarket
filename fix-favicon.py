from pathlib import Path
import re

ROOT = Path(".")

NEW_FAVICON = """    <!-- FAVICON / APP ICONS -->
    <link rel="icon" href="/favicon.ico" sizes="any" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <link rel="icon" type="image/png" sizes="96x96" href="/favicon-96x96.png" />
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
    <link rel="manifest" href="/site.webmanifest" />
    <meta name="theme-color" content="#0b0f13" />
"""

pattern = re.compile(
    r'(?:\s*<!--.*?FAVICON.*?-->)?'
    r'\s*<link[^>]+rel=["\']icon["\'][^>]*>'
    r'(?:\s*<link[^>]+rel=["\']icon["\'][^>]*>)*'
    r'(?:\s*<link[^>]+rel=["\']apple-touch-icon["\'][^>]*>)?'
    r'(?:\s*<link[^>]+rel=["\']manifest["\'][^>]*>)?',
    re.IGNORECASE | re.DOTALL
)

changed = 0

for path in ROOT.rglob("*.html"):
    text = path.read_text(encoding="utf-8")

    if re.search(r'rel=["\']icon["\']', text, re.IGNORECASE):
        new_text, count = pattern.subn(
            "\n" + NEW_FAVICON,
            text,
            count=1
        )

        if count and new_text != text:
            path.write_text(new_text, encoding="utf-8")
            print(f"Updated: {path}")
            changed += 1

print(f"\nDone. Updated {changed} HTML files.")