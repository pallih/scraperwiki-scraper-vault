###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['Artist', 'Album', 'Released', 'Sales (m)'])

# scrape_table function: gets passed an individual page to scrape
def scrape_page(soup):
    event = {}
    names = soup.findAll(attrs={'class':'name'})
    print names

    dates = soup.findAll(attrs={'class':'date'})
    
    print len(names)

    for i in range(len(names)):
        event['Title'] = names[i].text
        event['Date'] = dates[i].text.replace("to", "to ")
        event['URL'] = 'http://www.theatre-royal-winchester.co.uk' + names[i].a['href']

        scraperwiki.datastore.save(["Title"], event)


    

    
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_page(soup)
    next_link = soup.find(text="Next")
    print len(next_link.parent)
    print next_link.parent.name == "a"
    if next_link.parent.name == "a":
        next_url = 'http://www.theatre-royal-winchester.co.uk' + str(next_link.parent['href']).replace("#nav","")
        print next_url
        scrape_and_look_for_next_link(next_url)

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://www.theatre-royal-winchester.co.uk'
starting_url = base_url + '/whats_on/'
scrape_and_look_for_next_link(starting_url)
###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['Artist', 'Album', 'Released', 'Sales (m)'])

# scrape_table function: gets passed an individual page to scrape
def scrape_page(soup):
    event = {}
    names = soup.findAll(attrs={'class':'name'})
    print names

    dates = soup.findAll(attrs={'class':'date'})
    
    print len(names)

    for i in range(len(names)):
        event['Title'] = names[i].text
        event['Date'] = dates[i].text.replace("to", "to ")
        event['URL'] = 'http://www.theatre-royal-winchester.co.uk' + names[i].a['href']

        scraperwiki.datastore.save(["Title"], event)


    

    
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_page(soup)
    next_link = soup.find(text="Next")
    print len(next_link.parent)
    print next_link.parent.name == "a"
    if next_link.parent.name == "a":
        next_url = 'http://www.theatre-royal-winchester.co.uk' + str(next_link.parent['href']).replace("#nav","")
        print next_url
        scrape_and_look_for_next_link(next_url)

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://www.theatre-royal-winchester.co.uk'
starting_url = base_url + '/whats_on/'
scrape_and_look_for_next_link(starting_url)
