###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://www.ed.ac.uk/schools-departments/estates-buildings/buildings-information/a-z-buildings-list'
html = scraperwiki.scrape(starting_url)
print starting_url
soup = BeautifulSoup(html)

buildings = []
names = 0

# use BeautifulSoup to get all <td> tags
tds = soup.findAll('li') 
for td in tds:
    link = td.find('a')
    if link is not None:
        href=link.attrs[0][1]
        m = re.search('\d+',href)
        if m is None: continue
        id = m.group()
       

        if href.rfind('Building') > -1:
            #print href
            names = names + 1

print names

 
                         
                
    