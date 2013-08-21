from urllib2 import urlopen
from lxml.html import fromstring

MENU = "http://www.idph.state.il.us/about/nursing_home_violations/quarterlyreports.htm"

def parseMenu():
  x = fromstring(urlopen(MENU).read())
  years = x.xpath('//td[h3]')
  for year in years:
    h3s = year.xpath('h3/text()')
    assert 1 == len(h3s), h3s
    data = {"name":int(h3s[0])}
    

parseMenu()