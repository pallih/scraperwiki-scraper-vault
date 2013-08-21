###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
import urlparse
import lxml.html
import re

#this def scrapes the inidividual pages
def scrape_links(Links):
    page = scraperwiki.scrape(Links)
    root2 = lxml.html.fromstring(page)
    #print root2
    record = {}
    rows2 = root2.cssselect("table.ms-formtable tr td")[1]
    record['ref_number'] = rows2.text_content() 
    rows3 = root2.cssselect("table.ms-formtable tr td")[3]
    record['name'] = rows3.text_content()
    rows3a = root2.cssselect("table.ms-formtable tr td")[5]
    record['detail2'] = rows3a.text_content()
#print name
    rows4 = root2.cssselect("table.ms-formtable tr td")[31]
    record['detail'] = rows4.text_content()
    rows5 = root2.cssselect("table.ms-formtable tr td")[27]
    record['detail1'] = rows5.text_content()
    scraperwiki.sqlite.save(unique_keys=[],data={'Title':rows3.text_content(),'Detail':rows4.text_content(),'Detail1':rows5.text_content(),'Detail2':rows3a.text_content(),'Ref_number':rows2.text_content()})

# scrape_table function: gets passed the search result pages to scrape to get the individual page urls
def scrape_table(root):
    rows = root.cssselect("div.srch-results p")  # selects all <div> blocks within <table class="srch-results">
    for row in rows:
        
        table_cells = row.cssselect("p.ms-navheader a")
        for link in table_cells:
            print "table_cells[0].attrib['title']", table_cells[0].attrib['title']
        if table_cells: 
            Links = table_cells[0].attrib['href']
        #if Links:
            scrape_links(Links)
            print "Links", Links
            


     
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again

def scrape_and_look_for_next_link(url):     #I think this is looping too much and sending the results up to 'def Scrape_links'  
    html = scraperwiki.scrape(url)
    #print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    next_link = root.cssselect("div.srch-Page.srch-Page-bg a")
    for links in next_link:
        print "next_link.attrib['title']", next_link.attrib['title']
    #print next_link
    if next_link:
        next_link2 = next_link[2].attrib['href']
        print "next_link2", next_link2
        split_link = re.split("\)+",next_link2)
        split_link2 = re.split("\=+",split_link[0])
        split_link3 = re.split("\'+",split_link2[2])
        #print split_link3[0]
        #print split_link2
        if split_link3:
            next_url = nextlink_url+split_link3[0]
        #else:
            
            print "next_url", next_url
            scrape_and_look_for_next_link(next_url)
        

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
nextlink_url = 'https://www.supply2health.nhs.uk/results.aspx?k=Status"live"&start1='
base_url = 'https://www.supply2health.nhs.uk/'
starting_url = urlparse.urljoin(base_url, 'results.aspx?k=Status"live"&start1=1')
scrape_and_look_for_next_link(starting_url)
