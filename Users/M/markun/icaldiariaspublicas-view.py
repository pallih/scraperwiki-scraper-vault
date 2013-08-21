import scraperwiki
from icalendar import Calendar, Event, UTC
from datetime import datetime, date

sourcescraper = 'datasdediariascivis-br'
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select(           
    '''* from swdata'''
)

cal = Calendar()

cal.add('prodid', '-//THacker//Agenda Publica//BR')
cal.add('version', '2.0')
cal.add('calscale', 'GREGORIAN')
cal.add('method', 'PUBLISH')
cal.add('x-wr-calname', 'Agenda Publica')
cal.add('x-wr-timezone', 'America/Sao_Paulo')
cal.add('x-wr-caldesc', 'via Portal da Transparencia')

for evento in data:
    evento["inicio"] = evento["inicio"].strip("T00:00:00")
    evento["fim"] = evento["fim"].strip("T00:00:00")
    inicio = evento["inicio"].split("-")
    fim = evento["fim"].split("-")
    hoje = date.today()
    
    event = Event()
    valor = evento["valor"].replace(".", ",")
    event.add('summary', evento["favorecido"] + " - R$" + valor)
    event.add('description', "URL Original: " + evento["url"])
    if len(inicio[2]) == 1:
        inicio[2] = inicio[2] + "0"
    event.add('dtstart', date(int(inicio[0]),int(inicio[1]),int(inicio[2])))
    if len(fim[2]) == 1:
        fim[2] = fim[2] + "0"
    event.add('dtend', date(int(fim[0]),int(fim[1]),int(fim[2])))
    event.add('dtstamp', date.today())
    

    #event.add('created', datetime.today())
    event.add('last-modified', date.today())
    event.add('location', '')
    event.add('status', 'CONFIRMED')
    event.add('transp', 'TRANSPARENT')

    event['uid'] = str(evento["id"])+"/@thacker.com.br"
    cal.add_component(event)

print cal.as_string()