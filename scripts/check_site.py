"""Check the static site's local resources and content contract, without dependencies."""

from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import sys

ROOT = Path(__file__).resolve().parents[1]


class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.refs = []
        self.articles = []
        self.images = []
        self.labels = []
        self.structured = []
        self.in_structured = False

    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        if 'id' in attr:
            self.ids.append(attr['id'])
        for key in ('href', 'src'):
            if key in attr:
                self.refs.append(attr[key])
        for key in ('aria-labelledby', 'aria-controls'):
            self.labels.extend(attr.get(key, '').split())
        if tag == 'tr' and attr.get('data-work') in ('publication', 'report'):
            self.articles.append(attr)
        if tag == 'img':
            self.images.append(attr)
        if tag == 'script' and attr.get('type') == 'application/ld+json':
            self.in_structured = True

    def handle_data(self, data):
        if self.in_structured:
            self.structured.append(data)

    def handle_endtag(self, tag):
        if tag == 'script':
            self.in_structured = False


def main():
    html = (ROOT / 'index.html').read_text()
    site = SiteParser()
    site.feed(html)
    errors = []
    duplicates = [key for key, count in Counter(site.ids).items() if count > 1]
    if duplicates:
        errors.append(f'Duplicate IDs: {duplicates}')
    for ref in site.refs:
        url = urlsplit(ref)
        if not ref or ref == '#':
            errors.append('Empty or placeholder link')
        elif url.scheme or url.netloc:
            if url.scheme not in ('https', 'mailto'):
                errors.append(f'Unexpected external URL scheme: {ref}')
        elif url.path:
            target = (ROOT / unquote(url.path)).resolve()
            if not target.is_relative_to(ROOT) or not target.is_file():
                errors.append(f'Missing local resource: {ref}')
        elif url.fragment not in site.ids:
            errors.append(f'Missing anchor: {ref}')
    for label in site.labels:
        if label not in site.ids:
            errors.append(f'Missing accessibility target: {label}')
    for img in site.images:
        if not img.get('alt') or not img.get('width') or not img.get('height'):
            errors.append(f'Image needs alt text and dimensions: {img.get("src")}')
    selected = [item for item in site.articles if 'data-category' in item]
    reports = [item for item in site.articles if 'data-category' not in item]
    categories = Counter(item['data-category'] for item in selected)
    if categories != {'navigation': 6, 'vision-language': 4}:
        errors.append(f'Unexpected publication categories: {categories}')
    if len(selected) != 10:
        errors.append(f'Expected 10 selected works, found {len(selected)}')
    if [item.get('id') for item in reports] != ['agentic-world-modeling']:
        errors.append('Expected the world modeling report in its own section')
    if not selected or selected[-1].get('id') != 'maxsup':
        errors.append('MaxSup should be last in the selected publications')
    if 'trecvid' in site.ids:
        errors.append('The TRECVID paper should not appear in the web publication list')
    try:
        person = json.loads(''.join(site.structured))
        if person.get('name') != 'Yifei Dong' or person.get('email') != 'mailto:yfeidong@uw.edu':
            errors.append('Incorrect profile metadata')
    except (ValueError, TypeError):
        errors.append('Invalid structured profile metadata')
    cv = ROOT / 'assets/documents/Yifei_Dong_CV.pdf'
    if not cv.is_file() or not cv.read_bytes().startswith(b'%PDF-'):
        errors.append('CV missing or not a PDF')
    if errors:
        print('\n'.join(f'FAIL: {error}' for error in errors))
        return 1
    print(f'PASS: {len(selected)} selected works; {len(reports)} technical report; {len(site.images)} images; '
          f'{len(site.refs)} resource/link references; anchors, metadata, and CV.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
