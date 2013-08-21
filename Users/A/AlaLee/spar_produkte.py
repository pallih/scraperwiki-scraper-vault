import scraperwiki
import lxml.html
from lxml.html import parse, open_in_browser

#delete the old data
scraperwiki.sqlite.execute("drop table if exists swdata")

def insert(original, new, pos):
    return original[:pos] + new + original[pos:]

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

def getSublists(href, hinweis):
    try:
        html = scraperwiki.scrape(href)
        root = lxml.html.fromstring(html)
        root.make_links_absolute("http://www.spar.at/")
        open_in_browser(root)
        for sublist in root.cssselect("div.left-nav li.on"):
            try:
                    for element, attribute, link, pos in sublist.iterlinks():
                        #url = sublist.cssselect("li a")[0].attrib['href']
                        print "Sublist "+link
                        scrapeData(link,'"'+hinweis+'"') 
            except IndexError:
                print "no href"
            except ValueError:
                print "no href"
    except ValueError:
        print "no href"

def scrapeData(href,hinweis):
    html = scraperwiki.scrape(href)
    root = lxml.html.fromstring(html)
    root.make_links_absolute("http://www.spar.at/")
    preis = "n.a"
    beschreibung = ""

    for tr in root.cssselect("div.par div.modul-small"):
        #print len(tr)
        try:
            href =  tr.cssselect("a")[0].attrib['href']
        except KeyError:
            href = "nicht verfügbar"
        except IndexError:
            href = "nicht verfügbar"
        try:
            bezeichnung = tr.cssselect("img")[0].attrib['alt']
        except KeyError:
            bezeichnung = "nicht verfügbar"
        except IndexError:
            bezeichnung = "nicht verfügbar"
        try:
            bild= tr.cssselect("img")[0].attrib['src']
        except KeyError:
            bild = "nicht verfügbar"
        except IndexError:
            bild = "nicht verfügbar"
        try:
            preis = tr.cssselect("p.action-preises")[0].text_content()
            subpreis = tr.cssselect("sup")[0].text_content()
            #print subpreis
            index = preis.rfind(subpreis)
            #print index
            preis = insert(preis,'.',index)
            preis = preis.replace('*','')
            preis = preis.replace('-','0')
            #print preis
        except IndexError:
            preis = "0.0"
        try:
            beschreibung = tr.cssselect("p.info")[0].text_content()
        except IndexError:
            beschreibung = ""
        try:
            if preis != '0.0':
                setData(bezeichnung.lstrip().rstrip(),hinweis+' '+beschreibung.lstrip().rstrip(),bild, preis.lstrip().rstrip(),href,"Spar")
        except UnicodeDecodeError: 
            if preis != '0.0': 
                setData(bezeichnung,beschreibung,bild, preis,href,"Spar")
        

#getting the data from the spar site

#Aktionen
hinweis = ""
href = ""
html = scraperwiki.scrape("http://spar.at/de_AT/index/aktionen.html")

root = lxml.html.fromstring(html)
root.make_links_absolute("http://www.spar.at/")
for tr in root.cssselect("div.left-nav li"):
    href = tr.cssselect("a")[0].attrib['href']
    hinweis = tr.cssselect("a")[0].text_content()
    scrapeData(href,'"'+hinweis+'"') 
    #getSublists(href, hinweis)

#Eigenmarken
hinweis = ""
href = ""
html = scraperwiki.scrape("http://spar.at/de_AT/index/spar-marken.html")

root = lxml.html.fromstring(html)
root.make_links_absolute("http://www.spar.at/")
for tr in root.cssselect("div.left-nav li"):
    href = tr.cssselect("a")[0].attrib['href']
    hinweis = tr.cssselect("a")[0].text_content()
    getSublists(href, hinweis)
