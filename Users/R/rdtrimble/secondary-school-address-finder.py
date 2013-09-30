###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

#process an individual school record and save it
def scrape_school(link, school, LA):
    school_html = scraperwiki.scrape(link)
    school_soup = BeautifulSoup(school_html)
    #print school_soup
    record = {}
    record["LA"] = LA
    record["School"] = school 
    overview_table = school_soup.find("table", {"class": "overview"})
    overview_headings = overview_table.findAll("th")
    for heading in overview_headings:
        heading_data = ""
        if heading.findNextSibling("td").text != "":
            heading_data = heading.findNextSibling("td").contents[0]
        #print "       "+heading.text#.replace(":","")
        #print "       "+heading_data
        record[heading.text.replace(":","")] = heading_data
    scraperwiki.datastore.save(["School"], record)


    
#process a local authority listing and scrape each school in it  
def scrape_la(link, LA):
    try:
        la_html = scraperwiki.scrape(link)
        la_soup = BeautifulSoup(la_html)
        schools_div = la_soup.find("div", {"id": "schoolResults"})
        if schools_div:
            school_links = schools_div.findAll("a")
            for school_link in school_links:
                if school_link.text:
                    #print "!School: "+school_link.text
                    scrape_school(school_link['href'],school_link.text,LA)
    except:
        print "============== Error: "+LA+" ================"


def page_url(base_url,search_url):
    html = scraperwiki.scrape(search_url)
    #print html
    soup = BeautifulSoup(html)
    
    # use BeautifulSoup to get LA div
    la_div = soup.find("div", {"id":"laResults"})
    if la_div:
        la_links = la_div.findAll("a")
        for link in la_links:
            print "!LA: "+link.text
            #print  base_url+"/la/"+link.text.replace("  ","-")+"/?d=1&distancemeasure=miles&searchstring=w&distancevalue=5&pagetype=la"
            scrape_la(base_url+link['href'],link.text)

                
#for a given letter find any LA's beginning with that letter
#and scrape them
def letter_sweep(char):
    base_url = "http://schoolsfinder.direct.gov.uk"
    starting_url = base_url+'/search-results/?searchstring='+char+'&type=Secondary&distancevalue=5&distancemeasure=miles#'
    page_url(base_url,starting_url)




#in order to see any data need to 
#search the database for a letter
for char in "abcdefghijklmnopqrstuvwxyz":
    letter_sweep(char)



###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

#process an individual school record and save it
def scrape_school(link, school, LA):
    school_html = scraperwiki.scrape(link)
    school_soup = BeautifulSoup(school_html)
    #print school_soup
    record = {}
    record["LA"] = LA
    record["School"] = school 
    overview_table = school_soup.find("table", {"class": "overview"})
    overview_headings = overview_table.findAll("th")
    for heading in overview_headings:
        heading_data = ""
        if heading.findNextSibling("td").text != "":
            heading_data = heading.findNextSibling("td").contents[0]
        #print "       "+heading.text#.replace(":","")
        #print "       "+heading_data
        record[heading.text.replace(":","")] = heading_data
    scraperwiki.datastore.save(["School"], record)


    
#process a local authority listing and scrape each school in it  
def scrape_la(link, LA):
    try:
        la_html = scraperwiki.scrape(link)
        la_soup = BeautifulSoup(la_html)
        schools_div = la_soup.find("div", {"id": "schoolResults"})
        if schools_div:
            school_links = schools_div.findAll("a")
            for school_link in school_links:
                if school_link.text:
                    #print "!School: "+school_link.text
                    scrape_school(school_link['href'],school_link.text,LA)
    except:
        print "============== Error: "+LA+" ================"


def page_url(base_url,search_url):
    html = scraperwiki.scrape(search_url)
    #print html
    soup = BeautifulSoup(html)
    
    # use BeautifulSoup to get LA div
    la_div = soup.find("div", {"id":"laResults"})
    if la_div:
        la_links = la_div.findAll("a")
        for link in la_links:
            print "!LA: "+link.text
            #print  base_url+"/la/"+link.text.replace("  ","-")+"/?d=1&distancemeasure=miles&searchstring=w&distancevalue=5&pagetype=la"
            scrape_la(base_url+link['href'],link.text)

                
#for a given letter find any LA's beginning with that letter
#and scrape them
def letter_sweep(char):
    base_url = "http://schoolsfinder.direct.gov.uk"
    starting_url = base_url+'/search-results/?searchstring='+char+'&type=Secondary&distancevalue=5&distancemeasure=miles#'
    page_url(base_url,starting_url)




#in order to see any data need to 
#search the database for a letter
for char in "abcdefghijklmnopqrstuvwxyz":
    letter_sweep(char)



