import scraperwiki
from bs4 import BeautifulSoup

import string

html = scraperwiki.scrape("http://www.usatoday.com/sports/mlb/statistics/")
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
                'AB'     : cells[0].get_text().strip(), 
                'H'         : cells[1].get_text().strip(),
                'R' : cells[2].get_text().strip(),
                'RBI'       : cells[3].get_text().strip(),
                'HR' : cells[4].get_text().strip(),
                '3B' : cells[5].get_text().strip(),
                '2B' : cells[6].get_text().strip(),
                'SB' : cells[7].get_text().strip(),
                'AVG': cells[8].get_text().strip()
        
            }
            scraperwiki.sqlite.save(unique_keys=['nutrient'],data=data)
        except:
            print "MLB stats scraper"

print "et voila!"

