import scraperwiki

# Blank Python

import re
import scraperwiki
import lxml.html

# IDs to loop through

committeeids = ['931', '10']

# Scrape!

for committeeid in committeeids:           
    html = scraperwiki.scrape(''.join(['https://secure.sos.state.or.us/orestar/publicAccountSummary.do?filerId=',committeeid]))           
    root = lxml.html.fromstring(html)
    tables = root.cssselect('table')
    for table in tables:
        for tr in table:
            tds = tr.cssselect('td')
    scraperwiki.sqlite.save(unique_keys=["a"], data={"a":1, "bbb":"Bye there"})

    print scraperwiki.sqlite.show_tables()      