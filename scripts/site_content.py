"""Link visible service names without rewriting markup, attributes or structured data."""
import re
from pathlib import Path

SERVICE='Laser Tech Service'
LINK='<a class="service-name-link" href="https://lasertechservice.pl/">Laser Tech Service</a>'

def link_service_names(source):
    # Preserve existing links (including their destinations), metadata and raw text elements.
    pattern=r'(<!--.*?-->|<(?:script|style|title|textarea|option)\b[^>]*>.*?</(?:script|style|title|textarea|option)\s*>|<a\b[^>]*>.*?</a\s*>|<[^>]+>)'
    parts=re.split(pattern,source,flags=re.S|re.I)
    return ''.join(part if i%2 else part.replace(SERVICE,LINK) for i,part in enumerate(parts))

if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]
    count=0
    for path in root.rglob('*.html'):
        source=path.read_text();updated=link_service_names(source)
        if updated!=source:path.write_text(updated);count+=1
    print(f'Linked visible service names in {count} pages')
