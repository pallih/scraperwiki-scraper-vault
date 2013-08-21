import scraperwiki
import urllib2, urllib, urlparse
import re
import datetime
import httplib
import time
import mechanize
import lxml.html

url = "https://www.og.decc.gov.uk/pls/wons/wdep0100.qryWell"

def MakeTables():
    oilwellindexfields = ["quadrant text", "welltable text", "url text", "scrapedate text"]
    oilwellfields = ["quadrant text", "block text", "wellno text", "url text", "contents text", "scrapedate text"]

    scraperwiki.sqlite.execute("drop table if exists oilwellindex")
    scraperwiki.sqlite.execute("create table oilwellindex (%s, unique(quadrant, welltable))" % ",".join(oilwellindexfields))
    scraperwiki.sqlite.execute("drop table if exists oilwell")
    scraperwiki.sqlite.execute("create table oilwell (%s, unique(quadrant, block, wellno, contents))" % ",".join(oilwellfields))



def ScrapeIndexes():
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open(url)
    i = 0  
    while True:
        br.form = list(br.forms())[0]
        selectcontrol = br.form.find_control(name='f_quadNoList', type='select')
        if i >= len(selectcontrol.items):
            return None
        print i, len(selectcontrol.items)
        item = selectcontrol.items[i]
        quadrant = item.get_labels()[0].text
        selectcontrol.value = [quadrant]
        root = lxml.html.parse(br.submit()).getroot()
        welltable = root.cssselect("center table")[1]

        scraperwiki.sqlite.execute("insert or ignore into oilwellindex values (?,?,?,?)", 
                                   (quadrant, lxml.html.tostring(welltable), br.geturl(), datetime.datetime.now().isoformat()), verbose=0)

        i += 1
        scraperwiki.sqlite.commit()



def ScrapeNewPages():
    res = scraperwiki.sqlite.select("quadrant, welltable, url from oilwellindex")
    print len(res)
    for r in res:
        welltable = lxml.html.fromstring(r["welltable"])
        rows = welltable.cssselect("tr")
        assert [x.text  for x in rows[0].cssselect("td em")] == ['Quadrant/Block no', 'Well Numbers'], lxml.html.tostring(rows[0])
        print len(rows), r["quadrant"] 
        for row in rows[1:]:
            tdqb, cont = row.cssselect("td")
            tdq, tdb = tdqb.text.split("/")
            assert tdq == r["quadrant"]
            for a in cont.cssselect("a"):
                wellno = a.text
                url = urlparse.urljoin(r["url"], a.attrib.get("href"))
                contents = urllib.urlopen(url).read()
                scraperwiki.sqlite.execute("insert or ignore into oilwellfields values (?,?,?,?,?,?)", 
                                          (r["quadrant"], tdb, wellno, url, contents, datetime.datetime.now().isoformat()))

        scraperwiki.sqlite.commit()



#MakeTables()
#ScrapeIndexes()
ScrapeNewPages()
import scraperwiki
import urllib2, urllib, urlparse
import re
import datetime
import httplib
import time
import mechanize
import lxml.html

url = "https://www.og.decc.gov.uk/pls/wons/wdep0100.qryWell"

def MakeTables():
    oilwellindexfields = ["quadrant text", "welltable text", "url text", "scrapedate text"]
    oilwellfields = ["quadrant text", "block text", "wellno text", "url text", "contents text", "scrapedate text"]

    scraperwiki.sqlite.execute("drop table if exists oilwellindex")
    scraperwiki.sqlite.execute("create table oilwellindex (%s, unique(quadrant, welltable))" % ",".join(oilwellindexfields))
    scraperwiki.sqlite.execute("drop table if exists oilwell")
    scraperwiki.sqlite.execute("create table oilwell (%s, unique(quadrant, block, wellno, contents))" % ",".join(oilwellfields))



def ScrapeIndexes():
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open(url)
    i = 0  
    while True:
        br.form = list(br.forms())[0]
        selectcontrol = br.form.find_control(name='f_quadNoList', type='select')
        if i >= len(selectcontrol.items):
            return None
        print i, len(selectcontrol.items)
        item = selectcontrol.items[i]
        quadrant = item.get_labels()[0].text
        selectcontrol.value = [quadrant]
        root = lxml.html.parse(br.submit()).getroot()
        welltable = root.cssselect("center table")[1]

        scraperwiki.sqlite.execute("insert or ignore into oilwellindex values (?,?,?,?)", 
                                   (quadrant, lxml.html.tostring(welltable), br.geturl(), datetime.datetime.now().isoformat()), verbose=0)

        i += 1
        scraperwiki.sqlite.commit()



def ScrapeNewPages():
    res = scraperwiki.sqlite.select("quadrant, welltable, url from oilwellindex")
    print len(res)
    for r in res:
        welltable = lxml.html.fromstring(r["welltable"])
        rows = welltable.cssselect("tr")
        assert [x.text  for x in rows[0].cssselect("td em")] == ['Quadrant/Block no', 'Well Numbers'], lxml.html.tostring(rows[0])
        print len(rows), r["quadrant"] 
        for row in rows[1:]:
            tdqb, cont = row.cssselect("td")
            tdq, tdb = tdqb.text.split("/")
            assert tdq == r["quadrant"]
            for a in cont.cssselect("a"):
                wellno = a.text
                url = urlparse.urljoin(r["url"], a.attrib.get("href"))
                contents = urllib.urlopen(url).read()
                scraperwiki.sqlite.execute("insert or ignore into oilwellfields values (?,?,?,?,?,?)", 
                                          (r["quadrant"], tdb, wellno, url, contents, datetime.datetime.now().isoformat()))

        scraperwiki.sqlite.commit()



#MakeTables()
#ScrapeIndexes()
ScrapeNewPages()
import scraperwiki
import urllib2, urllib, urlparse
import re
import datetime
import httplib
import time
import mechanize
import lxml.html

url = "https://www.og.decc.gov.uk/pls/wons/wdep0100.qryWell"

def MakeTables():
    oilwellindexfields = ["quadrant text", "welltable text", "url text", "scrapedate text"]
    oilwellfields = ["quadrant text", "block text", "wellno text", "url text", "contents text", "scrapedate text"]

    scraperwiki.sqlite.execute("drop table if exists oilwellindex")
    scraperwiki.sqlite.execute("create table oilwellindex (%s, unique(quadrant, welltable))" % ",".join(oilwellindexfields))
    scraperwiki.sqlite.execute("drop table if exists oilwell")
    scraperwiki.sqlite.execute("create table oilwell (%s, unique(quadrant, block, wellno, contents))" % ",".join(oilwellfields))



def ScrapeIndexes():
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open(url)
    i = 0  
    while True:
        br.form = list(br.forms())[0]
        selectcontrol = br.form.find_control(name='f_quadNoList', type='select')
        if i >= len(selectcontrol.items):
            return None
        print i, len(selectcontrol.items)
        item = selectcontrol.items[i]
        quadrant = item.get_labels()[0].text
        selectcontrol.value = [quadrant]
        root = lxml.html.parse(br.submit()).getroot()
        welltable = root.cssselect("center table")[1]

        scraperwiki.sqlite.execute("insert or ignore into oilwellindex values (?,?,?,?)", 
                                   (quadrant, lxml.html.tostring(welltable), br.geturl(), datetime.datetime.now().isoformat()), verbose=0)

        i += 1
        scraperwiki.sqlite.commit()



def ScrapeNewPages():
    res = scraperwiki.sqlite.select("quadrant, welltable, url from oilwellindex")
    print len(res)
    for r in res:
        welltable = lxml.html.fromstring(r["welltable"])
        rows = welltable.cssselect("tr")
        assert [x.text  for x in rows[0].cssselect("td em")] == ['Quadrant/Block no', 'Well Numbers'], lxml.html.tostring(rows[0])
        print len(rows), r["quadrant"] 
        for row in rows[1:]:
            tdqb, cont = row.cssselect("td")
            tdq, tdb = tdqb.text.split("/")
            assert tdq == r["quadrant"]
            for a in cont.cssselect("a"):
                wellno = a.text
                url = urlparse.urljoin(r["url"], a.attrib.get("href"))
                contents = urllib.urlopen(url).read()
                scraperwiki.sqlite.execute("insert or ignore into oilwellfields values (?,?,?,?,?,?)", 
                                          (r["quadrant"], tdb, wellno, url, contents, datetime.datetime.now().isoformat()))

        scraperwiki.sqlite.commit()



#MakeTables()
#ScrapeIndexes()
ScrapeNewPages()
import scraperwiki
import urllib2, urllib, urlparse
import re
import datetime
import httplib
import time
import mechanize
import lxml.html

url = "https://www.og.decc.gov.uk/pls/wons/wdep0100.qryWell"

def MakeTables():
    oilwellindexfields = ["quadrant text", "welltable text", "url text", "scrapedate text"]
    oilwellfields = ["quadrant text", "block text", "wellno text", "url text", "contents text", "scrapedate text"]

    scraperwiki.sqlite.execute("drop table if exists oilwellindex")
    scraperwiki.sqlite.execute("create table oilwellindex (%s, unique(quadrant, welltable))" % ",".join(oilwellindexfields))
    scraperwiki.sqlite.execute("drop table if exists oilwell")
    scraperwiki.sqlite.execute("create table oilwell (%s, unique(quadrant, block, wellno, contents))" % ",".join(oilwellfields))



def ScrapeIndexes():
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open(url)
    i = 0  
    while True:
        br.form = list(br.forms())[0]
        selectcontrol = br.form.find_control(name='f_quadNoList', type='select')
        if i >= len(selectcontrol.items):
            return None
        print i, len(selectcontrol.items)
        item = selectcontrol.items[i]
        quadrant = item.get_labels()[0].text
        selectcontrol.value = [quadrant]
        root = lxml.html.parse(br.submit()).getroot()
        welltable = root.cssselect("center table")[1]

        scraperwiki.sqlite.execute("insert or ignore into oilwellindex values (?,?,?,?)", 
                                   (quadrant, lxml.html.tostring(welltable), br.geturl(), datetime.datetime.now().isoformat()), verbose=0)

        i += 1
        scraperwiki.sqlite.commit()



def ScrapeNewPages():
    res = scraperwiki.sqlite.select("quadrant, welltable, url from oilwellindex")
    print len(res)
    for r in res:
        welltable = lxml.html.fromstring(r["welltable"])
        rows = welltable.cssselect("tr")
        assert [x.text  for x in rows[0].cssselect("td em")] == ['Quadrant/Block no', 'Well Numbers'], lxml.html.tostring(rows[0])
        print len(rows), r["quadrant"] 
        for row in rows[1:]:
            tdqb, cont = row.cssselect("td")
            tdq, tdb = tdqb.text.split("/")
            assert tdq == r["quadrant"]
            for a in cont.cssselect("a"):
                wellno = a.text
                url = urlparse.urljoin(r["url"], a.attrib.get("href"))
                contents = urllib.urlopen(url).read()
                scraperwiki.sqlite.execute("insert or ignore into oilwellfields values (?,?,?,?,?,?)", 
                                          (r["quadrant"], tdb, wellno, url, contents, datetime.datetime.now().isoformat()))

        scraperwiki.sqlite.commit()



#MakeTables()
#ScrapeIndexes()
ScrapeNewPages()
