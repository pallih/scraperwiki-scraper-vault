import scraperwiki
import string
import scraperwiki
import lxml.html
# Blank Python

# function for parsing html ang save data
def parseHTML (url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    # print lxml.html.tostring(root)
    for el in root.cssselect("a.large"):
        title = el.getchildren()[0].text
        #tel = el.getchildren()[1].text
        #addr = el.getchildren()[2].getchildren()[0].text_content() + el.getchildren()[2].getchildren()[1].text_content()
        #niceAddr = " ".join(addr.split())
        print title
        salonURL = el.attrib['href']
        try:
            parseSinglePage(salonURL)
        except:
            print "... ... error ... ..."
            break
        
def parseSinglePage (salonURL):
    html = scraperwiki.scrape(salonURL)
    root = lxml.html.fromstring(html)
    # print lxml.html.tostring(root)
    table = root.cssselect("table.listing_content_table")[0]
    e1 = root.cssselect("div#inner_content_left h1")[0]
    #e2 = root.cssselect("div#inner_content_left h2")[0]
    #print e1.text
    #print e2.text
    title = e1.text
    address= table.getchildren()[2].text_content()
    region = table.getchildren()[4].text_content()
    station = table.getchildren()[5].text_content()
    tel = table.getchildren()[6].text_content()
    btype= table.getchildren()[8].text_content()
    #print title
    #print address
    #print region 
    #print station 
    #print tel 
    #print btype
    saveData (title, tel, address, region ,station, btype)

def saveData (title, tel, niceAddr, region, station, btype):
    data = {
        'title' : title,
        'tel' : tel,
        'addr' : niceAddr,
        'region' : region,
        'station' : station,
        'type' : btype
    }
    scraperwiki.sqlite.save(unique_keys=['addr'], data=data)


url = "http://www.allinlondon.co.uk/directory/index.php?type=keyword&tube=0&q=beauty%20hair&region=0&category=0&start=0&ordering=3"
#parseHTML(url)
for i in range(0, 515):
    x = i * 30
    url = "http://www.allinlondon.co.uk/directory/index.php?type=keyword&tube=0&q=beauty%20hair&region=0&category=0&start=" + str(x) + "&ordering=3"
    parseHTML(url)

