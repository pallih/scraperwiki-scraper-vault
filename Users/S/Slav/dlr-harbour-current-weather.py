###############################################################################
# Dun Laoghaire Harbour - CURRENT HARBOUR WEATHER
###############################################################################

import scraperwiki
import mechanize
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://www.dlharbour.ie/weather/index.php'
html = scraperwiki.scrape(starting_url)
#print html
soup = BeautifulSoup(html)

wdata = soup.find('div', { 'class' : 'wdata' })
print wdata

record = {}
lis = wdata.findAll('li')
for li in lis:
    val = li.text.split(':', 1)
    if len(val) > 1:
        record[val[0]] = val[1]

print record
# save records to the datastore
scraperwiki.sqlite.save(['Date', 'Time'], record) 