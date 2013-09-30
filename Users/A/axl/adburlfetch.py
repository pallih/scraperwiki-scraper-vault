import scraperwiki
import urlparse
import lxml.html
import lxml.etree

def scrape(url):

    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    items = root.cssselect("div[class='iteminfo']") # Get all "items"

    linkList = []
    for item in items:
        links = item.cssselect("a") # Get all links
        ids = root.cssselect("div[aditemid]") # Get all ids

        for link in links:
            carUrl = urlparse.urljoin(base_url, link.attrib.get('href'))
            #print carUrl
            linkList.append(carUrl)

    recordList = []   
    counter = 0
    for id in ids:  
        carId = id.attrib.get('aditemid')
        #print id.attrib.get('aditemid') 
        
        record = {} 
        record['link'] = linkList[counter]
        record['id'] = carId
        
        recordList.append(record)
        counter += 1
        print record

    scraperwiki.sqlite.save(["id"], recordList)



# ---------------------------------------------------------------------------
# START HERE
# ---------------------------------------------------------------------------

scraperwiki.sqlite.execute("drop table if exists swdata")

base_url = 'http://bil.autodb.no/'
#starting_url = urlparse.urljoin(base_url, 'http://bil.autodb.no/autodb/search.wa2?County2_Split=%3A10009%3A10010%3A10002%3A10006%3A10020%3A10004%3A10012%3A10015%3A10018%3A10005%3A10003%3A10011%3A10014%3A10008%3A10019%3A10017%3A10016%3A10007%3A10001;Limit=20000;ListOrder=amsAdItems.PayTime%20DESC;Offset=0;Status=Active;Type=hmaAuto;_cmd=results')

starting_url = urlparse.urljoin(base_url, 'http://bil.autodb.no/autodb/search.wa2?Limit=10&ListOrder=amsAdItems.PayTime%20ASC&Status=Active&Type=hmaAuto&_cmd=results&xBrand_Multiple=0')

scrape(starting_url)import scraperwiki
import urlparse
import lxml.html
import lxml.etree

def scrape(url):

    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    items = root.cssselect("div[class='iteminfo']") # Get all "items"

    linkList = []
    for item in items:
        links = item.cssselect("a") # Get all links
        ids = root.cssselect("div[aditemid]") # Get all ids

        for link in links:
            carUrl = urlparse.urljoin(base_url, link.attrib.get('href'))
            #print carUrl
            linkList.append(carUrl)

    recordList = []   
    counter = 0
    for id in ids:  
        carId = id.attrib.get('aditemid')
        #print id.attrib.get('aditemid') 
        
        record = {} 
        record['link'] = linkList[counter]
        record['id'] = carId
        
        recordList.append(record)
        counter += 1
        print record

    scraperwiki.sqlite.save(["id"], recordList)



# ---------------------------------------------------------------------------
# START HERE
# ---------------------------------------------------------------------------

scraperwiki.sqlite.execute("drop table if exists swdata")

base_url = 'http://bil.autodb.no/'
#starting_url = urlparse.urljoin(base_url, 'http://bil.autodb.no/autodb/search.wa2?County2_Split=%3A10009%3A10010%3A10002%3A10006%3A10020%3A10004%3A10012%3A10015%3A10018%3A10005%3A10003%3A10011%3A10014%3A10008%3A10019%3A10017%3A10016%3A10007%3A10001;Limit=20000;ListOrder=amsAdItems.PayTime%20DESC;Offset=0;Status=Active;Type=hmaAuto;_cmd=results')

starting_url = urlparse.urljoin(base_url, 'http://bil.autodb.no/autodb/search.wa2?Limit=10&ListOrder=amsAdItems.PayTime%20ASC&Status=Active&Type=hmaAuto&_cmd=results&xBrand_Multiple=0')

scrape(starting_url)