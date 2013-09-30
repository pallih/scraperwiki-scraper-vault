###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

#process an individual school record and save it
def scrape_school(link, school, address, LA):
    record = {}
    record["LA"] = LA
    record["School"] = school
    try:
        school_html = scraperwiki.scrape(link)
        school_soup = BeautifulSoup(school_html)
        overview_table = school_soup.find("table", {"class": "overview"})
        overview_headings = overview_table.findAll("th")
        for heading in overview_headings:
            heading_data = ""
            if heading.findNextSibling("td").text != "":
                heading_data = heading.findNextSibling("td").contents[0]
            record[heading.text.replace(":","")] = heading_data
    except:
        #Create default record details
        record["Address"] = address
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
                address = ""
                try:
                    if school_link.text:
                        li_parent = school_link.parent
                        address_class = li_parent.find("span", {"class":"schoolAddress"})
                        if address_class:
                            address = address_class.text
                        scrape_school(school_link['href'],school_link.text,address,LA)
                except:
                    #Create default record details
                    record = {}
                    record["LA"] = LA
                    record["School"] = school
                    record["Address"] = address
                    scraperwiki.datastore.save(["School"], record)
    except:
        print "Exception thrown in: scrape_la: LA = "+LA


def page_url(base_url,school_type):
    try:
        starting_url = base_url+'/search-results/?searchstring='+char+'&type='+school_type+'&distancevalue=5&distancemeasure=miles#'
        html = scraperwiki.scrape(starting_url) 
        soup = BeautifulSoup(html)
        la_div = soup.find("div", {"id":"laResults"})
        if la_div:
             la_links = la_div.findAll("a")
             for link in la_links:
                 print "!LA: "+link.text
                 scrape_la(base_url+link['href'],link.text)
    except:
        print "Exception thrown in: page_url: base_url = "+base_url+", school_type = "+school_type

                
#for a given letter find any LA's beginning with that letter
#and scrape them
def letter_sweep(char):
    try:
        base_url = "http://schoolsfinder.direct.gov.uk"
        school_type = "Primary%2CSecondary"
        page_url(base_url,school_type)
    except:
        print "Exception thrown in: letter_sweep: char = "+char



#in order to see any data need to 
#search the database for a letter
for char in "a":
    valid_chars = "bcdeghiklmnoprstwy"
    letter_sweep(char)


###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

#process an individual school record and save it
def scrape_school(link, school, address, LA):
    record = {}
    record["LA"] = LA
    record["School"] = school
    try:
        school_html = scraperwiki.scrape(link)
        school_soup = BeautifulSoup(school_html)
        overview_table = school_soup.find("table", {"class": "overview"})
        overview_headings = overview_table.findAll("th")
        for heading in overview_headings:
            heading_data = ""
            if heading.findNextSibling("td").text != "":
                heading_data = heading.findNextSibling("td").contents[0]
            record[heading.text.replace(":","")] = heading_data
    except:
        #Create default record details
        record["Address"] = address
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
                address = ""
                try:
                    if school_link.text:
                        li_parent = school_link.parent
                        address_class = li_parent.find("span", {"class":"schoolAddress"})
                        if address_class:
                            address = address_class.text
                        scrape_school(school_link['href'],school_link.text,address,LA)
                except:
                    #Create default record details
                    record = {}
                    record["LA"] = LA
                    record["School"] = school
                    record["Address"] = address
                    scraperwiki.datastore.save(["School"], record)
    except:
        print "Exception thrown in: scrape_la: LA = "+LA


def page_url(base_url,school_type):
    try:
        starting_url = base_url+'/search-results/?searchstring='+char+'&type='+school_type+'&distancevalue=5&distancemeasure=miles#'
        html = scraperwiki.scrape(starting_url) 
        soup = BeautifulSoup(html)
        la_div = soup.find("div", {"id":"laResults"})
        if la_div:
             la_links = la_div.findAll("a")
             for link in la_links:
                 print "!LA: "+link.text
                 scrape_la(base_url+link['href'],link.text)
    except:
        print "Exception thrown in: page_url: base_url = "+base_url+", school_type = "+school_type

                
#for a given letter find any LA's beginning with that letter
#and scrape them
def letter_sweep(char):
    try:
        base_url = "http://schoolsfinder.direct.gov.uk"
        school_type = "Primary%2CSecondary"
        page_url(base_url,school_type)
    except:
        print "Exception thrown in: letter_sweep: char = "+char



#in order to see any data need to 
#search the database for a letter
for char in "a":
    valid_chars = "bcdeghiklmnoprstwy"
    letter_sweep(char)


