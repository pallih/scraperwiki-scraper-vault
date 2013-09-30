#TODO clean data
import scraperwiki

sourcescraper = 'south_dakota_lobbyists_1'
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select('* from ' + sourcescraper + '.swdata')

#print data

for d in data:
    print d['lat_lon']
#print data#TODO clean data
import scraperwiki

sourcescraper = 'south_dakota_lobbyists_1'
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select('* from ' + sourcescraper + '.swdata')

#print data

for d in data:
    print d['lat_lon']
#print data