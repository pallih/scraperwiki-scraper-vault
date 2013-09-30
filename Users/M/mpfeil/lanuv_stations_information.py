import scraperwiki
import lxml.html
#from BeautifulSoup import BeautifulSoup

html = scraperwiki.scrape("http://www.lanuv.nrw.de/luft/temes/stat.htm")
root = lxml.html.fromstring(html)

table = root.cssselect("div#daten table tbody")

for el in table:
    print el.tag
    for el2 in el:
        print "--", el2.tag, el2.attrib




import scraperwiki
import lxml.html
#from BeautifulSoup import BeautifulSoup

html = scraperwiki.scrape("http://www.lanuv.nrw.de/luft/temes/stat.htm")
root = lxml.html.fromstring(html)

table = root.cssselect("div#daten table tbody")

for el in table:
    print el.tag
    for el2 in el:
        print "--", el2.tag, el2.attrib




