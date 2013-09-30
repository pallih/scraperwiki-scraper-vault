import scraperwiki
from BeautifulSoup import BeautifulSoup

html = scraperwiki.scrape('http://www.phila.gov/rfp/')
root = BeautifulSoup(html)

table = root.find('table',{"class" : "tableborderzero"})
uls = table.findAll('ul')

#for ul in uls:
    #records = ul.findAll('li')
records = table.findAll('li')
if records:
    for record in records:
        if record and not record.findParent('ul', {"type": "disc"}) and not record.findParent('ol'):
            print record.text

import scraperwiki
from BeautifulSoup import BeautifulSoup

html = scraperwiki.scrape('http://www.phila.gov/rfp/')
root = BeautifulSoup(html)

table = root.find('table',{"class" : "tableborderzero"})
uls = table.findAll('ul')

#for ul in uls:
    #records = ul.findAll('li')
records = table.findAll('li')
if records:
    for record in records:
        if record and not record.findParent('ul', {"type": "disc"}) and not record.findParent('ol'):
            print record.text

