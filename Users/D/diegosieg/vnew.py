from lxml.html import parse
import scraperwiki

page = parse('http://www.tvbandvale.com.br/noticias.php').getroot()

for event in page.cssselect('.Fonte11'):

    data = {}

    data['tittle'] = event.cssselect('a')[0].text_content()   
    
    scraperwiki.sqlite.save(['tittle'], data)