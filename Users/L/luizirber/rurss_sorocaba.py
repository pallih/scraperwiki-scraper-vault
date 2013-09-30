import scraperwiki

from pprint import pprint
from datetime import datetime
import rfc822


sourcescraper = 'ru-ufscar_sorocaba_1'


def build_date(theTime):
    data = rfc822.parsedate_tz(theTime.strftime("%a, %d %b %Y %H:%M:%S"))
    return rfc822.formatdate(rfc822.mktime_tz(data))


def build_desc(item):
    item.pop('data')
    item.pop('periodo')
    return ', '.join({item[tipo].rstrip() for tipo in item})

scraperwiki.sqlite.attach(sourcescraper)
data = scraperwiki.sqlite.execute('select * from swdata where data like ? order by data desc limit 10', datetime(2000, 1, 1).now().strftime('%d/%m/%Y'))

menu = []
for item in data['data']:
    menu.append(dict(zip(data['keys'], item)))

print '''<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0"><channel><title>RU UFSCar - Sorocaba</title><link>https://scraperwiki.com/scrapers/ru-ufscar_sorocaba_1</link><description></description>'''

print '''<lastBuildDate>%s</lastBuildDate>''' % (build_date(datetime(2000, 1, 1).now()))

for item in menu:
    title = 'Sorocaba - ' + item['data'] + ' - ' + item['periodo']
    link = 'http://www.sorocaba.ufscar.br/ufscar/?cardapio'
    guid = item['data'].replace('/', '') + item['periodo']
    date = datetime(*reversed([int(i) for i in item['data'].split('/')]))
    desc = build_desc(item)

    print '''<item><title>%s</title><link>%s</link>''' % (title, link),
    print '''<description>%s</description>''' % desc,
    print '''<guid isPermaLink="false">%s</guid>''' % guid,
    print '''<pubDate>%s</pubDate>''' % build_date(date),
    print '''</item>'''

print '''</channel></rss>'''
