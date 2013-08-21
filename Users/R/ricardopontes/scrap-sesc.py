from lxml.html import parse, HTMLParser
import scraperwiki

parser = HTMLParser(encoding='utf-8')

page = parse('http://www.sescsp.org.br/sesc/programa_new/busca.cfm', parser).getroot()

for box in page.cssselect('#box'):
    if box.cssselect('.tit a'):
        evento = {
            'title': box.cssselect('.tit a')[0].text_content(),
            'local': box.cssselect('.local')[0].text_content(),
            'url': box.cssselect('.tit a')[0].get('href')
        }
        scraperwiki.sqlite.save(['url'], evento)

nextpage = page.cssselect('.paginacao a')[0].get('href')
print nextpage
