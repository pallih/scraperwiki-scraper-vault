# Title:   Assoc of Drainage Authorities members
# Data Source: Internal Drainage Boards: http://www.ada.org.uk/listmembers.php?type=idbs&area=all
# Data Source: Regional Flood Defence Committees http://www.ada.org.uk/listmembers.php?type=rfdcs&area=all

import scraperwiki
from BeautifulSoup import BeautifulSoup

# 1. do IDBs:
html = scraperwiki.scrape('http://www.ada.org.uk/listmembers.php?type=idbs&area=all')

soup = BeautifulSoup(html) # turn our HTML into a BeautifulSoup object
tds = soup.findAll('td') # get all the <td> tags

for td in tds:
    print td # the full HTML tag
    print td.text # just the text inside the HTML tag

