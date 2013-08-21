import scraperwiki
import lxml.html
import random
import re
import urllib2

URL = "http://www.berlin.de/sen/bildung/schulverzeichnis_und_portraets/anwendung/"
skipped = []

def scrape_detail(id, i):
    try:
        detailsource = urllib2.urlopen(URL + "Schulportrait.aspx?IDSchulzweig=" + str(id), None, 6).read()
        detailpage = lxml.html.fromstring(detailsource)
        schulname = detailpage.cssselect("span#ctl00_ContentPlaceHolderMenuListe_lblSchulname")
        if len(schulname):
            print schulname[0].text_content()
    except Exception, e:
        skipped_tmp.append(id)
        print "Error: Schule", id, "bei Versuch", i, "ausgelassen -", e

listpage = lxml.html.fromstring(scraperwiki.scrape(URL + "SchulListe.aspx"))
skipped_tmp = []
xxcount = 200 #temp: anzahl beschränkt
for tr in listpage.cssselect("#GridViewSchulen tr[class]"):
    if xxcount > 0 and xxcount < 100 : #temp
        tds = tr.cssselect("td")
        id = int(tds[0].cssselect("a")[0].attrib.get("href").rsplit('=', 1)[1])
        scrape_detail(id, 1)
    xxcount -= 1 #temp
skipped = skipped_tmp
for i in range(2,11):
    if len(skipped):
        skipped_tmp = []
        for id in skipped:
            scrape_detail(id, i)
        skipped = skipped_tmp
print "auch bei Versuch 10 ausgelassen:", skipped
#ENDE
