"""Link visible service names without rewriting markup, attributes or structured data."""
import re
from pathlib import Path
from ai_resources import integration

SERVICE='Laser Tech Service'
LINK='<a class="service-name-link" href="https://lasertechservice.pl/">Laser Tech Service</a>'

def unlink_service_headings(source):
    """Keep service names as plain heading text; preserve every other link."""
    def heading(match):
        def anchor(link):
            label = re.sub(r'<[^>]+>', '', link[1]).strip()
            return link[1] if label == SERVICE else link[0]
        return re.sub(r'<a\b[^>]*>(.*?)</a\s*>', anchor, match[0], flags=re.S|re.I)
    return re.sub(r'<h([1-6])\b[^>]*>.*?</h\1\s*>', heading, source, flags=re.S|re.I)

def link_service_names(source):
    source = unlink_service_headings(source)
    # Preserve headings, existing links, metadata and raw text elements.
    pattern=r'(<!--.*?-->|<h[1-6]\b[^>]*>.*?</h[1-6]\s*>|<(?:script|style|title|textarea|option)\b[^>]*>.*?</(?:script|style|title|textarea|option)\s*>|<a\b[^>]*>.*?</a\s*>|<[^>]+>)'
    parts=re.split(pattern,source,flags=re.S|re.I)
    return integration(''.join(part if i%2 else part.replace(SERVICE,LINK) for i,part in enumerate(parts)))

if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]
    count=0
    for path in root.rglob('*.html'):
        source=path.read_text();updated=link_service_names(source)
        if updated!=source:path.write_text(updated);count+=1
    print(f'Linked visible service names in {count} pages')
