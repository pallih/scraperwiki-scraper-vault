import scraperwiki

from bs4 import BeautifulSoup

html = scraperwiki.scrape("http://www.census.gov/geo/reference/guidestloc/select_data.html")
soup = BeautifulSoup(html)

print soup.prettify()

print soup.find_all("table")

print len(soup.find_all("table"))

tables = soup.find_all("table", {"border" : "1", "cellspacing": "0", "cellpadding": "3"})
print len(tables)

print tables

for table in tables:
    for row in table.find_all('tr'):
        for cell in row.find_all("td"):
            print cell.get_text().strip()

rows = tables[0].find_all('tr')

for row in rows:
    for cell in row.find_all("td"):
        print cell.get_text().strip()
for row in rows:
    cells = row.find_all("td")
    if len(cells) > 5:
        data = {
            'ansi_code' : cells[0].get_text().strip(),
            'name' : cells[1].get_text().strip(),
            'population' : cells[2].get_text().strip(),
            'housing_units' : cells[3].get_text().strip(),
            'land_area' : cells[4].get_text().strip(),
            'population_density' : cells[5].get_text().strip()
        }
        scraperwiki.sqlite.save(unique_keys=['name'],data=data)
