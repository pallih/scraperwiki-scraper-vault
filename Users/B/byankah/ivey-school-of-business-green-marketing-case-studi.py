###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('hbr_greenmarketing', ['title', 'link', 'description', 'price', 'keywords'])


# scrape record for details
def scrape_for_details(url):
    details = {}
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    details['description'] = soup.find(id='item_info_text_full').text
    price_field = soup.find("input", { "id" : "productUnitPrice" })
    details['price'] = price_field['value']
    keywords = soup.find(text="Subjects Covered").parent.parent
    keyword_find = keywords.findAll('a')
    keyword_string = ''
    for kw in keyword_find:
        keyword_string = keyword_string + kw.text + ", "
    details['keywords'] = keyword_string
    return details

# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_table(soup):
    the_form = soup.find('form')
    print the_form
    #titles = soup.findAll(attrs={'href' : re.compile("http://cases.ivey.uwo.ca/Cases/Pages/home.aspx?Mode=showproduct&prod=$")})
    #titles = soup.findAll('a')
    #print titles
    #for title in titles:
    #    print title.text
                # save records to the datastore
                #scraperwiki.datastore.save(["title"], record) 


# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_table(soup)
    #next_link = soup.find("li", { "class" : "next" })   
    #if next_link:
    #    next_link = next_link.next
    #    next_url = base_url + next_link['href']
    #    scrape_and_look_for_next_link(next_url)


# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://cases.ivey.uwo.ca/Cases/Pages/home.aspx?Mode=Search&SearchMode=Interest&Search=Environmental/Ecology+Theme&cache=0'
starting_url = base_url
scrape_and_look_for_next_link(starting_url)
