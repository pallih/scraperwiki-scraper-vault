import scraperwiki

from bs4 import BeautifulSoup

html = scraperwiki.scrape("http://www.cetesb.sp.gov.br/Qualidade-da-Praia")
soup = BeautifulSoup(html)

tables = soup.find_all("table", {"width" : "8000"})
print len(tables)

print tables

for table in tables:
    for row in table.find_all('tr'):
        for cell in row.find_all("td"):
            print cell.get_text().strip()


#rows = tables[0].find_all('tr')

for row in rows:
    for cell in row.find_all("td"):
        print cell.get_text().strip()
for row in rows:
    cells = row.find_all("td")
    if len(cells) > 3:
        data = {
            'praia' : cells[0].get_text().strip(),
            'local' : cells[1].get_text().strip(),
            'qualidade' : cells[2].get_text().strip()
            
        }
        scraperwiki.sqlite.save(unique_keys=['praia'],data=data)

import scraperwiki

from bs4 import BeautifulSoup

html = scraperwiki.scrape("http://www.cetesb.sp.gov.br/Qualidade-da-Praia")
soup = BeautifulSoup(html)

tables = soup.find_all("table", {"width" : "8000"})
print len(tables)

print tables

for table in tables:
    for row in table.find_all('tr'):
        for cell in row.find_all("td"):
            print cell.get_text().strip()


#rows = tables[0].find_all('tr')

for row in rows:
    for cell in row.find_all("td"):
        print cell.get_text().strip()
for row in rows:
    cells = row.find_all("td")
    if len(cells) > 3:
        data = {
            'praia' : cells[0].get_text().strip(),
            'local' : cells[1].get_text().strip(),
            'qualidade' : cells[2].get_text().strip()
            
        }
        scraperwiki.sqlite.save(unique_keys=['praia'],data=data)

