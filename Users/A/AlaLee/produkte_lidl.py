import scraperwiki
import scraperwiki
import lxml.html

#deleting the entries in the database
scraperwiki.sqlite.execute("drop table if exists swdata")

#saving the data in the database
def setData(bezeichnung, beschreibung, bild, preis, href, markt):
    data = {
        'Bezeichnung' : bezeichnung,
        'Beschreibung' : beschreibung,
        'Markt' : markt,
        'Preis' : preis,
        'Bild' : bild,
        'Link' : href
    }
    if preis != "0.0":
        scraperwiki.sqlite.save(unique_keys=['Bezeichnung'], data=data)

#scraping the data
def scrapeData(href,hinweis):
    html = scraperwiki.scrape(href)
    root = lxml.html.fromstring(html)
    root.make_links_absolute("http://www.lidl.at/")

    preis = "n.a"
    beschreibung = ""

    for tr in root.cssselect("section.widecontent a.box"):
        #print len(tr)
        try:
            href =  tr.cssselect("a")[0].attrib['href']
        except KeyError:
            href = "nicht verfügbar"
        try:
            bezeichnung = tr.cssselect("img")[0].attrib['alt']
        except KeyError:
            bezeichnung = " "
        try:
            bild= tr.cssselect("img")[0].attrib['src']
        except KeyError:
            bild = "nicht verfügbar"
        try:
            preis= tr.cssselect("strong.price")[0].text_content()
            preis = preis.replace('*','')
            preis = preis.replace('-','0')
        except IndexError:
            preis = "0.0"
        try:
            beschreibung = tr.cssselect("small.amount")[0].text_content()
        except IndexError:
            beschreibung = " "
        try:
            setData(bezeichnung.lstrip().rstrip(),hinweis+' '+beschreibung.lstrip().rstrip(),bild, preis.lstrip().rstrip(),href,"Lidl")
        except UnicodeDecodeError: 
            setData(bezeichnung,beschreibung,bild, preis,href,"Lidl")


#getting the data from the lidl site

hinweis = ""
href = ""

#Ab 15.11.2012
html = scraperwiki.scrape("http://www.lidl.at/cps/rde/www_lidl_at")
root = lxml.html.fromstring(html)
root.make_links_absolute("http://www.lidl.at/")
for tr in root.cssselect("ul.secondlevel li"):
    if len(tr.cssselect("p"))>0:
        hinweis = tr.cssselect("p")[0].text_content()
        print hinweis
        href = tr.cssselect("a")[0].attrib['href']
        #print href
        scrapeData(href,'"'+hinweis+'"')


import scraperwiki
import scraperwiki
import lxml.html

#deleting the entries in the database
scraperwiki.sqlite.execute("drop table if exists swdata")

#saving the data in the database
def setData(bezeichnung, beschreibung, bild, preis, href, markt):
    data = {
        'Bezeichnung' : bezeichnung,
        'Beschreibung' : beschreibung,
        'Markt' : markt,
        'Preis' : preis,
        'Bild' : bild,
        'Link' : href
    }
    if preis != "0.0":
        scraperwiki.sqlite.save(unique_keys=['Bezeichnung'], data=data)

#scraping the data
def scrapeData(href,hinweis):
    html = scraperwiki.scrape(href)
    root = lxml.html.fromstring(html)
    root.make_links_absolute("http://www.lidl.at/")

    preis = "n.a"
    beschreibung = ""

    for tr in root.cssselect("section.widecontent a.box"):
        #print len(tr)
        try:
            href =  tr.cssselect("a")[0].attrib['href']
        except KeyError:
            href = "nicht verfügbar"
        try:
            bezeichnung = tr.cssselect("img")[0].attrib['alt']
        except KeyError:
            bezeichnung = " "
        try:
            bild= tr.cssselect("img")[0].attrib['src']
        except KeyError:
            bild = "nicht verfügbar"
        try:
            preis= tr.cssselect("strong.price")[0].text_content()
            preis = preis.replace('*','')
            preis = preis.replace('-','0')
        except IndexError:
            preis = "0.0"
        try:
            beschreibung = tr.cssselect("small.amount")[0].text_content()
        except IndexError:
            beschreibung = " "
        try:
            setData(bezeichnung.lstrip().rstrip(),hinweis+' '+beschreibung.lstrip().rstrip(),bild, preis.lstrip().rstrip(),href,"Lidl")
        except UnicodeDecodeError: 
            setData(bezeichnung,beschreibung,bild, preis,href,"Lidl")


#getting the data from the lidl site

hinweis = ""
href = ""

#Ab 15.11.2012
html = scraperwiki.scrape("http://www.lidl.at/cps/rde/www_lidl_at")
root = lxml.html.fromstring(html)
root.make_links_absolute("http://www.lidl.at/")
for tr in root.cssselect("ul.secondlevel li"):
    if len(tr.cssselect("p"))>0:
        hinweis = tr.cssselect("p")[0].text_content()
        print hinweis
        href = tr.cssselect("a")[0].attrib['href']
        #print href
        scrapeData(href,'"'+hinweis+'"')


