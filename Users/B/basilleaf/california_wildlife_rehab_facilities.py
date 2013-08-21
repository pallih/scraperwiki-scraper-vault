import scraperwiki
import urllib2
from BeautifulSoup import BeautifulStoneSoup

# California dept of fish and game list of wildlife rehab facilities:
url = 'http://www.dfg.ca.gov/wildlife/WIL/rehab/facilities.html'

page = urllib2.urlopen(url).read()
soup = BeautifulStoneSoup(page)

cols = [str(c.contents[0]).lower() for c in soup.findAll('th')[0:6][1:]] # limit because some th's being misused
cols.append('scraperwiki_id') # add unique key field

data_flat = [t.contents[0] for t in soup.findAll('td')]
data = [data_flat[i:i+5] for i in range(0, len(data_flat), 5)]

for i, d in enumerate(data):
    d.append(i)  # add unique key
    entry = {v[0]:v[1] for k, v in enumerate(zip(cols, d))}
    scraperwiki.sqlite.save(unique_keys=['scraperwiki_id'], data=entry)
