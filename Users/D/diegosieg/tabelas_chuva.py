import scraperwiki

from bs4 import BeautifulSoup

html = scraperwiki.scrape("http://www.cgesp.org/v3/alagamentos.jsp?dataBusca=12%2F11%2F2012&enviaBusca=Buscar")
soup = BeautifulSoup(html)



print len(soup.find_all("table"))

tables = soup.find_all("table")
print len(tables)


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
    if len(cells) > 1:
        data = {
            'ansi_code' : cells[0].get_text().strip(),
            'name' : cells[1].get_text().strip()
        }
        scraperwiki.sqlite.save(unique_keys=['name'],data=data)
