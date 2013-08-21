import scraperwiki
from lxml.html import parse
import re

# Blank Python
url = "http://pnc.culturadigital.br/metas"

html = parse(url).getroot()

metas = html.cssselect('.interaction')
for m in metas:
    meta = {}
    meta['name'] = m.cssselect('h1 a')[0].text
    meta['numero'] = re.search('Meta ([0-9]{1,2}):',meta['name']).group(1)
    meta['comments-number'] = m.cssselect('.comments-number')[0].text
    meta['commenters-number'] = m.cssselect('.commenters-number')[0].text
    scraperwiki.sqlite.save(['name'], meta)
    print meta
