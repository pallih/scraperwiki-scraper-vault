sourcescraper = 'coned_outages'

import scraperwiki
import datetime           
scraperwiki.sqlite.attach("coned_outages")

data = scraperwiki.sqlite.select(           
    '''DISTINCT `Cause` FROM coned_outages.Detail'''
)

print "<html><head></head><body><ul>"

for index, row in enumerate(data):
    print "<li>"
    print row['Cause']
    print "</li>"

print "</ul></body></html>"