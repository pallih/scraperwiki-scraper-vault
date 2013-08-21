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
        conz = detailpage.cssselect("span#ctl00_ContentPlaceHolderMenuListe_lblSprachen")
        if len(conz):
            data_list = []
            amn = conz[0].text_content().split(', ')
            for i in amn:
                m = re.findall('^([1-4]\. Fremdsprache) (.*)$', i)
                if m:
                    data_list.append({'IDSchulzweig' : tmpID, 'FSName' : m[0][1], 'FSType' : m[0][0]})
                else:
                    m = re.findall('^S[1-8] (.*)/(.*)$', i)
                    if m:
                        data_list.append({'IDSchulzweig' : tmpID, 'FSName' : m[0][0], 'FSType' : '1. Fremdsprache'})
                        data_list.append({'IDSchulzweig' : tmpID, 'FSName' : m[0][1], 'FSType' : '2. Fremdsprache'})
                    else:
                        m = re.findall('^Fremdsprache ab Klasse 1 (.*)$', i)
                        if m:
                            data_list.append({'IDSchulzweig' : tmpID, 'FSName' : m[0], 'FSType' : 'ab Klasse 1'})
                        else:
                            data_list.append({'IDSchulzweig' : tmpID, 'FSName' : i, 'FSType' : 'undefined'})
            scraperwiki.sqlite.save(unique_keys=['IDSchulzweig', 'FSName', 'FSType'], data=data_list, table_name="schule_hat_fs")
    except Exception, e:
        counte += 1
        print "Error:", e
print "Anzahl Fehler:"
print counte
