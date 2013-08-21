from scraperwiki.sqlite import save
from lxml.html import fromstring
from urllib2 import urlopen

x=fromstring(urlopen('http://www.bom.gov.au/products/IDQ60901/IDQ60901.94580.shtml').read())

def tables(x):
  return x.xpath('//table[@class!="stationdetails"]')

def trs(table):
  return table.xpath('descendant::tr[td]')

def tds(tr):
  return tr.xpath('td')

def data(td):
  return [''.join(td.xpath('attribute::headers')),''.join(td.xpath('text()'))]


d=[[ dict([data(td) for td in tds(tr)]) for tr in trs(table)] for table in tables(x)]
table_names=[table.xpath('attribute::id')[0] for table in tables(x)]

for table in d:
  for row in table:
    if row.has_key(''):
      del(row[''])

map(save, [[],[],[],[]],d,table_names)