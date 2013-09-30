
###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
import urlparse
import lxml.html
import urllib2

"""
# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    rows = root.cssselect("table tr")  # selects all <tr> blocks within <table>
    for row in rows:
        record = {}
        table_cells = row.cssselect("td")
        if table_cells:
            record['Name'] = table_cells[0].cssselect("a")[0].text
            record['What'] = table_cells[1].text
            record['Region'] = table_cells[2].text
            record['Country'] = table_cells[3].text
            record['Lat'] = table_cells[4].text
            record['Long'] = table_cells[5].text
            record['Elev'] = table_cells[6].text
            record['Pop'] = table_cells[7].text
            
            print record
            
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["Name"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    next_link = root.cssselect("a.next")
    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)
"""

def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    ps = root.cssselect("div.entry p")

    for p in ps:
        if p.text:
            print p.text
        #if 'rapidgator.net' in 
        #print lxml.html.tostring(links[1])

#VideoHive
#'http://downfootage.com/tag/videohive/page/18/'

base_url = 'http://downfootage.com/tag/videohive/page/'

#'VideoHive After Effects set 72'

for n in range(30):
    html = scraperwiki.scrape(base_url+str(n)+'/')
    root = lxml.html.fromstring(html)
    links = root.cssselect("div.post a")
    
    for link in links:
        #if 'set' in link.text and 'Download' not in link.text:
        if 'VideoHive After Effects set' in link.text and 'Download' not in link.text:
            print link.text, link.attrib['href']
            scrape_and_look_for_next_link(link.attrib['href'])

    #print links[0].text
    #print lxml.html.tostring(links[0])

###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
import urlparse
import lxml.html
import urllib2

"""
# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    rows = root.cssselect("table tr")  # selects all <tr> blocks within <table>
    for row in rows:
        record = {}
        table_cells = row.cssselect("td")
        if table_cells:
            record['Name'] = table_cells[0].cssselect("a")[0].text
            record['What'] = table_cells[1].text
            record['Region'] = table_cells[2].text
            record['Country'] = table_cells[3].text
            record['Lat'] = table_cells[4].text
            record['Long'] = table_cells[5].text
            record['Elev'] = table_cells[6].text
            record['Pop'] = table_cells[7].text
            
            print record
            
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["Name"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    next_link = root.cssselect("a.next")
    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)
"""

def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    ps = root.cssselect("div.entry p")

    for p in ps:
        if p.text:
            print p.text
        #if 'rapidgator.net' in 
        #print lxml.html.tostring(links[1])

#VideoHive
#'http://downfootage.com/tag/videohive/page/18/'

base_url = 'http://downfootage.com/tag/videohive/page/'

#'VideoHive After Effects set 72'

for n in range(30):
    html = scraperwiki.scrape(base_url+str(n)+'/')
    root = lxml.html.fromstring(html)
    links = root.cssselect("div.post a")
    
    for link in links:
        #if 'set' in link.text and 'Download' not in link.text:
        if 'VideoHive After Effects set' in link.text and 'Download' not in link.text:
            print link.text, link.attrib['href']
            scrape_and_look_for_next_link(link.attrib['href'])

    #print links[0].text
    #print lxml.html.tostring(links[0])
