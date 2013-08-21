# Blank Python
sourcescraper = ''

import scraperwiki
scraperwiki.sqlite.attach("easyscrapper1")
data = scraperwiki.sqlite.select(
    '''* from easyscrapper1.swdata '''
)

for d in data:
    print d["h3"], "<br>"