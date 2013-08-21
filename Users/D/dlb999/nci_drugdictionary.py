###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
import urlparse
import lxml.html

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
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    for link in root.cssselect("html body div#cgovContainer div#mainContainer div div#cgvBody div a"):
        record = {}
        content = link
        if content.get("name") is None:
            if content.get("class") is None:
                vloc = content.attrib['href']
                record['name'] = vbuf
                record['url'] = urlparse.urljoin(base_url, vloc)
                print vbuf, vloc, '--------'
                scraperwiki.sqlite.save(["name"], record)
                vbuf = None
                vloc = None
            elif content.get("class") == 'backtotop-link':
                break
        else:
            vbuf = content.get("name")
    for next in root.cssselect("html body div#cgovContainer div#mainContainer div div#cgvBody div p a"):
        content = next.text_content()
        if content.find('Next') == 0:
            nlink = next.attrib['href']
            next_url = urlparse.urljoin(base_url, nlink)
            print 'Next > ', nlink
            scrape_and_look_for_next_link(next_url)
            break
    

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://www.cancer.gov'
starting_url = urlparse.urljoin(base_url, '/drugdictionary/?&expand=All&searchTxt=%&first=1&page=1')
scrape_and_look_for_next_link(starting_url)
