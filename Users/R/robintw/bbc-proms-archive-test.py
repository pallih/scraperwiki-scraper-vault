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
    dates = soup.findAll(name = "a", attrs={'class':'blacklink'})    

    for date in dates:
        if date.text[-1] == "M" and date.text[-2] == "P":
            real_dates.append(date.text)

    print "Finished one page"

    
        
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_page(soup)

    links = soup.findAll("a", { "class" : "blacklink" })
    for link in links:
        if link.text == "Next":
            next_url = link['href']
            next_url = "http://www.bbc.co.uk" + next_url
            scrape_and_look_for_next_link(next_url)


    

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------

real_dates = []

base_url = 'http://www.bbc.co.uk/proms/archive/search/performance_find.shtml?work_id=1792&all=1&tab=search&sub_tab=work'
starting_url = base_url
scrape_and_look_for_next_link(starting_url)
print real_dates