###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# define the order our columns are displayed in the datastore
scraperwiki.sqlite.save_var('data_columns', ['Artist', 'Album', 'Released', 'Sales (m)'])

# scrape_table function: gets passed an individual page to scrape
def scrape_page(soup):
    sectors = soup.findAll(attrs={'class':'sector'})
    
    for sector in sectors:
        event = {}
        parent = sector.parent
        
        event['Title'] = parent.h3.text
        print event['Title']

        event['URL'] = "http://www.turnersims.co.uk" + parent.h3.a['href']
        
        event['Date'] = parent.find(attrs={'class':'listingsDate'}).text
        print event['Date']
        
        scraperwiki.sqlite.save(["Title"], event) # save the records one by one

# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_page(soup)
    next_link = soup.find("a", { "class" : "next" })
    print next_link
    if next_link:
        next_url = "http://www.turnersims.co.uk" + next_link['href']
        print next_url
        scrape_and_look_for_next_link(next_url)

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://www.turnersims.co.uk/upcoming-events'
scrape_and_look_for_next_link(base_url)
###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# define the order our columns are displayed in the datastore
scraperwiki.sqlite.save_var('data_columns', ['Artist', 'Album', 'Released', 'Sales (m)'])

# scrape_table function: gets passed an individual page to scrape
def scrape_page(soup):
    sectors = soup.findAll(attrs={'class':'sector'})
    
    for sector in sectors:
        event = {}
        parent = sector.parent
        
        event['Title'] = parent.h3.text
        print event['Title']

        event['URL'] = "http://www.turnersims.co.uk" + parent.h3.a['href']
        
        event['Date'] = parent.find(attrs={'class':'listingsDate'}).text
        print event['Date']
        
        scraperwiki.sqlite.save(["Title"], event) # save the records one by one

# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_page(soup)
    next_link = soup.find("a", { "class" : "next" })
    print next_link
    if next_link:
        next_url = "http://www.turnersims.co.uk" + next_link['href']
        print next_url
        scrape_and_look_for_next_link(next_url)

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://www.turnersims.co.uk/upcoming-events'
scrape_and_look_for_next_link(base_url)
