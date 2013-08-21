import scraperwiki

r = scraperwiki.scrape("http://www.data.scec.org/recent/recenteqs/Quakes/quakes0.html")
from lxml import etree
from cStringIO import StringIO
parser = etree.HTMLParser()
tree   = etree.parse(StringIO(r),parser)

#xpath copied = /html/body/table/tbody/tr[3]/td[3]/pre[2]/a[2] so REMOVE TABLE!


event = tree.xpath('/html/body/table/tr[3]/td[3]/pre[2]/a[2]')[0]
print event.text
mag = tree.xpath('/html/body/table/tr[3]/td[3]/pre[2]/text()')[1]

info = event.text.split(' ')
data = {'mag':mag,
    'date':info.pop(),
    'time':info.pop(),
    'lat':info.pop(),
    'lon':info.pop(),
    'depth':info.pop()}

scraperwiki.sqlite.save(unique_keys=['date','time'], data=data)
