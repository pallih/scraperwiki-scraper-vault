###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://edinburgh2.com/'
html = scraperwiki.scrape(starting_url)
# print html

from BeautifulSoup import BeautifulSoup
soup = BeautifulSoup(html) # turn our HTML into a BeautifulSoup object
lis = soup.findAll('li') # get all the <li> tags

for li in lis:
    name = link = timing = None
    item = li.findAll("h2")
    if len(item) > 0 and item[0] is not None:
        name = item[0].text
        a = item[0].a
        if a is not None:
            link = a['href']
            
        ps = li.findAll('p')
        for p in ps:
             if p['class'] is 'who':
                continue
             timing = p.text
                
    print name
    print link
    print timing
                   
   
###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://edinburgh2.com/'
html = scraperwiki.scrape(starting_url)
# print html

from BeautifulSoup import BeautifulSoup
soup = BeautifulSoup(html) # turn our HTML into a BeautifulSoup object
lis = soup.findAll('li') # get all the <li> tags

for li in lis:
    name = link = timing = None
    item = li.findAll("h2")
    if len(item) > 0 and item[0] is not None:
        name = item[0].text
        a = item[0].a
        if a is not None:
            link = a['href']
            
        ps = li.findAll('p')
        for p in ps:
             if p['class'] is 'who':
                continue
             timing = p.text
                
    print name
    print link
    print timing
                   
   
