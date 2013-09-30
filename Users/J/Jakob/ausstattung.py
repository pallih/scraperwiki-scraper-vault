import scraperwiki
import lxml.html
import re

import urllib2

URL = "http://www.berlin.de/sen/bildung/schulverzeichnis_und_portraets/anwendung/"

counte = 0
listpage = lxml.html.fromstring(scraperwiki.scrape(URL + "SchulListe.aspx"))
for tr in listpage.cssselect("#GridViewSchulen tr[class]"):
    try:
        tds = tr.cssselect("td")
        print tds[1].text_content()
        tmpID = int(tds[0].cssselect("a")[0].attrib.get("href").rsplit('=', 1)[1])
        link = tds[0].cssselect("a")[0].attrib.get("href")
        #detailhtml = scraperwiki.scrape(URL + link)
        detailhtml = urllib2.urlopen(URL + link, None, 20).read()
        detailpage = lxml.html.fromstring(detailhtml)
        conz = detailpage.cssselect("span#ctl00_ContentPlaceHolderMenuListe_lblAusstattung")
        if len(conz):
            data_list=[]
            print conz[0].text_content()
            amn = conz[0].text_content().split('; ')
            for i in amn:
                data = {'What' : i}
                data_list.append(data)
            scraperwiki.sqlite.save(unique_keys=['What'], data=data_list, table_name="ausstattung")
    except Exception, e:
        counte += 1
        print "Error:", e
print "Anzahl Fehler:"
print counte
import scraperwiki
import lxml.html
import re

import urllib2

URL = "http://www.berlin.de/sen/bildung/schulverzeichnis_und_portraets/anwendung/"

counte = 0
listpage = lxml.html.fromstring(scraperwiki.scrape(URL + "SchulListe.aspx"))
for tr in listpage.cssselect("#GridViewSchulen tr[class]"):
    try:
        tds = tr.cssselect("td")
        print tds[1].text_content()
        tmpID = int(tds[0].cssselect("a")[0].attrib.get("href").rsplit('=', 1)[1])
        link = tds[0].cssselect("a")[0].attrib.get("href")
        #detailhtml = scraperwiki.scrape(URL + link)
        detailhtml = urllib2.urlopen(URL + link, None, 20).read()
        detailpage = lxml.html.fromstring(detailhtml)
        conz = detailpage.cssselect("span#ctl00_ContentPlaceHolderMenuListe_lblAusstattung")
        if len(conz):
            data_list=[]
            print conz[0].text_content()
            amn = conz[0].text_content().split('; ')
            for i in amn:
                data = {'What' : i}
                data_list.append(data)
            scraperwiki.sqlite.save(unique_keys=['What'], data=data_list, table_name="ausstattung")
    except Exception, e:
        counte += 1
        print "Error:", e
print "Anzahl Fehler:"
print counte
