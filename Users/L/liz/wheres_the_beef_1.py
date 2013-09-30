import scraperwiki
from bs4 import BeautifulSoup

import string

html = scraperwiki.scrape("http://ndb.nal.usda.gov/ndb/beef/show")
soup = BeautifulSoup(html)

tables = soup.find_all("table")

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

html = scraperwiki.scrape("http://ndb.nal.usda.gov/ndb/beef/show")
soup = BeautifulSoup(html)

tables = soup.find_all("table")

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

