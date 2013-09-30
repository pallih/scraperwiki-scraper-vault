import scraperwiki

# Blank Python
from urlparse import urljoin
import lxml.html


import datetime
import dateutil.parser
html = scraperwiki.scrape( "http://www.unitar.org/unosat/node/44/1261")
root = lxml.html.fromstring(html) 
for td in root.cssselect("div td br"):
   record = lxml.html.tostring(td)
   print record   


  import scraperwiki

# Blank Python
from urlparse import urljoin
import lxml.html


import datetime
import dateutil.parser
html = scraperwiki.scrape( "http://www.unitar.org/unosat/node/44/1261")
root = lxml.html.fromstring(html) 
for td in root.cssselect("div td br"):
   record = lxml.html.tostring(td)
   print record   


  