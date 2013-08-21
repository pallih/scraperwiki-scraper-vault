import scraperwiki

import urllib
from lxml.html import fromstring, tostring

resp = urllib.urlopen("http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm")
html = fromstring(resp.read())

table = html.cssselect('table')[2]

rows = table.cssselect('tr')

for row in rows:
    print row

