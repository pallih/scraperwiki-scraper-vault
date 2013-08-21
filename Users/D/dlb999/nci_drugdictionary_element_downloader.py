# ------- Start --------

import scraperwiki
import urlparse
import lxml.html
from lxml.etree import tostring

# scrape_table function: gets passed an individual page to scrape
#def scrape_entries(content):
    
    #for entry in content.cssselect("a")
        #print entry
        # Set up our data record - we'll need it later
        #record = {}
        #if entry.attrib['href']:
            #record['url' = entry.attrib['href']
            # Print out the data we've gathered
            #print record, '------------'
            # Finally, save the record to the datastore - 'Drug' is our unique key
            #scraperwiki.datastore.save(["Drug"], record)

# scrape_page function
def scrape_page(url,name):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    record = {}
    for content in root.cssselect("html body div#cgovContainer div#mainContainer div div#cgvBody div"):
        n = 0
        for node in content:
            snode = tostring(node)
            sbr = '<br />&#13;'
            sa = '<a class="navigation-dark-red"'
            if snode.find(sbr) == 0:
                record['name'] = name
                n = 1
                utxt = lxml.html.fromstring(snode)
                drtxt = utxt.text_content().strip()
                rtxt = drtxt[:-10]
                print n,rtxt
                record['txt'] = rtxt
            elif snode.find(sa) == 0:
                n=n + 1
                rref = node.attrib['href']
                print n, rref
                if n == 2:
                    record['oct'] = rref
                elif n == 3:
                    record['cct'] = rref
                elif n == 4:
                    record['ncit'] = rref
    scraperwiki.sqlite.save(["name"], record)
            
    
# core program
sourcescraper = 'nci_drugdictionary'           
scraperwiki.sqlite.attach("nci_drugdictionary")
data = scraperwiki.sqlite.select(           
    '''* from nci_drugdictionary.swdata 
    order by name asc limit 10000'''
)
scraperwiki.sqlite.attach("nci_drugdictionary_element_downloader")

rows = data
for row in rows:
    url = row.get("url")
    name = row.get("name")
    scrape_page(url,name)

# ------------- junk -------------------

        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
# def scrape_and_look_for_next_link(url):
#    html = scraperwiki.scrape(url)
#    print html
#    root = lxml.html.fromstring(html)
#    for link in root.cssselect("html body div#cgovContainer div#mainContainer div div#cgvBody div a"):
#        record = {}
#        content = link
#        if content.get("name") is None:
#            if content.get("class") is None:
#                vloc = content.attrib['href']
#                record['name'] = vbuf
#                record['url'] = urlparse.urljoin(base_url, vloc)
#                print vbuf, vloc, '--------'
#                scraperwiki.sqlite.save(["name"], record)
#                vbuf = None
#                vloc = None
#            elif content.get("class") == 'backtotop-link':
#                break
#        else:
#            vbuf = content.get("name")
#    for next in root.cssselect("html body div#cgovContainer div#mainContainer div div#cgvBody div p a"):
#        content = next.text_content()
#        if content.find('Next') == 0:
#            nlink = next.attrib['href']
#            next_url = urlparse.urljoin(base_url, nlink)
#            print 'Next > ', nlink
#            scrape_and_look_for_next_link(next_url)
#            break
    

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
#base_url = 'http://www.cancer.gov'
#starting_url = urlparse.urljoin(base_url, '/drugdictionary/?&expand=All&searchTxt=%&first=1&page=1')
#scrape_and_look_for_next_link(starting_url)
