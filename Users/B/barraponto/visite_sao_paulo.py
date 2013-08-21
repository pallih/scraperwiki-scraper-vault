from lxml.html import parse
import scraperwiki

page = parse('http://www.visitesaopaulo.com/seu-evento.asp').getroot()

for event in page.cssselect('li.content'):

    data = {}

    data['title'] = event.cssselect('h4')[0].text_content()
    data['date'] = event.cssselect('.date')[0].text_content()
    data['local'] = event.cssselect('p')[0].text_content()

    scraperwiki.sqlite.save(['title'], data)
