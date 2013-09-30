import scraperwiki

sourcescraper = 'gaithersburg_crimes'

scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select("* from %s.swdata order by id" % sourcescraper) 

for record in data:
    address = record['address'] + ", Gaithersburg, MD"
    print address
import scraperwiki

sourcescraper = 'gaithersburg_crimes'

scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select("* from %s.swdata order by id" % sourcescraper) 

for record in data:
    address = record['address'] + ", Gaithersburg, MD"
    print address
