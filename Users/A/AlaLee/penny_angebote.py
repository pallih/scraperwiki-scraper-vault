import scraperwiki

import scraperwiki
import lxml.html

#delete the old data
scraperwiki.sqlite.execute("drop table if exists swdata")

def setData(bezeichnung, beschreibung, bild, preis, href, markt):
    data = {
        'Bezeichnung' : bezeichnung,
        'Beschreibung' : beschreibung,
        'Markt' : markt,
        'Preis' : preis,
        'Bild' : bild,
        'Link' : href
    }
    if preis != "0.00":
        scraperwiki.sqlite.save(unique_keys=['Bezeichnung'], data=data)

def scrapeData(href,hinweis):
    html = scraperwiki.scrape(href)
    root = lxml.html.fromstring(html)
    root.make_links_absolute("http://www.penny.at/")

    try:
        sublink = root.cssselect("div.cwmid")[0].text_content()
    except IndexError:
        sublink = "http://www.penny.at/default.aspx"
    
    print "Starting to extract"
    for tr in root.cssselect("ul.teaserContainer li"):
        #print len(tr)
        try:
            beschreibung = tr.cssselect("span.teaserHeadline")[0].text_content()
        except IndexError:
            beschreibung = ""
        try:
            href = tr.cssselect("a")[0].attrib['href']
        except IndexError:
            href = ""
        except KeyError:
            href = ""
        try:
            bezeichnung = tr.cssselect("span.teaserHeadline")[0].text_content()
        except IndexError:
            bezeichnung = ""        
        try:
            bild= tr.cssselect("img")[0].attrib['src']
        except IndexError:
            bild = "n.a"  
        try:
            preis1= tr.cssselect("span.price1")[0].text_content()
        except IndexError:
            preis1 = "0.0"  
        try:
            preis2= tr.cssselect("span.price2")[0].text_content()
        except IndexError:
            preis2 = "0" 
        try:
            sublink = scraperwiki.scrape(href)
            sublinkroot = lxml.html.fromstring(sublink)
            beschreibung1 = sublinkroot.cssselect("ul.specs")[0].text_content()
        except IndexError:
            beschreibung1= ""
        except ValueError:
            beschreibung1= ""    
    
        setData(bezeichnung,'"'+hinweis+'"'+'\n'+beschreibung+" "+beschreibung1,bild, preis1+preis2,href,"Penny")

#getting the data from the penny site
#Angebote
href = "http://www.penny.at/Angebote/Angebote/pe_DefaultContent1.aspx"
html = scraperwiki.scrape(href)
root = lxml.html.fromstring(html)
root.make_links_absolute("http://www.penny.at/")

for tr in root.cssselect("div.sideCol li"):
    link = tr.cssselect("a")[0].attrib['href']
    hinweis = tr.cssselect("a")[0].text_content()
    scrapeData(link,hinweis)

#Sortiment
href = "http://www.penny.at/Sortiment/Sortiment/pe_DefaultContent1.aspx"
html = scraperwiki.scrape(href)
root = lxml.html.fromstring(html)
root.make_links_absolute("http://www.penny.at/")

for tr in root.cssselect("div.sideCol li"):
    link = tr.cssselect("a")[0].attrib['href']
    hinweis = tr.cssselect("a")[0].text_content()
    scrapeData(link,hinweis)
    
    
    
    
    


import scraperwiki

import scraperwiki
import lxml.html

#delete the old data
scraperwiki.sqlite.execute("drop table if exists swdata")

def setData(bezeichnung, beschreibung, bild, preis, href, markt):
    data = {
        'Bezeichnung' : bezeichnung,
        'Beschreibung' : beschreibung,
        'Markt' : markt,
        'Preis' : preis,
        'Bild' : bild,
        'Link' : href
    }
    if preis != "0.00":
        scraperwiki.sqlite.save(unique_keys=['Bezeichnung'], data=data)

def scrapeData(href,hinweis):
    html = scraperwiki.scrape(href)
    root = lxml.html.fromstring(html)
    root.make_links_absolute("http://www.penny.at/")

    try:
        sublink = root.cssselect("div.cwmid")[0].text_content()
    except IndexError:
        sublink = "http://www.penny.at/default.aspx"
    
    print "Starting to extract"
    for tr in root.cssselect("ul.teaserContainer li"):
        #print len(tr)
        try:
            beschreibung = tr.cssselect("span.teaserHeadline")[0].text_content()
        except IndexError:
            beschreibung = ""
        try:
            href = tr.cssselect("a")[0].attrib['href']
        except IndexError:
            href = ""
        except KeyError:
            href = ""
        try:
            bezeichnung = tr.cssselect("span.teaserHeadline")[0].text_content()
        except IndexError:
            bezeichnung = ""        
        try:
            bild= tr.cssselect("img")[0].attrib['src']
        except IndexError:
            bild = "n.a"  
        try:
            preis1= tr.cssselect("span.price1")[0].text_content()
        except IndexError:
            preis1 = "0.0"  
        try:
            preis2= tr.cssselect("span.price2")[0].text_content()
        except IndexError:
            preis2 = "0" 
        try:
            sublink = scraperwiki.scrape(href)
            sublinkroot = lxml.html.fromstring(sublink)
            beschreibung1 = sublinkroot.cssselect("ul.specs")[0].text_content()
        except IndexError:
            beschreibung1= ""
        except ValueError:
            beschreibung1= ""    
    
        setData(bezeichnung,'"'+hinweis+'"'+'\n'+beschreibung+" "+beschreibung1,bild, preis1+preis2,href,"Penny")

#getting the data from the penny site
#Angebote
href = "http://www.penny.at/Angebote/Angebote/pe_DefaultContent1.aspx"
html = scraperwiki.scrape(href)
root = lxml.html.fromstring(html)
root.make_links_absolute("http://www.penny.at/")

for tr in root.cssselect("div.sideCol li"):
    link = tr.cssselect("a")[0].attrib['href']
    hinweis = tr.cssselect("a")[0].text_content()
    scrapeData(link,hinweis)

#Sortiment
href = "http://www.penny.at/Sortiment/Sortiment/pe_DefaultContent1.aspx"
html = scraperwiki.scrape(href)
root = lxml.html.fromstring(html)
root.make_links_absolute("http://www.penny.at/")

for tr in root.cssselect("div.sideCol li"):
    link = tr.cssselect("a")[0].attrib['href']
    hinweis = tr.cssselect("a")[0].text_content()
    scrapeData(link,hinweis)
    
    
    
    
    


