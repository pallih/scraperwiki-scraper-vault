import re
import scraperwiki
from BeautifulSoup import BeautifulStoneSoup

starting_url = 'http://www.london-fire.gov.uk/IncidentsRSS.xml'
xml = scraperwiki.scrape(starting_url)
soup = BeautifulStoneSoup(xml)

items = soup.findAll('item') 
for item in items:
    record = { "guid" : item.guid.text if item.guid else "", 
               "title" : item.title.text if item.title else "",
               "link" : item.link.text if item.link else "",
               "pubdate" : item.pubdate.text if item.pubdate else "",
               "description" : item.description.text if item.description else ""
            } 
    scraperwiki.datastore.save(["link"], record)
    import re
import scraperwiki
from BeautifulSoup import BeautifulStoneSoup

starting_url = 'http://www.london-fire.gov.uk/IncidentsRSS.xml'
xml = scraperwiki.scrape(starting_url)
soup = BeautifulStoneSoup(xml)

items = soup.findAll('item') 
for item in items:
    record = { "guid" : item.guid.text if item.guid else "", 
               "title" : item.title.text if item.title else "",
               "link" : item.link.text if item.link else "",
               "pubdate" : item.pubdate.text if item.pubdate else "",
               "description" : item.description.text if item.description else ""
            } 
    scraperwiki.datastore.save(["link"], record)
    