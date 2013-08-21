###############################################################################
# Basic scraper
# You need to run it starting from 07:00 AM GMT+1
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
import re

# retrieve a page
url = 'http://sites.radiofrance.fr/chaines/fip/endirect/'
html = scraperwiki.scrape(url)
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td class="blanc11"> tags
tds = soup.findAll("td", { "class" : "blanc11" } ) 

# our element is second retrieved.. Should use smtg more consistent
td = tds.pop(1)
contents =  td.contents

song={}
# Our data is in these childs
for i in [0, 2, 4]:
    try:
        song['artiste'] = contents[i].contents[0].contents[0].strip()
        song['titre'] = contents[i].contents[1].strip()[2:]
    except:
        try:
            # song[x]=y for x,y in [item for item in contents[i].split(":")]
            tmp = [item.strip() for item in contents[i].split(" : ")]
            song[tmp[0]] = tmp[1]
        except:
            pass
print song

# save records to the datastore
scraperwiki.datastore.save(['titre'], song) 
