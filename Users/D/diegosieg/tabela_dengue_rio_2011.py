import scraperwiki

from bs4 import BeautifulSoup

html = scraperwiki.scrape("http://200.141.78.79/dlstatic/10112/2352733/DLFE-246744.htm/Dadosdengue0.2.0.5.1.2.MES2.0.1.1..htm")
soup = BeautifulSoup(html)

tables = soup.find_all("table", {"class":"xl689667"}) #"border" : "0", "cellspacing": "0", "cellpadding": "0"
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
    if len(cells) > 14:
        data = {
            'local' : cells[0].get_text().strip(),
            'populacao' : cells[1].get_text().strip(),
            'jan' : cells[2].get_text().strip(),
            'fev' : cells[3].get_text().strip(),
            'mar' : cells[4].get_text().strip(),
            'abr' : cells[5].get_text().strip(),
            'mai' : cells[6].get_text().strip(),
            'jun' : cells[7].get_text().strip(),
            'jul' : cells[8].get_text().strip(),
            'ago' : cells[9].get_text().strip(),
            'set' : cells[10].get_text().strip(),
            'out' : cells[11].get_text().strip(),
            'nov' : cells[12].get_text().strip(),
            'dez' : cells[13].get_text().strip(),
            'total' : cells[14].get_text().strip()
        }
        scraperwiki.sqlite.save(unique_keys=['local'],data=data)

