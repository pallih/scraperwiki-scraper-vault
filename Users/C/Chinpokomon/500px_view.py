# Blank Python
sourcescraper = '500px-best'

print "This is a <em>fragment</em> of HTML." 

import scraperwiki           
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select(           
    '''* from swdata''' 
)
print data