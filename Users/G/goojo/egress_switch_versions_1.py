import scraperwiki

import lxml.html           
import re
import datetime

html = scraperwiki.scrape("https://reader.egress.com")
root = lxml.html.fromstring(html)

for meta in root.cssselect('meta'):
    name = meta.get('name')
    content = meta.get('content')
    if name=="generator":
        print 
        data = {"version": content.split("(c)")[0],
                "date": datetime.datetime.now()
        }
        scraperwiki.sqlite.save(unique_keys=['version'], data=data)


import scraperwiki

import lxml.html           
import re
import datetime

html = scraperwiki.scrape("https://reader.egress.com")
root = lxml.html.fromstring(html)

for meta in root.cssselect('meta'):
    name = meta.get('name')
    content = meta.get('content')
    if name=="generator":
        print 
        data = {"version": content.split("(c)")[0],
                "date": datetime.datetime.now()
        }
        scraperwiki.sqlite.save(unique_keys=['version'], data=data)


