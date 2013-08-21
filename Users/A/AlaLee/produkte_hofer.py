import scraperwiki
import lxml.html

print scraperwiki.sqlite.show_tables()
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
    scraperwiki.sqlite.save(unique_keys=['Bezeichnung'], data=data)

def scrapeData(href,hinweis):
    html = scraperwiki.scrape(href)
    root = lxml.html.fromstring(html)
    root.make_links_absolute("http://www.hofer.at/")

    preis = "0"
    preis1 = "n.a"
    preis2 = "n.a"
    beschreibung1 = " "
    beschreibung2 = " "

    for tr in root.cssselect("ul.box li"):
        #print len(tr)
        try: 
            href =  tr.cssselect("a")[0].attrib['href']
        except IndexError:
            print "no href"
        except KeyError:
            print "no href"
        try: 
            bezeichnung = tr.cssselect("img")[0].attrib['alt']
        except KeyError:
            bezeichnung = tr.cssselect("a")[0].text_content()
        bild= tr.cssselect("img")[0].attrib['src']
        try:
            preis1 = tr.cssselect("span.value")[0].text_content()
            #print preis1
            preis1 = preis1.replace('-',"")
        except IndexError:
            preis1 = '0.'; 
        try:
            preis2= tr.cssselect("span.decimal")[0].text_content()
        except IndexError:
            preis2 = '0'; 
        try:
            sublink = scraperwiki.scrape(href)
            sublinkroot = lxml.html.fromstring(sublink)
            beschreibung1 = sublinkroot.cssselect("p")[0].text_content()
        except BadStatusLine:
            beschreibung1 = ""
        if len(sublinkroot.cssselect("p")) > 2:
            beschreibung2 = sublinkroot.cssselect("p")[1].text_content()
        beschreibung = beschreibung1 + beschreibung2    
        preis = preis1+preis2
        preis = preis.replace(',','.')
        bezichnung = bezeichnung.lstrip().rstrip()
        beschreibung = beschreibung.lstrip().rstrip()
        if preis != "0.0":
            setData(bezeichnung,'"'+hinweis+'"'+"\n"+beschreibung,bild, preis,href,"Hofer")

#getting the data from the hofer site

#Aktionen
hinweis = ""
href = ""
html = scraperwiki.scrape("http://www.hofer.at/at/html/offers/aktuelle_angebote.htm?WT.z_src=main")
root = lxml.html.fromstring(html)
root.make_links_absolute("http://www.hofer.at/")
for tr in root.cssselect("div#boxes li.specialoffers2"):
    #print len(tr)
    href = tr.cssselect("a")[0].attrib['href']
    #print href
    hinweis = tr.cssselect("img.headline")[0].attrib['alt']
    #print hinweis
    scrapeData(href,hinweis)

#Beauty, Pflege und mehr
hinweis = ""
href = ""
html = scraperwiki.scrape("http://www.hofer.at/at/html/product_range/sortiment_beauty.htm?WT.z_src=main")
root = lxml.html.fromstring(html)
root.make_links_absolute("http://www.hofer.at/")
for tr in root.cssselect("div#list li"):
    #print len(tr)
    href = tr.cssselect("a")[0].attrib['href']
    print href
    try:
        hinweis = tr.cssselect("a")[0].text_content()
    except IndexError:
        hinweis = ""      
    print hinweis
    scrapeData(href,hinweis)

#Sortiment
hinweis = ""
href = ""
html = scraperwiki.scrape("http://www.hofer.at/at/html/product_range/sortiment.htm?WT.z_src=main")
root = lxml.html.fromstring(html)
root.make_links_absolute("http://www.hofer.at/")
for tr in root.cssselect("div#boxes div.info"):
    #print len(tr)
    href = tr.cssselect("a")[0].attrib['href']
    #print href
    try:
        hinweis = tr.cssselect("img.headline")[0].attrib['alt']
    except IndexError: 
        hinweis = ""      
    #print hinweis
    scrapeData(href,hinweis)



