import scraperwiki
import urllib
import BeautifulSoup

xml = urllib.urlopen('http://www.fingalcoco.public-i.tv/core/data/2704/archived/1/future/1/agenda/1.xml')
doc = BeautifulSoup.BeautifulStoneSoup(xml)
for item in doc.findAll('item'):
    for elt in item:
        if isinstance(elt,BeautifulSoup.Tag):
            print(elt)   

scraperwiki.sqlite.save(["elt"],elt)