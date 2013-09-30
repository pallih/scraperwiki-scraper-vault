import scraperwiki
from bs4 import BeautifulSoup

import string

html = scraperwiki.scrape("http://usatoday30.usatoday.com/money/economy/housing/2009-02-11-decline-housing-foreclosure_N.htm")
soup = BeautifulSoup(html)

tables = soup.find_all("table")
## if your page has tons of tables, you might need to get more specific
## with a find all like: 
## tables = soup.find_all("table", {"border" : "0", "cellspacing": "1", "cellpadding": "2"})

for table in tables:
    rows = table.find_all('tr') 
    for row in rows:
        cells = row.find_all("td")
        for c,cell in enumerate(cells):
            print c, cell.get_text()
        try:
            data = {
                'nutrient'     : cells[0].get_text().strip(), 
                'unit'         : cells[1].get_text().strip(),
                'value_in_100g' : cells[2].get_text().strip(),
                'per_lb'       : cells[3].get_text().strip(),
                'per_3oz' : cells[4].get_text().strip()
            }
            scraperwiki.sqlite.save(unique_keys=['nutrient'],data=data)
        except:
            print "where's the beef"

print "et voila!"

import scraperwiki
from bs4 import BeautifulSoup

import string

html = scraperwiki.scrape("http://usatoday30.usatoday.com/money/economy/housing/2009-02-11-decline-housing-foreclosure_N.htm")
soup = BeautifulSoup(html)

tables = soup.find_all("table")
## if your page has tons of tables, you might need to get more specific
## with a find all like: 
## tables = soup.find_all("table", {"border" : "0", "cellspacing": "1", "cellpadding": "2"})

for table in tables:
    rows = table.find_all('tr') 
    for row in rows:
        cells = row.find_all("td")
        for c,cell in enumerate(cells):
            print c, cell.get_text()
        try:
            data = {
                'nutrient'     : cells[0].get_text().strip(), 
                'unit'         : cells[1].get_text().strip(),
                'value_in_100g' : cells[2].get_text().strip(),
                'per_lb'       : cells[3].get_text().strip(),
                'per_3oz' : cells[4].get_text().strip()
            }
            scraperwiki.sqlite.save(unique_keys=['nutrient'],data=data)
        except:
            print "where's the beef"

print "et voila!"

