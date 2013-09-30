import lxml.html
import scraperwiki
import urllib, urlparse
from dateutil import parser

years = ["02","03","04","05","06","07","08","09","10"]

url = 'http://www.uspto.gov/web/offices/ac/ido/oeip/taf/topo_%s.htm' %(years[8])

html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
selection = root.cssselect("h2.text="Part B"")

for i in selection:
    print lxml.html.tostring(i)import lxml.html
import scraperwiki
import urllib, urlparse
from dateutil import parser

years = ["02","03","04","05","06","07","08","09","10"]

url = 'http://www.uspto.gov/web/offices/ac/ido/oeip/taf/topo_%s.htm' %(years[8])

html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
selection = root.cssselect("h2.text="Part B"")

for i in selection:
    print lxml.html.tostring(i)