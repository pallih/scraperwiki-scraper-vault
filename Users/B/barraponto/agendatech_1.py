import scraperwiki
from lxml.html import parse
from urlparse import urlparse

url = 'http://www.agendatech.com.br'

eventos = parse( url + '/eventos').getroot()

dados = []

for evento in eventos.cssselect('.evento'):
    dados.append({
        'id': evento.get('id'),
        'nome': evento.cssselect('#evento')[0].text_content(),
        'local': evento.cssselect('#evento + small')[0].text_content(),
        'data': evento.cssselect('.data')[0].text_content(),
        'url': url + evento.cssselect('#evento a')[0].get('href')  
    })

for evento in dados:
    page = parse(evento['url']).getroot()
    # a unica certeza no link do twitter eh que vem depois de um <span>
    for link in page.cssselect('.evento .info span + a'):
        parsedurl = urlparse(link.get('href'))
        if parsedurl.netloc == 'www.twitter.com' and len(parsedurl.path):
            evento['twitter'] = link.get('href')

scraperwiki.sqlite.save(['id'], dados)import scraperwiki
from lxml.html import parse
from urlparse import urlparse

url = 'http://www.agendatech.com.br'

eventos = parse( url + '/eventos').getroot()

dados = []

for evento in eventos.cssselect('.evento'):
    dados.append({
        'id': evento.get('id'),
        'nome': evento.cssselect('#evento')[0].text_content(),
        'local': evento.cssselect('#evento + small')[0].text_content(),
        'data': evento.cssselect('.data')[0].text_content(),
        'url': url + evento.cssselect('#evento a')[0].get('href')  
    })

for evento in dados:
    page = parse(evento['url']).getroot()
    # a unica certeza no link do twitter eh que vem depois de um <span>
    for link in page.cssselect('.evento .info span + a'):
        parsedurl = urlparse(link.get('href'))
        if parsedurl.netloc == 'www.twitter.com' and len(parsedurl.path):
            evento['twitter'] = link.get('href')

scraperwiki.sqlite.save(['id'], dados)