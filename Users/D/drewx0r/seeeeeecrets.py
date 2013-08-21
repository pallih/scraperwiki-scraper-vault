###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
import urlparse
import lxml.html
import re
import mechanize

# scrape_table function: gets passed an individual page to scrape
def scrape_list(root):
    items = root.cssselect("div#sidebarWrapper div ul li")  # selects all <tr> blocks within <table class="data">
    for item in items:
        # Set up our data record - we'll need it later
        record = {}
        link = item.cssselect("a")
        repinfo = link[0].text
        repinfo = re.findall(r'(.*) \((R|D)-(.*)\)', repinfo)[0]
        name = repinfo[0]
        party = repinfo[1]
        state = repinfo[2]
        print name
        print party
        print state
        cid = re.findall(r'cid=(N\d+)', link[0].get('href'))
        cid = ''.join(cid)
        print cid
        xmlurl = 'http://www.opensecrets.org/pfds/CIDsummary_getdata.php?cid=' + cid + '&year=2010&type=H&name=undefined'
#        getxml = scraperwiki.scrape(xmlurl)
        print xmlurl
#        if table_cells: 
#            record['Artist'] = table_cells[0].text
#            record['Album'] = table_cells[1].text
#            record['Released'] = table_cells[2].text
#            record['Sales m'] = table_cells[4].text
            # Print out the data we've gathered
#            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
#            scraperwiki.datastore.save(["Artist"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_list(root)
    next_link = root.cssselect("a.next")
#    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://www.opensecrets.org/cmteprofiles/profiles.php?cmteid=H04&cmte=HARM&congno=112'
# starting_url = urlparse.urljoin(base_url, 'example_table_1.html')
scrape_and_look_for_next_link(base_url)
