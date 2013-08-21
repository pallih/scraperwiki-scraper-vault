import scraperwiki
from lxml.html import parse

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

scraperwiki.sqlite.save(['id'], dados)