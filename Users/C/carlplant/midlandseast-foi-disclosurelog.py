import scraperwiki
import lxml.html
from datetime import date 
import re
from urlparse import urljoin

record = {}


def scrapeFiles(pageLinkJoin):
    html2 = scraperwiki.scrape(pageLinkJoin)
    root2 = lxml.html.fromstring(html2)
#print root

    divs = root2.cssselect('div.documentsBox ul') #select all of the tr elements

    for row in divs:
    
        info= row.cssselect('li') 
    #print info
        for link in info:
            linkUrl = link[0].attrib.get('href')
            record['linkTitle'] = link[0].text_content()
            #print linkTitle
            record['downloadFile'] = urljoin('https://www.eoe.nhs.uk/',linkUrl)
            scraperwiki.sqlite.save(unique_keys=[], data=record)
        

html = scraperwiki.scrape("https://www.eoe.nhs.uk/page.php?page_id=2193")
root = lxml.html.fromstring(html)
uls = root.cssselect('ul#subNav') 
for ul in uls:
    tab = ul.cssselect('li')
    for Link in tab:
        pageLink = Link[0].attrib.get('href')
        pageLinkJoin = urljoin('https://www.eoe.nhs.uk/',pageLink)
        scrapeFiles(pageLinkJoin)
        
        





