# Blank Python
sourcescraper = 'aoa6_2'

import scraperwiki 
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select( '''* from swdata''' ) 

for d in data:
    print d['link'] + '<br>'


