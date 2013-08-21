from lxml.html import parse
from urlparse import parse_qs, urlparse
import scraperwiki

courses = []
url = 'http://www.ocw.unicamp.br/index.php?id=15'
tree = parse(url).getroot()
tree.make_links_absolute()

for row in tree.cssselect('.trAreaConhecimento'):
    area = row.text_content().strip()
    for link in row.getnext().cssselect('a'):
        text = link.text_content().strip().partition('-')
        courses.append({
            'code': text[0],
            'name': text[2],
            'area': area,
            'url': link.get('href'),
            'id': parse_qs(urlparse(link.get('href'))[4])['id'][0]
        })

scraperwiki.sqlite.save(['id'], courses)