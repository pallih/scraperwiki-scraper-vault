###############################################################################
# Scrape Critics and Urls Need to add test for ad display page
###############################################################################

import scraperwiki
import re
html = scraperwiki.scrape('http://www.rottentomatoes.com/critics/authors.php')
# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['Critic Page Link', 'Critic'])

# -----------------------------------------------------------------------------
# 1. Parse the raw HTML to get the interesting bits - the part inside <td> tags.
# -- UNCOMMENT THE 6 LINES BELOW (i.e. delete the # at the start of the lines)
# -- CLICK THE 'RUN' BUTTON BELOW
# Check the 'Console' tab again, and you'll see how we're extracting 
# the HTML that was inside <td></td> tags.
# We use BeautifulSoup, which is a Python library especially for scraping.
# -----------------------------------------------------------------------------

from BeautifulSoup import BeautifulSoup



# scrape_table function: gets passed an individual page to scrape
def scrape_table(soup):
    tds = soup.findAll("td", { "class" : "onlyCol" }) 

    for td in tds:
        record = {}
        record['Critic Page Link'] = td.p.a['href'] 
        record['Critic'] = td.text
        scraperwiki.datastore.save(["Critic"], record)




# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    print "in scrape and look"
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_table(soup)
    return soup
    #next_link = soup.find("a", { "class" : "next" })
    #print next_link
    #if next_link:
        #next_url = base_url + next_link['href']
        #print next_url
        #scrape_and_look_for_next_link(next_url)        
    


# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
atoz = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]


for curView  in atoz:
    
    base_url = 'http://www.rottentomatoes.com/critics/authors.php?view=' + curView


    soup = scrape_and_look_for_next_link(base_url)


    for x in range(2,1000):
                
               #if  soup.find('a', href = '/critics/authors.php?view=' + curView + '&page=' + str(x) ):
                    
               #if soup.find('a', href = '/critics/authors.php?view=&page=' + str(x) ):
               if  soup.find('a', href = '/critics/authors.php?view=' + curView + '&page=' + str(x) ):
                   next_url = base_url + '?view=&page=' + str(x)
                   print next_url
                   print x
                   soup = scrape_and_look_for_next_link(next_url)