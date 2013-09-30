import scraperwiki
import scraperwiki
import lxml.html

#deleting the entries in the database
scraperwiki.sqlite.execute("drop table if exists swdata")

#writing the data to the database
def setData(bezeichnung, beschreibung, bild, preis, href, markt):
    data = {
        'Bezeichnung' : bezeichnung,
        'Beschreibung' : beschreibung,
        'Markt' : markt,
        'Preis' : preis,
        'Bild' : bild,
        'Link' : href
    }
    scraperwiki.sqlite.save(unique_keys=['Bezeichnung'], data=data)

#scraping the data
def scrapeData(href,hinweis):
    html = scraperwiki.scrape(href)
    root = lxml.html.fromstring(html)
    root.make_links_absolute("http://www.zielpunkt.at/")

    for tr in root.cssselect("table tr"):
        tds = tr.cssselect("td")  
        for tds in tr.cssselect("td"):
            if len(tds)>0:
                bezeichnung = ""
                beschreibung =""
                preisContainer =""
                bild = ""
                preis = "n.a"   
                markt = "Zielpunkt"
                x = len(tds)-1
                try:
                    bezeichnung = tds[x].cssselect("img[src]")[0].attrib['alt']
                    #print bezeichnung
                except KeyError: 
                    bezeichnung = " "
                except IndexError: 
                    bezeichnung = " "
                try:
                    bild = tds[x].cssselect("img[src]")[0].attrib['src']
                except KeyError:
                    bild = "nicht verfügbar"
                except IndexError:
                    bild = "nicht verfügbar"
                try:
                    beschreibung= tds[x].cssselect("div.prodText")[0].text_content()
                except IndexError:
                    beschreibung = " "
                try:   
                    preis = tr.cssselect("img")[1].attrib['alt']
                except KeyError:
                    preis = "0.0"
                except IndexError:
                    preis = "0.0"
                except AttributeError:
                    preis = "0.0"
                if preis != "0.0":
                    setData(bezeichnung,hinweis+" "+beschreibung,bild,preis,href,markt)



#Startseite
scrapeData("http://www.zielpunkt.at/home_1.html","Startseite")

#Aktionen
href = "http://zielpunkt.at/AKTIONEN_6.html"
html = scraperwiki.scrape(href)
root = lxml.html.fromstring(html)
root.make_links_absolute("http://www.zielpunkt.at/")
hinweis = ""
href = ""

for tr in root.cssselect("div#subMenuNr1 a"):
    href = tr.attrib['href']
    hinweis = tr[0].attrib['alt']
    scrapeData(href,'"'+hinweis+'"')

#Im Regal
href = "http://www.zielpunkt.at/ImRegal_196.html"
html = scraperwiki.scrape(href)
root = lxml.html.fromstring(html)
root.make_links_absolute("http://www.zielpunkt.at/")
hinweis = ""
href = ""

for tr in root.cssselect("div#subMenuNr2 a"):
    href = tr.attrib['href']
    hinweis = tr[0].attrib['alt']
    scrapeData(href,'"'+hinweis+'"')




import scraperwiki
import scraperwiki
import lxml.html

#deleting the entries in the database
scraperwiki.sqlite.execute("drop table if exists swdata")

#writing the data to the database
def setData(bezeichnung, beschreibung, bild, preis, href, markt):
    data = {
        'Bezeichnung' : bezeichnung,
        'Beschreibung' : beschreibung,
        'Markt' : markt,
        'Preis' : preis,
        'Bild' : bild,
        'Link' : href
    }
    scraperwiki.sqlite.save(unique_keys=['Bezeichnung'], data=data)

#scraping the data
def scrapeData(href,hinweis):
    html = scraperwiki.scrape(href)
    root = lxml.html.fromstring(html)
    root.make_links_absolute("http://www.zielpunkt.at/")

    for tr in root.cssselect("table tr"):
        tds = tr.cssselect("td")  
        for tds in tr.cssselect("td"):
            if len(tds)>0:
                bezeichnung = ""
                beschreibung =""
                preisContainer =""
                bild = ""
                preis = "n.a"   
                markt = "Zielpunkt"
                x = len(tds)-1
                try:
                    bezeichnung = tds[x].cssselect("img[src]")[0].attrib['alt']
                    #print bezeichnung
                except KeyError: 
                    bezeichnung = " "
                except IndexError: 
                    bezeichnung = " "
                try:
                    bild = tds[x].cssselect("img[src]")[0].attrib['src']
                except KeyError:
                    bild = "nicht verfügbar"
                except IndexError:
                    bild = "nicht verfügbar"
                try:
                    beschreibung= tds[x].cssselect("div.prodText")[0].text_content()
                except IndexError:
                    beschreibung = " "
                try:   
                    preis = tr.cssselect("img")[1].attrib['alt']
                except KeyError:
                    preis = "0.0"
                except IndexError:
                    preis = "0.0"
                except AttributeError:
                    preis = "0.0"
                if preis != "0.0":
                    setData(bezeichnung,hinweis+" "+beschreibung,bild,preis,href,markt)



#Startseite
scrapeData("http://www.zielpunkt.at/home_1.html","Startseite")

#Aktionen
href = "http://zielpunkt.at/AKTIONEN_6.html"
html = scraperwiki.scrape(href)
root = lxml.html.fromstring(html)
root.make_links_absolute("http://www.zielpunkt.at/")
hinweis = ""
href = ""

for tr in root.cssselect("div#subMenuNr1 a"):
    href = tr.attrib['href']
    hinweis = tr[0].attrib['alt']
    scrapeData(href,'"'+hinweis+'"')

#Im Regal
href = "http://www.zielpunkt.at/ImRegal_196.html"
html = scraperwiki.scrape(href)
root = lxml.html.fromstring(html)
root.make_links_absolute("http://www.zielpunkt.at/")
hinweis = ""
href = ""

for tr in root.cssselect("div#subMenuNr2 a"):
    href = tr.attrib['href']
    hinweis = tr[0].attrib['alt']
    scrapeData(href,'"'+hinweis+'"')




