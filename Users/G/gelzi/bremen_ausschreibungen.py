import scraperwiki
import lxml.html
import unicodedata

def parseMainpage(mainUrl): 
    html = scraperwiki.scrape(mainUrl)
    root = lxml.html.fromstring(html)
    for el in root.cssselect("td.tabelleLine2 a"):
        if el.text == "anzeigen" or el.text == "Bekanntmachung":
            detailpage = el.attrib['href']
            parseDetailpage(detailpage)
    for el in root.cssselect("td.tabelleLine1 a"):
        if el.text == "anzeigen" or el.text == "Bekanntmachung":
            detailpage = el.attrib['href']
            parseDetailpage(detailpage)
    
def parseDetailpage(detailUrl):
    detailhtml = scraperwiki.scrape("https://vergabe.bremen.de/NetServer/"+detailUrl)
    detailroot = lxml.html.fromstring(detailhtml)
    data = dict()
    #Hauptüberschrift
    for el in detailroot.cssselect("h2"):
        if el.text:
            data["header"] = el.text
    #einzeldingens
    for el in detailroot.cssselect("h3"):
        headkey = el.text
        nextEl = el.getnext()
        while not nextEl is None and nextEl.tag == "p":
            labelArray = nextEl.cssselect("label")
            if len(labelArray) > 0:
                label = labelArray[0].text
                valueArray = nextEl.cssselect("span")
                if len(valueArray) > 0:
                    value=valueArray[0].text
                    key = unicodedata.normalize('NFKD', (headkey[0:1]+"-"+label[0:50])).encode('ascii','ignore').translate(None, '():.,/').strip(': ')
                    print key                
                    data[key] = value
            nextEl = nextEl.getnext()
     
    scraperwiki.sqlite.save(unique_keys=['header'], data=data)
    
#offene Ausschreibungen
parseMainpage("https://vergabe.bremen.de/NetServer/PublicationSearchControllerServlet?function=ModifyPublicationsView&StartIndex=01&VisibleCount=100")

#parseDetailpage("PublicationControllerServlet?function=Detail&TOID=54321-NetTender-1343c883ec5-37ebb6d2c79a54cd&TenderKey=null")

import scraperwiki
import lxml.html
import unicodedata

def parseMainpage(mainUrl): 
    html = scraperwiki.scrape(mainUrl)
    root = lxml.html.fromstring(html)
    for el in root.cssselect("td.tabelleLine2 a"):
        if el.text == "anzeigen" or el.text == "Bekanntmachung":
            detailpage = el.attrib['href']
            parseDetailpage(detailpage)
    for el in root.cssselect("td.tabelleLine1 a"):
        if el.text == "anzeigen" or el.text == "Bekanntmachung":
            detailpage = el.attrib['href']
            parseDetailpage(detailpage)
    
def parseDetailpage(detailUrl):
    detailhtml = scraperwiki.scrape("https://vergabe.bremen.de/NetServer/"+detailUrl)
    detailroot = lxml.html.fromstring(detailhtml)
    data = dict()
    #Hauptüberschrift
    for el in detailroot.cssselect("h2"):
        if el.text:
            data["header"] = el.text
    #einzeldingens
    for el in detailroot.cssselect("h3"):
        headkey = el.text
        nextEl = el.getnext()
        while not nextEl is None and nextEl.tag == "p":
            labelArray = nextEl.cssselect("label")
            if len(labelArray) > 0:
                label = labelArray[0].text
                valueArray = nextEl.cssselect("span")
                if len(valueArray) > 0:
                    value=valueArray[0].text
                    key = unicodedata.normalize('NFKD', (headkey[0:1]+"-"+label[0:50])).encode('ascii','ignore').translate(None, '():.,/').strip(': ')
                    print key                
                    data[key] = value
            nextEl = nextEl.getnext()
     
    scraperwiki.sqlite.save(unique_keys=['header'], data=data)
    
#offene Ausschreibungen
parseMainpage("https://vergabe.bremen.de/NetServer/PublicationSearchControllerServlet?function=ModifyPublicationsView&StartIndex=01&VisibleCount=100")

#parseDetailpage("PublicationControllerServlet?function=Detail&TOID=54321-NetTender-1343c883ec5-37ebb6d2c79a54cd&TenderKey=null")

