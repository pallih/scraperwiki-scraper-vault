import scraperwiki
import lxml.html
import itertools
import re

# Blank Python


base="http://www.bcn.cat/estadistica/angles/dades/tpob/llars/a%s/persones/person03.htm"

years=[1991,1996,2001,2004,2005,2006,2007,2008,2009,2010,2011,2012]

def get_data(y):
    h=scraperwiki.scrape(base%y)
    r=lxml.html.fromstring(h)
    table=r.cssselect("table")[0]
    rows=itertools.ifilter(lambda x: re.search("^[0-9]+",x.text_content()), table.cssselect("tr")[3:])
    for r in rows:
        d=r.cssselect("td")
        name=d[0].text_content().split(" ",1)[1]
        for n in range(1,10):
            hh=d[1+n].text_content().replace(".","")
            hh=int(hh)
            data={"year":y,
                  "name": name,
                  "housholds": hh,
                  "houshold_size": n,
                  "unique": "%s-%s-%s"%(y,name,n) }
            scraperwiki.sqlite.save(unique_keys=["unique"],data=data)


for y in years:
    try:
        get_data(y)
    except: 
        print "year %s not scraped!"%y